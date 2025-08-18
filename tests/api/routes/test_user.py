from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload

from app.database.database import get_db
from app.main import app
from app.models import Account
from app.models.user import User
from app.config.security import hash_password, create_jwt


@pytest.mark.asyncio
async def test_get_me(client, async_session):
    user = User(
        full_name="Test User",
        email="testMe@example.com",
        password=hash_password("hashed")
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    token = create_jwt({'user_id': user.id, 'email': user.email})

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["full_name"] == user.full_name
    assert data["email"] == user.email


@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    response = await client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing token"}


@pytest.mark.asyncio
async def test_get_accounts(client, async_session, engine):
    user2 = User(
        full_name="Test User",
        email="testMe2@example.com",
        password=hash_password("hashed")
    )
    async_session.add(user2)
    await async_session.commit()
    await async_session.refresh(user2)

    account1 = Account(
        account_number="Test Account 1",
        user_id=user2.id,
        balance=Decimal("100")
    )
    account2 = Account(
        account_number="Test Account 2",
        user_id=user2.id,
        balance=Decimal("200")
    )

    async_session.add_all([account1, account2])
    await async_session.commit()
    await async_session.refresh(account1)
    await async_session.refresh(account2)

    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with AsyncSessionLocal() as new_session:
        async def override_get_db():
            yield new_session

        app.dependency_overrides[get_db] = override_get_db

        token = create_jwt({'user_id': user2.id, 'email': user2.email})
        response = await client.get(
            "/users/accounts",
            headers={"Authorization": f"Bearer {token}"}
        )
        app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["account_number"] == "Test Account 1"
    assert data[1]["account_number"] == "Test Account 2"


@pytest.mark.asyncio
async def test_get_accounts_unauthorized(client):
    response = await client.get("/users/accounts")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing token"}


@pytest.mark.asyncio
async def test_get_payments(client, async_session, engine):
    user = User(
        full_name="Test User",
        email="testPayment@example.com",
        password=hash_password("hashed")
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    account1 = Account(
        account_number="Test Account 1",
        user_id=user.id,
        balance=Decimal("100")
    )
    account2 = Account(
        account_number="Test Account 2",
        user_id=user.id,
        balance=Decimal("200")
    )

    async_session.add_all([account1, account2])
    await async_session.commit()
    await async_session.refresh(account1)
    await async_session.refresh(account2)
