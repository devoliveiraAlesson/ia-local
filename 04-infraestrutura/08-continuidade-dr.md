# Continuidade e DR — HA, Canary, Backup, RPO/RTO

> Etapa 4/5 da proposta. Estratégia de alta disponibilidade, atualização contínua e disaster recovery realista para LLM em produção.

## 1. Realismo de continuidade para LLM

LLM em produção tem dois aspectos de continuidade:

1. **Estado mutável pequeno**: configurações, prompts armazenados, RBAC, vector store, logs. **Recuperação relativamente simples**.
2. **Estado mutável grande mas regenerável**: índices vetoriais, KV-cache, cache semântico. **Pode ser reconstruído** em horas/dias se necessário.

Diferente de banco de dados transacional, **LLM raramente exige RTO < 1h ou RPO < 15min**. O alvo prático para a maioria dos casos corporativos é **RPO 1h / RTO 4h**.

## 2. SLOs de continuidade por caso de uso

| Caso | RPO alvo | RTO alvo | Disponibilidade alvo | Justificativa |
|------|----------|----------|----------------------|---------------|
| Chat interno | 1h | 4h | 99,5% | Produtividade interna; downtime aceitável |
| Coding assistant | 1h | 4h | 99,5% | Idem |
| RAG corporativo | 1h | 4h | 99,5% | Reindex possível em horas |
| **Atendimento cliente** | 15 min | 1h | 99,9% | Voltado para receita; impacta NPS |
| Sumarização batch | 24h | 24h | 99% | Tipicamente off-line, retry OK |
| **Compliance / classificação PII** | 0 | 0 | 99,99% | Crítico — todo dado tem que passar |

## 3. Camadas de HA

### 3.1 Camada 1 — HA intra-cluster (mínimo absoluto)

- **Pelo menos 2 réplicas** de cada modelo crítico (KServe `replicas: 2`).
- Topology spread constraints para distribuir réplicas em **zonas/racks distintos**.
- PodDisruptionBudget (`minAvailable: 1`) para upgrade controlado.
- Liveness/Readiness probes específicas para vLLM (`/health` + `/v1/models`).

### 3.2 Camada 2 — HA inter-cluster (1 site, múltiplos racks)

- 2 clusters K8s ativo-ativo no mesmo DC.
- Gateway LiteLLM faz round-robin com health-check.
- Vector store: Qdrant cluster com replicação 2; Milvus com replicação 2.
- Postgres: replicação síncrona ou semi-síncrona.

### 3.3 Camada 3 — DR site (multi-DC)

- Site secundário em DC geograficamente separado (>50 km).
- Snapshot replicado a cada 1h (Velero + Kasten K10).
- Modelo replicado em MinIO/S3 cross-site.
- Gateway pode rotear cross-site em caso de falha total do primário.
- **CAPEX adicional ~30–50% do site primário** (não duplicado, pois capacidade reduzida aceitável em DR).

| Camada | Disponibilidade efetiva | Custo adicional |
|--------|--------------------------|------------------|
| 1 (intra-cluster) | 99,5% | baseline |
| 2 (multi-rack ativo-ativo) | 99,9% | +20–30% |
| 3 (multi-DC) | 99,99% | +30–50% |

**Recomendação**: Camada 1+2 para todos os perfis; Camada 3 só para atendimento cliente regulado / compliance crítico.

## 4. Canary deployment de modelo via gateway

```
LiteLLM router config:
  models:
    - name: chat-prod
      provider: vllm-ha
      weight: 90
      backend: llama-3.3-70b-v2.1
    - name: chat-canary
      provider: vllm-canary
      weight: 10
      backend: llama-3.3-70b-v2.2
  rollout:
    auto_promote_after: 24h
    gates:
      - p99_latency_seconds < 3
      - error_rate < 0.5%
      - eval_faithfulness >= 0.85
    rollback_on:
      - p99_latency_seconds > 5
      - error_rate > 2%
```

### 4.1 Estratégias de rollout

| Estratégia | Quando usar |
|-----------|-------------|
| **Canary por % tráfego** (10/50/100) | Mudança de versão de modelo (v2.1 → v2.2) |
| **A/B com tenants seleto** | Mudança grande (Llama → Qwen) — testar em tenants pré-aprovados |
| **Shadow / mirror** | Compara resposta sem afetar usuário (custa 2× compute durante shadow) |
| **Blue/green** | Mudança de runtime (vLLM → SGLang) |

### 4.2 Gates de promoção

- Latência p99 dentro de SLO.
- Taxa de erro < baseline + delta.
- Eval automático (Ragas/Phoenix) acima do threshold.
- Feedback humano (thumbs up/down) não piorou.
- Sem aumento de bloqueios de guardrail.

## 5. Backup — o que e como

| Item | Tecnologia | Frequência | Retenção | Imutável? |
|------|-----------|------------|----------|-----------|
| Configs K8s (manifests) | Git (ArgoCD source of truth) | a cada commit | indefinido | sim (git) |
| Imagens de container | Harbor com replicação cross-site | streaming | 1 ano | tags imutáveis (Cosign) |
| Modelos (binários) | MinIO com replicação + Object Lock | release | indefinido | sim (Object Lock) |
| Postgres (Langfuse, RBAC, Keycloak) | pg_basebackup + WAL archiving | hour-on-hour PITR 7 dias | 30 dias | snapshots imutáveis em MinIO |
| Vector store (Qdrant) | snapshots HTTP API + cópia object | diário | 30 dias hot, 1 ano cold | sim |
| Vector store (Milvus) | backup tool oficial Milvus | diário | 30 dias hot | sim |
| Logs WORM (prompts/respostas) | nativo (Object Lock / SnapLock) | streaming | 5–10 anos | sim, regulado |
| Cache semântico | n/a (regenerável) | n/a | n/a | n/a |
| Embedding cache | snapshot opcional | semanal | 30 dias | n/a |

