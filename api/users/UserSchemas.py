import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    # hashed_password: Optional[str] = None  # This will store the hashed password
    is_active: bool = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserRegisterResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool


class UserLoginResponseSchema(BaseModel):
    authentication_type: str
    token: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class PasswordChangeSchema(BaseModel):
    current_password: SecretStr
    new_password: SecretStr


class LogoutResponseSchema(BaseModel):
    message: str


class ChangePasswordSchema(BaseModel):
    current_password: SecretStr
    new_password: SecretStr


class VotingSchema(BaseModel):
    candidate_id: int


class VoteCountResponseSchema(BaseModel):
    candidate_id: int
    candidate_name: str
    vote_count: int


class CandidateSchema(BaseModel):
    id: Optional[int] = None
    name: str
    party: Optional[str] = "independent"  # Party can be optional


class VoteResponseSchema(BaseModel):
    id: int
    user_id: int
    candidate_id: int
    created_at: datetime.datetime
