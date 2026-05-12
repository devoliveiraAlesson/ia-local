# Gateways / Proxy LLM (2026)

> Camada que padroniza acesso a modelos (interno + externo), aplica políticas (quotas, rate limit, redação PII, semantic cache, fallbacks, RBAC) e atribui custos. Em empresa sensível, é peça de **governança obrigatória** — todo tráfego LLM passa por aqui.

## Tabela comparativa

| Gateway | Self-host? | Throughput observado | Latência overhead | Forças | Fraquezas | Licença |
|---------|-----------|----------------------|-------------------|--------|-----------|---------|
| **LiteLLM** | Sim (referência OSS) | ~890 RPS | ~95 ms | Coverage de **100+ providers**, OpenAI-compat, virtual keys, budgets, audit log; barato de operar | Throughput limitado por GIL Python; sem guardrails built-in; observability básica | MIT |
| **Portkey** | Cloud + Gateway OSS | ~2.100 RPS | ~27 ms | Semantic cache, prompt mgmt, guardrails marketplace, OTel GenAI | Cloud é principal; self-host gateway é OSS mas plano enterprise é SaaS | OSS gateway (MIT) + SaaS |
| **Kong AI Gateway** | Sim (OSS Kong + plugins) | ~8.200 RPS | ~12 ms | Performance industrial; ecossistema Kong (rate limit, auth, mTLS); enterprise SSO | Operação Kong é peso para quem não usa | Apache 2.0 (gateway) + Enterprise para PII redaction |
| **Envoy AI Gateway** | Sim (OSS, projeto CNCF) | Alto (Envoy proxy) | <10 ms | Service mesh-friendly (Istio, Gloo), nativo Envoy, **AI-aware filters** (token-based RL) | Recente (lançado 2024); ainda menos features de governança | Apache 2.0 |
| **TrueFoundry** | Cloud + on-prem | Médio | médio | Governança, RBAC, observability | Comercial | Subscription |
| **OpenRouter** | SaaS público | — | — | Marketplace de modelos | Não é self-host | — |
| **MLflow Deployments / AI Gateway** | Sim | Médio | médio | Para times MLflow | Coverage menor | Apache 2.0 |

## Funcionalidades esperadas em um gateway corporativo

1. **OpenAI API compatibility** (`/v1/chat/completions`, `/v1/embeddings`).
2. **Multi-provider**: roteamento entre vLLM interno, NIM, Bedrock, Azure OpenAI (fallback).
3. **Virtual keys**: chave por equipe/usuário, com budget e rate limit.
4. **Audit log**: log estruturado de prompt/response (com PII opcional redacted).
5. **Rate limit**: por chave, por modelo, por janela.
6. **Cost attribution**: token count + custo por chamada.
7. **Semantic cache**: hash de embedding + lookup; corta 20-40% chamadas redundantes.
8. **Guardrails hooks**: integração com Llama Guard, Presidio, NeMo Guardrails.
9. **Fallback / failover**: se vLLM principal cair, encaminha para secundário.
10. **A/B testing / canary**: % de tráfego em versão nova.
11. **Observability OTel GenAI**: emite traces no padrão.

## Detalhamento

### LiteLLM
- **O que é**: SDK Python + servidor proxy OpenAI-compatible. **Cobertura mais ampla do mercado** (100+ providers).
- **Funcionalidades**: virtual keys, team budgets, request logging, OpenTelemetry, fallbacks, retries, **router** com load balancing entre múltiplos endpoints, **guardrails plugin** (Lakera, Aporia, Presidio).
- **Quando usar**: ambiente Python, tráfego moderado (<500 RPS), self-host simples (Docker + Postgres + Redis).
- **Quando NÃO**: alta escala (Kong é 9× mais rápido), workloads de baixa latência crítica.
- **Licença**: MIT (com Enterprise add-ons em cloud BerriAI).
- Links: <https://github.com/BerriAI/litellm> · <https://docs.litellm.ai/>

