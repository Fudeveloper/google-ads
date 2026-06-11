from __future__ import annotations


CONSENT_POINTS = {
    "missing": 0,
    "unknown": 0,
    "invalid": 0,
    "form_only": 6,
    "valid": 14,
    "versioned": 17,
    "buyer_scope_reviewed": 20,
}

DISCLOSURE_POINTS = {
    "missing": 0,
    "generic": 4,
    "category_disclosed": 8,
    "buyer_group": 12,
    "named_buyers": 15,
    "contract_reviewed": 15,
}

CONTACT_POINTS = {
    "unknown": 0,
    "missing": 0,
    "invalid": 0,
    "format_only": 4,
    "normalized": 7,
    "reachable_reviewed": 8,
    "not_collected": 8,
}

GEO_POINTS = {
    "unknown": 0,
    "bad_geo": 0,
    "partial": 4,
    "eligible": 8,
    "buyer_service_area": 10,
}

DUPLICATE_POINTS = {
    "missing": 0,
    "window_missing": 2,
    "hash_only": 8,
    "source_buyer_windowed": 12,
    "event_deduped": 15,
}

CHECK_POINTS = {
    "missing": 0,
    "unknown": 0,
    "blocked": 0,
    "stale": 3,
    "partial": 6,
    "checked": 10,
    "ready": 15,
}

PII_POINTS = {
    "unknown": 0,
    "raw_pii_in_url": 0,
    "over_collected": 1,
    "internal_only": 3,
    "hashed_minimized": 4,
    "post_only_selected_buyer": 5,
    "not_collected": 5,
}

RETENTION_POINTS = {
    "missing": 0,
    "draft": 1,
    "defined": 3,
    "deletion_ready": 4,
    "audited": 5,
}

SOURCE_POLICY_POINTS = {
    "unknown": 0,
    "disallowed": 0,
    "under_review": 4,
    "approved": 8,
    "buyer_approved": 10,
}

FEEDBACK_POINTS = {
    "missing": 0,
    "accepted_only": 3,
    "reject_reason_mapped": 7,
    "paid_feedback_ready": 10,
}


