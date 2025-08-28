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
    await async_session.execute(delete(User))
    await async_session.commit()
    yield


async def create_admin_user(async_session: AsyncSession, email: str) -> User:
    user_data = UserCreate(
        full_name="Admin User",
        email=email,
        password=hash_password("adminpassword123")
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create(user_data)
    user.is_admin = True
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_get_me_admin(client: AsyncClient, async_session: AsyncSession):
    unique_email = f"admin_{datetime.now().timestamp()}@example.com"
    admin = await create_admin_user(async_session, unique_email)

    token = create_jwt({"user_id": str(admin.id), "email": admin.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/admin/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == admin.id
    assert response_data["email"] == admin.email
    assert response_data["full_name"] == admin.full_name


@pytest.mark.asyncio
async def test_get_me_non_admin(
    client: AsyncClient, async_session: AsyncSession
):
    unique_email = f"user_{datetime.now().timestamp()}@example.com"
    user_data = UserCreate(
        full_name="Regular User",
        email=unique_email,
        password=hash_password("userpassword123")
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create(user_data)

    token = create_jwt({"user_id": str(user.id), "email": user.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/admin/me", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Admin access required"}


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = await client.get("/admin/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid token"}


@pytest.mark.asyncio
async def test_get_me_missing_token(client: AsyncClient):
    response = await client.get("/admin/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Missing token"}


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, async_session: AsyncSession):
    unique_admin_email = f"admin_{datetime.now().timestamp()}@example.com"
    admin = await create_admin_user(async_session, unique_admin_email)

    token = create_jwt({"user_id": str(admin.id), "email": admin.email})

    user_data = {
        "full_name": "New User",
        "email": f"newuser_{datetime.now().timestamp()}@example.com",
        "password": "newpassword123"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "admin/users", json=user_data, headers=headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["full_name"] == user_data["full_name"]
    assert response_data["email"] == user_data["email"]
    assert "id" in response_data


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, async_session: AsyncSession):
    unique_admin_email = f"admin_{datetime.now().timestamp()}@example.com"
    admin = await create_admin_user(async_session, unique_admin_email)

    unique_user_email = f"user_{datetime.now().timestamp()}@example.com"
    user_data = UserCreate(
        full_name="Old User",
        email=unique_user_email,
        password=hash_password("userpassword123")
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create(user_data)

    token = create_jwt({"user_id": str(admin.id), "email": admin.email})

    update_data = {
        "full_name": "Updated User",
        "email": f"updated_{datetime.now().timestamp()}@example.com"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.put(
        f"admin/users/{user.id}", json=update_data, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["full_name"] == update_data["full_name"]
    assert response_data["email"] == update_data["email"]
    assert response_data["id"] == user.id


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, async_session: AsyncSession):
    unique_admin_email = f"admin_{datetime.now().timestamp()}@example.com"
    admin = await create_admin_user(async_session, unique_admin_email)

    unique_user_email = f"user_{datetime.now().timestamp()}@example.com"
    user_data = UserCreate(
        full_name="User to Delete",
        email=unique_user_email,
        password=hash_password("userpassword123")
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create(user_data)

    token = create_jwt({"user_id": str(admin.id), "email": admin.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.delete(f"admin/users/{user.id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    deleted_user = await user_repo.get_by_id(user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, async_session: AsyncSession):
    unique_admin_email = f"admin_{datetime.now().timestamp()}@example.com"
    admin = await create_admin_user(async_session, unique_admin_email)

    user_repo = UserRepository(async_session)
    for i in range(2):
        user_data = UserCreate(
            full_name=f"User {i}",
            email=f"user_{i}_{datetime.now().timestamp()}@example.com",
            password=hash_password("userpassword123")
        )
        await user_repo.create(user_data)

    token = create_jwt({"user_id": str(admin.id), "email": admin.email})

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("admin/users", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 2
    for user in response_data:
        assert "full_name" in user
        assert "email" in user
        assert "id" in user
        assert "accounts" in user
        assert isinstance(user["accounts"], list)
        assert len(user["accounts"]) == 0
        assert "payments" in user
        assert isinstance(user["payments"], list)
        assert len(user["payments"]) == 0
