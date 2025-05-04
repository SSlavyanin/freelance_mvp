# backend/main.py

from fastapi import FastAPI, Request
import asyncio
from backend.scheduler import poll_parser
from shared.config import TELEGRAM_USERNAME
import httpx

app = FastAPI()

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(poll_parser())

@app.post("/receive_order")
async def receive_order(order: dict):
    """
    Получение заказа от парсера. Генерация отклика и пересылка в Telegram.
    """
    title = order.get("title", "Без названия")
    link = order.get("link", "#")

    reply = f"🧠 Автоотклик:\nЗдравствуйте! Заинтересован в этом заказе: {title}\n" \
            f"Свяжитесь со мной в Telegram: {TELEGRAM_USERNAME}"

    # Отправляем пользователю в Telegram
    await notify_user(title, link, reply)
    return {"status": "ok"}

async def notify_user(title, link, reply_text):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": "<user_chat_id>",  # позже заменить на динамическое
                    "text": f"📌 Новый заказ: {title}\n🔗 {link}\n\n{reply_text}"
                }
            )
    except Exception as e:
        print("Ошибка при отправке в Telegram:", e)
