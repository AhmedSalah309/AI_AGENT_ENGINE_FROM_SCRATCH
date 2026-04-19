import logging
import time
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

logger = logging.getLogger(__name__)


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tokens: int = Field(default=0, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

    model_config = ConfigDict(frozen=True)

    @field_validator("content")
    @classmethod
    def check_empty_content(cls, v: str) -> str:
        if not v.strip():
            logger.warning("Empty content passed to Message.")
        else:
            logger.debug(f"Content validation passed for message length: {len(v)}")
        return v

    def to_log_format(self) -> str:
        return f"[{self.role.upper()}] {self.content[:50]} ({self.tokens} tokens)"
