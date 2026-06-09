from __future__ import annotations


INTENT_POINTS = {
    "transactional": 25,
    "commercial": 22,
    "comparison": 20,
    "informational": 12,
    "brand": 8,
    "sensitive": 6,
    "official": 4,
    "support": 2,
    "job": 2,
    "free": 0,
    "unknown": 5,
}

POLICY_POINTS = {
    "low": 20,
    "medium": 10,
    "high": 0,
}

REVENUE_STATUS_POINTS = {
    "paid": 10,
    "approved": 7,
    "reported": 3,
    "none": 0,
}

DATA_STATUS_POINTS = {
    "mature": 10,
    "partial": 5,
    "fresh": 2,
}


def calculate_query_mining_review(
    *,
    query_intent: str,
    keyword_match_type: str,
    network: str,
    clicks: int,
    sessions: int,
    conversions: int,
    cost: float,
    approved_revenue: float,
    paid_revenue: float,
    buyer_reject_rate_percent: float,
    intent_fit_score: int,
    policy_risk: str,
    revenue_status: str,
    data_status: str,
    conversion_lag_days: int,
    brand_or_official: bool,
    support_or_login: bool,
) -> dict[str, object]:
    click_session_rate = _percent(sessions, clicks)
    cpc = cost / clicks if clicks > 0 else 0
    approved_rpv = approved_revenue / clicks if clicks > 0 else 0
    paid_rpv = paid_revenue / clicks if clicks > 0 else 0
    approved_roi = _percent(approved_revenue, cost)
    paid_roi = _percent(paid_revenue, cost)

    blockers = _blockers(
        query_intent=query_intent,
        keyword_match_type=keyword_match_type,
        network=network,
        clicks=clicks,
        sessions=sessions,
        conversions=conversions,
        cost=cost,
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        click_session_rate=click_session_rate,
        approved_roi=approved_roi,
        paid_roi=paid_roi,
        intent_fit_score=intent_fit_score,
        policy_risk=policy_risk,
        revenue_status=revenue_status,
        data_status=data_status,
        conversion_lag_days=conversion_lag_days,
        brand_or_official=brand_or_official,
        support_or_login=support_or_login,
    )

    score = 0
    score += _intent_points(query_intent, intent_fit_score)
    score += _revenue_points(
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
        approved_roi=approved_roi,
        paid_roi=paid_roi,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        revenue_status=revenue_status,
    )
    score += _cost_control_points(cost, clicks, approved_revenue, paid_revenue)
    score += POLICY_POINTS.get(policy_risk, 0)
    score += DATA_STATUS_POINTS.get(data_status, 0)
    score += _actionability_points(keyword_match_type, network)
    score = min(score, 100)

    recommended_action = _recommended_action(
        score=score,
        blockers=blockers,
        query_intent=query_intent,
        keyword_match_type=keyword_match_type,
        clicks=clicks,
        cost=cost,
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        intent_fit_score=intent_fit_score,
        policy_risk=policy_risk,
        data_status=data_status,
        revenue_status=revenue_status,
        brand_or_official=brand_or_official,
        support_or_login=support_or_login,
        click_session_rate=click_session_rate,
    )

    return {
        "score": score,
        "risk_level": _risk_level(score, blockers, policy_risk, query_intent),
        "recommended_action": recommended_action,
        "negative_match_type": _negative_match_type(
            recommended_action, query_intent, cost, clicks
        ),
        "negative_level": _negative_level(
            recommended_action, query_intent, policy_risk, brand_or_official
        ),
        "click_session_rate": round(click_session_rate, 2),
        "cpc": round(cpc, 4),
        "approved_rpv": round(approved_rpv, 4),
        "paid_rpv": round(paid_rpv, 4),
        "approved_roi": round(approved_roi, 2),
        "paid_roi": round(paid_roi, 2),
        "blockers": blockers,
    }


def _percent(value: float, denominator: float) -> float:
    if denominator <= 0:
        return 0
    return max(value, 0) / denominator * 100


def _intent_points(query_intent: str, intent_fit_score: int) -> int:
    base = INTENT_POINTS.get(query_intent, 5)
    if intent_fit_score >= 85:
        return base
    if intent_fit_score >= 70:
        return min(base, 18)
    if intent_fit_score >= 55:
        return min(base, 12)
    if intent_fit_score >= 35:
        return min(base, 6)
    return 0


def _revenue_points(
    *,
    approved_revenue: float,
    paid_revenue: float,
    approved_roi: float,
    paid_roi: float,
    buyer_reject_rate_percent: float,
    revenue_status: str,
) -> int:
    points = REVENUE_STATUS_POINTS.get(revenue_status, 0)
    if paid_revenue > 0 and paid_roi >= 130:
        points += 15
    elif paid_revenue > 0 and paid_roi >= 90:
        points += 10
    elif approved_revenue > 0 and approved_roi >= 130:
        points += 10
    elif approved_revenue > 0 and approved_roi >= 90:
        points += 6
    elif approved_revenue > 0 or paid_revenue > 0:
        points += 3

    if buyer_reject_rate_percent < 10:
        points += 5
    elif buyer_reject_rate_percent < 25:
        points += 3
    elif buyer_reject_rate_percent < 40:
        points += 1
    return min(points, 25)


def _cost_control_points(
    cost: float,
    clicks: int,
    approved_revenue: float,
    paid_revenue: float,
) -> int:
    if cost <= 0:
        return 8
    if paid_revenue > cost or approved_revenue > cost:
        return 15
    if clicks < 20:
        return 8
    if approved_revenue > 0 or paid_revenue > 0:
        return 5
    if cost < 25:
        return 4
    return 0


