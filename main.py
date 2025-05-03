import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖼 Генерация логотипа", callback_data="logo")],
        [InlineKeyboardButton("✍️ Написать текст", callback_data="text")],
        [InlineKeyboardButton("💻 Написать скрипт", callback_data="script")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери действие:", reply_markup=reply_markup)

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data
    await query.edit_message_text(f"🔄 Выполняю задачу: {action}...")

    # Простейшая имитация запроса (можно заменить на реальные вызовы агентов)
    result = f"✅ {action.capitalize()} выполнено успешно!"
    await bot.send_message(chat_id=query.message.chat_id, text=result)

# FastAPI route (тест)
@app.get("/")
async def root():
    return {"status": "ok"}

# Инициализация Telegram-бота
def start_bot():
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CallbackQueryHandler(handle_action))
    app_telegram.run_polling()

import threading
threading.Thread(target=start_bot).start()
