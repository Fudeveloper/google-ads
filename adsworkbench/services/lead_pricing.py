from __future__ import annotations


PAYOUT_MODEL_POINTS = {
    "raw_cpl": 6,
    "validated_cpl": 8,
    "qualified_cpl": 10,
    "pay_per_call": 7,
    "appointment": 7,
    "cpa": 6,
    "revshare": 5,
    "hybrid": 7,
}

QUALITY_EVIDENCE_POINTS = {
    "missing": 0,
    "anecdotal": 2,
    "last_7_days": 4,
    "cohort_30_days": 8,
    "paid_cohort": 10,
}

SOURCE_TRANSPARENCY_POINTS = {
    "opaque": 0,
    "partial": 4,
    "source_subid": 8,
    "buyer_approved": 10,
}

CONSENT_EVIDENCE_POINTS = {
    "missing": 0,
    "generic": 3,
    "buyer_named": 8,
    "channel_specific": 10,
}

BUYER_TERMS_POINTS = {
    "missing": 0,
    "draft": 2,
    "received": 5,
    "approved": 10,
}


def calculate_lead_pricing_review(
    *,
    payout_model: str,
    headline_payout: float,
    unit_payout: float,
    proposed_payout: float,
    minimum_acceptable_payout: float,
    estimated_cpc: float,
    click_to_lead_rate_percent: float,
    accepted_rate_percent: float,
    qualified_rate_percent: float,
    approval_rate_percent: float,
    paid_rate_percent: float,
    return_rate_percent: float,
    scrub_buffer_percent: float,
    chargeback_rate_percent: float,
    variable_cost_per_click: float,
    tracking_cost_per_click: float,
    content_cost_per_click: float,
    cashflow_cost_percent: float,
    cap_limit: float,
    expected_volume: float,
    return_window_days: int,
    payment_term_days: int,
    quality_evidence_status: str,
    source_transparency: str,
    consent_evidence: str,
    reject_reason_map_ready: bool,
    invoice_evidence: bool,
    dispute_reserve_present: bool,
    buyer_terms_status: str,
    human_review: bool,
) -> dict[str, object]:
    payout_for_model = unit_payout if unit_payout > 0 else proposed_payout
    accepted_rate = _rate(accepted_rate_percent)
    qualified_rate = _rate(qualified_rate_percent)
    approval_rate = _rate(approval_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    return_rate = _rate(return_rate_percent)
    scrub_buffer = _rate(scrub_buffer_percent)
    chargeback_rate = _rate(chargeback_rate_percent)
    click_to_lead_rate = _rate(click_to_lead_rate_percent)
    cashflow_cost_rate = _rate(cashflow_cost_percent)
    retained_rate = max(1 - return_rate - scrub_buffer - chargeback_rate, 0)

    effective_payout = (
        payout_for_model
        * accepted_rate
        * qualified_rate
        * approval_rate
        * paid_rate
        * retained_rate
    )
    paid_epc = click_to_lead_rate * effective_payout
    operating_cost_per_click = (
        variable_cost_per_click + tracking_cost_per_click + content_cost_per_click
    )
    cashflow_cost_per_click = paid_epc * cashflow_cost_rate
    safe_cpc = paid_epc * 0.70 - operating_cost_per_click - cashflow_cost_per_click
    margin_per_click = safe_cpc - estimated_cpc
    reserve_amount = payout_for_model * (return_rate + scrub_buffer + chargeback_rate)

    blockers = _blockers(
        payout_model=payout_model,
        headline_payout=headline_payout,
        unit_payout=unit_payout,
        proposed_payout=proposed_payout,
        minimum_acceptable_payout=minimum_acceptable_payout,
        estimated_cpc=estimated_cpc,
        click_to_lead_rate_percent=click_to_lead_rate_percent,
        accepted_rate_percent=accepted_rate_percent,
        qualified_rate_percent=qualified_rate_percent,
        approval_rate_percent=approval_rate_percent,
        paid_rate_percent=paid_rate_percent,
        return_rate_percent=return_rate_percent,
        scrub_buffer_percent=scrub_buffer_percent,
        chargeback_rate_percent=chargeback_rate_percent,
        safe_cpc=safe_cpc,
        cap_limit=cap_limit,
        expected_volume=expected_volume,
        return_window_days=return_window_days,
        payment_term_days=payment_term_days,
        quality_evidence_status=quality_evidence_status,
        source_transparency=source_transparency,
        consent_evidence=consent_evidence,
        reject_reason_map_ready=reject_reason_map_ready,
        invoice_evidence=invoice_evidence,
        dispute_reserve_present=dispute_reserve_present,
        buyer_terms_status=buyer_terms_status,
        human_review=human_review,
    )

    score = 0
    score += PAYOUT_MODEL_POINTS.get(payout_model, 0)
    score += _economics_points(
        payout_for_model=payout_for_model,
        minimum_acceptable_payout=minimum_acceptable_payout,
        paid_epc=paid_epc,
        safe_cpc=safe_cpc,
        estimated_cpc=estimated_cpc,
    )
    score += _quality_points(
        accepted_rate_percent=accepted_rate_percent,
        qualified_rate_percent=qualified_rate_percent,
        approval_rate_percent=approval_rate_percent,
        paid_rate_percent=paid_rate_percent,
        return_rate_percent=return_rate_percent,
        scrub_buffer_percent=scrub_buffer_percent,
        chargeback_rate_percent=chargeback_rate_percent,
    )
    score += _window_points(return_window_days, payment_term_days)
    score += _cap_points(cap_limit, expected_volume)
    score += QUALITY_EVIDENCE_POINTS.get(quality_evidence_status, 0)
    score += SOURCE_TRANSPARENCY_POINTS.get(source_transparency, 0)
    score += CONSENT_EVIDENCE_POINTS.get(consent_evidence, 0)
    score += 6 if reject_reason_map_ready else 0
    score += 5 if invoice_evidence else 0
    score += 5 if dispute_reserve_present else 0
    score += BUYER_TERMS_POINTS.get(buyer_terms_status, 0)
    score += 5 if human_review else 0
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(
            score=score,
            blockers=blockers,
            source_transparency=source_transparency,
            buyer_terms_status=buyer_terms_status,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            safe_cpc=safe_cpc,
            estimated_cpc=estimated_cpc,
            source_transparency=source_transparency,
            buyer_terms_status=buyer_terms_status,
            return_window_days=return_window_days,
            payment_term_days=payment_term_days,
            quality_evidence_status=quality_evidence_status,
        ),
        "effective_payout": round(effective_payout, 4),
        "paid_epc": round(paid_epc, 4),
        "safe_cpc": round(safe_cpc, 4),
        "margin_per_click": round(margin_per_click, 4),
        "reserve_amount": round(reserve_amount, 4),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _economics_points(
    *,
    payout_for_model: float,
    minimum_acceptable_payout: float,
    paid_epc: float,
    safe_cpc: float,
    estimated_cpc: float,
) -> int:
    if payout_for_model <= 0 or paid_epc <= 0:
        return 0
    points = 0
    if minimum_acceptable_payout <= 0 or payout_for_model >= minimum_acceptable_payout:
        points += 6
    if estimated_cpc <= 0:
        points += 4
    elif safe_cpc >= estimated_cpc * 1.4:
        points += 14
    elif safe_cpc >= estimated_cpc:
        points += 10
    elif safe_cpc >= estimated_cpc * 0.75:
        points += 5
    return points


def _quality_points(
    *,
    accepted_rate_percent: float,
    qualified_rate_percent: float,
    approval_rate_percent: float,
    paid_rate_percent: float,
    return_rate_percent: float,
    scrub_buffer_percent: float,
    chargeback_rate_percent: float,
) -> int:
    if (
        accepted_rate_percent >= 80
        and qualified_rate_percent >= 65
        and approval_rate_percent >= 75
        and paid_rate_percent >= 70
        and return_rate_percent <= 10
        and scrub_buffer_percent <= 10
        and chargeback_rate_percent <= 5
    ):
        return 18
    if (
        accepted_rate_percent >= 60
        and qualified_rate_percent >= 45
        and approval_rate_percent >= 55
        and paid_rate_percent >= 50
        and return_rate_percent <= 20
        and scrub_buffer_percent <= 20
        and chargeback_rate_percent <= 10
    ):
        return 10
    if accepted_rate_percent > 0 and qualified_rate_percent > 0:
        return 4
    return 0


def _window_points(return_window_days: int, payment_term_days: int) -> int:
    points = 0
    if return_window_days <= 7:
        points += 6
    elif return_window_days <= 30:
        points += 3
    if payment_term_days <= 15:
        points += 6
    elif payment_term_days <= 45:
        points += 3
    return points


def _cap_points(cap_limit: float, expected_volume: float) -> int:
    if cap_limit <= 0:
        return 0
    if expected_volume <= cap_limit * 0.70:
        return 8
    if expected_volume <= cap_limit:
        return 4
    return 0


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    source_transparency: str,
    buyer_terms_status: str,
) -> str:
    if source_transparency == "opaque" or buyer_terms_status in {"missing", "draft"}:
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
    safe_cpc: float,
    estimated_cpc: float,
    source_transparency: str,
    buyer_terms_status: str,
    return_window_days: int,
    payment_term_days: int,
    quality_evidence_status: str,
) -> str:
    if source_transparency == "opaque":
        return "hold_for_source_transparency"
    if buyer_terms_status in {"missing", "draft"}:
        return "hold_for_rate_card"
    if quality_evidence_status in {"missing", "anecdotal"}:
        return "collect_paid_evidence"
    if safe_cpc <= 0 or (estimated_cpc > 0 and safe_cpc < estimated_cpc):
        return "rework_price_or_cost"
    if return_window_days > 30 or payment_term_days > 45:
        return "add_scrub_reserve"
    if blockers:
        return "negotiation_evidence_required"
    if score >= 85:
        return "approve_manual_test"
    if score >= 70:
        return "small_test_only"
    return "hold_for_rate_card"


