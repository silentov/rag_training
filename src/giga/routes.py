from fastapi import APIRouter

# from models.models import Message



router = APIRouter(prefix="/chat", tags=["chat"])

# service = GigaService()

# @router.post("/send")
# async def send_message(input_message: Message):
#     logger.info("Получили сообщение")
#     input_message.rquid = uuid.uuid4()
#     return await service.send_message(input_message)
