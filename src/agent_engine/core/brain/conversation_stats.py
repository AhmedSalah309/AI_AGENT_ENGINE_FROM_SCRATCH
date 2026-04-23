from typing import Optional, Any, Literal
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from enum import Enum

class ConversationStatus(str, Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING_FOR_USER = "waiting_for_user"
    ERROR = "error"

class ConversationState(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    status: ConversationStatus = ConversationStatus.IDLE

    pending_tool_call_id: Optional[str] = None

    collected_data: dict[str, Any] = Field(default_factory=dict)

    error_message: Optional[str] = None

    current_turn_started_at: datetime | None = None

    retry_count: int = Field(default=0, ge=0)

    model_config = ConfigDict(
        frozen=False,
        json_encoders={
            UUID: lambda v: str(v)
        }
    )

