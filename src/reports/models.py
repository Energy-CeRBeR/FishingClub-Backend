import datetime
from enum import Enum
from typing import List

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

    report: Mapped["Report"] = relationship("Report", back_populates="images")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column()
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

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
