# backend/scheduler.py

import asyncio
import httpx
from shared.config import PARSER_URL, PARSE_INTERVAL_SECONDS

async def poll_parser():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                print("Запрос на парсинг...")
                resp = await client.get(PARSER_URL)
                if resp.status_code == 200:
                    print("Полуbackend/scheduler.pyчены заказы:", resp.json())
                else:
                    print("Ошибка парсера:", resp.status_code)
        except Exception as e:
            print("Ошибка при запросе к парсеру:", e)

        await asyncio.sleep(PARSE_INTERVAL_SECONDS)
