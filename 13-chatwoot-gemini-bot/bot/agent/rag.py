"""RAG pipeline: indexação e recuperação via Qdrant + embeddings Gemini."""

import uuid
import structlog
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from config import get_settings
from agent.gemini_client import embed_text

log = structlog.get_logger()

VECTOR_SIZE = 768  # text-embedding-004


def get_qdrant() -> AsyncQdrantClient:
    s = get_settings()
    return AsyncQdrantClient(host=s.qdrant_host, port=s.qdrant_port)


async def ensure_collection():
    s = get_settings()
    client = get_qdrant()
    collections = await client.get_collections()
    names = [c.name for c in collections.collections]
    if s.qdrant_collection not in names:
        await client.create_collection(
            collection_name=s.qdrant_collection,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        log.info("qdrant_collection_created", name=s.qdrant_collection)


async def index_chunk(text: str, metadata: dict | None = None):
    """Indexa um trecho de texto no Qdrant."""
    s = get_settings()
    vector = await embed_text(text)
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={"text": text, **(metadata or {})},
    )
    client = get_qdrant()
    await client.upsert(collection_name=s.qdrant_collection, points=[point])


async def search(query: str, top_k: int = 4, filter_tag: str | None = None) -> list[str]:
    """Busca os trechos mais relevantes para a query."""
    s = get_settings()
    vector = await embed_text(query)

    qfilter = None
    if filter_tag:
        qfilter = Filter(
            must=[FieldCondition(key="tag", match=MatchValue(value=filter_tag))]
        )

    client = get_qdrant()
    results = await client.search(
        collection_name=s.qdrant_collection,
        query_vector=vector,
        limit=top_k,
        query_filter=qfilter,
        score_threshold=0.5,
    )
    return [r.payload["text"] for r in results]
