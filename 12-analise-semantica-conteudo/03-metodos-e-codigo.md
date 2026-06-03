# Métodos e código — os scripts, comentados

> Aqui estão os scripts de cada degrau da escada ([`01`](./01-escada-de-tecnicas.md)), em Python, comentados para quem sabe programar mas não necessariamente domina NLP. Pressupõem os dois CSVs limpos do [`02`](./02-coleta-e-preparacao.md): `corpus_publico.csv` e `corpus_nosso.csv`. São didáticos — adapte caminhos, nomes de coluna e modelos à sua stack. As decisões de ferramenta (local vs. API) estão no [`05`](./05-stack-e-roadmap.md).

## Setup

```bash
# ambiente sugerido
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy scikit-learn matplotlib wordcloud nltk spacy
pip install sentence-transformers   # embeddings locais
pip install bertopic                 # topic modeling (degrau 3)
python -m spacy download pt_core_news_lg
```

```python
import pandas as pd
pub  = pd.read_csv("corpus_publico.csv")   # interesse do público
nos  = pd.read_csv("corpus_nosso.csv")     # nosso conteúdo
textos_pub = pub["texto_limpo"].dropna().tolist()
textos_nos = nos["texto_limpo"].dropna().tolist()
```

---

## Degrau 1a — Nuvem de palavras (a foto rápida)

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk; nltk.download("stopwords")

stop_pt = set(stopwords.words("portuguese"))
# adicione jargão genérico do seu setor que não distingue nada:
stop_pt |= {"investimento", "investimentos", "mercado", "sobre"}

def nuvem(textos, titulo):
    wc = WordCloud(width=1200, height=600, background_color="white",
                   stopwords=stop_pt, collocations=True).generate(" ".join(textos))
    plt.figure(figsize=(12,6)); plt.imshow(wc); plt.axis("off")
    plt.title(titulo); plt.tight_layout(); plt.savefig(f"{titulo}.png", dpi=150)

nuvem(textos_pub, "publico")
nuvem(textos_nos, "nosso")
```

> Útil para a reunião. **Não conclua daqui** — vá para o keyness, que compara de verdade.

## Degrau 1b — Keyness (palavras distintivas do público vs. as suas)

```python
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# conta frequências nos dois corpora no mesmo vocabulário
vec = CountVectorizer(stop_words=list(stop_pt), min_df=3, ngram_range=(1,2))
X = vec.fit_transform(textos_pub + textos_nos)
vocab = np.array(vec.get_feature_names_out())
n_pub = len(textos_pub)
freq_pub = np.asarray(X[:n_pub].sum(axis=0)).ravel()
freq_nos = np.asarray(X[n_pub:].sum(axis=0)).ravel()

# log-ratio (tamanho do efeito): quão mais característico do público que nosso
tot_pub, tot_nos = freq_pub.sum(), freq_nos.sum()
# +0.5 = suavização de Laplace para evitar divisão por zero
rate_pub = (freq_pub + 0.5) / tot_pub
rate_nos = (freq_nos + 0.5) / tot_nos
log_ratio = np.log2(rate_pub / rate_nos)

tab = pd.DataFrame({"termo": vocab, "freq_pub": freq_pub,
                    "freq_nos": freq_nos, "log_ratio": log_ratio})
print("=== Termos MUITO mais do público que nossos (gaps de vocabulário) ===")
print(tab[tab.freq_pub >= 5].sort_values("log_ratio", ascending=False).head(20))
print("=== Termos que nós martelamos e o público pouco usa ===")
print(tab[tab.freq_nos >= 5].sort_values("log_ratio").head(20))
```

> `log_ratio` alto = termo característico do **público**; baixo (negativo) = característico **seu**. Isso já é um mapa de gap no nível de palavra. Para a versão visual, use a biblioteca **`scattertext`** (gera um HTML interativo do "frequência no público × frequência em nós").

---

## Degrau 2 — Embeddings + cosseno (o coração)

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# modelo multilíngue forte em PT-BR, roda local (ver doc 05 para alternativas)
model = SentenceTransformer("BAAI/bge-m3")

emb_pub = model.encode(textos_pub, normalize_embeddings=True, show_progress_bar=True)
emb_nos = model.encode(textos_nos, normalize_embeddings=True, show_progress_bar=True)

# matriz de similaridade: cada post do público × cada post nosso
S = cosine_similarity(emb_pub, emb_nos)   # shape (n_pub, n_nos)
```

