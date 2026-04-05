"""
Session 1: Base FastAPI + LLM Call
Session 2: + RAG endpoint
Session 6: + Health check for Load Balancer
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import config

# --- App Setup ---
app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)

# --- LLM Client ---
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)


# ============================================================
# REQUEST / RESPONSE MODELS
# ============================================================

class Question(BaseModel):
    """What the user sends"""
    question: str


class Answer(BaseModel):
    """What we send back"""
    answer: str
    source: str  # "llm" or "rag"


# ============================================================
# SESSION 1 ENDPOINTS
# ============================================================

@app.get("/")
def home():
    """Simple home page - proves the API is running"""
    return {
        "message": "AI Knowledge Assistant is running!",
        "version": config.APP_VERSION,
        "deployed_via": "CI/CD Pipeline",
        "infrastructure": "AWS ECS + ALB + Auto Scaling"
    }


@app.get("/health")
def health():
    """Health check - Load Balancer will call this every 30 seconds"""
    return {"status": "healthy"}


@app.post("/ask", response_model=Answer)
def ask_llm(q: Question):
    """
    SESSION 1: Simple LLM call
    User sends question -> We call OpenAI -> Return answer
    """
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Give short, clear answers."},
                {"role": "user", "content": q.question}
            ],
            max_tokens=200
        )
        return Answer(
            answer=response.choices[0].message.content,
            source="llm"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# SESSION 2 ENDPOINTS (RAG) - imported from rag.py
# ============================================================

from rag import router as rag_router
app.include_router(rag_router)


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=config.APP_PORT, reload=True)
