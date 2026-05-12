# Frontends: Chat Interno e Coding Assistants (2026)

> Camada de UX. Em 2026 o mercado de "ChatGPT corporativo self-hosted" amadureceu — Open WebUI, LibreChat e AnythingLLM cobrem 80% dos casos de chat. Para IDE, **Continue.dev** (chat) e **Tabby** (autocomplete) são as escolhas dominantes; **Cline** e **Roo Code** lideram em agentes que mexem no código.

## A. Frontends de chat corporativo

### Tabela-resumo

| Frontend | SSO | RBAC | RAG | Multi-modelo | Linguagem | Licença | Stars |
|----------|-----|------|-----|--------------|-----------|---------|-------|
| **Open WebUI** (ex Ollama WebUI) | OIDC, SAML | Sim | Sim (built-in) | Sim (qualquer OpenAI-compat) | Python (Svelte) | BSD-3 (com cláusula de marca) | 100k+ |
| **LibreChat** | OIDC, LDAP, OAuth | Sim | Sim (RAG API + Meilisearch) | Sim | Node.js | MIT | 25k+ |
| **AnythingLLM** | sim (workspace-level) | parcial | **RAG por workspace** | sim | Node.js | MIT | 35k+ |
| **Big-AGI** | parcial | parcial | parcial | Sim | Next.js | MIT | 6k+ |
| **LobeChat** | OIDC | parcial | sim | Sim | Next.js | MIT | 50k+ |
| **Chatbot UI** | parcial | não | parcial | Sim | Next.js | MIT | 30k+ |
| **BionicGPT** | OIDC, SAML | Sim | Sim | Sim | Rust | Apache 2.0 | 2k+ |
| **HuggingChat / chat-ui** | sim | parcial | sim (assistants) | Sim | Svelte | Apache 2.0 | 9k+ |
| **Hoppscotch AI** | (parte de Hoppscotch) | parcial | parcial | Sim | TS | MIT | (parte) |

### Detalhamento

#### Open WebUI
- **O que é**: descende do Ollama WebUI; virou plataforma full chat self-hosted. Suporta **RAG embutido** (upload PDF/MD/TXT, embedding configurável), **Pipelines** (plugins Python para guardrails/transformações), **OIDC SSO**, **RBAC**, audit logs.
- **Quando usar**: substituto privado do ChatGPT em organização média/grande com SSO; deploy rápido com Helm chart.
- **Quando NÃO**: customização visual profunda exigida (substituir branding completo), workspace isolation extremo entre departamentos.
- **Licença**: BSD-3 modificada (mar/2025 — adicionou cláusula de "branding preservation": precisa preservar branding em deploys >50 usuários ou comprar licença enterprise). **Auditar antes de produção corporativa.**
- **Links**: <https://github.com/open-webui/open-webui> · <https://openwebui.com/>

#### LibreChat
- **O que é**: clone OSS do ChatGPT com **multi-provider** (OpenAI-compat, Anthropic, Bedrock, Azure), agents, **MCP support**, memory, RAG via serviço próprio (RAG API + Meilisearch para hybrid).
- **Quando usar**: hub multi-provider corporativo; auth corporativa com **LDAP**, OIDC, OAuth.
- **Quando NÃO**: workspace-level RAG forte (AnythingLLM é melhor).
- **Licença**: MIT.
- **Links**: <https://github.com/danny-avila/LibreChat> · <https://www.librechat.ai/>

#### AnythingLLM
- **O que é**: foco em **workspaces de documentos**. Cada workspace tem vector store próprio (LanceDB built-in ou Pinecone/Chroma/Weaviate/Qdrant/Milvus), web scraping built-in, suporte a agents, `@workspace` queries.
- **Quando usar**: cenários com isolamento por departamento/projeto e RAG no centro.
- **Quando NÃO**: chat geral sem necessidade de RAG isolado.
- **Licença**: MIT.
- **Links**: <https://github.com/Mintplex-Labs/anything-llm> · <https://anythingllm.com/>

#### Big-AGI
- **O que é**: app multi-modelo, multi-persona, com beam search visual, voice. Mais "playground avançado" que ChatGPT-clone.
- **Links**: <https://github.com/enricoros/big-AGI>

#### LobeChat
- **O que é**: front-end Next.js com **plugin store**, agents, RAG, voice, banco de dados.
- **Links**: <https://github.com/lobehub/lobe-chat>

#### BionicGPT
- **O que é**: plataforma Rust focada em **enterprise hardening** (RBAC granular, observability, K8s-native, SAML).
- **Quando usar**: empresa que prioriza segurança e compliance acima de UX rica.
- **Links**: <https://github.com/bionic-gpt/bionic-gpt>

#### HuggingChat / chat-ui
- **O que é**: front-end open source da Hugging Face, base do `huggingface.co/chat`. Suporta tools, assistants, web search.
- **Links**: <https://github.com/huggingface/chat-ui>

## B. Frontends de coding (IDE)

### Tabela-resumo

