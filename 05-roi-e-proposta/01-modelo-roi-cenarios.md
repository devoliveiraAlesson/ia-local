# Modelo de ROI — 3 Cenários (P / M / G)

> Etapa 5/5 da proposta. Documento técnico-financeiro. Para CFO, controladoria, FinOps e diretoria de TI. Maio/2026.
>
> **Disclaimer**: todos os valores são **estimativa pública** ancorada em (a) casos verificados na Etapa 3 (JPMorgan, BBVA, Walmart, Stripe, Bradesco), (b) CAPEX de hardware da Etapa 4 §02, (c) tabelas de preço de provedores cloud em maio/2026. Não substitui orçamento formal de fornecedor.

## 1. Premissas comuns aos 3 cenários

### 1.1 Premissas de produtividade (âncoras de mercado)

| Variável | Valor base | Faixa | Fonte / âncora |
|---------|-----------|-------|------------------|
| Horas/semana economizadas por usuário ativo | **3 h** | 2–6 h | BBVA (3h), JPMorgan (3–6h) — Etapa 3 §01 |
| Adoção (% dos elegíveis que viram ativos) | **60%** | 40–80% | Morgan Stanley 98% (advisors), Walmart 75k de ~210k corp ≈ 35%, BBVA 87k de ~120k ≈ 73%. Base conservadora 60%. |
| Semanas úteis/ano | 46 | — | Padrão BR/US (descontando férias + feriados) |
| Salário médio totalmente carregado (BR) | **R$ 12.000/mês** | R$ 7k–25k | Empresa média/grande BR; inclui encargos ~80% |
| Salário médio totalmente carregado (US) | **US$ 60.000/ano** | US$ 40k–120k | Empresa média/grande US; inclui benefits ~30% |
| Custo-hora médio BR | **R$ 75/h** | R$ 44–156 | R$ 12k × 12 ÷ 12 meses ÷ 160h |
| Custo-hora médio US | **US$ 32/h** | US$ 22–65 | US$ 60k ÷ 1.880h |
| Câmbio assumido | **R$ 5,00 / US$ 1,00** | — | Maio/2026 referência |

### 1.2 Premissas de utilização técnica (Etapa 4)

| Variável | Valor |
|---------|-------|
| Mensagens chat/usuário ativo/dia | 15 (base), 20 (heavy) |
| Tokens médios por mensagem (in + out) | 800 |
| Devs ativos / total devs | 70% |
| Completions coding / dev / dia | 150 |
| Conversas atendimento simultâneas (pico) | concorrência 10–800 conforme porte |
| Utilização efetiva GPU alvo | **>30%** (piso para superar API pública) |
| Throughput Llama 70B AWQ TP=4 H100 | 5.000–7.000 tokens/s |
| Custo/1M tokens on-prem (Llama 70B AWQ + H100 utilizado) | **US$ 0,15–0,30** (Etapa 2 + Stripe –73% ref.) |
| Custo/1M tokens API pública (GPT-4o, Claude Sonnet) | **US$ 3,00–5,00** |

### 1.3 Premissas financeiras

| Variável | BR | US |
|---------|----|-----|
| Taxa de desconto (NPV) | 13% a.a. | 8% a.a. |
| Vida útil do hardware (depreciação) | 4 anos | 4 anos |
| Vida útil contábil (CFO mode) | 5 anos | 5 anos |
| Inflação OPEX | 5% a.a. | 3% a.a. |
| Custo energia (R$/kWh ou US$/kWh) | R$ 0,75 | US$ 0,12 |
| PUE assumido | 1,4 | 1,4 |

### 1.4 Multiplicador CAPEX além do hardware

Sobre o CAPEX de hardware (Etapa 4 §02), somar:
- **+25–35%** rede (InfiniBand, switches, cabeamento), storage compartilhado, racks, retrofit DC, software enterprise (RHEL AI, NVIDIA AI Enterprise, Langfuse Enterprise se aplicável), implementação (consultoria, instalação).
- Cenários abaixo usam **+30%** como ponto médio.

---

## 2. Cenário P — Pequeno (500 usuários ativos)

### 2.1 Perfil

- Empresa regulada média (escritório jurídico/auditoria, hospital regional, BPO, seguradora média).
- Casos cobertos: Chat interno (Caso 1) + RAG corporativo (Caso 3) + Sumarização (Caso 6) + Coding 50 devs (Caso 4 — opcional).
- Topologia: 1 nó GPU on-prem ou VPC dedicada single-tenant.
- Referência de stack: **Perfil D — regulado médio** (Etapa 3 §08).

### 2.2 Investimento (CAPEX, ano 0)