def _actionability_points(keyword_match_type: str, network: str) -> int:
    points = 0
    if keyword_match_type in {"exact", "phrase"}:
        points += 3
    elif keyword_match_type == "broad":
        points += 1
    if network == "google_search":
        points += 2
    elif network == "search_partners":
        points += 1
    return min(points, 5)


def _risk_level(
    score: int,
    blockers: list[str],
    policy_risk: str,
    query_intent: str,
) -> str:
    if policy_risk == "high" or query_intent in {"support", "official", "free"}:
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
    query_intent: str,
    keyword_match_type: str,
    clicks: int,
    cost: float,
    approved_revenue: float,
    paid_revenue: float,
    buyer_reject_rate_percent: float,
    intent_fit_score: int,
    policy_risk: str,
    data_status: str,
    revenue_status: str,
    brand_or_official: bool,
    support_or_login: bool,
    click_session_rate: float,
) -> str:
    if policy_risk == "high" or brand_or_official or query_intent in {"official", "sensitive"}:
        return "policy_review_negative"
    if support_or_login or query_intent in {"support", "job", "free"}:
        return "add_negative_phrase"
    if clicks >= 50 and click_session_rate < 50:
        return "tracking_gap_review"
    if buyer_reject_rate_percent >= 40:
        return "add_negative_phrase"
    if data_status == "fresh" or revenue_status in {"none", "reported"}:
        if cost >= 75 and approved_revenue <= 0 and paid_revenue <= 0:
            return "watch_wait_for_revenue"
        return "watch_wait_for_revenue"
    if cost >= 50 and approved_revenue <= 0 and paid_revenue <= 0:
        return "add_negative_phrase"
    if score >= 80 and intent_fit_score >= 80 and (paid_revenue > 0 or approved_revenue > 0):
        if keyword_match_type == "exact":
            return "scale_exact_cautiously"
        return "promote_exact_test"
    if score >= 70 and intent_fit_score >= 70:
        return "promote_phrase_test"
    if score >= 55 and query_intent in {"commercial", "comparison", "informational"}:
        return "create_page_brief"
    if blockers:
        return "split_or_pause_ad_group"
    return "hold_review"


def _negative_match_type(recommended_action: str, query_intent: str, cost: float, clicks: int) -> str:
    if not recommended_action.startswith("add_negative") and recommended_action != "policy_review_negative":
        return "none"
    if query_intent in {"support", "job", "free"} or cost >= 100 or clicks >= 100:
        return "phrase"
    if query_intent in {"official", "sensitive", "brand"}:
        return "exact"
    return "exact"


def _negative_level(
    recommended_action: str,
    query_intent: str,
    policy_risk: str,
    brand_or_official: bool,
) -> str:
    if not recommended_action.startswith("add_negative") and recommended_action != "policy_review_negative":
        return "none"
    if policy_risk == "high" or query_intent in {"free", "job"}:
        return "shared_list"
    if brand_or_official or query_intent in {"official", "brand"}:
        return "campaign"
    return "ad_group"


def _blockers(
    *,
    query_intent: str,
    keyword_match_type: str,
    network: str,
    clicks: int,
    sessions: int,
    conversions: int,
    cost: float,
    approved_revenue: float,
    paid_revenue: float,
    buyer_reject_rate_percent: float,
    click_session_rate: float,
    approved_roi: float,
    paid_roi: float,
    intent_fit_score: int,
    policy_risk: str,
    revenue_status: str,
    data_status: str,
    conversion_lag_days: int,
    brand_or_official: bool,
    support_or_login: bool,
) -> list[str]:
    blockers: list[str] = []
    if policy_risk == "high":
        blockers.append("high policy risk query requires risk review")
    elif policy_risk == "medium":
        blockers.append("medium policy risk requires manual review")
    if brand_or_official:
        blockers.append("brand or official relationship risk is present")
    if support_or_login:
        blockers.append("support, login, cancellation, or customer-service intent is present")
    if query_intent in {"free", "job", "official", "support"}:
        blockers.append("query intent is usually unsuitable for arbitrage traffic")
    if keyword_match_type == "broad" and intent_fit_score < 70:
        blockers.append("broad match query drift requires tighter controls")
    if network == "search_partners" and intent_fit_score < 70:
        blockers.append("search partner query quality is not proven")
    if clicks >= 50 and sessions <= 0:
        blockers.append("sessions are missing for a meaningful click sample")
    elif clicks >= 50 and click_session_rate < 50:
        blockers.append("click to session rate is below 50 percent")
    if data_status != "mature":
        blockers.append("data window is not mature enough for final query action")
    if revenue_status in {"none", "reported"} and conversion_lag_days > 0:
        blockers.append("revenue status is not approved or paid yet")
    if cost >= 50 and approved_revenue <= 0 and paid_revenue <= 0 and data_status == "mature":
        blockers.append("mature query spend has no approved or paid revenue")
    if conversions > 0 and paid_revenue <= 0 and revenue_status == "paid":
        blockers.append("conversions exist but paid revenue is missing")
    if paid_revenue > 0 and paid_roi < 80:
        blockers.append("paid ROI is below 80 percent")
    elif paid_revenue <= 0 and approved_revenue > 0 and approved_roi < 80:
        blockers.append("approved ROI is below 80 percent")
    if buyer_reject_rate_percent >= 30:
        blockers.append("buyer reject rate is at or above 30 percent")
    if intent_fit_score < 55:
        blockers.append("intent fit score is below 55")
    return blockers
