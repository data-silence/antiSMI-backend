import datetime as dt
from datetime import date

from sqlalchemy import select, and_, distinct, func, cast, Date

from app.db import asmi_async_session_maker, tm_async_session_maker
from app.news.models import News, Embs
from app.agencies.models import Agencies
from app.dao.base import BaseDao


"""DAO - Data Access Object"""

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
                    Agencies.media_type == media_type or
                    Agencies.media_type == 'Non-political' or
                    Agencies.media_type == 'Neutral'
                )
            )
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_tody_news():
        if dt.datetime.now().hour < 10:
            today = date.today() - dt.timedelta(days=1)
        else:
            today = date.today()
        async with asmi_async_session_maker() as session:
            query = (
                select(News.__table__.columns, Agencies.media_type)
                .where(News.date >= today).join(News, Agencies.telegram == News.agency)
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
            ).filter_by(**filter_by).join(News, Embs.news_url == News.url).order_by(News.date.desc())
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_similar_news(embedding: list[float]):
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).join(News, Embs.news_url == News.url).order_by(
                Embs.embedding.l2_distance(embedding)).limit(100)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def find_similar_news(embedding: list[float], start_date: date, end_date: date, **filter_by):
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).where(
                and_(start_date < News.date, News.date < end_date)
            ).filter_by(**filter_by).join(News, Embs.news_url == News.url).order_by(
                Embs.embedding.l2_distance(embedding)).limit(100)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_news_and_categories(embedding: list[float], start_date: date, end_date: date, news_amount: int,
                                      category: str):
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).join(News, Embs.news_url == News.url).where(
                and_(start_date <= News.date, News.date <= end_date)).filter(News.category == category).order_by(
                Embs.embedding.l2_distance(embedding)).limit(news_amount)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_agencies_amount():
        async with tm_async_session_maker() as session:
            query = func.count(distinct(News.agency))
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_categories_amount():
        async with tm_async_session_maker() as session:
            query = func.count(distinct(News.category))
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_news_amount():
        async with tm_async_session_maker() as session:
            query = func.count(News.news)
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_borderline_date(value: str):
        async with tm_async_session_maker() as session:
            match value:
                case 'min':
                    query = func.min(News.date)
                case 'max':
                    query = func.max(News.date)
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_max_date():
        async with tm_async_session_maker() as session:
            query = func.max(News.date)
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_min_date():
        async with tm_async_session_maker() as session:
            query = func.min(News.date)
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_distinct_dates():
        async with tm_async_session_maker() as session:
            query = select(cast(News.date, Date), func.count(cast(News.date, Date))).group_by(
                cast(News.date, Date)).order_by(cast(News.date, Date))
            result = await session.execute(query)
            return result.mappings().all()
