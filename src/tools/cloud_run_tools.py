"""
Cloud Run management tools for GCP infrastructure.
These tools are auto-discovered by the agent.
"""

import subprocess
import json
from typing import Dict, List, Optional


def list_cloud_run_services(region: str = "us-central1", limit: int = 50) -> List[Dict]:
    """
    Lists Cloud Run services in the specified region.

    Args:
        region: GCP region (default: us-central1)
        limit: Maximum number of services to return (default: 50)

    Returns:
        List of service dictionaries with name, URL, and status
    """
    try:
        cmd = [
            "gcloud", "run", "services", "list",
            f"--region={region}",
            "--format=json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        services = json.loads(result.stdout)

        return [{
            "name": svc.get("metadata", {}).get("name"),
            "url": svc.get("status", {}).get("url"),
            "region": region,
            "ready": svc.get("status", {}).get("conditions", [{}])[0].get("status") == "True"
        } for svc in services[:limit]]

    except subprocess.CalledProcessError as e:
        return [{"error": f"Failed to list services: {e.stderr}"}]
    except json.JSONDecodeError:
        return [{"error": "Failed to parse service list"}]


def get_service_details(service_name: str, region: str = "us-central1") -> Dict:
    """
    Gets detailed information about a Cloud Run service.

    Args:
        service_name: Name of the Cloud Run service
        region: GCP region (default: us-central1)

    Returns:
        Dictionary with service configuration and status
    """
    try:
        cmd = [
            "gcloud", "run", "services", "describe", service_name,
            f"--region={region}",
            "--format=json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        service = json.loads(result.stdout)

        spec = service.get("spec", {}).get("template", {}).get("spec", {})
        containers = spec.get("containers", [{}])[0]
        resources = containers.get("resources", {}).get("limits", {})

        return {
            "name": service_name,
            "url": service.get("status", {}).get("url"),
            "memory": resources.get("memory", "unknown"),
            "cpu": resources.get("cpu", "unknown"),
            "image": containers.get("image", "unknown"),
            "env_vars": {e["name"]: e.get("value", "SECRET") for e in containers.get("env", [])},
            "status": service.get("status", {}).get("conditions", [{}])[0].get("status")
        }

    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to get service details: {e.stderr}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse service details"}


def check_service_health(service_url: str) -> Dict:
    """
    Checks the health of a service by calling its /health endpoint.

    Args:
        service_url: Full URL of the Cloud Run service

    Returns:
        Dictionary with health status and response
    """
    try:
        import requests
        response = requests.get(f"{service_url}/health", timeout=10)

        return {
            "url": service_url,
            "status_code": response.status_code,
            "healthy": response.status_code == 200,
            "response": response.text[:500]  # Limit response size
        }

    except requests.exceptions.RequestException as e:
        return {
            "url": service_url,
            "healthy": False,
            "error": str(e)
        }


def analyze_service_costs(days: int = 7) -> List[Dict]:
    """
    Analyzes Cloud Run service costs using BigQuery.

    Args:
        days: Number of days to analyze (default: 7)

    Returns:
        List of services with cost information
    """
    try:
        query = f"""
        SELECT
          service_name,
          SUM(cost) as total_cost,
          COUNT(*) as request_count,
          AVG(latency_ms) as avg_latency
        FROM `truckerbooks-mvp-prod.gateway_metrics.request_logs`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        GROUP BY service_name
        ORDER BY total_cost DESC
        LIMIT 20
        """

        cmd = ["bq", "query", "--use_legacy_sql=false", "--format=json", query]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        return json.loads(result.stdout)

    except subprocess.CalledProcessError:
        return [{"error": "Failed to query cost data"}]
    except json.JSONDecodeError:
        return [{"error": "Failed to parse cost data"}]


def find_dormant_services(min_days_inactive: int = 7) -> List[str]:
    """
    Finds Cloud Run services with no recent traffic.

    Args:
        min_days_inactive: Minimum days without traffic (default: 7)

    Returns:
        List of potentially dormant service names
    """
    try:
        query = f"""
        SELECT DISTINCT service_name
        FROM `truckerbooks-mvp-prod.gateway_metrics.request_logs`
        WHERE service_name NOT IN (
          SELECT DISTINCT service_name
          FROM `truckerbooks-mvp-prod.gateway_metrics.request_logs`
          WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {min_days_inactive} DAY)
        )
        LIMIT 50
        """

        cmd = ["bq", "query", "--use_legacy_sql=false", "--format=json", query]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        services = json.loads(result.stdout)

        return [svc["service_name"] for svc in services]

    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        return []
