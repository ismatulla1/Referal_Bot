# handlers/admin.py
from aiogram import Router, types
from aiogram.filters import Command
from config import ADMINS
from keyboards import admin_menu
from database import get_top_referrers

admin_router = Router()

# faqat adminlar uchun
def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@admin_router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("👑 Admin panelga xush kelibsiz!", reply_markup=admin_menu())

@admin_router.message()
async def admin_buttons(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    text = message.text

    if text == "📊 Statistika":
        leaders = await get_top_referrers(20)
        if not leaders:
            await message.answer("Statistika bo‘sh.")
        else:
            txt = "📊 Eng ko‘p taklif qilganlar:\n\n"
            for i, (uid, cnt) in enumerate(leaders, start=1):
                txt += f"{i}. 👤 {uid} — {cnt} ta\n"
            await message.answer(txt)

    elif text == "➕ Foydalanuvchi qo‘shish":
        await message.answer("🔧 Bu funksiya hali yozilmagan.")
