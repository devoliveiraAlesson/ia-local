# Equipe e Orçamento — Headcount por Porte e Custo BR/US

> Etapa 5/5. Documento de planejamento de RH e orçamento. Para CFO, CIO, RH, controladoria. Maio/2026.
>
> Premissas de salário totalmente carregado: ver §1 abaixo. Câmbio R$ 5,00/US$ 1,00.

## 1. Premissas de remuneração (totalmente carregado)

| Papel | BR R$/mês carregado | BR R$/ano | US US$/ano (TC inclusive benefits) |
|-------|---------------------|------------|-----------------------------------|
| Sponsor executivo (parcial 10–20%) | n/a (já no payroll) | — | — |
| Tech Lead / Arquiteto LLM | 50–70k | 600–840k | 220–300k |
| ML Engineer sênior | 30–45k | 360–540k | 180–240k |
| ML Engineer pleno | 20–30k | 240–360k | 130–170k |
| SRE / Platform Engineer | 25–40k | 300–480k | 160–220k |
| Data Engineer / RAG specialist | 22–32k | 264–384k | 140–190k |
| Segurança / Compliance | 25–35k | 300–420k | 150–200k |
| DPO (parcial 30%) | n/a | parcial | parcial |
| Product Owner por caso | 18–28k | 216–336k | 130–170k |
| DevEx engineer (Fase 2) | 25–35k | 300–420k | 150–200k |
| MLOps / Operações IA | 22–32k | 264–384k | 140–190k |
| UX / Comms / Treinamento (parcial) | 12–20k | 144–240k | 80–110k |
| Agent platform engineer (Fase 4) | 30–45k | 360–540k | 180–240k |

> **Nota**: salários BR refletem o mercado de São Paulo / Rio para empresa grande regulada. Para empresas no interior ou setor público, ajustar -20–30%. **Salários totalmente carregados** incluem encargos (~80% no BR, ~30% nos EUA).

---

## 2. Headcount por porte

### 2.1 Cenário P (Pequeno — 500 usuários)

| Papel | FTE | Notas |
|-------|-----|-------|
| Sponsor executivo | 0,2 | C-level com 1 dia/sem |
| Tech Lead / Arquiteto LLM | 1,0 | obrigatório |
| ML Engineer | 1,0 | pode acumular RAG inicialmente |
| SRE / Platform | 0,5 | compartilhado com TI tradicional |
| Data Engineer / RAG | 0,5 | pode ser consultoria |
| Segurança/Compliance | 0,3 | parcial |
| DPO | 0,2 | parcial |
| PO Caso 1 (chat) | 0,5 | parcial |
| **Total FTE** | **~4,2** | + consultoria contratada |

| Item | BR R$/ano | US US$/ano |
|------|-----------|-------------|
| Equipe interna (4,2 FTE) | 1,8–2,4 M | 700–950k |
| Consultoria implantação (Red Hat / NVIDIA / parceiro) ano 1 | 0,3–0,5 M | 100–200k |
| Treinamento equipe (3 cursos × 2 pax) | 60–100k | 20–35k |
| **Total equipe ano 1** | **2,2–3,0 M** | **820–1.185k** |

### 2.2 Cenário M (Médio — 5.000 usuários)

| Papel | FTE | Notas |
|-------|-----|-------|
| Sponsor executivo | 0,2 | |
| Tech Lead / Arquiteto LLM | 1,0 | |
| ML Engineer sênior | 1,0 | |
| ML Engineer pleno | 1,5 | crescimento progressivo |
| SRE / Platform | 1,5 | 24/7 light |
| Data Engineer / RAG | 1,0 | |
| Segurança/Compliance | 0,5 | |
| DPO | 0,3 | parcial |
| PO Caso 1 (chat) | 1,0 | |
| PO Caso 3 (RAG) | 0,5 | |
| DevEx engineer (Fase 2+) | 1,0 | a partir mês 5 |
| MLOps / Operações IA | 0,5 | |
| UX / Comms / Treinamento | 0,5 | |
| **Total FTE** | **~10,0** | |

