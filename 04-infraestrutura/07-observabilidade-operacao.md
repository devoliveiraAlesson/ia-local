# Observabilidade e Operação

> Etapa 4/5 da proposta. Stack de observabilidade dupla (infra + LLM), alertas e runbooks de incidentes típicos.

## 1. Princípio: dupla camada de observabilidade

Empresas que entram em produção com LLM aprendem rápido que **monitoramento "infra-only" é insuficiente**. É preciso operar duas camadas:

- **Camada A — Infra clássica**: GPU utilization, memória, throughput, erros HTTP, K8s healthchecks. Stack: **Prometheus + Grafana + Loki + Tempo + DCGM exporter**.
- **Camada B — LLM-specific**: traces de prompt/resposta, custo por usuário, qualidade (eval), drift de embeddings, taxa de bloqueio por guardrail. Stack: **Langfuse + Phoenix Arize + OpenTelemetry GenAI**.

## 2. Stack Camada A — Infra

| Componente | Função | Notas |
|-----------|--------|-------|
| **Prometheus** | Métricas de série temporal | Federação por cluster, retenção 30 dias hot |
| **Grafana** | Dashboards | Multi-tenant; integra Prom + Loki + Tempo |
| **Loki** | Logs estruturados | Cheap, label-based |
| **Tempo** | Tracing distribuído | Compatível OTel; integra com Grafana |
| **DCGM exporter (NVIDIA)** | Métricas de GPU | util, mem, ECC, throttle, temperatura |
| **amd-smi-exporter** | Métricas AMD | equivalente para MI300X+ |
| **gaudi-exporter** | Métricas Intel Gaudi | menos maduro |
| **node-exporter** | Métricas de SO | CPU, RAM, disco |
| **kube-state-metrics** | Estado K8s | pods, deployments, KServe |
| **Alertmanager** | Roteamento de alertas | PagerDuty, OpsGenie, Slack |
| **Thanos / Cortex / Mimir** | Long-term storage de Prom | retenção > 1 ano |

### 2.1 Métricas DCGM essenciais

| Métrica | Limite saudável | Alerta |
|---------|-----------------|--------|
| `DCGM_FI_DEV_GPU_UTIL` | 30–80% durante carga | <10% sustentado = idle; >95% sustentado = saturação |
| `DCGM_FI_DEV_FB_USED` | <90% da VRAM | >95% por 5min = OOM iminente |
| `DCGM_FI_DEV_GPU_TEMP` | <80°C | >85°C = throttling |
| `DCGM_FI_DEV_POWER_USAGE` | <90% TDP | >TDP sustentado = problema power/cooling |
| `DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL` | sob carga TP | colapso indica falha NVLink |
| `DCGM_FI_DEV_PCIE_REPLAY_COUNTER` | 0 | crescente = falha de PCIe |
| `DCGM_FI_DEV_XID_ERRORS` | 0 | qualquer XID 79/63/74 = GPU/driver instável |

### 2.2 Métricas vLLM/SGLang essenciais

| Métrica | Significado | Alerta |
|---------|-------------|--------|
| `vllm:num_requests_running` | Requests em processamento | depende capacity |
| `vllm:num_requests_waiting` | Fila | >50 sustentado = subdimensionado |
| `vllm:gpu_cache_usage_perc` | % do KV-cache em uso | >90% = thrashing iminente |
| `vllm:time_to_first_token_seconds` | TTFT | p99 > 2s = problema |
| `vllm:time_per_output_token_seconds` | TPOT | p99 > 200ms = problema |
| `vllm:e2e_request_latency_seconds` | latência fim-a-fim | p99 > 10s = problema |
| `vllm:prompt_tokens_total` / `vllm:generation_tokens_total` | volume | base para FinOps |

## 3. Stack Camada B — LLM-specific

| Componente | Função | Self-host on-prem? |
|-----------|--------|---------------------|
| **Langfuse** | Tracing de prompt/resposta, evals, prompt mgmt | sim, mature; PostgreSQL backend |
| **Phoenix Arize** | LLM evals, drift, embedding visualization | sim, OSS |
| **OpenTelemetry GenAI semantic conventions** | spec aberto para tracing | sim, ainda experimental em mai/2026 |
| **Ragas** | Evals automáticos para RAG | biblioteca, integra com Langfuse |
| **DeepEval** | Test framework para LLM | biblioteca |
| **Promptfoo** | Regression test de prompts | CLI/CI |
| **Helicone** | Proxy LLM com obs | em maintenance mode mar/2026 — evitar |
| **LangSmith** | Tracing comercial LangChain | só cloud — não recomendado para air-gap |
| **Datadog LLM Observability** | Comercial; integrado | Datadog é cloud — não para air-gap puro |

### 3.1 O que monitorar em LLM

