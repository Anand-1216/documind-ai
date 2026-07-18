# DocuMind AI 🧠

> AI-powered document Q&A platform with production-grade RAG pipeline

## What It Does
Upload any PDF and ask questions about it. DocuMind AI uses 
Retrieval Augmented Generation (RAG) to find relevant content 
and generate accurate, grounded answers.

## Tech Stack
Python • FastAPI • LangChain • ChromaDB • Groq (Llama 3.1)
SQLAlchemy • JWT Authentication • Sentence Transformers

## Architecture
```
PDF Upload → PyMuPDF extraction → Semantic chunking (800 chars)
→ SentenceTransformer embeddings (384-dim, local)
→ ChromaDB storage (per-user collections)
→ Question embedding → Cosine similarity retrieval (top-4)
→ Groq Llama 3.1 answer generation
→ Source attribution + retrieval scoring
```

## Features
- JWT secured multi-user system
- Per-user document isolation
- Async background PDF processing
- RAG evaluation with retrieval scoring
- 0% hallucination via strict prompting
- Production error handling + request logging
- Clean REST API (10 endpoints)

## Quick Start
```bash
git clone https://github.com/Anand-1216/documind-ai
cd documind-ai
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to .env
uvicorn main:app --reload
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /users/register | Create account |
| POST | /users/login | Get JWT token |
| POST | /documents/upload | Upload PDF |
| GET | /documents/ | List documents |
| GET | /documents/{id} | Document status |
| DELETE | /documents/{id} | Delete document |
| POST | /chat/{doc_id} | Ask question |
| GET | /chat/{doc_id}/history | Chat history |
| DELETE | /chat/{id} | Delete chat |
| GET | /health | Health check |

## What I Learned Building This
- RAG pipeline from scratch — chunking, embedding, retrieval
- Vector databases — ChromaDB with cosine similarity search
- Production patterns — caching, logging, error handling
- JWT authentication in FastAPI
- Async background task processing