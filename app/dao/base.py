from sqlalchemy import select
from app.db import asmi_async_session_maker


class BaseDao:
    """This Class is Data Access Object for common db requests to any tables"""
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        """Get record by id"""
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id).limit(5)
            result = await session.execute(query)
            return result.mappings.one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        """Get only one record or None for select request with filter"""
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).limit(5)
            result = await session.execute(query)
            return result.mappings.one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        """Get all records for select request with filter"""
        async with asmi_async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
