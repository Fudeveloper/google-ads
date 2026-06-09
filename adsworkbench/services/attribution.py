from __future__ import annotations


TEST_TYPE_POINTS = {
    "geo_holdout": 10,
    "campaign_experiment": 10,
    "audience_holdout": 8,
    "lift_study": 10,
    "model_comparison": 5,
    "pre_post": 2,
}

HOLDOUT_QUALITY_POINTS = {
    "clean": 20,
    "partial": 10,
    "weak": 4,
    "none": 0,
}

REVENUE_STATUS_POINTS = {
    "submitted": 3,
    "accepted": 6,
    "approved": 10,
    "finalized": 12,
    "paid": 12,
}

DATA_STATUS_POINTS = {
    "fresh": 2,
    "partial": 5,
    "mature": 8,
    "settled": 8,
}

RISK_POINTS = {
    "low": 8,
    "medium": 4,
    "high": 0,
}


def calculate_attribution_review(
    *,
    test_type: str,
    holdout_quality: str,
    revenue_status: str,
    data_status: str,
    attributed_revenue: float,
    treatment_revenue: float,
    control_revenue: float,
    ad_cost: float,
    variable_cost: float,
    attributed_conversions: int,
    incremental_conversions: int,
    sample_size: int,
    confidence_level: float,
    brand_cannibalization_risk: str,
    organic_cannibalization_risk: str,
    remarketing_cannibalization_risk: str,
    pmax_broad_overlap_risk: str,
    change_history_clean: bool,
    single_variable_test: bool,
    approved_paid_evidence: bool,
    human_review: bool,
) -> dict[str, object]:
    incremental_revenue = treatment_revenue - control_revenue
    i_roas = _ratio(incremental_revenue, ad_cost)
    incremental_profit = incremental_revenue - ad_cost - variable_cost
    attributed_to_incremental_ratio = _ratio(incremental_revenue, attributed_revenue)

    blockers = _blockers(
        test_type=test_type,
        holdout_quality=holdout_quality,
        revenue_status=revenue_status,
        data_status=data_status,
        attributed_revenue=attributed_revenue,
        incremental_revenue=incremental_revenue,
        incremental_profit=incremental_profit,
        i_roas=i_roas,
        attributed_conversions=attributed_conversions,
        incremental_conversions=incremental_conversions,
        sample_size=sample_size,
        confidence_level=confidence_level,
        brand_cannibalization_risk=brand_cannibalization_risk,
        organic_cannibalization_risk=organic_cannibalization_risk,
        remarketing_cannibalization_risk=remarketing_cannibalization_risk,
        pmax_broad_overlap_risk=pmax_broad_overlap_risk,
        change_history_clean=change_history_clean,
        single_variable_test=single_variable_test,
        approved_paid_evidence=approved_paid_evidence,
        human_review=human_review,
    )

    score = 0
    score += TEST_TYPE_POINTS.get(test_type, 0)
    score += HOLDOUT_QUALITY_POINTS.get(holdout_quality, 0)
    score += _incremental_signal_points(incremental_revenue, incremental_profit, i_roas)
    score += _sample_points(sample_size, confidence_level)
    score += REVENUE_STATUS_POINTS.get(revenue_status, 0)
    score += DATA_STATUS_POINTS.get(data_status, 0)
    score += RISK_POINTS.get(brand_cannibalization_risk, 0)
    score += RISK_POINTS.get(organic_cannibalization_risk, 0)
    score += RISK_POINTS.get(remarketing_cannibalization_risk, 0)
    score += RISK_POINTS.get(pmax_broad_overlap_risk, 0)
    score += 5 if change_history_clean else 0
    score += 5 if single_variable_test else 0
    score += 5 if approved_paid_evidence else 0
    score += 5 if human_review else 0
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(
            score,
            blockers,
            incremental_revenue,
            incremental_profit,
            i_roas,
            brand_cannibalization_risk,
            organic_cannibalization_risk,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            incremental_revenue=incremental_revenue,
            incremental_profit=incremental_profit,
            i_roas=i_roas,
        ),
        "incremental_revenue": round(incremental_revenue, 2),
        "i_roas": round(i_roas, 4),
        "incremental_profit": round(incremental_profit, 2),
        "attributed_to_incremental_ratio": round(attributed_to_incremental_ratio, 4),
        "blockers": blockers,
    }


