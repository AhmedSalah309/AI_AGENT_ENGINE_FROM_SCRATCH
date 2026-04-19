from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_session"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    max_tokens = Column(Integer, default=4000)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('chat_session.id'))
    role = Column(String, nullable=False) 
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")

