# Dimensionamento por Caso de Uso — 3 Cenários (P / M / G)

> Etapa 4/5 da proposta. Para cada um dos 5 casos P0 da Etapa 1 (chat interno, RAG corporativo, coding assistant, atendimento cliente, sumarização batch), 3 cenários de porte com hardware, throughput e CAPEX.

## Premissas de cálculo (todos os cenários)

- **Modelo "trabalho geral"**: Llama 3.3 70B Instruct AWQ-INT4 (≈40 GB VRAM) ou Qwen2.5-72B AWQ.
- **Modelo "raciocínio"**: DeepSeek-V3 / DeepSeek-R1 ou Qwen3-32B reasoning, conforme caso.
- **Modelo "embedding"**: BGE-M3 (568M) ou Granite-Embedding-278M.
- **Throughput de referência (vLLM 0.7+, H100 SXM 80GB, batch contínuo)**:
  - Llama 70B AWQ TP=2: **2.500–3.500 tokens/s agregado** (input+output) com 8–16 reqs concorrentes.
  - Llama 70B AWQ TP=4: **5.000–7.000 tokens/s agregado** com 32–64 reqs concorrentes.
  - Qwen2.5-Coder-32B AWQ TP=1 H100: **1.800–2.800 tokens/s** com 16 reqs.
  - BGE-M3 (em L40S 48GB): **~6.000 documentos/s** (chunks 512 tokens).
- **Taxas de uso assumidas**:
  - Chat interno: 60% dos usuários ativos diários, **15 mensagens/usuário/dia**, **800 tokens/mensagem** (in+out).
  - Coding assistant: 70% dos devs ativos, **150 completions/dia**, **400 tokens/completion**.
  - Atendimento: por conversa, **8 turnos**, **1.200 tokens/turno**, latência p95 < 4s.
  - Sumarização: por documento, **8.000 tokens entrada + 1.500 saída** ≈ **9.500 tokens/doc**.
  - RAG: queries que disparam embedding e geração; assumido **2.000 tokens/query** (resposta + contexto).

> Todos os valores de **CAPEX** são **estimativa pública** baseada em Etapa 4 §8 (`01-hardware-aceleracao.md`).

---

## CASO 1 — Chat interno (substituto privado do ChatGPT)

### Cenário P (Pequeno) — 500 usuários ativos

| Item | Valor |
|------|-------|
| Tokens/dia | ~3,6 M (300 ativos × 15 msg × 800 tok) |
| Pico (10× média durante 4h úteis) | ~250 tokens/s sustentados, picos ~1.000 tok/s |
| Modelo | Llama 3.3 70B Instruct AWQ-INT4 |
| GPUs | **2× L40S 48GB** (TP=2) ou **1× H100 NVL 94GB** ou **1× MI300X 192GB** |
| VRAM total | 96 GB ou 94 GB ou 192 GB |
| Servidor | 2× Xeon Gold 6448Y, 512 GB DDR5, 2× 3,84 TB NVMe |
| Storage local | 4 TB NVMe (modelos + cache) |
| Latência alvo | p50 < 1,5s (TTFT 400ms), p99 < 4s |
| CAPEX hardware | **US$ 80–110k** (1 servidor + GPU + rede 25/100G básica) |
| Notas | MIG (1×H100) habilita até 7 perfis para isolar testes |

### Cenário M (Médio) — 5.000 usuários ativos

| Item | Valor |
|------|-------|
| Tokens/dia | ~36 M |
| Pico | ~2.500 tok/s sustentado, picos 8.000 tok/s |
| Modelo | Llama 3.3 70B AWQ + Qwen2.5-Coder-32B (segundo modelo, multi-modelo via gateway) |
| GPUs | **8× H100 SXM 80GB** (1 servidor HGX) ou **8× MI300X** |
| VRAM total | 640 GB ou 1.536 GB |
| Servidor | DGX H100 ou HGX 8-way (2× Xeon Platinum, 2 TB DDR5, 30 TB NVMe) |
| Storage local | 30 TB NVMe |
| Rede | 2× 200G InfiniBand (preparado para crescer) |
| Latência alvo | p50 < 1s, p99 < 3s |
| CAPEX hardware | **US$ 320–420k** (1 servidor + rede + storage shared) |
| Notas | TP=4 para 70B com KV-cache amplo; sobra capacidade para coding e RAG |

