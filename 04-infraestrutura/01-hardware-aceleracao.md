# Hardware de Aceleração — Comparativo (Maio/2026)

> Etapa 4/5 da proposta. Comparativo de aceleradores para inferência e fine-tune de LLMs em ambiente corporativo on-premises.

## 1. Posicionamento de mercado em 2026

- **NVIDIA continua dominante (~85% do mercado de aceleradores para IA)** mas AMD e Intel ganharam tração concreta em 2025/2026.
- **Hopper (H100/H200)** é a "espinha dorsal" de praticamente todos os deployments enterprise de produção em 2026.
- **Blackwell (B100/B200/GB200)** começou a chegar em volume no 2º semestre de 2025; em maio/2026 já está em fila de entrega para Tier-1, mas com **lead time de 6–9 meses** ainda comum e **DLC obrigatório** acima de 4 GPUs/servidor.
- **AMD MI300X/MI325X**: maturidade de vLLM em ROCm 6.x consolidada; MI355X (CDNA4) lançada em 2025 entrega vRAM e bandwidth competitivos com B200 a custo geralmente 20–30% menor.
- **Intel Gaudi 3**: bom custo/token em inferência específica, mas **ecossistema (SynapseAI) ainda atrás** de CUDA e ROCm para casos não-Llama/não-Mistral.

## 2. NVIDIA — comparativo das SKUs relevantes

| GPU | Arquitetura | VRAM | BW memória | FP16/BF16 (TFLOPS dense) | FP8 (TFLOPS dense) | NVLink | TDP | Lançamento | Preço público estimado (USD) |
|------|-------------|------|------------|--------------------------|---------------------|--------|-----|-----------|------------------------------|
| **H100 SXM** | Hopper | 80 GB HBM3 | 3,35 TB/s | ~990 | ~1.979 | NVLink 4 (900 GB/s) | 700 W | 2022 | 25–35k (canal corporativo) |
| **H100 NVL (PCIe)** | Hopper | 94 GB HBM3 | 3,9 TB/s | ~1.671 | ~3.341 | bridge 600 GB/s | 400 W | 2023 | 30–40k |
| **H200 SXM** | Hopper | 141 GB HBM3e | 4,8 TB/s | ~990 | ~1.979 | NVLink 4 (900 GB/s) | 700 W | 2024 | 30–40k |
| **B100 SXM** | Blackwell | 192 GB HBM3e | 8 TB/s | ~1.800 | ~3.500 | NVLink 5 (1,8 TB/s) | 700 W | 2024 | ~35k (raro fora HGX) |
| **B200 SXM** | Blackwell | 192 GB HBM3e | 8 TB/s | ~2.250 | ~4.500 | NVLink 5 (1,8 TB/s) | 1.000 W | 2024 | 40–50k (estimativa) |
| **GB200 NVL72** | Blackwell + Grace | 13,5 TB total (rack) | — | rack-scale | rack-scale | rack NVLink 5 | ~120 kW/rack | 2024 | US$ 3–4 M /rack (estimativa) |
| **L40S** | Ada | 48 GB GDDR6 | 864 GB/s | ~362 | ~733 | sem NVLink | 350 W | 2023 | 8–11k |
| **L4** | Ada | 24 GB GDDR6 | 300 GB/s | ~121 | ~242 | sem NVLink | 72 W | 2023 | 2,5–3k |
| **RTX PRO 6000 Blackwell** | Blackwell | 96 GB GDDR7 | 1,8 TB/s | ~500 | ~1.000 | sem NVLink | 600 W | 2025 | 8–10k |

### Observações práticas

