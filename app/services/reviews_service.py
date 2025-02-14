from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from app.models.models import Review, SentimentAnalysis
from app.utils.utils import convert_date_to_timestamp, convert_timestamp_to_date
from app.services.ai_service import analyze_review_sentiment
from pydantic import BaseModel, field_validator


class ReviewOut(BaseModel):
    id: int
    customer_name: str
    review_date: int
    review_text: str
    sentiment: str

    @classmethod
    def from_orm(cls, review: Review):
        return cls(
            id=review.id,
            customer_name=review.customer_name,
            review_date=review.review_date,
            review_text=review.review_text,
            sentiment=review.sentiment,
        )


class ReviewService:
    def __init__(self, db: Session):
        """
        Initializes the ReviewService with a database session.
        """
        self.db = db

    def create_review(self, review_data: dict) -> dict:
        """
        Creates a new customer review and performs sentiment analysis.

        Args:
            db (Session): The database session.
            review_data (dict): A dictionary containing the review details:
                - "customer_name" (str): Name of the customer who wrote the review.
                - "review_text" (str): The content of the review.
                - "sentiment" (str): The sentiment classification (must be "positiva", "negativa", or "neutra").
                - "review_date" (str): The date of the review in "YYYY-MM-DD" format.

        Raises:
            HTTPException: If required fields are missing or have invalid values.

        Returns:
            dict: A dictionary containing the created review details, including sentiment analysis.
        """
        required_fields: list[str] = [
            "customer_name",
            "review_text",
            "sentiment",
            "review_date",
        ]
        for field in required_fields:
            if field not in review_data or not review_data[field]:
                raise HTTPException(status_code=400, detail=f"'{field}' é obrigatório.")

        if not isinstance(review_data["customer_name"], str) or not isinstance(
            review_data["review_text"], str
        ):
            raise HTTPException(
                status_code=400,
                detail="Os campos 'customer_name' e 'review_text' devem ser strings.",
            )

        if review_data["sentiment"] not in ["positiva", "negativa", "neutra"]:
            raise HTTPException(
                status_code=400,
                detail="O campo 'sentiment' deve ser 'positiva', 'negativa' ou 'neutra'.",
            )

        try:
            review_timestamp: int = convert_date_to_timestamp(
                review_data["review_date"], "%Y-%m-%d"
            )
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD."
            )

        new_review = Review(
            customer_name=review_data["customer_name"],
            review_text=review_data["review_text"],
            sentiment=review_data["sentiment"],
            review_date=review_timestamp,
        )

        self.db.add(new_review)
        self.db.commit()
        self.db.refresh(new_review)

        sentiment_analysis_dict = analyze_review_sentiment(new_review.review_text)

        new_analysis = SentimentAnalysis(
            review_id=new_review.id,
            sentiment=sentiment_analysis_dict.get("sentiment", ""),
            score=sentiment_analysis_dict.get("score", 0.0),
            keywords=",".join(sentiment_analysis_dict.get("keywords", [])),
            explanation=sentiment_analysis_dict.get(
                "explanation", "Análise sem explicação detalhada."
            ),
        )

        self.db.add(new_analysis)
        self.db.commit()

        return {
            "status": "OK",
            "review": {
                "id": new_review.id,
                "customer_name": new_review.customer_name,
                "review_text": new_review.review_text,
                "sentiment": new_review.sentiment,
                "review_date": review_data["review_date"],
            },
        }

    def get_all_reviews(self) -> Page[ReviewOut]:
        """
        Retrieves all stored customer reviews.

        Args:
            db (Session): The database session.

        Returns:
            dict: A dictionary containing a list of all reviews, or a 404 message if none are found.
        """

        query = select(Review).order_by(Review.review_date.desc())

        reviews = paginate(self.db, query)

        reviews.items = [ReviewOut.from_orm(review) for review in reviews.items]

        return reviews

    def get_review_by_id(self, review_id: int) -> dict:
        """
        Retrieves a specific customer review by its ID.

        Args:
            db (Session): The database session.
            review_id (int): The ID of the review to retrieve.

        Returns:
            dict: A dictionary containing the review details, or a 404 message if not found.
        """
        review: Review = self.db.query(Review).filter(Review.id == review_id).first()

        if not review:
            return {
                "status": 404,
                "message": "Avaliação não encontrada",
            }

        review_data = {
            "id": review.id,
            "customer_name": review.customer_name,
            "review_text": review.review_text,
            "sentiment": review.sentiment,
            "review_date": convert_timestamp_to_date(review.review_date),
        }

        return {"review": review_data}

    def get_reviews_report(self, start_date: str, end_date: str) -> dict:
        """
        Generates a report of customer reviews within a specified date range.

        Args:
            db (Session): The database session.
            start_date (str): The start date in "YYYY-MM-DD" format.
            end_date (str): The end date in "YYYY-MM-DD" format.

        Raises:
            HTTPException: If the date format is invalid.

        Returns:
            dict: A report containing the total number of reviews and a breakdown by sentiment.
        """
        try:
            start_timestamp: int = convert_date_to_timestamp(start_date, "%Y-%m-%d")
            end_timestamp: int = convert_date_to_timestamp(end_date, "%Y-%m-%d")

        except ValueError:
            return {
                "status": 400,
                "message": "Formato de data inválido. Use YYYY-MM-DD.",
            }

        query = (
            select(Review)
            .options(joinedload(Review.sentiment_analysis))
            .filter(
                Review.review_date >= start_timestamp,
                Review.review_date <= end_timestamp,
            )
            .order_by(Review.review_date.desc())
        )

        sentiment_mapping = {
            "positiva": "positive",
            "negativa": "negative",
            "neutra": "neutral",
        }

        def transform_review(review: Review) -> dict:
            analysis = review.sentiment_analysis
            sentiment_en = sentiment_mapping.get(analysis.sentiment.lower(), "neutral")

            return {
                "id": review.id,
                "customer_name": review.customer_name,
                "review_date": convert_timestamp_to_date(review.review_date),
                "review_text": review.review_text,
                "sentiment": sentiment_en,
                "score": analysis.score,
                "keywords": analysis.keywords,
                "explanation": analysis.explanation,
            }

        paginated_reviews = paginate(self.db, query, params=Params()).dict()

        paginated_reviews["items"] = list(
            map(transform_review, paginated_reviews["items"])
        )

        return paginated_reviews
