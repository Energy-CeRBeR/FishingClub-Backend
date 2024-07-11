from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.reports.models import Report
from src.reports.schemas import ReportCreate, ReportResponse
from src.reports.services import ReportService
from src.users.models import User
from src.users.services import UserService

router = APIRouter(tags=["fishing"], prefix="/fishing")


@router.post("/reports/new")
async def create_report(
        report_create: ReportCreate,
        current_user: Annotated[User, Depends(UserService().get_current_user)]
):
    await ReportService().create_report(report=report_create, user_id=current_user.id)
    return {"success": "ok"}


@router.get("/reports/all", response_model=List[ReportResponse])
async def get_all_reports():
    reports = await ReportService().get_all_reports()
    return reports
