from typing import Annotated, List, TypedDict
import sqlite3
from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.func import END, START
from langgraph.graph import StateGraph, add_messages

from app.adapters.providers.openai_client import get_openai_chat
from app.llm.prompts import SYSTEM_PROMPT
from app.core.config import settings


class ChatState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


graph = StateGraph(ChatState)

def chat_node(state: ChatState) -> ChatState:
    llm = get_openai_chat()

    system_msg = SystemMessage(content=SYSTEM_PROMPT)

    ai_message = llm.invoke([system_msg] + state["messages"])
    return {"messages": [ai_message]}

graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

def build_graph():
    # Create SQLite connection and pass to SqliteSaver constructor
    conn = sqlite3.connect(settings.sqlite_path, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    return graph.compile(checkpointer=checkpointer)