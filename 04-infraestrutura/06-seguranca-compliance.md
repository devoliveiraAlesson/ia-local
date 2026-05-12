# Segurança, Identity e Compliance

> Etapa 4/5 da proposta. Modelo de segurança, governança de modelos, identity, multi-tenancy e mapeamento de compliance (LGPD, GDPR, HIPAA, SOC 2, ISO 27001, ISO/IEC 42001).

## 1. Princípios de segurança da plataforma

1. **Zero-trust por padrão**: nada é confiável por estar dentro do perímetro.
2. **Defesa em profundidade**: ingress, gateway, guardrails, policy, observabilidade — falha em uma camada não compromete o todo.
3. **Mínimo privilégio**: cada workload e cada usuário tem apenas o necessário.
4. **Auditabilidade total**: todo prompt, resposta, decisão de guardrail, e operação administrativa é logada (e WORM quando regulado).
5. **Soberania de dados**: dados nunca atravessam fronteiras técnicas ou jurisdicionais sem decisão explícita.
6. **Supply chain controlada**: modelos só entram em produção com hash verificado, scan de segurança e aprovação.

## 2. Topologia de rede e perímetros

```
   ┌──────────────────────────────────────────────────────────┐
   │ Internet (não confiável)                                 │
   └────────────────────┬─────────────────────────────────────┘
                        │ Proxy de saída controlado
                        │ (Squid/Zscaler), allow-list rígido
                        ▼
   ┌──────────────────────────────────────────────────────────┐
   │ DMZ (zona desmilitarizada)                               │
   │ - Mirror HF Hub Enterprise / JFrog Artifactory           │
   │ - Update server (yum/apt internos)                       │
   │ - Container registry (Harbor) com Cosign                 │
   │ - Scanner ProtectAI / Garak / PyRIT                      │
   └────────────────────┬─────────────────────────────────────┘
                        │ Promoção controlada (CI/CD com aprovações)
                        ▼
   ┌──────────────────────────────────────────────────────────┐
   │ Zona corporativa interna                                 │
   │ - SSO (Keycloak / Entra ID) + MFA                        │
   │ - Reverse proxy + WAF                                    │
   │ - Frontend (Open WebUI) + Gateway (LiteLLM)              │
   │ - Guardrails IN/OUT                                      │
   └────────────────────┬─────────────────────────────────────┘
                        │ mTLS Istio
                        ▼
   ┌──────────────────────────────────────────────────────────┐
   │ Zona de inferência (mais sensível)                       │
   │ - K8s namespace ai-inference                             │
   │ - Sem saída para internet                                │
   │ - Logs WORM + SIEM                                       │
   └──────────────────────────────────────────────────────────┘
                        │
                        ▼
   ┌──────────────────────────────────────────────────────────┐
   │ Zona de dados (mais sensível ainda)                      │
   │ - Vector store, Postgres, MinIO WORM                     │
   │ - Acesso só por workloads autorizadas via mTLS           │
   └──────────────────────────────────────────────────────────┘
```

## 3. Air-gap completo vs DMZ controlada

| Modelo | Quando usar | Custos / penalidades |
|--------|-------------|---------------------|
| **Air-gap completo (sem internet)** | Defesa, governo nacional, dados ITAR/EAR, secret-grade | Atualizações por mídia removível ou diodo de dados; mais caro; equipe maior; lentidão de inovação |
| **DMZ + mirror controlado** | Banco T1, saúde regulada, jurídico | Padrão na maioria das empresas reguladas; suficiente para LGPD/GDPR/HIPAA |
| **Egress allow-list** | Empresa média regulada | Tráfego de saída só para domínios aprovados (huggingface.co, github.com, hub.docker.com); auditável |
| **Open egress** | Não recomendado em ambiente sensível | Risco de exfiltração via prompt; dificulta compliance |

**Recomendação para perfil corporativo regulado médio**: **DMZ + mirror HF + egress allow-list**, evoluindo para **air-gap em zonas críticas** (e.g., HR + jurídico + clínico) se exigência regulatória.

## 4. Mirror local de Hugging Face — controle de supply chain

### 4.1 Riscos OWASP LLM 2025 endereçados

- **LLM03 Supply Chain**: modelos comprometidos, datasets envenenados, dependências maliciosas.
- **LLM05 Improper Output Handling**: serialization malformada (pickle).
- **LLM10 Unbounded Consumption**: modelos com exfiltração ou DoS embutido.

