import logging

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from agent_engine.core.message import Message

logger = logging.getLogger(__name__)


# --- 1. Fixtures ---
@pytest.fixture
def valid_message_data():
    """
    Inputs: None
    Outputs: Dictionary containing valid message parameters
    Description: It Provides valid data as base for testing to ensure (Isolation)
    """
    return {
        "role": "user",
        "content": "Hello, Agent!",
        "tokens": 10,
        "metadata": {"session_id": "test_123"},
    }


# --- 2. Functional & Validation Tests ---
@pytest.mark.parametrize("role", ["system", "user", "assistant", "tool"])
def test_message_creation_valid_roles(role, valid_message_data):
    """
    Inputs: Role string from parametrize
    Outputs: None (Passes if no exception raised)
    Description: Testing acceptance of all allowed roles in the system.
    """
    valid_message_data["role"] = role
    msg = Message(**valid_message_data)
    assert msg.role == role
    logger.info(f"Successfully validated role: {role}")


@pytest.mark.parametrize("invalid_role", ["admin", "bot", 123, None])
def test_message_invalid_role_raises_error(invalid_role, valid_message_data):
    """
    Inputs: Invalid role values
    Outputs: Raises pydantic.ValidationError
    Description: Make sure that the system is denying any predefined roles.
    """
    valid_message_data["role"] = invalid_role
    with pytest.raises(ValidationError):
        Message(**valid_message_data)


def test_message_immutability(valid_message_data):
    """
    Inputs: Valid message instance
    Outputs: Raises ValidationError/AttributeError on mutation
    Description: Testing the immutability of the message.
    """
    msg = Message(**valid_message_data)
    with pytest.raises(ValidationError):
        msg.content = "New Content"


def test_invalid_tokens_negative(valid_message_data):
    """
    Inputs: Negative token count
    Outputs: Raises ValidationError
    Description: Testing the negative token count.
    """
    valid_message_data["tokens"] = -1
    with pytest.raises(ValidationError):
        Message(**valid_message_data)


# --- 3. Property-Based Testing (Hypothesis) ---
@given(content=st.text(min_size=1), tokens=st.integers(min_value=0, max_value=1000000))
def test_message_stress_test_inputs(content, tokens):
    """
    Inputs: Randomly generated strings and integers from Hypothesis
    Outputs: None (Passes if Message is created successfully)
    Description: Testing the stress test inputs.
    """
    msg = Message(role="user", content=content, tokens=tokens)
    assert msg.content == content
    assert msg.tokens == tokens


# --- 4. Logic & Methods Tests ---
def test_to_log_format(valid_message_data):
    """
    Inputs: Valid message
    Outputs: Formatted string
    Description: Testing the log format of the message.
    """
    msg = Message(**valid_message_data)
    log_str = msg.to_log_format()
    assert "[USER]" in log_str
    assert "Hello, Agent!" in log_str
    assert "10 tokens" in log_str
    