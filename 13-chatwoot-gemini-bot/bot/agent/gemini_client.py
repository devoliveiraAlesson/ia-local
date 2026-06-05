"""Wrapper do Gemini com suporte a histórico, tools e streaming."""

import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import structlog

from config import get_settings

log = structlog.get_logger()


def _build_client() -> genai.GenerativeModel:
    s = get_settings()
    genai.configure(api_key=s.gemini_api_key)
    return genai.GenerativeModel(
        model_name=s.gemini_model,
        system_instruction=s.bot_system_prompt,
        generation_config=GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
        ),
    )


_model: genai.GenerativeModel | None = None


def get_model() -> genai.GenerativeModel:
    global _model
    if _model is None:
        _model = _build_client()
    return _model


def build_history(messages: list[dict]) -> list[dict]:
    """Converte histórico do Chatwoot para o formato do Gemini."""
    history = []
    for msg in messages:
        if msg.get("message_type") == 2:
            continue  # ignora mensagens de atividade
        role = "model" if msg.get("message_type") == 1 else "user"
        content = msg.get("content") or ""
        if content.strip():
            history.append({"role": role, "parts": [content]})
    return history


async def chat(
    user_message: str,
    history: list[dict],
    context_chunks: list[str] | None = None,
    tools: list | None = None,
) -> str:
    """
    Envia mensagem ao Gemini e retorna resposta em texto.
    - history: histórico no formato Gemini (build_history)
    - context_chunks: trechos do RAG inseridos como contexto
    - tools: lista de FunctionDeclarations do Gemini
    """
    model = get_model()

    # Injeta contexto RAG antes da pergunta do usuário
    prompt = user_message
    if context_chunks:
        ctx = "\n---\n".join(context_chunks)
        prompt = (
            f"[CONTEXTO DA BASE DE CONHECIMENTO]\n{ctx}\n\n"
            f"[PERGUNTA DO USUÁRIO]\n{user_message}"
        )

    try:
        chat_session = model.start_chat(history=history)
        response = await chat_session.send_message_async(prompt)
        return response.text
    except Exception as exc:
        log.error("gemini_error", error=str(exc))
        return "Desculpe, tive um problema ao processar sua mensagem. Tente novamente em instantes."


async def embed_text(text: str) -> list[float]:
    """Gera embedding via Gemini para indexação no Qdrant."""
    s = get_settings()
    genai.configure(api_key=s.gemini_api_key)
    result = await genai.embed_content_async(
        model=s.gemini_embedding_model,
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]
