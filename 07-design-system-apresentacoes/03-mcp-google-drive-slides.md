# Servidores MCP para Google Drive e Google Slides

> Catálogo e configuração dos servidores MCP disponíveis para integrar o agente ao Google Drive (leitura de brand assets) e ao Google Slides (criação e edição de apresentações). Inclui o servidor MCP oficial do Google e alternativas open source.

## Panorama — o que existe em 2026

O Google anunciou suporte oficial a MCP no Google Cloud Next '26, com mais de 50 servidores gerenciados em GA ou Preview. Para Workspace:

| Servidor | Tipo | Status | Recursos |
|---|---|---|---|
| `Google Drive MCP` (oficial) | Remote HTTP | GA | Listar, criar, ler, mover, buscar arquivos; aceitar permissões |
| `Google Slides MCP` (oficial, via Workspace) | Remote HTTP | Preview | Criar e editar apresentações via Slides API |
| `google-slides-mcp` (matteoantoci, community) | stdio / HTTP | Estável | 5 tools: create, get, batch_update, get_page, summarize |
| `google-drive-mcp` (piotr-agier, community) | stdio | Estável | Drive + Docs + Sheets + Slides + Calendar |
| `mcp-gdrive` (isaacphi, community) | stdio | Estável | Leitura Drive + edição Sheets |
| `Google Apps Script MCP` (community) | HTTP via GAS | Experimental | Acesso ao Workspace via Apps Script sem infra própria |

**Recomendação**: para produção corporativa, usar o servidor MCP oficial do Google Workspace (autenticação corporativa, SLA Google, sem infra própria para manter). Para POC e desenvolvimento, `google-slides-mcp` (community) é o caminho mais rápido.

## Servidor MCP oficial do Google Workspace

### Configuração

```bash
# Adicionar ao Claude Code (escopo user ou project)
claude mcp add --transport http --scope user \
  google-drive \
  https://mcp.googleapis.com/workspace/drive

claude mcp add --transport http --scope user \
  google-slides \
  https://mcp.googleapis.com/workspace/slides
```

Autenticação via OAuth 2.0 com conta Google Workspace corporativa. O servidor usa os escopos:
- `https://www.googleapis.com/auth/drive.readonly` (leitura de assets)
- `https://www.googleapis.com/auth/drive.file` (criar arquivos no Drive)
- `https://www.googleapis.com/auth/presentations` (criar e editar slides)

### Tools expostas (Drive)

| Tool | Descrição |
|---|---|
| `drive.list_files` | Lista arquivos numa pasta por ID ou path |
| `drive.get_file` | Retorna metadados e conteúdo (Google Docs como texto, Sheets como CSV) |
| `drive.create_file` | Cria arquivo no Drive (suporta upload de bytes) |
| `drive.copy_file` | Copia um arquivo para nova pasta — **fundamental para copiar templates** |
| `drive.search` | Busca full-text no Drive (por nome, tipo, conteúdo) |
| `drive.share` | Define permissões de compartilhamento |

### Tools expostas (Slides)

| Tool | Descrição |
|---|---|
| `slides.create` | Cria apresentação em branco com título |
| `slides.get` | Lê estrutura completa de uma apresentação |
| `slides.batch_update` | Aplica array de requests (add slide, insert text, update style, etc.) |
| `slides.get_page` | Lê um slide específico pelo índice ou objectId |
| `slides.summarize` | Extrai texto de todos os slides (útil para auditoria) |
| `slides.export` | Exporta como PDF ou .pptx via Drive API |

## Servidor MCP community — google-slides-mcp

Para desenvolvimento e POC antes de ter OAuth corporativo configurado.

### Instalação

```bash
# Clonar e instalar
git clone https://github.com/matteoantoci/google-slides-mcp
cd google-slides-mcp
npm install

# Configurar credenciais Google Cloud
# 1. Criar projeto no Google Cloud Console
# 2. Ativar Google Slides API e Google Drive API
# 3. Criar OAuth 2.0 credentials (Desktop app)
# 4. Baixar credentials.json para a pasta do servidor

# Adicionar ao Claude Code (stdio)
claude mcp add --scope user google-slides-dev \
  -- node /path/to/google-slides-mcp/dist/index.js
```

