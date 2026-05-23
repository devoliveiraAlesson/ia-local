# Etapa 9 — Marketing Mix Modeling (MMM): mensurar mídia, calcular ROI e projetar cenários

> Dossiê sobre Marketing Mix Modeling (Modelagem de Mix de Marketing / Media Mix Modeling) escrito para Alesson — publicitário e cientista de dados assumindo uma posição de pivô entre Comercial e Marketing. Cobre o que é MMM, a estatística por trás, as ferramentas open source (Google Meridian, Meta Robyn, PyMC-Marketing), como construir o primeiro modelo, como ler a saída para tomar decisão de verba, e um caso aplicado a uma empresa brasileira. Maio/2026.

## A sua pergunta, respondida primeiro

Você escreveu (traduzindo): _"aprendi sobre isso ontem e me pediram para aprofundar a área no tema. Pelo pouco que entendi, talvez seja sobre usar padrões estatísticos pra avaliar performance e projetar hipóteses — é isso?"_

**Sim — e está mais certo do que "talvez".** MMM é exatamente isso, com nome técnico:

> MMM usa **modelagem estatística/econométrica sobre dados históricos agregados** para (1) **quantificar a contribuição de cada canal de marketing** num resultado de negócio (vendas, receita, conversões, pipeline), (2) **calcular o ROI/ROAS de cada canal**, e (3) **simular e otimizar cenários futuros de verba** ("se eu tirar R$ X de OOH e jogar em Google Ads, o que acontece com as vendas?").

"Avaliar performance" = a parte de **decomposição e ROI**. "Projetar hipóteses" = a parte de **response curves + otimização de cenários (what-if)**. Você intuiu as duas metades certas da disciplina. Este dossiê transforma essa intuição em capacidade técnica de construir e operar um MMM.

## O que é MMM em uma frase

> MMM é uma regressão (hoje, quase sempre **Bayesiana**) que explica uma variável de negócio em função do investimento em cada canal de mídia — depois de aplicar duas transformações não-lineares (**adstock** = efeito que perdura no tempo; **saturação** = retornos decrescentes) e de controlar fatores de base (sazonalidade, preço, promoção, distribuição, macroeconomia).

## Mensagem-chave em uma linha

> Pare de perguntar "quem clicou por último" e comece a perguntar "quanto cada real de cada canal realmente moveu a receita, e onde o próximo real rende mais" — isso é MMM.

## Por que MMM está vivendo um renascimento AGORA (2024–2026)

Não é modismo. É uma convergência de forças que **quebrou o rastreamento individual** e devolveu protagonismo ao MMM, que sempre trabalhou com dados **agregados** (não usa dado pessoa-a-pessoa):

| Força | O que aconteceu | Por que empurra para o MMM |
|---|---|---|
| **iOS App Tracking Transparency (ATT)** | Apple (iOS 14.5, abr/2021) passou a exigir opt-in para rastreamento. Opt-in global ficou em ~15–25%. | A maior parte do rastreamento mobile sumiu; atribuição user-level virou cega. MMM não depende disso. |
| **Fim do cookie de terceiros / ITP** | Safari (ITP), Firefox (ETP) e Chrome restringindo cookies de terceiros. | Jornadas cross-site ficaram irrastreáveis. MMM usa dado agregado de gasto vs. resultado. |
| **LGPD / GDPR** | Privacidade virou lei. Dado pessoal é passivo de risco. | MMM é **privacy-safe por construção** — trabalha com totais semanais, não com indivíduos. |
| **Declínio do last-click e do MTA** | Atribuição last-click superestima canais de fundo de funil; MTA (multi-touch) depende de tracking user-level que está morrendo. | MMM mede **contribuição incremental** sem precisar costurar a jornada do usuário. |
| **Google e Meta abriram ferramentas de MMM** | Meta abriu o **Robyn** (2021); Google abriu o **LightweightMMM** e, em **jan/2025**, lançou o **Meridian** (sucessor oficial, com o LightweightMMM agora descontinuado); a comunidade PyMC mantém o **PyMC-Marketing**. | A barreira de entrada caiu de "consultoria de R$ 500k" para "um cientista de dados com Python e 2 anos de dados". **Esse cientista de dados pode ser você.** |

Tradução para o seu mundo: a indústria voltou a precisar de **gente que junta estatística com planejamento de mídia**. É exatamente o seu cruzamento — publicitário + cientista de dados.

## O que cada documento deste dossiê entrega

