from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_transaction_id(
        self, transaction_id: str
    ) -> Payment | None:
        result = await self.db.execute(
            select(Payment).where(Payment.transaction_id == transaction_id)
        )
        return result.scalar_one_or_none()

    async def create(self, transaction_id: str, user_id: int, account_id: int, amount: Decimal) -> Payment:
        payment = Payment(
            transaction_id=transaction_id,
            user_id=user_id,
            account_id=account_id,
            amount=amount
        )
        self.db.add(payment)
        await self.db.flush()
        return payment
