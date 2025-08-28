import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from datetime import datetime
from app.models import User
from app.schemas.user import UserCreate
from app.config.security import hash_password, create_jwt
from app.repositories.users import UserRepository


@pytest.fixture(autouse=True)
async def clean_database(async_session: AsyncSession):
    """Ensure a clean database state before each test."""
    await async_session.execute(delete(User))
    await async_session.commit()
    yield


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, async_session: AsyncSession):
    unique_email = f"test_{datetime.now().timestamp()}@example.com"
    user_data = UserCreate(
        full_name="Test User",
        email=unique_email,
        password=hash_password("testpassword123")
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create(user_data)

    token = create_jwt({"user_id": user.id, "email": user.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == user.id
    assert response_data["email"] == user.email
    assert response_data["full_name"] == user.full_name


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = await client.get("users/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid token"}


@pytest.mark.asyncio
async def test_get_me_missing_token(client: AsyncClient):
    response = await client.get("users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Missing token"}


@pytest.mark.asyncio
async def test_get_accounts(client: AsyncClient, async_session: AsyncSession):
    unique_email = f"test_{datetime.now().timestamp()}@example.com"
    user_data = UserCreate(
        full_name="Test User",
        email=unique_email,
        password=hash_password("testpassword123")
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create(user_data)

    token = create_jwt({"user_id": user.id, "email": user.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("users/accounts", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_get_payments(client: AsyncClient, async_session: AsyncSession):
    unique_email = f"test_{datetime.now().timestamp()}@example.com"
    user_data = UserCreate(
        full_name="Test User",
        email=unique_email,
        password=hash_password("testpassword123")
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create(user_data)

    token = create_jwt({"user_id": str(user.id), "email": user.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("users/payments", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0