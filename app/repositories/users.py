from typing import Any

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from app.models import User, Account
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, ID: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == ID))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate) -> User:
        user = User(**user.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        user.full_name = user_data.full_name
        user.email = user_data.email
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        await self.db.delete(user)
        await self.db.commit()
