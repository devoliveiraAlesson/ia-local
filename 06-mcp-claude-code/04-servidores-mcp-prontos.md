# Servidores MCP prontos — catálogo curado para uso corporativo

> Mapeamento de servidores MCP open source / comerciais relevantes para empresa com dados sensíveis. Estado em maio/2026; revalidar release/licença antes de produção. Marcado com ⚠️ os que pedem cuidado extra (licença, telemetria, maturidade).

## Como ler esta tabela

- **Self-host**: roda dentro do perímetro (sem callback externo).
- **Auth**: `none` = OK só em stdio local; `oauth` = pronto para HTTP corporativo; `apikey` = aceitável atrás de gateway.
- **Maturidade**: ⭐ POC | ⭐⭐ uso interno | ⭐⭐⭐ produção observada em outras empresas.

## Categoria 1 — RAG / busca semântica local

| Servidor | Stack | Self-host | Auth | Maturidade | Quando usar |
|----------|-------|-----------|------|------------|--------------|
| **mcp-local-rag** ([shinpr](https://github.com/shinpr/mcp-local-rag)) | Node + embeddings locais + reranker | Sim | none (stdio) | ⭐⭐ | Dev individual; bootstrap de RAG em projeto pequeno |
| **knowledge-rag** ([patakuti](https://lobehub.com/mcp/patakuti-local-knowledge-rag-mcp)) | Hybrid (BM25 + dense + cross-encoder rerank), 20+ formatos | Sim | none | ⭐⭐ | POC rápida; upgrade trivial via npx |
| **claude-rag-mcp** ([VXConsulting](https://github.com/VXConsulting/claude-rag-mcp)) | RAG + captura de falhas para Claude Code | Sim | none | ⭐⭐ | Times pequenos; integração com workflow de erro |
| **mcp-rag-server** ([0xrdan](https://github.com/0xrdan/mcp-rag-server)) | RAG genérico para Claude Code | Sim | none | ⭐ | Referência para fork interno |
| **claude-code-helper / RAG-MCP-GUIDE** ([michelabboud](https://github.com/michelabboud/claude-code-helper)) | Redis + all-MiniLM-L6-v2 | Sim | none | ⭐ | Tutorial; útil como referência arquitetural |

⚠️ Nenhum dos servidores acima tem ACL multi-tenant nativo de nível corporativo. Para empresa com requisitos LGPD/HIPAA/Bacen, **fork e adapter próprio** (ver [`05-construir-mcp-interno.md`](./05-construir-mcp-interno.md)) é o caminho. Os servidores prontos servem como referência ou para devs individuais.

## Categoria 2 — Vector stores expostos diretamente como MCP

| Vector store | Servidor MCP oficial | Notas |
|--------------|----------------------|-------|
| **Qdrant** | [`mcp-server-qdrant`](https://github.com/qdrant/mcp-server-qdrant) (Rust, oficial) | Tools `find` / `store`. Bom como bloco de construção; complementar com adapter para ACL. |
| **Milvus / Zilliz** | [`mcp-server-milvus`](https://github.com/zilliztech/mcp-server-milvus) | Schema-aware; expõe collections como tools. |
| **Weaviate** | [`mcp-server-weaviate`](https://github.com/weaviate/mcp-server-weaviate) | Multi-tenant nativo; integra com RBAC do Weaviate. |
| **pgvector / Postgres** | [`@modelcontextprotocol/server-postgres`](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) (oficial) | Tools genéricas SQL; combinar com pgvector para RAG. |
| **Elasticsearch** | [`elasticsearch-mcp`](https://github.com/elastic/mcp-server-elasticsearch) | Hybrid search já maduro; aproveitar deploys existentes. |

**Decisão**: expor o vector store *direto* via MCP é simples mas perde reranker, ACL fina e auditoria. Em produção, prefira **adapter MCP próprio** que use o vector store como backend.

## Categoria 3 — Knowledge graph

| Servidor | Stack | Notas |
|----------|-------|-------|
| **mcp-neo4j-graphrag** ([neo4j-field](https://github.com/neo4j-field/mcp-neo4j-graphrag)) | Vector + fulltext + Cypher unificados | Recomendação default para Graph RAG corporativo |
| **mcp-neo4j** ([neo4j-contrib](https://github.com/neo4j-contrib/mcp-neo4j)) | Tools básicas: schema, cypher, modelagem | Neo4j Labs; mais flexível, menos opinionado |
| **graphify** ([safishamsi](https://github.com/safishamsi/graphify)) | Skill de Claude Code que indexa folders como grafo | Útil para code intelligence / linhagem |

## Categoria 4 — Plataforma de desenvolvimento (essenciais)

Servidores que todo dev com Claude Code ganha em consumir, independentemente do RAG corporativo:

| Servidor | Função | Auth | Notas |
|----------|--------|------|-------|
| **github** (oficial) | Issues, PRs, code search, CI status | OAuth / PAT | GitHub Enterprise on-prem suportado |
| **gitlab** (oficial / comunidade) | Equivalente para GitLab self-hosted | Token | Gateway recomendado |
| **filesystem** (oficial) | Leitura/escrita controlada de arquivos | none (stdio) | Default no Claude Code; cuidado com paths |
| **postgres** (oficial) | Read-only SQL contra DW interno | URL com credentials | Apontar para réplica, nunca primary |
| **slack** (oficial) | Buscar mensagens, contexto de canais | OAuth | Útil para "como decidimos X?" |
| **jira / confluence** (Atlassian / comunidade) | Issues, ADRs, runbooks | OAuth | Substituível por adapter sobre RAG |
| **sentry / datadog / opentelemetry** | Logs, traces, alertas | apikey | Triagem de incidentes |
| **kubernetes** ([mcp-k8s](https://github.com/strowk/mcp-k8s-go)) | kubectl-equivalent read-only | kubeconfig | Cuidado com escrita |
| **playwright / puppeteer** (oficial Anthropic) | Navegação web autenticada controlada | none | Só dentro de perímetro; útil para testes |

## Categoria 5 — Linguagem natural sobre dados estruturados

| Servidor | Função |
|----------|--------|
| **dbt-mcp** ([dbt Labs](https://github.com/dbt-labs/dbt-mcp)) | Lista models, executa, lê manifest |
| **bigquery / snowflake / databricks-mcp** | SQL governado, leitura de catalog |
| **trino-mcp** | Query federada sobre data lake |
| **lake-fs / unity-catalog-mcp** | Lineage e versionamento |

## Critérios de aceitação para colocar um servidor MCP em escopo `user` ou `project`

Checklist antes de promover servidor da experimentação para produção:

- [ ] Licença aceita pela política da empresa (atenção a AGPL, BSL, ELv2).
- [ ] Repositório com manutenção ativa (commits últimos 90 dias) **OU** vendor com SLA contratual.
- [ ] Sem telemetria por default; ou com flag confiável para desligar.
- [ ] Auth OAuth 2.1 (HTTP) **ou** rodando localmente em stdio (sem rede).
- [ ] Tools com input schema validável; sem surpresas (ex.: tool "auxiliar" que executa shell).
- [ ] Pode ser apontado para endpoint interno (não força SaaS).
- [ ] Inspecionado com **MCP Inspector** — descrições de tools revisadas.
- [ ] Empacotado / pinned: comando `npx -y x@latest` proibido em produção. Pin de versão obrigatório.
- [ ] Revisão SAST do código se for self-built (especialmente se tool executa código/SQL/cypher).
- [ ] Imagem container assinada e armazenada em registry interno; não puxar do npm/pip público em runtime.
- [ ] Documentação interna com runbook (start/stop, métricas, alarmes).

## Anti-padrões observados

- **"Rodar tudo via npx"**: agradável em demo; péssimo em prod (quebra air-gap, sem SBOM, sem reprodutibilidade).
- **Servidor MCP de terceiro com escopo `user` global** sem revisão: o servidor roda com a identidade do dev e pode ler tudo que o dev consegue ler.
- **Wrappers MCP que apenas re-exportam APIs SaaS sem rate-limit / audit**: viram um buraco de FinOps e de DLP.
- **Tools com nome ambíguo** (`run`, `execute`, `do`): modelo confunde; auditoria fica ilegível. Nomes verbosos vencem (`github.create_issue`, `rag.search_corporativo`).

## Como o catálogo evolui

Recomendação: criar um **MCP registry interno** simples (página em Confluence / repo em git) listando, por servidor: licença, scope, owner interno, versão pinada, contato em caso de incidente. Atualizado pelo time de plataforma trimestralmente. Spec MCP a partir de 2025 prevê discovery via "registry servers" — adoção ainda baixa em maio/2026, mas vale acompanhar.

## Referências

- MCP servers oficiais: <https://github.com/modelcontextprotocol/servers>
- Awesome MCP Servers: <https://mcpservers.org/>
- Glama (catálogo curado): <https://glama.ai/mcp/servers>
- LobeHub MCP catalog: <https://lobehub.com/mcp>
- Toolradar — Best MCP Servers for Claude Code 2026: <https://toolradar.com/blog/best-mcp-servers-claude-code>
