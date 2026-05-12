# Riscos e Mitigação — Proposta IA Local On-Premises

> Etapa 5/5. Documento de risco e governança. Para CISO, DPO, controladoria, comitê de risco. Maio/2026.
>
> Riscos ordenados por prioridade decrescente (probabilidade × impacto). Cada risco tem: descrição, gatilhos observáveis, mitigação pré-incidente, mitigação durante incidente, dono.

## Matriz resumo (16 riscos)

| # | Risco | Categoria | Prob. | Impacto | Severidade |
|---|-------|-----------|-------|---------|------------|
| 1 | Lead time de GPU > 16 semanas | Operacional | Alta | Alto | **Crítico** |
| 2 | Equipe insuficiente / dificuldade contratação | Pessoas | Alta | Alto | **Crítico** |
| 3 | Subdimensionamento de utilização (<30% GPU) | Financeiro | Média | Alto | Alto |
| 4 | Adoção baixa pelos usuários | Adoção | Média | Alto | Alto |
| 5 | Vazamento de PII em logs / SIEM | Segurança | Média | Crítico | **Crítico** |
| 6 | Compliance LGPD/HIPAA/EU AI Act inadequado | Regulatório | Média | Crítico | **Crítico** |
| 7 | Hallucination em saída regulada | Qualidade | Alta | Alto | Alto |
| 8 | Drift / queda silenciosa de qualidade | Qualidade | Alta | Médio | Médio |
| 9 | Lock-in de fornecedor (HW ou modelo) | Estratégico | Média | Médio | Médio |
| 10 | Supply chain de modelos comprometida | Segurança | Baixa | Crítico | Médio |
| 11 | Energia / cooling / DC inadequado | Físico | Média | Alto | Alto |
| 12 | Custo OPEX explode (sub-tier energia, suporte) | Financeiro | Média | Médio | Médio |
| 13 | Prompt injection / jailbreak em produção | Segurança | Alta | Médio-Alto | Alto |
| 14 | ACL ausente no retrieval (OWASP LLM08) | Segurança | Alta | Crítico | **Crítico** |
| 15 | Licença de modelo violada (Llama 700M MAU, Codestral MNPL) | Jurídico | Baixa | Alto | Médio |
| 16 | Sponsor executivo sai / muda prioridade | Político | Média | Crítico | **Crítico** |

---

## R1. Lead time de GPU > 16 semanas

**Descrição**: H100/H200 ainda têm lead time 12–24 semanas; B200 16–32 semanas; alocação por OEM pode atrasar a Fase 0.

**Gatilhos**: PO emitido sem confirmação por escrito; OEM responde com "alocação trimestral".

**Mitigação pré**:
- Cotar 2 OEMs simultaneamente (Dell + Supermicro / Lenovo + HPE).
- Considerar **AMD MI300X** ou **Intel Gaudi 3** como segunda fonte.
- Negociar contrato master com SLA de entrega.
- **Cloud-bridge VPC ponte** (8× H100 em VPC dedicada) para iniciar Fase 1 enquanto on-prem é construído.

**Mitigação durante**: ativar cloud-bridge; renegociar prioridade com OEM; usar L40S como gap-filler (entrega mais rápida).

**Dono**: Compras + Tech Lead.

---

## R2. Equipe insuficiente / dificuldade de contratação

**Descrição**: mercado BR/US de ML engineers e SREs com skill GPU está aquecido; risco de não contratar a tempo ou perder pessoa-chave.

**Gatilhos**: 2+ vagas abertas há >60 dias; saída do Tech Lead.

**Mitigação pré**:
- Contratar **Tech Lead antes do mês 1** (decisão crítica).
- Contrato com **Red Hat / NVIDIA / IBM Professional Services** ou parceiro local para os 6 primeiros meses.
- Plano de internalização explícito: cada FTE consultor tem um shadow interno.
- Salário-mercado + ações/PLR atraente.
- Documentação obrigatória; pair work; sem heroísmo.

**Mitigação durante**: ativar contrato de consultoria emergencial; recalibrar escopo (P em vez de M).

**Dono**: CIO + RH.

---

## R3. Subdimensionamento de utilização (<30% GPU)

**Descrição**: cluster on-prem com utilização <30% perde para API pública em custo total — ROI quebra.

**Gatilhos**: utilização média semanal <25% após mês 4; cache hit rate <10%.

