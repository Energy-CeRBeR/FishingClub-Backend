import datetime

from pydantic import BaseModel

from src.reports.models import FishingTackle


class ReportCreate(BaseModel):
    title: str
    description: str
    tackle: FishingTackle


class ReportResponse(BaseModel):
    title: str
    description: str
    tackle: FishingTackle
    created_at: datetime.datetime