### Tools expostas

```
create_presentation(title: string) → { presentationId, url }
get_presentation(presentationId: string, fields?: string) → objeto completo da apresentação
batch_update_presentation(presentationId: string, requests: array) → resultado do batchUpdate
get_page(presentationId: string, pageObjectId: string) → detalhes do slide
summarize_presentation(presentationId: string, includeNotes?: boolean) → texto extraído
```

### Exemplo de uso direto (teste via MCP Inspector)

```bash
npx @modelcontextprotocol/inspector node /path/to/google-slides-mcp/dist/index.js
```

No Inspector, chamar `create_presentation` com `{"title": "Teste MCP"}` para verificar autenticação.

## Servidor MCP community — google-drive-mcp (piotr-agier)

Mais completo para leitura de assets (suporta Drive + Docs + Sheets + Slides + Calendar).

```bash
# Instalar via pip
pip install google-drive-mcp

# Configurar
export GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json

# Adicionar ao Claude Code
claude mcp add --scope user google-drive-full \
  -- python -m google_drive_mcp
```

**Útil para**: ler o `tokens.json` da pasta de brand assets, listar templates disponíveis, ler o conteúdo de um Slides existente para auditoria.

## Fluxo completo: criar apresentação a partir do template

Este é o padrão correto de uso da Google Slides API via MCP:

```
1. drive.list_files(folderId=BRAND_ASSETS_FOLDER_ID, mimeType="application/vnd.google-apps.presentation")
   → retorna lista de templates disponíveis

2. drive.copy_file(fileId=TEMPLATE_ID, name="Novo Deck — {titulo}", destinationFolderId=OUTPUT_FOLDER_ID)
   → cria cópia do template no Drive; retorna novo presentationId

3. slides.get(presentationId=NOVO_ID)
   → lê estrutura: quais slides existem, quais placeholders há em cada um, objectIds de shapes

4. slides.batch_update(presentationId=NOVO_ID, requests=[
     replaceAllText("{{slide_title}}", "Proposta Comercial ABC"),
     replaceAllText("{{author_name}}", "João Silva"),
     replaceAllText("{{date}}", "Maio 2026"),
     updateTextStyle(...),
     insertImage(logoUrl, position, size),
     ...
   ])
   → preenche o template com o conteúdo coletado pelo wizard

5. drive.share(fileId=NOVO_ID, email=USER_EMAIL, role="editor")
   → compartilha o deck com o usuário que pediu
```

> **Nota crítica**: a `presentations.create` da Slides API **não** cria slides com conteúdo. O fluxo correto é sempre `drive.copy_file` (para copiar o template) → `slides.batch_update` (para preencher). Tentar criar do zero via API é muito mais trabalhoso e perde a fidelidade visual do template.

## Requests batchUpdate mais usados

A Slides API aceita dezenas de request types. Os mais usados para geração de apresentações:

```json
// Substituir texto (placeholder filling)
{ "replaceAllText": {
    "replaceText": "Proposta Comercial",
    "containsText": { "text": "{{slide_title}}", "matchCase": true }
  }
}

// Inserir novo slide (a partir de layout do Slide Master)
{ "duplicateObject": { "objectId": "TEMPLATE_SLIDE_ID" } }

// Atualizar estilo de texto
{ "updateTextStyle": {
    "objectId": "SHAPE_ID",
    "textRange": { "type": "ALL" },
    "style": {
      "foregroundColor": { "opaqueColor": { "rgbColor": {"red": 0.1, "green": 0.14, "blue": 0.49} } },
      "fontSize": { "magnitude": 32, "unit": "PT" },
      "bold": true
    },
    "fields": "foregroundColor,fontSize,bold"
  }
}

// Inserir imagem (logo, gráfico)
{ "createImage": {
    "url": "https://drive.google.com/uc?id=LOGO_FILE_ID",
    "elementProperties": {
      "pageObjectId": "SLIDE_ID",
      "size": { "height": {"magnitude": 720000, "unit": "EMU"}, "width": {"magnitude": 2880000, "unit": "EMU"} },
      "transform": { "scaleX": 1, "scaleY": 1, "translateX": 6858000, "translateY": 180000, "unit": "EMU" }
    }
  }
}
```

