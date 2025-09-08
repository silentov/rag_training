from typing import List
from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from database import Base
from models import associations


print("chat")


class ChatSession(Base):
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="session"
    )

    users: Mapped[List["User"]] = relationship(  # noqa F821
        "User",
        secondary=associations.user_chat_sessions,
        back_populates="chat_sessions",
    )


class ChatMessage(Base):
    session_id: Mapped[int] = mapped_column(ForeignKey("t_chatsession.id"))
    role: Mapped[str] = mapped_column(String(16))  # 'user' | 'assistant'
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    session: Mapped["ChatSession"] = relationship(back_populates="messages")
