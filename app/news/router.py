from datetime import date

from fastapi import APIRouter
from app.news.dao import NewsDao, get_news_by_date
from app.news.schemas import SShortNews

router = APIRouter(
    prefix='/news',
    tags=['News'],
)


@router.get('last_quota')
async def get_quota() -> list[SShortNews]:
    return await get_news_by_date(my_date=date(2022, 10, 11))
