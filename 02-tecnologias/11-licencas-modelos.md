# Licenças de Modelos: Tabela Master e Armadilhas Comerciais (2026)

> Referência rápida para o jurídico. Foco em **uso comercial em empresa grande on-premises**. Onde a licença não é OSI-approved, a coluna "Armadilha" descreve a cláusula que mais impacta. **Não é parecer jurídico** — é mapeamento operacional.

## Resumo executivo (cores)

- **Verde (Apache 2.0 / MIT)**: uso comercial irrestrito, modificação, distribuição, derivados. Sem cláusulas de uso ou MAU.
- **Amarelo (Permissivas com cláusulas)**: uso comercial OK mas com gatilhos (MAU, atribuição, restrições por região, ISO).
- **Vermelho (Não-comercial / restritiva)**: uso comercial proibido, **ou** apenas com licença paga, **ou** restrição que pode bloquear o caso da empresa.

## Tabela master de licenças

| Modelo | Licença | Cor | Uso comercial | Armadilhas-chave | Link |
|--------|---------|-----|---------------|------------------|------|
| **Llama 3 / 3.1 / 3.2 / 3.3** | Llama Community License | Amarelo | Sim, exceto >700M MAU | (1) >700M MAU exige licença separada de Meta; (2) **Llama 3.2 Vision restrito UE**; (3) atribuição "Built with Llama"; (4) **outputs não podem treinar modelos não-Llama**; (5) AUP da Meta | <https://www.llama.com/llama3/license/> |
| **Llama 4 (Scout, Maverick, Behemoth)** | Llama 4 Community License | Amarelo | Sim, exceto >700M MAU | Mesmas de Llama 3 + (vision UE proibida) | <https://www.llama.com/llama4/license/> |
| **Qwen 2.5 (≤32B)** | Apache 2.0 | Verde | Sim | — | <https://huggingface.co/Qwen> |
| **Qwen 2.5-72B / 2.5-Math 72B** | Tongyi Qianwen License | Amarelo | Sim, com >100M MAU exige licença | Atribuição "Powered by Qwen" | <https://huggingface.co/Qwen/Qwen2.5-72B-Instruct> |
| **Qwen 3 (todos tamanhos)** | Apache 2.0 | Verde | Sim | — | <https://qwenlm.github.io/blog/qwen3/> |
| **Qwen3-Embedding / Qwen3-Reranker** | Apache 2.0 | Verde | Sim | — | <https://qwenlm.github.io/blog/qwen3-embedding/> |
| **Qwen2-VL / Qwen2.5-VL / Qwen3-VL** | Apache 2.0 (variantes <72B); checar cada modelo | Verde/Amarelo | Sim | Verificar tamanho do modelo | <https://huggingface.co/Qwen> |
| **DeepSeek V3 / V3.1 / V3.2** | MIT | Verde | Sim | Pesos MIT; código repositório também MIT | <https://github.com/deepseek-ai/DeepSeek-V3> |
| **DeepSeek R1 / R1-0528** | MIT | Verde | Sim, **inclui distillation** | — | <https://github.com/deepseek-ai/DeepSeek-R1/blob/main/LICENSE> |
| **DeepSeek-Coder V2** | DeepSeek License (custom MIT-like) | Verde | Sim | Auditar AUP | <https://github.com/deepseek-ai/DeepSeek-Coder-V2> |
| **Mistral 7B, Mixtral 8x7B/8x22B, Codestral Mamba, Mathstral, Mistral Small 3** | Apache 2.0 | Verde | Sim | — | <https://help.mistral.ai/en/articles/347393> |
| **Mistral Large 2 (24.07)** | Mistral Research License (MRL) | Vermelho | **Não** sem licença comercial paga | Apenas uso de pesquisa/teste | <https://mistral.ai/news/mistral-large-2407> |
| **Codestral 22B / 25.08** | Mistral AI Non-Production License (MNPL) | Vermelho | **Não** — proibido até uso interno em atividade comercial | "Non-Production" inclui dev de produto comercial; precisa licença paga | <https://mistral.ai/news/mistral-ai-non-production-license-mnpl/> |
| **Pixtral 12B** | Apache 2.0 | Verde | Sim | — | <https://huggingface.co/mistralai/Pixtral-12B-2409> |
| **Pixtral Large** | MRL | Vermelho | Não sem licença | — | <https://huggingface.co/mistralai/Pixtral-Large-Instruct-2411> |
| **Devstral 2 (open variant)** | Apache 2.0 (variant) / MNPL (variant) | Misto | Verificar variante | — | <https://venturebeat.com/ai/mistral-launches-powerful-devstral-2-coding-model-including-open-source> |
| **IBM Granite 3.x / 4 (todas as famílias)** | Apache 2.0 | Verde | Sim | — | <https://www.ibm.com/granite/docs/models/granite> |
| **IBM Granite-Code 3B/8B/20B/34B** | Apache 2.0 | Verde | Sim | Treinado em código permissivamente licenciado | <https://huggingface.co/ibm-granite> |
| **IBM Granite Guardian** | Apache 2.0 | Verde | Sim | — | <https://huggingface.co/ibm-granite/granite-guardian-3.2-5b> |
| **IBM Granite Embedding (English / Multilingual)** | Apache 2.0 | Verde | Sim | **Único Apache + ISO/IEC 42001** | <https://huggingface.co/ibm-granite/granite-embedding-278m-multilingual> |
| **Phi-3 / Phi-3.5 / Phi-4 / Phi-4-multimodal** | MIT | Verde | Sim | — | <https://huggingface.co/microsoft> |
| **Gemma 2 / Gemma 3** | Gemma Terms of Use | Amarelo | Sim | AUP do Google; redistribuição precisa replicar termos | <https://ai.google.dev/gemma/terms> |
| **Gemma 4** | Apache 2.0 | Verde | Sim | — | <https://ai.google.dev/gemma/docs/core> |
| **NVIDIA Nemotron** | NVIDIA Open Model License | Amarelo | Sim, com AUP NVIDIA | Verificar restrições; NIM precisa AI Enterprise | <https://huggingface.co/nvidia> |
| **NV-Embed v2 / NVLM** | NVIDIA Open Model License | Amarelo | Sim, com AUP | — | <https://huggingface.co/nvidia> |
| **StarCoder 2** (BigCode) | BigCode Open RAIL-M | Amarelo | Sim, com restrições éticas | RAIL: cláusulas de uso (no harmful, etc.); auditar AUP | <https://huggingface.co/bigcode/starcoder2-15b> |
| **BGE-M3, BGE-reranker** | MIT | Verde | Sim | — | <https://huggingface.co/BAAI> |
| **Nomic Embed Text V1.5 / V2** | Apache 2.0 | Verde | Sim | — | <https://huggingface.co/nomic-ai> |
| **E5 (intfloat/multilingual-e5-large, e5-mistral-7b-instruct)** | MIT | Verde | Sim | E5-Mistral foi treinado a partir de Mistral 7B base (Apache) | <https://huggingface.co/intfloat> |
| **Stella** | MIT | Verde | Sim | — | <https://huggingface.co/dunzhang> |
| **mxbai-embed / mxbai-rerank** | Apache 2.0 | Verde | Sim | — | <https://huggingface.co/mixedbread-ai> |
| **Jina Embeddings v3 / Reranker v2** | CC BY-NC 4.0 (modelo) ou Apache 2.0 (variantes) | Misto | Verificar | Algumas variantes são NC; usar variantes Apache | <https://huggingface.co/jinaai> |
| **Cohere Command R / R+ / Embed v4 / Rerank 3** | CC BY-NC 4.0 (open weights) | Vermelho | **Não comercial** open weights; comercial via API ou Cohere North on-prem | "Open weights" Cohere é só não-comercial; produção exige Cohere | <https://docs.cohere.com/docs/responsible-use> |
| **Llama Guard 3 / Prompt Guard 2** | Llama Community License | Amarelo | Sim, mesmas regras de Llama | — | <https://huggingface.co/meta-llama/Llama-Guard-3-8B> |
| **InternVL 3** | Apache 2.0 (variantes) | Verde | Sim | Verificar checkpoint específico | <https://huggingface.co/OpenGVLab> |
| **GLM-4 / GLM-4.6V** | GLM License | Amarelo | Sim, com AUP | Variantes têm cláusulas | <https://huggingface.co/THUDM> |

