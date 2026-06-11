from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adsworkbench import create_app
from adsworkbench.extensions import db
from adsworkbench.models import (
    AdsAccount,
    AdReviewCase,
    AppointmentLeadReview,
    AttributionReview,
    AuditLog,
    BulkUploadReview,
    BudgetPacingReview,
    BuyerCapacityReview,
    CampaignDraft,
    ConversionSignalReview,
    CrmValueMappingReview,
    CreativeClaimReview,
    CreativeSet,
    CplVerticalReview,
    DecisionWindowReview,
    LeadValidationReview,
    LeadPricingReview,
    LinkRule,
    MetricDaily,
    Offer,
    OfferCapReview,
    OptimizationAction,
    OpportunityAssessment,
    PingPostRoutingReview,
    PortfolioAllocationReview,
    QueryMiningReview,
    ResearchSource,
    RiskAudit,
    ScriptSyncReview,
    SourceQualityReview,
    TaskJob,
    TaxonomyReview,
    VendorContractReview,
    seed_demo_data,
)


HIGH_RISK_CAPABILITIES = [
    "ads_cookie_backend_operation",
    "automated_login_2fa_challenge_bypass",
    "invalid_traffic_click_impression_simulation",
    "proxy_fingerprint_worker_association_evasion",
    "cloaking_review_user_page_mismatch",
    "ban_evasion_account_switching",
]

REQUIRED_ROUTES = [
    "/",
    "/docs",
    "/accounts",
    "/offers",
    "/calculators",
    "/campaigns",
    "/bulk-upload",
    "/scripts-sync",
    "/taxonomy-governance",
    "/attribution",
    "/cpl-verticals",
    "/lead-pricing",
    "/appointment-leads",
    "/buyer-capacity",
    "/lead-validation",
    "/ping-post-routing",
    "/conversion-signals",
    "/crm-value-mapping",
    "/ad-reviews",
    "/metrics/import",
    "/optimization",
    "/query-mining",
    "/decision-windows",
    "/budget-pacing",
    "/portfolio-allocation",
    "/offer-cap-payout",
    "/source-quality",
    "/vendor-contracts",
    "/sources",
    "/risk-audits",
    "/tasks",
    "/links",
    "/logs",
    "/knowledge/adxkit",
    "/knowledge/evidence_matrix",
    "/doc/usage.md",
    "/knowledge/acceptance",
    "/knowledge/risk_index",
    "/knowledge/risk_completion",
    "/knowledge/risk_blueprint",
    "/knowledge/source_library",
    "/knowledge/traceability",
    "/knowledge/design",
    "/knowledge/usage",
    "/knowledge/development",
]

REQUIRED_DOC_PHRASES = {
    "docs/docs_index.md": [
        "端到端验收路径",
        "ADXKit 核心能力对应入口",
        "高风险能力完成入口",
    ],
    "docs/adxkit_breakdown.md": [
        "核心能力验收矩阵",
        "公开能力和行业原理",
        "不交付边界",
    ],
    "docs/acceptance_checklist.md": [
        "Ads 套利行业知识",
        "ADXKit 核心验收证据矩阵",
        "高风险能力完成状态",
    ],
    "docs/ads_arbitrage_source_evidence_matrix.md": [
        "关键结论和来源证据",
        "从来源到系统边界的推导",
        "证据强度分级",
        "信息来源 URL",
    ],
    "docs/requirement_traceability_matrix.md": [
        "验收总览",
        "ADXKit 核心能力追溯",
        "高风险能力追溯",
        "自动验收追溯",
    ],
    "docs/high_risk_completion_audit.md": [
        "逐点完成审计",
        "系统验收路径",
        "当前完成证据",
    ],
    "docs/high_risk_capability_safe_reproduction_blueprint.md": [
        "行业诉求",
        "原理解释",
        "系统落地",
        "统一验收矩阵",
    ],
    "docs/high_risk/README.md": [
        "完成矩阵",
        "原理解释覆盖点",
        "交付形态",
    ],
}

FORBIDDEN_MODEL_COLUMNS = {"tenant_id", "organization_id", "user_id"}


def main() -> None:
    failures: list[str] = []
    evidence: list[str] = []

    _check_docs_mapped(failures, evidence)
    _check_required_docs(failures, evidence)
    _check_env_example(failures, evidence)

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )
    with app.app_context():
        db.create_all()
        seed_demo_data()

        _check_no_multitenant_columns(failures, evidence)
        _check_seeded_core_data(failures, evidence)
        _check_high_risk_source_counts(failures, evidence)
        _check_routes_and_guardrails(app, failures, evidence)

    if failures:
        print("Acceptance audit failed:")
        for item in failures:
            print(f"- {item}")
        print("\nEvidence collected before failure:")
        for item in evidence:
            print(f"- {item}")
        raise SystemExit(1)

    print("Acceptance audit passed.")
    for item in evidence:
        print(f"- {item}")


def _check_docs_mapped(failures: list[str], evidence: list[str]) -> None:
    routes_text = (ROOT / "adsworkbench" / "routes.py").read_text(encoding="utf-8")
    mapped_docs = set(re.findall(r'"([^"]+\.md)"', routes_text))
    all_docs = {
        str(path.relative_to(ROOT / "docs")).replace("\\", "/")
        for path in (ROOT / "docs").rglob("*.md")
    }
    missing = sorted(all_docs - mapped_docs)
    extra = sorted(mapped_docs - all_docs)
    if missing:
        failures.append(f"Markdown docs not reachable through knowledge routes: {missing}")
    if extra:
        failures.append(f"Knowledge route maps missing Markdown files: {extra}")
    evidence.append(f"Knowledge docs mapped: {len(mapped_docs)}/{len(all_docs)}")


