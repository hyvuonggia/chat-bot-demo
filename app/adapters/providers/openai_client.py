from langchain_openai import ChatOpenAI
from app.core.config import settings


def get_openai_chat(tempurature: float = 0.5, timeout: int = 30):
    """
    Returns an OpenAI chat client configured with the API key from settings.
    """
    return ChatOpenAI(model=settings.openai_chat_model,
                      temperature=tempurature,
                      openai_api_key=settings.openai_api_key,
                      request_timeout=timeout)