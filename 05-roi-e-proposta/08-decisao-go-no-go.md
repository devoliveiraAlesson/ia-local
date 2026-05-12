# Decisão Go/No-Go — Checklist Consolidado

> Etapa 5/5. Documento de governança e decisão. Para Sponsor, CIO, CFO, CISO, DPO, comitê de IA. Maio/2026.
>
> Este documento consolida (a) decisão executiva inicial — autorizar Fase 0+1; (b) gate Go/No-Go do mês 5 — autorizar Fases 2–4. Cada checklist é objetivo: verde / amarelo / vermelho.

---

## 1. Decisão executiva inicial (mês 0)

### 1.1 Pré-condições para iniciar Fase 0

| # | Pré-condição | Status (preencher) |
|---|---------------|---------------------|
| 1 | Sponsor executivo nomeado (C-level com 0,2 FTE comprometido) | [ ] OK [ ] ~ [ ] — |
| 2 | Comitê de IA constituído (CIO + CFO + CISO + DPO + Sponsor) | [ ] OK [ ] ~ [ ] — |
| 3 | Caso(s) prioritário(s) decidido(s) — Caso 1 + Caso 3 (mínimo) | [ ] OK [ ] ~ [ ] — |
| 4 | Volume estimado de tokens/dia ou usuários ativos | [ ] OK [ ] ~ [ ] — |
| 5 | Sensibilidade dos dados classificada | [ ] OK [ ] ~ [ ] — |
| 6 | Regulação aplicável mapeada (LGPD/HIPAA/GDPR/setoriais) | [ ] OK [ ] ~ [ ] — |
| 7 | Orçamento Fase 0+1 aprovado pelo CFO (ver §1.3) | [ ] OK [ ] ~ [ ] — |
| 8 | DPO engajado e ciente de DPIAs futuras | [ ] OK [ ] ~ [ ] — |
| 9 | Tech Lead/Arquiteto LLM em busca ativa (RH) | [ ] OK [ ] ~ [ ] — |
| 10 | Cenário (P/M/G) escolhido | [ ] OK [ ] ~ [ ] — |

> **Critério**: 9/10 itens verdes para iniciar. Itens vermelhos são bloqueadores.

### 1.2 Decisões pedidas ao board agora

| # | Decisão | Recomendação | CAPEX/OPEX requerido na decisão |
|---|---------|--------------|----------------------------------|
| 1 | Aprovar **Fase 0 + Fase 1** (5 meses) | **Sim** | P: US$ 0,2 M / M: US$ 0,8–1,2 M / G: US$ 4–6 M (valores parciais Fase 0+1) |
| 2 | Aprovar **pré-cotação de GPU** com lead time ≥ 16 sem | **Sim** | sem desembolso até PO emitido |
| 3 | Nomear **Sponsor Executivo + Tech Lead/Arquiteto LLM** | **Sim** | sem CAPEX (folha) |
| 4 | Marcar **gate de mid-life para mês 5** (Go/No-Go Fases 2–4) | **Sim** | sem desembolso até gate |
| 5 | Aprovar contrato de **consultoria** (Red Hat / NVIDIA / IBM ou parceiro local) | **Sim** | P: US$ 0,1–0,2 M / M: US$ 0,2–0,4 M / G: US$ 0,6–1,0 M ano 1 |
| 6 | Aprovar **multi-modelo desde dia 1** (Llama + Granite + Qwen mínimo) | **Sim** | dentro do CAPEX HW |
| 7 | Aprovar **stack open-source** (vLLM + Qdrant + LiteLLM + Open WebUI/LibreChat + Llama Guard 3 + Langfuse) | **Sim** | sem licença comercial obrigatória |

### 1.3 Orçamento Fase 0+1 (visão executiva)

| Cenário | CAPEX Fase 0+1 | OPEX Fase 0+1 (5 meses) | Total Fase 0+1 |
|---------|-----------------|---------------------------|------------------|
| **P** | US$ 200–350k | US$ 200–300k | **US$ 0,4–0,65 M** |
| **M** | US$ 800k–1,2 M | US$ 600–900k | **US$ 1,4–2,1 M** |
| **G** | US$ 4–6 M | US$ 2–3 M | **US$ 6–9 M** |

