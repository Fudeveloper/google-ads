from __future__ import annotations


CONSENT_POINTS = {
    "missing": 0,
    "none": 0,
    "single_buyer": 9,
    "named_buyer": 12,
    "named_buyer_group": 12,
    "shared_group": 8,
    "aged_refresh_reviewed": 10,
    "tcp_sms_reviewed": 12,
}

DISCLOSURE_POINTS = {
    "missing": 0,
    "generic": 4,
    "buyer_group": 9,
    "named_buyers": 12,
    "contract_reviewed": 12,
}

PING_FIELD_POINTS = {
    "unknown": 0,
    "full_pii": 0,
    "minimal_non_pii": 10,
    "hashed_dedupe": 12,
    "rule_reviewed": 12,
}

PII_POINTS = {
    "unknown": 0,
    "raw_pii_in_url": 0,
    "full_pii_ping": 0,
    "internal_only": 6,
    "hashed_minimized": 10,
    "post_only_to_selected_buyer": 12,
    "not_used": 12,
}

CHECK_STATUS_POINTS = {
    "missing": 0,
    "blocked": 0,
    "stale": 3,
    "partial": 5,
    "checked": 8,
    "ready": 10,
}

CAP_POINTS = {
    "missing": 0,
    "stale": 3,
    "same_day": 8,
    "realtime": 10,
}

FALLBACK_POINTS = {
    "missing": 0,
    "draft": 3,
    "disabled": 6,
    "reviewed_same_intent": 8,
    "approved": 10,
}

FEEDBACK_POINTS = {
    "missing": 0,
    "delayed": 4,
    "accepted_only": 5,
    "mapped": 8,
    "paid_feedback_ready": 10,
}

SOURCE_POLICY_POINTS = {
    "unknown": 0,
    "disallowed": 0,
    "under_review": 4,
    "approved": 8,
    "buyer_approved": 10,
}

ROUTING_MODE_POINTS = {
    "direct_post": 7,
    "ping_post": 10,
    "waterfall": 8,
    "auction": 10,
    "priority": 9,
    "weighted_split": 7,
    "exclusive_first_shared_fallback": 6,
}


