from abc import ABC, abstractmethod

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from gigachat.exceptions import ResponseError
from loguru import logger

from .schemas import Message, LLMResponse


class BaseLLMService(ABC):
    @abstractmethod
    async def send_message(self, message: Message) -> LLMResponse:
        raise NotImplementedError


class GigaService(BaseLLMService):
    def __init__(self, model: BaseChatModel, system_promt: str) -> None:
        """
        Инициализация сервиса для взаимдоействия с API GigaChat

        :param model: любая модель, наследуемая от langchain_core.language_models.chat_models.BaseChatModel
        :type model: BaseChatModel
        :param system_promt: системный промпт
        :type system_promt: str
        """
        self._model = model
        self._system_prompt = system_promt

    async def send_message(self, message: Message):
        """
        Асинхронный метод для отправки сообщения в API GigaChat

        :param message: сообщение от пользователя
        :type message: Message
        """
        logger.info("Отправляем сообщение. rquid: {}", message.rquid)
        try:
            response = await self._model.ainvoke(
                [
                    SystemMessage(content=self._system_prompt),
                    HumanMessage(content=message.message),
                ]
            )
        except ResponseError as e:
            if e.args[1] == 429:
                import asyncio

                logger.error("Превышено количество одновременных запросов... Ждем.")

                await asyncio.sleep(1)

                response = await self._model.ainvoke(
                    [
                        SystemMessage(content=self._system_prompt),
                        HumanMessage(content=message.message),
                    ]
                )
            elif e.args[1] == 413:
                tokens = self._model.tokens_count(
                    input_=[self._system_prompt, message.message],
                    model="GigaChat-2-Max",
                )
                logger.error(
                    "Превышено количество входящих токенов. Текущее количество токенов: {}",
                    tokens,
                )
            elif e.args[1] in (402, 403, 500):
                logger.error("Ошибка на сервере: {}", e.args[1])
        except Exception as e:
            logger.error(e)
        else:
            return response.content
