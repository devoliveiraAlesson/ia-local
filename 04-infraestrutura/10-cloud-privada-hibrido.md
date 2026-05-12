# Cloud Privada e Híbrido — Alternativas Parciais ao On-Prem Puro

> Etapa 4/5 da proposta. Quando "cloud privada" ou "híbrido" pode substituir parcial/totalmente o on-prem; quando NÃO pode.

## 1. Espectro de soluções (mais nuvem ↔ mais on-prem)

```
Cloud SaaS pública     Cloud privada single-tenant    Cloud privada     On-prem em DC          On-prem
(OpenAI, Bedrock)  ──► (Azure OpenAI, AWS Bedrock) ──► (Outposts, OCI ─► co-location ──────► próprio
                                                       Dedicated, IBM    (Equinix, Ascenty)    DC
                                                       Cloud Satellite)
```

A maioria das empresas reguladas opera num **mix**: on-prem para crítico + cloud privada para casos amplos.

## 2. Comparativo das soluções "cloud privada / appliance híbrido"

| Solução | Modelo | Soberania de dados | LLM nativo? | Quando faz sentido | Trade-off |
|---------|--------|---------------------|-------------|---------------------|-----------|
| **AWS Outposts** | Rack AWS instalado on-prem | dados não saem | SageMaker JumpStart + Bedrock subset | empresa AWS-first com requisito on-prem soft | lock-in AWS; latência para control plane |
| **AWS Outposts + Bedrock** | Idem + modelos hospedados | idem | sim (Llama, Claude via Bedrock) | empresa AWS regulada | dependência de control plane AWS |
| **Azure Local (ex-Azure Stack HCI)** | Servidores Microsoft on-prem | dados não saem | Azure OpenAI Air-Gapped (em rollout 2026) | Microsoft-first regulated | lock-in MS; Azure OpenAI air-gap ainda em GA |
| **Google Distributed Cloud Air-Gapped (GDC AG)** | Rack Google totalmente desconectado | total | Gemini on-prem + Llama | governo, defesa | nicho; suporte regional limitado |
| **Oracle Cloud Dedicated Region (OCI DR)** | Região OCI inteira no DC do cliente | total | OCI Generative AI (Llama, Cohere via Mistral) | grande empresa OCI / SAP | CAPEX 50M+ típico; só Tier-1 |
| **IBM Cloud Satellite** | Extensão IBM Cloud no DC do cliente | total | watsonx.ai inclui Granite 4 e Llama 3.x | empresa IBM-first / saúde / banco BR | flexibilidade boa; ecossistema IBM |
| **Dell APEX AIaaS / HPE GreenLake AI** | Hardware como serviço com modelo OpEx | dados no rack | varia (parceiros) | empresa quer on-prem mas sem CAPEX | contrato 3–5 anos; custo total > CAPEX puro |

## 3. AWS Outposts

- **Footprint**: rack 42U AWS gerenciado.
- **Capacidade GPU**: limitada (algumas SKUs com GPU; H100/H200 não em todos os Outposts). Em mai/2026, P5 instances (H100) estão em **alguns Outposts**, não em todos.
- **Bedrock**: alguns modelos (Llama, Claude via Bedrock) disponíveis com **dados que não saem** do rack.
- **Quando faz sentido**: empresa AWS-only que precisa de marca "on-prem" para compliance (ex.: bancos com BACEN exigindo dados em território BR + AWS BR insuficiente).
- **Risco**: se AWS sai do BR, o rack permanece mas operação fica complexa.

## 4. Azure Local + Azure OpenAI Air-Gapped

- **Azure Local (ex Azure Stack HCI)**: hipervisor MS rodando hardware do cliente, gerenciado via Azure portal.
- **Azure OpenAI Air-Gapped**: anunciado em 2025; em **rollout limitado em mai/2026** para clientes governamentais e altamente regulados (defesa, saúde).
- **Microsoft Sovereign Cloud (UE)**: oferece GPT-4o/o3-mini sob jurisdição UE.
- **Quando faz sentido**: empresa Microsoft-first com Azure OpenAI já em uso e exigência de soberania.
- **Risco**: dependência fortíssima do roadmap MS; portabilidade reduzida.

## 5. Google Distributed Cloud Air-Gapped (GDC AG)

- Rack Google totalmente offline; updates via mídia removível.
- Modelos: **Gemini Nano/Pro on-prem** (Gemini 2.x em mai/2026), Llama, Codey.
- **Casos**: governos (UK, NL), defesa, intelligence.
- **Suporte regional**: limitado fora US/EU/UK. **Brasil ainda emergente**.

## 6. Oracle OCI Dedicated Region

- **Footprint**: região OCI inteira (10–20+ racks) instalada no DC do cliente.
- **Mínimo prático**: ~US$ 50–80M de compromisso (+ DC com requisitos pesados).
- **LLM**: OCI Generative AI (Llama, Cohere/Mistral) + bring-your-own-model em compute GPU.
- **Casos**: T1 / governo nacional. Em BR: Banco Central usa OCI dedicated.
- **Quando faz sentido**: empresa Oracle-first com SAP / Fusion ERP (sinergia DB + apps + IA).

## 7. IBM Cloud Satellite + watsonx.ai

- Estende IBM Cloud para DC do cliente.
- watsonx.ai inclui **Granite 4 (ISO/IEC 42001!), Llama 3.x, Mistral, custom models**.
- Tem appliance "watsonx.governance" — relevante para ISO 42001 / EU AI Act.
- **Casos BR**: Bradesco e Itaú usam IBM em parte da stack; saúde (Mayo Clinic é cliente IBM).
- **Quando faz sentido**: empresa IBM-first, banco BR, foco em compliance ISO 42001.