**Mitigação pré**:
- **Multi-tenant lógico via gateway** desde o dia 1 (LiteLLM/Kong AI).
- **Semantic cache** ativo (Etapa 3 §09 — Stripe –73%).
- **Prefix-aware routing** (vLLM Production Stack ou llm-d) em vez de round-robin.
- Piso de utilização **30%** como critério de go-live; abaixo disso, recalibrar.
- Compartilhar GPUs entre casos (chat + sumarização batch noturno).

**Mitigação durante**: ativar mais casos sobre o mesmo cluster; ofertar para mais áreas internas; pausar expansão de hardware.

**Dono**: Tech Lead + FinOps.

---

## R4. Adoção baixa pelos usuários

**Descrição**: lançamento sem evangelização ativa → uso sobe e cai em 60 dias (anti-padrão E1 da Etapa 3 §09).

**Gatilhos**: DAU/MAU <0,3 após 60 dias do GA.

**Mitigação pré**:
- **Vertical, não genérico**: Connect Coach JPMorgan, Pair Noms Singapura — sempre fluxos contextualizados.
- **GenAI Championship Bosch-style**: competição interna; campeões por área.
- Treinamento + comunicação corporativa contínua.
- BBVA-style: 400+ funcionários submetendo casos; 20k GPTs custom.
- UX cuidadosa (Open WebUI default não basta para todos).

**Mitigação durante**: workshops por área; entrevistar usuários inativos; ajustar prompts pré-canned; mais campeões.

**Dono**: PO + UX/Comms.

---

## R5. Vazamento de PII em logs / SIEM (PHI, financeiro, código)

**Descrição**: prompts/respostas vazam para Datadog/Splunk SaaS ou Langfuse cloud — contradiz a soberania.

**Gatilhos**: logs em ferramenta externa; auditoria DPO encontra PII bruta.

**Mitigação pré**:
- **Presidio** na ingestão de observabilidade — PII sanitizada antes de log.
- **Langfuse self-host**, nunca Langfuse Cloud para empresa regulada.
- WORM logs com retenção por política (não eternos).
- DPIA cobre observabilidade.
- DLP no gateway para outputs.

**Mitigação durante**: incident response; comunicação ANPD se necessário (LGPD prazo 2 dias úteis); revisar política de retenção.

**Dono**: CISO + DPO.

---

## R6. Compliance LGPD/HIPAA/EU AI Act inadequado

**Descrição**: caso de alto risco posto em produção sem DPIA aprovada → multa LGPD até R$ 50 M/infração; bloqueio regulatório.

**Gatilhos**: caso 2 (atendimento) ou 11 (PII classification) em produção sem DPIA aceita.

**Mitigação pré**:
- DPO engajado desde a Fase 0.
- DPIA por caso; aceita antes de GA.
- Mapeamento OWASP LLM Top 10 2025 documentado.
- Contratos (DPA, BAA) com vendors de LLM externos (se híbrido).
- ISO 42001 como meta 2027 (Granite 4 já é ISO 42001 certificado, ajuda).
- Política de retenção, anonimização, opt-out.

**Mitigação durante**: pause go-live; reabrir DPIA; comunicar ANPD/regulador se necessário.

**Dono**: DPO + Jurídico + CISO.

---

## R7. Hallucination em saída regulada (jurídico, médico, financeiro)

**Descrição**: parecer com lei inexistente, diagnóstico errado, recomendação financeira errada.

**Gatilhos**: revisão humana encontra >5% de outputs com erro factual.

**Mitigação pré**:
- **RAG obrigatório** com citação ao documento fonte.
- **Groundedness check** (Ragas faithfulness, RAGAS context-precision).
- **Reranker** (BGE-reranker / Qwen3-Reranker) para precision.
- **Disclaimer obrigatório** em saídas reguladas.
- **Humano-na-curva** em outputs cliente-facing primeiros 60–90 dias.
- Evals contínuas (Promptfoo CI/CD).

**Mitigação durante**: rollback de modelo; reforço de prompt; auditoria humana mais densa.

**Dono**: ML Engineer + Compliance + PO do caso.

---

## R8. Drift / queda silenciosa de qualidade

**Descrição**: troca de modelo, mudança de prompt, atualização de RAG corpus → qualidade cai sem ninguém perceber.

**Gatilhos**: NPS cai >10 pontos; reclamação de usuários sobre "respostas piores".

