# Governo e Defesa — Casos Públicos

> Setor com requisitos de classificação (TS/SCI, Confidencial, Restrito), soberania nacional, e múltiplas redes (NIPR/SIPR/JWICS no caso US). É frequentemente o **gatilho mais forte para ON-PREM puro**.

## 1. CIA / Comunidade de Inteligência (EUA) — Osiris

**Setor**: inteligência (18 agências US IC). **Sede**: EUA.

### Status e escala
- ✅ **Produção** — IOC (initial operational capability) em 2023.
- ✅ Usado por **milhares de analistas** em 18 agências da IC.
- ✅ Posicionamento oficial: "absolute home run for us" (CTO da CIA).

### Stack
- ⚠️ Sobre **OSE (open source environment)** — isto é, **dados não-classificados, públicos ou comerciais**.
- ⚠️ **Múltiplos modelos comerciais** (multi-vendor); CIA não publica detalhes específicos.
- ⚠️ Foco: sumarização anotada + chatbot para Q&A sobre OSINT.

### Casos mapeados (etapa 1)
- **Caso 6** (sumarização), **Caso 11** (classificação/triagem), **Caso 14** (análise de e-mails / artigos).

### Drivers para LOCAL
- Mesmo em OSINT, a IC mantém isolamento de rede (não acessa Internet pública diretamente).
- Avaliação contínua de hallucination + audit trail.

### Fontes
- ✅ <https://www.pbs.org/newshour/world/u-s-intelligence-agencies-embrace-of-generative-ai-is-at-once-wary-and-urgent>
- ✅ <https://wtop.com/national/2024/05/insider-qa-cias-chief-technologists-cautious-embrace-of-generative-ai/>

## 2. DoD / CDAO — Task Force Lima → AI Rapid Capabilities Cell

**Setor**: defesa. **Sede**: EUA.

### Status
- ✅ Task Force Lima rodou de 2023 a dez/2024.
- ✅ **Sucessor**: **AI Rapid Capabilities Cell (AI RCC)**, em parceria com **DIU (Defense Innovation Unit)**.
- ✅ **US$ 100 mi** de FY24/FY25 alocados; US$ 35 mi para 4 frontier AI pilots em sprints de 90 dias (GIDE series).
- ✅ US$ 40 mi em SBIR contracts para non-traditional vendors.

### Casos prováveis (não detalhados)
- Tradução, sumarização de inteligência, RAG sobre regulações DoD, code/cyber defense.

### Drivers para LOCAL
- Classified networks (SIPR, JWICS) — air-gap absoluto.
- Vendor sovereignty (preferência por non-traditional + DIB).

### Fontes
- ✅ <https://defensescoop.com/2024/12/11/cdao-pentagon-generative-ai-rapid-capabilities-cell-sunset-task-force-lima/>
- ✅ <https://breakingdefense.com/2024/12/pentagon-launches-new-generative-ai-cell-with-100m-for-pilots-experiments/>
- ✅ <https://www.ai.mil/Portals/137/Documents/Resources%20Page/2024-12-TF%20Lima-ExecSum-TAB-A.pdf>

## 3. UK Government — Caddy + GOV.UK Chat + Redbox

**Setor**: governo. **Sede**: UK.

### Status e escala
- ✅ **Caddy**: AI-powered copilot para customer service agents (publicado pelo i.AI / GOV.UK).
- ✅ **GOV.UK Chat**: experimento aberto em jan/2024; private beta nov/2024 — chatbot que responde com base só em conteúdo publicado em GOV.UK.
- ✅ **Redbox**: rolled out a **6.000+ usuários**, 150.000 chats, 1,3 mi mensagens. Sunset em 2025 quando MS Copilot e Gemini ficaram amplamente disponíveis no governo.
- ✅ **Parliament MCP** (open source) — habilitando navegação de Hansard via LLMs existentes.

### Stack
- ✅ Mix entre **Redbox (open-source próprio do governo, base Llama)** e ferramentas comerciais (Copilot, Gemini Workspace).
- ✅ Padrão: **stack própria onde dados são sensíveis (Redbox); SaaS com licenças government onde não**.

### Drivers para LOCAL
- UK GDPR + sensibilidade política.
- Soberania (especialmente após DSIT/AISI).

### Fontes
- ✅ <https://insidegovuk.blog.gov.uk/2024/01/18/the-findings-of-our-first-generative-ai-experiment-gov-uk-chat/>
- ✅ <https://insidegovuk.blog.gov.uk/2024/11/05/were-running-a-private-beta-of-gov-uk-chat/>
- ✅ <https://ai.gov.uk/projects/caddy/>

## 4. Singapura — Pair (deep dive de governo)

**Setor**: governo / serviços públicos. **Sede**: SG.

