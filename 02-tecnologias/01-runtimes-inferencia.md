# Runtimes / Servidores de Inferência (2026)

> Camada 1 da stack (model server). Fonte de throughput, latência e custo. Em 2026 o mercado se consolidou em **vLLM** (padrão), com **SGLang** ganhando força em workloads RAG/multi-turn e **TensorRT-LLM** como ponta NVIDIA. O resto vive de POC, edge ou nichos.

## Tabela-resumo

| Runtime | O que é | Brilha em | Não brilha em | Maturidade | Licença | Versão atual |
|---------|---------|-----------|---------------|------------|---------|--------------|
| **vLLM** | Servidor de inferência com PagedAttention; OpenAI-compatible | Throughput em produção, multi-GPU, MoE (Llama 4), FP8 | Edge/CPU, GGUF nativo, modelos exóticos | Produção (V1 engine default desde v0.8) | Apache 2.0 | v0.19.0 (abr/2026) |
| **SGLang** | Runtime com RadixAttention (KV cache compartilhado por prefixo) | RAG, few-shot, multi-turn (até 6,4× sobre engines sem prefix sharing); 16,2k tok/s vs 12,5k vLLM em Llama 3.1 8B | Casos sem prefixo compartilhado significativo | Produção | Apache 2.0 | série 0.4.x |
| **TensorRT-LLM** | Compilador NVIDIA + runtime; gera engines otimizadas | NVIDIA H100/H200/B200, FP8 nativo, baixa latência | Vendor lock-in NVIDIA, build complexo, modelos novos demoram | Produção (NVIDIA) | Apache 2.0 (binários NVIDIA proprietários no NIM) | TRT-LLM 0.18+ |
| **TGI (HF)** | Text Generation Inference, da Hugging Face | Integração HF, multi-modal, simples | Throughput perdeu para vLLM em 2024-25 | Produção mas em 2º plano | HFOIL (após v2; restritiva acima de receita) | v3.x |
| **LMDeploy** | Stack chinesa (InternLM/MMRazor); TurboMind engine | Latência baixa, INT4/INT8 fortes, modelos InternLM/Qwen | Comunidade ocidental menor | Produção | Apache 2.0 | v0.7.x |
| **llama.cpp** | C++/ggml; quantização GGUF; CPU + GPU | CPU-only, Apple Silicon, edge, single-user; quantização agressiva (Q2_K..Q8_0) | Concorrência (não tem batching contínuo equivalente a vLLM) | Produção (POCs/edge) | MIT | tip-of-tree (releases mensais) |
| **Ollama** | Wrapper sobre llama.cpp + UX, modelfile, library | Setup em 30s, dev local, pequenas equipes | Multi-tenant produção (~3,2× lento vs vLLM), GPU sharing | Produção (POC/dev) | MIT | v0.5+ |
| **llamafile** | Mozilla; binário único auto-contido (Cosmopolitan) | Distribuição zero-deps, demo, air-gapped | Produção corporativa multi-GPU | Beta/produção (ferramenta) | Apache 2.0 | jul/2024+ |
| **MLC-LLM** | Compila modelos para device (web, mobile, RTX) | Cliente, navegador (WebGPU), mobile | Servidor multi-tenant | Produção (cliente) | Apache 2.0 | v0.18+ |
| **mistral.rs** | Runtime Rust, foco em quantização exótica e ISQ | Single-node, Rust-friendly, exploração | Comunidade pequena | Beta | MIT | v0.6+ |
| **candle** | Framework HF Rust (não é só inferência) | Embedding em apps Rust | Server full-feature | Beta/produção (lib) | Apache 2.0 | v0.9+ |
| **Ray Serve / KubeRay** | Camada de serving distribuído (Anyscale) | Multi-modelo, multi-nó, prefill-decode disagg., wide-EP | Sobrecarga para single-model single-node | Produção | Apache 2.0 | Ray 2.40+ |
| **KServe** | CRD InferenceService no Kubernetes | Padrão Kubeflow para autoscaling, canary, routing | Ainda exige conhecimento de K8s | Produção | Apache 2.0 | v0.14+ |

## Detalhamento

