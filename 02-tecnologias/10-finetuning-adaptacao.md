# Fine-tuning e Adaptação de Modelos (2026)

> Quando RAG não basta e é preciso ensinar um modelo a falar como a empresa, conhecer terminologia, ou mudar comportamento. Em 2026 o método dominante é **LoRA/QLoRA** (parameter-efficient) sobre modelo base aberto, com **InstructLab** ganhando tração para skills incrementais sem PhD em ML.

## Quando fazer fine-tuning vs RAG

| Cenário | RAG | Fine-tuning |
|---------|-----|-------------|
| Conhecimento factual atualizável | **Sim** | Não (cara para atualizar) |
| Estilo / tom corporativo | Parcial (system prompt) | **Sim** |
| Vocabulário/jargão técnico | Parcial | **Sim** |
| Formato de saída (JSON específico) | Parcial (function calling) | **Sim** (DPO/ORPO) |
| Compliance / segurança | RAG + guardrails | Fine-tune com dados aprovados |
| Custos contínuos | Inferência apenas | Treino + inferência |
| Velocidade de iteração | Rápida (re-indexa) | Lenta (re-treina) |

**Padrão observado**: 80% dos casos resolvem com RAG + bom prompt; 20% se beneficiam de fine-tune leve (LoRA) sobre o modelo base.

## Métodos de adaptação

| Método | O que faz | Custo | Quando |
|--------|-----------|-------|--------|
| **Few-shot / system prompt** | Exemplos no prompt | Zero treino | Primeira tentativa |
| **RAG** | Recuperar contexto | Operacional | Fatos atualizáveis |
| **Prompt tuning / soft prompts** | Aprende embeddings de prompt | Baixo | Raro hoje |
| **LoRA** (Low-Rank Adaptation) | Adiciona matrizes baixo-rank treináveis | Médio (1-10% params) | Padrão atual |
| **QLoRA** | LoRA sobre modelo quantizado 4-bit | Baixo (consumer GPU) | Padrão para single-GPU |
| **DoRA** | Decomposed LoRA (magnitude + direction) | Médio | Versão melhorada |
| **Full fine-tuning (SFT)** | Treina todos os pesos | Alto (multi-H100) | Qualidade máxima |
| **Continued pre-training** | Mais texto de domínio antes de SFT | Muito alto | Reorientação profunda |
| **DPO** (Direct Preference Optimization) | Alinha sem reward model | Médio | Estilo / preferências |
| **IPO / KTO / ORPO** | Alternativas a DPO | Médio | Variantes estabilidade |
| **GRPO** (Group Relative Policy Opt.) | RL leve, popularizado por DeepSeek-R1 | Médio-alto | Reasoning |
| **InstructLab LAB** | Síntese de dados + SFT em fases | Médio | Skills incrementais sem ML deep |

## Frameworks principais

### Tabela-resumo

| Tool | O que é | LoRA/QLoRA | Multi-GPU | Métodos avançados | Licença | Stars |
|------|---------|-----------|-----------|-------------------|---------|-------|
| **Axolotl** | Framework YAML-driven; padrão de fato OSS | Sim | Sim (FSDP, DeepSpeed) | DPO, IPO, KTO, ORPO, GRPO, GDPO, GPTQ, QAT | Apache 2.0 | 9k+ |
| **Unsloth** | Otimização extrema single-GPU; até 2× mais rápido, ~70% menos VRAM | Sim (foco) | Pro (paga) | LoRA, DPO | Apache 2.0 | 35k+ |
| **HF PEFT** | Lib HF de parameter-efficient | Sim | Sim (com Accelerate) | LoRA, prefix tuning, P-tuning | Apache 2.0 | 17k+ |
| **HF TRL** | Treinamento com reinforcement | Via PEFT | Sim | SFT, DPO, GRPO, RLOO, ORPO, KTO | Apache 2.0 | 13k+ |
| **InstructLab** | Síntese + SFT em fases (LAB method) | Sim (via Unsloth backend) | Sim | LAB skills | Apache 2.0 | 6k+ |
| **LLaMA-Factory** | UI/CLI alternativa, Chinese-origin | Sim | Sim | DPO, ORPO, etc. | Apache 2.0 | 35k+ |
| **TorchTune** | PyTorch-native, recipes simples | Sim | Sim | DPO | BSD-3 | 5k+ |
| **NVIDIA NeMo Customizer** | Parte do NVIDIA NeMo | Sim | Multi-GPU/multi-nó | Vários | NeMo (Apache+) | (parte) |
| **Mosaic AI Pretraining/Foundation Model Tuning** | Databricks | Sim | Sim | SFT, RLHF | Comercial | — |
| **OpenRLHF / verl** | RLHF distribuído escalável | Sim | Sim (Ray) | PPO, GRPO | Apache 2.0 | — |

