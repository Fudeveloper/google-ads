from __future__ import annotations

from datetime import datetime, timedelta

from adsworkbench.models import TaskJob
from adsworkbench.services.analytics import metric_totals
from adsworkbench.services.creative import generate_creative_sets
from adsworkbench.services.exporters import (
    campaign_to_google_ads_editor_csv,
    campaign_to_scripts_payload,
)
from adsworkbench.services.preflight import campaign_preflight_blockers


TASK_TYPES = [
    ("landing_audit_review", "落地页审计复核"),
    ("creative_generation", "创意生成"),
    ("export_csv", "CSV 导出检查"),
    ("export_script_payload", "Scripts JSON 导出检查"),
    ("link_plan_review", "链接计划检查"),
    ("metrics_review", "指标复核"),
]

TASK_TYPE_VALUES = {value for value, _label in TASK_TYPES}

FORBIDDEN_TASK_KEYWORDS = (
    "login",
    "signin",
    "password",
    "otp",
    "2fa",
    "mfa",
    "captcha",
    "challenge",
    "recovery",
    "cookie",
    "session",
    "token_refresh",
    "click",
    "impression",
    "visit",
    "traffic",
    "referer",
    "referrer",
    "scroll",
    "bounce",
    "autosurf",
)

FORBIDDEN_TASK_TEXT_TERMS = (
    "cookie",
    "session token",
    "browser profile",
    "login",
    "password",
    "2fa",
    "mfa",
    "captcha",
    "challenge",
    "click simulation",
    "simulate click",
    "fake click",
    "impression bot",
    "simulate traffic",
    "autosurf",
    "proxy pool",
    "fingerprint",
    "anti-detect",
    "antidetect",
    "worker forward",
    "cloaking",
    "googlebot",
    "adsbot",
    "account pool",
    "ban evasion",
    "cookie登录",
    "cookie接管",
    "登录态",
    "自动登录",
    "密码",
    "绕过2fa",
    "绕过 2fa",
    "验证码",
    "安全挑战",
    "补点击",
    "刷点击",
    "刷展示",
    "模拟自然流量",
    "代理池",
    "指纹",
    "反检测",
    "worker转发",
    "审核页",
    "用户页",
    "账号池",
    "封禁后",
    "规避封禁",
)


def validate_task_type(task_type: str) -> tuple[bool, str | None]:
    normalized = (task_type or "").strip().lower()
    if not normalized:
        return False, "Task type is required."
    if any(keyword in normalized for keyword in FORBIDDEN_TASK_KEYWORDS):
        return (
            False,
            "Authentication, cookie, 2FA, captcha, challenge, recovery, session, click, impression, visit, or traffic simulation tasks are not allowed.",
        )
    if normalized not in TASK_TYPE_VALUES:
        return False, f"Unsupported task type: {task_type}"
    return True, None


def validate_task_text(name: str, notes: str | None = None) -> tuple[bool, str | None]:
    task_text = " ".join([name or "", notes or ""]).lower()
    if any(term in task_text for term in FORBIDDEN_TASK_TEXT_TERMS):
        return (
            False,
            "Task name or notes contain login takeover, cookie, traffic simulation, proxy/fingerprint, cloaking, or account switching semantics. Use risk audit instead.",
        )
    return True, None


def run_task_job(job: TaskJob) -> dict:
    """Run a safe local task and return a structured result."""
    is_valid, error = validate_task_type(job.task_type)
    if is_valid:
        is_valid, error = validate_task_text(job.name, job.notes)
    if not is_valid:
        result = {"ok": False, "message": error}
        now = datetime.utcnow()
        job.last_run_at = now
        job.run_count += 1
        job.failure_count += 1
        job.status = "failed"
        job.last_result = result
        return result

    if job.task_type == "landing_audit_review":
        result = _landing_audit_review(job)
    elif job.task_type == "creative_generation":
        result = _creative_generation(job)
    elif job.task_type == "export_csv":
        result = _export_csv(job)
    elif job.task_type == "export_script_payload":
        result = _export_script_payload(job)
    elif job.task_type == "link_plan_review":
        result = _link_plan_review(job)
    elif job.task_type == "metrics_review":
        result = _metrics_review(job)
    else:
        result = {
            "ok": False,
            "message": f"Unsupported task type: {job.task_type}",
        }

    now = datetime.utcnow()
    job.last_run_at = now
    job.run_count += 1
    if result["ok"]:
        job.success_count += 1
        job.status = "success"
    else:
        job.failure_count += 1
        job.status = "failed"
    if job.schedule_mode == "interval":
        job.next_run_at = now + timedelta(minutes=job.interval_minutes)
    job.last_result = result
    return result


