from datetime import datetime

from pydantic import BaseModel
from pydantic_core import Url


class SNews(BaseModel):
    url: Url
    category: str
    title: str
    resume: str
    news: str
    date: datetime
    links: str
    agency: str

    class Config:
        from_attributes = True


class SShortNews(BaseModel):
    url: Url
    title: str
    resume: str
    date: datetime

    class Config:
        from_attributes = True