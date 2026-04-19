import logging
import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .message import Message

logger = logging.getLogger(__name__)


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    messages: list[Message] = Field(default_factory=list)
    max_tokens: int = Field(
        default=4000, ge=100, description="Allowed max Tokens before deleting"
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(validate_assignment=True)

    def add_message(self, message: Message) -> None:
        """Add New message to messages with strict token budget"""
        self.messages.append(message)
        logger.info(
            f"Conv[{self.id}]: Added {message.role.upper()} message "
            f"({message.tokens} tokens). Total: {len(self.messages)}"
        )
        self._enforce_token_budget()

    def get_total_tokens(self) -> int:
        """Calculate current tokens usage"""
        return sum(mes.tokens for mes in self.messages)

    def _enforce_token_budget(self) -> None:
        """Sliding Window Algorithm"""
        total = self.get_total_tokens()
        while total > self.max_tokens and len(self.messages) > 1:
            idx = 1 if self.messages[0].role == "system" else 0
            if idx == 1 and len(self.messages) <= 2:
                break

            removed = self.messages.pop(idx)
            total -= removed.tokens
            logger.warning(
                f"Conv[{self.id}]: Evicted message to save {removed.tokens} tokens."
            )

    def to_llm_payload(self) -> list[dict[str, str]]:
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def clear_history(self, keep_system: bool = True) -> None:
        if keep_system and self.messages and self.messages[0].role == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []
        logger.info(f"Conv[{self.id}]: History cleared.")
