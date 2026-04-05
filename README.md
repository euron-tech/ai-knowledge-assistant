# AI Knowledge Assistant - Production-Ready GenAI Platform on AWS

A complete, connected teaching system that builds a production-grade AI platform step by step.

## The System We Build

```
User --> Route53 --> ALB --> ECS Containers --> Redis Cache
                                    |
                                    +--> ChromaDB (RAG) --> OpenAI (LLM) --> Response
```

One story. One system. One deployment flow.

---

## Project Structure

```
ai-knowledge-assistant/
|
|-- app/                    # Application code
|   |-- main.py             # FastAPI app + /ask endpoint (Session 1)
|   |-- rag.py              # RAG pipeline + /ask-rag endpoint (Session 2)
|   |-- cache.py            # Redis caching (Session 7)
|   |-- config.py           # Configuration (environment variables)
|   |-- requirements.txt    # Python dependencies
|
|-- terraform/              # Infrastructure as Code (Session 4)
|   |-- main.tf             # VPC + ECS + ALB + Auto Scaling
|   |-- variables.tf        # Configurable values
|   |-- outputs.tf          # Output values after deploy
|
|-- .github/workflows/      # CI/CD Pipeline (Session 5)
|   |-- deploy.yml          # Auto build + deploy on push
|
|-- docs/                   # Session-wise documentation
|   |-- session-1-api.md
|   |-- session-2-rag.md
|   |-- session-3-docker.md
|   |-- session-4-terraform.md
|   |-- session-5-cicd.md
|   |-- session-6-scaling.md
|   |-- session-7-caching.md
|   |-- session-8-production.md
|
|-- Dockerfile              # Container packaging (Session 3)
|-- docker-compose.yml      # Local multi-container setup
|-- scripts/setup.sh        # One-command setup
```

---

## Session Flow (How to Teach)

| Session | Topic | What Students Build | Key File |
|---------|-------|-------------------|----------|
| 1 | Base API + LLM | FastAPI + OpenAI call | `app/main.py` |
| 2 | RAG | Vector search + knowledge base | `app/rag.py` |
| 3 | Docker | Containerize the app | `Dockerfile` |
| 4 | Terraform | Create AWS infrastructure with code | `terraform/main.tf` |
| 5 | CI/CD | Auto-deploy on git push | `.github/workflows/deploy.yml` |
| 6 | Scaling | Load balancer + auto scaling | (already in terraform) |
| 7 | Caching | Redis cache for LLM responses | `app/cache.py` |
| 8 | Production | Multi-region, monitoring, governance | (docs + AWS commands) |

Each session builds on the previous one. Nothing is standalone.

---

## Quick Start (5 minutes)

### 1. Clone and setup
```bash
git clone <your-repo-url>
cd ai-knowledge-assistant
bash scripts/setup.sh
```

### 2. Set your OpenAI key
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### 3. Run the app
```bash
cd app
python main.py
```

### 4. Open Swagger docs
```
http://localhost:8000/docs
```

### 5. Try these endpoints

| Endpoint | What it does |
|----------|-------------|
| `GET /` | Home page (is API running?) |
| `GET /health` | Health check (for load balancer) |
| `POST /ask` | Ask LLM a question |
| `POST /load-sample-data` | Load 5 demo documents |
| `POST /ask-rag` | Ask question using your documents |
| `GET /knowledge-stats` | How many documents loaded? |

---

## How Sessions Connect

```
Session 1: Build the API          --> "We have an AI that answers questions"
     |
Session 2: Add RAG               --> "Now it answers from OUR documents"
     |
Session 3: Dockerize             --> "Now it runs the same everywhere"
     |
Session 4: Terraform             --> "Now AWS infrastructure is automated"
     |
Session 5: CI/CD                 --> "Now deployment is automated"
     |
Session 6: Load Balancing        --> "Now it handles 1000s of users"
     |
Session 7: Caching + Queuing     --> "Now it's fast and cost-efficient"
     |
Session 8: Production            --> "Now it never goes down"
```

---

## Prerequisites

| Tool | Version | Needed For |
|------|---------|-----------|
| Python | 3.11+ | All sessions |
| Docker | Latest | Session 3+ |
| Terraform | 1.0+ | Session 4 |
| AWS CLI | v2 | Session 4+ |
| Git | Latest | Session 5 |

---

## AWS Resources Created (and estimated costs)

| Resource | Purpose | Monthly Cost |
|----------|---------|-------------|
| VPC + Subnets | Network | Free |
| ECS Fargate (2 tasks) | Run containers | ~$15 |
| ALB | Load balancer | ~$20 |
| ECR | Docker image storage | ~$1 |
| CloudWatch | Logs + monitoring | ~$5 |
| Secrets Manager | API key storage | ~$1 |
| **Total** | | **~$42/month** |

> Use `terraform destroy` after demos to avoid charges.

---

## Credentials Needed

| What | Where to Get | Used In |
|------|-------------|---------|
| OpenAI API Key | platform.openai.com | Session 1-2 |
| AWS Access Key | AWS IAM Console | Session 4+ |
| AWS Secret Key | AWS IAM Console | Session 4+ |
| GitHub Account | github.com | Session 5 |
