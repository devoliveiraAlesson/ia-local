# Narrativa Boardroom — 12 Slides

> Etapa 5/5. Slides em markdown para apresentação executiva (board, comitê de risco, CFO/CIO/CEO). Maio/2026.
>
> Cada slide cabe em ~1 minuto de fala. Total: 12–15 minutos. Tempo restante: Q&A com `07-perguntas-frequentes.md` à mão.

---

## Slide 1 — A pergunta de negócio

> **Título**: Por que precisamos discutir IA hoje

- Em 2026, ferramentas como ChatGPT/Claude/Gemini já são usadas, formal ou informalmente, na empresa.
- Para empresas com dados sensíveis (PII, prontuários, código, contratos), a pergunta deixou de ser "se" e passou a ser:
  > **"Como capturar produtividade da IA generativa sem expor dado regulado a APIs públicas?"**
- 44% das organizações apontam privacidade como a principal barreira de adoção de LLMs (PremAI, 2026).
- O custo médio de breach de dados em 2025 foi US$ 4,88 M (IBM Security); 35% dos breaches em 2024 envolveram **shadow AI**.

**Mensagem**: o board precisa **decidir hoje** se quer capturar o ganho de produtividade dentro de um perímetro controlado, ou continuar absorvendo o risco do uso informal.

---

## Slide 2 — O que outros já fizeram (5 evidências)

> **Título**: Bancos T1 e estatais BR/UK/Singapura já capitalizaram

| Empresa | Resultado verificado |
|---------|----------------------|
| **JPMorgan LLM Suite** | 200k+ usuários; 3–6 h/sem economizadas; **US$ 1–2 bi/ano** declarado em valor |
| **Morgan Stanley AI @ MS** | **98% adoção** entre advisors |
| **BBVA** | 3 h/sem economizadas; 1.000+ data scientists; ~20k GPTs custom |
| **Walmart My Assistant + Wallaby** | **75k+ associados** corporativos |
| **Stripe (vLLM)** | **−73% de custo** após migração |
| **Bradesco/IBM** | ~R$ 400 M investidos |
| **Singapura Pair** | **−46% admin time** |

**Mensagem**: o playbook existe. Não estamos pioneirando; estamos seguindo um caminho **provado em escala**.

---

## Slide 3 — A arquitetura proposta em uma imagem

> **Título**: Plataforma comum — multi-modelo, governada, observável

```
Usuário ─▶ SSO ─▶ Gateway (LiteLLM) ─▶ Guardrails ─▶ vLLM ─▶ GPU H100/H200
                       │                   │              │
                       └─▶ RAG (Qdrant + BGE-M3) ──────────┘
                       │
                       └─▶ Observabilidade (Langfuse + OTel + WORM logs)
```

- **Multi-modelo desde o dia 1**: Llama 3.3 + Granite 4 + Qwen 3 (não dependência de modelo único).
- **Soberania**: nenhum prompt, embedding ou log sai do perímetro.
- **Air-gap-ready**: mirror Hugging Face local; sem dependência de internet em runtime.

**Mensagem**: arquitetura **modular**, **substituível por camada**, **alinhada com padrões abertos** (K8s, OTel, OCI, OpenAPI).

---

## Slide 4 — 14 casos de uso priorizados

> **Título**: Não vamos fazer IA "em geral" — começamos com 2 casos

**P0 — Quick wins (mês 2–5)**:
- **Caso 1** — Chat interno seguro (substituto privado do ChatGPT)
- **Caso 3** — RAG corporativo (plataforma habilitadora para 4–8 outros casos)

**P1 — Mês 5–12**:
- Caso 4 (coding) + Caso 5 (code review)
- Caso 2 (atendimento) + Caso 6 (sumarização) + Caso 7 (extração)

**P2/P3 — Mês 12+**:
- Casos 8–14 (tradução, docs técnicos, logs, compliance, treinamento, pareceres, e-mails) ativados conforme demanda.

**Mensagem**: começamos com **2 casos**, não com 14. **Vertical** (não "chat genérico isolado"). Lições aprendidas de JPMorgan e Singapura: chat genérico tem teto de adoção; vertical sustenta crescimento.

---

## Slide 5 — Faixa de retorno em 3 cenários (P/M/G)

> **Título**: ROI defensável com premissas explícitas

