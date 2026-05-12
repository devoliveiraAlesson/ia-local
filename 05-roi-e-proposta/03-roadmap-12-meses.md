# Roadmap de Implantação — 12 meses + Fase 4 (mês 12+)

> Etapa 5/5. Documento de planejamento. Para PMO, sponsor executivo, tech lead, RH, compras. Maio/2026.
>
> Referência cruzada: roadmap detalhado por caso na Etapa 1; cronograma de prontidão na Etapa 4 §11.

## 1. Visão geral em uma página

```
Mês:  0─1─2─3─4─5─6─7─8─9─10─11─12─[18]
Fase 0 ████      Prontidão (DC, identidade, equipe, orçamento, RFP)
Fase 1     ███████   Chat interno + RAG + plataforma + observabilidade + guardrails
                    ▲ Gate Go/No-Go (mês 5) — APROVA Fases 2–4
Fase 2          ████████   Coding assistant + Code review
Fase 3                ██████   Atendimento + Sumarização + Extração
Fase 4                       ▶▶ InstructLab fine-tune, agentes, multimodal
```

| Fase | Mês | Foco | Casos (Etapa 1) | Decisão | Entregável-chave |
|------|-----|------|-----------------|---------|------------------|
| **0** | 0–2 | Prontidão | — | Go Fase 1 | Checklist Etapa 4 §11 ≥ 85%; PO de GPU emitido |
| **1** | 2–5 | Plataforma + Quick win | 1 (chat) + 3 (RAG) | **Gate mid-life mês 5** | 500–5k usuários ativos no chat; 1 corpus RAG produção |
| **2** | 5–8 | Engenharia | 4 (coding) + 5 (code review) | Go expansão devs | 70% adoção devs ativos; -15% cycle time |
| **3** | 8–12 | Cliente + Back-office | 2 (atend) + 6 (sum) + 7 (extração) | Go ano 2 | Atendimento 30% deflect; 1k docs/dia sumarização |
| **4** | 12+ | Avançado | 8–14 + agentes + multimodal + FT | — | InstructLab fine-tune; agentes governados |

---

## 2. Fase 0 — Prontidão (mês 0–2)

### Objetivo
Sair do mês 2 com hardware encomendado, equipe nuclear contratada, DC pronto, segurança/compliance alinhada e arquitetura desenhada.

### Atividades-chave

| # | Atividade | Resp | Mês |
|---|-----------|------|-----|
| 0.1 | Sponsor executivo nomeado + comitê de IA criado | CEO | 0 |
| 0.2 | Tech Lead / Arquiteto LLM contratado | CIO | 0–1 |
| 0.3 | Workshop com áreas — priorizar P0/P1 | Tech Lead | 1 |
| 0.4 | RFP de hardware (Dell/Supermicro/Lenovo/HPE) | Compras | 1 |
| 0.5 | Cotação concluída + PO emitido | Compras + CFO | 2 |
| 0.6 | DPO/encarregado engajado; DPIA iniciada para Casos 1, 2, 3 | DPO | 1–2 |
| 0.7 | Identity provider integração planejada (Keycloak/Entra ID) | SecOps | 1–2 |
| 0.8 | DC ou co-location decidido; retrofit elétrico/cooling iniciado | Facilities | 1–2 |
| 0.9 | Stack tecnológica fechada (decisões da Etapa 4 §11 §"Decisões") | Tech Lead | 1–2 |
| 0.10 | Plano de cloud-bridge (VPC ponte) caso lead time > 16 sem | Tech Lead + CFO | 2 |

### Entregáveis Fase 0

- Checklist Etapa 4 §11 com ≥85% itens verdes.
- Hardware encomendado com lead time confirmado.
- Equipe nuclear (4–6 FTE) contratada ou alocada.
- DPIA dos casos P0 iniciada.
- Documento de arquitetura aprovado pelo comitê.

### Métricas Fase 0
- Tempo até PO emitido: ≤ 8 semanas.
- % checklist verde: ≥ 85%.
- FTE alocadas: ≥ 4.

### GPUs envolvidas
- Nenhuma em produção. Cloud-bridge opcional (8× H100 em VPC) para Fase 1 enquanto on-prem é construído.

### Equipe Fase 0
- 1× Sponsor executivo
- 1× Tech Lead / Arquiteto LLM
- 1× SRE/Platform
- 0,5× Segurança/Compliance
- 0,5× DPO
- 0,5× Compras

---

## 3. Fase 1 — Chat interno + RAG + Plataforma (mês 2–5)

