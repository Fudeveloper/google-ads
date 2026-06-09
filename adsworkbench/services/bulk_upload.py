from __future__ import annotations


EXPORT_TYPE_POINTS = {
    "editor_csv": 8,
    "scripts_preview": 6,
    "bulk_upload_preview": 6,
}

PREFLIGHT_POINTS = {
    "passed": 15,
    "warnings": 6,
    "blocked": 0,
}

PREVIEW_POINTS = {
    "passed": 15,
    "warnings": 8,
    "errors": 0,
    "not_run": 0,
}

POST_STATUS_POINTS = {
    "not_posted": 8,
    "posted": 6,
    "partial_error": 0,
    "rolled_back": 3,
}


def calculate_bulk_upload_review(
    *,
    export_type: str,
    preflight_status: str,
    row_count: int,
    keyword_count: int,
    ad_count: int,
    expected_budget_delta: float,
    url_change_count: int,
    default_paused: bool,
    human_review: bool,
    preview_status: str,
    editor_check_status: str,
    post_status: str,
    change_history_attached: bool,
    rollback_plan: bool,
    target_customer_confirmed: bool,
    policy_review_complete: bool,
    high_risk_change_count: int,
) -> dict[str, object]:
    blockers = _blockers(
        preflight_status=preflight_status,
        row_count=row_count,
        keyword_count=keyword_count,
        ad_count=ad_count,
        expected_budget_delta=expected_budget_delta,
        url_change_count=url_change_count,
        default_paused=default_paused,
        human_review=human_review,
        preview_status=preview_status,
        editor_check_status=editor_check_status,
        post_status=post_status,
        change_history_attached=change_history_attached,
        rollback_plan=rollback_plan,
        target_customer_confirmed=target_customer_confirmed,
        policy_review_complete=policy_review_complete,
        high_risk_change_count=high_risk_change_count,
    )

    score = 0
    score += EXPORT_TYPE_POINTS.get(export_type, 0)
    score += PREFLIGHT_POINTS.get(preflight_status, 0)
    score += _scope_points(row_count, keyword_count, ad_count)
    score += _budget_points(expected_budget_delta)
    score += _url_points(url_change_count)
    score += 8 if default_paused else 0
    score += 8 if human_review else 0
    score += PREVIEW_POINTS.get(preview_status, 0)
    score += _editor_points(editor_check_status)
    score += POST_STATUS_POINTS.get(post_status, 0)
    score += 5 if change_history_attached else 0
    score += 5 if rollback_plan else 0
    score += 5 if target_customer_confirmed else 0
    score += 5 if policy_review_complete else 0
    score -= min(high_risk_change_count * 4, 20)
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(
            score,
            blockers,
            preflight_status,
            preview_status,
            editor_check_status,
            post_status,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            preflight_status=preflight_status,
            preview_status=preview_status,
            editor_check_status=editor_check_status,
            post_status=post_status,
            high_risk_change_count=high_risk_change_count,
        ),
        "budget_delta_percent": round(_budget_delta_percent(expected_budget_delta), 2),
        "change_scope": _change_scope(row_count, expected_budget_delta, url_change_count),
        "blockers": blockers,
    }


def _scope_points(row_count: int, keyword_count: int, ad_count: int) -> int:
    if row_count <= 0:
        return 0
    if row_count <= 20 and keyword_count <= 50 and ad_count <= 10:
        return 10
    if row_count <= 100 and keyword_count <= 200 and ad_count <= 25:
        return 6
    if row_count <= 500:
        return 3
    return 0


def _budget_points(expected_budget_delta: float) -> int:
    if expected_budget_delta <= 0:
        return 10
    if expected_budget_delta <= 50:
        return 8
    if expected_budget_delta <= 250:
        return 4
    return 0


def _url_points(url_change_count: int) -> int:
    if url_change_count == 0:
        return 8
    if url_change_count <= 2:
        return 4
    return 0


