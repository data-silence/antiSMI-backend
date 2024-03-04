from fastapi import APIRouter
from app.news.dao import NewsDao
from app.news.schemas import SShortNews, SNews
from app.news.services import get_time_period
import datetime as dt
# from sqlalchemy import cast, Date

router = APIRouter(
    prefix='/news',
    tags=['News'],
)


@router.get('/last_allowed_quota')
async def get_allowed_quota() -> list[SShortNews]:
    start, end = get_time_period()
    return await NewsDao.get_allowed_news_by_date(start=start, end=end)

@router.get('/last_quota')
async def get_quota() -> list[SNews]:
    start, end = get_time_period()
    return await NewsDao.get_news_by_date(start=start, end=end, agency='meduzalive')

# @router.get('/get_all_full')
# async def get_all_full() -> list[SNews]:
#     return await NewsDao.find_all(agency='meduzalive')
