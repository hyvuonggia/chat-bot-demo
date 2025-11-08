from pyexpat.errors import messages
from typing import Literal, Optional
from pydantic import BaseModel, Field

Role = Literal['system', 'user', 'assistant', ]

class Message(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    messages: list[Message] = Field(..., description="List of messages in the chat session")
    stream: bool = Field(False, description="Whether to stream the response or not")
    
class ChatResponse(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    content: str = Field(..., description="The assistant's response content")
    model: Optional[str] = Field(None, description="The model used to generate the response")