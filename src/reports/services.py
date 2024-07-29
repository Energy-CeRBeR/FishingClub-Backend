from typing import List

from src.reports.models import Report, CaughtFish
from src.reports.repositories import ReportRepository
from src.reports.schemas import ReportCreate, FishCreate


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

    async def add_fish_to_report(self, report: Report, fish: FishCreate):
        return await self.repository.add_fish(fish, report)

    @staticmethod
    def caught_fish_to_dict(caught_fish: list[CaughtFish]) -> list[dict]:
        fishes = []
        for fish in caught_fish:
            fishes.append({
                "fish_type": fish.fish_type.value,
                "total_weight": fish.total_weight,
                "total_count": fish.total_count
            })

        return fishes
