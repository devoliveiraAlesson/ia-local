"""Cliente para a API REST do Chatwoot."""

import httpx
from typing import Any
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

from config import get_settings

log = structlog.get_logger()


class ChatwootClient:
    def __init__(self):
        s = get_settings()
        self.base = f"{s.chatwoot_url}/api/v1/accounts/{s.chatwoot_account_id}"
        self.headers = {
            "api_access_token": s.chatwoot_api_token,
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def _post(self, path: str, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{self.base}{path}", json=payload, headers=self.headers)
            r.raise_for_status()
            return r.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def _patch(self, path: str, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.patch(f"{self.base}{path}", json=payload, headers=self.headers)
            r.raise_for_status()
            return r.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def _get(self, path: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{self.base}{path}", params=params, headers=self.headers)
            r.raise_for_status()
            return r.json()

    # ── Mensagens ────────────────────────────────────────────────────────────

    async def send_text(self, conversation_id: int, text: str, private: bool = False) -> dict:
        return await self._post(
            f"/conversations/{conversation_id}/messages",
            {"content": text, "message_type": "outgoing", "private": private},
        )

    async def send_attachment(
        self,
        conversation_id: int,
        file_url: str,
        caption: str = "",
        file_type: str = "image",
    ) -> dict:
        """Envia mídia via URL pública. Types: image | audio | video | file."""
        payload = {
            "content": caption,
            "message_type": "outgoing",
            "attachments": [{"resource_type": file_type, "file_url": file_url}],
        }
        return await self._post(f"/conversations/{conversation_id}/messages", payload)

    async def send_template(self, conversation_id: int, template: dict) -> dict:
        """Envia mensagem estruturada (cards/botões) para canais compatíveis."""
        return await self._post(
            f"/conversations/{conversation_id}/messages",
            {"content_type": "cards", "content_attributes": template, "message_type": "outgoing"},
        )

    # ── Conversas ────────────────────────────────────────────────────────────

    async def get_conversation(self, conversation_id: int) -> dict:
        return await self._get(f"/conversations/{conversation_id}")

    async def assign_agent(self, conversation_id: int, agent_id: int) -> dict:
        return await self._patch(
            f"/conversations/{conversation_id}/assignments",
            {"agent_id": agent_id},
        )

    async def toggle_status(self, conversation_id: int, status: str) -> dict:
        """status: open | resolved | pending | snoozed"""
        return await self._patch(
            f"/conversations/{conversation_id}",
            {"status": status},
        )

    async def add_label(self, conversation_id: int, labels: list[str]) -> dict:
        return await self._post(
            f"/conversations/{conversation_id}/labels",
            {"labels": labels},
        )

    async def get_messages(self, conversation_id: int) -> list[dict]:
        data = await self._get(f"/conversations/{conversation_id}/messages")
        return data.get("payload", [])

    # ── Contatos ─────────────────────────────────────────────────────────────

    async def get_contact(self, contact_id: int) -> dict:
        return await self._get(f"/contacts/{contact_id}")

    async def update_contact(self, contact_id: int, attributes: dict) -> dict:
        return await self._patch(f"/contacts/{contact_id}", attributes)

    async def search_contacts(self, query: str) -> list[dict]:
        data = await self._get("/contacts/search", {"q": query, "include_contacts": True})
        return data.get("payload", {}).get("contacts", [])

    # ── Agentes ──────────────────────────────────────────────────────────────

    async def list_agents(self) -> list[dict]:
        data = await self._get("/agents")
        return data if isinstance(data, list) else []

    # ── Inbox ────────────────────────────────────────────────────────────────

    async def list_inboxes(self) -> list[dict]:
        data = await self._get("/inboxes")
        return data.get("payload", [])
