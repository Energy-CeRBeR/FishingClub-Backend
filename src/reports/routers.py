from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.reports.schemas import ReportCreate, FishCreate, FishEdit, ReportResponse, SuccessfulResponse, ReportEdit
from src.reports.services import ReportService
from src.users.models import User
from src.users.services import UserService

router = APIRouter(tags=["fishing"], prefix="/reports")


@router.post("/new", response_model=ReportResponse)
async def create_report(
        report_create: ReportCreate,
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> ReportResponse:
    report = await ReportService().create_report(report=report_create, user_id=current_user.id)
    return ReportResponse(**report.to_dict())


@router.put("/{report_id}/edit", response_model=ReportResponse)
async def edit_report(
        report_id: int,
        edited_report: ReportEdit,
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> ReportResponse:
    upd_report = await ReportService().edit_report(report_id, edited_report, current_user)
    return ReportResponse(**upd_report.to_dict())


@router.delete("/{report_id}/delete", response_model=SuccessfulResponse)
async def delete_report(
        report_id: int,
        current_user: Annotated[User, Depends(UserService().get_current_user)]
) -> SuccessfulResponse:
    await ReportService().delete_report(report_id, current_user)
    return SuccessfulResponse()


@router.get("/all", response_model=list[ReportResponse])
async def get_all_reports() -> list[ReportResponse]:
    reports = await ReportService().get_all_reports()
    return list(map(lambda x: ReportResponse(**x.to_dict()), reports))


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report_by_id(report_id: int) -> ReportResponse:
    report = await ReportService().get_report_by_id(report_id)
    return ReportResponse(**report.to_dict())


@router.post("/{report_id}/stared", response_model=ReportResponse)
async def stared_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        report_id: int
) -> ReportResponse:
    upd_report = await ReportService().stared_report(report_id, current_user)
    return ReportResponse(**upd_report.to_dict())


@router.post("/{report_id}/comment", response_model=ReportResponse)
async def comment_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        report_id: int,
        comment: str
) -> ReportResponse:
    commented_report = await ReportService().comment_report(report_id, current_user, comment)
    return ReportResponse(**commented_report.to_dict())


@router.delete("/comment", response_model=SuccessfulResponse)
async def delete_comment(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        comment_id: int
) -> SuccessfulResponse:
    await ReportService().delete_comment(comment_id, current_user)
    return SuccessfulResponse()


@router.post("/{report_id}/fish/", response_model=ReportResponse)
async def add_fish_to_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        new_fish: FishCreate,
        report_id: int
) -> ReportResponse:
    upd_report = await ReportService().add_fish_to_report(report_id, new_fish, current_user)
    return ReportResponse(**upd_report.to_dict())


@router.put("/{report_id}/fish/", response_model=ReportResponse)
async def edit_fish_in_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        edit_fish: FishEdit,
        fish_id: int,
        report_id: int
) -> ReportResponse:
    upd_report = await ReportService().edit_fish_in_report(fish_id, edit_fish, report_id, current_user)
    return ReportResponse(**upd_report.to_dict())


@router.delete("/{report_id}/fish/", response_model=SuccessfulResponse)
async def delete_fish_from_report(
        current_user: Annotated[User, Depends(UserService().get_current_user)],
        fish_id: int,
        report_id: int
) -> SuccessfulResponse:
    await ReportService().delete_fish_from_report(fish_id, report_id, current_user)
    return SuccessfulResponse()
