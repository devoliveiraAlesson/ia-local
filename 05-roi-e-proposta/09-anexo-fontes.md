# Anexo — Bibliografia Consolidada

> Etapa 5/5. Compilação de todas as fontes citadas nas Etapas 1–5 da proposta. Maio/2026.
>
> Fontes agrupadas por temática. Marcadas com tipo: [P] primária (blog/press release/paper da empresa), [S] secundária (imprensa especializada), [T] técnica (documentação, GitHub, blog técnico), [R] regulatória, [V] vendor.

---

## A. Casos públicos corporativos

### Banco e financeiro

- [P] **JPMorgan Chase — LLM Suite case (Tearsheet)**: https://tearsheet.co/artificial-intelligence/jpmorgan-chases-gen-ai-implementation-450-use-cases-and-lessons-learned/
- [P] **Morgan Stanley AI @ MS** (corporate press release 2024–2025)
- [S] **Goldman Sachs LLM** (cobertura imprensa especializada)
- [P] **Bloomberg BloombergGPT** (paper arxiv 2303.17564): https://arxiv.org/abs/2303.17564
- [S] **Belitsoft on BloombergGPT**: https://belitsoft.com/bloomberggpt
- [P] **Itaú "Inteligência Itaú"** (release corporativo + investidores)
- [S] **Bradesco BIA + Bridge** (cobertura imprensa BR e parceria IBM watsonx)
- [P] **BTG Pactual Saturn Platform** (release corporativo)
- [S] **Nubank** (cobertura imprensa BR)
- [P] **BBVA — ChatGPT Enterprise + Gemini Workspace** (release corporativo OpenAI/Google)
- [S] **Santander** (cobertura imprensa)
- [S] **ING** (cobertura imprensa)

### Saúde / farma

- [P] **Mayo Clinic — DGX SuperPOD + Atlas pathology** (release Mayo + NVIDIA)
- [S] **Cleveland Clinic — Ambience documentation** (cobertura imprensa)
- [P] **Bayer — Recursion LOWE** (release corporativo): https://www.bayer.com
- [P] **Pfizer — Charlie platform** (release corporativo)
- [P] **Roche/Genentech — Lab in a Loop** (release corporativo)
- [S] **NHS UK — Federated Data Platform** (gov.uk)

### Indústria

- [P] **Bosch — AskBosch + ROB HR Agent + GenAI Championship** (release Bosch)
- [P] **Siemens — Industrial Copilot + Xcelerator** (release Siemens + Microsoft)
- [P] **BMW — AIconic Agent** (release BMW + AWS)
- [P] **Mercedes-Benz — MBUX Virtual Assistant** (release Mercedes)
- [S] **Embraer / Vale** (SAP Now 2024)

### Varejo

- [P] **Walmart — My Assistant + Wallaby + Element** (release Walmart)
- [S] **Mercado Livre** (cobertura imprensa LATAM)

### SaaS / Tecnologia

- [P] **Stripe — vLLM migração (-73%)**: blog técnico Stripe
- [P] **Snowflake Cortex** (release Snowflake)
- [P] **Databricks DBRX** (release Databricks)
- [P] **Red Hat interno** (US$ 5M cost avoidance, blog Red Hat)
- [P] **ARSAT — OpenShift AI** (case study Red Hat)

### Governo / estatal

- [P] **Singapura Pair (-46% admin time)** (release Smart Nation Singapore)
- [P] **UK Gov Redbox + Caddy** (gov.uk releases)
- [P] **Petrobras ChatPetrobras** (release Petrobras + Microsoft)
- [P] **Serpro ConversAÍ Studio** (release Serpro)

---

## B. Tecnologias e runtimes

### Inferência

- [T] **vLLM releases**: https://github.com/vllm-project/vllm/releases
- [T] **vLLM blog (V1 engine)**: https://blog.vllm.ai/
- [T] **SGLang vs vLLM**: https://particula.tech/blog/sglang-vs-vllm-inference-engine-comparison
- [T] **llm-d (vLLM multi-node)**: https://llm-d.ai/blog/production-grade-llm-inference-at-scale-kserve-llm-d-vllm
- [V] **Red Hat AI Inference Server**: https://developers.redhat.com/products/red-hat-ai/inference-server
- [V] **NVIDIA NIM**: https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/
- [T] **Anyscale Ray Serve LLM** (docs Anyscale)
- [T] **KServe docs**: https://kserve.github.io/website/
- [T] **TensorRT-LLM docs**: https://github.com/NVIDIA/TensorRT-LLM

### Modelos

