from app.dao.base import BaseDao
from app.agencies.models import Agencies

"""DAO - Data Access Object to Agencies"""


class AgenciesDao(BaseDao):
    model = Agencies
