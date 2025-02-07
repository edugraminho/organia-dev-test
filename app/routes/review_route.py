from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.schemas.review_schema import ReviewCreate
from app.services.reviews_service import process_create_review, process_get_all_reviews, process_get_review_by_id, process_reviews_report

router = APIRouter()


@router.post("/reviews/", status_code=201)
def reviews_create(review_data: ReviewCreate, db: Session = Depends(get_db)) -> dict:
    try:
        return process_create_review(db, review_data.model_dump(by_alias=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reviews/")
def get_all_reviews(db: Session = Depends(get_db)) -> dict:
    return process_get_all_reviews(db)


@router.get("/reviews/{review_id}")
def get_review_by_id(review_id: int, db: Session = Depends(get_db)) -> dict:
    return process_get_review_by_id(db, review_id)


@router.get("/reviews/report")
def get_reviews_report(start_date: str, end_date: str, db: Session = Depends(get_db)) -> dict:
    return process_reviews_report(db, start_date, end_date)