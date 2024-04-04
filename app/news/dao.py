import datetime as dt
from datetime import date

from sqlalchemy import select, and_, distinct, func, cast, Date

from app.db import asmi_async_session_maker, tm_async_session_maker
from app.news.models import News, Embs
from app.agencies.models import Agencies
from app.dao.base import BaseDao


class NewsDao(BaseDao):
    """News DAO - Data Access Object to News"""
    model = News

    @staticmethod
    async def get_allowed_news_by_date(start: date, end: date):
        """Picks out not forbidden today news"""
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
        """
        Get news by media type.
        News from non-political and neutral sources are added to all news of the transmitted type
        """
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
    async def get_today_news():
        """
        Picks up all today news. If the request is made before 10 am, then today's news stream has not been formed yet
        -> take yesterday's news stream
        """
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
        """Picks up news between two daytime values using filter"""
        async with asmi_async_session_maker() as session:
            query = select(News.__table__.columns).where(
                and_(start < News.date, News.date < end)
            ).filter_by(**filter_by).order_by(News.date.desc())
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_embs_news(start: date, end: date, **filter_by):
        """The same as previous get_news_by_date, but additionally returns news embedding"""
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).where(
                and_(start < News.date, News.date < end)
            ).filter_by(**filter_by).join(News, Embs.news_url == News.url).order_by(News.date.desc())
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_similar_news(embedding: list[float]):
        """Returns the news that is closest to the embedding that was transferred"""
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).join(News, Embs.news_url == News.url).order_by(
                Embs.embedding.l2_distance(embedding)).limit(100)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def find_similar_news(embedding: list[float], start_date: date, end_date: date, **filter_by):
        """The same as previous get_similar_news, but additionally uses filters"""
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).where(
                and_(start_date < News.date, News.date < end_date)
            ).filter_by(**filter_by).join(News, Embs.news_url == News.url).order_by(
                Embs.embedding.l2_distance(embedding)).limit(100)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_news_by_categories(embedding: list[float], start_date: date, end_date: date, news_amount: int,
                                     category: str):
        """Fetch news by categories using date and other filters"""
        async with tm_async_session_maker() as session:
            query = select(News.__table__.columns, Embs.embedding).join(News, Embs.news_url == News.url).where(
                and_(start_date <= News.date, News.date <= end_date)).filter(News.category == category).order_by(
                Embs.embedding.l2_distance(embedding)).limit(news_amount)
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_agencies_amount():
        """Fetching the current number of news agencies"""
        async with tm_async_session_maker() as session:
            query = func.count(distinct(News.agency))
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_categories_amount():
        """Fetching the current number of news categories in service"""
        async with tm_async_session_maker() as session:
            query = func.count(distinct(News.category))
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_news_amount():
        """Fetching the current number of news"""
        async with tm_async_session_maker() as session:
            query = func.count(News.news)
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_max_date():
        """Fetching the max news date of a service"""
        async with tm_async_session_maker() as session:
            query = func.max(News.date)
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_min_date():
        """Fetching the min news date of a service"""
        async with tm_async_session_maker() as session:
            query = func.min(News.date)
            result = await session.execute(query)
            return result.scalar_one()

    @staticmethod
    async def get_distinct_dates():
        """Fetching all distinct dates in a service"""
        async with tm_async_session_maker() as session:
            query = select(cast(News.date, Date), func.count(cast(News.date, Date))).group_by(
                cast(News.date, Date)).order_by(cast(News.date, Date))
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def get_borderline_date(value: str):
        """Don't work. Attempt to merge functions get_max_date and get_min_date"""
        async with tm_async_session_maker() as session:
            match value:
                case 'min':
                    query = func.min(News.date)
                case 'max':
                    query = func.max(News.date)
            result = await session.execute(query)
            return result.scalar_one()