### Cenário G (Grande) — 50.000 usuários ativos

| Item | Valor |
|------|-------|
| Tokens/dia | ~360 M |
| Pico | ~25.000 tok/s sustentado, picos 80.000 tok/s |
| Modelo | Multi-modelo (Llama 70B + Qwen 72B + reasoning + coding + embedding) |
| GPUs | **32–48× H200** (4–6 servidores HGX) ou **24× B200** (3 servidores HGX) |
| VRAM total | 4.512 GB (32× H200) |
| Servidor | 4× DGX H200 ou 3× DGX B200 + 2 nós para embedding/reranker (4× L40S) |
| Storage compartilhado | Weka ou VAST 300 TB para modelos + KV-cache + logs |
| Rede | InfiniBand NDR 400G (Spectrum-X aceitável) |
| Latência alvo | p50 < 800ms, p99 < 2,5s |
| CAPEX hardware | **US$ 2,2–3,5 M** (servidores + IB fabric + storage paralelo) |
| Notas | HA exige 2 sites; canary deploy via gateway. Próximo de **JPMorgan LLM Suite** (escala maior). |

---

## CASO 2 — RAG corporativo (plataforma habilitadora)

### Cenário P — 10M tokens indexados, 5k queries/dia

| Item | Valor |
|------|-------|
| Vetores | ~30k chunks (chunks de 300–400 tokens) |
| Queries/dia | 5.000 |
| Modelo gerador | Llama 3.3 70B AWQ (compartilhado com chat) |
| Modelo embedding | BGE-M3 |
| GPUs dedicadas | **1× L40S** (embedding + reranker) — gerador compartilhado com chat |
| Vector store | Qdrant single-node, 64 GB RAM, 500 GB NVMe |
| Storage | 1 TB NVMe (corpus + chunks + logs) |
| CAPEX adicional | **US$ 25–40k** (1 nó embed + Qdrant) |

### Cenário M — 100M tokens indexados, 100k queries/dia

| Item | Valor |
|------|-------|
| Vetores | ~300k chunks |
| Queries/dia | 100.000 (~1,2 query/s média, picos 10/s) |
| GPUs dedicadas | **2× L40S** (embedding) + **1× L40S** (reranker BGE-reranker-v2-M3) |
| Vector store | Qdrant cluster 3 nós (replicação=2), 128 GB RAM cada, 2 TB NVMe |
| Storage | 5 TB NVMe distribuído + 50 TB MinIO para corpus original |
| Notas | Modelo gerador permanece compartilhado com chat (CASO 1-M) |
| CAPEX adicional | **US$ 90–140k** (3 nós Qdrant + 3 GPUs L40S + storage) |

### Cenário G — 1B tokens indexados, 1M queries/dia

| Item | Valor |
|------|-------|
| Vetores | ~3M chunks |
| Queries/dia | 1.000.000 (~12 queries/s média, picos ~120/s) |
| GPUs dedicadas | **8× L40S** (embedding cluster) + **4× L40S** (reranker) ou **4× H100** se também for training |
| Vector store | Milvus cluster 6 nós (etcd + Pulsar + Querynode/Datanode), 256 GB RAM cada, 4 TB NVMe |
| Storage compartilhado | 200 TB MinIO/Ceph para corpus + 10 TB NVMe quente |
| Rede | 100G mínimo entre nós Milvus e GPUs (RoCE OK) |
| CAPEX adicional | **US$ 600–900k** (cluster Milvus + GPUs embed/rerank + storage) |
| Notas | A partir de ~500M tokens vale considerar **Vespa** ou **Elastic Enterprise** para hybrid search nativo |

---

## CASO 3 — Coding assistant (Continue/Tabby + Qwen2.5-Coder)

### Cenário P — 50 desenvolvedores

| Item | Valor |
|------|-------|
| Devs ativos/dia | 35 |
| Completions/dia | ~5.250 (35 × 150) |
| Tokens/dia | ~2,1 M |
| Modelo | Qwen2.5-Coder-32B AWQ (cabe em 1× H100 80GB) |
| GPUs | **1× H100 80GB** ou **2× L40S 48GB** TP=2 |
| Servidor | 1× HGX 1-2 GPU node, 256 GB RAM, 4 TB NVMe |
| Latência alvo | TTFT < 200ms para autocomplete; p99 < 1s |
| CAPEX | **US$ 60–90k** |
| Notas | Tabby cuidando de autocomplete; chat IDE via Continue.dev compartilha modelo de chat |

