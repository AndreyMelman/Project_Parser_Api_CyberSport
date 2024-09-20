import asyncio
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from parser.news import parser as p
from core import crud


async def collector():
    while True:
        await save_news_in_db()
        await asyncio.sleep(60)


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
                await crud.save_data_in_db(session, parser)
                logging.info(f'Успешное подключение к базе данных')

    except Exception as error:
        logging.error(f"Ошибка в процессе парсинга и отправки новостей: {error}")


# Функция получения не прочитанных новостей из базы данных
async def get_unread_news():
    try:
        async with db_helper.session_factory() as session:
            if session:
                unread_news = await crud.save_unread_news(session)
                return unread_news

    except Exception as error:
        logging.error(f"Ошибка в процессе парсинга и отправки новостей: {error}")
