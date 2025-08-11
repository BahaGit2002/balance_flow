from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.users import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.config.security import hash_password, verify_password


async def register_user(user: UserCreate, db: AsyncSession) -> User:
    existing_user = await UserRepository(db).get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists.",
        )
    user.password = hash_password(user.password)
    return await UserRepository(db).create(user)


async def login_user(user: UserLogin, db: AsyncSession) -> User:
    existing_user = await UserRepository(db).get_by_email(user.email)
    if not existing_user or not verify_password(
            user.password, hash_password(user.password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return existing_user
