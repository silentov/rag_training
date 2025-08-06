from configs.configs import configs
from logger import logger
from api.main_router import api_router

from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    #TODO: добавить проверку подключения к БД
    logger.info("Запуск приложения...")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

if __name__=="__main__":
    uvicorn.run(app, port=configs.app.port, host='0.0.0.0')