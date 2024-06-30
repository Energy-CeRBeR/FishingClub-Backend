import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Roles(Enum):
    user = "user"
    admin = "admin"


class Gender(Enum):
    male = "male"
    female = "female"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    short_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    gender: Mapped[Gender] = mapped_column(default=Gender.male)
    role: Mapped[Roles] = mapped_column(default=Roles.user)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
