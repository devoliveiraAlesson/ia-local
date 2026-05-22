# Design Tokens para Apresentações — Formato, Estrutura e Mapeamento

> Como definir, versionar e aplicar design tokens (formato W3C DTCG 2025.10) em Google Slides e .pptx. Referência para o designer e engenheiro de plataforma que vai manter o sistema de identidade visual.

## Por que design tokens para slides

Apresentações têm os mesmos problemas de inconsistência que sistemas de UI: cada pessoa que abre o template aplica as cores e fontes "por memória", e o resultado diverge. Design tokens resolvem isso da mesma forma que resolvem em código front-end: **a decisão de design fica num arquivo, não na cabeça das pessoas**.

Com tokens em um arquivo `tokens.json`:
- O servidor MCP **sempre** usa os valores corretos, independente de quem pediu o deck.
- Atualizar a marca exige mudar **um arquivo**; todos os decks gerados depois são atualizados.
- O arquivo pode ser versionado em git ou no Google Drive com histórico.
- Times de design e engenharia falam a mesma língua (Adobe, Figma, Google, Microsoft e Tokens Studio adotaram o mesmo formato DTCG).

## Formato W3C DTCG (Design Tokens Community Group)

A especificação DTCG 2025.10 (primeira versão estável, lançada em outubro de 2025) usa JSON com prefixo `$` nas propriedades de token. Exemplo mínimo:

```json
{
  "color": {
    "primary": {
      "$type": "color",
      "$value": "#1A237E",
      "$description": "Cor primária da marca — azul escuro"
    },
    "accent": {
      "$type": "color",
      "$value": "#FF6F00"
    }
  },
  "typography": {
    "display": {
      "$type": "fontFamily",
      "$value": "Inter"
    },
    "body": {
      "$type": "fontFamily",
      "$value": "Inter"
    },
    "size": {
      "title": { "$type": "dimension", "$value": "36px" },
      "subtitle": { "$type": "dimension", "$value": "24px" },
      "body": { "$type": "dimension", "$value": "18px" },
      "caption": { "$type": "dimension", "$value": "12px" }
    }
  }
}
```

O arquivo completo para apresentações corporativas é detalhado na seção abaixo.

## Estrutura completa de tokens para apresentações

