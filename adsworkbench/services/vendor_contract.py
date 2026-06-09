from __future__ import annotations


SOURCE_TRANSPARENCY_POINTS = {
    "full": 14,
    "partial": 7,
    "opaque": 0,
}

STOP_CONTROL_POINTS = {
    "precise": 6,
    "partial": 3,
    "none": 0,
}

REFUND_TERMS_POINTS = {
    "clear": 5,
    "partial": 2,
    "missing": 0,
}

POLICY_STATE_POINTS = {
    "clean": 6,
    "warning": 2,
    "active": 0,
}


def calculate_vendor_contract_review(
    *,
    contract_status: str,
    source_detail_level: str,
    tracking_appendix: bool,
    reporting_appendix: bool,
    quality_clause: bool,
    refund_clause: bool,
    stop_control: str,
    tracking_completeness_percent: float,
    report_delay_days: int,
    discrepancy_rate_percent: float,
    invalid_traffic_rate_percent: float,
    buyer_reject_rate_percent: float,
    approved_revenue: float,
    paid_revenue: float,
    spend_to_date: float,
    invoice_amount: float,
    disputed_amount: float,
    refund_credit_amount: float,
    makegood_value: float,
    dispute_response_days: int,
    payment_terms_days: int,
    refund_terms_status: str,
    policy_issue_state: str,
) -> dict[str, object]:
    amount_at_risk = max(disputed_amount - refund_credit_amount - makegood_value, 0)
    paid_roi = _percent(paid_revenue, spend_to_date)
    approved_roi = _percent(approved_revenue, spend_to_date)
    invoice_dispute_rate = _percent(disputed_amount, invoice_amount)
    credit_coverage_rate = _percent(refund_credit_amount + makegood_value, disputed_amount)

    blockers = _blockers(
        contract_status=contract_status,
        source_detail_level=source_detail_level,
        tracking_appendix=tracking_appendix,
        reporting_appendix=reporting_appendix,
        quality_clause=quality_clause,
        refund_clause=refund_clause,
        stop_control=stop_control,
        tracking_completeness_percent=tracking_completeness_percent,
        report_delay_days=report_delay_days,
        discrepancy_rate_percent=discrepancy_rate_percent,
        invalid_traffic_rate_percent=invalid_traffic_rate_percent,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
        paid_roi=paid_roi,
        approved_roi=approved_roi,
        disputed_amount=disputed_amount,
        amount_at_risk=amount_at_risk,
        dispute_response_days=dispute_response_days,
        payment_terms_days=payment_terms_days,
        refund_terms_status=refund_terms_status,
        policy_issue_state=policy_issue_state,
    )

    score = 0
    score += SOURCE_TRANSPARENCY_POINTS.get(source_detail_level, 0)
    score += STOP_CONTROL_POINTS.get(stop_control, 0)
    score += _tracking_points(tracking_appendix, tracking_completeness_percent)
    score += _traffic_quality_points(
        invalid_traffic_rate_percent=invalid_traffic_rate_percent,
        buyer_reject_rate_percent=buyer_reject_rate_percent,
        paid_roi=paid_roi,
        approved_roi=approved_roi,
        approved_revenue=approved_revenue,
        paid_revenue=paid_revenue,
    )
    score += _reporting_points(
        reporting_appendix=reporting_appendix,
        report_delay_days=report_delay_days,
        discrepancy_rate_percent=discrepancy_rate_percent,
    )
    score += _dispute_points(
        dispute_response_days=dispute_response_days,
        credit_coverage_rate=credit_coverage_rate,
        disputed_amount=disputed_amount,
    )
    score += _payment_points(payment_terms_days, refund_terms_status, refund_clause)
    score += _policy_points(policy_issue_state, quality_clause)
    score = min(score, 100)

    return {
        "score": score,
        "risk_level": _risk_level(score, blockers, policy_issue_state, contract_status),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            contract_status=contract_status,
            policy_issue_state=policy_issue_state,
            amount_at_risk=amount_at_risk,
            invalid_traffic_rate_percent=invalid_traffic_rate_percent,
            buyer_reject_rate_percent=buyer_reject_rate_percent,
        ),
        "amount_at_risk": round(amount_at_risk, 2),
        "paid_roi": round(paid_roi, 2),
        "approved_roi": round(approved_roi, 2),
        "invoice_dispute_rate": round(invoice_dispute_rate, 2),
        "credit_coverage_rate": round(credit_coverage_rate, 2),
        "blockers": blockers,
    }


