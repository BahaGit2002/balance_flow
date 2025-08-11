from pydantic import BaseModel, EmailStr

from app.schemas.account import AccountResponse
from app.schemas.payment import PaymentResponse


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserCreate(UserLogin):
    full_name: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str

    class Config:
        from_attributes = True


class UserListResponse(UserResponse):
    accounts: list[AccountResponse]
    payments: list[PaymentResponse]
