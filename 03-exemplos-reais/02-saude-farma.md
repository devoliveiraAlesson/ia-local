# Saúde e Farmacêutica — Casos Públicos

> Setor com regulação severa (HIPAA, LGPD, GDPR Art. 9, ANS, EMA, FDA 21 CFR Part 11, ANVISA). Padrão dominante: deployments híbridos com VPC + ON-PREM em hospitais grandes; farma usa ON-PREM em pesquisa proprietária e nuvem privada em operações.

## 1. Mayo Clinic (EUA) — caso ON-PREM em hospital

**Setor**: hospital de pesquisa. **Sede**: Rochester/MN.

### Status e escala
- ✅ **Produção** + plataforma multi-projeto.
- ✅ **>200 projetos AI** em curso, com **>US$ 1 bi** de investimento previsto.
- ✅ **NVIDIA DGX SuperPOD com B200** instalado para foundation models de pathomics, drug discovery e precision medicine.
- ✅ **Mayo Clinic Platform_Connect**: rede global com **26 PB** de dados clínicos, 3 bi de exames, 1,6 bi de notas, 6 bi de imagens.
- ✅ **Atlas pathology foundation model** (com Aignostics): 1,2M+ slides histopatológicos.

### Stack
- ✅ **ON-PREM puro** para foundation models internos (DGX SuperPOD).
- ⚠️ **Google Cloud** para enterprise search (parceria oficial).
- ⚠️ Microsoft GenAI tools para áreas administrativas.

### Casos mapeados
- **Caso 3** (RAG corporativo / enterprise search), **Caso 7** (extração estruturada de prontuário), **Caso 13** (pareceres regulatórios/clínicos), foundation models para imagem médica.

### Drivers para ON-PREM
- HIPAA + dados de prontuário multi-modal (imagem, texto, exames).
- IP em foundation models proprietários (Atlas).
- Colaboração federada com outros hospitais via Platform_Connect — exige soberania local.

### Fontes
- ✅ <https://newsnetwork.mayoclinic.org/discussion/mayo-clinic-launches-mayo-clinic-platform_insights-to-advance-digital-innovation-and-quality-improvement-across-healthcare/>
- ✅ <https://www.aha.org/aha-center-health-innovation-market-scan/2025-08-12-mayo-clinic-new-ai-computing-platform-will-advance-precision-medicine>
- ✅ <https://newsnetwork.mayoclinic.org/discussion/mayo-clinic-to-deploy-and-test-microsoft-generative-ai-tools/>
- ⚠️ <https://www.fiercehealthcare.com/ai-and-machine-learning/mayo-clinic-google-cloud-partner-generative-ai-power-enterprise-search>

## 2. Cleveland Clinic (EUA)

**Setor**: hospital. **Sede**: Cleveland/OH.

### Status e escala
- ⚠️ **Produção em larga escala**: ambient documentation (Ambience Healthcare) para **4.000+ clinicians**, com redução de **14 min/dia** em tempo de notas EHR.
- ⚠️ **Sepsis detection** (Bayesian Health) em **13 hospitais**: 10× menos falsos alertas, +46% casos identificados.
- ⚠️ Stack embarcada no **Epic** (workflow nativo).

### Stack
- ⚠️ Ambience Healthcare (ambient scribe) e Bayesian Health são SaaS verticais; integração com Epic (clinical EHR).
- 🟡 Pouco detalhe sobre on-prem vs SaaS — provável SaaS com BAA HIPAA.

### Fontes
- ⚠️ <https://www.getprosper.ai/blog/top-5-hospitals-that-use-ai-in-2025-for-better-care>
- ⚠️ <https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/>

## 3. Bayer (Alemanha)

**Setor**: farma + crop science. **Sede**: DE.

### Status e escala
- ✅ Primeira beta-user externa do **LOWE** (Recursion) para drug discovery, anunciado jun/2024.
- ⚠️ Uso de **Aleph Alpha** (LLM alemão soberano) para casos com IP sensível.

### Stack
- ✅ **HÍBRIDO**: LOWE (Recursion) em parceria + Aleph Alpha em deployments locais com IP regulado europeu.
- Aleph Alpha permite operar em **infraestrutura soberana europeia** (atende GDPR + soberania de dados industrial).

### Casos mapeados
- **Caso 7** (extração), **Caso 13** (pareceres regulatórios farma).

### Fontes
- ✅ Press release Recursion x Bayer (jun/2024) — citação em fontes secundárias.
- ⚠️ Aleph Alpha + Bosch + Bayer: covered em Hannover Messe materials.

## 4. Pfizer

**Setor**: farma. **Sede**: EUA.

### Status e escala
- ✅ **Charlie** AI platform lançada em fev/2024 — aplicação ampla (R&D + comercial).
- ✅ Parceria out/2024 com **Ignition AI Accelerator + NVIDIA + Tribe + Digital Industry Singapore** para drug discovery + manufacturing + commercialização.

