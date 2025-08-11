from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, admin_required
from app.database.database import get_db
from app.models import User
from app.repositories.users import UserRepository
from app.schemas.user import (
    UserResponse, UserCreate, UserUpdate,
    UserListResponse,
)
from app.services.admin import (
    create_user as create_user_services,
    update_user as update_user_service,
)

router = APIRouter()


@router.get("/me", status_code=200, response_model=UserResponse)
async def get_me(
    user: User = Depends(get_current_user),
    _: None = Depends(admin_required),
):
    return UserResponse.model_validate(user)


@router.post("/users", status_code=201, response_model=UserResponse)
async def create_user(
    user: UserCreate,
    _: None = Depends(admin_required),
    db: AsyncSession = Depends(get_db)
):
    user = await create_user_services(user, db)
    return UserResponse.model_validate(user)


@router.put("/users/{user_id}", status_code=200, response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    _: None = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
):
    user = await update_user_service(user_id, user, db)
    return UserResponse.model_validate(user)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    _: None = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
):
    await UserRepository(db).delete(user_id)
    return


@router.get("/users", status_code=200, response_model=List[UserListResponse])
async def get_users(
    _: None = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
):
    users = await UserRepository(db).get_all()
    return users
