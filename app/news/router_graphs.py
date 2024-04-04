from fastapi import APIRouter
from app.news.dao import NewsDao
from datetime import date


router = APIRouter(
    prefix='/graphs',
    tags=['Graphs'],
)


@router.get('/tm/agencies_amount')
async def get_agencies_amount() -> int:
    return await NewsDao.get_agencies_amount()


@router.get('/tm/categories_amount')
async def get_categories_amount() -> int:
    return await NewsDao.get_categories_amount()


@router.get('/tm/news_amount')
async def get_news_amount() -> int:
    return await NewsDao.get_news_amount()


@router.get('/tm/borderline_date/{value}')
async def get_borderline_date(value: str) -> date:
    borderline_date_with_time = await NewsDao.get_borderline_date(value=value)
    borderline_date = borderline_date_with_time.date()
    return borderline_date


@router.get('/tm/max_date')
async def get_max_date() -> date:
    max_date = await NewsDao.get_max_date()
    return max_date.date()


@router.get('/tm/min_date')
async def get_min_date() -> date:
    max_date = await NewsDao.get_min_date()
    return max_date.date()


@router.get('/tm/distinct_dates')
async def get_distinct_dates() -> list[dict]:
    return await NewsDao.get_distinct_dates()