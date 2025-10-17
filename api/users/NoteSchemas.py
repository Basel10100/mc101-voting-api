import datetime
from typing import Optional

from pydantic import BaseModel, SecretStr


class NoteCreateSchema(BaseModel):
    title: str
    content: str
    personal_encryption: bool = False
    password: Optional[SecretStr] = None  # used when personal_encryption=True


class NoteUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    # To re-encrypt, client may pass personal_encryption and password again
    personal_encryption: Optional[bool] = None
    password: Optional[SecretStr] = None


class NoteResponseSchema(BaseModel):
    id: int
    title: str
    content: str  # decrypted content when returned
    personal_encryption: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
