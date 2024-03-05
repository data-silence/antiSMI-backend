from sqlalchemy import select

from app.db import asmi_async_session_maker


class BaseDao:
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id).limit(5)
            result = await session.execute(query)
            return result.mappings.one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).limit(5)
            result = await session.execute(query)
            return result.mappings.one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).limit(5)
            result = await session.execute(query)
            return result.mappings().all()
