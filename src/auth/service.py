from fastapi import HTTPException
from loguru import logger
from unit_of_work import UnitOfWork
from .schemas import SUserRegister, SUserAuth, TokenResponse
from .utils import verify_password, create_tokens
from exceptions import IncorrectLoginException, IncorrectEmailOrPasswordException


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, user: SUserRegister):
        logger.debug("Creating user: {}", user)

        created_user = await self.uow.users.add(user)

        if created_user is None:
            raise HTTPException(
                status_code=409, detail="User with this login already exists"
            )
        return user

    async def update_user(self):
        pass

    async def delete_user(self):
        pass

    async def view_user(self):
        pass

    async def auth_user(self, user: SUserAuth) -> TokenResponse | None:
        db_user = await self.uow.users.find_user_by_login(user.login)

        if db_user is None:
            raise IncorrectLoginException

        if not verify_password(user.password, db_user.password):
            raise IncorrectEmailOrPasswordException

        return TokenResponse(**create_tokens({"sub": db_user.id}))

    async def logout_user(self):
        pass
