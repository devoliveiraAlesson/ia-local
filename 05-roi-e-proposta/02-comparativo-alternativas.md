# Comparativo de Alternativas — IA Local vs API Pública vs Copilot vs Híbrido

> Etapa 5/5. Documento técnico-financeiro. Para CIO, CTO, CISO, controladoria. Maio/2026.

## 1. Alternativas avaliadas

| ID | Alternativa | Descrição | Casos típicos |
|----|-------------|-----------|----------------|
| **A. Local on-prem** | LLM open + vLLM/SGLang em data center próprio | Soberania máxima | Banco T1 air-gap, gov, indústria com IP, saúde regulada |
| **B. VPC dedicada single-tenant** | Azure OpenAI dedicado / AWS Bedrock dedicado / OCI Dedicated | Soberania contratual | Bancos US, Petrobras, Siemens |
| **C. API pública multi-tenant** | OpenAI / Anthropic / Google direto (multi-tenant) | Time-to-market | POCs, casos não sensíveis |
| **D. Copilot Enterprise (M365)** | Microsoft 365 Copilot por seat | Produtividade office sem operar nada | Empresas Microsoft-shop |
| **E. GitHub Copilot Enterprise** | Coding assistant gerenciado por seat | Engenharia média/grande | Devs em organização Microsoft/GitHub |
| **F. Híbrido (recomendado)** | Combinação: A para sensível + C para não sensível + D/E onde fizer sentido | Maximiza ROI por caso | A maior parte das empresas reguladas reais (Etapa 3) |

---

## 2. Comparativo dimensional (15 critérios)

| # | Critério | A. Local | B. VPC | C. API | D. M365 Copilot | E. GH Copilot Ent | F. Híbrido |
|---|----------|----------|--------|--------|------------------|---------------------|-------------|
| 1 | Soberania de dados (prompt sai do perímetro?) | **Não sai** | Permanece em VPC contratada | Sai | Sai (com BAA M365) | Sai (com policy) | Sensível: não sai |
| 2 | LGPD Art. 7º X / Art. 11 (dados sensíveis) | ✅ Pleno | ✅ com DPA | ⚠️ DPA + BAA | ⚠️ DPA + BAA | ⚠️ DPA + BAA | ✅ por caso |
| 3 | EU AI Act high-risk (justificável ao auditor) | ✅ pleno controle | ✅ com docs | ⚠️ depende vendor | ⚠️ | ⚠️ | ✅ |
| 4 | Air-gap / ITAR / EAR | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ (parte) |
| 5 | Custo/1M tokens (utilização >40%) | **US$ 0,15–0,30** | US$ 1,0–3,0 | US$ 3–5 (GPT-4o); 0,6–2,5 (Sonnet/Haiku) | n/a (per seat) | n/a (per seat) | misto |
| 6 | Custo previsibilidade | CAPEX + OPEX previsíveis | OPEX previsível com reservas | Variável (token) | Per seat fixo | Per seat fixo | Misto |
| 7 | Time-to-market 1º caso | 4–6 meses | 2–4 meses | **dias** | **dias** | **dias** | 4–6 meses (sensível) + dias (resto) |
| 8 | Lock-in vendor | Baixo (multi-modelo open) | Alto (Azure/AWS) | Alto (modelo único) | Alto (Microsoft) | Alto (GitHub) | Médio |
| 9 | CAPEX inicial | Alto (US$ 0,3–24 M) | Baixo | **Zero** | **Zero** | **Zero** | Médio |
| 10 | OPEX anual ano 1 | Médio (energia + equipe) | Médio (compute reservado) | Variável (token) | US$ 30/seat/mês | US$ 19–39/seat/mês | Misto |
| 11 | Customização/fine-tune | Pleno (LoRA, InstructLab) | Limitado (RAG; alguns FT) | Limitado (FT API) | Não | Não | Pleno onde aplicável |
| 12 | Multi-modelo | Sim (3–7 LLMs) | Limitado (catálogo Azure/AWS) | Não (modelo único do provider) | Não (GPT-4o under hood) | Não (GPT-4o/Codex under hood) | Sim |
| 13 | Equipe necessária | 8–40 FTE (porte M–G) | 4–10 FTE | 1–3 FTE | 0,5 FTE (admin) | 0,5 FTE (admin) | 6–25 FTE |
| 14 | Performance state-of-art | Llama 70B / Granite 4 / Qwen 3 | GPT-4o / Claude / Gemini | GPT-4o / Claude / Gemini | GPT-4o | GPT-4o + Codex | melhor de cada |
| 15 | Risco técnico operacional | Alto (operar é com a empresa) | Médio | Baixo | **Mínimo** | **Mínimo** | Médio |

---

## 3. Análise por caso de uso (escolha por caso)

