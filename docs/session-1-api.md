# Session 1: Build the Base API + LLM Call

## What We Are Building
A simple API that takes a question and returns an answer from an LLM (like ChatGPT).

```
User sends question --> Our API --> Calls OpenAI --> Returns answer
```

## Why This Matters
Every AI product (ChatGPT, Copilot, Gemini) is just an API talking to an LLM behind the scenes. Today we build that exact thing.

---

## Step 1: Setup Project

```bash
# Create project folder
mkdir ai-knowledge-assistant
cd ai-knowledge-assistant

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt
```

## Step 2: Set Your API Key

```bash
# Windows (PowerShell):
$env:OPENAI_API_KEY="sk-your-key-here"

# Mac/Linux:
export OPENAI_API_KEY="sk-your-key-here"
```

> RULE: NEVER put API keys in code. Always use environment variables.

## Step 3: Run the API

```bash
cd app
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 4: Test It

### Test 1 - Home page
Open browser: http://localhost:8000

You should see:
```json
{"message": "AI Knowledge Assistant is running!", "version": "1.0.0"}
```

### Test 2 - Health check
Open: http://localhost:8000/health

```json
{"status": "healthy"}
```

### Test 3 - Ask a question
Open: http://localhost:8000/docs (Swagger UI)

Click on `/ask` -> Try it out -> Enter:
```json
{"question": "What is cloud computing in one line?"}
```

You get back:
```json
{
  "answer": "Cloud computing is accessing computing resources over the internet instead of your local machine.",
  "source": "llm"
}
```

### Test 4 - Using curl
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```

---

## What Students Learn
| Concept | Real World Use |
|---------|---------------|
| FastAPI | Building REST APIs (every tech company uses this) |
| Pydantic Models | Input validation (prevents bad data) |
| OpenAI Client | Calling LLMs programmatically |
| Environment Variables | Secret management basics |
| Health Endpoint | Load balancers need this (Session 6) |

---

## Key Code Explained

### Why `response_model=Answer`?
FastAPI auto-validates the response. If our code returns wrong data, it catches the error before the user sees it.

### Why `/health` endpoint?
When we deploy to AWS (Session 6), the Load Balancer will call `/health` every 30 seconds. If it fails, AWS replaces the container automatically.

### Why `max_tokens=200`?
Controls cost. Each token costs money. In production, you always set limits.

---

## Homework
1. Change the system prompt to make the AI respond like a pirate
2. Add a new endpoint `/summarize` that takes long text and returns a summary
3. Add a `temperature` parameter to the `/ask` endpoint (0 = factual, 1 = creative)
