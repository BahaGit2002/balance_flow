from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PaymentResponse(BaseModel):
    id: int
    transaction_id: str
    amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
