# Plataforma de Orquestração — K8s, OpenShift AI, Ray, Slurm, vGPU

> Etapa 4/5 da proposta. Camada de orquestração para serving e (opcional) treino de LLMs em ambiente corporativo.

## 1. Decisão central — Kubernetes vs HPC tradicional

| Eixo | Kubernetes (K8s + KServe + vLLM) | HPC clássico (Slurm + bare-metal) |
|------|----------------------------------|-----------------------------------|
| Foco | **Inferência (serving)** + treino leve | **Treino de larga escala** (full pretrain, multi-week) |
| Time | dev ops / cloud-native | HPC / sysadmin tradicional |
| Maturidade em IA local | dominante (90%+ dos casos) | nicho (laboratórios, governos) |
| Multi-tenant | nativo (namespace, NetworkPolicy, RBAC) | manual (account/QoS) |
| Lifecycle de modelo | declarativo (CRD) | scripts / manuais |
| Casos públicos | JPMorgan, Walmart, Stripe, UK Gov, Bradesco | Mayo (parcial), CERN, MetaAI Research |

**Recomendação**: **Kubernetes é a base padrão em 2026**. Reservar Slurm para clusters de **treino dedicado** quando a empresa tem time HPC.

## 2. Stack K8s para IA — componentes

```
┌────────────────────────────────────────────────────────────────────────┐
│ Camada 4 — Aplicações                                                  │
│   Frontends (Open WebUI, LibreChat), gateways (LiteLLM, Kong)          │
├────────────────────────────────────────────────────────────────────────┤
│ Camada 3 — Serving                                                     │
│   KServe (InferenceService) + vLLM/SGLang/TGI                          │
│   llm-d (multi-node vLLM oficial)                                      │
│   Ray Serve (alternativa)                                              │
│   NVIDIA NIM (catálogo de microsserviços homologados)                  │
├────────────────────────────────────────────────────────────────────────┤
│ Camada 2 — Lifecycle / GitOps                                          │
│   ArgoCD ou Flux                                                       │
│   Helm + Kustomize                                                     │
│   Renovate (atualizações de imagens / charts)                          │
├────────────────────────────────────────────────────────────────────────┤
│ Camada 1 — Plataforma K8s                                              │
│   Vanilla K8s (kubeadm/kubespray) ou OpenShift ou Rancher / SUSE       │
│   GPU: NVIDIA GPU Operator ou AMD ROCm Operator ou Intel Gaudi K8s     │
│   MIG / MPS / Time-slicing                                             │
│   CNI: Cilium (recomendado p/ multi-tenant) ou Calico                  │
│   CSI: Trident (NetApp) / VAST / Weka / Rook (Ceph) / OpenEBS          │
│   Service mesh: Istio (mTLS leste-oeste) ou Linkerd                    │
├────────────────────────────────────────────────────────────────────────┤
│ Camada 0 — Hardware (GPUs, nodes, storage, fabric)                     │
└────────────────────────────────────────────────────────────────────────┘
```

## 3. Distribuições K8s — comparativo

| Distribuição | Quando faz sentido | Pontos fortes | Pontos fracos |
|--------------|---------------------|----------------|----------------|
| **Vanilla upstream (kubeadm/kubespray)** | Time DevOps maduro, custo baixo | Flexibilidade total; sem licença | Carga operacional; sem suporte enterprise |
| **OpenShift Container Platform + OpenShift AI** | Empresa Red Hat / regulada / Granite | Suporte enterprise; pipeline AI incluído (KServe + vLLM + InstructLab + Granite); ISO/IEC 42001 friendly | Licença pesada; opinionated |
| **Rancher (SUSE)** | Multi-cluster (várias unidades de negócio) | Gestão multi-cluster excelente; RKE2 hardened | Menor presença em IA-specific |
| **VMware Tanzu / Cloud Foundation** | Empresa já com vSphere | Integração VMware; vGPU nativo | Pós-Broadcom: licenciamento incerto |
| **EKS Anywhere / GKE Enterprise / AKS Arc** | Híbrido com cloud pública | Operação familiar | Algum acoplamento com cloud |

## 4. OpenShift AI — quando vale o prêmio de preço

**OpenShift AI 2.x (mai/2026)** entrega "out-of-the-box":

