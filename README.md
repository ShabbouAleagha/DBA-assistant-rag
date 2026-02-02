# 🧠 Local RAG-Based DBA Assistant (Ollama + LangChain + ChromaDB)

A fully local Retrieval-Augmented Generation (RAG) platform designed to assist Database Administrators (DBAs) in diagnosing, understanding, and resolving database-related issues using private technical documentation.

This system operates **entirely offline**, relying on local LLMs via Ollama and a vector database for knowledge retrieval.

---

## 📌 Project Objectives

- Build a fully local AI assistant for database troubleshooting
- Enable semantic search over heterogeneous technical documents
- Preserve data confidentiality (no cloud API usage)
- Provide explainable answers with sources
- Demonstrate a complete RAG pipeline implementation

---

## 🏗️ System Architecture

### 1️⃣ Document Processing & Vectorization Pipeline

![Embedding Pipeline](images/pipeline_storage.png)

This stage is responsible for:

- Loading heterogeneous documents (PDF, XLSX, JSON, TXT)
- Splitting text into semantic chunks
- Generating embeddings
- Storing vectors in ChromaDB

---

### 2️⃣ End-to-End RAG Pipeline

![Full Pipeline](images/pipeline_full.png)

The complete pipeline includes:

1. Data ingestion
2. Cleaning & filtering
3. Chunking
4. Vector indexing
5. Similarity retrieval
6. LLM response generation

---

### 3️⃣ User Interaction Flow

![User Pipeline](images/rag_user_flow.png)

Users interact with the system through a conversational interface powered by Chainlit.

The retriever identifies relevant documents, and the generator produces grounded responses.

---

## ⚙️ Technical Stack

| Component        | Technology              |
|------------------|--------------------------|
| Interface        | Chainlit                 |
| LLM              | Ollama (LLaMA3 / Mistral) |
| Embeddings        | nomic-embed-text         |
| Vector DB         | ChromaDB                 |
| Framework         | LangChain                |
| Language          | Python 3.11              |

---

## 📂 Project Structure

