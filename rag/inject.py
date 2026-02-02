from __future__ import annotations
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from .config import settings
from .loaders import list_documents
from .vectorstore import get_chroma


def build_documents() -> List[Document]:
    pairs = list_documents(settings.DOCS_DIR)
    docs: List[Document] = []
    for path, text in pairs:
        docs.append(Document(page_content=text, metadata={"source": str(path)}))
    return docs


def ingest() -> dict:
    docs = build_documents()
    if not docs:
        return {
            "added": 0,
            "files": 0,
            "message": "No files found in ./docs. Add PDF/XLSX/JSON/TXT and run ingest again."
        }

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)

    vs = get_chroma(settings.CHROMA_DIR, settings.COLLECTION)

    # Optional: clear collection before re-ingest (uncomment if needed)
    # vs.delete_collection()
    # vs = get_chroma(settings.CHROMA_DIR, settings.COLLECTION)

    vs.add_documents(chunks)
    return {"added": len(chunks), "files": len(docs), "message": "Ingestion completed."}
