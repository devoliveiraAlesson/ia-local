# Etapa 7 — Design System para Apresentações: tokens, templates e MCP

> Estende as Etapas 1–6 com um sistema corporativo de construção de apresentações no Google Slides (e .pptx compatível), acionado via agente de IA. O agente acessa uma pasta do Google Drive com os assets da marca, aplica um design token system e conduz o criador da apresentação por um wizard guiado até entregar o deck pronto. Maio/2026.

## Por que esta etapa existe

Apresentações são o artefato de comunicação mais produzido em qualquer empresa — propostas, reports, decks executivos, treinamentos. São também os artefatos com maior **inconsistência visual** e maior **custo de tempo**: um analista passa 3–5 horas formatando manualmente o que deveria levar 30 minutos de conteúdo.

A Etapa 6 demonstrou que MCP virou o "USB-C" para tools de IA. A W3C Design Tokens Community Group publicou a primeira versão estável do formato DTCG em outubro de 2025. O Google anunciou servidores MCP oficiais para Workspace (Drive, Slides, Gmail, Calendar) no Google Cloud Next '26. **A stack necessária para o que o usuário pediu chegou madura em 2026.**

A proposta é:

> **Montar o design system da empresa uma vez (tokens + templates no Drive); expor via servidor MCP; o agente lê os assets, conduz o wizard com o usuário, e entrega o deck pronto no Google Drive — sem o usuário tocar em formatação.**

## Mensagem-chave em uma linha

> Tokens + templates no Drive → servidor MCP corporativo → wizard Claude → deck pronto, on-brand, no Drive.

## O que muda em relação ao processo atual

| Situação atual | Com Design System + MCP |
|---|---|
| Dev/analista abre template, duplica, reformata | Agente copia template automaticamente e aplica tokens |
| Cores, fontes, logos batem diferente em cada deck | Design tokens aplicados programaticamente — sem desvio |
| "Me manda o template atualizado" por Slack | Tokens e templates versionados no Drive; agente sempre pega a versão atual |
| Usuário passa 2–4 horas fazendo slides | Wizard coleta conteúdo em 10–20 min; slides gerados em seguida |
| Novo colaborador não sabe qual template usar | Agente conhece todos os templates e pergunta ao usuário qual objetivo tem |
| Deck novo para cliente → copiar/colar do deck antigo | Agente busca conteúdo relevante no RAG corporativo (Caso 3) e insere |

## O que esta Etapa entrega

| Doc | Conteúdo | Audiência |
|-----|----------|-----------|
| [`01-arquitetura-e-fundamentos.md`](./01-arquitetura-e-fundamentos.md) | Visão geral da stack, decisões arquiteturais, comparativo de abordagens | Tech Lead / Arquiteto |
| [`02-design-tokens-pptx.md`](./02-design-tokens-pptx.md) | Formato DTCG, mapeamento de tokens para Google Slides/PPTX, slide master | Designer / Eng de plataforma |
| [`03-mcp-google-drive-slides.md`](./03-mcp-google-drive-slides.md) | Servidores MCP disponíveis (oficiais e open source) para Drive e Slides | Eng de plataforma |
| [`04-wizard-guiado.md`](./04-wizard-guiado.md) | Padrão de wizard conversacional, skills de slides, fluxo ponta a ponta | Eng de software |
| [`05-construir-servidor-mcp.md`](./05-construir-servidor-mcp.md) | Build do servidor MCP interno (FastMCP), integração Drive API + Slides API | Eng de software |
| [`06-roadmap-adocao.md`](./06-roadmap-adocao.md) | Fases 0–3 de rollout, métricas de sucesso, integrações futuras (RAG + Caso 3) | PMO / Tech Lead |

## Viabilidade técnica — diagnóstico rápido

**Verde** (bloqueadores resolvidos, stack matura):
- Servidor MCP oficial do Google Workspace (Drive + Slides) anunciado em 2026, em GA.
- `google-slides-mcp` (community, open source): 5 tools prontas (create, get, batch_update, get_page, summarize).
- W3C DTCG design tokens: spec estável out/2025, adotada por Adobe, Google, Microsoft, Figma, Tokens Studio.
- Google Slides API: batch update, copy from template via Drive API, placeholder replacement — documentado e estável.
- `python-pptx`: de facto para geração .pptx; suporta slide master, layouts, placeholders, temas.

**Amarelo** (resolvível, requer decisão):
- **OAuth 2.0** para o servidor MCP acessar o Drive: requer app Google Cloud registrada + consentimento. Padrão, mas exige setup inicial.
- **Escopo de permissões**: servidor MCP com acesso à pasta de brand assets somente (não ao Drive inteiro). Requer service account ou OAuth com escopo restrito.
- **Google Slides vs .pptx**: Google Slides nativo tem API mais rica para manipulação; .pptx é universalmente editável. Pode-se oferecer os dois (exportar via Drive API).

**Vermelho** (limitação real):
- O servidor MCP PowerPoint COM (Windows-only, precisa do app instalado) **não é adequado** para uso corporativo server-side. A rota correta é Google Slides API + python-pptx para .pptx local.
- Google Slides API **não cria apresentações com conteúdo em um único request** — o fluxo correto é: copiar template via Drive API → preencher placeholders via batchUpdate. Necessário entender esse padrão.

## Decisões executivas que esta Etapa pede

1. **Definir a pasta do Drive como "fonte de verdade"**: quem controla os templates e tokens, com qual ciclo de atualização. Proposta: time de Design ou Comunicação como owner; Eng de Plataforma como mantenedor técnico.
2. **Escolher o escopo de output**: apenas Google Slides (nativo no Workspace), ou também .pptx para PowerPoint? Ambos são viáveis; .pptx exige python-pptx no servidor MCP. Recomendação: Google Slides primário + botão "baixar como .pptx".
3. **Integrar com RAG corporativo (Caso 3)**: o agente pode, durante o wizard, buscar conteúdo relevante na base de conhecimento. Depende de a Etapa 6 (servidor MCP RAG) estar implantada.
4. **Nível de autonomia do agente**: (a) wizard full-guiado — agente pergunta tudo antes de gerar; (b) geração especulativa — agente gera um draft e usuário revisa. Recomendação: começar com (a), evoluir para (b) após feedback.

## Onde se conecta com o resto da proposta

- **Caso 3 (RAG corporativo + Etapa 6)** → agente pode buscar dados reais (relatórios, políticas, números) para popular os slides. Elimina o "copiar tabela do sistema para o slide".
- **Caso 6 (Sumarização)** → entrada de um relatório PDF → sumarização → slides. Pipeline totalmente automático.
- **Etapa 6 (MCP)** → o servidor MCP de apresentações é mais um servidor no ecossistema MCP da empresa; reutiliza OAuth, gateway, observabilidade e patterns já definidos.

## Próxima leitura sugerida

Para entender a arquitetura completa: [`01-arquitetura-e-fundamentos.md`](./01-arquitetura-e-fundamentos.md). Para ver como os tokens mapeiam para slides: [`02-design-tokens-pptx.md`](./02-design-tokens-pptx.md). Para o plano de implementação: [`05-construir-servidor-mcp.md`](./05-construir-servidor-mcp.md).