```json
{
  "$schema": "https://www.designtokens.org/tr/drafts/format/",
  "$version": "1.0.0",
  "$description": "Design tokens corporativos — apresentações Google Slides / PPTX",

  "color": {
    "brand": {
      "primary":     { "$type": "color", "$value": "#1A237E" },
      "secondary":   { "$type": "color", "$value": "#283593" },
      "accent":      { "$type": "color", "$value": "#FF6F00" },
      "accent-light":{ "$type": "color", "$value": "#FFE0B2" }
    },
    "neutral": {
      "white":       { "$type": "color", "$value": "#FFFFFF" },
      "light":       { "$type": "color", "$value": "#F5F5F5" },
      "mid":         { "$type": "color", "$value": "#9E9E9E" },
      "dark":        { "$type": "color", "$value": "#212121" }
    },
    "slide": {
      "title-bg":    { "$type": "color", "$value": "{color.brand.primary}" },
      "section-bg":  { "$type": "color", "$value": "{color.brand.secondary}" },
      "content-bg":  { "$type": "color", "$value": "{color.neutral.white}" },
      "text-on-dark":{ "$type": "color", "$value": "{color.neutral.white}" },
      "text-on-light":{ "$type": "color", "$value": "{color.neutral.dark}" }
    }
  },

  "typography": {
    "family": {
      "display":     { "$type": "fontFamily", "$value": ["Inter", "Arial", "sans-serif"] },
      "body":        { "$type": "fontFamily", "$value": ["Inter", "Arial", "sans-serif"] }
    },
    "size": {
      "display":     { "$type": "dimension", "$value": "40pt" },
      "title":       { "$type": "dimension", "$value": "32pt" },
      "subtitle":    { "$type": "dimension", "$value": "24pt" },
      "body-lg":     { "$type": "dimension", "$value": "20pt" },
      "body":        { "$type": "dimension", "$value": "18pt" },
      "body-sm":     { "$type": "dimension", "$value": "14pt" },
      "caption":     { "$type": "dimension", "$value": "11pt" }
    },
    "weight": {
      "regular":     { "$type": "fontWeight", "$value": 400 },
      "medium":      { "$type": "fontWeight", "$value": 500 },
      "semibold":    { "$type": "fontWeight", "$value": 600 },
      "bold":        { "$type": "fontWeight", "$value": 700 }
    },
    "lineHeight": {
      "tight":       { "$type": "number", "$value": 1.2 },
      "normal":      { "$type": "number", "$value": 1.5 },
      "loose":       { "$type": "number", "$value": 1.8 }
    }
  },

  "spacing": {
    "slide-margin-horizontal": { "$type": "dimension", "$value": "72pt" },
    "slide-margin-vertical":   { "$type": "dimension", "$value": "54pt" },
    "element-gap":             { "$type": "dimension", "$value": "16pt" },
    "section-gap":             { "$type": "dimension", "$value": "32pt" }
  },

  "asset": {
    "logo-primary":  { "$type": "string", "$value": "logos/logo-primary.png" },
    "logo-white":    { "$type": "string", "$value": "logos/logo-white.png" },
    "logo-dark":     { "$type": "string", "$value": "logos/logo-dark.png" }
  },

  "theme": {
    "default": {
      "$description": "Tema padrão — cores completas da marca",
      "slide-bg":    { "$type": "color", "$value": "{color.neutral.white}" },
      "title-color": { "$type": "color", "$value": "{color.brand.primary}" },
      "body-color":  { "$type": "color", "$value": "{color.neutral.dark}" },
      "accent":      { "$type": "color", "$value": "{color.brand.accent}" }
    },
    "dark": {
      "$description": "Tema escuro — fundo primário, texto branco",
      "slide-bg":    { "$type": "color", "$value": "{color.brand.primary}" },
      "title-color": { "$type": "color", "$value": "{color.neutral.white}" },
      "body-color":  { "$type": "color", "$value": "{color.neutral.light}" },
      "accent":      { "$type": "color", "$value": "{color.brand.accent}" }
    },
    "clean": {
      "$description": "Tema limpo — fundo branco, texto escuro, acentos mínimos",
      "slide-bg":    { "$type": "color", "$value": "{color.neutral.white}" },
      "title-color": { "$type": "color", "$value": "{color.neutral.dark}" },
      "body-color":  { "$type": "color", "$value": "{color.neutral.dark}" },
      "accent":      { "$type": "color", "$value": "{color.brand.secondary}" }
    },
    "bold": {
      "$description": "Tema bold — cor de acento forte, alto contraste",
      "slide-bg":    { "$type": "color", "$value": "{color.brand.accent}" },
      "title-color": { "$type": "color", "$value": "{color.neutral.dark}" },
      "body-color":  { "$type": "color", "$value": "{color.neutral.dark}" },
      "accent":      { "$type": "color", "$value": "{color.brand.primary}" }
    }
  }
}
```

### Referências entre tokens

A notação `{color.brand.primary}` é alias — o DTCG resolve na hora de usar. O servidor MCP resolve os aliases antes de passar os valores para a Slides API.

## Mapeamento de tokens → propriedades Google Slides

A Slides API usa unidades EMU (English Metric Units): `1pt = 12700 EMU`. O servidor MCP converte automaticamente.

| Token | Propriedade Slides API | Onde se aplica |
|---|---|---|
| `color.slide.title-bg` | `pageBackgroundFill.solidFill.color` | Slide de capa e seção |
| `color.slide.content-bg` | `pageBackgroundFill.solidFill.color` | Slides de conteúdo |
| `theme.<variante>.title-color` | `textStyle.foregroundColor` | Títulos |
| `theme.<variante>.body-color` | `textStyle.foregroundColor` | Corpo de texto |
| `typography.family.display` | `textStyle.fontFamily` | Títulos |
| `typography.family.body` | `textStyle.fontFamily` | Corpo |
| `typography.size.title` | `textStyle.fontSize.magnitude` (unit: PT) | Títulos |
| `typography.size.body` | `textStyle.fontSize.magnitude` (unit: PT) | Corpo |
| `typography.weight.bold` | `textStyle.bold: true` | Destaques |
| `spacing.slide-margin-horizontal` | `placeholder.transform.translateX` | Posição dos placeholders |

## Mapeamento de tokens → python-pptx (export .pptx)

Para geração de .pptx, o servidor MCP usa `python-pptx` com o mapeamento:

