# Energia, Cooling e Espaço Físico

> Etapa 4/5 da proposta. Requisitos elétricos, térmicos e de ocupação para uma infraestrutura GPU corporativa em 2026.

## 1. Por que isso virou bottleneck em 2025–2026

A geração Hopper (H100) já elevou densidade de rack para faixas que muitos DCs corporativos brasileiros e europeus **não estavam preparados**. Blackwell (B200/GB200) **agrava** o problema:

- Rack DC corporativo médio (BR/EU): **8–15 kW/rack**.
- Rack típico HGX H100 8-GPU: **~10–12 kW por servidor** (rack pode ter 2–3 servidores) ⇒ **20–35 kW/rack**.
- Rack HGX B200 8-GPU: **~15 kW por servidor** ⇒ **30–45 kW/rack**.
- Rack GB200 NVL72: **~120 kW** — DCs precisam de DLC dedicado.

**Implicação**: maioria dos DCs corporativos exige **upgrade elétrico/térmico** ou **co-location em DC especializado** (Equinix, Digital Realty, Ascenty, Odata).

## 2. Consumo de energia por SKU

| GPU | TDP máx | Servidor 8-GPU TDP total (estimado, com CPU/RAM/NIC) |
|-----|---------|------------------------------------------------------|
| H100 SXM | 700 W | ~10–12 kW |
| H200 SXM | 700 W | ~10–12 kW |
| B100 SXM | 700 W | ~11–13 kW |
| B200 SXM | 1.000 W | ~14–16 kW |
| GB200 (NVL72 rack) | 2× B200 + Grace por nó | ~120 kW por rack inteiro |
| L40S | 350 W | ~3–5 kW (1U-2U servers tipicamente) |
| L4 | 72 W | ~1,5–2,5 kW |
| MI300X | 750 W | ~11–13 kW |
| MI325X | 1.000 W | ~14–16 kW |
| Gaudi 3 | 900 W | ~12–14 kW |

## 3. Densidade de rack

| Cenário | kW por rack | Tecnologia recomendada |
|---------|-------------|------------------------|
| Inferência leve (4× L40S) | 8–12 kW | ar tradicional (raised floor + CRAC) |
| Inferência média (2× HGX H100) | 20–30 kW | ar reforçado (rear-door heat exchanger — RDHx) |
| Inferência pesada (3× HGX H100) | 30–40 kW | RDHx ou DLC adoçado |
| Blackwell HGX (1–2× HGX B200) | 30–50 kW | **DLC frequentemente obrigatório** |
| GB200 NVL72 | 100–130 kW | **DLC obrigatório** + chiller tower nova |

## 4. Cooling — opções

### 4.1 Ar tradicional

- Limita-se a ~15 kW/rack na prática (alguns DCs declaram 20 kW mas com cuidados especiais).
- Aceitável para servidores L40S, HGX 1-2 GPU, embedding clusters.
- **Não viável para HGX 8-GPU pleno** sem reforço.

### 4.2 Rear-Door Heat Exchanger (RDHx)

- Porta traseira do rack com trocador de calor água/ar.
- Estende ar até **30–40 kW/rack**.
- Requer **chilled water loop** próximo (8–10°C).
- Custo: **US$ 8–15k/rack** (estimativa).
- **Boa escolha intermediária** para HGX H100/H200 corporativo.

### 4.3 Direct Liquid Cooling (DLC) — cold plate

- Placa fria sobre cada GPU/CPU; loop primário do rack para CDU (Coolant Distribution Unit).
- Suporta **>50 kW/rack** facilmente.
- **Requisito quase obrigatório para B200 HGX denso** e **obrigatório para GB200 NVL72**.
- Custo: **US$ 50–150k por rack** (CDU + retrofit) + necessidade de chilled water dedicado.
- DCs comerciais oferecendo DLC em 2026: **Equinix (alguns sites), Ascenty Tamboré, Digital Realty SAO10, Scala (Hyperscale)**.

### 4.4 Imersão (immersion cooling)

- Servidor mergulhado em fluido dielétrico (single-phase ou two-phase).
- Permite >100 kW/rack sem ar.
- Custo alto, operação não-trivial.
- Adoção corporativa rara em 2026; mais comum em hyperscalers (Microsoft Quincy).
- **Não recomendado para empresa corporativa típica** salvo nicho.

## 5. Energia — requisitos elétricos

### 5.1 Por servidor HGX 8-GPU

- 6× PSU 3 kW (3+3 redundância).
- Total instalado: ~18 kVA por servidor.
- Em uso típico: ~12–14 kW.
- Necessário **circuito dedicado** (geralmente 32A 415V trifásico ou equivalente).

### 5.2 Para um cluster M (16–24 GPUs ≈ 2–3 servidores HGX)

- Carga sustentada: **30–45 kW**.
- Carga de pico: **60 kW**.
- UPS: minimum N+1 com runtime 10 min.
- Gerador: backup de DC (não específico do cluster).
- PUE alvo: <1,3 (DC moderno).

### 5.3 Para um cluster G (80–150 GPUs ≈ 10–20 servidores HGX)

- Carga sustentada: **150–280 kW**.
- Carga de pico: **350+ kW**.
- Frequentemente **co-location obrigatória** (DC corporativo interno raramente entrega tanto).
- Linha dedicada com switchgear próprio.

### 5.4 GB200 NVL72 single rack

- **120 kW** sustentado.
- Custo de operação elétrica: **~US$ 90–150k/ano apenas em energia** (a R$ 0,50–0,80/kWh BR; mais barato em alguns DCs especializados).

