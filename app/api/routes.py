import uuid
from fastapi import APIRouter, HTTPException, Request
from openai.resources import Chat

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat import chat_once


router = APIRouter()

@router.post("/v1/chat", response_model=ChatResponse, tags=["chat"])
def chat(chat_request: ChatRequest, request: Request):
    
    req_id = str(uuid.uuid4())
    print(f"{req_id} - Received chat request for session_id: {chat_request.session_id} \
        with {len(chat_request.messages)} messages")
    
    try:
        reply_text = chat_once(chat_request)
        
    except Exception as e:
        print(f"{req_id} - Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    print(f"{req_id} - Sending reply for session_id: {chat_request.session_id}")
    return ChatResponse(session_id=chat_request.session_id, content=reply_text)
    