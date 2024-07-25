from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from src.reports.models import Report
from src.reports.schemas import ReportCreate, ReportResponse, FishCreate
from src.reports.services import ReportService
from src.users.models import User
from src.users.services import UserService

router = APIRouter(tags=["fishing"], prefix="/reports")


@router.post("/new")
async def create_report(
        report_create: ReportCreate,
        current_user: Annotated[User, Depends(UserService().get_current_user)]
):
    await ReportService().create_report(report=report_create, user_id=current_user.id)
    return {"success": "ok"}


@router.get("/all", response_model=List[ReportResponse])
async def get_all_reports() -> List[Report]:
    reports = await ReportService().get_all_reports()
    return reports


@router.get("/{report_id}")
async def get_report_by_id(report_id: int):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/{report_id}/add_fish/")
async def add_fish_to_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        fish: FishCreate,
        report_id: int):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access error")

    await ReportService().add_fish_to_report(report, fish)
    return {"success": "ok"}


@router.post("/{report_id}/fishes")
async def get_fishes_in_report(report_id: int):
    report = await ReportService().get_report_by_id(report_id)
    print("OKKKKKK")
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    fishes = report.caught_fishes
    print(type(fishes))
    return {"success": "ok"}
