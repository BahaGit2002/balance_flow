from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account
from app.services.account import generate_account_number


class AccountRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, ID: int) -> Account | None:
        result = await self.db.execute(select(Account).where(Account.id == ID))
        return result.scalar_one_or_none()

    async def get_by_id_user_id(self, ID: int, user_id: int) -> Account | None:
        result = await self.db.execute(
            select(Account).where(
                (Account.id == ID) & (Account.user_id == user_id)
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, account_id: int, amount: Decimal) -> Account:
        account_number = await generate_account_number()
        account = Account(
            id=account_id,
            user_id=user_id,
            balance=amount,
            account_number=account_number
        )
        self.db.add(account)
        await self.db.flush()
        return account

    async def update(self, account_id: int, amount: Decimal) -> Account | None:
        account = await self.get_by_id(account_id)
        if account is None:
            return None
        account.balance += amount
        await self.db.flush()
        return account
