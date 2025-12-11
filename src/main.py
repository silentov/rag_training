from configs import configs
from loguru import logger
from routes import api_router

from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager

from sqlalchemy.orm import configure_mappers

configure_mappers()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: добавить проверку подключения к БД
    logger.info("Запуск приложения...")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, port=configs.app.port, host="0.0.0.0")
