#!/bin/bash
# Test script to verify Antigravity workspace setup

echo "=========================================="
echo "Antigravity GCP Workspace Setup Test"
echo "=========================================="
echo ""

# Check virtual environment
echo "✓ Checking virtual environment..."
if [ -d "venv" ]; then
    echo "  ✅ Virtual environment exists"
else
    echo "  ❌ Virtual environment not found"
    exit 1
fi

# Check dependencies
echo ""
echo "✓ Checking Python dependencies..."
source venv/bin/activate
python -c "import requests; import google.cloud" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ Required packages installed"
else
    echo "  ⚠️  Some packages may be missing (this is okay if you don't need them)"
fi

# Check MCP configuration
echo ""
echo "✓ Checking MCP servers configuration..."
if [ -f "mcp_servers.json" ]; then
    echo "  ✅ MCP servers configured"
    echo "  Enabled servers:"
    cat mcp_servers.json | grep '"enabled": true' -B 3 | grep '"name"' | cut -d'"' -f4 | sed 's/^/    - /'
else
    echo "  ❌ MCP configuration not found"
fi

# Check context files
echo ""
echo "✓ Checking context files..."
CONTEXT_FILES=$(ls .context/*.md 2>/dev/null | wc -l)
echo "  📚 $CONTEXT_FILES context files found:"
ls .context/*.md 2>/dev/null | xargs -n1 basename | sed 's/^/    - /'

# Check custom tools
echo ""
echo "✓ Checking custom tools..."
TOOL_FILES=$(ls src/tools/*.py 2>/dev/null | wc -l)
echo "  🛠️  $TOOL_FILES tool files found:"
ls src/tools/*.py 2>/dev/null | xargs -n1 basename | sed 's/^/    - /'

# Check GCP authentication
echo ""
echo "✓ Checking GCP authentication..."
gcloud config get-value project >/dev/null 2>&1
if [ $? -eq 0 ]; then
    PROJECT=$(gcloud config get-value project 2>/dev/null)
    echo "  ✅ GCP authenticated"
    echo "  Project: $PROJECT"
else
    echo "  ⚠️  GCP not authenticated (may need to run: gcloud auth login)"
fi

# Check BigQuery access
echo ""
echo "✓ Checking BigQuery access..."
bq ls --project_id=truckerbooks-mvp-prod >/dev/null 2>&1
if [ $? -eq 0 ]; then
    DATASETS=$(bq ls --project_id=truckerbooks-mvp-prod 2>/dev/null | wc -l)
    echo "  ✅ BigQuery accessible"
    echo "  Datasets: $((DATASETS - 2))"  # Subtract header lines
else
    echo "  ⚠️  BigQuery access issue (check permissions)"
fi

# Check Cloud Run access
echo ""
echo "✓ Checking Cloud Run access..."
gcloud run services list --limit=1 >/dev/null 2>&1
if [ $? -eq 0 ]; then
    SERVICES=$(gcloud run services list 2>/dev/null | wc -l)
    echo "  ✅ Cloud Run accessible"
    echo "  Services: $((SERVICES - 2))"  # Subtract header lines
else
    echo "  ⚠️  Cloud Run access issue (check permissions)"
fi

echo ""
echo "=========================================="
echo "Setup Verification Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Run agent: python src/agent.py"
echo "3. Try example tasks from example_tasks.md"
echo ""
echo "For detailed instructions, see README_GCP.md"
echo ""