### Portkey
- **O que é**: gateway moderno com foco em features de prompt mgmt, semantic cache, guardrails marketplace.
- **Funcionalidades exclusivas**: **prompt versioning** com IDs no payload, **semantic cache** (~10-30 ms embedding lookup), guardrails store (parceiros), **virtual keys** com permissões granulares.
- **Quando usar**: regulado, multi-team, foco em prompt-as-code e guardrails plug-and-play.
- **Quando NÃO**: prefere stack 100% OSS sem dependência de plano SaaS para features avançadas.
- Links: <https://portkey.ai/> · <https://github.com/Portkey-AI/gateway>

### Kong AI Gateway
- **O que é**: extensão de **Kong Gateway** (API Gateway maduro) com plugins AI: `ai-proxy`, `ai-rate-limiting-advanced`, `ai-prompt-template`, `ai-prompt-decorator`, `ai-prompt-guard`, `ai-azure-content-safety`, `ai-semantic-cache`, `ai-request-transformer`.
- **Performance**: até **8.200 RPS, 12 ms overhead** em benchmark Kong (a referência para alta escala em 2026).
- **Quando usar**: empresa onde Kong já é o API gateway corporativo; alta escala.
- **Quando NÃO**: greenfield sem operação Kong; PII redaction e enterprise SSO são paid-only.
- Links: <https://docs.konghq.com/gateway/latest/ai-gateway/> · <https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm>

### Envoy AI Gateway
- **O que é**: projeto CNCF/Envoy oficial (lançado em 2024 pela parceria Envoy + Tetrate + Bloomberg + outros), com filtros AI-aware (token-based rate limit, model routing).
- **Quando usar**: empresa com **service mesh** (Istio/Envoy/Gloo); padrão CNCF.
- **Quando NÃO**: precisa de prompt management e guardrails out-of-the-box (use LiteLLM ou Portkey por cima).
- Links: <https://aigateway.envoyproxy.io/> · <https://github.com/envoyproxy/ai-gateway>

### TrueFoundry, MLflow Deployments
- TrueFoundry: comercial; popular em times de plataforma ML que querem appliance.
- MLflow AI Gateway (renomeado de "MLflow Deployments"): para times MLflow-house.
- Links: <https://www.truefoundry.com/> · <https://mlflow.org/docs/latest/llms/deployments/index.html>

## Padrões arquiteturais

### Single gateway (mais simples)
```
[Apps] -> [LiteLLM ou Portkey] -> [vLLM] / [NIM] / [Bedrock fallback]
```

### Service mesh + gateway
```
[Apps] -> [Envoy / Istio] -> [Envoy AI Gateway] -> [LiteLLM router] -> [vLLM cluster]
                                                                        \> [SGLang cluster]
```

### Hierárquico (corporações grandes)
```
[Apps de team A]  ->  [LiteLLM team A]  --\
[Apps de team B]  ->  [LiteLLM team B]  ---> [Kong AI Gateway corporativo] -> [vLLM / NIM / Bedrock]
                                          /
[Apps de team C]  ->  [Portkey team C]  -/
```

## Mapeamento gateway → controles OWASP

| OWASP | Gateway feature |
|-------|------------------|
| LLM01 prompt injection | Plugin Llama Guard / NeMo Guardrails / Lakera |
| LLM02 PII | Plugin Presidio / Microsoft PII / Kong AI Azure Content Safety |
| LLM06 excessive agency | Virtual keys com escopo de tools |
| LLM07 system prompt leakage | Prompt template centralizado, sem segredo no prompt |
| LLM10 unbounded consumption | Rate limit + token quota + circuit breaker + budget alerts |

## Fontes

- AI gateway benchmark Kong vs Portkey vs LiteLLM: <https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm>
- Top 5 LLM gateways 2026: <https://dev.to/varshithvhegde/top-5-llm-gateways-in-2026-a-deep-dive-comparison-for-production-teams-34d2>
- TrueFoundry guide AI gateways 2026: <https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison>
- LiteLLM: <https://github.com/BerriAI/litellm>
- Portkey gateway: <https://github.com/Portkey-AI/gateway>
- Kong AI Gateway: <https://docs.konghq.com/gateway/latest/ai-gateway/>
- Envoy AI Gateway: <https://aigateway.envoyproxy.io/>
