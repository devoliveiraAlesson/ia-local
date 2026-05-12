# Setor Financeiro — Casos Públicos

> Setor mais bem documentado e mais relevante como referência para empresa com dados sensíveis. Prioridade: privacidade, regulação (SEC, FINRA, BaCen, ECB, GDPR), confidencialidade de cliente, auditabilidade.

## 1. JPMorgan Chase — "LLM Suite" (deep dive)

**Setor**: banco universal global. **Sede**: EUA. **Tamanho**: ~317 mil funcionários.

### Status e escala
- ✅ **Produção** desde meados de 2024. Anúncio inicial: agosto/2024 (CNBC).
- ✅ Em rollout gradual: 60k → 140k → 200k → **230k+ funcionários ativos** dentro de 8 meses do lançamento.
- ✅ **600+ casos de uso em produção** (originalmente comunicados como "450 use cases", em fontes posteriores 600+).
- ✅ **Innovation of the Year 2025** (American Banker) — categoria GenAI.

### Stack (público)
- "LLM Suite" é descrita como **plataforma proprietária de gateway** que dá acesso a **7 LLMs distintos**, incluindo modelos da OpenAI, Anthropic e Meta (Llama).
- Operada em **ambiente controlado** com data protection e regulatory compliance — sem detalhamento público sobre ON-PREM puro vs. VPC dedicada (provável VPC dedicada Azure + air-gap parcial).
- Fine-tuning interno com dados próprios JPMorgan (compliance corporativa).
- Mapeamento aos casos da etapa 1: **Caso 1** (chat interno), **Caso 4** (coding), **Caso 6** (sumarização/decks), **Caso 7** (queries sobre PowerPoints e documentos).

### Produtos derivados / verticais
- **Connect Coach** (Private Bank) — research summarization, draft de reports, geração de ideias de investimento sobre datasets proprietários.
- **Quest IndexGPT** — usa GPT-4 para construção temática de índices de investimento; primeiro produto cliente (institucional) baseado em GenAI no banco. ✅
- **Spectrum / SpectrumGPT** — plataforma interna de Asset Management; usa GPT-4 dentro do ambiente cloud do JPMorgan; redução de tempo de research de até 83% (declarado). ⚠️
- **Coach AI** — copiloto para advisors.

### Resultados
- ✅ +30–40% de eficiência reportada por usuários (declaração do banco).
- ✅ Geração de pitch deck que tomava horas de analista júnior em ~30 segundos.
- ✅ +10–20% de produtividade em desenvolvimento de software.
- ✅ Estimativa de US$ 1,5–2,0 bi/ano em valor anual de IA (engloba mais que LLM Suite).
- ✅ Investimento total de US$ 18 bi em tecnologia (2024) com IA como vetor.

### Drivers para LOCAL/privacidade
- Dados regulados (SEC, FINRA, OCC, GDPR cross-border).
- Confidencialidade de cliente em wealth + IB.
- Restrição inicial ao ChatGPT público (2023) que motivou a construção interna.

### Lições / armadilhas
- **Multi-modelo é estratégia**: LLM Suite foi desenhada como **gateway** + 7 LLMs (não 1 modelo único) — alinha com o padrão LiteLLM/Portkey da etapa 2.
- **Adoção exige treinamento e ferramentas verticais** (Connect Coach, Spectrum) — chat genérico tem teto de adoção.
- **Não substitui humanos**: posicionamento explícito como copiloto.

### Fontes
- ✅ <https://www.jpmorganchase.com/about/technology/blog/llmsuite-ab-award>
- ✅ <https://tearsheet.co/artificial-intelligence/jpmorgan-chases-gen-ai-implementation-450-use-cases-and-lessons-learned/>
- ✅ <https://www.cnbc.com/2024/08/09/jpmorgan-chase-ai-artificial-intelligence-assistant-chatgpt-openai.html>
- ✅ <https://www.ciodive.com/news/JPMorgan-Chase-LLM-Suite-generative-ai-employee-tool/726772/>
- ✅ <https://www.jpmorgan.com/insights/markets/indices/indexgpt> (IndexGPT)

## 2. Morgan Stanley — AI @ Morgan Stanley + Debrief + AskResearchGPT

**Setor**: wealth management + IB. **Sede**: EUA.

