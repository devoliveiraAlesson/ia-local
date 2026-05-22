# Construindo o Servidor MCP de Apresentações — Guia de Implementação

> Build do servidor FastMCP Python que encapsula o wizard, as skills de slides, a integração com Drive API + Slides API, e a aplicação de design tokens. Referência para o engenheiro de plataforma que vai construir o servidor.

## Por que um servidor próprio

Os servidores MCP do Google (Drive + Slides) expõem as APIs brutas. A empresa precisa da camada de negócio:

- **Wizard**: sequência de perguntas → outline JSON.
- **Design tokens**: leitura do `tokens.json`, resolução de aliases, conversão de unidades.
- **Skills**: patterns de layout encapsulados (TitleSlide, DataSlide, etc.).
- **Integração RAG**: buscar conteúdo na base de conhecimento antes de gerar.
- **Audit trail**: logar quem gerou o quê, qual versão de tokens foi usada.
- **Proxy das APIs Google**: centralizar a autenticação (service account + OAuth user) sem cada cliente lidar com isso.

Custo de construção: ~500–900 linhas Python. Manter: <0,2 FTE.

## Estrutura do projeto

```
mcp-apresentacoes/
├── pyproject.toml
├── src/
│   └── mcp_apresentacoes/
│       ├── __init__.py
│       ├── server.py         # entrypoint MCP — tools expostas
│       ├── wizard.py         # estado do wizard e etapas de perguntas
│       ├── tokens.py         # leitura e resolução de design tokens DTCG
│       ├── skills/
│       │   ├── __init__.py
│       │   ├── title_slide.py
│       │   ├── agenda_slide.py
│       │   ├── content_slide.py
│       │   ├── data_slide.py
│       │   ├── quote_slide.py
│       │   ├── section_divider.py
│       │   └── closing_slide.py
│       ├── drive_client.py   # wrapper Google Drive API
│       ├── slides_client.py  # wrapper Google Slides API
│       ├── rag_client.py     # cliente do servidor MCP RAG (Etapa 6)
│       ├── audit.py          # OTel spans + Langfuse
│       └── settings.py       # pydantic-settings
├── tests/
│   ├── test_tokens.py
│   ├── test_wizard.py
│   └── test_contract.py      # testa contract das tools via MCP Inspector
├── assets/
│   └── tokens.default.json   # tokens padrão de fallback
├── Dockerfile
└── deploy/
    └── k8s.yaml
```

## server.py — entrypoint e tools expostas

