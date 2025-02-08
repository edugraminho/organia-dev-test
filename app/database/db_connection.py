from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models.models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    """
    Provides a database session.

    This function generates a SQLAlchemy session (`SessionLocal`) and ensures
    that the connection is properly closed after use.

    Yields:
        Session: A SQLAlchemy session for database interaction.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
