# Session 4: Terraform - Infrastructure as Code

## What We Are Building
Instead of clicking through AWS Console to create resources, we WRITE CODE that creates everything automatically.

```
terraform apply  -->  Creates VPC + ECS + Load Balancer + Auto Scaling
terraform destroy --> Deletes everything (no leftover charges!)
```

## Why Terraform Matters
| Without Terraform | With Terraform |
|---|---|
| Click 50 buttons in AWS Console | Run 1 command |
| Forget what you created | Everything is in code |
| Can't repeat for another project | Copy and reuse |
| Hard to delete cleanly | `terraform destroy` |

---

## Step 0: Prerequisites

```bash
# Install Terraform
# Windows: choco install terraform
# Mac: brew install terraform
# Verify:
terraform --version

# Install AWS CLI
# Verify:
aws --version

# Configure AWS
aws configure
# Enter: Access Key, Secret Key, Region (ap-south-1)
```

## Step 1: Store Your OpenAI Key in AWS Secrets Manager

```bash
# NEVER put API keys in code or Terraform files!
aws secretsmanager create-secret \
  --name openai-api-key \
  --secret-string "sk-your-openai-key-here" \
  --region ap-south-1

# Note the ARN from the output - you'll need it
```

## Step 2: Initialize Terraform

```bash
cd terraform

# Create your variables file
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Initialize (downloads AWS provider)
terraform init
```

Output:
```
Terraform has been successfully initialized!
```

## Step 3: Plan (Preview what will be created)

```bash
terraform plan
```

This shows EVERYTHING that will be created:
```
Plan: 18 to add, 0 to change, 0 to destroy.

  + aws_vpc.main
  + aws_subnet.public_a
  + aws_subnet.public_b
  + aws_lb.main              (Load Balancer)
  + aws_ecs_cluster.main     (Container cluster)
  + aws_ecs_service.app      (Runs 2 containers)
  + aws_appautoscaling_policy.cpu  (Auto-scale on CPU)
  ...
```

> ALWAYS run `plan` before `apply` to verify changes!

## Step 4: Apply (Create everything)

```bash
terraform apply
```

Type `yes` when prompted. Wait 3-5 minutes.

Output:
```
Apply complete! Resources: 18 added.

Outputs:
  app_url = "http://ai-assistant-alb-123456.ap-south-1.elb.amazonaws.com"
  ecr_repository_url = "123456.dkr.ecr.ap-south-1.amazonaws.com/ai-assistant"
```

## Step 5: Test

Open the `app_url` in your browser!

## Step 6: Destroy (Clean up - no more charges)

```bash
terraform destroy
```

---

## What Each Resource Does

```
VPC (Network)
  |
  +-- Subnet A (Mumbai Zone A)
  |     |
  +-- Subnet B (Mumbai Zone B)    <-- Two zones = High Availability
  |
  +-- Internet Gateway              <-- Door to internet
  |
  +-- Load Balancer (ALB)           <-- Distributes traffic
  |     |
  |     +-- Target Group            <-- Health checks containers
  |
  +-- ECS Cluster
        |
        +-- ECS Service              <-- Keeps 2 containers running
              |
              +-- Container A (Zone A)
              +-- Container B (Zone B)
              |
              +-- Auto Scaling        <-- Scale 2-6 based on CPU
```

---

## Key Concepts Explained

### What is a VPC?
Your own private network inside AWS. Like a building that only your app lives in.

### What is a Subnet?
A "room" inside the VPC. We use 2 rooms in different zones (buildings) so if one zone goes down, the other keeps working.

### What is a Security Group?
A firewall. We set rules:
- Load Balancer: Allow traffic from internet on port 80
- App: ONLY allow traffic from Load Balancer (not directly from internet)

### What is ECS Fargate?
AWS runs your Docker containers without you managing servers. You just say "run 2 containers" and AWS handles the rest.

---

## Terraform Commands Cheat Sheet

| Command | What it does |
|---------|-------------|
| `terraform init` | Download providers, setup |
| `terraform plan` | Preview changes (DRY RUN) |
| `terraform apply` | Create/update resources |
| `terraform destroy` | Delete everything |
| `terraform output` | Show output values |
| `terraform state list` | List created resources |

---

## Homework
1. Change `app_count` from 2 to 3, run `terraform plan` - what changes?
2. Add a new output that shows the VPC ID
3. Change the region to `us-east-1` - what happens to the availability zones?
