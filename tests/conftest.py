import pytest
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession,
    async_sessionmaker,
)
from app.main import app
from app.database.database import get_db
from app.models.base import Base
from httpx import AsyncClient, ASGITransport

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(engine):
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def client(async_session):
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
