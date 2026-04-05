# Session 8: Production-Ready System

## What We Are Building
The final pieces to make our system production-grade:
1. Multi-region failover
2. Monitoring + alerts
3. API governance
4. Cost control

---

## Part 1: Multi-Region Failover

### Why?
> "If Mumbai data center catches fire, Singapore takes over"

```
Normal:
  Users --> Route53 --> Mumbai (ap-south-1) [HEALTHY]

Failover:
  Users --> Route53 --> Mumbai [DOWN!]
                   \--> Singapore (ap-southeast-1) [TAKES OVER]
```

### How to Set Up:

#### Step 1: Deploy same infrastructure in 2 regions
```bash
# Region 1: Mumbai
cd terraform
terraform apply -var="aws_region=ap-south-1"

# Region 2: Singapore
terraform apply -var="aws_region=ap-southeast-1"
```

#### Step 2: Route53 Health Check + Failover

```bash
# Create health check
aws route53 create-health-check --caller-reference $(date +%s) \
  --health-check-config '{
    "FullyQualifiedDomainName": "mumbai-alb.example.com",
    "Port": 80,
    "ResourcePath": "/health",
    "Type": "HTTP",
    "RequestInterval": 30,
    "FailureThreshold": 3
  }'
```

#### Step 3: DNS Failover Records
```bash
# Primary record (Mumbai)
aws route53 change-resource-record-sets --hosted-zone-id YOUR_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.yourdomain.com",
        "Type": "A",
        "SetIdentifier": "primary",
        "Failover": "PRIMARY",
        "AliasTarget": {
          "DNSName": "mumbai-alb-dns-name",
          "HostedZoneId": "ALB_ZONE_ID",
          "EvaluateTargetHealth": true
        },
        "HealthCheckId": "HEALTH_CHECK_ID"
      }
    }]
  }'

# Secondary record (Singapore) - same but with "SECONDARY"
```

---

## Part 2: Monitoring + Alerts

### CloudWatch Dashboard

```bash
# Create a simple dashboard
aws cloudwatch put-dashboard --dashboard-name ai-assistant \
  --dashboard-body '{
    "widgets": [
      {
        "type": "metric",
        "properties": {
          "title": "API Response Time",
          "metrics": [
            ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", "ai-assistant-alb"]
          ],
          "period": 60
        }
      },
      {
        "type": "metric",
        "properties": {
          "title": "Request Count",
          "metrics": [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "ai-assistant-alb"]
          ],
          "period": 60
        }
      },
      {
        "type": "metric",
        "properties": {
          "title": "ECS CPU Usage",
          "metrics": [
            ["AWS/ECS", "CPUUtilization", "ClusterName", "ai-assistant-cluster"]
          ],
          "period": 60
        }
      }
    ]
  }'
```

### Set Up Alerts

```bash
# Alert when error rate > 5%
aws cloudwatch put-metric-alarm \
  --alarm-name "ai-assistant-high-errors" \
  --metric-name "HTTPCode_Target_5XX_Count" \
  --namespace "AWS/ApplicationELB" \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions "arn:aws:sns:ap-south-1:YOUR_ACCOUNT:alerts"
```

---

## Part 3: API Governance

### Rate Limiting with API Gateway

```
User --> API Gateway --> ALB --> ECS Containers
              |
              +-- Rate limit: 100 requests/minute per API key
              +-- API key validation
              +-- Request logging
```

### Simple Rate Limiting in FastAPI (without API Gateway)

```python
from fastapi import Request, HTTPException
from collections import defaultdict
import time

# Simple in-memory rate limiter
request_counts = defaultdict(list)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    # Keep only requests from last 60 seconds
    request_counts[client_ip] = [
        t for t in request_counts[client_ip] if now - t < 60
    ]
    
    # Check limit (100 requests per minute)
    if len(request_counts[client_ip]) >= 100:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    request_counts[client_ip].append(now)
    return await call_next(request)
```

---

## Part 4: Cost Control

### Estimated Monthly Costs

| Resource | Cost |
|----------|------|
| ECS Fargate (2 containers, 0.25 vCPU) | ~$15/month |
| ALB | ~$20/month |
| ECR (Docker images) | ~$1/month |
| CloudWatch Logs | ~$5/month |
| Route53 | ~$1/month |
| ElastiCache Redis (small) | ~$15/month |
| **Total** | **~$57/month** |

### Cost Saving Tips:
1. Use Fargate Spot for non-critical workloads (70% cheaper)
2. Set up billing alerts in AWS
3. Use `terraform destroy` when not demoing
4. Cache aggressively to reduce LLM API costs

```bash
# Set billing alert
aws cloudwatch put-metric-alarm \
  --alarm-name "monthly-cost-alert" \
  --metric-name "EstimatedCharges" \
  --namespace "AWS/Billing" \
  --statistic Maximum \
  --period 86400 \
  --threshold 100 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --alarm-actions "arn:aws:sns:us-east-1:YOUR_ACCOUNT:billing-alerts"
```

---

## The Complete System (Everything Connected)

```
User
  |
  v
Route53 (DNS + Failover)
  |
  v
API Gateway (Rate Limit + API Keys)
  |
  v
ALB (Load Balancer)
  |
  +-------+-------+
  |       |       |
  v       v       v
ECS     ECS     ECS        (Auto-scaled containers)
  |
  +---> Redis (Cache)       Check cache first
  |
  +---> ChromaDB (RAG)      Search documents
  |
  +---> OpenAI (LLM)        Generate answer
  |
  +---> CloudWatch           Log everything
  |
  +---> SQS (Queue)          Handle heavy tasks
```

---

## What Students Learn

| Concept | Why It Matters |
|---------|---------------|
| Multi-Region | Zero downtime, even if a region fails |
| CloudWatch | See what's happening inside your system |
| Alerts | Get notified before users complain |
| Rate Limiting | Prevent abuse and control costs |
| Cost Control | Real companies track every dollar |

---

## Final Homework: Build Your Own System!

Create your own AI Knowledge Assistant for a specific use case:
1. Pick a domain (medical FAQ, legal docs, student handbook)
2. Load 20+ real documents
3. Deploy with Terraform
4. Set up CI/CD
5. Add caching
6. Present to the class with a live demo

This is your portfolio project! Show it in interviews.
