from typing import List

from src.reports.models import Report, CaughtFish, Comment
from src.reports.repositories import ReportRepository
from src.reports.schemas import ReportCreate, FishCreate
from src.users.models import User


class ReportService:
    repository = ReportRepository()

    async def create_report(self, report: ReportCreate, user_id: int) -> None:
        return await self.repository.create_report(report, user_id)

    async def get_all_reports(self) -> List[Report]:
        return await self.repository.get_all_reports()

    async def get_all_user_reports(self, user_id: int) -> List[Report]:
        return await self.repository.get_all_user_reports(user_id)

    async def get_report_by_id(self, report_id: int) -> Report:
        return await self.repository.get_report_by_id(report_id)

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        return await self.repository.get_comment_by_id(comment_id)

    async def delete_report(self, report: Report) -> None:
        return await self.repository.delete_report(report)

    async def add_fish_to_report(self, report: Report, fish: FishCreate):
        return await self.repository.add_fish(fish, report)

    async def stared_report(self, report: Report, user: User):
        flag = self.is_stared(report, user)
        return await self.repository.stared_report(report, user, flag)

    async def comment_report(self, report: Report, user: User, text: str):
        return await self.repository.comment_report(report, user, text)

    async def delete_comment(self, comment: Comment):
        return await self.repository.delete_comment(comment)

    @staticmethod
    def is_stared(report: Report, user: User):
        for star in user.stars:
            if star.report_id == report.id:
                return True
        return False

    @staticmethod
    def caught_fish_to_dict(caught_fish: list[CaughtFish]) -> list[dict]:
        response = []
        for fish in caught_fish:
            response.append({
                "fish_type": fish.fish_type.value,
                "total_weight": fish.total_weight,
                "total_count": fish.total_count
            })

        return response

    @staticmethod
    def reports_to_dict(reports: list[Report]) -> list[Report]:
        response = []
        for report in reports:
            response.append(report)
        return response