## 6. Procedimento de DR — exercício realista

### 6.1 Cenário: falha total do DC primário

**Tempo total estimado para recuperar Chat + RAG + Coding em DR**:

| Etapa | Duração estimada |
|-------|-------------------|
| Detecção + decisão de failover | 15 min |
| DNS / gateway routing para DR | 5 min |
| Spin-up de pods K8s no DR | 10 min (imagens já em registry local) |
| Carregar modelos do MinIO local DR | 20–40 min (140 GB modelo via NVMe local) |
| Restaurar Postgres (último snapshot) | 15–30 min (PITR aplicado) |
| Restaurar Qdrant snapshot (1h atrás) | 15–60 min (depende do volume) |
| Validação de smoke tests | 30 min |
| **Total RTO** | **~2–4 horas** |

### 6.2 Exercícios obrigatórios

- **GameDay trimestral**: simular perda de 1 nó, 1 rack, 1 DC.
- **Restore test mensal** de pelo menos 1 backup aleatório.
- **Documentação atualizada** após cada exercício.

## 7. Atualizações contínuas — política

### 7.1 Cadência

| Componente | Frequência | Janela | Risco |
|-----------|------------|--------|-------|
| K8s | a cada 4 meses | manutenção noturna fim-de-semana | médio |
| GPU driver / CUDA | a cada 6 meses ou XID crítico | janela | alto (afeta toda a frota) |
| vLLM / SGLang | a cada 2 meses | canary | médio |
| Modelos | a cada release relevante | canary 24h | médio (qualidade) |
| Guardrails | a cada release | canary | médio |
| Sistema operacional (RHEL/Ubuntu) | trimestral | janela | médio |

### 7.2 Imutabilidade

- **Imagens**: tag por SHA256 ou semver imutável (`vllm:0.7.3-cuda12.4`), nunca `latest`.
- **Modelos**: pasta versionada no MinIO; checksum.
- **Configs**: git history; rollback por revert.

### 7.3 Janelas de manutenção

- **Off-peak**: madrugada local; comunicação prévia (status page interna).
- **Drain controlado**: cordon node, drenar pods, atualizar, descordonar, validar.
- **Sempre ter rollback testado** antes de iniciar.

## 8. Multi-AZ x Multi-DC x Multi-Region

| Configuração | Quando aplicar | Trade-off |
|--------------|----------------|-----------|
| **Multi-rack mesmo DC** | Padrão obrigatório p/ produção | Custo baixo |
| **Multi-DC mesmo metro (cross-cidade)** | Bancos, saúde, gov | +30% CAPEX; latência <5ms aceitável |
| **Multi-DC cross-region (BR + EU/US)** | Multinacional grande, soberania específica | Replica configs; **dados sensíveis BR ficam no BR** |
| **Cloud híbrida como DR** | Empresa média | Cuidado com soberania; BAA / Schrems II |

**Para empresa BR regulada**: 2 DCs no Brasil (e.g., SP + RJ ou SP + Campinas) é o padrão saudável.

## 9. Continuidade de fornecedores

### 9.1 Risco GPU NVIDIA

- Lead time de H100/H200/B200 oscila (em 2024–2025 chegou a 12 meses; 2026 melhorou para 4–8 semanas).
- **Mitigação**: contratos master de fornecimento; segunda fonte (AMD MI300X) para 1 nó treino-fallback.

### 9.2 Risco licença de modelo

- Llama Community License pode mudar (cláusula 700M MAU).
- Codestral MNPL bloqueia uso comercial.
- **Mitigação**: pelo menos um modelo Apache 2.0 (Granite/Qwen/Gemma) sempre disponível como fallback.

### 9.3 Risco fim de produto

- vLLM e SGLang são open source — sem risco de descontinuação abrupta.
- NIM/NVAIE: NVIDIA pode mudar política. **Mitigação**: K8s + vLLM puro como caminho de saída.
- Helicone foi para maintenance mode em mar/2026 — exemplo concreto.

## 10. Resumo executivo de continuidade

| Aspecto | Recomendação |
|---------|--------------|
| Réplicas mínimas por modelo | 2 (HA básico) |
| Nodes em racks distintos | sim |
| DR site | sim para casos cliente-facing regulados; opcional para chat interno |
| RPO realista | 1h chat / 15min atendimento |
| RTO realista | 4h chat / 1h atendimento |
| Backup imutável WORM | sim, obrigatório em ambiente regulado |
| GameDay | trimestral |
| Canary obrigatório | sim, em todo deploy de modelo ou runtime |
| Rollback documentado | sim, ensaiado |

## Referências

- KServe canary: <https://kserve.github.io/website/docs/concepts/architecture/control-plane#canary-rollout>
- Argo Rollouts: <https://argoproj.github.io/argo-rollouts/>
- Velero K8s backup: <https://velero.io/>
- Kasten K10: <https://www.kasten.io/>
- Qdrant snapshots: <https://qdrant.tech/documentation/concepts/snapshots/>
- Milvus backup tool: <https://milvus.io/docs/milvus_backup_overview.md>
- LiteLLM router & rollout: <https://docs.litellm.ai/docs/proxy/load_balancing>
