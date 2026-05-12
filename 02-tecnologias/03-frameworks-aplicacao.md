# Frameworks de Aplicação LLM (2026)

> Camada que liga o runtime (vLLM, etc.) à lógica de negócio (RAG, agentes, function calling). Em 2026 o padrão emergente é combinar **LlamaIndex (retrieval) + LangGraph (agentes) + DSPy (otimização programática de prompt)**, com Haystack como alternativa "tudo em um" mais opinativa e Semantic Kernel/Spring AI cobrindo .NET e Java/Kotlin.

## Tabela-resumo

| Framework | Linguagem | Foco principal | Maturidade | Licença | Stars (~mai/2026) |
|-----------|-----------|----------------|------------|---------|-------------------|
| **LangChain** | Python, JS/TS | Orquestração geral, integrações | Produção (modularizado em `langchain-core`, `langchain-community`) | MIT | 100k+ |
| **LangGraph** | Python, JS/TS | Agentes/grafos stateful (parte da família LangChain) | Produção | MIT | (subset) |
| **LlamaIndex** | Python, TS | RAG, ingestão, retrievers; agora Workflows event-driven | Produção | MIT | 35k+ |
| **Haystack** (deepset) | Python | Pipeline declarativo "tudo em um" | Produção (Haystack 2.x) | Apache 2.0 | 17k+ |
| **DSPy** (Stanford) | Python | Programação declarativa de prompts; otimização automática | Produção (early adopter) | MIT | 18k+ |
| **Semantic Kernel** (Microsoft) | C#/.NET, Python, Java | Orquestração + plugins, integração Microsoft 365 / Azure | Produção | MIT | 22k+ |
| **Spring AI** (VMware/Pivotal) | Java/Kotlin | Spring Boot starter para LLM | Produção (1.0 GA) | Apache 2.0 | 5k+ |
| **AutoGen** (Microsoft) | Python | Multi-agent conversation | Produção | CC-BY-4.0/MIT | 35k+ |
| **CrewAI** | Python | Multi-agent role-based | Produção | MIT | 25k+ |
| **Mirascope** | Python | Tipagem estrita estilo Pydantic | Produção (early) | MIT | 1k+ |
| **txtai** | Python | Embeddings + workflows | Produção | Apache 2.0 | 10k+ |

## Detalhamento

### LangChain / LangGraph
- **O que é**: ecossistema modularizado em `langchain-core` (interfaces), `langchain-community` (integrações), `langchain-openai`, etc. **LangGraph** é a peça nova: grafos stateful para agentes, com checkpointing (durabilidade), human-in-the-loop, time travel.
- **Quando usar**: chains complexas, integrações já cobertas (200+ vector stores, runtimes, tools), agentes multi-step com persistência de estado.
- **Quando NÃO**: app pequeno onde o overhead de abstração é proibitivo; preferir chamadas diretas ao OpenAI-compatible endpoint.
- **Integrações**: vLLM (`langchain-openai`), Qdrant/Milvus/Weaviate/pgvector, Langfuse, LangSmith.
- **Licença**: MIT.
- **Links**: <https://github.com/langchain-ai/langchain> · <https://langchain-ai.github.io/langgraph/>

### LlamaIndex
- **O que é**: começou como "Index + Retriever", virou framework de aplicação completo com **LlamaIndex Workflows** (event-driven, sucessor das chains lineares).
- **Quando usar**: foco em RAG/ingestão (1000+ readers em LlamaHub), agentes baseados em retrieval, ELT para embeddings.
- **Quando NÃO**: aplicativos sem componente de retrieval significativo.
- **Integrações**: vLLM, todos vector stores principais, Langfuse, observability via callbacks.
- **Links**: <https://github.com/run-llama/llama_index> · <https://docs.llamaindex.ai/>

### Haystack 2.x (deepset)
- **O que é**: framework declarativo de pipelines (componentes conectados por sockets tipados). Versão 2.x reescreveu tudo, com **agentes**, **streaming pipelines**, suporte nativo a tool calling e structured outputs.
- **Quando usar**: time que prefere pipeline declarativo (YAML/Python equivalente) em vez de chain imperativa.
- **Integrações**: vLLM, Elastic/OpenSearch, Qdrant, Weaviate, Milvus, Hugging Face.
- **Links**: <https://github.com/deepset-ai/haystack> · <https://haystack.deepset.ai/>

