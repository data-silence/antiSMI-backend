from app.dao.base import BaseDao
from app.agencies.models import Agencies
# from app.db import tm_async_session_maker
# from sqlalchemy import select, and_, distinct, func
# from app.news.models import News

# DAO - Data Access Object
class AgenciesDao(BaseDao):
    model = Agencies


