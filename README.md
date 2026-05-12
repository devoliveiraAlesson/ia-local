# Proposta: IA Local On-Premises para Empresa com Dados Sensíveis

Estudo e proposta para implantação de modelos de IA rodando localmente (on-premises ou em nuvem privada), com foco em segurança de dados, soberania e ROI. Maio/2026.

## Status

- [x] **01 — Casos de uso** (14 casos priorizados P0–P3, roadmap 12 meses)
- [x] **02 — Tecnologias** (12 docs, stack arquetípica, licenças)
- [x] **03 — Exemplos reais** (34 empresas, 5 stacks arquetípicas, lições)
- [x] **04 — Infraestrutura** (dimensionamento P/M/G, CAPEX, decisões executivas)
- [x] **05 — ROI e proposta consolidada** (10 documentos boardroom-ready)

---

## Como ler esta proposta

Para a **liderança / board** (15 minutos): comece em
1. [`05-roi-e-proposta/00-sumario-executivo.md`](./05-roi-e-proposta/00-sumario-executivo.md) — 1–2 páginas
2. [`05-roi-e-proposta/06-narrativa-boardroom.md`](./05-roi-e-proposta/06-narrativa-boardroom.md) — 12 slides
3. [`05-roi-e-proposta/08-decisao-go-no-go.md`](./05-roi-e-proposta/08-decisao-go-no-go.md) — checklist

Para o **CFO / controladoria** (30 minutos):
- [`05-roi-e-proposta/01-modelo-roi-cenarios.md`](./05-roi-e-proposta/01-modelo-roi-cenarios.md) — premissas, NPV, sensibilidade
- [`05-roi-e-proposta/04-equipe-e-orcamento.md`](./05-roi-e-proposta/04-equipe-e-orcamento.md) — headcount BR/US

Para o **CIO / CISO / DPO** (45 minutos):
- [`05-roi-e-proposta/02-comparativo-alternativas.md`](./05-roi-e-proposta/02-comparativo-alternativas.md) — Local vs API vs Copilot vs Híbrido
- [`05-roi-e-proposta/05-riscos-mitigacao.md`](./05-roi-e-proposta/05-riscos-mitigacao.md) — 16 riscos + OWASP LLM Top 10
- [`04-infraestrutura/00-resumo-arquitetura.md`](./04-infraestrutura/00-resumo-arquitetura.md) — arquitetura de referência

Para o **PMO / Tech Lead** (1–2 horas):
- [`05-roi-e-proposta/03-roadmap-12-meses.md`](./05-roi-e-proposta/03-roadmap-12-meses.md) — 4 fases
- [`04-infraestrutura/11-checklist-prontidao.md`](./04-infraestrutura/11-checklist-prontidao.md) — gate Fase 0
- [`02-tecnologias/00-mapa-da-stack.md`](./02-tecnologias/00-mapa-da-stack.md) — 8 camadas

Para perguntas executivas (Q&A boardroom):
- [`05-roi-e-proposta/07-perguntas-frequentes.md`](./05-roi-e-proposta/07-perguntas-frequentes.md) — FAQ antecipado

---

## Índice navegável

### Etapa 1 — Casos de uso

| Doc | Conteúdo |
|-----|----------|
| [`01-casos-de-uso/00-resumo-executivo.md`](./01-casos-de-uso/00-resumo-executivo.md) | 14 casos P0–P3, roadmap 12 meses |
| [`01-casos-de-uso/01-chat-interno.md`](./01-casos-de-uso/01-chat-interno.md) | Caso 1 — Chat interno seguro |
| [`01-casos-de-uso/02-atendimento-cliente.md`](./01-casos-de-uso/02-atendimento-cliente.md) | Caso 2 — Atendimento ao cliente |
| [`01-casos-de-uso/03-embeddings-rag.md`](./01-casos-de-uso/03-embeddings-rag.md) | Caso 3 — RAG corporativo |
| [`01-casos-de-uso/04-coding-assistant.md`](./01-casos-de-uso/04-coding-assistant.md) | Caso 4 — Coding assistant |
| [`01-casos-de-uso/05-code-review.md`](./01-casos-de-uso/05-code-review.md) | Caso 5 — Code review |
| [`01-casos-de-uso/06-sumarizacao.md`](./01-casos-de-uso/06-sumarizacao.md) | Caso 6 — Sumarização |
| [`01-casos-de-uso/07-extracao-estruturada.md`](./01-casos-de-uso/07-extracao-estruturada.md) | Caso 7 — Extração estruturada |
| [`01-casos-de-uso/08-outros-casos.md`](./01-casos-de-uso/08-outros-casos.md) | Casos 8–14 |

### Etapa 2 — Tecnologias

