import datetime
from enum import Enum
from typing import Dict, Any, List

from sqlalchemy import ForeignKey, func, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from src.users.models import User

from src.database import Base


class FishingTackle(Enum):
    feeder = "Фидер"
    float_rod = "Поплавочная удочка"
    carp_rod = "Карповое удилище"
    spinning = "Спиннинг"


class RiverFish(Enum):
    """50 самых популярных речных рыб"""
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
    weight: Mapped[float] = mapped_column()

    report: Mapped["Report"] = relationship("Report", back_populates="images")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    path: Mapped[str] = mapped_column()


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    tackle: Mapped[FishingTackle] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    caught_fishes: Mapped[List["CaughtFish"]] = relationship(
        "CaughtFish", back_populates="report", cascade="all, delete-orphan"
    )
    images: Mapped[List["Image"]] = relationship(
        "Image", back_populates="report", cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="reports")