def calculate_ping_post_routing_review(
    *,
    routing_mode: str,
    lead_type: str,
    consent_scope: str,
    buyer_disclosure_status: str,
    ping_field_scope: str,
    pii_level: str,
    suppression_status: str,
    dnc_status: str,
    cap_snapshot_status: str,
    fallback_status: str,
    buyer_feedback_status: str,
    source_policy_status: str,
    buyer_count: int,
    max_post_buyers: int,
    pinged_buyers: int,
    accepted_buyers: int,
    posted_buyers: int,
    primary_buyer_cap_remaining: float,
    cap_last_checked_minutes: int,
    lead_age_minutes: int,
    avg_ping_latency_ms: int,
    expected_bid_amount: float,
    fallback_payout_amount: float,
    buyer_accept_rate_percent: float,
    qualification_rate_percent: float,
    paid_rate_percent: float,
    no_buyer_rate_percent: float,
    reject_rate_percent: float,
    duplicate_rate_percent: float,
    complaint_rate_percent: float,
    fields_sent_schema: str,
    routing_rule_summary: str,
    reject_reason_map: str,
    fallback_policy: str,
    buyer_feedback_plan: str,
    incident_notes: str,
    consent_version_evidence: bool,
    buyer_disclosure_reviewed: bool,
    field_minimization_reviewed: bool,
    suppression_dnc_checked: bool,
    cap_snapshot_evidence: bool,
    routing_rule_reviewed: bool,
    exclusive_shared_terms_reviewed: bool,
    fallback_buyer_reviewed: bool,
    buyer_feedback_ready: bool,
    source_policy_reviewed: bool,
    human_review: bool,
) -> dict[str, object]:
    accept_rate = _rate(buyer_accept_rate_percent)
    qualified_rate = _rate(qualification_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    no_buyer_rate = _rate(no_buyer_rate_percent)
    duplicate_rate = _rate(duplicate_rate_percent)
    complaint_rate = _rate(complaint_rate_percent)

    fallback_multiplier = 1 if fallback_status in {"reviewed_same_intent", "approved"} else 0
    primary_value = expected_bid_amount * accept_rate * qualified_rate * paid_rate
    fallback_value = (
        fallback_payout_amount
        * max(1 - accept_rate, 0)
        * qualified_rate
        * paid_rate
        * fallback_multiplier
    )
    expected_payable_value = (
        (primary_value + fallback_value)
        * max(1 - no_buyer_rate, 0)
        * max(1 - duplicate_rate, 0)
        * max(1 - complaint_rate, 0)
    )
    safe_cpl = expected_payable_value * 0.65

    blockers = _blockers(
        routing_mode=routing_mode,
        lead_type=lead_type,
        consent_scope=consent_scope,
        buyer_disclosure_status=buyer_disclosure_status,
        ping_field_scope=ping_field_scope,
        pii_level=pii_level,
        suppression_status=suppression_status,
        dnc_status=dnc_status,
        cap_snapshot_status=cap_snapshot_status,
        fallback_status=fallback_status,
        buyer_feedback_status=buyer_feedback_status,
        source_policy_status=source_policy_status,
        buyer_count=buyer_count,
        max_post_buyers=max_post_buyers,
        pinged_buyers=pinged_buyers,
        accepted_buyers=accepted_buyers,
        posted_buyers=posted_buyers,
        primary_buyer_cap_remaining=primary_buyer_cap_remaining,
        cap_last_checked_minutes=cap_last_checked_minutes,
        lead_age_minutes=lead_age_minutes,
        avg_ping_latency_ms=avg_ping_latency_ms,
        expected_bid_amount=expected_bid_amount,
        buyer_accept_rate_percent=buyer_accept_rate_percent,
        qualification_rate_percent=qualification_rate_percent,
        paid_rate_percent=paid_rate_percent,
        no_buyer_rate_percent=no_buyer_rate_percent,
        reject_rate_percent=reject_rate_percent,
        duplicate_rate_percent=duplicate_rate_percent,
        complaint_rate_percent=complaint_rate_percent,
        fields_sent_schema=fields_sent_schema,
        routing_rule_summary=routing_rule_summary,
        reject_reason_map=reject_reason_map,
        fallback_policy=fallback_policy,
        buyer_feedback_plan=buyer_feedback_plan,
        incident_notes=incident_notes,
        consent_version_evidence=consent_version_evidence,
        buyer_disclosure_reviewed=buyer_disclosure_reviewed,
        field_minimization_reviewed=field_minimization_reviewed,
        suppression_dnc_checked=suppression_dnc_checked,
        cap_snapshot_evidence=cap_snapshot_evidence,
        routing_rule_reviewed=routing_rule_reviewed,
        exclusive_shared_terms_reviewed=exclusive_shared_terms_reviewed,
        fallback_buyer_reviewed=fallback_buyer_reviewed,
        buyer_feedback_ready=buyer_feedback_ready,
        source_policy_reviewed=source_policy_reviewed,
        human_review=human_review,
    )

    components = {
        "consent_and_disclosure": _consent_disclosure_points(
            consent_scope=consent_scope,
            buyer_disclosure_status=buyer_disclosure_status,
            consent_version_evidence=consent_version_evidence,
            buyer_disclosure_reviewed=buyer_disclosure_reviewed,
        ),
        "field_minimization_pii": _field_pii_points(
            ping_field_scope=ping_field_scope,
            pii_level=pii_level,
            field_minimization_reviewed=field_minimization_reviewed,
        ),
        "routing_rule_quality": _routing_points(
            routing_mode=routing_mode,
            buyer_count=buyer_count,
            max_post_buyers=max_post_buyers,
            pinged_buyers=pinged_buyers,
            accepted_buyers=accepted_buyers,
            posted_buyers=posted_buyers,
            avg_ping_latency_ms=avg_ping_latency_ms,
            routing_rule_reviewed=routing_rule_reviewed,
        ),
        "buyer_cap_capacity": _cap_points(
            cap_snapshot_status=cap_snapshot_status,
            primary_buyer_cap_remaining=primary_buyer_cap_remaining,
            cap_last_checked_minutes=cap_last_checked_minutes,
            no_buyer_rate_percent=no_buyer_rate_percent,
            cap_snapshot_evidence=cap_snapshot_evidence,
        ),
        "economics_feedback": _economics_feedback_points(
            expected_payable_value=expected_payable_value,
            buyer_accept_rate_percent=buyer_accept_rate_percent,
            qualification_rate_percent=qualification_rate_percent,
            paid_rate_percent=paid_rate_percent,
            reject_rate_percent=reject_rate_percent,
            buyer_feedback_status=buyer_feedback_status,
            buyer_feedback_ready=buyer_feedback_ready,
        ),
        "suppression_dnc": _suppression_points(
            suppression_status=suppression_status,
            dnc_status=dnc_status,
            suppression_dnc_checked=suppression_dnc_checked,
        ),
        "exclusive_shared_aged_governance": _lead_type_points(
            lead_type=lead_type,
            consent_scope=consent_scope,
            buyer_disclosure_status=buyer_disclosure_status,
            max_post_buyers=max_post_buyers,
            lead_age_minutes=lead_age_minutes,
            exclusive_shared_terms_reviewed=exclusive_shared_terms_reviewed,
            fallback_buyer_reviewed=fallback_buyer_reviewed,
        ),
        "incident_policy_safety": _incident_policy_points(
            source_policy_status=source_policy_status,
            duplicate_rate_percent=duplicate_rate_percent,
            complaint_rate_percent=complaint_rate_percent,
            incident_notes=incident_notes,
            source_policy_reviewed=source_policy_reviewed,
            human_review=human_review,
        ),
    }
    score = max(min(sum(components.values()), 100), 0)

    return {
        "score_components": components,
        "score": score,
        "risk_level": _risk_level(
            score=score,
            blockers=blockers,
            consent_scope=consent_scope,
            buyer_disclosure_status=buyer_disclosure_status,
            pii_level=pii_level,
            suppression_status=suppression_status,
            dnc_status=dnc_status,
            source_policy_status=source_policy_status,
            no_buyer_rate_percent=no_buyer_rate_percent,
            complaint_rate_percent=complaint_rate_percent,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            consent_scope=consent_scope,
            buyer_disclosure_status=buyer_disclosure_status,
            ping_field_scope=ping_field_scope,
            pii_level=pii_level,
            cap_snapshot_status=cap_snapshot_status,
            cap_last_checked_minutes=cap_last_checked_minutes,
            no_buyer_rate_percent=no_buyer_rate_percent,
            reject_rate_percent=reject_rate_percent,
            buyer_feedback_status=buyer_feedback_status,
            fallback_status=fallback_status,
        ),
        "expected_payable_value_per_lead": round(expected_payable_value, 4),
        "safe_cpl": round(safe_cpl, 4),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _weighted_points(primary: int, secondary: int, max_points: int) -> int:
    return min(int(round(primary * 0.6 + secondary * 0.4)), max_points)


def _consent_disclosure_points(
    *,
    consent_scope: str,
    buyer_disclosure_status: str,
    consent_version_evidence: bool,
    buyer_disclosure_reviewed: bool,
) -> int:
    points = _weighted_points(
        CONSENT_POINTS.get(consent_scope, 0),
        DISCLOSURE_POINTS.get(buyer_disclosure_status, 0),
        12,
    )
    points += 2 if consent_version_evidence else 0
    points += 1 if buyer_disclosure_reviewed else 0
    return min(points, 15)


def _field_pii_points(
    *,
    ping_field_scope: str,
    pii_level: str,
    field_minimization_reviewed: bool,
) -> int:
    points = _weighted_points(
        PING_FIELD_POINTS.get(ping_field_scope, 0),
        PII_POINTS.get(pii_level, 0),
        13,
    )
    points += 2 if field_minimization_reviewed else 0
    return min(points, 15)


def _routing_points(
    *,
    routing_mode: str,
    buyer_count: int,
    max_post_buyers: int,
    pinged_buyers: int,
    accepted_buyers: int,
    posted_buyers: int,
    avg_ping_latency_ms: int,
    routing_rule_reviewed: bool,
) -> int:
    points = min(ROUTING_MODE_POINTS.get(routing_mode, 0), 6)
    if buyer_count > 0:
        points += 2
    if pinged_buyers > 0:
        points += 2
    if accepted_buyers > 0:
        points += 2
    if 0 < posted_buyers <= max_post_buyers:
        points += 1
    if avg_ping_latency_ms <= 1200:
        points += 1
    if routing_rule_reviewed:
        points += 2
    return min(points, 15)


def _cap_points(
    *,
    cap_snapshot_status: str,
    primary_buyer_cap_remaining: float,
    cap_last_checked_minutes: int,
    no_buyer_rate_percent: float,
    cap_snapshot_evidence: bool,
) -> int:
    points = CAP_POINTS.get(cap_snapshot_status, 0)
    if primary_buyer_cap_remaining >= 20:
        points += 3
    elif primary_buyer_cap_remaining > 0:
        points += 1
    if cap_last_checked_minutes <= 60:
        points += 2
    elif cap_last_checked_minutes <= 240:
        points += 1
    if no_buyer_rate_percent <= 3:
        points += 2
    elif no_buyer_rate_percent <= 8:
        points += 1
    if cap_snapshot_evidence:
        points += 2
    return min(points, 15)


def _economics_feedback_points(
    *,
    expected_payable_value: float,
    buyer_accept_rate_percent: float,
    qualification_rate_percent: float,
    paid_rate_percent: float,
    reject_rate_percent: float,
    buyer_feedback_status: str,
    buyer_feedback_ready: bool,
) -> int:
    points = min(FEEDBACK_POINTS.get(buyer_feedback_status, 0), 5)
    if expected_payable_value > 0:
        points += 2
    if buyer_accept_rate_percent >= 60:
        points += 2
    elif buyer_accept_rate_percent >= 40:
        points += 1
    if qualification_rate_percent >= 50:
        points += 2
    elif qualification_rate_percent >= 30:
        points += 1
    if paid_rate_percent >= 45:
        points += 2
    elif paid_rate_percent >= 25:
        points += 1
    if reject_rate_percent <= 15:
        points += 1
    if buyer_feedback_ready:
        points += 2
    return min(points, 15)


def _suppression_points(
    *,
    suppression_status: str,
    dnc_status: str,
    suppression_dnc_checked: bool,
) -> int:
    points = int(
        round(
            CHECK_STATUS_POINTS.get(suppression_status, 0) * 0.45
            + CHECK_STATUS_POINTS.get(dnc_status, 0) * 0.45
        )
    )
    points += 1 if suppression_dnc_checked else 0
    return min(points, 10)


def _lead_type_points(
    *,
    lead_type: str,
    consent_scope: str,
    buyer_disclosure_status: str,
    max_post_buyers: int,
    lead_age_minutes: int,
    exclusive_shared_terms_reviewed: bool,
    fallback_buyer_reviewed: bool,
) -> int:
    points = 0
    if lead_type == "exclusive" and max_post_buyers <= 1:
        points += 4
    elif lead_type == "shared" and max_post_buyers > 1:
        points += 2
        if consent_scope in {"shared_group", "named_buyer_group", "tcp_sms_reviewed"}:
            points += 2
        if buyer_disclosure_status in {"buyer_group", "named_buyers", "contract_reviewed"}:
            points += 1
    elif lead_type == "aged":
        points += 2 if lead_age_minutes > 0 else 0
        if consent_scope == "aged_refresh_reviewed":
            points += 3
    elif lead_type == "transfer":
        points += 2
    if exclusive_shared_terms_reviewed:
        points += 3
    if fallback_buyer_reviewed:
        points += 2
    return min(points, 10)


def _incident_policy_points(
    *,
    source_policy_status: str,
    duplicate_rate_percent: float,
    complaint_rate_percent: float,
    incident_notes: str,
    source_policy_reviewed: bool,
    human_review: bool,
) -> int:
    points = 0
    if SOURCE_POLICY_POINTS.get(source_policy_status, 0) >= 8:
        points += 1
    if duplicate_rate_percent <= 5:
        points += 1
    if complaint_rate_percent <= 1:
        points += 1
    if source_policy_reviewed:
        points += 1
    if human_review:
        points += 1
    if "complaint" in incident_notes.lower() and complaint_rate_percent > 1:
        points -= 1
    return max(min(points, 5), 0)


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    consent_scope: str,
    buyer_disclosure_status: str,
    pii_level: str,
    suppression_status: str,
    dnc_status: str,
    source_policy_status: str,
    no_buyer_rate_percent: float,
    complaint_rate_percent: float,
) -> str:
    if consent_scope in {"missing", "none"}:
        return "critical"
    if buyer_disclosure_status == "missing":
        return "critical"
    if pii_level in {"raw_pii_in_url", "full_pii_ping"}:
        return "critical"
    if suppression_status == "blocked" or dnc_status == "blocked":
        return "critical"
    if source_policy_status == "disallowed":
        return "critical"
    if no_buyer_rate_percent > 15 or complaint_rate_percent > 2:
        return "high"
    if score >= 85 and not blockers:
        return "low"
    if score >= 70:
        return "medium"
    return "high"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    consent_scope: str,
    buyer_disclosure_status: str,
    ping_field_scope: str,
    pii_level: str,
    cap_snapshot_status: str,
    cap_last_checked_minutes: int,
    no_buyer_rate_percent: float,
    reject_rate_percent: float,
    buyer_feedback_status: str,
    fallback_status: str,
) -> str:
    if consent_scope in {"missing", "none"} or buyer_disclosure_status == "missing":
        return "block_consent_or_pii"
    if pii_level in {"raw_pii_in_url", "full_pii_ping"}:
        return "block_consent_or_pii"
    if ping_field_scope in {"unknown", "full_pii"}:
        return "fix_field_minimization"
    if cap_snapshot_status in {"missing", "stale"} or cap_last_checked_minutes > 240:
        return "refresh_cap_snapshot"
    if no_buyer_rate_percent > 10:
        return "fix_no_buyer"
    if reject_rate_percent > 25:
        return "fix_reject_reason_map"
    if fallback_status in {"missing", "draft"}:
        return "fallback_review"
    if buyer_feedback_status in {"missing", "delayed", "accepted_only"}:
        return "buyer_feedback_required"
    if score >= 85 and not blockers:
        return "routing_ready"
    if score >= 70:
        return "manual_test"
    if blockers:
        return "routing_review"
    return "blocked"