def calculate_lead_validation_review(
    *,
    consent_status: str,
    buyer_disclosure_status: str,
    phone_status: str,
    email_status: str,
    address_geo_status: str,
    duplicate_status: str,
    suppression_status: str,
    dnc_status: str,
    opt_out_status: str,
    pii_minimization_status: str,
    retention_status: str,
    source_policy_status: str,
    buyer_reject_feedback_status: str,
    validation_sample_size: int,
    valid_rate_percent: float,
    invalid_contact_rate_percent: float,
    duplicate_rate_percent: float,
    suppression_hit_rate_percent: float,
    dnc_hit_rate_percent: float,
    opt_out_rate_percent: float,
    bad_geo_rate_percent: float,
    no_consent_rate_percent: float,
    buyer_reject_rate_percent: float,
    complaint_rate_percent: float,
    fields_collected_schema: str,
    validation_rule_summary: str,
    duplicate_rule_summary: str,
    suppression_rule_summary: str,
    pii_handling_notes: str,
    retention_deletion_notes: str,
    buyer_reject_reason_map: str,
    source_form_fix_plan: str,
    incident_notes: str,
    consent_evidence: bool,
    buyer_disclosure_reviewed: bool,
    field_minimization_reviewed: bool,
    duplicate_rule_reviewed: bool,
    suppression_dnc_checked: bool,
    pii_access_reviewed: bool,
    retention_policy_reviewed: bool,
    reject_reason_mapped: bool,
    source_policy_reviewed: bool,
    human_review: bool,
) -> dict[str, object]:
    usable_lead_rate = _usable_lead_rate(
        valid_rate_percent=valid_rate_percent,
        invalid_contact_rate_percent=invalid_contact_rate_percent,
        duplicate_rate_percent=duplicate_rate_percent,
        suppression_hit_rate_percent=suppression_hit_rate_percent,
        dnc_hit_rate_percent=dnc_hit_rate_percent,
        opt_out_rate_percent=opt_out_rate_percent,
        bad_geo_rate_percent=bad_geo_rate_percent,
        no_consent_rate_percent=no_consent_rate_percent,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        complaint_rate_percent=complaint_rate_percent,
    )
    expected_valid_leads = validation_sample_size * _rate(usable_lead_rate)
    safe_routing_rate = _safe_routing_rate(
        usable_lead_rate=usable_lead_rate,
        consent_status=consent_status,
        buyer_disclosure_status=buyer_disclosure_status,
        suppression_status=suppression_status,
        dnc_status=dnc_status,
        opt_out_status=opt_out_status,
        pii_minimization_status=pii_minimization_status,
        source_policy_status=source_policy_status,
    )

    blockers = _blockers(
        consent_status=consent_status,
        buyer_disclosure_status=buyer_disclosure_status,
        phone_status=phone_status,
        email_status=email_status,
        address_geo_status=address_geo_status,
        duplicate_status=duplicate_status,
        suppression_status=suppression_status,
        dnc_status=dnc_status,
        opt_out_status=opt_out_status,
        pii_minimization_status=pii_minimization_status,
        retention_status=retention_status,
        source_policy_status=source_policy_status,
        buyer_reject_feedback_status=buyer_reject_feedback_status,
        validation_sample_size=validation_sample_size,
        valid_rate_percent=valid_rate_percent,
        invalid_contact_rate_percent=invalid_contact_rate_percent,
        duplicate_rate_percent=duplicate_rate_percent,
        suppression_hit_rate_percent=suppression_hit_rate_percent,
        dnc_hit_rate_percent=dnc_hit_rate_percent,
        opt_out_rate_percent=opt_out_rate_percent,
        bad_geo_rate_percent=bad_geo_rate_percent,
        no_consent_rate_percent=no_consent_rate_percent,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        complaint_rate_percent=complaint_rate_percent,
        fields_collected_schema=fields_collected_schema,
        validation_rule_summary=validation_rule_summary,
        duplicate_rule_summary=duplicate_rule_summary,
        suppression_rule_summary=suppression_rule_summary,
        pii_handling_notes=pii_handling_notes,
        retention_deletion_notes=retention_deletion_notes,
        buyer_reject_reason_map=buyer_reject_reason_map,
        source_form_fix_plan=source_form_fix_plan,
        incident_notes=incident_notes,
        consent_evidence=consent_evidence,
        buyer_disclosure_reviewed=buyer_disclosure_reviewed,
        field_minimization_reviewed=field_minimization_reviewed,
        duplicate_rule_reviewed=duplicate_rule_reviewed,
        suppression_dnc_checked=suppression_dnc_checked,
        pii_access_reviewed=pii_access_reviewed,
        retention_policy_reviewed=retention_policy_reviewed,
        reject_reason_mapped=reject_reason_mapped,
        source_policy_reviewed=source_policy_reviewed,
        human_review=human_review,
    )

    components = {
        "consent_integrity": _consent_points(
            consent_status=consent_status,
            buyer_disclosure_status=buyer_disclosure_status,
            consent_evidence=consent_evidence,
            buyer_disclosure_reviewed=buyer_disclosure_reviewed,
            no_consent_rate_percent=no_consent_rate_percent,
        ),
        "contact_format_quality": _contact_points(
            phone_status=phone_status,
            email_status=email_status,
            invalid_contact_rate_percent=invalid_contact_rate_percent,
        ),
        "duplicate_safety": _duplicate_points(
            duplicate_status=duplicate_status,
            duplicate_rate_percent=duplicate_rate_percent,
            duplicate_rule_reviewed=duplicate_rule_reviewed,
            duplicate_rule_summary=duplicate_rule_summary,
        ),
        "suppression_clearance": _suppression_points(
            suppression_status=suppression_status,
            dnc_status=dnc_status,
            opt_out_status=opt_out_status,
            suppression_hit_rate_percent=suppression_hit_rate_percent,
            dnc_hit_rate_percent=dnc_hit_rate_percent,
            opt_out_rate_percent=opt_out_rate_percent,
            suppression_dnc_checked=suppression_dnc_checked,
        ),
        "geo_offer_fit": _geo_points(
            address_geo_status=address_geo_status,
            bad_geo_rate_percent=bad_geo_rate_percent,
        ),
        "source_policy_fit": _source_policy_points(
            source_policy_status=source_policy_status,
            source_policy_reviewed=source_policy_reviewed,
        ),
        "buyer_feedback_quality": _buyer_feedback_points(
            buyer_reject_feedback_status=buyer_reject_feedback_status,
            buyer_reject_rate_percent=buyer_reject_rate_percent,
            buyer_reject_reason_map=buyer_reject_reason_map,
            reject_reason_mapped=reject_reason_mapped,
        ),
        "pii_minimization_retention": _pii_retention_points(
            pii_minimization_status=pii_minimization_status,
            retention_status=retention_status,
            field_minimization_reviewed=field_minimization_reviewed,
            pii_access_reviewed=pii_access_reviewed,
            retention_policy_reviewed=retention_policy_reviewed,
        ),
    }
    score = max(min(sum(components.values()), 100), 0)

    return {
        "score_components": components,
        "score": score,
        "risk_level": _risk_level(
            score=score,
            blockers=blockers,
            consent_status=consent_status,
            buyer_disclosure_status=buyer_disclosure_status,
            suppression_status=suppression_status,
            dnc_status=dnc_status,
            opt_out_status=opt_out_status,
            pii_minimization_status=pii_minimization_status,
            source_policy_status=source_policy_status,
            complaint_rate_percent=complaint_rate_percent,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            consent_status=consent_status,
            buyer_disclosure_status=buyer_disclosure_status,
            phone_status=phone_status,
            email_status=email_status,
            address_geo_status=address_geo_status,
            duplicate_status=duplicate_status,
            suppression_status=suppression_status,
            dnc_status=dnc_status,
            opt_out_status=opt_out_status,
            pii_minimization_status=pii_minimization_status,
            retention_status=retention_status,
            source_policy_status=source_policy_status,
            buyer_reject_feedback_status=buyer_reject_feedback_status,
            invalid_contact_rate_percent=invalid_contact_rate_percent,
            duplicate_rate_percent=duplicate_rate_percent,
            bad_geo_rate_percent=bad_geo_rate_percent,
            buyer_reject_rate_percent=buyer_reject_rate_percent,
        ),
        "usable_lead_rate_percent": round(usable_lead_rate, 2),
        "expected_valid_leads": round(expected_valid_leads, 2),
        "safe_routing_rate_percent": round(safe_routing_rate, 2),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _usable_lead_rate(
    *,
    valid_rate_percent: float,
    invalid_contact_rate_percent: float,
    duplicate_rate_percent: float,
    suppression_hit_rate_percent: float,
    dnc_hit_rate_percent: float,
    opt_out_rate_percent: float,
    bad_geo_rate_percent: float,
    no_consent_rate_percent: float,
    buyer_reject_rate_percent: float,
    complaint_rate_percent: float,
) -> float:
    usable = _rate(valid_rate_percent)
    for rate in [
        invalid_contact_rate_percent,
        duplicate_rate_percent,
        suppression_hit_rate_percent,
        dnc_hit_rate_percent,
        opt_out_rate_percent,
        bad_geo_rate_percent,
        no_consent_rate_percent,
        buyer_reject_rate_percent,
        complaint_rate_percent,
    ]:
        usable *= max(1 - _rate(rate), 0)
    return usable * 100


def _safe_routing_rate(
    *,
    usable_lead_rate: float,
    consent_status: str,
    buyer_disclosure_status: str,
    suppression_status: str,
    dnc_status: str,
    opt_out_status: str,
    pii_minimization_status: str,
    source_policy_status: str,
) -> float:
    hard_block = (
        consent_status in {"missing", "unknown", "invalid"}
        or buyer_disclosure_status == "missing"
        or suppression_status == "blocked"
        or dnc_status == "blocked"
        or opt_out_status == "blocked"
        or pii_minimization_status == "raw_pii_in_url"
        or source_policy_status == "disallowed"
    )
    if hard_block:
        return 0
    if suppression_status in {"missing", "unknown"} or dnc_status in {"missing", "unknown"}:
        return usable_lead_rate * 0.5
    return usable_lead_rate


def _consent_points(
    *,
    consent_status: str,
    buyer_disclosure_status: str,
    consent_evidence: bool,
    buyer_disclosure_reviewed: bool,
    no_consent_rate_percent: float,
) -> int:
    points = int(
        round(
            CONSENT_POINTS.get(consent_status, 0) * 0.7
            + DISCLOSURE_POINTS.get(buyer_disclosure_status, 0) * 0.3
        )
    )
    points += 1 if consent_evidence else 0
    points += 1 if buyer_disclosure_reviewed else 0
    if no_consent_rate_percent > 3:
        points -= 3
    return max(min(points, 20), 0)


def _contact_points(
    *,
    phone_status: str,
    email_status: str,
    invalid_contact_rate_percent: float,
) -> int:
    points = int(
        round(
            CONTACT_POINTS.get(phone_status, 0) * 0.55
            + CONTACT_POINTS.get(email_status, 0) * 0.45
        )
    )
    if invalid_contact_rate_percent <= 5:
        points += 5
    elif invalid_contact_rate_percent <= 10:
        points += 3
    elif invalid_contact_rate_percent <= 18:
        points += 1
    return max(min(points, 15), 0)


def _duplicate_points(
    *,
    duplicate_status: str,
    duplicate_rate_percent: float,
    duplicate_rule_reviewed: bool,
    duplicate_rule_summary: str,
) -> int:
    points = DUPLICATE_POINTS.get(duplicate_status, 0)
    if duplicate_rate_percent <= 3:
        points += 2
    elif duplicate_rate_percent <= 8:
        points += 1
    if duplicate_rule_reviewed:
        points += 1
    if duplicate_rule_summary.strip():
        points += 1
    return max(min(points, 15), 0)


def _suppression_points(
    *,
    suppression_status: str,
    dnc_status: str,
    opt_out_status: str,
    suppression_hit_rate_percent: float,
    dnc_hit_rate_percent: float,
    opt_out_rate_percent: float,
    suppression_dnc_checked: bool,
) -> int:
    points = int(
        round(
            CHECK_POINTS.get(suppression_status, 0) * 0.35
            + CHECK_POINTS.get(dnc_status, 0) * 0.35
            + CHECK_POINTS.get(opt_out_status, 0) * 0.3
        )
    )
    if suppression_hit_rate_percent <= 2 and dnc_hit_rate_percent <= 1 and opt_out_rate_percent <= 1:
        points += 2
    if suppression_dnc_checked:
        points += 1
    return max(min(points, 15), 0)


def _geo_points(*, address_geo_status: str, bad_geo_rate_percent: float) -> int:
    points = GEO_POINTS.get(address_geo_status, 0)
    if bad_geo_rate_percent <= 3:
        points += 2
    elif bad_geo_rate_percent <= 8:
        points += 1
    return max(min(points, 10), 0)


def _source_policy_points(*, source_policy_status: str, source_policy_reviewed: bool) -> int:
    points = SOURCE_POLICY_POINTS.get(source_policy_status, 0)
    if source_policy_reviewed:
        points += 1
    return max(min(points, 10), 0)


def _buyer_feedback_points(
    *,
    buyer_reject_feedback_status: str,
    buyer_reject_rate_percent: float,
    buyer_reject_reason_map: str,
    reject_reason_mapped: bool,
) -> int:
    points = FEEDBACK_POINTS.get(buyer_reject_feedback_status, 0)
    if buyer_reject_rate_percent <= 10:
        points += 1
    if buyer_reject_reason_map.strip():
        points += 1
    if reject_reason_mapped:
        points += 1
    return max(min(points, 10), 0)


def _pii_retention_points(
    *,
    pii_minimization_status: str,
    retention_status: str,
    field_minimization_reviewed: bool,
    pii_access_reviewed: bool,
    retention_policy_reviewed: bool,
) -> int:
    points = int(
        round(
            PII_POINTS.get(pii_minimization_status, 0) * 0.6
            + RETENTION_POINTS.get(retention_status, 0) * 0.4
        )
    )
    if field_minimization_reviewed and pii_access_reviewed and retention_policy_reviewed:
        points += 1
    return max(min(points, 5), 0)


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    consent_status: str,
    buyer_disclosure_status: str,
    suppression_status: str,
    dnc_status: str,
    opt_out_status: str,
    pii_minimization_status: str,
    source_policy_status: str,
    complaint_rate_percent: float,
) -> str:
    if consent_status in {"missing", "unknown", "invalid"}:
        return "critical"
    if buyer_disclosure_status == "missing":
        return "critical"
    if suppression_status == "blocked" or dnc_status == "blocked" or opt_out_status == "blocked":
        return "critical"
    if pii_minimization_status == "raw_pii_in_url":
        return "critical"
    if source_policy_status == "disallowed":
        return "critical"
    if complaint_rate_percent > 1:
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
    consent_status: str,
    buyer_disclosure_status: str,
    phone_status: str,
    email_status: str,
    address_geo_status: str,
    duplicate_status: str,
    suppression_status: str,
    dnc_status: str,
    opt_out_status: str,
    pii_minimization_status: str,
    retention_status: str,
    source_policy_status: str,
    buyer_reject_feedback_status: str,
    invalid_contact_rate_percent: float,
    duplicate_rate_percent: float,
    bad_geo_rate_percent: float,
    buyer_reject_rate_percent: float,
) -> str:
    if consent_status in {"missing", "unknown", "invalid"} or buyer_disclosure_status == "missing":
        return "block_pii_or_consent"
    if pii_minimization_status in {"raw_pii_in_url", "over_collected", "unknown"}:
        return "block_pii_or_consent"
    if suppression_status in {"missing", "unknown", "blocked"} or dnc_status in {"missing", "unknown", "blocked"} or opt_out_status in {"missing", "unknown", "blocked"}:
        return "block_suppression_dnc"
    if phone_status in {"unknown", "missing", "invalid"} or email_status in {"unknown", "missing", "invalid"} or invalid_contact_rate_percent > 12:
        return "fix_contact_validation"
    if duplicate_status in {"missing", "window_missing"} or duplicate_rate_percent > 8:
        return "fix_duplicate_rules"
    if address_geo_status in {"unknown", "bad_geo"} or bad_geo_rate_percent > 8:
        return "fix_geo_offer_fit"
    if source_policy_status in {"unknown", "under_review", "disallowed"}:
        return "fix_source_policy"
    if buyer_reject_feedback_status in {"missing", "accepted_only"} or buyer_reject_rate_percent > 20:
        return "map_reject_reasons"
    if retention_status in {"missing", "draft"}:
        return "retention_review"
    if score >= 85 and not blockers:
        return "validation_ready"
    if score >= 70:
        return "manual_review"
    if blockers:
        return "validation_review"
    return "blocked"


