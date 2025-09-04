from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage

from configs import configs
from loguru import logger

model = GigaChat(
    credentials=configs.giga.token.get_secret_value(),
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Max",
    verify_ssl_certs=False,
)


# class GigaService:
#     async def send_message(self, message: Message):
#         logger.info("Отправляем сообщение. rquid: {}", message.rquid)
#         response = await model.ainvoke([SystemMessage(content="Ты - дружелюбный и вежливый собеседник."),HumanMessage(content=message.message)])
#         return response.content