from __future__ import annotations


OFFER_STATUS_POINTS = {
    "researching": 2,
    "pending_approval": 4,
    "approved_for_test": 10,
    "active": 15,
    "near_cap": 6,
    "capped": 0,
    "paused_by_network": 0,
    "expired": 0,
    "quality_hold": 0,
    "retired": 0,
}

BUYER_CAPACITY_POINTS = {
    "unknown": 0,
    "paused": 0,
    "quality_hold": 0,
    "near_cap": 3,
    "limited": 6,
    "open": 10,
}

REPLACEMENT_STATUS_POINTS = {
    "not_needed": 8,
    "draft": 0,
    "needs_review": 2,
    "preapproved": 8,
    "rejected": 0,
}

SOURCE_QUALITY_POINTS = {
    "unstable": 0,
    "watch": 3,
    "stable": 8,
}

POLICY_RISK_POINTS = {
    "high": 0,
    "medium": 4,
    "low": 8,
}


def calculate_offer_cap_review(
    *,
    offer_status: str,
    cap_limit: float,
    cap_used: float,
    expected_next_conversions: float,
    current_payout: float,
    new_payout: float,
    approval_rate_percent: float,
    paid_rate_percent: float,
    deduction_rate_percent: float,
    days_since_cap_update: int,
    buyer_capacity_status: str,
    replacement_status: str,
    replacement_fit_score: int,
    same_intent_review: bool,
    source_quality: str,
    policy_risk: str,
) -> dict[str, object]:
    payout_for_model = new_payout if new_payout > 0 else current_payout
    approval_rate = _rate(approval_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    deduction_rate = _rate(deduction_rate_percent)
    cap_remaining = max(cap_limit - cap_used, 0)
    cap_usage_percent = _percent(cap_used, cap_limit)
    effective_payout = payout_for_model * approval_rate * paid_rate * (1 - deduction_rate)
    safe_daily_media_cost = max(cap_remaining - expected_next_conversions, 0) * effective_payout * 0.6

    blockers = _blockers(
        offer_status=offer_status,
        cap_limit=cap_limit,
        cap_used=cap_used,
        cap_remaining=cap_remaining,
        expected_next_conversions=expected_next_conversions,
        current_payout=current_payout,
        new_payout=new_payout,
        approval_rate_percent=approval_rate_percent,
        paid_rate_percent=paid_rate_percent,
        deduction_rate_percent=deduction_rate_percent,
        days_since_cap_update=days_since_cap_update,
        buyer_capacity_status=buyer_capacity_status,
        replacement_status=replacement_status,
        replacement_fit_score=replacement_fit_score,
        same_intent_review=same_intent_review,
        source_quality=source_quality,
        policy_risk=policy_risk,
    )

    score = 0
    score += OFFER_STATUS_POINTS.get(offer_status, 0)
    score += _cap_points(cap_usage_percent, cap_limit)
    score += _payout_points(current_payout, new_payout, effective_payout)
    score += _quality_points(approval_rate_percent, paid_rate_percent, deduction_rate_percent)
    score += _freshness_points(days_since_cap_update)
    score += BUYER_CAPACITY_POINTS.get(buyer_capacity_status, 0)
    score += REPLACEMENT_STATUS_POINTS.get(replacement_status, 0)
    score += _replacement_fit_points(replacement_status, replacement_fit_score, same_intent_review)
    score += SOURCE_QUALITY_POINTS.get(source_quality, 0)
    score += POLICY_RISK_POINTS.get(policy_risk, 0)
    score = min(score, 100)

    return {
        "score": score,
        "risk_level": _risk_level(score, blockers, offer_status, policy_risk),
        "recommended_action": _recommended_action(
            offer_status=offer_status,
            cap_usage_percent=cap_usage_percent,
            cap_remaining=cap_remaining,
            expected_next_conversions=expected_next_conversions,
            buyer_capacity_status=buyer_capacity_status,
            replacement_status=replacement_status,
            replacement_fit_score=replacement_fit_score,
            same_intent_review=same_intent_review,
            score=score,
            blockers=blockers,
        ),
        "cap_usage_percent": round(cap_usage_percent, 2),
        "cap_remaining": round(cap_remaining, 2),
        "effective_payout": round(effective_payout, 4),
        "safe_daily_media_cost": round(safe_daily_media_cost, 2),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _percent(value: float, denominator: float) -> float:
    if denominator <= 0:
        return 0
    return value / denominator * 100


def _cap_points(cap_usage_percent: float, cap_limit: float) -> int:
    if cap_limit <= 0:
        return 0
    if cap_usage_percent < 50:
        return 15
    if cap_usage_percent < 70:
        return 10
    if cap_usage_percent < 85:
        return 5
    return 0


def _payout_points(current_payout: float, new_payout: float, effective_payout: float) -> int:
    if current_payout <= 0 and new_payout <= 0:
        return 0
    if new_payout > 0 and current_payout > 0 and new_payout < current_payout:
        return 3
    if effective_payout > 0:
        return 12
    return 5


def _quality_points(
    approval_rate_percent: float,
    paid_rate_percent: float,
    deduction_rate_percent: float,
) -> int:
    if approval_rate_percent >= 80 and paid_rate_percent >= 70 and deduction_rate_percent <= 10:
        return 12
    if approval_rate_percent >= 60 and paid_rate_percent >= 50 and deduction_rate_percent <= 20:
        return 7
    if approval_rate_percent > 0 and paid_rate_percent > 0:
        return 3
    return 0


def _freshness_points(days_since_cap_update: int) -> int:
    if days_since_cap_update <= 1:
        return 8
    if days_since_cap_update <= 3:
        return 4
    return 0


def _replacement_fit_points(
    replacement_status: str,
    replacement_fit_score: int,
    same_intent_review: bool,
) -> int:
    if replacement_status == "not_needed":
        return 8
    if replacement_status == "preapproved" and same_intent_review and replacement_fit_score >= 80:
        return 8
    if replacement_status == "preapproved" and replacement_fit_score >= 60:
        return 4
    return 0


def _risk_level(
    score: int,
    blockers: list[str],
    offer_status: str,
    policy_risk: str,
) -> str:
    if offer_status in {"capped", "paused_by_network", "expired", "quality_hold"}:
        return "high"
    if policy_risk == "high":
        return "high"
    if score >= 80 and not blockers:
        return "low"
    if score >= 60:
        return "medium"
    return "high"


def _recommended_action(
    *,
    offer_status: str,
    cap_usage_percent: float,
    cap_remaining: float,
    expected_next_conversions: float,
    buyer_capacity_status: str,
    replacement_status: str,
    replacement_fit_score: int,
    same_intent_review: bool,
    score: int,
    blockers: list[str],
) -> str:
    if offer_status in {"paused_by_network", "expired", "quality_hold"}:
        return "pause_and_collect_evidence"
    if offer_status == "capped" or cap_remaining <= 0:
        if (
            replacement_status == "preapproved"
            and same_intent_review
            and replacement_fit_score >= 80
        ):
            return "manual_switch_preapproved_replacement"
        return "pause_until_cap_resets"
    if buyer_capacity_status in {"paused", "quality_hold"}:
        return "pause_and_collect_evidence"
    if cap_usage_percent >= 85 or expected_next_conversions > cap_remaining:
        return "reduce_budget_or_pause"
    if blockers:
        return "hold_for_manual_review"
    if score >= 80:
        return "approve_manual_test"
    if score >= 60:
        return "watch_no_scale"
    return "hold_for_manual_review"


def _blockers(
    *,
    offer_status: str,
    cap_limit: float,
    cap_used: float,
    cap_remaining: float,
    expected_next_conversions: float,
    current_payout: float,
    new_payout: float,
    approval_rate_percent: float,
    paid_rate_percent: float,
    deduction_rate_percent: float,
    days_since_cap_update: int,
    buyer_capacity_status: str,
    replacement_status: str,
    replacement_fit_score: int,
    same_intent_review: bool,
    source_quality: str,
    policy_risk: str,
) -> list[str]:
    blockers: list[str] = []
    if offer_status in {"researching", "pending_approval"}:
        blockers.append("offer is not approved for traffic")
    if offer_status in {"capped", "paused_by_network", "expired", "quality_hold", "retired"}:
        blockers.append("offer status blocks new traffic")
    if cap_limit <= 0:
        blockers.append("cap limit is missing")
    if cap_used >= cap_limit > 0:
        blockers.append("cap has been reached")
    if cap_limit > 0 and cap_used / cap_limit >= 0.85:
        blockers.append("cap usage is at or above 85 percent")
    if expected_next_conversions > cap_remaining:
        blockers.append("expected next batch can exceed remaining cap")
    if current_payout <= 0 and new_payout <= 0:
        blockers.append("payout evidence is missing")
    if new_payout > 0 and current_payout > 0 and new_payout < current_payout:
        blockers.append("payout decreased and break-even must be recalculated")
    if approval_rate_percent < 60:
        blockers.append("approval rate is below 60 percent")
    if paid_rate_percent < 50:
        blockers.append("paid rate is below 50 percent")
    if deduction_rate_percent > 20:
        blockers.append("deduction rate exceeds 20 percent")
    if days_since_cap_update > 1:
        blockers.append("cap or payout evidence is older than 24 hours")
    if buyer_capacity_status != "open":
        blockers.append("buyer capacity is not fully open")
    if replacement_status in {"draft", "needs_review"}:
        blockers.append("replacement offer is not preapproved")
    if replacement_status == "preapproved" and replacement_fit_score < 80:
        blockers.append("replacement fit score is below 80")
    if replacement_status == "preapproved" and not same_intent_review:
        blockers.append("replacement same-intent review is missing")
    if source_quality != "stable":
        blockers.append("source quality is not stable")
    if policy_risk == "high":
        blockers.append("high policy risk blocks offer action")
    elif policy_risk == "medium":
        blockers.append("medium policy risk requires tighter cap")
    return blockers
