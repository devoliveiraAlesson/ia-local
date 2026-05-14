# Roadmap de adoção — Fases 0–3 para integrar MCP ao stack corporativo de IA

> Sequência de implantação para empresa que já está no roadmap da Etapa 5 (Fases 0–4 do plano-mestre). MCP **não é projeto isolado**: encaixa como capacidade transversal sobre o RAG corporativo (Caso 3) e o coding assistant (Caso 4).

## Como esta Fase encaixa no plano-mestre

Recapitulação do roadmap consolidado em [`05-roi-e-proposta/03-roadmap-12-meses.md`](../05-roi-e-proposta/03-roadmap-12-meses.md):

| Fase mestre | Quando | Marco | Sobreposição com MCP |
|-------------|--------|-------|----------------------|
| Fase 0 — Fundação | M0–M2 | Stack base + governança | MCP Fase 0 (config registry, allowlist) |
| Fase 1 — RAG corporativo + Chat | M3–M5 | Caso 1 + Caso 3 em produção | MCP Fase 1 (adapter sobre RAG + piloto Claude Code) |
| Fase 2 — Coding assistant + casos 6/7 | M6–M8 | Caso 4 em escala | MCP Fase 2 (rollout amplo + segundo servidor MCP) |
| Fase 3 — Agentes complexos | M9–M12 | Workflows multi-tool | MCP Fase 3 (Graph RAG + servidores especializados) |

Não há "Fase MCP isolada" — as Fases 0/1/2/3 abaixo são entregas dentro do roadmap mestre.

## Fase 0 (M0–M2) — Fundação MCP

**Objetivo**: governança e infraestrutura prontas antes do primeiro dev tocar Claude Code com servidor corporativo.

| Entregável | Owner | Critério de pronto |
|------------|-------|---------------------|
| Política interna de MCP publicada | Eng de Plataforma + Sec | Documento aprovado por CISO; cobre escopos, allowlist, sandbox |
| Registry interno de servidores MCP | Plataforma | Página/repo com schema, versionamento, owner por servidor |
| Gateway interno HTTP + OAuth 2.1 contra IdP | SRE + IAM | Token funcional em conta de teste; rotação configurada |
| Sandbox para servidores experimentais | Sec + Plataforma | Container template testado (read-only, network-restricted) |
| Treinamento (1h) "MCP em 30 min" para devs do piloto | Plataforma + DevRel interno | Gravação + slides; 20+ devs treinados |
| MCP Inspector + pipeline de validação em CI | Plataforma | Inspector em pipeline de PR de servidor MCP |

**Custo Fase 0**: ~US$ 25–40k (0,5 FTE × 2 meses + ferramental). Pode ser absorvido na Fase 0 mestre.

## Fase 1 (M3–M5) — Primeiro servidor MCP em produção: RAG corporativo

**Objetivo**: Caso 3 (RAG corporativo) expõe tool `rag.search` via MCP; piloto de 15–30 devs consome via Claude Code; métricas estabilizadas.

| Entregável | Owner | Critério de pronto |
|------------|-------|---------------------|
| Adapter MCP sobre RAG corporativo (FastMCP) | Eng Plataforma | Tools: `rag.search`, `rag.fetch`, `rag.neighbors`; cobertura de teste ≥ 70% |
| Reranker (Qwen3-Reranker 4B/8B) em produção | Eng RAG | P95 do adapter < 600ms incluindo rerank |
| Política OPA para `rag.*` | Sec | Bloqueia acesso cross-departamento; testes adversariais passam |
| Observabilidade end-to-end | Plataforma | Cada tool-call em Langfuse com `audit_id`; dashboard de SLO |
| Piloto Claude Code 15–30 devs | DevEx + RH | Adoção semanal ≥ 70%; NPS interno ≥ 7 |
| CLAUDE.md template + guia interno | DevEx | Repo de referência com `.mcp.json` correto |

**KPIs de saída**:
- Acceptance rate do Claude Code: baseline (sem RAG) vs. com RAG — esperado uplift de +5–10 p.p.
- Latência P95 do adapter: < 600ms.
- % de respostas com citação de fonte: > 80%.
- 0 incidente de segurança grave (P1/P2) no servidor MCP.

**Decisão de go/no-go**: se uplift < 3 p.p. ou faithfulness não passar 88%, parar e revisar RAG (problema é a plataforma, não o MCP).

## Fase 2 (M6–M8) — Rollout amplo + segundo servidor

**Objetivo**: Claude Code com MCP corporativo vira default da engenharia; segundo servidor (GitHub interno ou Jira) entra no allowlist.

| Entregável | Owner | Critério de pronto |
|------------|-------|---------------------|
| Rollout Claude Code 100–300 devs | DevEx + RH | Onboarding documentado; suporte L1 treinado |
| Servidor MCP de GitHub Enterprise interno | Plataforma | Issues + PRs + code search com OAuth + audit |
| Servidor MCP de Jira / ServiceNow | Plataforma | Read + create ticket; ACL por projeto |
| Quota e rate limit por equipe no gateway | SRE | Métrica de top consumers; alerta de abuso |
| Política de licenciamento Claude Code consolidada | CFO + DevEx | Modelo de seats + budget por área |
| Dashboard executivo de adoção/ROI MCP | PMO | Reportável mensalmente |

