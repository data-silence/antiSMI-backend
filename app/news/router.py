from fastapi import APIRouter
from app.news.dao import NewsDao
from app.news.schemas import SShortNews, SFullNews, SEmbsNews
from app.news.services import get_time_period
from datetime import date
# import datetime as dt
from app.news.services import NewsService, default_categories, default_day

# from dateutil.parser import parse
# from loguru import logger
# import json

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


@router.get('/tm/{start_date}/{end_date}')
async def get_embs_news(start_date: date = date.today(), end_date: date = date.today()) -> list[SEmbsNews]:
    start, end = get_time_period(start_date=start_date, end_date=end_date)
    return await NewsDao.get_embs_news(start=start, end=end)


@router.post('/tm/get_similar_news')
async def get_most_similar_news(embedding: list[float]) -> list[SEmbsNews]:
    return await NewsDao.get_similar_news(embedding)


# @router.get('/asmi/today/full')
# async def get_embs_full() -> list[SEmbsNews]:
#     return get_today_emb()


# @router.post('/tm/get_date_news')
# def get_news_by_date(date: dt.date = default_day, news_amount: int = 3,
#                      categories: list[str] = default_categories) -> list[SFullNews]:
#     most_news = NewsService()
#     most_news.set_date_df(date=date)
#     most_news.set_news_amount(news_amount=news_amount)
#     most_news.set_categories(categories=categories)
#     dict_news = most_news.leave_me_alone().to_dict(orient='records')
#     return dict_news