```python
from fastmcp import FastMCP
from .wizard import WizardSession, wizard_store
from .tokens import load_tokens
from .drive_client import DriveClient
from .slides_client import SlidesClient
from .audit import span
from .settings import settings

mcp = FastMCP("apresentacoes-corp")
drive = DriveClient(settings.service_account_key, settings.brand_assets_folder_id)
slides_api = SlidesClient(settings.service_account_key)


@mcp.tool(
    name="presentation.wizard_start",
    description=(
        "Inicia o wizard de criação de apresentação. Chame PRIMEIRO quando o usuário "
        "pedir para criar, fazer ou montar uma apresentação ou deck. "
        "Retorna a primeira pergunta do wizard e um session_id para usar nas próximas chamadas."
    ),
)
async def wizard_start(user_id: str) -> dict:
    session = WizardSession(user_id=user_id)
    wizard_store[session.id] = session
    return {
        "session_id": session.id,
        "step": session.current_step,
        "question": session.current_question(),
        "options": session.current_options(),
    }


@mcp.tool(
    name="presentation.wizard_answer",
    description=(
        "Responde a pergunta atual do wizard e avança para a próxima etapa. "
        "Use o session_id retornado por wizard_start. "
        "Quando 'done' for true, o outline está pronto e você pode chamar wizard_confirm."
    ),
)
async def wizard_answer(session_id: str, answer: str) -> dict:
    session = wizard_store.get(session_id)
    if not session:
        return {"error": "Session not found or expired"}
    
    session.record_answer(answer)
    
    if session.is_complete():
        outline = session.build_outline()
        return {
            "session_id": session_id,
            "done": True,
            "outline_preview": outline.to_human_readable(),
            "outline": outline.dict(),
        }
    
    return {
        "session_id": session_id,
        "done": False,
        "step": session.current_step,
        "question": session.current_question(),
        "options": session.current_options(),
    }


@mcp.tool(
    name="presentation.wizard_confirm",
    description=(
        "Confirma o outline e gera a apresentação no Google Drive. "
        "Chame após wizard_answer retornar done=true e o usuário confirmar o plano. "
        "Retorna o link do Google Slides e o ID do arquivo no Drive."
    ),
)
async def wizard_confirm(session_id: str, user_email: str) -> dict:
    session = wizard_store.get(session_id)
    if not session:
        return {"error": "Session not found or expired"}
    
    outline = session.build_outline()
    
    with span("presentation.generate", user=user_email, session=session_id) as s:
        tokens = await load_tokens(drive, outline.design.theme)
        
        # Copia o template correto
        new_file_id = await drive.copy_template(
            template_name=outline.design.template,
            new_title=outline.meta.title,
            destination_folder_id=settings.output_folder_id,
        )
        
        # Gera os requests batchUpdate para todos os slides
        all_requests = []
        for slide_plan in outline.slides:
            skill_fn = get_skill(slide_plan.skill)
            all_requests.extend(skill_fn(slide_plan.content, tokens, outline.design.theme))
        
        # Aplica tudo de uma vez
        await slides_api.batch_update(new_file_id, all_requests)
        
        # Compartilha com o usuário
        await drive.share(new_file_id, user_email, role="writer")
        
        url = f"https://docs.google.com/presentation/d/{new_file_id}/edit"
        s.set_attribute("presentation_id", new_file_id)
        s.set_attribute("slides_count", len(outline.slides))
    
    del wizard_store[session_id]
    
    return {
        "url": url,
        "presentation_id": new_file_id,
        "slides_count": len(outline.slides),
        "theme": outline.design.theme,
        "template": outline.design.template,
        "tokens_version": tokens.version,
    }


@mcp.tool(
    name="presentation.list_templates",
    description="Lista os templates disponíveis na pasta de brand assets do Drive.",
)
async def list_templates() -> dict:
    templates = await drive.list_templates()
    return {"templates": templates}


@mcp.tool(
    name="presentation.update_slide",
    description=(
        "Atualiza o conteúdo de um slide específico de uma apresentação existente. "
        "Use quando o usuário quiser editar um deck já criado."
    ),
)
async def update_slide(
    presentation_id: str,
    slide_index: int,
    new_title: str | None = None,
    new_body: str | None = None,
) -> dict:
    slide_info = await slides_api.get_page(presentation_id, slide_index)
    requests = build_update_requests(slide_info, new_title, new_body)
    await slides_api.batch_update(presentation_id, requests)
    return {"updated": True, "slide_index": slide_index}


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8081)
```

## tokens.py — leitura e resolução DTCG

```python
import json
import re
from dataclasses import dataclass
from typing import Any
from .drive_client import DriveClient

@dataclass
class ResolvedTokens:
    raw: dict
    version: str

    def get(self, path: str) -> Any:
        """Resolve um token por path pontilhado, seguindo aliases {a.b.c}."""
        value = _traverse(self.raw, path.split("."))
        if isinstance(value, dict) and "$value" in value:
            raw_val = value["$value"]
            return self._resolve_alias(raw_val)
        raise KeyError(f"Token não encontrado: {path}")

    def _resolve_alias(self, value: Any, depth: int = 0) -> Any:
        if depth > 10:
            raise ValueError("Alias circular detectado")
        if isinstance(value, str) and re.match(r"^\{.+\}$", value):
            ref_path = value[1:-1]  # remove { e }
            return self.get(ref_path)
        if isinstance(value, list):
            return [self._resolve_alias(v, depth + 1) for v in value]
        return value

    def hex_to_rgb(self, hex_color: str) -> dict:
        """Converte #RRGGBB para dict {red, green, blue} com valores 0.0–1.0."""
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return {"red": r / 255, "green": g / 255, "blue": b / 255}

    def pt_to_emu(self, pt_str: str) -> int:
        """Converte '32pt' para EMU (1pt = 12700 EMU)."""
        pt = float(pt_str.replace("pt", "").replace("px", ""))
        return int(pt * 12700)


def _traverse(obj: dict, keys: list[str]) -> Any:
    if not keys:
        return obj
    key = keys[0]
    if key not in obj:
        raise KeyError(f"Chave não encontrada: {key}")
    return _traverse(obj[key], keys[1:])


async def load_tokens(drive: DriveClient, theme: str = "default") -> ResolvedTokens:
    """Carrega tokens.json do Drive e retorna um objeto resolvível."""
    raw = await drive.read_json("tokens.json")
    version = raw.get("$version", "unknown")
    return ResolvedTokens(raw=raw, version=version)
```