### vLLM
- **O que é**: servidor de inferência open source criado em UC Berkeley com **PagedAttention** (gerência de KV cache estilo paginação); API OpenAI-compatible (`/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`).
- **V1 Engine (default desde v0.8.0, jan/2025)**: rewrite que entrega **1,7× throughput sobre V0**, integra **FlashAttention 3**, prefix caching com <1% de overhead em 0% hit rate, comunicação scheduler-worker incremental. Testes recentes em 2× H100 com GPT-OSS-120B atingiram **4.741 tok/s a 100 reqs concorrentes**.
- **Quando usar**: produção, throughput, autoscaling, MoE (Llama 4 Scout/Maverick), suporte FP8 nativo (H100/H200), tensor/pipeline parallel.
- **Quando NÃO**: workloads single-user CPU/Apple, modelos sem suporte upstream ainda (raro), GGUF nativo (limitado).
- **Integrações**: KServe, Ray Serve, NVIDIA NIM, Red Hat AI Inference Server (que é um **vLLM hardened**), llm-d (multi-nó), LiteLLM como gateway.
- **Links**: <https://github.com/vllm-project/vllm> · <https://blog.vllm.ai/> · <https://docs.vllm.ai/>

### SGLang
- **O que é**: alternativa moderna ao vLLM, criada pelo time LMSYS; principal inovação é **RadixAttention** — armazena KV cache em árvore radix, reusando ativações entre requisições com prefixo comum.
- **Diferencial**: em RAG, few-shot e multi-turn, **até 6,4× a throughput** sobre runtimes sem prefix sharing. Em Llama 3.1 8B em H100, **~16,2k tok/s vs 12,5k do vLLM** (29% acima).
- **Quando usar**: agentes multi-turn, RAG com prefixos longos repetidos, classificação few-shot.
- **Quando NÃO**: workloads sem prefix sharing, alta concorrência onde vLLM (V1 com routing C++) escala melhor.
- **Links**: <https://github.com/sgl-project/sglang>

### TensorRT-LLM
- **O que é**: compilador NVIDIA que gera "engines" otimizados a partir de modelos PyTorch/HF, integrado ao Triton.
- **Quando usar**: H100/H200/B200 com FP8 nativo, requisitos de latência mais baixos, NIM em produção.
- **Quando NÃO**: AMD/Intel (vendor lock), times sem expertise NVIDIA, prototipagem rápida.
- **Integrações**: Triton Inference Server, NVIDIA NIM (entrega TRT-LLM como microserviço empacotado).
- **Links**: <https://github.com/NVIDIA/TensorRT-LLM> · <https://nvidia.github.io/TensorRT-LLM/>

### TGI (Text Generation Inference)
- **O que é**: servidor da Hugging Face, foi referência em 2023-24.
- **Status 2026**: perdeu protagonismo para vLLM. Continua relevante quando o time já vive no ecossistema HF (Spaces, Inference Endpoints).
- **Armadilha de licença**: a partir de v2, mudou para **HFOIL** (Hugging Face Optimized Inference License) que tem cláusulas comerciais (especificamente para grandes provedores). Auditar antes de produção.
- **Links**: <https://github.com/huggingface/text-generation-inference>

### LMDeploy
- **O que é**: stack chinesa, com motor TurboMind (CUDA) e PyTorch backends. Forte em quantização (W4A16, KV cache INT8/INT4).
- **Quando usar**: ambientes Qwen / InternLM, latência crítica.
- **Links**: <https://github.com/InternLM/lmdeploy>

### llama.cpp
- **O que é**: implementação C++ do Llama por Georgi Gerganov; introduz GGUF, motor ggml. Roda quantização Q2..Q8 muito eficiente.
- **Quando usar**: edge, dev local, Apple Silicon, single-user, demos air-gapped, ARM. Suporte multimodal (LLaVA, Qwen2-VL etc.) via mmproj.
- **Quando NÃO**: produção multi-tenant; não tem **continuous batching** equivalente a vLLM; throughput muito inferior.
- **Links**: <https://github.com/ggml-org/llama.cpp>

### Ollama
- **O que é**: wrapper sobre llama.cpp + biblioteca de modelos (`ollama pull llama3.3`) + API local.
- **Status**: ferramenta favorita para POC e dev. Em produção corporativa, substituído por vLLM (3,2× mais throughput segundo Agente 1).
- **Integração comum**: Open WebUI fala com Ollama nativamente; Continue.dev/Cline também.
- **Links**: <https://ollama.com/> · <https://github.com/ollama/ollama>

### llamafile
- **O que é**: projeto Mozilla; combina llama.cpp + Cosmopolitan Libc num executável único multi-OS.
- **Quando usar**: distribuição offline, demos, air-gapped extremo.
- **Links**: <https://github.com/Mozilla-Ocho/llamafile>

