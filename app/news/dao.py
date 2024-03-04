from datetime import date
from sqlalchemy import select, and_

from app.db import async_session_maker
from app.news.models import News
from app.agencies.models import Agencies
from app.dao.base import BaseDao


# DAO - Data Access Object
class NewsDao(BaseDao):
    model = News

    @staticmethod
    async def get_allowed_news_by_date(start: date, end: date):
        async with async_session_maker() as session:
            query = (
                select(News.__table__.columns, Agencies.telegram)
                .join(News, Agencies.telegram == News.agency)
                .filter(Agencies.is_forbidden == False)
                .where(
                    and_(start < News.date, News.date < end)
                )
            )
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_news_by_date(start: date, end: date, **filter_by):
        async with async_session_maker() as session:
            query = select(News.__table__.columns).where(
                and_(start < News.date, News.date < end)
            ).filter_by(**filter_by).order_by(News.date.desc())
            result = await session.execute(query)
            return result.mappings().all()


    # @classmethod
    # async def find_all(cls, **filter_by):
    #     async with async_session_maker() as session:
    #         query = select(cls.model.__table__.columns).filter_by(**filter_by)
    #         result = await session.execute(query)
    #         return result.mappings().all()
