from pydantic import BaseModel

class ReviewCreate(BaseModel):
    customer_name: str
    review_date: str
    review_text: str
    sentiment: str
