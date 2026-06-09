from __future__ import annotations


CAP_CONFIDENCE_POINTS = {
    "unknown": 0,
    "stale": 3,
    "same_day": 8,
    "realtime": 12,
}

ALIGNMENT_POINTS = {
    "missing": 0,
    "mismatch": 2,
    "partial": 6,
    "aligned": 12,
}

HOLIDAY_POINTS = {
    "missing": 0,
    "unknown": 0,
    "stale": 3,
    "ready": 8,
}

SOURCE_QUALITY_POINTS = {
    "low": 2,
    "medium": 5,
    "high": 8,
    "buyer_approved": 10,
}

FALLBACK_POINTS = {
    "disabled": 6,
    "missing": 0,
    "draft": 2,
    "reviewed_same_intent": 8,
    "approved": 10,
}

GUARDRAIL_POINTS = {
    "missing": 0,
    "manual": 4,
    "defined": 8,
    "tested": 10,
}


def calculate_buyer_capacity_review(
    *,
    cap_limit: float,
    cap_used: float,
    elapsed_operating_day_percent: float,
    expected_next_hour_leads: float,
    expected_daily_leads: float,
    hourly_contact_capacity: float,
    current_hour_capacity_used: float,
    expected_paid_value_per_lead: float,
    accepted_rate_percent: float,
    qualified_rate_percent: float,
    paid_rate_percent: float,
    no_buyer_rate_percent: float,
    missed_contact_rate_percent: float,
    after_hours_lead_rate_percent: float,
    cap_last_confirmed_hours: int,
    feedback_sla_hours: int,
    first_attempt_sla_minutes: int,
    cap_confidence_status: str,
    hours_alignment_status: str,
    ad_schedule_alignment_status: str,
    timezone_alignment_status: str,
    holiday_readiness_status: str,
    fallback_status: str,
    source_quality_status: str,
    overdelivery_guardrail_status: str,
    cap_snapshot_evidence: bool,
    buyer_hours_evidence: bool,
    ad_schedule_evidence: bool,
    call_reporting_evidence: bool,
    no_buyer_tracking_ready: bool,
    missed_contact_tracking_ready: bool,
    dayparting_cohort_ready: bool,
    fallback_buyer_reviewed: bool,
    human_review: bool,
) -> dict[str, object]:
    cap_remaining = max(cap_limit - cap_used, 0)
    cap_usage_percent = _percent(cap_used, cap_limit)
    elapsed_ratio = _rate(elapsed_operating_day_percent)
    projected_end_of_day_usage_percent = (
        cap_usage_percent / elapsed_ratio if elapsed_ratio > 0 else 0
    )
    contact_capacity_remaining = max(
        hourly_contact_capacity - current_hour_capacity_used, 0
    )
    daily_capacity_remaining = max(cap_limit - expected_daily_leads, 0)
    safe_leads_remaining = min(
        cap_remaining,
        contact_capacity_remaining,
        daily_capacity_remaining,
    )

    accepted_rate = _rate(accepted_rate_percent)
    qualified_rate = _rate(qualified_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    no_buyer_rate = _rate(no_buyer_rate_percent)
    net_value_per_lead = (
        expected_paid_value_per_lead
        * accepted_rate
        * qualified_rate
        * paid_rate
        * max(1 - no_buyer_rate, 0)
    )
    safe_media_spend_remaining = safe_leads_remaining * net_value_per_lead * 0.65

    blockers = _blockers(
        cap_limit=cap_limit,
        cap_remaining=cap_remaining,
        cap_usage_percent=cap_usage_percent,
        projected_end_of_day_usage_percent=projected_end_of_day_usage_percent,
        expected_next_hour_leads=expected_next_hour_leads,
        expected_daily_leads=expected_daily_leads,
        hourly_contact_capacity=hourly_contact_capacity,
        current_hour_capacity_used=current_hour_capacity_used,
        safe_leads_remaining=safe_leads_remaining,
        safe_media_spend_remaining=safe_media_spend_remaining,
        no_buyer_rate_percent=no_buyer_rate_percent,
        missed_contact_rate_percent=missed_contact_rate_percent,
        after_hours_lead_rate_percent=after_hours_lead_rate_percent,
        cap_last_confirmed_hours=cap_last_confirmed_hours,
        feedback_sla_hours=feedback_sla_hours,
        first_attempt_sla_minutes=first_attempt_sla_minutes,
        cap_confidence_status=cap_confidence_status,
        hours_alignment_status=hours_alignment_status,
        ad_schedule_alignment_status=ad_schedule_alignment_status,
        timezone_alignment_status=timezone_alignment_status,
        holiday_readiness_status=holiday_readiness_status,
        fallback_status=fallback_status,
        overdelivery_guardrail_status=overdelivery_guardrail_status,
        cap_snapshot_evidence=cap_snapshot_evidence,
        buyer_hours_evidence=buyer_hours_evidence,
        ad_schedule_evidence=ad_schedule_evidence,
        call_reporting_evidence=call_reporting_evidence,
        no_buyer_tracking_ready=no_buyer_tracking_ready,
        missed_contact_tracking_ready=missed_contact_tracking_ready,
        dayparting_cohort_ready=dayparting_cohort_ready,
        fallback_buyer_reviewed=fallback_buyer_reviewed,
        human_review=human_review,
    )

    score = 0
    score += CAP_CONFIDENCE_POINTS.get(cap_confidence_status, 0)
    score += ALIGNMENT_POINTS.get(hours_alignment_status, 0)
    score += ALIGNMENT_POINTS.get(ad_schedule_alignment_status, 0)
    score += ALIGNMENT_POINTS.get(timezone_alignment_status, 0)
    score += HOLIDAY_POINTS.get(holiday_readiness_status, 0)
    score += FALLBACK_POINTS.get(fallback_status, 0)
    score += SOURCE_QUALITY_POINTS.get(source_quality_status, 0)
    score += GUARDRAIL_POINTS.get(overdelivery_guardrail_status, 0)
    score += _capacity_points(
        cap_usage_percent=cap_usage_percent,
        projected_end_of_day_usage_percent=projected_end_of_day_usage_percent,
        safe_leads_remaining=safe_leads_remaining,
        expected_next_hour_leads=expected_next_hour_leads,
    )
    score += _contact_points(
        hourly_contact_capacity=hourly_contact_capacity,
        current_hour_capacity_used=current_hour_capacity_used,
        no_buyer_rate_percent=no_buyer_rate_percent,
        missed_contact_rate_percent=missed_contact_rate_percent,
        after_hours_lead_rate_percent=after_hours_lead_rate_percent,
    )
    score += _sla_points(feedback_sla_hours, first_attempt_sla_minutes)
    score += 4 if cap_snapshot_evidence else 0
    score += 4 if buyer_hours_evidence else 0
    score += 4 if ad_schedule_evidence else 0
    score += 4 if call_reporting_evidence else 0
    score += 3 if no_buyer_tracking_ready else 0
    score += 3 if missed_contact_tracking_ready else 0
    score += 4 if dayparting_cohort_ready else 0
    score += 4 if fallback_buyer_reviewed else 0
    score += 4 if human_review else 0
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(
            score=score,
            blockers=blockers,
            cap_confidence_status=cap_confidence_status,
            hours_alignment_status=hours_alignment_status,
            ad_schedule_alignment_status=ad_schedule_alignment_status,
            no_buyer_rate_percent=no_buyer_rate_percent,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            cap_confidence_status=cap_confidence_status,
            hours_alignment_status=hours_alignment_status,
            ad_schedule_alignment_status=ad_schedule_alignment_status,
            holiday_readiness_status=holiday_readiness_status,
            no_buyer_rate_percent=no_buyer_rate_percent,
            missed_contact_rate_percent=missed_contact_rate_percent,
            projected_end_of_day_usage_percent=projected_end_of_day_usage_percent,
            cap_remaining=cap_remaining,
            expected_next_hour_leads=expected_next_hour_leads,
            safe_media_spend_remaining=safe_media_spend_remaining,
        ),
        "cap_usage_percent": round(cap_usage_percent, 2),
        "cap_remaining": round(cap_remaining, 2),
        "projected_end_of_day_usage_percent": round(
            projected_end_of_day_usage_percent, 2
        ),
        "safe_leads_remaining": round(safe_leads_remaining, 2),
        "safe_media_spend_remaining": round(safe_media_spend_remaining, 2),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _percent(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0
    return numerator / denominator * 100


def _capacity_points(
    *,
    cap_usage_percent: float,
    projected_end_of_day_usage_percent: float,
    safe_leads_remaining: float,
    expected_next_hour_leads: float,
) -> int:
    if safe_leads_remaining <= 0:
        return 0
    points = 0
    if cap_usage_percent < 70:
        points += 8
    elif cap_usage_percent < 85:
        points += 4
    if projected_end_of_day_usage_percent < 85:
        points += 8
    elif projected_end_of_day_usage_percent < 100:
        points += 4
    if safe_leads_remaining >= expected_next_hour_leads * 2:
        points += 6
    elif safe_leads_remaining >= expected_next_hour_leads:
        points += 3
    return points


def _contact_points(
    *,
    hourly_contact_capacity: float,
    current_hour_capacity_used: float,
    no_buyer_rate_percent: float,
    missed_contact_rate_percent: float,
    after_hours_lead_rate_percent: float,
) -> int:
    if hourly_contact_capacity <= 0:
        return 0
    points = 0
    usage_percent = _percent(current_hour_capacity_used, hourly_contact_capacity)
    if usage_percent < 70:
        points += 6
    elif usage_percent < 90:
        points += 3
    if no_buyer_rate_percent <= 3:
        points += 5
    elif no_buyer_rate_percent <= 8:
        points += 2
    if missed_contact_rate_percent <= 10:
        points += 5
    elif missed_contact_rate_percent <= 20:
        points += 2
    if after_hours_lead_rate_percent <= 5:
        points += 4
    elif after_hours_lead_rate_percent <= 10:
        points += 2
    return points


def _sla_points(feedback_sla_hours: int, first_attempt_sla_minutes: int) -> int:
    points = 0
    if feedback_sla_hours <= 24:
        points += 5
    elif feedback_sla_hours <= 72:
        points += 2
    if first_attempt_sla_minutes <= 5:
        points += 5
    elif first_attempt_sla_minutes <= 15:
        points += 3
    return points


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    cap_confidence_status: str,
    hours_alignment_status: str,
    ad_schedule_alignment_status: str,
    no_buyer_rate_percent: float,
) -> str:
    if cap_confidence_status in {"unknown", "stale"}:
        return "high"
    if hours_alignment_status in {"missing", "mismatch"}:
        return "high"
    if ad_schedule_alignment_status in {"missing", "mismatch"}:
        return "high"
    if no_buyer_rate_percent > 15:
        return "high"
    if score >= 85 and not blockers:
        return "low"
    if score >= 65:
        return "medium"
    return "high"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    cap_confidence_status: str,
    hours_alignment_status: str,
    ad_schedule_alignment_status: str,
    holiday_readiness_status: str,
    no_buyer_rate_percent: float,
    missed_contact_rate_percent: float,
    projected_end_of_day_usage_percent: float,
    cap_remaining: float,
    expected_next_hour_leads: float,
    safe_media_spend_remaining: float,
) -> str:
    if cap_confidence_status in {"unknown", "stale"}:
        return "refresh_cap_snapshot"
    if hours_alignment_status in {"missing", "mismatch"}:
        return "fix_buyer_hours"
    if ad_schedule_alignment_status in {"missing", "mismatch"}:
        return "fix_dayparting_schedule"
    if holiday_readiness_status in {"missing", "unknown"}:
        return "hold_for_holiday_calendar"
    if no_buyer_rate_percent > 10:
        return "pause_and_fix_no_buyer"
    if missed_contact_rate_percent > 20:
        return "fix_call_capacity"
    if projected_end_of_day_usage_percent >= 100:
        return "reduce_budget_or_pause"
    if cap_remaining <= expected_next_hour_leads:
        return "reduce_budget_or_pause"
    if safe_media_spend_remaining <= 0:
        return "hold_for_capacity"
    if blockers:
        return "capacity_review"
    if score >= 85:
        return "approve_small_ramp"
    if score >= 70:
        return "monitor_capacity"
    return "hold_for_capacity_rework"


