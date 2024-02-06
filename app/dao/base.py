from sqlalchemy import select, func

from app.db import async_session_maker


class BaseDao:
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id).limit(5)
            result = await session.execute(query)
            return result.mappings.one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).limit(5)
            result = await session.execute(query)
            return result.mappings.one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).limit(5)
            result = await session.execute(query)
            return result.mappings().all()
