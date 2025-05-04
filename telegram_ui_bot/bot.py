# telegram_ui_bot/bot.py

from aiogram import Bot, Dispatcher, executor, types
from shared.config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Привет! Я бот, который будет присылать тебе свежие заказы и автоотклики.")

@dp.message_handler(commands=["id"])
async def get_id(msg: types.Message):
    await msg.reply(f"Твой chat_id: {msg.chat.id}")

if __name__ == "__main__":
    executor.start_polling(dp)
