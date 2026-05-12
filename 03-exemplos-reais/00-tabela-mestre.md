# Tabela Mestre — Casos Públicos de IA Generativa Corporativa

> Documento parte da Etapa 3/5 da proposta. Foco: empresas grandes/médias com deployments de IA generativa, com ênfase em on-premises / nuvem privada / dados sensíveis. Maio/2026.

## Como ler

- **Status**: Produção / Piloto / POC / Abandonado / Indefinido
- **Topologia**: ON-PREM (data center próprio) / VPC (cloud single-tenant) / SaaS-Enterprise (multi-tenant com isolamento) / API-Pública (OpenAI/Anthropic/Google nativo) / HÍBRIDA
- **Fonte**: blog corporativo / press release / imprensa especializada / paper / GitHub
- **Verificação**: vê **Legendas** abaixo

### Legendas de confiança
- ✅ verificado em fonte primária (blog corporativo, press release, paper)
- ⚠️ second-hand / imprensa especializada citando empresa (não checado em primária)
- 🟡 inferido (declarações genéricas, "uses AI", sem nomes/números)

## Tabela mestre

| # | Empresa | Setor | País | Caso (mapa 1–14) | Status | Topologia | Modelo / Stack mencionada | Escala | Verif. |
|---|---------|-------|------|-------------------|--------|-----------|---------------------------|--------|---------|
| 1 | JPMorgan Chase | Banco | EUA | 1, 4, 6, 7 | Produção | VPC (Azure) — multi-modelo controlado | "LLM Suite" — 7 LLMs (OpenAI, Anthropic, Meta) com gateway próprio | 230k+ usuários, 600+ casos, US$1,5–2bi/ano valor | ✅ |
| 2 | Morgan Stanley | Banco | EUA | 2, 6, 7 | Produção | VPC (Azure OpenAI) | GPT-4 + Whisper, RAG sobre 100k research reports | 15k advisors, 98% adoção em wealth | ✅ |
| 3 | Goldman Sachs | Banco | EUA | 4, 5 | Produção | Cloud privada air-gapped (Azure) | LLM custom fine-tuned (multi-modelo) | 10k+ usuários, 70%+ adoção, +25–35% e-mail, +40% código | ⚠️ |
| 4 | Bloomberg | Mídia financeira | EUA | 7, 8 | Produção | ON-PREM (HPC interno) | BloombergGPT 50B (BLOOM-style, ALiBi) — proprietário | Treinado em 64×8 A100 40GB; 363B tokens FinPile | ✅ |
| 5 | Itaú Unibanco | Banco | BR | 1, 2, 7 | Produção | HÍBRIDA — multi-agente sobre Anthropic + Meta + próprios | "Inteligência Itaú" multi-agente; Anthropic + Llama + custom | 100k clientes em IA invest., +84% iniciativas em 2025 | ✅ |
| 6 | Bradesco | Banco | BR | 2, 11 | Produção | HÍBRIDA — Bridge (próprio) sobre IBM watsonx + LLMs | Plataforma "Bridge" + BIA (24M usuários) | 82–90% retenção 1º nível; R$400M benefício/ano | ⚠️ |
| 7 | BTG Pactual | Banco | BR | 1, 2, 7 | Produção | VPC (Saturn Platform interna) | "Saturn Platform" para FM lifecycle; LLMs + voz | Assistente WhatsApp para clientes; ASR em escala | ✅ |
| 8 | Nubank | Banco digital | BR | 2, 7 | Produção/POC | HÍBRIDA — não publicado em detalhe | Modelos próprios em desenvolvimento; 7 TB/dia processados | 40% chats automatizados; 3 vertentes em produção | ⚠️ |
| 9 | BBVA | Banco | ES | 1, 9 | Produção | API-Pública (OpenAI Enterprise) + Google (Gemini) | ChatGPT Enterprise + Gemini Workspace | 11k licenças OpenAI; 87k usuários Gemini; 20k+ GPTs custom | ✅ |
| 10 | Santander | Banco | ES | 1, 7 | Produção | HÍBRIDA — pouco detalhe público | Não publicado | — | 🟡 |
| 11 | ING | Banco | NL | 2, 11 | Produção/Piloto | HÍBRIDA — "conservatively aggressive" | 5 áreas focadas sob COO | — | 🟡 |
| 12 | Bayer | Farma | DE | 7, 13 | Piloto | ON-PREM/VPC + parceria Recursion (LOWE) | LOWE para drug discovery; Aleph Alpha em outros pilotos | 1º beta external de LOWE em 2024 | ✅ |
| 13 | Pfizer | Farma | EUA | 1, 6, 7 | Produção | VPC (Azure OpenAI + Charlie) | "Charlie" platform (lançado fev/2024) | Acelerador NVIDIA + Tribe (out/2024) | ✅ |
| 14 | Roche / Genentech | Farma | CH/EUA | 7, 13 | Produção | HÍBRIDA — "Lab in a Loop" | GenAI integrada em discovery loop | — | ⚠️ |
| 15 | Novartis | Farma | CH | 7, 13 | Produção | HÍBRIDA — Microsoft + AI Innovation Lab | Frameworks ML em parceria com MS | — | ⚠️ |
| 16 | Mayo Clinic | Hospital | EUA | 3, 7, 13 | Produção | ON-PREM (DGX SuperPOD B200) + Google Cloud | Foundation models próprios (Atlas pathology) | 26 PB de dados; 1,2M slides; >200 projetos AI | ✅ |
| 17 | Cleveland Clinic | Hospital | EUA | 1, 7 | Produção | HÍBRIDA (Epic + Ambience + Bayesian) | Ambient documentation + sepsis detection | 4k+ clinicians; –14 min/dia EHR; 13 hospitais | ⚠️ |
| 18 | NHS (UK) | Saúde pública | UK | 6, 7 | Piloto/POC | ON-PREM (NHS Federated Data Platform) | Vários pilotos (radiology, ambient scribe) | — | 🟡 |
| 19 | Bosch | Indústria | DE | 1, 9 | Produção | HÍBRIDA — open-source + Aleph Alpha + GPT | "AskBosch" + ROB HR Agent (Cognigy) | ROB em 25 países; 120 use cases no GenAI Champ | ✅ |
| 20 | Siemens | Indústria | DE | 4, 9 | Produção | VPC (Azure OpenAI + Xcelerator) | "Industrial Copilot" (GPT) | 100+ empresas usando; ThyssenKrupp, Schaeffler | ✅ |
| 21 | BMW Group | Auto | DE | 7, 9 | Produção | HÍBRIDA — AWS + Alexa LLM + GenAI Purchasing | "AIconic Agent" multi-agente em compras | Knowledge Navigator + Tender Assistant em produção | ✅ |
| 22 | Mercedes-Benz | Auto | DE | (in-car) | Produção | EDGE/HÍBRIDA — MB.OS + LLM in-car | LLM-powered MBUX Virtual Assistant | Lançamento 2025 frota nova | ✅ |
| 23 | Embraer | Aeroespacial | BR | (inovação) | Piloto | SAP innovation tournament | GenAI sobre SAP — não publicado | — | 🟡 |
| 24 | Petrobras | Energia | BR | 1, 6 | Produção | VPC (Azure OpenAI) | "ChatPetrobras" (GPT em Azure OpenAI) | 110k trabalhadores | ✅ |
| 25 | Vale | Mineração | BR | 7 | Piloto | SAP — GenAI manutenção | GenAI em controle de manutenção (vencedora SAP Now 2024) | — | ⚠️ |
| 26 | Walmart | Varejo | EUA | 1, 6, 12 | Produção | HÍBRIDA — proprietária "Element" + LLMs próprios "Wallaby" | "My Assistant" (50k→75k+) + Wallaby retail-LLM | 75k+ associates corp, 11 países, 1,5M frontline | ✅ |
| 27 | Mercado Livre | E-commerce | LATAM | 4, 9 | Produção | HÍBRIDA — uso de GenAI image + dev | GenAI image gen para sellers + dev tools | — | ⚠️ |
| 28 | Snowflake (Cortex) | SaaS | EUA | 3, 7 | Produção | SaaS-Enterprise | Cortex Code; Arctic LLM (open) | 50%+ clientes ativos em Cortex Code (lançado nov/2025) | ✅ |
| 29 | Databricks (DBRX) | SaaS | EUA | 3, 4 | Produção | SaaS-Enterprise | DBRX (open MoE) | Adoção em finance, legal, healthcare, manuf. | ✅ |
| 30 | Red Hat (interno) | TI | EUA | 1, 10 | Produção | OpenShift AI on AWS | RHEL AI + OpenShift AI | 4 soluções em produção; US$5M de cost avoidance | ✅ |
| 31 | ARSAT | Telecom estatal | AR | 7, 10 | Produção | OpenShift AI | RAG supply chain | Reduziu response time e OPEX | ✅ |
| 32 | Cloudera | SaaS/Data | EUA | (infra) | Produção | NIM + Cloudera | NIM microservices | 36× perf boost (declarado por NVIDIA) | ⚠️ |
| 33 | Oracle (OCI) | Cloud | EUA | (infra) | Produção | NIM via OCI Console | 160+ tools NVIDIA AI Enterprise | Lançado mar/2025 | ✅ |
| 34 | IBM (watsonx) | TI | EUA | 1, 7, 13 | Produção | watsonx + NIM + Granite | Granite 3/4 + InstructLab + watsonx.ai | Vários clientes regulados (BNP, gov, saúde) | ✅ |