def _ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0
    return numerator / denominator


def _incremental_signal_points(
    incremental_revenue: float,
    incremental_profit: float,
    i_roas: float,
) -> int:
    if incremental_revenue <= 0 or incremental_profit <= 0:
        return 0
    if i_roas >= 2:
        return 20
    if i_roas >= 1.2:
        return 14
    if i_roas >= 1:
        return 8
    return 2


def _sample_points(sample_size: int, confidence_level: float) -> int:
    if sample_size >= 1000 and confidence_level >= 90:
        return 15
    if sample_size >= 500 and confidence_level >= 80:
        return 10
    if sample_size >= 100:
        return 5
    return 0


def _risk_level(
    score: int,
    blockers: list[str],
    incremental_revenue: float,
    incremental_profit: float,
    i_roas: float,
    brand_cannibalization_risk: str,
    organic_cannibalization_risk: str,
) -> str:
    if (
        incremental_revenue <= 0
        or incremental_profit <= 0
        or i_roas < 1
        or brand_cannibalization_risk == "high"
        or organic_cannibalization_risk == "high"
    ):
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
    incremental_revenue: float,
    incremental_profit: float,
    i_roas: float,
) -> str:
    if incremental_revenue <= 0 or incremental_profit <= 0 or i_roas < 1:
        return "stop_or_freeze"
    if blockers:
        return "run_holdout_or_reconcile"
    if score >= 85:
        return "scale_core_evidence"
    if score >= 70:
        return "small_ramp_retest"
    if score >= 55:
        return "test_only"
    return "run_holdout_or_reconcile"


def _blockers(
    *,
    test_type: str,
    holdout_quality: str,
    revenue_status: str,
    data_status: str,
    attributed_revenue: float,
    incremental_revenue: float,
    incremental_profit: float,
    i_roas: float,
    attributed_conversions: int,
    incremental_conversions: int,
    sample_size: int,
    confidence_level: float,
    brand_cannibalization_risk: str,
    organic_cannibalization_risk: str,
    remarketing_cannibalization_risk: str,
    pmax_broad_overlap_risk: str,
    change_history_clean: bool,
    single_variable_test: bool,
    approved_paid_evidence: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if test_type == "pre_post":
        blockers.append("pre/post comparison is weak without control")
    if holdout_quality in {"none", "weak"}:
        blockers.append("holdout or control quality is weak")
    if revenue_status in {"submitted", "accepted"}:
        blockers.append("revenue is not approved/finalized/paid")
    if data_status in {"fresh", "partial"}:
        blockers.append("data window is not mature")
    if attributed_revenue > 0 and incremental_revenue <= 0:
        blockers.append("attributed revenue has no incremental lift")
    if incremental_profit <= 0:
        blockers.append("incremental profit is not positive")
    if i_roas < 1:
        blockers.append("iROAS is below break-even")
    if attributed_conversions > 0 and incremental_conversions <= 0:
        blockers.append("attributed conversions do not show incremental conversions")
    if sample_size < 500:
        blockers.append("sample size is weak")
    if confidence_level < 80:
        blockers.append("confidence level is weak or not estimated")
    if brand_cannibalization_risk == "high":
        blockers.append("brand cannibalization risk is high")
    if organic_cannibalization_risk == "high":
        blockers.append("organic or direct cannibalization risk is high")
    if remarketing_cannibalization_risk == "high":
        blockers.append("remarketing cannibalization risk is high")
    if pmax_broad_overlap_risk == "high":
        blockers.append("PMax, broad, or automation overlap risk is high")
    if not change_history_clean:
        blockers.append("Change history is not clean during test window")
    if not single_variable_test:
        blockers.append("test changed multiple variables at once")
    if not approved_paid_evidence:
        blockers.append("approved/paid/finalized revenue evidence is missing")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
