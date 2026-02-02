import chainlit as cl

from rag.ingest import ingest
from rag.qa import answer


@cl.on_chat_start
async def on_chat_start():
    res = ingest()
    await cl.Message(
        content=(
            "✅ Local DBA Assistant (RAG) is running.\n\n"
            f"📦 Ingest status: {res.get('message')}\n"
            f"Files: {res.get('files', 0)} | Chunks added: {res.get('added', 0)}\n\n"
            "Put documents into `./docs` (PDF/XLSX/JSON/TXT/MD) and restart, "
            "or type `/ingest` to ingest again."
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    content = (message.content or "").strip()

    if content.lower() == "/ingest":
        res = ingest()
        await cl.Message(
            content=f"🔁 {res.get('message')} | Files: {res.get('files',0)} | Chunks: {res.get('added',0)}"
        ).send()
        return

    out, _ = answer(content)
    await cl.Message(content=out).send()
