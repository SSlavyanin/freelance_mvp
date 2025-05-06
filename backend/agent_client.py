import httpx

AGENT_URL = "https://code-agent-qi30.onrender.com/handle_order"  # адрес микросервиса code_agent

async def get_reply_from_agent(title: str, description: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(AGENT_URL, json={
                "title": title,
                "description": description
            })
            if response.status_code == 200:
                return response.json().get("reply", "Не удалось сгенерировать ответ.")
            else:
                return f"[Ошибка агента: {response.status_code}]"
    except Exception as e:
        return f"[Ошибка при обращении к агенту: {e}]"
