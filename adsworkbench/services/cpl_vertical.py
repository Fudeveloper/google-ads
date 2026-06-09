from __future__ import annotations


VERTICAL_POINTS = {
    "insurance": 8,
    "loan_debt": 5,
    "legal": 5,
    "home_services": 8,
    "education": 6,
    "healthcare": 4,
    "b2b_saas": 10,
    "crypto_investment": 2,
    "employment": 5,
    "gambling": 2,
    "addiction_treatment": 2,
    "government_services": 3,
    "other": 4,
}

BUYER_TERMS_POINTS = {
    "missing": 0,
    "draft": 2,
    "received": 5,
    "approved": 10,
}

CONSENT_STATUS_POINTS = {
    "missing": 0,
    "generic": 3,
    "buyer_named": 8,
    "channel_specific": 10,
}

RISK_POINTS = {
    "low": 10,
    "medium": 5,
    "high": 0,
}


def calculate_cpl_vertical_review(
    *,
    vertical: str,
    payout_amount: float,
    estimated_cpc: float,
    landing_cvr_percent: float,
    accepted_rate_percent: float,
    qualified_rate_percent: float,
    paid_rate_percent: float,
    deduction_rate_percent: float,
    chargeback_rate_percent: float,
    feedback_lag_days: int,
    contact_sla_minutes: int,
    required_fields_mapped: bool,
    reject_reason_map_ready: bool,
    accepted_definition_clear: bool,
    paid_definition_clear: bool,
    consent_disclosure_status: str,
    pii_minimization: bool,
    license_required: bool,
    license_evidence_present: bool,
    buyer_terms_status: str,
    source_quality: str,
    policy_risk: str,
    data_sensitivity: str,
    human_review: bool,
) -> dict[str, object]:
    accepted_rate = _rate(accepted_rate_percent)
    qualified_rate = _rate(qualified_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    deduction_rate = _rate(deduction_rate_percent)
    chargeback_rate = _rate(chargeback_rate_percent)
    landing_cvr = _rate(landing_cvr_percent)
    retained_rate = max(1 - deduction_rate - chargeback_rate, 0)

    effective_payout = (
        payout_amount * accepted_rate * qualified_rate * paid_rate * retained_rate
    )
    expected_value_per_click = effective_payout * landing_cvr
    safe_cpc = expected_value_per_click * 0.65
    cpc_margin_percent = _margin_percent(safe_cpc, estimated_cpc)

    blockers = _blockers(
        vertical=vertical,
        payout_amount=payout_amount,
        estimated_cpc=estimated_cpc,
        landing_cvr_percent=landing_cvr_percent,
        accepted_rate_percent=accepted_rate_percent,
        qualified_rate_percent=qualified_rate_percent,
        paid_rate_percent=paid_rate_percent,
        deduction_rate_percent=deduction_rate_percent,
        chargeback_rate_percent=chargeback_rate_percent,
        feedback_lag_days=feedback_lag_days,
        contact_sla_minutes=contact_sla_minutes,
        required_fields_mapped=required_fields_mapped,
        reject_reason_map_ready=reject_reason_map_ready,
        accepted_definition_clear=accepted_definition_clear,
        paid_definition_clear=paid_definition_clear,
        consent_disclosure_status=consent_disclosure_status,
        pii_minimization=pii_minimization,
        license_required=license_required,
        license_evidence_present=license_evidence_present,
        buyer_terms_status=buyer_terms_status,
        source_quality=source_quality,
        policy_risk=policy_risk,
        data_sensitivity=data_sensitivity,
        safe_cpc=safe_cpc,
        human_review=human_review,
    )

    score = 0
    score += VERTICAL_POINTS.get(vertical, 0)
    score += _economics_points(
        effective_payout=effective_payout,
        expected_value_per_click=expected_value_per_click,
        safe_cpc=safe_cpc,
        estimated_cpc=estimated_cpc,
    )
    score += _quality_points(
        accepted_rate_percent=accepted_rate_percent,
        qualified_rate_percent=qualified_rate_percent,
        paid_rate_percent=paid_rate_percent,
        deduction_rate_percent=deduction_rate_percent,
        chargeback_rate_percent=chargeback_rate_percent,
    )
    score += _feedback_points(feedback_lag_days, contact_sla_minutes)
    score += 6 if required_fields_mapped else 0
    score += 6 if reject_reason_map_ready else 0
    score += 5 if accepted_definition_clear else 0
    score += 5 if paid_definition_clear else 0
    score += CONSENT_STATUS_POINTS.get(consent_disclosure_status, 0)
    score += 5 if pii_minimization else 0
    score += 6 if (not license_required or license_evidence_present) else 0
    score += BUYER_TERMS_POINTS.get(buyer_terms_status, 0)
    score += RISK_POINTS.get(source_quality, 0)
    score += RISK_POINTS.get(policy_risk, 0)
    score += RISK_POINTS.get(data_sensitivity, 0)
    score += 5 if human_review else 0
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(score, blockers, policy_risk, data_sensitivity),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            policy_risk=policy_risk,
            buyer_terms_status=buyer_terms_status,
            safe_cpc=safe_cpc,
            estimated_cpc=estimated_cpc,
        ),
        "effective_payout": round(effective_payout, 4),
        "expected_value_per_click": round(expected_value_per_click, 4),
        "safe_cpc": round(safe_cpc, 4),
        "cpc_margin_percent": round(cpc_margin_percent, 2),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _margin_percent(safe_cpc: float, estimated_cpc: float) -> float:
    if estimated_cpc <= 0:
        return 0
    return (safe_cpc - estimated_cpc) / estimated_cpc * 100


