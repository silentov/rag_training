from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base
from models import associations


class User(Base):
    firstname: Mapped[str]
    lastname: Mapped[str]
    login: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str]

    chat_sessions: Mapped[List["ChatSession"]] = relationship(  # noqa F821
        "ChatSession",
        secondary=associations.user_chat_sessions,
        back_populates="users",
    )