### Objetivo
Entregar o quick win (Caso 1) e a plataforma habilitadora (Caso 3 RAG) simultaneamente, com observabilidade e guardrails desde o dia 1. Provar o ROI **antes do gate Go/No-Go do mês 5**.

### Atividades-chave

| # | Atividade | Resp | Mês |
|---|-----------|------|-----|
| 1.1 | Cluster K8s/OpenShift AI provisionado | SRE | 2–3 |
| 1.2 | vLLM + Llama 3.3 70B AWQ + Qwen 2.5 72B em staging | ML Eng | 3 |
| 1.3 | Gateway LiteLLM + RBAC + quotas + semantic cache | Platform | 3 |
| 1.4 | Llama Guard 3 8B + Presidio + WORM logs | Security | 3–4 |
| 1.5 | Open WebUI (ou LibreChat) com SSO Keycloak/Entra | Platform | 3–4 |
| 1.6 | Qdrant cluster + BGE-M3 embedding + reranker BGE | ML Eng | 3–4 |
| 1.7 | Pipeline de ingestão RAG (corpus piloto: políticas + manuais) | Data Eng | 3–4 |
| 1.8 | Observabilidade (Prometheus + Grafana + DCGM + Langfuse + OTel GenAI) | Platform | 3–5 |
| 1.9 | Pilot 50 → 500 → 5.000 usuários (rolagem por área) | PO + Tech Lead | 4–5 |
| 1.10 | Evals contínuas (Ragas + DeepEval + Promptfoo) | ML Eng | 4–5 |
| 1.11 | Comunicação corporativa + treinamento (campeões por área) | Comms + RH | 4–5 |

### Entregáveis Fase 1

- Plataforma comum em produção: vLLM + Qdrant + LiteLLM + Open WebUI + Llama Guard + Langfuse.
- Caso 1 (Chat interno) em produção para 500 (P) / 5.000 (M) / 50.000 (G) usuários.
- Caso 3 (RAG) ao menos 1 corpus em produção (políticas internas + 1 vertical de área).
- Observabilidade end-to-end com retenção de prompts conforme política.
- DPIA concluída para Casos 1 e 3.

### Métricas Fase 1 (gate mês 5)

| Métrica | Meta gate |
|---------|-----------|
| Adoção (% elegíveis ativos no chat) | ≥ 40% |
| DAU/MAU | ≥ 0,5 |
| TTFT p50 chat | ≤ 1,2s |
| Latência p99 RAG | ≤ 3s |
| Cache hit (semantic + KV) | ≥ 15% |
| Utilização efetiva GPU | ≥ 25% |
| NPS interno | ≥ 40 |
| Custo/1M tokens efetivo | ≤ US$ 0,40 |
| Incidentes de segurança (vazamento/jailbreak) | 0 críticos |

### GPUs Fase 1

| Porte | GPUs |
|-------|------|
| P | 2× L40S 48GB ou 1× H100 NVL |
| M | 8× H100 SXM (1 servidor HGX) + 1× L40S (embedding) |
| G | 32× H200 (4 servidores HGX) + 4× L40S (embedding/rerank) + canary 20% |

### Equipe Fase 1 acrescida
- +1× ML Engineer
- +1× Data Engineer / RAG specialist
- +1× SRE
- +1× PO Caso 1 (chat)
- +0,5× UX/Comms
- +0,5× Treinamento

### Risco principal
- Lead time de GPU > 16 semanas → mitigação via cloud-bridge VPC.

---

## 4. Gate Mid-Life (mês 5) — Go/No-Go Fases 2–4

### Critérios de aprovação
- Métricas Fase 1 batidas (≥80% das metas).
- DPIA aceita pelo DPO.
- Sem incidente de segurança crítico.
- Custo/1M tokens efetivo dentro do budget.

### Saídas possíveis
1. **Go pleno**: aprovar Fases 2 + 3 conforme planejado.
2. **Go condicional**: avançar Fase 2 (coding), adiar Fase 3 (atendimento) por 2 meses.
3. **Recalibrar**: melhorar adoção do Caso 1 antes de novos casos; revisar arquitetura.
4. **No-Go**: parar expansão; manter Fase 1 em produção; reavaliar em 6 meses.

### Quem decide
- Sponsor executivo + CFO + CIO + CISO + DPO em comitê formal.
- Recomendação técnica do Tech Lead com dados objetivos.

---

## 5. Fase 2 — Coding assistant + Code review (mês 5–8)

### Objetivo
Acelerar engenharia interna com coding assistant local + code review automatizado, mantendo IP de código no perímetro.

### Atividades-chave