> Outras empresas referenciadas em arquivos por setor (Carrefour, Magalu, B3, NSA, DoD, Singapura, Albert Einstein, Sírio-Libanês, Albertsons etc.) — quando os dados públicos forem fracos, a entrada está marcada 🟡 e o tratamento é breve.

## Síntese rápida

- **Casos com forte ON-PREM** (data center próprio, GPUs do cliente): Bloomberg (BloombergGPT), Mayo Clinic (DGX SuperPOD), parte da stack de Bayer (Aleph Alpha em DC alemão), Red Hat (OpenShift AI on-prem em vários clientes — ARSAT é exemplo público), JPMorgan (LLM Suite tem componentes em VPC dedicada controlada).
- **Casos VPC / nuvem privada com isolamento contratual**: maioria dos bancos US (JPMorgan, Morgan Stanley, Goldman) usa Azure OpenAI dedicado / air-gap; BBVA usa ChatGPT Enterprise + Gemini Workspace; Petrobras usa ChatPetrobras sobre Azure OpenAI; Siemens Industrial Copilot sobre Azure OpenAI.
- **Padrão híbrido brasileiro**: Itaú/Bradesco usam multi-modelo (Anthropic + Meta + custom + IBM watsonx) com camada própria de orquestração (Bridge no Bradesco, multi-agente no Itaú).
- **Casos puramente API pública**: BBVA é o exemplo mais transparente — ChatGPT Enterprise para 11k usuários, com governança.

