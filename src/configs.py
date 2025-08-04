from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from logger import logger

import sys


class ConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class DBConfig(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix="db_")

    port: str
    host: str


class GigaConfig(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix="giga_")

    token: SecretStr = Field(..., repr=False)
    model: str


class FastAPIConfig(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix="fastapi_")

    port: str


class Config(BaseSettings):
    db: DBConfig = Field(default_factory=DBConfig)
    giga: GigaConfig = Field(default_factory=GigaConfig)
    app: FastAPIConfig = Field(default_factory=FastAPIConfig)
    
    @classmethod
    def load(cls) -> "None | Config":    # ->"type" is forward references
        try:
            return cls()
        except ValidationError as e:
            logger.critical("❌ Ошибка валидации конфигурации:")
            for error in e.errors():
                field = " -> ".join(error["loc"])
                msg = error["msg"]
                logger.critical(f"  Поле: {field} | Ошибка: {msg}")
            logger.critical("Проверь файл .env и переменные окружения.")
            sys.exit(1)


