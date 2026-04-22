from datetime import datetime, timezone
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class MessageMetadata(BaseModel):
    processing_time_ms: int = Field(
        default=0,
        ge=0
    )
    
    input_tokens: int = Field(
        default=0,
        ge=0
    )
    
    output_tokens: int = Field(
        default=0,
        ge=0
    )
    
    model: Optional[str] = Field(default=None)
    
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)

    source: Optional[str] = Field(default=None)
    
    from_cache: bool = Field(default=False)
    
    extra: dict[str, Any] = Field(default_factory=dict)
   
    
    model_config = ConfigDict(
        frozen = True,
        json_encoders = {
            datetime: lambda v: v.isoformat()
        })