## Observações sobre stack e licenças

- **Modelo aberto rodando em produção corporativa observado em fontes**: Llama (Meta) na maioria dos bancos BR e em Walmart/Wallaby; Granite (IBM) em clientes regulados via watsonx; DBRX (Databricks) em finance/legal/healthcare; Arctic (Snowflake) é mais para infra interna do Snowflake.
- **Modelos comerciais via API ainda dominam o front-of-house corporativo** (Azure OpenAI / OpenAI Enterprise / Anthropic / Gemini). On-prem puro com modelo aberto é mais comum em **(a)** áreas reguladas que exigem air-gap, **(b)** casos com IP sensível (drug discovery, código proprietário, dados clínicos com LGPD/HIPAA), **(c)** organizações com GPU já provisionada (Bloomberg, Mayo).
- **Bloomberg é o caso "puro on-prem com modelo proprietário"** mais documentado tecnicamente (paper arxiv 2303.17564). É provavelmente o mais próximo do desenho que esta proposta sugere para a empresa.

## Observação metodológica

Esta tabela prioriza profundidade onde há fontes primárias. Casos como Embraer, Vale, Magalu, NSA/CIA têm cobertura pública limitada — estão registrados, com o rótulo apropriado, e tratados de forma resumida. Quando o caso é misto (parte API pública, parte privada), explicitamos.
