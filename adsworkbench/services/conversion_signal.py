from __future__ import annotations


ACTION_STAGE_POINTS = {
    "micro": 0,
    "submitted": 4,
    "accepted": 10,
    "qualified": 18,
    "approved": 23,
    "paid": 25,
}

VALUE_MODE_POINTS = {
    "zero": 0,
    "gross": 4,
    "fixed_guess": 6,
    "expected": 18,
    "approved": 22,
    "paid": 24,
    "net": 25,
}

SEGMENT_POINTS = {
    "mixed": 0,
    "unsegmented": 2,
    "offer_geo": 6,
    "offer_geo_buyer": 8,
    "offer_geo_buyer_source": 10,
}

POLICY_POINTS = {
    "missing": 0,
    "partial": 4,
    "reviewed": 8,
    "sensitive_reviewed": 10,
}

CUSTOMER_DATA_POINTS = {
    "missing": 0,
    "not_used": 7,
    "policy_reviewed": 10,
    "pii_in_url": 0,
}

IMPORT_POINTS = {
    "none": 0,
    "draft": 2,
    "manual_reviewed": 6,
    "diagnostics_ready": 8,
}

TRANSACTION_POINTS = {
    "missing": 0,
    "unstable": 3,
    "unique_per_stage": 8,
    "idempotent": 10,
}

LAG_POINTS = {
    "unknown": 0,
    "unstable": 3,
    "seasonal": 6,
    "stable": 10,
}


