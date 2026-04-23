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

    VALID_TRANSITIONS = {
        ConversationStatus.IDLE: {ConversationStatus.PROCESSING},
        ConversationStatus.PROCESSING: {
            ConversationStatus.WAITING_FOR_USER,
            ConversationStatus.ERROR
        },
        ConversationStatus.WAITING_FOR_USER: {
            ConversationStatus.PROCESSING
        },
        ConversationStatus.ERROR: {
            ConversationStatus.IDLE
        }
    }
    id: UUID = Field(default_factory=uuid4)

    status: ConversationStatus = Field(default=ConversationStatus.IDLE)

    pending_tool_call_id: Optional[str] = Field(default=None)

    collected_data: dict[str, Any] = Field(default_factory=dict)

    error_message: Optional[str] = Field(default=None)

    current_turn_started_at: datetime | None = Field(default=None)

    retry_count: int = Field(default=0, ge=0)

    def transition_to(self, new_status: ConversationStatus):
        allowed = type(self).VALID_TRANSITIONS.get(self.status, set())

        if new_status not in allowed:
            raise ValueError(
                f"Invalid transition: {self.status} → {new_status}"
            )

        self.status = new_status


    model_config = ConfigDict(
        frozen=False,
        json_encoders={
            UUID: lambda v: str(v)
        }
    )

