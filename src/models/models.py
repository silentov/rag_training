from pydantic import BaseModel, Field

import uuid


class Message(BaseModel):
    message: str = Field(min_length=1, max_length=8124)
    rquid: uuid.UUID = Field(default=None)