### Status e escala
- ✅ **Produção**. Roll-out completo aos advisors em set/2023 (primeiro big-bank com GPT-4 customizado em produção).
- ✅ ~15 mil advisors com acesso. **>98% de adoção** declarada em wealth management.
- ✅ **AI @ Morgan Stanley Debrief** (jul/2024): meeting summary com **Whisper + GPT-4**, integra ao CRM.
- ✅ **AskResearchGPT** (2024): primeira aplicação institutional securities; consulta sobre research interno.

### Stack
- VPC dedicada **Azure OpenAI** (parceria estratégica).
- RAG sobre **~100.000 research reports** + documentos internos (knowledge base "intellectual capital").
- Pipeline ASR (Whisper) → resumo (GPT-4) → CRM.

### Casos mapeados (etapa 1)
- **Caso 2** (atendimento ao advisor com RAG), **Caso 6** (sumarização de reuniões), **Caso 7** (extração estruturada para CRM).

### Drivers para LOCAL
- FINRA/SEC compliance.
- Confidencialidade de cliente + research proprietário.
- Cliente consent-based (Debrief só roda com consentimento gravado).

### Fontes
- ✅ <https://www.morganstanley.com/press-releases/key-milestone-in-innovation-journey-with-openai>
- ✅ <https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch>
- ✅ <https://www.morganstanley.com/press-releases/morgan-stanley-research-announces-askresearchgpt>
- ✅ <https://openai.com/index/morgan-stanley/>

## 3. Goldman Sachs — Coding assistant + assistente firmwide

**Setor**: IB / asset management. **Sede**: EUA.

### Status e escala
- ⚠️ **Produção** desde julho/2024 (primeiro tool de geração de código em produção firmwide).
- ⚠️ Pilot inicial com 500 desenvolvedores; expansão para 10k em mid-2024; rollout firmwide acelerado em jan/2025.
- ⚠️ Adoção >70% entre usuários elegíveis.

### Stack
- ⚠️ **LLM custom fine-tuned** sobre datasets internos (e-mails, repos, financial documents).
- ⚠️ Operação em **air-gapped secure cloud** para compliance bancário (GDPR + SEC).
- ⚠️ Integração em IDE + clientes de e-mail.

### Casos mapeados
- **Caso 4** (coding assistant), **Caso 5** (code review), **Caso 1** (chat interno).

### Resultados (declarados)
- ⚠️ –25–35% no tempo de e-mail.
- ⚠️ +40% em ciclos de desenvolvimento (quants e devs).

### Fontes
- ⚠️ <https://www.klover.ai/goldman-sachs-ai-strategy-analysis-of-ai-dominance-in-financial-technology/>
- ⚠️ <https://opendatascience.com/goldman-sachs-rolls-out-ai-assistant-firmwide-to-boost-employee-productivity/>
- ⚠️ <https://fortune.com/2025/06/24/goldman-sachs-internal-ai-assistant/>

## 4. Bloomberg — BloombergGPT (caso ON-PREM mais detalhado tecnicamente)

**Setor**: mídia financeira / data terminals. **Sede**: EUA.

### Status
- ✅ **Modelo proprietário**, treinado e operado internamente.
- ✅ **50B parâmetros**, decoder-only (BLOOM-style + ALiBi).
- ✅ Treinado em **64 × 8 = 512 A100 40GB** por 139.200 steps.
- ✅ Dataset: **363B tokens FinPile** (proprietário, archives desde 2007) + **345B tokens públicos**.

### Por que é referência
- É o **caso público mais detalhado de "modelo on-prem proprietário em finanças"**, com paper técnico (arXiv 2303.17564).
- Demonstra que a mistura **finance + general-purpose** supera ambas em benchmarks financeiros mantendo competitividade geral.
- Tarefas: sentimento, NER financeiro, classificação de notícias, Q&A.

### Limites
- 🟡 Em 2025/2026 sua relevância é discutida — modelos abertos genéricos (Llama 3.3, Qwen, DeepSeek) atingem performance comparável em finanças via RAG e fine-tune.
- ⚠️ Custo de re-treinar do zero ficou rapidamente proibitivo frente a usar Llama/Qwen como base.

