from multiprocessing import connection
import sqlite3
from typing import Annotated, List, TypedDict
from chromadb.app import settings
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.func import END, START
from langgraph.graph import StateGraph, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.adapters.providers.openai_client import get_openai_chat
from app.llm.prompts import SYSTEM_PROMPT
from app.services.rag_service import search_knowledge_base


# Bind LLM with tools
llm_with_tools = get_openai_chat().bind_tools([search_knowledge_base])

# Define ChatState TypedDict
class ChatState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]

# Define the agent node
def agent_node(state: ChatState) -> ChatState:
    """
    The Agent node. It invokes the LLM with the current message history.
    The result will be either:
    A) A standard text message (AIMessage.content = "Hello")
    B) A tool call request (AIMessage.tool_calls = [...])
    """
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages=messages)
    
    return ChatState(
        messages=[response]
    )
    
def build_graph():
    graph = StateGraph(ChatState)
    
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode([search_knowledge_base]))
    
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent",  tools_condition)
    graph.add_edge("tools", "agent")

    conn = sqlite3.connect(settings.sqlite_path, check_same_thread=False)
    checkpointer = SqliteSaver(connection=conn)
    
    return graph.compile(checkpointer=checkpointer)

    
    