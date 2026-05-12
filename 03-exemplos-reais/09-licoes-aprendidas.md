# Lições Aprendidas e Armadilhas Recorrentes

> Compilado dos casos públicos das seções 01–07 + posts técnicos de prática (vLLM, llm-d, AI21, OpenShift). Foco em **erros que se repetem** em deployments reais e em **práticas que separam pilotos de produção**.

## A. Armadilhas de hardware e infraestrutura

### A1. Subdimensionar GPU (memória)
- **Sintoma**: OOM em pico, batch_size baixo demais, latência ruim em prompts longos.
- **Causa raiz**: assumir uso de 100% da VRAM. Driver + PyTorch + vLLM runtime reservam **2–4 GB**. Activations + KV cache crescem com `max_model_len` × `max_num_seqs`.
- **Correção**: `gpu-memory-utilization=0.85–0.90` + tunar `max-model-len` realista para a carga.
- **Onde aparece**: SitePoint vLLM 2026, AI21 "Go big or go OOM", Spheron, Lyceum, DigitalOcean.

### A2. Sobredimensionar GPU (utilização baixa)
- **Sintoma**: 1 GPU dedicada a um modelo de tráfego intermitente; cluster a 40% de utilização.
- **Correção**: multi-tenant com vLLM **prefix-aware routing** (llm-d, vLLM Production Stack); compartilhar modelo entre tenants com semantic cache (LiteLLM/Portkey).
- **Onde aparece**: Lyceum 2026, llm-d.ai, Stripe (citação 73% economia ao migrar para vLLM).

### A3. NFS para pesos de modelo
- **Sintoma**: cold start de 5–15 min para modelos 70B; bottleneck em rolling restart.
- **Correção**: LVM persistent volumes locais + **affinity rules**; ou bake do modelo na imagem (caro em storage, rápido em start).
- **Onde aparece**: vLLM Optimization Guide (Databasemart).

### A4. Round-robin load balancing
- **Sintoma**: cache hit rate baixo; throughput agregado abaixo do esperado.
- **Causa raiz**: round-robin ignora **KV-cache localizada por GPU**.
- **Correção**: prefix-aware routing (vLLM Production Stack, llm-d, Anyscale Ray Serve LLM).

### A5. Network fabric subdimensionada
- **Sintoma**: tensor parallelism degrada em 2+ nós; latência inter-GPU ruim.
- **Correção**: **InfiniBand HDR/NDR ou Spectrum-X / RDMA over Ethernet** para multi-nó. Pelo menos 200 Gb/s.
- **Onde aparece**: VMware Cloud Foundation guide, llm-d posts.

## B. Armadilhas de RAG / retrieval

### B1. ACL ausente no retrieval (OWASP LLM08)
- **Sintoma**: usuário consegue acessar via RAG documento que não pode acessar diretamente.
- **Causa raiz**: vector store retorna por similaridade, não por permissão.
- **Correção**: **filtros de ACL no retrieval** (Qdrant payload filters, Elastic security, Milvus partition keys). Aplicar **mesma ACL** que o sistema fonte.
- **Onde aparece**: OWASP GenAI Top 10 2025 (LLM08 Vector & Embedding Weaknesses); Llama Guard guidance.

### B2. Chunking mal calibrado
- **Sintoma**: respostas quebradas em listas; citações erradas.
- **Correção**: **chunk semântico** (LlamaIndex SemanticSplitter, parser layout-aware como Unstructured.io). Em PDFs estruturados, dual-chunk (parent-child).

### B3. Sem reranker
- **Sintoma**: top-k retorna documentos só "topicamente similares", não exatos.
- **Correção**: **BGE-reranker** ou **Qwen3-Reranker** num segundo passo. Custos de latência (~50–150ms) compensam grande aumento de precision.

### B4. Embeddings desatualizados
- **Sintoma**: drift conforme corpus cresce; queries novas não recuperam doc novo.
- **Correção**: re-index incremental + **rebuild semestral**; monitorar P50/P95 de Recall@k via Ragas/DeepEval.

## C. Armadilhas de modelo e licença

### C1. Llama Community License — gatilho de 700M MAU
- **Sintoma**: a empresa cresce e pode ultrapassar 700M MAU (raro mas possível em gigantes).
- **Correção**: para **bancos T1, retail global, telcos com >100M usuários**, considerar **Granite (Apache 2.0)**, **Qwen 3 (Apache 2.0)**, **Mistral Apache** em vez de Llama em fluxos cliente-facing.
- **Onde aparece**: etapa 2, `11-licencas-modelos.md`.

### C2. Codestral MNPL — proibido para uso comercial sem licença paga
- Usar **Qwen2.5-Coder** ou **DeepSeek-Coder V2** ou **Granite-Code** em produção comercial.

### C3. Modelo de SaaS-vendor (DBRX / Arctic) abaixo do esperado
- **Sintoma**: benchmarks promocionais não se confirmam em produção.
- **Correção**: priorizar **modelos de labs especializados** (Meta, Mistral, Qwen, DeepSeek, IBM Granite) em vez de modelos open de vendors SaaS.

### C4. Quantização agressiva
- **Sintoma**: queda de qualidade em raciocínio (matemática, código, multi-step).
- **Correção**: AWQ-INT4 / GPTQ-INT4 para chat geral; **FP8** ou **INT8** para tarefas críticas; manter 1 modelo full-precision para evals contínuas.

