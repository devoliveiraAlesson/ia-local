# Storage — Modelos, Datasets, Vector Store, Logs

> Etapa 4/5 da proposta. Recomendações de storage para cada categoria de dado de uma plataforma de IA local.

## 1. Categorias de dado (perfil e volumes típicos)

| Categoria | Volume típico | Padrão de acesso | Latência tolerada | Persistência |
|-----------|---------------|-------------------|--------------------|--------------|
| **Modelos (checkpoints)** | 1–5 TB por modelo (Llama 70B FP16 ≈ 140 GB; 405B FP16 ≈ 800 GB) | leitura intensa em load, raro depois | 50–500 MB/s no boot | meses/anos |
| **KV-cache (transient)** | 100 GB–10 TB ativo | leitura/escrita constante por GPU | sub-µs (DRAM/HBM) | minutos |
| **Datasets fine-tune** | 100 GB–10 TB | leitura sequencial em treino | 10+ GB/s agregado | versões mantidas |
| **Vector store** | 50 GB–10 TB | random read intenso | 1–10 ms p99 | persistente, snapshot |
| **Documentos RAG (fonte)** | 100 GB–10 TB | append + leitura ocasional | 100 ms aceitável | longo prazo |
| **Logs prompts/respostas** | 10–500 GB/mês | write-heavy, leitura analítica | append rápido | regulada (anos) |
| **Imagens/containers** | 10–100 GB | leitura no deploy | seg | versões |
| **Backups** | 2–5× dados primários | cold | minutos a horas | anos |

## 2. Mapeamento categoria → tecnologia

| Categoria | Recomendação primária | Alternativa | Justificativa |
|-----------|------------------------|-------------|---------------|
| **Modelos quentes (em uso)** | NVMe local (Gen4/Gen5) por nó GPU | Weka/VAST/GPFS via 100G+ | Carregar 140 GB do disco local em ~40s vs ~3min via 25G |
| **Modelos frios (catálogo)** | MinIO / Ceph / S3-compatible on-prem | NFS de alto desempenho | Imutável, versionado, replicado |
| **KV-cache spill** | NVMe local (Gen5 NVMe-oF aceitável) | RAM | vLLM offload p/ NVMe quando KV excede VRAM |
| **Datasets de treino** | Weka, VAST, IBM Storage Scale (GPFS), Pure FlashBlade//E | DDN ExaScaler, Lustre tradicional | Throughput agregado para 8–32 GPUs simultâneas |
| **Vector store dados** | NVMe local distribuído (Qdrant/Milvus storage) | NVMe-oF | Latência de query crítica |
| **Vector store snapshot** | MinIO / S3 | NFS | Backup periódico |
| **Documentos RAG** | MinIO / Ceph (object) | SharePoint / OneDrive (com conector) | Imutável, ACL nativa |
| **Logs WORM** | MinIO Object Lock, IBM Cloud Object Storage WORM, Veritas | Azure Blob immutable | Compliance regulado (LGPD, HIPAA, SOX) |
| **Backups** | Veeam / Cohesity / Rubrik para K8s | Snapshot Velero | Imutabilidade de backup obrigatória |

## 3. Storage paralelo — comparativo (mai/2026)

| Solução | Modelo | Performance pico | Strengths | Trade-off | Caso público |
|---------|--------|-------------------|-----------|-----------|--------------|
| **Weka** | Software-defined em NVMe | 1+ TB/s lido em cluster | Mais rápido para small file e metadata; multi-protocol (POSIX/S3/NFS); GPUDirect Storage maduro | Requer NVMe denso; licença por capacidade efetiva | Stripe, Preferred Networks, vários SuperPODs |
| **VAST Data** | Disaggregated shared everything (DASE) | 1+ TB/s | Custo/TB melhor que Weka em escala; QLC + storage class memory; arquitetura "todo flash"; NVMe-oF nativo | Vendor único, lock-in arquitetural | NVIDIA NCP, CoreWeave, Lambda |
| **IBM Storage Scale (GPFS)** | Paralelo distribuído tradicional | TB/s em escala | Maturidade HPC, suporte enterprise IBM | Complexo de operar; stack IBM | Mayo Clinic (parcial), Coreweave, supercomputers |
| **Pure FlashBlade //E** | Object + file unificado all-flash | 600+ GB/s | Plug-and-play, suporte enterprise, baixa carga operacional | Custo/TB mais alto que VAST | Várias FSI tier-2 |
| **DDN AI400X / EXAScaler** | Lustre paralelo | TB/s | Líder HPC histórico; integração com Slurm | Complexidade Lustre; melhor em treino que inferência | Akamai/NVIDIA SuperPODs |
| **Ceph (RBD/CephFS/RGW)** | Open source distribuído | 100s GB/s | Open source, sem licença; multi-protocol | Operação não-trivial; latência maior | Universidades, governo (sem orçamento Weka/VAST) |
| **MinIO** | Object S3-compatible OSS | 100+ GB/s read | Simples, Kubernetes-native, S3-compat | Não é POSIX; não substitui Weka p/ treino | Bloomberg, vários on-prem médios |
| **NFS (NetApp / Pure / Dell PowerScale)** | NAS tradicional | 10–80 GB/s | Familiar, integrado com diretório | Não escala para frontier; latência | Empresas com PowerScale legado |

