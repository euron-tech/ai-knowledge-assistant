"""
Configuration - loads secrets from environment or AWS Secrets Manager.
RULE: Never hardcode API keys!
"""

import os


# --- LLM Settings ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key-here")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

# --- App Settings ---
APP_NAME = "AI Knowledge Assistant"
APP_VERSION = "1.0.0"
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# --- Redis Cache (Session 7) ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# --- AWS Settings ---
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
