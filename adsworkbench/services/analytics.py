from __future__ import annotations

from collections.abc import Iterable

from adsworkbench.models import MetricDaily


def metric_totals(metrics: Iterable[MetricDaily]) -> dict:
    rows = list(metrics)
    impressions = sum(row.impressions for row in rows)
    clicks = sum(row.clicks for row in rows)
    cost = sum(row.cost_float for row in rows)
    conversions = sum(row.conversions for row in rows)
    revenue = sum(row.revenue_float for row in rows)
    profit = revenue - cost
    return {
        "impressions": impressions,
        "clicks": clicks,
        "cost": cost,
        "conversions": conversions,
        "revenue": revenue,
        "profit": profit,
        "roi": profit / cost if cost else 0,
        "cpc": cost / clicks if clicks else 0,
        "rpv": revenue / clicks if clicks else 0,
        "ctr": clicks / impressions if impressions else 0,
        "cvr": conversions / clicks if clicks else 0,
    }


def recommended_actions(metric: MetricDaily) -> list[dict]:
    actions: list[dict] = []
    if metric.clicks >= 30 and metric.revenue_float == 0 and metric.cost_float > 0:
        actions.append(
            {
                "severity": "high",
                "action_type": "pause_check",
                "message": (
                    f"{metric.day} has {metric.clicks} clicks and no revenue. "
                    "Pause or isolate the source, then check search terms, negative keywords, "
                    "landing relevance, and tracking."
                ),
            }
        )
    if metric.cost_float >= 20 and metric.roi < -0.25:
        actions.append(
            {
                "severity": "high",
                "action_type": "stop_loss",
                "message": (
                    f"ROI is {metric.roi:.1%}. Apply stop-loss, reduce budget, "
                    "or split traffic by geo/device before more spend."
                ),
            }
        )
    if metric.cost_float >= 30 and metric.roi > 0.3 and metric.clicks >= 80:
        actions.append(
            {
                "severity": "medium",
                "action_type": "scale_candidate",
                "message": (
                    f"ROI is {metric.roi:.1%} with {metric.clicks} clicks. "
                    "Consider controlled budget ramp and fresh creatives."
                ),
            }
        )
    if metric.ctr > 0.08 and metric.rpv < metric.cpc and metric.clicks >= 60:
        actions.append(
            {
                "severity": "medium",
                "action_type": "creative_mismatch",
                "message": (
                    "CTR is high but revenue per visitor is below CPC. "
                    "Check search terms, query intent, and whether the ad promise is too broad "
                    "or clickbait-like."
                ),
            }
        )
    if metric.ctr > 0.2 and metric.clicks >= 50 and metric.revenue_float == 0:
        actions.append(
            {
                "severity": "high",
                "action_type": "invalid_traffic_review",
                "message": (
                    "CTR is unusually high with no revenue. Do not add clicks or simulated visits; "
                    "isolate the source and review placement, geo/device, tracking, and settlement data."
                ),
            }
        )
    if metric.clicks >= 100 and metric.conversions == 0 and metric.cost_float > 0:
        actions.append(
            {
                "severity": "medium",
                "action_type": "source_quality_review",
                "message": (
                    "Clicks are accumulating without conversions. Check source intent, landing relevance, "
                    "search terms, negative keyword gaps, click_id/postback continuity, and invalid "
                    "traffic indicators before more spend."
                ),
            }
        )
    if not actions:
        actions.append(
            {
                "severity": "info",
                "action_type": "monitor",
                "message": "No urgent action. Keep collecting source-level data and watch RPV stability.",
            }
        )
    return actions
