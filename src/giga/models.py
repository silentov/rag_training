from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from database.db import Base
from auth.models import user_chat_sessions, User


class ChatSession(Base):
    messages: Mapped[list["ChatMessage"]] = relationship("ChatMessage", back_populates="sessions")
    
    users: Mapped[list["User"]] = relationship(
        secondary=user_chat_sessions,
        back_populates="chat_sessions"
    )

class ChatMessage(Base):
    session_id: Mapped[int] = mapped_column(ForeignKey("t_chatsession.id"))
    role: Mapped[str] = mapped_column(String(16))  # 'user' | 'assistant'
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    session: Mapped["ChatSession"] = relationship(back_populates="messages")