from __future__ import annotations


DATA_STATUS_POINTS = {
    "fresh": 0,
    "partial": 6,
    "mature": 12,
    "settled": 15,
}

REVENUE_STATUS_POINTS = {
    "estimated": 0,
    "submitted": 0,
    "accepted": 5,
    "approved": 12,
    "finalized": 18,
    "paid": 18,
}

SOURCE_QUALITY_POINTS = {
    "unstable": 0,
    "watch": 2,
    "stable": 5,
}

INCIDENT_STATE_POINTS = {
    "active": 0,
    "recent": 2,
    "clean": 5,
}


def calculate_budget_pacing(
    *,
    current_daily_budget: float,
    proposed_daily_budget: float,
    test_budget: float,
    hard_stop: float,
    spend_to_date: float,
    approved_revenue: float,
    paid_revenue: float,
    safe_cpc: float,
    actual_cpc: float,
    sample_clicks: int,
    data_status: str,
    revenue_status: str,
    source_quality: str,
    incident_state: str,
    cash_buffer_days: int,
    overdelivery_buffer_percent: float,
) -> dict[str, object]:
    increase_ratio = _increase_ratio(current_daily_budget, proposed_daily_budget)
    blockers = _blockers(
        current_daily_budget=current_daily_budget,
        proposed_daily_budget=proposed_daily_budget,
        hard_stop=hard_stop,
        spend_to_date=spend_to_date,
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
        safe_cpc=safe_cpc,
        actual_cpc=actual_cpc,
        sample_clicks=sample_clicks,
        data_status=data_status,
        revenue_status=revenue_status,
        source_quality=source_quality,
        incident_state=incident_state,
        cash_buffer_days=cash_buffer_days,
        overdelivery_buffer_percent=overdelivery_buffer_percent,
    )
    score = 0
    score += _budget_points(increase_ratio)
    score += DATA_STATUS_POINTS.get(data_status, 0)
    score += REVENUE_STATUS_POINTS.get(revenue_status, 0)
    score += _sample_points(sample_clicks)
    score += _cpc_points(actual_cpc, safe_cpc)
    score += _hard_stop_points(spend_to_date, hard_stop)
    score += _revenue_points(approved_revenue, paid_revenue)
    score += _cash_points(cash_buffer_days)
    score += SOURCE_QUALITY_POINTS.get(source_quality, 0)
    score += INCIDENT_STATE_POINTS.get(incident_state, 0)
    score = min(score, 100)

    return {
        "score": score,
        "risk_level": _risk_level(score, blockers),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            current_daily_budget=current_daily_budget,
            proposed_daily_budget=proposed_daily_budget,
            hard_stop=hard_stop,
            spend_to_date=spend_to_date,
            safe_cpc=safe_cpc,
            actual_cpc=actual_cpc,
            cash_buffer_days=cash_buffer_days,
            incident_state=incident_state,
        ),
        "increase_percent": round(increase_ratio * 100, 2),
        "remaining_test_budget": round(max(test_budget - spend_to_date, 0), 2),
        "remaining_hard_stop": round(max(hard_stop - spend_to_date, 0), 2),
        "blockers": blockers,
    }


def _increase_ratio(current_daily_budget: float, proposed_daily_budget: float) -> float:
    if current_daily_budget <= 0:
        return 0 if proposed_daily_budget <= 0 else 1
    return (proposed_daily_budget - current_daily_budget) / current_daily_budget


def _budget_points(increase_ratio: float) -> int:
    if increase_ratio <= 0:
        return 15
    if increase_ratio <= 0.1:
        return 15
    if increase_ratio <= 0.3:
        return 10
    if increase_ratio <= 0.5:
        return 4
    return 0


def _sample_points(sample_clicks: int) -> int:
    if sample_clicks >= 100:
        return 10
    if sample_clicks >= 50:
        return 6
    if sample_clicks >= 20:
        return 3
    return 0


