from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.reports.schemas import ReportResponse
from src.users.models import Gender


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class UserCreate(BaseModel):
    name: str
    surname: str
    short_name: str
    email: str
    gender: Gender
    password: str


class UserEdit(BaseModel):
    name: str
    surname: str
    gender: Gender


# class UserLogin:
#     short_name: str
#     email: str
#     password: bytes


class TokenData(BaseModel):
    short_name: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    short_name: str
    email: str
    email_verified: bool
    gender: Gender
    created_at: datetime
    reports: List[ReportResponse]
