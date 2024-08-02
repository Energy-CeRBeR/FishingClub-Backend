from pydantic import BaseModel

from src.reports.models import Report
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


class UserLogin:
    short_name: str
    email: str
    password: bytes


class UserResponse(BaseModel):
    id: int
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

# class User(BaseModel):
#     user_id: int
#     name: str
#     surname: str
#     short_name: str
#     email: str
#     email_verified: bool
#     gender: Gender
#     created_at: Optional[datetime] = Field(None, alias="createdAt")
#     reports: List[Report] = []
#     comments: List[Comment] = []
#     stars: List[Star] = []
