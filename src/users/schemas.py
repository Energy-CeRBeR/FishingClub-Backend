from pydantic import BaseModel

from src.reports.models import Report
from src.users.models import Gender


class UserCreate(BaseModel):
    name: str
    surname: str
    short_name: str
    email: str
    gender: Gender
    password: str


class UserLogin:
    short_name: str
    email: str
    password: bytes


class UserResponse(BaseModel):
    name: str
    surname: str
    short_name: str
    email: str
    email_verified: bool
    gender: Gender


class TokenData(BaseModel):
    short_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