### Status e escala
- ✅ **Produção em massa** — Pair é a forma mais popular de servidores públicos usarem IA na rotina.
- ✅ **>60.000 usuários registrados**, **>20.000 weekly active users**, **>10 mi mensagens**.
- ✅ Estimativa: **46% de redução** no tempo administrativo declarado.
- ✅ **Cleared para Restricted/Sensitive Normal** sem logging pelo provider de LLM.
- ✅ Disponível **gratuitamente em todos os laptops government-issued**.

### Stack
- ✅ Múltiplos LLMs por trás (público sobre uso de **Meta Llama**, entre outros).
- ✅ Deployed pelo Open Government Products + GovTech Singapore.
- ✅ Suite de produtos: **Pair Chat** (chat seguro), **Pair Noms** (atas em <1h), **Pair Search** (debates parlamentares + jurisprudência), **Pair Intern** (acesso por e-mail).

### Casos mapeados
- **Caso 1** (chat interno), **Caso 6** (Pair Noms), **Caso 7** (Pair Search), **Caso 12** (treinamento).

### Por que é o caso de governo mais inspirador
- Modelo **transparente, com métricas reais** publicadas em report cards (open.gov.sg/pair).
- Política clara: "no logging by LLM providers" — design contratual + técnico.
- Disponibilidade universal (todos servidores).

### Fontes
- ✅ <https://pair.gov.sg/>
- ✅ <https://www.developer.tech.gov.sg/products/categories/productivity-tools/pair/overview>
- ✅ <https://reports.open.gov.sg/pair/updates>

## 5. Brasil — Serpro + Dataprev (deep dive)

**Setor**: governo federal — empresas estatais de TI.

### Status e escala
- ✅ **SerproLLM** em desenvolvimento — busca de parceria de mercado para um LLM treinado em **português brasileiro**, instanciado **dentro do Serpro** (técnico-administrado lá).
- ✅ **ConversAÍ Studio** — solução tipo "ChatGPT do governo" com **execução em servidores GPU dos próprios datacenters do Serpro** — dados sensíveis não saem do ambiente governamental.
- ✅ Coalizão: Serpro + MGI + MCTI + Dataprev + Enap.
- ✅ "Pesquisa inteligente" sobre legislação federal — ferramenta em produção.
- ✅ Painéis Serpro+Dataprev+BB+Caixa para coordenar IA em serviços ao cidadão.
- ✅ **SoberanIA (Piauí)** usa data center da Telebras + busca apoio Serpro/Dataprev — modelo soberano regional.

### Stack
- ✅ **ON-PREM puro** em data centers Serpro com GPUs.
- ⚠️ Detalhamento técnico (modelo base, runtime) ainda em construção em maio/2026.

### Por que é a referência mais relevante para a proposta
- **Caso brasileiro real de IA on-prem soberana operada por estatal**.
- Demonstra que existe capacidade técnica + política BR para ON-PREM.

### Casos mapeados
- **Caso 1** (chat seguro), **Caso 11** (PII, classificação), **Caso 7** (extração — legislação).

### Fontes
- ✅ <https://www.serpro.gov.br/menu/noticias/noticias-2025/serpro-ia-em-portugues>
- ✅ <https://www.serpro.gov.br/menu/noticias/noticias-2025/conversai-studio>
- ✅ <https://www.serpro.gov.br/menu/noticias/noticias-2024/IA-governo-federal>
- ✅ <https://convergenciadigital.com.br/governo/serpro-llm-proprio-passa-por-lago-de-dados-abastecido-pelo-governo/>
- ✅ <https://www.serpro.gov.br/menu/noticias/noticias-2025/serpro-gigantes-ia>

## 6. NSA / outras agências US

- 🟡 Cobertura pública limitada por classificação. Sabe-se que IC usa Osiris (ver item 1) e que há esforços de RAG sobre código aberto.

## Síntese do setor

| Entidade | Topologia | Padrão |
|----------|-----------|--------|
| CIA / IC | Air-gapped, multi-modelo comercial | Osiris para OSINT, milhares de analistas |
| DoD CDAO | Air-gapped + DIU | $100M frontier pilots, AI RCC |
| UK Gov | Mix Redbox próprio + Copilot/Gemini | Pragmatismo: SaaS onde possível, próprio onde sensível |
| Singapura (Pair) | VPC governo + multi-modelo | Universal, gratuito, com governança transparente |
| Serpro (BR) | ON-PREM puro em DC governo | Soberania + LLM em pt-BR |

**Padrões**:
- Governo é o setor mais **soberania-driven**: ON-PREM puro é mais comum aqui que em qualquer outro setor.
- **Singapura** é a referência operacional + de adoção (números claros).
- **Serpro** é a referência mais relevante para empresa BR querendo replicar postura soberana.
- DoD/CIA mostram que **air-gap + multi-modelo + governance** é viável em escala.

**Drivers para LOCAL**:
- Classificação de informação (US TS/SCI, BR Sigiloso/Reservado).
- Soberania nacional (ConversAÍ é "data não sai do governo BR").
- Custo (governos são price-sensitive).
- Idioma (LLM em pt-BR é diferencial soberano).
