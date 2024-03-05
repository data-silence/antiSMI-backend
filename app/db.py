"""
This is database connection module
For some reason credentials for connection are stored in public
"""
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

load_dotenv()

# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")

asmi_engine = create_async_engine(settings.ASMI_URL)
asmi_async_session_maker = sessionmaker(asmi_engine, class_=AsyncSession, expire_on_commit=False)

tm_engine = create_async_engine(settings.TM_URL)
tm_async_session_maker = sessionmaker(tm_engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
