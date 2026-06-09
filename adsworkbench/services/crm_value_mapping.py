from __future__ import annotations


STANDARD_STAGE_POINTS = {
    "form_started": 0,
    "submitted": 3,
    "validation_pass": 6,
    "accepted": 9,
    "contacted": 10,
    "qualified": 14,
    "approved": 15,
    "paid": 15,
    "returned": 0,
    "rejected": 0,
    "initial_reject": 0,
    "dispute_open": 2,
    "final_closed": 4,
}

VALUE_MODE_POINTS = {
    "zero": 2,
    "expected": 12,
    "approved": 14,
    "paid": 15,
    "net": 15,
    "adjustment": 8,
    "gross": 2,
}

TRANSACTION_POINTS = {
    "missing": 0,
    "unstable": 4,
    "unique_per_stage": 10,
    "idempotent": 12,
}

IMPORT_POINTS = {
    "none": 0,
    "draft": 3,
    "manual_reviewed": 10,
    "qa_ready": 12,
}

ADJUSTMENT_POINTS = {
    "missing": 0,
    "manual_notes": 4,
    "draft": 6,
    "ready": 10,
}

DIAGNOSTICS_POINTS = {
    "missing": 0,
    "errors_open": 3,
    "partial": 6,
    "reviewed": 8,
}

CONSENT_POINTS = {
    "missing": 0,
    "partial": 4,
    "reviewed": 8,
    "sensitive_reviewed": 10,
}

PII_POINTS = {
    "unknown": 0,
    "raw_pii_in_url": 0,
    "internal_only": 5,
    "hashed_minimized": 8,
    "not_used": 8,
}