def _blockers(
    *,
    routing_mode: str,
    lead_type: str,
    consent_scope: str,
    buyer_disclosure_status: str,
    ping_field_scope: str,
    pii_level: str,
    suppression_status: str,
    dnc_status: str,
    cap_snapshot_status: str,
    fallback_status: str,
    buyer_feedback_status: str,
    source_policy_status: str,
    buyer_count: int,
    max_post_buyers: int,
    pinged_buyers: int,
    accepted_buyers: int,
    posted_buyers: int,
    primary_buyer_cap_remaining: float,
    cap_last_checked_minutes: int,
    lead_age_minutes: int,
    avg_ping_latency_ms: int,
    expected_bid_amount: float,
    buyer_accept_rate_percent: float,
    qualification_rate_percent: float,
    paid_rate_percent: float,
    no_buyer_rate_percent: float,
    reject_rate_percent: float,
    duplicate_rate_percent: float,
    complaint_rate_percent: float,
    fields_sent_schema: str,
    routing_rule_summary: str,
    reject_reason_map: str,
    fallback_policy: str,
    buyer_feedback_plan: str,
    incident_notes: str,
    consent_version_evidence: bool,
    buyer_disclosure_reviewed: bool,
    field_minimization_reviewed: bool,
    suppression_dnc_checked: bool,
    cap_snapshot_evidence: bool,
    routing_rule_reviewed: bool,
    exclusive_shared_terms_reviewed: bool,
    fallback_buyer_reviewed: bool,
    buyer_feedback_ready: bool,
    source_policy_reviewed: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if consent_scope in {"missing", "none"}:
        blockers.append("consent scope is missing or none")
    if buyer_disclosure_status == "missing":
        blockers.append("buyer disclosure is missing")
    if ping_field_scope in {"unknown", "full_pii"}:
        blockers.append("ping field scope is unknown or sends full PII")
    if pii_level in {"unknown", "raw_pii_in_url", "full_pii_ping"}:
        blockers.append("PII handling is unknown or unsafe for ping/post")
    if suppression_status in {"missing", "blocked"}:
        blockers.append("suppression status is missing or blocked")
    if dnc_status in {"missing", "blocked"}:
        blockers.append("DNC status is missing or blocked")
    if cap_snapshot_status in {"missing", "stale"}:
        blockers.append("buyer cap snapshot is missing or stale")
    if source_policy_status in {"unknown", "disallowed"}:
        blockers.append("source policy status is unknown or disallowed")
    if buyer_count <= 0:
        blockers.append("buyer count is missing")
    if routing_mode != "direct_post" and pinged_buyers <= 0:
        blockers.append("ping/post route has no pinged buyers")
    if routing_mode != "direct_post" and accepted_buyers <= 0:
        blockers.append("ping/post route has no accepted buyers")
    if posted_buyers > max_post_buyers:
        blockers.append("posted buyers exceed max allowed buyer count")
    if lead_type == "exclusive" and max_post_buyers > 1:
        blockers.append("exclusive lead allows more than one post buyer")
    if lead_type == "exclusive" and posted_buyers > 1:
        blockers.append("exclusive lead has more than one posted buyer")
    if lead_type == "shared":
        if max_post_buyers <= 1:
            blockers.append("shared lead does not define shared buyer count")
        if consent_scope not in {"shared_group", "named_buyer_group", "tcp_sms_reviewed"}:
            blockers.append("shared lead consent scope does not cover shared routing")
        if buyer_disclosure_status not in {"buyer_group", "named_buyers", "contract_reviewed"}:
            blockers.append("shared lead buyer disclosure is not specific enough")
    if lead_type == "aged":
        if lead_age_minutes <= 0:
            blockers.append("aged lead age is missing")
        if consent_scope != "aged_refresh_reviewed":
            blockers.append("aged lead consent refresh is missing")
    if primary_buyer_cap_remaining <= 0:
        blockers.append("primary buyer cap remaining is zero")
    if cap_last_checked_minutes > 240:
        blockers.append("cap snapshot is older than 240 minutes")
    if avg_ping_latency_ms > 2000:
        blockers.append("average ping latency exceeds 2000 ms")
    if expected_bid_amount <= 0:
        blockers.append("expected bid or payout is missing")
    if buyer_accept_rate_percent < 35:
        blockers.append("buyer accept rate is below 35 percent")
    if qualification_rate_percent < 25:
        blockers.append("qualification rate is below 25 percent")
    if paid_rate_percent < 20:
        blockers.append("paid rate is below 20 percent")
    if no_buyer_rate_percent > 10:
        blockers.append("no-buyer rate exceeds 10 percent")
    if reject_rate_percent > 25:
        blockers.append("reject rate exceeds 25 percent")
    if duplicate_rate_percent > 8:
        blockers.append("duplicate rate exceeds 8 percent")
    if complaint_rate_percent > 1:
        blockers.append("complaint rate exceeds 1 percent")
    if not fields_sent_schema.strip():
        blockers.append("fields sent schema is missing")
    if not routing_rule_summary.strip():
        blockers.append("routing rule summary is missing")
    if not reject_reason_map.strip():
        blockers.append("reject reason map is missing")
    if fallback_status not in {"disabled", "reviewed_same_intent", "approved"}:
        blockers.append("fallback policy is not approved or intentionally disabled")
    if fallback_status != "disabled" and not fallback_policy.strip():
        blockers.append("fallback policy text is missing")
    if buyer_feedback_status in {"missing", "delayed", "accepted_only"}:
        blockers.append("buyer feedback is missing, delayed or accepted-only")
    if not buyer_feedback_plan.strip():
        blockers.append("buyer feedback plan is missing")
    if "complaint" in incident_notes.lower() and complaint_rate_percent > 1:
        blockers.append("open complaint incident requires routing pause review")
    if not consent_version_evidence:
        blockers.append("consent version evidence is missing")
    if not buyer_disclosure_reviewed:
        blockers.append("buyer disclosure review is missing")
    if not field_minimization_reviewed:
        blockers.append("field minimization review is missing")
    if not suppression_dnc_checked:
        blockers.append("suppression and DNC check evidence is missing")
    if not cap_snapshot_evidence:
        blockers.append("cap snapshot evidence is missing")
    if not routing_rule_reviewed:
        blockers.append("routing rule review is missing")
    if not exclusive_shared_terms_reviewed:
        blockers.append("exclusive/shared/aged terms review is missing")
    if fallback_status not in {"disabled"} and not fallback_buyer_reviewed:
        blockers.append("fallback buyer review is missing")
    if not buyer_feedback_ready:
        blockers.append("buyer feedback readiness is missing")
    if not source_policy_reviewed:
        blockers.append("source policy review is missing")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
