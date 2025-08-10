from typing import Any, Coroutine

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from app.models import User, Account
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_email(self, email: EmailStr) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate) -> User:
        user = User(**user.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_accounts(self, email: EmailStr) -> Mapped[list[Any]]:
        user = await self.get_by_email(email)
        return user.accounts

    async def get_user_payments(self, email: EmailStr) -> Mapped[list[Any]]:
        user = await self.get_by_email(email)
        return user.payments
