from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.accounts import AccountRepository
from app.repositories.payments import PaymentRepository
from app.repositories.users import UserRepository
from app.schemas.webhook import Webhook


class WebhookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.account_repo = AccountRepository(db)
        self.payment_repo = PaymentRepository(db)

    async def process_webhook(self, payload: Webhook):
        user = await self.user_repo.get_by_id(payload.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        existing_payment = await self.payment_repo.get_by_transaction_id(
            payload.transaction_id
        )
        if existing_payment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction already processed"
            )

        account = await self.account_repo.get_by_id_user_id(
            payload.account_id,
            payload.user_id
        )
        if not account:
            account = await self.account_repo.create(
                user_id=payload.user_id,
                account_id=payload.account_id,
                amount=Decimal("0.00"),
            )

        await self.payment_repo.create(
            transaction_id=payload.transaction_id,
            user_id=payload.user_id,
            account_id=payload.account_id,
            amount=Decimal(payload.amount),
        )
        await self.account_repo.update(
            account_id=account.id,
            amount=Decimal(payload.amount),
        )
        await self.db.commit()
        return {"status": "success", "transaction_id": payload.transaction_id}