## 8. Dell APEX AIaaS / HPE GreenLake AI / Lenovo TruScale

- Hardware moderno (HGX H100/H200/B200) como serviço — OpEx em vez de CAPEX.
- Equipe do fornecedor opera; cliente consome.
- **Quando faz sentido**: empresa que quer on-prem físico mas sem capex pesado nem time de operação.
- **Trade-off**: contrato 3–5 anos, custo total geralmente **20–35% maior** que CAPEX puro em 5 anos. Vale por **previsibilidade orçamentária** + **velocidade de deploy** (semanas vs meses).

## 9. Quando híbrido é OK e quando NÃO é

### 9.1 Híbrido OK

- **Casos amplos não-críticos** em VPC/cloud privada (ex.: chat genérico para "achar fornecedor X").
- **Picos** (burst) em cloud com modelo equivalente.
- **Treino off-line** em cloud que volta como modelo on-prem (separação claro: dados nunca saem, mas compute pode).
- **DR** em cloud privada do mesmo fornecedor.

### 9.2 Híbrido NÃO OK

- **Dados de paciente / PHI** (HIPAA): nunca em cloud sem BAA explícito, e mesmo assim com cuidado.
- **Dados clientes BR** sob LGPD com cláusula contratual de "permanência em território nacional".
- **Segredo industrial / IP estratégico**: ITAR/EAR, defesa, química especial.
- **Dados ANS, BACEN, CVM regulados**: regulação setorial específica.
- **Dados Schrems II-sensíveis (UE)**: cuidado com cloud headquartered US.

## 10. Padrão recomendado: hybrid orchestration via gateway

```
                  ┌───────────────┐
   usuário ────►  │  Gateway LLM  │
                  │  (LiteLLM)    │
                  └───────┬───────┘
                          │
       ┌──────────────────┼────────────────────┐
       │                  │                    │
       ▼                  ▼                    ▼
   on-prem            cloud privada         cloud SaaS
   (sensível)         (não sensível)        (capacidade extra)
   - Llama 70B        - Bedrock Llama       - Anthropic Claude
   - Granite          - Azure OpenAI        - GPT-4o
   - Qdrant           - Cohere R+
```

Decisão de roteamento por **tag do prompt** (`sensitivity: high|low`), por **tenant**, ou por **modelo solicitado**. Bloqueio explícito quando prompt sensível tenta sair do perímetro.

## 11. Custos comparativos (estimativa pública por 1k tokens, mai/2026)

| Caminho | $ por 1M tokens (estimativa) | Comentário |
|---------|------------------------------|------------|
| OpenAI GPT-4o API pública | ~US$ 5,00 | referência alta |
| Anthropic Claude Sonnet | ~US$ 3,00 | qualidade alta |
| Azure OpenAI VPC | ~US$ 5,00 | mesmo da OpenAI |
| AWS Bedrock Llama 3.3 70B | ~US$ 0,72 | razoável |
| Cloud privada single-tenant Llama 70B (calc próprio) | ~US$ 1,00–1,50 | depende |
| **On-prem Llama 70B AWQ em H100, full util** | **~US$ 0,15–0,30** | **5–25× mais barato** que API após payback |
| On-prem em hardware ocioso | ~US$ 1,50+ | utilização baixa mata o caso |

> **Insight crítico para Etapa 5 (ROI)**: on-prem só "ganha" da API se utilização sustentada > 30–40%. Subdimensionar utilização → CAPEX desperdiçado.

## 12. Decisões executivas

| Pergunta | Recomendação |
|----------|--------------|
| Híbrido ou on-prem puro? | Híbrido para 80% dos casos; on-prem puro só para casos rigorosamente regulados ou com mandato de soberania. |
| AWS Outposts / Azure Local / OCI DR? | Aderência ao stack hyperscaler já existente; **Azure Local + Azure OpenAI Air-Gapped** é a alternativa pragmática 2026 para Microsoft-first. |
| GreenLake / APEX AIaaS? | Boa alternativa quando empresa quer on-prem físico sem time de operação; trade-off é contrato 3–5 anos. |
| Cloud para DR? | OK se mesmo fornecedor, **dados não-sensíveis**; senão DR em DC próprio/secundário. |
| Burst para cloud? | OK via gateway com filtro de sensibilidade — solução pragmática para evitar superdimensionar on-prem para picos raros. |

## Referências

- AWS Outposts: <https://aws.amazon.com/outposts/>
- AWS Bedrock + Outposts: <https://aws.amazon.com/blogs/aws/category/sectors/government/>
- Azure Local: <https://learn.microsoft.com/en-us/azure/azure-local/>
- Azure OpenAI Sovereignty: <https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/sovereign-cloud>
- Google Distributed Cloud Air-Gapped: <https://cloud.google.com/distributed-cloud/air-gapped/docs>
- Oracle Dedicated Region: <https://www.oracle.com/cloud/cloud-at-customer/dedicated-region/>
- IBM Cloud Satellite + watsonx: <https://www.ibm.com/cloud/satellite>
- Dell APEX AIaaS: <https://www.dell.com/en-us/dt/apex/index.htm>
- HPE GreenLake AI: <https://www.hpe.com/us/en/greenlake/large-language-models.html>
- Lenovo TruScale: <https://www.lenovo.com/us/en/truscale/>