## 4. Storage por porte

### Porte P (Pequeno, 4–8 GPUs)

```
   ┌───────────────────────────────────────┐
   │ Servidor GPU                          │
   │  - 4× 7.68 TB NVMe Gen4 (RAID 10)     │
   │    => 15 TB usável                    │
   │  - Modelos quentes locais             │
   │  - KV-cache overflow                  │
   └───────────────────┬───────────────────┘
                       │ 100G Eth
                       ▼
   ┌───────────────────────────────────────┐
   │ MinIO single-tier (3 nós, 50 TB total)│
   │  - Modelos frios                      │
   │  - Datasets pequenos                  │
   │  - Documentos RAG                     │
   │  - Snapshots Qdrant                   │
   │  - Logs WORM (Object Lock)            │
   └───────────────────────────────────────┘
   Vector store: Qdrant single-node, NVMe local
```

CAPEX storage: **US$ 30–60k**.

### Porte M (Médio, 16–24 GPUs)

```
   ┌─────────────────┐  ┌─────────────────┐
   │ HGX node 1      │  │ HGX node 2      │
   │ 30 TB NVMe      │  │ 30 TB NVMe      │
   └────────┬────────┘  └────────┬────────┘
            │ 200G IB/Spectrum-X │
            ▼                    ▼
   ┌──────────────────────────────────────┐
   │ Parallel FS (opção A): Weka 200 TB    │
   │ ou (opção B): MinIO 300 TB + NFS Pure│
   │  - Datasets fine-tune                 │
   │  - Modelos catálogo                   │
   │  - Logs ativos                        │
   └──────────────────────────────────────┘
   ┌──────────────────────────────────────┐
   │ Object cold tier 500 TB (Ceph/MinIO) │
   │  - WORM logs LGPD/HIPAA              │
   │  - Backups                           │
   └──────────────────────────────────────┘
   Vector store: Qdrant cluster 3 nós, NVMe distribuído
```

CAPEX storage: **US$ 200–400k**.

### Porte G (Grande, 80+ GPUs)

```
   Múltiplos racks HGX com NVMe local denso
            │
            │ NDR 400G IB ou Spectrum-X
            ▼
   ┌──────────────────────────────────────┐
   │ Parallel FS Tier 0 (hot)             │
   │ Weka/VAST 500 TB–2 PB                │
   │ GPUDirect Storage habilitado         │
   └──────────────────────────────────────┘
   ┌──────────────────────────────────────┐
   │ Object Tier 1 (warm) 1–5 PB          │
   │ Ceph ou IBM Storage Fusion           │
   └──────────────────────────────────────┘
   ┌──────────────────────────────────────┐
   │ Object Tier 2 (cold/WORM) 5–50 PB    │
   │ MinIO Object Lock + tape (opcional)  │
   │ Veeam / Cohesity para backup         │
   └──────────────────────────────────────┘
   Vector store: Milvus cluster 6+ nós, NVMe local
```

CAPEX storage: **US$ 1,5–6 M**.

## 5. Vector store — capacity planning

| Métrica | Cálculo | Exemplo (Cenário M, 100M tokens) |
|---------|---------|-----------------------------------|
| Tokens indexados | dado | 100.000.000 |
| Chunks (≈350 tok/chunk) | tokens / 350 | 285.000 chunks |
| Bytes/chunk em vector (1024-dim float16) | 1024 × 2 = 2.048 B + payload ~2KB | 4 KB |
| Volume bruto | chunks × bytes | ~1,1 GB |
| Replicação=2 + índice HNSW + payload | × ~5 | ~5 GB |
| RAM recomendada | 1,5× volume índice quente | ~8 GB |
| **NVMe recomendado** | 10–50× volume bruto p/ growth | 100–500 GB por nó |

Em 1B tokens (Cenário G): índice ~50 GB, RAM 80 GB por nó, NVMe 1 TB por nó.

## 6. KV-cache — sizing

KV-cache cresce com **batch size × seq length × n_layers × hidden_dim × 2 (K+V) × bytes/elem**.