> **Observação**: o board aprova hoje **Fase 0+1**, não o CAPEX completo do Cenário escolhido. Decisão Fases 2–4 fica para o gate do mês 5.

### 1.4 Critérios de "no-go" inicial (sinais para adiar)

- DC corporativo NÃO comporta nem 30 kW/rack e não há orçamento de retrofit + co-location.
- Equipe interna sem **nenhum SRE/Kubernetes** + sem orçamento de consultoria.
- Volume estimado < 200k tokens/dia (cloud privada com BAA é provavelmente mais barata).
- Patrocinador executivo ausente ou tíbio.
- Casos de uso vagos ("queremos fazer IA").
- Compliance obrigatório (LGPD/HIPAA) sem DPO definido.
- Lead time de GPU + retrofit DC > 12 meses sem mitigação cloud-bridge.

---

## 2. Checklist de prontidão (Fase 0 → Fase 1) — gate intermediário (mês 2)

> Este checklist replica/sintetiza Etapa 4 §11. Ver lá para detalhe.

### A. Casos e patrocínio

- [ ] Casos P0 confirmados (Caso 1 + Caso 3 mínimo)
- [ ] **Patrocinador executivo nomeado**
- [ ] KPIs específicos definidos (NPS, TTFT, custo/1M tokens, adoção, etc.)
- [ ] Baseline atual medido (status quo sem IA)

### B. Tecnologia

- [ ] **Modelo(s) candidato(s) escolhido(s)** com licença validada
- [ ] Runtime escolhido (vLLM padrão; SGLang se RAG-pesado)
- [ ] Vector store escolhido (Qdrant default)
- [ ] Frontend escolhido (Open WebUI / LibreChat / AnythingLLM)
- [ ] Gateway escolhido (LiteLLM padrão; Kong AI se já há Kong)
- [ ] Guardrails baseline definido (Llama Guard 3 + Presidio)
- [ ] Observabilidade definida (Prometheus + Langfuse + OTel GenAI)

### C. Hardware

- [ ] **Quantidade de GPUs aprovada** com base em dimensionamento (Etapa 4 §02)
- [ ] Modelo de GPU definido
- [ ] **Cotação obtida** (mín. 2 OEMs)
- [ ] Lead time confirmado por escrito
- [ ] Suporte enterprise contratado
- [ ] Segunda fonte considerada (1 nó AMD ou Intel Gaudi 3)

### D. DC e energia

- [ ] **kW/rack disponível** medido e suficiente
- [ ] Capacidade elétrica total para 12 meses
- [ ] **Cooling adequado**
- [ ] **Tier do DC ≥ III**
- [ ] PUE alvo < 1,4

### E. Rede

- [ ] Bandwidth interna entre nós GPU adequada (200G mínimo)
- [ ] Storage acessível em alta velocidade (100G+)
- [ ] VLANs separadas (data, storage, management)
- [ ] Egress controlado para mirror HF

### F. Storage

- [ ] NVMe local ≥ 15 TB por servidor GPU
- [ ] Object store on-prem provisionado (MinIO/Ceph)
- [ ] Mirror HF Hub local definido
- [ ] WORM storage para logs regulados definido

### G. Identidade

- [ ] **IdP corporativo escolhido** (OIDC/SAML)
- [ ] **MFA obrigatória**
- [ ] Grupos AD/LDAP refletindo perfis
- [ ] RBAC mapeado

### H. Segurança e compliance

- [ ] **DPO/encarregado** envolvido (LGPD)
- [ ] **DPIA / RIPD** iniciada para casos de alto risco
- [ ] Política de retenção de prompts/respostas formalizada
- [ ] **OWASP LLM Top 10 2025** revisado
- [ ] Plano de incidente de IA documentado

### I. Equipe

- [ ] **Tech Lead/Arquiteto LLM** nomeado
- [ ] SRE (1+ FTE)
- [ ] ML Engineer (1+ FTE)
- [ ] Data Engineer (0,5–1 FTE)
- [ ] Security/Compliance (0,5 FTE)
- [ ] Plano de treinamento

### J. Orçamento

