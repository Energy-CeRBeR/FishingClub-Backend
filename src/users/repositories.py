from typing import Optional

from sqlalchemy import insert, select, delete

from src.utils import auth_settings
from .models import User
from .schemas import UserCreate

from fastapi import HTTPException

from ..database import async_session


class UserRepository:

    async def create(self, user: UserCreate) -> User:
        async with async_session() as session:
            query = select(User).where(User.email == user.email)
            result = await session.execute(query)
            potential_user = result.mappings().all()
        if potential_user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        password = user.password
        user_dc = user.dict(exclude={"password"})
        user_dc["password_hash"] = auth_settings.hash_password(password)

        async with async_session() as session:
            stmt = insert(User).values(**user_dc)
            result = await session.execute(stmt)
            await session.commit()
            user = result.scalar_one()

        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            user = result.scalar_one()
        return user

    async def get_user_by_short_name(self, short_name: str) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.short_name == short_name)
            result = await session.execute(query)
            user = result.scalar_one()
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one()
        return user

    async def delete_user(self, user: User) -> None:
        async with async_session() as session:
            stmt = delete(User).where(User.id == user.id)
            await session.execute(stmt)
            await session.commit()