Exemplos (Llama 3.3 70B, FP16, 80 layers, hidden 8192):
- 1 sequência de 4k tokens: ~2,6 GB
- 32 sequências concorrentes 4k: ~83 GB (não cabe em 1× H100 80GB junto com o modelo!)
- Solução: vLLM PagedAttention + offload NVMe (CPU/CXL/NVMe-oF) ou TP=2 para distribuir cache.

**NVMe local Gen5** (100+ GB/s) é crítico para KV-cache spill em 70B+. Servidores HGX devem ter 30 TB NVMe.

## 7. Mirror local de Hugging Face

Crítico para air-gap. Opções:

| Solução | Modelo | Quando |
|---------|--------|--------|
| **Hugging Face Hub Enterprise (on-prem)** | Comercial, suporte HF | Empresa que paga assinatura HF |
| **JFrog Artifactory (HF repo type)** | Repo já existente | Já tem Artifactory para Maven/npm |
| **Sonatype Nexus Repository (raw / proxy)** | Já existente | Idem para Nexus |
| **MinIO mirror manual via huggingface-cli download** | Custo zero | POC / pequeno |
| **OCI registry com modelos como artifacts** | Harbor + ORAS | Empresa que padronizou OCI |

**Boas práticas**:
- Whitelisting de modelos: só baixa quem está aprovado pelo time de IA Governance.
- Verificação SHA256 + assinatura Cosign quando possível.
- Scan de segurança antes de promover (Garak, ProtectAI Guardian, PyRIT, ModelScan).
- Retenção indefinida das versões em produção; nunca confiar em "latest".

## 8. Logs WORM (compliance)

Casos onde logs **devem** ser imutáveis:
- Saúde HIPAA (logs de acesso PHI).
- Banco/Financeiro (audit trail SOX/PCI/CVM).
- Jurídico (logs com peso probatório).
- LGPD Art. 37 (registro das operações de tratamento).

Tecnologias:
- **MinIO Object Lock (governance/compliance modes)** — open source, S3-compatible.
- **IBM Cloud Object Storage on-prem (immutable)**.
- **Veritas NetBackup com WORM**.
- **Dell ECS / PowerScale SmartLock**.
- **NetApp SnapLock**.

Retenção típica: **5 anos** (LGPD/HIPAA/SOX padrão), **10 anos** (jurídico/contratual).

Volume estimado: **~1 GB/dia em chat médio (5k usuários, prompts+respostas com metadados)**, escalando para 50–100 GB/dia em casos G.

## 9. GPUDirect Storage (GDS) — quando ativar

GDS permite NVMe → GPU direto, bypass de CPU/DRAM:

- **Vantagem real em**: load de modelo grande (405B), datasets de treino multi-TB, fine-tune frequente.
- **Pouco ganho em**: inferência steady-state (modelo já em VRAM).
- **Pré-requisitos**: NVIDIA Magnum IO ativado, Weka/VAST/GPFS com suporte GDS.
- **Recomendação**: ativar em Cenário G; opcional em M.

## 10. Backup e versionamento

| Categoria | Estratégia | Frequência | Retenção |
|-----------|-----------|------------|----------|
| Modelos (checkpoints prod) | snapshot + cópia object cold | a cada release | indefinida (3 últimas versões mín.) |
| Vector store | snapshot Qdrant/Milvus + cópia | diário | 30 dias quente, 1 ano cold |
| Postgres (Langfuse, RBAC) | pg_dump + WAL archive | hora em hora | 30 dias / PITR 7 dias |
| Logs WORM | nativo imutável | streaming | 5–10 anos |
| Configs K8s (ArgoCD/Flux) | git repository (já versionado) | commit | indefinida |

## 11. Estimativa de storage por cenário

| Cenário | NVMe local total | Object storage on-prem | Parallel FS | Custo total estimado |
|---------|-------------------|------------------------|-------------|----------------------|
| **P** | 15 TB | 50 TB | (não) | US$ 30–60k |
| **M** | 100 TB | 300 TB + 500 TB cold | 200 TB Weka opcional | US$ 200–500k |
| **G** | 500 TB+ | 5 PB+ | 1 PB Weka/VAST | US$ 2–8 M |

## Referências

- Weka NVIDIA reference architecture: <https://www.weka.io/solutions/ai/>
- VAST Data AI: <https://www.vastdata.com/solutions/ai>
- IBM Storage Scale (GPFS): <https://www.ibm.com/products/storage-scale>
- Pure FlashBlade //E: <https://www.purestorage.com/products/file-and-object/flashblade.html>
- MinIO on-prem AI: <https://min.io/solutions/object-storage-for-ai>
- Hugging Face Enterprise: <https://huggingface.co/enterprise>
- NVIDIA GPUDirect Storage: <https://docs.nvidia.com/gpudirect-storage/>
- Veeam Kasten K10 (K8s backup): <https://www.kasten.io/>
