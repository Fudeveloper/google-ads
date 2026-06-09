from __future__ import annotations


SOURCE_QUALITY_POINTS = {
    "unstable": 0,
    "watch": 3,
    "stable": 10,
}

POLICY_RISK_POINTS = {
    "high": 0,
    "medium": 4,
    "low": 10,
}

INCIDENT_STATE_POINTS = {
    "active": 0,
    "recent": 3,
    "clean": 10,
}

BUCKET_POINTS = {
    "quarantine": 0,
    "explore": 4,
    "test": 6,
    "scale": 8,
    "core": 10,
}


def calculate_portfolio_allocation(
    *,
    portfolio_bucket: str,
    monthly_media_budget: float,
    proposed_allocation: float,
    spend_to_date: float,
    reported_revenue: float,
    pending_revenue: float,
    approved_revenue: float,
    finalized_revenue: float,
    paid_revenue: float,
    deducted_revenue: float,
    single_offer_exposure_percent: float,
    single_source_exposure_percent: float,
    single_account_exposure_percent: float,
    single_partner_exposure_percent: float,
    cash_reserve_days: int,
    source_quality: str,
    policy_risk: str,
    incident_state: str,
) -> dict[str, object]:
    allocation_percent = _share(proposed_allocation, monthly_media_budget) * 100
    mature_revenue = max(approved_revenue + finalized_revenue + paid_revenue, 0)
    revenue_base = max(
        reported_revenue + pending_revenue + approved_revenue + finalized_revenue + paid_revenue,
        0,
    )
    revenue_quality_ratio = _share(mature_revenue, revenue_base)
    max_exposure = max(
        single_offer_exposure_percent,
        single_source_exposure_percent,
        single_account_exposure_percent,
        single_partner_exposure_percent,
    )

    blockers = _blockers(
        portfolio_bucket=portfolio_bucket,
        monthly_media_budget=monthly_media_budget,
        proposed_allocation=proposed_allocation,
        spend_to_date=spend_to_date,
        pending_revenue=pending_revenue,
        approved_revenue=approved_revenue,
        finalized_revenue=finalized_revenue,
        paid_revenue=paid_revenue,
        deducted_revenue=deducted_revenue,
        single_offer_exposure_percent=single_offer_exposure_percent,
        single_source_exposure_percent=single_source_exposure_percent,
        single_account_exposure_percent=single_account_exposure_percent,
        single_partner_exposure_percent=single_partner_exposure_percent,
        cash_reserve_days=cash_reserve_days,
        source_quality=source_quality,
        policy_risk=policy_risk,
        incident_state=incident_state,
    )

    score = 0
    score += _allocation_points(allocation_percent, portfolio_bucket)
    score += _budget_headroom_points(monthly_media_budget, proposed_allocation, spend_to_date)
    score += _revenue_quality_points(revenue_quality_ratio, paid_revenue, finalized_revenue)
    score += _deduction_points(deducted_revenue, mature_revenue)
    score += _exposure_points(max_exposure)
    score += _cash_points(cash_reserve_days)
    score += SOURCE_QUALITY_POINTS.get(source_quality, 0)
    score += POLICY_RISK_POINTS.get(policy_risk, 0)
    score += INCIDENT_STATE_POINTS.get(incident_state, 0)
    score += BUCKET_POINTS.get(portfolio_bucket, 0)
    score = min(score, 100)

    return {
        "score": score,
        "risk_level": _risk_level(score, blockers, policy_risk, incident_state),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            portfolio_bucket=portfolio_bucket,
            policy_risk=policy_risk,
            incident_state=incident_state,
            cash_reserve_days=cash_reserve_days,
            max_exposure=max_exposure,
        ),
        "allocation_percent": round(allocation_percent, 2),
        "remaining_monthly_budget": round(
            max(monthly_media_budget - spend_to_date - proposed_allocation, 0), 2
        ),
        "cash_at_risk": round(max(proposed_allocation + pending_revenue - paid_revenue, 0), 2),
        "revenue_quality_ratio": round(revenue_quality_ratio * 100, 2),
        "blockers": blockers,
    }


def _share(value: float, denominator: float) -> float:
    if denominator <= 0:
        return 0
    return value / denominator


def _allocation_points(allocation_percent: float, portfolio_bucket: str) -> int:
    if portfolio_bucket in {"test", "explore"}:
        if allocation_percent <= 5:
            return 10
        if allocation_percent <= 10:
            return 6
        return 0
    if allocation_percent <= 10:
        return 12
    if allocation_percent <= 20:
        return 8
    if allocation_percent <= 30:
        return 4
    return 0


def _budget_headroom_points(
    monthly_media_budget: float,
    proposed_allocation: float,
    spend_to_date: float,
) -> int:
    if monthly_media_budget <= 0:
        return 0
    remaining = monthly_media_budget - spend_to_date - proposed_allocation
    if remaining >= monthly_media_budget * 0.2:
        return 10
    if remaining >= 0:
        return 5
    return 0


