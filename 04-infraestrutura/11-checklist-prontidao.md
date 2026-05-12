# Checklist de Prontidão — Pré-Projeto IA Local

> Etapa 4/5 da proposta. Checklist concreto para a empresa preencher **antes** de iniciar o projeto. Cada bloco com critérios objetivos. Ideal: gate executivo formal antes de aprovar CAPEX.

## Como usar

- Marcar cada item como **OK** (X), **Parcial** (~), **Não** (—).
- Itens **bloqueadores** estão em negrito — sem eles, o projeto não deve iniciar.
- Itens recomendados são "nice to have" — viáveis com mitigação documentada.

---

## A. Casos de uso e patrocínio (alinhamento com Etapa 1)

- [ ] Caso(s) prioritário(s) identificado(s) — chat / RAG / coding / atendimento / sumarização
- [ ] **Patrocinador executivo nomeado (C-level + diretor de área)**
- [ ] Sucesso definido: KPIs específicos (NPS, tickets reduzidos, tempo de resposta, etc.)
- [ ] Baseline atual medido (status quo sem IA)
- [ ] **Volume estimado de tokens/dia ou usuários ativos**
- [ ] Sensibilidade dos dados classificada (público/interno/restrito/PII/PHI)
- [ ] Regulação aplicável mapeada (LGPD/HIPAA/GDPR/SOX/PCI/setoriais)
- [ ] Decisão de quais casos são P0 (etapa 1) vs P1/P2

## B. Arquitetura e tecnologia (alinhamento com Etapa 2)

- [ ] **Modelo(s) candidato(s) escolhido(s)** com licença validada (Llama vs Granite vs Qwen, evitar Codestral comercial)
- [ ] Runtime de inferência escolhido (vLLM padrão; SGLang se RAG-pesado)
- [ ] Vector store escolhido (Qdrant default; pgvector se < 10M vetores; Milvus se > 100M)
- [ ] Frontend escolhido (Open WebUI / LibreChat / AnythingLLM / custom)
- [ ] Gateway escolhido (LiteLLM padrão; Kong AI se já há Kong)
- [ ] Guardrails baseline definido (Llama Guard 3 + Presidio)
- [ ] Observabilidade definida (Prometheus + Langfuse + OTel GenAI)
- [ ] **Multi-modelo desde dia 1** (pelo menos 2 modelos via gateway)

## C. Hardware e fornecedor

- [ ] **Quantidade de GPUs aprovada com base em dimensionamento (Etapa 4 §02)**
- [ ] Modelo de GPU definido (H100/H200 default; B200 se DC já preparado; MI300X se anti-lock-in)
- [ ] **Cotação obtida** (Dell, Supermicro, Lenovo, HPE, NVIDIA direct)
- [ ] Lead time confirmado por escrito
- [ ] Contrato master de fornecimento (proteção contra mudança de preço)
- [ ] Suporte enterprise contratado (NVIDIA AI Enterprise, ROCm Enterprise, ou via OEM)
- [ ] Segunda fonte considerada (1 nó AMD MI300X ou similar)

## D. Data center e energia (alinhamento com Etapa 4 §09)

- [ ] **kW/rack disponível** medido e suficiente (≥30 kW p/ HGX H100; ≥50 kW p/ B200)
- [ ] Capacidade elétrica total disponível para crescer 12 meses
- [ ] **Cooling adequado** (ar reforçado / RDHx / DLC conforme densidade)
- [ ] **Tier do DC ≥ III**
- [ ] Espaço físico (U-rack) disponível com folga
- [ ] PUE atual conhecido (alvo < 1,4)
- [ ] Co-location avaliada como alternativa
- [ ] Logística para entrega de servidores 60–100 kg planejada

## E. Rede (alinhamento com Etapa 4 §03)

- [ ] **Bandwidth interna entre nós GPU adequada** (200G mínimo p/ multi-nó)
- [ ] **Storage acessível em alta velocidade** (100G+ se Weka/VAST)
- [ ] Rede de gerenciamento (BMC/IPMI) isolada
- [ ] VLANs separadas (data, storage, management)
- [ ] Latência cliente↔gateway aceitável (alvo <30ms p/ chat interno)
- [ ] Egress para mirror HF e Update Servers, com allow-list

## F. Storage (alinhamento com Etapa 4 §04)

- [ ] **NVMe local denso** em cada servidor GPU (≥15 TB)
- [ ] Storage de objeto on-prem (MinIO / Ceph / equivalente) provisionado
- [ ] Storage paralelo decidido (Weka/VAST/GPFS) se necessário (Cenário M+)
- [ ] **Mirror HF Hub local** definido (HF Enterprise, JFrog, Nexus, MinIO)
- [ ] Container registry on-prem (Harbor) com Cosign
- [ ] **WORM storage para logs regulados** definido

## G. Identidade e acesso (alinhamento com Etapa 4 §06)

- [ ] **IdP corporativo escolhido** (Keycloak / Entra ID / Okta) com OIDC/SAML
- [ ] **MFA obrigatória** habilitada
- [ ] Grupos AD/LDAP refletindo perfis de uso
- [ ] RBAC mapeado (quem usa qual modelo, qual quota)
- [ ] Service accounts via SPIFFE/SPIRE ou equivalente

## H. Segurança e compliance

- [ ] **DPO/encarregado** envolvido (LGPD)
- [ ] **DPIA / RIPD** iniciada para casos de alto risco
- [ ] BAA assinado com fornecedores (HIPAA — quando aplicável)
- [ ] Política de retenção de prompts/respostas formalizada
- [ ] **OWASP LLM Top 10 2025** revisado e endereçado
- [ ] Pipeline de promoção de modelo (scan + aprovação) definido
- [ ] Plano de incidente de IA (vazamento/jailbreak/poisoning) documentado
- [ ] ISO 42001 considerada como meta (2026–2027)

