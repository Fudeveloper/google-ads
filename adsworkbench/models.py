from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import inspect, text

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Offer(TimestampMixin, db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    vertical = db.Column(db.String(80), nullable=False, default="general")
    country = db.Column(db.String(80), nullable=False, default="US")
    language = db.Column(db.String(40), nullable=False, default="en")
    payout_model = db.Column(db.String(40), nullable=False, default="CPA")
    payout_value = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    target_url = db.Column(db.String(700), nullable=False)
    tracking_url = db.Column(db.String(700), nullable=True)
    status = db.Column(db.String(40), nullable=False, default="researching")
    policy_notes = db.Column(db.Text, nullable=True)

    landing_pages = db.relationship(
        "LandingPage", back_populates="offer", cascade="all, delete-orphan"
    )
    creatives = db.relationship(
        "CreativeSet", back_populates="offer", cascade="all, delete-orphan"
    )
    campaign_drafts = db.relationship(
        "CampaignDraft", back_populates="offer", cascade="all, delete-orphan"
    )
    metrics = db.relationship(
        "MetricDaily", back_populates="offer", cascade="all, delete-orphan"
    )
    link_rules = db.relationship(
        "LinkRule", back_populates="offer", cascade="all, delete-orphan"
    )

    @property
    def latest_landing_page(self) -> "LandingPage | None":
        return self.landing_pages[-1] if self.landing_pages else None

    @property
    def payout_float(self) -> float:
        return float(self.payout_value or 0)


class AdsAccount(TimestampMixin, db.Model):
    __tablename__ = "ads_accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    platform = db.Column(db.String(80), nullable=False, default="Google Ads")
    customer_id = db.Column(db.String(80), nullable=True)
    sync_method = db.Column(db.String(80), nullable=False, default="Google Ads Scripts")
    status = db.Column(db.String(40), nullable=False, default="active")
    notes = db.Column(db.Text, nullable=True)


class LandingPage(TimestampMixin, db.Model):
    __tablename__ = "landing_pages"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    url = db.Column(db.String(700), nullable=False)
    http_status = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)
    h1 = db.Column(db.String(300), nullable=True)
    h2 = db.Column(db.Text, nullable=True)
    word_count = db.Column(db.Integer, nullable=False, default=0)
    internal_links = db.Column(db.Integer, nullable=False, default=0)
    external_links = db.Column(db.Integer, nullable=False, default=0)
    technical_score = db.Column(db.Integer, nullable=False, default=0)
    transparency_score = db.Column(db.Integer, nullable=False, default=0)
    relevance_score = db.Column(db.Integer, nullable=False, default=0)
    quality_score = db.Column(db.Integer, nullable=False, default=0)
    raw_summary = db.Column(db.Text, nullable=True)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    offer = db.relationship("Offer", back_populates="landing_pages")


class CreativeSet(TimestampMixin, db.Model):
    __tablename__ = "creative_sets"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    angle = db.Column(db.String(80), nullable=False)
    headlines = db.Column(db.JSON, nullable=False, default=list)
    descriptions = db.Column(db.JSON, nullable=False, default=list)
    keywords = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="draft")

    offer = db.relationship("Offer", back_populates="creatives")
    campaign_drafts = db.relationship("CampaignDraft", back_populates="creative")
    claim_reviews = db.relationship(
        "CreativeClaimReview", back_populates="creative", cascade="all, delete-orphan"
    )


class CreativeClaimReview(TimestampMixin, db.Model):
    __tablename__ = "creative_claim_reviews"

    id = db.Column(db.Integer, primary_key=True)
    creative_set_id = db.Column(db.Integer, db.ForeignKey("creative_sets.id"), nullable=False)
    asset_type = db.Column(db.String(40), nullable=False)
    asset_text = db.Column(db.String(500), nullable=False)
    issue = db.Column(db.String(180), nullable=False)
    severity = db.Column(db.String(40), nullable=False, default="medium")
    action = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.Text, nullable=True)
    source_url = db.Column(db.String(800), nullable=True)
    review_status = db.Column(db.String(40), nullable=False, default="open")

    creative = db.relationship("CreativeSet", back_populates="claim_reviews")


class CampaignDraft(TimestampMixin, db.Model):
    __tablename__ = "campaign_drafts"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    creative_set_id = db.Column(
        db.Integer, db.ForeignKey("creative_sets.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    channel = db.Column(db.String(60), nullable=False, default="Google Search")
    daily_budget = db.Column(db.Numeric(12, 2), nullable=False, default=30)
    bid_strategy = db.Column(db.String(80), nullable=False, default="Maximize Clicks")
    final_url = db.Column(db.String(700), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="draft")
    notes = db.Column(db.Text, nullable=True)

    offer = db.relationship("Offer", back_populates="campaign_drafts")
    creative = db.relationship("CreativeSet", back_populates="campaign_drafts")
    metrics = db.relationship("MetricDaily", back_populates="campaign_draft")

    @property
    def budget_float(self) -> float:
        return float(self.daily_budget or 0)


class AdReviewCase(TimestampMixin, db.Model):
    __tablename__ = "ad_review_cases"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    creative_set_id = db.Column(db.Integer, db.ForeignKey("creative_sets.id"), nullable=True)
    object_type = db.Column(db.String(80), nullable=False, default="ad")
    object_ref = db.Column(db.String(180), nullable=True)
    policy_topic = db.Column(db.String(180), nullable=False)
    severity = db.Column(db.String(40), nullable=False, default="medium")
    status = db.Column(db.String(40), nullable=False, default="open")
    final_url = db.Column(db.String(700), nullable=True)
    expanded_url = db.Column(db.String(900), nullable=True)
    finding = db.Column(db.Text, nullable=False)
    change_summary = db.Column(db.Text, nullable=False)
    evidence_urls = db.Column(db.JSON, nullable=False, default=list)
    appeal_text = db.Column(db.Text, nullable=True)
    reviewer = db.Column(db.String(120), nullable=True)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")
    creative = db.relationship("CreativeSet")


class MetricDaily(TimestampMixin, db.Model):
    __tablename__ = "metrics_daily"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    day = db.Column(db.Date, nullable=False, default=date.today)
    channel = db.Column(db.String(80), nullable=False, default="Google Ads")
    country = db.Column(db.String(80), nullable=False, default="US")
    device = db.Column(db.String(40), nullable=False, default="all")
    impressions = db.Column(db.Integer, nullable=False, default=0)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    cost = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    conversions = db.Column(db.Integer, nullable=False, default=0)
    revenue = db.Column(db.Numeric(12, 4), nullable=False, default=0)

    offer = db.relationship("Offer", back_populates="metrics")
    campaign_draft = db.relationship("CampaignDraft", back_populates="metrics")

    @property
    def cost_float(self) -> float:
        return float(self.cost or 0)

    @property
    def revenue_float(self) -> float:
        return float(self.revenue or 0)

    @property
    def profit(self) -> float:
        return self.revenue_float - self.cost_float

    @property
    def roi(self) -> float:
        return self.profit / self.cost_float if self.cost_float else 0

    @property
    def cpc(self) -> float:
        return self.cost_float / self.clicks if self.clicks else 0

    @property
    def rpv(self) -> float:
        return self.revenue_float / self.clicks if self.clicks else 0

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions else 0

    @property
    def cvr(self) -> float:
        return self.conversions / self.clicks if self.clicks else 0


class DecisionWindowReview(TimestampMixin, db.Model):
    __tablename__ = "decision_window_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    data_status = db.Column(db.String(40), nullable=False, default="fresh")
    revenue_status = db.Column(db.String(40), nullable=False, default="estimated")
    conversion_lag_days = db.Column(db.Integer, nullable=False, default=0)
    approval_lag_days = db.Column(db.Integer, nullable=False, default=0)
    settlement_lag_days = db.Column(db.Integer, nullable=False, default=0)
    sample_clicks = db.Column(db.Integer, nullable=False, default=0)
    approved_revenue = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    paid_revenue = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    source_quality = db.Column(db.String(40), nullable=False, default="watch")
    incident_state = db.Column(db.String(40), nullable=False, default="clean")
    score = db.Column(db.Integer, nullable=False, default=0)
    maturity = db.Column(db.String(40), nullable=False, default="unsafe")
    recommended_action = db.Column(db.String(60), nullable=False, default="wait_loss")
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def approved_revenue_float(self) -> float:
        return float(self.approved_revenue or 0)

    @property
    def paid_revenue_float(self) -> float:
        return float(self.paid_revenue or 0)


class BudgetPacingReview(TimestampMixin, db.Model):
    __tablename__ = "budget_pacing_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    current_daily_budget = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    proposed_daily_budget = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    test_budget = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    hard_stop = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    spend_to_date = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    approved_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    paid_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    safe_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    actual_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    sample_clicks = db.Column(db.Integer, nullable=False, default=0)
    data_status = db.Column(db.String(40), nullable=False, default="fresh")
    revenue_status = db.Column(db.String(40), nullable=False, default="estimated")
    source_quality = db.Column(db.String(40), nullable=False, default="watch")
    incident_state = db.Column(db.String(40), nullable=False, default="clean")
    cash_buffer_days = db.Column(db.Integer, nullable=False, default=0)
    overdelivery_buffer_percent = db.Column(db.Numeric(6, 2), nullable=False, default=20)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(db.String(80), nullable=False, default="wait_or_block_scale")
    increase_percent = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    remaining_test_budget = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    remaining_hard_stop = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def current_daily_budget_float(self) -> float:
        return float(self.current_daily_budget or 0)

    @property
    def proposed_daily_budget_float(self) -> float:
        return float(self.proposed_daily_budget or 0)

    @property
    def test_budget_float(self) -> float:
        return float(self.test_budget or 0)

    @property
    def hard_stop_float(self) -> float:
        return float(self.hard_stop or 0)

    @property
    def spend_to_date_float(self) -> float:
        return float(self.spend_to_date or 0)

    @property
    def approved_revenue_float(self) -> float:
        return float(self.approved_revenue or 0)

    @property
    def paid_revenue_float(self) -> float:
        return float(self.paid_revenue or 0)

    @property
    def safe_cpc_float(self) -> float:
        return float(self.safe_cpc or 0)

    @property
    def actual_cpc_float(self) -> float:
        return float(self.actual_cpc or 0)


class PortfolioAllocationReview(TimestampMixin, db.Model):
    __tablename__ = "portfolio_allocation_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    portfolio_bucket = db.Column(db.String(40), nullable=False, default="test")
    monthly_media_budget = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    proposed_allocation = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    spend_to_date = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    reported_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    pending_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    approved_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    finalized_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    paid_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    deducted_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    single_offer_exposure_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    single_source_exposure_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    single_account_exposure_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    single_partner_exposure_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    cash_reserve_days = db.Column(db.Integer, nullable=False, default=0)
    source_quality = db.Column(db.String(40), nullable=False, default="watch")
    policy_risk = db.Column(db.String(40), nullable=False, default="medium")
    incident_state = db.Column(db.String(40), nullable=False, default="clean")
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="wait_for_settlement"
    )
    allocation_percent = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    remaining_monthly_budget = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    cash_at_risk = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    revenue_quality_ratio = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def monthly_media_budget_float(self) -> float:
        return float(self.monthly_media_budget or 0)

    @property
    def proposed_allocation_float(self) -> float:
        return float(self.proposed_allocation or 0)

    @property
    def spend_to_date_float(self) -> float:
        return float(self.spend_to_date or 0)

    @property
    def reported_revenue_float(self) -> float:
        return float(self.reported_revenue or 0)

    @property
    def pending_revenue_float(self) -> float:
        return float(self.pending_revenue or 0)

    @property
    def approved_revenue_float(self) -> float:
        return float(self.approved_revenue or 0)

    @property
    def finalized_revenue_float(self) -> float:
        return float(self.finalized_revenue or 0)

    @property
    def paid_revenue_float(self) -> float:
        return float(self.paid_revenue or 0)

    @property
    def deducted_revenue_float(self) -> float:
        return float(self.deducted_revenue or 0)


class OfferCapReview(TimestampMixin, db.Model):
    __tablename__ = "offer_cap_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    replacement_offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    offer_status = db.Column(db.String(40), nullable=False, default="active")
    cap_type = db.Column(db.String(60), nullable=False, default="daily_conversion")
    cap_period = db.Column(db.String(40), nullable=False, default="daily")
    cap_limit = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    cap_used = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    expected_next_conversions = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    current_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    new_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    approval_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    deduction_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    days_since_cap_update = db.Column(db.Integer, nullable=False, default=0)
    buyer_capacity_status = db.Column(db.String(40), nullable=False, default="unknown")
    replacement_status = db.Column(db.String(40), nullable=False, default="not_needed")
    replacement_fit_score = db.Column(db.Integer, nullable=False, default=0)
    same_intent_review = db.Column(db.Boolean, nullable=False, default=False)
    source_quality = db.Column(db.String(40), nullable=False, default="watch")
    policy_risk = db.Column(db.String(40), nullable=False, default="medium")
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_manual_review"
    )
    cap_usage_percent = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    cap_remaining = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    effective_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    safe_daily_media_cost = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer", foreign_keys=[offer_id])
    replacement_offer = db.relationship("Offer", foreign_keys=[replacement_offer_id])
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def cap_limit_float(self) -> float:
        return float(self.cap_limit or 0)

    @property
    def cap_used_float(self) -> float:
        return float(self.cap_used or 0)

    @property
    def expected_next_conversions_float(self) -> float:
        return float(self.expected_next_conversions or 0)

    @property
    def current_payout_float(self) -> float:
        return float(self.current_payout or 0)

    @property
    def new_payout_float(self) -> float:
        return float(self.new_payout or 0)

    @property
    def effective_payout_float(self) -> float:
        return float(self.effective_payout or 0)

    @property
    def safe_daily_media_cost_float(self) -> float:
        return float(self.safe_daily_media_cost or 0)


class SourceQualityReview(TimestampMixin, db.Model):
    __tablename__ = "source_quality_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    entity_type = db.Column(db.String(40), nullable=False, default="source")
    source_name = db.Column(db.String(180), nullable=False)
    publisher_name = db.Column(db.String(180), nullable=True)
    placement_ref = db.Column(db.String(240), nullable=True)
    subid = db.Column(db.String(160), nullable=True)
    network = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    device = db.Column(db.String(60), nullable=True)
    sample_url = db.Column(db.String(700), nullable=True)
    transparency_level = db.Column(db.String(40), nullable=False, default="partial")
    tracking_completeness_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    intent_fit_score = db.Column(db.Integer, nullable=False, default=0)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    sessions = db.Column(db.Integer, nullable=False, default=0)
    cost = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    reported_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    approved_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    paid_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    deducted_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    invalid_click_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    complaint_count = db.Column(db.Integer, nullable=False, default=0)
    buyer_reject_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    policy_issue_state = db.Column(db.String(40), nullable=False, default="clean")
    stop_control = db.Column(db.String(40), nullable=False, default="partial")
    consistency_days = db.Column(db.Integer, nullable=False, default=0)
    score = db.Column(db.Integer, nullable=False, default=0)
    quality_level = db.Column(db.String(40), nullable=False, default="low")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="watchlist_no_scale"
    )
    click_session_rate = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    approved_rate = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    paid_rate = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    deduction_rate = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    paid_roi = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    approved_roi = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def cost_float(self) -> float:
        return float(self.cost or 0)

    @property
    def reported_revenue_float(self) -> float:
        return float(self.reported_revenue or 0)

    @property
    def approved_revenue_float(self) -> float:
        return float(self.approved_revenue or 0)

    @property
    def paid_revenue_float(self) -> float:
        return float(self.paid_revenue or 0)

    @property
    def deducted_revenue_float(self) -> float:
        return float(self.deducted_revenue or 0)


class VendorContractReview(TimestampMixin, db.Model):
    __tablename__ = "vendor_contract_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    vendor_name = db.Column(db.String(180), nullable=False)
    vendor_type = db.Column(db.String(80), nullable=False, default="traffic_vendor")
    io_number = db.Column(db.String(120), nullable=True)
    line_item_ref = db.Column(db.String(160), nullable=True)
    contract_status = db.Column(db.String(40), nullable=False, default="prospect")
    pricing_model = db.Column(db.String(40), nullable=False, default="cpc")
    source_detail_level = db.Column(db.String(40), nullable=False, default="partial")
    tracking_appendix = db.Column(db.Boolean, nullable=False, default=False)
    reporting_appendix = db.Column(db.Boolean, nullable=False, default=False)
    quality_clause = db.Column(db.Boolean, nullable=False, default=False)
    refund_clause = db.Column(db.Boolean, nullable=False, default=False)
    stop_control = db.Column(db.String(40), nullable=False, default="partial")
    tracking_completeness_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    report_delay_days = db.Column(db.Integer, nullable=False, default=0)
    discrepancy_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    invalid_traffic_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    buyer_reject_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    budget_cap = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    spend_to_date = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    approved_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    paid_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    invoice_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    disputed_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    refund_credit_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    makegood_value = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    dispute_response_days = db.Column(db.Integer, nullable=False, default=0)
    payment_terms_days = db.Column(db.Integer, nullable=False, default=0)
    refund_terms_status = db.Column(db.String(40), nullable=False, default="missing")
    policy_issue_state = db.Column(db.String(40), nullable=False, default="clean")
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="collect_due_diligence"
    )
    amount_at_risk = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    paid_roi = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    approved_roi = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    invoice_dispute_rate = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    credit_coverage_rate = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def budget_cap_float(self) -> float:
        return float(self.budget_cap or 0)

    @property
    def spend_to_date_float(self) -> float:
        return float(self.spend_to_date or 0)

    @property
    def approved_revenue_float(self) -> float:
        return float(self.approved_revenue or 0)

    @property
    def paid_revenue_float(self) -> float:
        return float(self.paid_revenue or 0)

    @property
    def invoice_amount_float(self) -> float:
        return float(self.invoice_amount or 0)

    @property
    def disputed_amount_float(self) -> float:
        return float(self.disputed_amount or 0)

    @property
    def refund_credit_amount_float(self) -> float:
        return float(self.refund_credit_amount or 0)

    @property
    def makegood_value_float(self) -> float:
        return float(self.makegood_value or 0)


class QueryMiningReview(TimestampMixin, db.Model):
    __tablename__ = "query_mining_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    date_window = db.Column(db.String(80), nullable=True)
    ads_customer_id = db.Column(db.String(80), nullable=True)
    campaign_ref = db.Column(db.String(160), nullable=True)
    ad_group_ref = db.Column(db.String(160), nullable=True)
    keyword_text = db.Column(db.String(260), nullable=True)
    keyword_match_type = db.Column(db.String(40), nullable=False, default="broad")
    search_term = db.Column(db.String(500), nullable=False)
    search_term_match_type = db.Column(db.String(80), nullable=True)
    query_intent = db.Column(db.String(60), nullable=False, default="unknown")
    network = db.Column(db.String(60), nullable=False, default="google_search")
    device = db.Column(db.String(60), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    landing_version = db.Column(db.String(120), nullable=True)
    source_file_hash = db.Column(db.String(96), nullable=True)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    sessions = db.Column(db.Integer, nullable=False, default=0)
    conversions = db.Column(db.Integer, nullable=False, default=0)
    cost = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    approved_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    paid_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    buyer_reject_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    intent_fit_score = db.Column(db.Integer, nullable=False, default=0)
    policy_risk = db.Column(db.String(40), nullable=False, default="medium")
    revenue_status = db.Column(db.String(40), nullable=False, default="none")
    data_status = db.Column(db.String(40), nullable=False, default="fresh")
    conversion_lag_days = db.Column(db.Integer, nullable=False, default=0)
    brand_or_official = db.Column(db.Boolean, nullable=False, default=False)
    support_or_login = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_review"
    )
    negative_match_type = db.Column(db.String(40), nullable=False, default="none")
    negative_level = db.Column(db.String(40), nullable=False, default="none")
    click_session_rate = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    approved_rpv = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    paid_rpv = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    approved_roi = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    paid_roi = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def cost_float(self) -> float:
        return float(self.cost or 0)

    @property
    def approved_revenue_float(self) -> float:
        return float(self.approved_revenue or 0)

    @property
    def paid_revenue_float(self) -> float:
        return float(self.paid_revenue or 0)


class BulkUploadReview(TimestampMixin, db.Model):
    __tablename__ = "bulk_upload_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    export_type = db.Column(db.String(60), nullable=False, default="editor_csv")
    batch_id = db.Column(db.String(120), nullable=True)
    csv_hash = db.Column(db.String(128), nullable=True)
    payload_hash = db.Column(db.String(128), nullable=True)
    row_count = db.Column(db.Integer, nullable=False, default=0)
    keyword_count = db.Column(db.Integer, nullable=False, default=0)
    ad_count = db.Column(db.Integer, nullable=False, default=0)
    target_customer_id = db.Column(db.String(80), nullable=True)
    account_timezone = db.Column(db.String(80), nullable=True)
    currency = db.Column(db.String(20), nullable=True)
    expected_budget_delta = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    url_change_count = db.Column(db.Integer, nullable=False, default=0)
    high_risk_change_count = db.Column(db.Integer, nullable=False, default=0)
    preflight_status = db.Column(db.String(40), nullable=False, default="warnings")
    preview_status = db.Column(db.String(40), nullable=False, default="not_run")
    editor_check_status = db.Column(db.String(40), nullable=False, default="not_run")
    post_status = db.Column(db.String(40), nullable=False, default="not_posted")
    default_paused = db.Column(db.Boolean, nullable=False, default=True)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    change_history_attached = db.Column(db.Boolean, nullable=False, default=False)
    rollback_plan = db.Column(db.Boolean, nullable=False, default=False)
    target_customer_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    policy_review_complete = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_review"
    )
    budget_delta_percent = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    change_scope = db.Column(db.String(40), nullable=False, default="small")
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def expected_budget_delta_float(self) -> float:
        return float(self.expected_budget_delta or 0)


class ScriptSyncReview(TimestampMixin, db.Model):
    __tablename__ = "script_sync_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    auth_mode = db.Column(db.String(60), nullable=False, default="scripts_authorized")
    sync_type = db.Column(db.String(60), nullable=False, default="metrics_daily")
    script_name = db.Column(db.String(160), nullable=True)
    customer_id = db.Column(db.String(80), nullable=True)
    date_range = db.Column(db.String(80), nullable=True)
    account_timezone = db.Column(db.String(80), nullable=True)
    currency = db.Column(db.String(20), nullable=True)
    query_or_report = db.Column(db.String(240), nullable=True)
    source_snapshot_hash = db.Column(db.String(128), nullable=True)
    payload_hash = db.Column(db.String(128), nullable=True)
    row_count = db.Column(db.Integer, nullable=False, default=0)
    error_count = db.Column(db.Integer, nullable=False, default=0)
    warning_count = db.Column(db.Integer, nullable=False, default=0)
    freshness_minutes = db.Column(db.Integer, nullable=False, default=0)
    rerun_window_days = db.Column(db.Integer, nullable=False, default=0)
    data_status = db.Column(db.String(40), nullable=False, default="provisional")
    revenue_status = db.Column(db.String(40), nullable=False, default="estimated")
    conflict_status = db.Column(db.String(40), nullable=False, default="clean")
    external_change_count = db.Column(db.Integer, nullable=False, default=0)
    change_history_checked = db.Column(db.Boolean, nullable=False, default=False)
    preview_only = db.Column(db.Boolean, nullable=False, default=True)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    freshness_level = db.Column(db.String(40), nullable=False, default="missing")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_human_review"
    )
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")


class TaxonomyReview(TimestampMixin, db.Model):
    __tablename__ = "taxonomy_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    campaign_name = db.Column(db.String(255), nullable=False)
    ad_group_name = db.Column(db.String(255), nullable=False)
    labels_text = db.Column(db.Text, nullable=True)
    utm_source = db.Column(db.String(120), nullable=True)
    utm_medium = db.Column(db.String(120), nullable=True)
    utm_campaign = db.Column(db.String(255), nullable=True)
    utm_id = db.Column(db.String(160), nullable=True)
    utm_content = db.Column(db.String(255), nullable=True)
    utm_term = db.Column(db.String(255), nullable=True)
    valuetrack_template = db.Column(db.Text, nullable=True)
    custom_parameter_map = db.Column(db.Text, nullable=True)
    subid_map = db.Column(db.Text, nullable=True)
    dimension_dictionary_version = db.Column(db.String(80), nullable=True)
    parameter_map_version = db.Column(db.String(80), nullable=True)
    landing_version = db.Column(db.String(120), nullable=True)
    link_version = db.Column(db.String(120), nullable=True)
    creative_version = db.Column(db.String(120), nullable=True)
    payload_hash = db.Column(db.String(128), nullable=True)
    report_join_gap_count = db.Column(db.Integer, nullable=False, default=0)
    gclid_preserved = db.Column(db.Boolean, nullable=False, default=False)
    click_id_preserved = db.Column(db.Boolean, nullable=False, default=False)
    lowercase_normalized = db.Column(db.Boolean, nullable=False, default=False)
    url_encoded = db.Column(db.Boolean, nullable=False, default=False)
    no_pii_in_url = db.Column(db.Boolean, nullable=False, default=True)
    no_sensitive_attributes = db.Column(db.Boolean, nullable=False, default=True)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_mapping"
    )
    missing_campaign_tokens = db.Column(db.JSON, nullable=False, default=list)
    missing_utm_fields = db.Column(db.JSON, nullable=False, default=list)
    missing_label_groups = db.Column(db.JSON, nullable=False, default=list)
    valuetrack_fields = db.Column(db.JSON, nullable=False, default=list)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")


class AttributionReview(TimestampMixin, db.Model):
    __tablename__ = "attribution_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    test_type = db.Column(db.String(60), nullable=False, default="geo_holdout")
    attribution_model = db.Column(db.String(80), nullable=False, default="data_driven")
    hypothesis = db.Column(db.Text, nullable=True)
    treatment_scope = db.Column(db.Text, nullable=True)
    control_scope = db.Column(db.Text, nullable=True)
    split_method = db.Column(db.String(120), nullable=True)
    date_window = db.Column(db.String(120), nullable=True)
    primary_metric = db.Column(db.String(120), nullable=True)
    guardrail_metrics = db.Column(db.Text, nullable=True)
    attributed_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    treatment_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    control_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    incremental_revenue = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    ad_cost = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    variable_cost = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    incremental_profit = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    i_roas = db.Column(db.Numeric(8, 4), nullable=False, default=0)
    attributed_to_incremental_ratio = db.Column(
        db.Numeric(8, 4), nullable=False, default=0
    )
    attributed_conversions = db.Column(db.Integer, nullable=False, default=0)
    incremental_conversions = db.Column(db.Integer, nullable=False, default=0)
    sample_size = db.Column(db.Integer, nullable=False, default=0)
    confidence_level = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    holdout_quality = db.Column(db.String(40), nullable=False, default="none")
    revenue_status = db.Column(db.String(40), nullable=False, default="submitted")
    data_status = db.Column(db.String(40), nullable=False, default="fresh")
    brand_cannibalization_risk = db.Column(
        db.String(40), nullable=False, default="medium"
    )
    organic_cannibalization_risk = db.Column(
        db.String(40), nullable=False, default="medium"
    )
    remarketing_cannibalization_risk = db.Column(
        db.String(40), nullable=False, default="medium"
    )
    pmax_broad_overlap_risk = db.Column(
        db.String(40), nullable=False, default="medium"
    )
    change_history_clean = db.Column(db.Boolean, nullable=False, default=False)
    single_variable_test = db.Column(db.Boolean, nullable=False, default=False)
    approved_paid_evidence = db.Column(db.Boolean, nullable=False, default=False)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="run_holdout_or_reconcile"
    )
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def attributed_revenue_float(self) -> float:
        return float(self.attributed_revenue or 0)

    @property
    def incremental_revenue_float(self) -> float:
        return float(self.incremental_revenue or 0)

    @property
    def incremental_profit_float(self) -> float:
        return float(self.incremental_profit or 0)

    @property
    def i_roas_float(self) -> float:
        return float(self.i_roas or 0)


class CplVerticalReview(TimestampMixin, db.Model):
    __tablename__ = "cpl_vertical_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    vertical = db.Column(db.String(80), nullable=False, default="insurance")
    subvertical = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    buyer_type = db.Column(db.String(80), nullable=True)
    payout_model = db.Column(db.String(40), nullable=False, default="CPL")
    payout_amount = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    estimated_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    landing_cvr_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    accepted_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    qualified_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    deduction_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    chargeback_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    feedback_lag_days = db.Column(db.Integer, nullable=False, default=0)
    contact_sla_minutes = db.Column(db.Integer, nullable=False, default=0)
    qualification_fields = db.Column(db.Text, nullable=True)
    sensitive_fields = db.Column(db.Text, nullable=True)
    reject_reason_map = db.Column(db.Text, nullable=True)
    accepted_definition = db.Column(db.Text, nullable=True)
    paid_definition = db.Column(db.Text, nullable=True)
    policy_requirements = db.Column(db.Text, nullable=True)
    forbidden_claims = db.Column(db.Text, nullable=True)
    required_fields_mapped = db.Column(db.Boolean, nullable=False, default=False)
    reject_reason_map_ready = db.Column(db.Boolean, nullable=False, default=False)
    accepted_definition_clear = db.Column(db.Boolean, nullable=False, default=False)
    paid_definition_clear = db.Column(db.Boolean, nullable=False, default=False)
    consent_disclosure_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    pii_minimization = db.Column(db.Boolean, nullable=False, default=False)
    license_required = db.Column(db.Boolean, nullable=False, default=False)
    license_evidence_present = db.Column(db.Boolean, nullable=False, default=False)
    buyer_terms_status = db.Column(db.String(40), nullable=False, default="missing")
    source_quality = db.Column(db.String(40), nullable=False, default="medium")
    policy_risk = db.Column(db.String(40), nullable=False, default="medium")
    data_sensitivity = db.Column(db.String(40), nullable=False, default="medium")
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_vertical_rework"
    )
    effective_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    expected_value_per_click = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    safe_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    cpc_margin_percent = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def payout_amount_float(self) -> float:
        return float(self.payout_amount or 0)

    @property
    def estimated_cpc_float(self) -> float:
        return float(self.estimated_cpc or 0)

    @property
    def effective_payout_float(self) -> float:
        return float(self.effective_payout or 0)

    @property
    def expected_value_per_click_float(self) -> float:
        return float(self.expected_value_per_click or 0)

    @property
    def safe_cpc_float(self) -> float:
        return float(self.safe_cpc or 0)


class LeadPricingReview(TimestampMixin, db.Model):
    __tablename__ = "lead_pricing_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    buyer_name = db.Column(db.String(180), nullable=True)
    vertical = db.Column(db.String(80), nullable=False, default="b2b_saas")
    geo = db.Column(db.String(80), nullable=True)
    source_type = db.Column(db.String(80), nullable=False, default="search")
    exclusivity = db.Column(db.String(60), nullable=False, default="exclusive")
    payout_model = db.Column(db.String(40), nullable=False, default="qualified_cpl")
    headline_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    unit_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    proposed_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    minimum_acceptable_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    currency = db.Column(db.String(12), nullable=False, default="USD")
    estimated_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    click_to_lead_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    accepted_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    qualified_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    approval_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    return_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    scrub_buffer_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    chargeback_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    variable_cost_per_click = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    tracking_cost_per_click = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    content_cost_per_click = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    cashflow_cost_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    cap_limit = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    expected_volume = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    return_window_days = db.Column(db.Integer, nullable=False, default=0)
    payment_term_days = db.Column(db.Integer, nullable=False, default=0)
    qualification_definition = db.Column(db.Text, nullable=True)
    rate_card_evidence = db.Column(db.Text, nullable=True)
    negotiation_evidence = db.Column(db.Text, nullable=True)
    reject_reason_summary = db.Column(db.Text, nullable=True)
    invoice_terms = db.Column(db.Text, nullable=True)
    quality_evidence_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    source_transparency = db.Column(db.String(40), nullable=False, default="partial")
    consent_evidence = db.Column(db.String(40), nullable=False, default="missing")
    reject_reason_map_ready = db.Column(db.Boolean, nullable=False, default=False)
    invoice_evidence = db.Column(db.Boolean, nullable=False, default=False)
    dispute_reserve_present = db.Column(db.Boolean, nullable=False, default=False)
    buyer_terms_status = db.Column(db.String(40), nullable=False, default="missing")
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_rate_card"
    )
    effective_payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    paid_epc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    safe_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    margin_per_click = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    reserve_amount = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def headline_payout_float(self) -> float:
        return float(self.headline_payout or 0)

    @property
    def unit_payout_float(self) -> float:
        return float(self.unit_payout or 0)

    @property
    def proposed_payout_float(self) -> float:
        return float(self.proposed_payout or 0)

    @property
    def minimum_acceptable_payout_float(self) -> float:
        return float(self.minimum_acceptable_payout or 0)

    @property
    def estimated_cpc_float(self) -> float:
        return float(self.estimated_cpc or 0)

    @property
    def effective_payout_float(self) -> float:
        return float(self.effective_payout or 0)

    @property
    def paid_epc_float(self) -> float:
        return float(self.paid_epc or 0)

    @property
    def safe_cpc_float(self) -> float:
        return float(self.safe_cpc or 0)

    @property
    def margin_per_click_float(self) -> float:
        return float(self.margin_per_click or 0)

    @property
    def reserve_amount_float(self) -> float:
        return float(self.reserve_amount or 0)


class AppointmentLeadReview(TimestampMixin, db.Model):
    __tablename__ = "appointment_lead_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    buyer_name = db.Column(db.String(180), nullable=True)
    vertical = db.Column(db.String(80), nullable=False, default="healthcare")
    service_type = db.Column(db.String(120), nullable=True)
    geo = db.Column(db.String(80), nullable=True)
    appointment_platform = db.Column(db.String(120), nullable=True)
    payout_event = db.Column(db.String(40), nullable=False, default="showed")
    payout_amount = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    estimated_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    click_to_request_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    request_to_book_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    confirmation_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    show_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    completed_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    cancel_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    no_show_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    duplicate_booking_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    reschedule_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    reminder_cost_per_booking = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    no_show_cost_per_booking = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    available_slots = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    expected_bookings = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    lead_age_hours = db.Column(db.Integer, nullable=False, default=0)
    slot_delay_hours = db.Column(db.Integer, nullable=False, default=0)
    calendar_capacity_status = db.Column(
        db.String(40), nullable=False, default="unknown"
    )
    timezone_status = db.Column(db.String(40), nullable=False, default="unclear")
    reminder_channel = db.Column(db.String(60), nullable=False, default="email")
    reminder_consent_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    confirmation_process_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    buyer_terms_status = db.Column(db.String(40), nullable=False, default="missing")
    status_map = db.Column(db.Text, nullable=True)
    slot_policy = db.Column(db.Text, nullable=True)
    reminder_policy = db.Column(db.Text, nullable=True)
    no_show_reason_map = db.Column(db.Text, nullable=True)
    conversion_mapping = db.Column(db.Text, nullable=True)
    payout_definition_clear = db.Column(db.Boolean, nullable=False, default=False)
    duplicate_window_defined = db.Column(db.Boolean, nullable=False, default=False)
    no_show_reason_map_ready = db.Column(db.Boolean, nullable=False, default=False)
    calendar_capacity_evidence = db.Column(db.Boolean, nullable=False, default=False)
    reminder_template_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    offline_conversion_mapping_ready = db.Column(
        db.Boolean, nullable=False, default=False
    )
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_booking_rework"
    )
    expected_value_per_booking = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    expected_value_per_click = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    safe_cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    cpc_margin_percent = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    safe_appointment_spend = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def payout_amount_float(self) -> float:
        return float(self.payout_amount or 0)

    @property
    def estimated_cpc_float(self) -> float:
        return float(self.estimated_cpc or 0)

    @property
    def reminder_cost_per_booking_float(self) -> float:
        return float(self.reminder_cost_per_booking or 0)

    @property
    def no_show_cost_per_booking_float(self) -> float:
        return float(self.no_show_cost_per_booking or 0)

    @property
    def expected_value_per_booking_float(self) -> float:
        return float(self.expected_value_per_booking or 0)

    @property
    def expected_value_per_click_float(self) -> float:
        return float(self.expected_value_per_click or 0)

    @property
    def safe_cpc_float(self) -> float:
        return float(self.safe_cpc or 0)

    @property
    def safe_appointment_spend_float(self) -> float:
        return float(self.safe_appointment_spend or 0)


class BuyerCapacityReview(TimestampMixin, db.Model):
    __tablename__ = "buyer_capacity_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    buyer_name = db.Column(db.String(180), nullable=True)
    vertical = db.Column(db.String(80), nullable=False, default="b2b_saas")
    geo = db.Column(db.String(80), nullable=True)
    buyer_timezone = db.Column(db.String(80), nullable=False, default="America/New_York")
    account_timezone = db.Column(db.String(80), nullable=False, default="UTC")
    user_timezone_scope = db.Column(db.String(120), nullable=True)
    call_center_timezone = db.Column(db.String(80), nullable=True)
    cap_type = db.Column(db.String(40), nullable=False, default="daily_buyer_cap")
    cap_period = db.Column(db.String(40), nullable=False, default="daily")
    cap_limit = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    cap_used = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    elapsed_operating_day_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    expected_next_hour_leads = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    expected_daily_leads = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    hourly_contact_capacity = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    current_hour_capacity_used = db.Column(
        db.Numeric(12, 2), nullable=False, default=0
    )
    expected_paid_value_per_lead = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    accepted_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    qualified_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    no_buyer_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    missed_contact_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    after_hours_lead_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    cap_last_confirmed_hours = db.Column(db.Integer, nullable=False, default=0)
    feedback_sla_hours = db.Column(db.Integer, nullable=False, default=24)
    first_attempt_sla_minutes = db.Column(db.Integer, nullable=False, default=5)
    cap_confidence_status = db.Column(
        db.String(40), nullable=False, default="unknown"
    )
    hours_alignment_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    ad_schedule_alignment_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    timezone_alignment_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    holiday_readiness_status = db.Column(
        db.String(40), nullable=False, default="unknown"
    )
    fallback_status = db.Column(db.String(40), nullable=False, default="missing")
    source_quality_status = db.Column(db.String(40), nullable=False, default="medium")
    overdelivery_guardrail_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    operating_hours = db.Column(db.Text, nullable=True)
    cap_reset_rule = db.Column(db.Text, nullable=True)
    holiday_calendar = db.Column(db.Text, nullable=True)
    ad_schedule_summary = db.Column(db.Text, nullable=True)
    no_buyer_reason_map = db.Column(db.Text, nullable=True)
    routing_fallback_policy = db.Column(db.Text, nullable=True)
    dayparting_basis = db.Column(db.Text, nullable=True)
    cap_snapshot_evidence = db.Column(db.Boolean, nullable=False, default=False)
    buyer_hours_evidence = db.Column(db.Boolean, nullable=False, default=False)
    ad_schedule_evidence = db.Column(db.Boolean, nullable=False, default=False)
    call_reporting_evidence = db.Column(db.Boolean, nullable=False, default=False)
    no_buyer_tracking_ready = db.Column(db.Boolean, nullable=False, default=False)
    missed_contact_tracking_ready = db.Column(
        db.Boolean, nullable=False, default=False
    )
    dayparting_cohort_ready = db.Column(db.Boolean, nullable=False, default=False)
    fallback_buyer_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="hold_for_capacity_rework"
    )
    cap_usage_percent = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    cap_remaining = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    projected_end_of_day_usage_percent = db.Column(
        db.Numeric(8, 2), nullable=False, default=0
    )
    safe_leads_remaining = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    safe_media_spend_remaining = db.Column(
        db.Numeric(12, 2), nullable=False, default=0
    )
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def cap_limit_float(self) -> float:
        return float(self.cap_limit or 0)

    @property
    def cap_used_float(self) -> float:
        return float(self.cap_used or 0)

    @property
    def expected_paid_value_per_lead_float(self) -> float:
        return float(self.expected_paid_value_per_lead or 0)

    @property
    def cap_remaining_float(self) -> float:
        return float(self.cap_remaining or 0)

    @property
    def safe_leads_remaining_float(self) -> float:
        return float(self.safe_leads_remaining or 0)

    @property
    def safe_media_spend_remaining_float(self) -> float:
        return float(self.safe_media_spend_remaining or 0)


class ConversionSignalReview(TimestampMixin, db.Model):
    __tablename__ = "conversion_signal_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    vertical = db.Column(db.String(80), nullable=False, default="b2b_saas")
    geo = db.Column(db.String(80), nullable=True)
    conversion_goal_name = db.Column(db.String(180), nullable=False)
    conversion_action_name = db.Column(db.String(180), nullable=False)
    action_stage = db.Column(db.String(40), nullable=False, default="submitted")
    primary_status = db.Column(db.String(40), nullable=False, default="secondary")
    recommended_primary_status = db.Column(
        db.String(40), nullable=False, default="secondary_only"
    )
    value_mode = db.Column(db.String(40), nullable=False, default="expected")
    bid_strategy = db.Column(db.String(60), nullable=False, default="manual_cpc")
    traffic_scope = db.Column(db.String(80), nullable=False, default="search_exact")
    weekly_conversions = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    weekly_approved_conversions = db.Column(
        db.Numeric(12, 2), nullable=False, default=0
    )
    weekly_paid_conversions = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    reported_value_per_conversion = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    approved_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    click_id_coverage_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    offline_match_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    duplicate_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    average_lag_days = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    p95_lag_days = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    incident_count_30d = db.Column(db.Integer, nullable=False, default=0)
    segment_granularity_status = db.Column(
        db.String(40), nullable=False, default="mixed"
    )
    policy_consent_status = db.Column(db.String(40), nullable=False, default="missing")
    customer_data_status = db.Column(db.String(40), nullable=False, default="missing")
    offline_import_status = db.Column(db.String(40), nullable=False, default="none")
    transaction_id_status = db.Column(db.String(40), nullable=False, default="missing")
    lag_stability_status = db.Column(db.String(40), nullable=False, default="unknown")
    bid_strategy_status = db.Column(db.String(40), nullable=False, default="unknown")
    goal_change_summary = db.Column(db.Text, nullable=True)
    affected_campaigns = db.Column(db.Text, nullable=True)
    value_mapping_notes = db.Column(db.Text, nullable=True)
    dedupe_notes = db.Column(db.Text, nullable=True)
    lag_notes = db.Column(db.Text, nullable=True)
    diagnostics_notes = db.Column(db.Text, nullable=True)
    rollback_plan = db.Column(db.Text, nullable=True)
    primary_secondary_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    value_mapping_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    transaction_id_dedupe_ready = db.Column(
        db.Boolean, nullable=False, default=False
    )
    offline_import_diagnostics_ready = db.Column(
        db.Boolean, nullable=False, default=False
    )
    conversion_lag_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    segment_split_ready = db.Column(db.Boolean, nullable=False, default=False)
    consent_policy_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    bid_strategy_report_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    change_history_evidence = db.Column(db.Boolean, nullable=False, default=False)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score_components = db.Column(db.JSON, nullable=False, default=dict)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="fix_conversion_signal"
    )
    bid_readiness = db.Column(db.String(40), nullable=False, default="blocked")
    expected_paid_value_per_conversion = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    safe_target_cpa = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def weekly_conversions_float(self) -> float:
        return float(self.weekly_conversions or 0)

    @property
    def weekly_approved_conversions_float(self) -> float:
        return float(self.weekly_approved_conversions or 0)

    @property
    def weekly_paid_conversions_float(self) -> float:
        return float(self.weekly_paid_conversions or 0)

    @property
    def reported_value_per_conversion_float(self) -> float:
        return float(self.reported_value_per_conversion or 0)

    @property
    def expected_paid_value_per_conversion_float(self) -> float:
        return float(self.expected_paid_value_per_conversion or 0)

    @property
    def safe_target_cpa_float(self) -> float:
        return float(self.safe_target_cpa or 0)


class CrmValueMappingReview(TimestampMixin, db.Model):
    __tablename__ = "crm_value_mapping_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    buyer_name = db.Column(db.String(180), nullable=True)
    vertical = db.Column(db.String(80), nullable=False, default="b2b_saas")
    geo = db.Column(db.String(80), nullable=True)
    source_system = db.Column(db.String(120), nullable=False, default="crm")
    buyer_feedback_source = db.Column(db.String(120), nullable=True)
    source_stage = db.Column(db.String(120), nullable=False)
    standard_stage = db.Column(db.String(40), nullable=False, default="submitted")
    buyer_status = db.Column(db.String(80), nullable=True)
    conversion_action_name = db.Column(db.String(180), nullable=False)
    conversion_action_role = db.Column(db.String(40), nullable=False, default="secondary")
    primary_recommendation = db.Column(
        db.String(40), nullable=False, default="secondary_only"
    )
    value_mode = db.Column(db.String(40), nullable=False, default="expected")
    recommended_upload_policy = db.Column(
        db.String(60), nullable=False, default="do_not_upload"
    )
    payout_amount = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    approved_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    return_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    variable_cost_per_conversion = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    weekly_stage_count = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    weekly_unique_leads = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    rejected_count = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    returned_count = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    duplicate_count = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    click_id_match_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    import_success_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    import_error_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    average_stage_lag_days = db.Column(db.Numeric(8, 2), nullable=False, default=0)
    return_window_days = db.Column(db.Integer, nullable=False, default=0)
    transaction_id_status = db.Column(db.String(40), nullable=False, default="missing")
    adjustment_rule_status = db.Column(db.String(40), nullable=False, default="missing")
    import_batch_status = db.Column(db.String(40), nullable=False, default="draft")
    diagnostics_status = db.Column(db.String(40), nullable=False, default="missing")
    consent_status = db.Column(db.String(40), nullable=False, default="missing")
    pii_handling_status = db.Column(db.String(40), nullable=False, default="unknown")
    stage_mapping_notes = db.Column(db.Text, nullable=True)
    conversion_action_notes = db.Column(db.Text, nullable=True)
    value_mapping_notes = db.Column(db.Text, nullable=True)
    transaction_id_notes = db.Column(db.Text, nullable=True)
    import_qa_notes = db.Column(db.Text, nullable=True)
    adjustment_notes = db.Column(db.Text, nullable=True)
    lag_notes = db.Column(db.Text, nullable=True)
    diagnostics_notes = db.Column(db.Text, nullable=True)
    rollback_plan = db.Column(db.Text, nullable=True)
    stage_taxonomy_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    buyer_feedback_contract_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    conversion_action_mapping_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    primary_secondary_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    value_mode_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    transaction_id_rule_ready = db.Column(
        db.Boolean, nullable=False, default=False
    )
    rejected_returned_excluded = db.Column(
        db.Boolean, nullable=False, default=False
    )
    adjustment_policy_ready = db.Column(db.Boolean, nullable=False, default=False)
    import_batch_qa_ready = db.Column(db.Boolean, nullable=False, default=False)
    diagnostics_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    lag_profile_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    consent_policy_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score_components = db.Column(db.JSON, nullable=False, default=dict)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="fix_stage_mapping"
    )
    expected_value = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def payout_amount_float(self) -> float:
        return float(self.payout_amount or 0)

    @property
    def variable_cost_per_conversion_float(self) -> float:
        return float(self.variable_cost_per_conversion or 0)

    @property
    def weekly_stage_count_float(self) -> float:
        return float(self.weekly_stage_count or 0)

    @property
    def weekly_unique_leads_float(self) -> float:
        return float(self.weekly_unique_leads or 0)

    @property
    def expected_value_float(self) -> float:
        return float(self.expected_value or 0)


class LeadValidationReview(TimestampMixin, db.Model):
    __tablename__ = "lead_validation_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    vertical = db.Column(db.String(80), nullable=False, default="insurance")
    geo = db.Column(db.String(80), nullable=True)
    source_type = db.Column(db.String(80), nullable=False, default="google_search")
    form_version = db.Column(db.String(120), nullable=True)
    validation_scope = db.Column(db.String(80), nullable=False, default="pre_routing")
    lead_channel = db.Column(db.String(60), nullable=False, default="web_form")
    consent_status = db.Column(db.String(60), nullable=False, default="missing")
    buyer_disclosure_status = db.Column(
        db.String(60), nullable=False, default="missing"
    )
    phone_status = db.Column(db.String(60), nullable=False, default="unknown")
    email_status = db.Column(db.String(60), nullable=False, default="unknown")
    address_geo_status = db.Column(db.String(60), nullable=False, default="unknown")
    duplicate_status = db.Column(db.String(60), nullable=False, default="missing")
    suppression_status = db.Column(db.String(60), nullable=False, default="missing")
    dnc_status = db.Column(db.String(60), nullable=False, default="missing")
    opt_out_status = db.Column(db.String(60), nullable=False, default="missing")
    pii_minimization_status = db.Column(
        db.String(60), nullable=False, default="unknown"
    )
    retention_status = db.Column(db.String(60), nullable=False, default="missing")
    source_policy_status = db.Column(db.String(60), nullable=False, default="unknown")
    buyer_reject_feedback_status = db.Column(
        db.String(60), nullable=False, default="missing"
    )
    validation_sample_size = db.Column(db.Integer, nullable=False, default=0)
    valid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    invalid_contact_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    duplicate_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    suppression_hit_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    dnc_hit_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    opt_out_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    bad_geo_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    no_consent_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    buyer_reject_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    complaint_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    fields_collected_schema = db.Column(db.Text, nullable=True)
    validation_rule_summary = db.Column(db.Text, nullable=True)
    duplicate_rule_summary = db.Column(db.Text, nullable=True)
    suppression_rule_summary = db.Column(db.Text, nullable=True)
    pii_handling_notes = db.Column(db.Text, nullable=True)
    retention_deletion_notes = db.Column(db.Text, nullable=True)
    buyer_reject_reason_map = db.Column(db.Text, nullable=True)
    source_form_fix_plan = db.Column(db.Text, nullable=True)
    incident_notes = db.Column(db.Text, nullable=True)
    consent_evidence = db.Column(db.Boolean, nullable=False, default=False)
    buyer_disclosure_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    field_minimization_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    duplicate_rule_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    suppression_dnc_checked = db.Column(db.Boolean, nullable=False, default=False)
    pii_access_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    retention_policy_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    reject_reason_mapped = db.Column(db.Boolean, nullable=False, default=False)
    source_policy_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score_components = db.Column(db.JSON, nullable=False, default=dict)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="validation_review"
    )
    usable_lead_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    expected_valid_leads = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    safe_routing_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def usable_lead_rate_percent_float(self) -> float:
        return float(self.usable_lead_rate_percent or 0)

    @property
    def expected_valid_leads_float(self) -> float:
        return float(self.expected_valid_leads or 0)

    @property
    def safe_routing_rate_percent_float(self) -> float:
        return float(self.safe_routing_rate_percent or 0)


class PingPostRoutingReview(TimestampMixin, db.Model):
    __tablename__ = "ping_post_routing_reviews"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    name = db.Column(db.String(180), nullable=False)
    vertical = db.Column(db.String(80), nullable=False, default="insurance")
    geo = db.Column(db.String(80), nullable=True)
    buyer_group_name = db.Column(db.String(180), nullable=True)
    source_type = db.Column(db.String(80), nullable=False, default="google_search")
    form_version = db.Column(db.String(120), nullable=True)
    routing_mode = db.Column(db.String(60), nullable=False, default="ping_post")
    lead_type = db.Column(db.String(40), nullable=False, default="exclusive")
    consent_scope = db.Column(db.String(80), nullable=False, default="single_buyer")
    buyer_disclosure_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    ping_field_scope = db.Column(db.String(40), nullable=False, default="unknown")
    pii_level = db.Column(db.String(40), nullable=False, default="unknown")
    suppression_status = db.Column(db.String(40), nullable=False, default="missing")
    dnc_status = db.Column(db.String(40), nullable=False, default="missing")
    cap_snapshot_status = db.Column(db.String(40), nullable=False, default="missing")
    fallback_status = db.Column(db.String(40), nullable=False, default="missing")
    buyer_feedback_status = db.Column(
        db.String(40), nullable=False, default="missing"
    )
    source_policy_status = db.Column(db.String(40), nullable=False, default="unknown")
    buyer_count = db.Column(db.Integer, nullable=False, default=0)
    max_post_buyers = db.Column(db.Integer, nullable=False, default=1)
    pinged_buyers = db.Column(db.Integer, nullable=False, default=0)
    accepted_buyers = db.Column(db.Integer, nullable=False, default=0)
    posted_buyers = db.Column(db.Integer, nullable=False, default=0)
    primary_buyer_cap_remaining = db.Column(
        db.Numeric(12, 2), nullable=False, default=0
    )
    cap_last_checked_minutes = db.Column(db.Integer, nullable=False, default=0)
    lead_age_minutes = db.Column(db.Integer, nullable=False, default=0)
    avg_ping_latency_ms = db.Column(db.Integer, nullable=False, default=0)
    expected_bid_amount = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    fallback_payout_amount = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    buyer_accept_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    qualification_rate_percent = db.Column(
        db.Numeric(6, 2), nullable=False, default=0
    )
    paid_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    no_buyer_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    reject_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    duplicate_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    complaint_rate_percent = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    fields_sent_schema = db.Column(db.Text, nullable=True)
    routing_rule_summary = db.Column(db.Text, nullable=True)
    buyer_disclosure_notes = db.Column(db.Text, nullable=True)
    cap_snapshot_notes = db.Column(db.Text, nullable=True)
    reject_reason_map = db.Column(db.Text, nullable=True)
    fallback_policy = db.Column(db.Text, nullable=True)
    buyer_feedback_plan = db.Column(db.Text, nullable=True)
    suppression_notes = db.Column(db.Text, nullable=True)
    consent_evidence_notes = db.Column(db.Text, nullable=True)
    incident_notes = db.Column(db.Text, nullable=True)
    consent_version_evidence = db.Column(db.Boolean, nullable=False, default=False)
    buyer_disclosure_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    field_minimization_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    suppression_dnc_checked = db.Column(db.Boolean, nullable=False, default=False)
    cap_snapshot_evidence = db.Column(db.Boolean, nullable=False, default=False)
    routing_rule_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    exclusive_shared_terms_reviewed = db.Column(
        db.Boolean, nullable=False, default=False
    )
    fallback_buyer_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    buyer_feedback_ready = db.Column(db.Boolean, nullable=False, default=False)
    source_policy_reviewed = db.Column(db.Boolean, nullable=False, default=False)
    human_review = db.Column(db.Boolean, nullable=False, default=False)
    score_components = db.Column(db.JSON, nullable=False, default=dict)
    score = db.Column(db.Integer, nullable=False, default=0)
    risk_level = db.Column(db.String(40), nullable=False, default="high")
    recommended_action = db.Column(
        db.String(80), nullable=False, default="fix_consent_and_routing"
    )
    expected_payable_value_per_lead = db.Column(
        db.Numeric(12, 4), nullable=False, default=0
    )
    safe_cpl = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    blockers = db.Column(db.JSON, nullable=False, default=list)
    status = db.Column(db.String(40), nullable=False, default="open")
    notes = db.Column(db.Text, nullable=True)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")

    @property
    def expected_bid_amount_float(self) -> float:
        return float(self.expected_bid_amount or 0)

    @property
    def fallback_payout_amount_float(self) -> float:
        return float(self.fallback_payout_amount or 0)

    @property
    def primary_buyer_cap_remaining_float(self) -> float:
        return float(self.primary_buyer_cap_remaining or 0)

    @property
    def expected_payable_value_per_lead_float(self) -> float:
        return float(self.expected_payable_value_per_lead or 0)

    @property
    def safe_cpl_float(self) -> float:
        return float(self.safe_cpl or 0)


class LinkRule(TimestampMixin, db.Model):
    __tablename__ = "link_rules"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    name = db.Column(db.String(160), nullable=False)
    current_url = db.Column(db.String(700), nullable=False)
    candidate_urls = db.Column(db.JSON, nullable=False, default=list)
    rotation_reason = db.Column(db.String(240), nullable=False)
    frequency_minutes = db.Column(db.Integer, nullable=False, default=1440)
    require_manual_review = db.Column(db.Boolean, nullable=False, default=True)
    status = db.Column(db.String(40), nullable=False, default="draft")
    last_rotated_at = db.Column(db.DateTime, nullable=True)

    offer = db.relationship("Offer", back_populates="link_rules")


class RiskAudit(TimestampMixin, db.Model):
    __tablename__ = "risk_audits"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    capability = db.Column(db.String(120), nullable=False)
    severity = db.Column(db.String(20), nullable=False, default="medium")
    status = db.Column(db.String(40), nullable=False, default="open")
    finding = db.Column(db.Text, nullable=False)
    mitigation = db.Column(db.Text, nullable=False)
    source_urls = db.Column(db.JSON, nullable=False, default=list)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")


class ResearchSource(TimestampMixin, db.Model):
    __tablename__ = "research_sources"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), nullable=False)
    capability = db.Column(db.String(120), nullable=True)
    title = db.Column(db.String(220), nullable=False)
    url = db.Column(db.String(800), nullable=False)
    publisher = db.Column(db.String(140), nullable=False, default="unknown")
    source_type = db.Column(db.String(80), nullable=False, default="policy")
    reliability = db.Column(db.String(40), nullable=False, default="primary")
    review_status = db.Column(db.String(40), nullable=False, default="candidate")
    claim_summary = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    retrieved_on = db.Column(db.Date, nullable=False, default=date.today)


class OpportunityAssessment(TimestampMixin, db.Model):
    __tablename__ = "opportunity_assessments"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    name = db.Column(db.String(160), nullable=False)
    revenue_model = db.Column(db.String(40), nullable=False, default="CPA")
    session_rpm = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    payout = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    cvr_percent = db.Column(db.Numeric(8, 4), nullable=False, default=0)
    cpc = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    safety_factor = db.Column(db.Numeric(6, 4), nullable=False, default=0.6)
    target_clicks = db.Column(db.Integer, nullable=False, default=100)
    policy_score = db.Column(db.Integer, nullable=False, default=70)
    content_score = db.Column(db.Integer, nullable=False, default=70)
    tracking_score = db.Column(db.Integer, nullable=False, default=70)
    source_score = db.Column(db.Integer, nullable=False, default=70)
    cash_buffer_days = db.Column(db.Integer, nullable=False, default=14)
    result = db.Column(db.JSON, nullable=False, default=dict)
    recommendation = db.Column(db.String(40), nullable=False, default="review")

    offer = db.relationship("Offer")


class TaskJob(TimestampMixin, db.Model):
    __tablename__ = "task_jobs"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=True)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    link_rule_id = db.Column(db.Integer, db.ForeignKey("link_rules.id"), nullable=True)
    name = db.Column(db.String(160), nullable=False)
    task_type = db.Column(db.String(80), nullable=False)
    schedule_mode = db.Column(db.String(40), nullable=False, default="manual")
    interval_minutes = db.Column(db.Integer, nullable=False, default=1440)
    status = db.Column(db.String(40), nullable=False, default="ready")
    run_count = db.Column(db.Integer, nullable=False, default=0)
    success_count = db.Column(db.Integer, nullable=False, default=0)
    failure_count = db.Column(db.Integer, nullable=False, default=0)
    last_run_at = db.Column(db.DateTime, nullable=True)
    next_run_at = db.Column(db.DateTime, nullable=True)
    last_result = db.Column(db.JSON, nullable=False, default=dict)
    notes = db.Column(db.Text, nullable=True)

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")
    link_rule = db.relationship("LinkRule")


class OptimizationAction(TimestampMixin, db.Model):
    __tablename__ = "optimization_actions"

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey("offers.id"), nullable=False)
    campaign_draft_id = db.Column(
        db.Integer, db.ForeignKey("campaign_drafts.id"), nullable=True
    )
    severity = db.Column(db.String(20), nullable=False, default="info")
    action_type = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="open")

    offer = db.relationship("Offer")
    campaign_draft = db.relationship("CampaignDraft")


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.Integer, nullable=True)
    action = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


def add_audit(entity_type: str, entity_id: int | None, action: str, message: str) -> None:
    db.session.add(
        AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            message=message,
        )
    )


def decimal_value(value: str | float | int | Decimal | None, default: str = "0") -> Decimal:
    if value in (None, ""):
        return Decimal(default)
    return Decimal(str(value))


def seed_demo_data() -> None:
    if Offer.query.count():
        added = _seed_demo_research_sources()
        claim_reviews_added = _seed_demo_claim_reviews()
        ad_review_cases_added = _seed_demo_ad_review_cases()
        decision_reviews_added = _seed_demo_decision_window_reviews()
        budget_reviews_added = _seed_demo_budget_pacing_reviews()
        portfolio_reviews_added = _seed_demo_portfolio_allocation_reviews()
        offer_cap_reviews_added = _seed_demo_offer_cap_reviews()
        source_quality_reviews_added = _seed_demo_source_quality_reviews()
        vendor_contract_reviews_added = _seed_demo_vendor_contract_reviews()
        query_mining_reviews_added = _seed_demo_query_mining_reviews()
        bulk_upload_reviews_added = _seed_demo_bulk_upload_reviews()
        script_sync_reviews_added = _seed_demo_script_sync_reviews()
        taxonomy_reviews_added = _seed_demo_taxonomy_reviews()
        attribution_reviews_added = _seed_demo_attribution_reviews()
        cpl_vertical_reviews_added = _seed_demo_cpl_vertical_reviews()
        lead_pricing_reviews_added = _seed_demo_lead_pricing_reviews()
        appointment_lead_reviews_added = _seed_demo_appointment_lead_reviews()
        buyer_capacity_reviews_added = _seed_demo_buyer_capacity_reviews()
        lead_validation_reviews_added = _seed_demo_lead_validation_reviews()
        conversion_signal_reviews_added = _seed_demo_conversion_signal_reviews()
        crm_value_mapping_reviews_added = _seed_demo_crm_value_mapping_reviews()
        ping_post_routing_reviews_added = _seed_demo_ping_post_routing_reviews()
        if added:
            add_audit("research_source", None, "seed", f"Inserted {added} demo research sources.")
        if claim_reviews_added:
            add_audit(
                "creative_claim_review",
                None,
                "seed",
                f"Inserted {claim_reviews_added} demo creative claim reviews.",
            )
        if ad_review_cases_added:
            add_audit(
                "ad_review_case",
                None,
                "seed",
                f"Inserted {ad_review_cases_added} demo ad review cases.",
            )
        if decision_reviews_added:
            add_audit(
                "decision_window_review",
                None,
                "seed",
                f"Inserted {decision_reviews_added} demo decision window reviews.",
            )
        if budget_reviews_added:
            add_audit(
                "budget_pacing_review",
                None,
                "seed",
                f"Inserted {budget_reviews_added} demo budget pacing reviews.",
            )
        if portfolio_reviews_added:
            add_audit(
                "portfolio_allocation_review",
                None,
                "seed",
                f"Inserted {portfolio_reviews_added} demo portfolio allocation reviews.",
            )
        if offer_cap_reviews_added:
            add_audit(
                "offer_cap_review",
                None,
                "seed",
                f"Inserted {offer_cap_reviews_added} demo offer cap reviews.",
            )
        if source_quality_reviews_added:
            add_audit(
                "source_quality_review",
                None,
                "seed",
                f"Inserted {source_quality_reviews_added} demo source quality reviews.",
            )
        if vendor_contract_reviews_added:
            add_audit(
                "vendor_contract_review",
                None,
                "seed",
                f"Inserted {vendor_contract_reviews_added} demo vendor contract reviews.",
            )
        if query_mining_reviews_added:
            add_audit(
                "query_mining_review",
                None,
                "seed",
                f"Inserted {query_mining_reviews_added} demo query mining reviews.",
            )
        if bulk_upload_reviews_added:
            add_audit(
                "bulk_upload_review",
                None,
                "seed",
                f"Inserted {bulk_upload_reviews_added} demo bulk upload reviews.",
            )
        if script_sync_reviews_added:
            add_audit(
                "script_sync_review",
                None,
                "seed",
                f"Inserted {script_sync_reviews_added} demo script sync reviews.",
            )
        if taxonomy_reviews_added:
            add_audit(
                "taxonomy_review",
                None,
                "seed",
                f"Inserted {taxonomy_reviews_added} demo taxonomy reviews.",
            )
        if attribution_reviews_added:
            add_audit(
                "attribution_review",
                None,
                "seed",
                f"Inserted {attribution_reviews_added} demo attribution reviews.",
            )
        if cpl_vertical_reviews_added:
            add_audit(
                "cpl_vertical_review",
                None,
                "seed",
                f"Inserted {cpl_vertical_reviews_added} demo CPL vertical reviews.",
            )
        if lead_pricing_reviews_added:
            add_audit(
                "lead_pricing_review",
                None,
                "seed",
                f"Inserted {lead_pricing_reviews_added} demo lead pricing reviews.",
            )
        if appointment_lead_reviews_added:
            add_audit(
                "appointment_lead_review",
                None,
                "seed",
                f"Inserted {appointment_lead_reviews_added} demo appointment lead reviews.",
            )
        if buyer_capacity_reviews_added:
            add_audit(
                "buyer_capacity_review",
                None,
                "seed",
                f"Inserted {buyer_capacity_reviews_added} demo buyer capacity reviews.",
            )
        if lead_validation_reviews_added:
            add_audit(
                "lead_validation_review",
                None,
                "seed",
                f"Inserted {lead_validation_reviews_added} demo Lead validation reviews.",
            )
        if conversion_signal_reviews_added:
            add_audit(
                "conversion_signal_review",
                None,
                "seed",
                f"Inserted {conversion_signal_reviews_added} demo conversion signal reviews.",
            )
        if crm_value_mapping_reviews_added:
            add_audit(
                "crm_value_mapping_review",
                None,
                "seed",
                f"Inserted {crm_value_mapping_reviews_added} demo CRM value mapping reviews.",
            )
        if ping_post_routing_reviews_added:
            add_audit(
                "ping_post_routing_review",
                None,
                "seed",
                f"Inserted {ping_post_routing_reviews_added} demo Ping/Post routing reviews.",
            )
        if (
            added
            or ping_post_routing_reviews_added
            or crm_value_mapping_reviews_added
            or conversion_signal_reviews_added
            or lead_validation_reviews_added
            or buyer_capacity_reviews_added
            or appointment_lead_reviews_added
            or claim_reviews_added
            or ad_review_cases_added
            or decision_reviews_added
            or budget_reviews_added
            or portfolio_reviews_added
            or offer_cap_reviews_added
            or source_quality_reviews_added
            or vendor_contract_reviews_added
            or query_mining_reviews_added
            or bulk_upload_reviews_added
            or script_sync_reviews_added
            or taxonomy_reviews_added
            or attribution_reviews_added
            or cpl_vertical_reviews_added
            or lead_pricing_reviews_added
        ):
            db.session.commit()
        return

    offer = Offer(
        name="Cloud Backup Comparison",
        vertical="B2B SaaS",
        country="US",
        language="en",
        payout_model="CPA",
        payout_value=Decimal("42.00"),
        target_url="https://example.com/cloud-backup",
        tracking_url="https://trk.example.com/click?offer=cloud-backup",
        policy_notes="Use original comparison content. Avoid official-brand claims.",
        status="testing",
    )
    db.session.add(offer)
    account = AdsAccount(
        name="Demo Google Ads Account",
        platform="Google Ads",
        customer_id="123-456-7890",
        sync_method="Google Ads Scripts",
        notes="Demo account. Use CSV/Scripts/manual approval; no cookie automation.",
    )
    db.session.add(account)
    db.session.flush()

    landing = LandingPage(
        offer_id=offer.id,
        url=offer.target_url,
        http_status=200,
        title="Cloud Backup Tools Compared",
        description="A practical comparison of backup tools for small teams.",
        h1="Best Cloud Backup Tools",
        h2="Security, Pricing, Restore Speed",
        word_count=1250,
        internal_links=12,
        external_links=8,
        technical_score=35,
        transparency_score=30,
        relevance_score=28,
        quality_score=93,
        raw_summary=(
            "Title: Cloud Backup Tools Compared\n"
            "Description: A practical comparison of backup tools for small teams.\n"
            "H1: Best Cloud Backup Tools\n"
            "Readable words: 1250\n"
            "CTA texts: Compare plans | Review checklist\n"
            "Price/value snippets: Pricing table compares monthly cost and restore limits.\n"
            "Claim snippets: Compare secure cloud backup options before choosing a plan.\n"
            "Proof/review snippets: Editorial comparison covers features, pricing, and restore options.\n"
            "Forms: 0 forms / 0 user inputs"
        ),
    )
    db.session.add(landing)

    creative = CreativeSet(
        offer_id=offer.id,
        angle="Comparison",
        headlines=[
            "Compare Cloud Backup",
            "Backup Tools For Teams",
            "Find Secure Backup Plans",
        ],
        descriptions=[
            "Compare secure cloud backup options before choosing a plan.",
            "Review features, pricing, and restore options for small teams.",
        ],
        keywords=["cloud backup comparison", "best backup software", "team backup tools"],
    )
    db.session.add(creative)
    db.session.flush()
    db.session.add(
        CreativeClaimReview(
            creative_set_id=creative.id,
            asset_type="description",
            asset_text="Review features, pricing, and restore options for small teams.",
            issue="Review or testimonial claim",
            severity="medium",
            action="Needs verifiable review source and disclosure for any commercial relationship.",
            evidence="Editorial comparison covers features, pricing, and restore options.",
            source_url="https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides",
        )
    )

    campaign = CampaignDraft(
        offer_id=offer.id,
        creative_set_id=creative.id,
        name="US Search - Cloud Backup - Test",
        channel="Google Search",
        daily_budget=Decimal("50.00"),
        bid_strategy="Maximize Clicks",
        final_url=offer.target_url,
        status="draft",
    )
    db.session.add(campaign)
    db.session.flush()
    db.session.add(
        AdReviewCase(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            creative_set_id=creative.id,
            object_type="ad",
            object_ref="Demo RSA draft",
            policy_topic="Misrepresentation / claim substantiation",
            severity="medium",
            status="open",
            final_url=offer.target_url,
            expanded_url=offer.target_url,
            finding=(
                "Demo case: review copy that mentions secure backup and pricing before export."
            ),
            change_summary=(
                "Keep comparison wording, verify pricing table and proof snippets, "
                "and avoid guarantee or official relationship claims."
            ),
            evidence_urls=[
                "https://support.google.com/adspolicy/answer/6020955",
                "https://support.google.com/google-ads/answer/9338593",
            ],
            appeal_text=(
                "If rejected, appeal only after the ad text and landing page evidence are fixed."
            ),
            reviewer="demo reviewer",
        )
    )

    db.session.add(
        MetricDaily(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            day=date.today(),
            channel="Google Ads",
            country="US",
            device="desktop",
            impressions=2200,
            clicks=180,
            cost=Decimal("92.40"),
            conversions=4,
            revenue=Decimal("168.00"),
        )
    )
    db.session.add(
        DecisionWindowReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo maturity check",
            data_status="mature",
            revenue_status="approved",
            conversion_lag_days=7,
            approval_lag_days=5,
            settlement_lag_days=10,
            sample_clicks=180,
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("0.00"),
            source_quality="stable",
            incident_state="clean",
            score=82,
            maturity="mostly_mature",
            recommended_action="small_ramp",
            blockers=["paid revenue is not available yet"],
            status="open",
            notes="Demo decision: small ramp only after approved revenue is reviewed.",
            source_urls=[
                "https://support.google.com/google-ads/answer/9347141",
                "https://support.google.com/adsense/answer/7164703",
            ],
        )
    )
    db.session.add(
        BudgetPacingReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo budget ramp gate",
            current_daily_budget=Decimal("50.00"),
            proposed_daily_budget=Decimal("60.00"),
            test_budget=Decimal("150.00"),
            hard_stop=Decimal("180.00"),
            spend_to_date=Decimal("96.00"),
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("0.00"),
            safe_cpc=Decimal("0.55"),
            actual_cpc=Decimal("0.48"),
            sample_clicks=200,
            data_status="mature",
            revenue_status="approved",
            source_quality="stable",
            incident_state="clean",
            cash_buffer_days=30,
            overdelivery_buffer_percent=Decimal("20.00"),
            score=87,
            risk_level="low",
            recommended_action="approve_manual_ramp",
            increase_percent=Decimal("20.00"),
            remaining_test_budget=Decimal("54.00"),
            remaining_hard_stop=Decimal("84.00"),
            blockers=[],
            status="open",
            notes="Demo: approved revenue and safe CPC allow a manual +20% review.",
            source_urls=[
                "https://support.google.com/google-ads/answer/10702522",
                "https://support.google.com/google-ads/answer/1704443",
            ],
        )
    )
    db.session.add(
        PortfolioAllocationReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo portfolio exposure review",
            portfolio_bucket="scale",
            monthly_media_budget=Decimal("3000.00"),
            proposed_allocation=Decimal("450.00"),
            spend_to_date=Decimal("960.00"),
            reported_revenue=Decimal("220.00"),
            pending_revenue=Decimal("80.00"),
            approved_revenue=Decimal("168.00"),
            finalized_revenue=Decimal("0.00"),
            paid_revenue=Decimal("0.00"),
            deducted_revenue=Decimal("0.00"),
            single_offer_exposure_percent=Decimal("18.00"),
            single_source_exposure_percent=Decimal("22.00"),
            single_account_exposure_percent=Decimal("24.00"),
            single_partner_exposure_percent=Decimal("28.00"),
            cash_reserve_days=35,
            source_quality="stable",
            policy_risk="low",
            incident_state="clean",
            score=82,
            risk_level="medium",
            recommended_action="hold_or_small_test",
            allocation_percent=Decimal("15.00"),
            remaining_monthly_budget=Decimal("1590.00"),
            cash_at_risk=Decimal("530.00"),
            revenue_quality_ratio=Decimal("35.90"),
            blockers=["paid revenue is not available yet"],
            status="open",
            notes=(
                "Demo: concentration is under guardrails, but paid revenue is not ready "
                "for Core allocation."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/10702522",
                "https://support.google.com/adsense/answer/7164703",
            ],
        )
    )
    db.session.add(
        OfferCapReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo offer cap and payout check",
            offer_status="active",
            cap_type="daily_conversion",
            cap_period="daily",
            cap_limit=Decimal("20.00"),
            cap_used=Decimal("12.00"),
            expected_next_conversions=Decimal("3.00"),
            current_payout=Decimal("42.0000"),
            new_payout=Decimal("42.0000"),
            approval_rate_percent=Decimal("82.00"),
            paid_rate_percent=Decimal("74.00"),
            deduction_rate_percent=Decimal("5.00"),
            days_since_cap_update=1,
            buyer_capacity_status="open",
            replacement_status="preapproved",
            replacement_fit_score=86,
            same_intent_review=True,
            source_quality="stable",
            policy_risk="low",
            score=88,
            risk_level="low",
            recommended_action="approve_manual_test",
            cap_usage_percent=Decimal("60.00"),
            cap_remaining=Decimal("8.00"),
            effective_payout=Decimal("24.2138"),
            safe_daily_media_cost=Decimal("72.64"),
            blockers=[],
            status="open",
            notes="Demo: cap is under watch threshold and replacement has same-intent review.",
            source_urls=[
                "https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps",
                "https://developers.everflow.io/docs/affiliate/offers/",
            ],
        )
    )
    db.session.add(
        SourceQualityReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo source quality review",
            entity_type="placement",
            source_name="Google Search",
            publisher_name="Search intent segment",
            placement_ref="cloud backup comparison query group",
            subid="kw_cloud_backup_compare",
            network="Google Ads Search",
            country="US",
            device="desktop",
            sample_url="https://example.com/cloud-backup?utm_source=google",
            transparency_level="full",
            tracking_completeness_percent=Decimal("96.00"),
            intent_fit_score=88,
            clicks=180,
            sessions=165,
            cost=Decimal("92.40"),
            reported_revenue=Decimal("168.00"),
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("126.00"),
            deducted_revenue=Decimal("0.00"),
            invalid_click_rate_percent=Decimal("0.50"),
            complaint_count=0,
            buyer_reject_rate_percent=Decimal("5.00"),
            policy_issue_state="clean",
            stop_control="precise",
            consistency_days=10,
            score=91,
            quality_level="high",
            recommended_action="allowlist_scale",
            click_session_rate=Decimal("91.67"),
            approved_rate=Decimal("100.00"),
            paid_rate=Decimal("75.00"),
            deduction_rate=Decimal("0.00"),
            paid_roi=Decimal("136.36"),
            approved_roi=Decimal("181.82"),
            blockers=[],
            status="open",
            notes=(
                "Demo: transparent search source with complete tracking, approved revenue, "
                "low invalid-click signal, and precise stop control."
            ),
            source_urls=[
                "https://support.google.com/adsense/answer/1348722",
                "https://support.google.com/adspolicy/answer/6020955",
                "https://support.google.com/google-ads/answer/2549112",
            ],
        )
    )
    db.session.add(
        VendorContractReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo vendor IO readiness review",
            vendor_name="Demo newsletter partner",
            vendor_type="direct_publisher",
            io_number="IO-DEMO-001",
            line_item_ref="US desktop sponsorship",
            contract_status="preapproved",
            pricing_model="flat_fee",
            source_detail_level="full",
            tracking_appendix=True,
            reporting_appendix=True,
            quality_clause=True,
            refund_clause=True,
            stop_control="precise",
            tracking_completeness_percent=Decimal("95.00"),
            report_delay_days=1,
            discrepancy_rate_percent=Decimal("4.00"),
            invalid_traffic_rate_percent=Decimal("0.60"),
            buyer_reject_rate_percent=Decimal("6.00"),
            budget_cap=Decimal("500.00"),
            spend_to_date=Decimal("120.00"),
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("126.00"),
            invoice_amount=Decimal("120.00"),
            disputed_amount=Decimal("0.00"),
            refund_credit_amount=Decimal("0.00"),
            makegood_value=Decimal("0.00"),
            dispute_response_days=1,
            payment_terms_days=30,
            refund_terms_status="clear",
            policy_issue_state="clean",
            score=91,
            risk_level="low",
            recommended_action="approve_small_test",
            amount_at_risk=Decimal("0.00"),
            paid_roi=Decimal("105.00"),
            approved_roi=Decimal("140.00"),
            invoice_dispute_rate=Decimal("0.00"),
            credit_coverage_rate=Decimal("0.00"),
            blockers=[],
            status="open",
            notes=(
                "Demo: IO has tracking, reporting, refund and quality clauses; "
                "small test can proceed after manual approval."
            ),
            source_urls=[
                "https://www.iab.com/guidelines/general-terms-and-conditions/",
                "https://support.google.com/adsense/answer/3332805",
            ],
        )
    )
    db.session.add(
        QueryMiningReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo search term promotion review",
            date_window="2026-06-01..2026-06-07",
            ads_customer_id="123-456-7890",
            campaign_ref="US Search - Cloud Backup - Test",
            ad_group_ref="comparison",
            keyword_text="cloud backup comparison",
            keyword_match_type="phrase",
            search_term="best cloud backup for small business",
            search_term_match_type="phrase",
            query_intent="comparison",
            network="google_search",
            device="desktop",
            country="US",
            landing_version="cloud-backup-v1",
            source_file_hash="demo-search-terms",
            clicks=64,
            sessions=58,
            conversions=3,
            cost=Decimal("31.36"),
            approved_revenue=Decimal("126.00"),
            paid_revenue=Decimal("84.00"),
            buyer_reject_rate_percent=Decimal("4.00"),
            intent_fit_score=90,
            policy_risk="low",
            revenue_status="paid",
            data_status="mature",
            conversion_lag_days=7,
            brand_or_official=False,
            support_or_login=False,
            score=93,
            risk_level="low",
            recommended_action="promote_exact_test",
            negative_match_type="none",
            negative_level="none",
            click_session_rate=Decimal("90.63"),
            cpc=Decimal("0.4900"),
            approved_rpv=Decimal("1.9688"),
            paid_rpv=Decimal("1.3125"),
            approved_roi=Decimal("401.79"),
            paid_roi=Decimal("267.86"),
            blockers=[],
            status="open",
            notes=(
                "Demo: mature comparison query has paid evidence and can be promoted "
                "to an exact small test after manual review."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/2472708",
                "https://support.google.com/google-ads/answer/2453972",
            ],
        )
    )
    db.session.add(
        BulkUploadReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo Editor CSV batch review",
            export_type="editor_csv",
            batch_id="BULK-DEMO-001",
            csv_hash="demo-csv-hash",
            payload_hash="",
            row_count=3,
            keyword_count=3,
            ad_count=1,
            target_customer_id="123-456-7890",
            account_timezone="America/New_York",
            currency="USD",
            expected_budget_delta=Decimal("50.00"),
            url_change_count=0,
            high_risk_change_count=0,
            preflight_status="passed",
            preview_status="passed",
            editor_check_status="passed",
            post_status="not_posted",
            default_paused=True,
            human_review=True,
            change_history_attached=False,
            rollback_plan=True,
            target_customer_confirmed=True,
            policy_review_complete=True,
            score=92,
            risk_level="low",
            recommended_action="approve_manual_post",
            budget_delta_percent=Decimal("50.00"),
            change_scope="small",
            blockers=[],
            status="open",
            notes="Demo: small paused CSV batch is ready for manual Editor posting.",
            source_urls=[
                "https://support.google.com/google-ads/editor/answer/56368",
                "https://support.google.com/google-ads/editor/answer/56370",
            ],
        )
    )
    db.session.add(
        ScriptSyncReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo Scripts metrics snapshot",
            auth_mode="scripts_authorized",
            sync_type="metrics_daily",
            script_name="Daily Metrics Snapshot Preview",
            customer_id="123-456-7890",
            date_range="LAST_7_DAYS",
            account_timezone="America/New_York",
            currency="USD",
            query_or_report="campaign metrics daily GAQL",
            source_snapshot_hash="demo-source-snapshot-hash",
            payload_hash="demo-query-hash",
            row_count=35,
            error_count=0,
            warning_count=0,
            freshness_minutes=60,
            rerun_window_days=7,
            data_status="mature",
            revenue_status="approved",
            conflict_status="clean",
            external_change_count=0,
            change_history_checked=True,
            preview_only=True,
            human_review=True,
            score=92,
            risk_level="low",
            freshness_level="heartbeat",
            recommended_action="approve_manual_import",
            blockers=[],
            status="open",
            notes=(
                "Demo: authorized Scripts report snapshot has query hash, Change "
                "history check, and mature approved revenue evidence."
            ),
            source_urls=[
                "https://developers.google.com/google-ads/scripts/docs/concepts/reports",
                "https://developers.google.com/google-ads/scripts/docs/preview",
            ],
        )
    )
    db.session.add(
        TaxonomyReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo taxonomy export QA",
            campaign_name="gads-us-en-cloudbackup-ofr001-compare-search-mobile-202606-t001",
            ad_group_name="compare-cloudbackup-smallbiz-phrase-lpA-ang_compare_cost",
            labels_text=(
                "lifecycle:test,risk:claim_review,experiment:exp_202606_001,"
                "batch:batch_202606_editor_csv"
            ),
            utm_source="gads",
            utm_medium="cpc",
            utm_campaign="{campaignid}",
            utm_id="ofr001-202606-t001",
            utm_content="{adgroupid}",
            utm_term="{keyword}",
            valuetrack_template=(
                "cid={campaignid}&agid={adgroupid}&kw={keyword}&mt={matchtype}"
                "&dev={device}&net={network}&cr={creative}"
            ),
            custom_parameter_map="{_offer}=ofr001;{_lpv}=lpA;{_angle}=ang_compare_cost",
            subid_map="subid1=channel;subid2=campaign;subid3=intent;subid4=keyword;subid5=angle_lpv",
            dimension_dictionary_version="dim-2026-06",
            parameter_map_version="utm-subid-v1",
            landing_version="lpA_compare_v3",
            link_version="lnk_ofr001_cta_v4",
            creative_version="ang_compare_cost_v2",
            payload_hash="demo-taxonomy-payload-hash",
            report_join_gap_count=0,
            gclid_preserved=True,
            click_id_preserved=True,
            lowercase_normalized=True,
            url_encoded=True,
            no_pii_in_url=True,
            no_sensitive_attributes=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_export",
            missing_campaign_tokens=[],
            missing_utm_fields=[],
            missing_label_groups=[],
            valuetrack_fields=[
                "adgroupid",
                "campaignid",
                "creative",
                "device",
                "keyword",
                "matchtype",
                "network",
            ],
            blockers=[],
            status="open",
            notes="Demo: naming, labels, UTM, ValueTrack, versions and join keys are ready for export.",
            source_urls=[
                "https://support.google.com/google-ads/answer/2375447",
                "https://support.google.com/analytics/answer/10917952",
            ],
        )
    )
    db.session.add(
        AttributionReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo geo holdout incrementality review",
            test_type="geo_holdout",
            attribution_model="data_driven",
            hypothesis="US search comparison campaign creates incremental approved revenue.",
            treatment_scope="US Northeast states, generic comparison queries",
            control_scope="Comparable US Midwest states held at baseline budget",
            split_method="geo matched holdout",
            date_window="2026-06-01..2026-06-14",
            primary_metric="incremental approved revenue",
            guardrail_metrics="organic/direct sessions, brand query volume, buyer reject rate",
            attributed_revenue=Decimal("980.00"),
            treatment_revenue=Decimal("1260.00"),
            control_revenue=Decimal("720.00"),
            incremental_revenue=Decimal("540.00"),
            ad_cost=Decimal("210.00"),
            variable_cost=Decimal("40.00"),
            incremental_profit=Decimal("290.00"),
            i_roas=Decimal("2.5714"),
            attributed_to_incremental_ratio=Decimal("0.5510"),
            attributed_conversions=24,
            incremental_conversions=11,
            sample_size=1200,
            confidence_level=Decimal("91.00"),
            holdout_quality="clean",
            revenue_status="approved",
            data_status="mature",
            brand_cannibalization_risk="low",
            organic_cannibalization_risk="low",
            remarketing_cannibalization_risk="low",
            pmax_broad_overlap_risk="low",
            change_history_clean=True,
            single_variable_test=True,
            approved_paid_evidence=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="scale_core_evidence",
            blockers=[],
            status="open",
            notes="Demo: clean geo holdout shows positive incremental profit and low cannibalization.",
            source_urls=[
                "https://support.google.com/google-ads/answer/6261395",
                "https://support.google.com/google-ads/answer/6259715",
            ],
        )
    )
    db.session.add(
        CplVerticalReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo B2B SaaS CPL vertical fit review",
            vertical="b2b_saas",
            subvertical="cloud backup demo request",
            country="US",
            buyer_type="direct advertiser",
            payout_model="CPL",
            payout_amount=Decimal("42.0000"),
            estimated_cpc=Decimal("0.4500"),
            landing_cvr_percent=Decimal("8.00"),
            accepted_rate_percent=Decimal("82.00"),
            qualified_rate_percent=Decimal("70.00"),
            paid_rate_percent=Decimal("58.00"),
            deduction_rate_percent=Decimal("6.00"),
            chargeback_rate_percent=Decimal("1.00"),
            feedback_lag_days=3,
            contact_sla_minutes=5,
            qualification_fields="company size, role, backup need, timeline, business email",
            sensitive_fields="No financial, health, legal, or government identity fields",
            reject_reason_map="student/personal email, out of geo, no business need, duplicate",
            accepted_definition="Buyer accepts contactable business lead matching ICP fields.",
            paid_definition="Paid after buyer confirms qualified demo or accepted invoice line.",
            policy_requirements="No official Google or security certification claim without proof.",
            forbidden_claims="guaranteed savings, official partner, best ranked",
            required_fields_mapped=True,
            reject_reason_map_ready=True,
            accepted_definition_clear=True,
            paid_definition_clear=True,
            consent_disclosure_status="channel_specific",
            pii_minimization=True,
            license_required=False,
            license_evidence_present=False,
            buyer_terms_status="approved",
            source_quality="low",
            policy_risk="low",
            data_sensitivity="low",
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_manual_test",
            effective_payout=Decimal("19.7932"),
            expected_value_per_click=Decimal("1.5835"),
            safe_cpc=Decimal("1.0293"),
            cpc_margin_percent=Decimal("128.73"),
            blockers=[],
            status="open",
            notes="Demo: B2B SaaS CPL fields, buyer definitions and feedback lag support a small manual test.",
            source_urls=[
                "https://support.google.com/adspolicy/answer/6020956",
                "https://support.google.com/adspolicy/answer/143465",
            ],
        )
    )
    db.session.add(
        LeadPricingReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo B2B SaaS lead payout review",
            buyer_name="Demo direct advertiser",
            vertical="b2b_saas",
            geo="US",
            source_type="search",
            exclusivity="exclusive",
            payout_model="qualified_cpl",
            headline_payout=Decimal("60.0000"),
            unit_payout=Decimal("42.0000"),
            proposed_payout=Decimal("48.0000"),
            minimum_acceptable_payout=Decimal("35.0000"),
            currency="USD",
            estimated_cpc=Decimal("0.4500"),
            click_to_lead_rate_percent=Decimal("8.00"),
            accepted_rate_percent=Decimal("82.00"),
            qualified_rate_percent=Decimal("70.00"),
            approval_rate_percent=Decimal("80.00"),
            paid_rate_percent=Decimal("74.00"),
            return_rate_percent=Decimal("4.00"),
            scrub_buffer_percent=Decimal("6.00"),
            chargeback_rate_percent=Decimal("1.00"),
            variable_cost_per_click=Decimal("0.0200"),
            tracking_cost_per_click=Decimal("0.0050"),
            content_cost_per_click=Decimal("0.0100"),
            cashflow_cost_percent=Decimal("2.00"),
            cap_limit=Decimal("120.00"),
            expected_volume=Decimal("60.00"),
            return_window_days=14,
            payment_term_days=15,
            qualification_definition="ICP business email, company size, role, use case and timeline.",
            rate_card_evidence="Approved rate card: qualified B2B demo request at USD 42.",
            negotiation_evidence="30-day paid cohort supports requesting USD 48 after stable source mix.",
            reject_reason_summary="personal email, duplicate, out of geo, no business need.",
            invoice_terms="Net 15 invoice with lead_id, accepted, qualified, paid and credit columns.",
            quality_evidence_status="paid_cohort",
            source_transparency="buyer_approved",
            consent_evidence="channel_specific",
            reject_reason_map_ready=True,
            invoice_evidence=True,
            dispute_reserve_present=True,
            buyer_terms_status="approved",
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_manual_test",
            effective_payout=Decimal("12.7020"),
            paid_epc=Decimal("1.0162"),
            safe_cpc=Decimal("0.6560"),
            margin_per_click=Decimal("0.2060"),
            reserve_amount=Decimal("4.6200"),
            blockers=[],
            status="open",
            notes="Demo: approved unit payout, paid cohort and short payment term support a manual test.",
            source_urls=[
                "https://support.google.com/google-ads/answer/3419241",
                "https://doc.voluum.com/en/tracking_payout.html",
            ],
        )
    )
    db.session.add(
        AppointmentLeadReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo appointment showed value review",
            buyer_name="Demo clinic or demo team",
            vertical="b2b_saas",
            service_type="cloud backup demo consultation",
            geo="US",
            appointment_platform="Google Calendar appointment schedule",
            payout_event="showed",
            payout_amount=Decimal("55.0000"),
            estimated_cpc=Decimal("0.3200"),
            click_to_request_rate_percent=Decimal("7.00"),
            request_to_book_rate_percent=Decimal("78.00"),
            confirmation_rate_percent=Decimal("85.00"),
            show_rate_percent=Decimal("72.00"),
            completed_rate_percent=Decimal("70.00"),
            paid_rate_percent=Decimal("60.00"),
            cancel_rate_percent=Decimal("8.00"),
            no_show_rate_percent=Decimal("12.00"),
            duplicate_booking_rate_percent=Decimal("2.00"),
            reschedule_rate_percent=Decimal("10.00"),
            reminder_cost_per_booking=Decimal("0.7500"),
            no_show_cost_per_booking=Decimal("5.0000"),
            available_slots=Decimal("80.00"),
            expected_bookings=Decimal("40.00"),
            lead_age_hours=2,
            slot_delay_hours=24,
            calendar_capacity_status="open",
            timezone_status="aligned",
            reminder_channel="email_calendar",
            reminder_consent_status="channel_specific",
            confirmation_process_status="confirmed_workflow",
            buyer_terms_status="approved",
            status_map=(
                "submitted -> eligible_for_booking -> booked -> confirmed -> "
                "showed -> completed -> paid"
            ),
            slot_policy="US business-hour slots within 24 hours, timezone shown before booking.",
            reminder_policy="Email and calendar reminder only after channel-specific consent.",
            no_show_reason_map="bad fit, slot too far, reminder missing, duplicate, buyer cancelled.",
            conversion_mapping=(
                "booked remains secondary; showed and paid are used for mature value review."
            ),
            payout_definition_clear=True,
            duplicate_window_defined=True,
            no_show_reason_map_ready=True,
            calendar_capacity_evidence=True,
            reminder_template_reviewed=True,
            offline_conversion_mapping_ready=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_manual_test",
            expected_value_per_booking=Decimal("12.7235"),
            expected_value_per_click=Decimal("0.6947"),
            safe_cpc=Decimal("0.3778"),
            cpc_margin_percent=Decimal("18.06"),
            safe_appointment_spend=Decimal("305.36"),
            blockers=[],
            status="open",
            notes="Demo: showed appointment value, capacity, reminders and offline mapping are ready for a manual test.",
            source_urls=[
                "https://support.google.com/calendar/answer/10729749",
                "https://support.google.com/google-ads/answer/9347141",
            ],
        )
    )
    db.session.add(
        BuyerCapacityReview(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo buyer capacity pacing review",
            buyer_name="Demo direct advertiser",
            vertical="b2b_saas",
            geo="US",
            buyer_timezone="America/New_York",
            account_timezone="America/New_York",
            user_timezone_scope="US Eastern and Central business users",
            call_center_timezone="America/New_York",
            cap_type="daily_buyer_cap",
            cap_period="daily",
            cap_limit=Decimal("120.00"),
            cap_used=Decimal("42.00"),
            elapsed_operating_day_percent=Decimal("45.00"),
            expected_next_hour_leads=Decimal("12.00"),
            expected_daily_leads=Decimal("80.00"),
            hourly_contact_capacity=Decimal("28.00"),
            current_hour_capacity_used=Decimal("9.00"),
            expected_paid_value_per_lead=Decimal("42.0000"),
            accepted_rate_percent=Decimal("82.00"),
            qualified_rate_percent=Decimal("70.00"),
            paid_rate_percent=Decimal("74.00"),
            no_buyer_rate_percent=Decimal("2.00"),
            missed_contact_rate_percent=Decimal("6.00"),
            after_hours_lead_rate_percent=Decimal("3.00"),
            cap_last_confirmed_hours=2,
            feedback_sla_hours=24,
            first_attempt_sla_minutes=5,
            cap_confidence_status="same_day",
            hours_alignment_status="aligned",
            ad_schedule_alignment_status="aligned",
            timezone_alignment_status="aligned",
            holiday_readiness_status="ready",
            fallback_status="approved",
            source_quality_status="buyer_approved",
            overdelivery_guardrail_status="tested",
            operating_hours="Mon-Fri 09:00-18:00 buyer local time.",
            cap_reset_rule="Daily cap resets at 00:00 America/New_York; returned leads do not release cap until reviewed.",
            holiday_calendar="US federal holidays and buyer closure sheet reviewed for the current month.",
            ad_schedule_summary="Campaign schedule matches buyer hours with call-heavy ads disabled after hours.",
            no_buyer_reason_map="cap reached, buyer closed, source not approved, quality hold, CRM/API issue.",
            routing_fallback_policy="Fallback buyer is same intent, disclosed, approved and never used for cloaking.",
            dayparting_basis="Mature paid cohort by lead-created hour, not same-day upload time.",
            cap_snapshot_evidence=True,
            buyer_hours_evidence=True,
            ad_schedule_evidence=True,
            call_reporting_evidence=True,
            no_buyer_tracking_ready=True,
            missed_contact_tracking_ready=True,
            dayparting_cohort_ready=True,
            fallback_buyer_reviewed=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_small_ramp",
            cap_usage_percent=Decimal("35.00"),
            cap_remaining=Decimal("78.00"),
            projected_end_of_day_usage_percent=Decimal("77.78"),
            safe_leads_remaining=Decimal("19.00"),
            safe_media_spend_remaining=Decimal("545.44"),
            blockers=[],
            status="open",
            notes="Demo: buyer cap, hours, schedule, timezone and fallback evidence support a small manual ramp.",
            source_urls=[
                "https://support.google.com/google-ads/answer/6372656",
                "https://support.google.com/google-ads/answer/1704443",
            ],
        )
    )
    db.session.add(
        RiskAudit(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            capability="cloaking_review_user_page_mismatch",
            severity="medium",
            status="reviewed",
            finding="Demo check: final URL and ad promise must stay consistent.",
            mitigation="Use only reviewed same-topic URL changes and keep audit logs.",
            source_urls=[
                "https://support.google.com/adspolicy/answer/6008942",
                "https://developers.google.com/search/docs/essentials/spam-policies",
            ],
        )
    )
    db.session.add(
        LinkRule(
            offer_id=offer.id,
            name="Demo reviewed backup comparison URL",
            current_url="https://example.com/cloud-backup?utm_source=google",
            candidate_urls=[
                "https://example.com/cloud-backup?utm_source=google&utm_content=backup-test",
                "https://example.com/cloud-backup/checklist?utm_source=google",
            ],
            rotation_reason="Reviewed same-topic URL maintenance for tracking parameters and checklist variant.",
            frequency_minutes=1440,
            require_manual_review=True,
            status="draft",
        )
    )
    _seed_demo_research_sources()
    _seed_demo_conversion_signal_reviews()
    _seed_demo_crm_value_mapping_reviews()
    _seed_demo_lead_validation_reviews()
    _seed_demo_ping_post_routing_reviews()
    db.session.add(
        OpportunityAssessment(
            offer_id=offer.id,
            name="Demo CPA opportunity",
            revenue_model="CPA",
            payout=Decimal("42.00"),
            cvr_percent=Decimal("2.00"),
            cpc=Decimal("0.45"),
            safety_factor=Decimal("0.65"),
            target_clicks=150,
            policy_score=85,
            content_score=82,
            tracking_score=80,
            source_score=78,
            cash_buffer_days=30,
            result={
                "rpv": 0.84,
                "safe_cpc": 0.546,
                "expected_profit": 58.5,
                "roi": 0.8667,
                "opportunity_score": 82,
            },
            recommendation="test",
        )
    )
    db.session.add(
        TaskJob(
            offer_id=offer.id,
            campaign_draft_id=campaign.id,
            name="Demo script payload review",
            task_type="export_script_payload",
            schedule_mode="manual",
            interval_minutes=1440,
            notes="Safe demo task. Produces reviewed payload metadata only.",
        )
    )
    add_audit("system", None, "seed", "Inserted demo Ads arbitrage workflow data.")
    db.session.commit()


def _seed_demo_claim_reviews() -> int:
    creative = CreativeSet.query.order_by(CreativeSet.id).first()
    if not creative:
        return 0
    exists = CreativeClaimReview.query.filter_by(
        creative_set_id=creative.id,
        asset_type="description",
        asset_text="Review features, pricing, and restore options for small teams.",
        issue="Review or testimonial claim",
    ).first()
    if exists:
        return 0

    db.session.add(
        CreativeClaimReview(
            creative_set_id=creative.id,
            asset_type="description",
            asset_text="Review features, pricing, and restore options for small teams.",
            issue="Review or testimonial claim",
            severity="medium",
            action="Needs verifiable review source and disclosure for any commercial relationship.",
            evidence="Editorial comparison covers features, pricing, and restore options.",
            source_url="https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides",
        )
    )
    return 1


def _seed_demo_ad_review_cases() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = AdReviewCase.query.filter_by(
        campaign_draft_id=campaign.id,
        policy_topic="Misrepresentation / claim substantiation",
    ).first()
    if exists:
        return 0

    db.session.add(
        AdReviewCase(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            creative_set_id=campaign.creative_set_id,
            object_type="ad",
            object_ref="Demo RSA draft",
            policy_topic="Misrepresentation / claim substantiation",
            severity="medium",
            status="open",
            final_url=campaign.final_url,
            expanded_url=campaign.final_url,
            finding=(
                "Demo case: review copy that mentions secure backup and pricing before export."
            ),
            change_summary=(
                "Keep comparison wording, verify pricing table and proof snippets, "
                "and avoid guarantee or official relationship claims."
            ),
            evidence_urls=[
                "https://support.google.com/adspolicy/answer/6020955",
                "https://support.google.com/google-ads/answer/9338593",
            ],
            appeal_text=(
                "If rejected, appeal only after the ad text and landing page evidence are fixed."
            ),
            reviewer="demo reviewer",
        )
    )
    return 1


def _seed_demo_decision_window_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = DecisionWindowReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo maturity check",
    ).first()
    if exists:
        return 0

    db.session.add(
        DecisionWindowReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo maturity check",
            data_status="mature",
            revenue_status="approved",
            conversion_lag_days=7,
            approval_lag_days=5,
            settlement_lag_days=10,
            sample_clicks=180,
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("0.00"),
            source_quality="stable",
            incident_state="clean",
            score=82,
            maturity="mostly_mature",
            recommended_action="small_ramp",
            blockers=["paid revenue is not available yet"],
            status="open",
            notes="Demo decision: small ramp only after approved revenue is reviewed.",
            source_urls=[
                "https://support.google.com/google-ads/answer/9347141",
                "https://support.google.com/adsense/answer/7164703",
            ],
        )
    )
    return 1


def _seed_demo_budget_pacing_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = BudgetPacingReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo budget ramp gate",
    ).first()
    if exists:
        return 0

    db.session.add(
        BudgetPacingReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo budget ramp gate",
            current_daily_budget=Decimal("50.00"),
            proposed_daily_budget=Decimal("60.00"),
            test_budget=Decimal("150.00"),
            hard_stop=Decimal("180.00"),
            spend_to_date=Decimal("96.00"),
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("0.00"),
            safe_cpc=Decimal("0.55"),
            actual_cpc=Decimal("0.48"),
            sample_clicks=200,
            data_status="mature",
            revenue_status="approved",
            source_quality="stable",
            incident_state="clean",
            cash_buffer_days=30,
            overdelivery_buffer_percent=Decimal("20.00"),
            score=87,
            risk_level="low",
            recommended_action="approve_manual_ramp",
            increase_percent=Decimal("20.00"),
            remaining_test_budget=Decimal("54.00"),
            remaining_hard_stop=Decimal("84.00"),
            blockers=[],
            status="open",
            notes="Demo: approved revenue and safe CPC allow a manual +20% review.",
            source_urls=[
                "https://support.google.com/google-ads/answer/10702522",
                "https://support.google.com/google-ads/answer/1704443",
            ],
        )
    )
    return 1


def _seed_demo_portfolio_allocation_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = PortfolioAllocationReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo portfolio exposure review",
    ).first()
    if exists:
        return 0

    db.session.add(
        PortfolioAllocationReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo portfolio exposure review",
            portfolio_bucket="scale",
            monthly_media_budget=Decimal("3000.00"),
            proposed_allocation=Decimal("450.00"),
            spend_to_date=Decimal("960.00"),
            reported_revenue=Decimal("220.00"),
            pending_revenue=Decimal("80.00"),
            approved_revenue=Decimal("168.00"),
            finalized_revenue=Decimal("0.00"),
            paid_revenue=Decimal("0.00"),
            deducted_revenue=Decimal("0.00"),
            single_offer_exposure_percent=Decimal("18.00"),
            single_source_exposure_percent=Decimal("22.00"),
            single_account_exposure_percent=Decimal("24.00"),
            single_partner_exposure_percent=Decimal("28.00"),
            cash_reserve_days=35,
            source_quality="stable",
            policy_risk="low",
            incident_state="clean",
            score=82,
            risk_level="medium",
            recommended_action="hold_or_small_test",
            allocation_percent=Decimal("15.00"),
            remaining_monthly_budget=Decimal("1590.00"),
            cash_at_risk=Decimal("530.00"),
            revenue_quality_ratio=Decimal("35.90"),
            blockers=["paid revenue is not available yet"],
            status="open",
            notes=(
                "Demo: concentration is under guardrails, but paid revenue is not ready "
                "for Core allocation."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/10702522",
                "https://support.google.com/adsense/answer/7164703",
            ],
        )
    )
    return 1


def _seed_demo_offer_cap_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = OfferCapReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo offer cap and payout check",
    ).first()
    if exists:
        return 0

    db.session.add(
        OfferCapReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo offer cap and payout check",
            offer_status="active",
            cap_type="daily_conversion",
            cap_period="daily",
            cap_limit=Decimal("20.00"),
            cap_used=Decimal("12.00"),
            expected_next_conversions=Decimal("3.00"),
            current_payout=Decimal("42.0000"),
            new_payout=Decimal("42.0000"),
            approval_rate_percent=Decimal("82.00"),
            paid_rate_percent=Decimal("74.00"),
            deduction_rate_percent=Decimal("5.00"),
            days_since_cap_update=1,
            buyer_capacity_status="open",
            replacement_status="preapproved",
            replacement_fit_score=86,
            same_intent_review=True,
            source_quality="stable",
            policy_risk="low",
            score=88,
            risk_level="low",
            recommended_action="approve_manual_test",
            cap_usage_percent=Decimal("60.00"),
            cap_remaining=Decimal("8.00"),
            effective_payout=Decimal("24.2138"),
            safe_daily_media_cost=Decimal("72.64"),
            blockers=[],
            status="open",
            notes="Demo: cap is under watch threshold and replacement has same-intent review.",
            source_urls=[
                "https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps",
                "https://developers.everflow.io/docs/affiliate/offers/",
            ],
        )
    )
    return 1


def _seed_demo_source_quality_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = SourceQualityReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo source quality review",
    ).first()
    if exists:
        return 0

    db.session.add(
        SourceQualityReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo source quality review",
            entity_type="placement",
            source_name="Google Search",
            publisher_name="Search intent segment",
            placement_ref="cloud backup comparison query group",
            subid="kw_cloud_backup_compare",
            network="Google Ads Search",
            country="US",
            device="desktop",
            sample_url="https://example.com/cloud-backup?utm_source=google",
            transparency_level="full",
            tracking_completeness_percent=Decimal("96.00"),
            intent_fit_score=88,
            clicks=180,
            sessions=165,
            cost=Decimal("92.40"),
            reported_revenue=Decimal("168.00"),
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("126.00"),
            deducted_revenue=Decimal("0.00"),
            invalid_click_rate_percent=Decimal("0.50"),
            complaint_count=0,
            buyer_reject_rate_percent=Decimal("5.00"),
            policy_issue_state="clean",
            stop_control="precise",
            consistency_days=10,
            score=91,
            quality_level="high",
            recommended_action="allowlist_scale",
            click_session_rate=Decimal("91.67"),
            approved_rate=Decimal("100.00"),
            paid_rate=Decimal("75.00"),
            deduction_rate=Decimal("0.00"),
            paid_roi=Decimal("136.36"),
            approved_roi=Decimal("181.82"),
            blockers=[],
            status="open",
            notes=(
                "Demo: transparent search source with complete tracking, approved revenue, "
                "low invalid-click signal, and precise stop control."
            ),
            source_urls=[
                "https://support.google.com/adsense/answer/1348722",
                "https://support.google.com/adspolicy/answer/6020955",
                "https://support.google.com/google-ads/answer/2549112",
            ],
        )
    )
    return 1


def _seed_demo_vendor_contract_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = VendorContractReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo vendor IO readiness review",
    ).first()
    if exists:
        return 0

    db.session.add(
        VendorContractReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo vendor IO readiness review",
            vendor_name="Demo newsletter partner",
            vendor_type="direct_publisher",
            io_number="IO-DEMO-001",
            line_item_ref="US desktop sponsorship",
            contract_status="preapproved",
            pricing_model="flat_fee",
            source_detail_level="full",
            tracking_appendix=True,
            reporting_appendix=True,
            quality_clause=True,
            refund_clause=True,
            stop_control="precise",
            tracking_completeness_percent=Decimal("95.00"),
            report_delay_days=1,
            discrepancy_rate_percent=Decimal("4.00"),
            invalid_traffic_rate_percent=Decimal("0.60"),
            buyer_reject_rate_percent=Decimal("6.00"),
            budget_cap=Decimal("500.00"),
            spend_to_date=Decimal("120.00"),
            approved_revenue=Decimal("168.00"),
            paid_revenue=Decimal("126.00"),
            invoice_amount=Decimal("120.00"),
            disputed_amount=Decimal("0.00"),
            refund_credit_amount=Decimal("0.00"),
            makegood_value=Decimal("0.00"),
            dispute_response_days=1,
            payment_terms_days=30,
            refund_terms_status="clear",
            policy_issue_state="clean",
            score=91,
            risk_level="low",
            recommended_action="approve_small_test",
            amount_at_risk=Decimal("0.00"),
            paid_roi=Decimal("105.00"),
            approved_roi=Decimal("140.00"),
            invoice_dispute_rate=Decimal("0.00"),
            credit_coverage_rate=Decimal("0.00"),
            blockers=[],
            status="open",
            notes=(
                "Demo: IO has tracking, reporting, refund and quality clauses; "
                "small test can proceed after manual approval."
            ),
            source_urls=[
                "https://www.iab.com/guidelines/general-terms-and-conditions/",
                "https://support.google.com/adsense/answer/3332805",
            ],
        )
    )
    return 1


def _seed_demo_query_mining_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = QueryMiningReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo search term promotion review",
    ).first()
    if exists:
        return 0

    db.session.add(
        QueryMiningReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo search term promotion review",
            date_window="2026-06-01..2026-06-07",
            ads_customer_id="123-456-7890",
            campaign_ref="US Search - Cloud Backup - Test",
            ad_group_ref="comparison",
            keyword_text="cloud backup comparison",
            keyword_match_type="phrase",
            search_term="best cloud backup for small business",
            search_term_match_type="phrase",
            query_intent="comparison",
            network="google_search",
            device="desktop",
            country="US",
            landing_version="cloud-backup-v1",
            source_file_hash="demo-search-terms",
            clicks=64,
            sessions=58,
            conversions=3,
            cost=Decimal("31.36"),
            approved_revenue=Decimal("126.00"),
            paid_revenue=Decimal("84.00"),
            buyer_reject_rate_percent=Decimal("4.00"),
            intent_fit_score=90,
            policy_risk="low",
            revenue_status="paid",
            data_status="mature",
            conversion_lag_days=7,
            brand_or_official=False,
            support_or_login=False,
            score=93,
            risk_level="low",
            recommended_action="promote_exact_test",
            negative_match_type="none",
            negative_level="none",
            click_session_rate=Decimal("90.63"),
            cpc=Decimal("0.4900"),
            approved_rpv=Decimal("1.9688"),
            paid_rpv=Decimal("1.3125"),
            approved_roi=Decimal("401.79"),
            paid_roi=Decimal("267.86"),
            blockers=[],
            status="open",
            notes=(
                "Demo: mature comparison query has paid evidence and can be promoted "
                "to an exact small test after manual review."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/2472708",
                "https://support.google.com/google-ads/answer/2453972",
            ],
        )
    )
    return 1


def _seed_demo_bulk_upload_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = BulkUploadReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo Editor CSV batch review",
    ).first()
    if exists:
        return 0

    db.session.add(
        BulkUploadReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo Editor CSV batch review",
            export_type="editor_csv",
            batch_id="BULK-DEMO-001",
            csv_hash="demo-csv-hash",
            payload_hash="",
            row_count=3,
            keyword_count=3,
            ad_count=1,
            target_customer_id="123-456-7890",
            account_timezone="America/New_York",
            currency="USD",
            expected_budget_delta=Decimal("50.00"),
            url_change_count=0,
            high_risk_change_count=0,
            preflight_status="passed",
            preview_status="passed",
            editor_check_status="passed",
            post_status="not_posted",
            default_paused=True,
            human_review=True,
            change_history_attached=False,
            rollback_plan=True,
            target_customer_confirmed=True,
            policy_review_complete=True,
            score=92,
            risk_level="low",
            recommended_action="approve_manual_post",
            budget_delta_percent=Decimal("50.00"),
            change_scope="small",
            blockers=[],
            status="open",
            notes="Demo: small paused CSV batch is ready for manual Editor posting.",
            source_urls=[
                "https://support.google.com/google-ads/editor/answer/56368",
                "https://support.google.com/google-ads/editor/answer/56370",
            ],
        )
    )
    return 1


def _seed_demo_script_sync_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = ScriptSyncReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo Scripts metrics snapshot",
    ).first()
    if exists:
        return 0

    db.session.add(
        ScriptSyncReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo Scripts metrics snapshot",
            auth_mode="scripts_authorized",
            sync_type="metrics_daily",
            script_name="Daily Metrics Snapshot Preview",
            customer_id="123-456-7890",
            date_range="LAST_7_DAYS",
            account_timezone="America/New_York",
            currency="USD",
            query_or_report="campaign metrics daily GAQL",
            source_snapshot_hash="demo-source-snapshot-hash",
            payload_hash="demo-query-hash",
            row_count=35,
            error_count=0,
            warning_count=0,
            freshness_minutes=60,
            rerun_window_days=7,
            data_status="mature",
            revenue_status="approved",
            conflict_status="clean",
            external_change_count=0,
            change_history_checked=True,
            preview_only=True,
            human_review=True,
            score=92,
            risk_level="low",
            freshness_level="heartbeat",
            recommended_action="approve_manual_import",
            blockers=[],
            status="open",
            notes=(
                "Demo: authorized Scripts report snapshot has query hash, Change "
                "history check, and mature approved revenue evidence."
            ),
            source_urls=[
                "https://developers.google.com/google-ads/scripts/docs/concepts/reports",
                "https://developers.google.com/google-ads/scripts/docs/preview",
            ],
        )
    )
    return 1


def _seed_demo_taxonomy_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = TaxonomyReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo taxonomy export QA",
    ).first()
    if exists:
        return 0

    db.session.add(
        TaxonomyReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo taxonomy export QA",
            campaign_name="gads-us-en-cloudbackup-ofr001-compare-search-mobile-202606-t001",
            ad_group_name="compare-cloudbackup-smallbiz-phrase-lpA-ang_compare_cost",
            labels_text=(
                "lifecycle:test,risk:claim_review,experiment:exp_202606_001,"
                "batch:batch_202606_editor_csv"
            ),
            utm_source="gads",
            utm_medium="cpc",
            utm_campaign="{campaignid}",
            utm_id="ofr001-202606-t001",
            utm_content="{adgroupid}",
            utm_term="{keyword}",
            valuetrack_template=(
                "cid={campaignid}&agid={adgroupid}&kw={keyword}&mt={matchtype}"
                "&dev={device}&net={network}&cr={creative}"
            ),
            custom_parameter_map="{_offer}=ofr001;{_lpv}=lpA;{_angle}=ang_compare_cost",
            subid_map="subid1=channel;subid2=campaign;subid3=intent;subid4=keyword;subid5=angle_lpv",
            dimension_dictionary_version="dim-2026-06",
            parameter_map_version="utm-subid-v1",
            landing_version="lpA_compare_v3",
            link_version="lnk_ofr001_cta_v4",
            creative_version="ang_compare_cost_v2",
            payload_hash="demo-taxonomy-payload-hash",
            report_join_gap_count=0,
            gclid_preserved=True,
            click_id_preserved=True,
            lowercase_normalized=True,
            url_encoded=True,
            no_pii_in_url=True,
            no_sensitive_attributes=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_export",
            missing_campaign_tokens=[],
            missing_utm_fields=[],
            missing_label_groups=[],
            valuetrack_fields=[
                "adgroupid",
                "campaignid",
                "creative",
                "device",
                "keyword",
                "matchtype",
                "network",
            ],
            blockers=[],
            status="open",
            notes="Demo: naming, labels, UTM, ValueTrack, versions and join keys are ready for export.",
            source_urls=[
                "https://support.google.com/google-ads/answer/2375447",
                "https://support.google.com/analytics/answer/10917952",
            ],
        )
    )
    return 1


def _seed_demo_attribution_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = AttributionReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo geo holdout incrementality review",
    ).first()
    if exists:
        return 0

    db.session.add(
        AttributionReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo geo holdout incrementality review",
            test_type="geo_holdout",
            attribution_model="data_driven",
            hypothesis="US search comparison campaign creates incremental approved revenue.",
            treatment_scope="US Northeast states, generic comparison queries",
            control_scope="Comparable US Midwest states held at baseline budget",
            split_method="geo matched holdout",
            date_window="2026-06-01..2026-06-14",
            primary_metric="incremental approved revenue",
            guardrail_metrics="organic/direct sessions, brand query volume, buyer reject rate",
            attributed_revenue=Decimal("980.00"),
            treatment_revenue=Decimal("1260.00"),
            control_revenue=Decimal("720.00"),
            incremental_revenue=Decimal("540.00"),
            ad_cost=Decimal("210.00"),
            variable_cost=Decimal("40.00"),
            incremental_profit=Decimal("290.00"),
            i_roas=Decimal("2.5714"),
            attributed_to_incremental_ratio=Decimal("0.5510"),
            attributed_conversions=24,
            incremental_conversions=11,
            sample_size=1200,
            confidence_level=Decimal("91.00"),
            holdout_quality="clean",
            revenue_status="approved",
            data_status="mature",
            brand_cannibalization_risk="low",
            organic_cannibalization_risk="low",
            remarketing_cannibalization_risk="low",
            pmax_broad_overlap_risk="low",
            change_history_clean=True,
            single_variable_test=True,
            approved_paid_evidence=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="scale_core_evidence",
            blockers=[],
            status="open",
            notes="Demo: clean geo holdout shows positive incremental profit and low cannibalization.",
            source_urls=[
                "https://support.google.com/google-ads/answer/6261395",
                "https://support.google.com/google-ads/answer/6259715",
            ],
        )
    )
    return 1


def _seed_demo_cpl_vertical_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = CplVerticalReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo B2B SaaS CPL vertical fit review",
    ).first()
    if exists:
        return 0

    db.session.add(
        CplVerticalReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo B2B SaaS CPL vertical fit review",
            vertical="b2b_saas",
            subvertical="cloud backup demo request",
            country="US",
            buyer_type="direct advertiser",
            payout_model="CPL",
            payout_amount=Decimal("42.0000"),
            estimated_cpc=Decimal("0.4500"),
            landing_cvr_percent=Decimal("8.00"),
            accepted_rate_percent=Decimal("82.00"),
            qualified_rate_percent=Decimal("70.00"),
            paid_rate_percent=Decimal("58.00"),
            deduction_rate_percent=Decimal("6.00"),
            chargeback_rate_percent=Decimal("1.00"),
            feedback_lag_days=3,
            contact_sla_minutes=5,
            qualification_fields="company size, role, backup need, timeline, business email",
            sensitive_fields="No financial, health, legal, or government identity fields",
            reject_reason_map="student/personal email, out of geo, no business need, duplicate",
            accepted_definition="Buyer accepts contactable business lead matching ICP fields.",
            paid_definition="Paid after buyer confirms qualified demo or accepted invoice line.",
            policy_requirements="No official Google or security certification claim without proof.",
            forbidden_claims="guaranteed savings, official partner, best ranked",
            required_fields_mapped=True,
            reject_reason_map_ready=True,
            accepted_definition_clear=True,
            paid_definition_clear=True,
            consent_disclosure_status="channel_specific",
            pii_minimization=True,
            license_required=False,
            license_evidence_present=False,
            buyer_terms_status="approved",
            source_quality="low",
            policy_risk="low",
            data_sensitivity="low",
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_manual_test",
            effective_payout=Decimal("19.7932"),
            expected_value_per_click=Decimal("1.5835"),
            safe_cpc=Decimal("1.0293"),
            cpc_margin_percent=Decimal("128.73"),
            blockers=[],
            status="open",
            notes="Demo: B2B SaaS CPL fields, buyer definitions and feedback lag support a small manual test.",
            source_urls=[
                "https://support.google.com/adspolicy/answer/6020956",
                "https://support.google.com/adspolicy/answer/143465",
            ],
        )
    )
    return 1


def _seed_demo_lead_pricing_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = LeadPricingReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo B2B SaaS lead payout review",
    ).first()
    if exists:
        return 0

    db.session.add(
        LeadPricingReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo B2B SaaS lead payout review",
            buyer_name="Demo direct advertiser",
            vertical="b2b_saas",
            geo="US",
            source_type="search",
            exclusivity="exclusive",
            payout_model="qualified_cpl",
            headline_payout=Decimal("60.0000"),
            unit_payout=Decimal("42.0000"),
            proposed_payout=Decimal("48.0000"),
            minimum_acceptable_payout=Decimal("35.0000"),
            currency="USD",
            estimated_cpc=Decimal("0.4500"),
            click_to_lead_rate_percent=Decimal("8.00"),
            accepted_rate_percent=Decimal("82.00"),
            qualified_rate_percent=Decimal("70.00"),
            approval_rate_percent=Decimal("80.00"),
            paid_rate_percent=Decimal("74.00"),
            return_rate_percent=Decimal("4.00"),
            scrub_buffer_percent=Decimal("6.00"),
            chargeback_rate_percent=Decimal("1.00"),
            variable_cost_per_click=Decimal("0.0200"),
            tracking_cost_per_click=Decimal("0.0050"),
            content_cost_per_click=Decimal("0.0100"),
            cashflow_cost_percent=Decimal("2.00"),
            cap_limit=Decimal("120.00"),
            expected_volume=Decimal("60.00"),
            return_window_days=14,
            payment_term_days=15,
            qualification_definition=(
                "ICP business email, company size, role, use case and timeline."
            ),
            rate_card_evidence=(
                "Approved rate card: qualified B2B demo request at USD 42."
            ),
            negotiation_evidence=(
                "30-day paid cohort supports requesting USD 48 after stable source mix."
            ),
            reject_reason_summary="personal email, duplicate, out of geo, no business need.",
            invoice_terms=(
                "Net 15 invoice with lead_id, accepted, qualified, paid and credit columns."
            ),
            quality_evidence_status="paid_cohort",
            source_transparency="buyer_approved",
            consent_evidence="channel_specific",
            reject_reason_map_ready=True,
            invoice_evidence=True,
            dispute_reserve_present=True,
            buyer_terms_status="approved",
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_manual_test",
            effective_payout=Decimal("12.7020"),
            paid_epc=Decimal("1.0162"),
            safe_cpc=Decimal("0.6560"),
            margin_per_click=Decimal("0.2060"),
            reserve_amount=Decimal("4.6200"),
            blockers=[],
            status="open",
            notes=(
                "Demo: approved unit payout, paid cohort and short payment term "
                "support a manual test."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/3419241",
                "https://doc.voluum.com/en/tracking_payout.html",
            ],
        )
    )
    return 1


def _seed_demo_appointment_lead_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = AppointmentLeadReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo appointment showed value review",
    ).first()
    if exists:
        return 0

    db.session.add(
        AppointmentLeadReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo appointment showed value review",
            buyer_name="Demo clinic or demo team",
            vertical="b2b_saas",
            service_type="cloud backup demo consultation",
            geo="US",
            appointment_platform="Google Calendar appointment schedule",
            payout_event="showed",
            payout_amount=Decimal("55.0000"),
            estimated_cpc=Decimal("0.3200"),
            click_to_request_rate_percent=Decimal("7.00"),
            request_to_book_rate_percent=Decimal("78.00"),
            confirmation_rate_percent=Decimal("85.00"),
            show_rate_percent=Decimal("72.00"),
            completed_rate_percent=Decimal("70.00"),
            paid_rate_percent=Decimal("60.00"),
            cancel_rate_percent=Decimal("8.00"),
            no_show_rate_percent=Decimal("12.00"),
            duplicate_booking_rate_percent=Decimal("2.00"),
            reschedule_rate_percent=Decimal("10.00"),
            reminder_cost_per_booking=Decimal("0.7500"),
            no_show_cost_per_booking=Decimal("5.0000"),
            available_slots=Decimal("80.00"),
            expected_bookings=Decimal("40.00"),
            lead_age_hours=2,
            slot_delay_hours=24,
            calendar_capacity_status="open",
            timezone_status="aligned",
            reminder_channel="email_calendar",
            reminder_consent_status="channel_specific",
            confirmation_process_status="confirmed_workflow",
            buyer_terms_status="approved",
            status_map=(
                "submitted -> eligible_for_booking -> booked -> confirmed -> "
                "showed -> completed -> paid"
            ),
            slot_policy="US business-hour slots within 24 hours, timezone shown before booking.",
            reminder_policy="Email and calendar reminder only after channel-specific consent.",
            no_show_reason_map=(
                "bad fit, slot too far, reminder missing, duplicate, buyer cancelled."
            ),
            conversion_mapping=(
                "booked remains secondary; showed and paid are used for mature value review."
            ),
            payout_definition_clear=True,
            duplicate_window_defined=True,
            no_show_reason_map_ready=True,
            calendar_capacity_evidence=True,
            reminder_template_reviewed=True,
            offline_conversion_mapping_ready=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_manual_test",
            expected_value_per_booking=Decimal("12.7235"),
            expected_value_per_click=Decimal("0.6947"),
            safe_cpc=Decimal("0.3778"),
            cpc_margin_percent=Decimal("18.06"),
            safe_appointment_spend=Decimal("305.36"),
            blockers=[],
            status="open",
            notes=(
                "Demo: showed appointment value, capacity, reminders and offline "
                "mapping are ready for a manual test."
            ),
            source_urls=[
                "https://support.google.com/calendar/answer/10729749",
                "https://support.google.com/google-ads/answer/9347141",
            ],
        )
    )
    return 1


def _seed_demo_buyer_capacity_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = BuyerCapacityReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo buyer capacity pacing review",
    ).first()
    if exists:
        return 0

    db.session.add(
        BuyerCapacityReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo buyer capacity pacing review",
            buyer_name="Demo direct advertiser",
            vertical="b2b_saas",
            geo="US",
            buyer_timezone="America/New_York",
            account_timezone="America/New_York",
            user_timezone_scope="US Eastern and Central business users",
            call_center_timezone="America/New_York",
            cap_type="daily_buyer_cap",
            cap_period="daily",
            cap_limit=Decimal("120.00"),
            cap_used=Decimal("42.00"),
            elapsed_operating_day_percent=Decimal("45.00"),
            expected_next_hour_leads=Decimal("12.00"),
            expected_daily_leads=Decimal("80.00"),
            hourly_contact_capacity=Decimal("28.00"),
            current_hour_capacity_used=Decimal("9.00"),
            expected_paid_value_per_lead=Decimal("42.0000"),
            accepted_rate_percent=Decimal("82.00"),
            qualified_rate_percent=Decimal("70.00"),
            paid_rate_percent=Decimal("74.00"),
            no_buyer_rate_percent=Decimal("2.00"),
            missed_contact_rate_percent=Decimal("6.00"),
            after_hours_lead_rate_percent=Decimal("3.00"),
            cap_last_confirmed_hours=2,
            feedback_sla_hours=24,
            first_attempt_sla_minutes=5,
            cap_confidence_status="same_day",
            hours_alignment_status="aligned",
            ad_schedule_alignment_status="aligned",
            timezone_alignment_status="aligned",
            holiday_readiness_status="ready",
            fallback_status="approved",
            source_quality_status="buyer_approved",
            overdelivery_guardrail_status="tested",
            operating_hours="Mon-Fri 09:00-18:00 buyer local time.",
            cap_reset_rule=(
                "Daily cap resets at 00:00 America/New_York; returned leads do "
                "not release cap until reviewed."
            ),
            holiday_calendar=(
                "US federal holidays and buyer closure sheet reviewed for the "
                "current month."
            ),
            ad_schedule_summary=(
                "Campaign schedule matches buyer hours with call-heavy ads "
                "disabled after hours."
            ),
            no_buyer_reason_map=(
                "cap reached, buyer closed, source not approved, quality hold, "
                "CRM/API issue."
            ),
            routing_fallback_policy=(
                "Fallback buyer is same intent, disclosed, approved and never "
                "used for cloaking."
            ),
            dayparting_basis=(
                "Mature paid cohort by lead-created hour, not same-day upload time."
            ),
            cap_snapshot_evidence=True,
            buyer_hours_evidence=True,
            ad_schedule_evidence=True,
            call_reporting_evidence=True,
            no_buyer_tracking_ready=True,
            missed_contact_tracking_ready=True,
            dayparting_cohort_ready=True,
            fallback_buyer_reviewed=True,
            human_review=True,
            score=100,
            risk_level="low",
            recommended_action="approve_small_ramp",
            cap_usage_percent=Decimal("35.00"),
            cap_remaining=Decimal("78.00"),
            projected_end_of_day_usage_percent=Decimal("77.78"),
            safe_leads_remaining=Decimal("19.00"),
            safe_media_spend_remaining=Decimal("545.44"),
            blockers=[],
            status="open",
            notes=(
                "Demo: buyer cap, hours, schedule, timezone and fallback "
                "evidence support a small manual ramp."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/6372656",
                "https://support.google.com/google-ads/answer/1704443",
            ],
        )
    )
    return 1


def _seed_demo_conversion_signal_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = ConversionSignalReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo qualified lead signal review",
    ).first()
    if exists:
        return 0

    db.session.add(
        ConversionSignalReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo qualified lead signal review",
            vertical="b2b_saas",
            geo="US",
            conversion_goal_name="lead_quality_us",
            conversion_action_name="lead_qualified_b2b_us",
            action_stage="qualified",
            primary_status="secondary",
            recommended_primary_status="primary_candidate",
            value_mode="expected",
            bid_strategy="target_cpa",
            traffic_scope="search_phrase_exact",
            weekly_conversions=Decimal("86.00"),
            weekly_approved_conversions=Decimal("61.00"),
            weekly_paid_conversions=Decimal("44.00"),
            reported_value_per_conversion=Decimal("42.0000"),
            approved_rate_percent=Decimal("70.93"),
            paid_rate_percent=Decimal("72.13"),
            click_id_coverage_percent=Decimal("98.20"),
            offline_match_rate_percent=Decimal("86.40"),
            duplicate_rate_percent=Decimal("0.60"),
            average_lag_days=Decimal("1.80"),
            p95_lag_days=Decimal("4.20"),
            incident_count_30d=0,
            segment_granularity_status="offer_geo_buyer_source",
            policy_consent_status="reviewed",
            customer_data_status="policy_reviewed",
            offline_import_status="diagnostics_ready",
            transaction_id_status="idempotent",
            lag_stability_status="stable",
            bid_strategy_status="stable",
            goal_change_summary=(
                "Qualified stays secondary until two mature cohorts prove paid value."
            ),
            affected_campaigns="Demo cloud backup search draft.",
            value_mapping_notes=(
                "Expected value uses payout times approved and paid rates; paid "
                "event remains the mature calibration source."
            ),
            dedupe_notes="transaction_id = lead_id:qualified, one event per stage.",
            lag_notes="Primary observation window covers the 95th percentile lag.",
            diagnostics_notes=(
                "Offline import diagnostics, match rate and duplicate checks are "
                "reviewed before any bidding change."
            ),
            rollback_plan=(
                "Demote to secondary and return to manual CPC if reject, duplicate "
                "or match diagnostics degrade."
            ),
            primary_secondary_reviewed=True,
            value_mapping_reviewed=True,
            transaction_id_dedupe_ready=True,
            offline_import_diagnostics_ready=True,
            conversion_lag_reviewed=True,
            segment_split_ready=True,
            consent_policy_reviewed=True,
            bid_strategy_report_reviewed=True,
            change_history_evidence=True,
            human_review=True,
            score_components={
                "value_closeness_to_paid": 22,
                "match_and_attribution_quality": 15,
                "deduplication_integrity": 15,
                "lag_stability": 10,
                "sample_volume": 10,
                "segment_granularity": 10,
                "policy_and_consent_safety": 10,
                "incident_history": 5,
            },
            score=97,
            risk_level="low",
            recommended_action="bid_ready_with_cap",
            bid_readiness="bid_ready",
            expected_paid_value_per_conversion=Decimal("21.4900"),
            safe_target_cpa=Decimal("13.9685"),
            blockers=[],
            status="open",
            notes=(
                "Demo: qualified lead signal is close enough to paid value for a "
                "capped bidding test after human review."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/11461796",
                "https://support.google.com/google-ads/answer/3419241",
                "https://support.google.com/google-ads/answer/9347141",
            ],
        )
    )
    return 1


def _seed_demo_crm_value_mapping_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = CrmValueMappingReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo CRM qualified value mapping",
    ).first()
    if exists:
        return 0

    db.session.add(
        CrmValueMappingReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo CRM qualified value mapping",
            buyer_name="Demo direct advertiser",
            vertical="b2b_saas",
            geo="US",
            source_system="HubSpot CRM demo export",
            buyer_feedback_source="buyer weekly quality CSV",
            source_stage="SQL_ACCEPTED",
            standard_stage="qualified",
            buyer_status="qualified",
            conversion_action_name="lead_qualified_b2b_us",
            conversion_action_role="secondary",
            primary_recommendation="primary_candidate",
            value_mode="expected",
            recommended_upload_policy="offline_import_candidate",
            payout_amount=Decimal("42.0000"),
            approved_rate_percent=Decimal("72.00"),
            paid_rate_percent=Decimal("68.00"),
            return_rate_percent=Decimal("4.00"),
            variable_cost_per_conversion=Decimal("1.2500"),
            weekly_stage_count=Decimal("84.00"),
            weekly_unique_leads=Decimal("82.00"),
            rejected_count=Decimal("3.00"),
            returned_count=Decimal("2.00"),
            duplicate_count=Decimal("1.00"),
            click_id_match_rate_percent=Decimal("91.00"),
            import_success_rate_percent=Decimal("97.00"),
            import_error_rate_percent=Decimal("1.00"),
            average_stage_lag_days=Decimal("2.20"),
            return_window_days=14,
            transaction_id_status="idempotent",
            adjustment_rule_status="ready",
            import_batch_status="qa_ready",
            diagnostics_status="reviewed",
            consent_status="reviewed",
            pii_handling_status="hashed_minimized",
            stage_mapping_notes=(
                "SQL_ACCEPTED maps to qualified after buyer field contract review."
            ),
            conversion_action_notes=(
                "Qualified is kept secondary until mature paid cohorts support primary."
            ),
            value_mapping_notes=(
                "Expected value = payout * approved_rate * paid_rate - variable cost."
            ),
            transaction_id_notes="transaction_id = lead_id:qualified and is idempotent.",
            import_qa_notes="Batch QA checks row count, unique lead count and error rate.",
            adjustment_notes="Returned leads use adjustment/retraction review, not positive upload.",
            lag_notes="Qualified feedback lag is normally under 3 days.",
            diagnostics_notes="Offline import diagnostics and match rate are reviewed weekly.",
            rollback_plan="Stop upload candidate and demote to secondary on match or return spike.",
            stage_taxonomy_reviewed=True,
            buyer_feedback_contract_reviewed=True,
            conversion_action_mapping_reviewed=True,
            primary_secondary_reviewed=True,
            value_mode_reviewed=True,
            transaction_id_rule_ready=True,
            rejected_returned_excluded=True,
            adjustment_policy_ready=True,
            import_batch_qa_ready=True,
            diagnostics_reviewed=True,
            lag_profile_reviewed=True,
            consent_policy_reviewed=True,
            human_review=True,
            score_components={
                "stage_mapping": 15,
                "conversion_action_mapping": 14,
                "value_mapping": 15,
                "dedupe_and_transaction_id": 15,
                "import_batch_qa": 15,
                "adjustment_readiness": 10,
                "lag_profile": 5,
                "policy_and_pii": 10,
            },
            score=99,
            risk_level="low",
            recommended_action="offline_import_candidate",
            expected_value=Decimal("19.3136"),
            blockers=[],
            status="open",
            notes=(
                "Demo: CRM qualified stage is mapped, deduped and QA-ready for "
                "manual offline import review."
            ),
            source_urls=[
                "https://support.google.com/google-ads/answer/7012522",
                "https://developers.google.com/google-ads/api/docs/conversions/upload-clicks",
                "https://developers.google.com/google-ads/api/docs/conversions/adjust-conversions",
            ],
        )
    )
    return 1


def _seed_demo_lead_validation_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = LeadValidationReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo pre-routing lead validation gate",
    ).first()
    if exists:
        return 0

    db.session.add(
        LeadValidationReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo pre-routing lead validation gate",
            vertical="insurance",
            geo="US",
            source_type="google_search",
            form_version="form_v2026_06_consent_a",
            validation_scope="pre_routing",
            lead_channel="web_form",
            consent_status="buyer_scope_reviewed",
            buyer_disclosure_status="contract_reviewed",
            phone_status="normalized",
            email_status="normalized",
            address_geo_status="buyer_service_area",
            duplicate_status="source_buyer_windowed",
            suppression_status="ready",
            dnc_status="checked",
            opt_out_status="checked",
            pii_minimization_status="hashed_minimized",
            retention_status="deletion_ready",
            source_policy_status="buyer_approved",
            buyer_reject_feedback_status="paid_feedback_ready",
            validation_sample_size=500,
            valid_rate_percent=Decimal("86.00"),
            invalid_contact_rate_percent=Decimal("4.00"),
            duplicate_rate_percent=Decimal("2.00"),
            suppression_hit_rate_percent=Decimal("0.80"),
            dnc_hit_rate_percent=Decimal("0.30"),
            opt_out_rate_percent=Decimal("0.40"),
            bad_geo_rate_percent=Decimal("1.20"),
            no_consent_rate_percent=Decimal("0.50"),
            buyer_reject_rate_percent=Decimal("6.00"),
            complaint_rate_percent=Decimal("0.10"),
            fields_collected_schema=(
                "Operational IDs, consent version, source/form version, zip/state, "
                "qualification answers and phone/email hash. Raw contact fields are "
                "not written to URLs, subids, logs or AI prompts."
            ),
            validation_rule_summary=(
                "Schema, consent, format normalization, duplicate hash, suppression, "
                "DNC, opt-out, geo eligibility, source policy and buyer reject feedback "
                "are checked before routing."
            ),
            duplicate_rule_summary=(
                "Same phone/email hash 30d, same buyer campaign 90d and transaction_id "
                "forever. Event duplicates do not create additional conversions."
            ),
            suppression_rule_summary=(
                "Suppression, DNC, opt-out and consent revocation hashes are checked "
                "before any buyer handoff and resynced after complaint events."
            ),
            pii_handling_notes=(
                "Duplicate checks use salted hashes; raw contact fields are available "
                "only for approved handoff roles and are excluded from exports by default."
            ),
            retention_deletion_notes=(
                "Raw lead detail has a defined retention window; consent evidence and "
                "suppression hashes have separate retention/deletion workflows."
            ),
            buyer_reject_reason_map=(
                "invalid_contact, duplicate, bad_geo, no_consent, cap_reached, "
                "low_intent and prohibited_source map back to source/form fixes."
            ),
            source_form_fix_plan=(
                "Reject spikes open source quarantine, form copy review, disclosure "
                "version review and geo/qualification rule repair."
            ),
            incident_notes="No open suppression, DNC, opt-out or complaint incident for the demo cohort.",
            consent_evidence=True,
            buyer_disclosure_reviewed=True,
            field_minimization_reviewed=True,
            duplicate_rule_reviewed=True,
            suppression_dnc_checked=True,
            pii_access_reviewed=True,
            retention_policy_reviewed=True,
            reject_reason_mapped=True,
            source_policy_reviewed=True,
            human_review=True,
            score_components={
                "consent_integrity": 20,
                "contact_format_quality": 15,
                "duplicate_safety": 15,
                "suppression_clearance": 15,
                "geo_offer_fit": 10,
                "source_policy_fit": 10,
                "buyer_feedback_quality": 10,
                "pii_minimization_retention": 5,
            },
            score=100,
            risk_level="low",
            recommended_action="validation_ready",
            usable_lead_rate_percent=Decimal("76.56"),
            expected_valid_leads=Decimal("382.80"),
            safe_routing_rate_percent=Decimal("76.56"),
            blockers=[],
            status="open",
            notes=(
                "Demo: the cohort is ready for human-supervised routing because "
                "consent, suppression, DNC, opt-out, duplicate, PII and reject "
                "feedback controls are present."
            ),
            source_urls=[
                "https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business",
                "https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
                "https://telemarketing.donotcall.gov/",
                "https://csrc.nist.gov/pubs/sp/800/122/final",
                "https://support.google.com/analytics/answer/6366371",
            ],
        )
    )
    return 1


def _seed_demo_ping_post_routing_reviews() -> int:
    campaign = CampaignDraft.query.order_by(CampaignDraft.id).first()
    if not campaign:
        return 0
    exists = PingPostRoutingReview.query.filter_by(
        campaign_draft_id=campaign.id,
        name="Demo exclusive ping-post routing gate",
    ).first()
    if exists:
        return 0

    db.session.add(
        PingPostRoutingReview(
            offer_id=campaign.offer_id,
            campaign_draft_id=campaign.id,
            name="Demo exclusive ping-post routing gate",
            vertical="insurance",
            geo="US",
            buyer_group_name="Demo approved direct buyers",
            source_type="google_search",
            form_version="form_v2026_06_consent_a",
            routing_mode="ping_post",
            lead_type="exclusive",
            consent_scope="named_buyer_group",
            buyer_disclosure_status="contract_reviewed",
            ping_field_scope="hashed_dedupe",
            pii_level="post_only_to_selected_buyer",
            suppression_status="ready",
            dnc_status="checked",
            cap_snapshot_status="realtime",
            fallback_status="reviewed_same_intent",
            buyer_feedback_status="paid_feedback_ready",
            source_policy_status="buyer_approved",
            buyer_count=4,
            max_post_buyers=1,
            pinged_buyers=3,
            accepted_buyers=2,
            posted_buyers=1,
            primary_buyer_cap_remaining=Decimal("42.00"),
            cap_last_checked_minutes=12,
            lead_age_minutes=2,
            avg_ping_latency_ms=420,
            expected_bid_amount=Decimal("55.0000"),
            fallback_payout_amount=Decimal("24.0000"),
            buyer_accept_rate_percent=Decimal("72.00"),
            qualification_rate_percent=Decimal("58.00"),
            paid_rate_percent=Decimal("52.00"),
            no_buyer_rate_percent=Decimal("2.00"),
            reject_rate_percent=Decimal("9.00"),
            duplicate_rate_percent=Decimal("1.50"),
            complaint_rate_percent=Decimal("0.20"),
            fields_sent_schema=(
                "Ping sends vertical, zip3, lead_age_seconds, source_type, "
                "form_version, consent_version and phone/email hash only. Full "
                "contact data is only posted to the selected buyer after checks."
            ),
            routing_rule_summary=(
                "Consent and buyer disclosure first, then suppression/DNC, buyer "
                "match, realtime cap, effective paid value and exclusive post count."
            ),
            buyer_disclosure_notes=(
                "Buyer group and contact channels are disclosed in the reviewed form "
                "version; contract restricts resale and post count."
            ),
            cap_snapshot_notes=(
                "Realtime cap snapshot from buyer dashboard, checked under 15 minutes "
                "before the manual test window."
            ),
            reject_reason_map=(
                "duplicate, bad_geo, invalid_contact, no_consent, cap_reached, "
                "low_intent and buyer_closed map back to source/form fixes."
            ),
            fallback_policy=(
                "Fallback is same intent and same disclosure only; fallback payout "
                "must still clear safe CPL before traffic continues."
            ),
            buyer_feedback_plan=(
                "Buyer returns accepted, contacted, qualified, approved, paid, "
                "returned and complaint statuses with buyer_lead_id for reconciliation."
            ),
            suppression_notes=(
                "Opt-out, DNC and duplicate suppression are checked before routing and "
                "resynced to buyers on complaint or revocation."
            ),
            consent_evidence_notes=(
                "Evidence includes consent text hash, form URL, buyer group disclosure, "
                "privacy policy URL and timestamp."
            ),
            incident_notes="No open complaint or no-buyer incident for the demo cohort.",
            consent_version_evidence=True,
            buyer_disclosure_reviewed=True,
            field_minimization_reviewed=True,
            suppression_dnc_checked=True,
            cap_snapshot_evidence=True,
            routing_rule_reviewed=True,
            exclusive_shared_terms_reviewed=True,
            fallback_buyer_reviewed=True,
            buyer_feedback_ready=True,
            source_policy_reviewed=True,
            human_review=True,
            score_components={
                "consent_and_disclosure": 15,
                "field_minimization_pii": 15,
                "routing_rule_quality": 15,
                "buyer_cap_capacity": 15,
                "economics_feedback": 15,
                "suppression_dnc": 10,
                "exclusive_shared_aged_governance": 10,
                "incident_policy_safety": 5,
            },
            score=100,
            risk_level="low",
            recommended_action="routing_ready",
            expected_payable_value_per_lead=Decimal("13.4583"),
            safe_cpl=Decimal("8.7479"),
            blockers=[],
            status="open",
            notes=(
                "Demo: exclusive Ping/Post route is ready for a human-supervised "
                "small test because consent, field minimization, cap and feedback "
                "evidence are all present."
            ),
            source_urls=[
                "https://docs.pingtree.com/documentation/campaign/distribution/ping-post",
                "https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
                "https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200",
                "https://support.google.com/google-ads/answer/9423234",
            ],
        )
    )
    return 1


def ensure_schema_compatibility() -> None:
    """Apply small additive schema fixes for existing local demo databases."""
    inspector = inspect(db.engine)
    if "research_sources" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("research_sources")}
    if "review_status" not in columns:
        db.session.execute(
            text(
                "ALTER TABLE research_sources "
                "ADD COLUMN review_status VARCHAR(40) NOT NULL DEFAULT 'candidate'"
            )
        )
        db.session.commit()


def _seed_demo_research_sources() -> int:
    existing = {
        (source.title, source.url, source.capability)
        for source in ResearchSource.query.with_entities(
            ResearchSource.title, ResearchSource.url, ResearchSource.capability
        ).all()
    }
    added = 0
    for source in _demo_research_sources():
        key = (source.title, source.url, source.capability)
        if key in existing:
            continue
        db.session.add(source)
        existing.add(key)
        added += 1
    return added


def _demo_research_sources() -> list[ResearchSource]:
    return [
        ResearchSource(
            topic="ADXKit 公开功能拆解",
            capability=None,
            title="ADXKit homepage",
            url="https://adxkit.com/",
            publisher="ADXKit",
            source_type="product_page",
            reliability="public_claim",
            claim_summary=(
                "公开页面展示了无需 API、Scripts 同步、补点击、换链接、代理、"
                "Worker 转发、防关联、AI 创意生成等功能叙事。"
            ),
            notes="用于拆解产品定位和功能清单，不代表内部实现验证。",
        ),
        ResearchSource(
            topic="Ads 套利业务模式拆解",
            capability=None,
            title="Advertising network abuse",
            url="https://support.google.com/adspolicy/answer/6008942",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 广告网络滥用政策覆盖 arbitrage、桥页、网关页、"
                "广告目的地低价值和误导用户等模式风险。"
            ),
        ),
        ResearchSource(
            topic="Ads 套利业务模式拆解",
            capability="invalid_traffic_click_impression_simulation",
            title="Use of online advertising to get new users to the site",
            url="https://support.google.com/adsense/answer/1348722",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "发布商可以购买流量获取新用户，但需要对流量质量负责，"
                "并监控可疑来源和无效流量。"
            ),
        ),
        ResearchSource(
            topic="Ads 套利业务模式拆解",
            capability=None,
            title="A guide to identifying Made for Advertising websites",
            url="https://www.iabuk.com/news-article/guide-identifying-made-advertising-websites",
            publisher="IAB UK",
            source_type="industry_reference",
            reliability="industry_reference",
            claim_summary=(
                "IAB UK 用高广告密度、内容质量弱、流量模式异常等特征识别 MFA 库存。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="Using HTTP cookies",
            url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies",
            publisher="MDN",
            source_type="technical_reference",
            reliability="primary",
            claim_summary=(
                "Cookie 用于会话管理，浏览器会在后续请求携带会话 ID，"
                "因此登录 Cookie 属于敏感身份凭据。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="Secure your Google Ads account",
            url="https://support.google.com/google-ads/answer/2375456",
            publisher="Google Ads Help",
            source_type="security_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 安全文档把安全挑战用于保护账号免受 cookie theft，"
                "并建议 2-Step Verification、最小权限和访问审计。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="MDN, Set-Cookie header",
            url="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie",
            publisher="MDN",
            source_type="technical_reference",
            reliability="primary",
            claim_summary=(
                "Set-Cookie 文档支撑 Secure、HttpOnly、SameSite、Expires "
                "和 Max-Age 等会话安全属性说明。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="OWASP Session Management Cheat Sheet",
            url="https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html",
            publisher="OWASP",
            source_type="security_reference",
            reliability="primary",
            claim_summary=(
                "Session management guidance 支撑把 session id 视为敏感凭据，"
                "并做生命周期、传输、存储和撤销治理。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="Google Ads Help, About access levels in your Google Ads account",
            url="https://support.google.com/google-ads/answer/9978556",
            publisher="Google Ads Help",
            source_type="access_control",
            reliability="primary",
            claim_summary=(
                "Access levels 支撑用账号权限模型协作，"
                "而不是共享登录态或复用 Cookie。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="Google Ads API OAuth overview",
            url="https://developers.google.com/google-ads/api/docs/oauth/overview",
            publisher="Google Ads API Documentation",
            source_type="official_api_documentation",
            reliability="primary",
            claim_summary=(
                "OAuth overview 支撑用官方授权 token 和 scope 集成，"
                "不处理用户浏览器登录 Cookie。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="Google Ads Scripts, Authorization",
            url="https://developers.google.com/google-ads/scripts/docs/authorization",
            publisher="Google Ads Scripts Documentation",
            source_type="official_script_documentation",
            reliability="primary",
            claim_summary=(
                "Scripts authorization 支撑账号内授权脚本、preview/log "
                "和有限批量操作替代 Cookie 后台接管。"
            ),
        ),
        ResearchSource(
            topic="Ads Cookie 登录和后台操作",
            capability="ads_cookie_backend_operation",
            title="Google Ads Editor Help",
            url="https://support.google.com/google-ads/editor",
            publisher="Google Ads Help",
            source_type="official_tool_documentation",
            reliability="primary",
            claim_summary=(
                "Google Ads Editor 支撑人工审核型批量编辑、导入导出 "
                "和可回滚操作流程。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="About access levels in your Google Ads account",
            url="https://support.google.com/google-ads/answer/9978556",
            publisher="Google Ads Help",
            source_type="access_control",
            reliability="primary",
            claim_summary=(
                "Google Ads 支持按访问级别授权，说明合规协作应靠权限模型，"
                "不是共享登录态或绕过验证。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="Confirm it is you",
            url="https://support.google.com/google-ads/answer/12865189",
            publisher="Google Ads Help",
            source_type="security_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 会在敏感或异常场景下要求确认身份，"
                "说明安全挑战是账号保护机制，不应被自动绕过。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="Use OAuth 2.0 to Access Google Ads API",
            url="https://developers.google.com/google-ads/api/docs/oauth/overview",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Google Ads API 使用 OAuth 2.0 做认证授权，应用无需处理或存储用户登录信息。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="Secure your Google Ads account",
            url="https://support.google.com/google-ads/answer/2375456",
            publisher="Google Ads Help",
            source_type="security_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads account security guidance 支撑 2-Step Verification、"
                "访问审计、强密码和账号保护边界。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="Google Account Help, Turn on 2-Step Verification",
            url="https://support.google.com/accounts/answer/185839",
            publisher="Google Account Help",
            source_type="security_policy",
            reliability="primary",
            claim_summary=(
                "2-Step Verification guidance 支撑第二因素是账号保护机制，"
                "不应被自动化或供应商接管。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="Google Ads Help, Manager account access levels",
            url="https://support.google.com/google-ads/answer/9977851",
            publisher="Google Ads Help",
            source_type="access_control",
            reliability="primary",
            claim_summary=(
                "Manager account access levels 支撑 MCC 权限边界、"
                "多人协作和外包访问治理。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="Google Ads Scripts, Authorization",
            url="https://developers.google.com/google-ads/scripts/docs/authorization",
            publisher="Google Ads Scripts Documentation",
            source_type="official_script_documentation",
            reliability="primary",
            claim_summary=(
                "Scripts authorization 支撑授权用户安装和运行脚本，"
                "而不是绕过登录或安全挑战。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="OWASP Authentication Cheat Sheet",
            url="https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
            publisher="OWASP",
            source_type="security_reference",
            reliability="primary",
            claim_summary=(
                "Authentication guidance 支撑认证失败、安全响应、"
                "凭据保护和任务升级原则。"
            ),
        ),
        ResearchSource(
            topic="自动绕过登录、2FA、安全挑战",
            capability="automated_login_2fa_challenge_bypass",
            title="OWASP Multifactor Authentication Cheat Sheet",
            url="https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html",
            publisher="OWASP",
            source_type="security_reference",
            reliability="primary",
            claim_summary=(
                "MFA guidance 支撑第二因素、恢复流程和防止弱化 MFA "
                "的治理边界。"
            ),
        ),
        ResearchSource(
            topic="Search Arbitrage、Feed 与 Parking",
            capability=None,
            title="Search ads policies",
            url="https://support.google.com/adsense/answer/7003954",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Search ads policies 说明查询变量必须匹配用户搜索意图、"
                "每个用户动作只允许一个广告请求，广告必须清楚标识并用于搜索结果页。"
            ),
        ),
        ResearchSource(
            topic="Search Arbitrage、Feed 与 Parking",
            capability=None,
            title="Custom Search Ads Web Implementation",
            url="https://developers.google.com/custom-search-ads/web/",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Custom Search Ads web implementation 需要 active permission，"
                "适合作为 search feed 权限和结果页集成边界的来源。"
            ),
        ),
        ResearchSource(
            topic="Search Arbitrage、Feed 与 Parking",
            capability=None,
            title="Parked domain site",
            url="https://support.google.com/google-ads/answer/50002",
            publisher="Google Ads Help",
            source_type="ad_network_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads parked domain 文档说明 parked domain 定义、Search Partner "
                "库存语境，以及新旧账号默认 opt out parked domains 的时间。"
            ),
        ),
        ResearchSource(
            topic="Search Arbitrage、Feed 与 Parking",
            capability=None,
            title="Advertising network abuse",
            url="https://support.google.com/adspolicy/answer/6008942",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Advertising network abuse 支撑对 arbitrage、bridge/gateway、"
                "低价值目的地和广告网络滥用风险的判断。"
            ),
        ),
        ResearchSource(
            topic="RSOC / N2S 与 Search Feed Partner 治理",
            capability=None,
            title="Google AdSense Related search for content pages",
            url="https://support.google.com/adsense/answer/10233819",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Related Search for content pages 支撑 RSOC 的二屏搜索广告、文本内容、"
                "权限和页面焦点边界。"
            ),
        ),
        ResearchSource(
            topic="RSOC / N2S 与 Search Feed Partner 治理",
            capability=None,
            title="Google AdSense AFS Product-Integrated Feature policies",
            url="https://support.google.com/adsense/answer/14638581",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "PIF policies 支撑 Related Search、partner-provided terms、广告请求、"
                "诱导点击和搜索结果页边界。"
            ),
        ),
        ResearchSource(
            topic="RSOC / N2S 与 Search Feed Partner 治理",
            capability=None,
            title="Google Custom Search Ads implementation guide for RAC",
            url="https://developers.google.com/custom-search-ads/s/docs/implementation-guide",
            publisher="Google for Developers",
            source_type="technical_reference",
            reliability="primary",
            claim_summary=(
                "CSA implementation guide 支撑 referrerAdCreative、content page、"
                "Related Search unit 和受控流量创意证据要求。"
            ),
        ),
        ResearchSource(
            topic="RSOC / N2S 与 Search Feed Partner 治理",
            capability=None,
            title="Google AdSense Restricted Access Features",
            url="https://support.google.com/adsense/answer/16262554",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "RAF 文档支撑 strike、访问权限受限功能和政策违规对 Related Search 权限的影响。"
            ),
        ),
        ResearchSource(
            topic="RSOC / N2S 与 Search Feed Partner 治理",
            capability=None,
            title="Google Ads advertising network abuse for RSOC",
            url="https://support.google.com/adspolicy/answer/6008942",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Advertising network abuse 支撑对 bridge/gateway、arbitrage、"
                "低价值目的地和审核规避风险的判断。"
            ),
        ),
        ResearchSource(
            topic="RSOC / N2S 与 Search Feed Partner 治理",
            capability=None,
            title="Jounce Media terminology for arbitrage context",
            url="https://jouncemedia.com/resources/terminology",
            publisher="Jounce Media",
            source_type="industry_reference",
            reliability="industry_reference",
            claim_summary=(
                "Jounce terminology 仅作为 MFA、arbitrage 等行业术语背景，"
                "不作为合规放行依据。"
            ),
        ),
        ResearchSource(
            topic="补点击、刷展示、模拟自然流量",
            capability="invalid_traffic_click_impression_simulation",
            title="Definition of invalid traffic",
            url="https://support.google.com/adsense/answer/16737",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "无效流量包括可能人为抬高广告主成本或发布商收入的点击和展示，"
                "自动点击工具、机器人和欺骗性软件被明确列为问题。"
            ),
        ),
        ResearchSource(
            topic="补点击、刷展示、模拟自然流量",
            capability="invalid_traffic_click_impression_simulation",
            title="How Google prevents invalid traffic",
            url="https://support.google.com/adsense/answer/1348752",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "Google 使用自动系统和人工审核分析广告点击与展示，过滤可能人为抬高成本或收入的流量。"
            ),
        ),
        ResearchSource(
            topic="补点击、刷展示、模拟自然流量",
            capability="invalid_traffic_click_impression_simulation",
            title="Google AdSense Program policies",
            url="https://support.google.com/adsense/answer/48182",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Program policies 支撑禁止鼓励点击、自动点击工具、"
                "paid-to-click、paid-to-surf、autosurf 和 click-exchange。"
            ),
        ),
        ResearchSource(
            topic="补点击、刷展示、模拟自然流量",
            capability="invalid_traffic_click_impression_simulation",
            title="Google Publisher Policies",
            url="https://support.google.com/publisherpolicies/answer/10437486",
            publisher="Google Publisher Policies Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Publisher Policies 支撑发布商内容、广告行为、"
                "用户体验和流量质量的基础边界。"
            ),
        ),
        ResearchSource(
            topic="补点击、刷展示、模拟自然流量",
            capability="invalid_traffic_click_impression_simulation",
            title="Google AdSense Help, Deductions from earnings FAQs",
            url="https://support.google.com/adsense/answer/2808531",
            publisher="Google AdSense Help",
            source_type="settlement_guidance",
            reliability="primary",
            claim_summary=(
                "Deductions guidance 支撑 finalized revenue、deduction、"
                "invalid traffic adjustment 和 payable revenue 复盘。"
            ),
        ),
        ResearchSource(
            topic="流量源、追踪和归因",
            capability=None,
            title="About tracking in Google Ads",
            url="https://support.google.com/google-ads/answer/6076199",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads 支持 Final URL、tracking template、Final URL suffix "
                "和 URL options，用于记录点击上下文并测试落地页。"
            ),
        ),
        ResearchSource(
            topic="流量源、追踪和归因",
            capability=None,
            title="Traffic-source dimensions, manual tagging, and auto-tagging",
            url="https://support.google.com/analytics/answer/11242870",
            publisher="Google Analytics Help",
            source_type="analytics_reference",
            reliability="primary",
            claim_summary=(
                "GA4 用 source、medium、campaign 等维度描述流量来源，"
                "支持手动 UTM 标记和平台集成的自动标记。"
            ),
        ),
        ResearchSource(
            topic="流量源、追踪和归因",
            capability=None,
            title="Traffic provider checklist",
            url="https://support.google.com/adsense/answer/3332805",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "购买流量前应了解展示位置、供应商流量来源、样例 URL、"
                "成本异常和是否可按来源监控与停量。"
            ),
        ),
        ResearchSource(
            topic="Native、Advertorial 与 Presell Page",
            capability=None,
            title="FTC Native Advertising Guide for advertorial disclosure",
            url="https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC Native Advertising Guide 支撑 advertorial、native ad 和商业内容需要清楚披露广告性质。"
            ),
        ),
        ResearchSource(
            topic="Native、Advertorial 与 Presell Page",
            capability=None,
            title="FTC deceptively formatted advertisements policy",
            url="https://www.ftc.gov/legal-library/browse/commission-policy-statement-enforcement-policy-statement-deceptively-formatted-advertisements",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "Deceptively formatted advertisements policy 支撑识别伪装新闻、评测或独立内容的广告风险。"
            ),
        ),
        ResearchSource(
            topic="Native、Advertorial 与 Presell Page",
            capability=None,
            title="Google Ads destination requirements for presell pages",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Destination requirements 支撑 presell page 不应成为低价值桥页，广告承诺和最终页面要一致。"
            ),
        ),
        ResearchSource(
            topic="Native、Advertorial 与 Presell Page",
            capability=None,
            title="Google Ads misrepresentation for native claims",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation 支撑审查 native 标题、评价、官方关系、价格和商业关系是否误导。"
            ),
        ),
        ResearchSource(
            topic="Native、Advertorial 与 Presell Page",
            capability=None,
            title="Taboola advertising policies for native traffic",
            url="https://www.taboola.com/policies/advertising-policies",
            publisher="Taboola",
            source_type="platform_policy",
            reliability="primary",
            claim_summary=(
                "Taboola advertising policies 支撑 Native 平台对误导素材、敏感内容和落地页质量的要求。"
            ),
        ),
        ResearchSource(
            topic="Native、Advertorial 与 Presell Page",
            capability=None,
            title="Outbrain advertising guidelines for native campaigns",
            url="https://www.outbrain.com/guidelines/advertising-guidelines/",
            publisher="Outbrain",
            source_type="platform_policy",
            reliability="primary",
            claim_summary=(
                "Outbrain advertising guidelines 支撑 Native 平台对广告格式、误导素材和目标页质量的要求。"
            ),
        ),
        ResearchSource(
            topic="Click -> Session -> Revenue 对账",
            capability=None,
            title="Google Ads tracking for click-session reconciliation",
            url="https://support.google.com/google-ads/answer/6076199",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads URL options 支撑从广告点击到落地页请求的第一层 QA，"
                "用于检查 Final URL、tracking template 和 suffix。"
            ),
        ),
        ResearchSource(
            topic="Click -> Session -> Revenue 对账",
            capability=None,
            title="Auto-tagging for click identifiers",
            url="https://support.google.com/google-ads/answer/3095550",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Auto-tagging 支撑 gclid 等点击标识，帮助 Google Ads、GA4 和转化回传对账。"
            ),
        ),
        ResearchSource(
            topic="Click -> Session -> Revenue 对账",
            capability=None,
            title="GA4 data freshness for reconciliation windows",
            url="https://support.google.com/analytics/answer/11198161",
            publisher="Google Analytics Help",
            source_type="analytics_reference",
            reliability="primary",
            claim_summary=(
                "GA4 数据存在刷新延迟，日报需要标注 freshness，避免用未完整数据判断 ROI。"
            ),
        ),
        ResearchSource(
            topic="Click -> Session -> Revenue 对账",
            capability=None,
            title="Consent mode overview for measurement loss",
            url="https://developers.google.com/tag-platform/security/concepts/consent-mode",
            publisher="Google for Developers",
            source_type="privacy_reference",
            reliability="primary",
            claim_summary=(
                "Consent Mode 说明同意状态会影响广告和分析存储，"
                "click/session 差异需要考虑 consent 和 tag 行为。"
            ),
        ),
        ResearchSource(
            topic="Click -> Session -> Revenue 对账",
            capability=None,
            title="Google Ads API upload click conversions diagnostics",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-summaries",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Conversion upload diagnostics 支撑排查上传转化的匹配、错误和处理状态，"
                "不用伪造 postback 修复缺口。"
            ),
        ),
        ResearchSource(
            topic="Click -> Session -> Revenue 对账",
            capability="invalid_traffic_click_impression_simulation",
            title="AdSense invalid traffic for revenue reconciliation",
            url="https://support.google.com/adsense/answer/16737",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "AdSense invalid traffic 定义支撑把高点击、低收入或扣量问题归入来源隔离，"
                "而不是用补点击或模拟 session 修报表。"
            ),
        ),
        ResearchSource(
            topic="追踪模板、URL 参数与跳转链 QA",
            capability=None,
            title="About ValueTrack parameters",
            url="https://support.google.com/google-ads/answer/2375447",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "ValueTrack 参数会在点击时替换成关键词、设备、匹配类型等上下文，"
                "适合追踪真实点击来源。"
            ),
        ),
        ResearchSource(
            topic="追踪模板、URL 参数与跳转链 QA",
            capability=None,
            title="About parallel tracking",
            url="https://support.google.com/google-ads/answer/7544674",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Parallel tracking 让用户直接到达 Final URL，同时后台加载追踪请求，"
                "追踪平台需要兼容这种链路。"
            ),
        ),
        ResearchSource(
            topic="追踪模板、URL 参数与跳转链 QA",
            capability=None,
            title="About auto-tagging",
            url="https://support.google.com/google-ads/answer/3095550",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Auto-tagging 会添加 Google 点击标识，支撑 Google Ads、GA4 和转化归因。"
            ),
        ),
        ResearchSource(
            topic="追踪模板、URL 参数与跳转链 QA",
            capability=None,
            title="Final URL suffix",
            url="https://support.google.com/google-ads/answer/9054021",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Final URL suffix 用于向最终 URL 追加追踪参数，"
                "需要避免参数冲突、PII 暴露和归因重复。"
            ),
        ),
        ResearchSource(
            topic="追踪模板、URL 参数与跳转链 QA",
            capability=None,
            title="Campaign tracking URL template field",
            url="https://developers.google.com/google-ads/api/fields/v23/campaign#campaign.tracking_url_template",
            publisher="Google Ads API",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Google Ads API 提供 campaign.tracking_url_template 字段，"
                "未来可用官方 API 审计追踪模板，不需要 Cookie 后台接管。"
            ),
        ),
        ResearchSource(
            topic="转化追踪、价值回传与 Attribution",
            capability=None,
            title="Primary and secondary conversion actions",
            url="https://support.google.com/google-ads/answer/11461796",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Primary/secondary conversion actions 用于区分出价目标和观察口径，"
                "支撑 submitted、qualified、approved、paid 分层设计。"
            ),
        ),
        ResearchSource(
            topic="转化追踪、价值回传与 Attribution",
            capability=None,
            title="Manage offline conversions",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-offline",
            publisher="Google Ads API",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Offline conversions 可把 CRM、qualified lead、approved/paid revenue "
                "回传给 Google Ads，帮助优化到后端质量。"
            ),
        ),
        ResearchSource(
            topic="转化追踪、价值回传与 Attribution",
            capability=None,
            title="About enhanced conversions",
            url="https://support.google.com/google-ads/answer/9888656",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Enhanced Conversions 使用经过处理的用户提供数据提升测量准确性，"
                "需要和 customer data policy、consent、隐私披露一起设计。"
            ),
        ),
        ResearchSource(
            topic="转化追踪、价值回传与 Attribution",
            capability=None,
            title="About attribution models",
            url="https://support.google.com/google-ads/answer/6259715",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Attribution models 说明转化 credit 如何分配给广告互动，"
                "支撑 Ads、GA4、affiliate、CRM 之间的口径差异解释。"
            ),
        ),
        ResearchSource(
            topic="落地页质量、广告密度与 MFA 风险",
            capability=None,
            title="Destination requirements",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 目的地要求覆盖目的地不可用、不匹配、不可抓取、"
                "体验差、原创内容不足和桥页等落地页风险。"
            ),
        ),
        ResearchSource(
            topic="落地页质量、广告密度与 MFA 风险",
            capability=None,
            title="Better Ads Standards",
            url="https://www.betterads.org/standards/",
            publisher="Coalition for Better Ads",
            source_type="industry_standard",
            reliability="industry_reference",
            claim_summary=(
                "Better Ads Standards 列出弹窗、插屏、自动播放有声视频、"
                "高广告密度和 large sticky 等低体验广告形态。"
            ),
        ),
        ResearchSource(
            topic="落地页质量、广告密度与 MFA 风险",
            capability=None,
            title="A guide to identifying Made for Advertising websites",
            url="https://www.iabuk.com/news-article/guide-identifying-made-advertising-websites",
            publisher="IAB UK",
            source_type="industry_reference",
            reliability="industry_reference",
            claim_summary=(
                "IAB UK 将 MFA 常见特征概括为高广告密度、内容质量弱、"
                "流量模式异常和刻意延长用户旅程。"
            ),
        ),
        ResearchSource(
            topic="回款、结算与现金流风险",
            capability=None,
            title="About payment settings in Google Ads",
            url="https://support.google.com/google-ads/answer/2375432",
            publisher="Google Ads Help",
            source_type="billing_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads 支持自动付款、手动付款和月结发票；广告费可能在收入到账前发生。"
            ),
        ),
        ResearchSource(
            topic="回款、结算与现金流风险",
            capability=None,
            title="Payment timelines for AdSense",
            url="https://support.google.com/adsense/answer/7164703",
            publisher="Google AdSense Help",
            source_type="payment_reference",
            reliability="primary",
            claim_summary=(
                "AdSense 收入按月估算、次月初 finalized，达到阈值且无 hold 时通常在月中下旬付款。"
            ),
        ),
        ResearchSource(
            topic="回款、结算与现金流风险",
            capability=None,
            title="Deductions from earnings FAQs",
            url="https://support.google.com/adsense/answer/2808531",
            publisher="Google AdSense Help",
            source_type="payment_reference",
            reliability="primary",
            claim_summary=(
                "收入可能因无效点击、政策不合规或广告主付款问题发生扣减，"
                "需要纳入扣量和现金流安全垫。"
            ),
        ),
        ResearchSource(
            topic="发布商收入对账、Finalized Revenue 与扣量复盘",
            capability=None,
            title="AdSense Metrics glossary for revenue reconciliation",
            url="https://support.google.com/adsense/answer/2735899",
            publisher="Google AdSense Help",
            source_type="metrics_reference",
            reliability="primary",
            claim_summary=(
                "AdSense 指标词汇表定义 RPM、CTR、coverage、Active View 等收入端指标，"
                "用于统一 estimated/finalized revenue 对账口径。"
            ),
        ),
        ResearchSource(
            topic="发布商收入对账、Finalized Revenue 与扣量复盘",
            capability=None,
            title="AdSense Payment timelines for finalized revenue",
            url="https://support.google.com/adsense/answer/7164703",
            publisher="Google AdSense Help",
            source_type="payment_reference",
            reliability="primary",
            claim_summary=(
                "AdSense payment timeline 说明 estimated earnings、finalized earnings、"
                "付款时间、hold 和扣减周期，是月度关账的核心依据。"
            ),
        ),
        ResearchSource(
            topic="发布商收入对账、Finalized Revenue 与扣量复盘",
            capability=None,
            title="AdSense Deductions from earnings FAQs for reconciliation",
            url="https://support.google.com/adsense/answer/2808531",
            publisher="Google AdSense Help",
            source_type="payment_reference",
            reliability="primary",
            claim_summary=(
                "收入可能因无效流量、政策问题或广告主付款问题被扣减，"
                "对账时需要计算 deduction_rate 和 finalization_ratio。"
            ),
        ),
        ResearchSource(
            topic="发布商收入对账、Finalized Revenue 与扣量复盘",
            capability="invalid_traffic_click_impression_simulation",
            title="AdSense traffic segmentation plan for revenue QA",
            url="https://support.google.com/adsense/answer/2583698",
            publisher="Google AdSense Help",
            source_type="traffic_quality_reference",
            reliability="primary",
            claim_summary=(
                "按来源、渠道或广告位置分段监控流量，有助于把扣量复盘落到具体来源，"
                "并隔离异常流量。"
            ),
        ),
        ResearchSource(
            topic="发布商收入对账、Finalized Revenue 与扣量复盘",
            capability=None,
            title="AdSense Management API metrics and dimensions",
            url="https://developers.google.com/adsense/management/metrics-dimensions",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "AdSense Management API 指标和维度可作为未来报表导入器的字段口径来源。"
            ),
        ),
        ResearchSource(
            topic="发布商收入对账、Finalized Revenue 与扣量复盘",
            capability=None,
            title="Google Ad Manager API reporting for reconciliation",
            url="https://developers.google.com/ad-manager/api/reporting",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Google Ad Manager API reporting 支撑未来导入 GAM/AdX 报表并对账收入。"
            ),
        ),
        ResearchSource(
            topic="广告创意生成、测试与优化",
            capability=None,
            title="Responsive Search Ads",
            url="https://developers.google.com/google-ads/api/docs/responsive-search-ads/overview",
            publisher="Google Ads API",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Responsive Search Ads 使用多个 headlines 和 descriptions 自动组合测试表现，"
                "支持 pinning 和组合表现统计。"
            ),
        ),
        ResearchSource(
            topic="广告创意生成、测试与优化",
            capability=None,
            title="About Ad strength for responsive search ads",
            url="https://support.google.com/google-ads/answer/9921843",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "Ad Strength 提供 responsive search ad 的诊断反馈，"
                "帮助识别资产数量、相关性、重复和 sitelinks 等优化机会。"
            ),
        ),
        ResearchSource(
            topic="广告创意生成、测试与优化",
            capability=None,
            title="Text ad requirements",
            url="https://support.google.com/adspolicy/answer/6021630",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Text ads 需要遵守 Google Ads 标准政策，尤其是编辑、文字、目的地和常见拒登要求。"
            ),
        ),
        ResearchSource(
            topic="广告创意 Claim 审核与事实核查",
            capability=None,
            title="Misrepresentation for ad claim review",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation 政策支撑对主体、价格、服务、资质、官方关系、"
                "商业关系和结果承诺做创意上线前事实核查。"
            ),
        ),
        ResearchSource(
            topic="广告创意 Claim 审核与事实核查",
            capability=None,
            title="Editorial requirements for claim review",
            url="https://support.google.com/adspolicy/answer/6021546",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Editorial requirements 支撑检查异常大写、标点、符号、错拼、"
                "display URL 和 gimmicky wording。"
            ),
        ),
        ResearchSource(
            topic="广告创意 Claim 审核与事实核查",
            capability=None,
            title="Trademarks for creative claims",
            url="https://support.google.com/adspolicy/answer/6118",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "商标政策支撑广告文字中品牌、竞品名、授权关系和 reseller/informational "
                "表达的审核。"
            ),
        ),
        ResearchSource(
            topic="广告创意 Claim 审核与事实核查",
            capability=None,
            title="Unacceptable business practices for creative claims",
            url="https://support.google.com/adspolicy/answer/15938071",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Unacceptable business practices 支撑识别冒充品牌、组织、公众人物或诱导用户交钱/交信息的创意风险。"
            ),
        ),
        ResearchSource(
            topic="广告创意 Claim 审核与事实核查",
            capability=None,
            title="Responsive search ads and claim combinations",
            url="https://support.google.com/google-ads/answer/7684791",
            publisher="Google Ads Help",
            source_type="creative_reference",
            reliability="primary",
            claim_summary=(
                "RSA 会组合多个 headlines 和 descriptions，审核时需要检查组合后是否产生更强误导承诺。"
            ),
        ),
        ResearchSource(
            topic="广告创意 Claim 审核与事实核查",
            capability=None,
            title="FTC Endorsement Guides for review claims",
            url="https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides",
            publisher="FTC",
            source_type="consumer_protection_reference",
            reliability="primary",
            claim_summary=(
                "FTC Endorsement Guides 支撑用户评价、达人推荐、背书、affiliate "
                "关系和商业利益披露的事实核查。"
            ),
        ),
        ResearchSource(
            topic="AI Provider、Prompt 模板与创意成本治理",
            capability=None,
            title="Google Ads automatically created assets for AI governance",
            url="https://support.google.com/google-ads/answer/11259373",
            publisher="Google Ads Help",
            source_type="creative_reference",
            reliability="primary",
            claim_summary=(
                "Automatically created assets 支撑把自动生成资产作为候选进入 Claim 审核和人工放行。"
            ),
        ),
        ResearchSource(
            topic="AI Provider、Prompt 模板与创意成本治理",
            capability=None,
            title="Google Ads misrepresentation for AI outputs",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation 支撑拦截 AI 新增的主体、价格、资质、官方关系和结果承诺。"
            ),
        ),
        ResearchSource(
            topic="AI Provider、Prompt 模板与创意成本治理",
            capability=None,
            title="Google Ads editorial requirements for AI copy",
            url="https://support.google.com/adspolicy/answer/6021546",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Editorial requirements 支撑 AI 输出的标点、大小写、重复、样式和文案质量检查。"
            ),
        ),
        ResearchSource(
            topic="AI Provider、Prompt 模板与创意成本治理",
            capability=None,
            title="NIST AI Risk Management Framework",
            url="https://www.nist.gov/itl/ai-risk-management-framework",
            publisher="NIST",
            source_type="ai_governance_reference",
            reliability="primary",
            claim_summary=(
                "AI RMF 支撑 provider、prompt、输出、评估、人审和风险治理框架。"
            ),
        ),
        ResearchSource(
            topic="AI Provider、Prompt 模板与创意成本治理",
            capability=None,
            title="NIST AI RMF Generative AI Profile",
            url="https://www.nist.gov/itl/ai-risk-management-framework/generative-ai-profile",
            publisher="NIST",
            source_type="ai_governance_reference",
            reliability="primary",
            claim_summary=(
                "Generative AI Profile 支撑生成式 AI 幻觉、内容风险和治理控制。"
            ),
        ),
        ResearchSource(
            topic="AI Provider、Prompt 模板与创意成本治理",
            capability=None,
            title="OWASP Top 10 for LLM Applications",
            url="https://owasp.org/www-project-top-10-for-large-language-model-applications/",
            publisher="OWASP",
            source_type="ai_security_reference",
            reliability="primary",
            claim_summary=(
                "OWASP LLM Top 10 支撑 prompt injection、数据泄漏、输出处理和 LLM 应用安全检查。"
            ),
        ),
        ResearchSource(
            topic="落地页素材抽取、Offer Intelligence 与创意 Brief",
            capability=None,
            title="Destination experience",
            url="https://support.google.com/adspolicy/answer/16427615",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 目的地体验要求页面功能可用、有用且易于导航，"
                "素材抽取需要检查 CTA、承诺、导航和用户下一步是否一致。"
            ),
        ),
        ResearchSource(
            topic="落地页素材抽取、Offer Intelligence 与创意 Brief",
            capability=None,
            title="Editorial requirements",
            url="https://support.google.com/adspolicy/answer/6021546",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Editorial requirements 支撑广告文字、标点、格式、display URL "
                "和误导性表达的上线前检查。"
            ),
        ),
        ResearchSource(
            topic="落地页素材抽取、Offer Intelligence 与创意 Brief",
            capability=None,
            title="Misrepresentation for landing claims",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation 政策要求主体、价格、服务、资格、官方关系和商业关系真实透明，"
                "因此创意 claim 必须有页面 proof 支撑。"
            ),
        ),
        ResearchSource(
            topic="落地页素材抽取、Offer Intelligence 与创意 Brief",
            capability=None,
            title="Helpful content for offer briefs",
            url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content",
            publisher="Google Search Central",
            source_type="content_quality_reference",
            reliability="primary",
            claim_summary=(
                "Helpful content 文档支撑页面应围绕用户价值、原创信息、可信来源和清楚目的，"
                "可用于评估素材抽取后的创意 brief 是否真实。"
            ),
        ),
        ResearchSource(
            topic="落地页素材抽取、Offer Intelligence 与创意 Brief",
            capability=None,
            title="Endorsements, influencers, and reviews",
            url="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews",
            publisher="FTC",
            source_type="consumer_protection_reference",
            reliability="primary",
            claim_summary=(
                "FTC 对背书、达人推荐、用户评价和商业关系披露有明确消费者保护要求，"
                "评价素材不能伪造、误导或隐藏激励关系。"
            ),
        ),
        ResearchSource(
            topic="链接计划与换链接合规",
            capability=None,
            title="About tracking in Google Ads",
            url="https://support.google.com/google-ads/answer/6076199",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads 的 URL options 覆盖 Final URL、tracking template、"
                "Final URL suffix 和测试流程，适合可审计链接维护。"
            ),
        ),
        ResearchSource(
            topic="链接计划与换链接合规",
            capability="cloaking_review_user_page_mismatch",
            title="Circumventing systems",
            url="https://support.google.com/adspolicy/answer/15938075",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "通过隐藏真实目的地、向 Google 和用户展示不同内容或规避政策执行的换链接属于高风险红线。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 投放结构与安全自动化",
            capability=None,
            title="Campaigns overview",
            url="https://developers.google.com/google-ads/api/docs/campaigns/overview",
            publisher="Google Ads API",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Google Ads API 的 campaign 文档说明 campaign、ad group、ad 和 criteria "
                "等对象结构，支撑投放草稿和 API 方向集成。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 投放结构与安全自动化",
            capability=None,
            title="About negative keywords",
            url="https://support.google.com/google-ads/answer/2453972",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "否定词用于排除不相关搜索，是控制套利测试浪费和意图错配的重要机制。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 投放结构与安全自动化",
            capability=None,
            title="Google Ads Scripts authorization",
            url="https://developers.google.com/google-ads/scripts/docs/authorization",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Google Ads Scripts 需要授权才能代表账号执行，适合作为安全自动化路径，"
                "不需要处理登录 Cookie。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 安全自动化",
            capability=None,
            title="Google Ads Scripts Bulk Upload",
            url="https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Bulk Upload 支持通过 Google Ads Scripts 创建批量上传和预览，"
                "适合承接人审后的结构化 payload。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 安全自动化",
            capability=None,
            title="Google Ads Scripts Limits",
            url="https://developers.google.com/google-ads/scripts/docs/limits",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "Google Ads Scripts 有运行时长、账号范围和配额边界，"
                "不适合作为无限制无人值守后台操作器。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 安全自动化",
            capability=None,
            title="Google Ads Scripts AdsApp reference",
            url="https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "AdsApp 是 Google Ads Scripts 访问账号对象的官方入口，"
                "需要在授权脚本环境中运行。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 安全自动化",
            capability=None,
            title="Google Ads Scripts BulkUpload reference",
            url="https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp_bulkupload",
            publisher="Google for Developers",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "BulkUpload reference 说明 preview/apply 等对象行为，"
                "本项目模板默认只做 preview。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 竞价、Quality Score 与套利出价",
            capability=None,
            title="How the Google Ads auction works",
            url="https://support.google.com/google-ads/answer/6366577",
            publisher="Google Ads Help",
            source_type="auction_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads auction 文档支撑 Ad Rank、出价、广告质量、"
                "竞价上下文、资产影响和实际 CPC 的解释。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 竞价、Quality Score 与套利出价",
            capability=None,
            title="About Quality Score for Search campaigns",
            url="https://support.google.com/google-ads/answer/6167118",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "Quality Score 是诊断指标，包含 expected CTR、ad relevance "
                "和 landing page experience，可用于定位套利买量问题。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 竞价、Quality Score 与套利出价",
            capability=None,
            title="About Smart Bidding",
            url="https://support.google.com/google-ads/answer/7065882",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "Smart Bidding 使用转化和转化价值优化竞价；套利场景需要确保转化代表可收回收入。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 竞价、Quality Score 与套利出价",
            capability=None,
            title="About overdelivery and your average daily budget",
            url="https://support.google.com/google-ads/answer/1704443",
            publisher="Google Ads Help",
            source_type="billing_reference",
            reliability="primary",
            claim_summary=(
                "平均日预算可能发生 overdelivery，套利团队需要平台外部硬止损和现金流安全垫。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 报表诊断",
            capability=None,
            title="Google Ads search terms report for arbitrage diagnostics",
            url="https://support.google.com/google-ads/answer/2472708",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Search terms report 支撑按真实搜索词、keyword 和 match type 诊断意图、"
                "否定词和低 ROI 查询。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 报表诊断",
            capability=None,
            title="Google Ads auction insights for competitor pressure",
            url="https://support.google.com/google-ads/answer/2579754",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Auction insights 支撑用 impression share、overlap、top of page 和 outranking "
                "解释竞争变化和 CPC 压力。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 报表诊断",
            capability=None,
            title="Google Ads change history for performance incident review",
            url="https://support.google.com/google-ads/answer/19888",
            publisher="Google Ads Help",
            source_type="audit_reference",
            reliability="primary",
            claim_summary=(
                "Change history 支撑把预算、出价、素材、URL、转化和 recommendation 改动"
                "与表现波动关联。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 报表诊断",
            capability=None,
            title="Google Ads Report Editor for saved diagnostic exports",
            url="https://support.google.com/google-ads/answer/7489070",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Report Editor 支撑保存、下载和分段报表，作为优化动作的证据归档。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 报表诊断",
            capability=None,
            title="Google Ads landing pages report diagnostics",
            url="https://support.google.com/google-ads/answer/7543502",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Landing pages report 支撑 expanded URL、移动端页面体验、点击到站和页面版本诊断。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 报表诊断",
            capability=None,
            title="Google Ads bid strategy reports diagnostics",
            url="https://support.google.com/google-ads/answer/7074568",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Bid strategy reports 支撑 Smart Bidding 学习、状态、目标和自动出价表现诊断。"
            ),
        ),
        ResearchSource(
            topic="Performance Max / Demand Gen 自动化流量",
            capability=None,
            title="Google Ads Performance Max campaigns overview",
            url="https://support.google.com/google-ads/answer/10724817",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "Performance Max 支撑跨 Google Ads inventory 的自动化投放，"
                "套利团队需要先验证转化价值、页面和预算止损。"
            ),
        ),
        ResearchSource(
            topic="Performance Max / Demand Gen 自动化流量",
            capability=None,
            title="Google Ads Performance Max results evaluation",
            url="https://support.google.com/google-ads/answer/16279166",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "PMax 结果评估支撑把自动化流量拆成 channel、asset、landing page "
                "和后端 paid revenue 复盘。"
            ),
        ),
        ResearchSource(
            topic="Performance Max / Demand Gen 自动化流量",
            capability=None,
            title="Google Ads PMax channel performance report",
            url="https://support.google.com/google-ads/answer/16260130",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Channel performance report 支撑按 Search、YouTube、Discover、Gmail 等"
                "库存拆分 PMax ROI。"
            ),
        ),
        ResearchSource(
            topic="Performance Max / Demand Gen 自动化流量",
            capability=None,
            title="Google Ads Final URL expansion for PMax",
            url="https://support.google.com/google-ads/answer/16672777",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "Final URL expansion 会影响用户最终进入的页面，套利团队要记录 URL exclusions、"
                "page feed 和页面审核证据。"
            ),
        ),
        ResearchSource(
            topic="Performance Max / Demand Gen 自动化流量",
            capability=None,
            title="Google Ads Search themes for PMax",
            url="https://support.google.com/google-ads/answer/14767319",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "Search themes 是 PMax 的搜索主题提示，不是关键词硬匹配，"
                "需要与 query、brand exclusions 和后端收入一起复盘。"
            ),
        ),
        ResearchSource(
            topic="Performance Max / Demand Gen 自动化流量",
            capability=None,
            title="Google Ads Demand Gen campaigns overview",
            url="https://support.google.com/adwords/answer/6105478",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "Demand Gen 支撑视觉/内容场景触达，需要用素材质量、受众信号、"
                "engaged sessions 和 paid revenue 判断是否适合套利。"
            ),
        ),
        ResearchSource(
            topic="Search 自动化流量",
            capability=None,
            title="Google Ads AI Max for Search campaigns overview",
            url="https://support.google.com/google-ads/answer/15910187",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "AI Max for Search 支撑 Search campaign 中匹配、资产和 URL 自动化，"
                "需要 query、asset、landing page 和 paid revenue 复盘。"
            ),
        ),
        ResearchSource(
            topic="Search 自动化流量",
            capability=None,
            title="Google Ads AI Max Search setup controls",
            url="https://support.google.com/google-ads/answer/15909989",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "AI Max 设置文档支撑记录控制项、上线前审计和人工审批边界。"
            ),
        ),
        ResearchSource(
            topic="Search 自动化流量",
            capability=None,
            title="Google Ads Search final URL expansion controls",
            url="https://support.google.com/google-ads/answer/16230205",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "Search Final URL expansion 支撑 URL inclusions/exclusions、页面范围和追踪链 QA。"
            ),
        ),
        ResearchSource(
            topic="Search 自动化流量",
            capability=None,
            title="Google Ads broad match with Smart Bidding",
            url="https://support.google.com/google-ads/answer/12159290",
            publisher="Google Ads Help",
            source_type="bidding_reference",
            reliability="primary",
            claim_summary=(
                "Broad match 与 Smart Bidding 组合需要真实 conversion value 和后端收入校验，"
                "避免优化到低质转化。"
            ),
        ),
        ResearchSource(
            topic="Search 自动化流量",
            capability=None,
            title="Google Ads Dynamic Search Ads overview",
            url="https://support.google.com/google-ads/answer/2471185",
            publisher="Google Ads Help",
            source_type="campaign_reference",
            reliability="primary",
            claim_summary=(
                "DSA 基于网站内容匹配搜索并生成标题，适合页面库清晰而非薄页或混乱站点。"
            ),
        ),
        ResearchSource(
            topic="Search 自动化流量",
            capability=None,
            title="Google Ads automatically created assets overview",
            url="https://support.google.com/google-ads/answer/11259373",
            publisher="Google Ads Help",
            source_type="creative_reference",
            reliability="primary",
            claim_summary=(
                "Automatically created assets 需要进入 claim 审核和人工放行，"
                "不能自动生成无证据强声明。"
            ),
        ),
        ResearchSource(
            topic="域名、站点资产与站群治理",
            capability=None,
            title="Google Search spam policies for domain asset governance",
            url="https://developers.google.com/search/docs/essentials/spam-policies",
            publisher="Google Search Central",
            source_type="search_policy",
            reliability="primary",
            claim_summary=(
                "Search spam policies 支撑识别 expired domain abuse、site reputation abuse、"
                "cloaking 和低质 affiliate 风险。"
            ),
        ),
        ResearchSource(
            topic="域名、站点资产与站群治理",
            capability=None,
            title="Google Search site move with URL changes for migration QA",
            url="https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes",
            publisher="Google Search Central",
            source_type="migration_reference",
            reliability="primary",
            claim_summary=(
                "Site move with URL changes 支撑正常站点迁移、301、监控和迁移计划边界。"
            ),
        ),
        ResearchSource(
            topic="域名、站点资产与站群治理",
            capability=None,
            title="Google Ads destination requirements for domain final URL QA",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Help",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Destination requirements 支撑 Final URL、页面可访问、广告承诺一致和低价值目的地审计。"
            ),
        ),
        ResearchSource(
            topic="域名、站点资产与站群治理",
            capability="cloaking_review_user_page_mismatch",
            title="Google Ads circumventing systems for domain switching risk",
            url="https://support.google.com/adspolicy/answer/15938075",
            publisher="Google Ads Help",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Circumventing systems 支撑判断换域名、隐藏目的地、多站点和 cloaking 是否在规避政策执行。"
            ),
        ),
        ResearchSource(
            topic="域名、站点资产与站群治理",
            capability=None,
            title="AdSense add new site and site review for publisher assets",
            url="https://support.google.com/adsense/answer/12169212",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "AdSense Sites list 支撑发布商站点添加、审核状态和站点资产治理。"
            ),
        ),
        ResearchSource(
            topic="域名、站点资产与站群治理",
            capability=None,
            title="AdSense ads.txt file for authorized seller governance",
            url="https://support.google.com/adsense/answer/7532444",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "ads.txt 支撑发布商域名授权卖方声明，避免 seller ID 和站点授权关系不透明。"
            ),
        ),
        ResearchSource(
            topic="Geo、语言、本地化、时区与币种分层",
            capability=None,
            title="Google Ads geographic location targeting for arbitrage QA",
            url="https://support.google.com/google-ads/answer/1722043",
            publisher="Google Ads Help",
            source_type="targeting_reference",
            reliability="primary",
            claim_summary=(
                "Location targeting 支撑按国家、地区、城市和半径控制投放范围，"
                "用于扩国家和 bad geo 诊断。"
            ),
        ),
        ResearchSource(
            topic="Geo、语言、本地化、时区与币种分层",
            capability=None,
            title="Google Ads advanced location options presence interest",
            url="https://support.google.com/google-ads/answer/1722038",
            publisher="Google Ads Help",
            source_type="targeting_reference",
            reliability="primary",
            claim_summary=(
                "Advanced location options 支撑区分目标地实际用户、经常在该地用户和"
                "对目标地感兴趣的用户。"
            ),
        ),
        ResearchSource(
            topic="Geo、语言、本地化、时区与币种分层",
            capability=None,
            title="Google Ads language targeting for localized pages",
            url="https://support.google.com/google-ads/answer/1722078",
            publisher="Google Ads Help",
            source_type="targeting_reference",
            reliability="primary",
            claim_summary=(
                "Language targeting 支撑语言定向和页面本地化区分，不能替代广告文案和页面翻译审查。"
            ),
        ),
        ResearchSource(
            topic="Geo、语言、本地化、时区与币种分层",
            capability=None,
            title="Google Ads geographic performance measurement",
            url="https://support.google.com/google-ads/answer/2453994",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Geographic performance 支撑按地理位置复盘 cost、click、conversion、bad geo 和扩量机会。"
            ),
        ),
        ResearchSource(
            topic="Geo、语言、本地化、时区与币种分层",
            capability=None,
            title="Google Ads account language time zone currency settings",
            url="https://support.google.com/google-ads/answer/9842104",
            publisher="Google Ads Help",
            source_type="account_reference",
            reliability="primary",
            claim_summary=(
                "账号语言、数字格式、时区和币种设置会影响报表边界、账单和 ROI 对账。"
            ),
        ),
        ResearchSource(
            topic="Geo、语言、本地化、时区与币种分层",
            capability=None,
            title="Google Ads conversion lag reporting for timezone QA",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag reporting 支撑跨日转化、dayparting、日报 ROI 和回传延迟判断。"
            ),
        ),
        ResearchSource(
            topic="预算节奏、扩量与止损",
            capability=None,
            title="Budget report",
            url="https://support.google.com/google-ads/answer/10702522",
            publisher="Google Ads Help",
            source_type="budget_reference",
            reliability="primary",
            claim_summary=(
                "Budget report 可用于理解每日花费、月度花费限制和预算变化对投放的影响。"
            ),
        ),
        ResearchSource(
            topic="预算节奏、扩量与止损",
            capability=None,
            title="About ad scheduling",
            url="https://support.google.com/google-ads/answer/6372656",
            publisher="Google Ads Help",
            source_type="budget_reference",
            reliability="primary",
            claim_summary=(
                "Ad scheduling 支持按星期和小时控制广告展示，适合在有足够样本后做 dayparting。"
            ),
        ),
        ResearchSource(
            topic="预算节奏、扩量与止损",
            capability=None,
            title="About bid adjustments",
            url="https://support.google.com/google-ads/answer/2732132",
            publisher="Google Ads Help",
            source_type="bidding_reference",
            reliability="primary",
            claim_summary=(
                "Bid adjustments 可按设备、地点、时段等维度调整出价，"
                "套利场景应以可收款 RPV 倒推。"
            ),
        ),
        ResearchSource(
            topic="预算节奏、扩量与止损",
            capability=None,
            title="About location targeting",
            url="https://support.google.com/google-ads/answer/1722043",
            publisher="Google Ads Help",
            source_type="targeting_reference",
            reliability="primary",
            claim_summary=(
                "Location targeting 支撑按国家、地区或半径控制投放范围，"
                "用于 geo 分层预算和本地政策审计。"
            ),
        ),
        ResearchSource(
            topic="预算节奏、扩量与止损",
            capability=None,
            title="Time lag report",
            url="https://support.google.com/google-ads/answer/6239119",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Time lag report 展示从点击到转化的时间差，可避免因回传延迟过早停量或扩量。"
            ),
        ),
        ResearchSource(
            topic="Portfolio 预算分配、风险集中度与组合治理",
            capability="portfolio_budget_allocation_risk_concentration",
            title="Google Ads Help, Budget report",
            url="https://support.google.com/google-ads/answer/10702522",
            publisher="Google Ads Help",
            source_type="budget_reference",
            reliability="primary",
            claim_summary=(
                "Budget report 支撑理解每日花费、月度花费限制和预算变化，"
                "用于组合预算节奏和 cash at risk 复盘。"
            ),
        ),
        ResearchSource(
            topic="Portfolio 预算分配、风险集中度与组合治理",
            capability="portfolio_budget_allocation_risk_concentration",
            title="Google Ads Help, About spending limits",
            url="https://support.google.com/google-ads/answer/10486637",
            publisher="Google Ads Help",
            source_type="budget_reference",
            reliability="primary",
            claim_summary=(
                "Spending limits 支撑区分 average daily budget、daily spending limit、"
                "monthly spending limit、served cost 和 billed cost。"
            ),
        ),
        ResearchSource(
            topic="Portfolio 预算分配、风险集中度与组合治理",
            capability="portfolio_budget_allocation_risk_concentration",
            title="Google Ads Help, Performance Planner",
            url="https://support.google.com/google-ads/answer/9230124",
            publisher="Google Ads Help",
            source_type="planning_reference",
            reliability="primary",
            claim_summary=(
                "Performance Planner 支撑预算 scenario 和 campaign planning，"
                "但组合治理仍要以 approved/paid revenue 和风险上限为准。"
            ),
        ),
        ResearchSource(
            topic="Portfolio 预算分配、风险集中度与组合治理",
            capability="portfolio_budget_allocation_risk_concentration",
            title="Google Ads Help, About conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag reporting 支撑组合扩量前等待 conversion/revenue lag，"
                "避免把近期 ROI 误判为真实可收款表现。"
            ),
        ),
        ResearchSource(
            topic="Portfolio 预算分配、风险集中度与组合治理",
            capability="portfolio_budget_allocation_risk_concentration",
            title="Google AdSense Help, Payment timelines",
            url="https://support.google.com/adsense/answer/7164703",
            publisher="Google AdSense Help",
            source_type="payment_reference",
            reliability="primary",
            claim_summary=(
                "Payment timelines 支撑发布商收入到账延迟、cash reserve 和 paid revenue ratio "
                "在组合预算中的作用。"
            ),
        ),
        ResearchSource(
            topic="Portfolio 预算分配、风险集中度与组合治理",
            capability="portfolio_budget_allocation_risk_concentration",
            title="Google AdSense Help, Deductions from earnings FAQs",
            url="https://support.google.com/adsense/answer/2808531",
            publisher="Google AdSense Help",
            source_type="settlement_reference",
            reliability="primary",
            claim_summary=(
                "Deductions from earnings 支撑 finalized revenue 下调、deduction 和扣量风险，"
                "用于组合 revenue status mix 和集中度上限。"
            ),
        ),
        ResearchSource(
            topic="转化信号质量与出价学习治理",
            capability="conversion_signal_quality_bidding_learning_governance",
            title="Google Ads Help, About Smart Bidding",
            url="https://support.google.com/google-ads/answer/7065882",
            publisher="Google Ads Help",
            source_type="bidding_reference",
            reliability="primary",
            claim_summary=(
                "Smart Bidding 围绕 conversion 和 conversion value 优化，"
                "支撑把信号质量作为自动出价准入条件。"
            ),
        ),
        ResearchSource(
            topic="转化信号质量与出价学习治理",
            capability="conversion_signal_quality_bidding_learning_governance",
            title="Google Ads Help, Primary and secondary conversion actions",
            url="https://support.google.com/google-ads/answer/11461796",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Primary conversion actions 用于出价和默认 conversions 口径，"
                "secondary 更适合观察、诊断和浅层事件。"
            ),
        ),
        ResearchSource(
            topic="转化信号质量与出价学习治理",
            capability="conversion_signal_quality_bidding_learning_governance",
            title="Google Ads API, Upload offline conversions",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-offline",
            publisher="Google Ads API",
            source_type="api_reference",
            reliability="primary",
            claim_summary=(
                "Offline conversion upload 支撑把 CRM、buyer feedback、"
                "qualified、approved 和 paid 状态回传给广告优化系统。"
            ),
        ),
        ResearchSource(
            topic="转化信号质量与出价学习治理",
            capability="conversion_signal_quality_bidding_learning_governance",
            title="Google Ads Help, Fix offline conversion import discrepancies and errors",
            url="https://support.google.com/google-ads/answer/13321563",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Offline import discrepancies and errors 支撑记录 match、error、"
                "processing delay 和导入诊断，避免把未匹配数据当真相。"
            ),
        ),
        ResearchSource(
            topic="转化信号质量与出价学习治理",
            capability="conversion_signal_quality_bidding_learning_governance",
            title="Google Ads Help, About conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag reporting 支撑判断近期 CPA/ROAS 是否受回传延迟影响，"
                "并设定学习期和扩量等待窗口。"
            ),
        ),
        ResearchSource(
            topic="转化信号质量与出价学习治理",
            capability="conversion_signal_quality_bidding_learning_governance",
            title="Google Ads Help, Evaluate automated bid strategy performance",
            url="https://support.google.com/google-ads/answer/10167267",
            publisher="Google Ads Help",
            source_type="bidding_reference",
            reliability="primary",
            claim_summary=(
                "Automated bid strategy performance 评估需要考虑目标、"
                "学习状态、足够观察时间和 conversion lag。"
            ),
        ),
        ResearchSource(
            topic="决策窗口、回传延迟与收入延迟治理",
            capability="decision_window_revenue_lag_governance",
            title="Google Ads Help, About data freshness",
            url="https://support.google.com/google-ads/answer/2544985",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Data freshness 支撑不同指标和报表有刷新延迟，"
                "当天数据不能直接作为最终 ROI 决策。"
            ),
        ),
        ResearchSource(
            topic="决策窗口、回传延迟与收入延迟治理",
            capability="decision_window_revenue_lag_governance",
            title="Google Ads Help, Data discrepancies",
            url="https://support.google.com/google-ads/answer/7457111",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Data discrepancies 支撑 Google Ads、Analytics、第三方和内部报表差异诊断，"
                "避免把正常口径差异当事故。"
            ),
        ),
        ResearchSource(
            topic="决策窗口、回传延迟与收入延迟治理",
            capability="decision_window_revenue_lag_governance",
            title="Google Ads Help, About conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag reporting 支撑近期 CPA/ROAS、wait-loss "
                "和预算 ramp 的等待窗口设置。"
            ),
        ),
        ResearchSource(
            topic="决策窗口、回传延迟与收入延迟治理",
            capability="decision_window_revenue_lag_governance",
            title="Google Ads Help, About conversion delay estimates",
            url="https://support.google.com/google-ads/answer/14545572",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion delay estimates 支撑用延迟估计解释近期表现，"
                "避免过早暂停或扩量。"
            ),
        ),
        ResearchSource(
            topic="决策窗口、回传延迟与收入延迟治理",
            capability="decision_window_revenue_lag_governance",
            title="Google AdSense Help, Payment timelines",
            url="https://support.google.com/adsense/answer/7164703",
            publisher="Google AdSense Help",
            source_type="payment_reference",
            reliability="primary",
            claim_summary=(
                "Payment timelines 支撑区分 estimated、finalized 和 paid revenue，"
                "用于 settlement window 和现金流决策。"
            ),
        ),
        ResearchSource(
            topic="决策窗口、回传延迟与收入延迟治理",
            capability="decision_window_revenue_lag_governance",
            title="Google AdSense Help, Deductions from earnings FAQs",
            url="https://support.google.com/adsense/answer/2808531",
            publisher="Google AdSense Help",
            source_type="settlement_reference",
            reliability="primary",
            claim_summary=(
                "Deductions from earnings 支撑 finalized 下调、扣量和 deduction "
                "进入 revenue lag 与关账复盘。"
            ),
        ),
        ResearchSource(
            topic="单位经济模型、Break-even 与安全边际",
            capability="unit_economics_margin_safety",
            title="Google Ads Help, Determine a bid strategy based on your goals",
            url="https://support.google.com/google-ads/answer/2472725",
            publisher="Google Ads Help",
            source_type="bidding_reference",
            reliability="primary",
            claim_summary=(
                "Bid strategy selection 支撑按目标选择 CPC、conversion、CPA、ROAS，"
                "但套利团队需要先倒推可承受 CPC 和目标。"
            ),
        ),
        ResearchSource(
            topic="单位经济模型、Break-even 与安全边际",
            capability="unit_economics_margin_safety",
            title="Google Ads Help, Set a target ROAS bid strategy",
            url="https://support.google.com/google-ads/answer/6268637",
            publisher="Google Ads Help",
            source_type="bidding_reference",
            reliability="primary",
            claim_summary=(
                "Target ROAS 与 conversion value 相关，支撑用 net/paid value "
                "倒推出目标 ROAS，而不是使用 gross value。"
            ),
        ),
        ResearchSource(
            topic="单位经济模型、Break-even 与安全边际",
            capability="unit_economics_margin_safety",
            title="Google Ads Help, Budget report",
            url="https://support.google.com/google-ads/answer/10702522",
            publisher="Google Ads Help",
            source_type="budget_reference",
            reliability="primary",
            claim_summary=(
                "Budget report 支撑测试预算、硬止损和预算变化复盘，"
                "用于 unit economics 的成本侧治理。"
            ),
        ),
        ResearchSource(
            topic="单位经济模型、Break-even 与安全边际",
            capability="unit_economics_margin_safety",
            title="Google Ads API, Metrics fields",
            url="https://developers.google.com/google-ads/api/fields/v23/metrics",
            publisher="Google Ads API",
            source_type="api_reference",
            reliability="primary",
            claim_summary=(
                "Metrics fields 支撑 clicks、cost、conversions、conversion value "
                "等字段口径，用于未来报表导入和模型输入。"
            ),
        ),
        ResearchSource(
            topic="单位经济模型、Break-even 与安全边际",
            capability="unit_economics_margin_safety",
            title="Google AdSense Help, Metrics glossary",
            url="https://support.google.com/adsense/answer/2735899",
            publisher="Google AdSense Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Metrics glossary 支撑 RPM、CTR、coverage、Active View 等收入端指标，"
                "用于内容套利 RPV/RPM 模型。"
            ),
        ),
        ResearchSource(
            topic="单位经济模型、Break-even 与安全边际",
            capability="unit_economics_margin_safety",
            title="Google AdSense Help, Deductions from earnings FAQs",
            url="https://support.google.com/adsense/answer/2808531",
            publisher="Google AdSense Help",
            source_type="settlement_reference",
            reliability="primary",
            claim_summary=(
                "Deductions from earnings 支撑把扣量、无效流量和 finalized 下调 "
                "纳入 payable RPV、safe CPC 和 safety factor。"
            ),
        ),
        ResearchSource(
            topic="归因、增量性与流量蚕食治理",
            capability="attribution_incrementality_cannibalization",
            title="Google Ads Help, About attribution models",
            url="https://support.google.com/google-ads/answer/6259715",
            publisher="Google Ads Help",
            source_type="attribution_reference",
            reliability="primary",
            claim_summary=(
                "Attribution models 支撑解释 conversion credit 分配，"
                "但不能单独证明广告带来的增量利润。"
            ),
        ),
        ResearchSource(
            topic="归因、增量性与流量蚕食治理",
            capability="attribution_incrementality_cannibalization",
            title="Google Ads Help, Data-driven attribution",
            url="https://support.google.com/google-ads/answer/6394265",
            publisher="Google Ads Help",
            source_type="attribution_reference",
            reliability="primary",
            claim_summary=(
                "Data-driven attribution 是归因模型输出，"
                "套利预算仍要结合 holdout、lift 和增量收入判断。"
            ),
        ),
        ResearchSource(
            topic="归因、增量性与流量蚕食治理",
            capability="attribution_incrementality_cannibalization",
            title="Google Ads Help, About lift studies",
            url="https://support.google.com/google-ads/answer/16104408",
            publisher="Google Ads Help",
            source_type="incrementality_reference",
            reliability="primary",
            claim_summary=(
                "Lift studies 支撑测量广告带来的增量效果，"
                "用于区分 attributed revenue 和 incremental revenue。"
            ),
        ),
        ResearchSource(
            topic="归因、增量性与流量蚕食治理",
            capability="attribution_incrementality_cannibalization",
            title="Google Ads Help, Set up a custom experiment",
            url="https://support.google.com/google-ads/answer/6261395",
            publisher="Google Ads Help",
            source_type="experiment_reference",
            reliability="primary",
            claim_summary=(
                "Custom experiments 支撑 treatment/control 结构，"
                "用于测试出价、素材、流量和目标变化的增量效果。"
            ),
        ),
        ResearchSource(
            topic="归因、增量性与流量蚕食治理",
            capability="attribution_incrementality_cannibalization",
            title="Google Ads Help, Monitor your experiments",
            url="https://support.google.com/google-ads/answer/6318747",
            publisher="Google Ads Help",
            source_type="experiment_reference",
            reliability="primary",
            claim_summary=(
                "Monitor experiments 支撑实验观察、比较和决策，"
                "需要等待合适窗口和成熟收入。"
            ),
        ),
        ResearchSource(
            topic="归因、增量性与流量蚕食治理",
            capability="attribution_incrementality_cannibalization",
            title="Google Ads API, Experiments",
            url="https://developers.google.com/google-ads/api/docs/experiments/experiments",
            publisher="Google Ads API",
            source_type="api_reference",
            reliability="primary",
            claim_summary=(
                "Experiments API 支撑未来保存 experiment plan、split、"
                "status 和结果证据，而不是 Cookie 后台操作。"
            ),
        ),
        ResearchSource(
            topic="订阅、试用、退款、Chargeback 与 LTV 治理",
            capability="subscription_refund_ltv_chargeback_governance",
            title="FTC, Negative Option Rule",
            url="https://www.ftc.gov/legal-library/browse/rules/negative-option-rule",
            publisher="FTC",
            source_type="regulatory_reference",
            reliability="primary",
            claim_summary=(
                "Negative Option Rule 页面支撑订阅、自动续费和 negative option "
                "场景需要持续关注当前规则状态。"
            ),
        ),
        ResearchSource(
            topic="订阅、试用、退款、Chargeback 与 LTV 治理",
            capability="subscription_refund_ltv_chargeback_governance",
            title="FTC, Restore Online Shoppers' Confidence Act",
            url="https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act",
            publisher="FTC",
            source_type="regulatory_reference",
            reliability="primary",
            claim_summary=(
                "ROSCA 支撑在线 negative option、同意、披露和取消相关治理背景。"
            ),
        ),
        ResearchSource(
            topic="订阅、试用、退款、Chargeback 与 LTV 治理",
            capability="subscription_refund_ltv_chargeback_governance",
            title="FTC, .com Disclosures",
            url="https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising",
            publisher="FTC",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                ".com Disclosures 支撑价格、续费、退款、限制和重要条款需要清晰展示。"
            ),
        ),
        ResearchSource(
            topic="订阅、试用、退款、Chargeback 与 LTV 治理",
            capability="subscription_refund_ltv_chargeback_governance",
            title="Google Ads Policy, Misrepresentation",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation 支撑隐藏价格、收费、退款、资格或重要限制的广告风险判断。"
            ),
        ),
        ResearchSource(
            topic="订阅、试用、退款、Chargeback 与 LTV 治理",
            capability="subscription_refund_ltv_chargeback_governance",
            title="Google Ads Help, About conversion values",
            url="https://support.google.com/google-ads/answer/3419241",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion values 支撑订阅 LTV 和续费价值回传必须使用真实净值口径。"
            ),
        ),
        ResearchSource(
            topic="订阅、试用、退款、Chargeback 与 LTV 治理",
            capability="subscription_refund_ltv_chargeback_governance",
            title="Google Ads API, Upload offline conversions",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-offline",
            publisher="Google Ads API",
            source_type="api_reference",
            reliability="primary",
            claim_summary=(
                "Offline conversions 支撑把真实 renewal、paid、refund-adjusted value "
                "导回优化系统，而不是只回传 signup。"
            ),
        ),
        ResearchSource(
            topic="账号、MCC、付款与验证治理",
            capability=None,
            title="Google Ads manager accounts for account governance",
            url="https://support.google.com/google-ads/answer/6139186",
            publisher="Google Ads Help",
            source_type="account_reference",
            reliability="primary",
            claim_summary=(
                "Manager accounts 支撑集中管理多个账号，但应作为治理工具而不是账号池。"
            ),
        ),
        ResearchSource(
            topic="账号、MCC、付款与验证治理",
            capability=None,
            title="Google Ads account access levels governance",
            url="https://support.google.com/google-ads/answer/9978556",
            publisher="Google Ads Help",
            source_type="account_reference",
            reliability="primary",
            claim_summary=(
                "Access levels 支撑 Admin、Standard、Billing、Read only 等权限边界和最小权限协作。"
            ),
        ),
        ResearchSource(
            topic="账号、MCC、付款与验证治理",
            capability=None,
            title="Google Ads payment settings for billing governance",
            url="https://support.google.com/google-ads/answer/2375432",
            publisher="Google Ads Help",
            source_type="billing_reference",
            reliability="primary",
            claim_summary=(
                "Payment settings 支撑自动付款、手动付款、月结发票、账单国家和币种对现金流的影响。"
            ),
        ),
        ResearchSource(
            topic="账号、MCC、付款与验证治理",
            capability=None,
            title="Google Ads payments profile link types",
            url="https://support.google.com/google-ads/answer/15758513",
            publisher="Google Ads Help",
            source_type="billing_reference",
            reliability="primary",
            claim_summary=(
                "Payments profile link types 支撑付款 profile 与广告账号之间的关系解释和治理。"
            ),
        ),
        ResearchSource(
            topic="账号、MCC、付款与验证治理",
            capability=None,
            title="Google Ads advertiser verification governance",
            url="https://support.google.com/adspolicy/answer/9703665",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Advertiser verification 支撑广告主身份、业务操作、付款资料和广告披露一致性。"
            ),
        ),
        ResearchSource(
            topic="账号、MCC、付款与验证治理",
            capability="ban_evasion_account_switching",
            title="Google Ads circumventing systems account abuse policy",
            url="https://support.google.com/adspolicy/answer/15938075",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Circumventing systems 支撑识别多账号滥用、封禁后换号和用付款/代理关系规避政策执行。"
            ),
        ),
        ResearchSource(
            topic="关键词、搜索意图与选题研究",
            capability=None,
            title="Use Keyword Planner",
            url="https://support.google.com/google-ads/answer/7337243",
            publisher="Google Ads Help",
            source_type="planning_reference",
            reliability="primary",
            claim_summary=(
                "Keyword Planner 可用于发现关键词、查看历史统计和预测点击、成本、转化等计划指标。"
            ),
        ),
        ResearchSource(
            topic="关键词、搜索意图与选题研究",
            capability=None,
            title="Google Ads keyword matching",
            url="https://support.google.com/google-ads/answer/14996023",
            publisher="Google Ads Help",
            source_type="planning_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads keyword matching 说明 exact、phrase、broad match 如何匹配搜索意图。"
            ),
        ),
        ResearchSource(
            topic="关键词、搜索意图与选题研究",
            capability=None,
            title="About the search terms report",
            url="https://support.google.com/google-ads/answer/2472708",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "Search terms report 展示真实触发广告的查询，可用于新增否定词和发现高价值长尾词。"
            ),
        ),
        ResearchSource(
            topic="季节性、事件日历与需求预测",
            capability="seasonality_event_demand_forecasting",
            title="Google Ads Help, Get forecasts with Keyword Planner",
            url="https://support.google.com/google-ads/answer/3022575",
            publisher="Google Ads Help",
            source_type="planning_reference",
            reliability="primary",
            claim_summary=(
                "Keyword Planner forecasts 支撑按预算、出价、国家和语言估算 clicks、"
                "cost 和 forecast，用于季节性预算 ramp 前的规模判断。"
            ),
        ),
        ResearchSource(
            topic="季节性、事件日历与需求预测",
            capability="seasonality_event_demand_forecasting",
            title="Google Trends Help, FAQ about Trends data",
            url="https://support.google.com/trends/answer/4365533",
            publisher="Google Trends Help",
            source_type="trend_reference",
            reliability="primary",
            claim_summary=(
                "Trends FAQ 支撑理解 Trends 是归一化搜索兴趣，"
                "不能直接当作绝对点击量或收入预测。"
            ),
        ),
        ResearchSource(
            topic="季节性、事件日历与需求预测",
            capability="seasonality_event_demand_forecasting",
            title="Google Ads Help, About the Insights page",
            url="https://support.google.com/google-ads/answer/10256472",
            publisher="Google Ads Help",
            source_type="market_insight_reference",
            reliability="primary",
            claim_summary=(
                "Insights page 支撑把需求变化、趋势和市场洞察作为季节性诊断输入，"
                "但不能替代 paid revenue 和政策审计。"
            ),
        ),
        ResearchSource(
            topic="季节性、事件日历与需求预测",
            capability="seasonality_event_demand_forecasting",
            title="Google Ads Help, About seasonality adjustments",
            url="https://support.google.com/google-ads/answer/10369906",
            publisher="Google Ads Help",
            source_type="bidding_reference",
            reliability="primary",
            claim_summary=(
                "Seasonality adjustments 支撑 Smart Bidding 短期转化率变化提示的适用边界，"
                "不应被当成长期需求预测或错误回传修复。"
            ),
        ),
        ResearchSource(
            topic="季节性、事件日历与需求预测",
            capability="seasonality_event_demand_forecasting",
            title="IRS, Tax Time Guide",
            url="https://www.irs.gov/newsroom/tax-time-guide",
            publisher="IRS",
            source_type="official_calendar_reference",
            reliability="primary",
            claim_summary=(
                "IRS Tax Time Guide 支撑税务、退税和报税类页面使用官方税季资料和日期来源。"
            ),
        ),
        ResearchSource(
            topic="季节性、事件日历与需求预测",
            capability="seasonality_event_demand_forecasting",
            title="HealthCare.gov, Dates and deadlines",
            url="https://www.healthcare.gov/quick-guide/dates-and-deadlines/",
            publisher="HealthCare.gov",
            source_type="official_calendar_reference",
            reliability="primary",
            claim_summary=(
                "HealthCare.gov dates and deadlines 支撑健康保险开放注册类页面使用官方日期来源，"
                "避免旧日期或虚假紧迫感。"
            ),
        ),
        ResearchSource(
            topic="品牌词、商标与竞品投放合规",
            capability=None,
            title="Trademarks",
            url="https://support.google.com/adspolicy/answer/6118",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 商标政策说明商标投诉、广告中商标使用、"
                "reseller/informational site 以及商标关键词处理边界。"
            ),
        ),
        ResearchSource(
            topic="品牌词、商标与竞品投放合规",
            capability=None,
            title="Unacceptable business practices",
            url="https://support.google.com/adspolicy/answer/15938071",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "不可接受的商业行为覆盖冒充品牌、组织或公众人物，"
                "以及诱导用户交钱或提交个人信息的严重误导风险。"
            ),
        ),
        ResearchSource(
            topic="品牌词、商标与竞品投放合规",
            capability=None,
            title="Counterfeit goods",
            url="https://support.google.com/adspolicy/answer/176017",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Counterfeit goods 政策支撑仿牌、假货、近似商标商品和未授权正品声明的禁投边界。"
            ),
        ),
        ResearchSource(
            topic="品牌词、商标与竞品投放合规",
            capability=None,
            title="The FTC's Endorsement Guides",
            url="https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC Endorsement Guides 支撑 affiliate 推荐、评测、排名和商业利益披露要求。"
            ),
        ),
        ResearchSource(
            topic="买量渠道与流量供应商尽调",
            capability="invalid_traffic_click_impression_simulation",
            title="Traffic provider checklist",
            url="https://support.google.com/adsense/answer/3332805",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "购买流量前应询问供应商流量来源、展示位置、价格异常、样例 URL 和质量报告。"
            ),
        ),
        ResearchSource(
            topic="买量渠道与流量供应商尽调",
            capability="invalid_traffic_click_impression_simulation",
            title="Set up a traffic segmentation plan",
            url="https://support.google.com/adsense/answer/2583698",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "按渠道或来源分段监控流量，可以帮助发现无效流量和异常来源。"
            ),
        ),
        ResearchSource(
            topic="买量渠道与流量供应商尽调",
            capability=None,
            title="Google Network",
            url="https://support.google.com/google-ads/answer/1752334",
            publisher="Google Ads Help",
            source_type="ad_network_reference",
            reliability="primary",
            claim_summary=(
                "Google Network 包括 Search、Display、Search Partners 等不同库存，"
                "应按网络类型分开测试和对账。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 流量库存、版位与排除控制",
            capability=None,
            title="About content suitability",
            url="https://support.google.com/google-ads/answer/12764663",
            publisher="Google Ads Help",
            source_type="inventory_reference",
            reliability="primary",
            claim_summary=(
                "Content suitability 用于管理广告展示环境、内容类型和品牌安全，"
                "适合作为 Display、YouTube、Demand Gen 和 PMax 库存控制来源。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 流量库存、版位与排除控制",
            capability=None,
            title="Exclude placements at the account level",
            url="https://support.google.com/google-ads/answer/7331110",
            publisher="Google Ads Help",
            source_type="inventory_reference",
            reliability="primary",
            claim_summary=(
                "Account-level placement exclusions 可排除不适合的 websites、apps、"
                "YouTube videos/channels 等位置，支撑低质库存隔离。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 流量库存、版位与排除控制",
            capability=None,
            title="Performance Max channel performance report",
            url="https://support.google.com/google-ads/answer/16260130",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "PMax channel performance report 可按 Search、YouTube、Discover、Gmail 等 "
                "channel 复盘表现，避免把多库存混成平均 ROI。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 流量库存、版位与排除控制",
            capability=None,
            title="Final URL expansion in Performance Max",
            url="https://support.google.com/google-ads/answer/14337539",
            publisher="Google Ads Help",
            source_type="inventory_reference",
            reliability="primary",
            claim_summary=(
                "Final URL expansion 可能把用户送到同域其他页面，"
                "套利团队需要结合 URL exclusions 和页面审计控制风险。"
            ),
        ),
        ResearchSource(
            topic="受众定向、再营销与 Customer Match 合规",
            capability=None,
            title="About audience segments",
            url="https://support.google.com/google-ads/answer/2497941",
            publisher="Google Ads Help",
            source_type="audience_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads audience segments 覆盖 affinity、in-market、custom segments、"
                "your data segments 等受众类型。"
            ),
        ),
        ResearchSource(
            topic="受众定向、再营销与 Customer Match 合规",
            capability=None,
            title='About "Targeting" and "Observation" settings',
            url="https://support.google.com/google-ads/answer/7365594",
            publisher="Google Ads Help",
            source_type="audience_reference",
            reliability="primary",
            claim_summary=(
                "Targeting 会限制广告覆盖，Observation 可在不收窄流量的情况下观察受众表现。"
            ),
        ),
        ResearchSource(
            topic="受众定向、再营销与 Customer Match 合规",
            capability=None,
            title="Customer Match policy",
            url="https://support.google.com/google-ads/answer/6299717",
            publisher="Google Ads Help",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Customer Match 要求客户数据来源、同意、隐私披露和用途满足政策要求，"
                "不适合作为第三方名单上传器。"
            ),
        ),
        ResearchSource(
            topic="受众定向、再营销与 Customer Match 合规",
            capability=None,
            title="About audience signals for Performance Max campaigns",
            url="https://support.google.com/google-ads/answer/14530785",
            publisher="Google Ads Help",
            source_type="audience_reference",
            reliability="primary",
            claim_summary=(
                "Performance Max audience signals 是给自动化投放系统的学习提示，"
                "不是硬性受众定向。"
            ),
        ),
        ResearchSource(
            topic="受众定向、再营销与 Customer Match 合规",
            capability=None,
            title="About optimized targeting",
            url="https://support.google.com/google-ads/answer/10537509",
            publisher="Google Ads Help",
            source_type="audience_reference",
            reliability="primary",
            claim_summary=(
                "Optimized targeting 会在手动选择的信号之外寻找更多可能转化的用户，"
                "套利场景需要把它作为实验变量并用真实收入复盘。"
            ),
        ),
        ResearchSource(
            topic="Affiliate Network / Lead Buyer 尽调",
            capability=None,
            title="The FTC's Endorsement Guides",
            url="https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC Endorsement Guides 支撑 affiliate 推荐、评测、佣金关系和商业利益披露要求。"
            ),
        ),
        ResearchSource(
            topic="Affiliate Network / Lead Buyer 尽调",
            capability=None,
            title="Misrepresentation",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 禁止隐藏或歪曲商业身份、价格、服务和商业关系，"
                "这是 affiliate 页面和 lead 表单的重要红线。"
            ),
        ),
        ResearchSource(
            topic="Affiliate Network / Lead Buyer 尽调",
            capability="invalid_traffic_click_impression_simulation",
            title="Definition of invalid traffic",
            url="https://support.google.com/adsense/answer/16737",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "无效流量包括人为抬高广告主成本或发布商收入的点击、展示和自动工具。"
            ),
        ),
        ResearchSource(
            topic="Lead 质量、Postback 对账与拒付管理",
            capability=None,
            title="Follow the Lead: An FTC Workshop on Lead Generation",
            url="https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC lead generation workshop 用于理解 lead 生态、消费者信息流转、"
                "披露、透明度和消费者保护风险。"
            ),
        ),
        ResearchSource(
            topic="Lead 质量、Postback 对账与拒付管理",
            capability=None,
            title="About lead form assets",
            url="https://support.google.com/google-ads/answer/9423234",
            publisher="Google Ads Help",
            source_type="ad_product_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads lead form assets 说明使用 lead 表单需要满足广告政策、"
                "资格要求和隐私政策链接等要求。"
            ),
        ),
        ResearchSource(
            topic="Lead 质量、Postback 对账与拒付管理",
            capability=None,
            title="Upload offline conversions",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-offline",
            publisher="Google Ads API",
            source_type="official_api",
            reliability="primary",
            claim_summary=(
                "离线转化上传可用于把 lead 后续质量、批准或成交结果回传，"
                "是安全替代 Cookie 后台操作的质量闭环方向。"
            ),
        ),
        ResearchSource(
            topic="Lead 质量、Postback 对账与拒付管理",
            capability=None,
            title="Parameters in Postback URLs",
            url="https://doc.voluum.com/article/parameters-in-postback-urls",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="industry_reference",
            claim_summary=(
                "Postback 参数说明 click_id、payout、transaction_id 等字段如何支撑 "
                "CPA/CPL 归因、状态更新和去重。"
            ),
        ),
        ResearchSource(
            topic="Ping/Post、Lead Buyer Routing 与线索市场治理",
            capability="ping_post_lead_marketplace_buyer_routing",
            title="Follow the Lead: An FTC Workshop on Lead Generation",
            url="https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC lead generation workshop 用于理解 lead marketplace、消费者信息流转、"
                "披露、透明度和消费者保护风险。"
            ),
        ),
        ResearchSource(
            topic="Ping/Post、Lead Buyer Routing 与线索市场治理",
            capability="ping_post_lead_marketplace_buyer_routing",
            title="Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指导用于电话 lead、seller/telemarketer 责任、Do Not Call、"
                "记录保存和消费者保护治理。"
            ),
        ),
        ResearchSource(
            topic="Ping/Post、Lead Buyer Routing 与线索市场治理",
            capability="ping_post_lead_marketplace_buyer_routing",
            title="TCPA one-to-one consent rule court response / deletion order",
            url="https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf",
            publisher="Federal Communications Commission",
            source_type="regulatory_order",
            reliability="primary",
            claim_summary=(
                "FCC 2025 文件用于说明 lead generator one-to-one consent 规则状态"
                "需要按日期、来源和法律意见持续更新。"
            ),
        ),
        ResearchSource(
            topic="Ping/Post、Lead Buyer Routing 与线索市场治理",
            capability="ping_post_lead_marketplace_buyer_routing",
            title="Customer data policies",
            url="https://support.google.com/google-ads/answer/7475709",
            publisher="Google Ads Help",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads customer data policies 支撑用户数据收集、披露、同意、"
                "分享和隐私政策治理。"
            ),
        ),
        ResearchSource(
            topic="Ping/Post、Lead Buyer Routing 与线索市场治理",
            capability="ping_post_lead_marketplace_buyer_routing",
            title="Parameters in Postback URLs",
            url="https://doc.voluum.com/article/parameters-in-postback-urls",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="industry_reference",
            claim_summary=(
                "Postback 参数说明 click_id、transaction_id、payout 和状态字段，"
                "可支撑 ping/post 后的收入归因、状态迁移和去重。"
            ),
        ),
        ResearchSource(
            topic="Ping/Post、Lead Buyer Routing 与线索市场治理",
            capability="ping_post_lead_marketplace_buyer_routing",
            title="Ping Post",
            url="https://docs.pingtree.com/documentation/campaign/distribution/ping-post",
            publisher="PingTree",
            source_type="lead_distribution_reference",
            reliability="industry_reference",
            claim_summary=(
                "PingTree 文档作为行业参考，用于说明 ping/post、lead distribution、"
                "buyer response 和路由工具的通用实现形态。"
            ),
        ),
        ResearchSource(
            topic="Lead Freshness、Aged Lead 与 Recontact Window 治理",
            capability="lead_freshness_aged_recontact_governance",
            title="Follow the Lead: An FTC Workshop on Lead Generation",
            url="https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "FTC lead generation workshop 支撑消费者信息流转、"
                "披露、透明度、投诉和 lead 生命周期治理背景。"
            ),
        ),
        ResearchSource(
            topic="Lead Freshness、Aged Lead 与 Recontact Window 治理",
            capability="lead_freshness_aged_recontact_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指南支撑 recontact、DNC、seller/telemarketer、"
                "consent、记录保存和投诉治理。"
            ),
        ),
        ResearchSource(
            topic="Lead Freshness、Aged Lead 与 Recontact Window 治理",
            capability="lead_freshness_aged_recontact_governance",
            title="FTC, Q&A for Telemarketers & Sellers About DNC",
            url="https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC DNC 问答支撑 entity-specific DNC、opt-out、"
                "suppression 和 recontact 停止条件。"
            ),
        ),
        ResearchSource(
            topic="Lead Freshness、Aged Lead 与 Recontact Window 治理",
            capability="lead_freshness_aged_recontact_governance",
            title="Google Ads Help, Conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag reporting 支撑 lead age、qualified/paid "
                "feedback 和 day-level conversions 不能混作最终价值。"
            ),
        ),
        ResearchSource(
            topic="Lead Freshness、Aged Lead 与 Recontact Window 治理",
            capability="lead_freshness_aged_recontact_governance",
            title="ActiveProspect, TrustedForm",
            url="https://activeprospect.com/products/trustedform/",
            publisher="ActiveProspect",
            source_type="consent_certificate_reference",
            reliability="platform_documentation",
            claim_summary=(
                "TrustedForm 支撑 aged / recontact 争议中的 consent certificate、"
                "页面上下文和证据链治理。"
            ),
        ),
        ResearchSource(
            topic="Lead Freshness、Aged Lead 与 Recontact Window 治理",
            capability="lead_freshness_aged_recontact_governance",
            title="Aged Lead Sales, TCPA compliance for aged leads",
            url="https://agedleadsales.com/blog/tcpa-compliance-calling-aged-leads",
            publisher="Aged Lead Sales",
            source_type="industry_context",
            reliability="industry_reference",
            claim_summary=(
                "Aged lead 文章仅作为行业语境参考，说明 aged leads、"
                "DNC、consent 和投诉风险常被一起治理。"
            ),
        ),
        ResearchSource(
            topic="Lead 验证、Suppression、去重与 PII 治理",
            capability="lead_validation_suppression_pii_governance",
            title="Protecting Personal Information: A Guide for Business",
            url="https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business",
            publisher="Federal Trade Commission",
            source_type="privacy_security_guidance",
            reliability="primary",
            claim_summary=(
                "FTC 指南支撑个人信息最小化、访问控制、保留、删除和安全处理原则，"
                "适合作为 lead PII 治理基础。"
            ),
        ),
        ResearchSource(
            topic="Lead 验证、Suppression、去重与 PII 治理",
            capability="lead_validation_suppression_pii_governance",
            title="Q&A for Telemarketers & Sellers About DNC Provisions in TSR",
            url="https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC DNC 问答支撑 entity-specific do-not-call、opt-out、"
                "suppression 和电话 lead 联系边界治理。"
            ),
        ),
        ResearchSource(
            topic="Lead 验证、Suppression、去重与 PII 治理",
            capability="lead_validation_suppression_pii_governance",
            title="SP 800-122 Guide to Protecting the Confidentiality of PII",
            url="https://csrc.nist.gov/pubs/sp/800/122/final",
            publisher="NIST",
            source_type="privacy_security_standard",
            reliability="primary",
            claim_summary=(
                "NIST SP 800-122 用于 PII 识别、最小化、风险分级、保密性保护"
                "和访问控制设计。"
            ),
        ),
        ResearchSource(
            topic="Lead 验证、Suppression、去重与 PII 治理",
            capability="lead_validation_suppression_pii_governance",
            title="Data Brokers",
            url="https://cppa.ca.gov/data_brokers/",
            publisher="California Privacy Protection Agency",
            source_type="privacy_regulatory_reference",
            reliability="primary",
            claim_summary=(
                "CPPA data brokers 页面用于说明数据经纪人、删除请求、"
                "数据转售和用户权利需要进入 lead sharing 治理。"
            ),
        ),
        ResearchSource(
            topic="Lead 验证、Suppression、去重与 PII 治理",
            capability="lead_validation_suppression_pii_governance",
            title="Data collection and use",
            url="https://support.google.com/adspolicy/answer/6020956",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 数据收集和使用政策支撑 lead 页面披露、用途、"
                "个人信息收集和安全处理要求。"
            ),
        ),
        ResearchSource(
            topic="Lead 验证、Suppression、去重与 PII 治理",
            capability="lead_validation_suppression_pii_governance",
            title="Best practices to avoid sending PII",
            url="https://support.google.com/analytics/answer/6366371",
            publisher="Google Analytics Help",
            source_type="measurement_policy",
            reliability="primary",
            claim_summary=(
                "Google Analytics PII 指南支撑 URL、日志、analytics 字段、"
                "subid 和报表避免发送个人身份信息。"
            ),
        ),
        ResearchSource(
            topic="敏感垂类政策与 Offer 准入",
            capability=None,
            title="Financial products and services",
            url="https://support.google.com/adspolicy/answer/2464998",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "金融、贷款、债务、投资和加密类广告需要符合地区规则、"
                "披露、认证和禁投项，适合作为高 payout Offer 准入依据。"
            ),
        ),
        ResearchSource(
            topic="敏感垂类政策与 Offer 准入",
            capability=None,
            title="Healthcare and medicines",
            url="https://support.google.com/adspolicy/answer/176031",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "医疗、药品、远程医疗和健康服务广告存在认证、地区、"
                "药品类别和健康声明限制，需要在投放前完成资质审计。"
            ),
        ),
        ResearchSource(
            topic="敏感垂类政策与 Offer 准入",
            capability=None,
            title="Personalized advertising",
            url="https://support.google.com/adspolicy/answer/143465",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "个性化广告政策限制基于敏感兴趣、健康、金融困境、身份特征等维度定向，"
                "尤其影响住房、就业、信贷和医疗类 Offer。"
            ),
        ),
        ResearchSource(
            topic="CPL 垂类经济、资格问题与 Buyer Acceptance",
            capability="cpl_vertical_economics_qualification_playbook",
            title="Financial products and services",
            url="https://support.google.com/adspolicy/answer/2464998",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "金融、贷款、债务和相关 lead generation 需要关注地区规则、"
                "认证、披露和禁投项，是金融 CPL 垂类准入依据。"
            ),
        ),
        ResearchSource(
            topic="CPL 垂类经济、资格问题与 Buyer Acceptance",
            capability="cpl_vertical_economics_qualification_playbook",
            title="Local Services Ads platform policies",
            url="https://support.google.com/localservices/answer/6224841",
            publisher="Google Local Services Help",
            source_type="platform_policy",
            reliability="primary",
            claim_summary=(
                "Local Services Ads 平台政策支撑本地服务 lead 的业务筛查、"
                "许可、服务范围、消费者保护和服务商质量语境。"
            ),
        ),
        ResearchSource(
            topic="CPL 垂类经济、资格问题与 Buyer Acceptance",
            capability="cpl_vertical_economics_qualification_playbook",
            title="Follow the Lead: An FTC Workshop on Lead Generation",
            url="https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC lead generation workshop 支撑不同垂类 lead 的消费者信息流转、"
                "披露、透明度和消费者保护风险。"
            ),
        ),
        ResearchSource(
            topic="CPL 垂类经济、资格问题与 Buyer Acceptance",
            capability="cpl_vertical_economics_qualification_playbook",
            title="Digital comparison-shopping circular",
            url="https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/",
            publisher="Consumer Financial Protection Bureau",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "CFPB circular 支撑金融产品比较、推荐排序、补偿驱动导流"
                "和消费者误导风险判断。"
            ),
        ),
        ResearchSource(
            topic="CPL 垂类经济、资格问题与 Buyer Acceptance",
            capability="cpl_vertical_economics_qualification_playbook",
            title="Avoid student loan debt relief scams",
            url="https://studentaid.gov/resources/scams",
            publisher="Federal Student Aid",
            source_type="consumer_protection_reference",
            reliability="primary",
            claim_summary=(
                "Federal Student Aid 资料支撑教育、学生贷款减免、债务 relief"
                "和冒充官方服务的风险判断。"
            ),
        ),
        ResearchSource(
            topic="CPL 垂类经济、资格问题与 Buyer Acceptance",
            capability="cpl_vertical_economics_qualification_playbook",
            title="Model Rule 7.1 Communications Concerning a Lawyer's Services",
            url="https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communications_concerning_a_lawyers_services/",
            publisher="American Bar Association",
            source_type="professional_rule_reference",
            reliability="industry_reference",
            claim_summary=(
                "ABA Model Rule 7.1 作为法律服务广告行业规则参考，"
                "支撑法律 lead 中 false or misleading communication 风险判断。"
            ),
        ),
        ResearchSource(
            topic="实验设计、样本量与优化决策",
            capability=None,
            title="Test with confidence with the Experiments page",
            url="https://support.google.com/google-ads/answer/7281575",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads Experiments 用于以受控方式测试 campaign 变更，"
                "帮助判断优化动作是否真的改善表现。"
            ),
        ),
        ResearchSource(
            topic="实验设计、样本量与优化决策",
            capability=None,
            title="About conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag 会让短期 CPA、ROAS 和收入表现失真，"
                "实验决策需要等待合适观察窗口。"
            ),
        ),
        ResearchSource(
            topic="实验设计、样本量与优化决策",
            capability=None,
            title="GA4 data freshness",
            url="https://support.google.com/analytics/answer/11198161",
            publisher="Google Analytics Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "GA4 数据有处理和刷新延迟，日报和实验复盘需要区分数据新鲜度。"
            ),
        ),
        ResearchSource(
            topic="无效流量识别、异常监控与来源隔离",
            capability="invalid_traffic_click_impression_simulation",
            title="How Google prevents invalid traffic",
            url="https://support.google.com/adsense/answer/1348752",
            publisher="Google AdSense Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "Google 使用自动系统和人工审核过滤无效点击、展示和相关活动，"
                "发布商需要主动管理来源质量。"
            ),
        ),
        ResearchSource(
            topic="无效流量识别、异常监控与来源隔离",
            capability="invalid_traffic_click_impression_simulation",
            title="Managing invalid traffic",
            url="https://support.google.com/google-ads/answer/11182074",
            publisher="Google Ads Help",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 对 invalid clicks 和无效流量进行识别、过滤和管理，"
                "广告主仍应监控异常来源和报表。"
            ),
        ),
        ResearchSource(
            topic="无效流量识别、异常监控与来源隔离",
            capability="invalid_traffic_click_impression_simulation",
            title="Google Ad Traffic Quality",
            url="https://www.google.com/ads/adtrafficquality/how-we-prevent-it/",
            publisher="Google",
            source_type="traffic_quality_policy",
            reliability="primary",
            claim_summary=(
                "Google Ad Traffic Quality 说明 Google 如何检测和防止无效流量，"
                "适合作为异常监控和来源隔离的背景来源。"
            ),
        ),
        ResearchSource(
            topic="内容生产、页面可信度与编辑质量",
            capability=None,
            title="Creating helpful, reliable, people-first content",
            url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content",
            publisher="Google Search Central",
            source_type="content_quality_reference",
            reliability="primary",
            claim_summary=(
                "Google Search Central 建议创建以用户为先、可靠、有帮助的内容，"
                "关注原创价值、信任、作者和来源。"
            ),
        ),
        ResearchSource(
            topic="内容生产、页面可信度与编辑质量",
            capability=None,
            title="Spam policies for Google web search",
            url="https://developers.google.com/search/docs/essentials/spam-policies",
            publisher="Google Search Central",
            source_type="search_policy",
            reliability="primary",
            claim_summary=(
                "Spam policies 覆盖 cloaking、自动生成低质内容、薄 affiliate 页面和滥用规模化内容。"
            ),
        ),
        ResearchSource(
            topic="内容生产、页面可信度与编辑质量",
            capability=None,
            title="Destination requirements",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 目的地要求覆盖页面可达、原创内容、桥页和广告承诺一致性。"
            ),
        ),
        ResearchSource(
            topic="账号健康、政策中心与申诉 SOP",
            capability=None,
            title="Fix a disapproved ad or appeal a policy decision",
            url="https://support.google.com/google-ads/answer/9338593",
            publisher="Google Ads Help",
            source_type="policy_process",
            reliability="primary",
            claim_summary=(
                "Google Ads 支持在修复广告、资产或目标页后对 policy decision 提交申诉。"
            ),
        ),
        ResearchSource(
            topic="账号健康、政策中心与申诉 SOP",
            capability="ban_evasion_account_switching",
            title="Google Ads account suspensions overview",
            url="https://support.google.com/adspolicy/answer/2375414",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "账号暂停后合规路径是理解原因、修复问题并提交申诉；"
                "不能通过创建或切换账号继续同类违规。"
            ),
        ),
        ResearchSource(
            topic="账号健康、政策中心与申诉 SOP",
            capability=None,
            title="Fix policy issues that affect ad serving",
            url="https://support.google.com/adsense/answer/7003627",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "AdSense Policy Center 用于查看影响广告服务的问题，修复后可请求 review。"
            ),
        ),
        ResearchSource(
            topic="AdSense 站点审核、Policy Center 与广告投放限制",
            capability=None,
            title="AdSense connect your site for review",
            url="https://support.google.com/adsense/answer/7584263",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Connect your site 支撑 AdSense code、ads.txt、meta tag 和站点审核前置连接流程。"
            ),
        ),
        ResearchSource(
            topic="AdSense 站点审核、Policy Center 与广告投放限制",
            capability=None,
            title="AdSense add a new site to sites list",
            url="https://support.google.com/adsense/answer/12169212",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Sites list 文档支撑添加站点、检查站点状态和请求 review 的流程。"
            ),
        ),
        ResearchSource(
            topic="AdSense 站点审核、Policy Center 与广告投放限制",
            capability=None,
            title="AdSense site pages ready for approval",
            url="https://support.google.com/adsense/answer/7299563",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "站点 ready 文档支撑内容价值、导航、可访问性和审核准备检查。"
            ),
        ),
        ResearchSource(
            topic="AdSense 站点审核、Policy Center 与广告投放限制",
            capability=None,
            title="AdSense Policy Center overview",
            url="https://support.google.com/adsense/answer/9485926",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Policy Center overview 支撑集中查看政策问题、修复状态和广告服务影响。"
            ),
        ),
        ResearchSource(
            topic="AdSense 站点审核、Policy Center 与广告投放限制",
            capability="invalid_traffic_click_impression_simulation",
            title="AdSense ad serving limits",
            url="https://support.google.com/adsense/answer/9437976",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Ad serving limits 文档支撑账号评估、invalid traffic concerns 和广告服务限制响应。"
            ),
        ),
        ResearchSource(
            topic="AdSense 站点审核、Policy Center 与广告投放限制",
            capability="invalid_traffic_click_impression_simulation",
            title="AdSense traffic segmentation plan",
            url="https://support.google.com/adsense/answer/2583698",
            publisher="Google AdSense Help",
            source_type="traffic_quality_reference",
            reliability="primary",
            claim_summary=(
                "Traffic segmentation plan 支撑按来源隔离流量、排查无效流量和保留恢复证据。"
            ),
        ),
        ResearchSource(
            topic="发布商变现栈",
            capability=None,
            title="AdSense metrics glossary",
            url="https://support.google.com/adsense/answer/2735899",
            publisher="Google AdSense Help",
            source_type="metrics_reference",
            reliability="primary",
            claim_summary=(
                "AdSense 指标词汇表定义 page RPM、impression RPM、coverage、CTR、"
                "Active View 等收入端口径。"
            ),
        ),
        ResearchSource(
            topic="发布商变现栈",
            capability=None,
            title="Set up ads on your site",
            url="https://support.google.com/adsense/answer/7037624",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "AdSense 支持 Auto ads 和手动广告单元，用于在站点上设置广告变现。"
            ),
        ),
        ResearchSource(
            topic="发布商变现栈",
            capability="invalid_traffic_click_impression_simulation",
            title="Google Ad Manager Partner Guidelines",
            url="https://support.google.com/publisherpolicies/answer/9059370",
            publisher="Google Publisher Policies Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Ad Manager 合作伙伴指南覆盖广告行为、流量质量和发布商变现合规要求。"
            ),
        ),
        ResearchSource(
            topic="发布商广告质量、阻止控制与品牌安全",
            capability=None,
            title="AdSense allow and block ads guide",
            url="https://support.google.com/adsense/answer/180609",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Allow/block ads 指南支撑广告阻止控制、广告质量管理和收入影响权衡。"
            ),
        ),
        ResearchSource(
            topic="发布商广告质量、阻止控制与品牌安全",
            capability=None,
            title="AdSense block sensitive categories",
            url="https://support.google.com/adsense/answer/164131",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Sensitive categories 文档支撑按敏感分类进行品牌安全和用户体验控制。"
            ),
        ),
        ResearchSource(
            topic="发布商广告质量、阻止控制与品牌安全",
            capability=None,
            title="AdSense Ad review center",
            url="https://support.google.com/adsense/answer/2469354",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Ad review center 支撑查看、允许、阻止和报告具体广告，处理低质或恶意广告。"
            ),
        ),
        ResearchSource(
            topic="发布商广告质量、阻止控制与品牌安全",
            capability=None,
            title="AdSense blocking controls by site",
            url="https://support.google.com/adsense/answer/12169214",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Blocking controls by site 支撑多站点按站点主题、国家和用户预期设置阻止策略。"
            ),
        ),
        ResearchSource(
            topic="发布商广告质量、阻止控制与品牌安全",
            capability=None,
            title="Google Publisher Restrictions",
            url="https://support.google.com/adsense/answer/10437795",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "Publisher Restrictions 支撑理解某些内容不一定违规但可能降低广告需求。"
            ),
        ),
        ResearchSource(
            topic="发布商广告质量、阻止控制与品牌安全",
            capability=None,
            title="Google Ad Manager Ad review center",
            url="https://admanager.google.com/home/resources/feature-brief-ad-review-center/",
            publisher="Google Ad Manager",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "GAM Ad review center 支撑在 Ad Manager 场景中审查广告创意和需求内容。"
            ),
        ),
        ResearchSource(
            topic="程序化供应链透明度",
            capability=None,
            title="IAB Tech Lab ads.txt for authorized sellers",
            url="https://iabtechlab.com/ads-txt/",
            publisher="IAB Tech Lab",
            source_type="industry_standard",
            reliability="primary",
            claim_summary=(
                "ads.txt 用于发布商声明授权销售库存的广告系统和 seller，"
                "支撑 DIRECT/RESELLER 关系 QA。"
            ),
        ),
        ResearchSource(
            topic="程序化供应链透明度",
            capability=None,
            title="IAB Tech Lab sellers.json",
            url="https://iabtechlab.com/sellers-json/",
            publisher="IAB Tech Lab",
            source_type="industry_standard",
            reliability="primary",
            claim_summary=(
                "sellers.json 让广告系统公开 seller ID、seller type、name 和 domain，"
                "帮助买方验证供应链身份。"
            ),
        ),
        ResearchSource(
            topic="程序化供应链透明度",
            capability=None,
            title="IAB Tech Lab SupplyChain Object",
            url="https://iabtechlab.com/supplychainobject/",
            publisher="IAB Tech Lab",
            source_type="industry_standard",
            reliability="primary",
            claim_summary=(
                "SupplyChain Object 用于在 bid request 中表达供应链节点，"
                "支持 schain 完整性和 reseller 链路复盘。"
            ),
        ),
        ResearchSource(
            topic="程序化供应链透明度",
            capability=None,
            title="AdSense authorize sellers with ads.txt",
            url="https://support.google.com/adsense/answer/7532444",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "AdSense ads.txt 指南支撑发布商在站点上授权卖方，"
                "避免未授权库存销售影响收入。"
            ),
        ),
        ResearchSource(
            topic="程序化供应链透明度",
            capability=None,
            title="Google Ad Manager manage ads.txt files",
            url="https://support.google.com/admanager/answer/7441288",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "GAM ads.txt 管理文档支撑在 Ad Manager 场景中检查授权 seller 和可售库存。"
            ),
        ),
        ResearchSource(
            topic="程序化供应链透明度",
            capability=None,
            title="Google Ad Manager MCM manage inventory",
            url="https://support.google.com/admanager/answer/11103843",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "MCM manage inventory 支撑 parent/child publisher 和库存管理关系解释，"
                "用于识别 MCM、ads.txt 和 seller 关系是否一致。"
            ),
        ),
        ResearchSource(
            topic="GAM / AdX Yield、Floor Price 与 Pricing Rules",
            capability=None,
            title="Google Ad Manager unified pricing rules for yield QA",
            url="https://support.google.com/admanager/answer/9298008",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Unified pricing rules 支撑按库存、地域、设备和需求类型设置定价规则，"
                "用于 floor price 实验、影响范围和回滚点 QA。"
            ),
        ),
        ResearchSource(
            topic="GAM / AdX Yield、Floor Price 与 Pricing Rules",
            capability=None,
            title="Google Ad Manager dynamic allocation",
            url="https://support.google.com/admanager/answer/1143651",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Dynamic allocation 解释 GAM 中保留库存、AdX 和其他需求的竞争分配逻辑，"
                "用于诊断 line item、fill 和程序化收入变化。"
            ),
        ),
        ResearchSource(
            topic="GAM / AdX Yield、Floor Price 与 Pricing Rules",
            capability=None,
            title="Google Ad Manager line item types and priorities",
            url="https://support.google.com/admanager/answer/177279",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Line item 类型和优先级支撑 sponsorship、standard、price priority、house 等"
                "投放类型的 delivery、保量和 yield 冲突复盘。"
            ),
        ),
        ResearchSource(
            topic="GAM / AdX Yield、Floor Price 与 Pricing Rules",
            capability=None,
            title="Google Ad Manager Open Bidding",
            url="https://support.google.com/admanager/answer/7128453",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Open Bidding 支撑第三方 exchange 与 Google demand 在 GAM 中竞争，"
                "用于评估需求增量、对账复杂度和 partner 风险。"
            ),
        ),
        ResearchSource(
            topic="GAM / AdX Yield、Floor Price 与 Pricing Rules",
            capability=None,
            title="Google Ad Manager yield groups",
            url="https://support.google.com/admanager/answer/7386124",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Yield groups 支撑把多个 yield partner 组织到同一复盘口径，"
                "用于按 partner、ad unit、country 和 device 分层分析。"
            ),
        ),
        ResearchSource(
            topic="GAM / AdX Yield、Floor Price 与 Pricing Rules",
            capability=None,
            title="Google Ad Manager forecasting for line items",
            url="https://support.google.com/admanager/answer/2917835",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Forecasting 支撑检查 line item delivery 和库存可用性，"
                "避免 floor 或程序化配置误伤保量投放。"
            ),
        ),
        ResearchSource(
            topic="Header Bidding / Prebid.js 与广告栈延迟",
            capability=None,
            title="Prebid.js overview for header bidding stack QA",
            url="https://docs.prebid.org/prebid/prebidjs.html",
            publisher="Prebid.org",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Prebid.js 概览支撑页面端 header bidding、bidder、auction 和 ad server "
                "协作的基础解释。"
            ),
        ),
        ResearchSource(
            topic="Header Bidding / Prebid.js 与广告栈延迟",
            capability=None,
            title="Prebid Ad Ops step-by-step for GAM line items",
            url="https://docs.prebid.org/adops/step-by-step.html",
            publisher="Prebid.org",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Prebid Ad Ops 指南支撑 GAM line item、creative、key-value 和价格桶"
                "配置一致性 QA。"
            ),
        ),
        ResearchSource(
            topic="Header Bidding / Prebid.js 与广告栈延迟",
            capability=None,
            title="Prebid price granularity for line item planning",
            url="https://docs.prebid.org/adops/price-granularity.html",
            publisher="Prebid.org",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Price granularity 支撑 price bucket 粒度、GAM line item 数量和 yield "
                "精度之间的权衡。"
            ),
        ),
        ResearchSource(
            topic="Header Bidding / Prebid.js 与广告栈延迟",
            capability=None,
            title="Prebid Consent Management TCF module",
            url="https://docs.prebid.org/dev-docs/modules/consentManagementTcf.html",
            publisher="Prebid.org",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Consent Management TCF module 支撑 CMP、TCF、consent 状态和 bidder "
                "参与边界复盘。"
            ),
        ),
        ResearchSource(
            topic="Header Bidding / Prebid.js 与广告栈延迟",
            capability=None,
            title="Prebid Supply Chain Object module",
            url="https://docs.prebid.org/dev-docs/modules/schain.html",
            publisher="Prebid.org",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "Supply Chain Object module 支撑 Header Bidding 中 schain 传递、seller "
                "链路和供应链透明度 QA。"
            ),
        ),
        ResearchSource(
            topic="Header Bidding / Prebid.js 与广告栈延迟",
            capability=None,
            title="Google Ad Manager key-values for header bidding targeting",
            url="https://support.google.com/admanager/answer/177381",
            publisher="Google Ad Manager Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "GAM key-values 支撑 hb_pb、hb_bidder、slot 等 targeting 传递和 line item "
                "匹配诊断。"
            ),
        ),
        ResearchSource(
            topic="广告位、刷新、可见率与页面体验",
            capability=None,
            title="AdSense ad placement policies for layout QA",
            url="https://support.google.com/adsense/answer/1346295",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "AdSense 广告位政策支撑广告不能伪装成内容、不能诱导点击，"
                "广告位实验必须避免误点和改变广告行为。"
            ),
        ),
        ResearchSource(
            topic="广告位、刷新、可见率与页面体验",
            capability=None,
            title="AdSense best practices for ad placement",
            url="https://support.google.com/adsense/answer/1282097",
            publisher="Google AdSense Help",
            source_type="publisher_reference",
            reliability="primary",
            claim_summary=(
                "AdSense 广告位最佳实践支撑内容应易找、广告应可识别，"
                "广告数量和位置不能压过页面任务。"
            ),
        ),
        ResearchSource(
            topic="广告位、刷新、可见率与页面体验",
            capability=None,
            title="Declare ad refresh inventory",
            url="https://support.google.com/admanager/answer/6286179",
            publisher="Google Ad Manager Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "GAM 要求声明刷新库存，套利复盘需要把普通展示和 refresh 展示拆开看。"
            ),
        ),
        ResearchSource(
            topic="广告位、刷新、可见率与页面体验",
            capability=None,
            title="Google Publisher Tag control ad loading and refresh",
            url="https://developers.google.com/publisher-tag/guides/control-ad-loading",
            publisher="Google for Developers",
            source_type="technical_reference",
            reliability="primary",
            claim_summary=(
                "GPT 文档说明广告加载和刷新控制的技术语境；本项目只记录策略和审计，"
                "不生成刷新代码。"
            ),
        ),
        ResearchSource(
            topic="广告位、刷新、可见率与页面体验",
            capability=None,
            title="Cumulative Layout Shift",
            url="https://web.dev/articles/cls",
            publisher="web.dev",
            source_type="page_experience_reference",
            reliability="primary",
            claim_summary=(
                "CLS 支撑广告容器预留尺寸、动态插入广告和页面布局稳定性的 QA。"
            ),
        ),
        ResearchSource(
            topic="广告位、刷新、可见率与页面体验",
            capability=None,
            title="Better Ads Standards for ad layout QA",
            url="https://www.betterads.org/standards/",
            publisher="Coalition for Better Ads",
            source_type="industry_standard",
            reliability="industry_reference",
            claim_summary=(
                "Better Ads Standards 支撑弹窗、插屏、sticky、自动播放和广告密度等体验红线。"
            ),
        ),
        ResearchSource(
            topic="隐私、Consent 与追踪合规",
            capability=None,
            title="Consent mode overview",
            url="https://developers.google.com/tag-platform/security/concepts/consent-mode",
            publisher="Google for Developers",
            source_type="privacy_reference",
            reliability="primary",
            claim_summary=(
                "Consent Mode 让 Google tags 根据用户同意状态调整广告和分析存储、"
                "广告用户数据和个性化广告行为。"
            ),
        ),
        ResearchSource(
            topic="隐私、Consent 与追踪合规",
            capability=None,
            title="Google consent management requirements for publishers",
            url="https://support.google.com/adsense/answer/13554116",
            publisher="Google AdSense Help",
            source_type="publisher_policy",
            reliability="primary",
            claim_summary=(
                "AdSense 发布商面向 EEA、UK、Switzerland 用户时需要使用符合 Google 要求的 CMP。"
            ),
        ),
        ResearchSource(
            topic="隐私、Consent 与追踪合规",
            capability=None,
            title="Customer data policies",
            url="https://support.google.com/google-ads/answer/7475709",
            publisher="Google Ads Help",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 对使用 customer data、enhanced conversions 和用户提供数据有政策要求。"
            ),
        ),
        ResearchSource(
            topic="Lead Form、电话线索、Call Tracking 与 TCPA",
            capability=None,
            title="Google Ads, About lead form assets for lead compliance",
            url="https://support.google.com/google-ads/answer/9423234",
            publisher="Google Ads Help",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Lead form assets 支撑原生表单、隐私政策、字段收集和线索交接的合规 QA。"
            ),
        ),
        ResearchSource(
            topic="Lead Form、电话线索、Call Tracking 与 TCPA",
            capability=None,
            title="Google Ads, About call reporting for qualified calls",
            url="https://support.google.com/google-ads/answer/2454052",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Call reporting 支撑 Google forwarding numbers、通话指标、call duration threshold "
                "和电话转化复盘。"
            ),
        ),
        ResearchSource(
            topic="Lead Form、电话线索、Call Tracking 与 TCPA",
            capability=None,
            title="Google Ads, Customer data policies for lead data",
            url="https://support.google.com/google-ads/answer/7475709",
            publisher="Google Ads Help",
            source_type="privacy_policy",
            reliability="primary",
            claim_summary=(
                "Customer data policy 支撑用户提供数据、consent、隐私披露和 buyer handoff 边界。"
            ),
        ),
        ResearchSource(
            topic="Lead Form、电话线索、Call Tracking 与 TCPA",
            capability=None,
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="legal_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指南支撑 telemarketing、seller、DNC、consent、记录保存和投诉治理。"
            ),
        ),
        ResearchSource(
            topic="Lead Form、电话线索、Call Tracking 与 TCPA",
            capability=None,
            title="FCC, TCPA one-to-one consent rule deletion order",
            url="https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf",
            publisher="Federal Communications Commission",
            source_type="legal_update",
            reliability="primary",
            claim_summary=(
                "FCC 文件支撑 2025 年 one-to-one consent 规则状态变化，系统需记录来源日期并跟进最新规则。"
            ),
        ),
        ResearchSource(
            topic="Lead Form、电话线索、Call Tracking 与 TCPA",
            capability=None,
            title="eCFR, 47 CFR 64.1200 delivery restrictions",
            url="https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200",
            publisher="eCFR",
            source_type="regulation_text",
            reliability="primary",
            claim_summary=(
                "47 CFR 64.1200 支撑电话、自动拨号、预录音、短信和 prior express consent 的规则文本。"
            ),
        ),
        ResearchSource(
            topic="Call Tracking Number Pool、DNI 与电话归因治理",
            capability="call_tracking_dni_number_pool_attribution_governance",
            title="Google Ads Help, About call reporting",
            url="https://support.google.com/google-ads/answer/2454052",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Call reporting 支撑 Google forwarding numbers、通话指标、"
                "来电时间、call duration 和电话转化诊断。"
            ),
        ),
        ResearchSource(
            topic="Call Tracking Number Pool、DNI 与电话归因治理",
            capability="call_tracking_dni_number_pool_attribution_governance",
            title="Google Ads Help, Phone call conversion tracking",
            url="https://support.google.com/google-ads/answer/6100664",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Phone call conversion tracking 支撑 duration threshold、"
                "qualified call 和 call conversion action 口径。"
            ),
        ),
        ResearchSource(
            topic="Call Tracking Number Pool、DNI 与电话归因治理",
            capability="call_tracking_dni_number_pool_attribution_governance",
            title="Google Ads API, call_view fields",
            url="https://developers.google.com/google-ads/api/fields/v18/call_view",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "call_view fields 支撑 call detail 报表字段、"
                "call start、duration、status 和归因对账。"
            ),
        ),
        ResearchSource(
            topic="Call Tracking Number Pool、DNI 与电话归因治理",
            capability="call_tracking_dni_number_pool_attribution_governance",
            title="CallRail Help, Dynamic number insertion overview",
            url="https://support.callrail.com/hc/en-us/articles/5711814948877-Dynamic-number-insertion-overview",
            publisher="CallRail",
            source_type="call_tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "DNI overview 支撑 tracking number、号码替换、"
                "会话来源和电话归因的行业实现语境。"
            ),
        ),
        ResearchSource(
            topic="Call Tracking Number Pool、DNI 与电话归因治理",
            capability="call_tracking_dni_number_pool_attribution_governance",
            title="CallRail Help, Create a website pool",
            url="https://support.callrail.com/hc/en-us/articles/5711655270029-Create-a-website-pool",
            publisher="CallRail",
            source_type="call_tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Website pool 支撑号码池、pool size、swap rule、"
                "session attribution 和容量 QA。"
            ),
        ),
        ResearchSource(
            topic="Call Tracking Number Pool、DNI 与电话归因治理",
            capability="call_tracking_dni_number_pool_attribution_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指南支撑电话 lead、seller/telemarketer、DNC、"
                "consent、记录保存和投诉治理。"
            ),
        ),
        ResearchSource(
            topic="Pay-per-call、Call Buyer Routing 与 Duration Payout 治理",
            capability="pay_per_call_buyer_routing_duration_payout_governance",
            title="Google Ads Help, Phone call conversion tracking",
            url="https://support.google.com/google-ads/answer/6100664",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Phone call conversion tracking 支撑 duration threshold、"
                "call conversion 和 qualified call 口径。"
            ),
        ),
        ResearchSource(
            topic="Pay-per-call、Call Buyer Routing 与 Duration Payout 治理",
            capability="pay_per_call_buyer_routing_duration_payout_governance",
            title="Google Ads API, call_view fields",
            url="https://developers.google.com/google-ads/api/fields/v18/call_view",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "call_view fields 支撑 call detail、call start、duration、"
                "status 和电话对账。"
            ),
        ),
        ResearchSource(
            topic="Pay-per-call、Call Buyer Routing 与 Duration Payout 治理",
            capability="pay_per_call_buyer_routing_duration_payout_governance",
            title="Ringba Support, Call Flows with Ringba",
            url="https://support.ringba.com/hc/en-us/articles/17989801271703-Call-Flows-with-Ringba",
            publisher="Ringba",
            source_type="pay_per_call_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Ringba call flows 支撑 IVR、routing node、target "
                "和 pay-per-call call flow 行业语境。"
            ),
        ),
        ResearchSource(
            topic="Pay-per-call、Call Buyer Routing 与 Duration Payout 治理",
            capability="pay_per_call_buyer_routing_duration_payout_governance",
            title="Ringba Support, Targets",
            url="https://support.ringba.com/hc/en-us/articles/17882949857943-Targets-Video",
            publisher="Ringba",
            source_type="pay_per_call_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Ringba targets 支撑 call buyer endpoint、target、"
                "转接目的地和 routing QA。"
            ),
        ),
        ResearchSource(
            topic="Pay-per-call、Call Buyer Routing 与 Duration Payout 治理",
            capability="pay_per_call_buyer_routing_duration_payout_governance",
            title="Retreaver, Pay Per Call Campaign Roadmap",
            url="https://retreaver.com/call-tracking/pay-per-call",
            publisher="Retreaver",
            source_type="pay_per_call_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Retreaver pay-per-call roadmap 支撑 buyer、publisher、"
                "campaign、routing 和 performance marketing 电话业务语境。"
            ),
        ),
        ResearchSource(
            topic="Pay-per-call、Call Buyer Routing 与 Duration Payout 治理",
            capability="pay_per_call_buyer_routing_duration_payout_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指南支撑电话营销、seller/telemarketer、DNC、"
                "consent、记录保存和投诉治理。"
            ),
        ),
        ResearchSource(
            topic="Lead Consent Proof、TrustedForm / Jornaya 与证据链治理",
            capability="lead_consent_proof_certificate_evidence_governance",
            title="ActiveProspect, TrustedForm",
            url="https://activeprospect.com/products/trustedform/",
            publisher="ActiveProspect",
            source_type="consent_certificate_reference",
            reliability="platform_documentation",
            claim_summary=(
                "TrustedForm 支撑 consent certificate、lead proof、"
                "页面上下文和第三方证据链治理。"
            ),
        ),
        ResearchSource(
            topic="Lead Consent Proof、TrustedForm / Jornaya 与证据链治理",
            capability="lead_consent_proof_certificate_evidence_governance",
            title="ActiveProspect, Jornaya TCPA Guardian LeadConduit integration",
            url="https://activeprospect.com/leadconduit/integrations/jornaya/tcpa_guardian/",
            publisher="ActiveProspect",
            source_type="lead_integration_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Jornaya TCPA Guardian integration 支撑 LeadID / TCPA Guardian "
                "类证据、buyer workflow 和数据交接语境。"
            ),
        ),
        ResearchSource(
            topic="Lead Consent Proof、TrustedForm / Jornaya 与证据链治理",
            capability="lead_consent_proof_certificate_evidence_governance",
            title="Google Ads Policy, Data collection and use",
            url="https://support.google.com/adspolicy/answer/6020956",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Data collection and use 支撑 lead 页面收集个人信息时的"
                "披露、用途、隐私和安全处理要求。"
            ),
        ),
        ResearchSource(
            topic="Lead Consent Proof、TrustedForm / Jornaya 与证据链治理",
            capability="lead_consent_proof_certificate_evidence_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指南支撑 seller/telemarketer、DNC、consent、"
                "记录保存和投诉治理。"
            ),
        ),
        ResearchSource(
            topic="Lead Consent Proof、TrustedForm / Jornaya 与证据链治理",
            capability="lead_consent_proof_certificate_evidence_governance",
            title="eCFR, 47 CFR 64.1200 delivery restrictions",
            url="https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200",
            publisher="eCFR",
            source_type="regulation_text",
            reliability="primary",
            claim_summary=(
                "47 CFR 64.1200 支撑电话、短信、自动拨号、预录音和"
                "prior express consent 的规则文本。"
            ),
        ),
        ResearchSource(
            topic="Lead Consent Proof、TrustedForm / Jornaya 与证据链治理",
            capability="lead_consent_proof_certificate_evidence_governance",
            title="FTC, Protecting Personal Information",
            url="https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business",
            publisher="Federal Trade Commission",
            source_type="privacy_security_guidance",
            reliability="primary",
            claim_summary=(
                "FTC PII 指南支撑 consent evidence、certificate 引用、"
                "页面快照和 lead 数据的最小化、访问控制和保留。"
            ),
        ),
        ResearchSource(
            topic="Lead Form 漏斗、资格问题与移动端 UX 治理",
            capability="lead_form_funnel_qualification_ux",
            title="About lead form assets",
            url="https://support.google.com/google-ads/answer/9423234",
            publisher="Google Ads Help",
            source_type="ad_product_reference",
            reliability="primary",
            claim_summary=(
                "Lead form assets 支撑 Google Ads 原生表单、资格、隐私政策、"
                "字段收集和广告政策要求。"
            ),
        ),
        ResearchSource(
            topic="Lead Form 漏斗、资格问题与移动端 UX 治理",
            capability="lead_form_funnel_qualification_ux",
            title="Data collection and use",
            url="https://support.google.com/adspolicy/answer/6020956",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Data collection and use 支撑表单个人信息收集、披露、"
                "用途说明和安全处理要求。"
            ),
        ),
        ResearchSource(
            topic="Lead Form 漏斗、资格问题与移动端 UX 治理",
            capability="lead_form_funnel_qualification_ux",
            title=".com Disclosures",
            url="https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC .com Disclosures 支撑披露需要清楚、明显，并靠近相关 claim、"
                "CTA 或用户提交动作。"
            ),
        ),
        ResearchSource(
            topic="Lead Form 漏斗、资格问题与移动端 UX 治理",
            capability="lead_form_funnel_qualification_ux",
            title="Protecting Personal Information",
            url="https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business",
            publisher="Federal Trade Commission",
            source_type="privacy_guidance",
            reliability="primary",
            claim_summary=(
                "FTC PII 保护指南支撑字段最小化、访问控制、保留、删除和"
                "表单数据安全治理。"
            ),
        ),
        ResearchSource(
            topic="Lead Form 漏斗、资格问题与移动端 UX 治理",
            capability="lead_form_funnel_qualification_ux",
            title="Learn Forms",
            url="https://web.dev/learn/forms",
            publisher="web.dev",
            source_type="ux_reference",
            reliability="primary",
            claim_summary=(
                "web.dev Forms 支撑表单结构、label、输入类型、移动端填写和"
                "错误提示的 UX 基础。"
            ),
        ),
        ResearchSource(
            topic="Lead Form 漏斗、资格问题与移动端 UX 治理",
            capability="lead_form_funnel_qualification_ux",
            title="Forms Tutorial",
            url="https://www.w3.org/WAI/tutorials/forms/",
            publisher="W3C WAI",
            source_type="accessibility_reference",
            reliability="primary",
            claim_summary=(
                "WAI Forms Tutorial 支撑可访问表单中的 label、说明、错误提示、"
                "分组和焦点治理。"
            ),
        ),
        ResearchSource(
            topic="Speed-to-Lead、联系策略、坐席容量与 SLA 治理",
            capability="speed_to_lead_contact_sla_governance",
            title="About call reporting",
            url="https://support.google.com/google-ads/answer/2454052",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Call reporting 支撑 Google forwarding numbers、通话指标、来电时间、"
                "call duration 和电话转化诊断。"
            ),
        ),
        ResearchSource(
            topic="Speed-to-Lead、联系策略、坐席容量与 SLA 治理",
            capability="speed_to_lead_contact_sla_governance",
            title="About call assets",
            url="https://support.google.com/google-ads/answer/2453991",
            publisher="Google Ads Help",
            source_type="ad_product_reference",
            reliability="primary",
            claim_summary=(
                "Call assets 支撑电话入口、call-heavy campaign 和电话资产治理。"
            ),
        ),
        ResearchSource(
            topic="Speed-to-Lead、联系策略、坐席容量与 SLA 治理",
            capability="speed_to_lead_contact_sla_governance",
            title="How lead costs and credits work in Local Services Ads",
            url="https://support.google.com/localservices/answer/7436333",
            publisher="Google Local Services Help",
            source_type="local_services_reference",
            reliability="primary",
            claim_summary=(
                "Local Services lead costs and credits 支撑 charged lead、wrong service/area、"
                "credit 和本地服务 lead quality 语境。"
            ),
        ),
        ResearchSource(
            topic="Speed-to-Lead、联系策略、坐席容量与 SLA 治理",
            capability="speed_to_lead_contact_sla_governance",
            title="About ad scheduling",
            url="https://support.google.com/google-ads/answer/2404244",
            publisher="Google Ads Help",
            source_type="campaign_control_reference",
            reliability="primary",
            claim_summary=(
                "Ad scheduling 支撑按营业时间、坐席容量和时区设置广告投放时段。"
            ),
        ),
        ResearchSource(
            topic="Speed-to-Lead、联系策略、坐席容量与 SLA 治理",
            capability="speed_to_lead_contact_sla_governance",
            title="Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指南支撑 telemarketing、seller/telemarketer、DNC、consent、"
                "记录和投诉治理。"
            ),
        ),
        ResearchSource(
            topic="Speed-to-Lead、联系策略、坐席容量与 SLA 治理",
            capability="speed_to_lead_contact_sla_governance",
            title="47 CFR 64.1200 Delivery restrictions",
            url="https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200",
            publisher="eCFR",
            source_type="regulation_text",
            reliability="primary",
            claim_summary=(
                "47 CFR 64.1200 支撑电话、短信、自动拨号、预录音和 consent "
                "相关规则文本。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="Cover Your Tracks",
            url="https://coveryourtracks.eff.org/learn",
            publisher="Electronic Frontier Foundation",
            source_type="privacy_research",
            reliability="primary",
            claim_summary=(
                "浏览器指纹由时区、设置、软件版本、屏幕、字体等多种特征组合而成，"
                "可以用于跨站识别。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="Cloudflare Workers overview",
            url="https://developers.cloudflare.com/workers/",
            publisher="Cloudflare",
            source_type="technical_reference",
            reliability="primary",
            claim_summary=(
                "Workers 是运行在 Cloudflare 全球网络上的 serverless 平台，可用于构建 API、后台任务和边缘逻辑。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="W3C TAG, Unsanctioned Web Tracking",
            url="https://www.w3.org/2001/tag/doc/unsanctioned-tracking/",
            publisher="W3C Technical Architecture Group",
            source_type="privacy_reference",
            reliability="primary",
            claim_summary=(
                "Unsanctioned Web Tracking 支撑指纹、非授权追踪 "
                "和跨上下文识别的隐私与治理风险。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="Google Ads Policy, Circumventing systems",
            url="https://support.google.com/adspolicy/answer/15938075",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Circumventing systems policy 支撑隐藏真实目的地、规避政策执行、"
                "向 Google 和用户展示不同内容等红线。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="Google Ads Policy, Advertising network abuse",
            url="https://support.google.com/adspolicy/answer/6008942",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Advertising network abuse policy 支撑桥页、网关页、"
                "低价值目的地和隐藏链路风险判断。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="Google Ads Policy, Destination requirements",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Destination requirements 支撑最终 URL、页面可达、"
                "目的地体验和广告承诺一致性要求。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="Google Ads Help, About access levels in your Google Ads account",
            url="https://support.google.com/google-ads/answer/9978556",
            publisher="Google Ads Help",
            source_type="access_control",
            reliability="primary",
            claim_summary=(
                "Access levels 支撑通过用户权限、MCC 和审计协作，"
                "而不是共享环境或隐藏操作者。"
            ),
        ),
        ResearchSource(
            topic="代理、指纹、Worker 转发规避关联检测",
            capability="proxy_fingerprint_worker_association_evasion",
            title="Google Ads Help, Fix a suspended Google Ads account",
            url="https://support.google.com/google-ads/answer/2375414",
            publisher="Google Ads Help",
            source_type="account_health_policy",
            reliability="primary",
            claim_summary=(
                "Suspended account guidance 支撑受限后应修复问题和申诉，"
                "而不是切换代理、指纹、Worker 或账号继续投放。"
            ),
        ),
        ResearchSource(
            topic="Cloaking 或审核页/用户页不一致",
            capability="cloaking_review_user_page_mismatch",
            title="Circumventing systems",
            url="https://support.google.com/adspolicy/answer/15938075",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 将向 Google 和用户展示不同内容、隐藏真实目的地、"
                "通过多账号规避政策执行列为 Circumventing systems 问题。"
            ),
        ),
        ResearchSource(
            topic="Cloaking 或审核页/用户页不一致",
            capability="cloaking_review_user_page_mismatch",
            title="Spam policies for Google web search",
            url="https://developers.google.com/search/docs/essentials/spam-policies",
            publisher="Google Search Central",
            source_type="search_policy",
            reliability="primary",
            claim_summary=(
                "Google Search 将 cloaking 定义为为了操纵搜索排名和误导用户而向用户和搜索引擎展示不同内容。"
            ),
        ),
        ResearchSource(
            topic="Cloaking 或审核页/用户页不一致",
            capability="cloaking_review_user_page_mismatch",
            title="Google Ads Policy, Destination requirements",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Destination requirements 支撑 Final URL、目的地可达、"
                "页面体验和广告承诺一致性。"
            ),
        ),
        ResearchSource(
            topic="Cloaking 或审核页/用户页不一致",
            capability="cloaking_review_user_page_mismatch",
            title="Google Ads Policy, Advertising network abuse",
            url="https://support.google.com/adspolicy/answer/6008942",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Advertising network abuse 支撑 cloaking、bridge/gateway "
                "destinations、低价值目的地和广告网络滥用风险。"
            ),
        ),
        ResearchSource(
            topic="Cloaking 或审核页/用户页不一致",
            capability="cloaking_review_user_page_mismatch",
            title="Google Ads Scripts, Link Checker solution",
            url="https://developers.google.com/google-ads/scripts/docs/solutions/link-checker",
            publisher="Google Ads Scripts Documentation",
            source_type="official_script_documentation",
            reliability="primary",
            claim_summary=(
                "Link Checker solution 支撑链接检查应是 QA 和提醒，"
                "不是分流、隐藏目的地或审核绕过。"
            ),
        ),
        ResearchSource(
            topic="Cloaking 或审核页/用户页不一致",
            capability="cloaking_review_user_page_mismatch",
            title="Google Ads Help, Set up tracking with ValueTrack parameters",
            url="https://support.google.com/google-ads/answer/6305348",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "ValueTrack guidance 支撑 tracking 参数用于归因和报表，"
                "不应改变用户最终业务目的。"
            ),
        ),
        ResearchSource(
            topic="Cloaking 或审核页/用户页不一致",
            capability="cloaking_review_user_page_mismatch",
            title="Google Ads Help, About tracking in Google Ads",
            url="https://support.google.com/google-ads/answer/6076199",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Tracking in Google Ads 支撑 Final URL、tracking template "
                "和 URL options 的追踪边界。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Circumventing systems: Multiple account abuse",
            url="https://support.google.com/adspolicy/answer/15938075",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Google Ads 明确不允许因账号被暂停而创建更多账号继续违反政策，"
                "并建议通过申诉流程解决暂停问题。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Google Ads account suspensions overview",
            url="https://support.google.com/google-ads/answer/9841640",
            publisher="Google Ads Help",
            source_type="account_health_policy",
            reliability="primary",
            claim_summary=(
                "Account suspensions overview 支撑暂停原因、关联账号或新账号风险、"
                "申诉、验证和 read-only 状态说明。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Google Ads Policy, Advertising network abuse",
            url="https://support.google.com/adspolicy/answer/6008942",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Advertising network abuse 支撑桥页、cloaking、arbitrage、"
                "低价值目的地和广告网络滥用风险。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Google Ads Help, About access levels in your Google Ads account",
            url="https://support.google.com/google-ads/answer/9978556",
            publisher="Google Ads Help",
            source_type="access_control",
            reliability="primary",
            claim_summary=(
                "Access levels 支撑用访问级别和权限治理多账号协作，"
                "而不是共享或切换账号规避。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Google Ads Help, Manager account access levels",
            url="https://support.google.com/google-ads/answer/9977851",
            publisher="Google Ads Help",
            source_type="access_control",
            reliability="primary",
            claim_summary=(
                "Manager account access levels 支撑 MCC、代理关系、"
                "ownership 和用户权限边界。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Google Ads Help, Secure your Google Ads account",
            url="https://support.google.com/google-ads/answer/2375456",
            publisher="Google Ads Help",
            source_type="security_policy",
            reliability="primary",
            claim_summary=(
                "Account security guidance 支撑未授权活动、安全设置、"
                "访问审计和账号保护。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Google Ads Advertiser verification document requirements",
            url="https://support.google.com/adspolicy/answer/9872280",
            publisher="Google Ads Policy Help",
            source_type="verification_policy",
            reliability="primary",
            claim_summary=(
                "Advertiser verification document requirements 支撑真实身份、"
                "业务资料和验证证据治理。"
            ),
        ),
        ResearchSource(
            topic="为规避封禁创建或切换账号",
            capability="ban_evasion_account_switching",
            title="Google Ads API, Advertiser identity verification",
            url="https://developers.google.com/google-ads/api/docs/account-management/advertiser-identity-verification",
            publisher="Google Ads API Documentation",
            source_type="official_api_documentation",
            reliability="primary",
            claim_summary=(
                "Advertiser identity verification API 文档支撑 verification "
                "program 是官方账号治理对象，不是换主体绕过。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Editor CSV 与 Bulk Upload 批量变更治理",
            capability="editor_csv_bulk_upload_governance",
            title="Google Ads Editor, Prepare a CSV file",
            url="https://support.google.com/google-ads/editor/answer/56368",
            publisher="Google Ads Editor Help",
            source_type="editor_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads Editor CSV 文档支撑离线准备和批量导入字段合同，"
                "适合作为 Cookie 后台批量操作的安全替代。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Editor CSV 与 Bulk Upload 批量变更治理",
            capability="editor_csv_bulk_upload_governance",
            title="Google Ads Editor, Check changes before posting",
            url="https://support.google.com/google-ads/editor/answer/56370",
            publisher="Google Ads Editor Help",
            source_type="editor_reference",
            reliability="primary",
            claim_summary=(
                "Editor 发布前检查支撑先发现错误、再由授权人员发布，"
                "不能把 CSV 导出直接等同于自动投放。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Editor CSV 与 Bulk Upload 批量变更治理",
            capability="editor_csv_bulk_upload_governance",
            title="Google Ads Editor, Post changes",
            url="https://support.google.com/google-ads/editor/answer/30583",
            publisher="Google Ads Editor Help",
            source_type="editor_reference",
            reliability="primary",
            claim_summary=(
                "Post changes 文档支撑最终发布动作发生在授权 Editor 流程内，"
                "系统只准备草稿、版本和审计证据。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Editor CSV 与 Bulk Upload 批量变更治理",
            capability="editor_csv_bulk_upload_governance",
            title="Google Ads Help, Bulk uploads",
            url="https://support.google.com/google-ads/answer/10702433",
            publisher="Google Ads Help",
            source_type="bulk_upload_reference",
            reliability="primary",
            claim_summary=(
                "Bulk uploads 支撑批量上传、预览、执行和结果治理，"
                "需要保留批次、错误和 Change history。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Editor CSV 与 Bulk Upload 批量变更治理",
            capability="editor_csv_bulk_upload_governance",
            title="Google Ads API, Partial failures for bulk changes",
            url="https://developers.google.com/google-ads/api/docs/best-practices/partial-failures",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Partial failure 文档支撑批量变更必须保存行级错误，"
                "不能只记录整体成功或失败。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Editor CSV 与 Bulk Upload 批量变更治理",
            capability="editor_csv_bulk_upload_governance",
            title="Google Ads policy, Destination requirements",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Destination requirements 支撑 Final URL、页面可达、广告承诺一致性和目的地质量检查，"
                "CSV 批量变更不能用于绕审核换页。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 数据同步、快照与一致性",
            capability="scripts_data_sync_consistency",
            title="Google Ads Scripts, Reports for GAQL snapshots",
            url="https://developers.google.com/google-ads/scripts/docs/concepts/reports",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Scripts reports 文档支撑用 AdsApp.report/search 读取 GAQL 报表，"
                "并在内部保存 query、date range、pulled_at 和快照口径。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 数据同步、快照与一致性",
            capability="scripts_data_sync_consistency",
            title="Google Ads Scripts, Manager account scripts",
            url="https://developers.google.com/google-ads/scripts/docs/concepts/manager-scripts",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Manager scripts 支撑 MCC 下批量读取和检查 client accounts，"
                "但不能被设计成账号池、换号或规避封禁工具。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 数据同步、快照与一致性",
            capability="scripts_data_sync_consistency",
            title="Google Ads Scripts, External data integration",
            url="https://developers.google.com/google-ads/scripts/docs/integrations/external-data",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "External data 文档支撑 Sheets、Drive、JDBC、URL Fetch 等同步边界，"
                "同步器只能读取合规配置和报表，不能下发凭证或规避配置。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 数据同步、快照与一致性",
            capability="scripts_data_sync_consistency",
            title="Google Ads, About data freshness",
            url="https://support.google.com/google-ads/answer/2544985",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Data freshness 支撑 15 分钟同步不能被当成最终数据，"
                "同步结果需要标注 provisional、settling、finalized 等状态。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 数据同步、快照与一致性",
            capability="scripts_data_sync_consistency",
            title="Google Ads, About conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag 支撑近期 CPA/ROAS 会回填和变化，"
                "扩量前应做窗口重拉并等待收入状态稳定。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Scripts 数据同步、快照与一致性",
            capability="scripts_data_sync_consistency",
            title="Google Ads API, Reporting overview",
            url="https://developers.google.com/google-ads/api/docs/reporting/overview",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Reporting overview 支撑未来 API 同步也应保留 GAQL 查询、customer id、"
                "字段口径和原始快照，而不是只保存聚合 ROI。"
            ),
        ),
        ResearchSource(
            topic="任务编排、安全审批、执行日志与事故复盘",
            capability="task_orchestration_approval_audit",
            title="Google Ads, Using scripts to make automated changes",
            url="https://support.google.com/google-ads/answer/188712",
            publisher="Google Ads Help",
            source_type="automation_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads Scripts 可用于自动化变更，但应在官方脚本和授权语境内运行，"
                "不应被替换成 Cookie 后台接管。"
            ),
        ),
        ResearchSource(
            topic="任务编排、安全审批、执行日志与事故复盘",
            capability="task_orchestration_approval_audit",
            title="Google Ads Scripts, Authorization and user consent",
            url="https://developers.google.com/google-ads/scripts/docs/authorization",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Scripts 授权文档支撑任务执行必须由授权用户在账号语境内放行，"
                "不是复用浏览器会话或绕过登录。"
            ),
        ),
        ResearchSource(
            topic="任务编排、安全审批、执行日志与事故复盘",
            capability="task_orchestration_approval_audit",
            title="Google Ads Scripts, Limits and execution boundaries",
            url="https://developers.google.com/google-ads/scripts/docs/limits",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Scripts limits 支撑调度器必须考虑运行时长、账号范围和配额边界，"
                "不能设计成无限重试的无人值守写入器。"
            ),
        ),
        ResearchSource(
            topic="任务编排、安全审批、执行日志与事故复盘",
            capability="task_orchestration_approval_audit",
            title="Google Ads, Change history for audit evidence",
            url="https://support.google.com/google-ads/answer/19888",
            publisher="Google Ads Help",
            source_type="audit_reference",
            reliability="primary",
            claim_summary=(
                "Change history 支撑把外部广告后台变更纳入事故复盘，"
                "和本系统任务日志、Scripts log、指标日报一起对齐。"
            ),
        ),
        ResearchSource(
            topic="任务编排、安全审批、执行日志与事故复盘",
            capability="task_orchestration_approval_audit",
            title="Google Ads API, Change event",
            url="https://developers.google.com/google-ads/api/docs/change-event",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Change event 支撑未来通过官方 API 读取变更事件，"
                "用于外部审计和任务结果核对。"
            ),
        ),
        ResearchSource(
            topic="任务编排、安全审批、执行日志与事故复盘",
            capability="task_orchestration_approval_audit",
            title="Google SRE, Postmortem culture",
            url="https://sre.google/sre-book/postmortem-culture/",
            publisher="Google SRE",
            source_type="operations_reference",
            reliability="primary",
            claim_summary=(
                "SRE postmortem culture 支撑事故复盘应保留时间线、影响范围、根因、"
                "修复动作和预防项，而不是只记录失败状态。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 广告审核、拒登、Policy Manager 与申诉证据包",
            capability="ad_review_disapproval_appeal",
            title="Google Ads Help, About the ad review process",
            url="https://support.google.com/google-ads/answer/1722120",
            publisher="Google Ads Help",
            source_type="policy_reference",
            reliability="primary",
            claim_summary=(
                "广告审核流程说明支撑新建或修改广告/素材后进入审核，"
                "审核范围包括广告内容、关键词、目标页、图片、视频和其他资产。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 广告审核、拒登、Policy Manager 与申诉证据包",
            capability="ad_review_disapproval_appeal",
            title="Google Ads Help, Fix a disapproved ad or appeal a policy decision",
            url="https://support.google.com/google-ads/answer/9338593",
            publisher="Google Ads Help",
            source_type="policy_reference",
            reliability="primary",
            claim_summary=(
                "拒登修复和申诉说明支撑先定位 policy issue、修复广告/资产/目的地，"
                "再提交 review 或 appeal 的证据包流程。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 广告审核、拒登、Policy Manager 与申诉证据包",
            capability="ad_review_disapproval_appeal",
            title="Google Ads Help, About Policy Manager",
            url="https://support.google.com/google-ads/answer/9675313",
            publisher="Google Ads Help",
            source_type="policy_reference",
            reliability="primary",
            claim_summary=(
                "Policy Manager 支撑集中查看政策问题、受影响对象、申诉状态和处理结果，"
                "并把拒登转成可复盘工单。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 广告审核、拒登、Policy Manager 与申诉证据包",
            capability="ad_review_disapproval_appeal",
            title="Google Ads Policy, Destination requirements",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Destination requirements 支撑 Final URL、expanded URL、跳转链、移动端可达性和广告承诺一致性检查。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 广告审核、拒登、Policy Manager 与申诉证据包",
            capability="ad_review_disapproval_appeal",
            title="Google Ads Policy, Misrepresentation",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation 支撑主体、价格、资质、官方关系、结果承诺和重要限制不得误导用户。"
            ),
        ),
        ResearchSource(
            topic="Google Ads 广告审核、拒登、Policy Manager 与申诉证据包",
            capability="ad_review_disapproval_appeal",
            title="Google Ads API, PolicyTopicEntry",
            url="https://developers.google.com/google-ads/api/reference/rpc/latest/PolicyTopicEntry",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "PolicyTopicEntry 支撑未来把 policy topic、受影响对象和审核状态结构化保存，"
                "而不是通过 Cookie 后台抓取。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Recommendations、Experiments 与 Auto-apply 优化治理",
            capability="recommendations_experiments_auto_apply_governance",
            title="Google Ads Help, About recommendations",
            url="https://support.google.com/google-ads/answer/3448398",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "Recommendations 支撑把平台优化建议视为待评审假设，"
                "不能直接等同于 paid revenue 或 finalized revenue 改善。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Recommendations、Experiments 与 Auto-apply 优化治理",
            capability="recommendations_experiments_auto_apply_governance",
            title="Google Ads Help, Check your optimization score",
            url="https://support.google.com/google-ads/answer/9061547",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "Optimization score 支撑账户设置诊断和建议排序，"
                "但不能作为套利利润、回款或扣量风险的直接分数。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Recommendations、Experiments 与 Auto-apply 优化治理",
            capability="recommendations_experiments_auto_apply_governance",
            title="Google Ads Help, About applying recommendations automatically",
            url="https://support.google.com/google-ads/answer/10279006",
            publisher="Google Ads Help",
            source_type="automation_reference",
            reliability="primary",
            claim_summary=(
                "Auto-apply 会定期应用选定类型的建议，"
                "套利 V1 应默认关闭并用人工审批、白名单和回滚治理。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Recommendations、Experiments 与 Auto-apply 优化治理",
            capability="recommendations_experiments_auto_apply_governance",
            title="Google Ads Help, Set up a custom experiment",
            url="https://support.google.com/google-ads/answer/6261395",
            publisher="Google Ads Help",
            source_type="experiment_reference",
            reliability="primary",
            claim_summary=(
                "Custom experiments 支撑基线与实验版本分流，"
                "套利实验必须绑定 paid revenue、扣量、reject 和政策护栏。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Recommendations、Experiments 与 Auto-apply 优化治理",
            capability="recommendations_experiments_auto_apply_governance",
            title="Google Ads API, Optimization score and recommendations",
            url="https://developers.google.com/google-ads/api/docs/recommendations",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Google Ads API recommendations 支撑未来只读同步 recommendation、score uplift 和类型，"
                "写入动作必须审批和记录。"
            ),
        ),
        ResearchSource(
            topic="Google Ads Recommendations、Experiments 与 Auto-apply 优化治理",
            capability="recommendations_experiments_auto_apply_governance",
            title="Google Ads API, Experiments overview",
            url="https://developers.google.com/google-ads/api/docs/experiments/overview",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Experiments API 支撑未来保存 experiment plan、traffic split、result 和变更证据，"
                "但不应替代人工实验决策。"
            ),
        ),
        ResearchSource(
            topic="Creative Angle Library、素材版本与反馈闭环",
            capability="creative_angle_library_feedback_loop",
            title="Google Ads Help, About responsive search ads",
            url="https://support.google.com/google-ads/answer/7684791",
            publisher="Google Ads Help",
            source_type="creative_reference",
            reliability="primary",
            claim_summary=(
                "Responsive search ads 支撑多 headline/description 资产组合，"
                "素材库需要按 angle、role、version 和 evidence 记录资产。"
            ),
        ),
        ResearchSource(
            topic="Creative Angle Library、素材版本与反馈闭环",
            capability="creative_angle_library_feedback_loop",
            title="Google Ads Help, About Ad Strength",
            url="https://support.google.com/google-ads/answer/9921843",
            publisher="Google Ads Help",
            source_type="creative_reference",
            reliability="primary",
            claim_summary=(
                "Ad Strength 支撑资产覆盖和相关性诊断，"
                "但不能替代 paid revenue、扣量、拒付和政策反馈。"
            ),
        ),
        ResearchSource(
            topic="Creative Angle Library、素材版本与反馈闭环",
            capability="creative_angle_library_feedback_loop",
            title="Google Ads Help, View asset reporting for responsive search ads",
            url="https://support.google.com/google-ads/answer/9781208",
            publisher="Google Ads Help",
            source_type="creative_reporting",
            reliability="primary",
            claim_summary=(
                "Asset reporting 支撑按广告资产查看表现，"
                "用于素材版本和 angle 表现复盘。"
            ),
        ),
        ResearchSource(
            topic="Creative Angle Library、素材版本与反馈闭环",
            capability="creative_angle_library_feedback_loop",
            title="Google Ads Help, Set up ad variations",
            url="https://support.google.com/google-ads/answer/7438541",
            publisher="Google Ads Help",
            source_type="experiment_reference",
            reliability="primary",
            claim_summary=(
                "Ad variations 支撑对广告文案和 URL 变化做实验化比较，"
                "避免把多个素材变量混成不可解释结果。"
            ),
        ),
        ResearchSource(
            topic="Creative Angle Library、素材版本与反馈闭环",
            capability="creative_angle_library_feedback_loop",
            title="Google Ads API, Ad group ad asset view",
            url="https://developers.google.com/google-ads/api/fields/latest/ad_group_ad_asset_view",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Ad group ad asset view 支撑未来通过官方 API 读取资产表现和状态，"
                "而不是 Cookie 后台抓取。"
            ),
        ),
        ResearchSource(
            topic="Creative Angle Library、素材版本与反馈闭环",
            capability="creative_angle_library_feedback_loop",
            title="FTC, Endorsements, influencers, and reviews",
            url="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews",
            publisher="FTC",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC endorsement guidance 支撑评价、背书、商业关系披露和素材 claim 边界，"
                "不允许虚假评价或误导性引用。"
            ),
        ),
        ResearchSource(
            topic="竞品广告、SERP 与 Ads Transparency 情报",
            capability="competitor_ad_intelligence_serp_transparency",
            title="Google Ads Transparency Center",
            url="https://adstransparency.google.com/",
            publisher="Google",
            source_type="transparency_tool",
            reliability="primary",
            claim_summary=(
                "Ads Transparency Center 支撑人工查看公开广告素材和广告主透明度信息，"
                "用于市场 angle 和 claim 边界研究，不用于批量抓取或复制竞品。"
            ),
        ),
        ResearchSource(
            topic="竞品广告、SERP 与 Ads Transparency 情报",
            capability="competitor_ad_intelligence_serp_transparency",
            title="Google Ads Help, Ad Preview and Diagnosis tool",
            url="https://support.google.com/google-ads/answer/148778",
            publisher="Google Ads Help",
            source_type="diagnostic_reference",
            reliability="primary",
            claim_summary=(
                "Ad Preview and Diagnosis 支撑不通过真实搜索点击广告，也能预览和诊断广告展示语境。"
            ),
        ),
        ResearchSource(
            topic="竞品广告、SERP 与 Ads Transparency 情报",
            capability="competitor_ad_intelligence_serp_transparency",
            title="Google Ads Help, Auction insights",
            url="https://support.google.com/google-ads/answer/2579754",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Auction insights 支撑用 impression share、overlap、top of page 等指标解释竞争强度，"
                "不能用于推断竞品利润或组织对抗点击。"
            ),
        ),
        ResearchSource(
            topic="竞品广告、SERP 与 Ads Transparency 情报",
            capability="competitor_ad_intelligence_serp_transparency",
            title="Google Ads Help, Keyword Planner",
            url="https://support.google.com/google-ads/answer/7337243",
            publisher="Google Ads Help",
            source_type="keyword_research",
            reliability="primary",
            claim_summary=(
                "Keyword Planner 支撑把 SERP 和竞品观察转成关键词规模、竞争和测试优先级评估。"
            ),
        ),
        ResearchSource(
            topic="竞品广告、SERP 与 Ads Transparency 情报",
            capability="competitor_ad_intelligence_serp_transparency",
            title="Google Ads Policy, Trademarks",
            url="https://support.google.com/adspolicy/answer/6118",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Trademarks policy 支撑竞品情报不能转成商标误导、官方冒充、近似域名或仿冒素材。"
            ),
        ),
        ResearchSource(
            topic="竞品广告、SERP 与 Ads Transparency 情报",
            capability="competitor_ad_intelligence_serp_transparency",
            title="FTC, Native Advertising Guide for Businesses",
            url="https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses",
            publisher="FTC",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC native advertising guidance 支撑竞品比较页、原生广告和商业关系披露边界。"
            ),
        ),
        ResearchSource(
            topic="Campaign 命名、Labels、UTM/SubID 与维度治理",
            capability="campaign_taxonomy_naming_dimension_governance",
            title="Google Ads Help, About ValueTrack parameters",
            url="https://support.google.com/google-ads/answer/2375447",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "ValueTrack 支撑把 campaign、ad group、keyword、match type、device、"
                "network、creative 等点击上下文写入 URL，用于可复盘追踪。"
            ),
        ),
        ResearchSource(
            topic="Campaign 命名、Labels、UTM/SubID 与维度治理",
            capability="campaign_taxonomy_naming_dimension_governance",
            title="Google Ads Help, Create custom parameters for advanced tracking",
            url="https://support.google.com/google-ads/answer/6325879",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "Custom parameters 支撑用 `{_offer}`、`{_lpv}`、`{_angle}`、"
                "`{_linkv}` 等业务字段连接投放对象、页面版本和换链接版本。"
            ),
        ),
        ResearchSource(
            topic="Campaign 命名、Labels、UTM/SubID 与维度治理",
            capability="campaign_taxonomy_naming_dimension_governance",
            title="Google Ads Help, About ads labels",
            url="https://support.google.com/google-ads/answer/2475865",
            publisher="Google Ads Help",
            source_type="account_operations_reference",
            reliability="primary",
            claim_summary=(
                "Labels 可用于组织 campaign、ad group、ad、keyword 等对象，"
                "但需要快照和 registry，不能作为唯一事实来源。"
            ),
        ),
        ResearchSource(
            topic="Campaign 命名、Labels、UTM/SubID 与维度治理",
            capability="campaign_taxonomy_naming_dimension_governance",
            title="Google Analytics Help, URL builders",
            url="https://support.google.com/analytics/answer/10917952",
            publisher="Google Analytics Help",
            source_type="analytics_reference",
            reliability="primary",
            claim_summary=(
                "Campaign URL builders 支撑 utm_source、utm_medium、utm_campaign、"
                "utm_content、utm_term、utm_id 等手动标记口径。"
            ),
        ),
        ResearchSource(
            topic="Campaign 命名、Labels、UTM/SubID 与维度治理",
            capability="campaign_taxonomy_naming_dimension_governance",
            title="Google Ads API, Labels",
            url="https://developers.google.com/google-ads/api/docs/reporting/labels",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Labels API 支撑未来通过官方 API 保存 label id、resource name 和 label report，"
                "而不是抓取 Cookie 后台。"
            ),
        ),
        ResearchSource(
            topic="Campaign 命名、Labels、UTM/SubID 与维度治理",
            capability="campaign_taxonomy_naming_dimension_governance",
            title="Google Ads API, Google Ads Query Language",
            url="https://developers.google.com/google-ads/api/docs/query/overview",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "GAQL 支撑字段、segment、filter 和 report snapshot 的可复盘查询设计，"
                "用于报表 join key 和维度治理。"
            ),
        ),
        ResearchSource(
            topic="异常监控、告警、止损队列与事故分诊",
            capability="anomaly_monitoring_alerting_stoploss_triage",
            title="Google Ads Help, About spending limits",
            url="https://support.google.com/google-ads/answer/10486637",
            publisher="Google Ads Help",
            source_type="budget_reference",
            reliability="primary",
            claim_summary=(
                "Spending limits 支撑按 average daily budget、daily spending limit、"
                "monthly spending limit、served cost 和 billed cost 设计预算告警。"
            ),
        ),
        ResearchSource(
            topic="异常监控、告警、止损队列与事故分诊",
            capability="anomaly_monitoring_alerting_stoploss_triage",
            title="Google Ads Help, Set up automated rules",
            url="https://support.google.com/google-ads/answer/2472779",
            publisher="Google Ads Help",
            source_type="automation_reference",
            reliability="primary",
            claim_summary=(
                "Automated rules 支撑理解规则条件、频率和执行边界；"
                "本系统 V1 只生成建议和审批队列，不自动改后台。"
            ),
        ),
        ResearchSource(
            topic="异常监控、告警、止损队列与事故分诊",
            capability="anomaly_monitoring_alerting_stoploss_triage",
            title="Google Ads Help, Data discrepancies",
            url="https://support.google.com/google-ads/answer/7457111",
            publisher="Google Ads Help",
            source_type="diagnostic_reference",
            reliability="primary",
            claim_summary=(
                "Data discrepancies 支撑把 Google Ads、GA4、第三方报表、server log "
                "和内部收入差异作为分层诊断，而不是用补量修报表。"
            ),
        ),
        ResearchSource(
            topic="异常监控、告警、止损队列与事故分诊",
            capability="anomaly_monitoring_alerting_stoploss_triage",
            title="Google Ads Help, About conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag 支撑近期 CPA、ROAS、RPV 和 ROI 告警要有时间窗口，"
                "扩量必须等待收入和转化回填。"
            ),
        ),
        ResearchSource(
            topic="异常监控、告警、止损队列与事故分诊",
            capability="anomaly_monitoring_alerting_stoploss_triage",
            title="Google Ads Help, Change history",
            url="https://support.google.com/google-ads/answer/19888",
            publisher="Google Ads Help",
            source_type="audit_reference",
            reliability="primary",
            claim_summary=(
                "Change history 支撑异常前后按时间线查预算、关键词、URL、素材、"
                "conversion goal 和操作人。"
            ),
        ),
        ResearchSource(
            topic="异常监控、告警、止损队列与事故分诊",
            capability="anomaly_monitoring_alerting_stoploss_triage",
            title="Google SRE Book, Monitoring Distributed Systems",
            url="https://sre.google/sre-book/monitoring-distributed-systems/",
            publisher="Google SRE",
            source_type="operations_reference",
            reliability="primary",
            claim_summary=(
                "SRE monitoring principles 支撑低噪声、高行动性的告警设计、"
                "故障分诊和 postmortem 机制。"
            ),
        ),
        ResearchSource(
            topic="Search Terms、否定词与 Query Mining 治理",
            capability="search_terms_negative_keyword_query_mining",
            title="Google Ads Help, About the search terms report",
            url="https://support.google.com/google-ads/answer/2472708",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Search terms report 支撑用真实查询、keyword、match type、"
                "Search Partners 和表现数据做 query mining。"
            ),
        ),
        ResearchSource(
            topic="Search Terms、否定词与 Query Mining 治理",
            capability="search_terms_negative_keyword_query_mining",
            title="Google Ads Help, About negative keywords",
            url="https://support.google.com/google-ads/answer/2453972",
            publisher="Google Ads Help",
            source_type="targeting_reference",
            reliability="primary",
            claim_summary=(
                "Negative keywords 支撑 negative broad/phrase/exact、account-level negative、"
                "negative list 和层级治理。"
            ),
        ),
        ResearchSource(
            topic="Search Terms、否定词与 Query Mining 治理",
            capability="search_terms_negative_keyword_query_mining",
            title="Google Ads Help, Get negative keyword ideas using the search terms report",
            url="https://support.google.com/google-ads/answer/7102466",
            publisher="Google Ads Help",
            source_type="optimization_reference",
            reliability="primary",
            claim_summary=(
                "该来源支撑从 search terms report 选择 query 添加到 ad group、"
                "campaign 或 negative list。"
            ),
        ),
        ResearchSource(
            topic="Search Terms、否定词与 Query Mining 治理",
            capability="search_terms_negative_keyword_query_mining",
            title="Google Ads Help, About keyword matching options",
            url="https://support.google.com/google-ads/answer/7478529",
            publisher="Google Ads Help",
            source_type="targeting_reference",
            reliability="primary",
            claim_summary=(
                "Keyword matching options 支撑 broad、phrase、exact、negative keywords、"
                "PMax/Search 优先级和 query 匹配原理。"
            ),
        ),
        ResearchSource(
            topic="Search Terms、否定词与 Query Mining 治理",
            capability="search_terms_negative_keyword_query_mining",
            title="Google Ads Help, About search terms insights",
            url="https://support.google.com/google-ads/answer/11386930",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "Search terms insights 支撑 search category、subcategory、PMax/Search/Shopping "
                "聚合查询主题和隐私聚合边界。"
            ),
        ),
        ResearchSource(
            topic="Search Terms、否定词与 Query Mining 治理",
            capability="search_terms_negative_keyword_query_mining",
            title="Google Ads API, SearchTermView field reference",
            url="https://developers.google.com/google-ads/api/fields/latest/search_term_view",
            publisher="Google for Developers",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "SearchTermView 支撑未来以官方 API 保存 query 级报表、segments、metrics "
                "和 source snapshot。"
            ),
        ),
        ResearchSource(
            topic="Offer Cap、Payout、状态变更与替代 Offer 治理",
            capability="offer_cap_payout_status_governance",
            title="TUNE, Offer Payouts and Caps",
            url="https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps",
            publisher="TUNE",
            source_type="affiliate_platform_reference",
            reliability="platform_documentation",
            claim_summary=(
                "TUNE 文档支撑 affiliate offer 的 payout、conversion cap、"
                "budget cap 和 tier 概念。"
            ),
        ),
        ResearchSource(
            topic="Offer Cap、Payout、状态变更与替代 Offer 治理",
            capability="offer_cap_payout_status_governance",
            title="TUNE Dev Hub, OfferConversionCap",
            url="https://developers.tune.com/network-models/offerconversioncap/",
            publisher="TUNE",
            source_type="developer_reference",
            reliability="platform_documentation",
            claim_summary=(
                "OfferConversionCap 模型支撑按 offer/affiliate 保存 conversion、"
                "payout 和 revenue cap 的数据结构。"
            ),
        ),
        ResearchSource(
            topic="Offer Cap、Payout、状态变更与替代 Offer 治理",
            capability="offer_cap_payout_status_governance",
            title="Everflow API, Get Offer",
            url="https://developers.everflow.io/docs/affiliate/offers/",
            publisher="Everflow",
            source_type="developer_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Everflow offer API 字段支撑 offer status、daily payout cap、"
                "affiliate status 和 targeting rule 快照。"
            ),
        ),
        ResearchSource(
            topic="Offer Cap、Payout、状态变更与替代 Offer 治理",
            capability="offer_cap_payout_status_governance",
            title="Voluum, Tracking Payouts",
            url="https://doc.voluum.com/en/tracking_payout.html",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Tracking payouts 支撑从 affiliate network postback 接收动态 payout，"
                "避免只用静态 headline payout 计算 ROI。"
            ),
        ),
        ResearchSource(
            topic="Offer Cap、Payout、状态变更与替代 Offer 治理",
            capability="offer_cap_payout_status_governance",
            title="Voluum, Parameters in Postback URLs",
            url="https://doc.voluum.com/article/parameters-in-postback-urls",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Postback URL 参数支撑 click_id、transaction_id、payout、status "
                "和结算状态对账。"
            ),
        ),
        ResearchSource(
            topic="Offer Cap、Payout、状态变更与替代 Offer 治理",
            capability="offer_cap_payout_status_governance",
            title="Google Ads Policy, Destination requirements",
            url="https://support.google.com/adspolicy/answer/6368661",
            publisher="Google Ads Policy",
            source_type="ad_policy",
            reliability="primary",
            claim_summary=(
                "Destination requirements 支撑替代 Offer、Final URL 和落地页承诺必须一致，"
                "不能切到不相关或未审核目的地。"
            ),
        ),
        ResearchSource(
            topic="Source、Publisher、Placement 质量评分与名单治理",
            capability="source_publisher_placement_quality_governance",
            title="Google AdSense Help, Traffic provider checklist",
            url="https://support.google.com/adsense/answer/3332805",
            publisher="Google AdSense Help",
            source_type="traffic_quality_reference",
            reliability="primary",
            claim_summary=(
                "Traffic provider checklist 支撑供应商尽调、来源透明、样例 URL、"
                "价格异常和质量报告，作为 source quality 准入证据。"
            ),
        ),
        ResearchSource(
            topic="Source、Publisher、Placement 质量评分与名单治理",
            capability="source_publisher_placement_quality_governance",
            title="Google AdSense Help, Set up a traffic segmentation plan",
            url="https://support.google.com/adsense/answer/2583698",
            publisher="Google AdSense Help",
            source_type="traffic_quality_reference",
            reliability="primary",
            claim_summary=(
                "Traffic segmentation plan 支撑按来源、渠道和广告位置分段监控，"
                "用于发现异常来源并保存停源证据。"
            ),
        ),
        ResearchSource(
            topic="Source、Publisher、Placement 质量评分与名单治理",
            capability="source_publisher_placement_quality_governance",
            title="Google Ads Help, Managing invalid traffic",
            url="https://support.google.com/google-ads/answer/11182074",
            publisher="Google Ads Help",
            source_type="invalid_traffic_reference",
            reliability="primary",
            claim_summary=(
                "Managing invalid traffic 支撑广告主侧 invalid clicks、异常点击、"
                "账单 credit 和来源诊断，不支持补点击或伪造流量。"
            ),
        ),
        ResearchSource(
            topic="Source、Publisher、Placement 质量评分与名单治理",
            capability="source_publisher_placement_quality_governance",
            title="Google Ads Help, Use placement exclusion lists",
            url="https://support.google.com/google-ads/answer/9162992",
            publisher="Google Ads Help",
            source_type="placement_control_reference",
            reliability="primary",
            claim_summary=(
                "Placement exclusion lists 支撑把低质 publisher、placement、app、"
                "channel 保存为排除清单和名单治理对象。"
            ),
        ),
        ResearchSource(
            topic="Source、Publisher、Placement 质量评分与名单治理",
            capability="source_publisher_placement_quality_governance",
            title="Google Ads Help, PMax channel performance report",
            url="https://support.google.com/google-ads/answer/16260130",
            publisher="Google Ads Help",
            source_type="reporting_reference",
            reliability="primary",
            claim_summary=(
                "PMax channel performance report 支撑按 Search、YouTube、Discover、"
                "Gmail 等 channel 分解自动化流量质量。"
            ),
        ),
        ResearchSource(
            topic="Source、Publisher、Placement 质量评分与名单治理",
            capability="source_publisher_placement_quality_governance",
            title="Voluum, Parameters in Postback URLs",
            url="https://doc.voluum.com/article/parameters-in-postback-urls",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Postback URL 参数支撑 click_id、transaction_id、payout、status "
                "和 buyer feedback 回传，连接 subid 与 approved/paid revenue。"
            ),
        ),
        ResearchSource(
            topic="流量供应商合同、IO、退款与争议治理",
            capability="traffic_vendor_contract_io_dispute_governance",
            title="IAB, General Terms and Conditions",
            url="https://www.iab.com/guidelines/general-terms-and-conditions/",
            publisher="IAB",
            source_type="industry_terms_reference",
            reliability="industry_reference",
            claim_summary=(
                "IAB General Terms and Conditions 支撑数字广告媒体采购中的标准条款、"
                "IO、付款、取消、makegood 和争议治理背景。"
            ),
        ),
        ResearchSource(
            topic="流量供应商合同、IO、退款与争议治理",
            capability="traffic_vendor_contract_io_dispute_governance",
            title="Google AdSense Help, If you want to purchase traffic to your site",
            url="https://support.google.com/adsense/answer/1348722",
            publisher="Google AdSense Help",
            source_type="traffic_quality_reference",
            reliability="primary",
            claim_summary=(
                "购买流量指导支撑发布商需要监控每个来源、暂停可疑来源，"
                "并对第三方供应商带来的流量质量负责。"
            ),
        ),
        ResearchSource(
            topic="流量供应商合同、IO、退款与争议治理",
            capability="traffic_vendor_contract_io_dispute_governance",
            title="Google Ads Help, Managing invalid traffic",
            url="https://support.google.com/google-ads/answer/11182074",
            publisher="Google Ads Help",
            source_type="invalid_traffic_reference",
            reliability="primary",
            claim_summary=(
                "Managing invalid traffic 支撑把 invalid clicks、invalid click rate、"
                "billing credit 和异常来源诊断写入争议证据包。"
            ),
        ),
        ResearchSource(
            topic="流量供应商合同、IO、退款与争议治理",
            capability="traffic_vendor_contract_io_dispute_governance",
            title="Google Ads Help, About ValueTrack parameters",
            url="https://support.google.com/google-ads/answer/2375447",
            publisher="Google Ads Help",
            source_type="tracking_reference",
            reliability="primary",
            claim_summary=(
                "ValueTrack 支撑在 IO 的 tracking appendix 中约定 campaign、ad group、"
                "keyword、network、device、creative 等可回放字段。"
            ),
        ),
        ResearchSource(
            topic="流量供应商合同、IO、退款与争议治理",
            capability="traffic_vendor_contract_io_dispute_governance",
            title="FTC, Native Advertising Guide for Businesses",
            url="https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses",
            publisher="FTC",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "FTC native advertising guidance 支撑 direct buy、native、advertorial "
                "和 sponsorship 场景中的广告性质披露和素材责任。"
            ),
        ),
        ResearchSource(
            topic="流量供应商合同、IO、退款与争议治理",
            capability="traffic_vendor_contract_io_dispute_governance",
            title="Voluum, Parameters in Postback URLs",
            url="https://doc.voluum.com/article/parameters-in-postback-urls",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Postback 参数支撑在争议中连接 click_id、transaction_id、payout、"
                "status、approved/paid revenue 和 buyer feedback。"
            ),
        ),
        ResearchSource(
            topic="Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理",
            capability="lead_buyer_contract_io_paid_definition_governance",
            title="FTC, Follow the Lead workshop",
            url="https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Follow the Lead 支撑 lead generation 中消费者信息流转、"
                "buyer handoff、透明度、投诉和监管风险。"
            ),
        ),
        ResearchSource(
            topic="Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理",
            capability="lead_buyer_contract_io_paid_definition_governance",
            title="Google Ads API, Upload offline conversions",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-offline",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Offline conversion upload 支撑把真实 qualified、approved 或 paid "
                "buyer feedback 回传给广告优化，而不是通过 Cookie 后台操作。"
            ),
        ),
        ResearchSource(
            topic="Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理",
            capability="lead_buyer_contract_io_paid_definition_governance",
            title="Google Ads, Customer data policies",
            url="https://support.google.com/google-ads/answer/7475709",
            publisher="Google Ads Help",
            source_type="privacy_policy",
            reliability="primary",
            claim_summary=(
                "Customer data policies 支撑用户数据、consent、隐私披露、"
                "分享和安全处理要求。"
            ),
        ),
        ResearchSource(
            topic="Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理",
            capability="lead_buyer_contract_io_paid_definition_governance",
            title="TUNE, Offer Payouts and Caps",
            url="https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps",
            publisher="TUNE",
            source_type="affiliate_platform_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Offer payout and caps 支撑 payout、conversion cap、budget cap "
                "和 offer 经济口径。"
            ),
        ),
        ResearchSource(
            topic="Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理",
            capability="lead_buyer_contract_io_paid_definition_governance",
            title="Everflow API, Get Offer",
            url="https://developers.everflow.io/docs/affiliate/offers/",
            publisher="Everflow",
            source_type="developer_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Everflow offer API 支撑 offer status、payout、cap、targeting、"
                "affiliate status 和字段快照。"
            ),
        ),
        ResearchSource(
            topic="Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理",
            capability="lead_buyer_contract_io_paid_definition_governance",
            title="Voluum, Conversion Status",
            url="https://doc.voluum.com/article/conversion-status",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Conversion status 支撑 pending、approved、rejected、payout "
                "和 postback 状态对账。"
            ),
        ),
        ResearchSource(
            topic="Lead Pricing、Payout Negotiation 与结算安全垫治理",
            capability="lead_pricing_payout_negotiation_governance",
            title="FTC, Follow the Lead workshop",
            url="https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Follow the Lead 支撑 lead generation、buyer handoff、消费者信息流转、"
                "透明度和投诉风险。"
            ),
        ),
        ResearchSource(
            topic="Lead Pricing、Payout Negotiation 与结算安全垫治理",
            capability="lead_pricing_payout_negotiation_governance",
            title="Google Ads, About conversion values",
            url="https://support.google.com/google-ads/answer/3419241",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion values 支撑用真实业务价值和 net/paid value "
                "而不是 headline payout 作为出价输入。"
            ),
        ),
        ResearchSource(
            topic="Lead Pricing、Payout Negotiation 与结算安全垫治理",
            capability="lead_pricing_payout_negotiation_governance",
            title="Google Local Services Ads, Lead costs and credits",
            url="https://support.google.com/localservices/answer/7436333",
            publisher="Google Local Services Help",
            source_type="local_services_reference",
            reliability="primary",
            claim_summary=(
                "Local Services lead costs and credits 支撑 charged lead、"
                "wrong service/area、credit 和 lead quality 语境。"
            ),
        ),
        ResearchSource(
            topic="Lead Pricing、Payout Negotiation 与结算安全垫治理",
            capability="lead_pricing_payout_negotiation_governance",
            title="TUNE, Offer Payouts and Caps",
            url="https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps",
            publisher="TUNE",
            source_type="affiliate_platform_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Offer payout and caps 支撑 affiliate offer payout、cap、budget "
                "和 tier 概念。"
            ),
        ),
        ResearchSource(
            topic="Lead Pricing、Payout Negotiation 与结算安全垫治理",
            capability="lead_pricing_payout_negotiation_governance",
            title="Everflow API, Get Offer",
            url="https://developers.everflow.io/docs/affiliate/offers/",
            publisher="Everflow",
            source_type="developer_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Everflow offer API 支撑 offer status、payout、cap、targeting、"
                "affiliate status 和字段快照。"
            ),
        ),
        ResearchSource(
            topic="Lead Pricing、Payout Negotiation 与结算安全垫治理",
            capability="lead_pricing_payout_negotiation_governance",
            title="Voluum, Tracking Payouts",
            url="https://doc.voluum.com/en/tracking_payout.html",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Tracking payouts 支撑从 affiliate postback 接收动态 payout "
                "并按实际 payout 对账。"
            ),
        ),
        ResearchSource(
            topic="Appointment Lead、Booking、Show Rate 与 No-show 治理",
            capability="appointment_lead_booking_show_rate_governance",
            title="Google Calendar Help, Create an appointment schedule",
            url="https://support.google.com/calendar/answer/10729749",
            publisher="Google Calendar Help",
            source_type="booking_reference",
            reliability="primary",
            claim_summary=(
                "Appointment schedule 支撑 booking page、availability、"
                "slot 和日历预约流程语境。"
            ),
        ),
        ResearchSource(
            topic="Appointment Lead、Booking、Show Rate 与 No-show 治理",
            capability="appointment_lead_booking_show_rate_governance",
            title="Google Business Profile Help, Set up bookings through a provider",
            url="https://support.google.com/business/answer/7475773",
            publisher="Google Business Profile Help",
            source_type="booking_reference",
            reliability="primary",
            claim_summary=(
                "Business Profile bookings 支撑本地商家通过 provider "
                "接收预约和 Reserve with Google 语境。"
            ),
        ),
        ResearchSource(
            topic="Appointment Lead、Booking、Show Rate 与 No-show 治理",
            capability="appointment_lead_booking_show_rate_governance",
            title="Google Local Services Ads, How leads work",
            url="https://support.google.com/localservices/answer/7195435",
            publisher="Google Local Services Help",
            source_type="local_services_reference",
            reliability="primary",
            claim_summary=(
                "Local Services leads 支撑 valid lead、charged lead、"
                "service area、预算和 lead quality 语境。"
            ),
        ),
        ResearchSource(
            topic="Appointment Lead、Booking、Show Rate 与 No-show 治理",
            capability="appointment_lead_booking_show_rate_governance",
            title="Google Ads API, Upload offline conversions",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-offline",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Offline conversion upload 支撑把 showed、completed、paid "
                "等真实预约后续状态回传。"
            ),
        ),
        ResearchSource(
            topic="Appointment Lead、Booking、Show Rate 与 No-show 治理",
            capability="appointment_lead_booking_show_rate_governance",
            title="Google Ads API, Upload conversion adjustments",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Conversion adjustments 支撑 no-show、cancel、return 或"
                "预约价值错误后的修正治理。"
            ),
        ),
        ResearchSource(
            topic="Appointment Lead、Booking、Show Rate 与 No-show 治理",
            capability="appointment_lead_booking_show_rate_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_guidance",
            reliability="primary",
            claim_summary=(
                "TSR 指南支撑预约确认、电话提醒、DNC、consent、"
                "记录保存和投诉治理。"
            ),
        ),
        ResearchSource(
            topic="Buyer Capacity、Cap Pacing 与 Dayparting 治理",
            capability="buyer_capacity_cap_pacing_dayparting_governance",
            title="Google Ads Help, Set up an ad schedule",
            url="https://support.google.com/google-ads/answer/6372656",
            publisher="Google Ads Help",
            source_type="platform_reference",
            reliability="primary",
            claim_summary=(
                "Ad schedule 支撑按星期和小时控制广告展示，"
                "用于让投放时段匹配 buyer hours 和 call center capacity。"
            ),
        ),
        ResearchSource(
            topic="Buyer Capacity、Cap Pacing 与 Dayparting 治理",
            capability="buyer_capacity_cap_pacing_dayparting_governance",
            title="Google Ads Help, About overdelivery and average daily budget",
            url="https://support.google.com/google-ads/answer/1704443",
            publisher="Google Ads Help",
            source_type="budget_reference",
            reliability="primary",
            claim_summary=(
                "Average daily budget 和 overdelivery 支撑内部 hard stop、"
                "cap pacing 和预算超节奏风险治理。"
            ),
        ),
        ResearchSource(
            topic="Buyer Capacity、Cap Pacing 与 Dayparting 治理",
            capability="buyer_capacity_cap_pacing_dayparting_governance",
            title="Google Ads Help, About call reporting",
            url="https://support.google.com/google-ads/answer/2454052",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Call reporting 支撑按来电时间、call duration、missed call "
                "和 call conversion 诊断接量能力。"
            ),
        ),
        ResearchSource(
            topic="Buyer Capacity、Cap Pacing 与 Dayparting 治理",
            capability="buyer_capacity_cap_pacing_dayparting_governance",
            title="Google Ads Help, Conversion lag reporting",
            url="https://support.google.com/google-ads/answer/9347141",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Conversion lag reporting 支撑 dayparting 不能只看当天转化，"
                "要按 mature accepted/qualified/paid cohort 回看时段质量。"
            ),
        ),
        ResearchSource(
            topic="Buyer Capacity、Cap Pacing 与 Dayparting 治理",
            capability="buyer_capacity_cap_pacing_dayparting_governance",
            title="Google Local Services Ads, How leads work",
            url="https://support.google.com/localservices/answer/7195435",
            publisher="Google Local Services Help",
            source_type="local_services_reference",
            reliability="primary",
            claim_summary=(
                "Local Services leads 支撑 valid lead、charged lead、service area、"
                "预算和 lead quality 语境。"
            ),
        ),
        ResearchSource(
            topic="Buyer Capacity、Cap Pacing 与 Dayparting 治理",
            capability="buyer_capacity_cap_pacing_dayparting_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Telemarketing Sales Rule 支撑 phone lead 联系、DNC、consent、"
                "投诉和记录保存的 capacity governance 边界。"
            ),
        ),
        ResearchSource(
            topic="CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping",
            capability="crm_buyer_feedback_offline_conversion_mapping",
            title="Google Ads API, Upload offline conversions",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-offline",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Offline conversion upload 支撑把 CRM 和 buyer 的 qualified、"
                "approved、paid 状态导入 Google Ads。"
            ),
        ),
        ResearchSource(
            topic="CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping",
            capability="crm_buyer_feedback_offline_conversion_mapping",
            title="Google Ads API, Enhanced conversions for leads",
            url="https://developers.google.com/google-ads/api/docs/conversions/enhanced-conversions/leads",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Enhanced conversions for leads 支撑用合规哈希用户提供数据"
                "增强 lead 后续状态匹配。"
            ),
        ),
        ResearchSource(
            topic="CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping",
            capability="crm_buyer_feedback_offline_conversion_mapping",
            title="Google Ads API, Upload conversion adjustments",
            url="https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments",
            publisher="Google Ads API",
            source_type="developer_reference",
            reliability="primary",
            claim_summary=(
                "Conversion adjustments 支撑 returned、refund、clawback 或 value "
                "错误后的修正治理。"
            ),
        ),
        ResearchSource(
            topic="CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping",
            capability="crm_buyer_feedback_offline_conversion_mapping",
            title="Google Ads, Offline conversion import discrepancies and errors",
            url="https://support.google.com/google-ads/answer/13321563",
            publisher="Google Ads Help",
            source_type="measurement_reference",
            reliability="primary",
            claim_summary=(
                "Offline import discrepancies 支撑导入错误、匹配率、未匹配和"
                "诊断 QA。"
            ),
        ),
        ResearchSource(
            topic="CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping",
            capability="crm_buyer_feedback_offline_conversion_mapping",
            title="Google Ads, Customer data policies",
            url="https://support.google.com/google-ads/answer/7475709",
            publisher="Google Ads Help",
            source_type="privacy_policy",
            reliability="primary",
            claim_summary=(
                "Customer data policies 支撑 enhanced conversions、用户提供数据、"
                "consent、披露和安全处理要求。"
            ),
        ),
        ResearchSource(
            topic="CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping",
            capability="crm_buyer_feedback_offline_conversion_mapping",
            title="Voluum, Parameters in Postback URLs",
            url="https://doc.voluum.com/article/parameters-in-postback-urls",
            publisher="Voluum",
            source_type="tracking_reference",
            reliability="platform_documentation",
            claim_summary=(
                "Postback 参数支撑 click_id、transaction_id、payout、status "
                "等 buyer feedback 映射。"
            ),
        ),
        ResearchSource(
            topic="Insurance、Medicare / ACA 与 Final Expense Lead 治理",
            capability="insurance_medicare_aca_final_expense_lead_governance",
            title="Google Ads Policy, Health insurance ads",
            url="https://support.google.com/adspolicy/answer/15597838",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Health insurance ads policy 支撑保险 lead 页面和广告必须先确认"
                "健康保险广告认证、地区和产品限制。"
            ),
        ),
        ResearchSource(
            topic="Insurance、Medicare / ACA 与 Final Expense Lead 治理",
            capability="insurance_medicare_aca_final_expense_lead_governance",
            title="Google Ads Policy, Personalized advertising",
            url="https://support.google.com/adspolicy/answer/143465",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Personalized advertising policy 支撑健康、财务困难和受保护属性"
                "相关定向、素材和页面 claim 的边界。"
            ),
        ),
        ResearchSource(
            topic="Insurance、Medicare / ACA 与 Final Expense Lead 治理",
            capability="insurance_medicare_aca_final_expense_lead_governance",
            title="HealthCare.gov, Dates and deadlines",
            url="https://www.healthcare.gov/quick-guide/dates-and-deadlines/",
            publisher="HealthCare.gov",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "Dates and deadlines 支撑 ACA / Marketplace 开放注册、页面年份、"
                "预算 ramp 和窗口外投放的日期判断。"
            ),
        ),
        ResearchSource(
            topic="Insurance、Medicare / ACA 与 Final Expense Lead 治理",
            capability="insurance_medicare_aca_final_expense_lead_governance",
            title="Medicare.gov, Joining a plan",
            url="https://www.medicare.gov/basics/get-started-with-medicare/get-more-coverage/joining-a-plan",
            publisher="Medicare.gov",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "Joining a plan 支撑 Medicare plan 选择、加入和更换窗口，"
                "避免广告和页面使用过期 enrollment 文案。"
            ),
        ),
        ResearchSource(
            topic="Insurance、Medicare / ACA 与 Final Expense Lead 治理",
            capability="insurance_medicare_aca_final_expense_lead_governance",
            title="CMS, Contract Year 2025 Medicare Advantage and Part D Final Rule",
            url="https://www.cms.gov/newsroom/fact-sheets/contract-year-2025-medicare-advantage-and-part-d-final-rule-cms-4205-f",
            publisher="Centers for Medicare & Medicaid Services",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "CMS final rule fact sheet 支撑 Medicare marketing、TPMO、"
                "agent/broker 和第三方 lead 分发的治理语境。"
            ),
        ),
        ResearchSource(
            topic="Insurance、Medicare / ACA 与 Final Expense Lead 治理",
            capability="insurance_medicare_aca_final_expense_lead_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Telemarketing Sales Rule 支撑保险电话 lead 的披露、DNC、"
                "拒绝联系、记录和投诉治理边界。"
            ),
        ),
        ResearchSource(
            topic="Loan、Mortgage、Credit 与 Debt Lead 治理",
            capability="loan_mortgage_credit_debt_lead_governance",
            title="Google Ads Policy, Financial products and services",
            url="https://support.google.com/adspolicy/answer/2464998",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Financial products and services policy 支撑贷款、债务、信用和"
                "金融服务 lead 的披露、地区规则、认证和禁投项。"
            ),
        ),
        ResearchSource(
            topic="Loan、Mortgage、Credit 与 Debt Lead 治理",
            capability="loan_mortgage_credit_debt_lead_governance",
            title="Google Ads Policy, Housing, employment, and credit FAQ",
            url="https://support.google.com/adspolicy/answer/9997418",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Housing, employment, and credit FAQ 支撑美国/加拿大 mortgage、"
                "credit 和 loan 类广告的定向限制。"
            ),
        ),
        ResearchSource(
            topic="Loan、Mortgage、Credit 与 Debt Lead 治理",
            capability="loan_mortgage_credit_debt_lead_governance",
            title="CFPB, Digital comparison-shopping circular",
            url="https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/",
            publisher="Consumer Financial Protection Bureau",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Digital comparison-shopping circular 支撑金融产品比较、"
                "补偿驱动排序、导流和 steering 风险治理。"
            ),
        ),
        ResearchSource(
            topic="Loan、Mortgage、Credit 与 Debt Lead 治理",
            capability="loan_mortgage_credit_debt_lead_governance",
            title="CFPB, Regulation V / Fair Credit Reporting Act",
            url="https://www.consumerfinance.gov/rules-policy/regulations/1022/",
            publisher="Consumer Financial Protection Bureau",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Regulation V / FCRA 支撑 consumer report、credit eligibility "
                "和信贷/住房/保险/就业资格判断不能按普通营销 lead 简化处理。"
            ),
        ),
        ResearchSource(
            topic="Loan、Mortgage、Credit 与 Debt Lead 治理",
            capability="loan_mortgage_credit_debt_lead_governance",
            title="FTC, Complying with the Telemarketing Sales Rule",
            url="https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Telemarketing Sales Rule 支撑 debt relief、电话销售、DNC、"
                "advance fee、拒绝联系和记录保存边界。"
            ),
        ),
        ResearchSource(
            topic="Loan、Mortgage、Credit 与 Debt Lead 治理",
            capability="loan_mortgage_credit_debt_lead_governance",
            title="NMLS Consumer Access",
            url="https://www.nmlsconsumeraccess.org/",
            publisher="Nationwide Multistate Licensing System",
            source_type="licensing_reference",
            reliability="primary",
            claim_summary=(
                "NMLS Consumer Access 支撑 mortgage loan originator、lender "
                "和 broker licensing / authorization 证据引用。"
            ),
        ),
        ResearchSource(
            topic="Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理",
            capability="legal_case_intake_mass_tort_lead_governance",
            title="ABA Model Rule 7.1, Communications Concerning a Lawyer's Services",
            url="https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communications_concerning_a_lawyers_services/",
            publisher="American Bar Association",
            source_type="professional_conduct_reference",
            reliability="primary",
            claim_summary=(
                "Model Rule 7.1 支撑法律服务广告不能 false or misleading，"
                "用于赔偿、胜诉、官方关系和专业能力 claim 审核。"
            ),
        ),
        ResearchSource(
            topic="Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理",
            capability="legal_case_intake_mass_tort_lead_governance",
            title="ABA Model Rule 7.2, Specific Rules for Lawyer Communications",
            url="https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_2_communications_concerning_a_lawyers_services_specific_rules/",
            publisher="American Bar Association",
            source_type="professional_conduct_reference",
            reliability="primary",
            claim_summary=(
                "Model Rule 7.2 支撑律师广告、lead generator、referral、"
                "联系方式和补偿披露边界。"
            ),
        ),
        ResearchSource(
            topic="Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理",
            capability="legal_case_intake_mass_tort_lead_governance",
            title="ABA Model Rule 7.3, Solicitation of Clients",
            url="https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_3_solicitation_of_clients/",
            publisher="American Bar Association",
            source_type="professional_conduct_reference",
            reliability="primary",
            claim_summary=(
                "Model Rule 7.3 支撑 solicitation、实时联系、压力式获客和"
                "事故/案件人群定向联系风险判断。"
            ),
        ),
        ResearchSource(
            topic="Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理",
            capability="legal_case_intake_mass_tort_lead_governance",
            title="ABA Model Rule 1.18, Duties to Prospective Client",
            url="https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_18_duties_to_prospective_client/",
            publisher="American Bar Association",
            source_type="professional_conduct_reference",
            reliability="primary",
            claim_summary=(
                "Model Rule 1.18 支撑 prospective client 信息、初次咨询内容、"
                "case notes 和 intake data 的谨慎处理。"
            ),
        ),
        ResearchSource(
            topic="Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理",
            capability="legal_case_intake_mass_tort_lead_governance",
            title="Google Ads Policy, Personalized advertising",
            url="https://support.google.com/adspolicy/answer/143465",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Personalized advertising policy 支撑法律问题、身份、健康、"
                "财务困境等敏感状态不能被不当用于个性化广告。"
            ),
        ),
        ResearchSource(
            topic="Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理",
            capability="legal_case_intake_mass_tort_lead_governance",
            title="Google Local Services Ads, How leads work",
            url="https://support.google.com/localservices/answer/7195435",
            publisher="Google Local Services Help",
            source_type="local_services_reference",
            reliability="primary",
            claim_summary=(
                "Local Services leads 支撑 legal / professional services 的 charged lead、"
                "valid lead、service area 和 buyer feedback 语境。"
            ),
        ),
        ResearchSource(
            topic="Home Services、Solar 与 Local Services Lead 治理",
            capability="home_services_solar_local_services_lead_governance",
            title="Google Local Services Ads, How leads work",
            url="https://support.google.com/localservices/answer/7195435",
            publisher="Google Local Services Help",
            source_type="local_services_reference",
            reliability="primary",
            claim_summary=(
                "How leads work 支撑 valid lead、charged lead、lead type、"
                "budget、credit 和 LSA lead 口径。"
            ),
        ),
        ResearchSource(
            topic="Home Services、Solar 与 Local Services Lead 治理",
            capability="home_services_solar_local_services_lead_governance",
            title="Google Local Services Ads, Screening and verification process",
            url="https://support.google.com/localservices/answer/6226575",
            publisher="Google Local Services Help",
            source_type="local_services_reference",
            reliability="primary",
            claim_summary=(
                "Screening and verification 支撑 contractor background、business "
                "registration、insurance、license 和 review requirements。"
            ),
        ),
        ResearchSource(
            topic="Home Services、Solar 与 Local Services Lead 治理",
            capability="home_services_solar_local_services_lead_governance",
            title="Google Ads Policy, Local Services platform policies",
            url="https://support.google.com/adspolicy/answer/6245891",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Local Services platform policies 支撑 service provider、agency、"
                "lead generation、aggregator 的本地服务平台边界。"
            ),
        ),
        ResearchSource(
            topic="Home Services、Solar 与 Local Services Lead 治理",
            capability="home_services_solar_local_services_lead_governance",
            title="Google Business Profile, Guidelines for representing your business",
            url="https://support.google.com/business/answer/3038177",
            publisher="Google Business Profile Help",
            source_type="local_business_reference",
            reliability="primary",
            claim_summary=(
                "Business Profile guidelines 支撑真实业务名称、地址、service area "
                "和本地业务资料一致性。"
            ),
        ),
        ResearchSource(
            topic="Home Services、Solar 与 Local Services Lead 治理",
            capability="home_services_solar_local_services_lead_governance",
            title="FTC, How To Avoid a Home Improvement Scam",
            url="https://consumer.ftc.gov/articles/how-avoid-home-improvement-scam",
            publisher="Federal Trade Commission",
            source_type="consumer_protection",
            reliability="primary",
            claim_summary=(
                "Home improvement scam guidance 支撑 contractor、付款、pressure tactic、"
                "estimate 和 home improvement claim 审核。"
            ),
        ),
        ResearchSource(
            topic="Home Services、Solar 与 Local Services Lead 治理",
            capability="home_services_solar_local_services_lead_governance",
            title="FTC, Solar Power for Your Home",
            url="https://consumer.ftc.gov/articles/solar-power-your-home",
            publisher="Federal Trade Commission",
            source_type="consumer_protection",
            reliability="primary",
            claim_summary=(
                "Solar Power for Your Home 支撑 solar savings、lease/PPA、tax credit、"
                "PACE financing、roof/utility 条件和 installer 评估。"
            ),
        ),
        ResearchSource(
            topic="Education、Career Training 与 Student Lead 治理",
            capability="education_career_training_student_lead_governance",
            title="Google Ads Policy, Misrepresentation",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation policy 支撑学校主体、认证、费用、资助、"
                "就业结果和重要限制透明度。"
            ),
        ),
        ResearchSource(
            topic="Education、Career Training 与 Student Lead 治理",
            capability="education_career_training_student_lead_governance",
            title="Google Ads Policy, Personalized advertising",
            url="https://support.google.com/adspolicy/answer/143465",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Personalized advertising policy 支撑敏感身份、未成年人、"
                "财务困难和教育相关个性化广告边界。"
            ),
        ),
        ResearchSource(
            topic="Education、Career Training 与 Student Lead 治理",
            capability="education_career_training_student_lead_governance",
            title="FTC, Guides for Private Vocational and Distance Education Schools",
            url="https://www.ftc.gov/legal-library/browse/rules/private-vocational-distance-education-schools",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "FTC vocational and distance education guides 支撑 accreditation、"
                "就业前景、入学资格和 deceptive education claim 治理。"
            ),
        ),
        ResearchSource(
            topic="Education、Career Training 与 Student Lead 治理",
            capability="education_career_training_student_lead_governance",
            title="U.S. Department of Education, College Accreditation",
            url="https://www.ed.gov/laws-and-policy/higher-education-laws-and-policy/college-accreditation",
            publisher="U.S. Department of Education",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "College Accreditation 支撑学校/项目认证、认可机构和"
                "认证来源核验。"
            ),
        ),
        ResearchSource(
            topic="Education、Career Training 与 Student Lead 治理",
            capability="education_career_training_student_lead_governance",
            title="College Scorecard",
            url="https://collegescorecard.ed.gov/",
            publisher="U.S. Department of Education",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "College Scorecard 支撑 cost、fields of study、graduation、"
                "debt、earnings 和 school comparison。"
            ),
        ),
        ResearchSource(
            topic="Education、Career Training 与 Student Lead 治理",
            capability="education_career_training_student_lead_governance",
            title="Federal Student Aid, Avoid student loan debt relief scams",
            url="https://studentaid.gov/resources/scams",
            publisher="Federal Student Aid",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "Student loan debt relief scams guidance 支撑 student loan、"
                "政府冒充、收费代办和教育债务 claim 风险判断。"
            ),
        ),
        ResearchSource(
            topic="Healthcare、Medical Appointment 与 Clinic Lead 治理",
            capability="healthcare_medical_appointment_lead_governance",
            title="Google Ads Policy, Healthcare and medicines",
            url="https://support.google.com/adspolicy/answer/176031",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Healthcare and medicines policy 支撑医疗、药品、认证、"
                "地区和禁止内容边界。"
            ),
        ),
        ResearchSource(
            topic="Healthcare、Medical Appointment 与 Clinic Lead 治理",
            capability="healthcare_medical_appointment_lead_governance",
            title="Google Ads Policy, Personalized advertising",
            url="https://support.google.com/adspolicy/answer/143465",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Personalized advertising policy 支撑健康状态、敏感兴趣和"
                "医疗相关个性化广告限制。"
            ),
        ),
        ResearchSource(
            topic="Healthcare、Medical Appointment 与 Clinic Lead 治理",
            capability="healthcare_medical_appointment_lead_governance",
            title="HHS OCR, HIPAA Privacy Rule",
            url="https://www.hhs.gov/hipaa/for-professionals/privacy/index.html",
            publisher="U.S. Department of Health and Human Services",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "HIPAA Privacy Rule 支撑 PHI、covered entity、privacy safeguards "
                "和医疗数据治理语境。"
            ),
        ),
        ResearchSource(
            topic="Healthcare、Medical Appointment 与 Clinic Lead 治理",
            capability="healthcare_medical_appointment_lead_governance",
            title="HHS OCR, Use of Online Tracking Technologies",
            url="https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html",
            publisher="U.S. Department of Health and Human Services",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Online tracking guidance 支撑医疗页面 pixel、analytics、"
                "tracking tech 和 PHI 泄露风险。"
            ),
        ),
        ResearchSource(
            topic="Healthcare、Medical Appointment 与 Clinic Lead 治理",
            capability="healthcare_medical_appointment_lead_governance",
            title="FTC, Health Products Compliance Guidance",
            url="https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Health Products Compliance Guidance 支撑健康产品、疗效 claim "
                "和 substantiation 审核。"
            ),
        ),
        ResearchSource(
            topic="Healthcare、Medical Appointment 与 Clinic Lead 治理",
            capability="healthcare_medical_appointment_lead_governance",
            title="CMS, Good Faith Estimate",
            url="https://www.cms.gov/medical-bill-rights/help/guides/good-faith-estimate",
            publisher="Centers for Medicare & Medicaid Services",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "Good Faith Estimate 支撑 uninsured/self-pay 费用预估、"
                "No Surprises Act 和费用 claim 风险。"
            ),
        ),
        ResearchSource(
            topic="B2B SaaS、Professional Services 与 Demo Lead 治理",
            capability="b2b_saas_professional_services_lead_governance",
            title="Google Ads Policy, Misrepresentation",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation policy 支撑主体、价格、功能、官方关系、"
                "trial 和重要限制透明度。"
            ),
        ),
        ResearchSource(
            topic="B2B SaaS、Professional Services 与 Demo Lead 治理",
            capability="b2b_saas_professional_services_lead_governance",
            title="Google Ads Policy, Trademarks",
            url="https://support.google.com/adspolicy/answer/6118",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Trademarks policy 支撑竞品词、商标、ad text、reseller "
                "和 informational site 边界。"
            ),
        ),
        ResearchSource(
            topic="B2B SaaS、Professional Services 与 Demo Lead 治理",
            capability="b2b_saas_professional_services_lead_governance",
            title="Google Ads Policy, Unwanted software",
            url="https://support.google.com/adspolicy/answer/15938073",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Unwanted software policy 支撑软件下载、插件、安装器、"
                "权限和透明度边界。"
            ),
        ),
        ResearchSource(
            topic="B2B SaaS、Professional Services 与 Demo Lead 治理",
            capability="b2b_saas_professional_services_lead_governance",
            title="Google Ads Help, About lead form assets",
            url="https://support.google.com/google-ads/answer/9423234",
            publisher="Google Ads Help",
            source_type="platform_documentation",
            reliability="primary",
            claim_summary=(
                "Lead form assets documentation 支撑 B2B lead form、隐私政策、"
                "字段和 webhook 边界。"
            ),
        ),
        ResearchSource(
            topic="B2B SaaS、Professional Services 与 Demo Lead 治理",
            capability="b2b_saas_professional_services_lead_governance",
            title="Google Ads Customer data policies",
            url="https://support.google.com/google-ads/answer/7475709",
            publisher="Google Ads Help",
            source_type="platform_documentation",
            reliability="primary",
            claim_summary=(
                "Customer data policies 支撑 Customer Match、用户提供数据、"
                "披露和 consent 治理。"
            ),
        ),
        ResearchSource(
            topic="B2B SaaS、Professional Services 与 Demo Lead 治理",
            capability="b2b_saas_professional_services_lead_governance",
            title="FTC, Protecting Personal Information",
            url="https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business",
            publisher="Federal Trade Commission",
            source_type="privacy_guidance",
            reliability="primary",
            claim_summary=(
                "Protecting Personal Information 支撑 B2B 联系人数据最小化、"
                "保留、安全和删除。"
            ),
        ),
        ResearchSource(
            topic="Crypto、Investment 与 Trading Lead 治理",
            capability="crypto_investment_trading_lead_governance",
            title="Google Ads Policy, Cryptocurrencies and related products",
            url="https://support.google.com/adspolicy/answer/14009787",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Cryptocurrencies and related products policy 支撑 crypto exchange、"
                "wallet、coin trust、NFT、certification 和禁止/受限范围。"
            ),
        ),
        ResearchSource(
            topic="Crypto、Investment 与 Trading Lead 治理",
            capability="crypto_investment_trading_lead_governance",
            title="Google Ads Policy, Financial products and services",
            url="https://support.google.com/adspolicy/answer/2464998",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Financial products and services policy 支撑金融产品、费用、主体、"
                "地区、披露和金融服务政策。"
            ),
        ),
        ResearchSource(
            topic="Crypto、Investment 与 Trading Lead 治理",
            capability="crypto_investment_trading_lead_governance",
            title="SEC, Crypto Assets and Emerging Technology",
            url="https://www.sec.gov/securities-topics/crypto-assets",
            publisher="U.S. Securities and Exchange Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "SEC crypto assets topic 支撑 digital asset、securities law "
                "和 investor protection 语境。"
            ),
        ),
        ResearchSource(
            topic="Crypto、Investment 与 Trading Lead 治理",
            capability="crypto_investment_trading_lead_governance",
            title="Investor.gov, Red Flags of Investment Fraud Checklist",
            url="https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud/red-flags-investment-fraud-checklist",
            publisher="Investor.gov",
            source_type="investor_protection",
            reliability="primary",
            claim_summary=(
                "Investment fraud red flags 支撑 guaranteed return、pressure tactic、"
                "unregistered seller 和 fraud pattern 审核。"
            ),
        ),
        ResearchSource(
            topic="Crypto、Investment 与 Trading Lead 治理",
            capability="crypto_investment_trading_lead_governance",
            title="FINRA, Crypto Assets Risks",
            url="https://www.finra.org/investors/investing/investment-products/crypto-assets/risks",
            publisher="Financial Industry Regulatory Authority",
            source_type="investor_protection",
            reliability="primary",
            claim_summary=(
                "FINRA crypto asset risks 支撑 unregistered entities、volatility、"
                "custody 和 crypto investor risk 审核。"
            ),
        ),
        ResearchSource(
            topic="Crypto、Investment 与 Trading Lead 治理",
            capability="crypto_investment_trading_lead_governance",
            title="CFTC, Digital Asset Frauds",
            url="https://www.cftc.gov/LearnAndProtect/digitalassetfrauds",
            publisher="Commodity Futures Trading Commission",
            source_type="investor_protection",
            reliability="primary",
            claim_summary=(
                "Digital asset fraud guidance 支撑 fake platform、withdrawal scam、"
                "pump-and-dump 和 complaint risk。"
            ),
        ),
        ResearchSource(
            topic="Employment、Recruiting 与 Staffing Lead 治理",
            capability="employment_recruiting_staffing_lead_governance",
            title="Google Ads Policy, Personalized advertising",
            url="https://support.google.com/adspolicy/answer/143465",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Personalized advertising policy 支撑 employment opportunity、"
                "hiring 和 HEC targeting 限制。"
            ),
        ),
        ResearchSource(
            topic="Employment、Recruiting 与 Staffing Lead 治理",
            capability="employment_recruiting_staffing_lead_governance",
            title="Google Ads Policy, Housing, employment, and credit FAQ",
            url="https://support.google.com/adspolicy/answer/9997418",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Housing, employment, and credit FAQ 支撑美国/加拿大 employment ads "
                "scope、policy acceptance 和 appeal 语境。"
            ),
        ),
        ResearchSource(
            topic="Employment、Recruiting 与 Staffing Lead 治理",
            capability="employment_recruiting_staffing_lead_governance",
            title="FTC, Job Scams",
            url="https://consumer.ftc.gov/articles/job-scams",
            publisher="Federal Trade Commission",
            source_type="consumer_protection",
            reliability="primary",
            claim_summary=(
                "Job scams guidance 支撑 job scam、placement firm fee、"
                "government/postal job scam 和求职安全。"
            ),
        ),
        ResearchSource(
            topic="Employment、Recruiting 与 Staffing Lead 治理",
            capability="employment_recruiting_staffing_lead_governance",
            title="EEOC, Prohibited Employment Policies/Practices",
            url="https://www.eeoc.gov/prohibited-employment-policiespractices",
            publisher="U.S. Equal Employment Opportunity Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "EEOC prohibited practices 支撑 job ad、recruitment、application "
                "和 protected-class discrimination 边界。"
            ),
        ),
        ResearchSource(
            topic="Employment、Recruiting 与 Staffing Lead 治理",
            capability="employment_recruiting_staffing_lead_governance",
            title="DOL, Misclassification of Employees as Independent Contractors",
            url="https://www.dol.gov/agencies/whd/flsa/misclassification",
            publisher="U.S. Department of Labor",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "DOL misclassification guidance 支撑 employee vs independent contractor "
                "和 FLSA misclassification 风险。"
            ),
        ),
        ResearchSource(
            topic="Employment、Recruiting 与 Staffing Lead 治理",
            capability="employment_recruiting_staffing_lead_governance",
            title="FTC, Background Checks: What Employers Need to Know",
            url="https://www.ftc.gov/business-guidance/resources/background-checks-what-employers-need-know",
            publisher="Federal Trade Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Background checks guidance 支撑 employment background reports、"
                "written permission、FCRA 和 adverse action 语境。"
            ),
        ),
        ResearchSource(
            topic="Gambling、Sweepstakes 与 Sports Betting Lead 治理",
            capability="gambling_sweepstakes_sports_betting_lead_governance",
            title="Google Ads Policy, Gambling and games",
            url="https://support.google.com/adspolicy/answer/6018017",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Gambling and games policy 支撑 gambling-related content、online "
                "gambling、social casino、certification 和 country restrictions。"
            ),
        ),
        ResearchSource(
            topic="Gambling、Sweepstakes 与 Sports Betting Lead 治理",
            capability="gambling_sweepstakes_sports_betting_lead_governance",
            title="Google Ads Policy, Personalized advertising",
            url="https://support.google.com/adspolicy/answer/143465",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Personalized advertising policy 支撑 gambling / location-based "
                "gambling sensitive interest targeting 限制。"
            ),
        ),
        ResearchSource(
            topic="Gambling、Sweepstakes 与 Sports Betting Lead 治理",
            capability="gambling_sweepstakes_sports_betting_lead_governance",
            title="FTC, Fake Prize, Sweepstakes, and Lottery Scams",
            url="https://consumer.ftc.gov/articles/fake-prize-sweepstakes-and-lottery-scams",
            publisher="Federal Trade Commission",
            source_type="consumer_protection",
            reliability="primary",
            claim_summary=(
                "Fake prize and sweepstakes guidance 支撑 prize scam、"
                "预付费领奖和个人信息风险。"
            ),
        ),
        ResearchSource(
            topic="Gambling、Sweepstakes 与 Sports Betting Lead 治理",
            capability="gambling_sweepstakes_sports_betting_lead_governance",
            title="New York State Gaming Commission, Advertising Restrictions",
            url="https://gaming.ny.gov/advertising-restrictions",
            publisher="New York State Gaming Commission",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Advertising Restrictions 支撑 sports wagering advertising、"
                "responsible gambling message 和 licensee responsibility。"
            ),
        ),
        ResearchSource(
            topic="Gambling、Sweepstakes 与 Sports Betting Lead 治理",
            capability="gambling_sweepstakes_sports_betting_lead_governance",
            title="New Jersey DGE, Advertising Standards Best Practices",
            url="https://www.nj.gov/oag/ge/docs/BestPractices/AdvertisingBestPractices.pdf",
            publisher="New Jersey Division of Gaming Enforcement",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Advertising standards best practices 支撑 responsible gaming、"
                "prohibited / risky marketing practices 和 disclosure。"
            ),
        ),
        ResearchSource(
            topic="Gambling、Sweepstakes 与 Sports Betting Lead 治理",
            capability="gambling_sweepstakes_sports_betting_lead_governance",
            title="National Council on Problem Gambling",
            url="https://www.ncpgambling.org/ncpg/",
            publisher="National Council on Problem Gambling",
            source_type="responsible_gambling_reference",
            reliability="primary",
            claim_summary=(
                "NCPG resources 支撑 problem gambling resources、helpline "
                "和 responsible gambling 语境。"
            ),
        ),
        ResearchSource(
            topic="Addiction Treatment、Rehab 与 Behavioral Health Lead 治理",
            capability="addiction_treatment_rehab_behavioral_health_lead_governance",
            title="Google Ads Policy, Healthcare and medicines",
            url="https://support.google.com/adspolicy/answer/176031",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Healthcare and medicines policy 支撑 addiction services certification、"
                "healthcare policy 和 restricted medical content 边界。"
            ),
        ),
        ResearchSource(
            topic="Addiction Treatment、Rehab 与 Behavioral Health Lead 治理",
            capability="addiction_treatment_rehab_behavioral_health_lead_governance",
            title="LegitScript, Addiction Treatment Certification Process",
            url="https://www.legitscript.com/certification/addiction-treatment-certification/addiction-treatment-certification-process/",
            publisher="LegitScript",
            source_type="certification_reference",
            reliability="primary",
            claim_summary=(
                "Addiction Treatment Certification Process 支撑 addiction treatment "
                "advertising certification、provider/referral scope 和 platform trust。"
            ),
        ),
        ResearchSource(
            topic="Addiction Treatment、Rehab 与 Behavioral Health Lead 治理",
            capability="addiction_treatment_rehab_behavioral_health_lead_governance",
            title="SAMHSA, Find Substance Use Disorder Treatment",
            url="https://www.samhsa.gov/substance-use/treatment/find-treatment/",
            publisher="Substance Abuse and Mental Health Services Administration",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "Find Substance Use Disorder Treatment 支撑 official treatment locator、"
                "treatment options 和 public resource。"
            ),
        ),
        ResearchSource(
            topic="Addiction Treatment、Rehab 与 Behavioral Health Lead 治理",
            capability="addiction_treatment_rehab_behavioral_health_lead_governance",
            title="HHS, Understanding Confidentiality of SUD Patient Records / Part 2",
            url="https://www.hhs.gov/hipaa/for-professionals/special-topics/hipaa-part-2/index.html",
            publisher="U.S. Department of Health and Human Services",
            source_type="privacy_guidance",
            reliability="primary",
            claim_summary=(
                "Part 2 guidance 支撑 SUD patient record confidentiality、"
                "complaint path 和敏感数据治理。"
            ),
        ),
        ResearchSource(
            topic="Addiction Treatment、Rehab 与 Behavioral Health Lead 治理",
            capability="addiction_treatment_rehab_behavioral_health_lead_governance",
            title="HHS OCR, Use of Online Tracking Technologies",
            url="https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html",
            publisher="U.S. Department of Health and Human Services",
            source_type="privacy_guidance",
            reliability="primary",
            claim_summary=(
                "Online tracking guidance 支撑 SUD / behavioral health 页面 pixel、"
                "analytics、tracking tech 和 PHI 泄露风险。"
            ),
        ),
        ResearchSource(
            topic="Addiction Treatment、Rehab 与 Behavioral Health Lead 治理",
            capability="addiction_treatment_rehab_behavioral_health_lead_governance",
            title="Florida Statutes 817.505, Patient brokering prohibited",
            url="https://www.flsenate.gov/Laws/Statutes/2024/0817.505",
            publisher="The Florida Senate",
            source_type="regulatory_context",
            reliability="primary",
            claim_summary=(
                "Patient brokering statute 支撑 kickback、referral payment、"
                "travel incentive 和 ethical referral 风险治理。"
            ),
        ),
        ResearchSource(
            topic="Government Services、Immigration 与 Public Benefits Lead 治理",
            capability="government_services_immigration_public_benefits_lead_governance",
            title="Google Ads Policy, Government documents and services",
            url="https://support.google.com/adspolicy/answer/13156083",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Government documents and services policy 支撑 government service "
                "scope、authorized provider、certification 和非政府网站披露。"
            ),
        ),
        ResearchSource(
            topic="Government Services、Immigration 与 Public Benefits Lead 治理",
            capability="government_services_immigration_public_benefits_lead_governance",
            title="Google Ads Policy, Misrepresentation",
            url="https://support.google.com/adspolicy/answer/6020955",
            publisher="Google Ads Policy Help",
            source_type="advertising_policy",
            reliability="primary",
            claim_summary=(
                "Misrepresentation policy 支撑 official relationship、government "
                "identity、pricing、business identity 和误导 claim 治理。"
            ),
        ),
        ResearchSource(
            topic="Government Services、Immigration 与 Public Benefits Lead 治理",
            capability="government_services_immigration_public_benefits_lead_governance",
            title="FTC, How To Avoid Immigration Scams and Get Real Help",
            url="https://consumer.ftc.gov/articles/how-avoid-immigration-scams-and-get-real-help",
            publisher="Federal Trade Commission",
            source_type="consumer_protection_guidance",
            reliability="primary",
            claim_summary=(
                "Immigration scams guidance 支撑 notario scam、official forms、"
                "real immigration help 和付款风险提示。"
            ),
        ),
        ResearchSource(
            topic="Government Services、Immigration 与 Public Benefits Lead 治理",
            capability="government_services_immigration_public_benefits_lead_governance",
            title="USCIS, Avoid Scams",
            url="https://www.uscis.gov/scams-fraud-and-misconduct/avoid-scams",
            publisher="U.S. Citizenship and Immigration Services",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "USCIS Avoid Scams 支撑移民服务反诈、official USCIS source "
                "和第三方冒充风险治理。"
            ),
        ),
        ResearchSource(
            topic="Government Services、Immigration 与 Public Benefits Lead 治理",
            capability="government_services_immigration_public_benefits_lead_governance",
            title="USCIS, Find Legal Services",
            url="https://www.uscis.gov/scams-fraud-and-misconduct/avoid-scams/find-legal-services",
            publisher="U.S. Citizenship and Immigration Services",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "Find Legal Services 支撑 attorney、DOJ accredited representative "
                "和授权移民帮助边界。"
            ),
        ),
        ResearchSource(
            topic="Government Services、Immigration 与 Public Benefits Lead 治理",
            capability="government_services_immigration_public_benefits_lead_governance",
            title='USA.gov, Avoid "free money" from the government scams',
            url="https://www.usa.gov/no-free-money",
            publisher="USA.gov",
            source_type="official_government_reference",
            reliability="primary",
            claim_summary=(
                "No free money guidance 支撑 government grant、public benefits、"
                "free money scam、Benefits.gov 和 Grants.gov 官方路径。"
            ),
        ),
    ]
