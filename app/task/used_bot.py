import logging

from aiogram.utils.markdown import hbold
from aiogram.types import LinkPreviewOptions

from core import crud
from core.config import settings
from app.bot.telegram_bot import bot
from core.models import db_helper
from core.crud import mark_news_as_sent
from bot.telegram_bot import start_bot


async def tg_bot():
    await start_bot()


async def send_news_to_telegram(
    unread_news,
) -> None:
    list_id = []
    for news in unread_news:
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
            logging.info(f'333   Session is opened.   3')
            await mark_news_as_sent(session, list_id)
            logging.info(f'333    Session is still open.    333')
    logging.info(f'333    Session is closed.    333')
    

async def send_news():
    try:
        async with db_helper.session_factory() as session:
            if session:
                logging.info(f'222   Session is opened.   222')
                unread_news = await crud.save_unread_news(session)
                logging.info(f'222    Session is still open.    222')
        logging.info(f'222    Session is closed.    222')

        if unread_news:
            await send_news_to_telegram(unread_news)
        else:
            logging.info(f'Новых новостей в базе нет')
    except Exception as error:
        logging.error(f"Ошибка в процессе парсинга и отправки новостей: {error}")