| Doc | Conteúdo |
|-----|----------|
| [`02-tecnologias/00-mapa-da-stack.md`](./02-tecnologias/00-mapa-da-stack.md) | Mapa em 8 camadas |
| [`02-tecnologias/01-runtimes-inferencia.md`](./02-tecnologias/01-runtimes-inferencia.md) | vLLM, SGLang, TGI, llama.cpp, ... |
| [`02-tecnologias/02-modelos-abertos.md`](./02-tecnologias/02-modelos-abertos.md) | Llama, Qwen, DeepSeek, Granite, ... |
| [`02-tecnologias/03-frameworks-aplicacao.md`](./02-tecnologias/03-frameworks-aplicacao.md) | LangChain, LlamaIndex, Haystack, DSPy |
| [`02-tecnologias/04-frontends-chat.md`](./02-tecnologias/04-frontends-chat.md) | Open WebUI, LibreChat, AnythingLLM, Continue, Tabby |
| [`02-tecnologias/05-rag-vector-stores.md`](./02-tecnologias/05-rag-vector-stores.md) | Qdrant, Milvus, Weaviate, pgvector |
| [`02-tecnologias/06-plataformas-enterprise.md`](./02-tecnologias/06-plataformas-enterprise.md) | OpenShift AI, RHEL AI, watsonx, NIM |
| [`02-tecnologias/07-guardrails-seguranca.md`](./02-tecnologias/07-guardrails-seguranca.md) | Llama Guard 3, Presidio, NeMo Guardrails |
| [`02-tecnologias/08-observabilidade-finops.md`](./02-tecnologias/08-observabilidade-finops.md) | Langfuse, Phoenix, OTel GenAI, Ragas |
| [`02-tecnologias/09-gateways-llm.md`](./02-tecnologias/09-gateways-llm.md) | LiteLLM, Portkey, Kong AI, Envoy AI |
| [`02-tecnologias/10-finetuning-adaptacao.md`](./02-tecnologias/10-finetuning-adaptacao.md) | LoRA, InstructLab, Axolotl |
| [`02-tecnologias/11-licencas-modelos.md`](./02-tecnologias/11-licencas-modelos.md) | Tabela master de licenças (Llama 700M MAU, Codestral MNPL, ...) |

### Etapa 3 — Exemplos reais

| Doc | Conteúdo |
|-----|----------|
| [`03-exemplos-reais/00-tabela-mestre.md`](./03-exemplos-reais/00-tabela-mestre.md) | 34 empresas com casos públicos |
| [`03-exemplos-reais/01-financeiro.md`](./03-exemplos-reais/01-financeiro.md) | JPMorgan, Morgan Stanley, Itaú, Bradesco, BBVA, ... |
| [`03-exemplos-reais/02-saude-farma.md`](./03-exemplos-reais/02-saude-farma.md) | Mayo, Cleveland, Bayer, Pfizer, Roche, ... |
| [`03-exemplos-reais/03-industria-manufatura.md`](./03-exemplos-reais/03-industria-manufatura.md) | Bosch, Siemens, BMW, Mercedes, ... |
| [`03-exemplos-reais/04-varejo-ecommerce.md`](./03-exemplos-reais/04-varejo-ecommerce.md) | Walmart, Mercado Livre, ... |
| [`03-exemplos-reais/05-tecnologia-saas.md`](./03-exemplos-reais/05-tecnologia-saas.md) | Stripe, Snowflake, Databricks, Red Hat, ... |
| [`03-exemplos-reais/06-governo-defesa.md`](./03-exemplos-reais/06-governo-defesa.md) | Singapura, UK, Petrobras, Serpro, ... |
| [`03-exemplos-reais/07-discussoes-comunidade.md`](./03-exemplos-reais/07-discussoes-comunidade.md) | Reddit r/LocalLLaMA, blogs técnicos |
| [`03-exemplos-reais/08-stacks-arquetipicas.md`](./03-exemplos-reais/08-stacks-arquetipicas.md) | 5 perfis sintéticos |
| [`03-exemplos-reais/09-licoes-aprendidas.md`](./03-exemplos-reais/09-licoes-aprendidas.md) | Armadilhas e práticas vencedoras |

### Etapa 4 — Infraestrutura

| Doc | Conteúdo |
|-----|----------|
| [`04-infraestrutura/00-resumo-arquitetura.md`](./04-infraestrutura/00-resumo-arquitetura.md) | Arquitetura de referência em 13 camadas |
| [`04-infraestrutura/01-hardware-aceleracao.md`](./04-infraestrutura/01-hardware-aceleracao.md) | NVIDIA / AMD / Intel comparativo |
| [`04-infraestrutura/02-dimensionamento-por-caso.md`](./04-infraestrutura/02-dimensionamento-por-caso.md) | 3 cenários P/M/G por caso |
| [`04-infraestrutura/03-redes.md`](./04-infraestrutura/03-redes.md) | InfiniBand, Spectrum-X, RoCEv2 |
| [`04-infraestrutura/04-storage.md`](./04-infraestrutura/04-storage.md) | Modelos, datasets, vector, logs |
| [`04-infraestrutura/05-orquestracao.md`](./04-infraestrutura/05-orquestracao.md) | K8s/KServe, OpenShift AI, Ray, Slurm |
| [`04-infraestrutura/06-seguranca-compliance.md`](./04-infraestrutura/06-seguranca-compliance.md) | Air-gap, OWASP LLM, LGPD/HIPAA/ISO 42001 |
| [`04-infraestrutura/07-observabilidade-operacao.md`](./04-infraestrutura/07-observabilidade-operacao.md) | Prom/Grafana/DCGM + Langfuse + OTel |
| [`04-infraestrutura/08-continuidade-dr.md`](./04-infraestrutura/08-continuidade-dr.md) | HA, canary, RPO/RTO |
| [`04-infraestrutura/09-energia-fisica.md`](./04-infraestrutura/09-energia-fisica.md) | kW/rack, DLC, espaço |
| [`04-infraestrutura/10-cloud-privada-hibrido.md`](./04-infraestrutura/10-cloud-privada-hibrido.md) | Outposts, Azure Local, OCI, IBM |
| [`04-infraestrutura/11-checklist-prontidao.md`](./04-infraestrutura/11-checklist-prontidao.md) | Gate de prontidão antes do projeto |

