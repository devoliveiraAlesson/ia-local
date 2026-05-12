# Perguntas Frequentes — FAQ Antecipado

> Etapa 5/5. Documento de apoio à apresentação executiva. Para Q&A em board, comitê de risco, due diligence interna. Maio/2026.
>
> Cada pergunta tem **resposta executiva (1 frase)** + **detalhe (3–5 linhas)** + **referência cruzada** ao documento da proposta.

---

## A. Estratégia e justificativa

### A1. Por que não esperar mais 1–2 anos para a tecnologia amadurecer?

**Resposta executiva**: porque a tecnologia **já amadureceu** — o que está amadurecendo é o playbook corporativo, e a janela competitiva está se fechando.

**Detalhe**: vLLM, Llama 3.3, Granite 4, Qwen 3 estão em produção em 34 empresas mapeadas (Etapa 3 §00). JPMorgan declarou US$ 1–2 bi/ano em 2024–2025. BBVA tem 87k usuários em Gemini Workspace. Bradesco/IBM investiu R$ 400 M. Esperar 1–2 anos significa perder a janela de captura de produtividade enquanto concorrentes capitalizam.

**Ref**: Etapa 3 §00 (tabela mestre); Slide 2 da narrativa.

---

### A2. Por que não fazer 100% API pública (OpenAI Enterprise, Claude Enterprise)?

**Resposta executiva**: porque 11 dos 14 casos mapeados envolvem dado sensível que não pode sair do perímetro.

**Detalhe**: API pública (mesmo com DPA/BAA) implica sub-processadores não controlados, concentração em 1 vendor, custo variável que escala mal (US$ 248 M/ano para o volume do Cenário M com GPT-4o), e dificuldade de defender LGPD Art. 11 e EU AI Act ao auditor. Em volume corporativo, vLLM em on-prem custa 5–25× menos que API pública (Stripe declarou −73%).

**Ref**: `02-comparativo-alternativas.md`; Slide 6 e 10 da narrativa.

---

### A3. Por que não fazer 100% on-prem?

**Resposta executiva**: porque casos não sensíveis (tradução pública, geração de docs públicos, treinamento institucional) custam menos via API e ganham time-to-market.

**Detalhe**: a recomendação é **híbrido com on-prem dominando casos sensíveis**. Padrão observado em JPMorgan, Itaú, Bradesco, Bosch, BMW (Etapa 3 §08): mix on-prem para sensível + Azure/AWS para amplo. Não é "tudo ou nada".

**Ref**: `02-comparativo-alternativas.md` §8.

---

### A4. Quanto a IA vai economizar mesmo, sem hype?

**Resposta executiva**: 3 h/semana por usuário ativo × 60% adoção × custo-hora — números defensáveis de BBVA/JPMorgan.

**Detalhe**: em Cenário M (5.000 usuários), isso equivale a US$ 13,2 M/ano em tempo economizado de chat geral. Adicionando coding, atendimento e sumarização, faixa conservadora vai de **US$ 8–14 M/ano em benefícios** vs **US$ 2 M/ano de OPEX**. Payback 8–14 meses.

**Ref**: `01-modelo-roi-cenarios.md` §3.

---

### A5. E se a adoção for baixa (40% em vez de 60%)?

**Resposta executiva**: o payback fica em 14–22 meses no Cenário M. Não quebra o caso, atrasa.

**Detalhe**: análise de sensibilidade em `01-modelo-roi-cenarios.md` §5. Adoção é a variável **mais importante** para o ROI. Por isso o desenho exige campeões por área, GenAI Championship Bosch-style, e gate Go/No-Go no mês 5 baseado em adoção real.

**Ref**: `01-modelo-roi-cenarios.md` §5.1; `05-riscos-mitigacao.md` R4.

---

## B. Tecnologia

### B1. Qual modelo vamos usar e por quê?

**Resposta executiva**: multi-modelo desde o dia 1 — Llama 3.3 70B + Granite 4 + Qwen 3 — atrás de um gateway que abstrai a escolha.

