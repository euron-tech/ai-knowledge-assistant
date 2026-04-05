# Session 6: Load Balancing + Auto Scaling

## What We Are Building
Making our system handle 1000s of users without crashing.

```
100 users at once
        |
        v
   Load Balancer (ALB)
    /    |    \
   v     v     v
 Container  Container  Container
   #1       #2         #3
```

## Why This Matters
- 1 container = ~100 concurrent users max
- Load Balancer = splits traffic across containers
- Auto Scaling = adds more containers when traffic increases

---

## How Load Balancing Works

### Layer 4 (NLB - Network Load Balancer)
- Just forwards traffic (fast, dumb)
- Doesn't look at HTTP content
- Use for: databases, raw TCP connections

### Layer 7 (ALB - Application Load Balancer)
- Smart routing based on URL paths
- Can route `/api` to one service, `/admin` to another
- Use for: web apps, APIs (this is what we use)

```
ALB Example:
  /ask      --> AI Service containers
  /health   --> Health check response
  /admin    --> Admin panel containers (future)
```

## Already Built! (Session 4)

Our Terraform already created:
- ALB (Application Load Balancer)
- Target Group with health checks
- Auto Scaling (2-6 containers, based on CPU)

Let's understand what we built:

### Health Check Flow:
```
ALB calls GET /health every 30 seconds
  |
  v
Response 200 = healthy (keep sending traffic)
Response 500 = unhealthy (stop sending traffic, replace container)
```

### Auto Scaling Flow:
```
Normal traffic: 2 containers running (minimum)
  |
  v (CPU goes above 70%)
Auto Scaling adds containers (up to 6)
  |
  v (traffic decreases, CPU drops)
Auto Scaling removes extra containers (back to 2)
```

---

## Demo: Test Load Balancing

### Step 1: Check current containers
```bash
aws ecs describe-services \
  --cluster ai-assistant-cluster \
  --services ai-assistant-service \
  --query 'services[0].{desired: desiredCount, running: runningCount}'
```

### Step 2: Send load to trigger scaling
```bash
# Install hey (load testing tool)
# Mac: brew install hey
# Or download from: https://github.com/rakyll/hey

# Send 1000 requests, 50 at a time
hey -n 1000 -c 50 http://YOUR_ALB_URL/health
```

### Step 3: Watch containers scale
```bash
# Watch ECS service (run this in another terminal)
watch -n 5 "aws ecs describe-services \
  --cluster ai-assistant-cluster \
  --services ai-assistant-service \
  --query 'services[0].{desired: desiredCount, running: runningCount}'"
```

You'll see `desiredCount` go from 2 to 3, 4, etc.!

---

## High Availability Explained

```
AWS Region: ap-south-1 (Mumbai)
  |
  +-- Availability Zone A (Data Center 1)
  |     |
  |     +-- Container #1
  |
  +-- Availability Zone B (Data Center 2)
        |
        +-- Container #2

If Zone A goes down --> Zone B still works
If Container #1 crashes --> ALB sends all traffic to #2
                        --> ECS auto-starts a new #1
```

This is why we created 2 subnets in 2 zones in Session 4.

---

## What Students Learn

| Concept | Simple Explanation |
|---------|-------------------|
| ALB | Traffic cop that distributes requests |
| NLB | Fast forward (Layer 4) vs Smart routing (Layer 7) |
| Target Group | List of healthy containers |
| Health Check | "Are you alive?" ping every 30s |
| Auto Scaling | Add/remove containers based on load |
| Multi-AZ | Same app in multiple data centers |

---

## Homework
1. Change auto scaling to trigger at 50% CPU instead of 70%
2. Add a scaling policy based on request count (not just CPU)
3. Use CloudWatch to view the CPU metrics of your containers
