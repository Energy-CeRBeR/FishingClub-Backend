import datetime
from enum import Enum
from typing import Dict, Any

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Gender(Enum):
    male = "male"
    female = "female"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    gender: Mapped[Gender] = mapped_column(default=Gender.male, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now(), nullable=False)

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
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "gender": self.gender.value,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "reports": [report.to_dict() for report in self.reports],
            "comments": [comment.to_dict() for comment in self.comments],
            "stars": [star.to_dict() for star in self.stars],
        }