def calculate_crm_value_mapping_review(
    *,
    standard_stage: str,
    conversion_action_role: str,
    value_mode: str,
    payout_amount: float,
    approved_rate_percent: float,
    paid_rate_percent: float,
    return_rate_percent: float,
    variable_cost_per_conversion: float,
    weekly_stage_count: float,
    weekly_unique_leads: float,
    rejected_count: float,
    returned_count: float,
    duplicate_count: float,
    click_id_match_rate_percent: float,
    import_success_rate_percent: float,
    import_error_rate_percent: float,
    average_stage_lag_days: float,
    return_window_days: int,
    transaction_id_status: str,
    adjustment_rule_status: str,
    import_batch_status: str,
    diagnostics_status: str,
    consent_status: str,
    pii_handling_status: str,
    stage_taxonomy_reviewed: bool,
    buyer_feedback_contract_reviewed: bool,
    conversion_action_mapping_reviewed: bool,
    primary_secondary_reviewed: bool,
    value_mode_reviewed: bool,
    transaction_id_rule_ready: bool,
    rejected_returned_excluded: bool,
    adjustment_policy_ready: bool,
    import_batch_qa_ready: bool,
    diagnostics_reviewed: bool,
    lag_profile_reviewed: bool,
    consent_policy_reviewed: bool,
    human_review: bool,
) -> dict[str, object]:
    approved_rate = _rate(approved_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    return_rate = _rate(return_rate_percent)
    if value_mode == "zero":
        expected_value = 0
    elif value_mode == "approved":
        expected_value = payout_amount * max(1 - return_rate, 0)
    elif value_mode in {"paid", "net"}:
        expected_value = max(payout_amount - variable_cost_per_conversion, 0)
    elif value_mode == "adjustment":
        expected_value = 0
    else:
        expected_value = max(
            payout_amount * approved_rate * paid_rate * max(1 - return_rate, 0)
            - variable_cost_per_conversion,
            0,
        )

    blockers = _blockers(
        standard_stage=standard_stage,
        conversion_action_role=conversion_action_role,
        value_mode=value_mode,
        weekly_stage_count=weekly_stage_count,
        weekly_unique_leads=weekly_unique_leads,
        rejected_count=rejected_count,
        returned_count=returned_count,
        duplicate_count=duplicate_count,
        approved_rate_percent=approved_rate_percent,
        paid_rate_percent=paid_rate_percent,
        return_rate_percent=return_rate_percent,
        click_id_match_rate_percent=click_id_match_rate_percent,
        import_success_rate_percent=import_success_rate_percent,
        import_error_rate_percent=import_error_rate_percent,
        average_stage_lag_days=average_stage_lag_days,
        return_window_days=return_window_days,
        transaction_id_status=transaction_id_status,
        adjustment_rule_status=adjustment_rule_status,
        import_batch_status=import_batch_status,
        diagnostics_status=diagnostics_status,
        consent_status=consent_status,
        pii_handling_status=pii_handling_status,
        stage_taxonomy_reviewed=stage_taxonomy_reviewed,
        buyer_feedback_contract_reviewed=buyer_feedback_contract_reviewed,
        conversion_action_mapping_reviewed=conversion_action_mapping_reviewed,
        primary_secondary_reviewed=primary_secondary_reviewed,
        value_mode_reviewed=value_mode_reviewed,
        transaction_id_rule_ready=transaction_id_rule_ready,
        rejected_returned_excluded=rejected_returned_excluded,
        adjustment_policy_ready=adjustment_policy_ready,
        import_batch_qa_ready=import_batch_qa_ready,
        diagnostics_reviewed=diagnostics_reviewed,
        lag_profile_reviewed=lag_profile_reviewed,
        consent_policy_reviewed=consent_policy_reviewed,
        human_review=human_review,
    )

    components = {
        "stage_mapping": _stage_points(
            standard_stage=standard_stage,
            stage_taxonomy_reviewed=stage_taxonomy_reviewed,
            buyer_feedback_contract_reviewed=buyer_feedback_contract_reviewed,
        ),
        "conversion_action_mapping": _action_points(
            standard_stage=standard_stage,
            conversion_action_role=conversion_action_role,
            conversion_action_mapping_reviewed=conversion_action_mapping_reviewed,
            primary_secondary_reviewed=primary_secondary_reviewed,
        ),
        "value_mapping": _value_points(
            standard_stage=standard_stage,
            value_mode=value_mode,
            approved_rate_percent=approved_rate_percent,
            paid_rate_percent=paid_rate_percent,
            return_rate_percent=return_rate_percent,
            value_mode_reviewed=value_mode_reviewed,
        ),
        "dedupe_and_transaction_id": _dedupe_points(
            weekly_stage_count=weekly_stage_count,
            weekly_unique_leads=weekly_unique_leads,
            duplicate_count=duplicate_count,
            transaction_id_status=transaction_id_status,
            transaction_id_rule_ready=transaction_id_rule_ready,
        ),
        "import_batch_qa": _import_points(
            click_id_match_rate_percent=click_id_match_rate_percent,
            import_success_rate_percent=import_success_rate_percent,
            import_error_rate_percent=import_error_rate_percent,
            import_batch_status=import_batch_status,
            diagnostics_status=diagnostics_status,
            import_batch_qa_ready=import_batch_qa_ready,
            diagnostics_reviewed=diagnostics_reviewed,
        ),
        "adjustment_readiness": _adjustment_points(
            standard_stage=standard_stage,
            rejected_count=rejected_count,
            returned_count=returned_count,
            adjustment_rule_status=adjustment_rule_status,
            rejected_returned_excluded=rejected_returned_excluded,
            adjustment_policy_ready=adjustment_policy_ready,
        ),
        "lag_profile": _lag_points(
            average_stage_lag_days=average_stage_lag_days,
            return_window_days=return_window_days,
            lag_profile_reviewed=lag_profile_reviewed,
        ),
        "policy_and_pii": _policy_points(
            consent_status=consent_status,
            pii_handling_status=pii_handling_status,
            consent_policy_reviewed=consent_policy_reviewed,
            human_review=human_review,
        ),
    }
    score = max(min(sum(components.values()), 100), 0)

    return {
        "score": score,
        "score_components": components,
        "risk_level": _risk_level(
            score=score,
            blockers=blockers,
            standard_stage=standard_stage,
            conversion_action_role=conversion_action_role,
            consent_status=consent_status,
            pii_handling_status=pii_handling_status,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            standard_stage=standard_stage,
            conversion_action_role=conversion_action_role,
            value_mode=value_mode,
            transaction_id_status=transaction_id_status,
            import_batch_status=import_batch_status,
            diagnostics_status=diagnostics_status,
            adjustment_rule_status=adjustment_rule_status,
            consent_status=consent_status,
            pii_handling_status=pii_handling_status,
        ),
        "primary_recommendation": _primary_recommendation(
            score=score,
            blockers=blockers,
            standard_stage=standard_stage,
            consent_status=consent_status,
            pii_handling_status=pii_handling_status,
        ),
        "recommended_upload_policy": _upload_policy(
            score=score,
            blockers=blockers,
            standard_stage=standard_stage,
            import_batch_status=import_batch_status,
            diagnostics_status=diagnostics_status,
        ),
        "expected_value": round(expected_value, 4),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _stage_points(
    *,
    standard_stage: str,
    stage_taxonomy_reviewed: bool,
    buyer_feedback_contract_reviewed: bool,
) -> int:
    points = STANDARD_STAGE_POINTS.get(standard_stage, 0)
    if stage_taxonomy_reviewed:
        points += 2
    if buyer_feedback_contract_reviewed:
        points += 2
    return min(points, 15)


def _action_points(
    *,
    standard_stage: str,
    conversion_action_role: str,
    conversion_action_mapping_reviewed: bool,
    primary_secondary_reviewed: bool,
) -> int:
    if standard_stage in {"rejected", "returned", "initial_reject"}:
        points = 8 if conversion_action_role in {"adjustment", "none"} else 0
    elif standard_stage in {"form_started", "submitted", "validation_pass"}:
        points = 9 if conversion_action_role == "secondary" else 2
    elif standard_stage in {"qualified", "approved", "paid"}:
        points = 11 if conversion_action_role in {"primary_candidate", "primary"} else 8
    else:
        points = 6
    if conversion_action_mapping_reviewed:
        points += 2
    if primary_secondary_reviewed:
        points += 2
    return min(points, 15)


def _value_points(
    *,
    standard_stage: str,
    value_mode: str,
    approved_rate_percent: float,
    paid_rate_percent: float,
    return_rate_percent: float,
    value_mode_reviewed: bool,
) -> int:
    if standard_stage in {"rejected", "returned", "initial_reject"}:
        points = 9 if value_mode in {"zero", "adjustment"} else 0
    elif standard_stage in {"form_started", "submitted", "validation_pass"}:
        points = 8 if value_mode in {"zero", "expected"} else 2
    else:
        points = VALUE_MODE_POINTS.get(value_mode, 0)
    if approved_rate_percent >= 60 and paid_rate_percent >= 50:
        points += 2
    elif approved_rate_percent >= 40 and paid_rate_percent >= 30:
        points += 1
    if return_rate_percent <= 10:
        points += 1
    if value_mode_reviewed:
        points += 2
    return min(points, 15)


def _dedupe_points(
    *,
    weekly_stage_count: float,
    weekly_unique_leads: float,
    duplicate_count: float,
    transaction_id_status: str,
    transaction_id_rule_ready: bool,
) -> int:
    duplicate_rate = duplicate_count / weekly_stage_count * 100 if weekly_stage_count > 0 else 0
    unique_rate = weekly_unique_leads / weekly_stage_count * 100 if weekly_stage_count > 0 else 0
    points = min(TRANSACTION_POINTS.get(transaction_id_status, 0), 9)
    if duplicate_rate <= 1:
        points += 3
    elif duplicate_rate <= 3:
        points += 2
    elif duplicate_rate <= 5:
        points += 1
    if unique_rate >= 95:
        points += 2
    elif unique_rate >= 90:
        points += 1
    if transaction_id_rule_ready:
        points += 1
    return min(points, 15)


def _import_points(
    *,
    click_id_match_rate_percent: float,
    import_success_rate_percent: float,
    import_error_rate_percent: float,
    import_batch_status: str,
    diagnostics_status: str,
    import_batch_qa_ready: bool,
    diagnostics_reviewed: bool,
) -> int:
    points = min(IMPORT_POINTS.get(import_batch_status, 0), 5)
    points += min(DIAGNOSTICS_POINTS.get(diagnostics_status, 0), 3)
    if click_id_match_rate_percent >= 80:
        points += 3
    elif click_id_match_rate_percent >= 65:
        points += 2
    elif click_id_match_rate_percent >= 50:
        points += 1
    if import_success_rate_percent >= 95 and import_error_rate_percent <= 2:
        points += 2
    elif import_success_rate_percent >= 85 and import_error_rate_percent <= 5:
        points += 1
    if import_batch_qa_ready:
        points += 1
    if diagnostics_reviewed:
        points += 1
    return min(points, 15)


def _adjustment_points(
    *,
    standard_stage: str,
    rejected_count: float,
    returned_count: float,
    adjustment_rule_status: str,
    rejected_returned_excluded: bool,
    adjustment_policy_ready: bool,
) -> int:
    points = min(ADJUSTMENT_POINTS.get(adjustment_rule_status, 0), 5)
    if rejected_returned_excluded:
        points += 2
    if adjustment_policy_ready:
        points += 2
    if standard_stage in {"rejected", "returned", "initial_reject"}:
        points += 1 if adjustment_rule_status in {"ready", "draft"} else 0
    elif rejected_count + returned_count <= 5:
        points += 1
    return min(points, 10)


def _lag_points(
    *,
    average_stage_lag_days: float,
    return_window_days: int,
    lag_profile_reviewed: bool,
) -> int:
    points = 0
    if average_stage_lag_days <= 3:
        points += 3
    elif average_stage_lag_days <= 7:
        points += 2
    elif average_stage_lag_days <= 30:
        points += 1
    if return_window_days > 0:
        points += 1
    if lag_profile_reviewed:
        points += 1
    return min(points, 5)


def _policy_points(
    *,
    consent_status: str,
    pii_handling_status: str,
    consent_policy_reviewed: bool,
    human_review: bool,
) -> int:
    points = int(
        round(
            CONSENT_POINTS.get(consent_status, 0) * 0.55
            + PII_POINTS.get(pii_handling_status, 0) * 0.3
        )
    )
    if consent_policy_reviewed:
        points += 1
    if human_review:
        points += 1
    return min(points, 10)


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    standard_stage: str,
    conversion_action_role: str,
    consent_status: str,
    pii_handling_status: str,
) -> str:
    if pii_handling_status == "raw_pii_in_url" or consent_status == "missing":
        return "critical"
    if standard_stage in {"rejected", "returned", "initial_reject"} and conversion_action_role not in {
        "adjustment",
        "none",
    }:
        return "critical"
    if standard_stage in {"form_started", "submitted"} and conversion_action_role in {
        "primary",
        "primary_candidate",
    }:
        return "high"
    if score >= 85 and not blockers:
        return "low"
    if score >= 70:
        return "medium"
    if score >= 55:
        return "high"
    return "critical"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    standard_stage: str,
    conversion_action_role: str,
    value_mode: str,
    transaction_id_status: str,
    import_batch_status: str,
    diagnostics_status: str,
    adjustment_rule_status: str,
    consent_status: str,
    pii_handling_status: str,
) -> str:
    if pii_handling_status == "raw_pii_in_url" or consent_status == "missing":
        return "block_policy_or_pii"
    if standard_stage in {"rejected", "returned", "initial_reject"}:
        if conversion_action_role not in {"adjustment", "none"}:
            return "do_not_upload_positive"
        return "adjustment_review"
    if standard_stage in {"form_started", "submitted"} and conversion_action_role in {
        "primary",
        "primary_candidate",
    }:
        return "demote_to_secondary"
    if value_mode == "gross":
        return "rebuild_value_mapping"
    if transaction_id_status in {"missing", "unstable"}:
        return "fix_transaction_id"
    if import_batch_status in {"none", "draft"} or diagnostics_status in {
        "missing",
        "errors_open",
    }:
        return "import_qa_required"
    if adjustment_rule_status == "missing":
        return "define_adjustment_rule"
    if score >= 85 and not blockers:
        return "offline_import_candidate"
    if score >= 70:
        return "secondary_observation"
    if score >= 55:
        return "fix_stage_mapping"
    return "blocked"