def _economics_points(
    *,
    effective_payout: float,
    expected_value_per_click: float,
    safe_cpc: float,
    estimated_cpc: float,
) -> int:
    if effective_payout <= 0 or expected_value_per_click <= 0:
        return 0
    if estimated_cpc <= 0:
        return 6
    if safe_cpc >= estimated_cpc * 1.4:
        return 18
    if safe_cpc >= estimated_cpc:
        return 12
    if safe_cpc >= estimated_cpc * 0.75:
        return 6
    return 2


def _quality_points(
    *,
    accepted_rate_percent: float,
    qualified_rate_percent: float,
    paid_rate_percent: float,
    deduction_rate_percent: float,
    chargeback_rate_percent: float,
) -> int:
    if (
        accepted_rate_percent >= 75
        and qualified_rate_percent >= 65
        and paid_rate_percent >= 55
        and deduction_rate_percent <= 10
        and chargeback_rate_percent <= 5
    ):
        return 18
    if (
        accepted_rate_percent >= 55
        and qualified_rate_percent >= 45
        and paid_rate_percent >= 35
        and deduction_rate_percent <= 20
        and chargeback_rate_percent <= 10
    ):
        return 10
    if accepted_rate_percent > 0 and qualified_rate_percent > 0:
        return 4
    return 0


def _feedback_points(feedback_lag_days: int, contact_sla_minutes: int) -> int:
    points = 0
    if feedback_lag_days <= 3:
        points += 8
    elif feedback_lag_days <= 14:
        points += 4
    if contact_sla_minutes <= 5:
        points += 7
    elif contact_sla_minutes <= 30:
        points += 4
    return points


def _risk_level(
    score: int,
    blockers: list[str],
    policy_risk: str,
    data_sensitivity: str,
) -> str:
    if policy_risk == "high" or data_sensitivity == "high":
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
    policy_risk: str,
    buyer_terms_status: str,
    safe_cpc: float,
    estimated_cpc: float,
) -> str:
    if policy_risk == "high":
        return "policy_review_first"
    if buyer_terms_status in {"missing", "draft"}:
        return "hold_for_buyer_terms"
    if safe_cpc <= 0 or (estimated_cpc > 0 and safe_cpc < estimated_cpc):
        return "rework_economics_or_qualification"
    if blockers:
        return "tighten_qualification"
    if score >= 85:
        return "approve_manual_test"
    if score >= 70:
        return "small_test_only"
    return "hold_for_vertical_rework"


def _blockers(
    *,
    vertical: str,
    payout_amount: float,
    estimated_cpc: float,
    landing_cvr_percent: float,
    accepted_rate_percent: float,
    qualified_rate_percent: float,
    paid_rate_percent: float,
    deduction_rate_percent: float,
    chargeback_rate_percent: float,
    feedback_lag_days: int,
    contact_sla_minutes: int,
    required_fields_mapped: bool,
    reject_reason_map_ready: bool,
    accepted_definition_clear: bool,
    paid_definition_clear: bool,
    consent_disclosure_status: str,
    pii_minimization: bool,
    license_required: bool,
    license_evidence_present: bool,
    buyer_terms_status: str,
    source_quality: str,
    policy_risk: str,
    data_sensitivity: str,
    safe_cpc: float,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if vertical not in VERTICAL_POINTS:
        blockers.append("vertical is not mapped")
    if payout_amount <= 0:
        blockers.append("payout amount is missing")
    if estimated_cpc > 0 and safe_cpc < estimated_cpc:
        blockers.append("safe CPC is below estimated CPC")
    if landing_cvr_percent <= 0:
        blockers.append("landing CVR evidence is missing")
    if accepted_rate_percent < 55:
        blockers.append("accepted rate is below 55 percent")
    if qualified_rate_percent < 45:
        blockers.append("qualified rate is below 45 percent")
    if paid_rate_percent < 35:
        blockers.append("paid rate is below 35 percent")
    if deduction_rate_percent > 20:
        blockers.append("deduction or scrub rate exceeds 20 percent")
    if chargeback_rate_percent > 10:
        blockers.append("chargeback or refund rate exceeds 10 percent")
    if feedback_lag_days > 14:
        blockers.append("buyer feedback lag is longer than 14 days")
    if contact_sla_minutes > 30:
        blockers.append("contact SLA is slower than 30 minutes")
    if not required_fields_mapped:
        blockers.append("qualification fields are not mapped to reject reasons")
    if not reject_reason_map_ready:
        blockers.append("reject reason map is missing")
    if not accepted_definition_clear:
        blockers.append("accepted definition is not clear")
    if not paid_definition_clear:
        blockers.append("paid definition is not clear")
    if consent_disclosure_status in {"missing", "generic"}:
        blockers.append("consent or buyer disclosure is not specific enough")
    if not pii_minimization:
        blockers.append("PII minimization review is missing")
    if license_required and not license_evidence_present:
        blockers.append("license or certification evidence is missing")
    if buyer_terms_status in {"missing", "draft"}:
        blockers.append("buyer terms are not approved")
    if source_quality != "low" and source_quality not in RISK_POINTS:
        blockers.append("source quality is not mapped")
    if source_quality == "high":
        blockers.append("source quality risk is high")
    if policy_risk == "high":
        blockers.append("high policy risk blocks CPL scaling")
    elif policy_risk == "medium":
        blockers.append("medium policy risk requires tighter review")
    if data_sensitivity == "high":
        blockers.append("high data sensitivity requires privacy review")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
