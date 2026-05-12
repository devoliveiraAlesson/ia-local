# Stacks Arquetípicas — Perfis Corporativos

> 5 perfis sintéticos com a stack típica observada nos casos públicos. Cada perfil é uma **destilação realista** dos casos das seções 01–06, não um template fictício.

## Perfil A — Banco grande (Tier-1 com alta regulação)

**Inspiração**: JPMorgan, Morgan Stanley, Goldman, Bradesco/Itaú/BTG.

### Topologia
- **Air-gap parcial** ou **VPC dedicada** (Azure OpenAI / AWS Bedrock dedicado).
- **Frontend interno custom** (LLM Suite-style) em vez de Open WebUI puro.
- **Multi-modelo** (3–7 LLMs distintos por trás de um gateway).

### Stack
- **Gateway**: proprietário (LLM Suite-style) ou LiteLLM/Portkey enterprise.
- **Runtime**: vLLM ou Azure OpenAI direto; SGLang em RAG-pesado.
- **Modelos**: GPT-4o-class via Azure (compliance), Anthropic Claude (raciocínio), Llama 70B/Granite (workloads on-prem ou cost-sensitive), modelo coding (Qwen2.5-Coder/Granite-Code).
- **RAG**: Elastic ou Qdrant; embeddings BGE-M3 ou Granite-Embedding.
- **Guardrails**: Llama Guard 3 + Presidio + governança custom (Wall Street level).
- **Observabilidade**: Datadog LLM ou Langfuse on-prem; integração com SIEM.
- **Fine-tuning**: pouco usado em produção front-of-house; mais comum em research/quants.

### Volume típico
- 50k–250k usuários internos.
- 5–50 milhões tokens/dia.
- 50–500 GPUs efetivas.

### Casos mapeados (etapa 1)
- 1 (chat), 2 (atendimento RAG cliente), 4 (coding), 6 (sumarização), 7 (extração), 11 (compliance), 13 (pareceres regulatórios).

### Risco principal
- Audit trail e drift; vendor lock-in com Azure OpenAI.

---

## Perfil B — Hospital regional ou rede de saúde

**Inspiração**: Mayo Clinic (referência alta), Cleveland Clinic, NHS, Einstein/Sírio (BR).

### Topologia
- **Híbrida**: ON-PREM para imagem médica e foundation models proprietários (DGX); SaaS HIPAA/LGPD para ambient scribe e EHR-integration.
- Em alguns casos, **federated learning** via plataforma (Mayo Platform_Connect).

### Stack
- **Runtime**: vLLM em DGX H100/B100 para foundation models de imagem; instância NIM para serving médico.
- **Modelos**: Llama 3.3 / Granite (clínico), modelos vision (PaLI-style ou MedSAM-derivados), foundation model proprietário (Atlas-style).
- **RAG**: Qdrant ou Elastic com **ACL por especialidade**.
- **Frontend**: integração no **Epic / Tasy / MV / Soul MV**, não chat genérico.
- **Guardrails**: pesados — output disclaimer médico obrigatório; PHI redaction (Presidio).
- **Observability**: OTel GenAI + Langfuse on-prem.
- **Compliance**: HIPAA + LGPD Art. 11 + auditoria completa.

### Volume típico
- 1k–10k clinicians.
- 100k–1M tokens/dia + imagens/dia.
- 8–80 GPUs efetivas (com pico em radiology).

### Casos mapeados
- 3 (RAG corporativo), 6 (sumarização clínica), 7 (extração — prontuário), 11 (PII/PHI compliance), 13 (parecer regulatório).

### Risco principal
- Hallucination com peso clínico; audit trail; drift quando guideline médico muda.

---

## Perfil C — Indústria / Manufatura global

**Inspiração**: Bosch, Siemens, BMW, Petrobras.

### Topologia
- **Híbrida** com **camada soberana europeia (Aleph Alpha)** para IP estratégico.
- VPC Azure OpenAI para casos amplos (não-IP-crítico).
- ON-PREM para áreas de **defesa/aeroespacial / dual-use** (ITAR/EAR).

### Stack
- **Gateway**: LiteLLM ou Kong AI Gateway.
- **Runtime**: vLLM + KServe em OpenShift; Azure OpenAI para casos generalistas.
- **Modelos**: Llama 3.3, Granite (Apache 2.0 ajuda compliance), Mistral Large 2 (DE/EU sovereignty), Aleph Alpha (DE puro).
- **RAG**: pgvector ou Qdrant; embeddings BGE-M3.
- **Frontend**: Open WebUI ou **integração em sistema vertical** (Siemens Xcelerator, AskBosch, BMW AIconic).
- **Coding**: Continue.dev + Tabby + GitLab Duo Self-Hosted; Qwen2.5-Coder ou Granite-Code.
- **Observabilidade**: Langfuse + Phoenix.

### Volume típico
- 50k–400k associates.
- 1–10M tokens/dia.
- 20–200 GPUs efetivas.

### Casos mapeados
- 1 (chat), 4 (coding), 6 (sumarização — manuais técnicos), 7 (extração — BOMs, contratos), 9 (geração docs técnicos).

