from typing import Optional, List

from sqlalchemy import select, insert, delete

from src.database import async_session
from src.reports.models import Report, Image, CaughtFish
from src.reports.schemas import ReportCreate, FishCreate


class ReportRepository:
    async def create_report(self, report: ReportCreate, user_id: int) -> None:
        report_dc = report.dict()
        report_dc["user_id"] = user_id
        async with async_session() as session:
            stmt = insert(Report).values(**report_dc)
            await session.execute(stmt)
            await session.commit()

    async def get_all_reports(self) -> List[Report]:
        async with async_session() as session:
            stmt = select(Report)
            result = await session.execute(stmt)
            reports = result.scalars().all()
        return reports

    async def get_report_by_id(self, report_id: int) -> Optional[Report]:
        async with async_session() as session:
            stmt = select(Report).where(Report.id == report_id)
            result = await session.execute(stmt)
            report = result.scalars().first()
        return report

    async def delete_report(self, report: Report) -> None:
        async with async_session() as session:
            stmt = delete(Report).where(Report.id == report.id)
            await session.execute(stmt)
            await session.commit()

    async def add_fish(self, fish: FishCreate, report: Report) -> None:
        fish_dc = fish.dict()
        fish_dc["report_id"] = report.id
        async with async_session() as session:
            stmt = insert(CaughtFish).values(**fish_dc)
            await session.execute(stmt)
            await session.commit()
