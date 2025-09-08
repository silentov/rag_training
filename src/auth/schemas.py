from typing import Optional, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(BaseModel):
    login: str = Field(min_length=3, max_length=50, description="Логин пользователя")
    firstname: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Имя, от 3 до 50 символов",
    )
    lastname: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Фамилия, от 3 до 50 символов",
    )

    model_config = ConfigDict(from_attributes=True)


class SUserRegister(UserBase):
    password: str = Field(
        min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )

    @model_validator(mode="after")
    def hash_password(self) -> Self:
        self.password = pwd_context.hash(
            self.password
        )  # хешируем пароль до сохранения в базе данных
        return self


class SUserAddDB(UserBase):
    password: str = Field(min_length=5, description="Пароль в формате HASH-строки")


class SUserAuth(UserBase):
    password: str = Field(
        min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )
