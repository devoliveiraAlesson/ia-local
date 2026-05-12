# Redes — Topologias e Fabric (InfiniBand vs Spectrum-X vs RoCEv2)

> Etapa 4/5 da proposta. Decisões de network fabric por porte e por tipo de paralelismo.

## 1. Por que rede importa em IA local

A latência de rede entre GPUs é o **gargalo dominante** quando:
- Tensor parallel cruza o limite de 1 servidor (mais de 8 GPUs por modelo).
- Pipeline parallel é usado (modelos > 200B).
- Disaggregated serving (vLLM disagg, llm-d) separa **prefill** de **decode** em nós diferentes.
- Storage paralelo (Weka/VAST/GPFS) precisa alimentar 8–32 GPUs simultaneamente.

Para inferência **single-node 8-GPU**, NVLink intra-servidor resolve. **A rede começa a importar de verdade quando se passa de 1 servidor para múltiplos.**

## 2. Hierarquia de interconnect

```
Mais rápido / mais caro                                Mais lento / mais barato
─────────────────────────────────────────────────────────────────────────────
NVLink 5 (1,8 TB/s)         > NVLink 4 (900 GB/s)
   |
   |  (intra-servidor / intra-rack NVL72)
   ▼
InfiniBand NDR (400 Gbps)   > IB HDR (200G)            > IB EDR (100G)
   |
   |  (inter-servidor scale-out, RDMA nativo)
   ▼
Spectrum-X 400G Ethernet    > RoCEv2 400G              > RoCEv2 100G
   |                          (Ethernet com RDMA, lossless via PFC/ECN)
   ▼
Ethernet padrão 100G/25G    (storage e gerenciamento)
```

## 3. Comparativo principal

| Tecnologia | Bandwidth | Latência típica | RDMA | Lossless | Custo relativo | Maturidade vLLM/SGLang | Ideal para |
|-----------|-----------|------------------|------|----------|----------------|-------------------------|-------------|
| **NVLink 4** (H100/H200) | 900 GB/s GPU↔GPU | ~1 µs | nativo | sim | incluso na GPU | total | Tensor parallel intra-servidor |
| **NVLink 5** (B100/B200/GB200) | 1,8 TB/s GPU↔GPU | <1 µs | nativo | sim | incluso na GPU | total | Tensor parallel intra-servidor / NVL72 |
| **NVSwitch + NVLink Switch System** | 14,4 TB/s agregado em GB200 NVL72 | <1 µs | nativo | sim | rack-scale (~120 kW) | total (rack-scale) | 405B+ frontier |
| **InfiniBand HDR (200G)** | 200 Gbps por porta | ~1,5 µs | nativo (RC) | sim | alto (US$ 1k+/porta) | total | Médio porte (16–64 GPUs) |
| **InfiniBand NDR (400G)** | 400 Gbps por porta | <1 µs | nativo (RC) | sim | muito alto | total | Grande porte / SuperPOD |
| **InfiniBand XDR (800G)** | 800 Gbps por porta | <1 µs | nativo | sim | premium | inicial (mai/2026) | Frontier (B200/GB200) |
| **NVIDIA Spectrum-X (Ethernet 400/800G)** | 400/800 Gbps | ~1,5 µs | RoCEv2 com adaptive routing | sim (PFC + congestion control NVIDIA) | alto, < IB | total, otimizado para IA | Grande porte preferindo Ethernet |
| **RoCEv2 400G (Mellanox/Broadcom/Cisco "AI fabric")** | 400 Gbps | ~2 µs | RoCEv2 | configurável (PFC) | médio-alto | total | Médio-grande porte com Ethernet existente |
| **RoCEv2 100G** | 100 Gbps | ~2,5 µs | RoCEv2 | configurável | médio | total | Pequeno-médio porte; storage |
| **Ethernet padrão 25/100G** | 25–100 Gbps | ~5–10 µs | TCP/IP (sem RDMA) | não | baixo | n/a (gerenciamento) | Plano de controle, gerência |

## 4. Topologias por porte

### 4.1 Single-node (1 servidor 4–8 GPUs) — Cenários P/M

```
   ┌──────────────────────────────────────────────────────┐
   │            Servidor HGX 8-GPU (DGX H100/H200)        │
   │                                                      │
   │    GPU0 ◄──NVLink──► GPU1   GPU2 ◄──NVLink──► GPU3   │
   │     ▲                  ▲     ▲                  ▲    │
   │     │   NVSwitch full mesh (900 GB/s)           │    │
   │     ▼                  ▼     ▼                  ▼    │
   │    GPU4 ◄──NVLink──► GPU5   GPU6 ◄──NVLink──► GPU7   │
   │                                                      │
   │      NIC: 2× 200G IB ou 2× 100G Ethernet             │
   └──────────────────────────────────────────────────────┘
              │                              │
              ▼                              ▼
   ┌────────────────────┐          ┌────────────────────┐
   │ Storage 100G eth   │          │ Cliente / gateway  │
   │ MinIO/NFS          │          │ via 25/100G        │
   └────────────────────┘          └────────────────────┘
```

**Recomendação P**: Ethernet 25/100G é suficiente. NVLink interno cuida do tensor parallel.
**Recomendação M (1 servidor 8-GPU)**: 2× 200G IB ou Spectrum-X já como preparação para crescer.

### 4.2 Multi-node 2–8 servidores (16–64 GPUs) — Cenário M-G

```
        ┌──────────────────────────────────────────────────────────┐
        │              IB NDR 400G ou Spectrum-X 400G              │
        │              (spine-leaf, non-blocking ou 2:1)           │
        └────┬───────────────┬───────────────┬───────────────┬─────┘
             │               │               │               │
        ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
        │ HGX node │    │ HGX node │    │ HGX node │    │ HGX node │
        │ 8× H200  │    │ 8× H200  │    │ 8× H200  │    │ 8× H200  │
        │ 8× NIC   │    │ 8× NIC   │    │ 8× NIC   │    │ 8× NIC   │
        └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

**Recomendação**: 1 NIC IB/Eth por GPU (8× 200G ou 8× 400G). Topologia spine-leaf não-bloqueante para melhor coletivo.

### 4.3 Tensor parallel cross-node (modelos > 8 GPUs)

- 70B AWQ cabe em 2× H100 (TP=2). Não precisa de cross-node.
- 405B FP8 cabe em 8× H200 (TP=8). **Pode** ficar single-node.
- 405B FP16 ou DeepSeek-V3 671B requerem 16+ GPUs ⇒ cross-node ⇒ **InfiniBand NDR ou Spectrum-X obrigatório**.

### 4.4 Pipeline parallel — Ethernet 100/400G aceitável?

- Pipeline parallel tem **muito menos comunicação** que tensor parallel (apenas activations entre estágios).
- **Ethernet 100G RoCEv2 é aceitável** para pipeline parallel em treinamento/inferência de modelos muito grandes.
- TP+PP combinado: TP intra-nó (NVLink), PP inter-nó (RoCE/IB). Esquema clássico de Megatron-LM e DeepSpeed.

### 4.5 Disaggregated serving (vLLM disagg / llm-d / SGLang)

- Separa **prefill (computação)** e **decode (memória)** em pools diferentes.
- Transfere KV-cache entre pools via rede ⇒ **bandwidth alta obrigatória** (200G mínimo, 400G recomendado).
- **NIXL (NVIDIA Inference Xfer Library)** otimiza essa transferência sobre InfiniBand/Spectrum-X.
- Faz sentido **a partir de 32 GPUs** com cargas mistas (chat curto + sumarização longa).

## 5. InfiniBand vs Spectrum-X vs RoCEv2 — quando escolher

| Fator | InfiniBand (NDR/XDR) | Spectrum-X (NVIDIA Ethernet) | RoCEv2 puro (Mellanox/Broadcom/Cisco/Arista) |
|-------|----------------------|------------------------------|------------------------------------------------|
| Latência mínima | melhor | quase igual | um pouco pior |
| Bandwidth | até 800G XDR | até 800G | até 800G |
| Adaptive routing | sim | sim (NVIDIA proprietário) | parcial (depende do switch) |
| Custo | mais caro | médio-alto | mais barato |
| Operadores familiarizados | rede HPC | rede DC moderna | rede DC tradicional |
| Lock-in NVIDIA | sim (compra Mellanox→NVIDIA) | sim | menor (multi-vendor) |
| Multi-tenant fácil | médio | médio | melhor (VLAN/EVPN) |
| Casos públicos | Mayo DGX SuperPOD, Meta RSC, Microsoft GB200 | xAI Colossus, novos GB200 NVL72 | Meta Grand Teton (escala muito grande), AWS HyperPlane |
| Recomendação | **Frontier scale, treino crítico** | **Grande porte preferindo Ethernet** | **Médio porte com rede Ethernet existente** |

### Regras práticas

- **Até 16 GPUs (2 servidores)**: 200G IB ou 400G RoCE indistinguível na prática.
- **16–64 GPUs**: NDR IB 400G ou Spectrum-X 400G valem o investimento.
- **64+ GPUs (Frontier)**: NDR/XDR IB ainda lidera; Spectrum-X é alternativa séria; RoCE puro vira dor sem time HPC dedicado.

## 6. Bandwidth de rede por GPU (regra de bolso)

| Workload | Bandwidth recomendada por GPU |
|----------|-------------------------------|
| Inferência single-node TP | NVLink interno + 25–100G saída |
| Inferência multi-node TP | 200G por GPU mínimo |
| Inferência disaggregated | 400G por GPU |
| Treino full-pretrain frontier | 400G–800G por GPU + topologia rail-optimized |
| Fine-tune QLoRA 70B | 100G por GPU suficiente |
| Storage feed (treino) | 200G+ entre nó e parallel FS |

## 7. Topologia de referência — 4 servidores HGX H200 (Cenário M-G)

```
                  ┌───────────────────────────────────────┐
                  │  Spine: 2× NVIDIA QM9700 (NDR 400G)   │
                  │  ou 2× SN5400 (Spectrum-X 400G)       │
                  └───┬───────────────┬───────────────┬───┘
                      │               │               │
            ┌─────────┴──┐   ┌────────┴───┐   ┌───────┴────┐
            │ Leaf 1     │   │ Leaf 2     │   │ Leaf 3     │
            │ 32× 400G   │   │ 32× 400G   │   │ 32× 400G   │
            │ (rack 1)   │   │ (rack 2)   │   │ (rack 3)   │
            └────────────┘   └────────────┘   └────────────┘
                  │                 │                 │
            HGX 1 + HGX 2     HGX 3 + HGX 4     Storage paralelo
            (16 GPUs)         (16 GPUs)         (Weka/VAST)
