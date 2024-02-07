from datetime import date

from sqlalchemy import select, and_

from app.db import async_session_maker
from app.news.models import News
from app.dao.base import BaseDao
from app.news.schemas import SShortNews


# DAO - Data Access Object
class NewsDao(BaseDao):
    model = News


async def get_news_by_date(start: date, end: date) -> list[SShortNews]:
    async with async_session_maker() as session:
        query = select(News.__table__.columns).where(
            and_(start < News.date, News.date < end)
        )
        result = await session.execute(query)
        return result.mappings().all()