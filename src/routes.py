from fastapi import APIRouter
from giga.routes import giga_router

api_router = APIRouter()
api_router.include_router(giga_router)
