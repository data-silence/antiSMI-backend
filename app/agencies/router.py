from fastapi import APIRouter

from app.agencies.schemas import SAllAgencies
from app.agencies.dao import AgenciesDao

router = APIRouter(
    prefix='/agencies',
    tags=['Agencies'],
)


@router.get('/all')
async def get_all_agencies() -> list[SAllAgencies]:
    return await AgenciesDao.get_all()
    # return await AgenciesDao.get_all(is_forbidden=False)

