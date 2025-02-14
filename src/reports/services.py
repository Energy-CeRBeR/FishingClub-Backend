from typing import List

from src.reports.exceptions import ReportNotFoundException, SelfReportStarException, CommentNotFoundException, \
    FishAlreadyExistsException, FishNotFoundException
from src.reports.models import Report, CaughtFish, Comment
from src.reports.repositories import ReportRepository
from src.reports.schemas import ReportCreate, FishCreate, FishEdit, ReportEdit

from src.users.models import User


class ReportService:
    repository = ReportRepository()

    async def create_report(self, report: ReportCreate, user_id: int) -> Report:
        return await self.repository.create_report(report, user_id)

    async def edit_report(self, report_id: int, edited_report: ReportEdit, user: User) -> Report:
        report = await self.get_report_by_id(report_id)
        if report.user_id != user.id:
            raise ReportNotFoundException()

        return await self.repository.edit_report(report, edited_report)

    async def get_all_reports(self) -> List[Report]:
        return await self.repository.get_all_reports()

    async def get_all_user_reports(self, user_id: int) -> List[Report]:
        return await self.repository.get_all_user_reports(user_id)

    async def get_report_by_id(self, report_id: int) -> Report:
        report = await self.repository.get_report_by_id(report_id)
        if report is None:
            raise ReportNotFoundException()

        return report

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        comment = await self.repository.get_comment_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundException()

    async def delete_report(self, report_id: int, user: User) -> None:
        report = await self.get_report_by_id(report_id)
        if report.user_id != user.id:
            raise ReportNotFoundException()

        return await self.repository.delete_report(report)

    async def add_fish_to_report(self, report_id: int, new_fish: FishCreate, user: User) -> Report:
        report = await self.get_report_by_id(report_id)
        if report.user_id != user.id:
            raise ReportNotFoundException()
        if any(fish.fish_type == new_fish.fish_type for fish in report.caught_fish):
            raise FishAlreadyExistsException()

        return await self.repository.add_fish(new_fish, report)

    async def edit_fish_in_report(self, fish_id: int, edit_fish: FishEdit, report_id: int, user: User) -> Report:
        fish = await self.get_fish_by_id(fish_id)
        report = await self.get_report_by_id(report_id)
        if report.user_id != user.id or fish.report_id != report_id:
            raise ReportNotFoundException()

        return await self.repository.edit_fish(fish, edit_fish, report)

    async def delete_fish_from_report(self, fish_id: int, report_id: int, user: User) -> None:
        fish = await self.get_fish_by_id(fish_id)
        report = await self.get_report_by_id(report_id)
        if report.user_id != user.id or fish.report_id != report_id:
            raise ReportNotFoundException()

        return await self.repository.delete_fish(fish)

    async def get_fish_by_id(self, fish_id: int) -> CaughtFish:
        fish = await self.repository.get_fish_by_id(fish_id)
        if fish is None:
            raise FishNotFoundException()

        return fish

    async def stared_report(self, report_id: int, user: User) -> Report:
        report = await self.get_report_by_id(report_id)
        if report.user_id == user.id:
            raise SelfReportStarException()

        flag = self.is_stared(report, user)
        return await self.repository.stared_report(report, user, flag)

    async def comment_report(self, report_id: int, user: User, text: str) -> Report:
        report = await self.get_report_by_id(report_id)
        return await self.repository.comment_report(report, user, text)

    async def delete_comment(self, comment_id: int, user: User) -> None:
        comment = await self.get_comment_by_id(comment_id)
        if comment.user_id != user.id:
            raise CommentNotFoundException()
        return await self.repository.delete_comment(comment)

    @staticmethod
    def is_stared(report: Report, user: User):
        for star in user.stars:
            if star.report_id == report.id:
                return True
        return False

    @staticmethod
    def reports_to_dict(reports: list[Report]) -> list[Report]:
        response = []
        for report in reports:
            response.append(report)
        return response
