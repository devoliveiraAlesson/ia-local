# Indústria e Manufatura — Casos Públicos

> Setor com IP intensivo (designs, especificações, processos), normalmente cloud privada ou híbrida. Drivers: confidencialidade industrial (segredo de fabricação), conformidade ITAR/EAR, soberania nacional (especialmente DE/EU), grande volume de documentação técnica.

## 1. Bosch (Alemanha)

**Setor**: componentes automotivos + appliances + IoT. ~430 mil funcionários.

### Status e escala
- ✅ **Produção**. Estratégia híbrida: open source + big tech APIs + **Aleph Alpha** para IP estratégico.
- ✅ **AskBosch**: chat com dados internos + externos.
- ✅ **ROB** (HR AI Agent): sobre **Cognigy.AI + GPT**, em **25 países**.
- ✅ **GenAI Championship 2024**: 120 use cases submetidos internamente.
- ✅ Bosch Tech Day 2025: investimento massivo em IA como growth driver.

### Stack
- ✅ **Hybrid**: open source + GPT-via-Azure + **Aleph Alpha** para áreas com IP corporativo sensível.
- ✅ Cognigy.AI como camada de NLU para o agente HR.

### Casos mapeados
- **Caso 1** (chat interno via AskBosch), **Caso 9** (Q&A sobre políticas via ROB), **Caso 12** (treinamento e onboarding).

### Drivers para LOCAL/Aleph Alpha
- Soberania de dados europeia.
- Segredos industriais e know-how de fabricação automotiva.

### Fontes
- ✅ <https://www.bosch.com/stories/topics/ai-for-a-better-future-at-bosch/>
- ✅ <https://www.hannovermesse.de/en/news/news-articles/bosch-s-genai-strategy>
- ✅ <https://www.cognigy.com/en/case-study/bosch>

## 2. Siemens — Industrial Copilot (deep dive)

**Setor**: automação industrial / digitalização. **Sede**: DE.

### Status e escala
- ✅ **Produção** desde **julho/2024** (general availability).
- ✅ **+100 empresas** usando, incluindo **ThyssenKrupp Automation Engineering**, **Schaeffler**.
- ✅ Vencedor do **Hermes Award 2025** (Hannover Messe).
- ✅ Engenheiros geram visualizações de painel em 30s; código com 20% de adaptação manual.

### Stack
- ✅ **Siemens Xcelerator** (digital business platform) + **Microsoft Azure OpenAI Service (GPT-4)**.
- ✅ Componentes para PLC code generation em linguagem natural; expansão recente para módulo de manutenção.

### Casos mapeados
- **Caso 4** (coding — geração de código PLC), **Caso 6** (sumarização de specs), **Caso 9** (geração de docs técnicos).

### Drivers para LOCAL/VPC dedicada
- IP industrial (PLCs e simulações são parte do core de Siemens Xcelerator).
- Compliance com cliente final (que muitas vezes exige isolamento).
- Distribuição via Siemens Xcelerator garante **camada de governança própria** sobre Azure OpenAI.

### Fontes
- ✅ <https://www.siemens.com/global/en/products/automation/topic-areas/industrial-ai/industrial-copilot.html>
- ✅ <https://press.siemens.com/global/en/pressrelease/bringing-generative-ai-industry-siemens-industrial-copilot-wins-hermes-award-2025>
- ✅ <https://aimagazine.com/articles/siemens-expanded-industrial-copilot-adopted-by-thyssenkrupp>
- ✅ <https://news.microsoft.com/source/2024/10/24/siemens-and-microsoft-scale-industrial-ai>

## 3. BMW Group

**Setor**: automotivo premium. **Sede**: DE.

### Status e escala
- ✅ **Produção**. **AIconic Agent** (2024): multi-agente para **Compras + Supplier Network**.
- ✅ Componentes em produção: **Knowledge Navigator**, **Offer Analyst**, **Tender Assistant**.
- ✅ Hub de IA em **Cluj-Napoca, Romênia** (joint venture com NTT DATA Romania, fundado verão/2024).
- ✅ **GenAI in-car** com Alexa LLM apresentado na CES 2024.
- ✅ **AWS GenAI Cloud Optimization Assistant** (case AWS) — assistente para otimização de infra interna.

### Stack
- ✅ **HÍBRIDA**: AWS + Alexa LLM (in-car) + GenAI próprio em compras (AIconic) + parceria NTT DATA.

### Casos mapeados
- **Caso 7** (extração estruturada — análise de tenders), **Caso 9** (knowledge nav técnico).

