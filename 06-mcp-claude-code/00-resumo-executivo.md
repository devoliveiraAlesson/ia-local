# Etapa 6 — MCP + Claude Code: APIs internas de conhecimento como ferramenta nativa do agente

> Documento de abertura da Etapa 6. Estende as Etapas 1–5 (RAG corporativo do Caso 3 + Coding Assistant do Caso 4) para o padrão emergente de 2025–2026: expor a base de conhecimento da empresa como **servidor MCP**, consumido nativamente por Claude Code e qualquer cliente compatível. Maio/2026.

## Por que esta etapa existe

A Etapa 1 mapeou que **RAG corporativo (Caso 3)** é a plataforma de maior alavancagem — habilita atendimento, sumarização, extração e coding assistant. A Etapa 2 detalhou a stack (vector store + embeddings + reranker). A Etapa 4 dimensionou a infra.

Faltava responder a pergunta que apareceu na prática nos pilotos de coding assistant: **"como faço o agente buscar automaticamente na nossa base antes de cada tarefa, sem ter que colar contexto no prompt?"**

A resposta consolidada em 2026 é **Model Context Protocol (MCP)**. Anthropic, OpenAI, Google e Microsoft adotaram MCP como padrão de tool-calling; LangChain, CrewAI e LlamaIndex tornaram MCP o transporte default. Frameworks de RAG (Qdrant, Milvus, Weaviate, Neo4j) publicaram servidores MCP de primeira parte. **MCP virou o "USB-C" de contexto para agentes de IA.**

Para a empresa, isso significa: a mesma API interna de RAG que serve o chat corporativo (Caso 1), o atendimento (Caso 2) e a sumarização (Caso 6) passa a servir **também** o agente de codificação do desenvolvedor, sem código de glue específico por aplicação.

## Mensagem-chave em uma linha

> **Construa o RAG corporativo (Caso 3) uma vez; exponha como servidor MCP; consuma a partir de Claude Code, Continue, Cline, Cursor, agentes próprios e qualquer cliente MCP — sem reescrever ingestão, embedding, ACL ou rerank por aplicação.**

## O que muda em relação às Etapas 1–5

| Item | Antes (Etapas 1–5) | Com MCP (Etapa 6) |
|------|---------------------|-------------------|
| Acesso ao RAG pelo coding assistant | Plugin de IDE com integração custom por fornecedor | Servidor MCP único; qualquer cliente compatível plugga |
| Multiplicação de integrações | N clientes × M bases = N×M conectores | N + M (clientes falam MCP, bases expõem MCP) |
| Re-rank (Qwen3-Reranker, BGE) | Embutido na app que chama o vector store | Embutido no servidor MCP — transparente ao cliente |
| Governança (ACL, audit, quotas) | Por aplicação | Centralizada no servidor MCP + gateway |
| Contexto repetitivo no prompt | Dev cola "leia o CLAUDE.md, considere X, Y, Z..." | Agente busca automaticamente via tool MCP |
| Onboarding de novo cliente de IA | Semanas de integração | Configuração de um comando (`claude mcp add`) |

## O que esta Etapa entrega

| Doc | Conteúdo | Audiência |
|-----|----------|-----------|
| [`01-mcp-fundamentos.md`](./01-mcp-fundamentos.md) | O que é MCP, transportes (stdio/HTTP), escopos (local/project/user), arquitetura | Tech Lead / arquiteto |
| [`02-rag-via-mcp.md`](./02-rag-via-mcp.md) | Como o RAG corporativo do Caso 3 vira tool MCP (retrieve + rerank + cite) | Eng de plataforma / RAG |
| [`03-graph-rag-via-mcp.md`](./03-graph-rag-via-mcp.md) | Graph RAG (Neo4j, Kuzu) exposto via MCP — quando a estrutura importa mais que o texto | Eng de dados |
| [`04-servidores-mcp-prontos.md`](./04-servidores-mcp-prontos.md) | Catálogo: mcp-local-rag, knowledge-rag, mcp-neo4j-graphrag, github, postgres, etc. | Time de DevEx |
| [`05-construir-mcp-interno.md`](./05-construir-mcp-interno.md) | Build de servidor MCP próprio (FastMCP/Python ou TypeScript), expondo APIs internas | Eng de software |
| [`06-seguranca-governanca.md`](./06-seguranca-governanca.md) | OAuth 2.1, ACL no retrieval, audit trail, prompt injection via tool, OWASP LLM | CISO / DPO |
| [`07-roadmap-adocao.md`](./07-roadmap-adocao.md) | Fases 0–3 de rollout interno; integração com o roadmap mestre da Etapa 5 | PMO / Tech Lead |

## Decisões executivas que esta Etapa pede

1. **Tratar MCP como camada de plataforma**, não como POC isolada. O servidor MCP do RAG corporativo deve ser parte do produto interno mantido pelo time de plataforma, com SLO, observabilidade e CI/CD próprios.
2. **Padronizar Claude Code (ou cliente equivalente que fale MCP) como ferramenta padrão de coding assistant** — substitui ou complementa Continue/Tabby do Caso 4. Decisão de licenciamento e modelo (local vs API) na Etapa 5.
3. **Definir o escopo de exposição via MCP** logo (que dados, com qual ACL, com qual SLA). MCP facilita demais o consumo — sem governança, o blast radius cresce rápido.
4. **Air-gap-aware desde o dia 1**: servidores MCP devem rodar dentro do perímetro; OAuth 2.1 obrigatório para qualquer cliente externo; gateway LLM (LiteLLM/Portkey) intermedia tool-calls.

## Onde se conecta com o resto da proposta

- **Caso 3 (RAG corporativo)** → o servidor MCP é o "consumer interface" da plataforma. Quem implementa o Caso 3 ganha "de graça" a integração com qualquer agente compatível.
- **Caso 4 (Coding assistant)** → Claude Code consome o servidor MCP do RAG e o servidor MCP do GitHub interno; o dev pergunta "como nosso sistema autentica?" e o agente recupera dos docs antes de escrever.
- **Etapa 2 (Frameworks)** → LlamaIndex, LangChain e Haystack publicam adaptadores MCP. O framework não some — ele vira o builder do servidor MCP.
- **Etapa 4 (Observabilidade)** → toda chamada de tool MCP atravessa o gateway, vira span OTel GenAI no Langfuse.
- **Etapa 5 (ROI)** → o ganho mensurável é redução de "tempo colando contexto" + aumento de acceptance rate do coding assistant (esperado +5–10 p.p. com RAG ativo). Detalhado em `07-roadmap-adocao.md`.

## Próxima leitura sugerida

Para entender o protocolo: [`01-mcp-fundamentos.md`](./01-mcp-fundamentos.md). Para ver o desenho concreto de como ligar o RAG corporativo ao Claude Code: [`02-rag-via-mcp.md`](./02-rag-via-mcp.md). Para o checklist de rollout: [`07-roadmap-adocao.md`](./07-roadmap-adocao.md).
