# Plataformas Enterprise Integradas (2026)

> Quando a opção é "comprar suporte" em vez de montar com peças OSS soltas. Foco em **Red Hat (OpenShift AI / RHEL AI / InstructLab)**, **NVIDIA (NIM / NeMo / Triton / AI Enterprise)** e **IBM watsonx.ai**, com nota de Databricks, Anyscale, Cloudera, Dataiku.

## Tabela-resumo

| Plataforma | O que é | Forma | Suporte | Modelos validados | Licença |
|------------|---------|-------|---------|-------------------|---------|
| **Red Hat OpenShift AI** | Kubeflow + KServe + vLLM + governança em OpenShift | Container/K8s | Comercial Red Hat | Granite + Llama + Mistral + qualquer HF | Subscription |
| **Red Hat RHEL AI** | RHEL + InstructLab + Granite + vLLM em servidor único | Bootable container | Comercial Red Hat | Granite-first | Subscription |
| **Red Hat AI Inference Server** | vLLM hardened + tooling | Container | Comercial Red Hat | Validated catalog HF (RedHatAI org) | Subscription |
| **InstructLab** (upstream) | Toolkit para sintetizar dados + treinar (LAB method) | OSS Python | Comunidade + Red Hat | Granite, qualquer LLM treinável | Apache 2.0 |
| **NVIDIA NIM** | Microserviços de inferência empacotados (containers) | Container OCI | NVIDIA AI Enterprise | Llama 4, DeepSeek R2, Qwen 3, Mistral Large 3, Nemotron, NV-Embed, Parakeet, NVLM | $4.500/GPU/ano |
| **NVIDIA NeMo** | Framework treino + customização + retriever + guardrails | SDK Python | NVIDIA AI Enterprise | Próprios + Llama/Mistral/Qwen | Apache 2.0 (parte) + AI Enterprise |
| **NVIDIA Triton** | Servidor de inferência multi-framework | Container | OSS + AI Enterprise | Qualquer (TensorRT-LLM, vLLM backend, ONNX, PyTorch, TF) | BSD-3 |
| **IBM watsonx.ai** | Studio + governança + foundation models hospedados ou on-prem | SaaS / Cloud Pak for Data on-prem | Comercial IBM | Granite (foco), Llama, Mixtral, terceiros | Subscription |
| **Databricks Mosaic AI** | Plataforma data + ML + LLM (Lakehouse) | SaaS multi-cloud | Comercial Databricks | DBRX + qualquer | Subscription |
| **Anyscale** | Ray-as-a-service; Ray Serve LLM com vLLM | SaaS / VPC | Comercial Anyscale | Llama, Qwen, DeepSeek | Subscription |
| **Cloudera AI** (CML / AMP) | Stack data + ML on-prem maduro | On-prem / cloud | Comercial Cloudera | Catálogo customizado | Subscription |
| **Dataiku** | Plataforma data science + LLM Mesh (gateway) | SaaS / on-prem | Comercial Dataiku | Multi-provider | Subscription |
| **Cohere North** | Privado, on-prem; modelos Command/Embed/Rerank | On-prem appliance | Comercial Cohere | Command R+, Aya, Rerank 3 | Subscription |
| **AWS Bedrock + Outposts / Azure AI Foundry on-prem** | Híbrido com data plane gerenciado em data center cliente | Híbrido | Comercial cloud | Catálogo respectivo | Cloud cost + suporte |

## Detalhamento

### Red Hat — papel de cada peça

```
RHEL AI            -> servidor único; bootable container; 1 nó GPU; foco POC e dev
OpenShift AI       -> orquestração K8s; vários nós; produção; KServe + vLLM + Kubeflow
Red Hat AI         -> distribuição vLLM hardened (com llm-d para multi-nó)
  Inference Server
InstructLab        -> tuning via síntese (LAB method); Apache 2.0 upstream
Red Hat AI 3       -> guarda-chuva (anunciado); inclui llm-d, validated models, Training Hub
```

