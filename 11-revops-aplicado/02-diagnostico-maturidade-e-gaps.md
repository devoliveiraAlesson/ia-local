# Diagnóstico de maturidade e gaps — os 4 pilares

> Este é o coração da Fase 1. Avaliamos a operação nos quatro pilares de RevOps — **Pessoas, Processo, Tecnologia e Dados** — situando você num nível de maturidade e listando, para cada pilar, as **hipóteses de gargalo** (o que provavelmente está quebrado, com base no que você descreveu) e a **evidência que confirma ou refuta** cada hipótese. As evidências viram queries e perguntas concretas no [`04-instrumento-de-diagnostico.md`](./04-instrumento-de-diagnostico.md).

## Modelo de maturidade (resumo)

| Nível | Como se reconhece | Sinal típico |
|-------|-------------------|--------------|
| **1 — Caótico** | Planilhas dispersas, cada área com seu número, nada definido | "Qual é o número certo?" sem resposta |
| **2 — Reativo** | CRM existe mas subutilizado; dados coletados mas não acionados; processos informais | **← provável posição atual** |
| **3 — Definido** | Definições compartilhadas, fonte única de verdade, SLAs medidos, cadência rodando | Reuniões usam o mesmo dashboard |
| **4 — Otimizado** | Forecast confiável, scoring calibrado, atribuição canal→AUM, experimentação contínua | Decisões de budget saem de modelo |
| **5 — Preditivo** | Modelos preditivos em produção, otimização de share-of-wallet, automação | RevOps dirige a estratégia de receita |

> **Hipótese de posicionamento:** você está em **transição do Nível 2 para o 3**. Tem a matéria-prima de um Nível 4 (pipelines de dados, capacidade analítica), mas falta a fundação do Nível 3 (definições, fonte única, processo). O risco clássico do seu perfil é pular para modelagem (Nível 5) sem a fundação — modelo sofisticado sobre CRM sujo é "lixo com aparência de ciência". A sequência correta é **fechar o Nível 3 primeiro**.

```mermaid
flowchart LR
    N1["1 Caótico"] --> N2["2 Reativo\n(você está aqui)"]
    N2 -.->|"o salto da Fase 2"| N3["3 Definido\n(meta 90 dias)"]
    N3 --> N4["4 Otimizado"]
    N4 --> N5["5 Preditivo"]
    N2 -.->|"armadilha: pular etapas"| N5
    style N2 fill:#fde68a
    style N3 fill:#bbf7d0
```

---

## Pilar 1 — Pessoas

**O que avaliar:** clareza de papéis e do mandato de RevOps, ownership da jornada de receita ponta a ponta, e o alinhamento entre Marketing, SDR e Executivos.

| Hipótese de gargalo | Por que suspeitamos | Evidência que confirma/refuta |
|---------------------|---------------------|-------------------------------|
| **Ninguém é dono da jornada ponta a ponta** | Times "desestruturados", sem processos | Pergunte a cada líder "quem é dono do número de receita ponta a ponta?" — respostas divergentes confirmam |
| **Seu mandato de RevOps não está claro** | Cargo de fronteira, recém-criado | A quem você reporta? Qual seu escopo de decisão sobre CRM, definições e budget? |
| **Marketing e Comercial têm metas desalinhadas** | Silos típicos | Marketing é cobrado por leads e Comercial por AUM? Metas em unidades diferentes geram atrito |
| **Executivos sêniores fazem trabalho de triagem** | Sem filtro SDR confiável | % do tempo de executivo gasto com prospects que não fecham / não eram fit |

> **Nota para o seu perfil:** RevOps é ~50% relacionamento. Como você vem de dados, a armadilha é resolver tudo com dashboard e ignorar a co-criação das definições com Vendas/Marketing. Definição imposta não é adotada. Os melhores números, se não usados em reunião, não valem nada.

---

## Pilar 2 — Processo

**O que avaliar:** existência de definições compartilhadas (o que é um lead qualificado UHNW?), critérios de estágio, SLAs e instrumentação dos handoffs.

| Hipótese de gargalo | Por que suspeitamos | Evidência que confirma/refuta |
|---------------------|---------------------|-------------------------------|
| **Não há definição escrita de "lead qualificado UHNW"** | "Processos não definidos" | Peça a definição a Marketing, SDR e Executivo separadamente — divergência confirma |
| **Handoff SDR→Executivo não é instrumentado** | Funil descrito sem o estágio de aceite | Existe campo/estágio de "aceito pelo executivo"? Há motivo de rejeição? |
| **Estágios de pipeline são por sentimento, não por evidência** | CRM subutilizado | Os estágios têm *exit criteria* objetivos ou são "acho que vai fechar"? |
| **SLA de tempo de resposta ao lead não existe/não é medido** | Sem processo definido | Qual o tempo mediano entre criação do lead e 1º contato do SDR? |
| **Retenção/expansão de AUM não é processo** | Foco descrito está em aquisição (Mkt→SDR→Exec) | Há cadência de revisão de carteira, gatilhos de expansão, alerta de risco de saída? |
| **Não há método de forecast** | Maturidade 2 | Existe alguma previsão de AUM novo? Mede-se previsto vs. realizado? |

