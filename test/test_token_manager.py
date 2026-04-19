import pytest
from hypothesis import given, strategies as st, settings as hyp_settings
from agent_engine.core.token_manager import TokenManager
from agent_engine.core.message import Message

@pytest.fixture
def tokenizer():
    return TokenManager("gpt-4")

def test_empty_string_tokens(tokenizer):
    assert tokenizer.count_string_tokens("") == 0
    assert tokenizer.count_string_tokens(None) == 0

# Hypothesis tests can't use pytest fixtures as parameters,
# so we create the tokenizer inside the test
@given(text=st.text(min_size=1, max_size=1000))
@hyp_settings(max_examples=50)
def test_string_token_counting_never_fails(text):
    tokenizer = TokenManager("gpt-4")
    count = tokenizer.count_string_tokens(text)
    assert isinstance(count, int)
    assert count > 0

def test_message_token_calculation(tokenizer):
    msg = Message(role="user", content="Hello world")
    # "user" = 1 token, "Hello world" = 2 tokens, plus 3 structural tokens = 6
    count = tokenizer.count_message_tokens(msg)
    assert count >= 6

def test_total_tokens_and_limit(tokenizer):
    messages = [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="Explain AI.")
    ]
    total = tokenizer.get_total_tokens(messages)
    assert isinstance(total, int)
    
    # Test boundary limits
    assert tokenizer.is_within_limit(messages, max_tokens=10000) is True
    assert tokenizer.is_within_limit(messages, max_tokens=5) is False
    