from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import SecretStr, ConfigDict
from typing import Optional
from dotenv import load_dotenv

load_dotenv(".env")  # take environment variables from .env file


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra environment variables
    )
    
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int = 3600
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: Optional[str] = ""
    POSTGRES_HOST: Optional[str] = ""
    POSTGRES_PORT_ON_MACHINE: Optional[int] = None
    POSTGRES_PORT_IN_DOCKER: Optional[int] = None
    # App-level encryption secret used to derive note encryption keys when personal encryption is not provided
    APP_ENCRYPTION_KEY: SecretStr
    RUNTIME: str = "development"  # "development", "test", or "production"
    TEST_DB_URL: str = ""  # Only used when RUNTIME=test
    PRODUCTION_VOTING_APP_IMAGE_NAME: Optional[str] = None
    PRODUCTION_SERVER_IP: Optional[str] = None
    PRODUCTION_SERVER_USER: Optional[str] = None
    PRODUCTION_SSH_KEY: Optional[SecretStr] = None