| # | Atividade | Resp | Mês |
|---|-----------|------|-----|
| 2.1 | Qwen2.5-Coder-32B AWQ em vLLM dedicado | ML Eng | 5–6 |
| 2.2 | Tabby para autocomplete FIM nos IDEs | Platform | 6 |
| 2.3 | Continue.dev para chat IDE (compartilhando modelo de chat) | Platform | 6 |
| 2.4 | Integração GitLab Duo Self-Hosted ou Gitea AI (code review CI) | Platform + DevEx | 6–7 |
| 2.5 | Qwen3-Coder-Next 80B (MoE 3B ativos) para chat IDE escalável | ML Eng | 7 |
| 2.6 | Pilot 50 → 500 devs | DevEx + PO | 6–8 |
| 2.7 | Métricas DORA + cycle time + acceptance rate | DevEx | 7–8 |

### Entregáveis
- Caso 4 (Coding) em produção para 50 (P) / 500 (M) / 5.000 (G) devs.
- Caso 5 (Code review) em CI nos repos prioritários.
- Política de uso de Copilot/Codex externos sunset progressivo.

### Métricas Fase 2

| Métrica | Meta |
|---------|------|
| Devs ativos no Tabby/Continue | ≥ 70% |
| Acceptance rate de completions | ≥ 30% |
| Cycle time PR (CI → merge) | -15% vs baseline |
| Bugs encontrados no review automatizado / 100 PRs | rastreado |
| TTFT autocomplete | ≤ 200ms |

### GPUs Fase 2
- P: +1× H100 80GB (ou 2× L40S TP=2)
- M: +4× H100 SXM (servidor 4-GPU dedicado)
- G: +16× H100/H200 (2 servidores HGX)

### Equipe Fase 2 acrescida
- +1× DevEx engineer (PO de coding)
- Reuso da equipe ML Eng / Platform / SRE existente.

---

## 6. Fase 3 — Atendimento + Sumarização + Extração (mês 8–12)

### Objetivo
Implantar casos cliente-facing (atendimento) e back-office (sumarização, extração) sobre a plataforma já provada.

### Atividades-chave

| # | Atividade | Resp | Mês |
|---|-----------|------|-----|
| 3.1 | Modelo "raciocínio" (DeepSeek-R1 distill 32B ou Qwen 3 reasoning) para casos escalados | ML Eng | 8 |
| 3.2 | Llama Guard 3 8B reforçado + Presidio + system prompt cliente-facing | Security | 8–9 |
| 3.3 | Integração CRM/atendimento (Genesys/Salesforce/legado) via webhooks | Integration | 8–10 |
| 3.4 | RAG de FAQs + base de conhecimento de produto | Data Eng | 8–9 |
| 3.5 | Pipeline batch de sumarização (jurídico, contratos, atas) | Data Eng | 9–10 |
| 3.6 | Pipeline de extração estruturada (faturas, prontuários, formulários) | Data Eng | 10–11 |
| 3.7 | Humano-na-curva em outputs cliente-facing primeiros 60 dias | Operações | 10–11 |
| 3.8 | Soft launch 1.000 → 10.000 conv/dia (M) / 100k (G) | PO atendimento | 11–12 |

### Entregáveis
- Caso 2 (Atendimento) em produção com humano-na-curva → autonomia gradual.
- Caso 6 (Sumarização) em batch noturno + on-demand.
- Caso 7 (Extração estruturada) integrado a back-office.
- WORM logs com retenção 24+ meses para casos cliente-facing.

### Métricas Fase 3

| Métrica | Meta |
|---------|------|
| Tickets desviados (atendimento) | ≥ 25% |
| CSAT atendimento IA | ≥ 75% |
| Latência p95 atendimento | ≤ 4s |
| Sumarização — qualidade revisada por humano | ≥ 90% aceitação |
| Extração — F1 vs gold dataset | ≥ 0,90 |
| Audit trail completo (% requests com user/session/model id) | 100% |

### GPUs Fase 3
- P: +2× H100 80GB
- M: +8× H100 SXM
- G: +32× H200 / 24× B200

### Equipe Fase 3 acrescida
- +1× PO atendimento (negócio)
- +1× ML Engineer (raciocínio + pipelines batch)
- +1× Operações (humano-na-curva)
- +0,5× Compliance (auditoria de outputs)

---

## 7. Fase 4 — InstructLab fine-tune, agentes, multimodal (mês 12+)

### Objetivo
Sair do uso "RAG + prompt engineering" e começar a customização explícita (fine-tune leve, agentes governados, multimodal nativo).

### Atividades-chave

