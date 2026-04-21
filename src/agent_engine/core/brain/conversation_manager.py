from typing import Dict, List, Optional
from uuid import UUID
from abc import ABC, abstractmethod

from conversation import Conversation
from message import Message
from conversation_state import ConversationState


class ConversationManager(ABC):
    
    @abstractmethod
    def create(self, user_id: str, title: Optional[str] = None) -> Conversation:
        pass
    
    @abstractmethod
    def get(self, conversation_id: UUID) -> Optional[Conversation]:
        pass
    
    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        pass
    
    @abstractmethod
    def delete(self, conversation_id: UUID) -> bool:
        pass
    
    @abstractmethod
    def add_message(self, conversation_id: UUID, message: Message) -> None:
        pass
    
    @abstractmethod
    def update_state(self, conversation_id: UUID, state: ConversationState) -> None:
        pass
    
    @abstractmethod
    def list_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Conversation]:
        pass
    
    @abstractmethod
    def get_active_conversations(self, user_id: str) -> List[Conversation]:
        pass


class InMemoryConversationManager(ConversationManager):
    
    def __init__(self):
        self._storage: Dict[UUID, Conversation] = {}
    
    def create(self, user_id: str, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        self._storage[conversation.id] = conversation
        return conversation
    
    def get(self, conversation_id: UUID) -> Optional[Conversation]:
        return self._storage.get(conversation_id)
    
    def save(self, conversation: Conversation) -> None:
        self._storage[conversation.id] = conversation
    
    def delete(self, conversation_id: UUID) -> bool:
        if conversation_id in self._storage:
            del self._storage[conversation_id]
            return True
        return False
    
    def add_message(self, conversation_id: UUID, message: Message) -> None:
        conversation = self.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        conversation.add_message(message)
        self.save(conversation)
    
    def update_state(self, conversation_id: UUID, state: ConversationState) -> None:
        conversation = self.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        conversation.state = state
        conversation.updated_at = datetime.utcnow()
        self.save(conversation)
    
    def list_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Conversation]:
        user_conversations = [
            conv for conv in self._storage.values()
            if conv.user_id == user_id
        ]
        user_conversations.sort(key=lambda x: x.updated_at, reverse=True)
        return user_conversations[offset:offset + limit]
    
    def get_active_conversations(self, user_id: str) -> List[Conversation]:
        all_conversations = self.list_by_user(user_id, limit=1000)
        return [
            conv for conv in all_conversations
            if conv.state.status in ["processing", "waiting_for_user"]
        ]
