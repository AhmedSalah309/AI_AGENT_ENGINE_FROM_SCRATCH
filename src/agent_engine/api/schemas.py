import time
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class MessageSchema(BaseModel):
    role: Literal["user", "assistant", "tool"]
    content: str
    tokens: int = Field(default=0, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

    model_config = ConfigDict(frozen=True)


class ChatResponse(BaseModel):
    session_id: str
    history_count: int
    total_tokens: int
    last_reply: str
