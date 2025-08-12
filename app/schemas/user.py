from pydantic import BaseModel, EmailStr, ConfigDict

from app.schemas.account import AccountResponse
from app.schemas.payment import PaymentResponse


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserLogin):
    full_name: str


class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(UserResponse):
    accounts: list[AccountResponse]
    payments: list[PaymentResponse]
