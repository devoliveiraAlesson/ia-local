# Roadmap de Adoção — Design System de Apresentações

> Fases 0–3 de rollout do sistema de apresentações via MCP. Da POC ao uso corporativo amplo, com gates de aprovação e métricas de sucesso em cada fase.

## Visão do roadmap

```
Fase 0 (2 semanas)   → POC: wizard + 1 template + Google Slides API funcionando
Fase 1 (4 semanas)   → Alpha interno: 1 template onboarded, 3–5 usuários piloto
Fase 2 (6 semanas)   → Beta corporativo: todos templates, todos usuários, observabilidade
Fase 3 (ongoing)     → Produção: integrações avançadas (RAG, Jira, Slack), self-service
```

## Fase 0 — POC (semanas 1–2)

**Objetivo**: provar que a stack funciona ponta a ponta em ambiente de desenvolvimento.

**Entregáveis**:
- [ ] Conta Google Cloud criada, Drive API e Slides API ativadas.
- [ ] 1 template básico no Drive (pode ser o Corporativo, feito no Google Slides manualmente).
- [ ] `tokens.json` com a paleta de cores e tipografia real da empresa.
- [ ] Servidor MCP mínimo (FastMCP) rodando localmente com 3 tools: `wizard_start`, `wizard_answer`, `wizard_confirm`.
- [ ] 1 geração completa funcionando: wizard → cópia do template → batchUpdate com 5 slides → link no Drive.
- [ ] Claude Code configurado localmente (`claude mcp add --scope local`) e testado.

**Critério de aprovação**: um deck de 5 slides gerado via conversa com o agente, on-brand, em menos de 2 minutos de geração.

**Quem faz**: 1 engenheiro de plataforma, ~2 semanas dedicadas (ou 4 semanas em part-time).

**Riscos nesta fase**:
- OAuth 2.0 / service account pode ter friction com política do Google Workspace corporativo → testar com conta pessoal se necessário para POC.
- Fonts customizadas: Google Slides API suporta apenas Google Fonts → confirmar se a fonte da marca está no Google Fonts; caso contrário, definir substituta para esta fase.

---

## Fase 1 — Alpha Interno (semanas 3–6)

**Objetivo**: validar com usuários reais, coletar feedback, ajustar o wizard e os templates.

**Entregáveis**:
- [ ] Servidor MCP deployado em ambiente interno (container, Cloud Run, ou VM dedicada).
- [ ] OAuth por usuário funcionando: cada usuário autoriza o servidor com sua conta Google Workspace → deck gerado aparece no Drive do usuário.
- [ ] 3–4 templates prontos: Corporativo, Pitch, Treinamento, Executivo.
- [ ] Variantes de tema implementadas: default, dark, clean.
- [ ] Observabilidade básica: logs estruturados, span por geração, qual versão de tokens foi usada.
- [ ] 3–5 usuários piloto (sugestão: 1 de marketing, 1 de vendas, 1 técnico, 1 de produto).
- [ ] Formulário de feedback após cada uso (pode ser um Google Form simples).
- [ ] `claude mcp add` documentado em uma página interna (Confluence ou Notion).

**Critério de aprovação**: NPS ≥ 7 nos pilotos, < 20% de gerações com retrabalho manual pesado.

**Métricas a coletar**:
- Tempo médio do wizard (do wizard_start ao wizard_confirm).
- Tempo médio de geração (do confirm ao link entregue).
- Número de "quer ajustar algum slide?" após entrega.
- Slides modificados manualmente após geração (proxy: tempo de edição no Google Slides).

---

## Fase 2 — Beta Corporativo (semanas 7–12)

**Objetivo**: expandir para todos os usuários, garantir estabilidade e observabilidade completa.

**Entregáveis**:
- [ ] Todos os templates finalizados e aprovados pelo time de Design/Comunicação.
- [ ] `tokens.json` versionado em git, com processo de atualização: PR → review → deploy via CI/CD.
- [ ] Servidor MCP com autenticação via SSO corporativo (Keycloak/Azure AD/Okta), não mais OAuth individual por usuário.
- [ ] Rate limiting por usuário/equipe.
- [ ] Observabilidade completa: Langfuse, spans OTel, dashboard com gerações/dia, erros, latência.
- [ ] Documento de `GUIA-DE-USO.md` para usuários finais (não técnicos).
- [ ] Guia de atualização de tokens para o time de Design (sem precisar de eng de plataforma).
- [ ] Servidor MCP em escopo `project` no `.mcp.json` do repositório principal da empresa (ou escopo `user` via política de TI).
- [ ] Integração opcional com Slack: agente posta link do deck no canal após geração.

**Critério de aprovação**: 20+ gerações por semana, taxa de erro < 5%, tempo médio de geração < 90 segundos.

