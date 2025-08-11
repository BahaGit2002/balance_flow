from pydantic import BaseModel, EmailStr


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
