# Modelos Abertos para IA Local (2025-2026)

> Camada de modelos. Foco em pesos abertos com licenças usáveis em empresa. Detalhes de licenças e armadilhas comerciais consolidados em `11-licencas-modelos.md`.

## A. Modelos generalistas / chat

| Família | Tamanhos | Contexto | Pontos fortes | Licença | Onde brilha |
|---------|----------|----------|---------------|---------|-------------|
| **Llama 3.3** (Meta) | 70B | 128k | Inglês top, ampla compatibilidade de runtime | Llama 3.3 Community License | Substituto direto de modelos comerciais em inglês |
| **Llama 4 Scout** | 17B ativos / 109B total (MoE) | **10M** | Contexto extremo, multimodal nativo | Llama 4 Community License (700M MAU) | Documentos longos, RAG sem chunking pesado |
| **Llama 4 Maverick** | 17B ativos / 400B total (MoE) | 1M | Top em raciocínio MMLU Pro 80,5 / GPQA 69,8 | Llama 4 Community License | Substituto enterprise de modelos closed |
| **Llama 4 Behemoth** | 288B ativos / 2T total | (preview) | Frontier scale | Llama 4 Community License | Pesquisa, quem tem cluster H200 |
| **Qwen 2.5** (Alibaba) | 0.5B–72B | 128k | Multilíngue (PT-BR forte), instrução | Apache 2.0 (≥0,5B exceto 72B*) | Workhorse multilíngue empresarial |
| **Qwen 3** (Alibaba) | 0,6B – 235B (MoE com 22B ativos) | 128k–256k | Reasoning, agentes, code, multilíngue | Apache 2.0 | Topo open generalista, candidato preferencial PT-BR |
| **DeepSeek V3** | 671B total / 37B ativos (MoE) | 128k | Top open, custo de inferência baixo | MIT (modelo) + permissivo (uso comercial) | Quem tem hardware para MoE grande |
| **DeepSeek V3.1 / V3.2** | 671B total | 128k | Iteração de V3, melhor coding e function calling | MIT | Idem; contexto preservado |
| **DeepSeek R1** | 671B total / 37B ativos | 164k | Raciocínio (CoT longo); custo ~95% menor que o1 | MIT | Reasoning agents, math, code |
| **DeepSeek R1-0528** | (mai/2025 update) | 164k | JSON output, function calling | MIT | Workflows estruturados |
| **Mistral Large 2** (Large 24.07) | 123B | 128k | Inglês/francês, ferramentas | **MRL** (não comercial sem licença) | Use só com licença Mistral; senão evite |
| **Mistral Small 3 / 3.1** | 24B | 32k | Latência baixa, agentes | Apache 2.0 | Alternativa enterprise leve |
| **Mistral Devstral 2** | (variants) | — | Coding; versão laptop open | Mix (open + commercial) | Coding com ressalva de licença |
| **IBM Granite 3.x** | 2B / 8B / 13B / 34B | 128k | Enterprise, governança | Apache 2.0 | Áreas reguladas, watsonx.ai |
| **IBM Granite 4** | Nano 350M / Tiny 1B / Small 3B / Medium 7B + MoE | 128k+ | Hybrid Mamba-Transformer (~70% menos memória); **primeiro open com ISO/IEC 42001** | Apache 2.0 | Compliance-first deployments |
| **Phi 4** (Microsoft) | 14B (+ Phi-4-mini, Phi-4-multimodal) | 16k | Sintético-curado, edge corporativo, multimodal | MIT | Edge, on-device assistant |
| **Gemma 3** (Google) | 1B / 4B / 12B / 27B | 128k | Multilíngue (140+), pequeno, multimodal | Gemma Terms (Apache-like) | Edge multilíngue |
| **Gemma 4** (Google, abr/2026) | E2B / E4B / 26B MoE / 31B Dense | 128k+ | Multimodal (imagem+vídeo+áudio em E2B/E4B) | **Apache 2.0** | Edge moderno multimodal |
| **Nvidia Nemotron** (variants) | 22B – 340B | 128k | Reasoning, alinhamento NVIDIA | NVIDIA Open Model License | Quem usa NeMo/NIM |

\* Atenção: Qwen 2.5-72B foi lançado sob "Tongyi Qianwen License" (não Apache); Qwen 3 voltou todo a Apache 2.0.

## B. Modelos de código

