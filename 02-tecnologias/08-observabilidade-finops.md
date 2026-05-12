# Observabilidade, Avaliação e FinOps de LLM (2026)

> Camadas de **trace** (o que aconteceu na requisição), **eval** (qualidade da resposta), e **FinOps** (custo por usuário/feature/team). Em 2026, **OpenTelemetry GenAI Semantic Conventions** virou o padrão atravessador (ainda experimental em mar/2026, mas adotado por todos os principais).

## Tabela-resumo

| Plataforma | Self-host? | OTel GenAI? | Foco | Licença | Stars (mai/2026) |
|-----------|-----------|------------|------|---------|-------------------|
| **Langfuse** | **Sim (referência OSS)** | Sim (nativo) | Tracing + eval + prompt mgmt + datasets | MIT | 12k+ |
| **Arize Phoenix** | Sim (OSS) | Sim (OpenInference + OTel) | Tracing + eval + datasets, embedding analysis | Elastic License v2 | 5k+ |
| **Arize AX** (cloud) | Não | Sim | Tracing + eval enterprise | Comercial | — |
| **LangSmith** (LangChain) | Cloud (self-host enterprise) | Parcial | Tracing + eval + prompt hub | Comercial | — |
| **Helicone** | Sim (OSS) | Parcial | Tracing/proxy | **Em maintenance desde mar/2026** | — |
| **Weights & Biases Weave** | Cloud + self-host | Parcial | ML+LLM unificado | Comercial | — |
| **Braintrust** | Cloud | Sim | Eval + datasets + prompt CI | Comercial | — |
| **Datadog LLM Observability** | SaaS | Sim | Tracing + APM + segurança | Comercial | — |
| **OpenTelemetry GenAI** | Spec | (define o padrão) | Convenções universais | Apache 2.0 | — |

## OpenTelemetry GenAI Semantic Conventions

- **Spec aberta** que padroniza nomes de spans, atributos (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, etc.) e events.
- **Status mar/2026**: experimental (a maioria das partes). Adoção: Langfuse, Arize, Datadog, Portkey, OpenLLMetry, MLflow, ClickHouse seguem o padrão.
- **Ganho prático**: trocar backend (Langfuse → Datadog, etc.) sem reinstrumentar.
- Link: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>

## Detalhamento

### Langfuse
- **Plataforma OSS de referência** para self-host. Faz: tracing (LangChain, LlamaIndex, OpenAI SDK, vLLM via OTel), eval (LLM-as-judge, custom Python, **dataset experiments**), **prompt management com versionamento**, playground, **scores manuais** (anotação humana).
- **Quando usar**: empresa quer self-host completo com features modernas, eval automatizado em CI.
- **Quando NÃO**: time prefere SaaS gerenciado.
- Links: <https://github.com/langfuse/langfuse> · <https://langfuse.com/>

### Arize Phoenix (OSS) e Arize AX (cloud)
- **Phoenix**: OSS, **OpenInference** (spec própria compatível com OTel), forte em **embedding analysis** e drift detection. Self-host fácil.
- **Arize AX**: SaaS enterprise.
- **Quando usar**: time ML clássico que quer LLM observability + drift de embeddings; cenários multi-modelo.
- **Licença Phoenix**: Elastic License v2 (não é OSI, restrita a uso "como serviço").
- Links: <https://github.com/Arize-ai/phoenix> · <https://docs.arize.com/phoenix>

### LangSmith (LangChain)
- Casa do ecossistema LangChain. Tracing automático para LangChain/LangGraph; **prompt hub**, **evals**, **datasets**, **annotation queues**.
- Self-host **enterprise** (comercial).
- Links: <https://www.langchain.com/langsmith>

### Helicone
- Foi popular como proxy + observability. **Em maintenance desde 3/mar/2026** (founders foram para Mintlify). Não escolher para greenfield 2026.
- Links: <https://github.com/Helicone/helicone>

### Datadog LLM Observability
- Integração com APM existente; útil onde Datadog já é instalado.
- Links: <https://www.datadoghq.com/product/llm-observability/>

### Weights & Biases Weave
- Sucessor de W&B Prompts; tracing + eval; popular onde W&B já existe.
- Links: <https://wandb.ai/site/weave>

### Braintrust
- SaaS focado em **eval-driven development**; integra com CI; popular em teams que tratam prompts como código.
- Links: <https://www.braintrust.dev/>

## Frameworks de avaliação (eval)

