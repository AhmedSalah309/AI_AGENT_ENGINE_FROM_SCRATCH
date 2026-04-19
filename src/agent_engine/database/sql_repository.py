from typing import Optional
from agent_engine.core.conversation import Conversation
from agent_engine.core.message import Message
from agent_engine.database.session import SessionLocal
from agent_engine.database.models import ChatSession, ChatMessage

class SQLRepository:
    def save(self, session_id: str, conversation: Conversation):
        db = SessionLocal()
        try:
            # Check if the session exists or create it
            chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not chat_session:
                chat_session = ChatSession(id=session_id, max_tokens=conversation.max_tokens)
                db.add(chat_session)
            
            # Clear old messages and insert updated ones (simple synchronization method)
            db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
            
            for msg in conversation.messages:
                db_msg = ChatMessage(
                    session_id=session_id,
                    role=msg.role,
                    content=msg.content,
                    tokens=msg.tokens
                )
                db.add(db_msg)
            
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error saving to DB: {e}")
        finally:
            db.close()

    def load(self, session_id: str) -> Optional[Conversation]:
        db = SessionLocal()
        try:
            chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not chat_session:
                return None
            
            conv = Conversation()
            messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.id.asc()).all()
            
            for m in messages:
                conv.messages.append(Message(role=m.role, content=m.content, tokens=m.tokens))
            
            return conv
        finally:
            db.close()
