from fastapi import APIRouter
from app.news.dao import NewsDao, get_news_by_date
from app.news.schemas import SShortNews
from app.news.services import get_time_period

router = APIRouter(
    prefix='/news',
    tags=['News'],
)


@router.get('/last_quota')
async def get_quota() -> list[SShortNews]:
    start, end = get_time_period()
    return await get_news_by_date(start=start, end=end)
