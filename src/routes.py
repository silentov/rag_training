from fastapi import APIRouter
from giga.routes import router

api_router = APIRouter()
api_router.include_router(router)
