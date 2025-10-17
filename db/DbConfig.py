import os
from config import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settings = Settings()

# Postgres engine

def get_db_url() -> str:
    # Check if we're running in test mode
    runtime = os.getenv('RUNTIME', settings.RUNTIME)
    # Heuristic: if running under pytest, switch to test runtime automatically
    if 'PYTEST_CURRENT_TEST' in os.environ:
        runtime = 'test'
    
    if runtime == 'test':
        # Use the test database URL if provided, else default to local sqlite file
        test_db_url = os.getenv('TEST_DB_URL', settings.TEST_DB_URL) or 'sqlite:///./test.db'
        print(f"Using test database URL: {test_db_url}")
        return test_db_url
    
    # Otherwise, build the regular database URL
    # Check for environment variables first (Docker overrides), then fall back to settings
    user = os.getenv('POSTGRES_USER', settings.POSTGRES_USER)
    password = os.getenv('POSTGRES_PASSWORD', settings.POSTGRES_PASSWORD.get_secret_value())
    host = os.getenv('POSTGRES_HOST', settings.POSTGRES_HOST)
    db = os.getenv('POSTGRES_DB', settings.POSTGRES_DB)
    port = os.getenv('POSTGRES_PORT_IN_DOCKER', str(settings.POSTGRES_PORT_IN_DOCKER))
    
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    print(f"Using {runtime} database URL: {url}")  # For debugging purposes
    return url

# Create engine lazily to avoid connection issues at import time
def get_engine():
    """Get or create the database engine"""
    global _engine
    if '_engine' not in globals():
        url = get_db_url()
        if url.startswith('sqlite:'):
            _engine = create_engine(url, connect_args={"check_same_thread": False})
        else:
            _engine = create_engine(url)
    return _engine

Base = declarative_base()

def get_session_local():
    """Get SessionLocal bound to the current engine"""
    return sessionmaker(bind=get_engine())


# print("Database connection is successful!")

def get_db():
    """
    Dependency that provides a database session
    """
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()