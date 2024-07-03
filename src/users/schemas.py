from pydantic import BaseModel

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


