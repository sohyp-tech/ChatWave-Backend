from sqlalchemy import String, Integer, DateTime, Foreignkey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database.database import Base
import datetime

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    room: Mapped[str] = mapped_column(String)
    sender_id: Mapped[int] = mapped_column(Integer)
    reveirser_id: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(DateTime, default = datetime.datetime.utcnow, nullable = False)
