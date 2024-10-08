import random
from typing import Optional, List

from sqlalchemy import select, insert, delete, and_, update

from src.database import async_session
from src.reports.models import Report, CaughtFish, Star, Comment
from src.reports.schemas import ReportCreate, FishCreate, FishEdit
from src.users.models import User


class ReportRepository:

    async def generate_id(self) -> int:
        new_id = random.randint(10000000, 99999999)
        while await self.get_report_by_id(new_id):
            new_id = random.randint(10000000, 99999999)
        return new_id

    async def create_report(self, report: ReportCreate, user_id: int) -> Report:
        report_dc = report.dict()
        report_dc["user_id"] = user_id
        report_dc["id"] = await self.generate_id()
        async with async_session() as session:
            stmt = insert(Report).values(**report_dc)
            await session.execute(stmt)
            await session.commit()

            new_report: Report = await self.get_report_by_id(report_dc["id"])
            return new_report

    async def edit_report(self, report: Report, report_create: ReportCreate) -> Report:
        report_dc = report_create.dict()
        async with async_session() as session:
            stmt = update(Report).where(Report.id == report.id).values(**report_dc)
            await session.execute(stmt)
            await session.commit()

            upd_report: Report = await self.get_report_by_id(report.id)
            return upd_report

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

    async def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        async with async_session() as session:
            stmt = select(Comment).where(Comment.id == comment_id)
            result = await session.execute(stmt)
            comment = result.scalars().first()
        return comment

    async def delete_report(self, report: Report) -> None:
        async with async_session() as session:
            stmt = delete(Report).where(Report.id == report.id)
            await session.execute(stmt)
            await session.commit()

    async def stared_report(self, report: Report, user: User, flag: bool) -> Report:
        async with async_session() as session:
            if not flag:
                stmt = insert(Star).values(user_id=user.id, report_id=report.id)
            else:
                stmt = delete(Star).where(and_(Star.user_id == user.id, Star.report_id == report.id))
            await session.execute(stmt)
            await session.commit()

            upd_report: Report = await self.get_report_by_id(report.id)
            return upd_report

    async def comment_report(self, report: Report, user: User, text: str) -> Report:
        async with async_session() as session:
            stmt = insert(Comment).values(user_id=user.id, report_id=report.id, text=text)
            await session.execute(stmt)
            await session.commit()

            upd_report: Report = await self.get_report_by_id(report.id)
            return upd_report

    async def delete_comment(self, comment: Comment) -> None:
        async with async_session() as session:
            stmt = delete(Comment).where(Comment.id == comment.id)
            await session.execute(stmt)
            await session.commit()

    async def add_fish(self, fish: FishCreate, report: Report) -> Report:
        fish_dc = fish.dict()
        fish_dc["report_id"] = report.id
        async with async_session() as session:
            stmt = insert(CaughtFish).values(**fish_dc)
            await session.execute(stmt)
            await session.commit()

            upd_report: Report = await self.get_report_by_id(report.id)
            return upd_report

    async def edit_fish(self, fish: CaughtFish, edit_fish: FishEdit, report: Report) -> Report:
        fish_dc = edit_fish.dict()
        async with async_session() as session:
            stmt = update(CaughtFish).where(CaughtFish.id == fish.id).values(**fish_dc)
            await session.execute(stmt)
            await session.commit()

            upd_report: Report = await self.get_report_by_id(report.id)
            return upd_report

    async def delete_fish(self, fish: CaughtFish) -> None:
        async with async_session() as session:
            stmt = delete(CaughtFish).where(CaughtFish.id == fish.id)
            await session.execute(stmt)
            await session.commit()

    async def get_fish_by_id(self, fish_id: int) -> CaughtFish:
        async with async_session() as session:
            stmt = select(CaughtFish).where(CaughtFish.id == fish_id)
            result = await session.execute(stmt)
            fish = result.scalars().first()
        return fish
