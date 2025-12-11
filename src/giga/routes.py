import uuid
from fastapi import APIRouter, Depends

from .schemas import Message
from .utils import get_gigachat_service
from .service import GigaService


giga_router = APIRouter(prefix="/chat", tags=["chat"])


@giga_router.post("/send")
async def send_message(
    input_message: Message, service: GigaService = Depends(get_gigachat_service)
):
    input_message.rquid = uuid.uuid4()
    return await service.send_message(input_message)
