# Etapa 12 — Análise semântica: o que o público quer × o que publicamos

> Você perguntou (parafraseando): *"como meço a diferença entre assuntos e conteúdos? Nuvem de palavras para identificar assuntos, vetores para entender cosseno, um resumo estruturado… A ideia é analisar as publicações dos leads para entender o interesse deles e comparar com as nossas publicações — e não tenho noção de como fazer isso com ciência de dados, IA ou scripts."* Esta etapa responde exatamente isso, do conceito ao código, recortada para a sua gestora UHNW. Junho/2026.

## A pergunta de negócio, traduzida

Por trás do seu pedido há uma pergunta de RevOps/marketing muito específica e muito valiosa:

> **"O que publicamos está alinhado com o que o nosso público (de fato) se interessa? Onde estão os gaps — assuntos que eles querem e nós ignoramos, e assuntos que martelamos e ninguém liga?"**

Isso conecta-se diretamente ao gargalo nº 3 do seu diagnóstico ([`11-revops-aplicado/02`](../11-revops-aplicado/02-diagnostico-maturidade-e-gaps.md)): saber se o marketing fala a língua do público certo. E é a versão "de conteúdo" da pergunta de atribuição da [Etapa 9 (MMM)](../09-marketing-mix-model/): MMM mede *quanto cada canal moveu AUM*; **esta etapa mede se a mensagem casa com o interesse** — o ingrediente que o MMM pressupõe mas não analisa.

## A ideia em uma frase

> **Transformar texto (posts dos leads e seus posts) em números (vetores), medir distância entre esses números (cosseno) e agrupá-los em assuntos (topic modeling) — para enxergar, lado a lado, o "mapa de interesse" do público e o "mapa de conteúdo" da marca, e quantificar onde eles divergem.**

## Os três níveis de pergunta (e a técnica de cada um)

Há uma escada de sofisticação. Você citou pedaços dela; aqui está a escada inteira, do mais simples ao mais robusto:

| Nível | Pergunta que responde | Técnica | Dá para fazer com |
|-------|------------------------|---------|-------------------|
| **1 — Palavras** | "Quais *termos* aparecem mais? Em que difiro do público?" | Nuvem de palavras, **keyness** (distinção entre dois corpora) | Script simples (Python), poucas linhas |
| **2 — Significado** | "Quão *próximo* o meu conteúdo está do interesse deles, mesmo com palavras diferentes?" | **Embeddings + similaridade de cosseno** | Modelo de embedding + numpy |
| **3 — Assuntos** | "Quais *temas* emergem de cada lado? Qual tema o público discute e eu não cubro?" | **Topic modeling (BERTopic)** + **resumo estruturado via LLM** | Bibliotecas de DS + um LLM |

> **A grande sacada — e por que cosseno importa:** nuvem de palavras compara *palavras exatas*. Mas um lead pode falar de "preservar o patrimônio para os filhos" e você publicar sobre "planejamento sucessório" — **zero palavras em comum, mesmo assunto**. A nuvem de palavras não vê isso; o **cosseno entre embeddings vê**, porque embeddings capturam *significado*, não grafia. Por isso a escada não para no Nível 1.

## O que esta etapa entrega

| Doc | Conteúdo | Para quem |
|-----|----------|-----------|
| [`00-resumo-executivo.md`](./00-resumo-executivo.md) | Este documento: a pergunta, a escada de técnicas, o mapa | Visão geral |
| [`01-escada-de-tecnicas.md`](./01-escada-de-tecnicas.md) | Cada técnica explicada de verdade: o que mede, o que NÃO mede, quando usar — nuvem de palavras, keyness, embeddings, cosseno, topic modeling, resumo via LLM | Para entender os conceitos |
| [`02-coleta-e-preparacao.md`](./02-coleta-e-preparacao.md) | De onde tirar os textos (posts dos leads, seus posts), **ética e LGPD** (crítico no seu setor), limpeza e preparação em PT-BR | Antes de codar |
| [`03-metodos-e-codigo.md`](./03-metodos-e-codigo.md) | Os scripts: nuvem de palavras, keyness, embeddings + cosseno, BERTopic, resumo estruturado com LLM — código Python comentado | Mão na massa |
| [`04-workflow-aplicado.md`](./04-workflow-aplicado.md) | O pipeline completo aplicado ao seu caso: do dado bruto ao **"placar de alinhamento"** e ao mapa de gaps de conteúdo | Para rodar de ponta a ponta |
| [`05-stack-e-roadmap.md`](./05-stack-e-roadmap.md) | Ferramentas (local vs. API), modelos de embedding PT-BR, plano crawl/walk/run, armadilhas, referências | Para decidir e evoluir |

## Como ler

- **10 minutos, conceito:** este doc + [`01-escada-de-tecnicas.md`](./01-escada-de-tecnicas.md).
- **Vai codar essa semana:** [`02`](./02-coleta-e-preparacao.md) → [`03`](./03-metodos-e-codigo.md) → [`04`](./04-workflow-aplicado.md).

## Aviso de honestidade técnica (leia antes de empolgar)

Três limites que esta etapa respeita e explica em detalhe nos docs:

1. **LGPD e ética.** Analisar publicações de leads é tratamento de dado pessoal. No seu setor (financeiro, dado sensível, sob CVM), isso exige base legal, finalidade e cuidado — e há um jeito mais seguro: **agregar e anonimizar**, nunca criar perfil individual invasivo. O [`02`](./02-coleta-e-preparacao.md) trata disso primeiro, porque é pré-requisito, não rodapé.
2. **Volume baixo gera ruído.** Como na [Etapa 9](../09-marketing-mix-model/), seu público UHNW é pequeno. Topic modeling sobre 50 posts não é confiável. Os docs indicam quando você tem dados suficientes e o que fazer quando não tem (cair para o nível mais simples e robusto).
3. **A ferramenta não decide; ela ilumina.** O output é um *insight* ("o público fala muito de sucessão internacional, vocês publicam pouco") — a decisão editorial continua sua. É um holofote, não um piloto automático.

## Conexão com as outras etapas

| Esta etapa se apoia em… | …de |
|-------------------------|-----|
| Embeddings, vector stores, modelos PT-BR (BGE-M3), busca semântica | [`01-casos-de-uso/03-embeddings-rag.md`](../01-casos-de-uso/03-embeddings-rag.md), [`02-tecnologias/05-rag-vector-stores.md`](../02-tecnologias/05-rag-vector-stores.md) |
| Extração estruturada (resumo em JSON via LLM) | [`01-casos-de-uso/07-extracao-estruturada.md`](../01-casos-de-uso/07-extracao-estruturada.md) |
| A pergunta de atribuição e ROI de mensagem | [`09-marketing-mix-model/`](../09-marketing-mix-model/) |
| Método de experimentação (testar se ajustar a pauta move métrica) | [`10-startup-enxuta/`](../10-startup-enxuta/) |
| O gargalo "marketing alinhado ao público certo" | [`11-revops-aplicado/`](../11-revops-aplicado/) |

## Mensagem-chave em uma linha

> **Palavras mostram o vocabulário; vetores e cosseno mostram o significado; topic modeling mostra os assuntos. Use os três em escada para colocar o "mapa de interesse do público" e o "mapa do seu conteúdo" lado a lado e medir, em número, onde vocês não estão se falando.**
