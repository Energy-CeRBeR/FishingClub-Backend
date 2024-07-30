import datetime
from enum import Enum
from typing import Dict, Any

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


# from src.users.models import User


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
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    fish_type: Mapped[RiverFish] = mapped_column()
    total_weight: Mapped[float] = mapped_column()
    total_count: Mapped[int] = mapped_column()

    report: Mapped["Report"] = relationship(back_populates="caught_fish", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "fish_type": self.fish_type,
            "total_weight": self.total_weight,
            "total_count": self.total_count
        }


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column()
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))

    report: Mapped["Report"] = relationship(back_populates="images", uselist=False)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    report: Mapped["Report"] = relationship(back_populates="comments", uselist=False)
    user: Mapped["User"] = relationship(back_populates="comments", uselist=False)


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    tackle: Mapped[FishingTackle] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    stars: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    caught_fish: Mapped[list["CaughtFish"]] = relationship(back_populates="report", uselist=True, lazy="selectin")
    images: Mapped[list["Image"]] = relationship(back_populates="report", uselist=True, lazy="selectin")
    comments: Mapped[list["Comment"]] = relationship(back_populates="report", uselist=True, lazy="selectin")
    user: Mapped["User"] = relationship(back_populates="reports", uselist=False)
