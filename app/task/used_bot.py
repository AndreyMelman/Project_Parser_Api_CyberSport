from typing import AsyncGenerator

from aiogram.utils.markdown import hbold
from aiogram.types import LinkPreviewOptions
from requests import session

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from app.bot.telegram_bot import bot
from core.models import db_helper
from .collector import get_unread_news
from core.crud import mark_news_as_sent
from bot.telegram_bot import start_bot


async def tg_bot():
    await start_bot()


async def send_news_to_telegram(
    new_news,
) -> None:
    list_id = []
    for news in new_news:
        options = LinkPreviewOptions(url=news.url, prefer_small_media=True)
        message = f"⚡️{hbold(news.title)}\n\n" f"💬{news.category}\n\n"
        await bot.send_message(
            settings.token.id.get_secret_value(),
            text=message,
            link_preview_options=options,
        )
        list_id.append(news.id_news)

    async with db_helper.session_factory() as session:
        if session:
            await mark_news_as_sent(session, list_id)


async def send_news():
    unread_news = await get_unread_news()
    if unread_news:
        await send_news_to_telegram(unread_news)

