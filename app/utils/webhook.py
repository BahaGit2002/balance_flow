import hashlib
from decimal import Decimal


def verify_signature(
    account_id: int,
    amount: Decimal,
    transaction_id: str,
    user_id: int,
    signature: str,
) -> bool:
    data_string = f"{account_id}{amount:.0f}{transaction_id}{user_id}{signature}"
    computed_signature = hashlib.sha256(
        data_string.encode("utf-8")
    ).hexdigest()
    return computed_signature == signature