def _percent(value: float, denominator: float) -> float:
    if denominator <= 0:
        return 0
    return max(value, 0) / denominator * 100


def _tracking_points(tracking_appendix: bool, tracking_completeness_percent: float) -> int:
    if not tracking_appendix:
        return 0
    if tracking_completeness_percent >= 95:
        return 15
    if tracking_completeness_percent >= 85:
        return 12
    if tracking_completeness_percent >= 70:
        return 8
    return 3


def _traffic_quality_points(
    *,
    invalid_traffic_rate_percent: float,
    buyer_reject_rate_percent: float,
    paid_roi: float,
    approved_roi: float,
    approved_revenue: float,
    paid_revenue: float,
) -> int:
    points = 0
    if invalid_traffic_rate_percent < 1:
        points += 5
    elif invalid_traffic_rate_percent < 3:
        points += 3
    elif invalid_traffic_rate_percent < 5:
        points += 1

    if buyer_reject_rate_percent < 10:
        points += 5
    elif buyer_reject_rate_percent < 25:
        points += 3
    elif buyer_reject_rate_percent < 40:
        points += 1

    if paid_revenue > 0 and paid_roi >= 120:
        points += 6
    elif paid_revenue > 0 and paid_roi >= 80:
        points += 4
    elif approved_revenue > 0 and approved_roi >= 120:
        points += 4
    elif approved_revenue > 0 and approved_roi >= 80:
        points += 2

    if paid_revenue > 0:
        points += 4
    elif approved_revenue > 0:
        points += 2
    return min(points, 20)


def _reporting_points(
    *,
    reporting_appendix: bool,
    report_delay_days: int,
    discrepancy_rate_percent: float,
) -> int:
    points = 0
    if reporting_appendix:
        points += 5
    if report_delay_days <= 1:
        points += 5
    elif report_delay_days <= 3:
        points += 3
    elif report_delay_days <= 7:
        points += 1
    if discrepancy_rate_percent <= 5:
        points += 5
    elif discrepancy_rate_percent <= 10:
        points += 3
    elif discrepancy_rate_percent <= 20:
        points += 1
    return min(points, 15)


def _dispute_points(
    *,
    dispute_response_days: int,
    credit_coverage_rate: float,
    disputed_amount: float,
) -> int:
    if disputed_amount <= 0:
        return 10
    points = 0
    if dispute_response_days <= 2:
        points += 4
    elif dispute_response_days <= 5:
        points += 2
    if credit_coverage_rate >= 80:
        points += 6
    elif credit_coverage_rate >= 50:
        points += 4
    elif credit_coverage_rate > 0:
        points += 2
    return min(points, 10)


def _payment_points(
    payment_terms_days: int,
    refund_terms_status: str,
    refund_clause: bool,
) -> int:
    points = REFUND_TERMS_POINTS.get(refund_terms_status, 0)
    if refund_clause:
        points += 2
    if payment_terms_days >= 30:
        points += 3
    elif payment_terms_days >= 14:
        points += 2
    elif payment_terms_days >= 7:
        points += 1
    return min(points, 10)


def _policy_points(policy_issue_state: str, quality_clause: bool) -> int:
    points = POLICY_STATE_POINTS.get(policy_issue_state, 0)
    if quality_clause:
        points += 4
    return min(points, 10)