## 6. Espaço físico (U-rack)

| Servidor | U-rack | Quantos cabem em rack 42U? |
|---------|--------|------------------------------|
| HGX 8-GPU (H100/H200) — 8U | 8U | 5 servidores teoricamente; **2–3 na prática** (limite térmico/elétrico) |
| HGX B200 8-GPU — 8U–10U | 8–10U | 1–2 (limite térmico) |
| GB200 NVL72 | rack inteiro | 1 (é todo o rack) |
| L40S 1U-2U server | 1–2U | até 20 (limite elétrico/térmico) |
| Storage Weka/VAST | 1–4U | depende do modelo |
| Network spine/leaf | 1–2U | 2 por rack tipicamente |

**Regra prática**: limite **térmico-elétrico** quase sempre vence limite **U-rack**.

## 7. PUE e custo de energia ao longo da vida

PUE (Power Usage Effectiveness) = energia total DC / energia TI.

- DC corporativo BR típico: **PUE 1,5–2,0**.
- DC moderno (Equinix, Ascenty Tamboré): **PUE 1,3–1,4**.
- Hyperscaler bem operado: **PUE 1,1–1,2**.

**Custo total de energia** = TI × PUE × tarifa × horas/ano.

Exemplo cenário M (40 kW sustentados, PUE 1,4, tarifa BR R$ 0,55/kWh, 8.760h/ano):

- 40 × 1,4 × 8.760 = 490.560 kWh/ano.
- Custo: **R$ 270k/ano (~US$ 50k)** apenas em energia.

Exemplo cenário G (250 kW, mesmo PUE, mesma tarifa):

- 250 × 1,4 × 8.760 = 3.066.000 kWh/ano.
- Custo: **R$ 1,7M/ano (~US$ 320k)**.

## 8. Requisitos de DC corporativo para acomodar IA

| Item | Mínimo | Recomendado | Frontier |
|------|--------|-------------|----------|
| kW por rack | 15 | 30–40 | 50–120 |
| Tier (Uptime Institute) | III | III | IV (críticos) |
| Cooling | ar reforçado | RDHx ou DLC adoçado | DLC obrigatório |
| Chilled water | <12°C | <10°C | <8°C |
| Redundância elétrica | N+1 UPS | 2N | 2(N+1) |
| Conectividade | 2 ISPs + MPLS | 2 ISPs + dark fiber | 2 ISPs + dark fiber + carrier hotel |
| Acesso físico | controlado | biometria + man-trap | biometria + dual-control |
| PUE | <1,5 | <1,4 | <1,3 |

## 9. Co-location vs DC próprio

| Critério | DC próprio | Co-location |
|----------|------------|-------------|
| CAPEX inicial | Muito alto (DC novo: dezenas de US$ M) | Médio (rack rental) |
| OPEX | Alto (energia + staff) | Médio (rack rental + power draw) |
| Soberania | máxima | alta (contratualmente) |
| Tempo de start | 12–24 meses (DC novo) | 4–12 semanas |
| Capacidade de upgrade DLC | depende | varia por provedor |
| Recomendação BR | Estatais grandes (Serpro, Petrobras), bancos T1 | A maioria das empresas |

**Provedores de co-lo BR com IA-ready (mai/2026)**:
- **Equinix SP4 (Tamboré)**: DLC disponível.
- **Ascenty Tamboré 2 / Hortolândia**: capacidade GB200-class.
- **Scala Tamboré**: hyperscale BR.
- **Odata SP01 / SP02**: tradicional, em retrofit DLC.
- **Tivit / Embratel**: nuvem privada com GPU.

## 10. Logística e instalação

- **Peso de servidor HGX**: 60–100 kg → exige guincho elétrico no DC.
- **Pisos elevados**: alguns DCs antigos têm carga limite que não comporta racks densos modernos.
- **Lead time de DLC retrofit**: 3–6 meses.
- **Cabeamento óptico**: pré-instalar OM5/OS2 com folga; mudanças posteriores são caras.

## 11. Roadmap energético (proposta operacional)

```
T0  Avaliação do DC atual (kW disponível, cooling, espaço)
T+1 mês   Decisão: DC próprio retrofit OU co-lo
T+2 mês   Contrato de fornecimento elétrico expandido (se DC próprio)
T+3 mês   Pedido de servidores/GPU (lead time 4–8 semanas)
T+4 mês   Retrofit DLC se Blackwell
T+5 mês   Instalação + comissionamento
T+6 mês   Carga sustentada
```

## 12. Decisões executivas

| Pergunta | Recomendação |
|----------|--------------|
| DC próprio ou co-location? | Co-lo para >90% dos casos corporativos. DC próprio só em estatal/T1. |
| DLC necessário? | Sim se Blackwell no roadmap; opcional para H100/H200 com RDHx. |
| Tier do DC? | Tier III mínimo; Tier IV só para casos muito críticos (atendimento cliente regulado). |
| PUE objetivo? | < 1,4 (DC moderno). Importante para narrativa ESG/sustentabilidade. |

## Referências

- NVIDIA HGX/DGX power & cooling: <https://docs.nvidia.com/dgx/>
- Uptime Institute Tier standards: <https://uptimeinstitute.com/tiers>
- Equinix DLC: <https://www.equinix.com/data-centers/colocation>
- Ascenty Tamboré: <https://www.ascenty.com/en/data-centers/>
- ASHRAE TC 9.9 (DC environment guidelines): <https://www.ashrae.org/technical-resources/bookstore/datacom-series>
