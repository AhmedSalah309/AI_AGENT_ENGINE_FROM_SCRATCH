from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from memory.memory_interface import MemoryInterface
from core.brain.message import Message
from core.brain.conversation import Conversation


class ShortTermMemory(MemoryInterface):
    """
    short term memory - stores only the things that happened in the current conversation
    uses in-memory storage instead of database
    """
    
    def __init__(self, max_conversations: int = 1000):
        self._conversations: Dict[UUID, Conversation] = {}
        self._max_conversations = max_conversations
    
    def save_message(self, conversation_id: UUID, message: Message) -> None:
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"conversation {conversation_id} not found")
        
        conversation.add_message(message)
        self.save_conversation(conversation)
    
    def get_messages(self, conversation_id: UUID, limit: Optional[int] = None) -> List[Message]:
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return []
        
        messages = conversation.messages
        
        if limit and limit > 0:
            return messages[-limit:]
        
        return messages
    
    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        return self._conversations.get(conversation_id)
    
    def save_conversation(self, conversation: Conversation) -> None:
        if len(self._conversations) >= self._max_conversations:
            self._cleanup_oldest()
        
        self._conversations[conversation.id] = conversation
    
    def delete_conversation(self, conversation_id: UUID) -> bool:
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False
    
    def list_conversations(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Conversation]:
        user_conversations = [
            conv for conv in self._conversations.values()
            if conv.user_id == user_id
        ]
        
        user_conversations.sort(key=lambda x: x.updated_at, reverse=True)
        
        return user_conversations[offset:offset + limit]
    
    def clear(self) -> None:
        self._conversations.clear()
    
    def _cleanup_oldest(self) -> None:
        """
        when we exceed the maximum number of conversations, delete the oldest conversation
        """
        if not self._conversations:
            return
        
        oldest = min(self._conversations.values(), key=lambda x: x.updated_at)
        del self._conversations[oldest.id]
    
    def get_conversation_count(self) -> int:
        """
        return the number of conversations stored in memory
        """
        return len(self._conversations)
    
    def conversation_exists(self, conversation_id: UUID) -> bool:
        """
        check if conversation exists in memory
        """
        return conversation_id in self._conversations
