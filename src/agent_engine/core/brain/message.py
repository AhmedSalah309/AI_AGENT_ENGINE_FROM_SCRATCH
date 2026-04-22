import logging
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4, UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict

from message_metadata import MessageMetadata

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class Message(BaseModel):
    message_id: UUID = Field(default_factory=uuid4)
    
    role: Role
    
    content: str = Field(
        ...,
        min_length=settings.MESSAGE_MIN_LENGTH,
        max_length=settings.MESSAGE_MAX_LENGTH
    )
    
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    
    #important validator when instantiating the class 
    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Message content cannot be empty')
        return v.strip()
    
    model_config = ConfigDict(
        frozen = True,
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    )
