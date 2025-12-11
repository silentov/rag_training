from langchain_gigachat.chat_models import GigaChat

from .service import GigaService
from configs import configs


def get_model() -> GigaChat:
    return GigaChat(
        credentials=configs.giga.token.get_secret_value(),
        scope="GIGACHAT_API_PERS",
        model="GigaChat-2-Max",
        temperature=0.1,
        verify_ssl_certs=False,
    )


def get_gigachat_service() -> GigaService:
    return GigaService(
        model=get_model(), system_promt="Ты вежливый и полезный ассистент"
    )