| Métrica | Por que importa |
|---------|-----------------|
| Custo por usuário/tenant | FinOps; detecção de abuso |
| Tokens in/out por modelo | Capacity planning |
| Taxa de bloqueio por guardrail | Saúde de segurança; drift de tentativas |
| Latência (TTFT, TPOT, e2e) p50/p95/p99 | SLO |
| Eval scores (faithfulness, relevance, harmfulness) | Qualidade |
| Drift de embeddings | Mudança de comportamento dos usuários |
| Cache hit rate (semantic + KV) | Eficiência |
| Saturation por modelo | Quando rotear para fallback |

## 4. OpenTelemetry GenAI — status e recomendação

**Status mai/2026**: spec experimental mas adotada por Langfuse, Phoenix, Arize, Datadog, Splunk.

**Recomendação**: emitir spans OTel GenAI **desde dia 1** (instrumentação oficial em vLLM/LangChain/LlamaIndex disponível). Isso evita lock-in: hoje Langfuse, amanhã o que for melhor — basta apontar OTel collector.

### 4.1 Atributos OTel GenAI essenciais

```
gen_ai.system = "vllm"
gen_ai.request.model = "llama-3.3-70b-awq"
gen_ai.request.temperature = 0.7
gen_ai.request.max_tokens = 1024
gen_ai.usage.input_tokens = 850
gen_ai.usage.output_tokens = 312
gen_ai.response.finish_reasons = ["stop"]
gen_ai.user.id = "<hashed>"
gen_ai.tenant.id = "finance"
```

## 5. Pipeline de observabilidade end-to-end

```
       Frontend  ──►  Gateway  ──►  Guardrails  ──►  vLLM  ──►  Vector store
          │             │              │             │              │
          ▼             ▼              ▼             ▼              ▼
       OTel SDK     OTel SDK       OTel SDK      OTel exporter    OTel SDK
                                       │
                                       ▼
                              ┌──────────────────┐
                              │  OTel Collector  │
                              │  (sampling, redaction, routing)│
                              └─────────┬────────┘
                                        │
                ┌───────────────────────┼────────────────────────┐
                ▼                       ▼                        ▼
        ┌─────────────┐         ┌─────────────┐          ┌─────────────┐
        │  Prometheus │         │  Tempo /    │          │  Langfuse   │
        │  (métricas) │         │  Jaeger     │          │  (LLM trace)│
        │             │         │  (tracing)  │          │  + evals    │
        └──────┬──────┘         └──────┬──────┘          └─────┬───────┘
               │                       │                       │
               └───────────────────────┼───────────────────────┘
                                       ▼
                                  ┌─────────┐
                                  │ Grafana │
                                  │ (visão  │
                                  │  unificada)
                                  └─────────┘
```

## 6. Dashboards de referência

### 6.1 Dashboard "Capacity"

- GPU utilization por modelo (heatmap).
- KV-cache usage por servidor.
- Request queue depth.
- Tokens/s por modelo (sparkline).
- VRAM headroom.

### 6.2 Dashboard "SLO"

- Latência TTFT/TPOT/e2e — p50/p95/p99.
- Erros (HTTP 5xx, OOM, timeout).
- Disponibilidade rolling 30 dias.
- Burn-rate de error budget.

### 6.3 Dashboard "FinOps"

- Custo (estimado) por modelo, por tenant, por usuário top-N.
- Tokens consumidos por hora/dia/mês.
- Taxa de cache hit (semantic).
- Alerta de cost-spike.

### 6.4 Dashboard "Segurança / Guardrails"

- Bloqueios por categoria (Llama Guard 3).
- Detecções de PII (Presidio).
- Heatmap de tentativas suspeitas por usuário.
- Modelos não-aprovados em uso (alerta).

### 6.5 Dashboard "Qualidade"

- Eval scores (Ragas) — média móvel.
- Drift de embeddings.
- Top prompts com baixo score.
- Feedback humano (thumbs up/down) por modelo.

## 7. Alertas operacionais (sample)

| Severidade | Condição | Ação |
|-----------|----------|------|
| **Crítico** | XID error em GPU | Cordon node, abrir ticket NVIDIA |
| **Crítico** | KV-cache > 95% por 5 min | Scale-out / migrar tráfego |
| **Crítico** | p99 e2e > SLO por 10 min | PagerDuty para on-call |
| **Crítico** | Modelo não-aprovado em uso | Bloquear no gateway, ticket Sec |
| **Alto** | Taxa de jailbreak > 5% por hora | Investigar usuário, ativar rules adicionais |
| **Alto** | Cost-spike > 3× baseline | Investigar tenant; quota emergencial |
| **Alto** | Drift de eval > 10 pp | Investigar dataset/modelo; rollback |
| **Médio** | Cache hit < 30% sustentado | Revisar política semantic cache |
| **Médio** | GPU temp > 85°C | Verificar cooling do rack |