def _editor_points(editor_check_status: str) -> int:
    if editor_check_status == "passed":
        return 8
    if editor_check_status == "warnings":
        return 4
    if editor_check_status == "not_run":
        return 0
    return 0


def _budget_delta_percent(expected_budget_delta: float) -> float:
    if expected_budget_delta <= 0:
        return 0
    return expected_budget_delta


def _change_scope(row_count: int, expected_budget_delta: float, url_change_count: int) -> str:
    if row_count > 500 or expected_budget_delta > 250 or url_change_count > 5:
        return "large"
    if row_count > 100 or expected_budget_delta > 50 or url_change_count > 0:
        return "medium"
    return "small"


def _risk_level(
    score: int,
    blockers: list[str],
    preflight_status: str,
    preview_status: str,
    editor_check_status: str,
    post_status: str,
) -> str:
    if (
        preflight_status == "blocked"
        or preview_status == "errors"
        or editor_check_status == "errors"
        or post_status == "partial_error"
    ):
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
    preflight_status: str,
    preview_status: str,
    editor_check_status: str,
    post_status: str,
    high_risk_change_count: int,
) -> str:
    if preflight_status == "blocked":
        return "fix_preflight_before_export"
    if preview_status == "errors" or editor_check_status == "errors":
        return "fix_preview_errors"
    if post_status == "partial_error":
        return "reconcile_partial_failure"
    if high_risk_change_count > 0:
        return "manual_review_high_risk_changes"
    if blockers:
        return "hold_for_review"
    if score >= 80:
        return "approve_manual_post"
    if score >= 60:
        return "run_editor_or_preview_check"
    return "hold_for_review"


def _blockers(
    *,
    preflight_status: str,
    row_count: int,
    keyword_count: int,
    ad_count: int,
    expected_budget_delta: float,
    url_change_count: int,
    default_paused: bool,
    human_review: bool,
    preview_status: str,
    editor_check_status: str,
    post_status: str,
    change_history_attached: bool,
    rollback_plan: bool,
    target_customer_confirmed: bool,
    policy_review_complete: bool,
    high_risk_change_count: int,
) -> list[str]:
    blockers: list[str] = []
    if preflight_status == "blocked":
        blockers.append("campaign preflight blocks export")
    elif preflight_status == "warnings":
        blockers.append("campaign preflight has warnings")
    if row_count <= 0:
        blockers.append("row count is missing")
    if row_count > 500:
        blockers.append("row count is too large for a single batch")
    if keyword_count > 200:
        blockers.append("keyword count exceeds small batch threshold")
    if ad_count > 25:
        blockers.append("ad count exceeds small batch threshold")
    if expected_budget_delta > 250:
        blockers.append("expected budget delta exceeds safe review threshold")
    if url_change_count > 0:
        blockers.append("URL changes require link and destination QA")
    if not default_paused:
        blockers.append("new or changed entities are not default paused")
    if not human_review:
        blockers.append("human review is missing")
    if preview_status == "not_run":
        blockers.append("Bulk Upload or Scripts preview has not been run")
    elif preview_status == "warnings":
        blockers.append("preview has warnings")
    elif preview_status == "errors":
        blockers.append("preview has errors")
    if editor_check_status == "not_run":
        blockers.append("Google Ads Editor check has not been run")
    elif editor_check_status == "warnings":
        blockers.append("Editor check has warnings")
    elif editor_check_status == "errors":
        blockers.append("Editor check has errors")
    if post_status == "partial_error":
        blockers.append("posted batch has partial errors")
    if post_status in {"posted", "partial_error", "rolled_back"} and not change_history_attached:
        blockers.append("Change history evidence is missing")
    if not rollback_plan:
        blockers.append("rollback plan is missing")
    if not target_customer_confirmed:
        blockers.append("target customer, timezone, or currency is not confirmed")
    if not policy_review_complete:
        blockers.append("policy and claim review are not complete")
    if high_risk_change_count > 0:
        blockers.append("batch contains high-risk budget, URL, status, or conversion changes")
    return blockers
