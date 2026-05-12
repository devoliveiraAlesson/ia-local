# Resumo de Arquitetura — Plataforma de IA Local

> Etapa 4/5 da proposta. Este documento define a **arquitetura de referência** que será dimensionada nos arquivos seguintes (01–11).

## Princípios de design

1. **Soberania de dados**: nenhum prompt, resposta, embedding ou log de aplicação deixa o perímetro corporativo.
2. **Modularidade por camada**: cada camada (ingress, gateway, inferência, RAG, observabilidade) é independente e substituível.
3. **Multi-modelo desde o dia 1**: a empresa nunca depende de um único modelo. O gateway abstrai 3–7 LLMs em paralelo.
4. **Multi-tenant lógico**: namespaces, ACLs e tenant-headers permitem reaproveitar GPUs entre departamentos.
5. **Observabilidade end-to-end**: cada request carrega trace-id de borda à GPU, com retenção de prompts conforme política.
6. **Air-gap-ready**: arquitetura funciona com mirror local de Hugging Face, sem dependência de internet em runtime.
7. **Padrões abertos**: Kubernetes, OpenTelemetry, OCI images, OpenAPI; evitar formatos proprietários.

## Diagrama de referência (alto nível)

```
                          ┌──────────────────────────────────────────────────────────┐
                          │                  ZONA CORPORATIVA INTERNA                │
                          │                                                          │
   Usuários internos      │   ┌───────────────┐                                      │
   (browser/IDE/app) ─────┼──▶│ Reverse Proxy │  TLS, WAF, mTLS Istio                │
                          │   │ NGINX / Envoy │                                      │
                          │   └───────┬───────┘                                      │
                          │           │                                              │
                          │           ▼                                              │
                          │   ┌───────────────┐  SAML/OIDC ────▶ ┌──────────────┐    │
                          │   │  Identity     │                  │  Keycloak /  │    │
                          │   │  & Authorize  │◀──── token ──────│  Entra ID    │    │
                          │   └───────┬───────┘                  └──────────────┘    │
                          │           │                                              │
                          │           ▼                                              │
   ┌────────────────────┐ │   ┌──────────────────────┐  ┌──────────────────────┐     │
   │ Frontend           │ │   │   LLM Gateway        │  │   Guardrails         │     │
   │ Open WebUI /       │─┼──▶│   LiteLLM / Kong AI  │─▶│   Llama Guard +      │     │
   │ LibreChat / custom │ │   │   (routing+cache+RBAC)│  │   Presidio + policy  │     │
   └────────────────────┘ │   └──────────┬───────────┘  └──────────┬───────────┘     │
                          │              │                         │                 │
                          │              │ OpenAI-compatible       │                 │
                          │              │                         ▼                 │
                          │              │              ┌──────────────────┐         │
                          │              │              │  Audit / WORM    │         │
                          │              │              │  prompts/respostas│        │
                          │              │              └──────────────────┘         │
                          │              ▼                                           │
                          │   ┌──────────────────────────────────────────┐           │
                          │   │  K8s / OpenShift AI — Pool de Inferência │           │
                          │   │                                          │           │
                          │   │  ┌──────────┐ ┌──────────┐ ┌──────────┐  │           │
                          │   │  │ vLLM     │ │ vLLM     │ │ SGLang   │  │           │
                          │   │  │ Llama 70B│ │ Qwen 32B │ │ Granite  │  │           │
                          │   │  │ TP=4     │ │ TP=2     │ │ Coder    │  │           │
                          │   │  └────┬─────┘ └────┬─────┘ └────┬─────┘  │           │
                          │   │       │            │            │        │           │
                          │   │  ┌────▼────────────▼────────────▼─────┐  │           │
                          │   │  │   GPU Fabric (NVLink + IB/RoCE)    │  │           │
                          │   │  │   H100/H200/B200 ou MI300X         │  │           │
                          │   │  └────────────────────────────────────┘  │           │
                          │   └──────────────────────────────────────────┘           │
                          │              │                                           │
                          │              ▼                                           │
                          │   ┌──────────────────┐  ┌──────────────────┐             │
                          │   │  Vector Store    │  │  Embeddings      │             │
                          │   │  Qdrant /        │◀─│  BGE-M3 / Nomic  │             │
                          │   │  Milvus / pgvec  │  │  vLLM dedicado   │             │
                          │   └────────┬─────────┘  └──────────────────┘             │
                          │            │                                             │
                          │            ▼                                             │
                          │   ┌──────────────────┐  ┌──────────────────┐             │
                          │   │  Object Store    │  │  Parallel FS     │             │
                          │   │  MinIO / S3      │  │  Weka/VAST/GPFS  │             │
                          │   │  (modelos, docs) │  │  (treino/cache)  │             │
                          │   └──────────────────┘  └──────────────────┘             │
                          │                                                          │
                          │   ┌──────────────────────────────────────────┐           │
                          │   │  Observabilidade & FinOps                │           │
                          │   │  Prometheus + Grafana + DCGM + Langfuse  │           │
                          │   │  + OTel GenAI + SIEM (Splunk/Elastic)    │           │
                          │   └──────────────────────────────────────────┘           │
                          │                                                          │
                          └──────────────────────────────────────────────────────────┘
                                                  │
                                                  │ (somente saída controlada)
                                                  ▼
                                        ┌────────────────────┐
                                        │  HF Mirror / DMZ   │
                                        │  Artifactory / Nexus│
                                        │  (download de modelos
                                        │   assinados+scaneados)│
                                        └────────────────────┘
```

