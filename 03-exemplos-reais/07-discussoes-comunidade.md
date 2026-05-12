# Discussões de Comunidade — Reddit, HN, fóruns vLLM

> Síntese qualitativa de threads e posts de prática real (2024–maio/2026) que documentam **deployments efetivos** mais do que materiais de marketing. Este capítulo é deliberadamente **mais curto e qualitativo** — comunidade não é fonte primária, mas é onde armadilhas operacionais aparecem.

## Padrões recorrentes em r/LocalLLaMA + Hacker News

### 1. Escolha de runtime: vLLM venceu, mas com curva
- vLLM é claramente o padrão de produção em 2024–2026 (citações repetidas em SitePoint, Lyceum, Spheron, Introl, Nebius).
- **Curva**: GPU drivers + CUDA versions + quantization formats + multi-GPU orchestration. Nada plug-and-play como Ollama.
- **Citação recorrente**: "Upgrading vLLM is worthwhile, but won't rescue a misconfigured deployment."
- **SGLang** ganha terreno em RAG/multi-turn por RadixAttention (prefix sharing).

### 2. GPU sizing: erro mais comum
- Achar que se pode usar **100% da VRAM**. Na prática, driver + PyTorch + vLLM runtime reservam **2–4 GB**.
- VRAM se decompõe em: **Model Weights + KV Cache + Activations + Framework Overhead**.
- Configuração default sugerida: `gpu-memory-utilization=0.90`; reduzir para `0.85` se OOM em pico.
- **Anti-padrão**: dedicar uma GPU inteira a um modelo com tráfego intermitente — utilização de cluster cai a ~40%.

### 3. Networking & storage
- **Modelo grande em NFS = bottleneck**. Trocar para **LVM persistent volumes locais** acelera, mas cria affinity rígida (single hardware failure = manual reschedule).
- **Round-robin é ineficiente para LLM** porque ignora KV-cache localizada por GPU. Soluções: prefix-aware routing (llm-d, vLLM Production Stack).

### 4. Quantização em produção
- **AWQ-INT4** e **GPTQ-INT4** dominam para 70B-class em 1×H100 ou 2×L40S.
- **FP8** ganha tração em H100/H200.
- **Trade-off real**: ~1–3% de qualidade vs. ~50–60% de memória poupada.

### 5. Stripe (citação muito repetida em comunidade)
- "73% inference cost reduction via vLLM migration; 50M daily API calls on 1/3 the GPU fleet."
- Fonte primária Stripe não localizada em nossa pesquisa — citação é **second-hand consistente**, não verificada.

## Padrões recorrentes em r/LocalLLaMA (qualitativo)

- **Tema 1**: "Qual modelo para 1×H100 (80GB)?" — resposta evolui de Llama 3 70B para **Llama 3.3 70B AWQ**, **Qwen 2.5 72B**, **DeepSeek V3 quantized** ao longo de 2024–2026.
- **Tema 2**: "Coding local que rivaliza com Copilot" — convergência em **Qwen2.5-Coder 32B** (e em 2026 Qwen3-Coder-Next 80B com 3B ativos), **DeepSeek-Coder V2**, e **Granite-Code 34B** para regulados.
- **Tema 3**: "Frontend chat enterprise" — Open WebUI domina por SSO/OIDC; LibreChat ganha onde precisa LDAP; AnythingLLM ganha em RAG por workspace.
- **Tema 4**: "Vector store self-host que aguenta produção" — Qdrant lidera; pgvector OK até ~10M; Milvus em deploys multi-bilhão.
- **Tema 5**: "Como rodar 405B on-prem" — caro; recomendação prática é Llama 3.3 70B ou MoEs (Llama 4 Scout/Maverick) que ativam menos parâmetros.

## Hacker News — discussões relevantes

- **Posts de Anyscale (Ray Serve LLM)** sobre custo total de inferência apontam que **maior parte do TCO** vem de utilização (não preço da GPU).
- **Posts da Cloudflare/Together.ai** sobre roteamento inteligente: 30–50% economia ao rotear queries simples para modelos pequenos.
- **DeepSeek V3 launch** dominou HN em dez/2024–jan/2025 — caso de mercado que mostrou que open + barato + bom é viável.
- **Llama 4 launch** (abr/2024) trouxe debates sobre **licença Llama Community License com cláusula 700M MAU** — deal-breaker para algumas empresas grandes.

## Threads relevantes / blogs de prática

- AI21 — "Go big or go OOM: the art of scaling vLLM" (lições reais de batching, max-model-len).
- llm-d.ai — "Production-Grade LLM Inference at Scale with KServe, llm-d, and vLLM" (multi-nó vLLM).
- DigitalOcean — "How to Choose the Right GPU for vLLM Inference" (sizing prático).
- VMware Cloud Foundation Blog — "LLM Inference Sizing and Performance Guidance" (calculadoras de TCO).
- Databasemart — "vLLM Optimization Guide: How to Avoid Performance Pitfalls" (multi-GPU).

## Síntese qualitativa

- **Convergência forte para vLLM** como runtime padrão em produção on-prem.
- **Modelos open de labs especializados** (Llama, Qwen, DeepSeek, Mistral, Granite) batem **modelos open de vendors SaaS** (DBRX, Arctic) em qualidade prática.
- **Erro mais comum**: subdimensionar GPU (memória) e overdimensionar GPU (utilização baixa por tráfego intermitente). Os dois ao mesmo tempo.
- **Erro mais caro**: round-robin em load balancer ignora KV-cache.
- **Erro de governança** que a comunidade levanta menos que devia: **retrieval sem ACL** (LLM08 do OWASP).

## Fontes consultadas (consolidadas)

- ✅ <https://www.sitepoint.com/vllm-production-deployment-guide-2026/>
- ✅ <https://lyceum.technology/magazine/vllm-production-deployment-guide-2026/>
- ✅ <https://www.spheron.network/blog/vllm-production-deployment-2026/>
- ✅ <https://introl.com/blog/vllm-production-deployment-inference-serving-architecture>
- ✅ <https://www.ai21.com/blog/scaling-vllm-without-oom/>
- ✅ <https://llm-d.ai/blog/production-grade-llm-inference-at-scale-kserve-llm-d-vllm>
- ✅ <https://www.digitalocean.com/community/conceptual-articles/vllm-gpu-sizing-configuration-guide>
- ✅ <https://blogs.vmware.com/cloud-foundation/2024/09/25/llm-inference-sizing-and-performance-guidance/>
- ✅ <https://www.databasemart.com/blog/vllm-distributed-inference-optimization-guide>
- ✅ <https://nebius.com/blog/posts/serving-llms-with-vllm-practical-guide>
- ⚠️ Stripe vLLM (–73% inferência, 50M/dia) — citação repetida; fonte primária Stripe não localizada.