### Cenário M — 500 desenvolvedores

| Item | Valor |
|------|-------|
| Devs ativos/dia | 350 |
| Completions/dia | ~52.500 |
| Tokens/dia | ~21 M |
| Modelo | Qwen2.5-Coder-32B + Qwen3-Coder-Next 80B (3B ativos, MoE) para chat IDE |
| GPUs | **4× H100 SXM 80GB** (TP=2 para 32B, segundo TP=2 para 80B MoE) |
| Servidor | 1× HGX 4-GPU |
| Latência alvo | TTFT < 200ms, p99 < 1s |
| CAPEX | **US$ 160–220k** (servidor 4-GPU + storage) |
| Notas | Cache de prefixo do Tabby reduz latência drasticamente; SGLang RadixAttention vence aqui |

### Cenário G — 5.000 desenvolvedores

| Item | Valor |
|------|-------|
| Devs ativos/dia | 3.500 |
| Completions/dia | ~525.000 |
| Tokens/dia | ~210 M |
| Modelo | Qwen2.5-Coder-32B (autocomplete) + DeepSeek-Coder V2 ou Qwen3-Coder-Next 80B (chat) |
| GPUs | **16× H100/H200** distribuídas em 2 servidores HGX |
| Servidor | 2× DGX H200 |
| Storage | 50 TB NVMe + 200 TB shared (logs, embeddings de código) |
| Rede | NDR 400G IB ou Spectrum-X |
| CAPEX | **US$ 800k–1,2 M** |
| Notas | Próximo do que JPMorgan e Walmart relatam (assistente coding interno) |

---

## CASO 4 — Atendimento ao cliente (RAG + chat + guardrails pesados)

### Cenário P — 1.000 conversas/dia

| Item | Valor |
|------|-------|
| Tokens/dia | ~9,6 M (1k × 8 turnos × 1.200 tok) |
| Concorrência pico | ~10 conversas simultâneas |
| Modelo | Llama 3.3 70B AWQ ou Granite 3.x (Apache 2.0 ajuda compliance) |
| Guardrails | Llama Guard 3 8B + Presidio + reranker |
| GPUs | **2× H100 80GB** (gerador) + **1× L4** (Llama Guard) + **1× L4** (embed) |
| Servidor | 1× HGX 4-GPU node + 1× nó "guardrails" 2× L4 |
| Storage | 2 TB NVMe (KB + logs) + 20 TB MinIO (logs WORM) |
| CAPEX | **US$ 130–180k** |

### Cenário M — 10.000 conversas/dia

| Item | Valor |
|------|-------|
| Tokens/dia | ~96 M |
| Concorrência pico | ~80 simultâneas |
| Modelo | Llama 70B + modelo "raciocínio" para casos escalados (DeepSeek-R1 distill 32B) |
| GPUs | **8× H100 SXM** (1 servidor HGX) |
| Storage | 5 TB NVMe + 100 TB WORM logs |
| Rede | 100G interno; integração com CRM via VPN/MPLS |
| CAPEX | **US$ 380–500k** (servidor + integração + storage WORM) |

### Cenário G — 100.000 conversas/dia

| Item | Valor |
|------|-------|
| Tokens/dia | ~960 M |
| Concorrência pico | ~800 simultâneas |
| GPUs | **32× H200** ou **24× B200** distribuídas em 4 servidores HGX |
| Storage | Weka 100 TB hot + 1 PB MinIO/Ceph WORM logs |
| Rede | InfiniBand NDR 400G, Spectrum-X aceitável |
| HA | 2 sites ativo-ativo (DR exigência regulatória) |
| CAPEX | **US$ 2,8–4,5 M** |
| Notas | Próximo de Bradesco BIA/Itaú; integração com NLU legado e voicebots |

---

## CASO 5 — Sumarização batch (jurídico/contratual/clínico)

### Cenário P — 100 documentos/dia

