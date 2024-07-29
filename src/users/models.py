import datetime
from enum import Enum
from typing import Dict, Any

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from src.reports.models import Report

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
    password_hash: Mapped[bytes] = mapped_column()
    gender: Mapped[Gender] = mapped_column(default=Gender.male)
    role: Mapped[Roles] = mapped_column(default=Roles.user)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    reports: Mapped[list["Report"]] = relationship(back_populates="user", uselist=True, lazy="selectin")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "surname": self.surname,
            "short_name": self.short_name,
            "email": self.email,
            "email_verified": self.email_verified,
            "gender": self.gender,
        }