- [T] **IBM Granite 4**: https://www.ibm.com/new/announcements/ibm-granite-4-0-hyper-efficient-high-performance-hybrid-models
- [R] **Granite 4 ISO 42001**: https://digital.nemko.com/news/ibm-granite-40-first-iso-42001-certified-open-source-ai
- [T] **Qwen blog Qwen 3**: https://qwenlm.github.io/blog/qwen3/
- [T] **Qwen3-Embedding**: https://qwenlm.github.io/blog/qwen3-embedding/
- [T] **DeepSeek V3 GitHub**: https://github.com/deepseek-ai/DeepSeek-V3
- [T] **DeepSeek R1 LICENSE**: https://github.com/deepseek-ai/DeepSeek-R1/blob/main/LICENSE
- [V] **Llama license (Llama 3 / 4)**: https://www.llama.com/llama3/license/ ; https://www.llama.com/llama4/license/
- [V] **Mistral Codestral MNPL**: https://mistral.ai/news/mistral-ai-non-production-license-mnpl/
- [V] **Mistral Large 2 (MRL)**: https://mistral.ai/news/mistral-large-2407
- [V] **Microsoft Phi-4**: https://huggingface.co/microsoft
- [V] **Google Gemma terms**: https://ai.google.dev/gemma/terms

### Embeddings e RAG

- [T] **BGE-M3 (BAAI)**: https://huggingface.co/BAAI
- [T] **Granite Embedding**: https://huggingface.co/ibm-granite/granite-embedding-278m-multilingual
- [T] **Nomic Embed**: https://huggingface.co/nomic-ai
- [T] **Qdrant docs**: https://qdrant.tech/documentation/
- [T] **Milvus docs**: https://milvus.io/docs
- [T] **Weaviate docs**: https://weaviate.io/developers/weaviate
- [T] **pgvector**: https://github.com/pgvector/pgvector
- [V] **Elastic Vector Search**: https://www.elastic.co/elasticsearch/vector-database

### Frameworks de aplicação

- [T] **LangChain / LangGraph**: https://www.langchain.com/
- [T] **LlamaIndex**: https://www.llamaindex.ai/
- [T] **Haystack**: https://haystack.deepset.ai/
- [T] **DSPy**: https://dspy.ai/
- [V] **Microsoft Semantic Kernel**: https://learn.microsoft.com/semantic-kernel/
- [V] **Spring AI (VMware)**: https://spring.io/projects/spring-ai

### Frontends

- [T] **Open WebUI**: https://github.com/open-webui/open-webui
- [T] **LibreChat**: https://www.librechat.ai/
- [T] **AnythingLLM**: https://anythingllm.com/
- [T] **Big-AGI**: https://big-agi.com/
- [T] **Continue.dev**: https://continue.dev/
- [T] **Tabby**: https://www.tabbyml.com/
- [T] **Cline / Roo**: https://cline.bot/

### Gateway

- [T] **LiteLLM**: https://www.litellm.ai/
- [V] **Portkey**: https://portkey.ai/
- [V] **Kong AI Gateway**: https://konghq.com/products/kong-ai-gateway
- [T] **Envoy AI Gateway**: https://gateway.envoyproxy.io/

### Guardrails

- [T] **Llama Guard 3**: https://huggingface.co/meta-llama/Llama-Guard-3-8B
- [T] **Microsoft Presidio**: https://microsoft.github.io/presidio/
- [V] **NeMo Guardrails (NVIDIA)**: https://github.com/NVIDIA/NeMo-Guardrails
- [V] **Lakera Guard**: https://www.lakera.ai/
- [V] **ProtectAI**: https://protectai.com/

### Observabilidade / FinOps

- [T] **Langfuse**: https://langfuse.com/
- [T] **Phoenix Arize**: https://docs.arize.com/phoenix
- [T] **OTel GenAI conventions**: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- [T] **Ragas**: https://docs.ragas.io/
- [T] **DeepEval**: https://github.com/confident-ai/deepeval
- [T] **Promptfoo**: https://www.promptfoo.dev/
- [T] **DCGM**: https://github.com/NVIDIA/DCGM

### Fine-tuning

- [T] **InstructLab**: https://instructlab.ai/
- [T] **Axolotl**: https://github.com/axolotl-ai-cloud/axolotl
- [T] **Unsloth**: https://github.com/unslothai/unsloth
- [T] **TRL (Hugging Face)**: https://huggingface.co/docs/trl

---

## C. Hardware e infraestrutura

- [V] **NVIDIA H100/H200 datasheets**: https://www.nvidia.com/en-us/data-center/h200/
- [V] **NVIDIA Blackwell B200**: https://www.nvidia.com/en-us/data-center/blackwell-architecture/
- [V] **AMD MI300X**: https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html
- [V] **Intel Gaudi 3**: https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi.html
- [T] **InfiniBand fabric (Mellanox/NVIDIA)**: https://www.nvidia.com/en-us/networking/infiniband-architecture/
- [V] **Spectrum-X**: https://www.nvidia.com/en-us/networking/spectrumx/
- [V] **Weka, VAST Data, IBM Storage Scale (GPFS), Pure FlashBlade** (datasheets)
- [V] **MinIO, Ceph (Red Hat)** (docs)
- [V] **OpenShift AI**: https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai

---

## D. Compliance, segurança, regulação

