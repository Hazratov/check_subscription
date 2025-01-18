import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
import os

API_TOKEN = ""
CHANNEL_USERNAME = "@texna_uzb"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Obuna tekshirish uchun helper funksiya
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        return False

# Start komandasi uchun handler
@dp.message_handler(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer(
            "🎉 Salom, texnologiya ixlosmandi! Siz kanalimizga obuna bo‘lgansiz va botimizdan foydalanishni boshlashingiz mumkin."
        )
    else:
        # Kanalga obuna bo'lish uchun tugma
        subscribe_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📲 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Obunani tekshirish", callback_data="check_subscription"
                    )
                ],
            ]
        )
        await message.answer(
            "👋 Assalomu alaykum! Agar texnologiya haqida ko'proq bilim va yangiliklar o'rganmoqchi bo'lsangiz, "
            f"{CHANNEL_USERNAME} kanaliga obuna bo‘ling va zamonaviy hayot ritmini birga kuzating!\n\n"
            "⬇️ Pastdagi tugmani bosib, kanalga obuna bo‘ling.",
            reply_markup=subscribe_button,
        )

# Obuna holatini tekshirish uchun callback
@dp.callback_query_handler(lambda c: c.data == "check_subscription")
async def check_subscription_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await callback_query.message.edit_text(
            "🎉 Ajoyib! Siz kanalimizga obuna bo‘lgansiz. Endi botdan foydalanishni davom ettirishingiz mumkin!"
        )
    else:
        await callback_query.answer("⛔ Siz hali kanalga obuna bo‘lmadingiz!", show_alert=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
