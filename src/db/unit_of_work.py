# app/unit_of_work.py
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from auth.repository import UsersRepository  # добавь свои репозитории


class UnitOfWorkBase(ABC):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    """
    Продакшен Unit of Work для управления транзакциями и репозиториями.
    """

    def __init__(self, session: Callable[[], AsyncSession]):
        self.session = session
        self.users = UsersRepository(session)

    # async def __aenter__(self):
    #     logger.debug("Создаем репо")
    #     self.users = UsersRepository(self.session)
    #     return await super.__aenter__()

    async def commit(self):
        """Явный коммит транзакции."""
        try:
            logger.info("Коммитим транзакцию")
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Ошибка при коммите транзакции: {str(e)}") from e

    async def rollback(self):
        """Явный откат транзакции."""
        logger.warning("Откат транзакции")
        await self.session.rollback()

    @asynccontextmanager
    async def transaction(self):
        """
        Контекстный менеджер для управления транзакцией.
        Автоматически делает rollback при исключении, commit — при успехе.
        Поддерживает вложенные вызовы (через savepoint, если нужно — см. ниже).
        """
        try:
            yield self
            await self.commit()
        except Exception:
            await self.rollback()
            raise

    # --- Опционально: поддержка SAVEPOINT для вложенных транзакций ---
    @asynccontextmanager
    async def nested_transaction(self):
        """
        Используется, если нужно несколько точек отката в одной транзакции.
        Например: в цикле или при частичной обработке.
        """
        savepoint = await self.session.begin_nested()
        try:
            yield self
            await savepoint.commit()
        except Exception:
            await savepoint.rollback()
            raise
