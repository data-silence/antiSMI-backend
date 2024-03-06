from datetime import datetime

from pydantic import BaseModel
from pydantic_core import Url
from enum import Enum



class SShortNews(BaseModel):
    url: Url
    title: str
    resume: str
    date: datetime


class SFullNews(SShortNews):
    category: str
    news: str
    links: str
    agency: str

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True


class SEmbsNews(SFullNews):
    embedding: list[float]

    class Config:
        from_attributes = True

class CategoriesNames(str, Enum):
    """"Enum Class, contains the available news categories"""
    ECONOMY = 'economy'
    SCIENCE = 'science'
    SPORTS = 'sports'
    TECHNOLOGY = 'technology'
    ENTERTAINMENT = 'entertainment'
    SOCIETY = 'society'