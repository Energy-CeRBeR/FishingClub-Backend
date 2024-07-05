from pydantic import BaseModel

from src.reports.models import FishingTackle


class ReportCreate(BaseModel):
    title: str
    description: str
    tackle: FishingTackle

