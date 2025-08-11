from decimal import Decimal

from pydantic import BaseModel


class Webhook(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: Decimal
    signature: str

    model_config = {
        "from_attributes": True
    }