### Métrica 1 — Placar de alinhamento (o número-chave)
```python
# para cada interesse do público, quão perto está o NOSSO conteúdo mais próximo?
melhor_match_por_interesse = S.max(axis=1)        # vetor de tamanho n_pub
placar_alinhamento = melhor_match_por_interesse.mean()
print(f"Placar de alinhamento (0–1): {placar_alinhamento:.3f}")
```
> Interpretação: perto de 1 = para quase todo interesse do público existe conteúdo seu próximo. Baixo = muito interesse sem cobertura. **Calibre o que é "alto"** comparando com pares que você sabe que combinam (ver doc 01, armadilha do cosseno relativo).

### Métrica 2 — Gaps de conteúdo (interesses órfãos)
```python
# interesses do público SEM nenhum conteúdo nosso próximo
LIMIAR = 0.45  # calibrar!
gaps = [(textos_pub[i], melhor_match_por_interesse[i])
        for i in range(len(textos_pub)) if melhor_match_por_interesse[i] < LIMIAR]
gaps = sorted(gaps, key=lambda x: x[1])
print(f"{len(gaps)} interesses do público sem cobertura. Exemplos:")
for txt, sim in gaps[:15]:
    print(f"  [sim_max={sim:.2f}] {txt[:120]}")
```

### Métrica 3 — Conteúdo órfão (publicamos, ninguém demanda)
```python
melhor_match_por_post_nosso = S.max(axis=0)       # tamanho n_nos
orfaos = [(textos_nos[j], melhor_match_por_post_nosso[j])
          for j in range(len(textos_nos)) if melhor_match_por_post_nosso[j] < LIMIAR]
print(f"{len(orfaos)} posts nossos distantes de qualquer interesse do público.")
```

### Métrica 4 — Para um interesse, qual nosso conteúdo responde melhor
```python
def melhor_resposta(texto_interesse):
    e = model.encode([texto_interesse], normalize_embeddings=True)
    sims = cosine_similarity(e, emb_nos)[0]
    j = int(sims.argmax())
    return textos_nos[j], float(sims[j])

print(melhor_resposta("como proteger o patrimônio dos meus filhos no exterior"))
```

> Estas quatro métricas já entregam 80% do valor do projeto. Os degraus 3–4 aprofundam em *temas*.

---

## Degrau 3 — Topic modeling com BERTopic (descobrir os assuntos)

> Só vale a pena com **volume** (milhares de posts). Com poucas centenas, pule e fique no degrau 2 (ver armadilhas no doc 01).

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

emb_model = SentenceTransformer("BAAI/bge-m3")

# tópicos do PÚBLICO
topic_model_pub = BERTopic(embedding_model=emb_model, language="multilingual",
                           min_topic_size=15, calculate_probabilities=True)
topics_pub, _ = topic_model_pub.fit_transform(textos_pub)
print(topic_model_pub.get_topic_info().head(15))   # temas do público + tamanho

# tópicos do NOSSO conteúdo
topic_model_nos = BERTopic(embedding_model=emb_model, language="multilingual",
                           min_topic_size=10)