## wizard.py — estado e etapas de perguntas

```python
import uuid
from dataclasses import dataclass, field
from typing import Optional
from .outline import Outline, SlidePlan, Meta, Design

WIZARD_STEPS = [
    "objective",
    "audience",
    "structure",
    "template",
    "confirm",
]

QUESTIONS = {
    "objective": {
        "text": "Qual é o objetivo principal desta apresentação?",
        "options": [
            "Proposta comercial / oferta para cliente",
            "Report executivo / update de resultados",
            "Treinamento interno / onboarding",
            "Pitch de produto ou ideia",
            "Apresentação de projeto / briefing",
            "Outro",
        ],
    },
    "audience": {
        "text": "Quem vai ver esta apresentação? (descreva livremente)",
        "options": None,
    },
    "structure": {
        "text": (
            "Me ajuda com a estrutura:\n"
            "1. Título ou tema central do deck?\n"
            "2. Quais 3–6 seções ou pontos principais?\n"
            "3. Tem dados ou gráficos para incluir?\n"
            "(pode responder tudo junto)"
        ),
        "options": None,
    },
    "template": {
        "text": "Qual template e tema visual prefere?",
        "options": None,  # preenchido dinamicamente com templates do Drive
    },
}


@dataclass
class WizardSession:
    user_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    current_step: int = 0
    answers: dict = field(default_factory=dict)

    def current_question(self) -> str:
        step_name = WIZARD_STEPS[self.current_step]
        return QUESTIONS.get(step_name, {}).get("text", "")

    def current_options(self) -> Optional[list]:
        step_name = WIZARD_STEPS[self.current_step]
        return QUESTIONS.get(step_name, {}).get("options")

    def record_answer(self, answer: str):
        step_name = WIZARD_STEPS[self.current_step]
        self.answers[step_name] = answer
        self.current_step += 1

    def is_complete(self) -> bool:
        return self.current_step >= len(WIZARD_STEPS) - 1  # -1: confirm é feito pelo agent

    def build_outline(self) -> "Outline":
        # Parsear respostas e construir outline
        # (implementação simplificada; em produção usar LLM para interpretar resposta livre)
        return Outline(
            meta=Meta(
                title=self._extract_title(),
                author=self.user_id,
                audience=self.answers.get("audience", ""),
                objective=self.answers.get("objective", ""),
            ),
            design=Design(
                template=self._extract_template(),
                theme=self._extract_theme(),
            ),
            slides=self._build_slides(),
        )


wizard_store: dict[str, WizardSession] = {}
```

## drive_client.py — wrapper Drive API

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
]

