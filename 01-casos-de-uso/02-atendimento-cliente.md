# Caso 2 — Assistente de Atendimento ao Cliente (Bot com Base de Conhecimento)

## Descrição

Bot conversacional para suporte ao cliente, alimentado por RAG sobre a base de conhecimento da empresa (FAQs, manuais, políticas, contratos, base de tickets resolvidos, base de produtos). Pode ser usado em dois modos:

1. **Co-piloto do agente humano**: agente continua falando com o cliente; o LLM sugere a resposta e cita as fontes internas. Reduz o tempo médio de atendimento (TMA) e aumenta a aderência a roteiros.
2. **Self-service direto** (chat público ou app), com escalonamento para humano em casos complexos, alta sensibilidade ou baixa confiança da resposta.

A versão híbrida (1+2) é a mais comum em produção: bot resolve casos repetitivos e classifica os complexos para o agente certo.

## Por que precisa ser LOCAL

- Histórico de conversas com clientes contém: dados pessoais (LGPD), dados financeiros, números de cartão, informações médicas (saúde) e dados de identificação.
- Em setores regulados (Bacen, ANS, ANPD), o tratamento desses dados em provedor estrangeiro exige acordo de operador, transferência internacional aprovada e DPIA detalhada.
- Sigilo bancário (LC 105) e bancário/saúde restringem severamente o envio de dados a APIs externas.
- A base de conhecimento ela mesma costuma ser ativo competitivo (procedimentos internos, scripts, regras de negócio).

## Modelo recomendado

- **LLM gerador**: Llama 3.3 70B (qualidade) ou Mistral Small 3 / Qwen 2.5 14–32B (melhor custo/latência por agente concorrente).
- **Modelo de embeddings (PT-BR)**: BGE-M3 (multilíngue, esparso+denso), Nomic Embed v2, ou E5-Mistral. Crucial para qualidade do RAG em português.
- **Reranker**: BGE-Reranker v2-m3 ou Cohere Rerank 3 (se aceitar API) sobre top-50 → top-5.
- **Modelo classificador (intenção, sentimento, sensibilidade)**: IBM Granite 3 8B ou DistilBERT fine-tuned.

## Stack típica

- **Vector store**: Qdrant ou Milvus (on-prem, multi-tenant, filtering rico). Alternativa: pgvector se a base for pequena (<10M chunks).
- **Orquestração**: LlamaIndex ou Haystack (mais maduros para suporte) — encadeia ingestão, embedding, retrieval, rerank, geração.
- **Runtime**: vLLM para o LLM gerador; modelo de embedding e reranker em servidor dedicado (text-embeddings-inference da HuggingFace ou Infinity).
- **Telemetria**: Langfuse para tracing, avaliação automática (faithfulness, answer relevancy via Ragas) e A/B test de prompts.
- **Integração**: webhook no help-desk (Zendesk, Freshdesk, ServiceNow, Salesforce) ou no chat (front próprio, WhatsApp Business via integrador on-prem).
- **Guardrails**: filtro de PII, lista de tópicos proibidos, fallback para humano com baixa confiança.

## Métricas de sucesso / KPIs

- **Deflection rate**: % de tickets resolvidos sem agente humano (meta inicial: 25–40%).
- **Tempo médio de atendimento (TMA)**: redução de 20–35% no modo co-pilot (benchmark setor financeiro/telecom).
- **First Contact Resolution (FCR)**: aumento de 5–15 pp.
- **CSAT/NPS**: manter ou subir; degradação é red flag.
- **Faithfulness/Groundedness**: % de respostas sustentadas por trechos recuperados (medido com Ragas/TruLens). Meta > 90%.
- **Custo por interação**: vs. atendimento humano (R$ 4–12 humano vs. R$ 0,02–0,30 IA local com infra amortizada).
- **Taxa de escalonamento adequado**: bot reconhece quando deve passar para humano.

## Estimativa de retorno

**Alta.** Casos públicos (Klarna, Bradesco, Itaú, Vivo) reportam economias de dezenas de milhões de reais/ano em centros de atendimento, com TMA caindo 20–40% e deflection chegando a 50–70% para casos repetitivos. A versão local é mais cara em capex inicial, mas mantém compliance — em muitos setores é a única opção viável.

## Maturidade

**Produção média a complexa.** RAG funcional em 4–8 semanas; produção robusta com governança de respostas, guardrails, escalonamento e A/B testing leva 4–6 meses. A qualidade depende fortemente da curadoria da base de conhecimento — um RAG bom requer investimento em ingestão, chunking, metadados e avaliação contínua.

## Riscos e mitigação

- Resposta errada com aparência de certeza: sempre citar fonte, abstain quando confiança baixa, threshold de score do retrieval.
- Vazamento entre tenants/clientes: filtros mandatórios por client_id no retrieval.
- Drift de base: pipeline de reindex contínuo + monitoramento de qualidade.

## Fontes consultadas

- Mercity — Enterprise Customer Support Chatbot guide: <https://www.mercity.ai/blog-post/guide-to-building-an-enterprise-grade-customer-support-chatbot-using-llms>
- Heltar — Best LLMs for support 2025: <https://www.heltar.com/blogs/best-llm-models-for-customer-support-chatbot>
- Glean — RAG models for enterprise AI 2025: <https://www.glean.com/blog/rag-models-enterprise-ai>
- Data Nucleus — RAG enterprise guide 2025: <https://datanucleus.dev/rag-and-agentic-ai/what-is-rag-enterprise-guide-2025>
- DEV.to — Top 10 open-source RAG frameworks: <https://dev.to/rohan_sharma/top-10-open-source-rag-frameworks-you-need-3fhe>
- Newline — Top 10 enterprise RAG use cases: <https://www.newline.co/@Dipen/top-10-enterprise-ai-use-cases-with-rag-and-knowledge-graphs--1cd5f397>