### 4.2 Pipeline de promoção de modelo

```
1. Solicitação interna       → ticket "novo modelo X"
2. Curadoria IA Governance   → licença OK? Tarefa válida?
3. Download via mirror DMZ   → SHA256 + assinatura HF (se disponível)
4. Scan ProtectAI Guardian   → arquivos pickle, lambda layers, payloads
5. Scan Garak / PyRIT        → red-team automático (jailbreak, PII leak)
6. Avaliação técnica         → benchmarks internos + Langfuse evals
7. Aprovação Sec + Compliance→ assinatura digital
8. Cosign sign + push Harbor → imagem OCI imutável
9. Argo CD deploy canary     → 10% tráfego, 24h
10. Promote 100%             → após gate de qualidade
```

### 4.3 Soluções de mirror

- **Hugging Face Hub Enterprise (on-prem appliance)**: caminho oficial para empresa que paga assinatura HF.
- **JFrog Artifactory** com tipo "Hugging Face Repositories" (lançado 2024).
- **Sonatype Nexus Repository Pro** (raw repo type para HF).
- **MinIO + huggingface-cli mirror**: caminho mais barato; controle manual.

## 5. Identity & Access Management (IAM)

### 5.1 Provedores de identidade integrados

| IdP | Integração com Open WebUI | Integração com LibreChat | Integração com AnythingLLM | Notas |
|-----|----------------------------|---------------------------|------------------------------|-------|
| **Keycloak** (open source) | OIDC nativo | OIDC + LDAP | OIDC | Recomendado on-prem se sem IdP corporativo |
| **Microsoft Entra ID** | OIDC | OIDC + Azure AD | OIDC | Padrão em empresas Microsoft |
| **Okta** | OIDC | OIDC + SAML | OIDC | Common em empresas SaaS-first |
| **Ping Identity** | OIDC + SAML | OIDC + SAML | OIDC | Comum em FSI |
| **CyberArk Conjur** | OIDC + secret store | OIDC + secret store | n/a | FSI hardened |

**MFA obrigatória** para todos os usuários humanos. Para serviços, **service accounts + SPIFFE/SPIRE** ou **OIDC workload identity**.

### 5.2 RBAC em camadas

- **Borda (frontend)**: controle de acesso por grupo (LDAP/AAD), e.g., "Pode usar modelo de raciocínio?".
- **Gateway**: tenant headers, quotas, rate-limit por grupo.
- **Modelo**: alguns modelos só liberados para grupos específicos (e.g., DeepSeek-R1 para "advanced research").
- **RAG**: ACLs no índice (Qdrant tenants, Milvus partitions, pgvector RLS).
- **Logs**: leitura de logs WORM só para Compliance/Audit.

### 5.3 Audit trail

- Cada request: `user_id`, `tenant`, `group`, `prompt_hash`, `model`, `timestamp`, `decision_guardrail`, `tokens_in`, `tokens_out`, `cost_attribution`.
- Retenção: **5 anos** (LGPD/HIPAA/SOX padrão).
- Storage: WORM (MinIO Object Lock, Veritas).
- SIEM: Splunk, Elastic Security ou Microsoft Sentinel.

## 6. Multi-tenancy em vector store

| Tecnologia | Estratégia de isolamento | Quando funciona | Limites |
|-----------|---------------------------|------------------|---------|
| **Qdrant** | "Multi-tenancy" via payload index + filtro automático no SDK | Padrão recomendado em 2026 | Performance OK até milhares de tenants pequenos |
| **Milvus** | Partition key + schema por tenant | Grande escala | Operação complexa em milhares de tenants |
| **Weaviate** | Tenant nativo (multi-tenancy built-in v1.20+) | Excelente para tenants moderados | Bom equilíbrio |
| **pgvector + RLS** | Row Level Security por tenant_id | Postgres já é parte da stack | Limite ~10–50M vetores |
| **Elastic** | Index por tenant ou ILM com filter | Empresa Elastic-first | Custo de cluster |

**Recomendação**: começar com **Qdrant tenants** (escalável, low-ops); migrar para **Milvus** se >50M vetores ou consultas extremamente concorrentes.

### 6.1 Padrão de tenant header

```
HTTP request → gateway (LiteLLM)
  X-Tenant-ID: finance
  Authorization: Bearer <user-token>
gateway:
  - valida token contra IdP
  - resolve tenant via claim do token
  - injeta tenant_id em payload do RAG retriever
  - aplica quota por tenant
RAG retriever:
  - filtra Qdrant por tenant_id (server-side)
audit log:
  - user, tenant, model, retrievals, output
```

