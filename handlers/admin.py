# handlers/admin.py
from aiogram import Router, types
from aiogram.filters import Command
from config import ADMINS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_router = Router()

# Admin tekshirish
def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

# Admin menyu
def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📊 Top referallar", callback_data="top_referrers")],
        [InlineKeyboardButton("🔍 User statistikasi", callback_data="user_stats")],
        [InlineKeyboardButton("➕ Foydalanuvchi qo‘shish", callback_data="add_user")],
    ])

# /admin komandasi
@admin_router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    print("ADMIN CMD KIRDI:", message.from_user.id)  # Debug uchun
    if is_admin(message.from_user.id):
        await message.answer("👑 Admin panelga xush kelibsiz!", reply_markup=admin_menu())
    else:
        await message.answer("❌ Siz admin emassiz!")

# Inline tugmalar
@admin_router.callback_query()
async def inline_admin(callback: types.CallbackQuery):
    print("CALLBACK KIRDI:", callback.data, callback.from_user.id)  # Debug
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    if callback.data == "top_referrers":
        await callback.message.answer("📊 Top referallar (statistika joyi)")
    elif callback.data == "user_stats":
        await callback.message.answer("🔍 User statistikasi (raqamli ID kiriting)")
    elif callback.data == "add_user":
        await callback.message.answer("➕ Foydalanuvchi qo‘shish (hali yozilmagan)")
    await callback.answer()
