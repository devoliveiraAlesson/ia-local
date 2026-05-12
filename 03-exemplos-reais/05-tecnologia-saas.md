# Tecnologia e SaaS — Casos Públicos

> Empresas de tecnologia que **(a)** vendem stack para outros (Snowflake, Databricks, Cloudera, Red Hat, NVIDIA) e **(b)** rodam IA internamente. Servem como **referência de plataformas** que clientes corporativos podem comprar/adotar.

## 1. Snowflake (Cortex + Arctic)

**Setor**: data cloud / SaaS. **Sede**: EUA.

### Status e escala
- ✅ **Produção em SaaS-Enterprise**.
- ✅ **Snowflake Arctic** — LLM open MoE lançado em 2024, posicionado como "most open enterprise-grade LLM" (mas adoção real em produção fora do Snowflake é baixa).
- ✅ **Cortex Code** lançado nov/2025 — **>50% dos clientes ativamente usando** em poucos meses.
- ✅ Cortex Code = "one governed agent" sobre todo data stack: Snowflake, dbt, Airflow, Databricks, AWS Glue, Postgres etc.

### Por que importa
- Plataforma de IA que sobe **dentro do tenant Snowflake do cliente** — não exige movimento de dados (princípio "zero copy").
- Caso para empresa que já tem warehouse Snowflake — alternativa a stack vLLM/RAG própria.

### Fontes
- ✅ <https://www.snowflake.com/en/news/press-releases/snowflake-expands-snowflake-intelligence-and-cortex-code-to-power-the-control-plane-for-the-agentic-enterprise/>
- ✅ <https://www.snowflake.com/en/blog/cortex-code-governed-agent-data-stack/>
- ⚠️ <https://venturebeat.com/data-infrastructure/snowflake-launches-arctic-an-open-mixture-of-experts-llm-to-take-on-dbrx-llama-3>

## 2. Databricks (DBRX + Mosaic AI)

**Setor**: data + AI lakehouse. **Sede**: EUA.

### Status
- ✅ **DBRX** (open MoE) lançado mar/2024.
- ✅ Adoção em finance, legal, healthcare, manufacturing — clientes empresariais que valorizam transparência da training lineage.
- ⚠️ Contexto crítico: análise pós-lançamento (Mario Defelipe e outros) reportou que DBRX e Arctic **performam abaixo do esperado** vs. Llama 3 / Mistral em benchmarks práticos — **modelo open de fornecedor SaaS** ainda perde para modelos open de **labs especializados** (Meta, Mistral, Qwen).
- ✅ **Mosaic AI** (ex-MosaicML, adquirida) é a stack de fine-tuning + serving que muitos clientes usam.

### Fontes
- ✅ <https://closeloop.com/blog/dbrx-databricks-open-source-llm-for-enterprise-ai/>
- ⚠️ <https://medium.com/@mario.defelipe/my-deception-with-databricks-dbrx-and-snowflake-arctic-enterprise-llms-b4fd4faf752a>

## 3. Cloudera

- ⚠️ Parceria com NVIDIA em **NIM** reportou **36× perf boost** em deployments. Foco: clientes que ainda têm grandes data lakes Hadoop/Spark on-prem e querem rodar LLM no mesmo cluster.
- ✅ Caso útil para empresas com infra Hadoop/CDP legada.

## 4. Red Hat (auto-uso)

**Setor**: software open source enterprise. **Sede**: EUA (parte da IBM).

### Status
- ✅ **Caso interno publicado**: Red Hat Experience Engineering implantou **4 soluções AI** sobre **OpenShift AI + RHEL AI** em AWS.
- ✅ **US$ 5 mi de cost avoidance** em IT support.
- ✅ Demonstra a stack RHEL AI + OpenShift AI + Granite + InstructLab.

### Fontes
- ✅ <https://www.redhat.com/en/resources/red-hat-ai-powered-innovation-it-support-case-study>
- ✅ <https://www.redhat.com/en/resources/operationalize-ai-overview>

## 5. ARSAT — cliente Red Hat OpenShift AI (Argentina)

**Setor**: telecom estatal. **Sede**: AR.

### Status
- ✅ Migrou supply chain para automação com **Red Hat OpenShift AI**.
- ✅ Reduziu response time + OPEX + melhorou customer satisfaction.
- ✅ Único case study cliente OpenShift AI em LATAM publicado pela Red Hat até o momento de nossa pesquisa.

### Fontes
- ✅ <https://www.redhat.com/en/resources/arsat-openshift-ai-case-study>

## 6. JetBrains AI

