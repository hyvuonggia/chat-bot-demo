from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.llm.graph import build_graph
from app.models.schemas import ChatRequest

# call to compile the graph
graph = build_graph()

def chat_once(req: ChatRequest) -> str:
    langchain_messages: List = []
    for msg in req.messages:
        if msg.role == 'system':
            langchain_messages.append(SystemMessage(content=msg.content))
        elif msg.role == 'user':
            langchain_messages.append(HumanMessage(content=msg.content))
        elif msg.role == 'assistant':
            langchain_messages.append(AIMessage(content=msg.content))
        else:
            raise ValueError(f"Unknown role: {msg.role}")
        
    # map session_id to thread_id of langgraph
    config = {
        "configurable" : {
            "thread_id": req.session_id
        }
    }
    
    #invoke the graph
    result_state = graph.invoke(input={"messages": langchain_messages}, config=config)
    
    ai_reply = result_state["messages"][-1].content
    
    return ai_reply
    
    
    
    
    