from __future__ import annotations


TRANSPARENCY_POINTS = {
    "full": 20,
    "partial": 10,
    "opaque": 0,
}

POLICY_STATE_POINTS = {
    "clean": 8,
    "warning": 3,
    "active": 0,
}

STOP_CONTROL_POINTS = {
    "precise": 10,
    "partial": 4,
    "none": 0,
}


def calculate_source_quality_review(
    *,
    transparency_level: str,
    tracking_completeness_percent: float,
    intent_fit_score: int,
    clicks: int,
    sessions: int,
    cost: float,
    reported_revenue: float,
    approved_revenue: float,
    paid_revenue: float,
    deducted_revenue: float,
    invalid_click_rate_percent: float,
    complaint_count: int,
    buyer_reject_rate_percent: float,
    policy_issue_state: str,
    stop_control: str,
    consistency_days: int,
) -> dict[str, object]:
    click_session_rate = _percent(sessions, clicks)
    approved_rate = _percent(approved_revenue, reported_revenue)
    paid_rate = _percent(paid_revenue, approved_revenue)
    deduction_rate = _percent(deducted_revenue, approved_revenue + deducted_revenue)
    paid_roi = _percent(paid_revenue, cost)
    approved_roi = _percent(approved_revenue, cost)

    blockers = _blockers(
        transparency_level=transparency_level,
        tracking_completeness_percent=tracking_completeness_percent,
        intent_fit_score=intent_fit_score,
        clicks=clicks,
        click_session_rate=click_session_rate,
        reported_revenue=reported_revenue,
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
        approved_rate=approved_rate,
        paid_rate=paid_rate,
        deduction_rate=deduction_rate,
        paid_roi=paid_roi,
        approved_roi=approved_roi,
        invalid_click_rate_percent=invalid_click_rate_percent,
        complaint_count=complaint_count,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        policy_issue_state=policy_issue_state,
        stop_control=stop_control,
        consistency_days=consistency_days,
    )

    score = 0
    score += TRANSPARENCY_POINTS.get(transparency_level, 0)
    score += _tracking_points(tracking_completeness_percent)
    score += _intent_points(intent_fit_score)
    score += _revenue_quality_points(
        approved_rate=approved_rate,
        paid_rate=paid_rate,
        deduction_rate=deduction_rate,
        paid_roi=paid_roi,
        approved_roi=approved_roi,
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
    )
    score += _policy_safety_points(
        policy_issue_state=policy_issue_state,
        invalid_click_rate_percent=invalid_click_rate_percent,
        complaint_count=complaint_count,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
    )
    score += STOP_CONTROL_POINTS.get(stop_control, 0)
    score += _consistency_points(consistency_days)
    score = min(score, 100)

    return {
        "score": score,
        "quality_level": _quality_level(score, blockers, policy_issue_state),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            policy_issue_state=policy_issue_state,
            invalid_click_rate_percent=invalid_click_rate_percent,
            complaint_count=complaint_count,
            buyer_reject_rate_percent=buyer_reject_rate_percent,
            stop_control=stop_control,
        ),
        "click_session_rate": round(click_session_rate, 2),
        "approved_rate": round(approved_rate, 2),
        "paid_rate": round(paid_rate, 2),
        "deduction_rate": round(deduction_rate, 2),
        "paid_roi": round(paid_roi, 2),
        "approved_roi": round(approved_roi, 2),
        "blockers": blockers,
    }


def _percent(value: float, denominator: float) -> float:
    if denominator <= 0:
        return 0
    return max(value, 0) / denominator * 100


def _tracking_points(tracking_completeness_percent: float) -> int:
    if tracking_completeness_percent >= 95:
        return 15
    if tracking_completeness_percent >= 85:
        return 12
    if tracking_completeness_percent >= 70:
        return 8
    if tracking_completeness_percent >= 50:
        return 4
    return 0


def _intent_points(intent_fit_score: int) -> int:
    if intent_fit_score >= 85:
        return 15
    if intent_fit_score >= 70:
        return 11
    if intent_fit_score >= 55:
        return 7
    if intent_fit_score >= 35:
        return 3
    return 0


def _revenue_quality_points(
    *,
    approved_rate: float,
    paid_rate: float,
    deduction_rate: float,
    paid_roi: float,
    approved_roi: float,
    approved_revenue: float,
    paid_revenue: float,
) -> int:
    points = 0
    if approved_rate >= 80:
        points += 7
    elif approved_rate >= 60:
        points += 5
    elif approved_rate > 0:
        points += 2

    if paid_rate >= 70:
        points += 5
    elif paid_rate >= 50:
        points += 3
    elif paid_revenue > 0:
        points += 1
    elif approved_revenue > 0:
        points += 2

    if paid_roi >= 120:
        points += 5
    elif paid_roi >= 80:
        points += 3
    elif paid_roi > 0:
        points += 1
    elif approved_roi >= 120:
        points += 3
    elif approved_roi >= 80:
        points += 2

    if deduction_rate <= 5:
        points += 3
    elif deduction_rate <= 15:
        points += 2
    elif deduction_rate <= 25:
        points += 1
    return min(points, 20)