## Camadas da arquitetura

| Camada | Componentes | Função |
|--------|-------------|--------|
| **Ingress** | NGINX, Envoy, Istio (mTLS) | TLS, WAF, rate-limit, mTLS leste-oeste |
| **Identity** | Keycloak / Entra ID / Okta | SSO, SAML/OIDC, RBAC, MFA |
| **Frontend** | Open WebUI, LibreChat, AnythingLLM, app interno | UX final do usuário |
| **Gateway LLM** | LiteLLM, Kong AI Gateway, Portkey | Roteamento, cache, RBAC, billing, A/B |
| **Guardrails** | Llama Guard 3, Presidio, NeMo Guardrails | PII redaction, política de uso |
| **Inferência** | vLLM, SGLang, TGI, NIM | Serving de modelos generativos |
| **Embeddings** | vLLM com BGE-M3, Nomic, Granite-Embedding | Vetorização para RAG |
| **RAG/Vector** | Qdrant, Milvus, Weaviate, pgvector | Busca semântica, ACL multi-tenant |
| **Storage** | MinIO, Weka, VAST, GPFS, Pure FlashBlade | Modelos, datasets, KV-cache, logs |
| **Orquestração** | Kubernetes + KServe, OpenShift AI, Slurm (treino) | Scheduling, autoscaling, lifecycle |
| **Observabilidade** | Prometheus, Grafana, DCGM, Langfuse, Phoenix, OTel | Infra + LLM-specific |
| **Audit/WORM** | Object lock S3, Veritas, IBM Cloud Object Storage WORM | Retenção regulada de prompts/respostas |
| **Supply chain** | HF Mirror, JFrog Artifactory, Sonatype Nexus, ProtectAI | Modelos assinados e escaneados |

## Modelos de implantação possíveis

| Modelo | Quando faz sentido | Risco |
|--------|---------------------|-------|
| **On-prem puro (air-gapped)** | Defesa, governo, dados ITAR/EAR, segredo industrial | CAPEX alto; equipe especializada obrigatória |
| **On-prem + DMZ controlada** | Saúde regulada (HIPAA), bancos, jurídico | Mirror HF e atualizações ainda exigem governança |
| **Cloud privada single-tenant** (Outposts, Azure Local, OCI Dedicated) | Empresas média/grande sem maturidade DC | Lock-in de fornecedor; soberania parcial |
| **Híbrido (sensível on-prem, geral em VPC)** | Indústria global, varejo | Complexidade de governança dupla |
| **VPC dedicada single-tenant** | Empresas reguladas médias com baixo CAPEX | Não é "local" no sentido estrito |

## Próximos arquivos

- `01-hardware-aceleracao.md` — comparativo NVIDIA / AMD / Intel / alternativos.
- `02-dimensionamento-por-caso.md` — 3 cenários (P/M/G) por caso P0.
- `03-redes.md` — InfiniBand, Spectrum-X, RoCEv2.
- `04-storage.md` — modelos, datasets, vector, logs.
- `05-orquestracao.md` — K8s/KServe vs OpenShift AI vs Ray vs Slurm.
- `06-seguranca-compliance.md` — air-gap, mirror, identity, OWASP LLM, LGPD/HIPAA/ISO 42001.
- `07-observabilidade-operacao.md` — Prom/Grafana/DCGM + Langfuse + OTel + runbooks.
- `08-continuidade-dr.md` — HA, canary, RPO/RTO.
- `09-energia-fisica.md` — kW/rack, DLC, espaço.
- `10-cloud-privada-hibrido.md` — Outposts/Azure Local/Google Distributed/OCI/IBM.
- `11-checklist-prontidao.md` — gate de prontidão antes do projeto.
