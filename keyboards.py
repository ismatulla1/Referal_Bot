# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_USERNAME


# User panel tugmalari
def user_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="👥 Mening referallarim soni")
            ],
            [
                KeyboardButton(text="🔒 Yopiq guruh linki"),
                KeyboardButton(text="📞 Admin bilan bog‘lanish")
            ]
        ],
        resize_keyboard=True
    )

# Admin panel tugmalari
def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("📊 Statistika")],
            [KeyboardButton("➕ Foydalanuvchi qo‘shish")],
        ],
        resize_keyboard=True
    )

# Kanalga obuna bo‘lish tekshiruvi uchun inline
def subscription_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga qo‘shilish",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ A’zo bo‘ldim",
                    callback_data="check_subscription"
                )
            ]
        ]
    )