| Caso (Etapa 1) | Sensibilidade do dado | Recomendação 1ª escolha | 2ª escolha |
|----------------|------------------------|--------------------------|-------------|
| 1. Chat interno seguro | Alta (e-mails, brainstorm) | **A. Local** | B. VPC |
| 2. Atendimento ao cliente | Alta (PII cliente) | **A. Local** | B. VPC |
| 3. RAG corporativo | Alta (corpus inteiro) | **A. Local** | B. VPC |
| 4. Coding assistant | Alta (código proprietário) | **A. Local** (Tabby/Continue + Qwen-Coder) | E. GH Copilot Ent (se IP tolerável) |
| 5. Code review | Alta | **A. Local** | E. GH Copilot Ent |
| 6. Sumarização docs longos | Alta (jurídico, contratos) | **A. Local** | B. VPC |
| 7. Extração estruturada | Alta (faturas, prontuários) | **A. Local** | B. VPC |
| 8. Tradução interna | Média | A. Local ou C. API | D. M365 |
| 9. Geração docs técnicos | Média | A. Local | C. API |
| 10. Análise de logs | Alta (logs com PII) | **A. Local** | B. VPC |
| 11. Compliance/PII classification | **Crítica** | **A. Local** | A. Local (não há 2ª escolha) |
| 12. Treinamento/onboarding | Baixa | C. API ou D. M365 | A. Local |
| 13. Pareceres regulatórios | **Crítica** | **A. Local** | A. Local |
| 14. Triagem e-mails | Alta | **A. Local** | B. VPC |

> **Padrão observado**: 11 dos 14 casos têm **A. Local** como primeira escolha em empresa com dados sensíveis. Casos 8/9/12 admitem API/Copilot. Isto motiva a recomendação **F. Híbrido com A dominante**.

---

## 4. Comparação financeira a 5 anos (Cenário M — 5.000 usuários, ~62 B tokens/ano)

| Alternativa | CAPEX 5a | OPEX 5a | TCO 5a | Notas |
|-------------|----------|---------|--------|-------|
| **A. Local on-prem** | US$ 2,8 M (refresh ano 4 incluso) | US$ 10 M | **~US$ 13 M** | Inclui equipe, energia, suporte, fine-tune |
| **B. VPC dedicada Azure OpenAI** | mínimo | US$ 70–110 M (PTU dedicado + storage) | **~US$ 90 M** | Sem CAPEX; lock-in Azure |
| **C. API pública GPT-4o (full volume)** | 0 | US$ 1,2 bi (nominal) | **inviável** | Não considerado |
| **C. API pública Claude/Mistral blended** | 0 | US$ 100–150 M | ~US$ 125 M | Concentração em 1 vendor |
| **D. M365 Copilot (5k seats × US$30/m × 60mês)** | 0 | US$ 9 M | ~US$ 9 M | Cobre apenas casos office; não cobre RAG corporativo nem atendimento |
| **E. GH Copilot Ent (500 devs × US$39/m × 60mês)** | 0 | US$ 1,2 M | ~US$ 1,2 M | Cobre só coding |
| **F. Híbrido (A para sensíveis + D + E onde aplicável)** | US$ 2,8 M | US$ 18 M | **~US$ 21 M** | Cobre tudo + UX office mantida |

> **Comparação direta para o mesmo escopo (todos 14 casos)**: somente **A** ou **F** atendem. **D + E** são complementares, não substitutos. **B** custa ~7× mais que **A** em escala M e mantém lock-in de vendor.

---

## 5. Quando cada alternativa faz sentido (heurística decisória)

### A. Local on-prem é a primeira escolha quando:
- Volume > 10 M tokens/dia (Etapa 1 §00) **OU**
- Compliance air-gap exigida (defesa, ITAR/EAR, hospital crítico) **OU**
- Cenário M ou G com utilização projetada >30% **OU**
- IP do dado é diferenciador competitivo (segredo industrial, modelo financeiro proprietário, código)

### B. VPC dedicada faz sentido quando:
- Empresa já tem Azure / AWS enterprise agreement bem maduro
- Time interno < 4 FTE e sem CAPEX disponível
- Saúde / financeiro com BAA + DPA aceitos pelo regulador
- Caso "ponte" enquanto on-prem é construído

### C. API pública multi-tenant:
- POCs, ideação, casos com **dado público apenas**
- Volume baixo (< 1 M tokens/dia)
- Tradução interna sem terminologia sensível
- Treinamento/onboarding baseado em política pública

### D. M365 Copilot:
- Empresa Microsoft-shop com licenças E3/E5 dominantes
- Quer ganho em Word/Excel/Teams sem operar IA
- **Complemento**, não substituto da plataforma corporativa

