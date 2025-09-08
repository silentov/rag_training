from repository import Repository
from .models import User

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert


class UsersRepository(Repository["User"]):
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__()

    async def add(self, values: BaseModel) -> "User" | None:
        # Добавить одну запись
        logger.debug(values)
        values_dict = values.model_dump(
            exclude_unset=True, exclude={"confirm_password"}
        )

        stmt = insert(self.model).values(**values_dict)

        stmt = stmt.on_conflict_do_nothing(index_elements=["login"]).returning(
            self.model
        )  # ← игнорируем конфликт

        try:
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error("Ошибка выполнения execute: {}", e)
            raise