## D. Armadilhas de governança e segurança

### D1. Prompt injection ignorada
- **Sintoma**: agente executa ferramenta arbitrária ao receber instrução em documento.
- **Correção**: **defense in depth** — Llama Prompt Guard 2 + Presidio + system prompt + estrutura agent com validação por step.

### D2. Hallucination regulada (jurídico, médico, financeiro)
- **Sintoma**: parecer com citação de lei inexistente; diagnóstico errado.
- **Correção**: **groundedness check** (Ragas faithfulness, RAGAS context-precision); citações obrigatórias com link à fonte; disclaimers; revisão humana.

### D3. PII/PHI vazando para logs
- **Sintoma**: dados sensíveis acabam em Datadog/Splunk/Langfuse SaaS.
- **Correção**: **Presidio** na ingestão da observabilidade; **Langfuse self-host** em vez de SaaS; sanitização de prompts em logs.

### D4. Audit trail incompleto
- **Sintoma**: incidente regulatório, mas faltam evidências de qual prompt, modelo, output, usuário.
- **Correção**: **OTel GenAI** com captura de prompt/completion + IDs de usuário/sessão; retenção 12+ meses para regulados.

## E. Armadilhas de adoção e organização

### E1. Chat genérico tem teto de adoção
- **Sintoma**: lançou ChatGPT-style interno; uso sobe e cai em 60 dias.
- **Correção**: lançar **verticais por área** (Connect Coach JPMorgan, Pair Noms Singapore, AskResearchGPT MS) — adoção sustentada vem de fluxos contextualizados.
- **Onde aparece**: JPMorgan, Morgan Stanley, Singapura.

### E2. Sem campeões em cada área
- **Sintoma**: ferramenta só usada por TI/engenharia.
- **Correção**: **GenAI Championship Bosch-style** (120 use cases internos), **competição BBVA** (400+ funcionários submetendo) — capilarização orgânica.

### E3. FinOps invisível
- **Sintoma**: fatura mensal de Azure OpenAI ou consumo elétrico de GPU explode sem causa óbvia.
- **Correção**: **observability + cost dashboards por usuário/equipe/projeto** (Langfuse, Helicone-style); **quotas via gateway** (LiteLLM, Portkey); **semantic cache** para hits repetidos.

### E4. Drift sem evals contínuas
- **Sintoma**: qualidade decai ao trocar modelo; ninguém percebe até reclamação.
- **Correção**: **Ragas + DeepEval + Promptfoo** rodando como CI/CD para prompts e modelos; canary releases.

## F. Armadilhas específicas por setor (resumido)

| Setor | Armadilha mais comum | Fix |
|-------|----------------------|-----|
| Banco T1 | Audit trail e compliance MAS/SEC/BaCen | OTel GenAI + retenção 24m + revisão humana em outputs cliente-facing |
| Hospital | Hallucination clínica + PHI em logs | Presidio + groundedness check + disclaimers + humano-na-curva |
| Indústria | IP vazando para LLM externo | Aleph Alpha / Granite on-prem + DLP no gateway |
| Regulado médio | LGPD multi-cliente | Qdrant ACL por workspace; AnythingLLM workspaces |
| Governo | Adoção lenta + lock-in vendor | Singapura Pair-style: universal + gratuito + multi-LLM |

## G. Métricas que importam (e geralmente não são instrumentadas no piloto)

1. **Adoção** — DAU / MAU / WAU; % usuários ativos elegíveis.
2. **Profundidade de uso** — mensagens/usuário/dia; sessões/dia.
3. **Custo por interação** — US$/1k tokens efetivos por equipe.
4. **Quality regulatory** — % outputs com citação; taxa de erro encontrada em revisão humana.
5. **Latência percebida** — TTFT (time-to-first-token) P50/P95; tempo total da resposta.
6. **Cache hit rate** — semantic cache effectiveness; KV-cache reuse.
7. **GPU utilization** — meta >70%; <40% indica overdimensionamento.
8. **MTTR** quando o sistema falha; **% de uptime** com SLA negociado.

## H. Princípios destilados (top 7)

1. **Multi-modelo > modelo único**: JPMorgan tem 7 LLMs por trás do gateway. Não é overengineering — é resiliência + custo + compliance.
2. **Vertical > genérico**: chat genérico tem teto de adoção; vertical (Connect Coach, Pair Noms) sustenta crescimento.
3. **vLLM é o pivô** + KV-cache routing > round-robin.
4. **ACL no retrieval não é opcional** (OWASP LLM08).
5. **Apache 2.0 reduz fricção de compliance**: Granite, Qwen, Mistral abertos > Llama (Community License) > Codestral (MNPL).
6. **Observability + FinOps desde o dia 1** — não é coisa para "depois do piloto".
7. **Humano na curva** em outputs regulados (jurídico, médico, financeiro) — sempre.

## Lacunas que ficam para Etapa 4 (infra) e Etapa 5 (ROI)

- **Dimensionamento exato por carga** (tokens/dia → GPUs efetivas) — Etapa 4.
- **TCO incluindo redundância, energia, network fabric** — Etapa 4.
- **ROI por caso de uso** com base em dados de mercado dos casos públicos (JPMorgan, Walmart, Morgan Stanley publicaram números) — Etapa 5.
- **Cronograma de adoção típico** (60d → 6m → 18m) — Etapa 5.
