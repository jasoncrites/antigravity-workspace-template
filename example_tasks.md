# Example Tasks for GCP Infrastructure Agents

## Cost Optimization Tasks

### 1. Analyze Service Costs
```
Analyze Cloud Run service costs for the last 30 days and identify the top 10 most expensive services
```

### 2. Find Dormant Services
```
Find all Cloud Run services that haven't received traffic in the last 14 days and calculate potential cost savings
```

### 3. Cache Optimization
```
Analyze cache performance for the last 7 days and provide recommendations for improving hit rates
```

## Infrastructure Analysis

### 4. Service Health Check
```
Check the health status of all Cloud Run services and create a report of any unhealthy services
```

### 5. Resource Utilization
```
Analyze memory and CPU allocation across all services and identify over-provisioned services
```

### 6. Model Usage Analysis
```
Analyze AI model usage patterns, identify the most frequently used models, and calculate cost per model
```

## Data Analysis

### 7. BigQuery Dataset Audit
```
List all BigQuery datasets, identify their sizes, and find any unused or redundant datasets
```

### 8. Workflow Efficiency
```
Analyze workflow execution efficiency, success rates, and identify bottlenecks in the workflow pipeline
```

### 9. API Performance
```
Analyze API gateway performance metrics including latency, error rates, and throughput
```

## Security & Compliance

### 10. Service Access Audit
```
Identify all publicly accessible Cloud Run services and verify if they should be public or private
```

### 11. Cost Anomaly Detection
```
Analyze recent spending patterns and identify any unusual cost spikes or anomalies
```

### 12. Service Consolidation
```
Identify similar or duplicate services that could be consolidated to reduce complexity and costs
```

## Example Agent Prompts

### Infrastructure Audit Agent
```python
"""
Mission: Conduct a comprehensive infrastructure audit

Tasks:
1. List all Cloud Run services and their configurations
2. Check health status of each service
3. Analyze cost trends over the last 30 days
4. Identify dormant or underutilized services
5. Generate recommendations for optimization

Deliverables:
- Detailed audit report in artifacts/
- Cost optimization recommendations
- List of services for potential decommissioning
"""
```

### Cost Optimization Agent
```python
"""
Mission: Optimize GCP infrastructure costs

Tasks:
1. Query BigQuery for cost data across all services
2. Analyze cache hit rates and potential savings
3. Identify services with inefficient resource allocation
4. Calculate ROI for optimization opportunities
5. Create actionable optimization plan

Deliverables:
- Cost analysis report
- Optimization recommendations with expected savings
- Implementation priority matrix
"""
```

### Performance Monitoring Agent
```python
"""
Mission: Monitor and analyze system performance

Tasks:
1. Collect performance metrics from BigQuery
2. Analyze API latency and throughput
3. Identify performance bottlenecks
4. Monitor cache effectiveness
5. Generate performance dashboard

Deliverables:
- Performance analysis report
- Bottleneck identification
- Optimization recommendations
"""
```

## Running Example Tasks

### Using the Agent CLI
```bash
cd /home/jasoncrites/antigravity-gcp-workspace
source venv/bin/activate

# Run a simple analysis
python src/agent.py

# Then provide one of the prompts above
```

### Using Swarm Mode
```python
from src.swarm import SwarmOrchestrator

swarm = SwarmOrchestrator()
result = swarm.execute("Analyze Cloud Run service costs and identify optimization opportunities")
```

## Expected Outputs

All agent tasks will generate artifacts in the `artifacts/` directory:
- `plan_*.md` - Execution plans
- `log_*.json` - Detailed execution logs
- `evidence_*.json` - Supporting data and analysis
- `report_*.md` - Final reports and recommendations

## Tips for Effective Use

1. **Be Specific**: Provide clear, specific goals for better results
2. **Set Context**: Reference specific datasets or services when known
3. **Iterative Analysis**: Start broad, then drill down into specifics
4. **Verify Results**: Always verify agent recommendations before implementation
5. **Save Artifacts**: Review generated artifacts for detailed insights
