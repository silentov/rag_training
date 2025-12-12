import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .schemas import Message
from .utils import get_gigachat_service
from .service import GigaService
from utils.exceptions import LLMBusinessException

giga_router = APIRouter(prefix="/chat", tags=["chat"])


@giga_router.post("/send")
async def send_message(
    input_message: Message, service: GigaService = Depends(get_gigachat_service)
):
    input_message.rquid = str(uuid.uuid4())
    try:
        response = await service.send_message(input_message)
        return JSONResponse(
            content={"message": response.answer}, status_code=response.status_code
        )
    except LLMBusinessException as e:
        return JSONResponse(content={"error": str(e)}, status_code=e.status_code)
