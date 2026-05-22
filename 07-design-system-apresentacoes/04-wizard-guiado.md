# Wizard Guiado — Fluxo de Construção Conversacional de Apresentações

> Como implementar o wizard que guia o usuário desde "quero um deck" até o link do arquivo pronto no Drive. Cobre o padrão conversacional, skills de slides, estrutura do outline JSON e integração com o servidor MCP.

## O problema que o wizard resolve

Gerar uma apresentação de qualidade exige informações que o agente não tem de início:

- Quem vai ver? (audiência define tom, densidade de conteúdo, jargão)
- Qual o objetivo? (convencer, informar, treinar, reportar)
- Quantas seções e quais mensagens por seção?
- Tem dados, números, gráficos?
- Qual template usar?
- Qual variante de tema (default, dark, clean, bold)?

Sem o wizard, o agente tenta adivinhar ou pede tudo de uma vez em um prompt longo — a experiência fica ruim. O wizard quebra a coleta em turnos naturais, como uma conversa com um designer experiente.

## Arquitetura do wizard

O wizard pode ser implementado como:

1. **Claude Skill** (Anthropic Agent SDK) — recomendado para uso com Claude Code. O skill é um prompt estruturado que instrui o agente a seguir o roteiro de perguntas antes de chamar qualquer tool de geração.
2. **MCP Prompt** (primitiva nativa do protocolo) — o servidor MCP expõe o roteiro como um `Prompt` parametrizável. Clientes que suportam prompts MCP (Claude Desktop, Claude Code) o apresentam como slash command.
3. **Tool `wizard_start` com estado** — o servidor MCP retorna as perguntas em etapas, mantendo estado via `session_id` entre chamadas.

**Recomendação**: implementar como Tool com estado (`wizard_start` + `wizard_answer` + `wizard_confirm`) para compatibilidade com qualquer cliente MCP. Paralelamente, empacotar como Claude Skill para UX melhorada no Claude Code.

## Roteiro do wizard — 5 etapas

### Etapa 1 — Objetivo e contexto

```
Agente: Oi! Vou te ajudar a criar o deck. Antes de começar, me conta:

  Qual é o objetivo principal desta apresentação?
  
  (a) Proposta comercial / oferta para cliente
  (b) Report executivo / update de resultados
  (c) Treinamento interno / onboarding
  (d) Pitch de produto ou ideia
  (e) Apresentação de projeto / briefing
  (f) Outro: [descreva]
  
  (pode digitar a letra ou descrever livremente)
```

### Etapa 2 — Audiência e tom

```
Agente: Entendido. E quem vai ver esta apresentação?

  Por exemplo: "diretores da empresa", "time técnico de 5 pessoas",
  "cliente corporativo — CEO e CFO", "turma de novos funcionários".

  → [resposta livre]

  Alguma instrução especial de tom? 
  (ex: formal, descontraído, técnico, executivo — sem jargão)
  → [resposta livre ou "sem restrição"]
```

### Etapa 3 — Estrutura e conteúdo

```
Agente: Ótimo. Agora me ajuda a montar a estrutura:

  1. Qual o título ou tema central do deck?
     → [resposta livre]

  2. Quais são os 3–6 pontos ou seções principais que você quer cobrir?
     (pode ser uma lista, não precisa estar perfeito ainda)
     → [resposta livre]

  3. Tem dados específicos para incluir (números, tabelas, gráficos)?
     → [resposta livre ou "não"]

  4. Tem imagens ou exemplos visuais que quer colocar?
     → [resposta livre ou "não"]
```

### Etapa 4 — Template e visual

```
Agente: Perfeito. Vou buscar os templates disponíveis...

  [chama drive.list_files na pasta /templates]

  Templates disponíveis:
  (a) Corporativo — deck de proposta/relatório, layout sóbrio
  (b) Pitch — deck de pitch, visual moderno, menos texto
  (c) Treinamento — slides para ensinar, espaço para exemplos
  (d) Executivo — boardroom, pouquíssimo texto, muito visual

  Qual combina mais com o seu objetivo?
  → [resposta]

  E o tema de cores?
  (a) Default — cores da marca, completo
  (b) Clean — fundo branco, mínimo
  (c) Dark — fundo escuro, impactante
  (d) Bold — cores fortes, alto contraste
  → [resposta]
```

### Etapa 5 — Confirmação do outline

O agente monta o **outline JSON** com base nas respostas e apresenta para confirmação antes de gerar:

```
Agente: Aqui está o plano do seu deck:

  📋 Título: "Proposta de Parceria — Empresa ABC"
  👥 Audiência: Diretores comerciais
  🎨 Template: Corporativo | Tema: Default
  📑 Slides planejados:

  1. [Capa] Proposta de Parceria — Empresa ABC | João Silva | Maio 2026
  2. [Agenda] O que vamos cobrir hoje
  3. [Conteúdo] Contexto: por que esta parceria
  4. [Dados] Resultados esperados (gráfico + tabela)
  5. [Conteúdo] Nossa proposta de valor
  6. [Conteúdo] Próximos passos
  7. [Fechamento] Obrigado | Contato

  Isso parece certo? Quer ajustar alguma coisa antes de eu gerar?
  → [ok / ajustes livres]
```

