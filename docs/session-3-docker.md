# Session 3: Dockerize + Deploy to AWS ECS

## What We Are Building
Packaging our app into a Docker container so it runs the same everywhere - laptop, AWS, any cloud.

```
Your Code + Dependencies --> Docker Image --> Runs Anywhere
```

## Why Docker Matters
Without Docker:
- "It works on my machine!" (but breaks on server)
- Different Python versions, missing libraries, config issues

With Docker:
- Same environment everywhere
- One command to run
- Easy to scale (just run more containers)

---

## Step 1: Install Docker
- Windows: Download Docker Desktop from docker.com
- Verify: `docker --version`

## Step 2: Build the Image

```bash
# From project root folder
docker build -t ai-assistant .
```

What happens:
```
Step 1/8: FROM python:3.11-slim        -> Downloads Python
Step 3/8: COPY requirements.txt .       -> Copies requirements
Step 4/8: RUN pip install ...           -> Installs libraries
Step 5/8: COPY app/ .                   -> Copies your code
Step 8/8: CMD uvicorn ...               -> Sets startup command
```

## Step 3: Run the Container

```bash
# Run with your API key
docker run -p 8000:8000 -e OPENAI_API_KEY="sk-your-key" ai-assistant
```

Test: Open http://localhost:8000 - same as before, but now running inside Docker!

## Step 4: Run with Docker Compose (App + Redis)

```bash
# Create .env file with your key
echo "OPENAI_API_KEY=sk-your-key" > .env

# Start everything
docker-compose up

# Stop everything
docker-compose down
```

This starts:
- Your AI app on port 8000
- Redis on port 6379

---

## Step 5: Push to AWS ECR (Elastic Container Registry)

ECR = Docker Hub but inside AWS (private, secure).

```bash
# 1. Login to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

# 2. Create repository
aws ecr create-repository --repository-name ai-assistant

# 3. Tag the image
docker tag ai-assistant:latest YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/ai-assistant:latest

# 4. Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/ai-assistant:latest
```

## Step 6: Deploy to ECS (Elastic Container Service)

ECS = AWS runs your Docker containers for you.

```
You push image to ECR --> ECS pulls it --> Runs your container --> Users access it
```

We will automate this with Terraform (Session 4) and CI/CD (Session 5).

---

## Docker Commands Cheat Sheet

| Command | What it does |
|---------|-------------|
| `docker build -t name .` | Build image from Dockerfile |
| `docker run -p 8000:8000 name` | Run container |
| `docker ps` | List running containers |
| `docker stop <id>` | Stop a container |
| `docker logs <id>` | View container logs |
| `docker-compose up` | Start all services |
| `docker-compose down` | Stop all services |
| `docker images` | List all images |

---

## What Students Learn

| Concept | Real World Use |
|---------|---------------|
| Dockerfile | Package any app for deployment |
| Docker Compose | Run multi-container apps locally |
| ECR | Private container registry on AWS |
| ECS | AWS manages your containers |
| Health Check | Auto-restart unhealthy containers |

---

## Homework
1. Change the Dockerfile to use Python 3.12 instead of 3.11
2. Add a `nginx` service to docker-compose.yml as a reverse proxy
3. Run `docker stats` while the container is running - observe CPU and memory usage
