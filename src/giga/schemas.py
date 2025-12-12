from pydantic import BaseModel, Field
from typing import Optional


class Message(BaseModel):
    rquid: Optional[str] = Field(default=None, description="Request unique ID")
    message: str = Field(..., description="Текст сообщения пользователя")


class LLMResponse(BaseModel):
    rquid: str
    answer: str
    status_code: int
    model_name: Optional[str] = None