### MLC-LLM
- **O que é**: compila LLMs para qualquer hardware (WebGPU, Vulkan, Metal, CUDA, ROCm) usando TVM.
- **Quando usar**: clientes web/mobile (browser-side LLM), apps desktop sem GPU server.
- **Links**: <https://github.com/mlc-ai/mlc-llm>

### mistral.rs e candle
- Runtimes Rust. Útil para apps embarcados em servidores Rust ou pipelines tipo API Gateway com inferência local. Não substitutos de vLLM em produção.
- **Links**: <https://github.com/EricLBuehler/mistral.rs> · <https://github.com/huggingface/candle>

### Ray Serve / KubeRay
- **O que é**: framework de serving distribuído da Anyscale, com primitivas para data-parallel attention, expert parallelism, **prefill-decode disaggregation** e roteamento prefix-aware.
- **Quando usar**: clusters multi-modelo, multi-nó, observados ganhos de **3× output tok/s e 2× redução de TTFT** com prefix-cache aware routing.
- **Integração**: Ray Serve LLM usa **vLLM por baixo**; KubeRay roda em K8s.
- **Links**: <https://docs.ray.io/en/latest/serve/index.html> · <https://www.anyscale.com/blog/ray-serve-llm-anyscale-apis-wide-ep-disaggregated-serving-vllm>

### KServe
- **O que é**: CRD `InferenceService` no Kubernetes, parte do ecossistema Kubeflow. Faz autoscaling, canary, routing, transformação.
- **Quando usar**: stack Kubernetes corporativa que já roda Knative ou similar; padrão usado no OpenShift AI.
- **Integração**: roda **vLLM** ou **Triton** como runtime backend.
- **Links**: <https://kserve.github.io/website/> · <https://docs.vllm.ai/en/stable/deployment/integrations/kserve/>

### llm-d
- **O que é**: extensão da vLLM para inferência distribuída em K8s. É o caminho oficial para multi-nó vLLM endossado pelo projeto.
- **Quando usar**: modelos que excedem 1 nó (Llama 4 Maverick 400B, DeepSeek V3 671B), workloads heterogêneas.
- **Integração**: combina vLLM + KServe + roteamento prefix-aware.
- **Links**: <https://llm-d.ai/>

## Comparativo de throughput (referência H100, Llama 3.1 8B, abr/2026)

| Engine | Tok/s relativo | Quando vence |
|--------|----------------|--------------|
| SGLang | 16,2k (1,29×) | Multi-turn, RAG, prefix sharing |
| vLLM V1 | 12,5k (1,00×) | Concorrência alta, MoE, baseline produção |
| TensorRT-LLM | ~13–14k (variável) | NVIDIA puro, FP8, latência baixa |
| LMDeploy | ~12–13k | Quantização agressiva |
| TGI | ~9–10k | Contexto HF |
| Ollama (llama.cpp) | ~3–5k | Single-tenant POC |

## Quantização típica em 2026

| Método | Bits | Hardware ideal | Qualidade vs FP16 | Uso |
|--------|------|----------------|-------------------|-----|
| **FP8** (E4M3 / E5M2) | 8 | H100/H200/B200 (nativo) | -0,3 a -0,5 pt | Default produção 2026 |
| **INT8 (SmoothQuant)** | 8 | A100, MI300X | -0,5 a -0,9 pt | Quando não há FP8 nativo |
| **AWQ** | 4 | H100/A100/L40S/4090 | -1 a -1,5 pt | Quando memória aperta; AWQ v1.8+ tem FP8 |
| **GPTQ** | 4 | H100/MI300X (v2.3+) | -1,5 a -2 pt | Alternativa a AWQ |
| **GGUF Q4_K_M** | ~4,5 | CPU + GPU consumer | -2 pt | Edge / llama.cpp |

## Links centrais

- vLLM benchmarks 2026: <https://www.morphllm.com/vllm-benchmarks>
- SGLang vs vLLM 2026: <https://particula.tech/blog/sglang-vs-vllm-inference-engine-comparison>
- vLLM vs TensorRT-LLM vs SGLang H100: <https://www.spheron.network/blog/vllm-vs-tensorrt-llm-vs-sglang-benchmarks/>
- Red Hat AI Inference Server (vLLM hardened): <https://developers.redhat.com/products/red-hat-ai/inference-server>
- llm-d: <https://llm-d.ai/>
- AWQ guide 2026: <https://www.spheron.network/blog/awq-quantization-guide-llm-deployment/>
- Quantização tradeoffs: <https://www.digitalapplied.com/blog/quantization-tradeoffs-4bit-8bit-fp8-performance-data>