**Detalhe**: nenhum modelo único cobre todas as necessidades. Llama 3.3 para chat geral; Granite 4 (Apache 2.0 + ISO 42001) para casos regulados; Qwen 3 (Apache 2.0) para multilíngue e coding; DeepSeek-R1 para raciocínio. Trocar modelo via gateway sem mudar app.

**Ref**: Etapa 2 §02 e §11; `05-riscos-mitigacao.md` R9 (lock-in).

---

### B2. Por que vLLM e não Ollama / TGI / TensorRT-LLM?

**Resposta executiva**: vLLM virou substrato comum (Red Hat, NVIDIA NIM, Anyscale, llm-d) e tem 1,7×–3,2× throughput vs Ollama em produção corporativa.

**Detalhe**: SGLang é alternativa quando há prefix sharing pesado (RAG, multi-turn). Ollama é POC/edge, não produção. TensorRT-LLM trava em NVIDIA. vLLM é open + multi-fornecedor + multi-runtime.

**Ref**: Etapa 2 §00; Etapa 3 §09.

---

### B3. Vamos depender 100% de NVIDIA?

**Resposta executiva**: não. Multi-modelo + multi-fornecedor por desenho. AMD MI300X e Intel Gaudi 3 considerados como segunda fonte.

**Detalhe**: em Cenários M e G, recomendação é incluir **1 nó AMD ou Intel** como segunda fonte para evitar lock-in. vLLM roda em ambos. Custo total de troca em 2–3 anos é razoável.

**Ref**: Etapa 4 §01; `05-riscos-mitigacao.md` R9.

---

### B4. Vamos usar fine-tuning ou RAG?

**Resposta executiva**: RAG nas Fases 1–3; fine-tuning leve (InstructLab + Granite 4) na Fase 4, somente onde houver dataset > 5k exemplos curados.

**Detalhe**: 80% dos casos corporativos são bem servidos por RAG + prompt engineering. Fine-tuning vira diferenciação competitiva quando há terminologia interna (jurídico, médico, industrial) e dataset curado. InstructLab (Red Hat / IBM) é o caminho de menor risco.

**Ref**: Etapa 2 §10; `03-roadmap-12-meses.md` Fase 4.

---

### B5. E se um modelo melhor sair (GPT-5, Claude 5, Gemini 3)?

**Resposta executiva**: o gateway permite trocar modelo em horas, não meses. A arquitetura é projetada para essa volatilidade.

**Detalhe**: a empresa nunca depende de 1 modelo. Modelos abertos seguem o estado da arte com 6–12 meses de defasagem (Llama 3.3 hoje vs GPT-4o de meados de 2024). Para a maioria dos casos corporativos, isso é suficiente.

**Ref**: Slide 3 da narrativa.

---

## C. Risco e compliance

### C1. E se vazar PII?

**Resposta executiva**: o desenho **estrutural** impede vazamento — prompts, embeddings e logs ficam dentro do perímetro. Mas tratamos isto como risco crítico R5.

**Detalhe**: Presidio na ingestão de observabilidade; Langfuse self-host (não cloud); WORM logs; DPIA por caso; mapeamento OWASP LLM 2025 documentado. Custo médio de breach 2025: US$ 4,88 M (IBM Security).

**Ref**: `05-riscos-mitigacao.md` R5; Etapa 4 §06.

---

### C2. Como ficamos com EU AI Act?

**Resposta executiva**: arquitetura on-prem facilita compliance EU AI Act high-risk porque temos **controle pleno e documentado** dos componentes.

**Detalhe**: para sistemas high-risk (atendimento cliente, decisões automatizadas), EU AI Act exige documentação técnica, supervisão humana, registro de eventos, qualidade de dados. On-prem com OTel GenAI + Langfuse self-host + WORM logs entrega isso. Granite 4 já é ISO 42001 certificado, ajuda.

**Ref**: `02-comparativo-alternativas.md` §6; Etapa 4 §06.

---

### C3. Como respondemos ANPD em incidente?

**Resposta executiva**: temos audit trail completo via OTel GenAI + WORM logs com retenção 24+ meses, e um plano de incidente IA documentado.

