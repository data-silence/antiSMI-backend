from fastapi import APIRouter
from datetime import date

from app.news.dao import NewsDao
from app.news.schemas import SShortNews, SFullNews, SEmbsNews, SMediaNews, SFinalNews
from app.news.services import get_time_period, make_single_embs

import fasttext as fasttext
import warnings

warnings.filterwarnings("ignore")
fasttext.FastText.eprint = lambda x: None
model_class = fasttext.load_model("app/models/cat_model.ftz")

router = APIRouter(
    prefix='/news',
    tags=['News'],
)


@router.get('/last_allowed_quota')
async def get_allowed_quota() -> list[SShortNews]:
    """Handler to fetch last allowed news"""
    start, end = get_time_period()
    return await NewsDao.get_allowed_news_by_date(start=start, end=end)


@router.get('/asmi/today')
async def get_test_type() -> list[SMediaNews]:
    """Handler to fetch today news without further logic"""
    return await NewsDao.get_today_news()


@router.get('/asmi/today/brief')
async def get_quota() -> list[SFullNews]:
    """
    Handler to fetch all today news. If the request is made at a time when the news has not been processed yet,
    yesterday's news will be requested.
    """
    start, end = get_time_period()
    return await NewsDao.get_news_by_date(start=start, end=end)


@router.get('/asmi/date_news/{user_date}/{date_part}/{date_mode}')
async def get_some_quota(user_date: date, date_part: int, date_mode: str) -> list[SFinalNews]:
    """
    Handler to fetch one day news from aSMI. If the request is made at a time when the news has not been processed yet,
    yesterday's news will be requested.
    """
    start, end = get_time_period(user_start=user_date, date_part=date_part, mode=date_mode)
    answer_list = await NewsDao.get_news_by_date(start=start, end=end)
    result_list = [dict(el) for el in answer_list]

    for el in range(len(result_list)):
        result_list[el]['embedding'] = model_class.get_sentence_vector(result_list[el]['news']).tolist()

    return result_list


@router.get('/asmi/today/{media_type}')
async def get_media_type(media_type: str) -> list[SFullNews]:
    """Handler to fetch today news from a certain type of news agency"""
    return await NewsDao.get_media_types_news(media_type)


@router.get('/tm/{start_date}/{end_date}')
async def get_embs_news(start_date: date = date.today(), end_date: date = date.today()) -> list[SEmbsNews]:
    """Handler to fetch past news over a period of time"""
    start, end = get_time_period(user_start=start_date, user_end=end_date)
    return await NewsDao.get_embs_news(start=start, end=end)


@router.post('/tm/get_similar_news')
async def get_most_similar_news(embedding: list[float]) -> list[SEmbsNews]:
    """Handler to fetch most simular news to transferable embedding"""
    return await NewsDao.get_similar_news(embedding=embedding)


@router.get('/tm/find_similar_news/{start_date}/{end_date}')
async def find_similar_news(query: str, start_date: date, end_date: date) -> list[SFullNews]:
    """Handler to fetch most simular news to transferable query over a period of time"""
    embedding = make_single_embs(sentences=query)
    category = model_class.predict(query)[0][0].split('__')[-1]
    if category == 'not_news' or category == 'other':
        category = 'society'
    return await NewsDao.find_similar_news(embedding=embedding, start_date=start_date, end_date=end_date,
                                           category=category)
