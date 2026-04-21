import logging
from datetime import datetime
from typing import Literal, Optional
from uuid import uuid4, UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict

from message_metadata import MessageMetadata

logger = logging.getLogger(__name__)

class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    
    role: Literal["user", "assistant", "system", "tool"]
    
    content: str = Field(
        ...,
        min_length=1,
        max_length=100000
    )
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    
    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Message content cannot be empty')
        return v.strip()
    
    @field_validator('role')
    @classmethod
    def role_valid(cls, v: str) -> str:
        valid_roles = ["user", "assistant", "system", "tool"]
        if v not in valid_roles:
            raise ValueError(f'Role must be one of {valid_roles}')
        return v
    
    class Config:
        frozen = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
