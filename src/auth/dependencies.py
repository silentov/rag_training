from fastapi import Depends

from dependencies import get_uow
from unit_of_work import UnitOfWork
from .service import UserService


def get_service(uow: UnitOfWork = Depends(get_uow)):
    return UserService(uow)
