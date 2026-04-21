from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from agent_config import AgentConfig
from agent_state import AgentState


class Agent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    
    config: AgentConfig = Field(default_factory=AgentConfig)
    
    state: AgentState = Field(default_factory=AgentState)
    
    name: str = Field(default="default_agent")
    
    def start(self, user_input: str, conversation_id: UUID) -> None:
        self.state.start()
    
    def get_status(self) -> str:
        return self.state.status
    
    def is_busy(self) -> bool:
        return self.state.status not in ["idle", "terminated", "error"]
    
    def reset(self) -> None:
        self.state.reset()
    
    model_config = ConfigDict(
        frozen = False,
        json_encoders = {
            UUID: lambda v: str(v)
        }
    )