## I. Equipe (gaps típicos)

- [ ] **Líder técnico de IA Platform** nomeado
- [ ] SRE / DevOps Kubernetes (1+ FTE)
- [ ] ML Engineer (1+ FTE)
- [ ] Data Engineer / RAG specialist (0,5–1 FTE)
- [ ] Security/Compliance buddy (0,5 FTE)
- [ ] Contrato de consultoria temporária se gaps (Red Hat / NVIDIA Professional Services / parceiro local)
- [ ] Plano de treinamento para times consumidores

## J. Orçamento e governança financeira

- [ ] **CAPEX aprovado com folga 15–25%**
- [ ] OPEX aprovado para 3 anos (energia + suporte + pessoas + licenças)
- [ ] Modelo de chargeback/showback definido entre áreas
- [ ] FinOps habilitado (Langfuse cost tracking + Prometheus + tags)
- [ ] **Gate de mid-life** previsto (revisão de hardware em 2 anos)

## K. Cronograma realista (referência)

| Fase | Duração | Marcos |
|------|---------|--------|
| Pré-projeto / business case | 1–2 meses | Aprovação executiva, RFP |
| Aquisição de hardware | 2–4 meses | Lead time GPU + entrega |
| Retrofit DC (se necessário) | 3–6 meses | DLC, elétrica, cooling |
| Plataforma base (K8s, KServe, vLLM, Qdrant) | 1–2 meses | Smoke test |
| Caso 1 — Chat interno em piloto | 1 mês | 50–500 usuários |
| Caso 1 — Chat interno produção | 1 mês | rollout corporativo |
| Caso 2 — RAG corporativo | 2 meses | indexação + RAG |
| Caso 3 — Coding assistant | 1 mês | distribuição IDE |
| Hardening + observabilidade plena | contínuo | dashboards, evals |
| **Total para "P0 todo em produção"** | **9–12 meses** | |

## L. Critérios de "go-live" para cada caso

- [ ] SLOs definidos (latência, disponibilidade, eval)
- [ ] Smoke test e load test passados
- [ ] Pelo menos 1 GameDay de DR realizado
- [ ] Runbooks publicados
- [ ] Treinamento dos usuários final
- [ ] Comunicação corporativa preparada
- [ ] On-call definido com cobertura 24/7 (ou modelo proporcional ao SLO)
- [ ] Métricas de negócio sendo coletadas

---

## Decisões executivas pendentes (encaminhar a Etapa 5)

| Decisão | Caminho A | Caminho B | Quando decidir |
|---------|-----------|-----------|----------------|
| **NVIDIA puro vs NVIDIA + AMD** | Mais simples, ROCm-skill desnecessário | Anti-lock-in, custo melhor por GB de HBM, exige skill | Antes da cotação |
| **Kubernetes vanilla vs OpenShift AI** | Flexibilidade, menor custo | Suporte enterprise + Granite + InstructLab + ISO 42001 friendly | Antes da arquitetura final |
| **On-prem puro vs híbrido** | Soberania máxima | Picos em cloud + DR em cloud privada | Antes da arquitetura final |
| **DC próprio (retrofit) vs co-location** | Custo total menor em 5+ anos | Time-to-market 4–8 semanas; menos risco | Antes da aquisição |
| **DLC obrigatório?** | Apenas se Blackwell (B200/GB200) | RDHx + ar suficiente para H100/H200 | Junto do dimensionamento |
| **Modelo principal: Llama vs Granite vs Qwen** | Llama 3.3 70B (mainstream) | Granite 4 (Apache 2.0 + ISO 42001) ou Qwen 2.5 (Apache 2.0 + multilíngue) | Antes do início do POC |
| **Frontend: Open WebUI vs custom** | Time-to-market | Marca + UX corporativa | Após POC |
| **Modelo de operação: time interno vs MSP / GreenLake** | Capacidade interna long term | Velocidade, OPEX previsível | Antes do orçamento |

---

## Critérios de "no-go" (sinais para adiar projeto)

- DC corporativo NÃO comporta nem 30 kW/rack e não há orçamento de retrofit + co-location.
- Equipe interna sem **nenhum SRE/Kubernetes** + sem orçamento de consultoria.
- Volume estimado < 200k tokens/dia (cloud privada com BAA é provavelmente mais barata).
- Patrocinador executivo ausente ou tíbio.
- Casos de uso vagos ("queremos fazer IA").
- Compliance obrigatório (LGPD/HIPAA) sem DPO definido.
- Lead time de GPU + retrofit DC > 12 meses sem mitigação cloud-bridge.

## Resumo: matriz de prontidão

| Bloco | Bloqueadores | Score esperado para go-live |
|-------|--------------|------------------------------|
| A. Casos e patrocínio | 100% | 100% |
| B. Tecnologia | 80% | 90% |
| C. Hardware | 100% | 100% |
| D. DC e energia | 100% | 100% |
| E. Rede | 80% | 90% |
| F. Storage | 80% | 90% |
| G. Identidade | 100% | 100% |
| H. Segurança e compliance | 90% | 100% |
| I. Equipe | 70% | 90% |
| J. Orçamento | 100% | 100% |

Empresas que entram em produção com >85% médio têm **3–5× menos chance** de incidente operacional grave nos primeiros 6 meses (heurística baseada em casos públicos da Etapa 3).
