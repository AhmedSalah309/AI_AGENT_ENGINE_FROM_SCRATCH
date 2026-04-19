from typing import List

from agent_engine.core.message import Message
from agent_engine.core.token_manager import TokenManager


class Summarizer:
    def __init__(self, token_manager: TokenManager, max_context_tokens: int = 3000):
        self.token_manager = token_manager
        self.max_context_tokens = max_context_tokens

    def should_summarize(self, messages: List[Message]) -> bool:
        """Determine if the conversation needs to be summarized based on limit"""
        total_tokens = self.token_manager.get_total_tokens(messages)
        return total_tokens > self.max_context_tokens

    def get_messages_to_summarize(
        self, messages: List[Message], keep_last_n: int = 4
    ) -> List[Message]:
        """Separate old messages that need summarization from recent messages to keep"""
        if len(messages) <= keep_last_n:
            return []

        # Exclude the system message (System Prompt) if found at the beginning
        start_idx = 1 if messages[0].role == "system" else 0
        return messages[start_idx:-keep_last_n]

    def build_summary_prompt(self, old_messages: List[Message]) -> str:
        """Build the text to be sent to the LLM for summarization"""
        chat_text = "\n".join([f"{m.role}: {m.content}" for m in old_messages])
        prompt = (
            "Summarize the following conversation history briefly and accurately. "
            "Retain key facts, user preferences, and important context.\n\n"
            f"Conversation:\n{chat_text}\n\nSummary:"
        )
        return prompt

    def create_summary_message(self, summary_text: str) -> Message:
        """Create a new system message containing the summary"""
        return Message(
            role="system",
            content=f"[System Note: Previous conversation summary: {summary_text}]",
        )
