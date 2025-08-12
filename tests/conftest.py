import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app
from app.database.database import get_db


@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        from app.models.base import Base
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session
    await engine.dispose()


@pytest.fixture
def client(test_db):
    async def override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