| Modelo | Tamanho | Contexto | Pontos fortes | Licença |
|--------|---------|----------|---------------|---------|
| **Qwen 2.5-Coder** | 0,5B / 1,5B / 3B / 7B / 14B / 32B | 128k | SOTA open coding em 2024-25 | Apache 2.0 |
| **Qwen 3-Coder / Coder-Next 80B** | 80B (3B ativos MoE) | 256k | SOTA coding open 2026, agente | Apache 2.0 |
| **DeepSeek-Coder V2** | 16B (Lite) / 236B | 128k | Forte em multi-linguagem, FIM | MIT-like |
| **Granite-Code** | 3B / 8B / 20B / 34B | 8k–128k | Enterprise; trained on permissively-licensed code | Apache 2.0 |
| **StarCoder 2** (BigCode) | 3B / 7B / 15B | 16k | Treinado em "The Stack v2" auditado | BigCode Open RAIL-M (use comercial sim, com restrições éticas) |
| **Codestral 22B / 25.08** (Mistral) | 22B | 32k | Excelente fill-in-the-middle | **MNPL não-comercial** (Codestral) — proibido em produção sem licença paga |
| **Codestral Mamba** | 7B | 256k | Latência baixa, Mamba | Apache 2.0 |

## C. Modelos de embeddings

| Modelo | Dim | Multilíngue | MTEB | Licença | Notas |
|--------|-----|-------------|------|---------|-------|
| **BGE-M3** (BAAI) | 1024 | 100+ idiomas, até 8192 tokens | Top em retrieval/clustering | MIT | Workhorse multilíngue; suporta dense + sparse + multi-vector |
| **Qwen3-Embedding** (0,6B / 4B / 8B) | até 4096 | 100+ | **8B é #1 MTEB multilíngue (70,58)**; **80,68 em MTEB-Code** | Apache 2.0 | Estado-da-arte open jun/2025 |
| **Qwen3-VL-Embedding** | varia | sim | Multimodal | Apache 2.0 | RAG sobre imagens |
| **Granite Embedding** (107M / 278M, English & multilingual) | 384 / 768 | sim (variantes) | Forte em tarefas internas IBM, latência menor que peers de mesmo dim | **Apache 2.0** | Único open com ISO/IEC 42001 |
| **Nomic Embed Text V2** | 768 | 100 (MoE) | Forte em BEIR/MIRACL | Apache 2.0 | Primeiro embedding MoE |
| **E5 (multilingual-e5-large)** | 1024 | 100+ | Sólido | MIT | Tradicional, ainda relevante |
| **E5-Mistral-7B-Instruct** | 4096 | sim | Top em legacy MTEB | MIT | Custo alto (7B) |
| **Stella** | 1024 / 1536 | sim | ~57,45 média MTEB | MIT | Boa custo/perf |
| **NV-Embed-v2** (NVIDIA) | 4096 | sim | **Top no MTEB averaged abr/2026** | NVIDIA Open Model | Distribuído via NIM |
| **mxbai-embed-large** (Mixedbread) | 1024 | sim | Sólido, popular | Apache 2.0 | Generalista |

## D. Modelos de reranker

| Modelo | Tamanho | Notas | Licença |
|--------|---------|-------|---------|
| **BGE-reranker v2 (m3, gemma)** | 568M – 9B | Padrão self-host | Apache 2.0 |
| **Qwen3-Reranker** (0,6B / 4B / 8B) | até 8B | Estado-da-arte open 2026 | Apache 2.0 |
| **Jina Reranker v2** | base / multilingual | Forte multilíngue | Apache 2.0 (modelo) |
| **mxbai-rerank** | base / large | Boa custo/perf | Apache 2.0 |
| **Cohere Rerank 3** | (API) | Top mas API only — **não roda on-prem** | Proprietário |

## E. Modelos multimodais (visão e além)

| Modelo | Tamanho | Modalidades | Licença | Observações |
|--------|---------|-------------|---------|-------------|
| **Llama 3.2 Vision** | 11B / 90B | Texto + imagem | Llama 3.2 CL | Llama 3.2 Vision restrito UE; document VQA forte |
| **Llama 4 Scout/Maverick** | 17B/109B – 17B/400B MoE | Texto + imagem nativo | Llama 4 CL | UE: vision ainda restrita; multimodal nativo |
| **Qwen2-VL / Qwen2.5-VL / Qwen3-VL** | 2B – 72B | Imagem, vídeo, doc | Apache 2.0 (variantes) | Atual líder open multimodal; agentic UI |
| **Pixtral 12B / Pixtral Large** (Mistral) | 12B / 124B | Imagem | Apache 2.0 (Pixtral 12B); MRL (Large) | Forte instruction following |
| **InternVL 3 (até 78B)** | 1B–78B | Imagem, vídeo | Apache-like | +4 pts em multimodal reasoning vs v2 |
| **Phi-4-multimodal** | (multimodal variant) | Texto, áudio, imagem | MIT | Edge corporativo |
| **Gemma 3 / 4 (multimodal)** | 4B–31B | Imagem + áudio (Gemma 4 E2B/E4B) + vídeo | Apache 2.0 (Gemma 4) | Edge multimodal moderno |
| **NVLM / NV-VLM** | 72B | Imagem | NVIDIA Open Model | Servido via NIM |
| **GLM-4.6V** (Zhipu) | varia | Imagem | open | Subindo no benchmark 2026 |

