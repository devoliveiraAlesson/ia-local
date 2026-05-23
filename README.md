# Proposta: IA Local On-Premises para Empresa com Dados Sensíveis

Estudo e proposta para implantação de modelos de IA rodando localmente (on-premises ou em nuvem privada), com foco em segurança de dados, soberania e ROI. Maio/2026.

## Status

- [x] **01 — Casos de uso** (14 casos priorizados P0–P3, roadmap 12 meses)
- [x] **02 — Tecnologias** (12 docs, stack arquetípica, licenças)
- [x] **03 — Exemplos reais** (34 empresas, 5 stacks arquetípicas, lições)
- [x] **04 — Infraestrutura** (dimensionamento P/M/G, CAPEX, decisões executivas)
- [x] **05 — ROI e proposta consolidada** (10 documentos boardroom-ready)
- [x] **06 — MCP + Claude Code** (8 docs, RAG/Graph como tool nativa, segurança e roadmap)
- [x] **07 — Design System para Apresentações** (6 docs, tokens DTCG, Google Slides MCP, wizard guiado)

**Trilha de capacitação — nova função (Comercial × Marketing × Dados):**

- [x] **08 — RevOps** (8 docs: fundamentos, papel, métricas, stack, processos, roadmap 90 dias, referências)
- [x] **09 — Marketing Mix Model** (7 docs: fundamentos, estatística, implementação, decisão, caso aplicado, roadmap)
- [x] **10 — Startup Enxuta / Lean Startup** (6 docs: fundamentos, build-measure-learn, métricas, aplicação, roadmap)

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

### Etapa 6 — MCP + Claude Code

| Doc | Conteúdo |
|-----|----------|
| [`06-mcp-claude-code/00-resumo-executivo.md`](./06-mcp-claude-code/00-resumo-executivo.md) | Por que MCP, mensagem-chave, conexão com Etapas 1–5 |
| [`06-mcp-claude-code/01-mcp-fundamentos.md`](./06-mcp-claude-code/01-mcp-fundamentos.md) | Protocolo, transportes (stdio/HTTP), escopos, SDKs |
| [`06-mcp-claude-code/02-rag-via-mcp.md`](./06-mcp-claude-code/02-rag-via-mcp.md) | RAG corporativo (Caso 3) exposto como tool MCP com rerank |
| [`06-mcp-claude-code/03-graph-rag-via-mcp.md`](./06-mcp-claude-code/03-graph-rag-via-mcp.md) | Graph RAG (Neo4j, Kuzu) via MCP — quando estrutura > texto |
| [`06-mcp-claude-code/04-servidores-mcp-prontos.md`](./06-mcp-claude-code/04-servidores-mcp-prontos.md) | Catálogo curado (RAG, vector stores, knowledge graph, dev tooling) |
| [`06-mcp-claude-code/05-construir-mcp-interno.md`](./06-mcp-claude-code/05-construir-mcp-interno.md) | Adapter próprio (FastMCP / TypeScript) sobre APIs internas |
| [`06-mcp-claude-code/06-seguranca-governanca.md`](./06-mcp-claude-code/06-seguranca-governanca.md) | OWASP LLM Top 10 × MCP, OAuth 2.1, OPA, DLP, allowlist |
| [`06-mcp-claude-code/07-roadmap-adocao.md`](./06-mcp-claude-code/07-roadmap-adocao.md) | Fases 0–3, KPIs, orçamento incremental |

### Etapa 7 — Design System para Apresentações (Google Slides + MCP)

| Doc | Conteúdo | Audiência |
|-----|----------|-----------|
| [`07-design-system-apresentacoes/00-resumo-executivo.md`](./07-design-system-apresentacoes/00-resumo-executivo.md) | Viabilidade, decisões executivas, conexão com Etapas 3 e 6 | Tech Lead / Liderança |
| [`07-design-system-apresentacoes/01-arquitetura-e-fundamentos.md`](./07-design-system-apresentacoes/01-arquitetura-e-fundamentos.md) | Stack completa: tokens → templates → skills → wizard → Drive | Arquiteto / Tech Lead |
| [`07-design-system-apresentacoes/02-design-tokens-pptx.md`](./07-design-system-apresentacoes/02-design-tokens-pptx.md) | Formato DTCG 2025.10, estrutura de tokens, mapeamento para Slides API e python-pptx | Designer / Eng plataforma |
| [`07-design-system-apresentacoes/03-mcp-google-drive-slides.md`](./07-design-system-apresentacoes/03-mcp-google-drive-slides.md) | Catálogo de servidores MCP (Google oficial + community), fluxo de criação, autenticação | Eng de plataforma |
| [`07-design-system-apresentacoes/04-wizard-guiado.md`](./07-design-system-apresentacoes/04-wizard-guiado.md) | Roteiro de 5 etapas do wizard, skills de slides, outline JSON, integração RAG | Eng de software |
| [`07-design-system-apresentacoes/05-construir-servidor-mcp.md`](./07-design-system-apresentacoes/05-construir-servidor-mcp.md) | Build completo do servidor FastMCP: wizard, tokens, Drive client, Slides client, deploy | Eng de software |
| [`07-design-system-apresentacoes/06-roadmap-adocao.md`](./07-design-system-apresentacoes/06-roadmap-adocao.md) | Fases 0–3, gates de aprovação, métricas, integrações avançadas (RAG, PDF→slides, Jira) | PMO / Tech Lead |

