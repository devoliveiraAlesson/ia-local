# Resumo Executivo — Casos de Uso de IA Local (On-Premises / Nuvem Privada)

> Documento parte da Etapa 1/5 da proposta. Foco: empresa média/grande com restrições de privacidade (jurídico, saúde, financeiro, governamental).

## Por que IA local

- **44% das organizações** apontam privacidade e segurança de dados como a principal barreira para adoção de LLMs (fonte: PremAI, 2026).
- **Payback típico**: 6 a 12 meses para cargas que ultrapassam ~2 milhões de tokens/dia ou que exigem HIPAA, PCI, LGPD, GDPR.
- **Caso público de referência**: JPMorgan Chase implantou o "LLM Suite" em 2024, com mais de 230.000 funcionários ativos e mais de 600 casos de uso em produção, gerando ganhos de 30–40% em produtividade e US$ 1,5–2,0 bi/ano em valor anual estimado.
- **Hardware acessível em 2026**: deployments de porte médio começam em US$ 10–15 mil de hardware, e modelos abertos rivalizam com APIs comerciais para a maioria das tarefas corporativas.

## Tabela-Resumo de Casos de Uso

| # | Caso de Uso | Retorno Estimado | Maturidade | Prioridade Sugerida | Onde mais sensível |
|---|-------------|------------------|------------|---------------------|--------------------|
| 1 | Chat interno seguro (substituto privado do ChatGPT) | Alta (produtividade transversal) | POC fácil → Produção média | **P0 — Quick win** | E-mails, documentos colados, brainstorm |
| 2 | Assistente de atendimento ao cliente (RAG) | Alta (redução de tickets, NPS) | Produção média | **P1** | Dados de clientes, contratos, histórico |
| 3 | Servidor de embeddings + RAG corporativo | Muito Alta (alavanca para 4–8 outros casos) | Produção média | **P0 — Plataforma habilitadora** | Documentos, contratos, manuais |
| 4 | Coding assistant (Copilot local) | Alta (10–30% de produtividade dev) | POC fácil → Produção média | **P1** | Código proprietário, segredos |
| 5 | Code review automatizado | Média-Alta (qualidade + segurança) | Produção média | **P2** | Diffs, regras internas, vulnerabilidades |
| 6 | Sumarização de documentos longos | Alta (jurídico, atas, relatórios) | POC fácil | **P1** | Contratos, atas, laudos |
| 7 | Extração estruturada de dados (PDFs, formulários, e-mails) | Muito Alta (automação de back-office) | Produção média | **P1** | Faturas, prontuários, formulários |
| 8 | Tradução interna com terminologia | Média | POC fácil | **P3** | Comunicação multinacional, manuais |
| 9 | Geração de documentação técnica | Média | POC fácil | **P3** | Repositórios, APIs internas |
| 10 | Análise de logs / observabilidade assistida | Média-Alta (MTTR) | Produção complexa | **P2** | Logs com PII, telemetria sensível |
| 11 | Compliance / classificação de documentos sensíveis (PII/PHI) | Alta (mitigação de risco) | Produção média | **P1** | Toda a base não estruturada |
| 12 | Treinamento e onboarding (Q&A sobre políticas) | Média (DX + retenção) | POC fácil | **P2** | Políticas internas, RH |
| 13 | Geração / revisão de pareceres regulatórios (extra) | Alta | Produção complexa | **P2** | Jurídico/Compliance |
| 14 | Análise de e-mails (triagem, classificação) (extra) | Média | POC fácil | **P3** | Correio corporativo |

## Recomendação de Sequenciamento (12 meses)

1. **Trimestre 1**: Plataforma comum (vLLM + servidor de embeddings + Open WebUI/LibreChat) e Caso 1 (Chat interno) como quick win.
2. **Trimestre 2**: RAG corporativo (Caso 3) como plataforma e Caso 6 (Sumarização) e Caso 7 (Extração estruturada) sobre ela.
3. **Trimestre 3**: Coding assistant (Caso 4) e Code review (Caso 5) para engenharia; Caso 11 (Compliance/PII) para governança.
4. **Trimestre 4**: Atendimento ao cliente (Caso 2) com RAG e Caso 10 (Logs/observabilidade) — ambos exigem mais maturidade operacional.

## Modelos abertos de referência (2026)

- **Generalistas**: Llama 3.3 70B Instruct, Llama 4 Scout/Maverick (MoE multi-modal), Mistral Large 2, Qwen 2.5 / 3 (até 235B), DeepSeek V3 / V4 / R1, IBM Granite 3.x (8B/13B/34B).
- **Coding**: Qwen 2.5-Coder 32B, DeepSeek-Coder V2, Codestral (Mistral), Qwen3-Coder-Next 80B (3B ativos).
- **Embeddings**: BGE-M3, Nomic Embed Text V2, E5-Mistral, multilíngues recentes.
- **Reasoning**: DeepSeek-R1 (164k de contexto, custo 95% menor que o1), Qwen 3.5 reasoning.

## Stack de runtime/UI recomendado

- **Runtime de inferência**: vLLM (produção, alto throughput, PagedAttention, suporte a Llama 4 MoE) ou llama.cpp/Ollama (POCs e edge).
- **Plataforma corporativa**: Red Hat RHEL AI + OpenShift AI (com Granite + InstructLab), ou Kubernetes + vLLM + KServe.
- **UI**: Open WebUI (multi-tenant simples), LibreChat (SSO/Azure AD), AnythingLLM (RAG por workspace), BionicGPT (enterprise hardening).
- **Vector store**: Qdrant, Milvus, Weaviate, pgvector.
- **Coding IDE**: Continue.dev (BYOM), Tabby (full-stack auto-hospedado).

## Fontes consultadas (consolidadas)

- PremAI: <https://blog.premai.io/self-hosted-llm-guide-setup-tools-cost-comparison-2026/>
- PremAI (LLM enterprise comparison): <https://blog.premai.io/llama-vs-mistral-vs-phi-complete-open-source-llm-comparison-for-enterprise-2026/>
- BentoML (open-source LLMs 2026): <https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models>
- BentoML (DeepSeek guide): <https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond>
- Onyx leaderboard: <https://onyx.app/self-hosted-llm-leaderboard>
- Truefoundry on-prem LLMs: <https://www.truefoundry.com/blog/on-prem-llms>
- Red Hat / Granite: <https://www.redhat.com/en/topics/ai/what-are-granite-models>
- Red Hat Developer (RAG OpenShift AI): <https://developers.redhat.com/articles/2026/01/29/deploy-enterprise-rag-chatbot-red-hat-openshift-ai>
- vLLM releases: <https://github.com/vllm-project/vllm/releases>
- JPMorgan case (Tearsheet): <https://tearsheet.co/artificial-intelligence/jpmorgan-chases-gen-ai-implementation-450-use-cases-and-lessons-learned/>
- BloombergGPT: <https://belitsoft.com/bloomberggpt>
- Petronella (private deployment guide): <https://petronellatech.com/blog/private-ai-deployment-guide-enterprise/>

(Referências detalhadas por caso ficam em cada arquivo individual.)
