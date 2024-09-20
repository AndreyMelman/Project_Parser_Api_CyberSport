import logging

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import News




async def save_data_in_db(
    session: AsyncSession,
    news_dict: dict[str, dict[str, str]],
) -> None:
    try:
        for id_news, values in news_dict.items():
            stmt = insert(News).values(
                id_news=id_news,
                title=values["article_title"],
                created_at=values["article_date_time"],
                url=values["article_url"],
                img_url=values["article_img"],
                category=values["article_category"],
            )
            stmt = stmt.on_conflict_do_nothing(index_elements=["id_news"])
            await session.execute(stmt)
        await session.commit()
    except Exception as e:
        logging.error(f"Error save data in PostgreSQL: {e}")


async def save_unread_news(
    session: AsyncSession,
):
    try:
        stmt = (
            select(News)
            .where(News.sent_to_telegram == False)
            .order_by(News.created_at.desc())
        )
        result = await session.execute(stmt)
        news = result.scalars().all()

        return news

    except Exception as e:
        logging.error(f"Error get unread news: {e}")


async def mark_news_as_sent(
    session: AsyncSession,
    list_id: list,
):
    list_id = tuple(list_id)
    try:
        stmt = (
            update(News)
            .where(News.id_news.in_(list_id))
            .values(sent_to_telegram=True)
        )
        await session.execute(stmt)
        await session.commit()

    except Exception as e:
        logging.error(f"Error updating news status: {e}")
