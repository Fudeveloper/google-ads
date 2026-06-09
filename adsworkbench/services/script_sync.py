from __future__ import annotations


AUTH_MODE_POINTS = {
    "scripts_authorized": 8,
    "manual_import": 6,
    "sheets_bridge": 5,
    "url_fetch_internal": 4,
}

SYNC_TYPE_POINTS = {
    "metrics_daily": 8,
    "search_terms": 8,
    "change_history": 8,
    "object_snapshot": 6,
    "script_execution_log": 6,
    "write_preview": 4,
}

DATA_STATUS_POINTS = {
    "provisional": 3,
    "settling": 8,
    "mature": 12,
    "finalized": 15,
    "disputed": 0,
}

REVENUE_STATUS_POINTS = {
    "estimated": 2,
    "submitted": 5,
    "approved": 10,
    "finalized": 12,
    "paid": 15,
    "not_applicable": 8,
}

CONFLICT_POINTS = {
    "clean": 12,
    "manual_review": 5,
    "stale_payload": 0,
    "external_change": 0,
}


def calculate_script_sync_review(
    *,
    auth_mode: str,
    sync_type: str,
    data_status: str,
    revenue_status: str,
    freshness_minutes: int,
    row_count: int,
    error_count: int,
    warning_count: int,
    source_snapshot_hash_present: bool,
    payload_hash_present: bool,
    change_history_checked: bool,
    external_change_count: int,
    conflict_status: str,
    rerun_window_days: int,
    preview_only: bool,
    human_review: bool,
) -> dict[str, object]:
    blockers = _blockers(
        data_status=data_status,
        revenue_status=revenue_status,
        freshness_minutes=freshness_minutes,
        row_count=row_count,
        error_count=error_count,
        warning_count=warning_count,
        source_snapshot_hash_present=source_snapshot_hash_present,
        payload_hash_present=payload_hash_present,
        change_history_checked=change_history_checked,
        external_change_count=external_change_count,
        conflict_status=conflict_status,
        rerun_window_days=rerun_window_days,
        preview_only=preview_only,
        human_review=human_review,
    )

    score = 0
    score += AUTH_MODE_POINTS.get(auth_mode, 0)
    score += SYNC_TYPE_POINTS.get(sync_type, 0)
    score += DATA_STATUS_POINTS.get(data_status, 0)
    score += REVENUE_STATUS_POINTS.get(revenue_status, 0)
    score += _freshness_points(freshness_minutes)
    score += _row_points(row_count)
    score += _issue_points(error_count, warning_count)
    score += 5 if source_snapshot_hash_present else 0
    score += 5 if payload_hash_present else 0
    score += 8 if change_history_checked and external_change_count == 0 else 0
    score += CONFLICT_POINTS.get(conflict_status, 0)
    score += _rerun_points(rerun_window_days)
    score += 5 if preview_only else 0
    score += 5 if human_review else 0
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(
            score,
            data_status,
            error_count,
            conflict_status,
            external_change_count,
            preview_only,
            human_review,
        ),
        "freshness_level": _freshness_level(freshness_minutes),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            data_status=data_status,
            error_count=error_count,
            conflict_status=conflict_status,
            external_change_count=external_change_count,
            human_review=human_review,
        ),
        "blockers": blockers,
    }


def _freshness_points(freshness_minutes: int) -> int:
    if freshness_minutes <= 0:
        return 0
    if freshness_minutes <= 60:
        return 8
    if freshness_minutes <= 240:
        return 6
    if freshness_minutes <= 1440:
        return 4
    return 1


def _row_points(row_count: int) -> int:
    if row_count <= 0:
        return 0
    if row_count <= 5000:
        return 8
    if row_count <= 20000:
        return 4
    return 1


def _issue_points(error_count: int, warning_count: int) -> int:
    if error_count > 0:
        return 0
    if warning_count == 0:
        return 10
    if warning_count <= 5:
        return 6
    return 2


def _rerun_points(rerun_window_days: int) -> int:
    if rerun_window_days >= 7:
        return 8
    if rerun_window_days >= 1:
        return 4
    return 0


def _freshness_level(freshness_minutes: int) -> str:
    if freshness_minutes <= 0:
        return "missing"
    if freshness_minutes <= 60:
        return "heartbeat"
    if freshness_minutes <= 240:
        return "recent"
    if freshness_minutes <= 1440:
        return "stale_same_day"
    return "stale"


def _risk_level(
    score: int,
    data_status: str,
    error_count: int,
    conflict_status: str,
    external_change_count: int,
    preview_only: bool,
    human_review: bool,
) -> str:
    if (
        data_status == "disputed"
        or error_count > 0
        or conflict_status in {"stale_payload", "external_change"}
        or external_change_count > 0
        or not preview_only
        or not human_review
    ):
        return "high"
    if score >= 80:
        return "low"
    if score >= 60:
        return "medium"
    return "high"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    data_status: str,
    error_count: int,
    conflict_status: str,
    external_change_count: int,
    human_review: bool,
) -> str:
    if error_count > 0:
        return "fix_script_errors"
    if data_status == "disputed":
        return "reconcile_dispute"
    if conflict_status in {"stale_payload", "external_change"} or external_change_count > 0:
        return "rerun_snapshot_before_apply"
    if not human_review:
        return "hold_for_human_review"
    if blockers:
        return "rerun_or_reconcile"
    if score >= 80:
        return "approve_manual_import"
    if score >= 60:
        return "snapshot_ready"
    return "hold_for_human_review"


def _blockers(
    *,
    data_status: str,
    revenue_status: str,
    freshness_minutes: int,
    row_count: int,
    error_count: int,
    warning_count: int,
    source_snapshot_hash_present: bool,
    payload_hash_present: bool,
    change_history_checked: bool,
    external_change_count: int,
    conflict_status: str,
    rerun_window_days: int,
    preview_only: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if data_status in {"provisional", "settling"}:
        blockers.append("data is not mature enough for scale decisions")
    if data_status == "disputed":
        blockers.append("data is disputed and needs reconciliation")
    if revenue_status in {"estimated", "submitted"}:
        blockers.append("revenue is not approved/finalized/paid")
    if freshness_minutes <= 0:
        blockers.append("pulled_at freshness is missing")
    elif freshness_minutes > 1440:
        blockers.append("snapshot is stale and should be rerun")
    if row_count <= 0:
        blockers.append("row count is missing")
    if row_count > 20000:
        blockers.append("row count is too large for a single review batch")
    if error_count > 0:
        blockers.append("script run has errors")
    if warning_count > 5:
        blockers.append("script run has many warnings")
    if not source_snapshot_hash_present:
        blockers.append("source snapshot hash is missing")
    if not payload_hash_present:
        blockers.append("payload or query hash is missing")
    if not change_history_checked:
        blockers.append("Change history or ChangeEvent was not checked")
    if external_change_count > 0:
        blockers.append("external changes were detected after snapshot")
    if conflict_status != "clean":
        blockers.append("sync conflict status is not clean")
    if rerun_window_days <= 0:
        blockers.append("rerun window is missing")
    if not preview_only:
        blockers.append("script is not preview/read-only gated")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
