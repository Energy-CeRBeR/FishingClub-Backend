from typing import List

from src.reports.models import Report
from src.reports.repositories import ReportRepository
from src.reports.schemas import ReportCreate


class ReportService:
    repository = ReportRepository()

    async def create_report(self, report: ReportCreate, user_id: int) -> None:
        return await self.repository.create_report(report, user_id)

    async def get_all_reports(self) -> List[Report]:
        return await self.repository.get_all_reports()

    async def get_report_by_id(self, report_id: int) -> Report:
        return await self.repository.get_report_by_id(report_id)

    async def delete_report(self, report: Report) -> None:
        return await self.repository.delete_report(report)
