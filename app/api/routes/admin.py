from fastapi import APIRouter
from fastapi.params import Depends

from app.api.deps import get_current_user, admin_required
from app.models import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", status_code=200, response_model=UserResponse)
async def get_me(
    user: User = Depends(get_current_user),
    _: None = Depends(admin_required),
):
    return UserResponse.from_orm(user)
