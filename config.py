from langchain_ollama import ChatOllama

from settings import (
    MODEL_NAME,
    MODEL_TEMPERATURE,
    MODEL_MAX_OUTPUT_TOKENS,
    OLLAMA_BASE_URL,
)


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=MODEL_TEMPERATURE,
    num_predict=MODEL_MAX_OUTPUT_TOKENS,
    base_url=OLLAMA_BASE_URL
)