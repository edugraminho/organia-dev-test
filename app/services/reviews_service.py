from typing import List, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from app.models.models import Review
from app.utils import convert_date_to_timestamp, convert_timestamp_to_date

router = APIRouter()


def process_create_review(db: Session, review_data: dict) -> dict:
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
        review_timestamp: int = convert_date_to_timestamp(review_data["review_date"])
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
    try:
        start_timestamp: int = convert_date_to_timestamp(start_date, "%Y-%m-%d")
        end_timestamp: int = convert_date_to_timestamp(end_date, "%Y-%m-%d")

    except ValueError:
        return {"status": 400, "message": "Formato de data inválido. Use YYYY-MM-DD."}

    reviews_in_period = (
        db.query(Review.sentiment, func.count(Review.id))
        .filter(Review.review_date >= start_timestamp)
        .filter(Review.review_date <= end_timestamp)
        .group_by(Review.sentiment)
        .all()
    )

    report = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }

    for sentiment, count in reviews_in_period:
        if sentiment == "positive":
            report["positive"] = count
        elif sentiment == "negative":
            report["negative"] = count
        elif sentiment == "neutral":
            report["neutral"] = count

    return {"status": 200, "report": report}