def _revenue_quality_points(
    revenue_quality_ratio: float,
    paid_revenue: float,
    finalized_revenue: float,
) -> int:
    if paid_revenue > 0 and revenue_quality_ratio >= 0.5:
        return 15
    if finalized_revenue > 0 and revenue_quality_ratio >= 0.4:
        return 12
    if revenue_quality_ratio >= 0.4:
        return 8
    if revenue_quality_ratio > 0:
        return 4
    return 0


def _deduction_points(deducted_revenue: float, mature_revenue: float) -> int:
    if mature_revenue <= 0:
        return 0
    deduction_ratio = deducted_revenue / mature_revenue
    if deduction_ratio <= 0.05:
        return 8
    if deduction_ratio <= 0.15:
        return 4
    return 0


def _exposure_points(max_exposure: float) -> int:
    if max_exposure <= 20:
        return 15
    if max_exposure <= 35:
        return 10
    if max_exposure <= 50:
        return 4
    return 0


def _cash_points(cash_reserve_days: int) -> int:
    if cash_reserve_days >= 45:
        return 10
    if cash_reserve_days >= 30:
        return 8
    if cash_reserve_days >= 14:
        return 4
    return 0


def _risk_level(
    score: int,
    blockers: list[str],
    policy_risk: str,
    incident_state: str,
) -> str:
    if policy_risk == "high" or incident_state == "active":
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
    portfolio_bucket: str,
    policy_risk: str,
    incident_state: str,
    cash_reserve_days: int,
    max_exposure: float,
) -> str:
    if portfolio_bucket == "quarantine" or policy_risk == "high" or incident_state == "active":
        return "quarantine_or_zero_budget"
    if cash_reserve_days < 14 or max_exposure > 50:
        return "reduce_exposure"
    if blockers:
        return "wait_for_settlement"
    if score >= 85:
        return "approve_manual_allocation"
    if score >= 65:
        return "hold_or_small_test"
    if score >= 45:
        return "reduce_exposure"
    return "quarantine_or_zero_budget"


def _blockers(
    *,
    portfolio_bucket: str,
    monthly_media_budget: float,
    proposed_allocation: float,
    spend_to_date: float,
    pending_revenue: float,
    approved_revenue: float,
    finalized_revenue: float,
    paid_revenue: float,
    deducted_revenue: float,
    single_offer_exposure_percent: float,
    single_source_exposure_percent: float,
    single_account_exposure_percent: float,
    single_partner_exposure_percent: float,
    cash_reserve_days: int,
    source_quality: str,
    policy_risk: str,
    incident_state: str,
) -> list[str]:
    blockers: list[str] = []
    if monthly_media_budget <= 0:
        blockers.append("monthly media budget is missing")
    if proposed_allocation <= 0:
        blockers.append("proposed allocation is missing")
    if monthly_media_budget > 0 and proposed_allocation / monthly_media_budget > 0.2:
        blockers.append("proposed allocation exceeds 20 percent portfolio guardrail")
    if monthly_media_budget > 0 and spend_to_date + proposed_allocation > monthly_media_budget:
        blockers.append("proposed allocation exceeds remaining monthly media budget")
    if portfolio_bucket == "quarantine" and proposed_allocation > 0:
        blockers.append("quarantine bucket cannot receive growth allocation")

    mature_revenue = approved_revenue + finalized_revenue + paid_revenue
    if mature_revenue <= 0:
        blockers.append("no approved/finalized/paid revenue evidence")
    if pending_revenue > max(mature_revenue, 0):
        blockers.append("pending revenue dominates mature revenue")
    if mature_revenue > 0 and deducted_revenue / mature_revenue > 0.15:
        blockers.append("deducted revenue exceeds 15 percent of mature revenue")

    if single_offer_exposure_percent > 25:
        blockers.append("single offer exposure exceeds 25 percent")
    if single_source_exposure_percent > 35:
        blockers.append("single source exposure exceeds 35 percent")
    if single_account_exposure_percent > 30:
        blockers.append("single account exposure exceeds 30 percent")
    if single_partner_exposure_percent > 35:
        blockers.append("single revenue partner exposure exceeds 35 percent")

    if cash_reserve_days < 14:
        blockers.append("cash reserve is below 14 days")
    elif cash_reserve_days < 30:
        blockers.append("cash reserve is below 30 days for scale")
    if source_quality != "stable":
        blockers.append("source quality is not stable")
    if policy_risk == "high":
        blockers.append("high policy risk blocks allocation")
    elif policy_risk == "medium":
        blockers.append("medium policy risk requires tighter cap")
    if incident_state == "active":
        blockers.append("active incident blocks allocation")
    elif incident_state == "recent":
        blockers.append("recent incident requires hold period")
    return blockers