| Item | BR R$/ano | US US$/ano |
|------|-----------|-------------|
| Equipe interna (10 FTE) | 3,5–5,0 M | 1,5–2,1 M |
| Consultoria implantação ano 1 | 0,5–1,0 M | 200–400k |
| Suporte/treinamento ano 1 | 0,2–0,3 M | 80–120k |
| **Total equipe ano 1** | **4,2–6,3 M** | **1,78–2,62 M** |

### 2.3 Cenário G (Grande — 50.000 usuários)

| Papel | FTE | Notas |
|-------|-----|-------|
| Sponsor executivo | 0,3 | |
| Tech Lead / Arquiteto LLM | 1,0 | |
| Vice Tech Lead / Engineering Manager | 1,0 | escalar gestão |
| ML Engineer sênior | 3,0 | |
| ML Engineer pleno | 4,0 | |
| ML Researcher / fine-tune (Fase 4) | 1,0 | |
| SRE / Platform | 4,0 | 24/7 pleno |
| Data Engineer / RAG | 3,0 | |
| Segurança/Compliance | 2,0 | |
| DPO | 0,5 | |
| Red team / IA adversarial | 0,5 | |
| PO Caso 1 + 3 + 4 + 2 | 4,0 | 1 PO por caso P0 |
| DevEx engineer | 2,0 | suportar 5k devs |
| MLOps / Operações IA | 2,0 | |
| Agent platform engineer | 1,0 | Fase 4 |
| UX / Comms / Treinamento | 1,5 | |
| Compliance/ISO 42001 lead | 0,5 | |
| **Total FTE** | **~31** | (faixa 25–40) |

| Item | BR R$/ano | US US$/ano |
|------|-----------|-------------|
| Equipe interna (31 FTE) | 11,0–15,5 M | 4,7–6,3 M |
| Consultoria contínua (Red Hat / NVIDIA / IBM / Big4) | 1,5–2,5 M | 600–1.000k |
| Treinamento equipe + certificações | 0,4–0,7 M | 150–250k |
| **Total equipe ano 1** | **12,9–18,7 M** | **5,45–7,55 M** |

---

## 3. Tabela consolidada — equipe + custo anual

| Porte | FTE total | BR R$/ano (faixa) | US US$/ano (faixa) | Coerência |
|-------|-----------|-------------------|---------------------|-----------|
| **P** | 4–5 | 2,2–3,0 M | 0,82–1,18 M | Time mínimo viável; consultoria essencial |
| **M** | 8–12 | 4,2–6,3 M | 1,78–2,62 M | Operação 24/7 light |
| **G** | 25–40 | 12,9–18,7 M | 5,45–7,55 M | Operação 24/7 pleno; multi-time |

> Para referência comparativa: **JPMorgan LLM Suite** equipe central estimada >100 FTE em 2025 (não publicado em detalhe); **BBVA** declarou 1.000+ data scientists em ecossistema (escopo amplo, não só LLM); **Bradesco/IBM** R$ 400 M de investimento ao longo de anos (cobre HW + serviços + equipe). Os números acima são consistentes com a janela de portes M e G observada.

---

## 4. Curva de contratação ao longo de 12 meses (Cenário M)

| Mês | FTE acumulada | Quem entra | Por quê |
|-----|----------------|------------|---------|
| 0 | 1 | Sponsor (parcial) | Patrocínio |
| 1 | 3 | Tech Lead + 1 SRE + 0,5 sec | Decisões arquiteturais e contratação de hardware |
| 2 | 5 | + 1 ML Eng + 0,5 Data Eng + 0,5 DPO | Stack base |
| 3 | 7 | + 1 SRE + 1 Data Eng + 0,5 PO chat | Plataforma em build |
| 4 | 8 | + 1 ML Eng pleno | Capacidade Fase 1 |
| 5 | 9 | + 0,5 PO RAG + 0,5 UX | GA Fase 1 + gate |
| 6 | 10 | + 1 DevEx (Fase 2) | Coding |
| 8 | 11 | + 1 ML Eng pleno (Fase 3) | Atendimento |
| 10 | 12 | + 0,5 MLOps + 0,5 Operações | Sustentação |

> Curva similar para G (ajustar fator 3×) e P (fator 0,4×).