### Fontes
- ✅ <https://www.press.bmwgroup.com/global/article/detail/T0450032EN/greater-efficiency-and-productivity-with-artificial-intelligence-%E2%80%93-generative-ai-in-bmw-group-purchasing>
- ✅ <https://aws.amazon.com/solutions/case-studies/bmw-generative-ai/>
- ⚠️ <https://procurementmag.com/technology-and-ai/bmw-procurement-digital-transformation>

## 4. Mercedes-Benz

**Setor**: automotivo premium. **Sede**: DE.

### Status
- ✅ **MB.OS** + LLM-powered **MBUX Virtual Assistant** lançado em 2025 nos veículos.
- ⚠️ Parceria com Siemens em "digital energy twin" para fábricas.
- 🟡 Detalhamento de stack interno corporativo (não in-car) menos publicado.

### Casos mapeados
- (in-car / experiência do produto)

## 5. Volkswagen

- 🟡 Sem caso público forte e bem documentado de LLM corporativo on-prem mapeado em nossa pesquisa em maio/2026 (cobertura mais focada em parcerias com Microsoft Cloud para in-car).

## 6. Embraer (Brasil)

**Setor**: aeroespacial. **Sede**: BR.

### Status
- ⚠️ Participação em **SAP innovation tournament** com prototipação GenAI (SAP Now Brasil).
- 🟡 Detalhamento técnico de deploy interno **não publicado em fontes primárias verificáveis** em nossa pesquisa.

## 7. Petrobras — ChatPetrobras (Brasil)

**Setor**: óleo e gás. **Sede**: BR. ~110 mil trabalhadores e prestadores.

### Status e escala
- ✅ **Produção** desde 2024.
- ✅ **ChatPetrobras** disponibilizada a **110.000 trabalhadores** (empregados + serviços) via portal interno.
- ✅ Construído sobre **GPT (Azure OpenAI Service)** com políticas internas de segurança, LGPD, e regulação governamental brasileira.

### Stack
- ✅ **VPC Azure OpenAI** com governança interna.
- ✅ Não é on-prem, mas é **caso brasileiro grande de empresa estatal** com privacidade tratada via tenant Azure dedicado.

### Casos mapeados
- **Caso 1** (chat interno corporativo), **Caso 6** (sumarização de relatórios técnicos).

### Fontes
- ✅ <https://agencia.petrobras.com.br/w/petrobras-cria-ferramenta-com-inteligencia-artificial-generativa-para-apoiar-mais-de-100-mil-trabalhadores>
- ⚠️ <https://enkiai.com/petrobras-ai-initiatives-for-2025-key-projects-strategies-and-partnerships>

## 8. Vale

**Setor**: mineração. **Sede**: BR.

### Status
- ⚠️ Vencedora do **SAP innovation tournament** (SAP Now Brasil 2024) com solução GenAI integrando controle de manutenção com retorno automático de excedentes (sustentabilidade + manutenção).
- 🟡 Sem detalhamento público sobre topologia LLM on-prem corporativa.

### Casos mapeados
- **Caso 7** (extração — manutenção).

## Síntese do setor

| Empresa | Topologia | Padrão |
|--------|-----------|--------|
| Bosch | Híbrido + Aleph Alpha + GPT | Soberania para IP estratégico |
| Siemens | VPC Azure + Xcelerator | Industrial Copilot vendido para outros clientes |
| BMW | AWS + multi-agente próprio | Compras com agentes; Romenia hub |
| Mercedes | In-car + Siemens parceria | LLM no produto, não no back-office |
| Embraer | SAP + GenAI tournament | POC, sem detalhe |
| Petrobras | VPC Azure OpenAI | Estatal grande BR; 110k usuários |
| Vale | SAP + GenAI tournament | POC manutenção |

**Padrões**:
- **Indústria alemã** = híbrido com **Aleph Alpha** ou **Azure OpenAI** + governança interna pesada (DGCL, BetrVG, conselhos de trabalhadores).
- **OEMs automotivos** = mistura **in-car LLM** (Alexa, MBUX) + **back-office GenAI**.
- **Industrial Copilot da Siemens** virou **plataforma de mercado**: 100+ clientes industriais usando-a (dado mais robusto de adoção em manuf.).
- **BR estatal/pesada** = Azure OpenAI VPC ou parcerias SAP.

**Drivers para LOCAL** mais citados em manuf.:
- Segredos industriais (designs, processos).
- ITAR/EAR (defesa, aeroespacial — Embraer).
- Soberania europeia (Aleph Alpha).
- Documentação técnica massiva (manuais de máquinas, BOMs).