def _blockers(
    *,
    cap_limit: float,
    cap_remaining: float,
    cap_usage_percent: float,
    projected_end_of_day_usage_percent: float,
    expected_next_hour_leads: float,
    expected_daily_leads: float,
    hourly_contact_capacity: float,
    current_hour_capacity_used: float,
    safe_leads_remaining: float,
    safe_media_spend_remaining: float,
    no_buyer_rate_percent: float,
    missed_contact_rate_percent: float,
    after_hours_lead_rate_percent: float,
    cap_last_confirmed_hours: int,
    feedback_sla_hours: int,
    first_attempt_sla_minutes: int,
    cap_confidence_status: str,
    hours_alignment_status: str,
    ad_schedule_alignment_status: str,
    timezone_alignment_status: str,
    holiday_readiness_status: str,
    fallback_status: str,
    overdelivery_guardrail_status: str,
    cap_snapshot_evidence: bool,
    buyer_hours_evidence: bool,
    ad_schedule_evidence: bool,
    call_reporting_evidence: bool,
    no_buyer_tracking_ready: bool,
    missed_contact_tracking_ready: bool,
    dayparting_cohort_ready: bool,
    fallback_buyer_reviewed: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if cap_limit <= 0:
        blockers.append("buyer cap limit is missing")
    if cap_remaining <= 0:
        blockers.append("buyer cap is exhausted")
    if expected_daily_leads > cap_limit and cap_limit > 0:
        blockers.append("expected daily leads exceed buyer cap")
    if cap_remaining <= expected_next_hour_leads:
        blockers.append("cap remaining is not enough for the next hour")
    if cap_usage_percent >= 85:
        blockers.append("cap usage is above 85 percent")
    if projected_end_of_day_usage_percent >= 100:
        blockers.append("projected end-of-day usage exceeds cap")
    if hourly_contact_capacity <= 0:
        blockers.append("hourly contact capacity is missing")
    if current_hour_capacity_used > hourly_contact_capacity:
        blockers.append("current hour capacity is already overused")
    if safe_leads_remaining <= 0:
        blockers.append("safe leads remaining is zero")
    if safe_media_spend_remaining <= 0:
        blockers.append("safe media spend remaining is zero")
    if no_buyer_rate_percent > 10:
        blockers.append("no-buyer rate exceeds 10 percent")
    if missed_contact_rate_percent > 20:
        blockers.append("missed contact rate exceeds 20 percent")
    if after_hours_lead_rate_percent > 10:
        blockers.append("after-hours lead rate exceeds 10 percent")
    if cap_last_confirmed_hours > 24:
        blockers.append("cap confirmation is older than 24 hours")
    if feedback_sla_hours > 72:
        blockers.append("buyer feedback SLA is longer than 72 hours")
    if first_attempt_sla_minutes > 15:
        blockers.append("first attempt SLA is longer than 15 minutes")
    if cap_confidence_status in {"unknown", "stale"}:
        blockers.append("cap confidence is unknown or stale")
    if hours_alignment_status in {"missing", "mismatch"}:
        blockers.append("buyer hours are missing or mismatched")
    if ad_schedule_alignment_status in {"missing", "mismatch"}:
        blockers.append("ad schedule is missing or mismatched")
    if timezone_alignment_status in {"missing", "mismatch"}:
        blockers.append("timezone alignment is missing or mismatched")
    if holiday_readiness_status in {"missing", "unknown", "stale"}:
        blockers.append("holiday calendar is not ready")
    if fallback_status in {"missing", "draft"}:
        blockers.append("fallback buyer policy is not approved")
    if overdelivery_guardrail_status in {"missing", "manual"}:
        blockers.append("overdelivery hard-stop guardrail is not tested")
    if not cap_snapshot_evidence:
        blockers.append("cap snapshot evidence is missing")
    if not buyer_hours_evidence:
        blockers.append("buyer hours evidence is missing")
    if not ad_schedule_evidence:
        blockers.append("ad schedule evidence is missing")
    if not call_reporting_evidence:
        blockers.append("call or lead reporting evidence is missing")
    if not no_buyer_tracking_ready:
        blockers.append("no-buyer tracking is missing")
    if not missed_contact_tracking_ready:
        blockers.append("missed contact tracking is missing")
    if not dayparting_cohort_ready:
        blockers.append("dayparting cohort evidence is missing")
    if fallback_status not in {"disabled", "approved"} and not fallback_buyer_reviewed:
        blockers.append("fallback buyer review is missing")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
