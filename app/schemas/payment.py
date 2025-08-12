from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentResponse(BaseModel):
    id: int
    transaction_id: str
    amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