---

## 5. Make-vs-buy de capacidade

| Capacidade | Make (interno) | Buy (consultoria/parceiro) | Recomendação |
|-----------|-----------------|------------------------------|---------------|
| Tech leadership | 100% interno | — | Make |
| Plataforma K8s/vLLM operação | 70% | 30% Red Hat / NVIDIA PS no setup | Híbrido |
| Pipeline RAG / ingestão | 80% | 20% consultoria especializada | Híbrido |
| Fine-tuning (LoRA/InstructLab) | 50% | 50% Red Hat AI / IBM Watsonx | Buy/Make conforme volume |
| Segurança IA / red team | 60% | 40% (HackerOne / Lakera / Trail of Bits) | Híbrido |
| ISO 42001 / DPIA | 50% | 50% Big4 | Híbrido |
| Compliance jurídica de modelos | 30% | 70% jurídico interno + escritório especializado | Buy |
| UX / treinamento | 70% | 30% agência | Híbrido |

---

## 6. Orçamento total ano 1 — visão consolidada (Cenário M)

> Usar como template; replicar para P (×0,4) e G (×3,5).

| Bloco | BR R$/ano (faixa) | US US$/ano (faixa) |
|-------|-------------------|---------------------|
| **CAPEX hardware (ano 0)** | 7,5–14,0 M | 1,5–2,8 M |
| **CAPEX +30% (rede/storage/SW/impl.)** | 2,25–4,2 M | 0,45–0,84 M |
| **OPEX equipe ano 1** | 4,2–6,3 M | 1,78–2,62 M |
| **OPEX energia** | 350–650k | 70–130k |
| **OPEX suporte HW/SW** | 1,35–2,5 M | 270–500k |
| **OPEX co-location (se aplicável)** | 0,75–1,5 M | 150–300k |
| **OPEX manutenção/fine-tune/red team** | 500–1.000k | 100–200k |
| **OPEX atualizações / mirror** | 150–300k | 30–60k |
| **TOTAL ANO 1** | **17–30 M** | **4,4–7,5 M** |
| **TOTAL ANOS 2–5** (ajuste -CAPEX +inflação) | 8–12 M/ano | 2,5–3,5 M/ano |

---

## 7. Riscos de RH (cross-link com `05-riscos-mitigacao.md`)

| Risco | Mitigação |
|-------|-----------|
| Tech Lead não contratado a tempo | Interim via Red Hat/IBM PS por 3–6 meses |
| Mercado BR de ML eng aquecido | Senioridade sênior + ações + remoto BR-wide |
| Saída de pessoa-chave | Documentação obrigatória; rotação interna; pair work |
| Burnout em time pequeno (P) | Consultoria pesada nos primeiros 6 meses; on-call só após GA |
| Skill gap em segurança IA | OWASP LLM training; certificações Trail of Bits / SANS |

---

## 8. Plano de capacitação (todos portes)

| Trilha | Módulos | Frequência |
|--------|---------|-------------|
| **Tech Lead / Arquiteto** | Red Hat OpenShift AI, NVIDIA AI Enterprise, vLLM internals | 1×/ano (5 dias cada) |
| **ML Engineer** | InstructLab + Granite, LangGraph + DSPy, Ragas evals | 2×/ano (3 dias cada) |
| **SRE/Platform** | KServe, GPU operator, IB/RoCE tuning, DCGM | 1×/ano (5 dias) |
| **Segurança** | OWASP LLM 2025, Lakera, Trail of Bits AI red team | 1×/ano (3 dias) |
| **PO/Negócio** | Workshop "como medir ROI de IA", BBVA/JPMorgan playbook | 2×/ano (1 dia) |
| **End-users (campeões)** | Boas práticas prompt + governança de uso | trimestral |

---

## 9. Fontes

- Salários: pesquisas Robert Half BR/US 2025-2026, mercado SP/SF/NYC ML.
- Estrutura de equipe: heurística destilada da Etapa 3 §08 (perfis arquetípicos) e §09 (lições aprendidas).
- Templates Red Hat AI Practice / IBM Watsonx / NVIDIA Professional Services.
