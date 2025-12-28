# Quick Start Guide

## Get Started in 3 Minutes

### 1. Activate the Environment
```bash
cd /home/jasoncrites/antigravity-gcp-workspace
source venv/bin/activate
```

### 2. Run Your First Agent
```bash
python src/agent.py
```

### 3. Try These Example Prompts

#### Cost Analysis
```
Analyze Cloud Run service costs for the last 30 days and identify the top 10 most expensive services
```

#### Infrastructure Health
```
Check the health status of all my Cloud Run services and report any issues
```

#### Cache Performance
```
Analyze cache hit rates for the last 7 days and calculate total savings
```

#### Model Usage
```
Show me which AI models are most used and their costs for the last month
```

#### Service Optimization
```
Find all services that haven't received traffic in 14 days and calculate potential savings
```

## What You Have Available

### Automatic Tool Discovery
The agent automatically finds and uses these tools:

**Cloud Run Tools:**
- `list_cloud_run_services()` - List all services
- `get_service_details()` - Get service configuration
- `check_service_health()` - Health check services
- `analyze_service_costs()` - Cost analysis
- `find_dormant_services()` - Find unused services

**BigQuery Tools:**
- `query_bigquery()` - Execute SQL queries
- `analyze_cache_performance()` - Cache metrics
- `get_top_models_usage()` - Model usage stats
- `find_expensive_queries()` - Cost optimization
- `analyze_workflow_efficiency()` - Workflow analysis

### Automatic Context Injection
The agent knows about:
- All 213 Cloud Run services
- All 50 BigQuery datasets
- Your infrastructure architecture
- Common operations and patterns
- Best practices for GCP

### MCP Server Integration
Connected services:
- **BigQuery**: Direct database access
- **GitHub**: Repository management
- **Filesystem**: Local file operations
- **Memory**: Persistent agent memory

## Example Workflows

### Cost Optimization Workflow
1. "What are my top spending services?"
2. "Analyze the cache performance for those services"
3. "Find services with no recent traffic"
4. "Calculate total potential savings"

### Performance Monitoring
1. "Check health of all services"
2. "Show me services with high latency"
3. "Analyze model performance by provider"
4. "Recommend optimization opportunities"

### Infrastructure Audit
1. "List all services and their configurations"
2. "Identify over-provisioned services"
3. "Find duplicate or similar services"
4. "Generate consolidation recommendations"

## Advanced Features

### Multi-Agent Swarm
```python
from src.swarm import SwarmOrchestrator

swarm = SwarmOrchestrator()
result = swarm.execute("Your complex task here")
```

### Direct BigQuery Access
```python
from src.tools.bigquery_tools import query_bigquery

results = query_bigquery("""
  SELECT service_name, COUNT(*) as requests
  FROM `truckerbooks-mvp-prod.gateway_metrics.request_logs`
  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
  GROUP BY service_name
  ORDER BY requests DESC
  LIMIT 10
""")
```

### Custom Tool Development
Add new tools to `src/tools/` and they're automatically discovered!

## Tips for Success

1. **Be Specific**: "Analyze costs for services starting with 'afs-brain'" works better than "analyze costs"

2. **Iterate**: Start broad, then drill down
   - "Show me expensive services"
   - "Analyze afs-brain-prod in detail"
   - "What optimizations can reduce its cost?"

3. **Use Context**: Reference your infrastructure
   - "Our SCTPN services" (agent knows these are healthcare services)
   - "Our gateway services" (agent knows the gateway architecture)

4. **Check Artifacts**: All analysis creates files in `artifacts/`
   - Plans, logs, evidence, reports
   - Review for detailed insights

5. **Verify Results**: Always verify agent recommendations before implementation

## Common Issues

### "No module named 'requests'"
```bash
source venv/bin/activate  # Make sure venv is activated
pip install -r requirements.txt
```

### "BigQuery access denied"
```bash
gcloud auth application-default login
```

### "MCP server not found"
```bash
npm cache clean --force
# MCP servers install on-demand
```

## Next Steps

- See `README_GCP.md` for comprehensive documentation
- Check `example_tasks.md` for more task examples
- Explore `.context/` to understand available context
- Browse `src/tools/` to see available tools

## Need Help?

1. Run the test script: `./test_setup.sh`
2. Check logs in `artifacts/`
3. Review GCP context in `.context/gcp_infrastructure.md`
4. Read full docs in `docs/en/`

---

**Ready to optimize your infrastructure!** 🚀

Just run: `source venv/bin/activate && python src/agent.py`
