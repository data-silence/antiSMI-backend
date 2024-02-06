from datetime import datetime

from pydantic import BaseModel

class SNews(BaseModel):
    url: str
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
    url: str
    title: str
    resume: str
    date: datetime

    class Config:
        from_attributes = True