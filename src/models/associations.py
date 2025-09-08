from sqlalchemy import Table, Column, ForeignKey
from database import Base

user_chat_sessions = Table(
    "t_user_chat_session",
    Base.metadata,
    Column("user_id", ForeignKey("t_user.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "chat_session_id",
        ForeignKey("t_chatsession.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