| Item | Faixa US$ | Faixa BR R$ |
|------|-----------|--------------|
| Hardware (Etapa 4 §02 — agregado P) | 250–450k | 1,25–2,25 M |
| +30% rede/storage/SW/implantação | 75–135k | 375–675k |
| **CAPEX total ano 0** | **325–585k** | **1,63–2,93 M** |

### 2.3 OPEX anual (ano 1+)

| Item | US$/ano | R$/ano | Notas |
|------|---------|--------|-------|
| Energia (10–15 kW × 24/365 × 1,4 PUE) | 12–22k | 60–110k | |
| Suporte HW + SW (15–18% CAPEX HW) | 50–80k | 250–400k | NVIDIA AI Enterprise opcional |
| Equipe (3 FTE — ver `04-equipe-e-orcamento.md`) | 290–360k | 750–950k | Tech lead + 1 ML eng + 0,5 SRE + 0,5 sec |
| Co-location (se aplicável) | 25–60k | 125–300k | Opcional |
| Manutenção / fine-tune / evals | 15–25k | 75–125k | |
| **OPEX total** | **390–710k** | **1,26–1,89 M** |

### 2.4 Comparação com API pública (mesmo volume)

- Volume P ≈ **6 M tokens/dia** (chat 3,6M + RAG 1,5M + sum 0,9M + coding 2,1M) ≈ **2,2 bilhões tokens/ano**.
- API pública (GPT-4o, blended in+out US$ 4/1M): **US$ 8,8 M/ano**.
- API pública com tier corporate (Claude Haiku/Mistral Small via Bedrock US$ 1/1M blended): **US$ 2,2 M/ano**.
- On-prem (US$ 0,30/1M efetivo): **US$ 0,66 M/ano** em compute (já em OPEX acima).
- **Vantagem on-prem**: 3–13× em pure compute. Importante: em Cenário P, o ROI **não vem do compute** — vem do tempo economizado e do controle de dados.

### 2.5 Benefícios anuais quantificados

| Benefício | Cálculo | Valor estimado US$/ano | Valor BR R$/ano |
|-----------|---------|------------------------|------------------|
| Tempo economizado (chat geral) | 500 × 60% × 3h × 46 sem × US$32/h | **1,33 M** | 6,6 M |
| Tickets desviados (atendimento P P0/P1) | 1.000 conv/dia × 30% deflect × 365 × US$5 | 0,55 M | 2,75 M |
| Custo evitado SaaS (Copilot M365 a US$30/seat × 60% × 500) | 9k × 12 | 0,11 M | 0,55 M |
| Custo evitado API GPT-4o equivalente | (vs Bedrock blended) | 1,5–2,0 M | 7,5–10,0 M |
| **Total benefícios estimados** | — | **~2,0–4,0 M** | **10–20 M** |

### 2.6 Resultado consolidado P

| Métrica | Valor |
|---------|-------|
| CAPEX total ano 0 | US$ 0,33–0,59 M |
| OPEX anual médio | US$ 0,55 M |
| Benefício anual estimado | US$ 0,9–1,5 M (cenário conservador, descontando overlap) |
| **Payback estimado** | **10–15 meses** |
| **NPV 5 anos @ 8% (US)** | US$ 1,7–3,5 M positivo |
| **NPV 5 anos @ 13% (BR)** | R$ 6–14 M positivo |
| **TIR 5 anos** | 35–60% |

> **Observação**: Cenário P com utilização <30% **não vence API pública em compute puro**. O ROI vem de (a) horas economizadas, (b) controle de dados (não quantificado aqui), (c) custo evitado de SaaS por seat.

---

## 3. Cenário M — Médio (5.000 usuários ativos)

### 3.1 Perfil

- Empresa média/grande regulada (banco médio, varejo nacional, indústria global de porte médio, hospital de referência, estatal estadual).
- Casos cobertos: Chat 5k + RAG 100M tokens + Coding 500 devs + Atendimento 10k conv/dia + Sumarização 1k docs/dia.
- Topologia: ON-PREM 1 site + DR cloud privada, ou VPC dedicada multi-AZ.
- Referência de stack: **Perfil C (indústria) ou parte do Perfil A (banco T1 médio)**.

### 3.2 Investimento (CAPEX, ano 0)

| Item | Faixa US$ | Faixa BR R$ |
|------|-----------|--------------|
| Hardware (Etapa 4 §02 — agregado M) | 1,5–2,8 M | 7,5–14,0 M |
| +30% rede/storage/SW/implantação | 0,45–0,84 M | 2,25–4,2 M |
| **CAPEX total ano 0** | **1,95–3,64 M** | **9,75–18,2 M** |

