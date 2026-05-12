# Caso 4 — Coding Assistant Local (estilo Copilot)

## Descrição

Assistente de programação integrado à IDE (VS Code, JetBrains, Vim/Neovim) e/ou ao terminal, oferecendo:

- **Autocomplete inline** ("ghost text", FIM — fill-in-the-middle).
- **Chat lateral** com contexto do arquivo/projeto.
- **Geração de funções, testes, refatorações** a partir de instrução.
- **Explicação de código legado** e geração de comentários/docstrings.
- **Modo agente** (estilo Cursor/Aider): edita múltiplos arquivos, roda comandos, lê erros de teste/lint e itera.

Tudo isso com inferência rodando em GPU interna; o código nunca sai da rede da empresa.

## Por que precisa ser LOCAL

- Código-fonte é **propriedade intelectual** crítica. APIs comerciais (Copilot, Cursor) treinaram acusações de eco de código com licença restritiva e em alguns acordos enviam o código para análise.
- Empresas com **segredos no código** (chaves, queries, regras de negócio, algoritmos) não podem expor diffs a terceiros — viola NDA com clientes, requisitos do Bacen e contratos com governo.
- **DevSecOps**: muitas pipelines internas executam em ambientes air-gapped (PCI-DSS, defesa, governo); a única forma de IA é local.
- Custo: para 200+ devs ativos, licenças Copilot Business ($19/dev/mês) ou Cursor ($20–40) ultrapassam US$ 60–100k/ano — comparável ao custo de uma GPU dedicada amortizada.

## Modelo recomendado

- **Autocomplete (FIM, latência crítica)**:
  - Qwen 2.5-Coder 1.5B/3B/7B (FIM nativo, estado da arte em modelos pequenos).
  - DeepSeek-Coder V2 Lite 16B (MoE, 2.4B ativos).
  - StarCoder2 7B.
- **Chat / geração / agente (qualidade)**:
  - Qwen 2.5-Coder 32B (ou Qwen3-Coder em 2026, top open-weight em SWE-bench).
  - DeepSeek-Coder V2 236B (MoE, 21B ativos) ou DeepSeek V3 / V3.2 para reasoning de código.
  - Codestral 22B (Mistral, licença restrita a uso interno — verificar).
  - Devstral Small 2 (24B, ~68% SWE-bench Verified, roda em 1× RTX 4090).
- **Reasoning para tarefas difíceis**: DeepSeek-R1, Qwen 3 reasoning.

Uma combinação típica: **Qwen 2.5-Coder 7B** para autocomplete (latência <300ms) + **Qwen 2.5-Coder 32B** ou **DeepSeek-Coder V2** para chat/agente.

## Stack típica

- **Runtime**: vLLM com 2 deployments distintos (modelo pequeno para FIM, modelo grande para chat). Ollama para POC e estações poderosas isoladas.
- **Plugin de IDE / orquestrador**:
  - **Continue.dev** (open source, VS Code + JetBrains, BYOM, suporta FIM, MCP) — recomendação default.
  - **Tabby** (servidor self-hosted completo, indexação de repositório, RBAC).
  - **Aider** (terminal, multi-arquivo, auto-commit).
  - **OpenCode** / **Kilo Code** (BYOK, agente open source, MCP).
  - **Cline / Roo Code** (extensões VS Code agentic, BYOK).
- **Indexação de repo**: Sourcegraph self-hosted (com Cody alimentado por modelo local) ou indexação interna do Tabby/Continue.
- **Telemetria**: Langfuse (latência por token, taxas de aceitação), métricas próprias de aceitação.

## Métricas de sucesso / KPIs

- **Acceptance rate** (autocomplete): % de sugestões aceitas sem edição. Benchmark Copilot: 25–35%.
- **Char-accept ratio**: caracteres aceitos / caracteres oferecidos.
- **% de PRs com contribuição de IA** (anotado por commit ou métrica interna).
- **Lead time de PR**: redução de 10–30%.
- **DORA metrics**: deploy frequency, change failure rate (com IA não pode subir CFR).
- **Time-to-first-PR de novos devs** (rampa de onboarding cai com IA).
- **Latência P95 do autocomplete**: < 400ms (acima disso o dev abandona).
- **Adoção**: % de devs com plugin instalado e ativo.

## Estimativa de retorno

**Alta**. Estudos (GitHub, Microsoft, Faros, GitClear 2024–2025) mostram 10–30% de aumento em produtividade percebida e 20–40% mais rápido em tarefas isoladas. Em uma engenharia de 200 devs com salário médio de R$ 200k/ano, mesmo um ganho conservador de 8% representa R$ 3,2 milhões/ano de capacidade adicional.

Cuidado: ganho cai se o modelo é fraco; abaixo de Qwen 2.5-Coder 7B/14B a aceitação é baixa e desengaja o usuário.

## Maturidade

**POC fácil → Produção média.** Continue.dev + Ollama + Qwen-Coder roda em 1 dia em uma workstation. Subir para 200 devs com SLA de latência, indexação de repos, SSO, métricas e atualização de modelos é projeto de 2–3 meses.

## Riscos e mitigação

- **Sugestão com vulnerabilidade**: SAST no PR (Semgrep, CodeQL) + Caso 5 (code review) como segunda linha.
- **Latência alta = abandono**: dimensionar GPU para concorrência real, usar speculative decoding, manter modelo FIM pequeno.
- **Licenciamento de modelo**: Codestral é restrito a uso não comercial direto — confirmar; Qwen, DeepSeek, StarCoder2 e Llama estão liberados sob suas respectivas licenças (verificar Llama Community License para empresa com >700M MAU).
- **Confiança excessiva**: treinamento de uso e cultura de revisar criticamente.

## Fontes consultadas

- Pinggy — Best self-hosted coding LLMs 2026: <https://pinggy.io/blog/best_open_source_self_hosted_llms_for_coding/>
- Local AI Master — Best Local AI for Coding 2026: <https://localaimaster.com/blog/best-local-ai-models-programming>
- Kilo — Open Source Copilot alternatives 2026: <https://kilo.ai/articles/open-source-github-copilot-alternatives>
- Shakudo — Best AI coding assistants 2026: <https://www.shakudo.io/blog/best-ai-coding-assistants>
- Semaphore — Self-hosted LLM coding assistants: <https://semaphore.io/blog/selfhosted-llm-coding-assistants>
- Labellerr — 5 open source coding LLMs 2026: <https://www.labellerr.com/blog/best-coding-llms/>
- DEV.to — Every AI Coding CLI 2026: <https://dev.to/soulentheo/every-ai-coding-cli-in-2026-the-complete-map-30-tools-compared-4gob>