def _cpc_points(actual_cpc: float, safe_cpc: float) -> int:
    if safe_cpc <= 0:
        return 0
    if actual_cpc <= safe_cpc:
        return 15
    if actual_cpc <= safe_cpc * 1.2:
        return 8
    return 0


def _hard_stop_points(spend_to_date: float, hard_stop: float) -> int:
    if hard_stop <= 0:
        return 0
    if spend_to_date < hard_stop * 0.8:
        return 10
    if spend_to_date <= hard_stop:
        return 5
    return 0


def _revenue_points(approved_revenue: float, paid_revenue: float) -> int:
    if paid_revenue > 0:
        return 7
    if approved_revenue > 0:
        return 5
    return 0


def _cash_points(cash_buffer_days: int) -> int:
    if cash_buffer_days >= 30:
        return 10
    if cash_buffer_days >= 14:
        return 5
    return 0


def _risk_level(score: int, blockers: list[str]) -> str:
    if any("hard stop" in item or "active incident" in item for item in blockers):
        return "high"
    if score >= 80 and not blockers:
        return "low"
    if score >= 60:
        return "medium"
    return "high"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    current_daily_budget: float,
    proposed_daily_budget: float,
    hard_stop: float,
    spend_to_date: float,
    safe_cpc: float,
    actual_cpc: float,
    cash_buffer_days: int,
    incident_state: str,
) -> str:
    if proposed_daily_budget < current_daily_budget:
        return "reduce_or_pause"
    if hard_stop > 0 and spend_to_date >= hard_stop:
        return "stop_or_reduce"
    if safe_cpc > 0 and actual_cpc > safe_cpc * 1.2:
        return "stop_or_reduce"
    if cash_buffer_days < 14 or incident_state == "active":
        return "block_scale"
    if score >= 80 and not blockers:
        return "approve_manual_ramp"
    if score >= 60:
        return "hold_or_small_test"
    return "wait_or_block_scale"


def _blockers(
    *,
    current_daily_budget: float,
    proposed_daily_budget: float,
    hard_stop: float,
    spend_to_date: float,
    approved_revenue: float,
    paid_revenue: float,
    safe_cpc: float,
    actual_cpc: float,
    sample_clicks: int,
    data_status: str,
    revenue_status: str,
    source_quality: str,
    incident_state: str,
    cash_buffer_days: int,
    overdelivery_buffer_percent: float,
) -> list[str]:
    blockers: list[str] = []
    increase_ratio = _increase_ratio(current_daily_budget, proposed_daily_budget)
    if proposed_daily_budget > current_daily_budget and increase_ratio > 0.3:
        blockers.append("proposed budget increase exceeds 30 percent ramp guardrail")
    if data_status in {"fresh", "partial"}:
        blockers.append("data freshness is not mature enough for scale")
    if revenue_status in {"estimated", "submitted", "accepted"}:
        blockers.append("revenue is not approved/finalized/paid")
    if hard_stop > 0 and spend_to_date >= hard_stop:
        blockers.append("hard stop has been reached")
    if safe_cpc <= 0:
        blockers.append("safe CPC is missing")
    elif actual_cpc > safe_cpc * 1.2:
        blockers.append("actual CPC exceeds safe CPC by more than 20 percent")
    if sample_clicks < 50:
        blockers.append("sample size is weak")
    if approved_revenue <= 0 and paid_revenue <= 0:
        blockers.append("no approved or paid revenue evidence")
    if source_quality != "stable":
        blockers.append("source quality is not stable")
    if incident_state == "active":
        blockers.append("active incident blocks budget increase")
    elif incident_state == "recent":
        blockers.append("recent incident requires hold period")
    if cash_buffer_days < 14:
        blockers.append("cash buffer is below 14 days")
    overdelivery_exposure = proposed_daily_budget * (1 + overdelivery_buffer_percent / 100)
    if (
        proposed_daily_budget > current_daily_budget
        and hard_stop > 0
        and spend_to_date + overdelivery_exposure > hard_stop
    ):
        blockers.append("overdelivery exposure can exceed remaining hard stop")
    return blockers