| Doc | Conteúdo | Para o seu lado... |
|-----|----------|--------------------|
| [`01-fundamentos-mmm.md`](./01-fundamentos-mmm.md) | Definição, história (econometria, por que CPG inventou), conceitos centrais (base vs incremental, decomposição, ROI/ROAS), e o comparativo **MMM × MTA × Incrementalidade** | Publicitário — alinha vocabulário com o time de mídia |
| [`02-metodologia-estatistica.md`](./02-metodologia-estatistica.md) | A estatística a fundo: regressão (aditiva vs log-log), adstock (geométrico/Weibull), saturação (Hill/S-curve), multicolinearidade, ridge, abordagem **Bayesiana** (priors, MCMC), calibração | Cientista de dados — aqui você brilha |
| [`03-implementacao-pratica.md`](./03-implementacao-pratica.md) | Dados necessários, schema, comparativo de ferramentas (Meridian, Robyn, PyMC-Marketing, LightweightMMM legado), stack recomendada, workflow e código Python | Cientista de dados — o "mão na massa" |
| [`04-interpretacao-e-decisao.md`](./04-interpretacao-e-decisao.md) | Ler decomposição, ROI marginal vs médio, response curves, **otimização de verba**, cenários what-if, validação do modelo, como comunicar à liderança | Pivô Comercial×Marketing — sua entrega de valor |
| [`05-caso-aplicado.md`](./05-caso-aplicado.md) | Caso concreto numa empresa brasileira B2B/B2C: outcome, canais, dados a puxar do CRM/RevOps, hipóteses, primeiro entregável, conexão com CAC/pipeline | Você — leve para a sua realidade |
| [`06-roadmap-e-referencias.md`](./06-roadmap-e-referencias.md) | Plano em fases (crawl/walk/run), modelo de maturidade, armadilhas organizacionais, trilha de aprendizado e bibliografia consolidada | Você como dono da capacidade |

## Como isso se conecta ao seu perfil e à sua nova posição

- **Você é publicitário**: entende briefing, plano de mídia, TV vs digital vs OOH, promoção e preço. MMM precisa exatamente desse contexto para não tratar canais como números cegos. Você sabe que uma campanha de TV "respira" por semanas — isso é o **adstock**. Você sabe que dobrar a verba não dobra o resultado — isso é a **saturação**. Você já tem a intuição; o MMM dá a ela um número.
- **Você é cientista de dados**: a metodologia ([`02`](./02-metodologia-estatistica.md)) e a implementação ([`03`](./03-implementacao-pratica.md)) são o seu terreno. Regressão Bayesiana, MCMC, regularização, priors informativos — tudo isso é onde você adiciona rigor que o time de marketing não tem.
- **Você está virando pivô Comercial×Marketing (RevOps)**: MMM é a ponte natural. Ele conecta **investimento de marketing** com **resultado comercial** (receita, pipeline, CAC). O doc [`05`](./05-caso-aplicado.md) amarra MMM a métricas de RevOps. Você vira a pessoa que diz, com número na mão, "vale a pena tirar verba daqui e botar ali".

## Por onde começar a leitura

Se você tem 20 minutos: leia este resumo + a seção de comparativo (MMM×MTA×Incrementalidade) em [`01-fundamentos-mmm.md`](./01-fundamentos-mmm.md).

Se você quer botar a mão na massa neste fim de semana: pule para [`03-implementacao-pratica.md`](./03-implementacao-pratica.md) e instale o **PyMC-Marketing** (Python) ou abra o template do **Google Meridian**.

Se você precisa convencer a liderança primeiro: leve este resumo + [`04-interpretacao-e-decisao.md`](./04-interpretacao-e-decisao.md) (como vira decisão de verba).

## Referências

- Marketing mix modeling — Wikipedia: <https://en.wikipedia.org/wiki/Marketing_mix_modeling>
- Google Meridian (repositório oficial): <https://github.com/google/meridian>
- Meta Robyn (repositório oficial): <https://github.com/facebookexperimental/Robyn>
- PyMC-Marketing (documentação oficial): <https://www.pymc-marketing.io/>
- Migrate from LightweightMMM (Google for Developers): <https://developers.google.com/meridian/docs/migrate>
- The iOS 14 Reckoning: How App Tracking Transparency Reshaped eCommerce: <https://www.penandpaper.ai/post/the-ios-14-reckoning-how-app-tracking-transparency-reshaped-ecommerce>
- MMM e Retail Media (mensuração no Brasil): <https://retailmedianews.com.br/artigos/marketing-mix-modeling-mmm-e-retail-media-o-caminho-para-a-mensuracao-e-otimizacao-de-alta-performance/>
- Marketing Mix Modeling, conformidade com a LGPD (Approach): <https://www.approach.com.br/blog/marketing-mix-modeling/>