def _blockers(
    *,
    payout_model: str,
    headline_payout: float,
    unit_payout: float,
    proposed_payout: float,
    minimum_acceptable_payout: float,
    estimated_cpc: float,
    click_to_lead_rate_percent: float,
    accepted_rate_percent: float,
    qualified_rate_percent: float,
    approval_rate_percent: float,
    paid_rate_percent: float,
    return_rate_percent: float,
    scrub_buffer_percent: float,
    chargeback_rate_percent: float,
    safe_cpc: float,
    cap_limit: float,
    expected_volume: float,
    return_window_days: int,
    payment_term_days: int,
    quality_evidence_status: str,
    source_transparency: str,
    consent_evidence: str,
    reject_reason_map_ready: bool,
    invoice_evidence: bool,
    dispute_reserve_present: bool,
    buyer_terms_status: str,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if payout_model not in PAYOUT_MODEL_POINTS:
        blockers.append("payout model is not mapped")
    if headline_payout > 0 and unit_payout <= 0 and proposed_payout <= 0:
        blockers.append("headline payout exists without approved or proposed unit payout")
    if unit_payout <= 0 and proposed_payout <= 0:
        blockers.append("unit payout evidence is missing")
    if unit_payout <= 0 and proposed_payout > 0 and buyer_terms_status != "approved":
        blockers.append("proposed payout is not approved in buyer terms")
    if minimum_acceptable_payout > 0 and max(unit_payout, proposed_payout) < minimum_acceptable_payout:
        blockers.append("payout is below minimum acceptable floor")
    if click_to_lead_rate_percent <= 0:
        blockers.append("click-to-lead rate is missing")
    if estimated_cpc > 0 and safe_cpc < estimated_cpc:
        blockers.append("safe CPC is below estimated CPC")
    if safe_cpc <= 0:
        blockers.append("safe CPC is zero or negative after reserve and costs")
    if accepted_rate_percent < 60:
        blockers.append("accepted rate is below 60 percent")
    if qualified_rate_percent < 45:
        blockers.append("qualified rate is below 45 percent")
    if approval_rate_percent < 55:
        blockers.append("approval rate is below 55 percent")
    if paid_rate_percent < 50:
        blockers.append("paid rate is below 50 percent")
    if return_rate_percent > 20:
        blockers.append("return rate exceeds 20 percent")
    if scrub_buffer_percent > 20:
        blockers.append("scrub buffer exceeds 20 percent")
    if chargeback_rate_percent > 10:
        blockers.append("chargeback rate exceeds 10 percent")
    if cap_limit <= 0:
        blockers.append("buyer cap is missing")
    elif expected_volume > cap_limit:
        blockers.append("expected volume exceeds buyer cap")
    if return_window_days > 30:
        blockers.append("return window is longer than 30 days")
    if payment_term_days > 45:
        blockers.append("payment term is longer than 45 days")
    if quality_evidence_status in {"missing", "anecdotal"}:
        blockers.append("paid quality evidence is not mature")
    if source_transparency in {"opaque", "partial"}:
        blockers.append("source transparency is not buyer-approved")
    if consent_evidence in {"missing", "generic"}:
        blockers.append("consent evidence is not buyer/channel specific")
    if not reject_reason_map_ready:
        blockers.append("reject reason map is missing")
    if not invoice_evidence:
        blockers.append("invoice or settlement evidence is missing")
    if not dispute_reserve_present:
        blockers.append("dispute reserve is missing")
    if buyer_terms_status in {"missing", "draft"}:
        blockers.append("buyer rate card or terms are not approved")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
