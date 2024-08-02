from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from src.reports.models import FishingTackle, RiverFish


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class ReportCreate(BaseModel):
    title: str
    description: str
    tackle: FishingTackle


class ReportCreateResponse(BaseModel):
    title: str
    description: str
    tackle: FishingTackle
    created_at: datetime


class FishCreate(BaseModel):
    fish_type: RiverFish
    total_weight: float
    total_count: int


class FishEdit(BaseModel):
    total_weight: float
    total_count: int


class CaughtFishResponse(BaseModel):
    id: int
    report_id: int
    fish_type: RiverFish
    total_weight: float
    total_count: int


class ImageResponse(BaseModel):
    id: int
    path: str
    report_id: int


class CommentResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    report_id: int
    user_id: int


class StarResponse(BaseModel):
    id: int
    report_id: int
    user_id: int


class ReportResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    tackle: FishingTackle
    created_at: datetime
    user_id: int
    caught_fish: List[CaughtFishResponse]
    images: List[ImageResponse]
    comments: List[CommentResponse]
    stars: List[StarResponse]
