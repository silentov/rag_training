from fastapi import HTTPException
from loguru import logger
from unit_of_work import UnitOfWork
from .schemas import SUserRegister


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

    async def auth_user(self):
        pass

    async def logout_user(self):
        pass
