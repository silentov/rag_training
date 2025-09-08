from fastapi import APIRouter
from giga.routes import giga_router
from auth.routes import users_router

api_router = APIRouter()
api_router.include_router(giga_router)
api_router.include_router(users_router)
