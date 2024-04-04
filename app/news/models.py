from datetime import datetime

from sqlalchemy import Date
from sqlalchemy.orm import mapped_column, Mapped
from pgvector.sqlalchemy import Vector

from app.db import Base


class News(Base):
    __tablename__ = 'news'
    url: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    resume: Mapped[str] = mapped_column(nullable=False)
    news: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    links: Mapped[str] = mapped_column(nullable=False)
    agency: Mapped[str] = mapped_column(nullable=False)

    def __str__(self):
        return f"News {self.url}"


class Embs(Base):
    __tablename__ = 'embs'
    news_url: Mapped[str] = mapped_column(primary_key=True)
    embedding: Mapped[Vector] = mapped_column(Vector, nullable=False)

    def __str__(self):
        return f"News {self.news_url, self.embedding}"
