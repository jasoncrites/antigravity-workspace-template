#!/usr/bin/env python3
"""
Direct cost analysis script using our custom GCP tools.
Bypasses the agent for immediate results.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.bigquery_tools import (
    query_bigquery,
    analyze_cache_performance,
    get_top_models_usage,
    find_expensive_queries
)
from tools.cloud_run_tools import (
    list_cloud_run_services,
    analyze_service_costs,
    find_dormant_services
)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def main():
    print("\n🚀 GCP Infrastructure Cost Analysis")
    print("=" * 70)

    # 1. Cloud Run Services Overview
    print_section("📊 Cloud Run Services Overview")
    services = list_cloud_run_services(limit=10)
    if services and not services[0].get('error'):
        print(f"Total services found: {len(services)}")
        print("\nFirst 10 services:")
        for svc in services[:10]:
            status = "✅" if svc.get('ready') else "❌"
            print(f"  {status} {svc.get('name')} - {svc.get('url', 'N/A')}")
    else:
        print(f"❌ Error: {services[0].get('error', 'Unknown error')}")

    # 2. Service Costs Analysis
    print_section("💰 Service Costs (Last 7 Days)")
    costs = analyze_service_costs(days=7)
    if costs and not costs[0].get('error'):
        print(f"Found {len(costs)} services with cost data:\n")
        for i, svc in enumerate(costs[:10], 1):
            name = svc.get('service_name', 'Unknown')
            cost = float(svc.get('total_cost', 0))
            requests = int(svc.get('request_count', 0))
            latency = float(svc.get('avg_latency', 0))
            print(f"{i:2}. {name}")
            print(f"    Cost: ${cost:.2f} | Requests: {requests:,} | Avg Latency: {latency:.0f}ms")
    else:
        print("⚠️  No cost data available (table may not exist yet)")

    # 3. Dormant Services
    print_section("💤 Dormant Services (No Traffic in 7 Days)")
    dormant = find_dormant_services(min_days_inactive=7)
    if dormant:
        print(f"Found {len(dormant)} dormant services:\n")
        for svc in dormant[:15]:
            print(f"  • {svc}")
        if len(dormant) > 15:
            print(f"\n  ... and {len(dormant) - 15} more")
    else:
        print("✅ No dormant services found or no tracking data available")

    # 4. Cache Performance
    print_section("🔄 Cache Performance")
    cache_perf = analyze_cache_performance(days=7)
    if cache_perf and not cache_perf.get('error'):
        total = int(cache_perf.get('total_requests', 0))
        hits = int(cache_perf.get('cache_hits', 0))
        rate = float(cache_perf.get('hit_rate', 0))
        savings = float(cache_perf.get('total_savings_usd', 0))
        cache_lat = float(cache_perf.get('avg_cache_latency', 0))
        miss_lat = float(cache_perf.get('avg_miss_latency', 0))

        print(f"Total Requests:     {total:,}")
        print(f"Cache Hits:         {hits:,}")
        print(f"Hit Rate:           {rate:.1f}%")
        print(f"Total Savings:      ${savings:.2f}")
        print(f"Avg Cache Latency:  {cache_lat:.0f}ms")
        print(f"Avg Miss Latency:   {miss_lat:.0f}ms")

        if cache_lat > 0 and miss_lat > 0:
            speedup = miss_lat / cache_lat
            print(f"Speedup Factor:     {speedup:.1f}x faster with cache")
    else:
        print("⚠️  Cache data not available")

    # 5. Top AI Models Usage
    print_section("🤖 Top AI Models Usage (Last 30 Days)")
    models = get_top_models_usage(days=30, limit=10)
    if models and not models[0].get('error'):
        print(f"Found {len(models)} models:\n")
        for i, model in enumerate(models, 1):
            name = model.get('model', 'Unknown')
            cost = float(model.get('total_cost_usd', 0))
            requests = int(model.get('request_count', 0))
            in_tokens = int(model.get('total_input_tokens', 0))
            out_tokens = int(model.get('total_output_tokens', 0))
            latency = float(model.get('avg_latency_ms', 0))

            print(f"{i:2}. {name}")
            print(f"    Cost: ${cost:.2f} | Requests: {requests:,}")
            print(f"    Tokens: {in_tokens:,} in / {out_tokens:,} out | Latency: {latency:.0f}ms")
    else:
        print("⚠️  Model usage data not available")

    # 6. Expensive Queries
    print_section("💸 Most Expensive Queries (Last 7 Days)")
    expensive = find_expensive_queries(days=7, min_cost=1.0)
    if expensive and not expensive[0].get('error'):
        if len(expensive) > 0:
            print(f"Found {len(expensive)} expensive queries (>$1.00):\n")
            for i, query in enumerate(expensive[:5], 1):
                model = query.get('model', 'Unknown')
                cost = float(query.get('cost_usd', 0))
                in_tok = int(query.get('input_tokens', 0))
                out_tok = int(query.get('output_tokens', 0))
                latency = float(query.get('latency_ms', 0))

                print(f"{i}. Model: {model} | Cost: ${cost:.2f}")
                print(f"   Tokens: {in_tok:,} in / {out_tok:,} out | {latency:.0f}ms")
        else:
            print("✅ No expensive queries found (all < $1.00)")
    else:
        print("⚠️  Expensive query data not available")

    # 7. Summary and Recommendations
    print_section("📋 Summary & Recommendations")

    recommendations = []

    if dormant and len(dormant) > 0:
        recommendations.append(
            f"🔸 Review {len(dormant)} dormant services for potential decommissioning"
        )

    if cache_perf and not cache_perf.get('error'):
        hit_rate = float(cache_perf.get('hit_rate', 0))
        if hit_rate < 50:
            recommendations.append(
                f"🔸 Cache hit rate is {hit_rate:.1f}% - consider optimizing cache keys"
            )
        else:
            recommendations.append(
                f"✅ Cache performance is good ({hit_rate:.1f}% hit rate)"
            )

    if costs and not costs[0].get('error') and len(costs) > 0:
        top_cost = float(costs[0].get('total_cost', 0))
        recommendations.append(
            f"🔸 Top service cost: ${top_cost:.2f} - review for optimization opportunities"
        )

    if recommendations:
        for rec in recommendations:
            print(f"  {rec}")
    else:
        print("  ℹ️  Insufficient data for recommendations")

    print("\n" + "=" * 70)
    print("✅ Analysis Complete!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
