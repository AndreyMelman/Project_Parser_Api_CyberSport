from typing import AsyncGenerator

from aiogram.utils.markdown import hbold
from aiogram.types import LinkPreviewOptions
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from app.bot.telegram_bot import bot
from core.models import db_helper
from .collector import save_unread_news
from core.crud import mark_news_as_sent
from bot.telegram_bot import start_bot

async def tg_bot():
    await start_bot()


async def send_news_to_telegram(sess: AsyncGenerator[AsyncSession, None] = db_helper.session_getter()) -> None:
    mark_news = await save_unread_news()
    list_id = []
    for news in mark_news:
        options = LinkPreviewOptions(url=news.url, prefer_small_media=True)
        message = f"⚡️{hbold(news.title)}\n\n" f"💬{news.category}\n\n"
        await bot.send_message(
            settings.token.id.get_secret_value(),
            text=message,
            link_preview_options=options,
        )
        list_id.append(news.id_news)

    async for sess in sess:
        await mark_news_as_sent(sess, list_id)
