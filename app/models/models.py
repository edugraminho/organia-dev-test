from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base


class SentimentEnum(str, PyEnum):
    POSITIVE = "positiva"
    NEUTRAL = "neutra"
    NEGATIVE = "negativa"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    review_date = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)
    sentiment = Column(Enum(SentimentEnum), nullable=False)

    sentiment_analysis = relationship(
        "SentimentAnalysis",
        back_populates="review",
        cascade="all, delete-orphan",
        uselist=False,
    )


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(
        Integer,
        ForeignKey("reviews.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    sentiment = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    keywords = Column(String, nullable=False)
    explanation = Column(String, nullable=False)

    review = relationship("Review", back_populates="sentiment_analysis")
