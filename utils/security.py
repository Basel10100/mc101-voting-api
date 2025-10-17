from datetime import datetime, timezone, timedelta
import uuid
from passlib.context import CryptContext
# from api.users.UserDBModels import get_user_by_email
from config import Settings
from pydantic import SecretStr
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from db.DBModels import UserDBModel, TokenBlacklist
from db.DbConfig import get_db
from utils.constants import ResponseMessages

settings = Settings()

def hash_context() -> CryptContext:
    # deprecated="auto" will mark old algorithms as deprecated when a new one is added
    # .needs_update() can be used to check if a hash needs to be updated
    return CryptContext(schemes=["bcrypt", "pbkdf2_sha256", "argon2"], deprecated="auto")

def hash_password(password: SecretStr) -> str:
    pwd_context = hash_context()
    return pwd_context.hash(password.get_secret_value())


def verify_password(plain_password: SecretStr, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    pwd_context = hash_context()
    return pwd_context.verify(plain_password.get_secret_value(), hashed_password)


def create_access_token(data: dict) -> str: 
    """
    Create a JWT token with an expiration time.
    """ 
    data_to_encode = data.copy() 
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION_TIME)
    # Convert datetime to Unix timestamp (seconds since epoch) as required by JWT
    jti = str(uuid.uuid4())
    data_to_encode.update({"exp": expire_time.timestamp(), "jti": jti})  # Add expiration and unique token id
    encoded_jwt = jwt.encode(
        data_to_encode,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM
    ) 
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def decode_access_token(token: str = Depends(oauth2_scheme), db = Depends(get_db)) -> dict:
    """
    Decode a JWT token and return the payload.
    """
    try:
        # This code will try to decode the JWT token and if it fails, it will raise an exception
        # As the result of this exception rais, try will fail. When any code inside the try block
        # fails, automatically code jumps to the except block and do not execute the rest of the try block
        payload = jwt.decode(token, settings.JWT_SECRET_KEY.get_secret_value(), algorithms=[settings.JWT_ALGORITHM])
        
        # Check if payload has required fields
        email = payload.get("email")
        if not email:
            # If no email, if will raise
            raise JWTError(status_code=401, detail=ResponseMessages.INVALID_TOKEN_MISSING_EMAIL)
        # Blacklist check
        jti = payload.get("jti")
        if jti:
            bl = db.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first()
            if bl:
                raise JWTError("Token is revoked")
        user = db.query(UserDBModel).filter(UserDBModel.email == email).first()
        if not user:
            raise JWTError(status_code=401, detail=ResponseMessages.INVALID_TOKEN_MISSING_USER) 
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=ResponseMessages.INVALID_TOKEN)