> **O gargalo de processo mais provável e mais caro:** o handoff **SDR → Executivo** sem instrumentação. Numa gestora UHNW, o recurso mais escasso é o tempo do executivo sênior. Se você não mede a taxa de aceite e o motivo das rejeições, não consegue nem calibrar o filtro do SDR nem proteger o tempo do executivo — e ambos sangram receita silenciosamente.

---

## Pilar 3 — Tecnologia

**O que avaliar:** adequação e adoção do CRM, integração das ferramentas (RD, CRM, canais), e a existência de uma camada de BI/fonte única de verdade.

| Hipótese de gargalo | Por que suspeitamos | Evidência que confirma/refuta |
|---------------------|---------------------|-------------------------------|
| **CRM subutilizado (baixa adoção)** | Suas palavras: "OK mas não super bem usado" | % de oportunidades com campos-chave preenchidos; % de atividades registradas |
| **Ferramentas em silos, dados não conciliados** | RD + CRM + canais extraídos, mas "não vira ação" | RD e CRM "conversam"? Dá para ligar uma campanha RD a um AUM fechado no CRM? |
| **Não há fonte única de verdade (SSoT)** | Cada área olha um número | Existe um dashboard único usado nas reuniões, ou cada um traz sua planilha? |
| **Pipelines de dados levam a um data lake, não a decisões** | "Ampla coleta, sem estruturar em ações" | Os dados extraídos alimentam algum painel de decisão, ou só ficam armazenados? |

> Você está em vantagem aqui: já tem pipelines de extração de **todos os canais + RD + CRM**. O problema não é *engenharia de dados* — é que falta a **camada semântica e de decisão** em cima deles (definições + fonte única). Isso é mais barato e rápido de resolver do que construir a extração do zero. É um quick win esperando para acontecer.

---

## Pilar 4 — Dados

**O que avaliar:** qualidade/higiene do CRM, existência de um modelo de dados de receita coerente, e a capacidade de conectar marketing → funil → AUM.

| Hipótese de gargalo | Por que suspeitamos | Evidência que confirma/refuta |
|---------------------|---------------------|-------------------------------|
| **Campos-chave vazios ou inconsistentes** | CRM subutilizado | % de oportunidades sem: origem, tier de patrimônio, AUM estimado, data prevista, motivo de perda |
| **Sem chave que ligue lead (RD) → cliente (CRM) → AUM** | Dados em silos | Existe um identificador que percorre RD→CRM→custódia? |
| **Origem do cliente não é confiável** | Atribuição ausente | A "fonte" no CRM é preenchida e confiável? Indicação é capturada com *quem* indicou? |
| **Duplicatas e registros órfãos** | Higiene baixa | Contagem de contatos/contas duplicados; oportunidades sem dono ou paradas |
| **AUM e fluxos não estão no mesmo modelo do funil** | Receita vive na custódia, funil no CRM | Dá para cruzar AUM real (custódia) com a oportunidade que o originou? |

> **Este é o pilar onde você brilha — e por isso a armadilha é começar por ele.** A tentação será fazer um diagnóstico de qualidade de dados lindíssimo e parar aí. Faça-o (é munição: "X% das oportunidades estão sem tier de patrimônio, o que inviabiliza qualquer scoring"), mas lembre que dados limpos só geram valor quando há **definição** (Processo) e **uso em reunião** (Pessoas). Higiene primeiro, modelo depois.

---

## Síntese do diagnóstico (a preencher com dados reais)

A tabela abaixo é o **placar do diagnóstico**. Hoje preenchemos a coluna de hipótese; o [`04-instrumento-de-diagnostico.md`](./04-instrumento-de-diagnostico.md) gera os números que fecham as colunas de evidência e severidade.

| Pilar | Nível hipótese | Gargalo nº 1 hipotético | Severidade (a confirmar) |
|-------|----------------|--------------------------|--------------------------|
| Pessoas | 2 | Mandato de RevOps e ownership da jornada indefinidos | ? |
| Processo | 1–2 | Handoff SDR→Executivo não instrumentado; sem definição de lead UHNW | ? |
| Tecnologia | 2–3 | Falta a fonte única de verdade sobre pipelines existentes | ? |
| Dados | 2 | Sem chave RD→CRM→AUM; campos-chave vazios | ? |

## As 3 dores que o diagnóstico provavelmente vai elevar ao topo

1. **"Não sabemos quais canais/indicações trazem AUM"** → atribuição canal→AUM ausente (ponte para [Etapa 9 / MMM](../09-marketing-mix-model/)).
2. **"O tempo dos executivos é mal aproveitado"** → handoff SDR→Executivo sem filtro/aceite medido.
3. **"Cada reunião discute números diferentes"** → ausência de fonte única de verdade sobre dados que já existem.

> Estas três dores são, não por acaso, **quick wins de alto impacto e baixo atrito político** — exatamente o tipo de alvo que a Fase 2 vai priorizar (ver a lógica em [`08-revops/06-roadmap-90-dias.md`](../08-revops/06-roadmap-90-dias.md)).

Próximo documento: a **árvore de métricas** correta para o seu modelo ([`03`](./03-metricas-do-modelo.md)).