- ✅ JetBrains AI Assistant disponível em IntelliJ, PyCharm, GoLand, Webstorm, Rubymine.
- ✅ Suporta múltiplos providers; competidor direto do Copilot/Cursor para devs JVM/Python/Go.

## 7. GitHub Copilot Enterprise (contraponto)

**Setor**: dev tools (Microsoft). **Sede**: EUA.

### Status
- ✅ **Padrão de mercado em coding assistant na nuvem**: API + integração GitHub.com / Visual Studio.
- ✅ **Não é on-prem** — fica na infra da Microsoft (mesmo no plano Enterprise).
- ✅ Útil como **contraponto** para a empresa: se a sensibilidade de código é alta, não é a opção.
- ✅ Alternativa local: **Continue.dev + vLLM com Qwen2.5-Coder ou Granite-Code** (mapeado na etapa 2).

## 8. GitLab Duo Self-Hosted

**Setor**: DevOps + AI tools. **Sede**: EUA.

### Status e escala
- ✅ **Produção como produto comercial** (GitLab Duo Self-Hosted Released, 2024).
- ✅ Cliente operacionaliza um **AI Gateway próprio + LLMs próprios em sua infra**, sem usar infra GitLab e sem usar modelos do vendor padrão.
- ✅ LLMs suportados: **Anthropic, Mistral, OpenAI**. Cliente também pode plugar modelo open-source via runtime suportado (vLLM e outros).
- ✅ Plugin para JetBrains IDEs.

### Por que é referência
- É o **caminho oficial e suportado** para Copilot-equivalente **on-prem** com governança DevSecOps (e diferencial vs. GitHub Copilot).
- Mapeia para Caso 4 (coding) + Caso 5 (code review) da etapa 1.

### Fontes
- ✅ <https://docs.gitlab.com/administration/gitlab_duo_self_hosted/>
- ✅ <https://docs.gitlab.com/administration/gitlab_duo_self_hosted/supported_llm_serving_platforms/>
- ✅ <https://www.devopsdigest.com/gitlab-duo-self-hosted-released>

## 9. Sourcegraph Cody

- ✅ Suporta **BYOM** (bring your own model) com modelos próprios do cliente.
- ✅ Indexação de codebase como contexto.
- ✅ Foco enterprise: alternativa a Copilot para empresas que precisam manter código interno.

## 10. TabbyML — referência open-source

- ✅ Self-hosted AI coding assistant (Apache 2.0).
- ✅ Versão 0.30 indexa **GitLab Merge Requests como contexto**.
- ✅ Aparece como uma das primeiras escolhas em deployments on-prem para coding (mapeado em etapa 2 — `04-frontends-chat.md`).

## 11. Stripe — caso operacional (vLLM)

**Setor**: pagamentos / fintech. **Sede**: EUA.

### Status
- ⚠️ **Produção**. Migrou inferência interna para **vLLM**, alcançando **–73% de custo de inferência**, processando **50 milhões de chamadas/dia em 1/3 da frota de GPU original**.
- ⚠️ É frequentemente citado em conteúdos técnicos e blogs de prática vLLM, mas a fonte primária Stripe não foi encontrada em nossa pesquisa — então marcamos com cautela.

### Por que importa
- Maior número público de **redução de custo via vLLM** num caso de produção em escala (50M req/dia).

### Fontes
- ⚠️ <https://introl.com/blog/vllm-production-deployment-inference-serving-architecture> (relata o caso)
- ⚠️ <https://www.sitepoint.com/vllm-production-deployment-guide-2026/>

## 12. IBM (auto-uso + watsonx)

- ✅ **watsonx.ai** + **Granite 3/4** + **InstructLab** = stack consolidada (cobertura na etapa 2 sec. 06).
- ✅ Adotada por clientes regulados (BNP Paribas, governo, saúde — alguns com NDA).
- ✅ **IBM Granite 4** = primeiro LLM open com **certificação ISO/IEC 42001**.

## Síntese

- Plataformas SaaS-Enterprise (Snowflake Cortex, Databricks Mosaic, watsonx) competem com stack open-source (vLLM + KServe + LiteLLM).
- A grande virada de 2024–2026 foi **vLLM se tornar o substrato comum**: NIM homologa, OpenShift AI roda, Anyscale Ray Serve roda, Stripe migrou, Cloudera plugou.
- **GitLab Duo Self-Hosted** é o melhor caminho oficial para coding on-prem; **Continue.dev / Tabby** são as opções OSS puras.
- DBRX / Arctic (modelos open de vendors SaaS) **não são as melhores escolhas** em 2026 — empresa séria escolhe **Llama / Qwen / Granite / DeepSeek / Mistral** como base.
