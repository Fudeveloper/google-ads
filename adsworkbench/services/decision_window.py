from __future__ import annotations


DATA_STATUS_POINTS = {
    "fresh": 4,
    "partial": 10,
    "mature": 15,
    "settled": 15,
}

REVENUE_STATUS_POINTS = {
    "estimated": 4,
    "submitted": 6,
    "accepted": 10,
    "approved": 15,
    "finalized": 20,
    "paid": 20,
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


def calculate_decision_window(
    *,
    data_status: str,
    revenue_status: str,
    conversion_lag_days: int,
    approval_lag_days: int,
    settlement_lag_days: int,
    sample_clicks: int,
    approved_revenue: float,
    paid_revenue: float,
    source_quality: str,
    incident_state: str,
) -> dict[str, object]:
    score = 0
    score += DATA_STATUS_POINTS.get(data_status, 0)
    score += _lag_points(conversion_lag_days, [(7, 20), (3, 12), (1, 6)])
    score += _lag_points(approval_lag_days, [(7, 20), (3, 12), (1, 6)])
    score += REVENUE_STATUS_POINTS.get(revenue_status, 0)
    score += _sample_points(sample_clicks, approved_revenue, paid_revenue)
    score += SOURCE_QUALITY_POINTS.get(source_quality, 0)
    score += INCIDENT_STATE_POINTS.get(incident_state, 0)

    score = min(score, 100)
    return {
        "score": score,
        "maturity": _maturity(score),
        "recommended_action": _recommended_action(score),
        "blockers": _blockers(
            data_status=data_status,
            revenue_status=revenue_status,
            conversion_lag_days=conversion_lag_days,
            approval_lag_days=approval_lag_days,
            settlement_lag_days=settlement_lag_days,
            sample_clicks=sample_clicks,
            approved_revenue=approved_revenue,
            paid_revenue=paid_revenue,
            source_quality=source_quality,
            incident_state=incident_state,
        ),
    }


def _lag_points(value: int, tiers: list[tuple[int, int]]) -> int:
    for threshold, points in tiers:
        if value >= threshold:
            return points
    return 0


def _sample_points(sample_clicks: int, approved_revenue: float, paid_revenue: float) -> int:
    if sample_clicks >= 100 and (paid_revenue > 0 or approved_revenue > 0):
        return 10
    if sample_clicks >= 50:
        return 6
    if sample_clicks >= 20:
        return 3
    return 0


def _maturity(score: int) -> str:
    if score >= 85:
        return "settled"
    if score >= 70:
        return "mostly_mature"
    if score >= 55:
        return "partial"
    if score >= 35:
        return "early"
    return "unsafe"


def _recommended_action(score: int) -> str:
    if score >= 85:
        return "scale_review"
    if score >= 70:
        return "small_ramp"
    if score >= 55:
        return "diagnose_only"
    if score >= 35:
        return "wait_loss"
    return "stop_or_freeze"


def _blockers(
    *,
    data_status: str,
    revenue_status: str,
    conversion_lag_days: int,
    approval_lag_days: int,
    settlement_lag_days: int,
    sample_clicks: int,
    approved_revenue: float,
    paid_revenue: float,
    source_quality: str,
    incident_state: str,
) -> list[str]:
    blockers: list[str] = []
    if data_status in {"fresh", "partial"}:
        blockers.append("data freshness is not mature enough for scale")
    if revenue_status in {"estimated", "submitted", "accepted"}:
        blockers.append("revenue is not approved/finalized/paid")
    if conversion_lag_days < 3:
        blockers.append("conversion lag window is too short")
    if approval_lag_days < 3:
        blockers.append("buyer/network approval lag is not covered")
    if settlement_lag_days < 7 and revenue_status not in {"paid", "finalized"}:
        blockers.append("settlement window is not covered")
    if sample_clicks < 50:
        blockers.append("sample size is weak")
    if approved_revenue <= 0 and paid_revenue <= 0:
        blockers.append("no approved or paid revenue evidence")
    if source_quality != "stable":
        blockers.append("source quality is not stable")
    if incident_state != "clean":
        blockers.append("recent or active incident blocks scale")
    return blockers