def _primary_recommendation(
    *,
    score: int,
    blockers: list[str],
    standard_stage: str,
    consent_status: str,
    pii_handling_status: str,
) -> str:
    if pii_handling_status == "raw_pii_in_url" or consent_status == "missing":
        return "blocked"
    if standard_stage in {"rejected", "returned", "initial_reject"}:
        return "adjustment_only"
    if standard_stage in {"form_started", "submitted", "validation_pass"}:
        return "secondary_only"
    if score >= 85 and not blockers:
        return "primary_candidate"
    if score >= 70:
        return "secondary_observation"
    return "secondary_only"


def _upload_policy(
    *,
    score: int,
    blockers: list[str],
    standard_stage: str,
    import_batch_status: str,
    diagnostics_status: str,
) -> str:
    if standard_stage in {"rejected", "returned", "initial_reject"}:
        return "adjustment_only"
    if standard_stage in {"form_started"}:
        return "do_not_upload"
    if standard_stage in {"submitted", "validation_pass"}:
        return "secondary_observation"
    if import_batch_status in {"none", "draft"} or diagnostics_status in {"missing", "errors_open"}:
        return "qa_before_upload"
    if score >= 85 and not blockers:
        return "offline_import_candidate"
    if score >= 70:
        return "manual_review_only"
    return "do_not_upload"


