from __future__ import annotations

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


def main() -> None:
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
        offer = Offer.query.first()
        campaign = CampaignDraft.query.first()
        assert offer is not None
        assert campaign is not None

        client = app.test_client()
        for path in [
            "/",
            "/accounts",
            "/calculators",
            "/offers",
            f"/offers/{offer.id}",
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
            "/docs",
            "/doc/usage.md",
            "/knowledge/docs_index",
            "/knowledge/industry",
            "/knowledge/business_models",
            "/knowledge/operations",
            "/knowledge/evidence_matrix",
            "/knowledge/search_feed_parking",
            "/knowledge/rsoc_n2s",
            "/knowledge/keyword_intent",
            "/knowledge/seasonality_forecasting",
            "/knowledge/search_terms_mining",
            "/knowledge/brand_trademark",
            "/knowledge/competitor_intelligence",
            "/knowledge/traffic_vendor",
            "/knowledge/inventory_controls",
            "/knowledge/source_quality_governance",
            "/knowledge/vendor_contracts",
            "/knowledge/audience_remarketing",
            "/knowledge/affiliate_due_diligence",
            "/knowledge/lead_buyer_contracts",
            "/knowledge/lead_quality",
            "/knowledge/lead_call_tracking",
            "/knowledge/call_tracking_attribution",
            "/knowledge/pay_per_call_routing",
            "/knowledge/lead_consent_proof",
            "/knowledge/lead_form_funnel",
            "/knowledge/ping_post_leads",
            "/knowledge/lead_freshness",
            "/knowledge/lead_validation",
            "/knowledge/lead_contact_sla",
            "/knowledge/experiment_design",
            "/knowledge/invalid_traffic_sop",
            "/knowledge/anomaly_alerting",
            "/knowledge/content_quality",
            "/knowledge/sensitive_verticals",
            "/knowledge/metrics",
            "/knowledge/unit_economics",
            "/knowledge/verticals",
            "/knowledge/cpl_vertical_economics",
            "/knowledge/insurance_leads",
            "/knowledge/loan_debt_leads",
            "/knowledge/legal_leads",
            "/knowledge/home_services_leads",
            "/knowledge/education_leads",
            "/knowledge/healthcare_leads",
            "/knowledge/b2b_saas_leads",
            "/knowledge/crypto_investment_leads",
            "/knowledge/employment_leads",
            "/knowledge/gambling_leads",
            "/knowledge/addiction_treatment_leads",
            "/knowledge/government_services_leads",
            "/knowledge/lead_pricing",
            "/knowledge/appointment_leads",
            "/knowledge/offer_cap_payout",
            "/knowledge/buyer_capacity",
            "/knowledge/traffic_tracking",
            "/knowledge/native_presell",
            "/knowledge/click_session_revenue",
            "/knowledge/tracking_chain",
            "/knowledge/taxonomy_governance",
            "/knowledge/attribution_incrementality",
            "/knowledge/conversion_tracking",
            "/knowledge/conversion_signal_quality",
            "/knowledge/crm_value_mapping",
            "/knowledge/decision_windows",
            "/knowledge/landing_quality",
            "/knowledge/domain_assets",
            "/knowledge/landing_intelligence",
            "/knowledge/cashflow",
            "/knowledge/subscription_ltv",
            "/knowledge/revenue_reconciliation",
            "/knowledge/creative_testing",
            "/knowledge/creative_angle_library",
            "/knowledge/creative_claim_review",
            "/knowledge/ad_review_appeal",
            "/knowledge/ai_prompt_governance",
            "/knowledge/link_rotation",
            "/knowledge/campaign_launch",
            "/knowledge/editor_csv_bulk",
            "/knowledge/scripts_automation",
            "/knowledge/scripts_data_sync",
            "/knowledge/task_orchestration",
            "/knowledge/recommendations_experiments",
            "/knowledge/auction_bidding",
            "/knowledge/ads_reporting",
            "/knowledge/search_automation",
            "/knowledge/pmax_demand_gen",
            "/knowledge/geo_localization",
            "/knowledge/budget_pacing",
            "/knowledge/portfolio_allocation",
            "/knowledge/account_governance",
            "/knowledge/account_health",
            "/knowledge/adsense_site_approval",
            "/knowledge/publisher_stack",
            "/knowledge/ad_quality",
            "/knowledge/programmatic_supply_chain",
            "/knowledge/gam_yield",
            "/knowledge/header_bidding",
            "/knowledge/ad_placement",
            "/knowledge/privacy_consent",
            "/knowledge/playbook",
            "/knowledge/adxkit",
            "/knowledge/redlines",
            "/knowledge/risk_matrix",
            "/knowledge/risk_completion",
            "/knowledge/risk_blueprint",
            "/knowledge/source_library",
            "/knowledge/traceability",
            "/knowledge/risk_index",
            "/knowledge/acceptance",
            "/knowledge/risk_cookie",
            "/knowledge/risk_auth",
            "/knowledge/risk_invalid_traffic",
            "/knowledge/risk_association",
            "/knowledge/risk_cloaking",
            "/knowledge/risk_ban_evasion",
            "/knowledge/design",
            "/knowledge/usage",
            "/knowledge/development",
        ]:
            response = client.get(path)
            assert response.status_code == 200, (path, response.status_code)

        docs_response = client.get("/docs")
        assert docs_response.status_code == 200
        assert b"markdown-doc" in docs_response.data
        assert b"doc-table" in docs_response.data
        assert b"/doc/ads_arbitrage_industry.md" in docs_response.data

        offer_response = client.get(f"/offers/{offer.id}")
        assert offer_response.status_code == 200
        assert "Claim 审核".encode("utf-8") in offer_response.data
        creative = CreativeSet.query.first()
        assert creative is not None
        claim_refresh_response = client.post(
            f"/creatives/{creative.id}/claim-reviews/run",
            follow_redirects=True,
        )
        assert claim_refresh_response.status_code == 200
        claim_review = CreativeClaimReview.query.filter_by(
            creative_set_id=creative.id
        ).first()
        assert claim_review is not None
        claim_status_response = client.post(
            f"/claim-reviews/{claim_review.id}/status",
            data={"review_status": "rewrite_required"},
            follow_redirects=True,
        )
        assert claim_status_response.status_code == 200
        assert claim_review.review_status == "rewrite_required"
        assert (
            AuditLog.query.filter_by(
                entity_type="creative_claim_review",
                entity_id=claim_review.id,
                action="status_update",
            ).first()
            is not None
        )

        campaign_review_response = client.post(
            f"/campaigns/{campaign.id}/status",
            data={"status": "reviewing"},
            follow_redirects=True,
        )
        assert campaign_review_response.status_code == 200
        assert campaign.status == "reviewing"
        campaign_approve_response = client.post(
            f"/campaigns/{campaign.id}/status",
            data={"status": "approved"},
            follow_redirects=True,
        )
        assert campaign_approve_response.status_code == 200
        assert campaign.status == "approved"
        assert (
            AuditLog.query.filter_by(
                entity_type="campaign",
                entity_id=campaign.id,
                action="status_update",
            ).first()
            is not None
        )

        blocked_export_response = client.get(
            f"/campaigns/{campaign.id}/export.csv",
            follow_redirects=True,
        )
        assert blocked_export_response.status_code == 200
        assert (
            AuditLog.query.filter_by(
                entity_type="campaign",
                entity_id=campaign.id,
                action="export_blocked",
            ).first()
            is not None
        )
        claim_status_approve_response = client.post(
            f"/claim-reviews/{claim_review.id}/status",
            data={"review_status": "approved"},
            follow_redirects=True,
        )
        assert claim_status_approve_response.status_code == 200
        seed_ad_review_case = AdReviewCase.query.filter_by(
            campaign_draft_id=campaign.id
        ).first()
        assert seed_ad_review_case is not None
        seed_ad_review_status_response = client.post(
            f"/ad-reviews/{seed_ad_review_case.id}/status",
            data={"status": "fixed"},
            follow_redirects=True,
        )
        assert seed_ad_review_status_response.status_code == 200

        csv_response = client.get(f"/campaigns/{campaign.id}/export.csv")
        assert csv_response.status_code == 200
        assert b"Campaign,Ad group,Keyword" in csv_response.data

        script_response = client.get(f"/campaigns/{campaign.id}/export.script.json")
        assert script_response.status_code == 200
        assert b"no_cookie_automation" in script_response.data

        ad_review_response = client.post(
            "/ad-reviews",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "creative_set_id": str(creative.id),
                "object_type": "ad",
                "object_ref": "Smoke RSA draft",
                "policy_topic": "Destination requirements",
                "severity": "medium",
                "status": "open",
                "final_url": offer.target_url,
                "expanded_url": offer.target_url,
                "finding": "Smoke case records a destination review issue.",
                "change_summary": "Verify final URL, mobile page, claim evidence, and tracking parameters.",
                "evidence_urls": "https://support.google.com/adspolicy/answer/6368661",
                "appeal_text": "Appeal only after the destination and ad claim are fixed.",
                "reviewer": "smoke",
            },
            follow_redirects=True,
        )
        assert ad_review_response.status_code == 200
        ad_review_case = AdReviewCase.query.order_by(AdReviewCase.id.desc()).first()
        assert ad_review_case is not None
        assert AdReviewCase.query.count() >= 2
        ad_review_status_response = client.post(
            f"/ad-reviews/{ad_review_case.id}/status",
            data={"status": "appeal_ready"},
            follow_redirects=True,
        )
        assert ad_review_status_response.status_code == 200
        assert ad_review_case.status == "appeal_ready"
        assert (
            AuditLog.query.filter_by(
                entity_type="ad_review_case",
                entity_id=ad_review_case.id,
                action="status_update",
            ).first()
            is not None
        )
        blocked_ad_review_response = client.post(
            "/ad-reviews",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "creative_set_id": str(creative.id),
                "object_type": "ad",
                "object_ref": "Unsafe appeal",
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
        assert blocked_ad_review_response.status_code == 200
        assert AdReviewCase.query.filter_by(object_ref="Unsafe appeal").first() is None

        assert DecisionWindowReview.query.count() >= 1
        decision_window_response = client.post(
            "/decision-windows",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke early window",
                "data_status": "fresh",
                "revenue_status": "estimated",
                "conversion_lag_days": "1",
                "approval_lag_days": "0",
                "settlement_lag_days": "0",
                "sample_clicks": "12",
                "approved_revenue": "0",
                "paid_revenue": "0",
                "source_quality": "watch",
                "incident_state": "clean",
                "status": "open",
                "notes": "Smoke early window must wait instead of scaling.",
                "source_urls": "https://support.google.com/google-ads/answer/9347141",
            },
            follow_redirects=True,
        )
        assert decision_window_response.status_code == 200
        decision_window = DecisionWindowReview.query.filter_by(
            name="Smoke early window"
        ).first()
        assert decision_window is not None
        assert decision_window.score < 55
        assert decision_window.recommended_action in {"wait_loss", "stop_or_freeze"}
        assert decision_window.blockers
        decision_window_status_response = client.post(
            f"/decision-windows/{decision_window.id}/status",
            data={"status": "waiting"},
            follow_redirects=True,
        )
        assert decision_window_status_response.status_code == 200
        assert decision_window.status == "waiting"
        assert (
            AuditLog.query.filter_by(
                entity_type="decision_window_review",
                entity_id=decision_window.id,
                action="status_update",
            ).first()
            is not None
        )

        assert BudgetPacingReview.query.count() >= 1
        budget_pacing_response = client.post(
            "/budget-pacing",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke blocked budget ramp",
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
                "notes": "Smoke review should block scale and preserve audit evidence.",
                "source_urls": "https://support.google.com/google-ads/answer/10702522",
            },
            follow_redirects=True,
        )
        assert budget_pacing_response.status_code == 200
        budget_review = BudgetPacingReview.query.filter_by(
            name="Smoke blocked budget ramp"
        ).first()
        assert budget_review is not None
        assert budget_review.blockers
        assert budget_review.recommended_action in {
            "stop_or_reduce",
            "block_scale",
            "wait_or_block_scale",
        }
        budget_status_response = client.post(
            f"/budget-pacing/{budget_review.id}/status",
            data={"status": "blocked"},
            follow_redirects=True,
        )
        assert budget_status_response.status_code == 200
        assert budget_review.status == "blocked"
        assert (
            AuditLog.query.filter_by(
                entity_type="budget_pacing_review",
                entity_id=budget_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert PortfolioAllocationReview.query.count() >= 1
        portfolio_response = client.post(
            "/portfolio-allocation",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke concentrated portfolio",
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
                "notes": "Smoke portfolio should reduce exposure before more spend.",
                "source_urls": "https://support.google.com/google-ads/answer/10702522",
            },
            follow_redirects=True,
        )
        assert portfolio_response.status_code == 200
        portfolio_review = PortfolioAllocationReview.query.filter_by(
            name="Smoke concentrated portfolio"
        ).first()
        assert portfolio_review is not None
        assert portfolio_review.blockers
        assert portfolio_review.recommended_action in {
            "quarantine_or_zero_budget",
            "reduce_exposure",
            "wait_for_settlement",
        }
        portfolio_status_response = client.post(
            f"/portfolio-allocation/{portfolio_review.id}/status",
            data={"status": "quarantine"},
            follow_redirects=True,
        )
        assert portfolio_status_response.status_code == 200
        assert portfolio_review.status == "quarantine"
        assert (
            AuditLog.query.filter_by(
                entity_type="portfolio_allocation_review",
                entity_id=portfolio_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert OfferCapReview.query.count() >= 1
        offer_cap_response = client.post(
            "/offer-cap-payout",
            data={
                "offer_id": str(offer.id),
                "replacement_offer_id": "",
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke capped offer",
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
                "notes": "Smoke cap review should block new traffic and require evidence.",
                "source_urls": "https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps",
            },
            follow_redirects=True,
        )
        assert offer_cap_response.status_code == 200
        offer_cap_review = OfferCapReview.query.filter_by(
            name="Smoke capped offer"
        ).first()
        assert offer_cap_review is not None
        assert offer_cap_review.blockers
        assert offer_cap_review.recommended_action in {
            "pause_until_cap_resets",
            "reduce_budget_or_pause",
            "hold_for_manual_review",
        }
        offer_cap_status_response = client.post(
            f"/offer-cap-payout/{offer_cap_review.id}/status",
            data={"status": "pause_traffic"},
            follow_redirects=True,
        )
        assert offer_cap_status_response.status_code == 200
        assert offer_cap_review.status == "pause_traffic"
        assert (
            AuditLog.query.filter_by(
                entity_type="offer_cap_review",
                entity_id=offer_cap_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert SourceQualityReview.query.count() >= 1
        unsafe_source_count = SourceQualityReview.query.count()
        unsafe_source_response = client.post(
            "/source-quality",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe hidden source",
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
                "notes": "This unsafe smoke case mentions proxy and hidden source.",
                "source_urls": "https://support.google.com/adsense/answer/1348722",
            },
            follow_redirects=True,
        )
        assert unsafe_source_response.status_code == 200
        assert SourceQualityReview.query.count() == unsafe_source_count

        source_quality_response = client.post(
            "/source-quality",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke low source quality",
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
                "notes": "Smoke source review should quarantine or blocklist this source.",
                "source_urls": "https://support.google.com/adsense/answer/1348722",
            },
            follow_redirects=True,
        )
        assert source_quality_response.status_code == 200
        source_quality_review = SourceQualityReview.query.filter_by(
            name="Smoke low source quality"
        ).first()
        assert source_quality_review is not None
        assert source_quality_review.blockers
        assert source_quality_review.recommended_action in {
            "quarantine_diagnose",
            "blocklist_stop",
            "watchlist_no_scale",
        }
        source_quality_status_response = client.post(
            f"/source-quality/{source_quality_review.id}/status",
            data={"status": "blocklist"},
            follow_redirects=True,
        )
        assert source_quality_status_response.status_code == 200
        assert source_quality_review.status == "blocklist"
        assert (
            AuditLog.query.filter_by(
                entity_type="source_quality_review",
                entity_id=source_quality_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert VendorContractReview.query.count() >= 1
        unsafe_vendor_count = VendorContractReview.query.count()
        unsafe_vendor_response = client.post(
            "/vendor-contracts",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe traffic vendor",
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
                "notes": "Smoke unsafe vendor mentions hidden source and proxy.",
                "source_urls": "https://support.google.com/adsense/answer/3332805",
            },
            follow_redirects=True,
        )
        assert unsafe_vendor_response.status_code == 200
        assert VendorContractReview.query.count() == unsafe_vendor_count

        vendor_contract_response = client.post(
            "/vendor-contracts",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke vendor dispute",
                "vendor_name": "Unknown media partner",
                "vendor_type": "traffic_vendor",
                "io_number": "IO-SMOKE-001",
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
                "notes": "Smoke vendor dispute should suspend or block spend.",
                "source_urls": "https://support.google.com/adsense/answer/3332805",
            },
            follow_redirects=True,
        )
        assert vendor_contract_response.status_code == 200
        vendor_contract_review = VendorContractReview.query.filter_by(
            name="Smoke vendor dispute"
        ).first()
        assert vendor_contract_review is not None
        assert vendor_contract_review.blockers
        assert vendor_contract_review.recommended_action in {
            "open_dispute",
            "suspend_vendor",
            "block_vendor",
        }
        vendor_status_response = client.post(
            f"/vendor-contracts/{vendor_contract_review.id}/status",
            data={"status": "dispute_open"},
            follow_redirects=True,
        )
        assert vendor_status_response.status_code == 200
        assert vendor_contract_review.status == "dispute_open"
        assert (
            AuditLog.query.filter_by(
                entity_type="vendor_contract_review",
                entity_id=vendor_contract_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert QueryMiningReview.query.count() >= 1
        unsafe_query_count = QueryMiningReview.query.count()
        unsafe_query_response = client.post(
            "/query-mining",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe query mining",
                "date_window": "2026-06-01..2026-06-07",
                "ads_customer_id": "123-456-7890",
                "campaign_ref": "Smoke Search",
                "ad_group_ref": "broad",
                "source_file_hash": "smoke",
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
        assert unsafe_query_response.status_code == 200
        assert QueryMiningReview.query.count() == unsafe_query_count

        query_mining_response = client.post(
            "/query-mining",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke support query negative",
                "date_window": "2026-06-01..2026-06-07",
                "ads_customer_id": "123-456-7890",
                "campaign_ref": "Smoke Search",
                "ad_group_ref": "broad",
                "source_file_hash": "smoke",
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
                "notes": "Smoke query review should propose a negative keyword and policy review.",
                "source_urls": "https://support.google.com/google-ads/answer/2472708",
            },
            follow_redirects=True,
        )
        assert query_mining_response.status_code == 200
        query_review = QueryMiningReview.query.filter_by(
            name="Smoke support query negative"
        ).first()
        assert query_review is not None
        assert query_review.blockers
        assert query_review.recommended_action in {
            "policy_review_negative",
            "add_negative_phrase",
        }
        query_status_response = client.post(
            f"/query-mining/{query_review.id}/status",
            data={"status": "negative_proposed"},
            follow_redirects=True,
        )
        assert query_status_response.status_code == 200
        assert query_review.status == "negative_proposed"
        assert (
            AuditLog.query.filter_by(
                entity_type="query_mining_review",
                entity_id=query_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert BulkUploadReview.query.count() >= 1
        unsafe_bulk_count = BulkUploadReview.query.count()
        unsafe_bulk_response = client.post(
            "/bulk-upload",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe auto post",
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
        assert unsafe_bulk_response.status_code == 200
        assert BulkUploadReview.query.count() == unsafe_bulk_count

        bulk_response = client.post(
            "/bulk-upload",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke bulk preview errors",
                "export_type": "editor_csv",
                "batch_id": "BULK-SMOKE-001",
                "csv_hash": "smoke-hash",
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
                "notes": "Smoke bulk upload should block posting until preview errors are fixed.",
                "source_urls": "https://support.google.com/google-ads/editor/answer/56368",
            },
            follow_redirects=True,
        )
        assert bulk_response.status_code == 200
        bulk_review = BulkUploadReview.query.filter_by(
            name="Smoke bulk preview errors"
        ).first()
        assert bulk_review is not None
        assert bulk_review.blockers
        assert bulk_review.recommended_action in {
            "fix_preflight_before_export",
            "fix_preview_errors",
            "hold_for_review",
        }
        bulk_status_response = client.post(
            f"/bulk-upload/{bulk_review.id}/status",
            data={"status": "blocked"},
            follow_redirects=True,
        )
        assert bulk_status_response.status_code == 200
        assert bulk_review.status == "blocked"
        assert (
            AuditLog.query.filter_by(
                entity_type="bulk_upload_review",
                entity_id=bulk_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert ScriptSyncReview.query.count() >= 1
        unsafe_sync_count = ScriptSyncReview.query.count()
        unsafe_sync_response = client.post(
            "/scripts-sync",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe cookie sync",
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
        assert unsafe_sync_response.status_code == 200
        assert ScriptSyncReview.query.count() == unsafe_sync_count

        sync_response = client.post(
            "/scripts-sync",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke Scripts stale conflict",
                "auth_mode": "scripts_authorized",
                "sync_type": "metrics_daily",
                "script_name": "Daily Metrics Snapshot Preview",
                "customer_id": "123-456-7890",
                "date_range": "LAST_7_DAYS",
                "account_timezone": "America/New_York",
                "currency": "USD",
                "query_or_report": "campaign metrics daily GAQL",
                "source_snapshot_hash": "smoke-source-hash",
                "payload_hash": "smoke-query-hash",
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
                "notes": "Smoke sync should require rerun before import.",
                "source_urls": "https://developers.google.com/google-ads/scripts/docs/concepts/reports",
            },
            follow_redirects=True,
        )
        assert sync_response.status_code == 200
        sync_review = ScriptSyncReview.query.filter_by(
            name="Smoke Scripts stale conflict"
        ).first()
        assert sync_review is not None
        assert sync_review.blockers
        assert sync_review.recommended_action == "rerun_snapshot_before_apply"
        sync_status_response = client.post(
            f"/scripts-sync/{sync_review.id}/status",
            data={"status": "conflict_review"},
            follow_redirects=True,
        )
        assert sync_status_response.status_code == 200
        assert sync_review.status == "conflict_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="script_sync_review",
                entity_id=sync_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert TaxonomyReview.query.count() >= 1
        unsafe_taxonomy_count = TaxonomyReview.query.count()
        unsafe_taxonomy_response = client.post(
            "/taxonomy-governance",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe PII taxonomy",
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
        assert unsafe_taxonomy_response.status_code == 200
        assert TaxonomyReview.query.count() == unsafe_taxonomy_count

        taxonomy_response = client.post(
            "/taxonomy-governance",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke taxonomy missing join keys",
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
                "notes": "Smoke taxonomy should block export until mapping is fixed.",
                "source_urls": "https://support.google.com/google-ads/answer/2375447",
            },
            follow_redirects=True,
        )
        assert taxonomy_response.status_code == 200
        taxonomy_review = TaxonomyReview.query.filter_by(
            name="Smoke taxonomy missing join keys"
        ).first()
        assert taxonomy_review is not None
        assert taxonomy_review.blockers
        assert taxonomy_review.recommended_action == "fix_report_join_gaps"
        taxonomy_status_response = client.post(
            f"/taxonomy-governance/{taxonomy_review.id}/status",
            data={"status": "mapping_fix"},
            follow_redirects=True,
        )
        assert taxonomy_status_response.status_code == 200
        assert taxonomy_review.status == "mapping_fix"
        assert (
            AuditLog.query.filter_by(
                entity_type="taxonomy_review",
                entity_id=taxonomy_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert AttributionReview.query.count() >= 1
        unsafe_attribution_count = AttributionReview.query.count()
        unsafe_attribution_response = client.post(
            "/attribution",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe fake lift",
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
                "notes": "Unsafe smoke case mentions fake conversion and auto apply winner.",
                "source_urls": "https://support.google.com/google-ads/answer/6261395",
            },
            follow_redirects=True,
        )
        assert unsafe_attribution_response.status_code == 200
        assert AttributionReview.query.count() == unsafe_attribution_count

        attribution_response = client.post(
            "/attribution",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke weak cannibalization review",
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
                "notes": "Smoke review should stop or freeze until holdout and paid evidence exist.",
                "source_urls": "https://support.google.com/google-ads/answer/6259715",
            },
            follow_redirects=True,
        )
        assert attribution_response.status_code == 200
        attribution_review = AttributionReview.query.filter_by(
            name="Smoke weak cannibalization review"
        ).first()
        assert attribution_review is not None
        assert attribution_review.blockers
        assert attribution_review.risk_level == "high"
        assert attribution_review.recommended_action == "stop_or_freeze"
        attribution_status_response = client.post(
            f"/attribution/{attribution_review.id}/status",
            data={"status": "cannibalization_review"},
            follow_redirects=True,
        )
        assert attribution_status_response.status_code == 200
        assert attribution_review.status == "cannibalization_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="attribution_review",
                entity_id=attribution_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert CplVerticalReview.query.count() >= 1
        unsafe_cpl_count = CplVerticalReview.query.count()
        unsafe_cpl_response = client.post(
            "/cpl-verticals",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe CPL fake lead plan",
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
                "notes": "Unsafe smoke case mentions auto submit fake form.",
                "source_urls": "https://support.google.com/adspolicy/answer/6020956",
            },
            follow_redirects=True,
        )
        assert unsafe_cpl_response.status_code == 200
        assert CplVerticalReview.query.count() == unsafe_cpl_count

        cpl_response = client.post(
            "/cpl-verticals",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke weak debt lead vertical",
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
                "notes": "Smoke CPL vertical should block scaling until terms, consent and economics are fixed.",
                "source_urls": "https://support.google.com/adspolicy/answer/143465",
            },
            follow_redirects=True,
        )
        assert cpl_response.status_code == 200
        cpl_review = CplVerticalReview.query.filter_by(
            name="Smoke weak debt lead vertical"
        ).first()
        assert cpl_review is not None
        assert cpl_review.blockers
        assert cpl_review.risk_level == "high"
        assert cpl_review.recommended_action == "policy_review_first"
        cpl_status_response = client.post(
            f"/cpl-verticals/{cpl_review.id}/status",
            data={"status": "policy_review"},
            follow_redirects=True,
        )
        assert cpl_status_response.status_code == 200
        assert cpl_review.status == "policy_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="cpl_vertical_review",
                entity_id=cpl_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert LeadPricingReview.query.count() >= 1
        unsafe_lead_pricing_count = LeadPricingReview.query.count()
        unsafe_lead_pricing_response = client.post(
            "/lead-pricing",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe fake paid report",
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
                "notes": "Unsafe smoke case mentions fake paid report and fake invoice.",
                "source_urls": "https://support.google.com/google-ads/answer/3419241",
            },
            follow_redirects=True,
        )
        assert unsafe_lead_pricing_response.status_code == 200
        assert LeadPricingReview.query.count() == unsafe_lead_pricing_count

        lead_pricing_response = client.post(
            "/lead-pricing",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke weak lead payout",
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
                "notes": "Smoke pricing should hold until rate card, source transparency and paid evidence are fixed.",
                "source_urls": "https://support.google.com/google-ads/answer/3419241",
            },
            follow_redirects=True,
        )
        assert lead_pricing_response.status_code == 200
        lead_pricing_review = LeadPricingReview.query.filter_by(
            name="Smoke weak lead payout"
        ).first()
        assert lead_pricing_review is not None
        assert lead_pricing_review.blockers
        assert lead_pricing_review.risk_level == "high"
        assert lead_pricing_review.recommended_action == "hold_for_rate_card"
        lead_pricing_status_response = client.post(
            f"/lead-pricing/{lead_pricing_review.id}/status",
            data={"status": "rate_card_review"},
            follow_redirects=True,
        )
        assert lead_pricing_status_response.status_code == 200
        assert lead_pricing_review.status == "rate_card_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="lead_pricing_review",
                entity_id=lead_pricing_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert AppointmentLeadReview.query.count() >= 1
        unsafe_appointment_count = AppointmentLeadReview.query.count()
        unsafe_appointment_response = client.post(
            "/appointment-leads",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe fake appointment",
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
                "notes": "Unsafe smoke case mentions fake showed appointment and mass SMS.",
                "source_urls": "https://support.google.com/calendar/answer/10729749",
            },
            follow_redirects=True,
        )
        assert unsafe_appointment_response.status_code == 200
        assert AppointmentLeadReview.query.count() == unsafe_appointment_count

        appointment_response = client.post(
            "/appointment-leads",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke weak appointment funnel",
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
                "notes": "Smoke appointment should block scaling until calendar capacity and showed mapping are fixed.",
                "source_urls": "https://support.google.com/google-ads/answer/9347141",
            },
            follow_redirects=True,
        )
        assert appointment_response.status_code == 200
        appointment_review = AppointmentLeadReview.query.filter_by(
            name="Smoke weak appointment funnel"
        ).first()
        assert appointment_review is not None
        assert appointment_review.blockers
        assert appointment_review.risk_level == "high"
        assert appointment_review.recommended_action == "hold_for_calendar_capacity"
        appointment_status_response = client.post(
            f"/appointment-leads/{appointment_review.id}/status",
            data={"status": "calendar_review"},
            follow_redirects=True,
        )
        assert appointment_status_response.status_code == 200
        assert appointment_review.status == "calendar_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="appointment_lead_review",
                entity_id=appointment_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert BuyerCapacityReview.query.count() >= 1
        unsafe_buyer_capacity_count = BuyerCapacityReview.query.count()
        unsafe_buyer_capacity_response = client.post(
            "/buyer-capacity",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe auto capacity",
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
                "notes": "Unsafe smoke case wants auto change budget with cookie session token.",
                "source_urls": "https://support.google.com/google-ads/answer/6372656",
            },
            follow_redirects=True,
        )
        assert unsafe_buyer_capacity_response.status_code == 200
        assert BuyerCapacityReview.query.count() == unsafe_buyer_capacity_count

        buyer_capacity_response = client.post(
            "/buyer-capacity",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke stale buyer capacity",
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
                "notes": "Smoke capacity should block scaling until cap, hours, schedule and no buyer tracking are fixed.",
                "source_urls": "https://support.google.com/google-ads/answer/1704443",
            },
            follow_redirects=True,
        )
        assert buyer_capacity_response.status_code == 200
        buyer_capacity_review = BuyerCapacityReview.query.filter_by(
            name="Smoke stale buyer capacity"
        ).first()
        assert buyer_capacity_review is not None
        assert buyer_capacity_review.blockers
        assert buyer_capacity_review.risk_level == "high"
        assert buyer_capacity_review.recommended_action == "refresh_cap_snapshot"
        buyer_capacity_status_response = client.post(
            f"/buyer-capacity/{buyer_capacity_review.id}/status",
            data={"status": "cap_refresh"},
            follow_redirects=True,
        )
        assert buyer_capacity_status_response.status_code == 200
        assert buyer_capacity_review.status == "cap_refresh"
        assert (
            AuditLog.query.filter_by(
                entity_type="buyer_capacity_review",
                entity_id=buyer_capacity_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert ConversionSignalReview.query.count() >= 1
        unsafe_conversion_signal_count = ConversionSignalReview.query.count()
        unsafe_conversion_signal_response = client.post(
            "/conversion-signals",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe fake signal",
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
                "notes": "Unsafe smoke case wants fake conversion upload with cookie session token.",
                "source_urls": "https://support.google.com/google-ads/answer/7012522",
            },
            follow_redirects=True,
        )
        assert unsafe_conversion_signal_response.status_code == 200
        assert ConversionSignalReview.query.count() == unsafe_conversion_signal_count

        conversion_signal_response = client.post(
            "/conversion-signals",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke shallow primary signal",
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
                "affected_campaigns": "Smoke campaign.",
                "value_mapping_notes": "Gross payout is used as value.",
                "dedupe_notes": "Transaction ID is not stable.",
                "lag_notes": "Lag is not mature.",
                "diagnostics_notes": "Diagnostics are draft only.",
                "rollback_plan": "Demote submitted to secondary and rebuild value mapping.",
                "status": "open",
                "notes": "Smoke signal should block automated bidding.",
                "source_urls": "https://support.google.com/google-ads/answer/11461796",
            },
            follow_redirects=True,
        )
        assert conversion_signal_response.status_code == 200
        conversion_signal_review = ConversionSignalReview.query.filter_by(
            name="Smoke shallow primary signal"
        ).first()
        assert conversion_signal_review is not None
        assert conversion_signal_review.blockers
        assert conversion_signal_review.recommended_action == "demote_to_secondary"
        assert conversion_signal_review.recommended_primary_status == "secondary_only"
        conversion_signal_status_response = client.post(
            f"/conversion-signals/{conversion_signal_review.id}/status",
            data={"status": "goal_review"},
            follow_redirects=True,
        )
        assert conversion_signal_status_response.status_code == 200
        assert conversion_signal_review.status == "goal_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="conversion_signal_review",
                entity_id=conversion_signal_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert CrmValueMappingReview.query.count() >= 1
        unsafe_crm_mapping_count = CrmValueMappingReview.query.count()
        unsafe_crm_mapping_response = client.post(
            "/crm-value-mapping",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe CRM mapping",
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
                "notes": "Unsafe smoke case wants fake buyer feedback and auto upload with cookie session token.",
                "source_urls": "https://support.google.com/google-ads/answer/7012522",
            },
            follow_redirects=True,
        )
        assert unsafe_crm_mapping_response.status_code == 200
        assert CrmValueMappingReview.query.count() == unsafe_crm_mapping_count

        crm_mapping_response = client.post(
            "/crm-value-mapping",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke returned positive CRM mapping",
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
                "notes": "Smoke mapping should block positive upload and require adjustment review.",
                "source_urls": "https://developers.google.com/google-ads/api/docs/conversions/adjust-conversions",
            },
            follow_redirects=True,
        )
        assert crm_mapping_response.status_code == 200
        crm_mapping_review = CrmValueMappingReview.query.filter_by(
            name="Smoke returned positive CRM mapping"
        ).first()
        assert crm_mapping_review is not None
        assert crm_mapping_review.blockers
        assert crm_mapping_review.recommended_action == "do_not_upload_positive"
        assert crm_mapping_review.primary_recommendation == "adjustment_only"
        crm_mapping_status_response = client.post(
            f"/crm-value-mapping/{crm_mapping_review.id}/status",
            data={"status": "adjustment_review"},
            follow_redirects=True,
        )
        assert crm_mapping_status_response.status_code == 200
        assert crm_mapping_review.status == "adjustment_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="crm_value_mapping_review",
                entity_id=crm_mapping_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert LeadValidationReview.query.count() >= 1
        unsafe_lead_validation_count = LeadValidationReview.query.count()
        unsafe_lead_validation_response = client.post(
            "/lead-validation",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe lead validation",
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
                "notes": "Unsafe smoke case should not be persisted.",
                "source_urls": "https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business",
            },
            follow_redirects=True,
        )
        assert unsafe_lead_validation_response.status_code == 200
        assert LeadValidationReview.query.count() == unsafe_lead_validation_count

        lead_validation_response = client.post(
            "/lead-validation",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke weak lead validation gate",
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
                "notes": "Smoke validation should block until consent, PII and suppression are repaired.",
                "source_urls": "https://csrc.nist.gov/pubs/sp/800/122/final",
            },
            follow_redirects=True,
        )
        assert lead_validation_response.status_code == 200
        lead_validation_review = LeadValidationReview.query.filter_by(
            name="Smoke weak lead validation gate"
        ).first()
        assert lead_validation_review is not None
        assert lead_validation_review.blockers
        assert lead_validation_review.recommended_action == "block_pii_or_consent"
        assert lead_validation_review.safe_routing_rate_percent_float == 0
        lead_validation_status_response = client.post(
            f"/lead-validation/{lead_validation_review.id}/status",
            data={"status": "pii_review"},
            follow_redirects=True,
        )
        assert lead_validation_status_response.status_code == 200
        assert lead_validation_review.status == "pii_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="lead_validation_review",
                entity_id=lead_validation_review.id,
                action="status_update",
            ).first()
            is not None
        )

        assert PingPostRoutingReview.query.count() >= 1
        unsafe_ping_post_count = PingPostRoutingReview.query.count()
        unsafe_ping_post_response = client.post(
            "/ping-post-routing",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke unsafe ping post",
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
                "notes": "Unsafe smoke case should not be persisted.",
                "source_urls": "https://docs.pingtree.com/documentation/campaign/distribution/ping-post",
            },
            follow_redirects=True,
        )
        assert unsafe_ping_post_response.status_code == 200
        assert PingPostRoutingReview.query.count() == unsafe_ping_post_count

        ping_post_response = client.post(
            "/ping-post-routing",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "name": "Smoke weak shared ping-post route",
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
                "notes": "Smoke route should block until consent, minimization, cap and feedback are repaired.",
                "source_urls": "https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            },
            follow_redirects=True,
        )
        assert ping_post_response.status_code == 200
        ping_post_review = PingPostRoutingReview.query.filter_by(
            name="Smoke weak shared ping-post route"
        ).first()
        assert ping_post_review is not None
        assert ping_post_review.blockers
        assert ping_post_review.recommended_action == "block_consent_or_pii"
        assert ping_post_review.safe_cpl_float >= 0
        ping_post_status_response = client.post(
            f"/ping-post-routing/{ping_post_review.id}/status",
            data={"status": "field_minimization"},
            follow_redirects=True,
        )
        assert ping_post_status_response.status_code == 200
        assert ping_post_review.status == "field_minimization"
        assert (
            AuditLog.query.filter_by(
                entity_type="ping_post_routing_review",
                entity_id=ping_post_review.id,
                action="status_update",
            ).first()
            is not None
        )

        calc_response = client.post(
            "/calculators",
            data={
                "offer_id": str(offer.id),
                "name": "Smoke CPA opportunity",
                "revenue_model": "CPA",
                "session_rpm": "0",
                "payout": "42",
                "cvr_percent": "2",
                "cpc": "0.45",
                "safety_factor": "0.65",
                "target_clicks": "150",
                "policy_score": "85",
                "content_score": "82",
                "tracking_score": "80",
                "source_score": "78",
                "cash_buffer_days": "30",
            },
            follow_redirects=True,
        )
        assert calc_response.status_code == 200
        assert OpportunityAssessment.query.count() >= 2

        source_response = client.post(
            "/sources",
            data={
                "topic": "Smoke source",
                "capability": "ads_cookie_backend_operation",
                "title": "Smoke source title",
                "url": "https://example.com/source",
                "publisher": "Example",
                "source_type": "test",
                "reliability": "secondary",
                "claim_summary": "Smoke test source summary.",
                "notes": "Created by smoke test.",
            },
            follow_redirects=True,
        )
        assert source_response.status_code == 200
        assert ResearchSource.query.count() >= 2
        source = ResearchSource.query.order_by(ResearchSource.id.desc()).first()
        assert source is not None
        source_status_response = client.post(
            f"/sources/{source.id}/status",
            data={"review_status": "accepted"},
            follow_redirects=True,
        )
        assert source_status_response.status_code == 200
        assert source.review_status == "accepted"
        assert (
            AuditLog.query.filter_by(
                entity_type="research_source",
                entity_id=source.id,
                action="status_update",
            ).first()
            is not None
        )

        risk_response = client.post(
            "/risk-audits",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "capability": "invalid_traffic_click_impression_simulation",
                "severity": "high",
                "status": "open",
                "finding": "No click or impression simulation is allowed.",
                "mitigation": "Use metric import and source isolation instead.",
                "source_urls": "https://support.google.com/adsense/answer/16737",
            },
            follow_redirects=True,
        )
        assert risk_response.status_code == 200
        risk_audit = RiskAudit.query.order_by(RiskAudit.id.desc()).first()
        assert risk_audit is not None
        assert RiskAudit.query.count() >= 2
        risk_status_response = client.post(
            f"/risk-audits/{risk_audit.id}/status",
            data={"status": "mitigated"},
            follow_redirects=True,
        )
        assert risk_status_response.status_code == 200
        assert risk_audit.status == "mitigated"
        assert (
            AuditLog.query.filter_by(
                entity_type="risk_audit",
                entity_id=risk_audit.id,
                action="status_update",
            ).first()
            is not None
        )

        blocked_account_response = client.post(
            "/accounts",
            data={
                "name": "Unsafe account pool",
                "platform": "Google Ads",
                "customer_id": "999-999-9999",
                "sync_method": "Manual Review",
                "status": "active",
                "notes": "封禁后换号继续同一个 offer，防关联不断号。",
            },
            follow_redirects=True,
        )
        assert blocked_account_response.status_code == 200
        assert AdsAccount.query.filter_by(name="Unsafe account pool").first() is None

        blocked_cookie_account_response = client.post(
            "/accounts",
            data={
                "name": "Unsafe cookie login account",
                "platform": "Google Ads",
                "customer_id": "888-888-8888",
                "sync_method": "Cookie login automation",
                "status": "active",
                "notes": "Store session token and browser profile for backend operation.",
            },
            follow_redirects=True,
        )
        assert blocked_cookie_account_response.status_code == 200
        assert AdsAccount.query.filter_by(name="Unsafe cookie login account").first() is None

        blocked_link_response = client.post(
            "/links",
            data={
                "offer_id": str(offer.id),
                "name": "Unsafe cloaking link plan",
                "current_url": "https://example.com/safe-review",
                "candidate_urls": "https://example.com/hidden-offer?googlebot=review",
                "rotation_reason": "绕审核后切用户页",
                "frequency_minutes": "1440",
            },
            follow_redirects=True,
        )
        assert blocked_link_response.status_code == 200
        assert LinkRule.query.filter_by(name="Unsafe cloaking link plan").first() is None

        blocked_worker_link_response = client.post(
            "/links",
            data={
                "offer_id": str(offer.id),
                "name": "Unsafe worker proxy link plan",
                "current_url": "https://example.com/current",
                "candidate_urls": "https://worker.example.com/offer",
                "rotation_reason": "Use worker forward and proxy pool to hide association.",
                "frequency_minutes": "1440",
            },
            follow_redirects=True,
        )
        assert blocked_worker_link_response.status_code == 200
        assert LinkRule.query.filter_by(name="Unsafe worker proxy link plan").first() is None

        safe_link_rule = LinkRule.query.first()
        assert safe_link_rule is not None
        old_url = safe_link_rule.current_url
        draft_rotate_response = client.post(
            f"/links/{safe_link_rule.id}/rotate",
            follow_redirects=True,
        )
        assert draft_rotate_response.status_code == 200
        assert safe_link_rule.current_url == old_url
        assert safe_link_rule.status == "draft"
        link_status_response = client.post(
            f"/links/{safe_link_rule.id}/status",
            data={"status": "approved"},
            follow_redirects=True,
        )
        assert link_status_response.status_code == 200
        assert safe_link_rule.status == "approved"
        rotate_response = client.post(
            f"/links/{safe_link_rule.id}/rotate",
            follow_redirects=True,
        )
        assert rotate_response.status_code == 200
        assert safe_link_rule.current_url != old_url
        assert safe_link_rule.status == "rotated"
        assert safe_link_rule.last_rotated_at is not None
        assert (
            AuditLog.query.filter_by(
                entity_type="link_rule",
                entity_id=safe_link_rule.id,
                action="status_update",
            ).first()
            is not None
        )
        assert (
            AuditLog.query.filter_by(
                entity_type="link_rule",
                entity_id=safe_link_rule.id,
                action="manual_rotate",
            ).first()
            is not None
        )

        task_response = client.post(
            "/tasks",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "link_rule_id": "",
                "name": "Smoke script payload review",
                "task_type": "export_script_payload",
                "schedule_mode": "manual",
                "interval_minutes": "1440",
                "notes": "Smoke test task.",
            },
            follow_redirects=True,
        )
        assert task_response.status_code == 200
        job = TaskJob.query.order_by(TaskJob.id.desc()).first()
        assert job is not None
        run_response = client.post(f"/tasks/{job.id}/run", follow_redirects=True)
        assert run_response.status_code == 200
        assert job.run_count == 1
        assert job.success_count == 1

        campaign.status = "draft"
        db.session.commit()
        preflight_task_response = client.post(
            "/tasks",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "link_rule_id": "",
                "name": "Smoke blocked preflight script payload",
                "task_type": "export_script_payload",
                "schedule_mode": "manual",
                "interval_minutes": "1440",
                "notes": "Should fail because campaign preflight is unresolved.",
            },
            follow_redirects=True,
        )
        assert preflight_task_response.status_code == 200
        preflight_job = TaskJob.query.filter_by(
            name="Smoke blocked preflight script payload"
        ).first()
        assert preflight_job is not None
        preflight_run_response = client.post(
            f"/tasks/{preflight_job.id}/run", follow_redirects=True
        )
        assert preflight_run_response.status_code == 200
        assert preflight_job.failure_count == 1
        assert preflight_job.last_result["ok"] is False
        assert "preflight" in preflight_job.last_result["message"].lower()

        blocked_task_response = client.post(
            "/tasks",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": "",
                "link_rule_id": "",
                "name": "Unsafe login retry task",
                "task_type": "login_2fa_challenge_solver",
                "schedule_mode": "manual",
                "interval_minutes": "1440",
                "notes": "Should be rejected by task safety guard.",
            },
            follow_redirects=True,
        )
        assert blocked_task_response.status_code == 200
        assert TaskJob.query.filter_by(name="Unsafe login retry task").first() is None

        blocked_traffic_task_response = client.post(
            "/tasks",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": "",
                "link_rule_id": "",
                "name": "Unsafe traffic simulation task",
                "task_type": "simulate_click_traffic",
                "schedule_mode": "manual",
                "interval_minutes": "1440",
                "notes": "Should be rejected by task safety guard.",
            },
            follow_redirects=True,
        )
        assert blocked_traffic_task_response.status_code == 200
        assert TaskJob.query.filter_by(name="Unsafe traffic simulation task").first() is None

        blocked_task_notes_response = client.post(
            "/tasks",
            data={
                "offer_id": str(offer.id),
                "campaign_draft_id": str(campaign.id),
                "link_rule_id": "",
                "name": "Unsafe safe-type task",
                "task_type": "export_script_payload",
                "schedule_mode": "manual",
                "interval_minutes": "1440",
                "notes": "Use cookie session token after export to bypass 2FA challenge.",
            },
            follow_redirects=True,
        )
        assert blocked_task_notes_response.status_code == 200
        assert TaskJob.query.filter_by(name="Unsafe safe-type task").first() is None

        metric_csv = (
            "offer_id,campaign_draft_id,day,channel,country,device,"
            "impressions,clicks,cost,conversions,revenue\n"
            f"{offer.id},{campaign.id},2026-06-08,Google Ads,US,mobile,"
            "1500,100,60.00,1,42.00\n"
            f"{offer.id},{campaign.id},2026-06-09,Google Ads,US,desktop,"
            "200,80,35.00,0,0.00\n"
        )
        import_response = client.post(
            "/metrics/import",
            data={"csv_text": metric_csv},
            follow_redirects=True,
        )
        assert import_response.status_code == 200
        assert "优化建议".encode("utf-8") in import_response.data
        action = OptimizationAction.query.filter_by(
            action_type="invalid_traffic_review"
        ).first()
        assert action is not None

        status_response = client.post(
            f"/optimization/{action.id}/status",
            data={"status": "manual_review"},
            follow_redirects=True,
        )
        assert status_response.status_code == 200
        assert action.status == "manual_review"
        assert (
            AuditLog.query.filter_by(
                entity_type="optimization_action",
                entity_id=action.id,
                action="status_update",
            ).first()
            is not None
        )

    print("Smoke test passed.")


if __name__ == "__main__":
    main()