---

## Trilha de capacitação — RevOps, MMM e Lean Startup

> Dossiês para a função de pivot entre Comercial e Marketing (perfil cientista de dados + publicitário). Os três temas se conectam de propósito: **Lean Startup é o método** (hipótese → experimento → aprendizado validado), **RevOps é a operação de receita orientada a dados**, e o **Marketing Mix Model é uma das máquinas de decisão de investimento**. Recomendo ler na ordem 10 → 08 → 09, ou começar pelo resumo executivo de cada um.

### Etapa 8 — RevOps (Revenue Operations)

| Doc | Conteúdo |
|-----|----------|
| [`08-revops/00-resumo-executivo.md`](./08-revops/00-resumo-executivo.md) | O que é RevOps, por que existe, conexão com seu perfil de dados + publicidade |
| [`08-revops/01-fundamentos-revops.md`](./08-revops/01-fundamentos-revops.md) | Definição, origem, silos Mkt/Vendas/CS, modelo bowtie, RevOps vs SalesOps vs MktOps |
| [`08-revops/02-papel-e-responsabilidades.md`](./08-revops/02-papel-e-responsabilidades.md) | Responsabilidades, maturidade e seção "onde seu perfil de cientista de dados entra" |
| [`08-revops/03-metricas-e-kpis.md`](./08-revops/03-metricas-e-kpis.md) | Métricas por estágio do funil, fórmulas e benchmarks (CAC, LTV, NRR, win rate, forecast) |
| [`08-revops/04-stack-ferramentas.md`](./08-revops/04-stack-ferramentas.md) | CRM, automação, BI, revenue intelligence; comparativo + nota Brasil (RD Station) |
| [`08-revops/05-processos-e-frameworks.md`](./08-revops/05-processos-e-frameworks.md) | Lead lifecycle, SLAs MQL→SQL, forecasting, cadência RevOps, governança de dados |
| [`08-revops/06-roadmap-90-dias.md`](./08-revops/06-roadmap-90-dias.md) | Plano 30/60/90, primeiros entregáveis que provam valor, armadilhas comuns |
| [`08-revops/07-referencias-e-aprendizado.md`](./08-revops/07-referencias-e-aprendizado.md) | Livros, comunidades, certificações e bibliografia consolidada |

### Etapa 9 — Marketing Mix Model (MMM)

| Doc | Conteúdo |
|-----|----------|
| [`09-marketing-mix-model/00-resumo-executivo.md`](./09-marketing-mix-model/00-resumo-executivo.md) | O que é MMM, renascimento (cookieless/LGPD), conexão com seu perfil |
| [`09-marketing-mix-model/01-fundamentos-mmm.md`](./09-marketing-mix-model/01-fundamentos-mmm.md) | Definição, história, base vs incremental, MMM vs MTA vs testes de incrementalidade |
| [`09-marketing-mix-model/02-metodologia-estatistica.md`](./09-marketing-mix-model/02-metodologia-estatistica.md) | Regressão, adstock, saturação (Hill), ridge, abordagem Bayesiana, calibração |
| [`09-marketing-mix-model/03-implementacao-pratica.md`](./09-marketing-mix-model/03-implementacao-pratica.md) | Dados necessários, Meridian/Robyn/PyMC-Marketing, workflow e código |
| [`09-marketing-mix-model/04-interpretacao-e-decisao.md`](./09-marketing-mix-model/04-interpretacao-e-decisao.md) | Decomposição, ROI/ROAS, curvas de resposta, otimização de budget, validação |
| [`09-marketing-mix-model/05-caso-aplicado.md`](./09-marketing-mix-model/05-caso-aplicado.md) | Caso aplicado à sua realidade: canais, dados, hipóteses, primeiro entregável |
| [`09-marketing-mix-model/06-roadmap-e-referencias.md`](./09-marketing-mix-model/06-roadmap-e-referencias.md) | Plano faseado (crawl/walk/run), maturidade, armadilhas, bibliografia |

