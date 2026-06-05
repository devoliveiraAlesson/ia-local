"""
Indexa documentos da pasta knowledge-base/ no Qdrant.
Suporta: .txt, .md, .pdf, .docx

Uso:
  docker compose exec bot python /scripts/ingest_kb.py
  # ou localmente:
  cd bot && python ../scripts/ingest_kb.py
"""

import asyncio
import sys
import os
from pathlib import Path

# Garante que o módulo bot está no path
sys.path.insert(0, str(Path(__file__).parent.parent / "bot"))

from agent.rag import ensure_collection, index_chunk
from agent.gemini_client import embed_text  # noqa: F401 — força config do genai


KB_DIR = Path(__file__).parent.parent / "knowledge-base" / "docs"
CHUNK_SIZE = 800  # chars por chunk
CHUNK_OVERLAP = 100


def split_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return [c.strip() for c in chunks if c.strip()]


def read_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(str(path))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except ImportError:
            print(f"  [AVISO] PyPDF2 não instalado. Pulando {path.name}")
            return ""
    if suffix == ".docx":
        try:
            import docx
            doc = docx.Document(str(path))
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            print(f"  [AVISO] python-docx não instalado. Pulando {path.name}")
            return ""
    return ""


async def main():
    if not KB_DIR.exists():
        print(f"Pasta não encontrada: {KB_DIR}")
        print("Crie arquivos .txt/.md/.pdf/.docx em knowledge-base/docs/")
        return

    files = list(KB_DIR.glob("**/*"))
    files = [f for f in files if f.is_file() and f.suffix.lower() in (".txt", ".md", ".pdf", ".docx")]

    if not files:
        print(f"Nenhum documento encontrado em {KB_DIR}")
        return

    print(f"Preparando coleção Qdrant...")
    await ensure_collection()

    total_chunks = 0
    for file in files:
        print(f"Processando: {file.name}")
        text = read_file(file)
        if not text:
            continue
        chunks = split_text(text)
        for i, chunk in enumerate(chunks):
            await index_chunk(chunk, metadata={"source": file.name, "chunk": i})
            total_chunks += 1
        print(f"  → {len(chunks)} chunks indexados")

    print(f"\nConcluído! {total_chunks} chunks indexados de {len(files)} arquivo(s).")


if __name__ == "__main__":
    asyncio.run(main())