**Mitigação pré**:
- **Ragas + DeepEval + Promptfoo** rodando como CI/CD.
- **Canary release** (gateway redireciona 5% para novo modelo, compara métricas).
- Eval set regenerado trimestralmente.
- Dashboard Langfuse com alerta de drift.

**Mitigação durante**: rollback; reabrir avaliação; ativar champions para feedback rápido.

**Dono**: ML Engineer + Tech Lead.

---

## R9. Lock-in de fornecedor (HW ou modelo)

**Descrição**: dependência forte de NVIDIA e/ou de um modelo (Llama) limita opções futuras.

**Gatilhos**: 100% NVIDIA + 100% Llama; sem nó AMD/Intel; sem segundo modelo no gateway.

**Mitigação pré**:
- **Multi-modelo desde dia 1** (Llama + Granite + Qwen via gateway).
- Considerar 1 nó AMD MI300X ou Intel Gaudi 3 como segunda fonte.
- Stack baseada em **padrões abertos**: K8s, OTel, OCI images, OpenAPI.
- vLLM > NIM (vLLM é open; NIM trava em NVIDIA AI Enterprise).
- Contrato com saída plausível.

**Mitigação durante**: testar alternativa em paralelo; trocar modelo via gateway sem mudar app.

**Dono**: Tech Lead + Compras.

---

## R10. Supply chain de modelos comprometida

**Descrição**: modelo baixado do Hugging Face com peso "envenenado" (poisoning) ou backdoor; CVE em vLLM.

**Gatilhos**: alerta de CVE; checksum diferente do publicado; comportamento estranho do modelo.

**Mitigação pré**:
- **Mirror HF Hub on-prem** (HF Enterprise, JFrog Artifactory, Sonatype Nexus, MinIO assinado).
- **Cosign** + hash checksum obrigatório.
- **ProtectAI Guardian** ou similar para scan de modelo.
- Container image scanning (Trivy, Grype) no pipeline CI.
- SBOM (Software Bill of Materials) por release.

**Mitigação durante**: rollback para checkpoint anterior; isolar modelo afetado; auditoria forense.

**Dono**: CISO + Platform Engineering.

---

## R11. Energia / cooling / DC inadequado

**Descrição**: rack <30 kW para HGX H100 ou <50 kW para B200; cooling de ar insuficiente; PUE alto.

**Gatilhos**: DC team relata throttling térmico; bills de energia explodem.

**Mitigação pré**:
- Etapa 4 §09 — kW/rack medido antes do PO.
- DLC obrigatório para Blackwell (B200/GB200); RDHx aceitável para H100.
- Co-location avaliada como alternativa antes de retrofit.
- Tier do DC ≥ III.

**Mitigação durante**: throttle de carga; mover carga para co-location; acelerar retrofit.

**Dono**: Facilities + Tech Lead.

---

## R12. Custo OPEX explode

**Descrição**: energia em tier mais caro; suporte premium não negociado; auto-scaling sem teto; consultoria não cap.

**Gatilhos**: OPEX > 130% do orçado em qualquer trimestre.

**Mitigação pré**:
- **FinOps habilitado dia 1**: Langfuse cost tracking + Prometheus + tags.
- Quotas via gateway (LiteLLM, Portkey).
- Auto-scaling com teto.
- Contrato de suporte negociado (não default).
- Energy contract com tier negociado.

**Mitigação durante**: cap quotas; pausar fine-tunes; renegociar contratos.

**Dono**: FinOps + CFO.

---

## R13. Prompt injection / jailbreak em produção

**Descrição**: usuário / documento RAG injeta instrução que faz o modelo executar ação não autorizada (especialmente em agentes).

**Gatilhos**: relato de "comportamento estranho"; auditoria descobre output inesperado.

**Mitigação pré**:
- **Defense in depth**: Llama Prompt Guard 2 + Llama Guard 3 + Presidio + system prompt + structured output.
- Agentes com **kill-switch** + step-by-step validation.
- Red team contratado anualmente (Trail of Bits / Lakera / HackerOne).
- OWASP LLM Top 10 2025 (especialmente LLM01 — Prompt Injection).

**Mitigação durante**: bloquear input pattern; pausar agente; reforço de guardrails.

**Dono**: CISO + ML Engineer.

---

## R14. ACL ausente no retrieval (OWASP LLM08)

**Descrição**: usuário recupera via RAG documento que não pode acessar diretamente — vetor é "topicamente similar" sem checagem de permissão.

**Gatilhos**: auditoria interna encontra usuário acessando dado fora do seu escopo via RAG.