def _risk_level(
    score: int,
    blockers: list[str],
    policy_issue_state: str,
    contract_status: str,
) -> str:
    if contract_status in {"blocked", "suspended"}:
        return "high"
    if policy_issue_state == "active":
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
    contract_status: str,
    policy_issue_state: str,
    amount_at_risk: float,
    invalid_traffic_rate_percent: float,
    buyer_reject_rate_percent: float,
) -> str:
    if contract_status == "blocked" or policy_issue_state == "active":
        return "block_vendor"
    if (
        contract_status == "suspended"
        or invalid_traffic_rate_percent >= 10
        or buyer_reject_rate_percent >= 50
    ):
        return "suspend_vendor"
    if amount_at_risk > 0:
        return "open_dispute"
    if blockers:
        return "watchlist_hold_scale"
    if score >= 85 and contract_status == "active_scale":
        return "allow_scale"
    if score >= 75:
        return "approve_small_test"
    if score >= 55:
        return "watchlist_hold_scale"
    return "collect_due_diligence"


def _blockers(
    *,
    contract_status: str,
    source_detail_level: str,
    tracking_appendix: bool,
    reporting_appendix: bool,
    quality_clause: bool,
    refund_clause: bool,
    stop_control: str,
    tracking_completeness_percent: float,
    report_delay_days: int,
    discrepancy_rate_percent: float,
    invalid_traffic_rate_percent: float,
    buyer_reject_rate_percent: float,
    approved_revenue: float,
    paid_revenue: float,
    paid_roi: float,
    approved_roi: float,
    disputed_amount: float,
    amount_at_risk: float,
    dispute_response_days: int,
    payment_terms_days: int,
    refund_terms_status: str,
    policy_issue_state: str,
) -> list[str]:
    blockers: list[str] = []
    if contract_status in {"blocked", "suspended"}:
        blockers.append("vendor status blocks new spend")
    if source_detail_level == "opaque":
        blockers.append("source, publisher, or placement details are opaque")
    elif source_detail_level == "partial":
        blockers.append("source details are incomplete")
    if not tracking_appendix:
        blockers.append("tracking appendix is missing")
    if tracking_completeness_percent < 70:
        blockers.append("tracking completeness is below 70 percent")
    if not reporting_appendix:
        blockers.append("reporting appendix is missing")
    if report_delay_days > 3:
        blockers.append("vendor reporting delay exceeds three days")
    if discrepancy_rate_percent > 10:
        blockers.append("reporting discrepancy exceeds 10 percent")
    if not quality_clause:
        blockers.append("quality clause is missing")
    if not refund_clause:
        blockers.append("refund, credit, or makegood clause is missing")
    if stop_control == "none":
        blockers.append("vendor cannot stop by source, publisher, placement, or subid")
    elif stop_control == "partial":
        blockers.append("vendor stop control is partial")
    if invalid_traffic_rate_percent >= 5:
        blockers.append("invalid traffic rate is at or above 5 percent")
    if buyer_reject_rate_percent >= 30:
        blockers.append("buyer reject rate is at or above 30 percent")
    if approved_revenue <= 0 and paid_revenue <= 0:
        blockers.append("approved or paid revenue evidence is missing")
    if paid_revenue > 0 and paid_roi < 80:
        blockers.append("paid ROI is below 80 percent")
    elif paid_revenue <= 0 and approved_roi < 80:
        blockers.append("approved ROI is below 80 percent")
    if disputed_amount > 0 and amount_at_risk > 0:
        blockers.append("disputed amount remains at risk")
    if disputed_amount > 0 and dispute_response_days > 5:
        blockers.append("vendor dispute response is slower than five days")
    if payment_terms_days < 14:
        blockers.append("payment terms are too short for revenue validation")
    if refund_terms_status != "clear":
        blockers.append("refund, credit, or makegood terms are not clear")
    if policy_issue_state == "active":
        blockers.append("active policy issue blocks vendor spend")
    elif policy_issue_state == "warning":
        blockers.append("policy warning requires remediation")
    return blockers
