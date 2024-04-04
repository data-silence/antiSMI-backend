from datetime import datetime

from pydantic import BaseModel
from pydantic_core import Url
from enum import Enum



class SShortNews(BaseModel):
    """Class representing the news in a brief form"""
    url: Url
    title: str
    resume: str
    date: datetime


class SFullNews(SShortNews):
    """Class representing the news in a full form"""
    category: str
    news: str
    links: str
    agency: str

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True


class SEmbsNews(SFullNews):
    """Class representing the news in a full form with embeddings"""
    embedding: list[float]

    class Config:
        from_attributes = True


class SMediaNews(SFullNews):
    """Class representing the news in a full form with media type"""
    media_type: str

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