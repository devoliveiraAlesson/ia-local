# Sumário Executivo — Proposta de IA Local On-Premises

> Etapa 5/5. Documento boardroom. 1–2 páginas. Para CFO/CIO/CEO. Maio/2026.

## A pergunta de negócio

Em 2026, ferramentas como ChatGPT/Claude/Gemini já são usadas informalmente por colaboradores em quase todas as empresas. Para uma organização que **lida com dados sensíveis** (PII, prontuários, código proprietário, contratos, segredos industriais, dados regulados por LGPD/HIPAA/PCI), a pergunta deixou de ser "se" e passou a ser **"como capturar o ganho de produtividade da IA generativa sem expor dado regulado a APIs públicas?"**.

A resposta proposta neste documento é **uma plataforma corporativa de IA local (on-premises ou nuvem privada)**, multi-modelo, governada, com casos de uso priorizados em 12 meses.

## Recomendação executiva

**Aprovar a Fase 0 + Fase 1** (mês 0–5), com escopo:

1. Plataforma comum (vLLM + Qdrant + LiteLLM + Open WebUI/LibreChat + Llama Guard 3 + Langfuse).
2. Caso 1 — **Chat interno seguro** como quick win.
3. Caso 3 — **RAG corporativo** como plataforma habilitadora para 4–8 outros casos.

Aprovar **decisão go/no-go** ao final da Fase 1 (mês 5) para Fases 2–4 (coding, atendimento, sumarização, fine-tune).

## Por que agora — 5 evidências

| # | Evidência | Implicação |
|---|-----------|-----------|
| 1 | **JPMorgan LLM Suite**: 200k+ usuários, 3–6h/semana economizadas/usuário, US$ 1–2 bi/ano em valor declarado. | Banco T1 já provou ROI em escala — o playbook existe. |
| 2 | **Morgan Stanley AI @ MS**: 98% de adoção entre advisors. | IA bem desenhada não tem teto de adoção em conhecimento intensivo. |
| 3 | **BBVA**: 3h/semana economizadas, 1.000+ data scientists, ~20k GPTs custom. | Mesmo via API pública, ROI é quantificável; on-prem mantém o ROI sem o risco. |
| 4 | **Stripe**: −73% de custo ao migrar para vLLM. | Stack open de produção já é mais barata que LLM-as-a-service em volume. |
| 5 | **Bradesco/IBM**: ~R$ 400 milhões investidos. | Players regulados BR estão capitalizando agora — há janela competitiva. |

## Faixa de retorno (3 cenários — premissas explícitas em `01-modelo-roi-cenarios.md`)

| Cenário | Usuários ativos | CAPEX HW + 30% (rede/SW/impl.) | OPEX ano | Benefício anual estimado | Payback estimado |
|---------|-----------------|--------------------------------|----------|--------------------------|------------------|
| **P (Pequeno)** | 500 | US$ 0,32–0,59 M | US$ 0,4–0,7 M | US$ 0,9–1,5 M | **10–15 meses** |
| **M (Médio)** | 5.000 | US$ 1,95–3,64 M | US$ 1,8–3,2 M | US$ 8–14 M | **8–14 meses** |
| **G (Grande)** | 50.000 | US$ 10,4–24,3 M | US$ 7–14 M | US$ 80–180 M | **6–12 meses** |

> Premissas: 3h/semana economizadas (âncora BBVA/JPMorgan), salário médio totalmente carregado US$ 60k (BR R$ 12k/mês), 60% adoção, 30% utilização efetiva GPU. Sensibilidade detalhada em §01.

**Vantagem on-prem vs API pública**: a partir de ~30–40% de utilização efetiva, custo por 1M tokens cai de US$ 3–5 (GPT-4o/Claude API) para **US$ 0,15–0,30** (Llama 70B AWQ + H100), uma diferença de **5–25×** que comporta o CAPEX em 6–14 meses no Cenário M e G.

