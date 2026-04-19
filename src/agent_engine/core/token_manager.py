import tiktoken
from agent_engine.core.message import Message

class TokenManager:
    def __init__(self, model_name: str = "gemma2b"):
        """
        Initialize the TokenManager with a specific model name.
        """
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # If the model is not known to tiktoken, use the default
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_string_tokens(self, text: str) -> int:
        """Calculate the number of tokens in a normal string (String)"""
        if not text:
            return 0
        return len(self.encoding.encode(text))

    def count_message_tokens(self, message: Message) -> int:
        """
        Calculate the number of tokens in a single message including the Role.
        Add 3 tokens as an average for the formatting of each message 
        (like <|im_start|> and <|im_end|>)
        """
        tokens_per_message = 3
        total_tokens = tokens_per_message
        
        total_tokens += self.count_string_tokens(message.role)
        total_tokens += self.count_string_tokens(message.content)
        
        return total_tokens

    def get_total_tokens(self, messages: list[Message]) -> int:
        """Calculate the total tokens for the entire conversation"""
        total = 0
        for msg in messages:
            total += self.count_message_tokens(msg)
        
        # Add 3 additional tokens as a prime for the next assistant response
        total += 3
        return total

    def is_within_limit(self, messages: list[Message], max_tokens: int) -> bool:
        """Check if the conversation is within the allowed limit"""
        return self.get_total_tokens(messages) <= max_tokens