### 3.3 OPEX anual (ano 1+)

| Item | US$/ano | R$/ano |
|------|---------|--------|
| Energia (60–100 kW × 24/365 × 1,4 PUE) | 70–130k | 350–650k |
| Suporte HW + SW (15–18% CAPEX HW) | 270–500k | 1,35–2,5 M |
| Equipe (8–10 FTE) | 950–1.350k | 2,5–3,8 M |
| Co-location (opcional, se sem DC próprio) | 150–300k | 750–1.500k |
| Manutenção / fine-tune / evals / red team | 100–200k | 500–1.000k |
| Atualizações de modelo (egress, mirror) | 30–60k | 150–300k |
| **OPEX total** | **1,57–2,54 M** | **5,6–9,75 M** |

### 3.4 Comparação com API pública (mesmo volume)

- Volume M ≈ **170 M tokens/dia** (chat 36M + RAG 50M + atend 96M + coding 21M + sum 9,5M; abate sobreposição ≈ 170M efetivo) ≈ **62 bilhões tokens/ano**.
- API pública GPT-4o blended (US$ 4/1M): **US$ 248 M/ano** (proibitivo).
- API pública Claude Sonnet/Mistral Large blended (US$ 2,5/1M): **US$ 155 M/ano**.
- API pública Bedrock/Haiku/Llama70B-on-Bedrock blended (US$ 0,6/1M): **US$ 37 M/ano**.
- On-prem (US$ 0,20/1M efetivo, com utilização >40%): **US$ 12,4 M/ano em compute** — coerente com OPEX listado.
- **Vantagem on-prem em compute (vs Bedrock-low-tier)**: ~3×. **Vs GPT-4o**: 20×.

### 3.5 Benefícios anuais quantificados

| Benefício | Cálculo | Estimativa US$/ano | BR R$/ano |
|-----------|---------|--------------------|------------|
| Tempo chat (5.000 × 60% × 3h × 46sem × US$32) | — | **13,2 M** | 66 M |
| Coding (500 × 70% × 20% cycle time × US$80k) | — | 5,6 M | 28 M |
| Atendimento (10k conv/dia × 30% deflect × 365 × US$5) | — | 5,5 M | 27 M |
| Sumarização (1k docs/dia × 365 × 1h economizada × US$32) | — | 11,7 M | 58 M |
| Custo evitado SaaS (Copilot 60% × 5k × US$30/m × 12) | — | 1,1 M | 5,5 M |
| Custo evitado API (vs Bedrock-low blended US$0,6/1M) | — | 25–35 M | 125–175 M |
| **Total estimativa conservadora (sem somar all)** | — | **~25–40 M** | **~125–200 M** |
| **Total estimativa-ponto** (com correlação 0,5) | — | **8–14 M** | **40–70 M** |

> **Conservador**: aplicamos correlação parcial (0,5) entre benefícios para evitar dupla contagem (chat + atendimento se sobrepõem em parte; coding + cycle-time idem). Faixa publicada na proposta usa o valor conservador.

### 3.6 Resultado consolidado M

| Métrica | Valor |
|---------|-------|
| CAPEX total ano 0 | US$ 1,95–3,64 M |
| OPEX anual médio | US$ 2,0 M |
| Benefício anual estimado | **US$ 8–14 M** (conservador) |
| **Payback estimado** | **8–14 meses** |
| **NPV 5 anos @ 8% (US)** | US$ 23–47 M positivo |
| **NPV 5 anos @ 13% (BR)** | R$ 90–200 M positivo |
| **TIR 5 anos** | 130–280% |

> Esta faixa coloca o Cenário M no mesmo perfil de retorno declarado por **JPMorgan (US$1–2 bi/ano em escala 230k usuários)**: ~US$ 4–9k de valor anual por usuário ativo. O Cenário M usa **US$ 1.600–2.800/usuário ativo** — coerente com BBVA (3h/sem × salário ES médio).

---

## 4. Cenário G — Grande (50.000 usuários ativos)

### 4.1 Perfil

- Empresa grande T1 (banco T1 BR/US, varejista global, indústria multinacional, estatal nacional).
- Casos cobertos: portfólio completo dos 14 casos da Etapa 1, com escala nominal.
- Topologia: ON-PREM 2 sites ativo-ativo, DR cloud privada, mirror HF próprio.
- Referência de stack: **Perfil A (banco T1) ou E (órgão público grande)**.

### 4.2 Investimento (CAPEX, ano 0)

