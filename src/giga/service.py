from abc import ABC, abstractmethod

import gigachat.context
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from gigachat.exceptions import ResponseError
from loguru import logger

from .schemas import Message, LLMResponse
from utils.decorators import async_retry
from utils.exceptions import (
    TokenLimitExceededError,
    BackendError,
    RateLimitError,
    LLMBusinessException,
)


class BaseLLMService(ABC):
    @abstractmethod
    async def send_message(self, message: Message) -> LLMResponse:
        raise NotImplementedError


class GigaService(BaseLLMService):
    def __init__(
        self, model: GigaChat, system_prompt: str
    ) -> None:  # исправлена опечатка
        """
        Инициализация сервиса для взаимдоействия с API GigaChat

        :param model: любая модель, наследуемая от langchain_core.language_models.chat_models.BaseChatModel
        :type model: BaseChatModel
        :param system_promt: системный промпт
        :type system_promt: str
        """
        self._model = model
        self._system_prompt = system_prompt

    @async_retry(exceptions=[RateLimitError], max_retries=3)
    async def send_message(self, message: Message) -> LLMResponse:
        """
        Асинхронный метод для отправки сообщения в API GigaChat

        :param message: сообщение от пользователя
        :type message: Message
        """
        logger.info("Отправляем сообщение. rquid: {}", message.rquid)
        try:
            gigachat.context.request_id_cvar.set(message.rquid)
            payload = Chat(
                messages=[
                    Messages(role=MessagesRole.SYSTEM, content=self._system_prompt),
                    Messages(role=MessagesRole.USER, content=message.message),
                ]
            )
            response = await self._model.achat(payload)
            return LLMResponse(
                rquid=message.rquid,
                answer=response.choices[0].message.content,
                status_code=200,
            )
        except ResponseError as e:
            status_code = getattr(e, "status_code", None) or (
                e.args[1] if len(e.args) > 1 else None
            )
            logger.error("Ошибка GigaChat: статус {}", status_code)

            if status_code == 413:
                raise TokenLimitExceededError()
            elif status_code >= 500:
                raise BackendError(code=status_code)
            elif status_code == 429:
                raise RateLimitError(rquid=message.rquid)
            else:
                raise LLMBusinessException(status_code=status_code)
        except Exception:
            logger.exception("Неизвестная ошибка при вызове модели")
            return LLMResponse(
                rquid=message.rquid,
                answer="Возникла неизвестная ошибка",
                status_code=500,
            )