## 7. Guardrails — defesa em profundidade

| Camada | Tecnologia | Função |
|--------|-----------|--------|
| Input | **Llama Guard 3 8B** | Categorias proibidas (violência, self-harm, jailbreak, etc.) |
| Input | **Microsoft Presidio** | Detecção e mascaramento de PII/PHI/PCI |
| Input | **Guardrails AI / NeMo Guardrails** | Política custom, allow-list de tópicos |
| Output | **Llama Guard 3 8B** | Mesma checagem na saída |
| Output | **Presidio reverse** | Re-mascarar PII se vazou |
| Output | **Lakera Guard / ProtectAI Rebuff** | Anti prompt-injection avançado (comercial) |
| Retrieval | **Filtros ACL no vector store** | LLM08 — Vector & Embedding Weaknesses |
| Tools | **Allow-list de funções/MCP** | LLM06 — Excessive Agency |

OWASP LLM Top 10 2025 — mapeamento:

| Risco OWASP | Mitigação |
|-------------|-----------|
| LLM01 Prompt Injection | Guardrails IN, system prompt hardening, separation of context, scan Garak |
| LLM02 Sensitive Info Disclosure | Presidio IN/OUT, classifier de saída, política de retenção |
| LLM03 Supply Chain | Mirror HF + Cosign + ProtectAI scan + aprovação |
| LLM04 Data and Model Poisoning | Curadoria de fine-tune; teste pré-promoção |
| LLM05 Improper Output Handling | Sanitização de markdown/HTML; validação de chamada de tool |
| LLM06 Excessive Agency | Allow-list de tools + dry-run + human-in-loop em ações destrutivas |
| LLM07 System Prompt Leakage | Não confiar no system prompt como segurança; segregar dados |
| LLM08 Vector & Embedding Weaknesses | Multi-tenancy real no vector store; ACL no retrieval |
| LLM09 Misinformation / Hallucination | RAG com fontes; reranker; eval contínuo (Ragas/DeepEval) |
| LLM10 Unbounded Consumption | Quotas por tenant; circuit breaker; alerta de cost spike |

## 8. Logs de prompts — política de retenção

| Categoria | Conteúdo retido | Retenção mínima | Imutabilidade |
|-----------|------------------|------------------|----------------|
| Auditoria de acesso | user, model, timestamp | 5 anos | WORM obrigatório (LGPD Art. 37) |
| Prompt content (em casos não sensíveis) | full prompt + response | 90 dias | mutável aceito |
| Prompt content (saúde/financeiro) | redacted (Presidio) | 5 anos | WORM |
| Decisões de guardrail | categoria, confidence | 5 anos | WORM |
| Dados pessoais | criptografado, com chave separada | conforme LGPD | direito de exclusão (Art. 18) implementado |

**Atenção LGPD Art. 18**: usuário pode pedir exclusão. Logs WORM + LGPD = projetar **anonimização irreversível** após X dias, mantendo só hash + metadados.

## 9. Mapeamento de compliance

### 9.1 LGPD (Brasil)

- Art. 7º: base legal (consentimento, legítimo interesse, etc.) explícita por caso de uso.
- Art. 11: dado sensível (saúde, religião, biometria) — base legal mais restrita.
- Art. 18: titular pode pedir acesso, correção, exclusão.
- Art. 37: registro das operações de tratamento (audit trail).
- Art. 50: programa de governança em privacidade (DPO + RIPD para casos com automatizada).
- Art. 20: direito à revisão de decisão automatizada — relevante para atendimento.

### 9.2 GDPR (UE)

- Art. 22: decisão automatizada exige human-in-loop ou opt-out.
- Art. 30: registro das atividades.
- Art. 32: medidas técnicas e organizacionais.
- Art. 35: DPIA para casos com risco alto.

### 9.3 HIPAA (US — saúde)

- BAA com fornecedor.
- PHI nunca em logs sem mascaramento.
- Audit trail mínimo 6 anos.
- Modelos comerciais (OpenAI/Anthropic) só com BAA assinado — frequente bloqueador para chat público.

### 9.4 SOC 2 Tipo II

- Trust criteria: Security, Availability, Confidentiality, Processing Integrity, Privacy.
- Controles documentados + auditoria anual.
- IA precisa estar dentro do escopo dos controles existentes.