| # | Atividade |
|---|-----------|
| 4.1 | InstructLab + Granite 4 para terminologia interna (jurídico, médico, industrial) — taxonomia + skills |
| 4.2 | LoRA/QLoRA opcional para casos com dataset > 5k exemplos curados |
| 4.3 | Agentes governados (LangGraph + DSPy) para back-office multi-step |
| 4.4 | Multimodal: Pixtral 12B / Qwen 3-VL para PDFs com layout, formulários, diagramas |
| 4.5 | Avaliação ISO 42001 piloto (com Granite 4 já compatível) |
| 4.6 | Casos 8–14 da Etapa 1 (tradução, docs técnicos, logs, compliance, treinamento, pareceres, e-mails) ativados conforme demanda |

### Entregáveis Fase 4
- 1+ modelo fine-tuned em produção com ganho mensurável (≥3% em métrica do caso).
- 1+ agente em produção governado (com kill-switch, eval contínua, humano-na-curva).
- Multimodal: 1 caso documental ativo.
- Roadmap ISO 42001 (formalização 2027).

### Métricas Fase 4
- Cost-quality trade-off do fine-tune (vs base model) documentado.
- Erros operacionais de agente / 1k execuções.
- % outputs multimodal com citação/grounding.

### GPUs Fase 4
- Reuso do parque + 1–2 nós dedicados a treino (1 nó 4–8× H100 com NVLink, ou batch off-peak no cluster G).

### Equipe Fase 4 acrescida
- +0,5× ML Researcher / fine-tune specialist (consultoria Red Hat / IBM se necessário)
- +0,5× Agent platform engineer
- +0,5× Compliance/ISO 42001 lead

---

## 8. Marcos de comunicação corporativa

| Marco | Mês | Audiência | Conteúdo |
|-------|-----|-----------|----------|
| **Kick-off interno** | 0 | Toda empresa | "Vamos construir IA segura corporativa" |
| **Aviso DPO/jurídico** | 1 | Áreas reguladas | DPIA + retenção + opt-in |
| **Beta restrito Caso 1** | 4 | 50–500 champions | Convite + treinamento |
| **GA Caso 1** | 5 | Toda empresa elegível | Lançamento + tutorial |
| **Showcase mid-life** | 5 | Board | Resultados Fase 1 + decisão Fases 2–4 |
| **GA Coding** | 8 | Engenharia | Tabby/Continue + treinamento DevEx |
| **Beta Atendimento** | 10 | Operações + sample clientes | Humano-na-curva ativo |
| **GA Atendimento** | 12 | Toda área | Comunicação cliente externa também |
| **Anual review** | 12 | Board | ROI medido vs estimado |

---

## 9. Dependências críticas no caminho crítico

1. **PO de hardware antes do mês 2** — sem isto, Fase 1 atrasa em proporção 1:1.
2. **Tech Lead/Arquiteto contratado antes do mês 1** — sem isto, decisões de arquitetura ficam reativas.
3. **DPIA aceita antes do beta Fase 1 (mês 4)** — sem isto, não há produção em saúde/financeiro.
4. **DC com kW/rack adequado antes do mês 4** — sem isto, GPUs ficam encaixotadas.
5. **Identity provider corporativo antes do mês 3** — sem SSO, não há multi-tenant.
6. **Mirror HF + Artifactory antes do mês 3** — sem isto, modelo travado em supply chain.

---

## 10. Sumário executivo do roadmap

- **Mês 0–2** (Fase 0): prontidão. CAPEX comitê aprovado, hardware encomendado, equipe nuclear ativa.
- **Mês 2–5** (Fase 1): plataforma + chat + RAG. Quick win mensurável.
- **Mês 5** (Gate): board decide Fases 2–4 com dados reais.
- **Mês 5–8** (Fase 2): coding assistant. ROI rápido em engenharia.
- **Mês 8–12** (Fase 3): atendimento + sumarização + extração. ROI cliente-facing + back-office.
- **Mês 12+** (Fase 4): fine-tune, agentes, multimodal — diferenciação competitiva.

> **Princípio**: cada fase precede a próxima por **dependência de dados**, não por preferência. Não pular Fase 1 (a plataforma é habilitadora). Não fazer atendimento (Fase 3) antes de provar o RAG (Fase 1).

---

## 11. Fontes / referências cruzadas

- Etapa 1 §00 (sequenciamento dos 14 casos)
- Etapa 4 §11 (checklist de prontidão e cronograma de 9–12 meses)
- Etapa 3 §08 (perfis arquetípicos e velocidade de implantação observada)
- Etapa 3 §09 (lições — campeões por área, vertical > genérico)
