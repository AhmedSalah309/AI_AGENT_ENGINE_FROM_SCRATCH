from typing import Optional, Any, Literal
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4


class ConversationState(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    
    status: Literal["idle", "processing", "waiting_for_user", "error"] = Field(
        default="idle"
    )
    
    pending_tool_call_id: Optional[str] = Field(default=None)
    
    collected_data: dict[str, Any] = Field(default_factory=dict)
    
    error_message: Optional[str] = Field(default=None)
    
    current_turn_started_at: Optional[str] = Field(default=None)
    
    retry_count: int = Field(default=0, ge=0)
    
    model_config = ConfigDict(
        frozen = False,
        json_encoders = {
            UUID: lambda v: str(v)
        })
