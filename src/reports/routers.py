from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.reports.schemas import ReportCreate, FishCreate
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


@router.put("/{report_id}/edit")
async def edit_report(
        report_id: int,
        report_create: ReportCreate,
        current_user: Annotated[User, Depends(UserService().get_current_user)]
):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this report")

    await ReportService().edit_report(report, report_create)

    return {"success": "ok"}


@router.delete("/{report_id}/delete")
async def delete_report(report_id: int, current_user: Annotated[User, Depends(UserService().get_current_user)]):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this report")

    await ReportService().delete_report(report)

    return {"success": "ok"}


@router.get("/all")
async def get_all_reports():
    reports = await ReportService().get_all_reports()
    return reports


@router.get("/{report_id}")
async def get_report_by_id(report_id: int):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


@router.post("/{report_id}/stared")
async def stared_report(current_user: Annotated[User, Depends(UserService().get_current_user)], report_id: int):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id == current_user.id:
        raise HTTPException(status_code=403, detail="You can't star your own report")

    await ReportService().stared_report(report, current_user)

    return {"success": "ok"}


@router.post("/{report_id}/comment")
async def comment_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        report_id: int,
        comment: str):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    await ReportService().comment_report(report, current_user, comment)

    return {"success": "ok"}


@router.delete("/comment")
async def delete_comment(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        comment_id: int):
    comment = await ReportService().get_comment_by_id(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access error")

    await ReportService().delete_comment(comment)

    return {"success": "ok"}


@router.delete("/{report_id}")
async def delete_report(current_user: Annotated[User, Depends(UserService().get_current_user)], report_id: int):
    report = await ReportService().get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access error")

    await ReportService().delete_report(report)

    return {"success": "ok"}


@router.post("/{report_id}/fish/")
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


@router.delete("/{report_id}/fish/")
async def delete_fish_from_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        fish_id: int,
        report_id: int):
    fish = await ReportService().get_fish_by_id(fish_id)
    report = await ReportService().get_report_by_id(report_id)
    if fish is None:
        raise HTTPException(status_code=404, detail="Fish not found")
    if fish.report_id != report_id or report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access error")

    await ReportService().delete_fish_from_report(fish)

    return {"success": "ok"}
