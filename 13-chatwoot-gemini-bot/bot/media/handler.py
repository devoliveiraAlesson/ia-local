"""Helpers para envio de múltiplos formatos de mídia via Chatwoot."""

from chatwoot.api import ChatwootClient


async def send_image(cw: ChatwootClient, conversation_id: int, url: str, caption: str = ""):
    return await cw.send_attachment(conversation_id, url, caption, "image")


async def send_video(cw: ChatwootClient, conversation_id: int, url: str, caption: str = ""):
    return await cw.send_attachment(conversation_id, url, caption, "video")


async def send_audio(cw: ChatwootClient, conversation_id: int, url: str):
    return await cw.send_attachment(conversation_id, url, "", "audio")


async def send_file(cw: ChatwootClient, conversation_id: int, url: str, caption: str = ""):
    return await cw.send_attachment(conversation_id, url, caption, "file")


async def send_card(
    cw: ChatwootClient,
    conversation_id: int,
    title: str,
    description: str,
    image_url: str = "",
    actions: list[dict] | None = None,
):
    """
    Envia card interativo (suportado em canais compatíveis).
    actions: [{"type": "link", "text": "Ver mais", "uri": "https://..."}]
    """
    template = {
        "items": [{
            "title": title,
            "description": description,
            "media_url": image_url,
            "actions": actions or [],
        }]
    }
    return await cw.send_template(conversation_id, template)


async def send_quick_replies(
    cw: ChatwootClient,
    conversation_id: int,
    text: str,
    options: list[str],
):
    """Envia mensagem com opções de resposta rápida."""
    buttons = [{"title": opt, "value": opt} for opt in options]
    template = {"type": "input_select", "content": text, "items": buttons}
    return await cw.send_template(conversation_id, template)
