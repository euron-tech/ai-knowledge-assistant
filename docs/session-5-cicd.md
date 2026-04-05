# Session 5: CI/CD with GitHub Actions

## What We Are Building
Automatic deployment: Push code to GitHub -> Tests run -> Docker builds -> Deploys to AWS.

```
Developer pushes code
        |
        v
GitHub Actions triggers
        |
        v
   Run Tests -----> FAIL? --> Stop. Fix the code.
        |
        v (PASS)
   Build Docker Image
        |
        v
   Push to AWS ECR
        |
        v
   Deploy to ECS
        |
        v
   Users get new version!
```

## Why CI/CD Matters
Without CI/CD:
- Manual build, manual upload, manual deploy
- "Did you run the tests?" "Uh... I forgot"
- Deploy on Friday at 5 PM -> break everything -> weekend ruined

With CI/CD:
- Every push is tested automatically
- Every merge to `main` deploys automatically
- Broken code never reaches production

---

## Step 1: Create GitHub Repository

```bash
# From project root
git init
git add .
git commit -m "Initial commit - AI Knowledge Assistant"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ai-assistant.git
git push -u origin main
```

## Step 2: Add AWS Secrets to GitHub

Go to: GitHub Repo -> Settings -> Secrets and variables -> Actions

Add these secrets:

| Secret Name | Value |
|------------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |

> These secrets are encrypted. Nobody can read them, not even repo admins.

## Step 3: Create Branch Strategy

```bash
# Create dev branch
git checkout -b dev

# Make changes on dev
# ... edit code ...
git add .
git commit -m "Add new feature"
git push origin dev

# Create Pull Request on GitHub: dev -> main
# When PR is merged -> CI/CD auto-deploys!
```

### Branch Flow:
```
feature-branch --> dev (testing) --> main (production)
                     |                  |
                  Run tests          Run tests + Deploy
```

## Step 4: Watch It Work

1. Make a small change (edit the welcome message in `main.py`)
2. Push to `main`
3. Go to GitHub -> Actions tab
4. Watch the pipeline run in real-time!

```
[Test]  Running tests...         (30 seconds)
[Test]  All tests passed!
[Build] Building Docker image... (2 minutes)
[Build] Pushing to ECR...        (1 minute)
[Deploy] Deploying to ECS...     (3 minutes)
[Deploy] Deployment complete!
```

## Step 5: Rollback (If Something Breaks)

### Option A: Git Revert
```bash
# Undo the last commit
git revert HEAD
git push origin main
# CI/CD auto-deploys the fix!
```

### Option B: ECS Manual Rollback
```bash
# List recent task definitions
aws ecs list-task-definitions --family ai-assistant --sort DESC

# Update service to use previous version
aws ecs update-service \
  --cluster ai-assistant-cluster \
  --service ai-assistant-service \
  --task-definition ai-assistant:PREVIOUS_VERSION
```

---

## Understanding the Pipeline File

Our `.github/workflows/deploy.yml` has 2 jobs:

### Job 1: `test`
- Runs on every push AND every pull request
- Installs Python, installs dependencies
- Runs basic import tests
- If this fails, nothing else runs

### Job 2: `deploy`
- Only runs on push to `main` (not on PRs)
- Only runs if `test` passes (`needs: test`)
- Builds Docker image
- Pushes to ECR
- Deploys to ECS

---

## What Students Learn

| Concept | Real World Use |
|---------|---------------|
| GitHub Actions | Most popular CI/CD tool |
| Secrets | Secure credential storage |
| Branch strategy | Team collaboration |
| Auto deploy | Zero-downtime releases |
| Rollback | Recovery from bad deploys |

---

## Homework
1. Add a step to the pipeline that runs `python -m pytest` (create a simple test first)
2. Add a Slack notification step that posts to a channel when deploy succeeds
3. Create a `staging` branch that deploys to a separate ECS service