- [ ] **CAPEX aprovado com folga 15–25%**
- [ ] OPEX aprovado para 3 anos
- [ ] Modelo de chargeback/showback definido
- [ ] FinOps habilitado dia 1 (Langfuse cost + Prometheus + tags)

> **Critério gate Fase 0 → Fase 1**: ≥85% médio dos blocos. Bloqueadores em vermelho impedem início.

---

## 3. Gate Go/No-Go (mês 5) — Fases 2–4

### 3.1 Métricas que devem ser batidas

| Métrica | Meta | Status |
|---------|------|--------|
| Adoção (% elegíveis ativos no chat) | ≥ 40% | [ ] |
| DAU/MAU | ≥ 0,5 | [ ] |
| TTFT p50 chat | ≤ 1,2s | [ ] |
| Latência p99 RAG | ≤ 3s | [ ] |
| Cache hit (semantic + KV) | ≥ 15% | [ ] |
| Utilização efetiva GPU | ≥ 25% | [ ] |
| NPS interno | ≥ 40 | [ ] |
| Custo/1M tokens efetivo | ≤ US$ 0,40 | [ ] |
| Incidentes de segurança críticos | 0 | [ ] |
| DPIA aceita pelo DPO (Caso 1 + Caso 3) | OK | [ ] |
| Eval automatizada Ragas faithfulness | ≥ 0,75 | [ ] |
| Auditoria interna sem findings críticos | OK | [ ] |

> **Critério Go pleno**: ≥80% das metas batidas. Adoção e custo são bloqueadores.

### 3.2 Saídas possíveis do gate

| Saída | Quando aplicar | Próximo passo |
|-------|-----------------|----------------|
| **Go pleno** | ≥80% metas + sem incidente crítico | Aprovar Fases 2 + 3 |
| **Go condicional** | 60–80% metas, ou 1 área de preocupação isolada | Avançar Fase 2 (coding); adiar Fase 3 (atendimento) por 2 meses; novo gate mês 7 |
| **Recalibrar** | <60% metas mas plataforma estável | Manter Fase 1; investir 2–3 meses em adoção e UX antes de novos casos |
| **No-Go (raro)** | Incidente crítico, custos explodidos, regulador interveio | Pausar expansão; manter Fase 1 em produção; reavaliar em 6 meses |

### 3.3 Quem decide

- **Comitê formal**: Sponsor executivo + CFO + CIO + CISO + DPO.
- **Recomendação técnica**: Tech Lead com dashboard de métricas objetivas.
- **Quórum**: 4/5 voto favorável para Go pleno.
- **Documentação**: ata formal + dashboard exportado + decisão registrada.

---

## 4. Decisões pendentes a serem fechadas em Fase 0

> Cross-link com Etapa 4 §11 §"Decisões executivas pendentes".

| Decisão | Caminho A | Caminho B | Decisão registrada |
|---------|-----------|-----------|---------------------|
| **NVIDIA puro vs NVIDIA + AMD/Intel** | Mais simples, ROCm/Gaudi-skill desnecessário | Anti-lock-in, custo melhor por GB de HBM | [ ] A [ ] B |
| **Kubernetes vanilla vs OpenShift AI** | Flexibilidade, menor custo | Suporte enterprise + Granite + InstructLab + ISO 42001 friendly | [ ] A [ ] B |
| **On-prem puro vs híbrido** | Soberania máxima | Picos em cloud + DR em cloud privada | [ ] A [ ] B |
| **DC próprio (retrofit) vs co-location** | Custo total menor em 5+ anos | Time-to-market 4–8 semanas; menos risco | [ ] A [ ] B |
| **DLC obrigatório?** | Apenas se Blackwell | RDHx + ar suficiente para H100/H200 | [ ] A [ ] B |
| **Modelo principal** | Llama 3.3 70B (mainstream) | Granite 4 (Apache 2.0 + ISO 42001) ou Qwen 3 (Apache 2.0) | [ ] A [ ] B |
| **Frontend** | Open WebUI (time-to-market) | Custom (marca + UX) | [ ] A [ ] B |
| **Modelo de operação** | Time interno full | MSP / GreenLake / parceiro | [ ] A [ ] B |

---

## 5. Critérios de "go-live" para cada caso

> Aplicado a cada caso individualmente (Caso 1, Caso 3, Caso 4, Caso 2, Caso 6, Caso 7, ...).