| Cenário | Usuários | CAPEX (HW + 30%) | OPEX/ano | Benefício/ano | Payback | NPV 5a |
|---------|----------|-------------------|----------|----------------|---------|---------|
| **P** | 500 | US$ 0,33–0,59 M | US$ 0,55 M | US$ 0,9–1,5 M | **10–15 m** | US$ 1,7–3,5 M |
| **M** | 5.000 | US$ 1,95–3,64 M | US$ 2,0 M | US$ 8–14 M | **8–14 m** | US$ 23–47 M |
| **G** | 50.000 | US$ 10,4–24,3 M | US$ 9 M | US$ 80–180 M | **6–12 m** | US$ 280–680 M |

> Premissas-âncora: 3 h/sem economizadas (BBVA), 60% adoção, custo-hora US$ 32 (US) / R$ 75 (BR).

**Mensagem**: a âncora não é "IA é o futuro". A âncora é **"3 h × custo-hora × adoção"** — números defensáveis vindos de empresas reais.

---

## Slide 6 — Vantagem on-prem vs API pública

> **Título**: A partir de ~30–40% de utilização, on-prem ganha em 5–25×

| Volume diário | API pública (GPT-4o blended US$ 4/1M) | On-prem (Llama 70B AWQ + H100) | Vantagem |
|---------------|----------------------------------------|----------------------------------|----------|
| 6 M tokens | US$ 8.800/ano | US$ 660/ano em compute | 13× |
| 170 M tokens | US$ 248 M/ano | US$ 12,4 M/ano em compute | 20× |
| 1,8 B tokens | US$ 2,6 bi/ano | US$ 99 M/ano em compute | 25× |

> Stripe declarou **−73% de custo** ao migrar para vLLM. Em volume corporativo, isso é **dezenas a centenas de milhões de US$/ano**.

**Mensagem**: on-prem só ganha **a partir de utilização efetiva ≥30%**. Por isso o desenho começa com 2 casos sólidos (chat + RAG) — para garantir utilização — e não com um portfólio inflado.

---

## Slide 7 — Roadmap em 4 fases (12 meses + Fase 4)

> **Título**: Não é um big bang. É um roadmap escalonado

| Fase | Mês | Foco | Decisão |
|------|-----|------|---------|
| **0** | 0–2 | Prontidão (DC, identidade, equipe, PO de GPU) | Go Fase 1 |
| **1** | 2–5 | Plataforma + Chat + RAG | **Gate Go/No-Go (mês 5)** |
| **2** | 5–8 | Coding + Code review | Go expansão devs |
| **3** | 8–12 | Atendimento + Sumarização + Extração | Go ano 2 |
| **4** | 12+ | InstructLab fine-tune, agentes, multimodal | — |

**Mensagem**: o board aprova hoje **Fase 0+1**. No mês 5, com dados reais de adoção, custo, latência, satisfação, decide Fases 2–4. Decisão **faseada**, não tudo de uma vez.

---

## Slide 8 — Equipe e orçamento por porte

> **Título**: O hardware é só metade do orçamento. A outra metade é gente.

| Porte | FTE | Orçamento ano 1 (BR R$) | Orçamento ano 1 (US US$) |
|-------|-----|---------------------------|---------------------------|
| **P** | 4–5 | 4–6 M | 1–2 M |
| **M** | 8–12 | 17–30 M | 4–7,5 M |
| **G** | 25–40 | 60–110 M | 14–25 M |

**Papéis-chave**: Sponsor, Tech Lead/Arquiteto LLM, ML Engineers, SREs, Data Engineers, Segurança/Compliance, POs por caso, DevEx, Treinamento.

**Mensagem**: o **maior risco financeiro não é o hardware** — é equipe insuficiente e adoção baixa. Investir em consultoria pesada (Red Hat / NVIDIA / IBM) nos primeiros 6 meses, com plano de internalização.

---

## Slide 9 — Riscos críticos e mitigação

> **Título**: 5 riscos que precisam de decisão executiva agora

| # | Risco | Mitigação |
|---|-------|-----------|
| 1 | **Lead time de GPU** (12–32 sem) | Pré-cotação imediata + cloud-bridge VPC primeiros 60 dias |
| 2 | **Equipe insuficiente** | Contrato Red Hat / NVIDIA PS / parceiro local + plano de internalização |
| 3 | **Subdimensionamento de utilização** | Multi-tenant via gateway + semantic cache desde dia 1; piso 30% |
| 4 | **Adoção baixa** | Vertical (não chat genérico); GenAI Championship Bosch-style; campeões |
| 5 | **Compliance LGPD/EU AI Act** | OTel GenAI + Langfuse self-host + WORM logs + ISO 42001 (Granite 4) |

