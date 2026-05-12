# Varejo e E-commerce — Casos Públicos

> Setor menos sensível em termos regulatórios (exceto PCI/cartão) que financeiro, mas com forte ênfase em escala, custo por interação, e diferenciação de catálogo.

## 1. Walmart — "My Assistant" + Wallaby

**Setor**: varejo (físico + online). **Sede**: EUA. **Tamanho**: 2,1 mi de associates globais.

### Status e escala
- ✅ **Produção** desde 2023.
- ✅ Inicial: **50.000 corporate associates**; expansão para **75.000+ em 11 países** em 2024.
- ✅ **Wallaby**: série de **LLMs proprietários "retail-specific"** treinados em décadas de dados Walmart próprios.
- ✅ **Element**: plataforma proprietária de ML que ancora todos os tools.
- ✅ Em jun/2025: anúncio de tools AI para **1,5 milhão** de associates frontline.

### Stack
- ✅ **Walmart Element** (plataforma ML proprietária).
- ✅ **Wallaby** (família de LLMs próprios — Walmart **treinou modelos próprios** em vez de só usar APIs).
- ⚠️ Mistura com APIs externas (sem detalhe percentual público).

### Casos mapeados
- **Caso 1** (chat interno — My Assistant), **Caso 6** (sumarização de docs/relatórios), **Caso 12** (onboarding/treinamento), **Caso 2** (atendimento ao cliente em escala — frontline).

### Por que importa
- **Caso de modelo proprietário em larga escala fora do setor financeiro**.
- Demonstra que **dados verticais (décadas de retail)** justificam investir em treinar modelos próprios em vez de só usar APIs.

### Fontes
- ✅ <https://corporate.walmart.com/news/2024/01/09/walmarts-expanding-one-of-a-kind-associate-genai-tool-to-11-countries-in-2024>
- ✅ <https://corporate.walmart.com/news/2025/06/24/walmart-unveils-new-ai-powered-tools-to-empower-1-5-million-associates>
- ✅ <https://www.cnbc.com/2024/08/28/why-jpmorgan-and-walmart-are-opting-for-internal-gen-ai-assistants.html>
- ⚠️ <https://www.techtarget.com/searchcio/feature/Walmart-AI-Retailer-taps-employees-to-find-GenAI-use-cases>

## 2. Mercado Livre / Mercado Pago

**Setor**: e-commerce + fintech LATAM. **Sede**: BR/AR/UY.

### Status
- ⚠️ **Produção em desenvolvimento + dev tools**. Generative AI para:
  - **Image generation** integrada ao editor de imagem dos vendedores (vendor de roupas faz upload, AI gera modelo vestindo).
  - **Coding assistants** para desenvolvedores internos (não detalha qual).
- 🟡 Topologia interna pouco detalhada em fontes públicas.

### Fontes
- ⚠️ <https://www.mobiletime.com.br/noticias/26/09/2025/mercado-livre-ia/>

## 3. Magalu — "Cérebro da Lu" (Brasil)

**Setor**: varejo + marketplace + logística. **Sede**: BR.

### Status e escala
- ✅ **Produção desde 2025**. Lu agora "vende" no WhatsApp.
- ✅ Conversão **3× maior** declarada (Brazil Journal).

### Stack
- ✅ **HÍBRIDA com Magalu Cloud**: Gemini Flash/Pro (5B/12B) para visão e comparações pesadas + **modelos open-source leves rodando em Magalu Cloud** para FAQs e respostas rápidas + LLMs maiores para reasoning profundo.
- ✅ Diretoria de IA criada com diretor dedicado (Caio Gomes).
- ✅ Multi-agente + multi-modal (texto, imagem, voz com Pix).

### Por que importa
- Caso brasileiro de **estratégia "modelo certo para a tarefa certa"**, com **infra própria de cloud** (Magalu Cloud).
- Demonstra arquitetura de produção corporativa BR sofisticada em varejo.

### Casos mapeados
- **Caso 2** (atendimento ao cliente — comércio conversacional), **Caso 7** (extração — comparação de produtos via imagem).

### Fontes
- ✅ <https://itforum.com.br/noticias/magalu-whatsapp-lu/>
- ✅ <https://exame.com/inteligencia-artificial/lu-do-magalu-ganha-cerebro-com-ia-e-vira-vendedora-dentro-do-whatsapp/>
- ⚠️ <https://braziljournal.com/a-aposta-do-magalu-na-ai-esta-convertendo-3x-mais-vai-mexer-o-ponteiro/>
- ⚠️ <https://convergenciadigital.com.br/mercado/lu-do-magalu-quer-ser-a-protagonista-da-ia-no-varejo/>

## 4. Amazon (uso interno)

**Setor**: e-commerce + cloud + logística. **Sede**: EUA.

### Status
- 🟡 Uso interno massivo de IA (Rufus para clientes, Q para devs internos AWS, Bedrock).
- ⚠️ Foco do uso público: ferramentas para clientes (não tanto interno corporativo bem documentado em fontes que cobrimos).

## 5. Carrefour

- 🟡 Cobertura pública limitada para deploy LLM corporativo on-prem.

## 6. Shopify

- 🟡 Anúncios sobre Sidekick (assistente para merchants), mas é SaaS para clientes, não corporate internal.

## Síntese do setor

| Empresa | Topologia | Padrão |
|--------|-----------|--------|
| Walmart | Híbrido + LLMs próprios "Wallaby" | Modelos verticais sobre décadas de dados |
| Mercado Livre | Híbrido | Image gen + dev tools |
| Magalu | Magalu Cloud + Gemini + open source | Multi-modelo BR sofisticado |
| Amazon | Interno (Bedrock + próprios) | Pouco detalhe público |

**Padrões**:
- **Walmart e Magalu** são os exemplos mais transparentes de **modelo próprio + multi-LLM via plataforma própria**.
- Varejo grande tem **caso para modelo vertical** (Wallaby) por volume de dados próprios.
- Diferentemente do financeiro, há **menos restrição regulatória** — então a topologia escolhida tende a ser mais **multi-cloud / híbrida** que ON-PREM.

**Drivers para LOCAL** menos urgentes que em finanças/saúde — exceto:
- Custo por interação (volume gigante de chat ao cliente).
- Latência conversacional (ChatBot em WhatsApp/scale).
- Diferenciação de catálogo (Wallaby treina sobre dados próprios que ninguém mais tem).