### Detalhamento

#### Axolotl
- **O que é**: framework YAML que abstrai HF Trainer; reusa o mesmo config para SFT, LoRA, QLoRA, DPO, etc.
- **Backends**: integra **Unsloth** para acelerar single-GPU; FSDP / DeepSpeed para multi-GPU.
- **Quando usar**: padrão de fato; melhor coverage de métodos.
- Links: <https://github.com/axolotl-ai-cloud/axolotl> · <https://docs.axolotl.ai/>

#### Unsloth
- **O que é**: kernel-level rewrite (Triton kernels) para fine-tune em single GPU; ~2× mais rápido, 70% menos VRAM que padrão HF.
- **Limites**: free é single-GPU (multi-GPU é Unsloth Pro pago).
- **Quando usar**: laptop / 1× consumer GPU (4090, 5090, A100 80G).
- Links: <https://github.com/unslothai/unsloth> · <https://unsloth.ai/>

#### HF PEFT + TRL
- **PEFT**: implementações de referência de LoRA, DoRA, IA³, prefix-tuning.
- **TRL**: Trainer wrappers para SFT, DPO, GRPO, ORPO, KTO, RLOO.
- **Quando usar**: stack HF custom; controle máximo.
- Links: <https://github.com/huggingface/peft> · <https://github.com/huggingface/trl>

#### InstructLab
- **O que é**: método **LAB** (Large-scale Alignment for chatBots) da IBM/Red Hat. Combina:
  1. **Taxonomia** de skills (knowledge + skills) em YAML.
  2. **Geração sintética** de dados via "teacher model" (Mixtral, Granite).
  3. **SFT em fases** (knowledge phase + skills phase) sobre modelo base (Granite, Llama, Mistral).
- **Vantagem**: SMEs sem expertise ML contribuem com YAML; pipeline reproduzível.
- **Quando usar**: empresa Red Hat / Granite-house; áreas reguladas onde a "rastreabilidade da fonte de cada skill" importa.
- Links: <https://github.com/instructlab/instructlab> · <https://instructlab.ai/>

#### LLaMA-Factory
- Alternativa a Axolotl com UI WebUI; popular comunidade chinesa.
- Links: <https://github.com/hiyouga/LLaMA-Factory>

#### TorchTune (PyTorch oficial)
- "Recipes" PyTorch-puras, sem dependência externa pesada. Reusa torchao para quantização.
- Links: <https://github.com/pytorch/torchtune>

#### NVIDIA NeMo Customizer
- Parte do NVIDIA AI Enterprise; finetune e tune-as-a-service em DGX Cloud ou on-prem.
- Links: <https://docs.nvidia.com/nemo-framework/user-guide/latest/customize/index.html>

#### OpenRLHF / verl
- Frameworks distribuídos para RLHF/GRPO em escala; preferidos para reproduzir DeepSeek-R1.
- Links: <https://github.com/OpenRLHF/OpenRLHF> · <https://github.com/volcengine/verl>

## Métodos de alinhamento (DPO e variantes)