- **KServe + vLLM (Red Hat AI Inference Server, fork upstream)** integrados.
- **Distributed workloads** com Ray on KubeRay.
- **InstructLab** + Granite para fine-tuning sem RLHF complexo.
- **Data Science Pipelines** (Kubeflow Pipelines).
- **Model Registry** centralizado.
- **Monitoring dashboards GenAI** (TrustyAI integration).
- **Suporte Red Hat enterprise** (importante para auditoria ISO 42001).

**Faz sentido quando**:
- Empresa **já é Red Hat** (RHEL + OpenShift + Ansible).
- Setor **regulado** (saúde, banco, gov) que precisa **suporte com SLA contratual**.
- Estratégia **Granite + InstructLab** (Apache 2.0 + ISO/IEC 42001).

**NÃO faz sentido quando**:
- Empresa é cloud-native pura (EKS/GKE/AKS dominante).
- CAPEX/OPEX limitado (licença OpenShift por core dobra o custo de plataforma).
- Time não tem tradição Red Hat.

## 5. Ray + Anyscale

| Cenário | Ray nativo (open source) | Anyscale (comercial) |
|---------|---------------------------|----------------------|
| Treino distribuído | Excelente (RLHF, DPO, RLOO) | Idem + suporte |
| Serving | Ray Serve com vLLM (RayLLM) | Idem otimizado |
| Hyperparameter tuning | Ray Tune | Idem |
| Caso público | Stripe, OpenAI (parte), Anthropic, Cohere | Pinterest, Spotify |

**Quando vale on-prem**: cargas mistas treino + serving + RLHF, especialmente se equipe ML já usa Ray. **Não substitui** KServe — frequentemente coexistem (Ray para batch/training, KServe para serving online).

## 6. NVIDIA NIM — catálogo de microsserviços

NIM = container OCI com modelo otimizado, geralmente vLLM ou TensorRT-LLM por baixo + APIs OpenAI-compat.

**Vantagens**:
- Pré-otimizado (engine + quantização + batch defaults certos).
- Integra com **NVIDIA AI Enterprise (NVAIE)** — licença que inclui suporte L2/L3.
- Catálogo cobre Llama, Mistral, Granite, NeMo Retriever embeddings, NeMo Guardrails.
- Roda em K8s vanilla, OpenShift, RKE2, Rafay.

**Desvantagens**:
- Lock-in NVIDIA (rodar NIM em AMD não é o ponto).
- Custo de licença NVAIE: **US$ 4.500–6.000 por GPU/ano** (estimativa pública 2026).
- Algumas customizações (chat templates exóticos) exigem rebuild.

**Recomendação**: **opcional**. NIM acelera Day-1, mas vLLM puro em K8s já é production-ready. Bons casos: empresa que paga DGX/HGX e quer suporte unificado NVIDIA.

## 7. Slurm — quando ainda faz sentido

- **Treino full pretrain** com job de dias/semanas.
- **HPC tradicional** com cargas mistas (CFD, genômica, IA).
- **Ambientes acadêmicos / governamentais**.
- **Reservas de GPU determinísticas** (Slurm tem account/QoS muito mais granular que K8s).

**Padrão híbrido**: **Slurm para treino + K8s para serving**. Mayo Clinic, CERN, vários supercomputadores nacionais usam isso.

## 8. Bare-metal vs virtualização

### 8.1 Bare-metal (K8s direto sobre hardware)

- **Vantagem**: ~5–15% mais throughput em LLMs grandes (sem overhead hypervisor).
- **Vantagem**: PCIe passthrough completo, NVLink direto.
- **Desvantagem**: difícil compartilhar máquina física entre tenants/áreas com isolamento forte.
- **Recomendação**: **padrão para nodes GPU em produção**.

### 8.2 NVIDIA AI Enterprise + vGPU sobre VMware/Nutanix

- **Vantagem**: provisionamento dinâmico de slices de GPU; Live Migration; integração com vSphere existente.
- **Desvantagem**: licença vGPU adicional (~US$ 500–1.000/GPU/ano); 5–15% overhead; suporte vGPU pode ser mais lento que MIG.
- **Recomendação**: empresas com **operação VMware muito madura** que querem manter unidade de gerência. Pós-Broadcom (2024+), avaliar com cuidado o roadmap.

### 8.3 MIG (NVIDIA Multi-Instance GPU)

- Particiona H100/H200/B200 em até 7 instâncias com isolamento de hardware.
- **Recomendação**: usar para **chat interno multi-tenant** com tenants pequenos, ou **dev/test** isolado de produção.
- **Não usar para**: workloads que precisam de mais de 1/7 da GPU (a maioria de inferência 70B).

