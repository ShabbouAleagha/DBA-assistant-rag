from __future__ import annotations
from typing import Tuple, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from .config import settings
from .vectorstore import get_chroma


SYSTEM_PROMPT = """You are a DBA assistant.
Answer using ONLY the provided context when possible.
If context is missing, say clearly that you don't have enough information and suggest what document to add.
Be concise, technical, and action-oriented.
Always include a short "Sources:" list of file names if any were used.
"""


def _format_sources(docs) -> str:
    sources = []
    for d in docs:
        src = d.metadata.get("source", "")
        if src:
            sources.append(src)
    sources = sorted(set(sources))
    if not sources:
        return "Sources: (none)"
    short = [s.split("/")[-1] for s in sources]
    return "Sources: " + ", ".join(short[:10])


def answer(question: str) -> Tuple[str, List]:
    vs = get_chroma(settings.CHROMA_DIR, settings.COLLECTION)
    retriever = vs.as_retriever(search_kwargs={"k": settings.TOP_K})
    ctx_docs = retriever.get_relevant_documents(question)

    context = "\n\n".join(
        [f"[{i+1}] {d.page_content}" for i, d in enumerate(ctx_docs)]
    ) if ctx_docs else ""

    llm = ChatOllama(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.2,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Question:\n{question}\n\nContext:\n{context}\n\nReturn a helpful answer."),
    ])

    chain = prompt | llm | StrOutputParser()
    out = chain.invoke({"question": question, "context": context})

    out = out.strip() + "\n\n" + _format_sources(ctx_docs)
    return out, ctx_docs
