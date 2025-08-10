from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.config.security import create_jwt
from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.users import register_user, login_user, get_user

router = APIRouter()


@router.post("/register",status_code=201, response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_user(user, db)
    access_token = create_jwt({"user_id": user.id})
    return Token(access_token=access_token)


@router.post("/login",status_code=200, response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await login_user(user, db)
    access_token = create_jwt({"user_id": user.id, "email": user.email})
    return Token(access_token=access_token)


@router.get("/me", status_code=200, response_model=UserResponse)
async def get_me(user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_user(user.get("email"), db)
