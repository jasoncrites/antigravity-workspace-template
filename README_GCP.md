# Antigravity IDE Workspace for GCP Infrastructure

This is a customized Antigravity workspace configured specifically for managing your Google Cloud Platform infrastructure at `truckerbooks-mvp-prod`.

## What's Been Set Up

### ✅ Environment Configuration
- Python virtual environment with all dependencies
- MCP servers configured for BigQuery and GCP services
- GCP authentication using existing credentials
- Environment variables for truckerbooks-mvp-prod project

### ✅ MCP Server Integrations
- **BigQuery**: Direct access to all datasets and tables
- **Filesystem**: Local file operations
- **GitHub**: Repository management
- **Memory**: Persistent agent memory

### ✅ Custom Tools (Auto-Discovered)
Located in `src/tools/`:
- **cloud_run_tools.py**: Cloud Run service management
  - List services, get details, check health
  - Analyze costs, find dormant services
- **bigquery_tools.py**: BigQuery analysis
  - Execute queries, analyze cache performance
  - Model usage analysis, workflow efficiency

### ✅ Context Files (Auto-Injected)
Located in `.context/`:
- **gcp_infrastructure.md**: Complete infrastructure overview
  - 50+ Cloud Run services documented
  - 20+ BigQuery datasets cataloged
  - Architecture patterns and conventions
- **common_operations.md**: Common GCP operations
  - Cloud Run commands
  - BigQuery queries
  - Troubleshooting guides

## Quick Start

### 1. Activate Environment
```bash
cd /home/jasoncrites/antigravity-gcp-workspace
source venv/bin/activate
```

### 2. Configure API Keys (Optional)
If you want to use Anthropic API instead of default:
```bash
nano .env
# Add your ANTHROPIC_API_KEY if not already set in environment
```

### 3. Run the Agent
```bash
python src/agent.py
```

### 4. Try Sample Tasks
See `example_tasks.md` for ready-to-use prompts like:
- "Analyze Cloud Run costs for last 30 days"
- "Find dormant services with no traffic"
- "Check cache hit rates and savings"

## Your GCP Infrastructure at a Glance

### Cloud Run Services (50+)
- **AI/ML**: afs-brain-prod, afs-unified-gateway, apollo-gateway-v2
- **Healthcare**: sctpn-api, sctpn-security, sandy-care-mvp
- **Business**: truckerbooks-unified, llc-formation-service
- **Infrastructure**: afs-auto-healer, afs-observability

### BigQuery Datasets (20+)
- **Analytics**: cache_analytics, gateway_metrics, workflow_analytics
- **ML/AI**: afs_ml, afs_brain, afs_intelligence
- **Billing**: afs_billing, afs_metering, afs_cost_analysis
- **Operations**: afs_deployments, agent_logs, autonomous_agent

### Architecture Highlights
- Multi-level caching with Firestore
- Multi-model AI routing (Claude, Gemini, GPT, Granite)
- BQML models for cost prediction
- IAM-based security throughout

## Example Agent Interactions

### Cost Analysis
```
Agent: "Analyze service costs for the last month"

The agent will:
1. Query BigQuery cost data
2. Identify top spending services
3. Compare trends month-over-month
4. Generate savings recommendations
5. Create detailed report in artifacts/
```

### Infrastructure Health Check
```
Agent: "Check health of all Cloud Run services"

The agent will:
1. List all services
2. Call /health endpoints
3. Check service configurations
4. Identify issues
5. Suggest fixes
```

### Cache Optimization
```
Agent: "How can we improve cache hit rates?"

The agent will:
1. Query cache_analytics dataset
2. Analyze hit/miss patterns
3. Identify optimization opportunities
4. Calculate potential savings
5. Provide actionable recommendations
```

## Advanced Usage

### Multi-Agent Swarm
For complex tasks, use swarm orchestration:

```python
from src.swarm import SwarmOrchestrator

swarm = SwarmOrchestrator()

# Decompose complex infrastructure audit
result = swarm.execute("""
Conduct a comprehensive infrastructure audit:
1. Analyze costs across all services
2. Identify optimization opportunities
3. Check service health and performance
4. Generate executive summary with recommendations
""")
```

### Custom Tool Development
Add new tools by creating Python functions in `src/tools/`:

```python
# src/tools/my_custom_tool.py
def analyze_vpc_traffic(days: int = 7) -> dict:
    """
    Analyzes VPC traffic patterns.

    Args:
        days: Number of days to analyze

    Returns:
        Dictionary with traffic analysis
    """
    # Your implementation
    return {}
```

The tool is automatically discovered on next run!

### Adding Context
Add domain knowledge to `.context/` for automatic injection:

```bash
echo "## Custom Architecture Notes" > .context/my_notes.md
echo "Our services follow pattern X..." >> .context/my_notes.md
```

## Useful BigQuery Queries

### Top 10 Most Expensive Services
```sql
SELECT service_name, SUM(cost) as total_cost
FROM `truckerbooks-mvp-prod.gateway_metrics.request_logs`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY service_name
ORDER BY total_cost DESC
LIMIT 10
```

### Cache Performance
```sql
SELECT
  DATE(timestamp) as date,
  COUNT(*) as requests,
  SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END) as hits,
  ROUND(100.0 * SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END) / COUNT(*), 2) as hit_rate
FROM `truckerbooks-mvp-prod.cache_analytics.cache_metrics`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY date
ORDER BY date DESC
```

## Troubleshooting

### Agent Can't Access BigQuery
```bash
# Verify gcloud authentication
gcloud auth list

# Re-authenticate if needed
gcloud auth application-default login
```

### MCP Server Issues
```bash
# Check if MCP tools are available
npx -y @modelcontextprotocol/server-bigquery --version

# Reinstall if needed
npm cache clean --force
```

### Tool Not Discovered
```bash
# Restart agent after adding new tools
# Check tool syntax (must have docstring and type hints)
python src/agent.py
```

## Best Practices

1. **Start Small**: Begin with simple queries, then expand
2. **Verify Results**: Always verify agent recommendations
3. **Use Context**: Add project-specific knowledge to `.context/`
4. **Review Artifacts**: Check generated files for detailed analysis
5. **Iterate**: Refine prompts based on results

## Resources

- Original Template: https://github.com/study8677/antigravity-workspace-template
- Full Docs: `docs/en/`
- Example Tasks: `example_tasks.md`
- GCP Context: `.context/gcp_infrastructure.md`

## What's Next?

1. **Try the example tasks** in `example_tasks.md`
2. **Explore your data** using BigQuery tools
3. **Create custom agents** for specific workflows
4. **Add your own tools** for specialized operations
5. **Build swarms** for complex multi-step analysis

---

**Your infrastructure is now ready for AI-powered management!** 🚀

Start with: `python src/agent.py` and ask:
> "Analyze my Cloud Run infrastructure and suggest optimizations"