- **H100/H200 é o "ponto doce" de produção em 2026**: ROI já mapeado, vLLM 100% otimizado, oferta secundária estável.
- **B200**: ganho real de **~2× tokens/s vs H100** em modelos densos 70B, mas exige **DLC** (ar não suporta 1 kW/GPU em rack denso) e re-engenharia de DC. Justifica-se a partir do médio porte.
- **L40S**: melhor opção em **inferência single-tenant pequena** ou modelos ≤70B AWQ; sem NVLink, então tensor-parallel além de 2 GPUs sofre.
- **L4**: viável para **embedding e reranker dedicados**, **Llama Guard 3 8B**, ou **edge** (filiais).
- **RTX PRO 6000 Blackwell** é a estrela "estação de trabalho/pequeno servidor" em 2026: 96 GB GDDR7 cabe Llama 70B AWQ com folga, 600 W aceita ar; alternativa boa para POC e dev.
- **MIG (Multi-Instance GPU)**: H100/H200 e B200 suportam até 7 instâncias por GPU. Útil em chat interno ocioso para multi-tenancy.

## 3. AMD — MI300X / MI325X / MI355X

| GPU | Arquitetura | VRAM | BW memória | FP16/BF16 (TFLOPS dense) | FP8 (TFLOPS dense) | Interconnect | TDP | Lançamento | Preço público estimado (USD) |
|------|-------------|------|------------|--------------------------|---------------------|--------------|-----|-----------|------------------------------|
| **MI300X OAM** | CDNA3 | 192 GB HBM3 | 5,3 TB/s | ~1.307 | ~2.615 | Infinity Fabric (896 GB/s) | 750 W | 2023 | 15–20k |
| **MI325X OAM** | CDNA3 | 256 GB HBM3e | 6 TB/s | ~1.307 | ~2.615 | Infinity Fabric (896 GB/s) | 1.000 W | 2024 | 18–25k |
| **MI355X (CDNA4)** | CDNA4 | 288 GB HBM3e | 8 TB/s | ~2.300 | ~4.600 | Infinity Fabric Gen5 | 1.000 W | 2025 | 25–30k (estimativa) |

### Maturidade ROCm + vLLM (maio/2026)

- **vLLM em ROCm 6.x: production-ready** para Llama 3.x/4, Qwen 2.5/3, Mistral, Granite, DeepSeek. Performance dentro de 5–15% do equivalente CUDA em FP16/FP8.
- **SGLang em ROCm**: experimental para alguns modelos; vLLM é a aposta segura.
- **AWQ/GPTQ**: suportados; **FP8 (OCP) nativo** em CDNA3+ via Quark.
- **Pontos fracos**: depuração mais difícil, ecossistema TensorRT-LLM ausente, poucas referências enterprise BR/EU. Casos públicos: **Microsoft Azure (MI300X em produção desde 2024), Meta, Oracle OCI**.
- **Vantagem da VRAM**: MI300X com 192 GB cabe **Llama 3.1 405B FP8 em uma única GPU**, algo que H100 não faz. Isso reduz drasticamente custo por modelo em frontier-class.

### Quando escolher AMD

- Empresa com cláusula de "second source" obrigatória (defesa, governo).
- Workload conhecido (Llama 70B-405B em vLLM); sem necessidade de TensorRT-LLM.
- Pressão de custo: MI300X **~30–40% mais barata por GB de HBM** que H100/H200.
- Equipe com maturidade Linux/HPC; tolera depuração em ROCm.

## 4. Intel — Gaudi 3

| Acelerador | VRAM | BW memória | TFLOPS BF16 | TDP | Interconnect | Preço público estimado (USD) |
|------------|------|------------|-------------|-----|--------------|------------------------------|
| **Gaudi 3** | 128 GB HBM2e | 3,7 TB/s | ~1.835 | 900 W | 24× 200 GbE on-chip (RoCE) | ~16k (HLB-325 server cards) |

### Maturidade SynapseAI

- vLLM-fork da Intel (vllm-fork em GitHub) com cobertura para **Llama, Mistral, Mixtral, Qwen, Falcon, Granite**. Lag de 1–2 releases atrás do upstream.
- **Vantagem econômica**: Dell/Supermicro vendem servidor 8× Gaudi 3 por **~US$ 125–155k**, contra **US$ 280–350k** para 8× H100. Custo/token ~50% menor em workloads cobertos.
- **Pontos fracos**: ecossistema (compiler/profiler) ainda menor que CUDA/ROCm; suporte TGI/SGLang limitado; menor liquidez em mercado secundário.
- **Caso público**: IBM Cloud oferece Gaudi 3 como opção em watsonx.