| Item | Valor |
|------|-------|
| Tokens/dia | ~950k |
| Throughput exigido | ~100 docs em janela de 4h ≈ 7 docs/min ≈ 1.100 tokens/s |
| Modelo | Qwen2.5-72B AWQ (contexto 32k–128k) ou Llama 3.3 70B |
| GPUs | **2× H100** (TP=2) ou **2× L40S** TP=2 (com batch agressivo) |
| Servidor | 1× nó 2-GPU compartilhado com chat |
| CAPEX adicional | **US$ 40–70k** (raramente exige hardware dedicado) |
| Notas | Pode rodar à noite, compartilhando GPU com chat |

### Cenário M — 1.000 documentos/dia

| Item | Valor |
|------|-------|
| Tokens/dia | ~9,5 M |
| Throughput | ~12 docs/min = 1.900 tokens/s |
| GPUs | **4× H100** (TP=4) dedicadas ou compartilhadas com chat (M) |
| Storage | 5 TB NVMe + 50 TB MinIO (documentos + saídas) |
| CAPEX dedicado | **US$ 180–250k** se isolado |

### Cenário G — 10.000 documentos/dia

| Item | Valor |
|------|-------|
| Tokens/dia | ~95 M |
| Throughput | ~120 docs/min = 19.000 tokens/s sustentados |
| GPUs | **8× H200 dedicadas** ou batch off-peak no cluster maior |
| Storage | Weka/VAST 50 TB + 500 TB MinIO |
| Rede | Storage para GPU 100G suficiente; KV-cache local NVMe crítico |
| CAPEX dedicado | **US$ 500–700k** |
| Notas | Sumarização sempre se beneficia de **batch contínuo + prefix sharing** (SGLang); tipo de carga onde Stripe relatou −73% |

---

## CAPEX agregado por porte (tudo somado, sem duplicação por compartilhamento)

| Porte | Casos cobertos | GPUs efetivas | CAPEX hardware total estimado |
|-------|----------------|---------------|-------------------------------|
| **P (Pequeno)** | Chat 500 + RAG 10M + Coding 50 + Atend. 1k + Sumar. 100 | 4–8 | **US$ 250–450k** |
| **M (Médio)** | Chat 5k + RAG 100M + Coding 500 + Atend. 10k + Sumar. 1k | 16–24 | **US$ 1,5–2,8 M** |
| **G (Grande)** | Chat 50k + RAG 1B + Coding 5k + Atend. 100k + Sumar. 10k | 80–150 | **US$ 8–18 M** |

> A esses CAPEX **somar 25–35% para rede, storage compartilhado, racks, energia, software enterprise e implementação** — ver `09-energia-fisica.md` e Etapa 5 (ROI).

## CPU/RAM/Storage de referência por servidor GPU

| Componente | Mínimo | Recomendado | Justificativa |
|-----------|--------|-------------|---------------|
| CPU | 2× 32 cores | 2× 56 cores Xeon Platinum / EPYC Genoa | Pré-processamento, tokenização, vLLM frontend |
| RAM | 1 TB DDR5 | 2 TB DDR5 ECC | KV-cache offload, multi-modelo, cache de modelo |
| NVMe local | 8 TB | 30 TB (NVMe Gen4/5) | Múltiplos modelos quentes, KV-cache spill |
| NIC | 2× 100G | 2× 200G IB ou 2× 400G Ethernet | Tensor parallel + storage |
| Power | 4× 3 kW PSU redundantes | 6× 3 kW (B200) | Redundância n+1 |

## Principais armadilhas de dimensionamento

1. **Subdimensionar memória do servidor**: KV-cache pode exigir 100+ GB de DRAM para modelos grandes com offload.
2. **Subdimensionar NIC**: tensor parallel multi-nó com 25G mata throughput; 100G é mínimo, 200G+ é recomendado.
3. **Não reservar GPU para guardrails**: Llama Guard 3 8B + Presidio são contínuos e disputam GPU se mal isolados.
4. **Não reservar GPU para embedding**: cluster RAG com embedding compartilhado com chat sofre durante picos.
5. **Não dimensionar para canary**: precisa de **20–30% de capacidade ociosa** para rollouts seguros.
6. **Storage subdimensionado**: WORM logs em saúde/financeiro crescem rápido (1 GB/dia em chat médio).