| Método | Princípio | Vantagem | Quando usar |
|--------|-----------|---------|-------------|
| **RLHF (PPO)** | Reward model + RL | Clássico (ChatGPT) | Pesquisa; complexidade alta |
| **DPO** | Otimiza diretamente preferências (sem reward model) | Simples, estável | Default 2024-25 |
| **IPO** | Variante DPO contra overfitting | Estável | Datasets pequenos |
| **KTO** | Usa só "thumbs up/down" (não pares) | Aceita feedback simples | Telemetria de produção |
| **ORPO** | Combina SFT + DPO em um passo | Mais rápido | One-shot training |
| **GRPO** | RL leve sem critic, popular em reasoning | Escalável; deu DeepSeek-R1 | Reasoning / math |
| **SimPO** | Variante DPO simplificada | Variante recente | Comparações |

## Workflow recomendado para empresa

```
1. Modelo base: Granite 4 / Llama 3.3 / Qwen 3 (Apache/MIT preferíveis)
2. Dados: curados, com ACL e versionamento (DVC, LakeFS)
3. SFT inicial: LoRA/QLoRA via Axolotl ou InstructLab
4. (Opcional) DPO/ORPO com pares de preferência humanos ou via LLM-as-judge
5. Avaliação: Ragas (RAG), DeepEval, conjunto interno de regressão
6. Quantização: AWQ INT4 ou FP8 (LLM Compressor / AutoAWQ / Quanto)
7. Deploy: vLLM/SGLang com adapters LoRA carregados (vLLM suporta multi-LoRA)
8. Monitoramento: Langfuse + métricas drift
```

## Hardware típico para fine-tune

| Setup | LoRA 7B | LoRA 70B | Full SFT 7B | Full SFT 70B |
|-------|---------|----------|-------------|--------------|
| 1× RTX 4090 24GB | QLoRA OK | Não | Não | Não |
| 1× A100 80GB | LoRA OK | QLoRA OK | OK (com FSDP) | Não |
| 4× H100 80GB | OK | LoRA OK | OK | QLoRA OK |
| 8× H100 80GB | OK | OK | OK | OK |
| 16× H100 + InfiniBand | — | — | — | OK rápido |

(LoRA típico = 1-2% dos params como adapter; QLoRA = LoRA sobre base 4-bit.)

## Armadilhas

- **Catastrophic forgetting**: SFT mal feito apaga capacidades gerais. Solução: data mixing com instructions gerais; LoRA com rank baixo (8-16); manter eval geral.
- **Licenças de modelo bloqueiam treino**: Llama 3 Community License **proíbe usar outputs do Llama para treinar modelos não-Llama**. Codestral MNPL bloqueia uso comercial até de derivados. Auditar antes.
- **Synthetic data licensing**: dados gerados por GPT-4/Claude têm Terms of Service que proíbem treino de modelos competidores. InstructLab gera com Mixtral/Granite (Apache) para evitar isso.
- **Drift**: re-avaliar após cada release do base model; adapters LoRA podem precisar retraining.

## Fontes

- Red Hat Unsloth + Training Hub: <https://developers.redhat.com/articles/2026/04/01/unsloth-and-training-hub-lightning-fast-lora-and-qlora-fine-tuning>
- Axolotl: <https://github.com/axolotl-ai-cloud/axolotl>
- Axolotl docs: <https://docs.axolotl.ai/>
- Unsloth: <https://unsloth.ai/>
- HF PEFT: <https://huggingface.co/docs/peft>
- HF TRL: <https://huggingface.co/docs/trl>
- InstructLab: <https://instructlab.ai/>
- TorchTune: <https://pytorch.org/torchtune/>
- LLaMA-Factory: <https://github.com/hiyouga/LLaMA-Factory>
- Axolotl vs Unsloth vs TorchTune 2026: <https://www.spheron.network/blog/axolotl-vs-unsloth-vs-torchtune/>
- vLLM multi-LoRA serving: <https://docs.vllm.ai/en/stable/features/lora.html>