def calculate_conversion_signal_review(
    *,
    action_stage: str,
    primary_status: str,
    value_mode: str,
    bid_strategy: str,
    weekly_conversions: float,
    weekly_approved_conversions: float,
    weekly_paid_conversions: float,
    reported_value_per_conversion: float,
    approved_rate_percent: float,
    paid_rate_percent: float,
    click_id_coverage_percent: float,
    offline_match_rate_percent: float,
    duplicate_rate_percent: float,
    average_lag_days: float,
    p95_lag_days: float,
    incident_count_30d: int,
    segment_granularity_status: str,
    policy_consent_status: str,
    customer_data_status: str,
    offline_import_status: str,
    transaction_id_status: str,
    lag_stability_status: str,
    bid_strategy_status: str,
    primary_secondary_reviewed: bool,
    value_mapping_reviewed: bool,
    transaction_id_dedupe_ready: bool,
    offline_import_diagnostics_ready: bool,
    conversion_lag_reviewed: bool,
    segment_split_ready: bool,
    consent_policy_reviewed: bool,
    bid_strategy_report_reviewed: bool,
    change_history_evidence: bool,
    human_review: bool,
) -> dict[str, object]:
    approved_rate = _rate(approved_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    expected_paid_value = reported_value_per_conversion * approved_rate * paid_rate
    if value_mode in {"paid", "net"}:
        expected_paid_value = reported_value_per_conversion
    elif value_mode == "approved":
        expected_paid_value = reported_value_per_conversion * max(paid_rate, 0.5)

    blockers = _blockers(
        action_stage=action_stage,
        primary_status=primary_status,
        value_mode=value_mode,
        weekly_conversions=weekly_conversions,
        weekly_approved_conversions=weekly_approved_conversions,
        weekly_paid_conversions=weekly_paid_conversions,
        approved_rate_percent=approved_rate_percent,
        paid_rate_percent=paid_rate_percent,
        click_id_coverage_percent=click_id_coverage_percent,
        offline_match_rate_percent=offline_match_rate_percent,
        duplicate_rate_percent=duplicate_rate_percent,
        average_lag_days=average_lag_days,
        p95_lag_days=p95_lag_days,
        incident_count_30d=incident_count_30d,
        segment_granularity_status=segment_granularity_status,
        policy_consent_status=policy_consent_status,
        customer_data_status=customer_data_status,
        offline_import_status=offline_import_status,
        transaction_id_status=transaction_id_status,
        lag_stability_status=lag_stability_status,
        bid_strategy_status=bid_strategy_status,
        primary_secondary_reviewed=primary_secondary_reviewed,
        value_mapping_reviewed=value_mapping_reviewed,
        transaction_id_dedupe_ready=transaction_id_dedupe_ready,
        offline_import_diagnostics_ready=offline_import_diagnostics_ready,
        conversion_lag_reviewed=conversion_lag_reviewed,
        segment_split_ready=segment_split_ready,
        consent_policy_reviewed=consent_policy_reviewed,
        bid_strategy_report_reviewed=bid_strategy_report_reviewed,
        change_history_evidence=change_history_evidence,
        human_review=human_review,
    )

    components = {
        "value_closeness_to_paid": _value_points(
            action_stage=action_stage,
            value_mode=value_mode,
            approved_rate_percent=approved_rate_percent,
            paid_rate_percent=paid_rate_percent,
            primary_secondary_reviewed=primary_secondary_reviewed,
            value_mapping_reviewed=value_mapping_reviewed,
        ),
        "match_and_attribution_quality": _match_points(
            click_id_coverage_percent=click_id_coverage_percent,
            offline_match_rate_percent=offline_match_rate_percent,
            offline_import_status=offline_import_status,
            offline_import_diagnostics_ready=offline_import_diagnostics_ready,
        ),
        "deduplication_integrity": _dedupe_points(
            duplicate_rate_percent=duplicate_rate_percent,
            transaction_id_status=transaction_id_status,
            transaction_id_dedupe_ready=transaction_id_dedupe_ready,
        ),
        "lag_stability": _lag_points(
            average_lag_days=average_lag_days,
            p95_lag_days=p95_lag_days,
            lag_stability_status=lag_stability_status,
            conversion_lag_reviewed=conversion_lag_reviewed,
        ),
        "sample_volume": _sample_points(
            weekly_conversions=weekly_conversions,
            weekly_approved_conversions=weekly_approved_conversions,
            weekly_paid_conversions=weekly_paid_conversions,
        ),
        "segment_granularity": _segment_points(
            segment_granularity_status=segment_granularity_status,
            segment_split_ready=segment_split_ready,
        ),
        "policy_and_consent_safety": _policy_points(
            policy_consent_status=policy_consent_status,
            customer_data_status=customer_data_status,
            consent_policy_reviewed=consent_policy_reviewed,
        ),
        "incident_history": _incident_points(
            incident_count_30d=incident_count_30d,
            change_history_evidence=change_history_evidence,
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
            policy_consent_status=policy_consent_status,
            customer_data_status=customer_data_status,
            duplicate_rate_percent=duplicate_rate_percent,
            primary_status=primary_status,
            action_stage=action_stage,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            action_stage=action_stage,
            primary_status=primary_status,
            value_mode=value_mode,
            click_id_coverage_percent=click_id_coverage_percent,
            offline_match_rate_percent=offline_match_rate_percent,
            duplicate_rate_percent=duplicate_rate_percent,
            lag_stability_status=lag_stability_status,
            policy_consent_status=policy_consent_status,
            customer_data_status=customer_data_status,
            bid_strategy=bid_strategy,
        ),
        "recommended_primary_status": _recommended_primary_status(
            score=score,
            blockers=blockers,
            action_stage=action_stage,
            policy_consent_status=policy_consent_status,
            customer_data_status=customer_data_status,
        ),
        "bid_readiness": _bid_readiness(score, blockers, bid_strategy),
        "expected_paid_value_per_conversion": round(expected_paid_value, 4),
        "safe_target_cpa": round(max(expected_paid_value, 0) * 0.65, 4),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _value_points(
    *,
    action_stage: str,
    value_mode: str,
    approved_rate_percent: float,
    paid_rate_percent: float,
    primary_secondary_reviewed: bool,
    value_mapping_reviewed: bool,
) -> int:
    stage_points = ACTION_STAGE_POINTS.get(action_stage, 0)
    mode_points = VALUE_MODE_POINTS.get(value_mode, 0)
    points = int(round(stage_points * 0.45 + mode_points * 0.35))
    if approved_rate_percent >= 70 and paid_rate_percent >= 60:
        points += 3
    elif approved_rate_percent >= 50 and paid_rate_percent >= 40:
        points += 2
    elif approved_rate_percent > 0 and paid_rate_percent > 0:
        points += 1
    if primary_secondary_reviewed:
        points += 2
    if value_mapping_reviewed:
        points += 2
    return min(points, 25)


def _match_points(
    *,
    click_id_coverage_percent: float,
    offline_match_rate_percent: float,
    offline_import_status: str,
    offline_import_diagnostics_ready: bool,
) -> int:
    points = 0
    if click_id_coverage_percent >= 95:
        points += 5
    elif click_id_coverage_percent >= 85:
        points += 3
    elif click_id_coverage_percent >= 70:
        points += 1
    if offline_match_rate_percent >= 80:
        points += 5
    elif offline_match_rate_percent >= 65:
        points += 3
    elif offline_match_rate_percent >= 50:
        points += 1
    points += min(IMPORT_POINTS.get(offline_import_status, 0), 3)
    if offline_import_diagnostics_ready:
        points += 2
    return min(points, 15)


def _dedupe_points(
    *,
    duplicate_rate_percent: float,
    transaction_id_status: str,
    transaction_id_dedupe_ready: bool,
) -> int:
    points = 0
    if duplicate_rate_percent <= 0.5:
        points += 5
    elif duplicate_rate_percent <= 1:
        points += 4
    elif duplicate_rate_percent <= 2:
        points += 2
    elif duplicate_rate_percent <= 5:
        points += 1
    points += TRANSACTION_POINTS.get(transaction_id_status, 0)
    if transaction_id_dedupe_ready:
        points += 2
    return min(points, 15)


def _lag_points(
    *,
    average_lag_days: float,
    p95_lag_days: float,
    lag_stability_status: str,
    conversion_lag_reviewed: bool,
) -> int:
    points = min(LAG_POINTS.get(lag_stability_status, 0), 6)
    if average_lag_days <= 2 and p95_lag_days <= 7:
        points += 3
    elif average_lag_days <= 5 and p95_lag_days <= 14:
        points += 2
    elif p95_lag_days <= 30:
        points += 1
    if conversion_lag_reviewed:
        points += 1
    return min(points, 10)


def _sample_points(
    *,
    weekly_conversions: float,
    weekly_approved_conversions: float,
    weekly_paid_conversions: float,
) -> int:
    points = 0
    if weekly_conversions >= 50:
        points += 3
    elif weekly_conversions >= 30:
        points += 2
    elif weekly_conversions >= 15:
        points += 1
    if weekly_approved_conversions >= 30:
        points += 4
    elif weekly_approved_conversions >= 15:
        points += 3
    elif weekly_approved_conversions >= 5:
        points += 1
    if weekly_paid_conversions >= 20:
        points += 3
    elif weekly_paid_conversions >= 10:
        points += 2
    elif weekly_paid_conversions >= 3:
        points += 1
    return min(points, 10)


def _segment_points(*, segment_granularity_status: str, segment_split_ready: bool) -> int:
    points = SEGMENT_POINTS.get(segment_granularity_status, 0)
    if segment_split_ready:
        points += 2
    return min(points, 10)


def _policy_points(
    *,
    policy_consent_status: str,
    customer_data_status: str,
    consent_policy_reviewed: bool,
) -> int:
    points = int(
        round(
            POLICY_POINTS.get(policy_consent_status, 0) * 0.6
            + CUSTOMER_DATA_POINTS.get(customer_data_status, 0) * 0.3
        )
    )
    if consent_policy_reviewed:
        points += 1
    return min(points, 10)


def _incident_points(
    *,
    incident_count_30d: int,
    change_history_evidence: bool,
    human_review: bool,
) -> int:
    if incident_count_30d <= 0:
        points = 3
    elif incident_count_30d == 1:
        points = 2
    elif incident_count_30d == 2:
        points = 1
    else:
        points = 0
    if change_history_evidence:
        points += 1
    if human_review:
        points += 1
    return min(points, 5)


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    policy_consent_status: str,
    customer_data_status: str,
    duplicate_rate_percent: float,
    primary_status: str,
    action_stage: str,
) -> str:
    if policy_consent_status == "missing" or customer_data_status == "pii_in_url":
        return "critical"
    if primary_status == "primary" and action_stage in {"micro", "submitted"}:
        return "high"
    if duplicate_rate_percent > 5:
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
    action_stage: str,
    primary_status: str,
    value_mode: str,
    click_id_coverage_percent: float,
    offline_match_rate_percent: float,
    duplicate_rate_percent: float,
    lag_stability_status: str,
    policy_consent_status: str,
    customer_data_status: str,
    bid_strategy: str,
) -> str:
    if policy_consent_status == "missing" or customer_data_status == "pii_in_url":
        return "block_policy_or_consent"
    if primary_status == "primary" and action_stage in {"micro", "submitted"}:
        return "demote_to_secondary"
    if value_mode in {"zero", "gross", "fixed_guess"} and action_stage not in {"paid"}:
        return "rebuild_value_mapping"
    if duplicate_rate_percent > 2:
        return "fix_dedupe"
    if click_id_coverage_percent < 85 or offline_match_rate_percent < 65:
        return "fix_click_id_match"
    if lag_stability_status in {"unknown", "unstable"}:
        return "wait_for_lag_window"
    if score >= 85 and not blockers:
        if bid_strategy in {"target_cpa", "target_roas", "max_conversion_value", "pmax", "broad_ai_max"}:
            return "bid_ready_with_cap"
        return "primary_candidate"
    if score >= 70:
        return "small_automated_test_with_cap"
    if score >= 55:
        return "observation_only"
    return "fix_conversion_signal"