**KPIs de saída**:
- Devs ativos semanais com Claude Code + MCP ≥ 70%.
- Tempo médio de "preparação de contexto" antes de tarefa de código: -50% vs. baseline.
- 3+ aplicações internas (não-coding) também consumindo o servidor MCP de RAG.

## Fase 3 (M9–M12) — Capacidades avançadas

**Objetivo**: agentes multi-tool encadeando MCP servers; Graph RAG entra para casos relacionais.

| Entregável | Owner | Critério de pronto |
|------------|-------|---------------------|
| Servidor MCP de Graph RAG (Neo4j) | Eng Dados + Plataforma | Caso âncora identificado (incident, compliance, lineage) |
| Servidores MCP especializados (DW, observabilidade, secrets vault read-only) | Plataforma + áreas owners | Cada um com política OPA + audit |
| Templates de agentes multi-tool | DevEx | Receitas: "investigação de incidente", "análise de impacto", "code review profundo" |
| Test set adversarial em CI para todos servidores | Sec | Cobertura prompt-injection / tool-injection |
| Reavaliação trimestral de catálogo | Comitê de risco | Rotacionar entradas obsoletas; promover experimentais |

**KPIs de saída**:
- Workflows multi-tool com ≥ 3 servidores MCP em produção: ≥ 5 receitas internas.
- Tempo médio de investigação de incidente: -30%.
- Adoção fora da engenharia (produto, ops, atendimento): ≥ 2 áreas.

## Cronograma sintético

```
M0  M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12
[ Fase 0 — Fundação ]
            [ Fase 1 — Primeiro servidor + piloto ]
                            [ Fase 2 — Rollout amplo + 2º servidor ]
                                            [ Fase 3 — Multi-tool + Graph RAG ]
```

## Orçamento incremental (sobre a Etapa 5)

Cenário M (referência da Etapa 5 — 200–500 funcionários, 100–300 devs):

| Item | Ano 1 | Ano 2+ |
|------|-------|--------|
| 0,5–1 FTE eng de plataforma (build + manutenção dos adapters MCP) | US$ 70–110k | US$ 70–110k |
| Licença Claude Code (estimativa, 150 seats × tier corp) | US$ 90–150k | US$ 90–150k |
| Infra adicional K8s + GPU para reranker dedicado | US$ 15–25k | US$ 10–20k |
| Sec/governance overhead (auditoria adicional, policy mgmt) | US$ 15–25k | US$ 10–15k |
| **Total incremental** | **US$ 190–310k** | **US$ 180–295k** |

Compor com o ROI da Etapa 5: a justificativa é uplift de **acceptance rate do coding assistant** + redução de tempo de cola de contexto. Em time de 200 devs × US$ 60/h × ganho de 1–2h/semana × 60% adoção, o retorno é ~US$ 1,5–3 M/ano. **Payback estimado: 2–4 meses.**

## Riscos da implantação e gatilhos

| Risco | Sinal | Resposta |
|-------|-------|----------|
| Adoção baixa do Claude Code | DAU < 30% no fim do M5 | Pesquisa qualitativa; verificar latência, qualidade do RAG, treinamento |
| Latência do servidor MCP estourando SLO | P95 > 1s consistente | Escalar réplicas, reduzir top_k, otimizar reranker (quantização, batch) |
| Política OPA bloqueia falsos positivos | Devs reclamam de "acesso negado" frequente | Revisão de política; ampliar grupos; adicionar telemetria de denies |
| Servidor de terceiro vira incidente de segurança | Detecção via SIEM | Remoção imediata do allowlist; pos-mortem; reforço de revisão |
| Custo do reranker maior que esperado | TCO Q1 acima do orçado | Quantização (INT8); cache de rerank por query similar |

## Como medir sucesso ao fim de 12 meses

- Acceptance rate do coding assistant: baseline + ≥ 8 p.p. de uplift com MCP ligado.
- Tempo médio de "preparação de contexto" para tarefas de código: −50%.
- ≥ 3 servidores MCP corporativos em produção, com SLO atingido.
- ≥ 70% dos devs em rollout ativos semanalmente.
- 0 incidente de segurança P1; ≤ 2 P2.
- NPS interno do dev experience: ≥ 8 sobre o stack de IA.

## Próxima leitura

- Visão de board: [`00-resumo-executivo.md`](./00-resumo-executivo.md).
- Implementação técnica: [`05-construir-mcp-interno.md`](./05-construir-mcp-interno.md).
- Riscos consolidados (incluindo MCP): [`05-roi-e-proposta/05-riscos-mitigacao.md`](../05-roi-e-proposta/05-riscos-mitigacao.md).
- Roadmap mestre: [`05-roi-e-proposta/03-roadmap-12-meses.md`](../05-roi-e-proposta/03-roadmap-12-meses.md).
