"""
Session 7: Redis Caching for LLM Responses

Why cache?
- LLM calls cost money ($0.002 per call)
- LLM calls are slow (1-3 seconds)
- Many users ask the same questions
- Cache = instant response + zero cost for repeated questions

Flow:
  Question comes in
       |
       v
  Check Redis cache --> HIT? --> Return cached answer (instant!)
       |
       v (MISS)
  Call LLM --> Get answer --> Save to cache --> Return answer
"""

import json
import hashlib
import redis
import config


class LLMCache:
    """Simple Redis cache for LLM responses"""

    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                decode_responses=True
            )
            self.redis.ping()
            self.enabled = True
            print("Redis cache connected!")
        except redis.ConnectionError:
            self.enabled = False
            print("Redis not available - caching disabled (this is OK for development)")

    def _make_key(self, question: str) -> str:
        """Create a cache key from the question"""
        # Hash the question so similar questions get different keys
        return "llm:" + hashlib.md5(question.lower().strip().encode()).hexdigest()

    def get(self, question: str) -> dict | None:
        """Check if we have a cached answer"""
        if not self.enabled:
            return None

        key = self._make_key(question)
        cached = self.redis.get(key)

        if cached:
            print(f"CACHE HIT: {question[:50]}...")
            return json.loads(cached)

        print(f"CACHE MISS: {question[:50]}...")
        return None

    def set(self, question: str, answer: dict, ttl_seconds: int = 3600):
        """Save an answer to cache (default: 1 hour)"""
        if not self.enabled:
            return

        key = self._make_key(question)
        self.redis.set(key, json.dumps(answer), ex=ttl_seconds)

    def stats(self) -> dict:
        """Get cache statistics"""
        if not self.enabled:
            return {"status": "disabled", "reason": "Redis not connected"}

        info = self.redis.info()
        return {
            "status": "enabled",
            "total_keys": self.redis.dbsize(),
            "memory_used": info.get("used_memory_human", "unknown"),
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
        }

    def clear(self):
        """Clear all cached responses"""
        if self.enabled:
            self.redis.flushdb()


# Global cache instance
cache = LLMCache()
