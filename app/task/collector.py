import asyncio
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
async def save_news_in_db(
    session: AsyncGenerator[AsyncSession, None] = db_helper.session_getter(),
):
    parser = await parse_news()

    async for session in session:
        await crud.save_data_in_db(session, parser)


# Функция получения не прочитанных новостей из базы данных
async def save_unread_news(
    session: AsyncGenerator[AsyncSession, None] = db_helper.session_getter()
):
    async for session in session:
        res = await crud.get_unread_news(session)
        return res


async def mark_news(
    session: AsyncGenerator[AsyncSession, None] = db_helper.session_getter()
):
    async for session in session:
        res = await crud.mark_news_as_sent(session)