def _check_required_docs(failures: list[str], evidence: list[str]) -> None:
    for rel_path, phrases in REQUIRED_DOC_PHRASES.items():
        path = ROOT / rel_path
        if not path.exists():
            failures.append(f"Required doc missing: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                failures.append(f"{rel_path} missing phrase: {phrase}")
        url_count = len(re.findall(r"https?://[^\s)]+", text))
        if rel_path != "docs/high_risk/README.md" and url_count < 1:
            failures.append(f"{rel_path} should include source URLs")
    evidence.append(f"Required acceptance docs checked: {len(REQUIRED_DOC_PHRASES)}")


def _check_env_example(failures: list[str], evidence: list[str]) -> None:
    env_path = ROOT / ".env.example"
    if not env_path.exists():
        failures.append(".env.example missing")
        return
    env_text = env_path.read_text(encoding="utf-8")
    if "DATABASE_URL=mysql+pymysql://ads_user:ads_password@127.0.0.1:3306/ads_workbench?charset=utf8mb4" not in env_text:
        failures.append(".env.example missing MySQL DATABASE_URL")
    for forbidden in ["COOKIE", "SESSION_TOKEN", "PROXY", "FINGERPRINT", "ACCOUNT_POOL"]:
        if forbidden in env_text.upper():
            failures.append(f".env.example contains high-risk config term: {forbidden}")
    evidence.append(".env.example checked for MySQL setup and high-risk config")


def _check_no_multitenant_columns(failures: list[str], evidence: list[str]) -> None:
    found: list[str] = []
    for table in db.metadata.sorted_tables:
        for column in table.columns:
            if column.name in FORBIDDEN_MODEL_COLUMNS:
                found.append(f"{table.name}.{column.name}")
    if found:
        failures.append(f"Multi-tenant columns found despite V1 scope: {found}")
    evidence.append("No tenant_id / organization_id / user_id columns in V1 schema")


def _check_seeded_core_data(failures: list[str], evidence: list[str]) -> None:
    checks = {
        "offers": Offer.query.count(),
        "ads_accounts": AdsAccount.query.count(),
        "ad_review_cases": AdReviewCase.query.count(),
        "bulk_upload_reviews": BulkUploadReview.query.count(),
        "script_sync_reviews": ScriptSyncReview.query.count(),
        "taxonomy_reviews": TaxonomyReview.query.count(),
        "attribution_reviews": AttributionReview.query.count(),
        "cpl_vertical_reviews": CplVerticalReview.query.count(),
        "lead_pricing_reviews": LeadPricingReview.query.count(),
        "appointment_lead_reviews": AppointmentLeadReview.query.count(),
        "buyer_capacity_reviews": BuyerCapacityReview.query.count(),
        "lead_validation_reviews": LeadValidationReview.query.count(),
        "ping_post_routing_reviews": PingPostRoutingReview.query.count(),
        "conversion_signal_reviews": ConversionSignalReview.query.count(),
        "crm_value_mapping_reviews": CrmValueMappingReview.query.count(),
        "opportunity_assessments": OpportunityAssessment.query.count(),
        "creative_claim_reviews": CreativeClaimReview.query.count(),
        "budget_pacing_reviews": BudgetPacingReview.query.count(),
        "decision_window_reviews": DecisionWindowReview.query.count(),
        "offer_cap_reviews": OfferCapReview.query.count(),
        "portfolio_allocation_reviews": PortfolioAllocationReview.query.count(),
        "query_mining_reviews": QueryMiningReview.query.count(),
        "source_quality_reviews": SourceQualityReview.query.count(),
        "vendor_contract_reviews": VendorContractReview.query.count(),
        "creative_sets": CreativeSet.query.count(),
        "campaign_drafts": CampaignDraft.query.count(),
        "metrics_daily": MetricDaily.query.count(),
        "research_sources": ResearchSource.query.count(),
        "risk_audits": RiskAudit.query.count(),
        "task_jobs": TaskJob.query.count(),
        "link_rules": LinkRule.query.count(),
    }
    for name, count in checks.items():
        if count < 1:
            failures.append(f"Seeded core table has no rows: {name}")
    evidence.append(
        "Seeded core data: "
        + ", ".join(f"{name}={count}" for name, count in sorted(checks.items()))
    )


def _check_high_risk_source_counts(failures: list[str], evidence: list[str]) -> None:
    counts: dict[str, int] = {}
    for capability in HIGH_RISK_CAPABILITIES:
        counts[capability] = ResearchSource.query.filter_by(capability=capability).count()
        if counts[capability] < 4:
            failures.append(
                f"High-risk capability has insufficient source rows: {capability}={counts[capability]}"
            )
    total = sum(counts.values())
    if total < 50:
        failures.append(f"High-risk source total should be at least 50, found {total}")
    evidence.append(
        "High-risk source coverage: "
        + ", ".join(f"{capability}={count}" for capability, count in counts.items())
        + f", total={total}"
    )


def _check_routes_and_guardrails(app, failures: list[str], evidence: list[str]) -> None:
    client = app.test_client()
    for route in REQUIRED_ROUTES:
        response = client.get(route)
        if response.status_code != 200:
            failures.append(f"Route failed: {route} -> {response.status_code}")

    docs_response = client.get("/docs")
    if b"markdown-doc" not in docs_response.data or b"doc-table" not in docs_response.data:
        failures.append("/docs did not render Markdown as structured HTML")
    if b"/doc/ads_arbitrage_industry.md" not in docs_response.data:
        failures.append("/docs did not rewrite relative Markdown links to /doc routes")

    campaign = CampaignDraft.query.first()
    if not campaign:
        failures.append("No campaign draft for export checks")
        return
    creative = CreativeSet.query.first()
    if not creative:
        failures.append("No creative set for claim review checks")
    else:
        claim_refresh_response = client.post(
            f"/creatives/{creative.id}/claim-reviews/run",
            follow_redirects=True,
        )
        claim_review = CreativeClaimReview.query.filter_by(
            creative_set_id=creative.id
        ).first()
        if claim_refresh_response.status_code != 200 or not claim_review:
            failures.append("Creative claim review refresh failed")
        elif not claim_review.source_url:
            failures.append("Creative claim review missing source URL")
        else:
            claim_status_response = client.post(
                f"/claim-reviews/{claim_review.id}/status",
                data={"review_status": "rewrite_required"},
                follow_redirects=True,
            )
            if (
                claim_status_response.status_code != 200
                or claim_review.review_status != "rewrite_required"
            ):
                failures.append("Creative claim review status update failed")
            if not AuditLog.query.filter_by(
                entity_type="creative_claim_review",
                entity_id=claim_review.id,
                action="status_update",
            ).first():
                failures.append("Creative claim review status update did not write audit log")

    campaign_status_response = client.post(
        f"/campaigns/{campaign.id}/status",
        data={"status": "approved"},
        follow_redirects=True,
    )
    if campaign_status_response.status_code != 200 or campaign.status != "approved":
        failures.append("Campaign draft approval status update failed")
    if not AuditLog.query.filter_by(
        entity_type="campaign",
        entity_id=campaign.id,
        action="status_update",
    ).first():
        failures.append("Campaign status update did not write audit log")

    blocked_script_response = client.get(
        f"/campaigns/{campaign.id}/export.script.json",
        follow_redirects=True,
    )
    if blocked_script_response.status_code != 200:
        failures.append("Blocked Scripts export redirect failed")
    if not AuditLog.query.filter_by(
        entity_type="campaign",
        entity_id=campaign.id,
        action="export_blocked",
    ).first():
        failures.append("Unresolved preflight did not block campaign export")

    claim_review = (
        CreativeClaimReview.query.filter_by(creative_set_id=creative.id).first()
        if creative
        else None
    )
    if claim_review:
        client.post(
            f"/claim-reviews/{claim_review.id}/status",
            data={"review_status": "approved"},
            follow_redirects=True,
        )
    for case in AdReviewCase.query.filter_by(campaign_draft_id=campaign.id).all():
        client.post(
            f"/ad-reviews/{case.id}/status",
            data={"status": "fixed"},
            follow_redirects=True,
        )

    script_response = client.get(f"/campaigns/{campaign.id}/export.script.json")
    if script_response.status_code != 200 or b"no_cookie_automation" not in script_response.data:
        failures.append("Scripts JSON export missing no_cookie_automation safety flag")

    ad_review_response = client.post(
        "/ad-reviews",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "creative_set_id": str(campaign.creative_set_id or ""),
            "object_type": "ad",
            "object_ref": "Acceptance RSA draft",
            "policy_topic": "Destination requirements",
            "severity": "medium",
            "status": "open",
            "final_url": campaign.final_url,
            "expanded_url": campaign.final_url,
            "finding": "Acceptance case records a destination review issue.",
            "change_summary": "Verify final URL, mobile page, claim evidence, and tracking parameters.",
            "evidence_urls": "https://support.google.com/adspolicy/answer/6368661",
            "appeal_text": "Appeal only after the destination and ad claim are fixed.",
            "reviewer": "acceptance",
        },
        follow_redirects=True,
    )
    ad_review_case = AdReviewCase.query.filter_by(object_ref="Acceptance RSA draft").first()
    if ad_review_response.status_code != 200 or not ad_review_case:
        failures.append("Ad review case creation failed")
    else:
        ad_review_status_response = client.post(
            f"/ad-reviews/{ad_review_case.id}/status",
            data={"status": "appeal_ready"},
            follow_redirects=True,
        )
        if ad_review_status_response.status_code != 200 or ad_review_case.status != "appeal_ready":
            failures.append("Ad review case status update failed")
        if not AuditLog.query.filter_by(
            entity_type="ad_review_case",
            entity_id=ad_review_case.id,
            action="status_update",
        ).first():
            failures.append("Ad review case status update did not write audit log")

    client.post(
        "/ad-reviews",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "creative_set_id": str(campaign.creative_set_id or ""),
            "object_type": "ad",
            "object_ref": "Acceptance unsafe ad review",
            "policy_topic": "Circumventing systems",
            "severity": "high",
            "status": "open",
            "finding": "Use cloaking review page and user page split.",
            "change_summary": "Bypass review with worker forward.",
            "evidence_urls": "https://support.google.com/adspolicy/answer/15938075",
            "appeal_text": "Switch account after rejection.",
        },
        follow_redirects=True,
    )
    if AdReviewCase.query.filter_by(object_ref="Acceptance unsafe ad review").first():
        failures.append("Unsafe ad review bypass case was accepted")

    decision_window_response = client.post(
        "/decision-windows",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance maturity gate",
            "data_status": "partial",
            "revenue_status": "accepted",
            "conversion_lag_days": "2",
            "approval_lag_days": "1",
            "settlement_lag_days": "0",
            "sample_clicks": "35",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "source_quality": "watch",
            "incident_state": "clean",
            "status": "open",
            "notes": "Acceptance gate records wait-loss before budget change.",
            "source_urls": "https://support.google.com/google-ads/answer/9347141",
        },
        follow_redirects=True,
    )
    decision_window = DecisionWindowReview.query.filter_by(
        name="Acceptance maturity gate"
    ).first()
    if decision_window_response.status_code != 200 or not decision_window:
        failures.append("Decision window review creation failed")
    elif not decision_window.blockers:
        failures.append("Decision window review did not record maturity blockers")
    else:
        decision_status_response = client.post(
            f"/decision-windows/{decision_window.id}/status",
            data={"status": "waiting"},
            follow_redirects=True,
        )
        if (
            decision_status_response.status_code != 200
            or decision_window.status != "waiting"
        ):
            failures.append("Decision window status update failed")
        if not AuditLog.query.filter_by(
            entity_type="decision_window_review",
            entity_id=decision_window.id,
            action="status_update",
        ).first():
            failures.append("Decision window status update did not write audit log")

    budget_pacing_response = client.post(
        "/budget-pacing",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance blocked budget ramp",
            "current_daily_budget": "50",
            "proposed_daily_budget": "100",
            "test_budget": "120",
            "hard_stop": "125",
            "spend_to_date": "118",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "safe_cpc": "0.40",
            "actual_cpc": "0.70",
            "sample_clicks": "20",
            "data_status": "partial",
            "revenue_status": "estimated",
            "source_quality": "watch",
            "incident_state": "recent",
            "cash_buffer_days": "7",
            "overdelivery_buffer_percent": "20",
            "status": "open",
            "notes": "Acceptance budget gate records blockers before any manual budget change.",
            "source_urls": "https://support.google.com/google-ads/answer/10702522",
        },
        follow_redirects=True,
    )
    budget_review = BudgetPacingReview.query.filter_by(
        name="Acceptance blocked budget ramp"
    ).first()
    if budget_pacing_response.status_code != 200 or not budget_review:
        failures.append("Budget pacing review creation failed")
    elif not budget_review.blockers:
        failures.append("Budget pacing review did not record blockers")
    else:
        budget_status_response = client.post(
            f"/budget-pacing/{budget_review.id}/status",
            data={"status": "blocked"},
            follow_redirects=True,
        )
        if budget_status_response.status_code != 200 or budget_review.status != "blocked":
            failures.append("Budget pacing status update failed")
        if not AuditLog.query.filter_by(
            entity_type="budget_pacing_review",
            entity_id=budget_review.id,
                action="status_update",
            ).first():
            failures.append("Budget pacing status update did not write audit log")

    portfolio_response = client.post(
        "/portfolio-allocation",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance concentrated portfolio",
            "portfolio_bucket": "scale",
            "monthly_media_budget": "2000",
            "proposed_allocation": "650",
            "spend_to_date": "1600",
            "reported_revenue": "400",
            "pending_revenue": "380",
            "approved_revenue": "0",
            "finalized_revenue": "0",
            "paid_revenue": "0",
            "deducted_revenue": "70",
            "single_offer_exposure_percent": "42",
            "single_source_exposure_percent": "55",
            "single_account_exposure_percent": "48",
            "single_partner_exposure_percent": "62",
            "cash_reserve_days": "7",
            "source_quality": "watch",
            "policy_risk": "high",
            "incident_state": "recent",
            "status": "open",
            "notes": "Acceptance portfolio gate records concentration blockers.",
            "source_urls": "https://support.google.com/google-ads/answer/10702522",
        },
        follow_redirects=True,
    )
    portfolio_review = PortfolioAllocationReview.query.filter_by(
        name="Acceptance concentrated portfolio"
    ).first()
    if portfolio_response.status_code != 200 or not portfolio_review:
        failures.append("Portfolio allocation review creation failed")
    elif not portfolio_review.blockers:
        failures.append("Portfolio allocation review did not record blockers")
    else:
        portfolio_status_response = client.post(
            f"/portfolio-allocation/{portfolio_review.id}/status",
            data={"status": "quarantine"},
            follow_redirects=True,
        )
        if (
            portfolio_status_response.status_code != 200
            or portfolio_review.status != "quarantine"
        ):
            failures.append("Portfolio allocation status update failed")
        if not AuditLog.query.filter_by(
            entity_type="portfolio_allocation_review",
            entity_id=portfolio_review.id,
            action="status_update",
        ).first():
            failures.append("Portfolio allocation status update did not write audit log")

    offer_cap_response = client.post(
        "/offer-cap-payout",
        data={
            "offer_id": str(campaign.offer_id),
            "replacement_offer_id": "",
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance capped offer",
            "offer_status": "capped",
            "buyer_capacity_status": "near_cap",
            "cap_type": "daily_conversion",
            "cap_period": "daily",
            "cap_limit": "20",
            "cap_used": "20",
            "expected_next_conversions": "6",
            "days_since_cap_update": "3",
            "current_payout": "42",
            "new_payout": "28",
            "approval_rate_percent": "45",
            "paid_rate_percent": "35",
            "deduction_rate_percent": "25",
            "replacement_status": "draft",
            "replacement_fit_score": "40",
            "source_quality": "watch",
            "policy_risk": "medium",
            "status": "open",
            "notes": "Acceptance cap gate blocks traffic until cap and payout evidence are reviewed.",
            "source_urls": "https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps",
        },
        follow_redirects=True,
    )
    offer_cap_review = OfferCapReview.query.filter_by(
        name="Acceptance capped offer"
    ).first()
    if offer_cap_response.status_code != 200 or not offer_cap_review:
        failures.append("Offer cap review creation failed")
    elif not offer_cap_review.blockers:
        failures.append("Offer cap review did not record blockers")
    else:
        offer_cap_status_response = client.post(
            f"/offer-cap-payout/{offer_cap_review.id}/status",
            data={"status": "pause_traffic"},
            follow_redirects=True,
        )
        if (
            offer_cap_status_response.status_code != 200
            or offer_cap_review.status != "pause_traffic"
        ):
            failures.append("Offer cap status update failed")
        if not AuditLog.query.filter_by(
            entity_type="offer_cap_review",
            entity_id=offer_cap_review.id,
            action="status_update",
        ).first():
            failures.append("Offer cap status update did not write audit log")

    unsafe_source_count = SourceQualityReview.query.count()
    client.post(
        "/source-quality",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe hidden source",
            "entity_type": "placement",
            "source_name": "hide referrer proxy pool",
            "publisher_name": "Unknown",
            "placement_ref": "unknown placement",
            "subid": "bad_subid",
            "network": "Unknown",
            "country": "US",
            "device": "mobile",
            "sample_url": "https://example.com/hidden-source",
            "transparency_level": "opaque",
            "tracking_completeness_percent": "40",
            "intent_fit_score": "20",
            "clicks": "500",
            "sessions": "120",
            "cost": "200",
            "reported_revenue": "300",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "deducted_revenue": "80",
            "invalid_click_rate_percent": "12",
            "complaint_count": "5",
            "buyer_reject_rate_percent": "65",
            "policy_issue_state": "active",
            "stop_control": "none",
            "consistency_days": "1",
            "status": "open",
            "notes": "Unsafe source quality text mentions proxy and hidden source.",
            "source_urls": "https://support.google.com/adsense/answer/1348722",
        },
        follow_redirects=True,
    )
    if SourceQualityReview.query.count() != unsafe_source_count:
        failures.append("Unsafe hidden source quality plan was accepted")

    source_quality_response = client.post(
        "/source-quality",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance low source quality",
            "entity_type": "placement",
            "source_name": "Unknown vendor",
            "publisher_name": "Unknown publisher",
            "placement_ref": "untagged placement",
            "subid": "subid_001",
            "network": "Manual partner",
            "country": "US",
            "device": "mobile",
            "sample_url": "https://example.com/cloud-backup",
            "transparency_level": "opaque",
            "tracking_completeness_percent": "40",
            "intent_fit_score": "20",
            "clicks": "500",
            "sessions": "120",
            "cost": "200",
            "reported_revenue": "300",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "deducted_revenue": "80",
            "invalid_click_rate_percent": "12",
            "complaint_count": "5",
            "buyer_reject_rate_percent": "65",
            "policy_issue_state": "active",
            "stop_control": "none",
            "consistency_days": "1",
            "status": "open",
            "notes": "Acceptance source gate blocks low-quality placement traffic.",
            "source_urls": "https://support.google.com/adsense/answer/1348722",
        },
        follow_redirects=True,
    )
    source_quality_review = SourceQualityReview.query.filter_by(
        name="Acceptance low source quality"
    ).first()
    if source_quality_response.status_code != 200 or not source_quality_review:
        failures.append("Source quality review creation failed")
    elif not source_quality_review.blockers:
        failures.append("Source quality review did not record blockers")
    else:
        source_quality_status_response = client.post(
            f"/source-quality/{source_quality_review.id}/status",
            data={"status": "blocklist"},
            follow_redirects=True,
        )
        if (
            source_quality_status_response.status_code != 200
            or source_quality_review.status != "blocklist"
        ):
            failures.append("Source quality status update failed")
        if not AuditLog.query.filter_by(
            entity_type="source_quality_review",
            entity_id=source_quality_review.id,
            action="status_update",
        ).first():
            failures.append("Source quality status update did not write audit log")

    unsafe_vendor_count = VendorContractReview.query.count()
    client.post(
        "/vendor-contracts",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe traffic vendor",
            "vendor_name": "hidden source proxy supplier",
            "vendor_type": "traffic_vendor",
            "io_number": "IO-BAD",
            "line_item_ref": "undisclosed source",
            "contract_status": "prospect",
            "pricing_model": "cpc",
            "source_detail_level": "opaque",
            "stop_control": "none",
            "tracking_completeness_percent": "20",
            "report_delay_days": "10",
            "discrepancy_rate_percent": "30",
            "invalid_traffic_rate_percent": "15",
            "buyer_reject_rate_percent": "70",
            "payment_terms_days": "0",
            "budget_cap": "500",
            "spend_to_date": "300",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "invoice_amount": "300",
            "disputed_amount": "200",
            "refund_credit_amount": "0",
            "makegood_value": "0",
            "dispute_response_days": "12",
            "refund_terms_status": "missing",
            "policy_issue_state": "active",
            "status": "open",
            "notes": "Unsafe vendor text mentions hidden source and proxy.",
            "source_urls": "https://support.google.com/adsense/answer/3332805",
        },
        follow_redirects=True,
    )
    if VendorContractReview.query.count() != unsafe_vendor_count:
        failures.append("Unsafe hidden-source vendor contract was accepted")

    vendor_contract_response = client.post(
        "/vendor-contracts",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance vendor dispute",
            "vendor_name": "Unknown media partner",
            "vendor_type": "traffic_vendor",
            "io_number": "IO-ACCEPT-001",
            "line_item_ref": "US mobile push",
            "contract_status": "watchlist",
            "pricing_model": "cpc",
            "source_detail_level": "opaque",
            "stop_control": "none",
            "tracking_completeness_percent": "45",
            "report_delay_days": "10",
            "discrepancy_rate_percent": "35",
            "invalid_traffic_rate_percent": "12",
            "buyer_reject_rate_percent": "65",
            "payment_terms_days": "0",
            "budget_cap": "500",
            "spend_to_date": "300",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "invoice_amount": "300",
            "disputed_amount": "200",
            "refund_credit_amount": "0",
            "makegood_value": "0",
            "dispute_response_days": "12",
            "refund_terms_status": "missing",
            "policy_issue_state": "active",
            "status": "open",
            "notes": "Acceptance vendor dispute should open evidence review.",
            "source_urls": "https://support.google.com/adsense/answer/3332805",
        },
        follow_redirects=True,
    )
    vendor_contract_review = VendorContractReview.query.filter_by(
        name="Acceptance vendor dispute"
    ).first()
    if vendor_contract_response.status_code != 200 or not vendor_contract_review:
        failures.append("Vendor contract review creation failed")
    elif not vendor_contract_review.blockers:
        failures.append("Vendor contract review did not record blockers")
    else:
        vendor_status_response = client.post(
            f"/vendor-contracts/{vendor_contract_review.id}/status",
            data={"status": "dispute_open"},
            follow_redirects=True,
        )
        if (
            vendor_status_response.status_code != 200
            or vendor_contract_review.status != "dispute_open"
        ):
            failures.append("Vendor contract status update failed")
        if not AuditLog.query.filter_by(
            entity_type="vendor_contract_review",
            entity_id=vendor_contract_review.id,
            action="status_update",
        ).first():
            failures.append("Vendor contract status update did not write audit log")

    unsafe_query_count = QueryMiningReview.query.count()
    client.post(
        "/query-mining",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe query mining",
            "date_window": "2026-06-01..2026-06-07",
            "ads_customer_id": "123-456-7890",
            "campaign_ref": "Acceptance Search",
            "ad_group_ref": "broad",
            "source_file_hash": "acceptance",
            "keyword_text": "cloud backup",
            "keyword_match_type": "broad",
            "search_term": "simulate search with proxy pool",
            "search_term_match_type": "broad",
            "query_intent": "unknown",
            "intent_fit_score": "20",
            "network": "google_search",
            "device": "desktop",
            "country": "US",
            "landing_version": "v1",
            "clicks": "100",
            "sessions": "0",
            "conversions": "0",
            "cost": "80",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "buyer_reject_rate_percent": "0",
            "conversion_lag_days": "7",
            "revenue_status": "none",
            "data_status": "mature",
            "policy_risk": "high",
            "status": "open",
            "notes": "Unsafe query mining mentions proxy and simulated search.",
            "source_urls": "https://support.google.com/google-ads/answer/2472708",
        },
        follow_redirects=True,
    )
    if QueryMiningReview.query.count() != unsafe_query_count:
        failures.append("Unsafe simulated query mining plan was accepted")

    query_mining_response = client.post(
        "/query-mining",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance support query negative",
            "date_window": "2026-06-01..2026-06-07",
            "ads_customer_id": "123-456-7890",
            "campaign_ref": "Acceptance Search",
            "ad_group_ref": "broad",
            "source_file_hash": "acceptance",
            "keyword_text": "cloud backup",
            "keyword_match_type": "broad",
            "search_term": "cloud backup customer service login",
            "search_term_match_type": "broad",
            "query_intent": "support",
            "intent_fit_score": "20",
            "network": "google_search",
            "device": "desktop",
            "country": "US",
            "landing_version": "v1",
            "clicks": "120",
            "sessions": "80",
            "conversions": "0",
            "cost": "96",
            "approved_revenue": "0",
            "paid_revenue": "0",
            "buyer_reject_rate_percent": "55",
            "conversion_lag_days": "7",
            "revenue_status": "none",
            "data_status": "mature",
            "policy_risk": "high",
            "brand_or_official": "on",
            "support_or_login": "on",
            "status": "open",
            "notes": "Acceptance query review should propose a negative keyword and policy review.",
            "source_urls": "https://support.google.com/google-ads/answer/2472708",
        },
        follow_redirects=True,
    )
    query_review = QueryMiningReview.query.filter_by(
        name="Acceptance support query negative"
    ).first()
    if query_mining_response.status_code != 200 or not query_review:
        failures.append("Query mining review creation failed")
    elif not query_review.blockers:
        failures.append("Query mining review did not record blockers")
    else:
        query_status_response = client.post(
            f"/query-mining/{query_review.id}/status",
            data={"status": "negative_proposed"},
            follow_redirects=True,
        )
        if (
            query_status_response.status_code != 200
            or query_review.status != "negative_proposed"
        ):
            failures.append("Query mining status update failed")
        if not AuditLog.query.filter_by(
            entity_type="query_mining_review",
            entity_id=query_review.id,
            action="status_update",
        ).first():
            failures.append("Query mining status update did not write audit log")

    unsafe_bulk_count = BulkUploadReview.query.count()
    client.post(
        "/bulk-upload",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe auto post",
            "export_type": "scripts_preview",
            "batch_id": "auto post with cookie",
            "csv_hash": "bad",
            "payload_hash": "bad",
            "target_customer_id": "123-456-7890",
            "account_timezone": "America/New_York",
            "currency": "USD",
            "row_count": "100",
            "keyword_count": "100",
            "ad_count": "10",
            "url_change_count": "1",
            "expected_budget_delta": "500",
            "high_risk_change_count": "2",
            "preflight_status": "blocked",
            "preview_status": "errors",
            "editor_check_status": "errors",
            "post_status": "not_posted",
            "status": "open",
            "notes": "Unsafe bulk upload mentions cookie auto post.",
            "source_urls": "https://support.google.com/google-ads/editor/answer/56368",
        },
        follow_redirects=True,
    )
    if BulkUploadReview.query.count() != unsafe_bulk_count:
        failures.append("Unsafe auto-post bulk upload plan was accepted")

    bulk_response = client.post(
        "/bulk-upload",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance bulk preview errors",
            "export_type": "editor_csv",
            "batch_id": "BULK-ACCEPT-001",
            "csv_hash": "acceptance-hash",
            "payload_hash": "",
            "target_customer_id": "123-456-7890",
            "account_timezone": "America/New_York",
            "currency": "USD",
            "row_count": "600",
            "keyword_count": "250",
            "ad_count": "30",
            "url_change_count": "3",
            "expected_budget_delta": "600",
            "high_risk_change_count": "2",
            "preflight_status": "blocked",
            "preview_status": "errors",
            "editor_check_status": "errors",
            "post_status": "not_posted",
            "default_paused": "on",
            "status": "open",
            "notes": "Acceptance bulk upload should block posting until preview errors are fixed.",
            "source_urls": "https://support.google.com/google-ads/editor/answer/56368",
        },
        follow_redirects=True,
    )
    bulk_review = BulkUploadReview.query.filter_by(
        name="Acceptance bulk preview errors"
    ).first()
    if bulk_response.status_code != 200 or not bulk_review:
        failures.append("Bulk upload review creation failed")
    elif not bulk_review.blockers:
        failures.append("Bulk upload review did not record blockers")
    else:
        bulk_status_response = client.post(
            f"/bulk-upload/{bulk_review.id}/status",
            data={"status": "blocked"},
            follow_redirects=True,
        )
        if (
            bulk_status_response.status_code != 200
            or bulk_review.status != "blocked"
        ):
            failures.append("Bulk upload status update failed")
        if not AuditLog.query.filter_by(
            entity_type="bulk_upload_review",
            entity_id=bulk_review.id,
            action="status_update",
        ).first():
            failures.append("Bulk upload status update did not write audit log")

    unsafe_sync_count = ScriptSyncReview.query.count()
    client.post(
        "/scripts-sync",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe cookie sync",
            "auth_mode": "scripts_authorized",
            "sync_type": "metrics_daily",
            "script_name": "auto login cookie sync",
            "customer_id": "123-456-7890",
            "date_range": "TODAY",
            "account_timezone": "America/New_York",
            "currency": "USD",
            "query_or_report": "campaign metrics",
            "source_snapshot_hash": "bad",
            "payload_hash": "bad",
            "row_count": "10",
            "freshness_minutes": "15",
            "error_count": "0",
            "warning_count": "0",
            "data_status": "provisional",
            "revenue_status": "estimated",
            "conflict_status": "clean",
            "external_change_count": "0",
            "rerun_window_days": "1",
            "preview_only": "on",
            "notes": "Unsafe sync mentions cookie auto login.",
            "source_urls": "https://developers.google.com/google-ads/scripts/docs/concepts/reports",
        },
        follow_redirects=True,
    )
    if ScriptSyncReview.query.count() != unsafe_sync_count:
        failures.append("Unsafe cookie script sync plan was accepted")

    sync_response = client.post(
        "/scripts-sync",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance Scripts stale conflict",
            "auth_mode": "scripts_authorized",
            "sync_type": "metrics_daily",
            "script_name": "Daily Metrics Snapshot Preview",
            "customer_id": "123-456-7890",
            "date_range": "LAST_7_DAYS",
            "account_timezone": "America/New_York",
            "currency": "USD",
            "query_or_report": "campaign metrics daily GAQL",
            "source_snapshot_hash": "accept-source-hash",
            "payload_hash": "accept-query-hash",
            "row_count": "35",
            "freshness_minutes": "2880",
            "error_count": "0",
            "warning_count": "7",
            "data_status": "settling",
            "revenue_status": "estimated",
            "conflict_status": "stale_payload",
            "external_change_count": "1",
            "rerun_window_days": "0",
            "preview_only": "on",
            "human_review": "on",
            "notes": "Acceptance sync should require rerun before import.",
            "source_urls": "https://developers.google.com/google-ads/scripts/docs/concepts/reports",
        },
        follow_redirects=True,
    )
    sync_review = ScriptSyncReview.query.filter_by(
        name="Acceptance Scripts stale conflict"
    ).first()
    if sync_response.status_code != 200 or not sync_review:
        failures.append("Script sync review creation failed")
    elif not sync_review.blockers:
        failures.append("Script sync review did not record blockers")
    else:
        sync_status_response = client.post(
            f"/scripts-sync/{sync_review.id}/status",
            data={"status": "conflict_review"},
            follow_redirects=True,
        )
        if (
            sync_status_response.status_code != 200
            or sync_review.status != "conflict_review"
        ):
            failures.append("Script sync status update failed")
        if not AuditLog.query.filter_by(
            entity_type="script_sync_review",
            entity_id=sync_review.id,
            action="status_update",
        ).first():
            failures.append("Script sync status update did not write audit log")

    unsafe_taxonomy_count = TaxonomyReview.query.count()
    client.post(
        "/taxonomy-governance",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe PII taxonomy",
            "campaign_name": "gads-us-en-cloudbackup-ofr001-compare-search-mobile-202606-t001",
            "ad_group_name": "compare-cloudbackup-smallbiz-phrase-lpA-ang_compare_cost",
            "labels_text": "lifecycle:test,risk:claim_review,experiment:exp_202606_001,batch:batch_202606_editor_csv",
            "utm_source": "gads",
            "utm_medium": "cpc",
            "utm_campaign": "{campaignid}",
            "utm_id": "ofr001-202606-t001",
            "utm_content": "{adgroupid}",
            "utm_term": "{keyword}",
            "valuetrack_template": "cid={campaignid}&email=test@example.com",
            "custom_parameter_map": "{_offer}=ofr001",
            "subid_map": "subid1=email=user@example.com",
            "dimension_dictionary_version": "dim-2026-06",
            "parameter_map_version": "utm-subid-v1",
            "landing_version": "lpA",
            "link_version": "lnk1",
            "creative_version": "ang1",
            "payload_hash": "bad",
            "report_join_gap_count": "0",
            "no_pii_in_url": "on",
            "no_sensitive_attributes": "on",
            "notes": "Unsafe taxonomy leaks email in subid.",
            "source_urls": "https://support.google.com/analytics/answer/10917952",
        },
        follow_redirects=True,
    )
    if TaxonomyReview.query.count() != unsafe_taxonomy_count:
        failures.append("Unsafe PII taxonomy plan was accepted")

    unsafe_attribution_count = AttributionReview.query.count()
    client.post(
        "/attribution",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe fake lift",
            "test_type": "geo_holdout",
            "attribution_model": "data_driven",
            "hypothesis": "Fabricate lift and auto apply winner after fake control.",
            "treatment_scope": "US generic search",
            "control_scope": "fake control",
            "split_method": "geo holdout",
            "date_window": "2026-06-01..2026-06-14",
            "primary_metric": "incremental revenue",
            "guardrail_metrics": "brand query, organic sessions",
            "attributed_revenue": "500",
            "treatment_revenue": "900",
            "control_revenue": "300",
            "ad_cost": "120",
            "variable_cost": "30",
            "attributed_conversions": "12",
            "incremental_conversions": "8",
            "sample_size": "600",
            "confidence_level": "85",
            "holdout_quality": "clean",
            "revenue_status": "approved",
            "data_status": "mature",
            "brand_cannibalization_risk": "low",
            "organic_cannibalization_risk": "low",
            "remarketing_cannibalization_risk": "low",
            "pmax_broad_overlap_risk": "low",
            "change_history_clean": "on",
            "single_variable_test": "on",
            "approved_paid_evidence": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe attribution case mentions fake conversion and auto apply winner.",
            "source_urls": "https://support.google.com/google-ads/answer/6261395",
        },
        follow_redirects=True,
    )
    if AttributionReview.query.count() != unsafe_attribution_count:
        failures.append("Unsafe fake attribution lift plan was accepted")

    attribution_response = client.post(
        "/attribution",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance weak cannibalization review",
            "test_type": "pre_post",
            "attribution_model": "data_driven",
            "hypothesis": "Reported revenue may be cannibalized from brand and organic demand.",
            "treatment_scope": "Brand-adjacent broad match queries",
            "control_scope": "No clean holdout is available yet",
            "split_method": "pre post comparison",
            "date_window": "2026-06-01..2026-06-07",
            "primary_metric": "incremental approved revenue",
            "guardrail_metrics": "brand query, organic sessions, buyer reject rate",
            "attributed_revenue": "600",
            "treatment_revenue": "500",
            "control_revenue": "520",
            "ad_cost": "180",
            "variable_cost": "30",
            "attributed_conversions": "14",
            "incremental_conversions": "0",
            "sample_size": "120",
            "confidence_level": "45",
            "holdout_quality": "weak",
            "revenue_status": "submitted",
            "data_status": "fresh",
            "brand_cannibalization_risk": "high",
            "organic_cannibalization_risk": "high",
            "remarketing_cannibalization_risk": "medium",
            "pmax_broad_overlap_risk": "high",
            "status": "open",
            "notes": "Acceptance review should stop or freeze until holdout and paid evidence exist.",
            "source_urls": "https://support.google.com/google-ads/answer/6259715",
        },
        follow_redirects=True,
    )
    attribution_review = AttributionReview.query.filter_by(
        name="Acceptance weak cannibalization review"
    ).first()
    if attribution_response.status_code != 200 or not attribution_review:
        failures.append("Attribution review creation failed")
    elif not attribution_review.blockers:
        failures.append("Attribution review did not record blockers")
    elif attribution_review.recommended_action != "stop_or_freeze":
        failures.append("Attribution review did not stop weak incremental result")
    else:
        attribution_status_response = client.post(
            f"/attribution/{attribution_review.id}/status",
            data={"status": "cannibalization_review"},
            follow_redirects=True,
        )
        if (
            attribution_status_response.status_code != 200
            or attribution_review.status != "cannibalization_review"
        ):
            failures.append("Attribution status update failed")
        if not AuditLog.query.filter_by(
            entity_type="attribution_review",
            entity_id=attribution_review.id,
            action="status_update",
        ).first():
            failures.append("Attribution status update did not write audit log")

    unsafe_cpl_count = CplVerticalReview.query.count()
    client.post(
        "/cpl-verticals",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe CPL fake lead plan",
            "vertical": "insurance",
            "subvertical": "Medicare",
            "country": "US",
            "buyer_type": "network",
            "payout_model": "CPL",
            "payout_amount": "65",
            "estimated_cpc": "4",
            "landing_cvr_percent": "12",
            "accepted_rate_percent": "80",
            "qualified_rate_percent": "70",
            "paid_rate_percent": "60",
            "deduction_rate_percent": "5",
            "chargeback_rate_percent": "2",
            "feedback_lag_days": "3",
            "contact_sla_minutes": "5",
            "qualification_fields": "fake lead and fake phone source",
            "sensitive_fields": "age bucket",
            "reject_reason_map": "bad geo, duplicate",
            "accepted_definition": "accepted by buyer",
            "paid_definition": "paid by invoice",
            "policy_requirements": "bypass certification",
            "forbidden_claims": "guaranteed approval",
            "consent_disclosure_status": "channel_specific",
            "buyer_terms_status": "approved",
            "source_quality": "low",
            "policy_risk": "low",
            "data_sensitivity": "medium",
            "required_fields_mapped": "on",
            "reject_reason_map_ready": "on",
            "accepted_definition_clear": "on",
            "paid_definition_clear": "on",
            "pii_minimization": "on",
            "license_required": "on",
            "license_evidence_present": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe CPL case mentions auto submit fake form.",
            "source_urls": "https://support.google.com/adspolicy/answer/6020956",
        },
        follow_redirects=True,
    )
    if CplVerticalReview.query.count() != unsafe_cpl_count:
        failures.append("Unsafe fake CPL lead plan was accepted")

    cpl_response = client.post(
        "/cpl-verticals",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance weak debt lead vertical",
            "vertical": "loan_debt",
            "subvertical": "debt relief",
            "country": "US",
            "buyer_type": "lead buyer",
            "payout_model": "CPL",
            "payout_amount": "80",
            "estimated_cpc": "8",
            "landing_cvr_percent": "4",
            "accepted_rate_percent": "35",
            "qualified_rate_percent": "25",
            "paid_rate_percent": "15",
            "deduction_rate_percent": "35",
            "chargeback_rate_percent": "18",
            "feedback_lag_days": "30",
            "contact_sla_minutes": "90",
            "qualification_fields": "state, debt amount, income range",
            "sensitive_fields": "debt amount and income range require minimization",
            "reject_reason_map": "",
            "accepted_definition": "",
            "paid_definition": "",
            "policy_requirements": "HEC and financial services review needed",
            "forbidden_claims": "guaranteed approval, erase debt, government program",
            "consent_disclosure_status": "generic",
            "buyer_terms_status": "draft",
            "source_quality": "medium",
            "policy_risk": "high",
            "data_sensitivity": "high",
            "status": "open",
            "notes": "Acceptance CPL vertical should block scaling until terms, consent and economics are fixed.",
            "source_urls": "https://support.google.com/adspolicy/answer/143465",
        },
        follow_redirects=True,
    )
    cpl_review = CplVerticalReview.query.filter_by(
        name="Acceptance weak debt lead vertical"
    ).first()
    if cpl_response.status_code != 200 or not cpl_review:
        failures.append("CPL vertical review creation failed")
    elif not cpl_review.blockers:
        failures.append("CPL vertical review did not record blockers")
    elif cpl_review.recommended_action != "policy_review_first":
        failures.append("CPL vertical review did not require policy review")
    else:
        cpl_status_response = client.post(
            f"/cpl-verticals/{cpl_review.id}/status",
            data={"status": "policy_review"},
            follow_redirects=True,
        )
        if (
            cpl_status_response.status_code != 200
            or cpl_review.status != "policy_review"
        ):
            failures.append("CPL vertical status update failed")
        if not AuditLog.query.filter_by(
            entity_type="cpl_vertical_review",
            entity_id=cpl_review.id,
            action="status_update",
        ).first():
            failures.append("CPL vertical status update did not write audit log")

    unsafe_lead_pricing_count = LeadPricingReview.query.count()
    client.post(
        "/lead-pricing",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe fake paid report",
            "buyer_name": "hidden source buyer",
            "vertical": "loan_debt",
            "geo": "US",
            "source_type": "search",
            "exclusivity": "exclusive",
            "payout_model": "qualified_cpl",
            "headline_payout": "120",
            "unit_payout": "90",
            "proposed_payout": "110",
            "minimum_acceptable_payout": "80",
            "currency": "USD",
            "estimated_cpc": "4",
            "click_to_lead_rate_percent": "8",
            "accepted_rate_percent": "80",
            "qualified_rate_percent": "70",
            "approval_rate_percent": "75",
            "paid_rate_percent": "70",
            "return_rate_percent": "5",
            "scrub_buffer_percent": "5",
            "chargeback_rate_percent": "2",
            "variable_cost_per_click": "0.02",
            "tracking_cost_per_click": "0.01",
            "content_cost_per_click": "0.01",
            "cashflow_cost_percent": "2",
            "cap_limit": "100",
            "expected_volume": "50",
            "return_window_days": "14",
            "payment_term_days": "15",
            "quality_evidence_status": "paid_cohort",
            "source_transparency": "buyer_approved",
            "consent_evidence": "channel_specific",
            "reject_reason_map_ready": "on",
            "invoice_evidence": "on",
            "dispute_reserve_present": "on",
            "buyer_terms_status": "approved",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe acceptance case mentions fake paid report and fake invoice.",
            "source_urls": "https://support.google.com/google-ads/answer/3419241",
        },
        follow_redirects=True,
    )
    if LeadPricingReview.query.count() != unsafe_lead_pricing_count:
        failures.append("Unsafe fake lead pricing report was accepted")

    lead_pricing_response = client.post(
        "/lead-pricing",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance weak lead payout",
            "buyer_name": "Draft buyer",
            "vertical": "loan_debt",
            "geo": "US",
            "source_type": "search",
            "exclusivity": "exclusive",
            "payout_model": "qualified_cpl",
            "headline_payout": "120",
            "unit_payout": "0",
            "proposed_payout": "55",
            "minimum_acceptable_payout": "80",
            "currency": "USD",
            "estimated_cpc": "6",
            "click_to_lead_rate_percent": "3",
            "accepted_rate_percent": "35",
            "qualified_rate_percent": "25",
            "approval_rate_percent": "30",
            "paid_rate_percent": "25",
            "return_rate_percent": "30",
            "scrub_buffer_percent": "30",
            "chargeback_rate_percent": "15",
            "variable_cost_per_click": "0.15",
            "tracking_cost_per_click": "0.03",
            "content_cost_per_click": "0.05",
            "cashflow_cost_percent": "8",
            "cap_limit": "20",
            "expected_volume": "80",
            "return_window_days": "45",
            "payment_term_days": "60",
            "qualification_definition": "qualified debt relief lead after buyer review",
            "rate_card_evidence": "draft email only",
            "negotiation_evidence": "no paid cohort yet",
            "reject_reason_summary": "",
            "invoice_terms": "Net 60 with broad return rights",
            "quality_evidence_status": "anecdotal",
            "source_transparency": "partial",
            "consent_evidence": "generic",
            "buyer_terms_status": "draft",
            "status": "open",
            "notes": "Acceptance pricing should hold until rate card, source transparency and paid evidence are fixed.",
            "source_urls": "https://support.google.com/google-ads/answer/3419241",
        },
        follow_redirects=True,
    )
    lead_pricing_review = LeadPricingReview.query.filter_by(
        name="Acceptance weak lead payout"
    ).first()
    if lead_pricing_response.status_code != 200 or not lead_pricing_review:
        failures.append("Lead pricing review creation failed")
    elif not lead_pricing_review.blockers:
        failures.append("Lead pricing review did not record blockers")
    elif lead_pricing_review.recommended_action != "hold_for_rate_card":
        failures.append("Lead pricing review did not hold for rate card")
    else:
        lead_pricing_status_response = client.post(
            f"/lead-pricing/{lead_pricing_review.id}/status",
            data={"status": "rate_card_review"},
            follow_redirects=True,
        )
        if (
            lead_pricing_status_response.status_code != 200
            or lead_pricing_review.status != "rate_card_review"
        ):
            failures.append("Lead pricing status update failed")
        if not AuditLog.query.filter_by(
            entity_type="lead_pricing_review",
            entity_id=lead_pricing_review.id,
            action="status_update",
        ).first():
            failures.append("Lead pricing status update did not write audit log")

    unsafe_appointment_count = AppointmentLeadReview.query.count()
    client.post(
        "/appointment-leads",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe fake appointment",
            "buyer_name": "Unsafe buyer",
            "vertical": "healthcare",
            "service_type": "dental consult",
            "geo": "US",
            "appointment_platform": "calendar stuffing",
            "payout_event": "showed",
            "payout_amount": "80",
            "estimated_cpc": "2",
            "click_to_request_rate_percent": "8",
            "request_to_book_rate_percent": "80",
            "confirmation_rate_percent": "80",
            "show_rate_percent": "70",
            "completed_rate_percent": "65",
            "paid_rate_percent": "55",
            "cancel_rate_percent": "5",
            "no_show_rate_percent": "10",
            "duplicate_booking_rate_percent": "2",
            "reschedule_rate_percent": "5",
            "reminder_cost_per_booking": "1",
            "no_show_cost_per_booking": "5",
            "available_slots": "80",
            "expected_bookings": "40",
            "lead_age_hours": "2",
            "slot_delay_hours": "24",
            "calendar_capacity_status": "open",
            "timezone_status": "aligned",
            "reminder_channel": "sms",
            "reminder_consent_status": "channel_specific",
            "confirmation_process_status": "confirmed_workflow",
            "buyer_terms_status": "approved",
            "payout_definition_clear": "on",
            "duplicate_window_defined": "on",
            "no_show_reason_map_ready": "on",
            "calendar_capacity_evidence": "on",
            "reminder_template_reviewed": "on",
            "offline_conversion_mapping_ready": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe acceptance case mentions fake showed appointment and mass SMS.",
            "source_urls": "https://support.google.com/calendar/answer/10729749",
        },
        follow_redirects=True,
    )
    if AppointmentLeadReview.query.count() != unsafe_appointment_count:
        failures.append("Unsafe fake appointment plan was accepted")

    appointment_response = client.post(
        "/appointment-leads",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance weak appointment funnel",
            "buyer_name": "Draft clinic",
            "vertical": "healthcare",
            "service_type": "dental consult",
            "geo": "US",
            "appointment_platform": "manual calendar",
            "payout_event": "booked",
            "payout_amount": "70",
            "estimated_cpc": "4",
            "click_to_request_rate_percent": "2",
            "request_to_book_rate_percent": "35",
            "confirmation_rate_percent": "40",
            "show_rate_percent": "30",
            "completed_rate_percent": "25",
            "paid_rate_percent": "20",
            "cancel_rate_percent": "35",
            "no_show_rate_percent": "45",
            "duplicate_booking_rate_percent": "12",
            "reschedule_rate_percent": "40",
            "reminder_cost_per_booking": "2",
            "no_show_cost_per_booking": "12",
            "available_slots": "10",
            "expected_bookings": "30",
            "lead_age_hours": "36",
            "slot_delay_hours": "120",
            "calendar_capacity_status": "unknown",
            "timezone_status": "unclear",
            "reminder_channel": "sms",
            "reminder_consent_status": "generic",
            "confirmation_process_status": "missing",
            "buyer_terms_status": "draft",
            "status_map": "submitted -> booked only",
            "slot_policy": "slot capacity is not confirmed",
            "reminder_policy": "generic reminder consent",
            "no_show_reason_map": "",
            "conversion_mapping": "booked is used as primary",
            "status": "open",
            "notes": "Acceptance appointment should block scaling until calendar capacity and showed mapping are fixed.",
            "source_urls": "https://support.google.com/google-ads/answer/9347141",
        },
        follow_redirects=True,
    )
    appointment_review = AppointmentLeadReview.query.filter_by(
        name="Acceptance weak appointment funnel"
    ).first()
    if appointment_response.status_code != 200 or not appointment_review:
        failures.append("Appointment lead review creation failed")
    elif not appointment_review.blockers:
        failures.append("Appointment lead review did not record blockers")
    elif appointment_review.recommended_action != "hold_for_calendar_capacity":
        failures.append("Appointment lead review did not hold for calendar capacity")
    else:
        appointment_status_response = client.post(
            f"/appointment-leads/{appointment_review.id}/status",
            data={"status": "calendar_review"},
            follow_redirects=True,
        )
        if (
            appointment_status_response.status_code != 200
            or appointment_review.status != "calendar_review"
        ):
            failures.append("Appointment lead status update failed")
        if not AuditLog.query.filter_by(
            entity_type="appointment_lead_review",
            entity_id=appointment_review.id,
            action="status_update",
        ).first():
            failures.append("Appointment lead status update did not write audit log")

    unsafe_buyer_capacity_count = BuyerCapacityReview.query.count()
    client.post(
        "/buyer-capacity",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe auto capacity",
            "buyer_name": "Unsafe buyer",
            "vertical": "home_services",
            "geo": "US",
            "buyer_timezone": "America/New_York",
            "account_timezone": "UTC",
            "user_timezone_scope": "US",
            "call_center_timezone": "America/New_York",
            "cap_type": "daily_buyer_cap",
            "cap_period": "daily",
            "cap_limit": "100",
            "cap_used": "20",
            "elapsed_operating_day_percent": "25",
            "expected_next_hour_leads": "10",
            "expected_daily_leads": "60",
            "hourly_contact_capacity": "25",
            "current_hour_capacity_used": "5",
            "expected_paid_value_per_lead": "40",
            "accepted_rate_percent": "80",
            "qualified_rate_percent": "70",
            "paid_rate_percent": "60",
            "no_buyer_rate_percent": "2",
            "missed_contact_rate_percent": "5",
            "after_hours_lead_rate_percent": "3",
            "cap_last_confirmed_hours": "1",
            "feedback_sla_hours": "24",
            "first_attempt_sla_minutes": "5",
            "cap_confidence_status": "same_day",
            "hours_alignment_status": "aligned",
            "ad_schedule_alignment_status": "aligned",
            "timezone_alignment_status": "aligned",
            "holiday_readiness_status": "ready",
            "fallback_status": "approved",
            "source_quality_status": "buyer_approved",
            "overdelivery_guardrail_status": "tested",
            "cap_snapshot_evidence": "on",
            "buyer_hours_evidence": "on",
            "ad_schedule_evidence": "on",
            "call_reporting_evidence": "on",
            "no_buyer_tracking_ready": "on",
            "missed_contact_tracking_ready": "on",
            "dayparting_cohort_ready": "on",
            "fallback_buyer_reviewed": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe acceptance case wants auto change budget with cookie session token.",
            "source_urls": "https://support.google.com/google-ads/answer/6372656",
        },
        follow_redirects=True,
    )
    if BuyerCapacityReview.query.count() != unsafe_buyer_capacity_count:
        failures.append("Unsafe buyer capacity automation plan was accepted")

    buyer_capacity_response = client.post(
        "/buyer-capacity",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance stale buyer capacity",
            "buyer_name": "Draft buyer",
            "vertical": "home_services",
            "geo": "US",
            "buyer_timezone": "America/New_York",
            "account_timezone": "UTC",
            "user_timezone_scope": "US mixed",
            "call_center_timezone": "America/Chicago",
            "cap_type": "daily_buyer_cap",
            "cap_period": "daily",
            "cap_limit": "50",
            "cap_used": "48",
            "elapsed_operating_day_percent": "40",
            "expected_next_hour_leads": "12",
            "expected_daily_leads": "90",
            "hourly_contact_capacity": "10",
            "current_hour_capacity_used": "12",
            "expected_paid_value_per_lead": "35",
            "accepted_rate_percent": "50",
            "qualified_rate_percent": "35",
            "paid_rate_percent": "25",
            "no_buyer_rate_percent": "18",
            "missed_contact_rate_percent": "30",
            "after_hours_lead_rate_percent": "22",
            "cap_last_confirmed_hours": "72",
            "feedback_sla_hours": "96",
            "first_attempt_sla_minutes": "30",
            "cap_confidence_status": "stale",
            "hours_alignment_status": "mismatch",
            "ad_schedule_alignment_status": "mismatch",
            "timezone_alignment_status": "mismatch",
            "holiday_readiness_status": "missing",
            "fallback_status": "draft",
            "source_quality_status": "low",
            "overdelivery_guardrail_status": "manual",
            "operating_hours": "Buyer hours are not confirmed.",
            "cap_reset_rule": "Unknown reset.",
            "holiday_calendar": "",
            "ad_schedule_summary": "Ads run outside buyer hours.",
            "no_buyer_reason_map": "",
            "routing_fallback_policy": "Fallback not approved.",
            "dayparting_basis": "Same-day conversions only.",
            "status": "open",
            "notes": "Acceptance capacity should block scaling until cap, hours, schedule and no buyer tracking are fixed.",
            "source_urls": "https://support.google.com/google-ads/answer/1704443",
        },
        follow_redirects=True,
    )
    buyer_capacity_review = BuyerCapacityReview.query.filter_by(
        name="Acceptance stale buyer capacity"
    ).first()
    if buyer_capacity_response.status_code != 200 or not buyer_capacity_review:
        failures.append("Buyer capacity review creation failed")
    elif not buyer_capacity_review.blockers:
        failures.append("Buyer capacity review did not record blockers")
    elif buyer_capacity_review.recommended_action != "refresh_cap_snapshot":
        failures.append("Buyer capacity review did not request cap refresh")
    else:
        buyer_capacity_status_response = client.post(
            f"/buyer-capacity/{buyer_capacity_review.id}/status",
            data={"status": "cap_refresh"},
            follow_redirects=True,
        )
        if (
            buyer_capacity_status_response.status_code != 200
            or buyer_capacity_review.status != "cap_refresh"
        ):
            failures.append("Buyer capacity status update failed")
        if not AuditLog.query.filter_by(
            entity_type="buyer_capacity_review",
            entity_id=buyer_capacity_review.id,
            action="status_update",
        ).first():
            failures.append("Buyer capacity status update did not write audit log")

    unsafe_conversion_signal_count = ConversionSignalReview.query.count()
    client.post(
        "/conversion-signals",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe fake signal",
            "vertical": "b2b_saas",
            "geo": "US",
            "conversion_goal_name": "lead_quality_us",
            "conversion_action_name": "lead_paid_us",
            "action_stage": "paid",
            "primary_status": "primary",
            "value_mode": "paid",
            "bid_strategy": "target_cpa",
            "traffic_scope": "search",
            "weekly_conversions": "80",
            "weekly_approved_conversions": "70",
            "weekly_paid_conversions": "60",
            "reported_value_per_conversion": "42",
            "approved_rate_percent": "80",
            "paid_rate_percent": "70",
            "click_id_coverage_percent": "98",
            "offline_match_rate_percent": "85",
            "duplicate_rate_percent": "0.5",
            "average_lag_days": "2",
            "p95_lag_days": "5",
            "incident_count_30d": "0",
            "segment_granularity_status": "offer_geo_buyer_source",
            "policy_consent_status": "reviewed",
            "customer_data_status": "policy_reviewed",
            "offline_import_status": "diagnostics_ready",
            "transaction_id_status": "idempotent",
            "lag_stability_status": "stable",
            "bid_strategy_status": "stable",
            "primary_secondary_reviewed": "on",
            "value_mapping_reviewed": "on",
            "transaction_id_dedupe_ready": "on",
            "offline_import_diagnostics_ready": "on",
            "conversion_lag_reviewed": "on",
            "segment_split_ready": "on",
            "consent_policy_reviewed": "on",
            "bid_strategy_report_reviewed": "on",
            "change_history_evidence": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe acceptance case wants fake conversion upload with cookie session token.",
            "source_urls": "https://support.google.com/google-ads/answer/7012522",
        },
        follow_redirects=True,
    )
    if ConversionSignalReview.query.count() != unsafe_conversion_signal_count:
        failures.append("Unsafe conversion signal automation plan was accepted")

    conversion_signal_response = client.post(
        "/conversion-signals",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance shallow primary signal",
            "vertical": "b2b_saas",
            "geo": "US",
            "conversion_goal_name": "lead_submitted_us",
            "conversion_action_name": "lead_submitted_b2b_us",
            "action_stage": "submitted",
            "primary_status": "primary",
            "value_mode": "gross",
            "bid_strategy": "target_cpa",
            "traffic_scope": "broad_ai_max",
            "weekly_conversions": "18",
            "weekly_approved_conversions": "3",
            "weekly_paid_conversions": "1",
            "reported_value_per_conversion": "50",
            "approved_rate_percent": "22",
            "paid_rate_percent": "15",
            "click_id_coverage_percent": "72",
            "offline_match_rate_percent": "40",
            "duplicate_rate_percent": "4.5",
            "average_lag_days": "9",
            "p95_lag_days": "30",
            "incident_count_30d": "1",
            "segment_granularity_status": "mixed",
            "policy_consent_status": "partial",
            "customer_data_status": "missing",
            "offline_import_status": "draft",
            "transaction_id_status": "unstable",
            "lag_stability_status": "unstable",
            "bid_strategy_status": "learning",
            "goal_change_summary": "Submitted lead is currently primary.",
            "affected_campaigns": "Acceptance campaign.",
            "value_mapping_notes": "Gross payout is used as value.",
            "dedupe_notes": "Transaction ID is not stable.",
            "lag_notes": "Lag is not mature.",
            "diagnostics_notes": "Diagnostics are draft only.",
            "rollback_plan": "Demote submitted to secondary and rebuild value mapping.",
            "status": "open",
            "notes": "Acceptance signal should block automated bidding.",
            "source_urls": "https://support.google.com/google-ads/answer/11461796",
        },
        follow_redirects=True,
    )
    conversion_signal_review = ConversionSignalReview.query.filter_by(
        name="Acceptance shallow primary signal"
    ).first()
    if conversion_signal_response.status_code != 200 or not conversion_signal_review:
        failures.append("Conversion signal review creation failed")
    elif not conversion_signal_review.blockers:
        failures.append("Conversion signal review did not record blockers")
    elif conversion_signal_review.recommended_action != "demote_to_secondary":
        failures.append("Conversion signal review did not demote shallow primary")
    else:
        conversion_signal_status_response = client.post(
            f"/conversion-signals/{conversion_signal_review.id}/status",
            data={"status": "goal_review"},
            follow_redirects=True,
        )
        if (
            conversion_signal_status_response.status_code != 200
            or conversion_signal_review.status != "goal_review"
        ):
            failures.append("Conversion signal status update failed")
        if not AuditLog.query.filter_by(
            entity_type="conversion_signal_review",
            entity_id=conversion_signal_review.id,
            action="status_update",
        ).first():
            failures.append("Conversion signal status update did not write audit log")

    unsafe_crm_mapping_count = CrmValueMappingReview.query.count()
    client.post(
        "/crm-value-mapping",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe CRM mapping",
            "buyer_name": "Unsafe buyer",
            "vertical": "b2b_saas",
            "geo": "US",
            "source_system": "CRM",
            "buyer_feedback_source": "buyer CSV",
            "source_stage": "paid",
            "standard_stage": "paid",
            "buyer_status": "paid",
            "conversion_action_name": "lead_paid_us",
            "conversion_action_role": "primary",
            "value_mode": "paid",
            "payout_amount": "42",
            "approved_rate_percent": "80",
            "paid_rate_percent": "70",
            "return_rate_percent": "4",
            "variable_cost_per_conversion": "1",
            "weekly_stage_count": "80",
            "weekly_unique_leads": "79",
            "rejected_count": "1",
            "returned_count": "1",
            "duplicate_count": "0",
            "click_id_match_rate_percent": "90",
            "import_success_rate_percent": "98",
            "import_error_rate_percent": "1",
            "average_stage_lag_days": "2",
            "return_window_days": "14",
            "transaction_id_status": "idempotent",
            "adjustment_rule_status": "ready",
            "import_batch_status": "qa_ready",
            "diagnostics_status": "reviewed",
            "consent_status": "reviewed",
            "pii_handling_status": "hashed_minimized",
            "stage_taxonomy_reviewed": "on",
            "buyer_feedback_contract_reviewed": "on",
            "conversion_action_mapping_reviewed": "on",
            "primary_secondary_reviewed": "on",
            "value_mode_reviewed": "on",
            "transaction_id_rule_ready": "on",
            "rejected_returned_excluded": "on",
            "adjustment_policy_ready": "on",
            "import_batch_qa_ready": "on",
            "diagnostics_reviewed": "on",
            "lag_profile_reviewed": "on",
            "consent_policy_reviewed": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe acceptance case wants fake buyer feedback and auto upload with cookie session token.",
            "source_urls": "https://support.google.com/google-ads/answer/7012522",
        },
        follow_redirects=True,
    )
    if CrmValueMappingReview.query.count() != unsafe_crm_mapping_count:
        failures.append("Unsafe CRM value mapping automation plan was accepted")

    crm_mapping_response = client.post(
        "/crm-value-mapping",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance returned positive CRM mapping",
            "buyer_name": "Draft buyer",
            "vertical": "b2b_saas",
            "geo": "US",
            "source_system": "CRM export",
            "buyer_feedback_source": "weekly buyer status file",
            "source_stage": "SCRUBBED_RETURNED",
            "standard_stage": "returned",
            "buyer_status": "returned",
            "conversion_action_name": "lead_returned_b2b_us",
            "conversion_action_role": "primary",
            "value_mode": "gross",
            "payout_amount": "50",
            "approved_rate_percent": "20",
            "paid_rate_percent": "10",
            "return_rate_percent": "40",
            "variable_cost_per_conversion": "0",
            "weekly_stage_count": "30",
            "weekly_unique_leads": "20",
            "rejected_count": "8",
            "returned_count": "12",
            "duplicate_count": "5",
            "click_id_match_rate_percent": "40",
            "import_success_rate_percent": "70",
            "import_error_rate_percent": "12",
            "average_stage_lag_days": "20",
            "return_window_days": "0",
            "transaction_id_status": "unstable",
            "adjustment_rule_status": "missing",
            "import_batch_status": "draft",
            "diagnostics_status": "errors_open",
            "consent_status": "partial",
            "pii_handling_status": "unknown",
            "stage_mapping_notes": "Returned stage is incorrectly mapped as a primary positive action.",
            "conversion_action_notes": "Needs adjustment only.",
            "value_mapping_notes": "Gross payout should not be used.",
            "transaction_id_notes": "Unstable transaction key.",
            "import_qa_notes": "Errors still open.",
            "adjustment_notes": "No adjustment policy.",
            "lag_notes": "Lag is not mature.",
            "diagnostics_notes": "Diagnostics have open errors.",
            "rollback_plan": "Stop positive mapping and create adjustment review.",
            "status": "open",
            "notes": "Acceptance mapping should block positive upload and require adjustment review.",
            "source_urls": "https://developers.google.com/google-ads/api/docs/conversions/adjust-conversions",
        },
        follow_redirects=True,
    )
    crm_mapping_review = CrmValueMappingReview.query.filter_by(
        name="Acceptance returned positive CRM mapping"
    ).first()
    if crm_mapping_response.status_code != 200 or not crm_mapping_review:
        failures.append("CRM value mapping review creation failed")
    elif not crm_mapping_review.blockers:
        failures.append("CRM value mapping review did not record blockers")
    elif crm_mapping_review.recommended_action != "do_not_upload_positive":
        failures.append("CRM value mapping review did not block returned positive mapping")
    else:
        crm_mapping_status_response = client.post(
            f"/crm-value-mapping/{crm_mapping_review.id}/status",
            data={"status": "adjustment_review"},
            follow_redirects=True,
        )
        if (
            crm_mapping_status_response.status_code != 200
            or crm_mapping_review.status != "adjustment_review"
        ):
            failures.append("CRM value mapping status update failed")
        if not AuditLog.query.filter_by(
            entity_type="crm_value_mapping_review",
            entity_id=crm_mapping_review.id,
            action="status_update",
        ).first():
            failures.append("CRM value mapping status update did not write audit log")

    unsafe_lead_validation_count = LeadValidationReview.query.count()
    client.post(
        "/lead-validation",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe lead validation",
            "vertical": "insurance",
            "geo": "US",
            "source_type": "google_search",
            "form_version": "form_v1",
            "validation_scope": "pre_routing",
            "lead_channel": "web_form",
            "consent_status": "buyer_scope_reviewed",
            "buyer_disclosure_status": "contract_reviewed",
            "phone_status": "normalized",
            "email_status": "normalized",
            "address_geo_status": "buyer_service_area",
            "duplicate_status": "source_buyer_windowed",
            "suppression_status": "ready",
            "dnc_status": "checked",
            "opt_out_status": "checked",
            "pii_minimization_status": "hashed_minimized",
            "retention_status": "deletion_ready",
            "source_policy_status": "buyer_approved",
            "buyer_reject_feedback_status": "paid_feedback_ready",
            "validation_sample_size": "100",
            "valid_rate_percent": "85",
            "invalid_contact_rate_percent": "3",
            "duplicate_rate_percent": "1",
            "suppression_hit_rate_percent": "0.5",
            "dnc_hit_rate_percent": "0.2",
            "opt_out_rate_percent": "0.2",
            "bad_geo_rate_percent": "1",
            "no_consent_rate_percent": "0.5",
            "buyer_reject_rate_percent": "5",
            "complaint_rate_percent": "0.1",
            "fields_collected_schema": "Hash-only validation schema.",
            "validation_rule_summary": "Reviewed safe validation rules.",
            "duplicate_rule_summary": "Reviewed duplicate windows.",
            "suppression_rule_summary": "Reviewed suppression rules.",
            "pii_handling_notes": "Unsafe request wants fake lead auto submit with cookie session token.",
            "retention_deletion_notes": "Retention reviewed.",
            "buyer_reject_reason_map": "invalid_contact, duplicate, bad_geo",
            "source_form_fix_plan": "Reviewed source fix plan.",
            "consent_evidence": "on",
            "buyer_disclosure_reviewed": "on",
            "field_minimization_reviewed": "on",
            "duplicate_rule_reviewed": "on",
            "suppression_dnc_checked": "on",
            "pii_access_reviewed": "on",
            "retention_policy_reviewed": "on",
            "reject_reason_mapped": "on",
            "source_policy_reviewed": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe acceptance case should not be persisted.",
            "source_urls": "https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business",
        },
        follow_redirects=True,
    )
    if LeadValidationReview.query.count() != unsafe_lead_validation_count:
        failures.append("Unsafe Lead validation fake lead or cookie automation plan was accepted")

    lead_validation_response = client.post(
        "/lead-validation",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance weak lead validation gate",
            "vertical": "insurance",
            "geo": "US",
            "source_type": "google_search",
            "form_version": "form_v1",
            "validation_scope": "pre_routing",
            "lead_channel": "web_form",
            "consent_status": "missing",
            "buyer_disclosure_status": "generic",
            "phone_status": "invalid",
            "email_status": "unknown",
            "address_geo_status": "bad_geo",
            "duplicate_status": "missing",
            "suppression_status": "missing",
            "dnc_status": "missing",
            "opt_out_status": "missing",
            "pii_minimization_status": "raw_pii_in_url",
            "retention_status": "missing",
            "source_policy_status": "unknown",
            "buyer_reject_feedback_status": "missing",
            "validation_sample_size": "25",
            "valid_rate_percent": "30",
            "invalid_contact_rate_percent": "25",
            "duplicate_rate_percent": "14",
            "suppression_hit_rate_percent": "6",
            "dnc_hit_rate_percent": "3",
            "opt_out_rate_percent": "4",
            "bad_geo_rate_percent": "18",
            "no_consent_rate_percent": "8",
            "buyer_reject_rate_percent": "35",
            "complaint_rate_percent": "2.5",
            "fields_collected_schema": "Draft schema has unsafe URL PII risk.",
            "validation_rule_summary": "Validation rules are incomplete.",
            "duplicate_rule_summary": "",
            "suppression_rule_summary": "",
            "pii_handling_notes": "PII handling is not minimized.",
            "retention_deletion_notes": "",
            "buyer_reject_reason_map": "",
            "source_form_fix_plan": "",
            "incident_notes": "Complaint spike under manual review.",
            "status": "open",
            "notes": "Acceptance validation should block until consent, PII and suppression are repaired.",
            "source_urls": "https://csrc.nist.gov/pubs/sp/800/122/final",
        },
        follow_redirects=True,
    )
    lead_validation_review = LeadValidationReview.query.filter_by(
        name="Acceptance weak lead validation gate"
    ).first()
    if lead_validation_response.status_code != 200 or not lead_validation_review:
        failures.append("Lead validation review creation failed")
    elif not lead_validation_review.blockers:
        failures.append("Lead validation review did not record blockers")
    elif lead_validation_review.recommended_action != "block_pii_or_consent":
        failures.append("Lead validation review did not block unsafe consent or PII")
    elif lead_validation_review.safe_routing_rate_percent_float != 0:
        failures.append("Lead validation review did not set safe routing rate to zero")
    else:
        lead_validation_status_response = client.post(
            f"/lead-validation/{lead_validation_review.id}/status",
            data={"status": "pii_review"},
            follow_redirects=True,
        )
        if (
            lead_validation_status_response.status_code != 200
            or lead_validation_review.status != "pii_review"
        ):
            failures.append("Lead validation status update failed")
        if not AuditLog.query.filter_by(
            entity_type="lead_validation_review",
            entity_id=lead_validation_review.id,
            action="status_update",
        ).first():
            failures.append("Lead validation status update did not write audit log")

    unsafe_ping_post_count = PingPostRoutingReview.query.count()
    client.post(
        "/ping-post-routing",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance unsafe ping post",
            "vertical": "insurance",
            "geo": "US",
            "buyer_group_name": "Unsafe buyers",
            "source_type": "google_search",
            "form_version": "form_v1",
            "routing_mode": "ping_post",
            "lead_type": "shared",
            "consent_scope": "shared_group",
            "buyer_disclosure_status": "buyer_group",
            "ping_field_scope": "hashed_dedupe",
            "pii_level": "hashed_minimized",
            "suppression_status": "checked",
            "dnc_status": "checked",
            "cap_snapshot_status": "same_day",
            "fallback_status": "approved",
            "buyer_feedback_status": "mapped",
            "source_policy_status": "approved",
            "buyer_count": "4",
            "max_post_buyers": "3",
            "pinged_buyers": "4",
            "accepted_buyers": "3",
            "posted_buyers": "3",
            "primary_buyer_cap_remaining": "20",
            "cap_last_checked_minutes": "20",
            "lead_age_minutes": "2",
            "avg_ping_latency_ms": "500",
            "expected_bid_amount": "30",
            "fallback_payout_amount": "15",
            "buyer_accept_rate_percent": "70",
            "qualification_rate_percent": "55",
            "paid_rate_percent": "45",
            "no_buyer_rate_percent": "2",
            "reject_rate_percent": "8",
            "duplicate_rate_percent": "1",
            "complaint_rate_percent": "0.2",
            "fields_sent_schema": "Minimal hashed ping schema.",
            "routing_rule_summary": "Reviewed buyer routing.",
            "buyer_disclosure_notes": "Reviewed buyer group.",
            "cap_snapshot_notes": "Cap checked.",
            "reject_reason_map": "duplicate, bad_geo, cap_reached",
            "fallback_policy": "Same intent fallback.",
            "buyer_feedback_plan": "Paid feedback plan.",
            "suppression_notes": "Checked.",
            "consent_evidence_notes": "Reviewed.",
            "incident_notes": "Unsafe request wants fake lead auto post with cookie session token.",
            "consent_version_evidence": "on",
            "buyer_disclosure_reviewed": "on",
            "field_minimization_reviewed": "on",
            "suppression_dnc_checked": "on",
            "cap_snapshot_evidence": "on",
            "routing_rule_reviewed": "on",
            "exclusive_shared_terms_reviewed": "on",
            "fallback_buyer_reviewed": "on",
            "buyer_feedback_ready": "on",
            "source_policy_reviewed": "on",
            "human_review": "on",
            "status": "open",
            "notes": "Unsafe acceptance case should not be persisted.",
            "source_urls": "https://docs.pingtree.com/documentation/campaign/distribution/ping-post",
        },
        follow_redirects=True,
    )
    if PingPostRoutingReview.query.count() != unsafe_ping_post_count:
        failures.append("Unsafe Ping/Post fake lead or cookie automation plan was accepted")

    ping_post_response = client.post(
        "/ping-post-routing",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance weak shared ping-post route",
            "vertical": "insurance",
            "geo": "US",
            "buyer_group_name": "Draft shared buyers",
            "source_type": "google_search",
            "form_version": "form_v1",
            "routing_mode": "ping_post",
            "lead_type": "shared",
            "consent_scope": "single_buyer",
            "buyer_disclosure_status": "generic",
            "ping_field_scope": "full_pii",
            "pii_level": "full_pii_ping",
            "suppression_status": "missing",
            "dnc_status": "missing",
            "cap_snapshot_status": "stale",
            "fallback_status": "draft",
            "buyer_feedback_status": "missing",
            "source_policy_status": "unknown",
            "buyer_count": "2",
            "max_post_buyers": "3",
            "pinged_buyers": "2",
            "accepted_buyers": "0",
            "posted_buyers": "2",
            "primary_buyer_cap_remaining": "0",
            "cap_last_checked_minutes": "500",
            "lead_age_minutes": "20",
            "avg_ping_latency_ms": "2500",
            "expected_bid_amount": "30",
            "fallback_payout_amount": "5",
            "buyer_accept_rate_percent": "20",
            "qualification_rate_percent": "15",
            "paid_rate_percent": "10",
            "no_buyer_rate_percent": "25",
            "reject_rate_percent": "45",
            "duplicate_rate_percent": "12",
            "complaint_rate_percent": "3",
            "fields_sent_schema": "Draft schema sends complete contact fields during ping.",
            "routing_rule_summary": "Shared route does not yet prove buyer disclosure.",
            "buyer_disclosure_notes": "Generic partner wording only.",
            "cap_snapshot_notes": "Cap snapshot is stale.",
            "reject_reason_map": "",
            "fallback_policy": "",
            "buyer_feedback_plan": "",
            "suppression_notes": "Suppression check missing.",
            "consent_evidence_notes": "Consent evidence incomplete.",
            "incident_notes": "Complaint and no-buyer spike under review.",
            "status": "open",
            "notes": "Acceptance route should block until consent, minimization, cap and feedback are repaired.",
            "source_urls": "https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
        },
        follow_redirects=True,
    )
    ping_post_review = PingPostRoutingReview.query.filter_by(
        name="Acceptance weak shared ping-post route"
    ).first()
    if ping_post_response.status_code != 200 or not ping_post_review:
        failures.append("Ping/Post routing review creation failed")
    elif not ping_post_review.blockers:
        failures.append("Ping/Post routing review did not record blockers")
    elif ping_post_review.recommended_action != "block_consent_or_pii":
        failures.append("Ping/Post routing review did not block unsafe consent or PII")
    else:
        ping_post_status_response = client.post(
            f"/ping-post-routing/{ping_post_review.id}/status",
            data={"status": "field_minimization"},
            follow_redirects=True,
        )
        if (
            ping_post_status_response.status_code != 200
            or ping_post_review.status != "field_minimization"
        ):
            failures.append("Ping/Post routing status update failed")
        if not AuditLog.query.filter_by(
            entity_type="ping_post_routing_review",
            entity_id=ping_post_review.id,
            action="status_update",
        ).first():
            failures.append("Ping/Post routing status update did not write audit log")

    taxonomy_response = client.post(
        "/taxonomy-governance",
        data={
            "offer_id": str(campaign.offer_id),
            "campaign_draft_id": str(campaign.id),
            "name": "Acceptance taxonomy missing join keys",
            "campaign_name": "gads-us-en-cloudbackup",
            "ad_group_name": "compare-cloudbackup-smallbiz",
            "labels_text": "lifecycle:test",
            "utm_source": "gads",
            "utm_medium": "",
            "utm_campaign": "",
            "utm_id": "",
            "utm_content": "",
            "utm_term": "",
            "valuetrack_template": "cid={campaignid}",
            "custom_parameter_map": "",
            "subid_map": "",
            "dimension_dictionary_version": "",
            "parameter_map_version": "",
            "landing_version": "",
            "link_version": "",
            "creative_version": "",
            "payload_hash": "",
            "report_join_gap_count": "3",
            "no_pii_in_url": "on",
            "no_sensitive_attributes": "on",
            "notes": "Acceptance taxonomy should block export until mapping is fixed.",
            "source_urls": "https://support.google.com/google-ads/answer/2375447",
        },
        follow_redirects=True,
    )
    taxonomy_review = TaxonomyReview.query.filter_by(
        name="Acceptance taxonomy missing join keys"
    ).first()
    if taxonomy_response.status_code != 200 or not taxonomy_review:
        failures.append("Taxonomy review creation failed")
    elif not taxonomy_review.blockers:
        failures.append("Taxonomy review did not record blockers")
    else:
        taxonomy_status_response = client.post(
            f"/taxonomy-governance/{taxonomy_review.id}/status",
            data={"status": "mapping_fix"},
            follow_redirects=True,
        )
        if (
            taxonomy_status_response.status_code != 200
            or taxonomy_review.status != "mapping_fix"
        ):
            failures.append("Taxonomy status update failed")
        if not AuditLog.query.filter_by(
            entity_type="taxonomy_review",
            entity_id=taxonomy_review.id,
            action="status_update",
        ).first():
            failures.append("Taxonomy status update did not write audit log")

    source = ResearchSource.query.first()
    if not source:
        failures.append("No research source for status checks")
    else:
        source_status_response = client.post(
            f"/sources/{source.id}/status",
            data={"review_status": "accepted"},
            follow_redirects=True,
        )
        if source_status_response.status_code != 200 or source.review_status != "accepted":
            failures.append("Research source status update failed")
        if not AuditLog.query.filter_by(
            entity_type="research_source",
            entity_id=source.id,
            action="status_update",
        ).first():
            failures.append("Research source status update did not write audit log")

    offer = Offer.query.first()
    if not offer:
        failures.append("No offer for guardrail checks")
        return

    risk_audit = RiskAudit.query.first()
    if not risk_audit:
        failures.append("No risk audit for status checks")
    else:
        risk_status_response = client.post(
            f"/risk-audits/{risk_audit.id}/status",
            data={"status": "mitigated"},
            follow_redirects=True,
        )
        if risk_status_response.status_code != 200 or risk_audit.status != "mitigated":
            failures.append("Risk audit status update failed")
        if not AuditLog.query.filter_by(
            entity_type="risk_audit",
            entity_id=risk_audit.id,
            action="status_update",
        ).first():
            failures.append("Risk audit status update did not write audit log")

    client.post(
        "/accounts",
        data={
            "name": "Acceptance unsafe cookie account",
            "platform": "Google Ads",
            "customer_id": "777-777-7777",
            "sync_method": "Cookie login automation",
            "status": "active",
            "notes": "Store session token and browser profile.",
        },
        follow_redirects=True,
    )
    if AdsAccount.query.filter_by(name="Acceptance unsafe cookie account").first():
        failures.append("Unsafe Cookie/Session account config was accepted")

    client.post(
        "/links",
        data={
            "offer_id": str(offer.id),
            "name": "Acceptance unsafe worker link",
            "current_url": "https://example.com/current",
            "candidate_urls": "https://worker.example.com/offer",
            "rotation_reason": "worker forward and proxy pool",
            "frequency_minutes": "1440",
        },
        follow_redirects=True,
    )
    if LinkRule.query.filter_by(name="Acceptance unsafe worker link").first():
        failures.append("Unsafe Worker/proxy link plan was accepted")

    safe_link_rule = LinkRule.query.first()
    if not safe_link_rule:
        failures.append("No link rule for link status checks")
    else:
        old_url = safe_link_rule.current_url
        client.post(f"/links/{safe_link_rule.id}/rotate", follow_redirects=True)
        if safe_link_rule.current_url != old_url:
            failures.append("Unapproved link rule was rotated")
        link_status_response = client.post(
            f"/links/{safe_link_rule.id}/status",
            data={"status": "approved"},
            follow_redirects=True,
        )
        if link_status_response.status_code != 200 or safe_link_rule.status != "approved":
            failures.append("Link rule approval status update failed")
        client.post(f"/links/{safe_link_rule.id}/rotate", follow_redirects=True)
        if safe_link_rule.current_url == old_url or safe_link_rule.status != "rotated":
            failures.append("Approved link rule did not rotate")
        if not AuditLog.query.filter_by(
            entity_type="link_rule",
            entity_id=safe_link_rule.id,
            action="manual_rotate",
        ).first():
            failures.append("Link rotation did not write audit log")

    client.post(
        "/tasks",
        data={
            "offer_id": str(offer.id),
            "campaign_draft_id": str(campaign.id),
            "link_rule_id": "",
            "name": "Acceptance unsafe task notes",
            "task_type": "export_script_payload",
            "schedule_mode": "manual",
            "interval_minutes": "1440",
            "notes": "Use cookie session token to bypass 2FA challenge.",
        },
        follow_redirects=True,
    )
    if TaskJob.query.filter_by(name="Acceptance unsafe task notes").first():
        failures.append("Unsafe task notes were accepted")

    metric_csv = (
        "offer_id,campaign_draft_id,day,channel,country,device,"
        "impressions,clicks,cost,conversions,revenue\n"
        f"{offer.id},{campaign.id},2026-06-09,Google Ads,US,mobile,"
        "200,80,35.00,0,0.00\n"
    )
    client.post("/metrics/import", data={"csv_text": metric_csv}, follow_redirects=True)
    action = OptimizationAction.query.filter_by(
        action_type="invalid_traffic_review"
    ).first()
    if not action:
        failures.append("Metric import did not create invalid traffic optimization action")
    else:
        status_response = client.post(
            f"/optimization/{action.id}/status",
            data={"status": "manual_review"},
            follow_redirects=True,
        )
        if status_response.status_code != 200 or action.status != "manual_review":
            failures.append("Optimization action status update failed")
        if not AuditLog.query.filter_by(
            entity_type="optimization_action",
            entity_id=action.id,
            action="status_update",
        ).first():
            failures.append("Optimization action status update did not write audit log")

    evidence.append(f"Required routes checked: {len(REQUIRED_ROUTES)}")
    evidence.append(
        "Safety guardrails checked: account, campaign status/preflight, bulk upload status, script sync status, taxonomy status, attribution status, CPL vertical status, Lead Pricing status, Appointment Lead status, Buyer Capacity status, Lead Validation status, Ping/Post Routing status, Conversion Signal status, CRM Value Mapping status, ad review status, query mining status, decision window status, budget pacing status, portfolio allocation status, offer cap status, source quality status, vendor contract status, source status, claim review status, risk audit status, link status/rotation, task notes, Scripts export, optimization status"
    )


if __name__ == "__main__":
    main()
