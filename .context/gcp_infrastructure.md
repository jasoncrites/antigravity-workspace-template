# GCP Infrastructure Overview

## Project Information
- **Project ID**: truckerbooks-mvp-prod
- **Primary Region**: us-central1
- **Service Account**: truckerbooks-mvp-prod@appspot.gserviceaccount.com

## Cloud Run Services (50+ services)

### Core AI/ML Services
- **afs-brain-prod**: Main AI brain service (4GB RAM, 4 CPU)
- **afs-unified-gateway**: Primary API gateway with caching and routing
- **afs-ai-gateway**: AI model routing and management
- **apollo-gateway-v2**: GraphQL gateway for AI queries

### Gateway & Routing Services
- **afs-gateway-prod**: Production API gateway
- **afs-bridge-gateway**: Bridge gateway for service mesh
- **afs-quantum-gateway**: Quantum-inspired routing
- **afs-secure-proxy**: Security proxy layer

### Healthcare/SCTPN Services
- **sctpn-api**: Healthcare API service
- **sctpn-security**: Security and compliance layer
- **sctpn-ehr**: Electronic Health Records
- **sandy-care-mvp**: Sandy Care healthcare platform

### Infrastructure Services
- **afs-auto-healer**: Automated service recovery
- **afs-auto-deploy**: Automated deployment system
- **afs-build-trigger**: CI/CD triggers
- **afs-observability**: Monitoring and observability

### Business Applications
- **truckerbooks-unified**: Trucking industry application
- **truckerbooks-pro**: Professional tier
- **llc-formation-service**: LLC formation automation

## BigQuery Datasets

### Analytics & Telemetry
- **cache_analytics**: Cache hit/miss metrics, optimization data
- **gateway_metrics**: API gateway performance and usage
- **workflow_analytics**: Workflow execution and training data
- **afs_analytics**: General AFS platform analytics

### ML & AI
- **afs_ml**: Machine learning model data
- **afs_brain**: Brain service telemetry
- **afs_brain_complete**: Complete brain analytics
- **afs_intelligence**: AI intelligence metrics

### Billing & Usage
- **afs_billing**: Billing and payment data
- **afs_metering**: Usage metering and quotas
- **afs_usage**: API usage tracking
- **afs_cost_analysis**: Cost optimization data

### Operations
- **afs_deployments**: Deployment history and metrics
- **agent_logs**: Autonomous agent logs
- **afs_logs**: General application logs
- **autonomous_agent**: Agent-specific data

## Key Services Architecture

### Caching Layer
- Firestore-based request deduplication
- Multi-level caching (system prompt, full request)
- BigQuery analytics for cache optimization
- BQML models for savings prediction

### Multi-Model Routing
- Claude (Anthropic): opus-4, sonnet-4, haiku
- Gemini (Google): 2.0-flash, pro
- GPT (OpenAI): gpt-4, gpt-4-turbo
- Granite (IBM): granite-3.1

### Security & Compliance
- IAM-based authentication
- Private Cloud Run services
- VPC connector integration
- HIPAA-compliant healthcare services

## Common Patterns

### Service Categories
1. **ML/AI Services** (~15 services) - 4GB+ RAM, 2-4 CPU
2. **Gateway Services** (~10 services) - 2GB RAM, 2 CPU
3. **Business Apps** (~20 services) - 512MB-2GB RAM
4. **Infrastructure** (~10 services) - Variable resources

### Monitoring Strategy
- Cloud Logging for all services
- BigQuery sinks for analytics
- Custom metrics via Cloud Monitoring
- Automated alerting via Pub/Sub

### Cost Optimization
- Min instances = 0 for most services
- Auto-scaling based on load
- Request deduplication via caching
- BQML models for cost prediction