## 8. Runbooks — incidentes típicos

### 8.1 GPU OOM em vLLM

1. Verificar `DCGM_FI_DEV_FB_USED` no momento do crash.
2. Verificar `vllm:num_requests_running` e `gpu_cache_usage_perc`.
3. Causa comum: prompt anormalmente longo (>32k tokens) com batch alto.
4. Mitigação: reduzir `max_num_seqs`, aumentar `gpu_memory_utilization` reverso, ativar prefix caching.
5. Permanente: aumentar VRAM (TP=4) ou ativar offload NVMe.

### 8.2 Latência p99 explodindo

1. Verificar fila de requests (`vllm:num_requests_waiting`).
2. Verificar bandwidth NVLink/IB.
3. Verificar saturação de CPU do nó (tokenização pode virar gargalo).
4. Mitigação: reduzir `max_num_batched_tokens`; ativar chunked prefill; rotear excesso para canary fallback.

### 8.3 Modelo respondendo "fora de assunto"

1. Verificar logs de retrieval (RAG): retornou chunks corretos?
2. Verificar reranker: top-3 são relevantes?
3. Verificar drift de embeddings (Phoenix).
4. Mitigação imediata: aumentar top-k do retriever; ajustar prompt.
5. Permanente: re-indexar corpus; re-treinar embeddings se mudança de domínio significativa.

### 8.4 Vazamento de PII

1. Bloqueio Presidio falhou? Categorizar tipo de PII.
2. Logs WORM já registraram? Iniciar processo de incidente conforme LGPD.
3. Mitigação: ajustar regras Presidio; adicionar regex custom.
4. Comunicar DPO em <72h se confirmado vazamento (LGPD Art. 48).

### 8.5 Jailbreak bem-sucedido

1. Capturar prompt + resposta (já em Langfuse).
2. Categorizar técnica (prompt injection, role-play, encoding).
3. Adicionar ao corpus de Garak/PyRIT.
4. Rebuild de Llama Guard 3 fine-tune ou política Guardrails AI.
5. Re-rodar regression suite (Promptfoo).

### 8.6 Modelo "envenenado" detectado

1. Snapshot do modelo + logs.
2. Quarentena: marcar imagem como deprecated em Harbor.
3. Rollback ArgoCD para versão anterior.
4. Investigar supply chain: como passou pelo scan?
5. Atualizar pipeline de promoção com nova checagem.

## 9. SLOs típicos (referência inicial)

| Caso de uso | TTFT p99 | E2E p99 | Disponibilidade | Eval mínimo |
|-------------|----------|---------|------------------|--------------|
| Chat interno | 1,5s | 5s | 99,5% | NPS interno > 70 |
| Coding autocomplete | 200ms | 800ms | 99,9% | Aceite > 25% |
| RAG corporativo | 1s | 4s | 99,5% | Faithfulness > 0,85 |
| Atendimento cliente | 1s | 4s | 99,9% | CSAT > 4,2/5 |
| Sumarização batch | n/a | janela 4h | 99% | Precisão fato > 95% |

## 10. FinOps — atribuição de custo

- Cada request carrega `tenant`, `cost_center`, `model`.
- Custo real GPU: **(GPU $/hora) × (tempo ocupado)** ou aproximação **(tokens × custo por token)**.
- Showback mensal por tenant; chargeback opcional após 6 meses.
- KPI executivo: **US$ por 1k tokens em média** vs **provedor cloud equivalente**. Alvo: <50% do API público.

## 11. Decisões executivas

| Pergunta | Recomendação |
|----------|--------------|
| Stack obs comercial ou open source? | OSS (Prom + Grafana + Langfuse + Phoenix) salvo se já paga Datadog/Splunk |
| OTel GenAI desde dia 1? | Sim — investimento que não fica obsoleto |
| Quem opera? | Equipe de SRE existente + 1–2 ML engineers para Camada B |
| Retenção de logs LLM? | Mínimo 90 dias hot, conforme regulação (até 5 anos WORM) |

## Referências

- vLLM metrics: <https://docs.vllm.ai/en/latest/serving/metrics.html>
- DCGM exporter: <https://github.com/NVIDIA/dcgm-exporter>
- Langfuse self-hosting: <https://langfuse.com/self-hosting>
- Phoenix Arize: <https://docs.arize.com/phoenix>
- OpenTelemetry GenAI: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Ragas: <https://docs.ragas.io/>
- Promptfoo: <https://www.promptfoo.dev/>
- DeepEval: <https://docs.confident-ai.com/>
- Grafana Tempo: <https://grafana.com/oss/tempo/>
