from fastapi import FastAPI, Request
import asyncio
from backend.scheduler import poll_parser
from shared.config import TELEGRAM_USERNAME, TELEGRAM_BOT_TOKEN
from backend.agent_client import get_reply_from_agent
import httpx

app = FastAPI()

AGENT_URL = "https://code-agent-qi30.onrender.com/handle_order"  # адрес микросервиса code_agent

@app.get("/")
def root():
    return {"status": "OK"}


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(poll_parser())


@app.post("/receive_order")
async def receive_order(order: dict):
    """
    Получение заказа от парсера. Генерация отклика и пересылка в Telegram.
    """
    title = order.get("title", "Без названия")
    desc = order.get("desc", "")
    link = order.get("link", "#")
    contact = order.get("contact", None)

    # 🔹 Генерация отклика через AI-агента
    reply = await get_reply_from_agent(title, desc)

    # 🔹 Добавляем ссылку на Telegram
    reply = await get_reply_from_agent(title, order.get("desc", ""))

    # 🔹 Отправка в Telegram
    await notify_user(title, link, contact, reply)
    return {"status": "ok"}


async def notify_user(title, link, contact, reply_text):
    try:
        contact_text = f"\n👤 Контакт: {contact}" if contact else ""
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": "<user_chat_id>",  # TODO: заменить на динамический ID
                    "text": f"📌 Новый заказ: {title}\n🔗 {link}{contact_text}\n\n🧠 Автоответ:\n{reply_text}"
                }
            )
    except Exception as e:
        print("Ошибка при отправке в Telegram:", e)


async def get_reply_from_agent(title: str, desc: str) -> str:
    """
    Отправка запроса агенту и получение сгенерированного отклика.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(AGENT_URL, json={"title": title, "desc": desc})
            response.raise_for_status()
            return response.json().get("reply", "🤖 Автоответ не сгенерирован.")
    except Exception as e:
        print("Agent error:", e)
        return "⚠️ Ошибка генерации автоответа."
