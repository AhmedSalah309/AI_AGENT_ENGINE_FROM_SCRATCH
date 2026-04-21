from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from agent_engine.config.settings import settings


class AgentConfig(BaseModel):
    model_name: str = Field(
        default=settings.DEFAULT_MODEL,
        description="Name of the LLM model to use"
    )
    
    temperature: float = Field(
        default=settings.TEMPERATURE,
        ge=0.0,
        le=2.0,
        description="The temperature of the language model (degree of randomness)"
    )
    
    max_tokens: int = Field(
        default=4096,
        ge=1,
        le=128000,
        description="The maximum number of tokens in the response"
    )
    
    max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="The maximum number of iterations before the final response"
    )
    
    timeout_seconds: int = Field(
        default=30,
        ge=1,
        le=300,
        description="The maximum time to execute the agent in seconds"
    )
    
    allowed_tools: List[str] = Field(
        default_factory=list,
        description="List of tool names allowed for the agent to use"
    )
    
    system_prompt: Optional[str] = Field(
        default=None,
        description="The system prompt for the agent"
    )
    
    llm_provider: Literal["openai", "anthropic", "local"] = Field(
        default="openai",
        description="The LLM provider to use"
    )
    
    enable_streaming: bool = Field(
        default=False,
        description="Whether the agent supports streaming responses"
    )
    
    retry_count: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Number of retry attempts when the language model call fails"
    )
    
    model_config = ConfigDict(
        frozen = True,
        extra = "ignore"
    )