**Mensagem**: o risco real **não é tecnológico** — é de **adoção, equipe e governança**. Documento `05-riscos-mitigacao.md` cobre 16 riscos em detalhe + mapeamento OWASP LLM Top 10.

---

## Slide 10 — Por que NÃO fazer híbrido com API pública apenas

> **Título**: API pública não cobre os 11 casos sensíveis

- Em **11 dos 14 casos** mapeados, dado sensível está exposto: e-mails internos, contratos, prontuários, código proprietário, base de clientes.
- API pública (mesmo com BAA/DPA) implica:
  - Sub-processadores não controlados
  - Concentração em 1 vendor (lock-in OpenAI/Anthropic/Google)
  - Custo variável imprevisível em escala
  - LGPD Art. 11 e EU AI Act high-risk **mais difíceis** de defender ao auditor
- **Padrão observado em empresas reais** (Etapa 3 §08): JPMorgan, Itaú, Bradesco, Bosch, BMW operam **híbrido com on-prem dominando casos sensíveis**.

**Mensagem**: a recomendação **não é "tudo on-prem"**. É **híbrido com on-prem como espinha dorsal** para os 11 casos sensíveis e API/Copilot apenas onde o dado é público/baixo risco.

---

## Slide 11 — Decisão pedida ao board hoje

> **Título**: 4 decisões pequenas, não 1 grande

| # | Decisão | Recomendação | CAPEX requerido agora |
|---|---------|--------------|-------------------------|
| 1 | Aprovar **Fase 0 + Fase 1** (5 meses) | **Sim** | US$ 0,8–1,2 M (Cenário M base) |
| 2 | Pré-cotação de GPU com lead time ≥ 16 sem | **Sim** | sem desembolso até PO |
| 3 | Nomear Sponsor Executivo + Tech Lead/Arquiteto LLM | **Sim** | sem CAPEX |
| 4 | Marcar **gate de mid-life para mês 5** (Go/No-Go Fases 2–4) | **Sim** | sem desembolso até gate |

**Mensagem**: a decisão **Fases 2–4 fica para o gate do mês 5** — após dados reais de adoção, custo, latência e satisfação do Caso 1 + RAG. **Sem comprometer agora** todo o CAPEX do Cenário M completo.

---

## Slide 12 — 5 mensagens finais para o board

> **Título**: Em uma página, o que importa

1. **A janela competitiva está aberta hoje** — bancos T1 e estatais BR já capitalizaram; quem não embarca em 12 meses fica em desvantagem em produtividade e compliance.
2. **A âncora não é "IA". A âncora é "3 h/sem × custo-hora × 60% adoção"** — números defensáveis vindos de JPMorgan/BBVA/Walmart.
3. **On-prem só ganha de API a partir de utilização ≥30–40%** — por isso o desenho começa com 2 casos sólidos (chat + RAG), não com 14.
4. **O risco real não é tecnológico, é de adoção e governança** — vertical, campeões, observabilidade desde o dia 1.
5. **A decisão é faseada** — board aprova Fase 0+1 hoje; revisa dados reais no mês 5; segue ou recalibra.

---

## Anexos para Q&A

- `00-sumario-executivo.md` — 1 página
- `01-modelo-roi-cenarios.md` — premissas, sensibilidade, NPV/TIR
- `02-comparativo-alternativas.md` — Local vs API vs Copilot vs Híbrido
- `03-roadmap-12-meses.md` — 4 fases com entregáveis
- `04-equipe-e-orcamento.md` — headcount BR/US
- `05-riscos-mitigacao.md` — 16 riscos + OWASP
- `07-perguntas-frequentes.md` — FAQ antecipado
- `08-decisao-go-no-go.md` — checklist
- `09-anexo-fontes.md` — bibliografia

---

## Bônus — slide reserva: comparação com competidores BR

| Empresa | Investimento conhecido | Ano | Status |
|---------|------------------------|-----|--------|
| Bradesco/IBM | R$ 400 M | 2024–2026 | Produção (BIA, Bridge) |
| Itaú | n/p | 2024–2025 | Produção (Inteligência Itaú multi-agente) |
| BTG Pactual | n/p (Saturn Platform interna) | 2024+ | Produção (assistente WhatsApp) |
| Petrobras | n/p (Azure OpenAI) | 2024+ | Produção (ChatPetrobras 110k usuários) |
| **Nossa empresa hoje** | — | — | **Em decisão** |

**Mensagem**: BR está se mexendo. Conglomerados regulados estão capitalizando agora. **A janela é de 6–12 meses** antes da defasagem ficar visível.
