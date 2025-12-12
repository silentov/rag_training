from typing import Any, AsyncGenerator
from db.database import AsyncSessionLocal
from db.unit_of_work import UnitOfWork

from loguru import logger


# TODO: почитать про асинк генератор
async def get_uow() -> AsyncGenerator[Any, Any]:
    """
    Dependency для FastAPI: создаёт сессию и оборачивает в UnitOfWork.
    """
    async with AsyncSessionLocal() as session:
        logger.debug("Входим в контекст")
        uow = UnitOfWork(session)
        async with uow.transaction():  # ← начинаем транзакцию на уровне запроса
            logger.debug("Начинаем транзакцию")
            yield uow
        # commit/rollback произойдут автоматически при выходе