## Armadilhas detalhadas

### 1. Llama Community License — limite de 700M MAU
- A licença permite uso comercial gratuito, **exceto** se a sua organização (ou affiliates) tiver **>700M MAU** medido na data de release. Acima disso, é necessário pedir licença a Meta.
- A maioria das corporações **não atinge esse limite** (apenas Big Techs, telcos massivas, redes sociais). Mas **conglomerados** podem atingir somando empresas do grupo (telco + banco + varejo).
- **Checklist**: contar MAU consolidado do grupo na data de release do modelo.
- **Outputs do Llama**: a license proíbe usar **outputs do Llama para treinar/melhorar modelos que não sejam Llama**. Isso afeta destilação, geração sintética para fine-tune de outro base.
- **Atribuição "Built with Llama"** em produtos, documentação e UI.
- **Vision restrito UE**: Llama 3.2 Vision e Llama 4 multimodal **proibidos para licenciados domiciliados na UE**. Usar variantes text-only ou outros modelos (Qwen-VL, Pixtral 12B Apache).

### 2. Mistral — duas trilhas (Apache vs MNPL/MRL)
- **Apache 2.0**: Mistral 7B, Mixtral 8x7B/8x22B, Codestral Mamba, Mathstral, Mistral Small 3, Pixtral 12B → uso livre.
- **MNPL (Codestral 22B/25.08)**: **proibido qualquer uso "production"** — incluindo "internal usage by employees in the context of the company's business activities". Logo, **não usar Codestral em coding assistant interno** sem licença comercial paga junto à Mistral.
- **MRL (Mistral Large 2, Pixtral Large)**: **research/test only**. Para uso comercial → assinatura Mistral.
- **Recomendação**: para coding interno open, usar **Qwen 2.5/3-Coder, Granite-Code, DeepSeek-Coder V2 ou StarCoder 2**.

