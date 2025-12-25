# RAG Chatbot Agent

A production-style chatbot backend built with FastAPI and LangGraph, featuring Retrieval-Augmented Generation (RAG) capabilities with OpenAI integration and conversation checkpointing.

## Features

- 🤖 AI-powered chatbot using OpenAI's GPT models
- 📚 RAG (Retrieval-Augmented Generation) with Chroma vector store
- 💾 Conversation persistence with SQLite checkpointing
- 🔄 Session-based chat management with LangGraph
- 🚀 FastAPI backend with async support
- 📝 Document ingestion from knowledge base

## Prerequisites

- Python 3.10 or higher (< 3.14)
- OpenAI API key
- `uv` package manager (recommended) or `pip`

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd chat-bot-demo
```

### 2. Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install Dependencies

Using `uv`:
```bash
uv sync
```

Or using `pip`:
```bash
pip install -e .
```

## Configuration

### 1. Create Environment File

Create a `.env` file in the project root:

```bash
touch .env
```

### 2. Configure Environment Variables

Add the following to your `.env` file:

```env
# Required: OpenAI API credentials
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model configurations (defaults shown)
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small

# Optional: Storage paths
LANGGRAPH_SQLITE_PATH=.data/checkpoints.sqlite3
CHROMA_DB_PATH=.data/chroma_db

# Optional: Server settings
APP_ENV=dev
LOG_LEVEL=INFO
PORT=8000
```

## Usage

### Step 1: Ingest Knowledge Base Documents

Before using the chatbot, populate the vector store with your documents:

1. Place your text files (`.txt`) in the `knowledge_base/` directory
2. Run the ingestion script:

```bash
uv run python ingest.py
```

This will:
- Load all `.txt` files from `knowledge_base/`
- Split them into chunks (1000 chars with 200 char overlap)
- Generate embeddings using OpenAI
- Store them in the Chroma vector database

### Step 2: Start the Server

Using `uv`:
```bash
uv run uvicorn main:app --reload
```

Or if you're in an activated virtual environment:
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### Step 3: Interact with the API

#### API Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Chat Endpoint

**POST** `/v1/chat`

Request body:
```json
{
  "session_id": "user-123",
  "messages": [
    {
      "role": "user",
      "content": "What is the story about?"
    }
  ]
}
```

Response:
```json
{
  "session_id": "user-123",
  "content": "The story is about..."
}
```

#### Example using cURL

```bash
curl -X POST "http://localhost:8000/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user-123",
    "messages": [
      {
        "role": "user",
        "content": "Tell me about the content in the knowledge base"
      }
    ]
  }'
```

#### Example using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat",
    json={
        "session_id": "user-123",
        "messages": [
            {
                "role": "user",
                "content": "What information do you have?"
            }
        ]
    }
)

print(response.json())
```

## Project Structure

```
chat-bot-demo/
├── app/
│   ├── adapters/          # External service adapters
│   │   └── providers/     # OpenAI client
│   ├── api/               # FastAPI routes
│   ├── core/              # Configuration
│   ├── llm/               # LangGraph agent & prompts
│   ├── models/            # Pydantic schemas
│   └── services/          # Business logic (chat, RAG)
├── knowledge_base/        # Documents for RAG ingestion
├── main.py               # FastAPI application entry point
├── ingest.py             # Document ingestion script
├── clear_session.py      # Utility to clear chat sessions
└── pyproject.toml        # Project dependencies
```

## Key Components

### RAG Service
The RAG service retrieves relevant documents from the vector store to provide context-aware responses.

### LangGraph Agent
Manages conversation flow with checkpointing, allowing resumption of chat sessions.

### Session Management
Each conversation is identified by a `session_id`, with full history persisted in SQLite.

## Maintenance

### Clear Chat Sessions

To clear all conversation history:

```bash
uv run python clear_session.py
```

### Update Knowledge Base

To update the knowledge base:
1. Add/modify files in `knowledge_base/`
2. Re-run the ingestion script: `uv run python ingest.py`

### View Logs

The application uses structured logging. Check console output for detailed request/response logs.

## Optional Dependencies

### PostgreSQL Backend (for production)

Install the PostgreSQL checkpoint backend:

```bash
uv sync --extra postgres
```

Then update your configuration to use PostgreSQL instead of SQLite.

## Troubleshooting

### OpenAI API Key Error
Ensure your `.env` file contains a valid `OPENAI_API_KEY`.

### No Documents Retrieved
Run `ingest.py` to populate the vector store before chatting.

### Port Already in Use
Change the port in `.env` or use: `uvicorn main:app --port 8001`

## License

MIT

## Author

Vuong Gia Hy