| Item | Faixa US$ | Faixa BR R$ |
|------|-----------|--------------|
| Hardware (Etapa 4 §02 — agregado G) | 8–18 M | 40–90 M |
| +30% rede/storage/SW/implantação | 2,4–5,4 M | 12–27 M |
| **CAPEX total ano 0** | **10,4–24,3 M** (~US$ 17 M ponto médio) | **52–117 M** |

> Para referência: **Bradesco/IBM** declarou ~R$ 400 M de investimento em IA — consistente com o porte G+, faixa alta, em horizonte de 3 anos somando produto e plataforma.

### 4.3 OPEX anual (ano 1+)

| Item | US$/ano | R$/ano |
|------|---------|--------|
| Energia (350–600 kW × 24/365 × 1,4 PUE) | 410–700k | 2,0–3,5 M |
| Suporte HW + SW (15–18% CAPEX HW) | 1,4–2,9 M | 7–14,5 M |
| Equipe (25–40 FTE) | 3,5–6,0 M | 9–15 M |
| DR cloud privada (Azure Local / Outposts) | 0,8–1,5 M | 4–7,5 M |
| Manutenção / fine-tune / red team / certificação ISO | 0,4–0,8 M | 2–4 M |
| Updates / mirror / Artifactory enterprise | 0,1–0,2 M | 0,5–1 M |
| **OPEX total** | **6,6–12,1 M** | **24,5–45,5 M** |

### 4.4 Comparação com API pública (mesmo volume)

- Volume G ≈ **1,8 B tokens/dia** (chat 360M + atend 960M + coding 210M + sum 95M + RAG 200M, com abate de overlap).
- ≈ **657 bilhões tokens/ano**.
- API pública GPT-4o (US$ 4/1M): **US$ 2,6 bi/ano** (impraticável).
- API pública blended low-tier (US$ 0,6/1M): **US$ 394 M/ano**.
- On-prem (US$ 0,15/1M, utilização >50%): **US$ 99 M/ano** em compute — abaixo do OPEX listado (porque OPEX inclui equipe e DR).
- **Vantagem on-prem vs blended low-tier**: ~4×. Vantagem vs GPT-4o-only: ~25×. Mesmo após CAPEX, vence.

### 4.5 Benefícios anuais quantificados

| Benefício | Cálculo | Estimativa US$/ano | BR R$/ano |
|-----------|---------|--------------------|------------|
| Tempo chat (50.000 × 60% × 3h × 46sem × US$32) | — | **132 M** | 660 M |
| Coding (5.000 × 70% × 20% cycle × US$80k) | — | 56 M | 280 M |
| Atendimento (100k conv/dia × 30% × 365 × US$5) | — | 55 M | 275 M |
| Sumarização (10k docs/dia × 365 × 1h × US$32) | — | 117 M | 585 M |
| Custo evitado SaaS (Copilot 60% × 50k × US$360/ano) | — | 11 M | 55 M |
| Custo evitado API blended-low | — | 350 M | 1.750 M |
| **Total estimativa-ponto (correlação 0,4)** | — | **80–180 M** | **400–900 M** |

> JPMorgan declara **US$ 1,5–2,0 bi/ano** em valor para 230k usuários ≈ US$ 6,5–8,7k/usuário ativo. Nosso Cenário G usa **US$ 1,6–3,6k/usuário ativo** — consistente, conservador.

### 4.6 Resultado consolidado G

| Métrica | Valor |
|---------|-------|
| CAPEX total ano 0 | US$ 10,4–24,3 M |
| OPEX anual médio | US$ 9 M |
| Benefício anual estimado | **US$ 80–180 M** |
| **Payback estimado** | **6–12 meses** |
| **NPV 5 anos @ 8% (US)** | US$ 280–680 M positivo |
| **NPV 5 anos @ 13% (BR)** | R$ 1,0–2,8 bi positivo |
| **TIR 5 anos** | >300% |

---

## 5. Sensibilidade — variáveis críticas

### 5.1 Sensibilidade no Cenário M

Variáveis ordenadas por impacto no NPV 5 anos:

| Variável | -1σ → benefício | base → benefício | +1σ → benefício |
|----------|-----------------|-------------------|------------------|
| **Adoção (% ativos)** | 40% → US$ 6 M | 60% → US$ 11 M | 80% → US$ 15 M |
| **Horas economizadas/sem** | 2h → US$ 7 M | 3h → US$ 11 M | 6h → US$ 22 M |
| **Custo-hora médio** | US$ 22 → US$ 8 M | US$ 32 → US$ 11 M | US$ 65 → US$ 22 M |
| **Utilização GPU** (afeta vantagem vs API) | 20% → break-even tarda 6m | 40% → base | 70% → payback −3m |
| **CAPEX HW (faixa Etapa 4)** | -20% → NPV +3 M | base | +20% → NPV −3 M |

