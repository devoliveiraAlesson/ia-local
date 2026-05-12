# Caso 5 — Code Review Automatizado

## Descrição

Bot que se inscreve no webhook de Pull Request do GitLab/GitHub/Bitbucket interno e, a cada push, faz uma análise automática do diff:

- Comenta inline em linhas com problemas (bugs, race conditions, vulnerabilidades, smells, regras internas).
- Sumariza o PR em alto nível ("o que esse PR faz, em que módulos toca, quais riscos").
- Sugere testes faltantes.
- Verifica aderência a guias de estilo internos, ADRs e regras de arquitetura específicas da empresa.
- Opcionalmente bloqueia merge em achados críticos (security, contratos quebrados).

Roda como complemento — não substituto — do reviewer humano.

## Por que precisa ser LOCAL

- O bot precisa ler o diff completo, frequentemente código proprietário com regras de negócio sensíveis (algoritmos de pricing, antifraude, scoring de crédito, etc.).
- Precisa indexar o **repositório inteiro** para dar respostas com contexto (cross-file). Mandar todo o repo para uma API pública é inaceitável em qualquer empresa séria com IP relevante.
- Em ambientes regulados (PCI, governo, defesa), o source-code já é classificado e não pode sair do perímetro.

## Modelo recomendado

- **Análise de diff (qualidade alta + contexto longo)**:
  - Qwen 2.5-Coder 32B ou Qwen3-Coder (256k+ context).
  - DeepSeek V3.2 ou DeepSeek-Coder V2 (160k context, MoE eficiente).
  - Llama 3.3 70B (generalista bom em código).
- **Sumarização de PR**: o mesmo modelo acima ou um modelo menor (Qwen 2.5 14B, Granite 3 8B) para custo reduzido.
- **Reasoning intenso (refactor proposto, análise de race condition)**: DeepSeek-R1 ou Qwen 3 reasoning.

## Stack típica

- **Runtime**: vLLM (em background queue, não no caminho síncrono do webhook — webhook do GitHub tem timeout de 10s).
- **Orquestração**:
  - **CodeRabbit self-hosted** (versão enterprise).
  - **Greptile** (revisor agentic).
  - **Sweep / Aider** em modo bot.
  - Ou bot caseiro: webhook → fila (Redis/Celery/Temporal) → worker → vLLM → API do GitLab/GitHub para postar comentários.
- **Análise estática complementar (não-LLM)**: Semgrep, CodeQL, SonarQube — o LLM enriquece os achados com explicação e sugestão.
- **Indexação do repo**: Sourcegraph self-hosted ou índice próprio (tree-sitter + embeddings).
- **Observabilidade**: Langfuse + métricas próprias (taxa de comentário aceito, falsos positivos).

## Métricas de sucesso / KPIs

- **% de comentários úteis** (marcados como "thumbs up" pelo dev).
- **% de comentários acionados** (gerou commit subsequente).
- **Falso positivo rate** (meta < 25%; acima disso devs ignoram).
- **Bugs/vulnerabilidades capturados antes do merge** (cross-check com bugs em produção subsequentes).
- **Tempo de revisão humana**: redução esperada 15–30% (humano foca em arquitetura, IA cuida do trivial).
- **Cobertura**: % de PRs revisados pelo bot.
- **MTTR de PR** (tempo da abertura até merge): meta de redução 10–20%.

## Estimativa de retorno

**Média-Alta.** Não substitui o reviewer humano, mas:
- Reduz o tempo gasto em pequenos detalhes (typo, naming, falta de teste, regra de estilo).
- Aumenta a captura de bugs e vulnerabilidades antes do merge.
- Padroniza qualidade, especialmente útil em times distribuídos ou júnior-pesados.
- Custos diretos (1 GPU dedicada) muito inferiores a CodeRabbit/Greptile SaaS para volumes médios/altos.

## Maturidade

**Produção média.** Bot funcional em 3–6 semanas. Refinamento (reduzir falsos positivos, ajustar prompts ao guia interno, integrar SAST) leva mais 2–3 meses. Tem que ser opt-out por time no início — bot ruim gera anticorpos rapidamente.

## Riscos e mitigação

- **Falsos positivos** matam adoção: começar conservador (só erros óbvios e segurança), iterar.
- **Latência fora do webhook**: usar background job, comentar quando pronto, GitHub permite.
- **Bot virando ruído**: deixar dev silenciar com label/comando, métrica obrigatória de "comentários acionados".
- **Confiança excessiva**: reviewer humano continua obrigatório; bot é assistente.
- **Limite de contexto em PRs grandes**: estratégia de chunking de diff por arquivo, com sumário global.

## Fontes consultadas

- SitePoint — Self-Hosted AI Code Review with Local LLMs: <https://www.sitepoint.com/self-hosting-ai-code-review-local-models/>
- Augment Code — Open Source AI Code Review tools 2026: <https://www.augmentcode.com/tools/open-source-ai-code-review-tools-worth-trying>
- Onyx — Self-hosted LLM leaderboard 2026: <https://onyx.app/self-hosted-llm-leaderboard>
- Greptile: <https://www.greptile.com/>
- Medium — Building a Local AI-Powered Code Review Agent: <https://medium.com/@bhavin_mistry/building-a-local-ai-powered-code-review-agent-integrate-with-devops-vs-code-f3c4430bd6ba>
- awesome-local-llm: <https://github.com/rafska/awesome-local-llm>
