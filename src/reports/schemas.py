import datetime

from pydantic import BaseModel

from src.reports.models import FishingTackle, RiverFish


class ReportCreate(BaseModel):
    title: str
    description: str
    tackle: FishingTackle


class ReportResponse(BaseModel):
    title: str
    description: str
    tackle: FishingTackle
    created_at: datetime.datetime


class FishCreate(BaseModel):
    fish_type: RiverFish
    total_weight: float
    total_count: int


class FishEdit(BaseModel):
    total_weight: float
    total_count: int
