from datetime import date

from sqlalchemy import select

from app.db import async_session_maker
from app.news.models import News
from app.dao.base import BaseDao


# DAO - Data Access Object
class NewsDao(BaseDao):
    model = News


async def get_news_by_date(my_date: date):
    async with async_session_maker() as session:
        query = select(News.__table__.columns).filter(News.date > my_date).limit(5)
        result = await session.execute(query)
        return result.mappings().all()