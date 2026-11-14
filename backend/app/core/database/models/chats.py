from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database.database import Base
import datetime

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"))
    user2_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user1_name = relationship("User", foreign_keys=[user1_id])
    user2_name = relationship("User", foreign_keys=[user2_id])


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    sender_name = relationship("User", foreign_keys=[sender_id])
    content = Column(Text)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    is_read = Column(Boolean, default=False)