- [ ] SLOs definidos (latência, disponibilidade, eval)
- [ ] Smoke test e load test passados
- [ ] Pelo menos 1 GameDay de DR realizado
- [ ] Runbooks publicados
- [ ] Treinamento dos usuários final
- [ ] Comunicação corporativa preparada
- [ ] On-call definido (24/7 ou modelo proporcional ao SLO)
- [ ] Métricas de negócio sendo coletadas
- [ ] DPIA aceita (para casos de alto risco)
- [ ] Humano-na-curva configurado nos primeiros 60 dias (cliente-facing)
- [ ] Auditoria interna OK
- [ ] Eval baseline (Ragas + Promptfoo) passou

---

## 6. Roteiro de aprovação (governança)

```
[Mês 0]  Apresentação ao board (slides §06)
   │
   ├─[Aprovação Fase 0+1] ──▶ Sponsor + Tech Lead + RFP HW + DPO
   │                                │
   │                          [Mês 2 — gate prontidão §2]
   │                                │
   │                          ≥85% verde? ──▶ Sim ──▶ Fase 1
   │                                                       │
   │                                                 [Mês 5 — gate §3]
   │                                                       │
   │                                              ≥80% metas?
   │                                                       │
   │                              ┌────────────┬───────────┼────────────┬────────────┐
   │                              │            │           │            │            │
   │                            Go pleno  Go condic.  Recalibrar      No-Go        │
   │                              │            │           │                        │
   │                            Fase 2+3   Fase 2 só  Manter Fase 1                 │
   │
   └─[Não aprovado] ──▶ Adiamento documentado + revisão em 6 meses
```

---

## 7. Templates de comunicação

### 7.1 Aprovação executiva (modelo de ata)

> "Em [data], o Comitê de IA composto por [nomes/cargos] aprovou:
> - Fase 0 + Fase 1 da plataforma de IA local on-premises
> - Orçamento Fase 0+1: [US$/R$] consolidado
> - Sponsor executivo nomeado: [nome]
> - Tech Lead/Arquiteto LLM em recrutamento prioritário
> - Pré-cotação de hardware autorizada em 3 OEMs (Dell, Supermicro, Lenovo/HPE)
> - Gate Go/No-Go programado para [data mês 5]
> - Stack tecnológica: vLLM + Qdrant + LiteLLM + Open WebUI/LibreChat + Llama Guard 3 + Langfuse
> - Multi-modelo aprovado: Llama 3.3 + Granite 4 + Qwen 3 (mínimo)
> A próxima revisão executiva ocorrerá em [data] com dados reais de adoção, custo, latência e satisfação dos Casos 1 e 3."

### 7.2 Comunicação aos colaboradores (kick-off mês 0)

> "A empresa está investindo em uma plataforma de IA corporativa segura, dentro do nosso perímetro, para [fins definidos: produtividade, atendimento, qualidade de software]. Os primeiros casos serão Chat interno seguro e RAG corporativo, em produção até o mês 5. Garantimos que nenhum dado sensível sairá do nosso controle. Convidamos áreas a se candidatar como campeãs/pilotos."

---

## 8. Resumo

- **Hoje**: aprovar Fase 0+1 (US$ 0,4–9 M conforme porte). Sem comprometer CAPEX completo do Cenário.
- **Mês 2**: gate de prontidão (Etapa 4 §11). ≥85% verde para entrar Fase 1.
- **Mês 5**: gate Go/No-Go Fases 2–4. ≥80% das 12 métricas batidas.
- **Mês 12**: revisão anual de ROI; decisão sobre Fase 4 (fine-tune, agentes, multimodal).

> A decisão é **faseada por desenho**. Cada gate **adiciona informação real** antes do próximo CAPEX. Esta estrutura é adotada por JPMorgan, Itaú e Bradesco — não é exceção, é a melhor prática do setor.

---

## Fontes

- Etapa 4 §11 (checklist completo de prontidão)
- `01-modelo-roi-cenarios.md` §8 (métricas para acompanhar)
- `03-roadmap-12-meses.md` §4 (gate mid-life)
- `05-riscos-mitigacao.md` (todos os 16 riscos)