#### OpenShift AI (versão 2.20+)
- Catálogo de modelos UI; **distributed training (PyTorch via Kubeflow)**; **feature store (Feast)**.
- vLLM como runtime servable via KServe; **llm-d para multi-nó**.
- Suporta GPUs NVIDIA e **AMD MI300X**.
- Integra Trustyai (fairness/explainability), Kueue (job queueing).
- **Quando usar**: empresa que já roda OpenShift; precisa governança + suporte; áreas reguladas.
- Links: <https://www.redhat.com/en/products/ai/openshift-ai> · <https://developers.redhat.com/articles/2025/10/02/autoscaling-vllm-openshift-ai>

#### RHEL AI
- "Servidor LLM em uma caixa": instala como container booteável; foco Granite-first.
- **Quando usar**: piloto rápido em servidor único, ambiente air-gapped.
- **RHEL AI 1.5** disponível em GCP Marketplace (também AWS, Azure).
- Links: <https://developers.redhat.com/products/rhel-ai>

#### Red Hat AI Inference Server
- vLLM hardened pela Red Hat com **CVE patches**, **suporte LTS**, **modelos validados** publicados em `huggingface.co/RedHatAI` (já quantizados FP8/INT4 para H100/MI300X), **LLM Compressor** (ferramenta de quantização).
- Links: <https://developers.redhat.com/products/red-hat-ai/inference-server> · <https://huggingface.co/RedHatAI>

#### InstructLab
- **Método LAB** (Large-scale Alignment for chatBots): taxonomia de skills + síntese de dados + tuning. Permite que SMEs (sem equipe ML) contribuam com conhecimento.
- Multilíngue (espanhol, alemão, francês, italiano em GA; japonês, hindi, coreano em pipeline).
- Roda upstream OSS ou via OpenShift AI (Training Hub).
- Links: <https://github.com/instructlab/instructlab> · <https://instructlab.ai/>

### NVIDIA — papel de cada peça

```
NVIDIA AI Enterprise (umbrella, $4.500/GPU/ano)
  ├── NIM            (microserviços de inferência prontos)
  ├── NeMo           (framework: dados, treino, customização, retriever, guardrails)
  ├── Triton         (servidor de inferência multi-framework)
  ├── TensorRT-LLM   (compilador/runtime)
  ├── BlueField DPUs (segurança / tenancy)
  └── DGX Cloud      (gerenciado para grandes contas)
```

#### NVIDIA NIM
- **Containers self-hostable** (Docker/K8s) com modelo + runtime otimizado + APIs OpenAI-compatible. **Catálogo (mai/2026)**: Llama 4, DeepSeek R2, Qwen 3, Mistral Large 3, Nvidia Nemotron, NV-Embed, NV-Reranker, Parakeet (ASR), NVLM (vision).
- Roda em K8s com **NVIDIA GPU Operator**.
- **Custo**: NVIDIA AI Enterprise license (~$4.500/GPU/ano), incluído com DGX/HGX.
- **Quando usar**: empresa NVIDIA-house, equipe pequena, precisa de SLA NVIDIA.
- **Quando NÃO**: AMD/Intel mix, restrições de licença comercial NVIDIA, multi-cloud agnóstico.
- Links: <https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/> · <https://developer.nvidia.com/nim>

#### NVIDIA NeMo
- Framework completo: **NeMo Curator** (dados), **NeMo Customizer** (fine-tune), **NeMo Retriever** (RAG/embeddings), **NeMo Guardrails** (segurança, OSS), **NeMo Evaluator**.
- Links: <https://docs.nvidia.com/nemo-framework/>

#### Triton Inference Server
- Servidor multi-backend (TensorRT, ONNX, PyTorch, TF, vLLM, Python). Mais "infra primitiva" que NIM.
- **Triton-Dynamo** (2026) — combinação dynamo (LLM-serving novo da NVIDIA) + Triton.
- Links: <https://developer.nvidia.com/triton-inference-server>

### IBM watsonx.ai
- **Studio + Governance + Data**: foundation models (Granite + parceiros), prompts, tuning, evaluation, deploy.
- **On-premises**: via **Cloud Pak for Data** em OpenShift; integra com IBM Storage Fusion.
- **2026**: native vector store; agentes; integração Hugging Face anunciada (jan/2026).
- **Quando usar**: shop IBM, áreas reguladas, integração com z/Linux, Storage IBM, Granite.
- Links: <https://www.ibm.com/products/watsonx-ai> · <https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html>