def _landing_audit_review(job: TaskJob) -> dict:
    if not job.offer:
        return {"ok": False, "message": "Offer is required for landing audit review."}
    page = job.offer.latest_landing_page
    if not page:
        return {
            "ok": False,
            "message": "No landing page audit found. Run Offer crawl first.",
        }
    return {
        "ok": True,
        "message": "Landing audit reviewed.",
        "quality_score": page.quality_score,
        "http_status": page.http_status,
        "word_count": page.word_count,
    }


def _creative_generation(job: TaskJob) -> dict:
    if not job.offer:
        return {"ok": False, "message": "Offer is required for creative generation."}
    payloads = generate_creative_sets(job.offer, job.offer.latest_landing_page)
    return {
        "ok": True,
        "message": "Creative generation payload prepared for manual review.",
        "sets": len(payloads),
        "headlines": sum(len(item["headlines"]) for item in payloads),
        "descriptions": sum(len(item["descriptions"]) for item in payloads),
        "keywords": sum(len(item["keywords"]) for item in payloads),
    }


def _export_csv(job: TaskJob) -> dict:
    if not job.campaign_draft:
        return {"ok": False, "message": "Campaign draft is required for CSV export."}
    blockers = campaign_preflight_blockers(job.campaign_draft)
    if blockers:
        return {
            "ok": False,
            "message": "CSV export blocked by campaign preflight.",
            "blockers": blockers,
            "campaign": job.campaign_draft.name,
        }
    csv_text = campaign_to_google_ads_editor_csv(job.campaign_draft)
    return {
        "ok": True,
        "message": "CSV export payload generated for manual download.",
        "bytes": len(csv_text.encode("utf-8")),
        "campaign": job.campaign_draft.name,
    }


def _export_script_payload(job: TaskJob) -> dict:
    if not job.campaign_draft:
        return {
            "ok": False,
            "message": "Campaign draft is required for Scripts JSON export.",
        }
    blockers = campaign_preflight_blockers(job.campaign_draft)
    if blockers:
        return {
            "ok": False,
            "message": "Scripts JSON export blocked by campaign preflight.",
            "blockers": blockers,
            "campaign": job.campaign_draft.name,
        }
    payload = campaign_to_scripts_payload(job.campaign_draft)
    return {
        "ok": True,
        "message": "Scripts JSON payload generated for manual review.",
        "bytes": len(payload.encode("utf-8")),
        "campaign": job.campaign_draft.name,
        "no_cookie_automation": True,
    }


def _link_plan_review(job: TaskJob) -> dict:
    if not job.link_rule:
        return {"ok": False, "message": "Link rule is required for link review."}
    return {
        "ok": True,
        "message": "Link plan reviewed. Manual approval remains required.",
        "current_url": job.link_rule.current_url,
        "candidate_count": len(job.link_rule.candidate_urls or []),
        "require_manual_review": job.link_rule.require_manual_review,
    }


def _metrics_review(job: TaskJob) -> dict:
    if not job.offer:
        return {"ok": False, "message": "Offer is required for metrics review."}
    totals = metric_totals(job.offer.metrics)
    return {
        "ok": True,
        "message": "Metrics reviewed.",
        "clicks": totals["clicks"],
        "cost": round(totals["cost"], 4),
        "revenue": round(totals["revenue"], 4),
        "profit": round(totals["profit"], 4),
        "roi": round(totals["roi"], 6),
    }