Após confirmação, o servidor MCP gera a apresentação.

## Estrutura do outline JSON

O wizard produz um JSON que alimenta o servidor de geração:

```json
{
  "session_id": "wiz-2026-abc123",
  "meta": {
    "title": "Proposta de Parceria — Empresa ABC",
    "author": "João Silva",
    "date": "Maio 2026",
    "audience": "Diretores comerciais",
    "tone": "formal",
    "objective": "proposta_comercial"
  },
  "design": {
    "template": "template-corporativo",
    "theme": "default"
  },
  "slides": [
    {
      "index": 1,
      "skill": "TitleSlide",
      "content": {
        "title": "Proposta de Parceria",
        "subtitle": "Empresa ABC",
        "author": "João Silva",
        "date": "Maio 2026"
      }
    },
    {
      "index": 2,
      "skill": "AgendaSlide",
      "content": {
        "title": "O que vamos cobrir hoje",
        "items": [
          "Contexto: por que esta parceria",
          "Resultados esperados",
          "Nossa proposta de valor",
          "Próximos passos"
        ]
      }
    },
    {
      "index": 3,
      "skill": "ContentSlide",
      "content": {
        "title": "Contexto: por que esta parceria",
        "body": "{{aguardando conteúdo do usuário ou RAG}}",
        "bullet_points": []
      }
    },
    {
      "index": 4,
      "skill": "DataSlide",
      "content": {
        "title": "Resultados esperados",
        "data_description": "{{aguardando dados do usuário}}",
        "footnote": ""
      }
    },
    {
      "index": 7,
      "skill": "ClosingSlide",
      "content": {
        "title": "Obrigado",
        "contact": "joao.silva@empresa.com"
      }
    }
  ]
}
```

## Skills de slides — catálogo

Cada skill sabe como montar um tipo de slide usando os tokens e a Slides API.

### TitleSlide

```python
def skill_title_slide(content: dict, tokens: dict, theme: str) -> list[dict]:
    """Slide de capa: título grande, subtítulo, autor, data, logo."""
    bg_color = resolve_token(tokens, f"theme.{theme}.slide-bg")
    title_color = resolve_token(tokens, f"theme.{theme}.title-color")
    
    return [
        update_background(slide_id, bg_color),
        insert_text(title_ph_id, content["title"], size=40, color=title_color, bold=True),
        insert_text(subtitle_ph_id, content["subtitle"], size=24, color=title_color),
        insert_text(author_ph_id, content["author"], size=14),
        insert_text(date_ph_id, content["date"], size=14),
        insert_logo(logo_url=get_logo_url(tokens, theme), position="bottom-right"),
    ]
```

### AgendaSlide

```python
def skill_agenda_slide(content: dict, tokens: dict, theme: str) -> list[dict]:
    """Slide de agenda com bullets numerados e linha de acento."""
    requests = [
        insert_text(title_ph_id, content["title"], size=32, bold=True),
        insert_accent_line(color=resolve_token(tokens, f"theme.{theme}.accent")),
    ]
    for i, item in enumerate(content["items"], 1):
        requests.append(insert_bullet(body_ph_id, f"{i}. {item}", size=20))
    return requests
```

### DataSlide

```python
def skill_data_slide(content: dict, tokens: dict, theme: str) -> list[dict]:
    """Slide com dado de destaque: número grande + descrição + footnote."""
    return [
        insert_text(title_ph_id, content["title"], size=28, bold=True),
        insert_big_number(content.get("highlight_number", ""), size=64,
                          color=resolve_token(tokens, f"theme.{theme}.accent")),
        insert_text(body_ph_id, content.get("description", ""), size=18),
        insert_text(footnote_ph_id, content.get("footnote", ""), size=11),
    ]
```

### QuoteSlide

```python
def skill_quote_slide(content: dict, tokens: dict, theme: str) -> list[dict]:
    """Slide de citação com aspas grandes e fundo de destaque."""
    return [
        update_background(slide_id, resolve_token(tokens, f"theme.{theme}.slide-bg")),
        insert_quote_marks(size=80, color=resolve_token(tokens, f"theme.{theme}.accent")),
        insert_text(quote_ph_id, f'"{content["quote"]}"', size=24, italic=True),
        insert_text(author_ph_id, f"— {content['author']}", size=16),
    ]
```

### SectionDivider

```python
def skill_section_divider(content: dict, tokens: dict, theme: str) -> list[dict]:
    """Slide de transição entre seções: fundo de acento, texto grande centralizado."""
    section_bg = resolve_token(tokens, "color.slide.section-bg")
    text_color = resolve_token(tokens, "color.slide.text-on-dark")
    return [
        update_background(slide_id, section_bg),
        insert_text(title_ph_id, content["section_title"], size=36, color=text_color, bold=True, align="center"),
    ]
```

