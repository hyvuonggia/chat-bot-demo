import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):

    """
    Centralized runtime configuration loaded from environment variables
    """

    # API keys / models
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_chat_model: str = Field("gpt-4o-mini", alias="OPENAI_CHAT_MODEL")
    openai_embed_model: str = Field("text-embedding-3-small", alias="OPENAI_EMBED_MODEL")

    # LangGraph checkpointing (SQLite path)
    sqlite_path: str = Field(".data/checkpoints.sqlite3", alias="LANGGRAPH_SQLITE_PATH")

    # Server/runtime
    app_env: str = Field("dev", alias="APP_ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    port: int = Field(8000, alias="PORT")

    model_config = SettingsConfigDict(
        env_file=".env",          # read .env
    )

settings = Settings()


