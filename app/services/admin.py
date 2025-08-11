from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.users import UserRepository
from app.schemas.user import UserCreate, UserUpdate


async def create_user(user: UserCreate, db: AsyncSession) -> User:
    user = await UserRepository(db).create(user)
    return user


async def update_user(user_id: int, user: UserUpdate, db: AsyncSession) -> User:
    user = await UserRepository(db).update(user_id, user)
    return user
