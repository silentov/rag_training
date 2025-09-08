from fastapi import Depends, HTTPException, APIRouter
from .dependencies import get_service
from .service import UserService
from .schemas import SUserRegister


users_router = APIRouter(prefix="/users", tags=["chat"])


@users_router.post("/register")
async def register_user(
    user: SUserRegister, user_service: UserService = Depends(get_service)
):
    try:
        user = await user_service.create_user(user)
        return user
    except Exception as e:
        # Можно логировать или оборачивать в HTTPException
        raise HTTPException(status_code=500, detail=str(e))


@users_router.post("/auth")
async def login_user():
    pass
