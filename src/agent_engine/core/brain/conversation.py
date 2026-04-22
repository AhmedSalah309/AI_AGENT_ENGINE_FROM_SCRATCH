import logging
from datetime import datetime, timezone
from typing import Optional, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator, ConfigDict

from message import Message
from conversation_state import ConversationState

logger = logging.getLogger(__name__)

class Conversation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    
    user_id: str = Field(..., min_length=1)
    
    messages: list[Message] = Field(default_factory=list)
    
    state: ConversationState = Field(default_factory=ConversationState)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    title: Optional[str] = Field(default=None)
    
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('user_id')
    @classmethod
    def user_id_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('User ID cannot be empty')
        return v.strip()
    
    def add_message(self, message: Message) -> None:
        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)

    def generate_title(self):
        if not self.messages:
            return "New Chat"
        return self.messages[0].content[:50]
    
    def get_last_message(self) -> Optional[Message]:
        if not self.messages:
            return None
        return self.messages[-1]
    
    def get_messages_by_role(self, role: Role) -> list[Message]:
        return [msg for msg in self.messages if msg.role == role]
    
    def get_message_count(self) -> int:
        return len(self.messages)
    
    model_config = ConfigDict(
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        })
