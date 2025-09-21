import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers.start import start_router
from handlers.admin import admin_router
from database import init_db   # 🔑 DB initialize qilish uchun import

async def main():
    # Avval DB yaratib olamiz
    await init_db()

    # Bot yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(start_router)
    dp.include_router(admin_router)

    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
