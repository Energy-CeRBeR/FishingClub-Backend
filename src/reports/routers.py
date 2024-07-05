from typing import Annotated

from fastapi import APIRouter, Depends

from src.reports.schemas import ReportCreate
from src.users.models import User
from src.users.services import UserService

router = APIRouter(tags=["fishing"], prefix="/fishing")


@router.post("/reports/new")
async def create_report(
        report_create: ReportCreate,
        current_user: Annotated[User, Depends(UserService().get_current_user)]
):
    pass


@router.get("/reports/all")
async def get_all_reports():
    pass
