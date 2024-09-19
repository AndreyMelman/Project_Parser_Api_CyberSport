import asyncio
from .used_bot import send_news_to_telegram


# Функция запускает отправку новостей в телеграм бот каждые 2 часа
async def spammer():
    while True:
        await send_news_to_telegram()
        await asyncio.sleep(120)