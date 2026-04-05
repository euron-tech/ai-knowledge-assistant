# Session 2: Add RAG (Retrieval Augmented Generation)

## What We Are Building
Adding a "brain" to our API. Instead of just calling the LLM with a question, we first search our own documents, then send relevant info + question to the LLM.

```
User Question
     |
     v
Search our documents (Vector DB)
     |
     v
Found relevant chunks
     |
     v
Send chunks + question to LLM
     |
     v
LLM answers using OUR data
```

## Why RAG Matters
- ChatGPT doesn't know your company's policies, products, or data
- Fine-tuning is expensive ($$$) and slow
- RAG = cheap, fast, and you can update documents anytime

---

## Step 1: Start the API (same as Session 1)

```bash
cd app
python main.py
```

## Step 2: Load Sample Documents

Open http://localhost:8000/docs (Swagger UI)

Call `POST /load-sample-data`

Response:
```json
{"message": "Loaded 5 sample documents", "total_docs": 5}
```

## Step 3: Ask a RAG Question

Call `POST /ask-rag`:
```json
{"question": "How many days of leave do I get?"}
```

Response:
```json
{
  "answer": "You get 20 days of paid leave per year, with the ability to carry forward up to 5 days. Additionally, you get 10 days of sick leave separately.",
  "sources": ["hr-policy.pdf"],
  "context_used": "Our company provides 20 days of paid leave per year. Employees can carry forward up to 5 days..."
}
```

Notice: The answer comes from OUR document, not from ChatGPT's general knowledge!

## Step 4: Add Your Own Document

Call `POST /add-knowledge`:
```json
{
  "text": "The office cafeteria is open from 8 AM to 6 PM. Free coffee and tea are available all day.",
  "source": "office-guide.pdf"
}
```

Now ask: "What time does the cafeteria close?"

---

## How Vector Search Works (Simple Explanation)

```
Normal Search:  "leave policy" -> looks for exact words
Vector Search:  "how many holidays" -> understands MEANING -> finds "leave policy" document
```

This is why RAG is powerful - it understands meaning, not just keywords.

### The 5-Step RAG Pipeline

| Step | What Happens | Tool |
|------|-------------|------|
| 1. Load | Read documents | Python |
| 2. Chunk | Split into small pieces | Text splitter |
| 3. Embed | Convert text to numbers (vectors) | OpenAI / Sentence Transformers |
| 4. Store | Save vectors in database | ChromaDB |
| 5. Query | Search + LLM answer | ChromaDB + OpenAI |

---

## Compare: /ask vs /ask-rag

| Feature | /ask (Session 1) | /ask-rag (Session 2) |
|---------|------------------|---------------------|
| Source | LLM's training data | Your documents |
| Accuracy | General knowledge | Specific to your data |
| Hallucination | Can make things up | Grounded in real docs |
| Cost | Lower (1 LLM call) | Slightly higher (search + LLM) |
| Use case | General questions | Company/domain specific |

---

## Homework
1. Add 10 more documents about a topic you like (e.g., cricket rules, cooking recipes)
2. Test what happens when you ask a question that's NOT in the documents
3. Change `n_results=3` to `n_results=1` - does the answer quality change?
4. Add a `/delete-knowledge` endpoint that removes a document by ID