**Detalhe**: cada request tem trace-id da borda à GPU; user/session/model/timestamp gravados. Plano de incidente cobre vazamento, jailbreak, poisoning. Comunicação ANPD em prazo de 2 dias úteis (LGPD).

**Ref**: `05-riscos-mitigacao.md` R5, R10, R13; Etapa 4 §07.

---

### C4. Se o modelo "alucinar" e gerar parecer errado em jurídico/médico, quem responde?

**Resposta executiva**: a empresa, como sempre. Por isso casos cliente-facing têm humano-na-curva nos primeiros 60–90 dias e citações obrigatórias com link à fonte.

**Detalhe**: em pareceres regulados, a IA gera draft, humano valida. Disclaimers obrigatórios. Groundedness check (Ragas faithfulness) automatizado. Eval contínua. Não é diferente do BPO atual — só mais barato e mais rápido.

**Ref**: `05-riscos-mitigacao.md` R7; Etapa 3 §09.

---

### C5. E quanto a licença de modelo (Llama 700M MAU, Codestral MNPL)?

**Resposta executiva**: jurídico já mapeou (Etapa 2 §11). Para coding usamos Qwen-Coder/Granite-Code (não Codestral). Para grupos > 100M MAU, usamos Granite/Qwen (Apache 2.0) em vez de Llama em fluxos cliente-facing.

**Detalhe**: tabela master de licenças em Etapa 2 §11. Auditoria de licenças trimestral. SBOM de modelos por release.

**Ref**: Etapa 2 §11; `05-riscos-mitigacao.md` R15.

---

## D. Custo e ROI

### D1. CAPEX está realista?

**Resposta executiva**: faixa baseada em hardware estimativa pública (Etapa 4 §02): P US$ 250–450k / M US$ 1,5–2,8M / G US$ 8–18M, mais 25–35% para rede/storage/SW/implantação.

**Detalhe**: 3 OEMs cotados em paralelo (Dell, Supermicro, Lenovo, HPE). Cotação obrigatória antes do PO (`08-decisao-go-no-go.md`). Para referência: Bradesco/IBM declarou R$ 400 M total em horizonte plurianual — coerente com Cenário G+.

**Ref**: Etapa 4 §02; `01-modelo-roi-cenarios.md` §2–4.

---

### D2. OPEX está realista?

**Resposta executiva**: ~US$ 0,55 M/ano (P), 2 M/ano (M), 9 M/ano (G), incluindo energia, suporte, equipe, manutenção.

**Detalhe**: equipe é 60–70% do OPEX. Hardware support + software (RHEL AI, NVIDIA AI Enterprise opcional) + energia somam 25%. Manutenção/fine-tune/red team 10–15%.

**Ref**: `01-modelo-roi-cenarios.md` §2.3, §3.3, §4.3.

---

### D3. Quando exatamente recuperamos o investimento?

**Resposta executiva**: Cenário M base — payback **8–14 meses** assumindo 60% adoção e 3h/semana economizadas. Pessimista (40% adoção, 2h/sem): 22–30 meses.

**Detalhe**: análise de sensibilidade em §5 do `01-modelo-roi-cenarios.md`. NPV 5 anos no Cenário M base é US$ 23–47 M positivo. TIR 130–280%.

**Ref**: `01-modelo-roi-cenarios.md` §3.6 e §5.

---

### D4. E se o hardware ficar obsoleto em 3 anos?

**Resposta executiva**: depreciação contábil planejada em 4–5 anos. CAPEX de refresh está orçado no TCO 5 anos. ROI sobrevive ao refresh.

**Detalhe**: H100/H200 de hoje são economicamente viáveis até 2028–2029 para a maioria dos casos corporativos. Refresh para Blackwell/Rubin em ano 4 é planejado. NPV 5 anos contempla isto.

**Ref**: `01-modelo-roi-cenarios.md` §1.3 e §7.

---

### D5. Por que CAPEX em vez de OPEX puro (cloud)?