### ClosingSlide

```python
def skill_closing_slide(content: dict, tokens: dict, theme: str) -> list[dict]:
    """Slide de fechamento com logo central, obrigado e contato."""
    return [
        update_background(slide_id, resolve_token(tokens, f"theme.{theme}.slide-bg")),
        insert_logo(logo_url=get_logo_url(tokens, theme), position="center", size="large"),
        insert_text(title_ph_id, content.get("title", "Obrigado"), size=40, bold=True),
        insert_text(contact_ph_id, content.get("contact", ""), size=16),
    ]
```

## Integração com RAG Corporativo

Quando o Caso 3 (RAG corporativo, Etapa 6) estiver disponível, o wizard pode enriquecer o conteúdo automaticamente:

```python
async def enrich_slide_content(slide: dict, rag_client) -> dict:
    """Busca conteúdo relevante no RAG corporativo para preencher slides."""
    if slide["skill"] in ["ContentSlide", "DataSlide"] and "{{aguardando" in str(slide["content"]):
        query = f"{slide['content']['title']} {meta['objective']} {meta['audience']}"
        rag_result = await rag_client.search(query=query, top_k=3)
        
        if rag_result["chunks"]:
            best_chunk = rag_result["chunks"][0]
            slide["content"]["body"] = best_chunk["text"]
            slide["content"]["source"] = best_chunk["uri"]
            slide["content"]["rag_enriched"] = True
    
    return slide
```

O agente apresenta o conteúdo encontrado ao usuário antes de inserir: "Encontrei este texto relevante na base de conhecimento — quer usar como ponto de partida para o slide 3?"

## Exemplo de conversa completa (do pedido ao link)

```
Usuário: quero criar uma apresentação pra propor nosso produto pra um cliente novo

Agente: Oi! Vou te ajudar a criar o deck. Qual é o objetivo principal?
        (a) Proposta comercial / oferta para cliente ← esse parece!
        (b) Report executivo...

Usuário: a, proposta comercial

Agente: Quem vai ver esta apresentação?

Usuário: é o CEO e o CTO de uma startup de logística, eles são técnicos mas precisam da visão de negócio também

Agente: Entendido — tom formal-técnico. Qual o título e os pontos principais?

Usuário: título é "Como Nossa Plataforma Resolve Rastreamento em Tempo Real"
         pontos: problema atual deles, como funciona nossa solução, casos de uso, 
         diferenciais, próximos passos e preço

Agente: [lista templates] Qual combina mais?

Usuário: pitch

Agente: Tema de cores?

Usuário: dark, quero algo impactante

Agente: Aqui está o plano do seu deck:
        📋 "Como Nossa Plataforma Resolve Rastreamento em Tempo Real"
        👥 CEO + CTO startup logística | Tom: formal-técnico
        🎨 Template: Pitch | Tema: Dark
        📑 8 slides: Capa → Problema → Solução → Como funciona → 
           Casos de uso → Diferenciais → Preço → Próximos passos
        Posso começar?

Usuário: vai!

Agente: [copia template, aplica tokens dark, preenche slides via batchUpdate]
        ✅ Deck pronto! Aqui está o link: https://docs.google.com/presentation/d/...
        Compartilhado com você no Drive. Quer ajustar algum slide?
```

Tempo total da conversa: ~5–8 minutos. Tempo de geração pelo servidor: ~30–60 segundos.

## Tratamento de edge cases

| Situação | Comportamento do wizard |
|---|---|
| Usuário quer um deck "rápido" sem responder tudo | Agente usa defaults: template corporativo, tema default, estrutura padrão para o objetivo inferido |
| Usuário cola um texto longo (relatório, briefing) | Agente extrai pontos chave automaticamente e mapeia para slides antes de confirmar |
| Usuário pede para "atualizar o deck da semana passada" | Agente pede o link do Drive, lê via `slides.get`, mostra o que vai mudar e pede confirmação |
| Usuário quer slides de dados mas não tem os números ainda | Agente cria `{{placeholder_dado}}` no slide e avisa para preencher depois |
| Usuário menciona um relatório interno | Agente chama RAG (se disponível) para buscar o documento e extrair dados relevantes |

## Referências

- Anthropic Agent SDK (Skill framework): <https://docs.anthropic.com/en/docs/claude-code/sdk>
- MCP Prompts primitive: <https://modelcontextprotocol.io/docs/concepts/prompts>
- MCP UI Framework (Anthropic, jan/2026): <https://www.cometapi.com/claude-skills-vs-mcp-the-2026-guide-to-agentic-architecture/>
- PPTAgent (referência de pipeline agentic de slides): <https://github.com/icip-cas/PPTAgent>
- Claude Skills para PowerPoint (step-by-step): <https://sider.ai/blog/ai-tools/step-by-step-claude-skills-that-build-branded-powerpoints-so-you-don-t-at-2-a_m>