def _blockers(
    *,
    standard_stage: str,
    conversion_action_role: str,
    value_mode: str,
    weekly_stage_count: float,
    weekly_unique_leads: float,
    rejected_count: float,
    returned_count: float,
    duplicate_count: float,
    approved_rate_percent: float,
    paid_rate_percent: float,
    return_rate_percent: float,
    click_id_match_rate_percent: float,
    import_success_rate_percent: float,
    import_error_rate_percent: float,
    average_stage_lag_days: float,
    return_window_days: int,
    transaction_id_status: str,
    adjustment_rule_status: str,
    import_batch_status: str,
    diagnostics_status: str,
    consent_status: str,
    pii_handling_status: str,
    stage_taxonomy_reviewed: bool,
    buyer_feedback_contract_reviewed: bool,
    conversion_action_mapping_reviewed: bool,
    primary_secondary_reviewed: bool,
    value_mode_reviewed: bool,
    transaction_id_rule_ready: bool,
    rejected_returned_excluded: bool,
    adjustment_policy_ready: bool,
    import_batch_qa_ready: bool,
    diagnostics_reviewed: bool,
    lag_profile_reviewed: bool,
    consent_policy_reviewed: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if standard_stage in {"rejected", "returned", "initial_reject"} and conversion_action_role not in {
        "adjustment",
        "none",
    }:
        blockers.append("rejected or returned stage is mapped as positive conversion")
    if standard_stage in {"form_started", "submitted"} and conversion_action_role in {
        "primary",
        "primary_candidate",
    }:
        blockers.append("shallow CRM stage is mapped as primary")
    if value_mode == "gross":
        blockers.append("gross payout is used as conversion value")
    if weekly_stage_count <= 0:
        blockers.append("stage sample count is missing")
    if weekly_stage_count > 0:
        duplicate_rate = duplicate_count / weekly_stage_count * 100
        unique_rate = weekly_unique_leads / weekly_stage_count * 100
        rejected_returned_rate = (rejected_count + returned_count) / weekly_stage_count * 100
        if duplicate_rate > 3:
            blockers.append("duplicate row rate exceeds 3 percent")
        if unique_rate < 90:
            blockers.append("unique lead rate is below 90 percent")
        if rejected_returned_rate > 20:
            blockers.append("rejected and returned share exceeds 20 percent")
    if standard_stage in {"qualified", "approved", "paid"} and approved_rate_percent < 40:
        blockers.append("approved rate is below 40 percent")
    if standard_stage in {"approved", "paid"} and paid_rate_percent < 30:
        blockers.append("paid rate is below 30 percent")
    if return_rate_percent > 25:
        blockers.append("return rate exceeds 25 percent")
    if click_id_match_rate_percent < 65 and standard_stage not in {"form_started"}:
        blockers.append("click ID match rate is below 65 percent")
    if import_success_rate_percent < 90 and standard_stage not in {"form_started"}:
        blockers.append("import success rate is below 90 percent")
    if import_error_rate_percent > 5:
        blockers.append("import error rate exceeds 5 percent")
    if average_stage_lag_days > 14:
        blockers.append("stage lag exceeds 14 days")
    if standard_stage in {"approved", "paid"} and return_window_days <= 0:
        blockers.append("return window is missing for approved or paid stage")
    if transaction_id_status in {"missing", "unstable"}:
        blockers.append("transaction_id rule is missing or unstable")
    if adjustment_rule_status == "missing":
        blockers.append("adjustment rule is missing")
    if import_batch_status in {"none", "draft"} and standard_stage not in {"form_started"}:
        blockers.append("offline import batch QA is not ready")
    if diagnostics_status in {"missing", "errors_open"} and standard_stage not in {"form_started"}:
        blockers.append("offline import diagnostics are missing or open")
    if consent_status in {"missing", "partial"}:
        blockers.append("consent review is incomplete")
    if pii_handling_status == "raw_pii_in_url":
        blockers.append("raw PII appears in URL, subid or logs")
    if pii_handling_status == "unknown":
        blockers.append("PII handling status is unknown")
    if not stage_taxonomy_reviewed:
        blockers.append("stage taxonomy review is missing")
    if not buyer_feedback_contract_reviewed:
        blockers.append("buyer feedback contract review is missing")
    if not conversion_action_mapping_reviewed:
        blockers.append("conversion action mapping review is missing")
    if not primary_secondary_reviewed:
        blockers.append("primary and secondary review is missing")
    if not value_mode_reviewed:
        blockers.append("value mode review is missing")
    if not transaction_id_rule_ready:
        blockers.append("transaction_id rule evidence is missing")
    if not rejected_returned_excluded:
        blockers.append("rejected and returned exclusion is missing")
    if not adjustment_policy_ready:
        blockers.append("adjustment policy readiness is missing")
    if not import_batch_qa_ready:
        blockers.append("import batch QA evidence is missing")
    if not diagnostics_reviewed:
        blockers.append("diagnostics review is missing")
    if not lag_profile_reviewed:
        blockers.append("lag profile review is missing")
    if not consent_policy_reviewed:
        blockers.append("consent and policy review is missing")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