**Resposta executiva**: porque em volume > 10 M tokens/dia e utilização > 30%, on-prem custa 5–25× menos que API e dá soberania regulatória. Em volume baixo, fazemos cloud-bridge VPC.

**Detalhe**: Stripe, JPMorgan, BBVA, Walmart, Bradesco operam on-prem (parte ou todo) por essa lógica. ROI medido em casos públicos.

**Ref**: `02-comparativo-alternativas.md` §4.

---

## E. Implantação e equipe

### E1. Quanto tempo até primeiro caso em produção?

**Resposta executiva**: 5 meses (mês 5) — Caso 1 (Chat) + Caso 3 (RAG corporativo) em produção; gate Go/No-Go neste marco.

**Detalhe**: Fase 0 (mês 0–2) prontidão; Fase 1 (mês 2–5) plataforma + chat + RAG. Lead time de GPU > 16 sem mitigado por cloud-bridge VPC.

**Ref**: `03-roadmap-12-meses.md` Fases 0–1.

---

### E2. Quem opera isso depois? Não temos esse time hoje.

**Resposta executiva**: equipe de 4 a 40 FTE conforme porte; primeiros 6 meses com consultoria pesada (Red Hat / NVIDIA / IBM) e plano de internalização explícito.

**Detalhe**: Tech Lead/Arquiteto LLM contratado antes do mês 1 é decisão crítica. Cada FTE consultor tem shadow interno. Treinamento estruturado por trilha (Tech Lead, ML Eng, SRE, Segurança, PO).

**Ref**: `04-equipe-e-orcamento.md`.

---

### E3. E se o Tech Lead sair?

**Resposta executiva**: documentação obrigatória, pair work, comitê de IA com 3+ stakeholders C-level. Risco mitigado mas real.

**Detalhe**: R2 em `05-riscos-mitigacao.md`. Plano de sucessão considerado desde o dia 1. Consultoria emergencial pré-contratada como gap-filler.

**Ref**: `05-riscos-mitigacao.md` R2 e R16.

---

### E4. E se o sponsor executivo sair?

**Resposta executiva**: comitê com 3+ C-levels (CIO + CFO + COO + CISO), não 1 só. ROI documentado mês a mês. Vinculação a OKR de longo prazo.

**Detalhe**: R16 em `05-riscos-mitigacao.md`.

**Ref**: `05-riscos-mitigacao.md` R16.

---

### E5. Como mediremos sucesso?

**Resposta executiva**: 9 métricas por gate (mês 5 e mês 12) — adoção, horas economizadas, utilização GPU, custo/1M tokens, latência, cache hit, NPS, tickets desviados, cycle time.

**Detalhe**: tabela completa em `01-modelo-roi-cenarios.md` §8.

**Ref**: `01-modelo-roi-cenarios.md` §8.

---

## F. Comparações

### F1. Por que não comprar Microsoft 365 Copilot e GitHub Copilot Enterprise para todos?

**Resposta executiva**: porque cobrem apenas casos office e coding — **não cobrem** RAG corporativo, atendimento, compliance, pareceres, classificação PII.

**Detalhe**: M365 Copilot = US$ 30/seat/mês × 5k × 60 meses = US$ 9 M (apenas casos office). Não cobre os 11 casos sensíveis. Pode ser **complemento** ao on-prem para usuários office, não substituto.

**Ref**: `02-comparativo-alternativas.md` §3 e §4.

---

### F2. Comparado a Bradesco/Itaú/JPMorgan, onde estamos?

**Resposta executiva**: ainda não estamos. Esses três já capitalizaram. A janela é de 6–12 meses antes da defasagem ficar visível.

**Detalhe**: ver Slide 12 bônus e Etapa 3 §01 (financeiro BR).

**Ref**: Etapa 3 §00 e §01.

---

### F3. E o Cohere North? Ele entrega isso "em caixa"?

**Resposta executiva**: Cohere North é uma alternativa "appliance" comercial. Custos de licença e lock-in pesam. Open-source equivalente (vLLM + Llama/Granite) entrega 80–90% do valor com 30–50% do TCO.

