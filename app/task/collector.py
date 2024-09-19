import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from parser.news import parser as p
from core import crud


async def collector():
    while True:
        await parse_news()
        await asyncio.sleep(60)


async def parse_news(
    session: AsyncGenerator[AsyncSession, None] = db_helper.session_getter()
):
    parser = await p.load_articles()

    async for session in session:
        await crud.save_data_in_db(session, parser)
