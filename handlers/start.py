# handlers/start.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from config import CHANNEL_ID, ADMIN_USERNAME, PRIVATE_GROUP_LINK, REQUIRED_REFERRALS
from database import (
    add_user, add_referral, get_referrals_count,
    has_received_group_link, mark_group_link_sent,
    get_top_referrers, user_exists, increment_referrals, get_inviter_id
)
from keyboards import user_menu, subscription_keyboard
from utils import generate_ref_link

start_router = Router()

# Inline "A’zo bo‘ldim" tugmasi handler
@start_router.callback_query(lambda c: c.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Agar allaqachon guruh linki berilgan bo'lsa
    if await has_received_group_link(user_id):
        await callback.answer("Siz allaqachon kanalga qo‘shildingiz ✅", show_alert=True)
        return

    # Kanal a’zoligini tekshirish
    try:
        member = await callback.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            await callback.answer("❌ Hali kanalga qo‘shilmadingiz!", show_alert=True)
            return
    except Exception:
        await callback.answer("❌ Kanal a'zolarini tekshirish mumkin emas!", show_alert=True)
        return

    # Foydalanuvchiga guruh linkini belgilash
    await mark_group_link_sent(user_id)
    await callback.answer("A’zo bo‘ldingiz! ✅", show_alert=True)
    await callback.message.edit_reply_markup(reply_markup=None)

    # Inviter_id ni olish va referral hisoblash
    inviter_id = await get_inviter_id(user_id)
    if inviter_id:
        added = await add_referral(inviter_id, user_id)
        if added:
            await increment_referrals(inviter_id)
            ref_count = await get_referrals_count(inviter_id)
            try:
                await callback.bot.send_message(
                    inviter_id,
                    f"✅ Siz yangi foydalanuvchini taklif qildingiz!\n"
                    f"Jami takliflaringiz: {ref_count}"
                )
                if ref_count == REQUIRED_REFERRALS:
                    await callback.bot.send_message(
                        inviter_id,
                        f"🎉 Tabriklaymiz! Siz {REQUIRED_REFERRALS} ta odam taklif qildingiz.\n"
                        f"Mana yopiq guruh linki: {PRIVATE_GROUP_LINK}"
                    )
                    await mark_group_link_sent(inviter_id)
            except:
                pass


# /start komandasi
@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    args = message.text.split()
    user = message.from_user

    invited_by = None
    if len(args) > 1:
        try:
            invited_by = int(args[1])
        except ValueError:
            invited_by = None

    # Foydalanuvchini bazaga qo‘shish
    if not await user_exists(user.id):
        await add_user(user.id, user.username, invited_by)

    # Bot username va referral link yaratish
    bot_username = (await message.bot.get_me()).username
    ref_link = generate_ref_link(bot_username, user.id)

    # Kanal a’zoligini tekshirish
    try:
        member = await message.bot.get_chat_member(CHANNEL_ID, user.id)
        if member.status not in ["member", "administrator", "creator"]:
            # Kanalga a’zo bo‘lmagan foydalanuvchi uchun inline tugma
            await message.answer(
                "✅ Obuna bo'ldingiz do'stlaringizni taklif qilishni boshlang! /start bosing",
                reply_markup=subscription_keyboard()
            )
            return
    except Exception:
        await message.answer(
            "❌ Kanal a'zolarini tekshirish mumkin emas! Iltimos kanalga qo‘shiling.",
            reply_markup=subscription_keyboard()
        )
        return

    # Agar foydalanuvchi kanalga obuna bo‘lsa, referral hisoblash
    if invited_by and invited_by != user.id:
        added = await add_referral(invited_by, user.id)
        if added:
            await increment_referrals(invited_by)
            ref_count = await get_referrals_count(invited_by)
            try:
                await message.bot.send_message(
                    invited_by,
                    f"✅ Siz yangi foydalanuvchini taklif qildingiz!\n"
                    f"Jami takliflaringiz: {ref_count}"
                )
                if ref_count == REQUIRED_REFERRALS:
                    await message.bot.send_message(
                        invited_by,
                        f"🎉 Tabriklaymiz! Siz {REQUIRED_REFERRALS} ta odam taklif qildingiz.\n"
                        f"Mana yopiq guruh linki: {PRIVATE_GROUP_LINK}"
                    )
                    await mark_group_link_sent(invited_by)
            except:
                pass

    # Foydalanuvchiga referal link va menyu ko‘rsatish
    await message.answer(
        f"Salom {user.first_name}! 👋\n\n"
        f"✅ Sizning referal linkingiz:\n{ref_link}\n\n"
        "Quyidagi menyudan foydalaning 👇",
        reply_markup=user_menu()
    )


# User tugmalari ishlovchi handler
@start_router.message()
async def user_buttons(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text == "👥 Mening referallarim soni":
        count = await get_referrals_count(user_id)
        await message.answer(f"👥 Siz {count} ta odamni taklif qildingiz.")

    elif text == "🔒 Yopiq guruh linki":
        count = await get_referrals_count(user_id)
        if count >= REQUIRED_REFERRALS:
            if not await has_received_group_link(user_id):
                await mark_group_link_sent(user_id)
            await message.answer(f"🔗 Sizning guruh linkingiz: {PRIVATE_GROUP_LINK}")
        else:
            await message.answer(
                f"❌ Guruh linkini olish uchun yana {REQUIRED_REFERRALS - count} ta odam taklif qilishingiz kerak."
            )

    elif text == "📊 Statistika":
        leaders = await get_top_referrers()
        if not leaders:
            await message.answer("Hali hech kim referral qo‘shmagan.")
        else:
            text = "🏆 Top referallar:\n\n"
            for i, (uid, cnt) in enumerate(leaders, start=1):
                text += f"{i}. 👤 {uid} — {cnt} ta\n"
            await message.answer(text)

    elif text == "📞 Admin bilan bog‘lanish":
        await message.answer(f"👨‍💻 Admin: {ADMIN_USERNAME}")
