from sqlalchemy import Column, String, Enum, Integer
from enum import Enum as PyEnum
from .base import Base


class SentimentEnum(str, PyEnum):
    POSITIVE = "positiva"
    NEUTRAL = "neutra"
    NEGATIVE = "negativa"


class Review(Base):
    __tablename__: str = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    review_date = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)
    sentiment = Column(Enum(SentimentEnum), nullable=False)
