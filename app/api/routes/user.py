from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.database import get_db
from app.repositories.users import UserRepository
from app.schemas.account import AccountResponse
from app.schemas.payment import PaymentResponse
from app.schemas.user import UserResponse
from app.services.users import get_user

router = APIRouter()


@router.get("/me", status_code=200, response_model=UserResponse)
async def get_me(
    user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await get_user(user, db)


@router.get("/accounts", status_code=200, response_model=List[AccountResponse])
async def get_accounts(
    user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    accounts = await UserRepository(db).get_user_accounts(user.get("email"))
    return accounts


@router.get("/payments", status_code=200, response_model=List[PaymentResponse])
async def get_payments(
    user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    payments = await UserRepository(db).get_user_payments(user.get("email"))
    return payments
