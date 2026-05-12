# Caso 1 — Chat Interno Seguro (Substituto Privado do ChatGPT)

> Quick win clássico. Reduz drasticamente o "shadow AI" (uso não controlado de ChatGPT/Claude/Gemini gratuitos por funcionários colando dados sensíveis em sites públicos).

## Descrição

Disponibilizar uma interface de chat conversacional para todos os funcionários da empresa, com a mesma ergonomia do ChatGPT (multi-conversa, anexos, prompts reutilizáveis, histórico, busca), mas servida 100% dentro do perímetro corporativo. O modelo é um LLM aberto rodando em GPU on-prem ou em nuvem privada (VPC dedicada). Toda a interação — prompts, anexos, histórico — fica em banco interno, sob controle do time de Segurança/TI, com SSO corporativo, RBAC, auditoria e retenção configurável.

Casos típicos de uso pelos funcionários:
- Reescrever e-mails e comunicações.
- Resumir documentos colados (atas, contratos, relatórios).
- Brainstorm de copy, propostas e apresentações.
- Pequenas conversões (CSV → JSON, regex, etc.).
- Q&A sobre arquivos anexados (com RAG opcional já neste caso).

## Por que precisa ser LOCAL

- Funcionários colam regularmente: trechos de contratos, dados de clientes, código proprietário, números financeiros não públicos, dados pessoais (LGPD/GDPR), informações cobertas por sigilo bancário, fiscal ou médico.
- Em APIs públicas o conteúdo trafega para fora do país, fica em logs do provedor por pelo menos 30 dias e, em alguns planos, pode ser usado para treinamento.
- Mesmo "modo enterprise" de provedores comerciais transfere dados para fora do tenant — inaceitável para setores regulados (Bacen 4.658/8.681, HIPAA, ISO 27701, LGPD em dados sensíveis).
- "Shadow AI": pesquisas (Cyberhaven, Kong) mostram que 4–11% dos funcionários colam regularmente dados sensíveis em IA pública. Oferecer uma alternativa interna é a contramedida mais eficaz.

## Modelo recomendado

- **Padrão (alto volume, qualidade próxima de GPT-4o)**: Llama 3.3 70B Instruct ou Llama 4 Scout (MoE, 17B ativos, contexto longo).
- **Eficiência**: Mistral Small 3, Qwen 2.5 14B/32B, IBM Granite 3.1 8B (forte em tom corporativo, certificado ISO/IEC 42001).
- **Reasoning sob demanda**: DeepSeek-R1 ou Qwen 3 reasoning para tarefas analíticas mais pesadas (modo "pensar").
- **Multilíngue PT-BR**: Llama 3.3, Qwen 2.5/3 e Mistral Large 2 têm bom desempenho em português; reforçar com prompts e few-shot.

Faixa típica de tamanho: 8B a 70B densos, ou 100–400B MoE. 70B denso quantizado em AWQ 4-bit roda em 2× A100 80 GB ou 1× H100 80 GB com folga.

## Stack típica

- **Runtime**: vLLM (gold standard de produção) servindo via API compatível OpenAI; alternativas: TGI (HuggingFace), SGLang, llama.cpp para edge.
- **Interface**: Open WebUI (rápido de subir, RBAC básico, plug-ins), LibreChat (SSO/OIDC/Azure AD/SAML, melhor para empresa), AnythingLLM (foco em RAG por workspace), BionicGPT (hardening corporativo).
- **Auth/SSO**: Keycloak, Azure AD, Okta via OIDC.
- **Telemetria/eval**: Langfuse (open source, on-prem) para tracing, custos, prompt management, avaliação automática.
- **Guardrails**: NVIDIA NeMo Guardrails, Llama Guard 3, ou regras customizadas para PII/segredo.

## Métricas de sucesso / KPIs

- Adoção: % de funcionários ativos semanais (WAU) e mensais (MAU). Benchmark JPMorgan: ~70% de WAU em 8 meses.
- Engajamento: número médio de conversas/usuário/semana, % de usuários "power" (>10 conversas/semana).
- Tempo economizado: 3 a 6 horas/semana/usuário (autorrelatado, validado em pesquisas internas — métrica usada pelo JPMorgan).
- Redução de uso de IA pública: queda em URLs de chatgpt.com/claude.ai nos logs de proxy.
- Latência: P50 < 1.5s para primeiro token, P95 < 3s.
- NPS interno do produto.

## Estimativa de retorno

**Alta**. Curva de adoção viral quando o produto chega "bom o suficiente" (qualidade ~85–90% do GPT-4o em tarefas corporativas comuns). Em uma empresa de 5.000 funcionários com 30% de adoção e 3h economizadas/semana, são ~234.000 horas/ano — equivalente a >100 FTE em produtividade recuperada.

## Maturidade

**POC fácil → Produção média.** Subir Open WebUI + Ollama com Llama 3.3 leva uma tarde. Levar a produção corporativa (SSO, RBAC, auditoria, HA, GPU sharing, FinOps, guardrails, programa de adoção) é projeto de 2–4 meses.

## Riscos e mitigação

- Vazamento de prompt para logs do produto: criptografia em repouso + retenção configurável + sanitização de PII.
- Alucinação em tarefas factuais: integrar RAG (Caso 3) e indicar claramente quando o modelo não tem fonte.
- Uso indevido (gerar conteúdo ofensivo, contornar políticas): Llama Guard 3 ou NeMo Guardrails + auditoria.

## Fontes consultadas

- JPMorgan Chase LLM Suite: <https://www.jpmorganchase.com/about/technology/blog/llmsuite-ab-award>
- The Digital Banker — JPMorgan LLM Suite: <https://thedigitalbanker.com/jpmorgan-chases-llm-suite-drives-ai-transformation-across-the-enterprise/>
- PremAI — Open WebUI alternatives 2026: <https://blog.premai.io/11-best-open-webui-alternatives-for-enterprise-llm-chat-2026/>
- Portkey — LibreChat vs Open WebUI: <https://portkey.ai/blog/librechat-vs-openwebui/>
- Digital Applied — Local LLM Deployment Guide: <https://www.digitalapplied.com/blog/local-llm-deployment-privacy-guide-2025>
- vLLM Recipes — Llama 3.3 70B: <https://docs.vllm.ai/projects/recipes/en/latest/Llama/Llama3.3-70B.html>
- HuggingFace blog — Best Open-Source LLMs 2025: <https://huggingface.co/blog/daya-shankar/open-source-llms>
- Langfuse (observabilidade open source): <https://github.com/langfuse/langfuse>