```python
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor

def apply_tokens_to_slide(slide, tokens, theme_variant="default"):
    theme = tokens["theme"][theme_variant]
    typography = tokens["typography"]

    # Background
    bg_hex = resolve_alias(tokens, theme["slide-bg"]["$value"])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(bg_hex.lstrip("#"))

    # Title placeholder
    title_ph = slide.placeholders[0]
    title_ph.text_frame.paragraphs[0].runs[0].font.size = Pt(
        int(typography["size"]["title"]["$value"].replace("pt", ""))
    )
    title_color_hex = resolve_alias(tokens, theme["title-color"]["$value"])
    title_ph.text_frame.paragraphs[0].runs[0].font.color.rgb = RGBColor.from_string(
        title_color_hex.lstrip("#")
    )
```

A função `resolve_alias()` percorre referências `{a.b.c}` recursivamente até encontrar o valor literal.

## Slide Master vs aplicação por slide

### Abordagem 1: Slide Master (recomendada para templates novos)

Configurar o Slide Master do template com os tokens diretamente:
- Muito eficiente: todos os slides herdam automaticamente.
- Menos chamadas de API.
- O designer pode abrir o template e ver visualmente os estilos.
- Exige que o template seja criado/atualizado programaticamente quando os tokens mudam.

### Abordagem 2: Aplicação por slide (via batchUpdate)

Aplicar tokens via batchUpdate em cada slide gerado:
- Mais flexível: slides podem ter variantes diferentes.
- Mais chamadas de API, mas batchUpdate agrupa tudo em uma requisição.
- Não requer manter o Slide Master atualizado no Drive.

**Recomendação**: Slide Master para o template base (rodado pelo time de Design ao atualizar tokens); aplicação por slide via batchUpdate para variações de tema e conteúdo dinâmico.

## Script de atualização do template

Quando o `tokens.json` muda, rodar o script para atualizar o Slide Master de cada template no Drive:

```python
from googleapiclient.discovery import build
import json

def update_slide_master_from_tokens(presentation_id, tokens_path, theme="default"):
    with open(tokens_path) as f:
        tokens = json.load(f)
    
    slides_service = build("slides", "v1", credentials=creds)
    
    # Obtém o ID do Slide Master
    pres = slides_service.presentations().get(presentationId=presentation_id).execute()
    master_id = pres["masters"][0]["objectId"]
    
    theme_tokens = tokens["theme"][theme]
    primary_color = resolve_alias(tokens, theme_tokens["slide-bg"]["$value"])
    title_color = resolve_alias(tokens, theme_tokens["title-color"]["$value"])
    body_size = tokens["typography"]["size"]["body"]["$value"].replace("pt", "")
    
    requests = [
        # Atualiza fundo do master
        {
            "updatePageProperties": {
                "objectId": master_id,
                "pageProperties": {
                    "pageBackgroundFill": {
                        "solidFill": {"color": {"rgbColor": hex_to_rgb(primary_color)}}
                    }
                },
                "fields": "pageBackgroundFill"
            }
        }
        # ... mais updates de tipografia ...
    ]
    
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()
```

## Versionamento dos tokens

Manter `tokens.json` com campo de versão semântica (`$version`). O servidor MCP loga qual versão de token foi usada em cada geração (no Langfuse/audit trail). Isso permite:

- Reproduzir um deck exatamente como foi gerado.
- Fazer rollback visual se uma atualização de tokens quebrar algo.
- Comunicar mudanças de marca com changelog claro.

Fluxo de atualização:
1. Designer atualiza `tokens.json` no Drive (ou via PR no git).
2. Incrementa `$version`.
3. Script de CI/CD chama `update_slide_master_from_tokens()` para cada template.
4. Servidor MCP pega nova versão automaticamente (sem restart necessário se ler sob demanda).

## Referências

- W3C DTCG Specification 2025.10: <https://www.designtokens.org/tr/drafts/format/>
- W3C Design Tokens Community Group: <https://www.w3.org/community/design-tokens/>
- Tokens Studio (Figma plugin, W3C DTCG compatível): <https://docs.tokens.studio/manage-settings/token-format>
- Google Slides API — textStyle: <https://developers.google.com/slides/api/reference/rest/v1/presentations.pages/types#TextStyle>
- python-pptx — Slide Masters: <https://python-pptx.readthedocs.io/en/latest/dev/analysis/sld-layout.html>
- Brand token system com python-pptx (2025): <https://skywork.ai/blog/how-to-keep-ai-ppt-on-brand-colors-fonts-templates-guide/>