### DSPy (Stanford)
- **O que é**: tratar prompts como **programas**, não strings; o DSPy compila prompts e few-shots otimizados a partir de métricas e dados.
- **Quando usar**: pipelines onde a qualidade do prompt importa muito e há ground truth (eval set); RAG, classificação, extração.
- **Quando NÃO**: prototipagem livre; o overhead de pensar declarativamente é alto.
- **Combinação típica**: DSPy compila → LangGraph orquestra → LlamaIndex faz retrieval.
- **Links**: <https://github.com/stanfordnlp/dspy> · <https://dspy.ai/>

### Semantic Kernel (Microsoft)
- **O que é**: SDK Microsoft para .NET, Python e Java; foco em "skills" (plugins), planners e integração com Microsoft 365 / Copilot.
- **Quando usar**: shop .NET, integração com Azure AI Search, Office, Teams.
- **Links**: <https://github.com/microsoft/semantic-kernel> · <https://learn.microsoft.com/en-us/semantic-kernel/>

### Spring AI
- **O que é**: starter Spring Boot para abstrair providers de LLM e vector stores. **1.0 GA em 2024**, com integração nativa a Spring Data, Spring Security, Actuator.
- **Quando usar**: stack JVM corporativa (banco, governo) com Spring Boot dominante.
- **Integrações**: vLLM/OpenAI-compatible, Qdrant, pgvector, Redis, Cassandra, Milvus, Weaviate, Chroma, Neo4j.
- **Links**: <https://spring.io/projects/spring-ai> · <https://docs.spring.io/spring-ai/reference/>

### AutoGen (Microsoft)
- **O que é**: framework multi-agent com mensagens entre agentes; v0.4 reescrita assíncrona/distribuída.
- **Quando usar**: simulações de equipes de agentes, code generation com revisor.
- **Links**: <https://github.com/microsoft/autogen>

### CrewAI
- **O que é**: multi-agent baseado em "papéis" (researcher, writer, reviewer).
- **Quando usar**: tarefas decomponíveis em papéis claros.
- **Links**: <https://github.com/crewAIInc/crewAI>

### Mirascope
- **O que é**: SDK Python tipado fortemente (Pydantic) para extrair structured outputs.
- **Links**: <https://github.com/Mirascope/mirascope>

### txtai
- **O que é**: alternativa "tudo em um" Python; embeddings + workflows + RAG num único pip.
- **Links**: <https://github.com/neuml/txtai>

## Padrões de combinação observados em produção (2026)

| Padrão | Stack | Caso típico |
|--------|-------|-------------|
| **"BigCo Python"** | LlamaIndex + LangGraph + DSPy + Langfuse | Empresas grandes, eval rigoroso |
| **"Haystack-only"** | Haystack 2.x + vLLM + Weaviate | Time data science que prefere YAML/declarativo |
| **".NET shop"** | Semantic Kernel + Azure AI Search + AKS + vLLM | Empresas Microsoft-house |
| **"Java enterprise"** | Spring AI + Qdrant/pgvector + vLLM em K8s | Bancos, governo, JVM dominante |
| **"Lightweight"** | OpenAI SDK direto + Qdrant client + Pydantic | App simples, sem overhead |

## Critérios de escolha rápidos

1. **Linguagem do time** corta opções: .NET → Semantic Kernel; Java → Spring AI; Python/TS → resto.
2. **Volume de integrações novas**: LangChain (200+) > LlamaIndex (RAG-foco) > Haystack > DSPy.
3. **Stateful agents** (long-running, human-in-the-loop): LangGraph é a referência atual.
4. **Eval-driven**: DSPy é único framework com otimização automática de prompt.
5. **Observabilidade**: todos integram com Langfuse/Phoenix/LangSmith via OTel ou callbacks; LangSmith é "casa" da LangChain.

## Fontes

- LangChain stats e modularização: <https://www.morphllm.com/llm-frameworks>
- RAG frameworks 2026: <https://aimultiple.com/rag-frameworks>
- LangChain vs LlamaIndex 2026: <https://zenvanriel.com/ai-engineer-blog/langchain-vs-llamaindex-2026-update/>
- Haystack 2.x: <https://haystack.deepset.ai/>
- DSPy: <https://dspy.ai/>
- Semantic Kernel: <https://learn.microsoft.com/en-us/semantic-kernel/>
- Spring AI: <https://docs.spring.io/spring-ai/reference/>
