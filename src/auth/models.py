from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from database.db import Base
from giga.models import ChatSession


user_chat_sessions = Table(
    "t_user_chat_session",
    Base.metadata,
    Column("user_id", ForeignKey("t_user.id", ondelete="CASCADE"), primary_key=True),
    Column("chat_session_id", ForeignKey("t_chatsession.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    firstname: Mapped[str]
    lastname: Mapped[str]
    login: Mapped[str]
    password: Mapped[str]

    is_active: Mapped[bool] = True

    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        secondary=user_chat_sessions,
        back_populates="users"
    )
