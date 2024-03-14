import datetime
from datetime import date
from datetime import timedelta

from fastapi.openapi.models import MediaType
from sqlalchemy import select, and_

from app.db import asmi_async_session_maker, tm_async_session_maker
from app.news.models import News, Embs
from app.agencies.models import Agencies
from app.dao.base import BaseDao


# DAO - Data Access Object
class NewsDao(BaseDao):
    model = News

    @staticmethod
    async def get_allowed_news_by_date(start: date, end: date):
        async with asmi_async_session_maker() as session:
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
    async def get_media_types_news(media_type: str):
        async with asmi_async_session_maker() as session:
            query = (
                select(News.__table__.columns, Agencies.telegram)
                .join(News, Agencies.telegram == News.agency)
                .where(News.date >= date.today())
                .filter(
                    Agencies.media_type == media_type and Agencies.media_type == 'Non-political' and Agencies.media_type == 'Neutral')
            )
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_news_by_date(start: date, end: date, **filter_by):
        async with asmi_async_session_maker() as session:
            query = select(News.__table__.columns).where(
                and_(start < News.date, News.date < end)
            ).filter_by(**filter_by).order_by(News.date.desc())
            result = await session.execute(query)
            return result.mappings().all()

    # start: date, end: date, ** filter_by
    # .where(and_(start < News.date, News.date < end))
    # .filter_by(**filter_by)
    # .order_by(News.date.desc())


    @staticmethod
    async def get_embs_news(start: date, end: date, **filter_by):
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).where(
                and_(start < News.date, News.date < end)
            ).filter_by(**filter_by).order_by(News.date.desc()).join(News, Embs.news_url == News.url)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_similar_news(embedding: list[float]):
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).join(News, Embs.news_url == News.url).order_by(
                Embs.embedding.l2_distance(embedding)).limit(100)
            result = await session.execute(query)
            return result.mappings().all()

    # @staticmethod
    # async def get_similar_news(embedding: list[float], start_date: date, end_date: date, news_amount: int,
    #                            category: str):
    #     async with tm_async_session_maker() as session:
    #         query = select(News.__table__.columns, Embs.embedding).join(News, Embs.news_url == News.url).where(
    #             and_(start_date <= News.date, News.date <= end_date)).filter(News.category == category).order_by(
    #             Embs.embedding.l2_distance(embedding)).limit(news_amount)
    #         result = await session.execute(query)
    #         return result.mappings().all()

    # @classmethod
    # async def find_all(cls, **filter_by):
    #     async with async_session_maker() as session:
    #         query = select(cls.model.__table__.columns).filter_by(**filter_by)
    #         result = await session.execute(query)
    #         return result.mappings().all()
