# Common GCP Operations

## Cloud Run Management

### Listing Services
```bash
gcloud run services list --region=us-central1
```

### Service Details
```bash
gcloud run services describe SERVICE_NAME --region=us-central1
```

### Updating Service Configuration
```bash
gcloud run services update SERVICE_NAME \
  --region=us-central1 \
  --memory=2Gi \
  --cpu=2 \
  --min-instances=0 \
  --max-instances=10
```

### Deployment
```bash
gcloud run deploy SERVICE_NAME \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated  # or --no-allow-unauthenticated for private
```

## BigQuery Operations

### Query Execution
```bash
bq query --use_legacy_sql=false "
SELECT * FROM \`truckerbooks-mvp-prod.cache_analytics.cache_metrics\`
LIMIT 10
"
```

### Dataset Operations
```bash
# List datasets
bq ls --project_id=truckerbooks-mvp-prod

# Create dataset
bq mk --dataset truckerbooks-mvp-prod:new_dataset

# Describe dataset
bq show truckerbooks-mvp-prod:dataset_name
```

### Table Operations
```bash
# List tables
bq ls truckerbooks-mvp-prod:dataset_name

# Describe table
bq show --schema truckerbooks-mvp-prod:dataset_name.table_name
```

## Service Health Checks

### Check Service Status
```bash
curl https://SERVICE_URL/health
```

### Check with Authentication
```bash
TOKEN=$(gcloud auth print-identity-token)
curl -H "Authorization: Bearer $TOKEN" https://SERVICE_URL/health
```

## Log Analysis

### View Recent Logs
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=SERVICE_NAME" \
  --limit=50 \
  --format=json
```

### Search for Errors
```bash
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit=50
```

## Cost Analysis

### Service Cost Query
```sql
SELECT
  service_name,
  SUM(cost) as total_cost,
  COUNT(*) as request_count
FROM `truckerbooks-mvp-prod.afs_billing.usage_metrics`
WHERE DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY service_name
ORDER BY total_cost DESC
```

### Cache Savings Query
```sql
SELECT
  DATE(timestamp) as date,
  SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END) as cache_hits,
  COUNT(*) as total_requests,
  SUM(savings) as total_savings_usd
FROM `truckerbooks-mvp-prod.cache_analytics.cache_metrics`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date DESC
```

## Common Issues & Solutions

### Issue: Service Not Responding
1. Check service status: `gcloud run services describe SERVICE_NAME`
2. Check recent logs for errors
3. Verify IAM permissions
4. Check if service is private (requires authentication)

### Issue: High Costs
1. Query usage metrics in BigQuery
2. Check for services with min_instances > 0
3. Analyze cache hit rates
4. Review unnecessary service duplication

### Issue: Slow Performance
1. Check service memory/CPU allocation
2. Analyze cold start times
3. Review database query performance
4. Check for cache misses

## Security Best Practices

### Private Services
- Use `--no-allow-unauthenticated` for internal services
- Implement IAM-based access control
- Use service accounts for inter-service communication

### API Keys
- Store in Secret Manager
- Rotate regularly
- Use environment variables for configuration

### Data Protection
- Enable encryption at rest
- Use VPC connectors for database access
- Implement audit logging
