from pydantic import BaseModel, EmailStr

from src.users.models import Gender


class UserCreate(BaseModel):
    name: str
    surname: str
    short_name: str
    email: EmailStr
    gender: Gender
    password: bytes


class UserLogin:
    short_name: str
    email: EmailStr
    password: bytes