| Tool | Tipo | IDE / Forma | Self-hosted? | Licença | Stars (mai/2026) |
|------|------|-------------|--------------|---------|-------------------|
| **Continue.dev** | Chat + autocomplete + edits + agents | VS Code + JetBrains; CLI ("AI checks in CI") | Sim (BYO model server) | Apache 2.0 | 31k |
| **Tabby** | Autocomplete + chat | VS Code, JetBrains, Vim, Eclipse, Helix | **Sim, primário** (Docker single binary) | Apache 2.0 | 33k |
| **Cline** | Agente full-coding | VS Code + CLI 2.0 | Sim (BYO model) | Apache 2.0 | 58k |
| **Roo Code** (fork de Cline) | Agente full-coding com mais modos | VS Code | Sim | Apache 2.0 | 22k |
| **Aider** | CLI git-aware coding | Terminal | Sim (BYO model) | Apache 2.0 | 41k |
| **OpenHands** (ex OpenDevin) | Plataforma full agent | Browser/VS Code | Sim | MIT | 68k |
| **Goose** (Block) | CLI agent | Terminal/desktop | Sim | Apache 2.0 | 32k |
| **bolt.diy** | Web full-stack agent | Web | Sim | MIT | 19k |
| **Void Editor** | Fork de VS Code com IA built-in | App standalone | Sim | Apache 2.0 | 15k+ |

### Detalhamento

#### Continue.dev
- **O que é**: extensão VS Code/JetBrains. Conecta a qualquer endpoint OpenAI-compatible (vLLM, Ollama, etc.). Funcionalidades: **autocomplete** (FIM com Qwen-Coder, etc.), **chat lateral**, **inline edit**, **agents** com tools.
- **Pivô 2025-26**: focou também em **AI checks in CI** (CLI para code review automatizado em PRs).
- **Quando usar**: BYOM em IDE; cenário "Tabby + algo a mais (chat e edit)".
- **Links**: <https://github.com/continuedev/continue> · <https://docs.continue.dev/>

#### Tabby
- **O que é**: **substituto open source do GitHub Copilot**: single binary/Docker, painel admin com usuários, IDE plugins (VS Code, JetBrains, Vim/Neovim, Eclipse). Roda Qwen-Coder, DeepSeek-Coder, StarCoder etc.
- **Capacidade**: 1× A100 80GB com Qwen2.5-Coder 32B (4-bit) atende **15-25 devs concorrentes** com queueing.
- **Quando usar**: appliance "drop-in" replacement para Copilot self-hosted.
- **Links**: <https://github.com/TabbyML/tabby> · <https://www.tabbyml.com/>

#### Cline / Roo Code
- **O que é**: agentes full-coding em VS Code que **leem, editam, executam comandos**, com aprovação humana ou automática. **Cline 2.0 CLI** (2026) trouxe headless e parallel.
- **Quando usar**: tarefas complexas (refactor cross-file, implementação de feature inteira). Forte em modelos com reasoning (Claude Sonnet, DeepSeek R1, GPT-5).
- **Diferença**: Roo é fork com mais modos customizáveis (Architect, Code, Debug, Custom).
- **Links**: <https://github.com/cline/cline> · <https://github.com/RooCodeInc/Roo-Code>

#### Aider
- **O que é**: CLI git-aware (cada interação vira commit). Excelente em refactor de repos.
- **Links**: <https://github.com/Aider-AI/aider>

#### OpenHands (ex OpenDevin)
- **O que é**: plataforma agent autônoma (runtime sandboxed, browser, terminal); 68k stars, líder em adoção open agent platform.
- **Quando usar**: workflows autônomos de longa duração.
- **Licença**: MIT.
- **Links**: <https://github.com/All-Hands-AI/OpenHands>

#### Goose (Block / Square)
- **O que é**: agent CLI/desktop, MCP-native, da Block. Forte em integrações via MCP servers.
- **Links**: <https://github.com/block/goose>

#### Void Editor
- **O que é**: fork open source de VS Code com IA integrada nativamente (sem extensão). Compete com Cursor.
- **Links**: <https://voideditor.com/>

## Mapeamento caso de uso → frontend

| Caso de uso | Front-end candidato |
|-------------|---------------------|
| Chat interno seguro (Caso 1 do Agente 1) | Open WebUI ou LibreChat (SSO maduro) |
| RAG corporativo (Caso 3) | AnythingLLM (workspace) ou Open WebUI (knowledge collections) |
| Atendimento ao cliente | Frontend custom Next.js/React + LangGraph; LibreChat se permitir cliente externo |
| Coding assistant (Caso 4) | Tabby (autocomplete) + Continue.dev (chat IDE) |
| Code review (Caso 5) | Continue CLI em CI/CD; Cline para refactor manual |
| Agentes autônomos | OpenHands; Cline/Roo |

## Armadilhas notáveis

- **Open WebUI mudou licença em 2025** para BSD-3 modificada com cláusula de branding preservation acima de 50 usuários. Para deploys corporativos >50, a leitura literal exige preservar marca ou pegar licença enterprise — **avaliar com jurídico**.
- **Multi-tenant real é raro**: a maioria dos frontends OSS isola só por usuário, não por tenant logico (RBAC + organização). BionicGPT é exceção parcial.
- **Open WebUI Pipelines** roda código Python arbitrário no servidor — risco se admin não controlar quem cria pipelines.

## Fontes

- 11 best Open WebUI alternatives 2026: <https://blog.premai.io/11-best-open-webui-alternatives-for-enterprise-llm-chat-2026/>
- Open WebUI vs LibreChat 2026: <https://tokenmix.ai/blog/openwebui-vs-librechat-self-hosted-comparison-2026>
- Open WebUI vs AnythingLLM vs LibreChat 2026: <https://toolhalla.ai/blog/open-webui-vs-anythingllm-vs-librechat-2026>
- Best open-source AI coding tools 2026: <https://frontman.sh/blog/best-open-source-ai-coding-tools-2026/>
- Self-host AI coding assistants 2026: <https://scopir.com/posts/self-hosted-ai-coding-assistants-tabby-continue-void/>
- Tabby: <https://www.tabbyml.com/>
- Continue: <https://docs.continue.dev/>
