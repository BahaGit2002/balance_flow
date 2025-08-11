from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    account_number: str
    balance: Decimal

    model_config = {
        "from_attributes": True,
    }
