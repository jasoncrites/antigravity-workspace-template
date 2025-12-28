#!/usr/bin/env python3
"""
Comprehensive Service Audit - Find dormant and unused services

This script:
1. Lists all Cloud Run services
2. Checks request logs for activity
3. Identifies dormant services (no traffic in X days)
4. Calculates potential cost savings
5. Generates audit report
"""

import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.bigquery_tools import query_bigquery
from tools.cloud_run_tools import list_cloud_run_services, get_service_details

def main():
    print("\n🔍 GCP Service Audit Report")
    print("=" * 70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

    # Get all services
    print("📊 Fetching all Cloud Run services...")
    all_services = list_cloud_run_services(limit=500)

    if not all_services or all_services[0].get('error'):
        print(f"❌ Error fetching services: {all_services[0].get('error', 'Unknown')}")
        sys.exit(1)

    total_services = len(all_services)
    print(f"✓ Found {total_services} Cloud Run services\n")

    # Query activity for all services
    print("📈 Analyzing service activity (last 30 days)...")
    activity_query = """
    SELECT
      service_name,
      COUNT(*) as request_count,
      MAX(timestamp) as last_request,
      TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(timestamp), DAY) as days_since_last_request
    FROM `truckerbooks-mvp-prod.gateway_metrics.gateway_request_logs`
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    GROUP BY service_name
    ORDER BY days_since_last_request DESC
    """

    try:
        activity_data = query_bigquery(activity_query)
        activity_map = {item['service_name']: item for item in activity_data if not item.get('error')}
    except:
        print("⚠️  Could not query activity data - some services may not be tracked")
        activity_map = {}

    # Categorize services
    active_services = []  # Traffic in last 7 days
    dormant_services = []  # Traffic 7-30 days ago
    inactive_services = []  # No traffic in 30+ days
    unknown_services = []  # Not tracked in logs

    dormancy_threshold_days = 14

    for svc in all_services:
        svc_name = svc.get('name')

        if svc_name in activity_map:
            days_since = int(activity_map[svc_name].get('days_since_last_request', 999))

            if days_since <= 7:
                active_services.append({
                    "name": svc_name,
                    "url": svc.get('url'),
                    "days_since_last_request": days_since,
                    "request_count": int(activity_map[svc_name].get('request_count', 0))
                })
            elif days_since <= dormancy_threshold_days:
                dormant_services.append({
                    "name": svc_name,
                    "url": svc.get('url'),
                    "days_since_last_request": days_since,
                    "request_count": int(activity_map[svc_name].get('request_count', 0))
                })
            else:
                inactive_services.append({
                    "name": svc_name,
                    "url": svc.get('url'),
                    "days_since_last_request": days_since,
                    "request_count": int(activity_map[svc_name].get('request_count', 0))
                })
        else:
            # Not in activity logs
            unknown_services.append({
                "name": svc_name,
                "url": svc.get('url'),
                "tracked": False
            })

    # Print summary
    print("\n📊 Service Activity Summary")
    print("=" * 70)
    print(f"Total Services:        {total_services}")
    print(f"Active (< 7 days):     {len(active_services)} ({len(active_services)/total_services*100:.1f}%)")
    print(f"Dormant (7-{dormancy_threshold_days} days):    {len(dormant_services)} ({len(dormant_services)/total_services*100:.1f}%)")
    print(f"Inactive (>{dormancy_threshold_days} days):   {len(inactive_services)} ({len(inactive_services)/total_services*100:.1f}%)")
    print(f"Unknown/Untracked:     {len(unknown_services)} ({len(unknown_services)/total_services*100:.1f}%)")
    print("=" * 70 + "\n")

    # Active services
    if active_services:
        print(f"✅ Active Services ({len(active_services)})")
        print("─" * 70)
        for svc in sorted(active_services, key=lambda x: x['request_count'], reverse=True)[:10]:
            print(f"  • {svc['name']}")
            print(f"    Requests: {svc['request_count']:,} | Last: {svc['days_since_last_request']} days ago")
        if len(active_services) > 10:
            print(f"  ... and {len(active_services) - 10} more")
        print()

    # Dormant services
    if dormant_services:
        print(f"⚠️  Dormant Services ({len(dormant_services)}) - Review for potential removal")
        print("─" * 70)
        for svc in sorted(dormant_services, key=lambda x: x['days_since_last_request'], reverse=True):
            print(f"  • {svc['name']}")
            print(f"    Last activity: {svc['days_since_last_request']} days ago | Requests: {svc['request_count']:,}")
        print()

    # Inactive services
    if inactive_services:
        print(f"🔴 Inactive Services ({len(inactive_services)}) - Strong candidates for removal")
        print("─" * 70)
        for svc in sorted(inactive_services, key=lambda x: x['days_since_last_request'], reverse=True)[:20]:
            print(f"  • {svc['name']}")
            print(f"    Last activity: {svc['days_since_last_request']}+ days ago | Requests: {svc['request_count']:,}")
        if len(inactive_services) > 20:
            print(f"  ... and {len(inactive_services) - 20} more")
        print()

    # Unknown services
    if unknown_services:
        print(f"❓ Untracked Services ({len(unknown_services)}) - Not in activity logs")
        print("─" * 70)
        for svc in unknown_services[:15]:
            print(f"  • {svc['name']}")
        if len(unknown_services) > 15:
            print(f"  ... and {len(unknown_services) - 15} more")
        print()

    # Recommendations
    print("\n💡 Recommendations")
    print("=" * 70)

    if dormant_services or inactive_services:
        potential_removals = len(dormant_services) + len(inactive_services)
        print(f"1. Review {potential_removals} dormant/inactive services for removal")
        print(f"   - Dormant: {len(dormant_services)} services with 7-{dormancy_threshold_days} days inactivity")
        print(f"   - Inactive: {len(inactive_services)} services with {dormancy_threshold_days}+ days inactivity")
        print()

    if unknown_services:
        print(f"2. Investigate {len(unknown_services)} untracked services")
        print(f"   - May be internal services without logging")
        print(f"   - May be legacy services no longer used")
        print()

    active_percentage = (len(active_services) / total_services * 100) if total_services > 0 else 0
    if active_percentage < 50:
        print(f"3. ⚠️  Only {active_percentage:.1f}% of services are actively used")
        print(f"   - Consider consolidating similar services")
        print(f"   - Archive or remove unused services")
        print()

    # Cost estimates
    print("\n💰 Estimated Cost Impact")
    print("=" * 70)
    # Assume ~$1-2/month per idle service (min instances, storage, etc.)
    estimated_savings_per_service = 1.5
    potential_savings = (len(dormant_services) + len(inactive_services)) * estimated_savings_per_service

    print(f"Dormant/Inactive services: {len(dormant_services) + len(inactive_services)}")
    print(f"Estimated cost per idle service: ${estimated_savings_per_service:.2f}/month")
    print(f"Potential monthly savings: ${potential_savings:.2f}")
    print(f"Annual savings: ${potential_savings * 12:.2f}")
    print()

    # Action items
    print("\n✅ Next Steps")
    print("=" * 70)
    print("1. Review each dormant service and confirm if still needed")
    print("2. For services to remove:")
    print("   gcloud run services delete SERVICE_NAME --region=us-central1")
    print()
    print("3. For services to keep but reduce costs:")
    print("   gcloud run services update SERVICE_NAME --min-instances=0")
    print()
    print("4. Export list for documentation:")
    print("   python audit_all_services.py > audit_report.txt")
    print()

    print("=" * 70)
    print("✅ Audit Complete!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Audit interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during audit: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