### Fontes
- ✅ <https://www.bloomberg.com/company/press/bloomberggpt-50-billion-parameter-llm-tuned-finance/>
- ✅ <https://arxiv.org/abs/2303.17564>
- 🟡 <https://beancount.io/bean-labs/research-logs/2026/05/05/bloomberggpt-large-language-model-finance> (análise crítica 2026)

## 5. Itaú Unibanco — "Inteligência Itaú" (Brasil)

**Setor**: banco universal. **Sede**: BR. ~100 mil funcionários.

### Status e escala
- ✅ **Produção** desde 2024.
- ✅ **Inteligência de Investimentos**: 100 mil clientes em nov/2025 (10 mil em jun/2025).
- ✅ +84% no volume de iniciativas de IA generativa em uso (2025 vs 2024).
- ✅ +35% na velocidade de implantações tecnológicas.
- ✅ "Itaú Emps" para empreendedores; Pix no WhatsApp para 100% dos clientes.

### Stack
- ✅ **Multi-agente** com **Anthropic + Meta (Llama) + soluções próprias**. Fine-tuning sobre dados internos.
- ✅ Mistura de modelos abertos e comerciais — não detalham percentual on-prem.
- ⚠️ Migração reportada do core para AWS (não significa que LLM seja em AWS; alguns casos são).

### Casos mapeados
- **Caso 1** (chat interno), **Caso 2** (atendimento RAG), **Caso 7** (extração).

### Fontes
- ✅ <https://medium.com/itautech/desenvolvendo-a-intelig%C3%AAncia-ita%C3%BA-a-constru%C3%A7%C3%A3o-de-uma-arquitetura-de-ia-multiagentes-com-foco-no-5819d71fd3bc>
- ✅ <https://convergenciadigital.com.br/mercado/itau-unibanco-expande-ia-generativa-de-investimentos-para-100-mil-clientes/>
- ⚠️ <https://tiinside.com.br/11/02/2026/itau-avanca-35-em-velocidade-de-implantacoes-tecnologicas-em-2025-e-amplia-uso-de-ia-generativa-na-experiencia-dos-clientes/>

## 6. Bradesco — BIA + Plataforma Bridge (Brasil)

**Setor**: banco universal. **Sede**: BR.

### Status e escala
- ✅ **Produção**. BIA ativa desde 2016 (IBM Watson); migração para **plataforma proprietária "Bridge"** em abril/2024.
- ⚠️ **82–90% de retenção em 1º nível** de atendimento digital (2025) — declarado.
- ⚠️ **24 milhões** de usuários do app interagem com BIA.
- ⚠️ **R$ 400 mi** em benefícios atribuídos a IA generativa em 2025.
- ✅ Aquisição da **Kunumi** (spin-off UFMG, 100+ engenheiros de GenAI).

### Stack
- ⚠️ **Bridge** (plataforma própria) sobre **IBM watsonx + outros LLMs**.
- ⚠️ BIA evoluiu de regras determinísticas (Watson clássico) → IA generativa.

### Casos mapeados
- **Caso 2** (atendimento), **Caso 11** (compliance/classificação).

### Fontes
- ✅ <https://www.ibm.com/blogs/ibm-comunica/com-bia-bradesco-e-ibm-transformam-o-atendimento-de-milhoes-de-usuarios/>
- ⚠️ <https://www.bloomberglinea.com.br/negocios/ia-generativa-resolve-82-dos-atendimentos-iniciais-no-bradesco-diz-diretora/>
- ⚠️ <https://tiinside.com.br/11/06/2025/com-ia-generativa-bia-ja-retem-ate-90-das-demandas-no-atendimento-digital-do-bradesco/>

## 7. BTG Pactual — Saturn Platform (Brasil)

**Setor**: banco de investimento + asset. **Sede**: BR.

### Status e escala
- ✅ **Produção** (assistente WhatsApp, fev/2025) + **Saturn Platform** descrita em paper arXiv (2312.07721).
- ✅ Capacidades: agentic AI, LLMs, virtual assistants, large-scale voice transcription.

### Stack
- ✅ **Saturn Platform**: orquestração proprietária para Foundation Model lifecycle (build + deploy + integração com IT ops).
- ✅ Multi-modal: texto + imagem + voz (assistente WhatsApp interpreta áudio, imagem e manuscrito).

### Casos mapeados
- **Caso 1**, **Caso 2**, **Caso 7**.