def _blockers(
    *,
    consent_status: str,
    buyer_disclosure_status: str,
    phone_status: str,
    email_status: str,
    address_geo_status: str,
    duplicate_status: str,
    suppression_status: str,
    dnc_status: str,
    opt_out_status: str,
    pii_minimization_status: str,
    retention_status: str,
    source_policy_status: str,
    buyer_reject_feedback_status: str,
    validation_sample_size: int,
    valid_rate_percent: float,
    invalid_contact_rate_percent: float,
    duplicate_rate_percent: float,
    suppression_hit_rate_percent: float,
    dnc_hit_rate_percent: float,
    opt_out_rate_percent: float,
    bad_geo_rate_percent: float,
    no_consent_rate_percent: float,
    buyer_reject_rate_percent: float,
    complaint_rate_percent: float,
    fields_collected_schema: str,
    validation_rule_summary: str,
    duplicate_rule_summary: str,
    suppression_rule_summary: str,
    pii_handling_notes: str,
    retention_deletion_notes: str,
    buyer_reject_reason_map: str,
    source_form_fix_plan: str,
    incident_notes: str,
    consent_evidence: bool,
    buyer_disclosure_reviewed: bool,
    field_minimization_reviewed: bool,
    duplicate_rule_reviewed: bool,
    suppression_dnc_checked: bool,
    pii_access_reviewed: bool,
    retention_policy_reviewed: bool,
    reject_reason_mapped: bool,
    source_policy_reviewed: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if validation_sample_size <= 0:
        blockers.append("validation sample size is missing")
    if consent_status in {"missing", "unknown", "invalid"}:
        blockers.append("consent status is missing, unknown or invalid")
    if buyer_disclosure_status == "missing":
        blockers.append("buyer disclosure is missing")
    if phone_status in {"unknown", "missing", "invalid"}:
        blockers.append("phone validation is unknown, missing or invalid")
    if email_status in {"unknown", "missing", "invalid"}:
        blockers.append("email validation is unknown, missing or invalid")
    if address_geo_status in {"unknown", "bad_geo"}:
        blockers.append("address or geo eligibility is unknown or bad geo")
    if duplicate_status in {"missing", "window_missing"}:
        blockers.append("duplicate rule window is missing")
    if suppression_status in {"missing", "unknown", "blocked"}:
        blockers.append("suppression status is missing, unknown or blocked")
    if dnc_status in {"missing", "unknown", "blocked"}:
        blockers.append("DNC status is missing, unknown or blocked")
    if opt_out_status in {"missing", "unknown", "blocked"}:
        blockers.append("opt-out status is missing, unknown or blocked")
    if pii_minimization_status in {"unknown", "raw_pii_in_url", "over_collected"}:
        blockers.append("PII minimization is unknown or unsafe")
    if retention_status in {"missing", "draft"}:
        blockers.append("retention or deletion policy is missing or draft")
    if source_policy_status in {"unknown", "disallowed"}:
        blockers.append("source policy status is unknown or disallowed")
    if buyer_reject_feedback_status in {"missing", "accepted_only"}:
        blockers.append("buyer reject feedback is missing or accepted-only")
    if valid_rate_percent < 45:
        blockers.append("valid rate is below 45 percent")
    if invalid_contact_rate_percent > 12:
        blockers.append("invalid contact rate exceeds 12 percent")
    if duplicate_rate_percent > 8:
        blockers.append("duplicate rate exceeds 8 percent")
    if suppression_hit_rate_percent > 4:
        blockers.append("suppression hit rate exceeds 4 percent")
    if dnc_hit_rate_percent > 2:
        blockers.append("DNC hit rate exceeds 2 percent")
    if opt_out_rate_percent > 2:
        blockers.append("opt-out rate exceeds 2 percent")
    if bad_geo_rate_percent > 8:
        blockers.append("bad geo rate exceeds 8 percent")
    if no_consent_rate_percent > 3:
        blockers.append("no-consent rate exceeds 3 percent")
    if buyer_reject_rate_percent > 20:
        blockers.append("buyer reject rate exceeds 20 percent")
    if complaint_rate_percent > 1:
        blockers.append("complaint rate exceeds 1 percent")
    if not fields_collected_schema.strip():
        blockers.append("fields collected schema is missing")
    if not validation_rule_summary.strip():
        blockers.append("validation rule summary is missing")
    if not duplicate_rule_summary.strip():
        blockers.append("duplicate rule summary is missing")
    if not suppression_rule_summary.strip():
        blockers.append("suppression rule summary is missing")
    if not pii_handling_notes.strip():
        blockers.append("PII handling notes are missing")
    if not retention_deletion_notes.strip():
        blockers.append("retention and deletion notes are missing")
    if not buyer_reject_reason_map.strip():
        blockers.append("buyer reject reason map is missing")
    if not source_form_fix_plan.strip():
        blockers.append("source form fix plan is missing")
    if "complaint" in incident_notes.lower() and complaint_rate_percent > 1:
        blockers.append("open complaint incident requires routing pause review")
    if not consent_evidence:
        blockers.append("consent evidence is missing")
    if not buyer_disclosure_reviewed:
        blockers.append("buyer disclosure review is missing")
    if not field_minimization_reviewed:
        blockers.append("field minimization review is missing")
    if not duplicate_rule_reviewed:
        blockers.append("duplicate rule review is missing")
    if not suppression_dnc_checked:
        blockers.append("suppression, DNC and opt-out check evidence is missing")
    if not pii_access_reviewed:
        blockers.append("PII access review is missing")
    if not retention_policy_reviewed:
        blockers.append("retention policy review is missing")
    if not reject_reason_mapped:
        blockers.append("reject reason map review is missing")
    if not source_policy_reviewed:
        blockers.append("source policy review is missing")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
