from __future__ import annotations

import math


def calculate_opportunity(
    *,
    revenue_model: str,
    session_rpm: float,
    payout: float,
    cvr_percent: float,
    cpc: float,
    safety_factor: float,
    target_clicks: int,
    policy_score: int,
    content_score: int,
    tracking_score: int,
    source_score: int,
    cash_buffer_days: int,
) -> dict:
    model = revenue_model.lower()
    cvr = max(cvr_percent, 0) / 100
    if "rpm" in model or "display" in model:
        rpv = max(session_rpm, 0) / 1000
        revenue_basis = "Session RPM"
        min_sample_clicks = max(100, target_clicks)
    else:
        rpv = max(payout, 0) * cvr
        revenue_basis = "Payout * CVR"
        min_sample_clicks = max(100, math.ceil(3 / cvr)) if cvr > 0 else 100

    break_even_cpc = rpv
    safe_cpc = break_even_cpc * max(min(safety_factor, 1), 0)
    expected_revenue = target_clicks * rpv
    expected_cost = target_clicks * max(cpc, 0)
    expected_profit = expected_revenue - expected_cost
    roi = expected_profit / expected_cost if expected_cost else 0
    test_budget = min_sample_clicks * max(cpc, 0)
    hard_stop = test_budget * 1.2
    safety_margin = (safe_cpc - cpc) / safe_cpc if safe_cpc > 0 else 0

    economics_score = _economics_score(cpc, break_even_cpc, safe_cpc)
    quality_score = _avg_score(policy_score, content_score, tracking_score, source_score)
    cash_score = _clamp((cash_buffer_days / 30) * 100)
    opportunity_score = round(
        economics_score * 0.45 + quality_score * 0.40 + cash_score * 0.15
    )

    warnings = []
    if break_even_cpc <= 0:
        warnings.append("Revenue basis is zero; fill RPM or payout/CVR before testing.")
    if cpc > safe_cpc and break_even_cpc > 0:
        warnings.append("CPC is above safe CPC; do not scale before improving traffic cost or revenue.")
    if policy_score < 60:
        warnings.append("Policy score is weak; review ad promise, page claims, and platform restrictions.")
    if content_score < 60:
        warnings.append("Content score is weak; improve originality, usefulness, and transparency.")
    if tracking_score < 60:
        warnings.append("Tracking score is weak; fix UTM/SubID/postback before buying traffic.")
    if source_score < 60:
        warnings.append("Traffic source score is weak; isolate source/geo/device before spending.")
    if cash_buffer_days < 14:
        warnings.append("Cash buffer is short; payment delay or clawback could break the test.")

    recommendation = _recommendation(opportunity_score, cpc, safe_cpc, warnings)

    return {
        "revenue_basis": revenue_basis,
        "rpv": round(rpv, 6),
        "break_even_cpc": round(break_even_cpc, 6),
        "safe_cpc": round(safe_cpc, 6),
        "safety_margin": round(safety_margin, 6),
        "expected_revenue": round(expected_revenue, 4),
        "expected_cost": round(expected_cost, 4),
        "expected_profit": round(expected_profit, 4),
        "roi": round(roi, 6),
        "min_sample_clicks": min_sample_clicks,
        "test_budget": round(test_budget, 4),
        "hard_stop": round(hard_stop, 4),
        "economics_score": round(economics_score),
        "quality_score": round(quality_score),
        "cash_score": round(cash_score),
        "opportunity_score": opportunity_score,
        "recommendation": recommendation,
        "warnings": warnings,
    }


def _economics_score(cpc: float, break_even_cpc: float, safe_cpc: float) -> float:
    if break_even_cpc <= 0:
        return 0
    if cpc <= safe_cpc:
        margin_ratio = (safe_cpc - cpc) / break_even_cpc
        return _clamp(70 + margin_ratio * 80)
    over_ratio = (cpc - safe_cpc) / break_even_cpc
    return _clamp(65 - over_ratio * 100)


def _avg_score(*values: int) -> float:
    cleaned = [_clamp(value) for value in values]
    return sum(cleaned) / len(cleaned)


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def _recommendation(
    opportunity_score: int, cpc: float, safe_cpc: float, warnings: list[str]
) -> str:
    if warnings and any("do not scale" in warning.lower() for warning in warnings):
        return "hold"
    if opportunity_score >= 80 and cpc <= safe_cpc:
        return "test"
    if opportunity_score >= 65:
        return "small_test"
    if opportunity_score >= 50:
        return "review"
    return "reject"
