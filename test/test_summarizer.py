import pytest

from agent_engine.core.message import Message
from agent_engine.core.summarizer import Summarizer
from agent_engine.core.token_manager import TokenManager


@pytest.fixture
def summarizer():
    tm = TokenManager()
    return Summarizer(token_manager=tm, max_context_tokens=100)


def test_should_summarize(summarizer):
    # Create a long message that exceeds 100 tokens
    long_msg = Message(role="user", content="word " * 150)
    assert summarizer.should_summarize([long_msg]) is True

    short_msg = Message(role="user", content="Hello")
    assert summarizer.should_summarize([short_msg]) is False


def test_get_messages_to_summarize(summarizer):
    msgs = [Message(role="user", content=str(i)) for i in range(10)]
    # Keep last 4 messages -> 10 - 4 = 6 messages to summarize
    to_summarize = summarizer.get_messages_to_summarize(msgs, keep_last_n=4)

    assert len(to_summarize) == 6
    assert to_summarize[0].content == "0"
    assert to_summarize[-1].content == "5"


def test_build_summary_prompt(summarizer):
    msgs = [
        Message(role="user", content="Hi"),
        Message(role="assistant", content="Hello!"),
    ]
    prompt = summarizer.build_summary_prompt(msgs)
    assert "user: Hi" in prompt
    assert "assistant: Hello!" in prompt
