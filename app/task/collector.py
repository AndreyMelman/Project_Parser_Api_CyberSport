import asyncio
import logging

from core.models import db_helper
from parser.news import parser as p
from core import crud


async def collector():
    while True:
        await save_news_in_db()
        await asyncio.sleep(60*10)


# Функция парсера новостей
async def parse_news():
    parser = await p.load_articles()
    return parser


# Функция сохранения новых новостей в базу данных
async def save_news_in_db():
    try:
        parser = await parse_news()
        async with db_helper.session_factory() as session:
            if session:
                logging.info(f'Session save news in db is opened.')
                await crud.save_data_in_db(session, parser)

        logging.info(f'111    Session is closed.')
    except Exception as error:
        logging.error(f"Ошибка в процессе парсинга и отправки новостей: {error}")