### 5.2 Cenários estressados

| Cenário | Premissas | Payback | NPV 5a |
|---------|-----------|---------|--------|
| **Pessimista M** | adoção 40%, 2h economizadas, utilização 25%, CAPEX +20% | 22–30 meses | levemente positivo |
| **Base M** | adoção 60%, 3h, utilização 40% | 8–14 meses | US$ 23–47 M |
| **Otimista M** | adoção 80%, 5h, utilização 60% | 4–7 meses | US$ 80–150 M |

> **Conclusão de sensibilidade**: **Adoção** e **horas economizadas** são as variáveis dominantes. Hardware barateando 20% muda pouco; utilização GPU baixa demora o payback mas não quebra o caso. **Subdimensionar a equipe de adoção é o maior risco financeiro**, não o hardware.

---

## 6. Tratamento qualitativo (não somado ao NPV acima)

| Benefício qualitativo | Notas |
|-----------------------|-------|
| **Risco de vazamento de dados evitado** | Custo médio de breach corporativo 2025 (IBM Security): US$ 4,88 M; 35% dos breaches em 2024 envolveram shadow AI. Evitar 1 incidente em 5 anos cobre ~30% do CAPEX M. |
| **Soberania regulatória** | Alinhamento LGPD Art. 7º X / Art. 11; GDPR Art. 28; ISO 42001 (Granite 4); EU AI Act high-risk para casos críticos. Reduz risco regulatório (multas LGPD até R$ 50 M/infração). |
| **Lock-in evitado** | Multi-modelo desde dia 1; substituir LLM em horas vs meses. |
| **Atratividade de talento** | Engenharia interna em LLM é diferencial em retenção sênior; relatos qualitativos JPMorgan/Goldman. |
| **Dado proprietário como ativo** | Embeddings do corpus + fine-tunes ficam na empresa — viram vantagem competitiva acumulada. |

---

## 7. Resumo executivo das 3 faixas

| Cenário | Usuários | CAPEX (HW + 30%) | OPEX/ano | Benefício/ano | Payback | NPV 5a (US$) |
|---------|----------|-------------------|----------|----------------|---------|---------------|
| **P** | 500 | US$ 0,33–0,59 M | US$ 0,55 M | US$ 0,9–1,5 M | 10–15 meses | 1,7–3,5 M |
| **M** | 5.000 | US$ 1,95–3,64 M | US$ 2,0 M | US$ 8–14 M | 8–14 meses | 23–47 M |
| **G** | 50.000 | US$ 10,4–24,3 M | US$ 9 M | US$ 80–180 M | 6–12 meses | 280–680 M |

> **Mensagem-chave para CFO**: O ROI cresce de forma **superlinear com escala** porque (a) hardware é compartilhado entre casos e tenants; (b) custo marginal por token cai com utilização; (c) benefícios são lineares em usuários × horas economizadas, mas overhead de equipe é **sublinear**. Cenário G entrega 25× mais NPV/CAPEX que Cenário P pelo mesmo motivo que JPMorgan declara US$ 1,5–2,0 bi/ano e empresas pequenas declaram quick wins.

---

## 8. Métricas para acompanhar (gate mês 5 → mês 12)

| Métrica | Meta gate mês 5 | Meta produção mês 12 |
|---------|------------------|------------------------|
| Adoção DAU/MAU dos elegíveis | ≥40% | ≥60% |
| Horas economizadas/usuário/semana (auto-relatada + medida) | ≥1,5h | ≥3h |
| Utilização efetiva GPU | ≥25% | ≥40% |
| Custo/1M tokens efetivo (on-prem) | ≤US$ 0,40 | ≤US$ 0,25 |
| TTFT p50 chat | ≤1,2s | ≤0,8s |
| Cache hit rate (semantic + KV) | ≥15% | ≥30% |
| NPS interno | ≥40 | ≥60 |
| Tickets desviados (atendimento) | n/a | ≥25% |
| Cycle time dev (coding) | n/a | -15% |

---

## 9. Fontes consultadas

- Etapa 1 §00 (resumo casos de uso)
- Etapa 2 §11 (licenças)
- Etapa 3 §00 (tabela mestre 34 empresas), §01 (financeiro), §08 (stacks arquetípicas), §09 (lições)
- Etapa 4 §02 (dimensionamento), §09 (energia)
- Stripe / vLLM (–73% custo)
- JPMorgan Tearsheet
- BBVA case (3h/semana, 87k usuários)
- IBM Security Cost of a Data Breach 2025
- ANPD multas LGPD (referência)