### Casos mapeados
- **Caso 1** (chat interno), **Caso 6** (sumarização clínica), **Caso 7** (extração).

### Fontes
- ✅ <https://markets.financialcontent.com/stocks/article/tokenring-2025-10-4-pfizers-ai-revolution-a-new-era-for-drug-discovery-and-pharmaceutical-innovation>
- ⚠️ <https://www.klover.ai/pfizer-ai-strategy-analysis-of-dominance-in-pharma/>

## 5. Roche / Genentech

**Setor**: farma. **Sede**: CH/EUA.

### Status
- ⚠️ "**Lab in a Loop**" — GenAI integrada ao loop de drug discovery + development.
- 🟡 Pouco detalhe técnico público sobre stack/topologia.

### Casos mapeados
- **Caso 7**, **Caso 13**.

### Fontes
- ⚠️ <https://pmc.ncbi.nlm.nih.gov/articles/PMC12298131/>

## 6. Novartis

**Setor**: farma. **Sede**: CH.

### Status
- ⚠️ **Novartis AI Innovation Lab** + parceria **Microsoft** para frameworks ML em discovery/development.
- ⚠️ Uso de IA em clinical trial feasibility e site selection.
- 🟡 Topologia provavelmente VPC Azure + IP em on-prem para casos críticos (não detalhado).

## 7. NHS (Reino Unido)

**Setor**: saúde pública. **Sede**: UK.

### Status
- 🟡 **Vários pilotos**: ambient scribe, radiology AI, genomics AI.
- ✅ **NHS Federated Data Platform** (Palantir Foundry) é a base de dados — não LLM diretamente.
- ⚠️ Posicionamento conservador devido a sensibilidade política e regulação UK GDPR.

### Casos mapeados
- **Caso 6**, **Caso 7**.

## 8. HCor / Albert Einstein / Sírio-Libanês (Brasil)

**Setor**: hospitais privados de referência. **Sede**: BR.

### Status
- ⚠️ Discussões públicas em conferências (Hospitalar 2024, Futurecom 2024) — adoção crescente.
- ✅ **Albert Einstein**: R$ 900 mi em tecnologia (incluindo IA) nos últimos 6 anos.
- ⚠️ Uso de GenAI em SOC (Sírio-Libanês), telemedicina (Einstein).
- 🟡 Detalhamento técnico de deploy LLM on-prem **não disponível em fontes primárias verificáveis** — predomina discurso institucional.

### Fontes
- ⚠️ <https://eval.digital/en/blog/artificial-intelligence/hospital-fair-2024-artificial-intelligence-is-an-irreversible-trend-says-einsteins-head-of-innovation/>
- ⚠️ <https://hospitalsiriolibanes.org.br/blog/inovacao/sirio-libanes-no-futurecom-2024>

## 9. Outros casos (referência rápida)

- **Recursion** (não cliente, vendor) — plataforma LOWE distribuída como API + colaboração; relevante para entender arquitetura federada em farma.
- **Insilico Medicine, Atomwise, Exscientia** — startups de drug discovery com modelos proprietários on-prem.
- **Tempus Labs, Flatiron Health** — oncologia + LLMs sobre prontuário (HIPAA) — uso intenso de modelos proprietários.

## Síntese do setor

| Empresa | Topologia dominante | Padrão |
|--------|---------------------|--------|
| Mayo Clinic | ON-PREM (DGX) + Google Cloud | Foundation models proprietários em imagem |
| Cleveland Clinic | SaaS HIPAA + Epic | Ambient scribe + sepsis triage |
| Bayer | Híbrido + Aleph Alpha (DE) | Soberania europeia para IP |
| Pfizer | VPC Azure + parcerias NVIDIA | Plataforma "Charlie" multi-uso |
| Roche/Genentech | Híbrido | "Lab in a Loop" |
| Novartis | VPC Azure + MS | AI Innovation Lab |
| NHS | Pilotos federados | FDP (Palantir) |
| Einstein/Sírio | Em construção | Forte invest tech, deploy LLM on-prem 🟡 |

**Padrões**:
- **Hospital de pesquisa de elite (Mayo)** = ON-PREM com DGX próprio para imagem + foundation models.
- **Hospital operacional (Cleveland)** = SaaS HIPAA com integração Epic.
- **Farma global** = híbrido com camada **soberana europeia (Aleph Alpha)** quando IP exige.
- **Saúde pública (NHS, Singapura)** = pilotos federados + restrição forte.

**Drivers para LOCAL** mais citados: HIPAA / LGPD Art. 11 / GDPR Art. 9 (dados de saúde como categoria especial), IP em discovery, prontuário multi-modal, soberania nacional.