### Risco principal
- Soberania de dados industriais (segredos de fabricação); compliance ITAR/EAR.

---

## Perfil D — Empresa regulada média (legal, seguros, contábil)

**Inspiração**: empresas tipo Eurofarma, SulAmérica, Stefanini, escritórios de advocacia, BPO contábil.

### Topologia
- **VPC privada single-tenant** ou **ON-PREM modesto** (1–2 nós com 2–4 H100/L40S).
- Pouco fine-tune; muita prompt-engineering + RAG.

### Stack
- **Runtime**: vLLM (ou Ollama em fase de POC).
- **Modelos**: Llama 3.3 70B AWQ ou Qwen 2.5 72B; Granite 8B/13B em casos com compliance Apache 2.0 estrito.
- **RAG**: Qdrant (foco em ACL por cliente) ou Elastic.
- **Frontend**: Open WebUI, LibreChat ou AnythingLLM (workspaces por cliente).
- **Coding**: Continue.dev + Tabby (poucos devs).
- **Guardrails**: Llama Guard 3 + Presidio + reranker BGE-reranker para reduzir hallucination.
- **Observability**: Langfuse self-host (gratuito até X traces).
- **Fine-tune**: opcional — LoRA/Axolotl para terminologia específica do setor.

### Volume típico
- 500–10k usuários.
- 100k–1M tokens/dia.
- 1–8 GPUs efetivas.

### Casos mapeados
- 1, 6 (sumarização — especialmente jurídico), 7 (extração — contratos/faturas), 11 (PII), 13 (pareceres regulatórios).

### Risco principal
- ACL no retrieval (mistura de dados de clientes diferentes); LGPD (esp. Art. 11 saúde).

---

## Perfil E — Órgão público / estatal

**Inspiração**: Serpro, Singapura (Pair), UK Gov (Redbox, Caddy), Petrobras (estatal grande).

### Topologia
- **ON-PREM puro** em data center governamental ou de empresa estatal (Serpro, Telebras).
- Multi-tenant interno (várias secretarias / órgãos consumindo do mesmo cluster).
- Forte ênfase em **soberania nacional** (modelo treinado em pt-BR, no Brasil).

### Stack
- **Hardware**: GPUs em data center próprio (H100 ou L40S; em alguns casos, NPUs/Gaudi).
- **Runtime**: vLLM ou serviço próprio (ConversAÍ Studio em Serpro).
- **Modelos**: Llama 3.3, Granite, Mistral Large; **modelos soberanos** (SerproLLM em construção; Aleph Alpha no caso DE).
- **RAG**: Qdrant ou pgvector.
- **Frontend**: produto próprio (Pair Chat, ConversAÍ Studio); para públicos externos, RAG sobre legislação (GOV.UK Chat).
- **Guardrails**: contratual + técnico ("no logging by LLM providers").
- **Observability**: OTel GenAI; transparência pública (Pair publica report cards).

### Volume típico
- 5k–60k servidores internos (Singapura: 60k; UK Redbox: 6k).
- 1–20M mensagens/mês.
- 8–80 GPUs efetivas.

### Casos mapeados
- 1 (chat seguro Pair-style), 6 (Pair Noms — atas), 7 (extração — legislação), 12 (treinamento), 11 (classificação documentos).

### Risco principal
- Adoção lenta sem evangelização ativa; lock-in com fornecedor único.

---

## Tabela comparativa dos perfis

| Perfil | Topologia | Modelos típicos | GPUs | Volume tokens/dia | Casos prioritários |
|--------|-----------|-----------------|------|--------------------|---------------------|
| A. Banco T1 | Air-gap/VPC multi-modelo | GPT-4o + Claude + Llama/Granite | 50–500 | 5–50M | 1, 2, 4, 6, 7, 11, 13 |
| B. Hospital | Híbrido + DGX | Llama/Granite + Vision FM | 8–80 | 100k–1M + imgs | 3, 6, 7, 11, 13 |
| C. Indústria | Híbrido + Aleph Alpha | Llama/Granite/Mistral | 20–200 | 1–10M | 1, 4, 6, 7, 9 |
| D. Regulado médio | VPC/ON-PREM modesto | Llama 70B AWQ ou Qwen | 1–8 | 100k–1M | 1, 6, 7, 11, 13 |
| E. Órgão público | ON-PREM puro | Llama/Granite/SerproLLM | 8–80 | 1–20M/mês | 1, 6, 7, 11, 12 |

## Padrão atravessador

- **vLLM** aparece em todos os perfis (exceto A puro que usa Azure OpenAI).
- **Llama 3.3 / Granite** aparecem como base em todos os perfis on-prem.
- **Qdrant** é o vector store mais comum em on-prem médio.
- **Open WebUI / LibreChat / produto próprio** dependendo da escala.
- **Llama Guard 3 + Presidio** é a base de guardrails em todos os perfis regulados.

A stack arquetípica geral é coerente; o que muda é **(a) topologia (VPC vs ON-PREM puro)**, **(b) escolha de modelos baseada em licença (Apache 2.0 ganha em regulados)**, **(c) frontend (custom em bancos T1 vs Open WebUI em médios)**.