## F. Modelos de raciocínio (reasoning)

- **DeepSeek-R1 / R1-0528** — referência open, 164k contexto, ~95% mais barato que o1 — **MIT**.
- **Qwen 3 reasoning variants** — modos `think` toggle in-context.
- **Granite reasoning variants** (IBM) — em watsonx.ai.
- **Mistral Magistral** — modelo de raciocínio Mistral 2025 (verificar licença).
- **OpenReasoner / OpenThinker** — comunidade, distilações de R1.

## G. Como mapear caso de uso → modelo

| Caso de uso (do Agente 1) | Modelos candidatos | Por quê |
|----------------------------|--------------------|---------|
| Chat interno seguro | Llama 3.3 70B, Qwen 3 32B/72B, Granite 4 Medium, Mistral Small 3 | Chat geral; Granite se compliance ISO 42001 importa |
| Embeddings + RAG | BGE-M3 ou Qwen3-Embedding-8B + BGE-reranker-v2 ou Qwen3-Reranker-4B | Estado-da-arte open + multilíngue |
| Coding assistant | Qwen 2.5-Coder 32B ou Qwen 3-Coder 80B; Granite-Code 34B; DeepSeek-Coder V2 | Codestral é proibido sem licença paga |
| Atendimento ao cliente (RAG) | Llama 3.3 70B, Qwen 3 70B, Granite 4 + reranker | Latência + qualidade |
| Sumarização longa | Llama 4 Scout (10M ctx), Qwen 3 235B, Granite 4 Hybrid | Contexto longo |
| Extração estruturada | Qwen 3 14-32B, Mistral Small 3, Granite 4 Small/Medium, DeepSeek R1-0528 (function calling) | JSON estruturado, schema |
| Análise de imagem (laudos, formulários) | Qwen3-VL, Llama 3.2 Vision, Pixtral, InternVL3 | Multimodal open |
| Reasoning / pareceres | DeepSeek R1, Qwen 3 (reasoning), Granite reasoning | CoT |

## Versões e datas-chave (2025-2026)

- Llama 4 Scout/Maverick: **abr/2025** (`<https://huggingface.co/blog/llama4-release>`)
- Qwen 3 + Qwen3-Embedding/Reranker: **jun/2025** (`<https://qwenlm.github.io/blog/qwen3-embedding/>`)
- DeepSeek R1: **20/jan/2025**; R1-0528: **mai/2025** (`<https://github.com/deepseek-ai/DeepSeek-R1>`)
- IBM Granite 4: **2025**; Granite 4 Nano: **out/2025** (`<https://www.ibm.com/granite/docs/models/granite>`)
- Phi-4: **2025** (`<https://azure.microsoft.com/en-us/products/phi>`)
- Gemma 3: **mar/2025**; Gemma 4: **abr/2026** (`<https://ai.google.dev/gemma/docs/core>`)

## Fontes principais

- BentoML "open source LLMs": <https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models>
- BentoML DeepSeek: <https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond>
- Llama 4 release: <https://huggingface.co/blog/llama4-release>
- Llama 4 license: <https://www.llama.com/llama4/license/>
- Qwen3 Embedding: <https://qwenlm.github.io/blog/qwen3-embedding/>
- IBM Granite 4: <https://www.ibm.com/new/announcements/ibm-granite-4-0-hyper-efficient-high-performance-hybrid-models>
- Granite 4 ISO 42001: <https://digital.nemko.com/news/ibm-granite-40-first-iso-42001-certified-open-source-ai>
- BentoML embeddings 2026: <https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models>
- BentoML vision 2026: <https://www.bentoml.com/blog/multimodal-ai-a-guide-to-open-source-vision-language-models>
- Mistral Codestral license (MNPL): <https://mistral.ai/news/mistral-ai-non-production-license-mnpl/>