topics_nos, _ = topic_model_nos.fit_transform(textos_nos)
print(topic_model_nos.get_topic_info().head(15))
```

### Cruzando os temas dos dois lados (o mapa de gap por assunto)
```python
# representa cada TÓPICO por seu embedding médio e compara os dois conjuntos
import numpy as np
def centroides(topic_model, textos, topics):
    embs = emb_model.encode(textos, normalize_embeddings=True)
    ids = sorted(set(t for t in topics if t != -1))   # -1 = outlier
    return ids, np.vstack([embs[np.array(topics)==t].mean(0) for t in ids])

ids_p, C_pub = centroides(topic_model_pub, textos_pub, topics_pub)
ids_n, C_nos = centroides(topic_model_nos, textos_nos, topics_nos)
M = cosine_similarity(C_pub, C_nos)

for k, tid in enumerate(ids_p):
    cobertura = M[k].max()
    palavras = [w for w,_ in topic_model_pub.get_topic(tid)][:6]
    flag = "  <-- GAP DE TEMA" if cobertura < 0.5 else ""
    print(f"Tema público {tid} ({', '.join(palavras)}): cobertura={cobertura:.2f}{flag}")
```
> Tópicos do público com `cobertura` baixa = **temas que o público discute e você não cobre**. Esse é o entregável mais "executivo" do projeto.

> **Ajuste para volume baixo:** reduza `min_topic_size`; para forçar atribuição (menos outliers) use `hdbscan_model` com `min_cluster_size` pequeno, ou substitua o clusterizador por `KMeans`. Mas se os tópicos saírem incoerentes, é sinal de que falta dado — volte ao degrau 2.

---

## Degrau 4 — Resumo estruturado via LLM (tema → pauta acionável)

> Para cada cluster do degrau 3, peça a um LLM um resumo em JSON. Use LLM **local** se houver qualquer PII (ver [`06-mcp-claude-code/`](../06-mcp-claude-code/)).

```python
# pseudo-código de orquestração; o cliente do LLM depende da sua stack
import json

PROMPT = """Você é analista de conteúdo de uma gestora de patrimônio.
Abaixo, posts reais do público-alvo agrupados por tema.
Responda SOMENTE em JSON com o schema:
{{"tema": str, "dores_implicitas": [str], "perguntas_frequentes": [str],
  "vocabulario_do_publico": [str], "angulos_de_pauta_sugeridos": [str]}}
Baseie-se ESTRITAMENTE nos posts; não invente.

Posts do tema:
{posts}"""

def resumir_cluster(posts_do_cluster, llm):
    amostra = "\n- ".join(posts_do_cluster[:30])      # limite de contexto
    resp = llm(PROMPT.format(posts=amostra))           # sua função de chamada
    return json.loads(resp)

# exemplo de saída esperada:
# {"tema": "Sucessão patrimonial internacional",
#  "dores_implicitas": ["medo de carga tributária na herança", "filhos no exterior"],
#  "perguntas_frequentes": ["como funciona holding no exterior?"],
#  "vocabulario_do_publico": ["offshore", "herdeiros", "blindagem"],
#  "angulos_de_pauta_sugeridos": ["Guia: estruturar sucessão com ativos fora do país"]}
```

> Valide: rode em uma amostra, leia as saídas, confira que não há alucinação. O JSON estruturado (schema fixo, ao estilo da [Etapa 1/Caso 7](../01-casos-de-uso/07-extracao-estruturada.md)) é o que torna o output utilizável num dashboard ou numa pauta editorial.

---

## Resumo do código

| Degrau | Script | Saída |
|--------|--------|-------|
| 1a | WordCloud | imagens `publico.png`, `nosso.png` |
| 1b | CountVectorizer + log-ratio | tabela de termos distintivos (gaps de vocabulário) |
| 2 | SentenceTransformer + cosine_similarity | **placar de alinhamento + 3 listas de gap** |
| 3 | BERTopic + centroides | temas dos dois lados + flag de gap por tema |
| 4 | LLM + JSON schema | pauta acionável por tema |

Próximo: amarrar tudo no **workflow aplicado ao seu caso** ([`04`](./04-workflow-aplicado.md)).
