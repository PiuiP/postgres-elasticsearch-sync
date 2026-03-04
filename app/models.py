from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey,  JSON, ARRAY, Integer, Text
from datetime import datetime
from typing import Optional, List

class Base(DeclarativeBase):
    pass

class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[Optional[str]] = mapped_column(Text)
    pub_date: Mapped[Optional[datetime]]
    source: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Risk(Base):
    __tablename__ = "risks"
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    risk_type: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[Optional[float]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Entity(Base):
     __tablename__ = "entities"
     id: Mapped[int] = mapped_column(primary_key=True)
     article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
     text: Mapped[str] = mapped_column(Text, nullable=False)
     type: Mapped[str] = mapped_column(Text, nullable=False)
     start_pos: Mapped[Optional[int]]
     end_pos: Mapped[Optional[int]]
     details: Mapped[Optional[dict]] = mapped_column(JSON)

class Cluster(Base):
    __tablename__ = "clusters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    article_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    created_at: Mapped[datetime]