from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.schemas.review_schema import ReviewCreate
from app.services.reviews_service import (
    process_create_review,
    process_get_all_reviews,
    process_get_review_by_id,
    process_reviews_report,
)

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", status_code=201)
def reviews_create(review_data: ReviewCreate, db: Session = Depends(get_db)) -> dict:
    """
    Retrieves all stored reviews.

    Args:
        db (Session): Database session dependency.

    Returns:
        dict: A list of all reviews stored in the database.
    """
    try:
        return process_create_review(db, review_data.model_dump(by_alias=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_all_reviews(db: Session = Depends(get_db)) -> dict:
    """
    Retrieves all stored reviews.

    Args:
        db (Session): Database session dependency.

    Returns:
        dict: A list of all reviews stored in the database.
    """
    return process_get_all_reviews(db)


@router.get("/report")
def get_reviews_report(
    start_date: str, end_date: str, db: Session = Depends(get_db)
) -> dict:
    """
    Generates a report of reviews within a given date range.

    Args:
        start_date (str): Start date in the format YYYY-MM-DD.
        end_date (str): End date in the format YYYY-MM-DD.
        db (Session): Database session dependency.

    Returns:
        dict: A summary of the number of positive, negative, and neutral reviews within the specified period.
    """
    return process_reviews_report(db, start_date, end_date)


@router.get("/{review_id}")
def get_review_by_id(review_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Retrieves a specific review by its ID.

    Args:
        review_id (int): The ID of the review to retrieve.
        db (Session): Database session dependency.

    Returns:
        dict: The requested review data or an error message if not found.
    """
    return process_get_review_by_id(db, review_id)