### 8.4 MPS (Multi-Process Service) e Time-slicing

- MPS: vários processos compartilham 1 GPU sem isolamento forte. Útil para **embedding cluster** (dezenas de processos pequenos).
- Time-slicing: scheduler do GPU Operator divide GPU. Útil para dev/test.
- **Não usar em produção** com tenants conflitantes (sem isolamento forte).

## 9. Service mesh e mTLS

**Recomendação clara**: **Istio (ou Linkerd) com mTLS automático leste-oeste**.

Por quê:
- Zero-trust entre serviços (gateway → vLLM → Qdrant → Postgres).
- Authn baseada em identidade de pod (SPIFFE/SPIRE).
- Auditoria de tráfego.
- Política de tráfego (e.g., só gateway pode chamar vLLM diretamente).

Custo: ~5% de overhead de CPU; aceitável.

## 10. CNI multi-tenant (Cilium + NetworkPolicy + Hubble)

- **Cilium** com eBPF: melhor performance + observabilidade nativa (Hubble).
- **NetworkPolicy estritas** por namespace (default deny).
- **Cilium L7 policy** opcional para HTTP-aware (e.g., só permitir `POST /v1/chat/completions`).

## 11. Esquema de namespaces (multi-tenancy)

```
cluster (1 K8s)
├── ns: ai-platform        → vLLM/SGLang, KServe, Qdrant compartilhado
├── ns: ai-gateway         → LiteLLM, Kong, guardrails
├── ns: tenant-finance     → recursos isolados do depto financeiro
├── ns: tenant-legal       → idem jurídico
├── ns: tenant-customer    → produção atendimento
├── ns: ai-monitoring      → Prometheus, Langfuse
└── ns: ai-cicd            → ArgoCD, model registry
```

Combinado com:
- **Node pools dedicados**: tenants críticos têm nodes próprios via taint/toleration.
- **Resource quotas** por tenant.
- **NetworkPolicy** estritas.
- **PodSecurityStandards** (`restricted`).
- **OPA/Gatekeeper** ou **Kyverno** para policy as code.

## 12. Lifecycle de modelo — GitOps

```
git repo (modelos.yaml)
  │
  │  pull request: bump Llama 3.3 70B v2.1 → v2.2
  │
  ▼
ArgoCD detect drift
  │
  ▼
KServe InferenceService apply
  │
  ├── canary 10% por 24h
  ├── compare quality (Phoenix evals)
  ├── promote 100% se OK
  └── rollback automático se p99 ↑ ou eval ↓
```

Componentes-chave:
- **Argo CD** ou **Flux** para sincronização declarativa.
- **Argo Rollouts** para canary/blue-green com promoção automática.
- **Phoenix Arize** ou **Langfuse Evals** para gate de qualidade.

## 13. Decisões executivas

| Pergunta | Recomendação para perfil corporativo médio |
|----------|--------------------------------------------|
| K8s vanilla ou OpenShift AI? | OpenShift AI se já é Red Hat ou se Granite/InstructLab é estratégia; vanilla com ArgoCD em outros casos. |
| KServe ou Ray Serve? | KServe (padrão, mais maduro em prod). Ray onde já há Ray para treino. |
| NIM ou vLLM puro? | vLLM puro como base; NIM para modelos NVIDIA-otimizados específicos com NVAIE pago. |
| Slurm necessário? | Não, exceto se há treino full-pretrain em planejamento. |
| Bare-metal ou vGPU? | Bare-metal em produção; vGPU em dev/test ou se VMware é mandato corporativo. |
| Service mesh? | Sim — Istio ou Linkerd. |

## Referências

- KServe v0.13+ (vLLM runtime): <https://kserve.github.io/website/>
- Red Hat OpenShift AI 2.x: <https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai>
- llm-d (KServe + vLLM multi-nó): <https://llm-d.ai/>
- Ray Serve LLM: <https://docs.ray.io/en/latest/serve/llm/serving-llms.html>
- NVIDIA AI Enterprise + NIM: <https://www.nvidia.com/en-us/data-center/products/ai-enterprise/>
- Cilium: <https://cilium.io/>
- Argo CD + Argo Rollouts: <https://argo-cd.readthedocs.io/>
- NVIDIA GPU Operator: <https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/>
- AMD ROCm Operator: <https://rocm.docs.amd.com/projects/k8s-device-plugin/>
