"""
Ferramentas externas que o agente pode chamar.
Adicione novas tools aqui e registre em TOOLS_REGISTRY.
"""

import httpx
import structlog

log = structlog.get_logger()


# ── Estrutura de tool ─────────────────────────────────────────────────────────

class ToolResult:
    def __init__(self, success: bool, data: dict | str):
        self.success = success
        self.data = data

    def __str__(self):
        if self.success:
            return f"[OK] {self.data}"
        return f"[ERRO] {self.data}"


# ── Tools disponíveis ─────────────────────────────────────────────────────────

async def buscar_cep(cep: str) -> ToolResult:
    """Consulta endereço pelo CEP."""
    cep = cep.replace("-", "").strip()
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(f"https://viacep.com.br/ws/{cep}/json/")
            r.raise_for_status()
            data = r.json()
            if data.get("erro"):
                return ToolResult(False, "CEP não encontrado.")
            return ToolResult(True, data)
        except Exception as e:
            log.error("tool_buscar_cep", error=str(e))
            return ToolResult(False, str(e))


async def enriquecer_lead(email: str) -> ToolResult:
    """
    Placeholder para enriquecimento de lead.
    Conecte aqui à sua API (Hunter.io, Clearbit, RD Station, etc.)
    """
    # Exemplo: retorna dados simulados
    return ToolResult(True, {
        "email": email,
        "empresa": "Não identificada",
        "cargo": "Desconhecido",
        "nota": "Integre com Hunter.io ou Clearbit para dados reais.",
    })


async def consultar_crm(contact_id: str) -> ToolResult:
    """
    Placeholder para consulta ao CRM.
    Adapte para seu CRM (RD Station, HubSpot, Pipedrive...).
    """
    return ToolResult(True, {
        "contact_id": contact_id,
        "status": "Conecte ao seu CRM aqui.",
    })


async def webhook_externo(url: str, payload: dict) -> ToolResult:
    """Dispara webhook para sistema externo."""
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return ToolResult(True, r.json())
        except Exception as e:
            log.error("tool_webhook_externo", error=str(e))
            return ToolResult(False, str(e))


# ── Registry ─────────────────────────────────────────────────────────────────

TOOLS_REGISTRY: dict[str, callable] = {
    "buscar_cep": buscar_cep,
    "enriquecer_lead": enriquecer_lead,
    "consultar_crm": consultar_crm,
    "webhook_externo": webhook_externo,
}


async def run_tool(name: str, **kwargs) -> ToolResult:
    fn = TOOLS_REGISTRY.get(name)
    if not fn:
        return ToolResult(False, f"Tool '{name}' não encontrada.")
    return await fn(**kwargs)
