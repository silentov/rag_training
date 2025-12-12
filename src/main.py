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


if configs.app.environment == "dev":
    from scalar_fastapi import get_scalar_api_reference

    @app.get("/scalar", include_in_schema=False)
    async def scalar_html():
        return get_scalar_api_reference(
            # Your OpenAPI document
            openapi_url=app.openapi_url,
            # Avoid CORS issues (optional)
            scalar_proxy_url="https://proxy.scalar.com",
        )


if __name__ == "__main__":
    uvicorn.run(app, port=configs.app.port, host="0.0.0.0")