---

## Fase 3 — Produção e Integrações Avançadas (mês 4 em diante)

**Objetivo**: maximizar o valor do sistema com integrações que eliminam tarefas manuais.

### Integração 1: RAG Corporativo (Caso 3 + Etapa 6)

Quando o servidor MCP de RAG estiver em produção, o servidor de apresentações passa a buscar conteúdo automaticamente durante o wizard:

```python
# Durante build_outline, para cada slide de conteúdo:
rag_chunks = await rag_client.search(
    query=f"{slide.title} {meta.objective} {meta.audience}",
    top_k=3,
)
if rag_chunks:
    slide.content.body_draft = rag_chunks[0].text
    slide.content.source = rag_chunks[0].uri
```

O agente mostra o draft ao usuário: "Encontrei este conteúdo relevante na nossa base para o slide 3 — quer usar?"

**Ganho**: elimina o "abrir o relatório → copiar trecho → colar no slide". Estimativa: -30 min por deck que usa dados internos.

### Integração 2: PDF/Relatório → Slides (Caso 6)

Novo entry point do wizard:

```
Usuário: gere slides a partir deste relatório [anexa PDF]

Agente: [chama tool presentation.from_document(pdf_url, audience, objective)]
        → sumariza o PDF (Caso 6)
        → mapeia seções para skills de slides
        → confirma outline com usuário
        → gera o deck
```

**Ganho**: relatório de 30 páginas → deck executivo de 10 slides em 5 minutos.

### Integração 3: Sprint Review Automático (GitHub/Jira + Slides)

Template de sprint review preenchido automaticamente com dados do Jira/GitHub via MCP:

```
Usuário: gere o deck de sprint review da Sprint 42

Agente: [chama jira.get_sprint_summary(sprint=42)]
        [chama github.get_merged_prs(since=sprint_start)]
        → monta deck com: o que foi feito, métricas, bugs, próxima sprint
        → envia link no Slack para o time
```

**Ganho**: -2h de prep de sprint review por sprint. Para time com sprints de 2 semanas = ~50h/ano por dev.

### Integração 4: Atualização de Deck Existente

```
Usuário: [cola link de um deck] atualize os números deste slide com os dados de Abril

Agente: [chama slides.get(presentationId)]
        [identifica slide com dados numéricos]
        [busca dados de Abril no RAG ou pede ao usuário]
        → atualiza somente o slide de dados, preserva o resto
```

### Revisão contínua dos tokens

Processo trimestral recomendado:

1. Time de Design revisa `tokens.json` à luz de feedback das apresentações geradas.
2. Abre PR com mudança de tokens + bump de versão.
3. CI/CD roda `update_slide_master_from_tokens()` para cada template no Drive.
4. Servidor MCP pega nova versão automaticamente.
5. Slack notification: "tokens atualizados para v1.2.0 — novos decks usarão a nova paleta".

---

## Resumo de métricas por fase

| Métrica | Fase 0 (POC) | Fase 1 (Alpha) | Fase 2 (Beta) | Fase 3 (Prod) |
|---|---|---|---|---|
| Usuários ativos | 1 (eng) | 3–5 pilotos | Todos | Todos + integrações |
| Templates disponíveis | 1 | 3–4 | 4–6 | 4–6 + específicos |
| Tempo médio de geração | < 2 min | < 90 s | < 60 s | < 60 s |
| Taxa de erro (geração falhou) | Não medido | < 20% | < 5% | < 2% |
| Gerações/semana | 1–5 | 5–15 | 20+ | 50+ |
| Satisfação (NPS pós-uso) | Não medido | ≥ 7 | ≥ 8 | ≥ 8 |
| Slides editados manualmente após geração | Não medido | Coletar | < 30% | < 15% |

---

## Integração com o roadmap mestre da Etapa 5

| Item da Etapa 5 | Relação com este sistema |
|---|---|
| Fase 1 — chat interno (Q1) | Pode servir como canal de acesso ao wizard de apresentações |
| Fase 2 — RAG corporativo (Q2) | Pré-requisito para Integração 1 (enriquecimento de conteúdo) |
| Fase 2 — coding assistant (Q2) | Mesmo servidor MCP de plataforma; patterns reusáveis |
| Fase 3 — sumarização (Q3) | Pré-requisito para Integração 2 (PDF → slides) |
| Fase 4 — automações (Q4) | Integração 3 (sprint review automático) se encaixa aqui |

---

## Próxima ação imediata

Para dar o próximo passo: abrir uma issue interna com o escopo da **Fase 0** (POC), alocar 1 eng por 2 semanas, e entregar o primeiro deck gerado via agente para aprovação do Tech Lead. O material técnico para implementar está em [`05-construir-servidor-mcp.md`](./05-construir-servidor-mcp.md).
