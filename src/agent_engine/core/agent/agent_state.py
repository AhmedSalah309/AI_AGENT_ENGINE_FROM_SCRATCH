from typing import Optional, Dict, Any, Literal
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field, ConfigDict


class AgentState(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    
    status: Literal[
        "idle",
        "thinking",
        "executing_tool",
        "responding",
        "error",
        "terminated"
    ] = Field(default="idle")
    
    current_iteration: int = Field(default=0, ge=0)
    
    current_tool_name: Optional[str] = Field(default=None)
    
    error_message: Optional[str] = Field(default=None)
    
    started_at: Optional[datetime] = Field(default=None)
    
    last_active_at: datetime = Field(default_factory=datetime.utcnow)
    
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def start(self) -> None:
        self.status = "thinking"
        self.started_at = datetime.utcnow()
        self.last_active_at = datetime.utcnow()
    
    def start_tool_execution(self, tool_name: str) -> None:
        self.status = "executing_tool"
        self.current_tool_name = tool_name
        self.last_active_at = datetime.utcnow()
    
    def finish_tool_execution(self) -> None:
        self.status = "thinking"
        self.current_tool_name = None
        self.current_iteration += 1
        self.last_active_at = datetime.utcnow()
    
    def finish(self) -> None:
        self.status = "terminated"
        self.last_active_at = datetime.utcnow()
    
    def set_error(self, error: str) -> None:
        self.status = "error"
        self.error_message = error
        self.last_active_at = datetime.utcnow()
    
    def reset(self) -> None:
        self.status = "idle"
        self.current_iteration = 0
        self.current_tool_name = None
        self.error_message = None
        self.started_at = None
        self.last_active_at = datetime.utcnow()
    
    model_config = ConfigDict(
        frozen = False,
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    )