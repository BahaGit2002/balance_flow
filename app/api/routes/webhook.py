from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.webhook import Webhook
from app.services.webhook import WebhookService
from app.utils.webhook import verify_signature

router = APIRouter()


@router.post("", status_code=200)
async def process_webhook(
    payload: Webhook,
    db: AsyncSession = Depends(get_db),
):
    is_valid = verify_signature(
        account_id=payload.account_id,
        amount=payload.amount,
        transaction_id=payload.transaction_id,
        user_id=payload.user_id,
        signature=payload.signature,
    )
    if is_valid:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature",
        )

    service = WebhookService(db=db)
    result = await service.process_webhook(payload)
    return result
