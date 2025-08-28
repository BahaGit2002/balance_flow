import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import status
from app.models import User
from sqlalchemy import select


@pytest.mark.asyncio
async def test_register_user_success(
    client: AsyncClient, async_session: AsyncSession
):
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }
    response = await client.post("auth/register", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()
    token = response.json()
    assert isinstance(token["access_token"], str)
    assert len(token["access_token"]) > 0

    result = await async_session.execute(
        select(User).where(User.email == user_data["email"])
    )
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]


@pytest.mark.asyncio
async def test_register_duplicate_user(
    client: AsyncClient, async_session: AsyncSession
):
    user_data = {
        "email": "duplicate@example.com",
        "password": "TestPassword123!",
        "full_name": "Duplicate User"
    }

    response1 = await client.post("auth/register", json=user_data)
    assert response1.status_code == status.HTTP_201_CREATED

    result = await async_session.execute(
        select(User).where(User.email == user_data["email"])
    )
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.email == user_data["email"]

    response2 = await client.post("auth/register", json=user_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert response2.json()[
               "detail"] == f"User with email {user_data['email']} already exists."


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    user_data = {
        "email": "login@example.com",
        "password": "TestPassword123!",
        "full_name": "Login User"
    }
    register_response = await client.post("auth/register", json=user_data)
    assert register_response.status_code == status.HTTP_201_CREATED

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    login_response = await client.post("auth/login", json=login_data)

    assert login_response.status_code == status.HTTP_200_OK
    assert "access_token" in login_response.json()
    token = login_response.json()
    assert isinstance(token["access_token"], str)
    assert len(token["access_token"]) > 0


@pytest.mark.asyncio
async def test_login_invalid_email(client: AsyncClient):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "TestPassword123!"
    }
    response = await client.post("auth/login", json=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    user_data = {
        "email": "wrongpass@example.com",
        "password": "TestPassword123!",
        "full_name": "Wrong Pass User"
    }
    register_response = await client.post("auth/register", json=user_data)
    assert register_response.status_code == status.HTTP_201_CREATED

    login_data = {
        "email": user_data["email"],
        "password": "WrongPassword123!"
    }
    login_response = await client.post("auth/login", json=login_data)

    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert login_response.json()["detail"] == "Invalid email or password."


@pytest.mark.asyncio
async def test_register_missing_fields(client: AsyncClient):
    user_data = {
        "email": "missing@example.com",
        # Password and full_name are missing
    }
    response = await client.post("auth/register", json=user_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_login_missing_fields(client: AsyncClient):
    login_data = {
        "email": "missing@example.com"
        # Password is missing
    }
    response = await client.post("auth/login", json=login_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()