## 5. Aceleradores especiais

### 5.1 Cerebras Wafer-Scale (WSE-3 / CS-3)

- Wafer único de 900k cores, 44 GB SRAM on-chip + 1,2 PB MemoryX externa.
- **Inferência ultra-rápida (2.000+ tokens/s em Llama 3.1 70B)**, batch=1.
- **On-prem viável**: Mayo Clinic e G42 são clientes; CAPEX por sistema CS-3: **US$ 2,5–3 M+** (estimativa pública).
- **Quando faz sentido on-prem**: cargas de **baixa latência extrema** (real-time voice agents, streaming code completion sub-100ms TTFT) em escala única.
- **Quando NÃO faz sentido**: chat genérico — desperdiça arquitetura.

### 5.2 Groq LPU

- **Cloud-only** em 2026 (GroqCloud). Não há SKU on-prem de produção. Excluir do escopo on-prem corporativo.

### 5.3 SambaNova SN40L

- Reconfigurable Dataflow Unit, 1,5 TB de memória por sistema.
- **On-prem disponível** via "DataScale" (rack completo). Casos: gov/defesa US.
- CAPEX: **US$ 3–5 M /rack** (estimativa pública).
- Nicho: cargas com **muitos modelos co-residentes** (até 1.000 modelos servidos do mesmo rack via swap rápido).

### 5.4 Apple Silicon (M3 Ultra / M4 Ultra Mac Studio)

- Mac Studio M3 Ultra com 512 GB unified memory: **viável para POC e desenvolvedor individual**. Llama 70B AWQ roda em ~20–25 tok/s.
- **NÃO é solução de produção corporativa** (sem multi-tenancy nativo, sem rack form-factor, suporte enterprise inexistente).
- Útil como **estação de dev** em times pequenos.

## 6. CPU-only (llama.cpp + AMX/AVX-512)

Em 2026 é viável para **modelos pequenos/quantizados** em CPU moderna:

| CPU | Cores | RAM máx | Throughput estimado Llama 8B Q4 | Caso de uso |
|-----|-------|---------|----------------------------------|-------------|
| **Intel Xeon 6 (Granite Rapids)** | 64–128 P-cores + AMX | 6–8 TB DDR5-6400 MRDIMM | 20–40 tok/s (bsz=1) | Edge, fallback, POC |
| **AMD EPYC 9005 "Turin"** | 96–192 cores | 6 TB DDR5-6000 | 15–35 tok/s | Idem |

- **Quando vale**: filiais sem GPU, agente local em workstation, fallback de DR.
- **Quando NÃO vale**: produção multi-usuário; 1 GPU H100 entrega 30–100× o throughput de uma CPU Xeon top em modelos 70B.

## 7. Tabela-síntese: GPU recomendada por carga

| Carga | GPU recomendada (1ª escolha) | Alternativa anti-lock-in | Por quê |
|-------|------------------------------|---------------------------|---------|
| Chat interno < 5k usuários | **2–4× L40S** ou **2× H100 NVL PCIe** | 2× MI300X | VRAM 48–80GB suficiente para 70B AWQ; sem NVLink crítico |
| Chat interno 5k–25k | **4–8× H100 SXM** ou **4× H200** | 4× MI300X | NVLink necessário p/ TP=4 em 70B FP16/AWQ |
| Chat interno 25k+ | **8× H200** ou **8× B200** | 8× MI325X | Throughput agregado, MIG p/ multi-tenancy |
| RAG embeddings dedicado | **1–2× L40S** ou **L4** | 1× MI210 | BGE-M3 cabe em 24–48GB |
| Reranker | **L4** ou **L40S** | RX 7900 XTX (lab) | Qwen3-Reranker 8B leve |
| Coding assistant 500–5k devs | **4–8× H100** | 4× MI300X | Qwen2.5-Coder-32B AWQ + cache de prefixo |
| Sumarização batch grande | **2–4× H100** ou **L40S** | 2× MI300X | Throughput > latência |
| Fine-tune QLoRA 70B | **4–8× H100** ou **MI300X** | Gaudi 3 8× | VRAM > 120GB total |
| Fine-tune full 70B | **DGX 8× H200** ou **HGX 8× B200** | 8× MI325X | Memória + interconnect |
| Frontier 405B serving | **8× H200** ou **8× MI300X** | — | 405B FP8 cabe em 8×141GB ou 1×192GB |
| Frontier 405B fine-tune | **DGX SuperPOD (32+ GPUs)** | — | InfiniBand NDR + paralelismo 3D |

