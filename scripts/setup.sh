#!/bin/bash
# ============================================================
# Quick Setup Script for AI Knowledge Assistant
# Run this once to set up everything locally
# ============================================================

echo "=== AI Knowledge Assistant Setup ==="
echo ""

# Step 1: Check Python
echo "Checking Python..."
python --version 2>/dev/null || python3 --version 2>/dev/null || {
    echo "ERROR: Python not found. Install Python 3.11+"
    exit 1
}

# Step 2: Create virtual environment
echo "Creating virtual environment..."
python -m venv venv 2>/dev/null || python3 -m venv venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate

# Step 3: Install dependencies
echo "Installing dependencies..."
pip install -r app/requirements.txt

# Step 4: Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "WARNING: OPENAI_API_KEY not set!"
    echo "Set it with:"
    echo "  export OPENAI_API_KEY='sk-your-key-here'   (Mac/Linux)"
    echo "  set OPENAI_API_KEY=sk-your-key-here        (Windows CMD)"
    echo ""
fi

# Step 5: Check Docker
echo "Checking Docker..."
docker --version 2>/dev/null || echo "WARNING: Docker not found (needed for Session 3+)"

# Step 6: Check Terraform
echo "Checking Terraform..."
terraform --version 2>/dev/null || echo "WARNING: Terraform not found (needed for Session 4)"

# Step 7: Check AWS CLI
echo "Checking AWS CLI..."
aws --version 2>/dev/null || echo "WARNING: AWS CLI not found (needed for Session 4+)"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To start the app:"
echo "  cd app"
echo "  python main.py"
echo ""
echo "Then open: http://localhost:8000/docs"
