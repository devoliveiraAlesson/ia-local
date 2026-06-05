from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    gemini_embedding_model: str = "models/text-embedding-004"

    chatwoot_url: str = "http://localhost:3000"
    chatwoot_api_token: str
    chatwoot_account_id: int = 1

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "knowledge_base"

    bot_webhook_secret: str = ""
    bot_inbox_id: str = ""

    # Nome do agente bot que aparece no Chatwoot
    bot_agent_name: str = "Assistente IA"

    # Instrução de sistema do bot (personalize aqui)
    bot_system_prompt: str = """Você é um assistente de atendimento inteligente e prestativo.
Responda sempre em português brasileiro, de forma clara, objetiva e amigável.
Use as informações da base de conhecimento quando disponíveis.
Se não souber algo, diga isso com transparência e ofereça encaminhar para um atendente humano."""

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
