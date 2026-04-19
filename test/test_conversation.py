import logging

from agent_engine.core.conversation import Conversation
from agent_engine.core.message import Message

logger = logging.getLogger(__name__)


def test_conversation_initialization():
    """Inputs: None
    Outputs: None (Passes if no exception raised)
    Description: Testing the basic initialization of the conversation.
    """
    conv = Conversation()
    assert conv.get_total_tokens() == 0


def test_sliding_window_enforces_budget():
    """Inputs: None
    Outputs: None (Passes if no exception raised)
    Description: Testing the sliding window algorithm to enforce token budget.
    """
    logger.info("Testing Sliding Window Context Trimming...")
    conv = Conversation(max_tokens=100)

    conv.add_message(Message(role="system", content="System Setup", tokens=10))
    conv.add_message(Message(role="user", content="Question 1", tokens=50))
    conv.add_message(Message(role="assistant", content="Answer 1", tokens=30))

    # Adding a message that exceeds the token budget
    conv.add_message(Message(role="user", content="Question 2", tokens=40))

    # The system should evict the first user message to stay within the budget
    assert conv.get_total_tokens() <= 100
    assert conv.messages[0].role == "system"


def test_to_llm_payload():
    """Inputs: None
    Outputs: None (Passes if no exception raised)
    Description: Testing the conversion of the class to a format understood by the APIs.
    """
    conv = Conversation()
    conv.add_message(Message(role="user", content="Hello"))

    payload = conv.to_llm_payload()
    assert isinstance(payload, list)
    assert payload[0]["role"] == "user"
    assert "tokens" not in payload[0]  # The API should not see the tokens field


def test_clear_history():
    """Inputs: None
    Outputs: None (Passes if no exception raised)
    Description: Testing the clearing of the conversation history.
    """
    conv = Conversation()
    conv.add_message(Message(role="system", content="You are a bot"))
    conv.add_message(Message(role="user", content="Hi"))

    conv.clear_history(keep_system=True)
    assert len(conv.messages) == 1
    assert conv.messages[0].role == "system"
