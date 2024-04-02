from fastapi import APIRouter
from app.news.dao import NewsDao
from app.news.embs_exps import make_single_embs
from app.news.schemas import SShortNews, SFullNews, SEmbsNews, SMediaNews
from app.news.services import get_time_period
from datetime import date
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
    start, end = get_time_period()
    return await NewsDao.get_allowed_news_by_date(start=start, end=end)


@router.get('/asmi/today/brief')
async def get_quota() -> list[SFullNews]:
    start, end = get_time_period()
    return await NewsDao.get_news_by_date(start=start, end=end)


@router.get('/asmi/today')
async def get_test_type() -> list[SMediaNews]:
    return await NewsDao.get_tody_news()


@router.get('/asmi/today/{media_type}')
async def get_media_type(media_type: str) -> list[SFullNews]:
    return await NewsDao.get_media_types_news(media_type)


@router.get('/tm/{start_date}/{end_date}')
async def get_embs_news(start_date: date = date.today(), end_date: date = date.today()) -> list[SEmbsNews]:
    start, end = get_time_period(start_date=start_date, end_date=end_date)
    return await NewsDao.get_embs_news(start=start, end=end)


@router.post('/tm/get_similar_news')
async def get_most_similar_news(embedding: list[float]) -> list[SEmbsNews]:
    return await NewsDao.get_similar_news(embedding=embedding)


# @router.post('/tm/get_similar_news_advanced/{query}/{start_date}/{end_date}')
# async def get_similar_news_advanced(query: str, start_date: date, end_date: date) -> list[SFullNews]:
#     embedding = make_single_embs(sentences=query)
#     return await NewsDao.get_similar_news_advanced(embedding=embedding, start_date=start_date, end_date=end_date)

@router.get('/tm/find_similar_news/{start_date}/{end_date}')
async def find_similar_news(query: str, start_date: date, end_date: date) -> list[SFullNews]:
    embedding = make_single_embs(sentences=query)
    category = model_class.predict(query)[0][0].split('__')[-1]
    if category == 'not_news' or category == 'other':
        category = 'society'
    return await NewsDao.find_similar_news(embedding=embedding, start_date=start_date, end_date=end_date,
                                           category=category)


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
