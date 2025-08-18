import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from app.main import app


@pytest.mark.asyncio
async def test_register(client):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        response = await ac.post("/auth/register", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    json_resp = response.json()
    assert "access_token" in json_resp
    assert isinstance(json_resp["access_token"], str)


@pytest.mark.asyncio
async def test_register_existing_email(client):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        first_data = {
            "full_name": "Test User",
            "email": "duplicate@example.com",
            "password": "strongpassword123"
        }
        response = await ac.post("/auth/register", json=first_data)

        second_data = {
            "full_name": "Another User",
            "email": "duplicate@example.com",
            "password": "anotherpassword123"
        }
        response = await ac.post("/auth/register", json=second_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_resp = response.json()
    assert "detail" in json_resp or "error" in json_resp


@pytest.mark.asyncio
async def test_login(client):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        register_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        r = await ac.post("/auth/register", json=register_data)
        assert r.status_code == status.HTTP_201_CREATED

        login_data = {
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        response = await ac.post("/auth/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK

        json_resp = response.json()
        assert "access_token" in json_resp
        assert isinstance(json_resp["access_token"], str)


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        register_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        r = await ac.post("/auth/register", json=register_data)
        assert r.status_code == status.HTTP_201_CREATED

        login_data = {
            "email": "test@example.com",
            "password": "strongpassword124"
        }
        response = await ac.post("/auth/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        json_resp = response.json()
        assert "detail" in json_resp or "Invalid email or password." in json_resp


@pytest.mark.asyncio
async def test_login_wrong_email(client):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        register_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        r = await ac.post("/auth/register", json=register_data)
        assert r.status_code == status.HTTP_201_CREATED

        login_data = {
            "email": "test1@example.com",
            "password": "strongpassword123"
        }
        response = await ac.post("/auth/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        json_resp = response.json()
        assert "detail" in json_resp or "Invalid email or password." in json_resp