### Fontes
- ✅ <https://arxiv.org/html/2312.07721v1> (Saturn Platform paper)
- ✅ <https://itforum.com.br/noticias/btg-pactual-assistente-whatsapp/>
- ✅ <https://github.com/BTGPactual> (presença pública em open source, mas recursos limitados)

## 8. Nubank (Brasil)

**Setor**: banco digital. ~110M clientes em 4 países.

### Status e escala
- ⚠️ **Produção parcial / POC ativo**. Três vertentes: interpretação de documentos não-estruturados, customização de discurso, copilots de atendentes.
- ⚠️ **40% dos chats** totalmente automatizados.
- ⚠️ Construção de modelos próprios em curso (7 TB/dia de dados).

### Casos mapeados
- **Caso 2** (atendimento), **Caso 7** (extração).

### Stack
- 🟡 Pouco detalhe público; provável híbrido (modelos open + APIs).

### Fontes
- ⚠️ <https://www.mobiletime.com.br/noticias/15/05/2024/nubank-testa-ia-generativa-em-tres-vertentes-revela-cto/>
- ⚠️ <https://building.nubank.com/ai-at-nubank-how-one-of-the-largest-digital-banks-in-the-world-uses-artificial-intelligence/>

## 9. BBVA (Espanha) — caso transparente de **API pública governada**

**Setor**: banco universal global. **Sede**: ES.

### Status e escala
- ✅ **Produção em escala** com **ChatGPT Enterprise**: licenças escalaram de **3.300 → 11.000**.
- ✅ **Google Workspace + Gemini** para 87.000 funcionários (mais amplo).
- ✅ +1.000 data scientists no quadro.
- ✅ +20.000 GPTs custom criados; 4.000+ usados regularmente.
- ✅ +80% dos licenciados usam diariamente; ~3 horas/semana economizadas.

### Por que vale citar mesmo sendo API pública
- Mostra **caminho alternativo** com governança rigorosa via **Enterprise plans (data não usado para treino)**.
- ROI publicado e benchmark da Harvard Business Review (BBVA = referência de adoção corporativa).
- Útil como **contraponto** à abordagem on-prem.

### Fontes
- ✅ <https://openai.com/index/bbva-collaboration-expansion/>
- ✅ <https://www.bbva.com/en/innovation/bbva-deploys-the-eight-its-strategy-to-transform-the-financial-experience-with-ai/>
- ✅ <https://www.googlecloudpresscorner.com/2025-07-02-BBVA-Deepens-Partnership-with-Google-Cloud-to-Innovate-with-AI>

## 10. ING (Holanda) — abordagem "conservatively aggressive"

- 🟡 Discurso oficial: 5 áreas focadas sob COO; pouco detalhe técnico público.
- ✅ Útil como exemplo de **governança** + risk management europeu (DORA, GDPR).
- Fontes: declarações do CTO global em imprensa especializada.

## 11. Santander

- 🟡 Cobertura pública limitada (parcerias com fintechs e automação). Sem deployment LLM público bem detalhado em fontes que pudemos verificar.

## Síntese do setor

| Empresa | Topologia | Padrão |
|--------|-----------|--------|
| JPMorgan | VPC controlada multi-modelo | Gateway próprio + 7 LLMs (Anthropic/OpenAI/Meta) |
| Morgan Stanley | VPC Azure OpenAI dedicada | Single-vendor profundo + RAG |
| Goldman | Air-gap cloud privada | Custom fine-tune proprietário |
| Bloomberg | ON-PREM (HPC interno) | Modelo proprietário do zero |
| Itaú | Híbrido multi-modelo | Multi-agente Anthropic+Llama+próprio |
| Bradesco | Híbrido — Bridge + watsonx | Plataforma proprietária + IBM |
| BTG | VPC + Saturn | Plataforma própria com voz/imagem |
| Nubank | Híbrido | Modelos próprios em construção |
| BBVA | API Pública Enterprise | OpenAI+Gemini com governança |
| ING | Híbrido conservador | Pouco detalhe público |

**Padrão observado**: bancos US grandes vão para VPC dedicada / air-gap com Azure OpenAI; bancos BR vão multi-modelo híbrido com forte presença de Llama + Anthropic + IBM watsonx; europeus oscilam entre governança rígida (ING) e API pública governada (BBVA). **Bloomberg permanece o caso mais on-prem/proprietário.**