- [R] **LGPD (Lei Geral de Proteção de Dados)** — Lei 13.709/2018 — ANPD
- [R] **GDPR (EU 2016/679)**
- [R] **EU AI Act** — Regulation (EU) 2024/1689
- [R] **HIPAA (US Health Insurance Portability and Accountability Act)**
- [R] **ISO/IEC 42001:2023** (AI Management System)
- [R] **ISO/IEC 27001 / 27701** (segurança da informação + privacidade)
- [R] **PCI-DSS 4.0** (cartões)
- [R] **SOX** (controles)
- [T] **OWASP GenAI Top 10 (2025)**: https://genai.owasp.org/
- [T] **OWASP LLM Security Verification Standard**: https://owasp.org/
- [T] **MITRE ATLAS**: https://atlas.mitre.org/

---

## E. Estudos de mercado e referências quantitativas

- [S] **PremAI 2026 — self-hosted LLM guide**: https://blog.premai.io/self-hosted-llm-guide-setup-tools-cost-comparison-2026/
- [S] **PremAI — LLM enterprise comparison 2026**: https://blog.premai.io/llama-vs-mistral-vs-phi-complete-open-source-llm-comparison-for-enterprise-2026/
- [S] **BentoML — open-source LLMs 2026**: https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models
- [S] **BentoML — DeepSeek guide**: https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond
- [S] **Onyx self-hosted LLM leaderboard**: https://onyx.app/self-hosted-llm-leaderboard
- [S] **Truefoundry on-prem LLMs**: https://www.truefoundry.com/blog/on-prem-llms
- [S] **Petronella — private AI deployment guide**: https://petronellatech.com/blog/private-ai-deployment-guide-enterprise/
- [P] **IBM Security — Cost of a Data Breach 2025**: https://www.ibm.com/security/data-breach
- [P] **Stanford AI Index Report** (anual): https://aiindex.stanford.edu/
- [P] **McKinsey State of AI** (anual)
- [P] **Andreessen Horowitz — Generative AI in Enterprise** (releases regulares a16z)

---

## F. Documentação governamental / regulatória adicional (BR)

- [R] **ANPD — guias e resoluções**: https://www.gov.br/anpd/pt-br
- [R] **BACEN — Resolução CMN sobre uso de IA em risco de crédito** (quando aplicável)
- [R] **CVM — orientações sobre IA em mercado de capitais**
- [R] **CFM — Resoluções sobre uso de IA em medicina** (BR)
- [R] **OAB — orientações sobre uso de IA em advocacia** (BR)
- [R] **ANS — IA em saúde suplementar** (BR)

---

## G. Comunidades e recursos contínuos

- **Hugging Face Hub**: https://huggingface.co/
- **GitHub vLLM project**: https://github.com/vllm-project/vllm
- **GitHub SGLang**: https://github.com/sgl-project/sglang
- **GitHub Open WebUI**: https://github.com/open-webui/open-webui
- **r/LocalLLaMA (Reddit)**: https://reddit.com/r/LocalLLaMA
- **MLOps Community**: https://mlops.community/
- **AI Alliance** (IBM, Meta, Red Hat, ...): https://thealliance.ai/

---

## H. Etapas 1–4 da proposta (referências internas)

| Etapa | Documento | Conteúdo |
|-------|-----------|----------|
| 1 | `01-casos-de-uso/00-resumo-executivo.md` | 14 casos de uso priorizados P0–P3 |
| 1 | `01-casos-de-uso/01-08-*.md` | Detalhe por caso |
| 2 | `02-tecnologias/00-mapa-da-stack.md` | Mapa em 8 camadas |
| 2 | `02-tecnologias/11-licencas-modelos.md` | Tabela master de licenças |
| 3 | `03-exemplos-reais/00-tabela-mestre.md` | 34 empresas mapeadas |
| 3 | `03-exemplos-reais/08-stacks-arquetipicas.md` | 5 perfis sintéticos |
| 3 | `03-exemplos-reais/09-licoes-aprendidas.md` | Armadilhas e práticas |
| 4 | `04-infraestrutura/00-resumo-arquitetura.md` | Arquitetura de referência |
| 4 | `04-infraestrutura/02-dimensionamento-por-caso.md` | Dimensionamento P/M/G |
| 4 | `04-infraestrutura/06-seguranca-compliance.md` | OWASP LLM, LGPD, ISO 42001 |
| 4 | `04-infraestrutura/11-checklist-prontidao.md` | Checklist pré-projeto |
| 5 | `05-roi-e-proposta/00-08-*.md` | Esta proposta consolidada |

---

## Notas finais

- Todos os links foram verificados como acessíveis até **maio/2026**. Conteúdo na web pode mudar; a proposta é defensável pelos fatos relatados, não pela permanência das URLs.
- Casos públicos com pouca cobertura formal (Embraer, Vale, Magalu, NSA/CIA) foram registrados na Etapa 3 com tag de confiança 🟡 e tratados de forma resumida.
- Valores monetários (CAPEX, OPEX, salários) são estimativa pública; orçamento formal exige cotação OEM e proposta de fornecedor.
- Para cada decisão crítica, o documento da Etapa 5 traz a referência cruzada à Etapa que sustenta a afirmação.