## 8. CAPEX típico de servidor GPU 8-way (estimativa pública, maio/2026)

| Plataforma | CAPEX por servidor (USD) | Inclui | Notas |
|-----------|---------------------------|--------|-------|
| **DGX H100** (8× H100 SXM, 2 TB RAM, 30 TB NVMe) | 280–350k | Suporte NVIDIA enterprise | Lead time 4–8 semanas (estável em 2026) |
| **DGX H200** (8× H200 SXM) | 320–400k | Idem | "H100++" |
| **DGX B200** (8× B200 SXM) | 500–650k | DLC inclusa em rack-scale | Exige DC preparado |
| **HGX H100/H200 (Supermicro/Dell/Lenovo)** | 230–320k | Sem suporte premium NVIDIA | Mais flexível, integração via parceiro |
| **HGX B200 (3rd party)** | 450–580k | DLC obrigatório | Lead time 6–9 meses ainda em mai/2026 |
| **AMD MI300X 8-way (Supermicro/Dell)** | 180–240k | ROCm enterprise | Custo/GB de HBM melhor |
| **AMD MI325X 8-way** | 220–280k | Idem | Lança em volume final 2025 |
| **Gaudi 3 HLB-325 (8× Gaudi 3)** | 125–155k | SynapseAI | Custo/token agressivo, ecossistema menor |
| **GB200 NVL72 (1 rack)** | 3–4 M | 72 GPUs + interconnect | Frontier scale |

## 9. Escolha estratégica resumida

| Cenário da empresa | Recomendação 2026 |
|---------------------|-------------------|
| Banco T1 / saúde altamente regulada | NVIDIA H200 (2026) → B200 (2027) com NVIDIA AI Enterprise |
| Indústria/varejo regulado moderado | NVIDIA H100/H200 + 1 nó AMD MI300X como segunda fonte |
| Governo/defesa com mandato anti-lock-in | Mix planejado: 60% NVIDIA + 30% AMD + 10% Gaudi 3 |
| Empresa média 1–8 GPUs | NVIDIA L40S ou H100 NVL PCIe; MI300X se time tem skill ROCm |
| Edge / filial | NVIDIA L4 ou CPU Xeon 6 + AMX |
| Frontier/pesquisa | DGX/HGX SuperPOD ou MI300X cluster com IB NDR |

## Referências

- NVIDIA H200 specs: <https://www.nvidia.com/en-us/data-center/h200/>
- NVIDIA Blackwell B200: <https://www.nvidia.com/en-us/data-center/dgx-b200/>
- AMD Instinct MI300X: <https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html>
- AMD MI325X / MI355X: <https://www.amd.com/en/products/accelerators/instinct/mi325x.html>
- Intel Gaudi 3: <https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi3.html>
- vLLM ROCm support: <https://docs.vllm.ai/en/latest/getting_started/installation/amd-installation.html>
- Cerebras CS-3: <https://www.cerebras.ai/product-system>
- SambaNova SN40L: <https://sambanova.ai/products/sn40l-chip>
- DGX H200 / B200: <https://www.nvidia.com/en-us/data-center/dgx-platform/>