**Mitigação pré**:
- **Filtros de ACL no retrieval** (Qdrant payload filters, Elastic security, Milvus partition keys).
- Replicar **mesma ACL** do sistema fonte.
- Multi-tenant lógico no vector store.
- Teste de penetração específico para RAG.

**Mitigação durante**: incident response; revogar índices afetados; reindex com ACL correta; comunicar DPO.

**Dono**: ML Engineer + CISO + DPO.

---

## R15. Licença de modelo violada

**Descrição**: usar **Codestral 22B/25.08** (MNPL — proibido em produção sem licença paga) ou ultrapassar **700M MAU Llama** sem licença Meta.

**Gatilhos**: jurídico identifica em auditoria; Meta envia notificação.

**Mitigação pré**:
- **Etapa 2 §11** revisada com jurídico antes do PoC.
- Para coding interno usar **Qwen 2.5/3-Coder, Granite-Code, DeepSeek-Coder V2 ou StarCoder 2** (não Codestral).
- Para grupos com >100M MAU consolidado, considerar **Granite (Apache 2.0)** ou **Qwen 3 (Apache 2.0)** em vez de Llama em fluxos cliente-facing.
- SBOM de modelos por release.

**Mitigação durante**: trocar modelo via gateway (sem mudar app); regularizar licença; comunicar jurídico.

**Dono**: Jurídico + Tech Lead.

---

## R16. Sponsor executivo sai / muda prioridade

**Descrição**: troca de C-level, mudança de prioridade estratégica → projeto perde patrocínio na metade.

**Gatilhos**: anúncio de saída do sponsor; revisão de portfólio corporativo.

**Mitigação pré**:
- Comitê de IA com **3+ stakeholders C-level** (CIO + CFO + COO + CISO), não 1 só.
- ROI documentado mês a mês com dashboard executivo.
- Vinculação a OKR/meta corporativa de longo prazo.
- Casos de uso com proprietário de negócio (não só TI).

**Mitigação durante**: re-engajar novo sponsor cedo; demonstrar ROI medido; ajustar narrativa.

**Dono**: Tech Lead + CIO + RH.

---

## Mapeamento OWASP LLM Top 10 (2025) → Riscos desta proposta

| OWASP | Risco interno | Onde mitigado |
|-------|---------------|----------------|
| LLM01 — Prompt Injection | R13 | Llama Prompt Guard 2 + system prompt + structured |
| LLM02 — Sensitive Information Disclosure | R5, R14 | Presidio + ACL retrieval + WORM |
| LLM03 — Supply Chain | R10, R15 | Mirror HF + Cosign + scan + licenças |
| LLM04 — Data and Model Poisoning | R10 | ProtectAI Guardian + checksum |
| LLM05 — Improper Output Handling | R7, R13 | Output guardrails + structured + humano |
| LLM06 — Excessive Agency | R13 | Agentes com kill-switch + step validation |
| LLM07 — System Prompt Leakage | R5 | System prompt segregado + auditado |
| LLM08 — Vector & Embedding Weaknesses | R14 | ACL no retrieval + reranker |
| LLM09 — Misinformation | R7, R8 | RAG citações + groundedness + humano |
| LLM10 — Unbounded Consumption | R12 | Quotas no gateway + cost dashboards |

---

## Plano de exercícios de risco (anual)

| Exercício | Frequência | Quem participa |
|-----------|------------|------------------|
| Red team IA (prompt injection, jailbreak) | Semestral | CISO + Lakera/Trail of Bits |
| GameDay DR (failover de cluster) | Trimestral | SRE + Tech Lead |
| Tabletop DPIA (vazamento PII) | Anual | DPO + Jurídico + CISO |
| Auditoria de licenças de modelo | Trimestral | Jurídico + Tech Lead |
| Revisão de OWASP LLM Top 10 | Anual | CISO + Tech Lead |
| Drift evaluation (Ragas + DeepEval) | Mensal | ML Engineer |

---

## Fontes

- Etapa 3 §09 (lições aprendidas + armadilhas + métricas que importam)
- Etapa 4 §06 (segurança e compliance)
- Etapa 4 §11 (checklist de prontidão)
- OWASP GenAI Top 10 LLM 2025 (`https://genai.owasp.org/`)
- LGPD Art. 7 X / Art. 11 / multas ANPD
- ISO/IEC 42001 (Granite 4 referência)
- IBM Security Cost of a Data Breach 2025
