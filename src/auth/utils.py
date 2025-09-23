from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import jwt
from configs import configs
from fastapi import Response
from .schemas import TokenResponse


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(user, password):
    if (
        not user
        or verify_password(plain_password=password, hashed_password=user.password)
        is False
    ):
        return None
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_tokens(data: dict) -> dict:
    # Текущее время в UTC
    now = datetime.now(timezone.utc)

    # AccessToken - 30 минут
    access_expire = now + timedelta(minutes=30)
    access_payload = data.copy()
    access_payload.update({"exp": int(access_expire.timestamp()), "type": "access"})
    access_token = jwt.encode(
        access_payload, configs.auth.secret_key, algorithm=configs.auth.algorithm
    )

    # RefreshToken - 7 дней
    refresh_expire = now + timedelta(days=7)
    refresh_payload = data.copy()
    refresh_payload.update({"exp": int(refresh_expire.timestamp()), "type": "refresh"})
    refresh_token = jwt.encode(
        refresh_payload, configs.auth.secret_key, algorithm=configs.auth.algorithm
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def set_tokens(response: Response, tokens: TokenResponse) -> None:
    response.set_cookie(
        key="user_access_token",
        value=tokens.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        key="user_refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
