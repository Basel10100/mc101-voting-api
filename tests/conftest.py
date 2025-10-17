import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure project root is on sys.path so `import main` works when running pytest from various contexts
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Minimal environment for tests (uses SQLite via DbConfig when PYTEST_CURRENT_TEST is present)
os.environ.setdefault("RUNTIME", "test")
os.environ.setdefault("TEST_DB_URL", "sqlite:///./test.db")
os.environ.setdefault("JWT_SECRET_KEY", "test_secret_key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_EXPIRATION_TIME", "10")
os.environ.setdefault("APP_ENCRYPTION_KEY", "test_app_encryption_key")
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("POSTGRES_DB", "voting_db")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT_IN_DOCKER", "5432")


@pytest.fixture(scope="function", autouse=True)
def clean_database():
    """Clean database before each test"""
    # Import here to avoid circular imports
    from db.DbConfig import Base, get_db_url
    from db.DBModels import CandidateDBModel, UserDBModel, VoteDBModel

    # Create engine and clear all tables
    engine = create_engine(get_db_url())
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Clear all data before each test
    db = SessionLocal()
    try:
        db.query(VoteDBModel).delete()
        db.query(CandidateDBModel).delete()
        db.query(UserDBModel).delete()
        db.commit()
    finally:
        db.close()

    yield

    # Cleanup after test if needed
    db = SessionLocal()
    try:
        db.query(VoteDBModel).delete()
        db.query(CandidateDBModel).delete()
        db.query(UserDBModel).delete()
        db.commit()
    finally:
        db.close()
