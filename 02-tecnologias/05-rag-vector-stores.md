# RAG e Vector Stores (2026)

> Foco em ACL (controle de acesso por documento/chunk), busca híbrida (BM25 + dense + reranker) e multi-tenancy. OWASP LLM 2025 elevou "**LLM08: Vector & Embedding Weaknesses**" a item Top 10 — retrieval seguro deixou de ser opcional.

## Princípios de RAG corporativo (2026)

1. **Hybrid search é padrão**: BM25 (sparse) + dense (HNSW/IVF) + reranker. Pure dense perdeu para hybrid em quase todos os benchmarks empresariais.
2. **ACL no retrieval**: filtrar **antes** do top-k, não depois. Filtros pré-query (per-document permissions) precisam ser nativos.
3. **Multi-tenancy**: isolar por collection/namespace; per-tenant payload encryption se PII pesado.
4. **Multi-vector / late interaction**: ColBERT-style (e.g., BGE-M3 multi-vector) ganha em recall em alguns casos; vetor único + reranker é caminho mais simples.
5. **Reranker é quase sempre vantagem**: BGE-reranker / Qwen3-Reranker custa pouco para top-k=20 e melhora muito.

## Tabela comparativa

| Vector store | Linguagem | ACL nativa | Hybrid (BM25+dense) | Multi-tenancy | Escala observada | Operação | Licença |
|--------------|-----------|------------|----------------------|---------------|--------------------|----------|---------|
| **Qdrant** | Rust | Filtros payload + JWT/role-based | Sim (sparse + dense, late interaction) | Sim (collections + payload partitions) | 10⁹ vetores em cluster | Single binary, Docker, K8s; simples | Apache 2.0 |
| **Milvus / Zilliz** | C++/Go | Sim (RBAC nativo desde 2.4+, partition-key) | Sim (BM25 nativo desde 2.5) | Sim (databases + collections + partitions) | 10⁹+ (escolha de big shops) | Mais complexo (etcd, MinIO, Pulsar/Kafka) | Apache 2.0 |
| **Weaviate** | Go | Sim (RBAC desde 1.29 GA; multi-tenancy é cidadão de primeira classe) | Sim (BM25 + vector) | Sim (tenants nativos) | 10⁸+ | Single node simples; cluster requer cuidado | BSD-3 |
| **pgvector + pgvectorscale** | C (Postgres ext) | Herda Postgres (RLS, GRANTs) | Sim (com `pg_trgm` ou `paradedb`/`pg_search`) | Schemas/RLS | ~10⁷–10⁸ realista (pgvectorscale ~10× mais que pgvector puro) | Quem já roda Postgres não tem novo sistema | PostgreSQL License + Apache 2.0 (scale) |
| **Elasticsearch / OpenSearch** | Java | RBAC + DLS (document-level security) | **Forte** (BM25 nativo + kNN HNSW) | Index/role-based | 10⁹+ | DBA dedicado | Elastic License v2 / Apache 2.0 (OpenSearch) |
| **Chroma** | Python/Rust | Limitada | Limitada | Limitada | <10⁶ | Excelente para POC | Apache 2.0 |
| **Marqo** | Python | Parcial | Sim | Sim | 10⁷+ | Foco em multi-modal | Apache 2.0 |
| **LanceDB** | Rust | Limitada (filtros) | Sim (com tantivy) | Limitada | 10⁸ | Embedded, single-node | Apache 2.0 |
| **Vespa** (Yahoo) | Java/C++ | RBAC | Sim (forte) | Sim | 10¹⁰ | Curva de aprendizado alta | Apache 2.0 |
| **pgvector + ParadeDB** | C/Rust | Postgres-native | BM25 nativo (Tantivy embedded) | Schemas/RLS | 10⁸ | Postgres como única DB | AGPL/Apache 2.0 |

## Detalhamento

### Qdrant
- **Por que escolhem**: Rust, single binary, **payload filters + ACL via JWT**, hybrid (sparse + dense + multi-vector ColBERT), gRPC nativo. **Líder em "operacionalmente simples + features modernas"**.
- **Multi-tenancy**: collections + payload `tenant_id` filtrado pré-query.
- **Quando usar**: greenfield self-hosted; equipes pequenas/médias; cargas até bilhões.
- **Quando NÃO**: empresa que já roda Postgres pesado e não quer +1 sistema; ou quem precisa de federation/multi-region complexa.
- **Links**: <https://github.com/qdrant/qdrant> · <https://qdrant.tech/>

### Milvus / Zilliz
- **Por que escolhem**: escala de bilhões, distributed, GPU-accelerated search (Zilliz Cloud), **partition keys** para multi-tenancy, **BM25 nativo (2.5+)**, RBAC.
- **Quando usar**: cargas >10⁸ vetores, requisitos de throughput pesado, GPU search.
- **Quando NÃO**: time pequeno (etcd + MinIO + Pulsar/Kafka é overhead operacional sério).
- **Performance**: a 50M vetores, **41 QPS @ 99% recall** vs **471 QPS do pgvectorscale** (caso particular onde Postgres-otimizado vence em recall fixo).
- **Links**: <https://github.com/milvus-io/milvus> · <https://milvus.io/>

### Weaviate
- **Por que escolhem**: **multi-tenancy first-class** (tenants nativos, isolamento físico opcional), módulos de embedding embutidos, hybrid, RBAC GA (1.29).
- **Quando usar**: SaaS multi-tenant; quem quer "vetor + grafo".
- **Quando NÃO**: latência crítica em single-tenant grande (Qdrant é mais rápido em alguns benchmarks single-tenant).
- **Links**: <https://github.com/weaviate/weaviate> · <https://weaviate.io/>

