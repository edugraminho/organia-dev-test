from typing import List, Any
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, HTTPException
from app.models.models import Review, SentimentAnalysis
from app.utils.utils import convert_date_to_timestamp, convert_timestamp_to_date
from app.services.ai_service import analyze_review_sentiment

router = APIRouter()


def process_create_review(db: Session, review_data: dict) -> dict:
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

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

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

    db.add(new_analysis)
    db.commit()

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


def process_get_all_reviews(db: Session) -> dict[str, Any] | dict[str, list]:
    """
    Retrieves all stored customer reviews.

    Args:
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a list of all reviews, or a 404 message if none are found.
    """
    reviews_list: List[Review] = db.query(Review).all()

    if not reviews_list:
        return {
            "status": 404,
            "message": "Não há avaliações listados",
        }

    reviews_data = []
    for review in reviews_list:
        review_data = {
            "id": review.id,
            "customer_name": review.customer_name,
            "review_text": review.review_text,
            "sentiment": review.sentiment,
            "review_date": convert_timestamp_to_date(review.review_date),
        }

        reviews_data.append(review_data)

    return {"reviews_list": reviews_data}


def process_get_review_by_id(
    db: Session, review_id: int
) -> dict[str, Any] | dict[str, list]:
    """
    Retrieves a specific customer review by its ID.

    Args:
        db (Session): The database session.
        review_id (int): The ID of the review to retrieve.

    Returns:
        dict: A dictionary containing the review details, or a 404 message if not found.
    """
    review: Review = db.query(Review).filter(Review.id == review_id).first()

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


def process_reviews_report(db: Session, start_date: str, end_date: str) -> dict:
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
        return {"status": 400, "message": "Formato de data inválido. Use YYYY-MM-DD."}

    reviews: List[Review] = (
        db.query(Review)
        .options(joinedload(Review.sentiment_analysis))
        .filter(
            Review.review_date >= start_timestamp,
            Review.review_date <= end_timestamp,
        )
        .all()
    )

    if not reviews:
        return {"message": "Nenhuma avaliação encontrada no período informado."}

    sentiment_mapping = {
        "positiva": "positive",
        "negativa": "negative",
        "neutra": "neutral",
    }

    report: dict = {
        "total_reviews": len(reviews),
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "reviews": [],
    }

    for review in reviews:
        analysis = review.sentiment_analysis

        sentiment_en = sentiment_mapping.get(analysis.sentiment.lower(), "neutral")
        report[sentiment_en] += 1

        report["reviews"].append(
            {
                "id": review.id,
                "customer_name": review.customer_name,
                "review_date": convert_timestamp_to_date(review.review_date),
                "review_text": review.review_text,
                "sentiment": analysis.sentiment,
                "score": analysis.score,
                "keywords": analysis.keywords,
                "explanation": analysis.explanation,
            }
        )

    return report