```

- **Spine-leaf não-bloqueante** ou 2:1 (aceitável até 32 GPUs).
- 8 NICs por nó (1 NIC por GPU). Total: 32 NICs por rack de 16 GPUs.
- **Storage em VLAN separada** (RoCEv2 100G é suficiente).

## 8. Rede de gerenciamento (out-of-band)

- **Sempre separar**: 1 Gb Ethernet dedicado para BMC/iDRAC/iLO/IPMI + console + atualizações de firmware.
- VLAN management isolada de VLAN dados/storage/inference.
- Acesso só via bastion + MFA.

## 9. Decisões executivas

| Pergunta | Resposta para perfil corporativo médio |
|----------|----------------------------------------|
| IB ou Ethernet para o fabric de IA? | **Spectrum-X 400G** ou **RoCEv2 400G** se já existe Arista/Cisco maduro; **IB NDR** se time HPC dedicado e foco em treino. |
| Qual bandwidth por GPU? | 200G mínimo para multi-nó; 400G para Blackwell/MI355X. |
| Storage no mesmo fabric? | **Não**. VLAN dedicada (mesma fabric física, lógica separada). |
| 2:1 oversubscription aceitável? | Para **inferência puro**, sim. Para **treino**, não. |
| Lock-in NVIDIA aceitável? | Spectrum-X é, IB é. RoCEv2 multi-vendor reduz lock-in mas exige expertise. |

## Referências

- NVIDIA Spectrum-X: <https://www.nvidia.com/en-us/networking/spectrumx/>
- NVIDIA Quantum-2 InfiniBand: <https://www.nvidia.com/en-us/networking/quantum2/>
- vLLM disagg: <https://docs.vllm.ai/en/latest/features/disagg_prefill.html>
- llm-d (KServe + vLLM multi-node): <https://llm-d.ai/>
- Meta Grand Teton (RoCE): <https://engineering.fb.com/2022/10/18/open-source/ocp-summit-2022-grand-teton/>
- Cisco AI fabric: <https://www.cisco.com/site/us/en/solutions/artificial-intelligence/ai-infrastructure/index.html>
- Arista AI Networking: <https://www.arista.com/en/solutions/ai-networking>
