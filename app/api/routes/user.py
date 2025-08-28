from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, swagger_auth
from app.models import User
from app.schemas.account import AccountResponse
from app.schemas.payment import PaymentResponse
from app.schemas.user import UserResponse

router = APIRouter()


@router.get(
    "/me", status_code=200, response_model=UserResponse,
    dependencies=[Depends(swagger_auth)]
)
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


@router.get(
    "/accounts", status_code=200, response_model=List[AccountResponse],
    dependencies=[Depends(swagger_auth)]
)
async def get_accounts(user: User = Depends(get_current_user)):
    return user.accounts


@router.get(
    "/payments", status_code=200, response_model=List[PaymentResponse],
    dependencies=[Depends(swagger_auth)]
)
async def get_payments(user: User = Depends(get_current_user)):
    return user.payments