## Autenticação em produção — service account vs OAuth por usuário

| Abordagem | Como funciona | Prós | Contras | Quando usar |
|---|---|---|---|---|
| **Service account** | Conta de serviço Google com chave JSON; acesso compartilhado à pasta de brand assets | Sem interação do usuário; perfeito para ler assets de marca | Arquivos criados ficam na conta da service account (não do usuário) | Leitura de `tokens.json` e templates |
| **OAuth por usuário** | Cada usuário autoriza o servidor via OIDC/OAuth flow | Arquivo criado fica no Drive do usuário; permissões corretas | Requer redirect OAuth; mais complexo de implementar | Criação de apresentações no Drive do usuário |
| **Híbrido (recomendado)** | Service account para leitura de assets; OAuth por usuário para criação | Melhor dos dois mundos | Mais setup inicial | **Produção corporativa** |

### Configuração service account (leitura de assets)

```bash
# No Google Cloud Console:
# 1. IAM > Service Accounts > Create
# 2. Baixar key.json
# 3. No Google Drive: Compartilhar a pasta /brand-assets com o e-mail da service account (leitor)

# Configuração no servidor MCP:
export GOOGLE_SERVICE_ACCOUNT_KEY=/etc/mcp/service-account.json
export BRAND_ASSETS_FOLDER_ID=<ID da pasta no Drive>
```

## Testando a integração

Checklist antes de produção:

```bash
# 1. Testar autenticação
claude mcp test google-drive-full

# 2. Listar templates disponíveis
# (via Claude Code)
> liste os templates disponíveis na pasta de brand assets

# 3. Criar apresentação de teste
> crie uma apresentação de teste com o template corporativo, título "Teste MCP"

# 4. Verificar que o link foi gerado e o arquivo aparece no Drive
> mostre o link do deck que você criou

# 5. Testar preenchimento de placeholder
> preencha o template com título "Proposta Teste" e autor "Ana Silva"
```

## Limitações conhecidas

| Limitação | Impacto | Mitigação |
|---|---|---|
| Slides API não cria apresentações com conteúdo em 1 step | Fluxo mais verboso | Usar `drive.copy_file` + `batch_update` (documentado acima) |
| Imagens externas: Slides API exige URL pública para `createImage` | Logos internos precisam de URL temporária | Gerar signed URL temporária via Drive API para arquivos de logo |
| Fontes customizadas: Google Slides suporta apenas fontes do Google Fonts por API | Fontes proprietárias não ficam disponíveis via API | Usar fontes do Google Fonts equivalentes; fontes customizadas somente via editor manual |
| Rate limits: 300 requests/min por projeto Google Cloud | Geração em lote pode ser throttled | Implementar exponential backoff; usar batchUpdate para agrupar requests |
| Export .pptx: disponível via Drive API (`files.export`) | O export nem sempre preserva layouts complexos | Testar templates específicos; usar python-pptx para geração .pptx se fidelidade for crítica |

## Referências

- Google Workspace MCP (oficial): <https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services>
- google-slides-mcp (community): <https://github.com/matteoantoci/google-slides-mcp>
- google-drive-mcp (community): <https://github.com/piotr-agier/google-drive-mcp>
- Google Slides API Reference — presentations.batchUpdate: <https://developers.google.com/slides/api/reference/rest/v1/presentations/batchUpdate>
- Google Slides API — Request types completo: <https://developers.google.com/slides/api/reference/rest/v1/presentations/batchUpdate#Request>
- Drive API — files.copy: <https://developers.google.com/drive/api/reference/rest/v3/files/copy>
- Composio — Google Slides MCP com Claude Code: <https://composio.dev/toolkits/googleslides/framework/claude-code>
