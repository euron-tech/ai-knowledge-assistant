# Session 7: Caching with Redis + Queuing with SQS

## What We Are Building
Two performance boosters:
1. **Cache** - Don't call the LLM for questions we've already answered
2. **Queue** - Handle traffic spikes without crashing

---

## Part 1: Redis Caching

### Why Cache LLM Responses?

| Without Cache | With Cache |
|---|---|
| Every question calls LLM | Repeated questions are instant |
| 1-3 seconds per response | <10ms for cached responses |
| $0.002 per call | $0 for cached calls |
| 1000 users = 1000 LLM calls | 1000 users = maybe 200 LLM calls |

### How It Works

```
User asks: "What is cloud computing?"
       |
       v
Check Redis cache
       |
  +----+----+
  |         |
  v         v
 HIT       MISS
  |         |
  v         v
Return     Call LLM
instantly   |
            v
          Save to Redis
            |
            v
          Return answer

Next user asks same question -> HIT -> Instant!
```

### Step 1: Run Redis locally

```bash
# Using Docker (easiest)
docker run -d -p 6379:6379 redis:7-alpine

# Or with docker-compose (already configured!)
docker-compose up redis
```

### Step 2: Test the cache

```bash
# First call - CACHE MISS (calls LLM, ~2 seconds)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'

# Second call - CACHE HIT (instant, <10ms)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'

# Check cache stats
curl http://localhost:8000/cache-stats
```

### Step 3: AWS ElastiCache (Production Redis)

In production, use AWS ElastiCache instead of running Redis yourself:

```bash
# Add to terraform/main.tf:
# Creates a managed Redis cluster in AWS
# (This is included in the advanced terraform config)
```

---

## Part 2: Queuing with SQS

### Why Queues?

```
Without queue:
  1000 requests at once --> API tries to handle all --> CRASH!

With queue:
  1000 requests at once --> Queue holds them --> API processes 10 at a time --> All succeed
```

### SQS Flow:

```
User Request --> API --> Put in SQS Queue --> Worker picks up --> Process --> Return
```

### When to Use:
- Heavy LLM calls (long documents, image processing)
- Batch processing (process 100 documents)
- Traffic spikes (Black Friday, viral moment)

### Simple SQS Example:

```python
import boto3

# Create SQS client
sqs = boto3.client('sqs', region_name='ap-south-1')
queue_url = 'https://sqs.ap-south-1.amazonaws.com/YOUR_ACCOUNT/ai-assistant-queue'

# Producer: Send message to queue
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='{"question": "What is AI?", "user_id": "123"}'
)

# Consumer: Read and process messages
response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
for message in response.get('Messages', []):
    # Process the question
    process_question(message['Body'])
    # Delete from queue (mark as done)
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
```

---

## What Students Learn

| Concept | Real World Example |
|---------|-------------------|
| Redis Cache | Google caches search results |
| Cache TTL | Cache expires after 1 hour (fresh data) |
| Cache Key | Hash of question = unique identifier |
| SQS Queue | Like a restaurant waitlist |
| Producer/Consumer | Waiter takes order / Chef cooks |

---

## Homework
1. Change cache TTL from 1 hour to 5 minutes - when would you want shorter TTL?
2. Add a `/cache-clear` endpoint that flushes the cache
3. Create an SQS queue in AWS Console and send/receive a message using Python