**Detalhe**: Etapa 2 §06 cobre plataformas enterprise. Cohere "open weights" (Command R, Embed v4, Rerank 3) são CC BY-NC — não comercial.

**Ref**: Etapa 2 §06; Etapa 2 §11.

---

## G. Decisão

### G1. Se aprovarmos hoje, o que muda na semana que vem?

**Resposta executiva**: Sponsor nomeado; Tech Lead em busca; RFP de hardware em 3 OEMs; DPO engajado; comitê de IA constituído.

**Detalhe**: Fase 0 começa imediatamente. Decisões executivas pendentes (Etapa 4 §11) entram em pauta semanal.

**Ref**: `08-decisao-go-no-go.md`.

---

### G2. Se não aprovarmos, qual o cenário?

**Resposta executiva**: 3 cenários — (a) shadow AI continua sem governança, (b) concorrentes capitalizam e ganham produtividade, (c) auditoria regulatória futura aponta gap.

**Detalhe**: 35% dos breaches em 2024 envolveram shadow AI (IBM Security). LGPD Art. 11 e EU AI Act high-risk são audits previsíveis.

**Ref**: Slide 1 da narrativa.

---

### G3. Há um caminho intermediário?

**Resposta executiva**: sim — o **gate Go/No-Go do mês 5** é exatamente isso. Aprovar Fase 0+1 hoje (US$ 0,8–1,2 M no Cenário M); decidir Fases 2–4 com dados reais.

**Detalhe**: a decisão **não é tudo ou nada**. É faseada. Fase 1 valida a tese com dados próprios da empresa antes de comprometer CAPEX maior.

**Ref**: `03-roadmap-12-meses.md` §4 (gate); Slide 11.

---

### G4. Qual o custo de NÃO decidir agora?

**Resposta executiva**: 6–12 meses de defasagem competitiva + risco crescente de shadow AI + lead time de GPU somando atrasos.

**Detalhe**: lead time de hardware sozinho é 4–8 meses. Cada mês de adiamento = 1 mês a menos de produtividade capturada. Cenário M: ~US$ 1 M/mês de benefício deixado na mesa.

**Ref**: `01-modelo-roi-cenarios.md` §3.5.

---

## H. Operação contínua

### H1. Quem responde quando o cluster cai às 3h da manhã?

**Resposta executiva**: SRE on-call. Cobertura 24/7 light no Cenário M, plena no Cenário G. Runbooks publicados.

**Detalhe**: GameDay DR trimestral. Runbooks por cenário (vLLM down, Qdrant down, gateway down, GPU térmica). MTTR alvo conforme SLO.

**Ref**: Etapa 4 §07 e §08; `04-equipe-e-orcamento.md`.

---

### H2. Como validamos que o modelo está bom?

**Resposta executiva**: evals contínuas (Ragas + DeepEval + Promptfoo) rodando como CI/CD; canary release via gateway; dashboard Langfuse com alerta de drift.

**Detalhe**: cada mudança de modelo ou prompt passa por canary (5% tráfego). Métricas de qualidade comparadas; rollback automático se cair.

**Ref**: `05-riscos-mitigacao.md` R8; Etapa 2 §08.

---

### H3. Como garantimos que o RAG não retorna documento errado para usuário errado?

**Resposta executiva**: ACL no retrieval (Qdrant payload filters), replicando ACL do sistema fonte. Teste de penetração específico.

**Detalhe**: OWASP LLM08 (Vector & Embedding Weaknesses) é tratada como risco crítico (R14). Auditoria interna trimestral.

**Ref**: `05-riscos-mitigacao.md` R14; Etapa 3 §09.

---

## Fontes

- Etapa 1 (casos de uso); Etapa 2 (tecnologias); Etapa 3 (exemplos reais); Etapa 4 (infraestrutura).
- IBM Security Cost of a Data Breach 2025.
- OWASP GenAI Top 10 LLM 2025.
- LGPD, GDPR, EU AI Act, ISO/IEC 42001.
- Casos públicos: JPMorgan, BBVA, Walmart, Stripe, Bradesco, Mayo, Singapura, Bosch, BMW.
