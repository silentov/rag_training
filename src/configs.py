from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from loguru import logger

from functools import lru_cache
from typing import Optional
from pathlib import Path


project_root = Path(__file__).parent.parent.resolve()


class ConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=project_root / ".env", env_file_encoding="utf-8", extra="ignore"
    )


class MilvusConfig(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix="milvus_")

    port: str
    host: str


class PostgreConfig(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix="postgre_")

    user: str
    password: str
    db: str
    port: int
    pool_size: int
    max_overflow: int


class GigaConfig(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix="giga_")

    token: SecretStr = Field(..., repr=False)
    model: str


class FastAPIConfig(ConfigSettings):
    model_config = SettingsConfigDict(env_prefix="fastapi_")

    port: int


class Config(BaseSettings):
    milvus: MilvusConfig = Field(default_factory=MilvusConfig)
    postgre: PostgreConfig = Field(default_factory=PostgreConfig)
    giga: GigaConfig = Field(default_factory=GigaConfig)
    app: FastAPIConfig = Field(default_factory=FastAPIConfig)

    @classmethod
    @lru_cache(maxsize=1)  # Кэширование результата
    def load(cls) -> Optional["Config"]:
        env_file = project_root / ".env"

        if not env_file.exists():
            logger.critical(f"❌ Файл конфигурации {env_file} не найден.")
            return None

        try:
            return cls()
        except FileNotFoundError as e:
            logger.critical(f"❌ Ошибка чтения файла: {str(e)}")
            return None
        except ValidationError as e:
            logger.critical("❌ Ошибка валидации конфигурации:")
            for error in e.errors():
                field = " -> ".join(error["loc"])
                msg = error["msg"]
                logger.critical(f"  Поле: {field} | Ошибка: {msg}")
            logger.critical("Проверь файл .env и переменные окружения.")
            return None
        except Exception as e:
            logger.critical(f"❌ Неожиданная ошибка: {str(e)}")
            return None


configs = Config.load()
