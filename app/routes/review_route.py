from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.services.reviews_service import ReviewService, ReviewOut

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", status_code=201)
def reviews_create(review_data: dict, db: Session = Depends(get_db)) -> dict:
    """
    Retrieves all stored reviews.

    Args:
        db (Session): Database session dependency.

    Returns:
        dict: A list of all reviews stored in the database.
    """
    return ReviewService(db).create_review(review_data)


@router.get("/")
def get_all_reviews(db: Session = Depends(get_db)) -> Page[ReviewOut]:
    """
    Retrieves all stored reviews.

    Args:
        db (Session): Database session dependency.

    Returns:
        dict: A list of all reviews stored in the database.
    """
    return ReviewService(db).get_all_reviews()


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
    return ReviewService(db).get_reviews_report(start_date, end_date)


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
    return ReviewService(db).get_review_by_id(review_id)
