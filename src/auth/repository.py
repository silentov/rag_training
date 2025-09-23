from sqlalchemy import select
from repository import Repository
from .models import User
from .schemas import SUserAddDB

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert

from typing import Optional


class UsersRepository(Repository["User"]):
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__()

    async def add(self, values: SUserAddDB) -> Optional["User"]:
        # Добавить одну запись
        logger.debug(values)
        values_dict = values.model_dump(exclude_unset=True)
        stmt = insert(self.model).values(**values_dict)
        stmt = stmt.on_conflict_do_nothing(index_elements=["login"]).returning(
            self.model
        )
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            logger.exception("Ошибка выполнения execute")
            raise

    async def find_user_by_login(self, login: str) -> Optional["User"]:
        try:
            query = select(self.model).filter_by(login=login)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            logger.exception("Ошибка выполнения execute")
            raise

    # async def update(self, values: SUserAddDB) -> Optional["User"]:
    #     if values.id:
    #         stmt = (
    #             self.model.update()
    #             .where(self.model.id == values.id)
    #             .values(**values.model_dump(exclude_unset=True))
    #         )
    #         try:
