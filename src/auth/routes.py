from fastapi import Depends, HTTPException, APIRouter
from .dependencies import get_service
from .service import UserService
from .schemas import SUserRegister, SUserAuth


users_router = APIRouter(prefix="/users", tags=["chat"])


@users_router.post("/register")
async def register_user(
    user: SUserRegister, user_service: UserService = Depends(get_service)
):
    user = await user_service.create_user(user)
    return user

@users_router.post("/auth")
async def login_user(
    user: SUserAuth, user_service: UserService = Depends(get_service)
):
    return await user_service.auth_user(user)

