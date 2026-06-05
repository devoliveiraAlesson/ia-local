"""Recebe e valida webhooks do Chatwoot."""

import hashlib
import hmac
import structlog
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from config import get_settings
from chatwoot.api import ChatwootClient
from agent.orchestrator import handle_message

log = structlog.get_logger()
router = APIRouter()


def verify_signature(body: bytes, signature: str, secret: str) -> bool:
    if not secret:
        return True
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def process_event(payload: dict):
    """Processa evento do Chatwoot em background."""
    event = payload.get("event")

    # Só nos interessa mensagens recebidas (incoming)
    if event != "message_created":
        return
    if payload.get("message_type") != "incoming":
        return

    # Ignora mensagens de bots (evita loop)
    sender = payload.get("sender", {})
    if sender.get("type") == "agent_bot":
        return

    conversation = payload.get("conversation", {})
    conversation_id = conversation.get("id")
    contact_id = payload.get("sender", {}).get("id")
    content = payload.get("content") or ""

    if not conversation_id or not content.strip():
        return

    # Verifica se o bot está ativo para esta conversa
    s = get_settings()
    if s.bot_inbox_id:
        inbox_id = str(conversation.get("inbox_id", ""))
        if inbox_id != s.bot_inbox_id:
            log.debug("skipped_inbox", inbox_id=inbox_id)
            return

    log.info("incoming_message", conversation_id=conversation_id, chars=len(content))

    cw = ChatwootClient()
    await handle_message(
        conversation_id=conversation_id,
        contact_id=contact_id,
        user_message=content,
        cw=cw,
    )


@router.post("/webhook")
async def chatwoot_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    s = get_settings()

    sig = request.headers.get("X-Chatwoot-Signature", "")
    if s.bot_webhook_secret and not verify_signature(body, sig, s.bot_webhook_secret):
        raise HTTPException(status_code=401, detail="Assinatura inválida")

    payload = await request.json()
    background_tasks.add_task(process_event, payload)

    return {"status": "accepted"}
