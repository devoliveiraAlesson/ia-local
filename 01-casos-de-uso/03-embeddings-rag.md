# Caso 3 — Servidor de Embeddings + RAG Corporativo (Plataforma Habilitadora)

> Este é o caso de **maior alavancagem**: ele habilita os Casos 2, 6, 7, 8, 11 e 12. Deve ser tratado como plataforma compartilhada, não como projeto isolado.

## Descrição

Construir uma **plataforma de Retrieval-Augmented Generation** corporativa que permite a qualquer aplicação interna fazer perguntas em linguagem natural sobre documentos da empresa e receber respostas com citação de fonte. Componentes:

- **Conectores de ingestão**: SharePoint, Confluence, Drive, e-mail, file-shares, repositórios Git, Salesforce, Jira, ServiceNow, banco de dados, ERP.
- **Pipeline de processamento**: parser (incluindo PDFs com OCR, tabelas, imagens), chunking semântico, geração de embeddings, indexação vetorial, indexação léxica (BM25) e indexação por metadados (ACL, departamento, data, classificação).
- **Servidor de embeddings dedicado**: API interna de embedding sob alta concorrência, com cache.
- **Camada de retrieval híbrido**: BM25 + vetor + filtro por ACL, seguido de reranker.
- **API de RAG**: endpoint OpenAI-compatible que aplicações consomem (`/v1/chat/completions` com `tools=retrieve`).

## Por que precisa ser LOCAL

- Os documentos cobrem **toda a área cinzenta de dados sensíveis**: contratos, atas, propostas, prontuários, pareceres, planilhas financeiras, segredo comercial, propriedade intelectual.
- Embeddings **vazam informação**: a OWASP catalogou em 2025 "Vector & Embedding Weaknesses" como LLM08, top-10 risk. Embeddings podem ser invertidos para reconstruir trechos sensíveis.
- Regulamentações de **soberania de dados** (LGPD, GDPR, requisitos do Bacen 4.893/8.681) exigem que os dados não cruzem jurisdição mesmo na fase de embedding.
- ACL: filtros de permissionamento têm que ser **mandatory at retrieval time**, jamais delegados ao LLM (risco de vazamento entre departamentos).

## Modelo recomendado

- **Embeddings (multilíngues, PT-BR forte)**: BGE-M3 (Beijing AI Academy) — denso + esparso + multi-vetor, 8k tokens de contexto; Nomic Embed v2 (Apache 2.0, 768 dim); Jina Embeddings v3 (multilíngue); E5-Mistral-7B (qualidade top, mais caro).
- **Reranker**: BGE-Reranker v2-m3, Jina Reranker v2 (cross-encoder pequeno, alta qualidade).
- **LLM gerador (via API interna)**: Llama 3.3 70B, Llama 4 Scout (MoE com contexto longo, ideal para RAG), Qwen 2.5 32B/72B, Mistral Large 2.
- **Modelos especializados**: IBM Granite-Embedding e Granite-Reasoning (ISO/IEC 42001 certified, bom em RAG enterprise).

## Stack típica

- **Vector store**:
  - **Qdrant** (Rust, performático, filtros ricos, hybrid search nativo) — recomendação default.
  - **Milvus** (escala alta, GPU optional, multi-tenant maduro).
  - **Weaviate** (módulos RAG embutidos).
  - **pgvector / Postgres** (se a base for ≤ 10M chunks e equipe já é Postgres-first).
- **Servidor de embeddings**: HuggingFace TEI (text-embeddings-inference) ou Infinity — alto throughput, gRPC, batching.
- **Orquestração**: LlamaIndex (mais opinionado, melhor DX para RAG), Haystack 2.x (modular, OTel-native), LangChain (mais flexível, mais pegadinhas).
- **Parsing de documentos**: Docling (IBM, open source, ótimo em PDF/tabelas), MinerU (PDF→Markdown/JSON), Unstructured.io self-hosted, LlamaParse (se aceitar SaaS).
- **Observabilidade**: Langfuse + Ragas (faithfulness, context precision/recall, answer relevancy).
- **Plataforma "tudo-em-um" (alternativa)**: Red Hat OpenShift AI (RAG reference architecture com Granite + Milvus), NVIDIA NIM/NeMo Retriever, Verba (Weaviate).

## Métricas de sucesso / KPIs

- **Cobertura**: % das perguntas internas que encontram resposta com citação no top-5.
- **Faithfulness**: % de respostas sustentadas pelo contexto recuperado (Ragas, meta > 90%).
- **Context precision / recall**: qualidade do retrieval em si (BEIR-like, mas com gold set interno).
- **Latência E2E**: P50 < 2s, P95 < 5s.
- **Frescor**: lag entre publicação de documento e disponibilidade no índice (meta < 1h).
- **ACL hit rate**: % de queries em que o ACL filtrou ao menos um chunk (sinal de que o filtro está vivo).
- **Adoção**: número de aplicações internas consumindo a API.

## Estimativa de retorno

**Muito alta** — porque é multiplicadora. Cada aplicação que sobe em cima do RAG (suporte, jurídico, RH, compliance, vendas) reaproveita ingestão, embeddings, ACL e governança, reduzindo cost-to-build de cada caso novo em 60–80%.

## Maturidade

**Produção média.** Pipeline básico em 6–10 semanas. Pipeline corporativo (com ACL, frescor, multi-tenant, eval contínua, governança de fonte) em 4–6 meses. A complexidade vem da ingestão (parsing de PDFs ruins, formatos exóticos, deduplicação, segurança).

## Riscos e mitigação

- **ACL bypass via embedding**: filtro obrigatório no retrieval com payload por documento, nunca confiar só em prompt.
- **Embedding inversion attack**: limitar acesso direto ao índice; nunca expor o vector store sem auth.
- **Drift de fontes**: pipeline de reindex programado + detecção de stale chunks.
- **Documentos com classificação misturada**: enriquecer cada chunk com tag de classificação (público/interno/confidencial/restrito) e filtrar no retrieval.
- **Custo de embeddings em larga escala**: cache + estratégia incremental (só re-embedar o que mudou).

## Fontes consultadas

- NStarX — RAG enterprise 2026-2030: <https://nstarxinc.com/blog/the-next-frontier-of-rag-how-enterprise-knowledge-systems-will-evolve-2026-2030/>
- Data Nucleus — RAG enterprise guide 2025: <https://datanucleus.dev/rag-and-agentic-ai/what-is-rag-enterprise-guide-2025>
- Squirro — State of RAG 2026: <https://squirro.com/squirro-blog/state-of-rag-genai>
- MinIO — RAG in enterprise: <https://www.min.io/learn/retrieval-augmented-generation>
- Markets&Markets — RAG market 2025-2030: <https://www.marketsandmarkets.com/Market-Reports/retrieval-augmented-generation-rag-market-135976317.html>
- Glean — RAG models 2025: <https://www.glean.com/blog/rag-models-enterprise-ai>
- IBM Granite 3.0 announcement: <https://www.ibm.com/new/announcements/ibm-granite-3-0-open-state-of-the-art-enterprise-models>
