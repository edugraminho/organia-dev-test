from pydantic import BaseModel

class ReviewCreate(BaseModel):
    """
    Schema for creating a new customer review.

    Attributes:
        customer_name (str): The name of the customer who wrote the review.
        review_date (str): The date of the review in the format YYYY-MM-DD.
        review_text (str): The text content of the review.
        sentiment (str): The sentiment classification of the review (e.g., "positive", "negative", "neutral").
    """
    customer_name: str
    review_date: str
    review_text: str
    sentiment: str
