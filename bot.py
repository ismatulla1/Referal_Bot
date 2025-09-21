import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update

from config import BOT_TOKEN
from handlers.start import start_router
from handlers.admin import admin_router
from database import init_db

logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(admin_router)

# Webhook sozlamalari
WEBHOOK_PATH = "/webhook"
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL", "https://referal-bot.onrender.com")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

PORT = int(os.getenv("PORT", 8080))


# === Webhook funksiyalari ===
async def on_startup(app: web.Application):
    await init_db()
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Webhook o‘rnatildi: {WEBHOOK_URL}")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    logging.info("❌ Webhook o‘chirildi")

async def handle(request: web.Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response()

def run_webhook():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host="0.0.0.0", port=PORT)


# === Polling (local) funksiyasi ===
async def run_polling():
    await init_db()
    logging.info("🚀 Polling rejimida ishga tushdi (local) ...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    # LOCAL yoki SERVER rejim tanlash
    if os.getenv("MODE", "LOCAL") == "WEBHOOK":
        run_webhook()
    else:
        asyncio.run(run_polling())