### 3. Cohere — open weights "para olhar"
- "Open weights" do Command R, Command R+, Embed v4, Rerank 3 são publicados sob **CC BY-NC 4.0** — **não comercial**. Para uso em produção: API Cohere ou **Cohere North** (appliance on-prem comercial).

### 4. Gemma Terms (Google)
- Não é Apache, mas é "permissiva" com AUP. Redistribuição requer replicar termos. Atribuição. **Gemma 4 voltou a Apache 2.0** — preferir Gemma 4 quando possível.

### 5. NVIDIA Open Model License
- Permite uso comercial. Com cláusulas de AUP NVIDIA (sem fins militares, etc.). Para servir via NIM, requer **NVIDIA AI Enterprise** ($4.500/GPU/ano).

### 6. StarCoder 2 — BigCode Open RAIL-M
- RAIL-M é "Responsible AI License — Modified". Permite uso comercial **com cláusulas éticas** (não pode usar para "harm by design", deepfakes maliciosos, vigilância sem consentimento, etc.).
- Auditar a cláusula 5 com jurídico.

### 7. Synthetic data via API closed
- Dados gerados por **GPT-4/Claude/Gemini** têm Terms of Service que **proíbem treinar modelos competidores**. InstructLab e a maioria dos pipelines open usam **Mixtral/Granite/Llama (Apache/MIT) como teacher**.

## Recomendações operacionais para empresa

1. **Default em projetos novos**: priorize **Apache 2.0 / MIT** (Qwen 3, DeepSeek, Granite 4, Phi 4, Gemma 4, BGE, Nomic, E5, Stella).
2. **Llama é OK para a maioria** (raramente passa de 700M MAU), mas **comprometa-se com o trabalho de atribuição** e evite Llama Vision na UE.
3. **Não use Codestral** em pipeline corporativo de coding sem licença Mistral comercial.
4. **Nunca produção em Cohere open weights** — usar API ou Cohere North.
5. **Para compliance forte (ISO 42001)**: **Granite 4** (cripto-assinado, certificado).
6. **Para fine-tune**: prefira **base Apache/MIT** para evitar herança de cláusulas restritivas no derivado.
7. **Documente em registro central**: cada modelo em produção, qual licença, qual versão, data de download, hash. Reauditar a cada release de licença.

## Fontes

- Llama 4 license: <https://www.llama.com/llama4/license/>
- Llama 3 license: <https://www.llama.com/llama3/license/>
- Royfactory Llama 4 license checklist: <https://royfactory.net/posts/ai/202512/meta-llama4-open-weights-scout-maverick-license/>
- Mistral licensing FAQ: <https://help.mistral.ai/en/articles/347393-under-which-license-are-mistral-s-open-models-available>
- Mistral MNPL: <https://mistral.ai/news/mistral-ai-non-production-license-mnpl/>
- DeepSeek R1 LICENSE: <https://github.com/deepseek-ai/DeepSeek-R1/blob/main/LICENSE>
- IBM Granite 4: <https://www.ibm.com/granite/docs/models/granite>
- Granite 4 ISO 42001: <https://digital.nemko.com/news/ibm-granite-40-first-iso-42001-certified-open-source-ai>
- Qwen 3: <https://qwenlm.github.io/blog/qwen3/>
- Gemma terms: <https://ai.google.dev/gemma/terms>
- Gemma 4 Apache: <https://ai.google.dev/gemma/docs/core>
- BigCode RAIL: <https://www.bigcode-project.org/docs/pages/bigcode-openrail/>
- Cohere AUP: <https://docs.cohere.com/docs/responsible-use>
