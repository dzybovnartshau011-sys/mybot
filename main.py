import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = "8401655753:AAGg48JUxzvaH3SaDQn1UN0pVxs9-pnsQm0"
ADMIN_ID = 2137782503 

bot = Bot(token=TOKEN)
dp = Dispatcher()
active_chats = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🤖 Бот запущен и готов к работе.")
    else:
        await message.answer("👋 Привет! Напиши свой вопрос, и я передам его автору.")

@dp.message(F.chat.type == "private", ~F.from_user.id == ADMIN_ID)
async def to_admin(message: types.Message):
    msg = await message.forward(chat_id=ADMIN_ID)
    active_chats[msg.message_id] = message.from_user.id
    await message.answer("✅ Отправлено. Ожидайте ответа.")

@dp.message(F.from_user.id == ADMIN_ID, F.reply_to_message)
async def from_admin(message: types.Message):
    orig_msg_id = message.reply_to_message.message_id
    if orig_msg_id in active_chats:
        user_id = active_chats[orig_msg_id]
        try:
            await bot.send_message(user_id, f"<b>Ответ:</b>\n\n{message.text}", parse_mode="HTML")
            await message.answer("📨 Отправлено.")
        except:
            await message.answer("❌ Ошибка отправки.")
    else:
        await message.answer("⚠️ Нажми 'Reply' на сообщение пользователя.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