def _recommended_primary_status(
    *,
    score: int,
    blockers: list[str],
    action_stage: str,
    policy_consent_status: str,
    customer_data_status: str,
) -> str:
    if policy_consent_status == "missing" or customer_data_status == "pii_in_url":
        return "blocked"
    if action_stage in {"micro", "submitted"} or score < 55:
        return "secondary_only"
    if score >= 85 and not blockers:
        return "bid_ready"
    if score >= 70:
        return "primary_candidate"
    return "secondary_only"


def _bid_readiness(score: int, blockers: list[str], bid_strategy: str) -> str:
    if score >= 85 and not blockers:
        return "bid_ready"
    if score >= 70 and bid_strategy in {"target_cpa", "target_roas", "max_conversions"}:
        return "small_test"
    if score >= 55:
        return "observation"
    return "blocked"


def _blockers(
    *,
    action_stage: str,
    primary_status: str,
    value_mode: str,
    weekly_conversions: float,
    weekly_approved_conversions: float,
    weekly_paid_conversions: float,
    approved_rate_percent: float,
    paid_rate_percent: float,
    click_id_coverage_percent: float,
    offline_match_rate_percent: float,
    duplicate_rate_percent: float,
    average_lag_days: float,
    p95_lag_days: float,
    incident_count_30d: int,
    segment_granularity_status: str,
    policy_consent_status: str,
    customer_data_status: str,
    offline_import_status: str,
    transaction_id_status: str,
    lag_stability_status: str,
    bid_strategy_status: str,
    primary_secondary_reviewed: bool,
    value_mapping_reviewed: bool,
    transaction_id_dedupe_ready: bool,
    offline_import_diagnostics_ready: bool,
    conversion_lag_reviewed: bool,
    segment_split_ready: bool,
    consent_policy_reviewed: bool,
    bid_strategy_report_reviewed: bool,
    change_history_evidence: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if primary_status == "primary" and action_stage in {"micro", "submitted"}:
        blockers.append("shallow event is configured as primary")
    if value_mode in {"zero", "gross", "fixed_guess"} and action_stage != "paid":
        blockers.append("conversion value is not close to expected paid value")
    if weekly_conversions < 30:
        blockers.append("weekly conversion sample is below 30")
    if weekly_approved_conversions < 10:
        blockers.append("approved conversion sample is too small")
    if weekly_paid_conversions < 5 and action_stage in {"approved", "paid", "qualified"}:
        blockers.append("paid conversion sample is too small")
    if approved_rate_percent < 40:
        blockers.append("approved rate is below 40 percent")
    if paid_rate_percent < 30:
        blockers.append("paid rate is below 30 percent")
    if click_id_coverage_percent < 85:
        blockers.append("click id coverage is below 85 percent")
    if offline_match_rate_percent < 65:
        blockers.append("offline match rate is below 65 percent")
    if duplicate_rate_percent > 2:
        blockers.append("duplicate conversion rate exceeds 2 percent")
    if duplicate_rate_percent > 5:
        blockers.append("duplicate conversion rate exceeds 5 percent")
    if average_lag_days > 7 or p95_lag_days > 21:
        blockers.append("conversion lag window is too long for current ramp")
    if incident_count_30d > 0:
        blockers.append("recent signal incident exists")
    if segment_granularity_status in {"mixed", "unsegmented"}:
        blockers.append("conversion goal mixes unlike offers, geos or buyers")
    if policy_consent_status in {"missing", "partial"}:
        blockers.append("policy and consent review is incomplete")
    if customer_data_status == "pii_in_url":
        blockers.append("PII appears in URL, subid or logs")
    if customer_data_status == "missing":
        blockers.append("customer data policy status is missing")
    if offline_import_status in {"none", "draft"}:
        blockers.append("offline import diagnostics are not ready")
    if transaction_id_status in {"missing", "unstable"}:
        blockers.append("transaction_id is missing or unstable")
    if lag_stability_status in {"unknown", "unstable"}:
        blockers.append("conversion lag is unknown or unstable")
    if bid_strategy_status in {"limited", "misconfigured"}:
        blockers.append("bid strategy report is limited or misconfigured")
    if not primary_secondary_reviewed:
        blockers.append("primary and secondary settings are not reviewed")
    if not value_mapping_reviewed:
        blockers.append("value mapping is not reviewed")
    if not transaction_id_dedupe_ready:
        blockers.append("transaction_id dedupe readiness is missing")
    if not offline_import_diagnostics_ready:
        blockers.append("offline import diagnostics evidence is missing")
    if not conversion_lag_reviewed:
        blockers.append("conversion lag evidence is missing")
    if not segment_split_ready:
        blockers.append("segment split review is missing")
    if not consent_policy_reviewed:
        blockers.append("consent and policy review is missing")
    if not bid_strategy_report_reviewed:
        blockers.append("bid strategy report evidence is missing")
    if not change_history_evidence:
        blockers.append("change history evidence is missing")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
