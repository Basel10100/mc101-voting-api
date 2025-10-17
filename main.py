import time

import uvicorn
from fastapi import FastAPI, Request, status
from jose import jwt

from api.users.UserEndpoints import AdminRouter, UserRouter
from config import Settings
from logger import get_logger
from utils.constants import Endpoints, ResponseMessages

# Loading the logger from logger.py
logger = get_logger()
settings = Settings()

# Making an instance of FastAPI as voting_app
voting_app = FastAPI(
    title="MC101 Notes & Voting API",
    description="Personal notes with encryption + sample voting endpoints",
    version="1.1.0",
    docs_url="/mc101docs",
    redoc_url="/mc101redoc",
)

# Adding the user router to the main application
voting_app.include_router(UserRouter)
voting_app.include_router(AdminRouter)
logger.info("User router has been included in the main application.")


@voting_app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    user_id = "-"
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer "):
        token = auth.split(" ", 1)[1]
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY.get_secret_value(),
                algorithms=[settings.JWT_ALGORITHM],
            )
            user_id = str(payload.get("user_id", "-"))
        except Exception:
            pass
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        f"%s %s %s user=%s %.1fms",
        request.method,
        request.url.path,
        response.status_code,
        user_id,
        duration_ms,
    )
    return response


@voting_app.get(Endpoints.ROOT, status_code=status.HTTP_200_OK)
def read_root():
    """
    A docstring describing the root endpoint
    """
    return {"message": ResponseMessages.WELCOME, "status": status.HTTP_200_OK}


@voting_app.get(Endpoints.HEALTH)
def read_health():
    return {"message": ResponseMessages.HEALTH_OK, "status": status.HTTP_200_OK}


logger.info("Health check endpoint is set up.")
logger.info(
    "Application setup is complete. Going to start the server if this is the main module."
)