### 9.5 ISO 27001

- ISMS — Information Security Management System.
- Controles do Anexo A aplicados a workloads de IA.
- Em 2026, organizações maduras já têm Annex A 8.34 (proteção de informação durante teste) e 8.16 (atividades de monitoramento) cobrindo IA.

### 9.6 ISO/IEC 42001 (AI Management System) — relevante 2026

- Primeira norma certificável para "AI Management System".
- Controles para: governança de IA, ciclo de vida de modelo, dados, transparência.
- **IBM Granite 4 é o primeiro modelo open source ISO/IEC 42001 certificado** (ver Etapa 2). Útil para empresa que precisa **alinhar prova ao auditor**.
- Em 2026, ISO 42001 vira **diferencial em RFPs governamentais BR/EU**.

### 9.7 EU AI Act (entrada em vigor escalonada 2025–2027)

- **Risco inaceitável** (proibido): sistemas de social scoring, manipulação subliminar.
- **Alto risco** (controles pesados): saúde, educação, RH (recrutamento), crédito, justiça.
- **Limited risk** (transparência): chatbot deve identificar-se como IA.
- **Mínimo risco**: maioria dos chatbots internos.
- Mais relevante para empresas EU; ressoa em multinacionais com operação UE.

## 10. Auditoria e SIEM

- Logs estruturados em JSON com **trace-id propagado**.
- Coleta via **OpenTelemetry GenAI semantic conventions**.
- SIEM (Splunk / Elastic / Sentinel) ingere logs de:
  - Gateway (decisões de roteamento, quotas).
  - Guardrails (bloqueios, categorias).
  - Inferência (modelo, latência, tokens).
  - Vector store (queries, ACLs).
  - K8s audit log.
  - IdP (logins, MFA).
- Alertas: jailbreak detectado, exfiltração suspeita, cost spike, modelo não-aprovado em uso.

## 11. Soberania de dados (BR / EU / US / CN)

| Restrição comum | Implicação para arquitetura |
|------------------|-------------------------------|
| Dados BR não saem do BR | Datacenter em SP/RJ; nuvem privada brasileira; sem dependência de cloud US-headquartered (em casos extremos) |
| Dados EU não saem da UE | Datacenters em FR/DE/IE; alternativa Aleph Alpha (DE); evitar cloud US-headquartered (Schrems II) |
| Dados US (DoD/IL) | GovCloud / IL5+; equipe US-cleared |
| Dados CN | NÃO usar Qwen oficialmente em ambientes anti-CN; preferir Llama/Granite |

Para empresas brasileiras **reguladas** (BACEN, ANS, ANPD), a posição segura em 2026 é **on-prem em DC nacional** ou **cloud privada nacional** (Serpro, Embratel, TIVIT).

## 12. Decisões executivas

| Pergunta | Recomendação |
|----------|--------------|
| Air-gap completo? | Só se ITAR/EAR/segredo de Estado; caso contrário DMZ + allow-list. |
| IdP único ou separado? | Único corporativo (Entra ID/Okta/Keycloak); evitar usuários locais. |
| Mirror HF interno obrigatório? | Sim, em qualquer ambiente regulado. |
| Llama Guard 3 obrigatório? | Sim em prod externa; opcional em chat interno baixo-risco. |
| WORM de prompts obrigatório? | Sim em saúde/financeiro/jurídico/gov. |
| ISO 42001 alvo? | Sim para empresas reguladas em 2026–2027. |

## Referências

- OWASP Top 10 LLM 2025: <https://genai.owasp.org/llm-top-10/>
- ISO/IEC 42001: <https://www.iso.org/standard/81230.html>
- IBM Granite ISO 42001: <https://digital.nemko.com/news/ibm-granite-40-first-iso-42001-certified-open-source-ai>
- LGPD: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>
- EU AI Act: <https://artificialintelligenceact.eu/>
- Microsoft Presidio: <https://microsoft.github.io/presidio/>
- Llama Guard 3: <https://huggingface.co/meta-llama/Llama-Guard-3-8B>
- ProtectAI Guardian: <https://protectai.com/guardian>
- Garak: <https://github.com/leondz/garak>
- PyRIT: <https://github.com/Azure/PyRIT>
- Cosign: <https://www.sigstore.dev/>
- SPIFFE/SPIRE: <https://spiffe.io/>
