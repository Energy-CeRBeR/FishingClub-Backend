from typing import Optional, List

from sqlalchemy import select, insert, delete, and_

from src.database import async_session
from src.reports.models import Report, Image, CaughtFish, Star
from src.reports.schemas import ReportCreate, FishCreate
from src.users.models import User


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

    async def get_all_user_reports(self, user_id: int) -> List[Report]:
        async with async_session() as session:
            stmt = select(Report).where(Report.user_id == user_id)
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

    async def stared_report(self, report: Report, user: User, flag: bool) -> None:
        async with async_session() as session:
            if not flag:
                stmt = insert(Star).values(user_id=user.id, report_id=report.id)
            else:
                stmt = delete(Star).where(and_(Star.user_id == user.id, Star.report_id == report.id))
            await session.execute(stmt)
            await session.commit()

    async def add_fish(self, fish: FishCreate, report: Report) -> None:
        fish_dc = fish.dict()
        fish_dc["report_id"] = report.id
        async with async_session() as session:
            stmt = insert(CaughtFish).values(**fish_dc)
            await session.execute(stmt)
            await session.commit()
