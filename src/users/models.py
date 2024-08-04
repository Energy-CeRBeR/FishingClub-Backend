import datetime
from enum import Enum
from typing import Dict, Any

from sqlalchemy import func
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

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    short_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    password_hash: Mapped[bytes] = mapped_column()
    gender: Mapped[Gender] = mapped_column(default=Gender.male)
    role: Mapped[Roles] = mapped_column(default=Roles.user)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    reports: Mapped[list["Report"]] = relationship(back_populates="user", uselist=True, lazy="selectin",
                                                   cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user", uselist=True, lazy="selectin",
                                                     cascade="all, delete-orphan")
    stars: Mapped[list["Star"]] = relationship(back_populates="user", uselist=True, lazy="selectin",
                                               cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "short_name": self.short_name,
            "email": self.email,
            "email_verified": self.email_verified,
            "gender": self.gender.value,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "reports": [report.to_dict() for report in self.reports],
            "comments": [comment.to_dict() for comment in self.comments],
            "stars": [star.to_dict() for star in self.stars],
        }