### E. GitHub Copilot Enterprise:
- < 200 devs, sem time de plataforma para operar Tabby/Continue
- IP do código tolera política Microsoft (revisar contrato)
- **Complemento** a A para alguns squads enquanto coding-on-prem amadurece

### F. Híbrido:
- A maior parte das empresas reais (Etapa 3): JPMorgan, Itaú, Bradesco, Bosch, BMW operam híbrido por design.
- Caminho recomendado para **Cenário M e G** desta proposta.

---

## 6. Risco regulatório (LGPD/EU AI Act/HIPAA) por alternativa

| Cenário regulatório | A. Local | B. VPC | C. API | D. M365 | E. GH | F. Híbrido |
|---------------------|----------|--------|--------|---------|-------|-------------|
| LGPD Art. 11 (saúde, biometria) | ✅ Pleno | ⚠️ DPA + DPIA | ❌ Risco alto | ❌ | ❌ | ✅ (parte A) |
| LGPD Art. 7º X (interesse legítimo) | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| GDPR Art. 28 sub-processadores | ✅ | ⚠️ verificar lista | ⚠️ verificar lista | ⚠️ | ⚠️ | ✅ |
| HIPAA (saúde EUA) | ✅ | ✅ com BAA | ⚠️ (precisa BAA) | ✅ com BAA | ⚠️ | ✅ |
| EU AI Act high-risk system | ✅ docs internas | ⚠️ depende vendor | ⚠️ depende vendor | ⚠️ | ⚠️ | ✅ |
| ISO/IEC 42001 (sistema gestão IA) | ✅ pleno (Granite 4 traz) | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| Soberania nacional (gov BR) | ✅ DC nacional | ⚠️ DC região | ❌ | ❌ | ❌ | ✅ |

> **Mensagem regulatória**: para casos críticos LGPD Art. 11 e ISO 42001, **A é a única** que dá controle total documentado. **F** preserva A onde importa.

---

## 7. Casos reais por alternativa (Etapa 3 §00 cross-ref)

| Alternativa | Empresas que adotam (Etapa 3) |
|-------------|--------------------------------|
| **A. Local on-prem** | Bloomberg (BloombergGPT), Mayo Clinic (DGX SuperPOD B200), Bayer (Aleph Alpha em DC alemão), Singapura Pair (DC governamental), partes do JPMorgan LLM Suite |
| **B. VPC dedicada** | JPMorgan, Morgan Stanley, Goldman, Petrobras (ChatPetrobras), Siemens (Industrial Copilot) — todos sobre Azure OpenAI |
| **C. API pública** | BBVA (ChatGPT Enterprise + Gemini Workspace) — caso transparente |
| **D. M365 Copilot** | (não detalhado caso público) — uso comum em base instalada Microsoft |
| **E. GH Copilot Ent** | (uso comum em devs) — Walmart e outros relatam mix com Copilot/Cody/internal |
| **F. Híbrido** | Itaú (Anthropic + Llama + custom), Bradesco (Bridge sobre IBM watsonx + LLMs externos), Bosch (open + Aleph + GPT), BMW (AWS + Alexa LLM) |

> Padrão dominante em empresas reguladas reais: **F. Híbrido** com **A** dominando casos sensíveis e **B/C** complementando casos abertos.

---

## 8. Recomendação final

**Adotar F. Híbrido com A. Local on-prem como espinha dorsal**:
1. **A. Local on-prem** para os 11 casos sensíveis (chat interno, RAG, atendimento, coding, sumarização, extração, compliance, pareceres, code review, logs, e-mails).
2. **C. API pública** mantida apenas para casos comprovadamente não sensíveis (tradução pública, geração de docs públicos, treinamento institucional).
3. **D. M365 Copilot** por seat para usuários cuja produtividade dependa de Word/Excel/Teams — preserva UX já adotada.
4. **E. GitHub Copilot Enterprise** somente onde o coding-on-prem ainda não tenha cobertura (squads em rampa) — substituir progressivamente por Tabby/Continue + Qwen-Coder à medida que o caso 4 amadurece.

Esta combinação **maximiza ROI por caso, minimiza risco regulatório e evita lock-in**, espelhando o padrão observado em JPMorgan, Itaú, Bradesco, Bosch, BMW (Etapa 3 §08).

---

## 9. Fontes

- Etapa 1 §00 (mapeamento dos 14 casos)
- Etapa 2 §11 (licenças, lock-in)
- Etapa 3 §00 e §08 (padrões reais de combinação)
- Etapa 4 §02 (custo/1M tokens; CAPEX)
- Microsoft 365 Copilot pricing (US$ 30/seat/mês) — referência maio/2026
- GitHub Copilot Enterprise (US$ 39/seat/mês) — referência maio/2026
- OpenAI / Anthropic / Google preços API maio/2026
