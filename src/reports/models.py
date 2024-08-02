import datetime
from enum import Enum
from typing import Dict, Any

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class FishingTackle(Enum):
    feeder = "Фидер"
    float_rod = "Поплавочная удочка"
    carp_rod = "Карповое удилище"
    spinning = "Спиннинг"


class RiverFish(Enum):
    carp = "Карп"
    crucian_carp = "Карась"
    bream = "Лещ"
    rudd = "Плотва"
    perch = "Окунь"
    pike = "Щука"
    burbot = "Налим"
    asp = "Язь"
    ide = "Елец"
    tench = "Линь"
    roach = "Густера"
    chub = "Голавль"
    barbel = "Усач"
    zander = "Судак"
    eel = "Угорь"
    grayling = "Хариус"
    trout = "Форель"
    salmon = "Лосось"
    whitefish = "Сиг"
    pikeperch = "Судак"


class CaughtFish(Base):
    __tablename__ = "caught_fish"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"))
    fish_type: Mapped[RiverFish] = mapped_column()
    total_weight: Mapped[float] = mapped_column()
    total_count: Mapped[int] = mapped_column()

    report: Mapped["Report"] = relationship(back_populates="caught_fish", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "report_id": self.report_id,
            "fish_type": self.fish_type,
            "total_weight": self.total_weight,
            "total_count": self.total_count
        }


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column()
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"))

    report: Mapped["Report"] = relationship(back_populates="images", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "path": self.path,
            "report_id": self.report_id,
        }


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    report: Mapped["Report"] = relationship(back_populates="comments", uselist=False)
    user: Mapped["User"] = relationship(back_populates="comments", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "report_id": self.report_id,
            "user_id": self.user_id,
        }


class Star(Base):
    __tablename__ = "stars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    report: Mapped["Report"] = relationship(back_populates="stars", uselist=False)
    user: Mapped["User"] = relationship(back_populates="stars", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "report_id": self.report_id,
            "user_id": self.user_id,
        }


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    tackle: Mapped[FishingTackle] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    caught_fish: Mapped[list["CaughtFish"]] = relationship(back_populates="report", uselist=True, lazy="selectin",
                                                           cascade="all, delete-orphan")
    images: Mapped[list["Image"]] = relationship(back_populates="report", uselist=True, lazy="selectin",
                                                 cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="report", uselist=True, lazy="selectin",
                                                     cascade="all, delete-orphan")
    stars: Mapped[list["Star"]] = relationship(back_populates="report", uselist=True, lazy="selectin",
                                               cascade="all, delete-orphan")
    user: Mapped["User"] = relationship(back_populates="reports", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tackle": self.tackle,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
            "caught_fish": [fish.to_dict() for fish in self.caught_fish],
            "images": [image.to_dict() for image in self.images],
            "comments": [comment.to_dict() for comment in self.comments],
            "stars": [star.to_dict() for star in self.stars],
        }