### Etapa 10 — Startup Enxuta (Lean Startup)

| Doc | Conteúdo |
|-----|----------|
| [`10-startup-enxuta/00-resumo-executivo.md`](./10-startup-enxuta/00-resumo-executivo.md) | Lean Startup afiado para quem já conhece o básico, por que cabe no seu cenário, conexão 08+09 |
| [`10-startup-enxuta/01-fundamentos-lean-startup.md`](./10-startup-enxuta/01-fundamentos-lean-startup.md) | Linhagem (Ries/Blank/Toyota/Agile), 5 princípios, aprendizado validado, intraempreendedorismo |
| [`10-startup-enxuta/02-build-measure-learn.md`](./10-startup-enxuta/02-build-measure-learn.md) | Loop construir-medir-aprender, hipóteses, MVP, catálogo de pivôs |
| [`10-startup-enxuta/03-metricas-experimentacao.md`](./10-startup-enxuta/03-metricas-experimentacao.md) | Contabilidade da inovação, métricas de vaidade vs acionáveis, coorte, A/B, rigor estatístico |
| [`10-startup-enxuta/04-aplicacao-comercial-marketing-revops.md`](./10-startup-enxuta/04-aplicacao-comercial-marketing-revops.md) | Ponte: experimentos em RevOps/marketing/comercial + template de experimento reutilizável |
| [`10-startup-enxuta/05-roadmap-e-referencias.md`](./10-startup-enxuta/05-roadmap-e-referencias.md) | Plano 90 dias, maturidade, armadilhas, trilha de leitura (Ries, Maurya, Lean Analytics) |

---

## Estrutura de pastas

| Pasta | Conteúdo |
|---|---|
| `01-casos-de-uso/` | Mapeamento de 14 casos de uso aplicáveis. |
| `02-tecnologias/` | Stack tecnológica em 8 camadas (runtimes, modelos, frameworks, RAG, gateways, guardrails, observabilidade, fine-tuning). |
| `03-exemplos-reais/` | 34 casos reais de empresas (financeiro, saúde, indústria, varejo, SaaS, governo) + lições aprendidas. |
| `04-infraestrutura/` | Hardware, dimensionamento, rede, storage, orquestração, segurança, energia, checklist. |
| `05-roi-e-proposta/` | ROI por cenário, comparação com alternativas, riscos, roadmap, narrativa boardroom, FAQ, decisão. |
| `06-mcp-claude-code/` | MCP como camada de tool-calling: RAG/Graph como serviço nativo do agente, servidor MCP corporativo, segurança, roadmap. |
| `07-design-system-apresentacoes/` | Design system para Google Slides/PPTX: tokens DTCG, templates no Drive, servidor MCP com wizard guiado, skills de slides, roadmap de adoção. |
| `08-revops/` | Revenue Operations: fundamentos, papel e responsabilidades, métricas/KPIs, stack de ferramentas, processos, roadmap 90 dias e referências. |
| `09-marketing-mix-model/` | Marketing Mix Model: fundamentos, metodologia estatística (adstock, saturação, Bayesiano), implementação (Meridian/Robyn/PyMC), decisão e caso aplicado. |
| `10-startup-enxuta/` | Lean Startup aplicado: build-measure-learn, métricas acionáveis vs vaidade, experimentação em RevOps/marketing/comercial, roadmap e referências. |

---

## Metodologia

A pesquisa foi executada por **5 agentes em modo sequencial** — cada agente recebeu e expandiu o contexto do anterior, evitando duplicação e centralizando o conhecimento construído. As Etapas 1–4 produzem dados; a Etapa 5 consolida em proposta executiva com ROI defensável.

Todos os números monetários (CAPEX, OPEX, salários, benefícios) são **estimativa pública** ancorada em casos verificados ou tabelas de mercado, com fonte explícita. Não substituem orçamento formal de fornecedor.

---

## Mensagem-chave em uma linha

> **A janela competitiva está aberta hoje. A âncora é "3 h/semana × custo-hora × 60% adoção" (BBVA, JPMorgan). O risco real não é tecnológico — é adoção e governança. A decisão é faseada: aprovar Fase 0+1 hoje (US$ 0,8–1,2 M no Cenário M); revisar dados reais no mês 5.**

Próximos documentos a ler dependendo do papel: ver "Como ler esta proposta" no topo deste README.
