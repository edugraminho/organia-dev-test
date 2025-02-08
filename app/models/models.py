from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

Base = declarative_base()


class SentimentEnum(str, PyEnum):
    """
    Enumeration representing possible sentiment classifications.

    Attributes:
        POSITIVE (str): Represents a positive sentiment.
        NEUTRAL (str): Represents a neutral sentiment.
        NEGATIVE (str): Represents a negative sentiment.
    """

    POSITIVE = "positiva"
    NEUTRAL = "neutra"
    NEGATIVE = "negativa"


class Review(Base):
    """
    Represents a customer review.

    Attributes:
        id (int): Primary key, auto-incremented.
        customer_name (str): Name of the customer who wrote the review.
        review_date (int): Timestamp representing the review date.
        review_text (str): The text content of the review.
        sentiment (SentimentEnum): The sentiment classification of the review.
        sentiment_analysis (SentimentAnalysis): Relationship to the sentiment analysis.
    """

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
    """
    Represents an AI sentiment analysis for a review.

    Attributes:
        id (int): Primary key, auto-incremented.
        review_id (int): Foreign key linking to the associated review.
        sentiment (str): Sentiment classification of the review.
        score (float): Sentiment score ranging from -1 (negative) to 1 (positive).
        keywords (str): Keywords extracted from the review text.
        explanation (str): Explanation of the sentiment classification.
        review (Review): Relationship back to the review.
    """

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
