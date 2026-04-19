import pytest
from unittest.mock import patch, Mock
import requests
from agent_engine.core.agent import Agent
from agent_engine.core.conversation import Conversation
from agent_engine.core.message import Message

def test_agent_initialization():
    agent = Agent(name="Test Agent", system_prompt="Test Prompt")
    assert agent.name == "Test Agent"
    assert agent.system_prompt == "Test Prompt"

@patch("agent_engine.core.agent.requests.post")
def test_agent_generate_response_success(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {
        "message": {"role": "assistant", "content": "This is a mocked response from Gemma."}
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    agent = Agent()
    conv = Conversation()
    conv.add_message(Message(role="user", content="Hello"))
    reply = agent.generate_response(conv)

    assert reply == "This is a mocked response from Gemma."
    assert len(conv.messages) == 2  
    assert conv.messages[-1].content == "This is a mocked response from Gemma."
    mock_post.assert_called_once() 

@patch("agent_engine.core.agent.requests.post")
def test_agent_generate_response_failure(mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection Refused")
    
    agent = Agent()
    conv = Conversation()
    conv.add_message(Message(role="user", content="Hello"))
    
    reply = agent.generate_response(conv)
    
    assert "System Error" in reply
    assert len(conv.messages) == 2
    
