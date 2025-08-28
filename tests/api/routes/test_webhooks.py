import pytest
import hashlib
from decimal import Decimal
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException, status


@pytest.mark.asyncio
async def test_process_webhook_valid_signature_success(client):
    payload = {
        "transaction_id": "tx_123",
        "user_id": 1,
        "account_id": 1,
        "amount": "100.00",
        "signature": ""
    }

    data_string = f"{payload['account_id']}{Decimal(payload['amount']):.0f}{payload['transaction_id']}{payload['user_id']}"
    payload["signature"] = hashlib.sha256(
        data_string.encode("utf-8")
    ).hexdigest()

    with patch(
            "app.services.webhook.WebhookService.process_webhook",
            new=AsyncMock()
    ) as mock_service:
        mock_service.return_value = {
            "status": "success", "transaction_id": "tx_123"
        }

        response = await client.post("/webhook", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "success", "transaction_id": "tx_123"}
    mock_service.assert_called_once()


@pytest.mark.asyncio
async def test_process_webhook_invalid_signature(client):
    payload = {
        "transaction_id": "tx_123",
        "user_id": 1,
        "account_id": 1,
        "amount": "100.00",
        "signature": "invalid_signature"
    }

    response = await client.post("/webhook", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid signature"


@pytest.mark.asyncio
async def test_process_webhook_missing_fields(client):
    payload = {
        "transaction_id": "tx_123",
        "user_id": 1,
    }

    response = await client.post("/webhook", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()

    errors = response.json()["detail"]
    missing_fields = [error["loc"][-1] for error in errors]

    assert "account_id" in missing_fields
    assert "amount" in missing_fields
    assert "signature" in missing_fields


@pytest.mark.asyncio
async def test_process_webhook_invalid_amount_format(client):
    payload = {
        "transaction_id": "tx_123",
        "user_id": 1,
        "account_id": 1,
        "amount": "invalid_amount",
        "signature": "some_signature"
    }

    response = await client.post("/webhook", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_process_webhook_invalid_signature_real_function(client):
    payload = {
        "transaction_id": "tx_123",
        "user_id": 1,
        "account_id": 1,
        "amount": "100.00",
        "signature": "definitely_invalid_signature"
    }

    response = await client.post("/webhook", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid signature"


@pytest.mark.asyncio
async def test_process_webhook_service_exception(client):
    payload = {
        "transaction_id": "tx_123",
        "user_id": 1,
        "account_id": 1,
        "amount": "100.00",
        "signature": ""
    }

    data_string = f"{payload['account_id']}{Decimal(payload['amount']):.0f}{payload['transaction_id']}{payload['user_id']}"
    payload["signature"] = hashlib.sha256(
        data_string.encode("utf-8")
    ).hexdigest()

    with patch(
            "app.services.webhook.WebhookService.process_webhook",
            new=AsyncMock()
    ) as mock_service:
        mock_service.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

        response = await client.post("/webhook", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
