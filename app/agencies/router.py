from fastapi import APIRouter

# from app.agencies.schemas import SAgencies
# from app.agencies.dao import AgenciesDao

router = APIRouter(
    prefix='/agencies',
    tags=['Agencies'],
)


# @router.get('/take_some')
# async def get_allowed_agencies() -> list[SAgencies]:
#     return await AgenciesDao.get_all(is_forbidden=False)
