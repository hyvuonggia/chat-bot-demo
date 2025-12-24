from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.llm.graph import build_graph
from app.models.schemas import ChatRequest

# call to compile the graph
graph = build_graph()

def chat_once(req: ChatRequest) -> str:
    print(f"[DEBUG CHAT] chat_once called for session: {req.session_id}")
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
    
    print(f"[DEBUG CHAT] Prepared {len(langchain_messages)} messages")
    print(f"[DEBUG CHAT] Last message: {langchain_messages[-1].content if langchain_messages else 'None'}")
        
    # map session_id to thread_id of langgraph
    config = {
        "configurable" : {
            "thread_id": req.session_id
        }
    }
    
    #invoke the graph
    print(f"[DEBUG CHAT] Invoking graph with thread_id: {req.session_id}")
    print(f"[DEBUG CHAT] NOTE: LangGraph will load previous conversation history from checkpoints if exists")
    result_state = graph.invoke(input={"messages": langchain_messages}, config=config)
    
    print(f"[DEBUG CHAT] Graph returned {len(result_state['messages'])} messages")
    ai_reply = result_state["messages"][-1].content
    print(f"[DEBUG CHAT] AI reply: {ai_reply[:200] if ai_reply else 'None'}...")
    
    return ai_reply
    
    
    
    
    