# Caso 6 — Sumarização de Documentos Longos

## Descrição

Serviço para gerar resumos de qualidade profissional sobre documentos longos: contratos, atas de reunião, relatórios financeiros, processos jurídicos, laudos técnicos, RFPs, transcrições de call center e teleconferências. Modos:

- **Sumário executivo** (3–10 bullets, 1 página).
- **Sumário estruturado** (partes/cláusulas/decisões/responsáveis/prazos).
- **Sumário focado** (responder "o que esse contrato diz sobre rescisão?").
- **Sumário comparativo** (contraste entre versões de contrato — diff jurídico).
- **Resumo encadeado** para documentos que excedem o contexto do modelo (map-reduce ou refine).

## Por que precisa ser LOCAL

- Contratos contêm: partes, valores, cláusulas comerciais sensíveis, NDAs, dados de clientes, garantias, multas — tipicamente sob confidencialidade contratual.
- Atas de board / C-level são informações **material non-public information (MNPI)** — vazá-las pode configurar uso indevido de informação privilegiada (CVM, SEC).
- Laudos médicos, processos judiciais e relatórios de auditoria contêm PII/PHI sob regimes específicos (sigilo médico, segredo de justiça, sigilo fiscal).
- Transcrições de reunião com clientes contêm informações estratégicas e regulamentadas (LGPD).

## Modelo recomendado

- **Contexto longo / qualidade**:
  - Llama 4 Scout (MoE, contexto até 10M tokens em hardware adequado, ideal para contrato/processo inteiro).
  - Qwen 2.5 32B / 72B (contexto 128k–1M).
  - Mistral Large 2 (128k).
  - DeepSeek V3 / V3.2 (160k).
- **Bom custo-benefício**: Llama 3.3 70B (128k), Qwen 2.5 14B (128k), Mistral Small 3 (32k–128k).
- **Reasoning para sumário analítico de contratos**: DeepSeek-R1, Qwen 3 reasoning.
- **Especializado em jurídico (se houver volume alto)**: fine-tuning de Llama 3.3 ou Granite 3 sobre corpus interno.

## Stack típica

- **Runtime**: vLLM com flag `--max-model-len` adequada ao caso (cuidado com VRAM consumida pelo KV-cache em contextos longos).
- **Parsing**:
  - **Docling** (IBM, open source) — excelente em PDF, tabelas, layout, OCR opcional.
  - **MinerU** (PDF → Markdown/JSON).
  - **Unstructured.io self-hosted**.
  - **LlamaParse** se aceitar SaaS (mas geralmente queremos on-prem aqui).
- **Pipeline**:
  - Estratégias map-reduce e refine (LangChain/LlamaIndex) para documentos > contexto.
  - Sumário estruturado: prompts com schema JSON validado por Pydantic / Outlines / Instructor.
- **UI**: Open WebUI / LibreChat com upload de arquivo, ou app dedicado integrado ao DMS (SharePoint, Alfresco).
- **Avaliação**: ROUGE/BERTScore + human-in-the-loop por amostragem; faithfulness com Ragas.

## Métricas de sucesso / KPIs

- **Tempo médio de leitura economizado** (h/documento, autorrelatado e por amostra controlada).
- **Aderência factual** (faithfulness): % de afirmações no resumo verificáveis no documento, meta > 95%.
- **Cobertura**: % das cláusulas/decisões importantes capturadas (avaliado por especialista em amostra).
- **Tempo até primeiro draft de parecer/ata** redução de 40–70%.
- **Adoção por área** (jurídico, compliance, secretaria de governança, auditoria interna).
- **Taxa de re-edição** pelo profissional (meta caindo ao longo do tempo).

## Estimativa de retorno

**Alta.** Em jurídico/compliance e auditoria, a leitura de contratos longos consome muitas horas de profissionais caros. Casos públicos (Allen & Overy/Harvey, JPMorgan COiN) reportam redução de 70–90% no tempo de revisão de contratos e atas, com qualidade comparável quando o humano valida no final.

## Maturidade

**POC fácil.** Sumário básico é o caso "hello world" do LLM. A complexidade vem na qualidade jurídica/financeira (faithfulness, fidelidade a cláusulas) e em documentos com layout difícil (tabelas, scans antigos). Produção robusta em 2–4 meses, com QA por amostra.

## Riscos e mitigação

- **Alucinação em cláusula crítica**: sempre exigir citação (offset/página) e validação humana para uso jurídico vinculante.
- **Perda de informação em map-reduce**: comparar versão refine vs map-reduce em gold set; em contratos preferir refine.
- **PDF mal parseado** (tabelas, scans): pipeline de parsing precisa OCR fallback (Tesseract, PaddleOCR, ou modelos visão-linguagem locais como Qwen 2.5-VL).
- **Confidencialidade reforçada**: trilha de auditoria (quem sumarizou o que e quando) com retenção alinhada à política da empresa.

## Fontes consultadas

- Width.ai — Contract Summarization Using LLMs: <https://www.width.ai/post/contract-summarization-using-llms>
- SiliconFlow — Best Open Source LLM for Legal Document Analysis 2026: <https://www.siliconflow.com/articles/en/best-open-source-LLM-for-Legal-Document-Analysis>
- ACL Anthology — LLM-Based Legal Negotiation: <https://aclanthology.org/2024.nllp-1.11.pdf>
- IBM Developer — Fine-tuning LLMs for contract analysis (DPK): <https://developer.ibm.com/tutorials/dpk-fine-tuning-llms/>
- PMC — Technical evaluation of legal LLMs (clause extraction, classification, summarization): <https://pmc.ncbi.nlm.nih.gov/articles/PMC13062225/>
- LegalFly — Lawyer's guide to LLMs: <https://www.legalfly.com/post/a-lawyers-guide-to-large-language-models-llms>
- IBM Granite 3.0: <https://www.ibm.com/new/announcements/ibm-granite-3-0-open-state-of-the-art-enterprise-models>
