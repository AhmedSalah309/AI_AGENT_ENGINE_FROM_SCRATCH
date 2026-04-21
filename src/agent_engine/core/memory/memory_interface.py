from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from core.brain.message import Message
from core.brain.conversation import Conversation


class MemoryInterface(ABC):
    """
    interface for memory
    """
    
    @abstractmethod
    def save_message(self, conversation_id: UUID, message: Message) -> None:
        """
        save message in memory
        """
        pass
    
    @abstractmethod
    def get_messages(self, conversation_id: UUID, limit: Optional[int] = None) -> List[Message]:
        """
        get messages from memory
        """
        pass
    
    @abstractmethod
    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        """
        get conversation from memory
        """
        pass
    
    @abstractmethod
    def save_conversation(self, conversation: Conversation) -> None:
        """
        save conversation in memory
        """
        pass
    
    @abstractmethod
    def delete_conversation(self, conversation_id: UUID) -> bool:
        """
        delete conversation from memory
        """
        pass
    
    @abstractmethod
    def list_conversations(self, user_id: str, limit: int, offset: int) -> List[Conversation]:
        """
        list all conversations of a user
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """
        delete all data in memory
        """
        pass