### Databricks Mosaic AI
- Lakehouse + Mosaic (treino) + Vector Search + Model Serving + Foundation Model APIs.
- **Quando usar**: empresa que já vive em Databricks/Spark/Delta.
- **Quando NÃO**: requisito on-prem puro (Databricks é multi-cloud, não on-prem real, exceto via container futuro).
- Links: <https://www.databricks.com/product/machine-learning>

### Anyscale (Ray)
- **Ray Serve LLM** com vLLM, **disaggregated serving**, **wide-EP**, prefix-aware routing.
- **Quando usar**: workloads multi-modelo, long-running training+serving, time Python/Ray.
- Links: <https://www.anyscale.com/> · <https://www.anyscale.com/blog/ray-serve-llm-anyscale-apis-wide-ep-disaggregated-serving-vllm>

### Cloudera AI / Dataiku
- **Cloudera AI**: stack data + ML em CDP, ainda forte em finance/telco com Hadoop legacy.
- **Dataiku**: **LLM Mesh** funciona como gateway interno + governança; abordagem "low-code para data team".
- Links: <https://www.cloudera.com/products/machine-learning.html> · <https://www.dataiku.com/product/llm-mesh/>

### Cohere North
- Plataforma privada da Cohere com Command R+, Aya, Embed v4, Rerank 3 — **roda dentro do data center do cliente**.
- **Quando usar**: empresa que quer "Cohere on-prem" como appliance.
- Links: <https://cohere.com/north>

### AWS Bedrock + Outposts / Azure AI Foundry on-prem
- "Híbrido extremo": data plane gerenciado roda em hardware AWS/Azure entregue ao data center do cliente. Não é "on-prem puro" mas resolve data residency com SLA cloud.
- Links: <https://aws.amazon.com/bedrock/> · <https://azure.microsoft.com/en-us/products/ai-foundry>

## Como as plataformas se diferenciam

| Eixo | Red Hat | NVIDIA | IBM | Databricks | Anyscale |
|------|---------|--------|-----|------------|----------|
| **Open source first** | Sim (vLLM, KServe, InstructLab) | Parcial (NeMo OSS, NIM proprietário) | Granite OSS, restante mix | DBRX OSS, restante proprietário | Ray OSS |
| **On-prem puro** | Sim (estrela) | Sim (NIM) | Sim (Cloud Pak for Data) | Não real (multi-cloud) | Sim (KubeRay) |
| **Hardware lock** | Não (NVIDIA + AMD MI300X) | NVIDIA only | Agnóstico | Cloud GPUs | Agnóstico |
| **Compliance/governança** | OpenShift AI (TrustyAI, AI Hub) | NeMo Guardrails + Eval | Watsonx.governance forte | Unity Catalog | Limitada |
| **ISO/IEC 42001** | Granite via parceria | — | Granite (próprio) | — | — |
| **Stack model** | Granite/Llama/qualquer | Llama 4 / DeepSeek / Nemotron / Qwen no NIM | Granite first | DBRX + parceiros | Llama / Qwen / DeepSeek |

## Fontes

- Red Hat OpenShift AI: <https://www.redhat.com/en/products/ai/openshift-ai>
- Red Hat AI 3 (umbrella): <https://itdaily.com/news/software/red-hat-ai-3/>
- Red Hat AI Inference Server: <https://developers.redhat.com/products/red-hat-ai/inference-server>
- RedHatAI HF org (modelos validados): <https://huggingface.co/RedHatAI>
- InstructLab: <https://instructlab.ai/>
- NVIDIA NIM: <https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/>
- NeMo Framework: <https://docs.nvidia.com/nemo-framework/>
- IBM watsonx.ai: <https://www.ibm.com/products/watsonx-ai>
- Databricks Mosaic AI: <https://www.databricks.com/product/machine-learning>
- Anyscale Ray Serve LLM: <https://www.anyscale.com/blog/ray-serve-llm-anyscale-apis-wide-ep-disaggregated-serving-vllm>
- Dataiku LLM Mesh: <https://www.dataiku.com/product/llm-mesh/>
