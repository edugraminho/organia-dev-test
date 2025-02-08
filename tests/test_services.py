import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, Review, SentimentAnalysis
from app.services.reviews_service import (
    process_create_review,
    process_get_all_reviews,
    process_get_review_by_id,
    process_reviews_report,
)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_review():
    return {
        "customer_name": "Eduardo FG",
        "review_text": "Ótimo atendimento e suporte muito rapido!",
        "sentiment": "positiva",
        "review_date": "2024-06-01",
    }


def test_process_create_review_should_return_1(db_session, sample_review):
    response = process_create_review(db_session, sample_review)

    assert response["status"] == "OK"
    assert response["review"]["customer_name"] == sample_review["customer_name"]
    assert response["review"]["review_text"] == sample_review["review_text"]

    review = db_session.query(Review).filter_by(customer_name="Eduardo FG").first()
    assert review is not None

    analysis = (
        db_session.query(SentimentAnalysis).filter_by(review_id=review.id).first()
    )
    assert analysis is not None
    assert analysis.sentiment == "positiva"


def test_process_get_all_reviews_should_return_1(db_session, sample_review):
    process_create_review(db_session, sample_review)

    response = process_get_all_reviews(db_session)
    assert "reviews_list" in response
    assert len(response["reviews_list"]) == 1
    assert (
        response["reviews_list"][0]["customer_name"] == sample_review["customer_name"]
    )


def test_process_get_review_by_id(db_session, sample_review):
    response = process_create_review(db_session, sample_review)
    review_id = response["review"]["id"]

    response = process_get_review_by_id(db_session, review_id)
    assert response["review"]["id"] == review_id
    assert response["review"]["customer_name"] == sample_review["customer_name"]


def test_process_reviews_report(db_session, sample_review):
    process_create_review(db_session, sample_review)

    start_date = "2024-06-01"
    end_date = "2024-06-30"
    response = process_reviews_report(db_session, start_date, end_date)

    assert "total_reviews" in response
    assert response["total_reviews"] == 1
    assert response["positive"] == 1
