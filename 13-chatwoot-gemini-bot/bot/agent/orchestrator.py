"""
Orquestrador principal do agente.
Decide se responde com bot ou escalona para humano,
monta o contexto RAG e chama o Gemini.
"""

import structlog
from chatwoot.api import ChatwootClient
from agent.gemini_client import chat, build_history
from agent.rag import search

log = structlog.get_logger()

# Palavras-chave que disparam escalonamento para humano
ESCALATION_TRIGGERS = [
    "falar com atendente",
    "falar com humano",
    "atendente humano",
    "pessoa real",
    "quero falar com alguém",
    "suporte humano",
]


def should_escalate(text: str) -> bool:
    low = text.lower()
    return any(t in low for t in ESCALATION_TRIGGERS)


async def handle_message(
    conversation_id: int,
    contact_id: int,
    user_message: str,
    cw: ChatwootClient,
):
    """Ponto de entrada para cada nova mensagem recebida."""

    # 1. Verifica se usuário quer atendente humano
    if should_escalate(user_message):
        await cw.send_text(
            conversation_id,
            "Entendido! Vou transferir você para um de nossos atendentes agora. Aguarde um momento.",
        )
        await cw.toggle_status(conversation_id, "open")
        await cw.add_label(conversation_id, ["escalado-humano"])
        log.info("escalated_to_human", conversation_id=conversation_id)
        return

    # 2. Busca histórico da conversa
    raw_messages = await cw.get_messages(conversation_id)
    # Mantém apenas as últimas 20 trocas para não estourar contexto
    history = build_history(raw_messages[-20:])

    # 3. RAG — busca contexto relevante na base de conhecimento
    context_chunks = await search(user_message, top_k=4)

    # 4. Enriquece contexto com dados do contato (opcional)
    try:
        contact = await cw.get_contact(contact_id)
        contact_info = (
            f"Nome: {contact.get('name', 'Não informado')}, "
            f"Email: {contact.get('email', 'Não informado')}, "
            f"Telefone: {contact.get('phone_number', 'Não informado')}"
        )
        if context_chunks:
            context_chunks.insert(0, f"[Dados do contato]\n{contact_info}")
    except Exception:
        pass

    # 5. Chama o Gemini
    response_text = await chat(
        user_message=user_message,
        history=history,
        context_chunks=context_chunks or None,
    )

    # 6. Envia resposta pelo Chatwoot
    await cw.send_text(conversation_id, response_text)
    log.info("bot_replied", conversation_id=conversation_id, chars=len(response_text))