def _policy_safety_points(
    *,
    policy_issue_state: str,
    invalid_click_rate_percent: float,
    complaint_count: int,
    buyer_reject_rate_percent: float,
) -> int:
    points = POLICY_STATE_POINTS.get(policy_issue_state, 0)
    if invalid_click_rate_percent < 1:
        points += 4
    elif invalid_click_rate_percent < 3:
        points += 3
    elif invalid_click_rate_percent < 5:
        points += 1
    if complaint_count == 0 and buyer_reject_rate_percent < 10:
        points += 3
    elif complaint_count <= 1 and buyer_reject_rate_percent < 25:
        points += 2
    elif complaint_count <= 2 and buyer_reject_rate_percent < 40:
        points += 1
    return min(points, 15)


def _consistency_points(consistency_days: int) -> int:
    if consistency_days >= 14:
        return 5
    if consistency_days >= 7:
        return 3
    if consistency_days >= 3:
        return 1
    return 0


def _quality_level(score: int, blockers: list[str], policy_issue_state: str) -> str:
    if policy_issue_state == "active":
        return "critical"
    if score >= 80 and not blockers:
        return "high"
    if score >= 65:
        return "medium"
    if score >= 45:
        return "low"
    return "critical"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    policy_issue_state: str,
    invalid_click_rate_percent: float,
    complaint_count: int,
    buyer_reject_rate_percent: float,
    stop_control: str,
) -> str:
    if (
        policy_issue_state == "active"
        or invalid_click_rate_percent >= 10
        or complaint_count >= 3
        or buyer_reject_rate_percent >= 50
        or (stop_control == "none" and score < 55)
    ):
        return "blocklist_stop"
    if score >= 80 and not blockers:
        return "allowlist_scale"
    if score >= 70:
        return "allowlist_test"
    if score >= 55:
        return "watchlist_no_scale"
    if score >= 40:
        return "quarantine_diagnose"
    return "blocklist_stop"


def _blockers(
    *,
    transparency_level: str,
    tracking_completeness_percent: float,
    intent_fit_score: int,
    clicks: int,
    click_session_rate: float,
    reported_revenue: float,
    approved_revenue: float,
    paid_revenue: float,
    approved_rate: float,
    paid_rate: float,
    deduction_rate: float,
    paid_roi: float,
    approved_roi: float,
    invalid_click_rate_percent: float,
    complaint_count: int,
    buyer_reject_rate_percent: float,
    policy_issue_state: str,
    stop_control: str,
    consistency_days: int,
) -> list[str]:
    blockers: list[str] = []
    if transparency_level == "opaque":
        blockers.append("source, publisher, or placement identity is opaque")
    elif transparency_level == "partial":
        blockers.append("source transparency is incomplete")
    if tracking_completeness_percent < 70:
        blockers.append("tracking completeness is below 70 percent")
    if intent_fit_score < 55:
        blockers.append("intent fit score is below 55")
    if clicks >= 50 and click_session_rate < 50:
        blockers.append("click to session rate is below 50 percent")
    if reported_revenue <= 0 and approved_revenue <= 0 and paid_revenue <= 0:
        blockers.append("revenue evidence is missing")
    if reported_revenue > 0 and approved_revenue <= 0:
        blockers.append("approved revenue evidence is missing")
    if approved_rate > 0 and approved_rate < 50:
        blockers.append("approval rate is below 50 percent")
    if approved_revenue > 0 and paid_revenue <= 0:
        blockers.append("paid revenue is not available yet")
    if paid_revenue > 0 and paid_rate < 50:
        blockers.append("paid rate is below 50 percent")
    if paid_revenue > 0 and paid_roi < 80:
        blockers.append("paid ROI is below 80 percent")
    elif paid_revenue <= 0 and approved_roi < 80:
        blockers.append("approved ROI is below 80 percent")
    if deduction_rate > 20:
        blockers.append("deduction rate exceeds 20 percent")
    if invalid_click_rate_percent >= 5:
        blockers.append("invalid click rate is at or above 5 percent")
    if complaint_count > 0:
        blockers.append("complaints require manual source review")
    if buyer_reject_rate_percent >= 30:
        blockers.append("buyer reject rate is at or above 30 percent")
    if policy_issue_state == "active":
        blockers.append("active policy issue blocks traffic")
    elif policy_issue_state == "warning":
        blockers.append("policy warning requires remediation")
    if stop_control == "none":
        blockers.append("no precise stop control for this source")
    elif stop_control == "partial":
        blockers.append("stop control is partial")
    if consistency_days < 3:
        blockers.append("sample is too short for source quality decision")
    return blockers