| Framework | Tipo | Quando usar | Licença |
|-----------|------|-------------|---------|
| **Ragas** | Métricas RAG-specific (faithfulness, context relevance, answer correctness) | Eval pipelines RAG; sem ground truth necessário | Apache 2.0 |
| **DeepEval** | Pytest-style; metric library extensa (G-Eval, hallucination, summarization, ...) | CI/CD gating; unit-test-style | Apache 2.0 |
| **Promptfoo** | YAML declarativo; **red team** built-in | Testes de regressão e segurança em CI | MIT |
| **OpenAI Evals** | Framework open OpenAI | Reuso de evals públicos | MIT |
| **lm-evaluation-harness** (EleutherAI) | Benchmark acadêmico (MMLU, HellaSwag, etc.) | Avaliar modelos base | MIT |
| **TruLens** | Tracing + feedback functions | Eval contínuo em produção | MIT |
| **Phoenix evals** | Built-in no Phoenix | Junto com tracing | Elastic v2 |
| **HELM** (Stanford) | Holistic eval suite | Pesquisa, comparações amplas | Apache 2.0 |
| **G-Eval / Geval** | LLM-as-judge framework genérico | Eval qualitativo automatizado | — |

### Padrão observado em 2026

1. **CI gating**: DeepEval ou Promptfoo bloqueando PRs com regressão.
2. **Production tracing + eval contínuo**: Langfuse ou Phoenix coletando 100% de traces, com eval programático (Ragas) e LLM-as-judge.
3. **Annotation queue**: humanos anotam amostras → vira dataset → vira métrica.

## FinOps para LLM (2026)

### Métricas-chave

| Métrica | Definição | Alvo típico |
|---------|-----------|-------------|
| Tokens in / out por request | Tracing nível request | Limite via gateway |
| **Cost per request** | $$ por chamada (com custo de GPU rateado) | < custo equivalente API comercial |
| **Tokens per second per GPU** | Throughput | Maximizar com vLLM/SGLang + batching |
| **Cache hit rate** (semantic + KV) | % requests servidos de cache | 20-40% típico em RAG |
| **Cost per active user / per case** | Atribuição multi-tenant | KPI de adoção |
| **GPU utilization** | % | >70% sustentado (DCGM/NVML) |
| **Latency p50 / p95 / p99** | TTFT, TPOT | TTFT <500ms, TPOT <50ms padrão |

### Ferramentas de FinOps

- **Langfuse / Phoenix / LangSmith**: cost tracking por request.
- **LiteLLM / Portkey**: rate limit + budget alerts + virtual keys (atribuição por equipe).
- **Kubecost / OpenCost**: custo de GPU rateado em K8s.
- **NVIDIA DCGM / `nvidia-smi`**: utilização real GPU.
- **Prometheus + Grafana**: dashboards (vLLM exporta métricas Prometheus nativamente).

### Otimizações comuns 2026

1. **FP8 em H100/H200/B200**: -50% memória, ~99,9% qualidade. Default 2026.
2. **AWQ INT4** quando memória aperta: -75% memória, ~98,5% qualidade.
3. **Semantic cache** no gateway (Portkey, LiteLLM com Redis): reduz 20-40% requests.
4. **Prefix caching** (vLLM V1, SGLang RadixAttention): grátis e acumula sobre RAG.
5. **Speculative decoding** (vLLM, TGI, TRT-LLM): -30-50% latência para mesma qualidade.
6. **Disaggregated serving** (Anyscale, llm-d): separa prefill/decode → utilização melhor.
7. **Right-sizing model**: Qwen3 14B + reranker frequentemente substitui 70B em RAG.

## Convenções OTel GenAI: atributos críticos

```
gen_ai.system           = "vllm" | "openai" | "ollama" | ...
gen_ai.request.model    = "Qwen/Qwen3-72B-Instruct"
gen_ai.usage.input_tokens
gen_ai.usage.output_tokens
gen_ai.response.id
gen_ai.response.finish_reasons
gen_ai.operation.name   = "chat" | "text_completion" | "embeddings" | "tool"
gen_ai.user.id          (RBAC / FinOps)
gen_ai.tool.name        (function calling)
```

## Fontes

- OTel GenAI conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Portkey on OTel GenAI: <https://portkey.ai/blog/opentelemetry-semantic-conventions-for-genai-traces/>
- Langfuse OTel: <https://langfuse.com/integrations/native/opentelemetry>
- Langfuse: <https://github.com/langfuse/langfuse>
- Phoenix Arize: <https://github.com/Arize-ai/phoenix>
- Helicone status: <https://agentmodeai.com/agent-observability-langfuse-arize-helicone-langsmith/>
- DeepEval: <https://github.com/confident-ai/deepeval>
- Ragas: <https://github.com/explodinggradients/ragas>
- Promptfoo: <https://github.com/promptfoo/promptfoo>
- LLM eval frameworks 2026: <https://atlan.com/know/llm-evaluation-frameworks-compared/>
