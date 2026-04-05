"""
Session 2: Simple RAG (Retrieval Augmented Generation)

How RAG works:
1. Load documents (PDF, text, etc.)
2. Split into small chunks
3. Convert chunks to vectors (embeddings)
4. Store in vector database (ChromaDB)
5. When user asks question:
   - Convert question to vector
   - Find similar chunks
   - Send chunks + question to LLM
   - LLM gives answer using those chunks

Why RAG?
- LLMs don't know your company's data
- RAG lets you add your own knowledge without retraining
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import chromadb
import openai
import config
import os

router = APIRouter()

# --- Vector Database (like a smart search engine) ---
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="knowledge_base")

# --- LLM Client ---
llm_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)


# ============================================================
# MODELS
# ============================================================

class Document(BaseModel):
    """A piece of knowledge to add"""
    text: str
    source: str  # e.g., "company-policy.pdf"


class RAGQuestion(BaseModel):
    """User's question for RAG"""
    question: str


class RAGAnswer(BaseModel):
    """Answer with sources"""
    answer: str
    sources: list[str]
    context_used: str


# ============================================================
# ENDPOINTS
# ============================================================

@router.post("/add-knowledge")
def add_knowledge(doc: Document):
    """
    Step 1: Add documents to the knowledge base.
    In real life, this would be PDFs, web pages, databases, etc.
    """
    doc_id = f"doc_{collection.count()}"
    collection.add(
        documents=[doc.text],
        metadatas=[{"source": doc.source}],
        ids=[doc_id]
    )
    return {"message": f"Added document: {doc_id}", "total_docs": collection.count()}


@router.post("/ask-rag", response_model=RAGAnswer)
def ask_with_rag(q: RAGQuestion):
    """
    Step 2: Ask a question using RAG.

    Flow:
    Question -> Search Vector DB -> Get relevant chunks -> Send to LLM -> Answer
    """
    if collection.count() == 0:
        raise HTTPException(status_code=400, detail="No documents in knowledge base. Add some first using /add-knowledge")

    # 1. Search for relevant documents
    results = collection.query(
        query_texts=[q.question],
        n_results=min(3, collection.count())  # Get top 3 matches
    )

    # 2. Build context from search results
    context_chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    context = "\n---\n".join(context_chunks)

    # 3. Send question + context to LLM
    try:
        response = llm_client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Answer the question using ONLY the context provided. "
                        "If the context doesn't contain the answer, say 'I don't have enough information'."
                    )
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {q.question}"
                }
            ],
            max_tokens=300
        )

        return RAGAnswer(
            answer=response.choices[0].message.content,
            sources=sources,
            context_used=context[:200] + "..."  # Show first 200 chars
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-stats")
def knowledge_stats():
    """Check how many documents are in the knowledge base"""
    return {"total_documents": collection.count()}


@router.post("/load-sample-data")
def load_sample_data():
    """
    Load sample documents for demo purposes.
    In real life, you'd load from files, databases, or web scraping.
    """
    sample_docs = [
        {
            "text": "Our company provides 20 days of paid leave per year. Employees can carry forward up to 5 days to the next year. Sick leave is separate and provides 10 days per year.",
            "source": "hr-policy.pdf"
        },
        {
            "text": "The engineering team uses Python and FastAPI for backend services. All code must be reviewed by at least one senior engineer before merging. We deploy every Thursday.",
            "source": "engineering-handbook.pdf"
        },
        {
            "text": "Customer refund requests must be processed within 48 hours. Refunds over $500 require manager approval. All refunds are tracked in the finance dashboard.",
            "source": "customer-support-guide.pdf"
        },
        {
            "text": "New employees must complete security training within their first week. VPN access requires IT approval. All passwords must be at least 12 characters with special characters.",
            "source": "security-policy.pdf"
        },
        {
            "text": "Our AI products use RAG (Retrieval Augmented Generation) to answer questions from company documents. The system uses ChromaDB for vector storage and OpenAI for language understanding.",
            "source": "tech-architecture.pdf"
        }
    ]

    for i, doc in enumerate(sample_docs):
        collection.add(
            documents=[doc["text"]],
            metadatas=[{"source": doc["source"]}],
            ids=[f"sample_{i}"]
        )

    return {"message": f"Loaded {len(sample_docs)} sample documents", "total_docs": collection.count()}