### pgvector + pgvectorscale + ParadeDB / pg_search
- **Por que escolhem**: **DBA já existe**, transações ACID, joins com dados relacionais, RLS herdada para ACL.
- **pgvector** sozinho: até ~10M vetores razoável.
- **pgvectorscale** (Timescale): adiciona índice DiskANN-like — escala para 100M+, ~10× pgvector em benchmarks publicados.
- **ParadeDB / pg_search**: BM25 via Tantivy embarcado em Postgres — habilita hybrid search dentro do Postgres.
- **Quando usar**: stack Postgres dominante, dados relacionais críticos para o RAG.
- **Quando NÃO**: cargas multi-bilhão, latência sub-10ms a alta concorrência.
- **Links**: <https://github.com/pgvector/pgvector> · <https://github.com/timescale/pgvectorscale> · <https://github.com/paradedb/paradedb>

### Elasticsearch / OpenSearch
- **Por que escolhem**: time já opera ELK; **DLS (Document-Level Security)** maduro para ACL; BM25 industrial; HNSW desde 8.0 (Elastic) / 2.x (OpenSearch).
- **Quando usar**: ACL fina existente em Elastic; logs + RAG no mesmo cluster.
- **Quando NÃO**: greenfield onde DBA Postgres já existe; latência sub-10ms em vetores massivos (HNSW lá não bate Qdrant/Milvus).
- **Links**: <https://www.elastic.co/elasticsearch/vector-database> · <https://opensearch.org/platform/search/vector-database.html>

### Chroma
- **Por que escolhem**: setup em 1 linha (`pip install chromadb`), API Pythonic.
- **Quando usar**: POC, dev local, projetos pequenos.
- **Quando NÃO**: produção corporativa séria.
- **Links**: <https://github.com/chroma-core/chroma>

### Marqo
- **Por que escolhem**: **multimodal nativo** (texto + imagem) sem pipeline manual; tensor-based search.
- **Links**: <https://github.com/marqo-ai/marqo>

### LanceDB
- **Por que escolhem**: embedded (sem servidor), formato Lance (eficiente em S3/object storage), SQL.
- **Quando usar**: app desktop, edge, batch analytics.
- **Links**: <https://github.com/lancedb/lancedb>

### Vespa
- **Por que escolhem**: extremo em escala (Yahoo Search). Hybrid, ranking learnable.
- **Quando usar**: cargas 10⁹+ com requisitos de ranking complexo.
- **Quando NÃO**: time pequeno (curva de aprendizado alta).
- **Links**: <https://vespa.ai/>

## Modelos de embedding e reranker para RAG empresarial

| Camada | Open source recomendado (2026) | Notas |
|--------|--------------------------------|-------|
| Dense embedding (multilíngue, PT-BR) | **BGE-M3**, **Qwen3-Embedding-8B**, **Granite-Embedding multilingual** | Granite tem ISO 42001 |
| Sparse / BM25 | nativo do vector store; alternativamente BGE-M3 produz sparse | hybrid > pure dense |
| Reranker | **BGE-reranker-v2 (m3 ou gemma)**, **Qwen3-Reranker-4B/8B**, **Jina Reranker v2** | Aplicar em top-k=20-50 |
| Multi-modal embedding | **Qwen3-VL-Embedding**, **Marqo embedding**, **NV-Embed-VL** | Para RAG sobre imagens |

## Padrão de pipeline RAG enterprise (2026)

```
Documento (PDF, DOCX, HTML)
   |
   v
Parser (Unstructured, Docling, LlamaParse, Marker, Azure Document Intelligence)
   |
   v
Chunking (semantic, layout-aware, recursive)
   |
   v
Embedding (BGE-M3 / Qwen3-Embedding) + sparse (BM25 / SPLADE)
   |
   v
Vector store (Qdrant/Milvus/...) com payload de ACL (tenant_id, classification, source)
   |
   v
Query: embedding + filtros ACL pré-query  -->  top-50 hybrid
   |
   v
Reranker (BGE / Qwen3-Reranker)            -->  top-5
   |
   v
LLM (vLLM/SGLang) com prompt + citações
```

## Mapeamento OWASP LLM08 (Vector & Embedding Weaknesses) → controles

| Risco | Controle |
|-------|----------|
| Acesso indevido a chunks | ACL pré-query no vector store; filter-then-search; per-tenant collections |
| Embedding inversion | Não armazenar PII em texto plano no payload; redação via Presidio antes de embedar |
| Poisoning de índice | Pipeline de ingestão com revisão; assinatura de fonte; quarentena de fontes não confiáveis |
| Vazamento entre tenants | Multi-tenancy nativo (Weaviate tenants, Qdrant collections, Postgres RLS) |
| Reranker disclosure | Reranker hospedado on-prem (não usar Cohere Rerank API se data residency importa) |

## Fontes

- Encore vector DB 2026: <https://encore.dev/articles/best-vector-databases>
- Vector DB benchmarks 2026 (CallSphere): <https://callsphere.ai/blog/vector-database-benchmarks-2026-pgvector-qdrant-weaviate-milvus-lancedb>
- Firecrawl best vector DBs 2026: <https://www.firecrawl.dev/blog/best-vector-databases>
- pgvectorscale: <https://github.com/timescale/pgvectorscale>
- ParadeDB pg_search: <https://github.com/paradedb/paradedb>
- Weaviate multi-tenancy: <https://docs.weaviate.io/weaviate/concepts/data#multi-tenancy>
- Qdrant ACL/JWT: <https://qdrant.tech/documentation/guides/security/>
- Milvus partition key multi-tenancy: <https://milvus.io/docs/multi_tenancy.md>
- OWASP GenAI LLM Top 10 2025 (LLM08): <https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/>
