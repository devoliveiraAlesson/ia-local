# Caso 7 — Extração Estruturada de Dados (PDFs, E-mails, Formulários)

## Descrição

Transformar documentos não estruturados em **JSON validado** por schema, alimentando sistemas downstream (ERP, CRM, BI, BPM). Casos típicos:

- **Faturas / notas fiscais** → fornecedor, CNPJ, itens, valores, tributos, datas.
- **Contratos** → partes, valor, índice de reajuste, cláusulas-chave, data de início/término, multa.
- **Prontuários / laudos** → diagnóstico, exames, medicamentos, alergias, histórico.
- **Formulários / cadastros** → preenchimento automático em CRM/onboarding.
- **E-mails de clientes** → triagem, classificação, extração de campos (pedido, urgência, motivo).
- **Currículos** → educação, experiências, skills, anos por cargo.
- **Documentos de identidade / KYC** → nome, documento, validade (com detecção de fraude separada).

Tudo com saída validada (Pydantic / JSON Schema) e ramo de fallback humano para baixa confiança.

## Por que precisa ser LOCAL

- Faturas e contratos contêm dados financeiros e fiscais sigilosos (segredo fiscal, sigilo bancário).
- Prontuários e laudos são dados pessoais sensíveis (LGPD art. 5º II — dado de saúde, requer base legal específica).
- Currículos e formulários incluem PII (CPF, RG, data de nascimento, endereço, salário pretendido).
- E-mails contêm informação de cliente, contratos e operações.
- Em **back-office regulado** (bancos, planos de saúde, governo), pipeline de extração é parte da cadeia de auditoria — tem que ser auditável e dentro do perímetro.

## Modelo recomendado

- **Geral, com saída JSON forte**:
  - Llama 3.3 70B (function calling/tool use confiável).
  - Qwen 2.5 32B/72B (excelente em JSON estruturado).
  - Mistral Small 3 (eficiente, JSON nativo).
  - IBM Granite 3 8B (forte em extração estruturada empresarial, ISO/IEC 42001).
- **Visão-linguagem (PDFs com layout, scans, formulários)**:
  - Qwen 2.5-VL 7B / 32B / 72B — estado da arte open source em 2025–2026 para documentos.
  - Llama 4 Scout (multi-modal nativo).
  - InternVL 2.5, Pixtral 12B (Mistral).
- **Específico para documentos**: Granite-Vision (IBM), Florence-2.

## Stack típica

- **Parsing prévio (não-VL)**:
  - **Docling** (IBM) — best-in-class open source para PDF/tabelas/layout, suporta OCR.
  - **MinerU** (OpenDataLab) — PDF/Office → Markdown/JSON.
  - **Unstructured.io** self-hosted.
  - **PaddleOCR / Tesseract** para OCR puro.
- **Extração com LLM**:
  - **Outlines** ou **Instructor** ou **JSON Schema** nativo do vLLM — saída garantida.
  - **LlamaExtract** (LlamaIndex) se aceitar combinar com agente.
  - **LLMWare** para pipelines RAG-extract empresariais.
- **Validação**: Pydantic + regras de negócio + reconciliação com mestres internos (lista de fornecedores, CNPJs ativos, planos de contas).
- **Orquestração**: Prefect, Airflow, Temporal, Dagster.
- **Human-in-the-loop**: fila com confidence < threshold cai para revisão humana (Label Studio, Argilla, app interno).

## Métricas de sucesso / KPIs

- **Field-level accuracy** por tipo de campo (meta > 98% para campos críticos como valor, CNPJ, datas).
- **% straight-through-processing** (documentos que não precisam de revisão humana).
- **Throughput** (documentos/hora).
- **Custo por documento** (vs baseline RPA/OCR tradicional).
- **Tempo de ciclo** do back-office (ex.: contas a pagar — de dias para minutos).
- **Taxa de re-trabalho** detectada na conciliação a jusante.

## Estimativa de retorno

**Muito alta.** Provavelmente o caso com **ROI mais mensurável** da proposta. Cenário típico em contas a pagar: 50.000 faturas/mês, 4 minutos de processamento manual cada → 3.300 horas/mês = ~20 FTE. Automação chega a 60–85% straight-through em 6 meses, com payback em < 12 meses.

Setores onde o retorno é especialmente claro: financeiro (KYC, onboarding), saúde (prontuários, faturamento TUSS/CBHPM), seguros (sinistros, formulários), governo (protocolos, requerimentos), jurídico (peças, processos).

## Maturidade

**Produção média.** Pipeline funcional em 6–10 semanas para um tipo de documento. Ampliar para 5–10 tipos com governança, monitoramento de drift e HITL leva 6–9 meses.

## Riscos e mitigação

- **Alucinação em valor numérico**: forçar saída com regex/JSON schema + validação cruzada (soma de itens = total) + double-check com OCR puro.
- **Drift de layout** (fornecedor muda template): monitorar accuracy por origem; alertar quando cair.
- **Documentos com qualidade ruim** (scan torto, baixa resolução): pré-processamento + threshold de confiança automático para HITL.
- **Compliance**: trilha de auditoria por documento (qual modelo, qual versão, qual prompt, quando, por quem).

## Fontes consultadas

- Unstract — LLMs for Structured Data Extraction from PDFs 2026: <https://unstract.com/blog/comparing-approaches-for-using-llms-for-structured-data-extraction-from-pdfs/>
- LlamaIndex — Beyond OCR / PDF parsing with LLMs: <https://www.llamaindex.ai/blog/beyond-ocr-how-llms-are-revolutionizing-pdf-parsing>
- LlamaIndex — LlamaExtract: <https://www.llamaindex.ai/blog/introducing-llamaextract-unlocking-structured-data-extraction-in-just-a-few-clicks>
- MinerU (OpenDataLab): <https://github.com/opendatalab/mineru>
- Simon Willison — Structured data extraction with LLM schemas: <https://simonwillison.net/2025/Feb/28/llm-schemas/>
- AlgoDocs — Best LLMs for document processing 2025: <https://algodocs.com/best-llm-models-for-document-processing-in-2025/>
- Databricks Community — End-to-End Structured Extraction with LLM: <https://community.databricks.com/t5/technical-blog/end-to-end-structured-extraction-with-llm-part-1-batch-entity/ba-p/98396>