### Etapa 5 — ROI e proposta consolidada

| Doc | Conteúdo | Audiência |
|-----|----------|-----------|
| [`05-roi-e-proposta/00-sumario-executivo.md`](./05-roi-e-proposta/00-sumario-executivo.md) | 1–2 páginas executivas | Board / CEO |
| [`05-roi-e-proposta/01-modelo-roi-cenarios.md`](./05-roi-e-proposta/01-modelo-roi-cenarios.md) | 3 cenários P/M/G + sensibilidade + NPV/TIR | CFO / Controladoria |
| [`05-roi-e-proposta/02-comparativo-alternativas.md`](./05-roi-e-proposta/02-comparativo-alternativas.md) | Local vs API vs Copilot vs Híbrido | CIO / CISO |
| [`05-roi-e-proposta/03-roadmap-12-meses.md`](./05-roi-e-proposta/03-roadmap-12-meses.md) | Fases 0–4 com entregáveis e métricas | PMO / Tech Lead |
| [`05-roi-e-proposta/04-equipe-e-orcamento.md`](./05-roi-e-proposta/04-equipe-e-orcamento.md) | Headcount BR/US por porte | RH / CFO |
| [`05-roi-e-proposta/05-riscos-mitigacao.md`](./05-roi-e-proposta/05-riscos-mitigacao.md) | 16 riscos + OWASP LLM Top 10 | CISO / Comitê risco |
| [`05-roi-e-proposta/06-narrativa-boardroom.md`](./05-roi-e-proposta/06-narrativa-boardroom.md) | 12 slides em markdown | Board / CEO |
| [`05-roi-e-proposta/07-perguntas-frequentes.md`](./05-roi-e-proposta/07-perguntas-frequentes.md) | FAQ antecipado (Q&A) | Para Q&A board |
| [`05-roi-e-proposta/08-decisao-go-no-go.md`](./05-roi-e-proposta/08-decisao-go-no-go.md) | Checklist consolidado de decisão | Sponsor / comitê |
| [`05-roi-e-proposta/09-anexo-fontes.md`](./05-roi-e-proposta/09-anexo-fontes.md) | Bibliografia consolidada de todas as etapas | Auditoria / due diligence |

---

## Estrutura de pastas

| Pasta | Conteúdo |
|---|---|
| `01-casos-de-uso/` | Mapeamento de 14 casos de uso aplicáveis. |
| `02-tecnologias/` | Stack tecnológica em 8 camadas (runtimes, modelos, frameworks, RAG, gateways, guardrails, observabilidade, fine-tuning). |
| `03-exemplos-reais/` | 34 casos reais de empresas (financeiro, saúde, indústria, varejo, SaaS, governo) + lições aprendidas. |
| `04-infraestrutura/` | Hardware, dimensionamento, rede, storage, orquestração, segurança, energia, checklist. |
| `05-roi-e-proposta/` | ROI por cenário, comparação com alternativas, riscos, roadmap, narrativa boardroom, FAQ, decisão. |

---

## Metodologia

A pesquisa foi executada por **5 agentes em modo sequencial** — cada agente recebeu e expandiu o contexto do anterior, evitando duplicação e centralizando o conhecimento construído. As Etapas 1–4 produzem dados; a Etapa 5 consolida em proposta executiva com ROI defensável.

Todos os números monetários (CAPEX, OPEX, salários, benefícios) são **estimativa pública** ancorada em casos verificados ou tabelas de mercado, com fonte explícita. Não substituem orçamento formal de fornecedor.

---

## Mensagem-chave em uma linha

> **A janela competitiva está aberta hoje. A âncora é "3 h/semana × custo-hora × 60% adoção" (BBVA, JPMorgan). O risco real não é tecnológico — é adoção e governança. A decisão é faseada: aprovar Fase 0+1 hoje (US$ 0,8–1,2 M no Cenário M); revisar dados reais no mês 5.**

Próximos documentos a ler dependendo do papel: ver "Como ler esta proposta" no topo deste README.
