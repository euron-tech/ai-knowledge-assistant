# ============================================================
# Session 3: Dockerize our AI Knowledge Assistant
# ============================================================
# Think of Docker as: "Pack your entire app + all dependencies into ONE box"
# That box runs the same everywhere: your laptop, AWS, anywhere.

# Step 1: Start from a Python base image
FROM python:3.12-slim

# Step 2: Set working directory inside the container
WORKDIR /app

# Step 3: Install core packages from pre-downloaded wheels (fast, no network)
COPY wheels/ /tmp/wheels/
RUN pip install --no-cache-dir --no-index --find-links=/tmp/wheels/ \
    fastapi uvicorn pydantic redis httpx openai \
    && rm -rf /tmp/wheels/

# Step 4: Install chromadb from PyPI (needs network, large package)
RUN pip install --no-cache-dir --timeout=600 chromadb>=0.6.0

# Step 5: Copy our application code
COPY app/ .

# Step 6: Expose port 8000 (same port our FastAPI runs on)
EXPOSE 8000

# Step 7: Health check - AWS Load Balancer also does this, but Docker can too
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Step 8: Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
