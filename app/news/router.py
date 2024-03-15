from fastapi import APIRouter
from app.news.dao import NewsDao
from app.news.schemas import SShortNews, SFullNews, SEmbsNews
from app.news.services import get_time_period
from datetime import date

router = APIRouter(
    prefix='/news',
    tags=['News'],
)


@router.get('/last_allowed_quota')
async def get_allowed_quota() -> list[SShortNews]:
    start, end = get_time_period()
    return await NewsDao.get_allowed_news_by_date(start=start, end=end)


@router.get('/asmi/today/brief')
async def get_quota() -> list[SFullNews]:
    start, end = get_time_period()
    return await NewsDao.get_news_by_date(start=start, end=end)


@router.get('/asmi/today/{media_type}')
async def get_allowed_quota(media_type: str) -> list[SFullNews]:
    return await NewsDao.get_media_types_news(media_type)


@router.get('/tm/{start_date}/{end_date}')
async def get_embs_news(start_date: date = date.today(), end_date: date = date.today()) -> list[SEmbsNews]:
    start, end = get_time_period(start_date=start_date, end_date=end_date)
    return await NewsDao.get_embs_news(start=start, end=end)


@router.post('/tm/get_similar_news')
async def get_most_similar_news(embedding: list[float]) -> list[SEmbsNews]:
    return await NewsDao.get_similar_news(embedding=embedding)
