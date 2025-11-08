# test_graph.py
from app.models.schemas import ChatRequest, Message
from app.services.chat import chat_once

message = input("Enter your message: ")

def main():
    req = ChatRequest(
        session_id="local-test-1",
        messages=[Message(role="user", content=message)]
    )
    reply = chat_once(req)
    print("AI reply:", reply)

if __name__ == "__main__":
    main()
