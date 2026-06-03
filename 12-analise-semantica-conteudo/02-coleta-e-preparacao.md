# Coleta, ética/LGPD e preparação dos textos

> Antes de qualquer código, três coisas: (1) decidir **de onde** vêm os textos do público e os seus; (2) acertar **ética e LGPD** — inegociável no seu setor; (3) **limpar e preparar** o texto em português. Este documento trata as três, nessa ordem, porque a ordem importa: coletar errado gera risco jurídico, e texto sujo gera embedding sujo.

## Parte 1 — A ética e a LGPD vêm primeiro (não é rodapé)

Você é uma **gestora de patrimônio para clientes ultra ricos**, regulada (CVM) e lidando com dado sensível. Analisar "publicações de leads" é **tratamento de dados pessoais**. Isso não inviabiliza o projeto — mas define *como* fazer.

### Os princípios que mantêm o projeto seguro

| Princípio LGPD | O que significa na prática aqui |
|----------------|----------------------------------|
| **Finalidade** | Defina e registre o porquê: "entender temas de interesse do público para alinhar a pauta de conteúdo" — agregado, não vigilância individual |
| **Minimização** | Colete só o texto necessário ao tema. Não puxe dado financeiro, localização, rede de contatos |
| **Base legal** | Conteúdo público tem nuances; defina a base (legítimo interesse vs. consentimento) **com o jurídico/DPO** antes de coletar |
| **Anonimização/agregação** | **A regra de ouro:** analise *padrões do público*, não *perfis de pessoas*. Remova nomes, @s, e qualquer identificador antes de processar |
| **Transparência e ToS** | Respeite os Termos de Serviço da plataforma. Raspagem que viola ToS é risco jurídico e reputacional — gravíssimo no seu setor |

> **A linha que não se cruza:** *"Fulano (lead na conta X) postou sobre Y, então vamos abordá-lo sobre Y"* é criação de perfil individual invasivo — risco reputacional e de compliance enorme para uma gestora UHNW. *"O nosso público-alvo, no agregado, demonstra forte interesse em sucessão internacional"* é legítimo e seguro. **Trabalhe sempre no segundo modo.**

### Recomendação prática
- Faça a coleta e a anonimização **antes** de qualquer análise; trabalhe com um corpus já sem PII.
- Se houver qualquer dúvida, **valide com o DPO/jurídico** — registre o aval. Este projeto não vale um incidente de privacidade.
- Prefira **fontes de baixo risco**: seu próprio CRM/RD (dados que o lead já consentiu em compartilhar com você), pesquisas, formulários, e conteúdo agregado de mercado.

---

## Parte 2 — De onde vêm os textos

Você precisa de **dois corpora** (conjuntos de textos): o do **público** e o **seu**.

### Corpus A — Interesse do público
Em ordem de preferência (do mais seguro/útil ao mais sensível):

| Fonte | O que extrair | Risco/Nota |
|-------|---------------|------------|
| **Seu CRM + RD** | Campos de texto que o lead já te deu: motivo do contato, respostas a formulários, assuntos de e-mail, anotações de SDR sobre dores citadas | **Melhor fonte.** Dado consentido, já no seu perímetro. Comece por aqui |
| **Perguntas em webinars/eventos** | Perguntas que o público faz ao vivo ou em Q&A | Alto sinal de interesse real, baixo risco |
| **Buscas e termos** (Search Console, RD) | O que as pessoas buscaram para chegar até você | Agregado por natureza, seguro |
| **Comentários/posts públicos em suas redes** | Comentários nas suas publicações | Público, mas anonimize; respeite ToS |
| **Conteúdo público de mercado** (notícias, fóruns de investidor) | Temas em alta no universo UHNW | Use agregado; cuidado com ToS de raspagem |

> **Insight:** você provavelmente já tem ouro no CRM/RD — anotações de SDR sobre "o que o lead disse que queria". Isso é interesse declarado, consentido e no seu perímetro. **Comece o projeto por aí**, não por raspagem de rede social.

### Corpus B — O seu conteúdo
Mais simples, é seu: posts de redes, artigos do blog/newsletter, roteiros, descrições de campanha (RD), páginas do site. Exporte texto + data + canal + (se tiver) métrica de engajamento — a métrica permite, depois, cruzar *alinhamento × performance*.

---

## Parte 3 — Preparação do texto (em português)

Texto bruto não entra direto no modelo. O grau de limpeza **depende do degrau** (ver [`01`](./01-escada-de-tecnicas.md)):

> **Regra que confunde muita gente:** nuvem de palavras/keyness (degrau 1) **precisa** de limpeza pesada (remover stopwords, normalizar). Embeddings (degrau 2+) **quase não precisam** — o modelo entende contexto e você pode até atrapalhar removendo palavras. Não limpe demais para embeddings.

### Pipeline de limpeza por degrau

| Passo | Degrau 1 (palavras) | Degrau 2+ (embeddings) |
|-------|---------------------|------------------------|
| Remover URLs, @menções, emojis soltos | Sim | Sim (menos crítico) |
| **Anonimizar** (tirar nomes/PII) | **Sempre** | **Sempre** |
| Minúsculas | Sim | Não precisa |
| Remover stopwords PT ("de", "para", "que"…) | Sim | **Não** (atrapalha) |
| Lematizar/stemizar ("investindo"→"investir") | Opcional | **Não** |
| Remover pontuação | Sim | Não |
| Deduplicar posts idênticos/quase | Sim | Sim |
| Filtrar muito curtos (< ~5 palavras) | Sim | Sim (pouco sinal) |

### Ferramentas PT-BR
- **spaCy** (`pt_core_news_lg`) — tokenização, lematização, NER (útil para *detectar* nomes a anonimizar).
- **NLTK** — listas de stopwords PT.
- **Presidio** (Microsoft) — detecção/anonimização de PII, já citado na [`02-tecnologias/07-guardrails-seguranca.md`](../02-tecnologias/07-guardrails-seguranca.md). Ideal para a etapa de anonimização.

### Particularidades do português que afetam o resultado
- **Stopwords PT** são diferentes do inglês — use lista PT, senão "não", "sem" (que invertem sentido!) podem sumir indevidamente. Para análise de tema, ok remover; para sentimento, cuidado.
- **Acentuação e variação:** "análise"/"analise", caixa, abreviações. Normalize para o degrau 1.
- **Domínio financeiro:** jargão ("alocação", "renda fixa", "private", "offshore", "holding") — considere um dicionário de termos do setor para não tratar como ruído.

---

## Saída desta etapa

Ao final, você tem dois arquivos limpos e anonimizados, prontos para o código do [`03`](./03-metodos-e-codigo.md):

```
corpus_publico.csv   →  colunas: id_anon, texto_limpo, data, fonte
corpus_nosso.csv     →  colunas: id, texto_limpo, data, canal, engajamento (opcional)
```

> **Checklist antes de seguir:**
> - [ ] Finalidade e base legal definidas com DPO/jurídico
> - [ ] PII removida (rodou Presidio/NER, conferiu amostra)
> - [ ] Respeito aos ToS das fontes verificado
> - [ ] Dois corpora montados, deduplicados, sem textos minúsculos
> - [ ] Versão "limpa pesada" (degrau 1) e versão "leve" (degrau 2+) preparadas

Próximo: os **métodos e o código** ([`03`](./03-metodos-e-codigo.md)).
