"""
BigQuery analysis tools for GCP infrastructure.
These tools are auto-discovered by the agent.
"""

import subprocess
import json
from typing import Dict, List, Optional


def query_bigquery(query: str, project: str = "truckerbooks-mvp-prod") -> List[Dict]:
    """
    Executes a BigQuery SQL query and returns results.

    Args:
        query: SQL query to execute (standard SQL)
        project: GCP project ID (default: truckerbooks-mvp-prod)

    Returns:
        List of result rows as dictionaries
    """
    try:
        cmd = [
            "bq", "query",
            "--use_legacy_sql=false",
            "--format=json",
            f"--project_id={project}",
            query
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        return [{"error": f"Query failed: {e.stderr}"}]
    except json.JSONDecodeError:
        return [{"error": "Failed to parse query results"}]


def list_datasets(project: str = "truckerbooks-mvp-prod") -> List[str]:
    """
    Lists all BigQuery datasets in the project.

    Args:
        project: GCP project ID (default: truckerbooks-mvp-prod)

    Returns:
        List of dataset names
    """
    try:
        cmd = ["bq", "ls", f"--project_id={project}", "--format=json"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        datasets = json.loads(result.stdout)

        return [ds.get("datasetReference", {}).get("datasetId") for ds in datasets]

    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []


def get_table_schema(dataset: str, table: str, project: str = "truckerbooks-mvp-prod") -> Dict:
    """
    Gets the schema of a BigQuery table.

    Args:
        dataset: Dataset name
        table: Table name
        project: GCP project ID (default: truckerbooks-mvp-prod)

    Returns:
        Dictionary with table schema and metadata
    """
    try:
        cmd = [
            "bq", "show",
            "--format=json",
            f"{project}:{dataset}.{table}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        table_info = json.loads(result.stdout)

        return {
            "dataset": dataset,
            "table": table,
            "schema": table_info.get("schema", {}).get("fields", []),
            "num_rows": table_info.get("numRows"),
            "size_bytes": table_info.get("numBytes")
        }

    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to get schema: {e.stderr}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse schema"}


def analyze_cache_performance(days: int = 7) -> Dict:
    """
    Analyzes cache hit rates and savings.

    Args:
        days: Number of days to analyze (default: 7)

    Returns:
        Dictionary with cache performance metrics
    """
    query = f"""
    SELECT
      COUNT(*) as total_requests,
      SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END) as cache_hits,
      ROUND(SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as hit_rate,
      SUM(savings) as total_savings_usd,
      AVG(CASE WHEN cache_hit THEN latency_ms ELSE NULL END) as avg_cache_latency,
      AVG(CASE WHEN NOT cache_hit THEN latency_ms ELSE NULL END) as avg_miss_latency
    FROM `truckerbooks-mvp-prod.cache_analytics.cache_metrics`
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
    """

    results = query_bigquery(query)
    return results[0] if results and not results[0].get("error") else {"error": "No data available"}


def get_top_models_usage(days: int = 30, limit: int = 10) -> List[Dict]:
    """
    Gets the most used AI models and their costs.

    Args:
        days: Number of days to analyze (default: 30)
        limit: Number of top models to return (default: 10)

    Returns:
        List of models with usage statistics
    """
    query = f"""
    SELECT
      model,
      COUNT(*) as request_count,
      SUM(input_tokens) as total_input_tokens,
      SUM(output_tokens) as total_output_tokens,
      ROUND(SUM(cost), 2) as total_cost_usd,
      ROUND(AVG(latency_ms), 0) as avg_latency_ms
    FROM `truckerbooks-mvp-prod.gateway_metrics.request_logs`
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
      AND model IS NOT NULL
    GROUP BY model
    ORDER BY total_cost_usd DESC
    LIMIT {limit}
    """

    return query_bigquery(query)


def find_expensive_queries(days: int = 7, min_cost: float = 1.0) -> List[Dict]:
    """
    Finds expensive AI model requests.

    Args:
        days: Number of days to analyze (default: 7)
        min_cost: Minimum cost threshold in USD (default: 1.0)

    Returns:
        List of expensive queries with details
    """
    query = f"""
    SELECT
      request_hash,
      model,
      input_tokens,
      output_tokens,
      cost as cost_usd,
      latency_ms,
      timestamp
    FROM `truckerbooks-mvp-prod.gateway_metrics.request_logs`
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
      AND cost >= {min_cost}
    ORDER BY cost DESC
    LIMIT 20
    """

    return query_bigquery(query)


def analyze_workflow_efficiency() -> Dict:
    """
    Analyzes workflow execution efficiency and success rates.

    Returns:
        Dictionary with workflow performance metrics
    """
    query = """
    SELECT
      COUNT(*) as total_executions,
      SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful,
      ROUND(SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate,
      ROUND(AVG(duration_ms), 0) as avg_duration_ms,
      ROUND(AVG(total_cost), 4) as avg_cost_usd
    FROM `truckerbooks-mvp-prod.workflow_analytics.workflow_training_data`
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    """

    results = query_bigquery(query)
    return results[0] if results and not results[0].get("error") else {"error": "No data available"}