## O que muda para a empresa

- **Risco de vazamento estrutural eliminado**: nenhum prompt, embedding ou log sai do perímetro.
- **Soberania regulatória**: LGPD Art. 11 (saúde), Art. 7º X (dados sensíveis), GDPR Art. 28 sub-processadores, ISO/IEC 42001 endereçáveis com auditoria interna.
- **Liberdade de modelo**: multi-modelo desde o dia 1 (Llama 3.3 / Granite 4 / Qwen 3 / DeepSeek) — sem lock-in OpenAI/Anthropic.
- **Custo previsível**: CAPEX amortizado em 3–5 anos; OPEX dominado por energia + suporte; sem surpresa de "fatura de tokens".

## Riscos críticos (detalhe em `05-riscos-mitigacao.md`)

1. **Lead time de GPU** (12–32 semanas H200/B200) — mitigação: pré-cotação imediata + cloud-bridge nos primeiros 60 dias.
2. **Equipe insuficiente** — mitigação: contrato Red Hat / NVIDIA Professional Services / parceiro local + plano de internalização.
3. **Subdimensionamento de utilização** — mitigação: multi-tenant via gateway + semantic cache desde o dia 1; piso de 30% de utilização para justificar on-prem.
4. **Adoção baixa** — mitigação: vertical (não chat genérico isolado); GenAI Championship Bosch-style; campeões por área.
5. **Compliance/auditoria** — mitigação: OTel GenAI + Langfuse self-host + WORM logs + ISO 42001 (Granite 4) como roadmap.

## Decisão pedida ao board

| # | Decisão | Recomendação | Investimento aprovado nessa decisão |
|---|---------|--------------|--------------------------------------|
| 1 | Aprovar Fase 0 + Fase 1 (5 meses) | **Sim** | US$ 0,8–1,2 M (Cenário M base) |
| 2 | Aprovar pré-cotação de GPU com lead time ≥ 16 semanas | **Sim** | sem desembolso até PO |
| 3 | Nomear Sponsor Executivo + Tech Lead/Arquiteto LLM | **Sim** | sem CAPEX |
| 4 | Marcar gate de mid-life para mês 5 (Go/No-Go Fases 2–4) | **Sim** | sem desembolso até gate |

**Decisão Fases 2–4 fica para gate do mês 5** — após dados reais de adoção, custo, latência e satisfação do Caso 1 + RAG.

## 5 mensagens finais para o board

1. **A janela competitiva está aberta hoje** — bancos T1 e estatais BR já capitalizaram; quem não embarca em 12 meses fica em desvantagem em produtividade e compliance.
2. **A âncora não é "IA". A âncora é "3h/semana × custo-hora × 60% de adoção"** — números defensáveis vindos de JPMorgan/BBVA/Walmart.
3. **On-prem só ganha de API a partir de utilização efetiva ≥30–40%** — por isso o desenho começa com 2 casos sólidos (chat + RAG), não com um portfólio inflado.
4. **O risco real não é tecnológico, é de adoção e governança** — vertical, campeões, observabilidade desde o dia 1.
5. **A decisão é faseada** — board aprova Fase 0+1 hoje; revisa dados reais no mês 5; segue ou recalibra.

## Próximos documentos desta etapa

- `01-modelo-roi-cenarios.md` — premissas, sensibilidade, NPV/TIR.
- `02-comparativo-alternativas.md` — Local vs API pública vs Copilot vs Híbrido.
- `03-roadmap-12-meses.md` — Fases 0–4 com entregáveis e métricas.
- `04-equipe-e-orcamento.md` — headcount BR/US.
- `05-riscos-mitigacao.md` — 14 riscos.
- `06-narrativa-boardroom.md` — 12 slides.
- `07-perguntas-frequentes.md` — FAQ antecipado.
- `08-decisao-go-no-go.md` — checklist consolidado.
- `09-anexo-fontes.md` — bibliografia.