class DriveClient:
    def __init__(self, service_account_key: str, brand_folder_id: str):
        creds = service_account.Credentials.from_service_account_file(
            service_account_key, scopes=SCOPES
        )
        self._svc = build("drive", "v3", credentials=creds)
        self._brand_folder_id = brand_folder_id

    async def list_templates(self) -> list[dict]:
        """Lista templates .gslides na pasta /templates do Drive."""
        templates_folder = self._get_subfolder_id("templates")
        result = self._svc.files().list(
            q=f"'{templates_folder}' in parents and mimeType='application/vnd.google-apps.presentation'",
            fields="files(id,name,description)",
        ).execute()
        return result.get("files", [])

    async def copy_template(self, template_name: str, new_title: str, destination_folder_id: str) -> str:
        """Copia template pelo nome e retorna o ID do novo arquivo."""
        templates = await self.list_templates()
        template = next((t for t in templates if template_name in t["name"]), None)
        if not template:
            raise ValueError(f"Template '{template_name}' não encontrado no Drive")
        
        body = {
            "name": new_title,
            "parents": [destination_folder_id],
        }
        copied = self._svc.files().copy(fileId=template["id"], body=body).execute()
        return copied["id"]

    async def read_json(self, filename: str) -> dict:
        """Lê um arquivo JSON da pasta brand-assets."""
        result = self._svc.files().list(
            q=f"'{self._brand_folder_id}' in parents and name='{filename}'",
            fields="files(id)",
        ).execute()
        files = result.get("files", [])
        if not files:
            raise FileNotFoundError(f"{filename} não encontrado na pasta brand-assets")
        
        content = self._svc.files().get_media(fileId=files[0]["id"]).execute()
        return json.loads(content)

    async def share(self, file_id: str, email: str, role: str = "writer"):
        """Compartilha arquivo com usuário."""
        permission = {"type": "user", "role": role, "emailAddress": email}
        self._svc.permissions().create(
            fileId=file_id,
            body=permission,
            sendNotificationEmail=False,
        ).execute()
```

## Configuração e deploy

`settings.py` (pydantic-settings):

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    service_account_key: str = "/etc/mcp/service-account.json"
    brand_assets_folder_id: str
    output_folder_id: str
    rag_mcp_url: str = ""  # URL do servidor MCP RAG (Etapa 6); vazio = desabilitado
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    log_level: str = "INFO"

    class Config:
        env_prefix = "MCP_PRES_"

settings = Settings()
```

`Dockerfile`:

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY src ./src

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /app /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8081
CMD ["python", "-m", "mcp_apresentacoes.server"]
```

Adicionar ao Claude Code (escopo user ou project):

```bash
# Local (dev)
claude mcp add --scope user apresentacoes \
  -- python -m mcp_apresentacoes.server --transport stdio

# Remoto (produção)
claude mcp add --transport http --scope user \
  apresentacoes https://mcp.empresa.local/apresentacoes
```

## Validação de contrato (CI)

```python
# tests/test_contract.py
import asyncio
from fastmcp import Client

async def test_tools_contract():
    async with Client("http://localhost:8081/mcp") as c:
        tools = {t.name: t for t in await c.list_tools()}
        
        assert "presentation.wizard_start" in tools
        assert "presentation.wizard_answer" in tools
        assert "presentation.wizard_confirm" in tools
        assert "presentation.list_templates" in tools
        
        # Testa fluxo completo do wizard em modo de teste
        r1 = await c.call_tool("presentation.wizard_start", {"user_id": "test-user"})
        assert "session_id" in r1
        assert "question" in r1
        
        r2 = await c.call_tool("presentation.wizard_answer", {
            "session_id": r1["session_id"],
            "answer": "Proposta comercial"
        })
        assert "done" in r2
```

## Custo estimado

| Item | Custo anual |
|---|---|
| 0,2 FTE de eng de plataforma (constrói + mantém) | R$ 40–70k (BR) / US$ 20–35k |
| Google Cloud: Slides API + Drive API (usage-based) | Praticamente gratuito para volume corporativo (<500 decks/mês) |
| Container no K8s / Cloud Run | R$ 500–1.500/mês |
| Langfuse / observabilidade | Já incluso na Etapa 4 |
| **Total incremental** | **~R$ 50–80k/ano** |

ROI: um analista que economiza 3h/semana formatando slides = ~R$ 15–30k/ano em produtividade recuperada por pessoa. Com 5 usuários frequentes, o sistema se paga em 2–3 meses.

## Referências

- FastMCP: <https://github.com/jlowin/fastmcp>
- Google Drive API Python: <https://developers.google.com/drive/api/quickstart/python>
- Google Slides API Python: <https://developers.google.com/workspace/slides/api/quickstart/python>
- pydantic-settings: <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>
- python-pptx (para export .pptx): <https://python-pptx.readthedocs.io/>
- PPT Automation MCP Server (referência Windows): <https://github.com/socamalo/PPT_MCP_Server>
- Agentic PPT Generator com python-pptx + n8n: <https://github.com/prakhar483/Agentic-Based-Presentation-Generator>
