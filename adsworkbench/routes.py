from __future__ import annotations

import csv
from datetime import datetime
from io import StringIO
from pathlib import Path

from flask import (
    Blueprint,
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .extensions import db
from .models import (
    AdsAccount,
    AdReviewCase,
    AppointmentLeadReview,
    AttributionReview,
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
    add_audit,
    decimal_value,
)
from .services.analytics import metric_totals, recommended_actions
from .services.appointment_lead import calculate_appointment_lead_review
from .services.attribution import calculate_attribution_review
from .services.bulk_upload import calculate_bulk_upload_review
from .services.budget_pacing import calculate_budget_pacing
from .services.buyer_capacity import calculate_buyer_capacity_review
from .services.calculator import calculate_opportunity
from .services.claim_review import audit_creative_claims
from .services.conversion_signal import calculate_conversion_signal_review
from .services.crm_value_mapping import calculate_crm_value_mapping_review
from .services.cpl_vertical import calculate_cpl_vertical_review
from .services.creative import generate_creative_sets
from .services.decision_window import calculate_decision_window
from .services.exporters import campaign_to_google_ads_editor_csv
from .services.exporters import campaign_to_scripts_payload
from .services.landing import audit_landing_page
from .services.lead_pricing import calculate_lead_pricing_review
from .services.markdown_render import render_markdown
from .services.offer_cap import calculate_offer_cap_review
from .services.ping_post_routing import calculate_ping_post_routing_review
from .services.preflight import campaign_preflight_blockers
from .services.portfolio import calculate_portfolio_allocation
from .services.query_mining import calculate_query_mining_review
from .services.script_sync import calculate_script_sync_review
from .services.source_quality import calculate_source_quality_review
from .services.taxonomy import calculate_taxonomy_review
from .services.tasks import (
    TASK_TYPES,
    run_task_job,
    validate_task_text,
    validate_task_type,
)
from .services.vendor_contract import calculate_vendor_contract_review

bp = Blueprint("main", __name__)

RISK_CAPABILITIES = [
    ("ads_cookie_backend_operation", "Ads Cookie 登录和后台操作"),
    ("automated_login_2fa_challenge_bypass", "自动绕过登录、2FA、安全挑战"),
    ("invalid_traffic_click_impression_simulation", "补点击、刷展示、模拟自然流量"),
    ("proxy_fingerprint_worker_association_evasion", "代理、指纹、Worker 转发规避关联检测"),
    ("cloaking_review_user_page_mismatch", "Cloaking 或审核页/用户页不一致"),
    ("ban_evasion_account_switching", "为规避封禁创建或切换账号"),
    ("audience_remarketing_customer_match_policy", "受众、再营销、Customer Match 与 Personalized Ads"),
]

RISK_AUDIT_STATUSES = {
    "open": "待处理",
    "reviewed": "已复核",
    "mitigated": "已缓解",
    "rejected": "已拒绝",
}

CAMPAIGN_DRAFT_STATUSES = {
    "draft": "草稿",
    "reviewing": "评审中",
    "approved": "已批准",
    "exported": "已导出",
    "paused": "暂停",
    "rejected": "拒绝",
}

LINK_RULE_STATUSES = {
    "draft": "草稿",
    "reviewing": "评审中",
    "approved": "已批准",
    "rotated": "已轮换",
    "paused": "暂停",
    "rejected": "拒绝",
}

OPTIMIZATION_ACTION_STATUSES = {
    "open": "待处理",
    "manual_review": "转人工处理",
    "resolved": "已解决",
    "dismissed": "已关闭",
}

SOURCE_REVIEW_STATUSES = {
    "candidate": "待复核",
    "accepted": "已采纳",
    "needs_update": "需更新",
    "archived": "已归档",
}

CLAIM_REVIEW_STATUSES = {
    "open": "待复核",
    "approved": "可保留",
    "rewrite_required": "需降级改写",
    "blocked": "已阻止",
    "dismissed": "已关闭",
}

AD_REVIEW_CASE_STATUSES = {
    "open": "待处理",
    "fixed": "已修复",
    "appeal_ready": "申诉证据就绪",
    "appeal_submitted": "已提交申诉",
    "approved": "已通过",
    "rejected": "申诉失败",
    "abandoned": "已放弃",
}

DECISION_WINDOW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "waiting": "等待回传",
    "ramp_ready": "可小幅扩量",
    "blocked": "阻止扩量",
    "closed": "已关闭",
}

BUDGET_PACING_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "waiting": "等待回传",
    "approved_for_manual_change": "人工改预算已批准",
    "reduced": "已建议降预算",
    "blocked": "阻止扩量",
    "closed": "已关闭",
}

PORTFOLIO_ALLOCATION_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "waiting": "等待回款",
    "approved_for_manual_allocation": "人工分配已批准",
    "reduce_exposure": "降低集中度",
    "quarantine": "隔离观察",
    "closed": "已关闭",
}

OFFER_CAP_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "waiting_cap_update": "等待 Cap 更新",
    "reduce_budget": "降低预算",
    "pause_traffic": "暂停流量",
    "manual_replacement_ready": "人工替代就绪",
    "closed": "已关闭",
}

SOURCE_QUALITY_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "allowlist": "加入 allowlist",
    "watchlist": "加入 watchlist",
    "quarantine": "隔离观察",
    "blocklist": "加入 blocklist",
    "retest": "等待复测",
    "closed": "已关闭",
}

VENDOR_CONTRACT_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "preapproved": "允许小测",
    "active_test": "小测中",
    "active_scale": "可扩量",
    "watchlist": "观察名单",
    "dispute_open": "争议处理中",
    "suspended": "暂停采购",
    "blocked": "禁止合作",
    "closed": "已关闭",
}

QUERY_MINING_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "negative_proposed": "否定词待审核",
    "promotion_proposed": "加词待审核",
    "page_brief": "页面 Brief 待处理",
    "risk_review": "风险复核",
    "applied": "已人工执行",
    "dismissed": "已忽略",
    "closed": "已关闭",
}

BULK_UPLOAD_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "preview_ready": "预览通过",
    "approved_for_manual_post": "人工发布已批准",
    "posted_manual": "已人工发布",
    "partial_error": "部分失败待修复",
    "rollback_review": "回滚复核",
    "blocked": "阻止发布",
    "closed": "已关闭",
}

SCRIPT_SYNC_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "snapshot_ready": "快照可用",
    "rerun_required": "需要重拉",
    "conflict_review": "冲突复核",
    "approved_for_import": "人工导入已批准",
    "imported_manual": "已人工导入",
    "blocked": "阻止使用",
    "closed": "已关闭",
}

TAXONOMY_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "dictionary_ready": "字典已确认",
    "mapping_fix": "映射待修",
    "export_ready": "可导出",
    "qa_failed": "QA 失败",
    "blocked": "阻止导出",
    "closed": "已关闭",
}

ATTRIBUTION_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "holdout_planned": "Holdout 已规划",
    "experiment_running": "实验中",
    "evidence_ready": "证据就绪",
    "small_ramp": "小幅扩量",
    "scale_ready": "可进入核心预算",
    "cannibalization_review": "蚕食复核",
    "blocked": "阻止扩量",
    "closed": "已关闭",
}

CPL_VERTICAL_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "field_mapping": "字段映射中",
    "buyer_terms_review": "Buyer 条款复核",
    "policy_review": "政策复核",
    "test_ready": "可小测",
    "scale_ready": "可扩量",
    "blocked": "阻止放量",
    "closed": "已关闭",
}

LEAD_PRICING_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "rate_card_review": "Rate card 复核",
    "evidence_needed": "补质量证据",
    "buyer_terms_review": "Buyer 条款复核",
    "reserve_review": "安全垫复核",
    "negotiation_ready": "谈价材料就绪",
    "test_ready": "可小测",
    "blocked": "阻止放量",
    "closed": "已关闭",
}

APPOINTMENT_LEAD_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "calendar_review": "Calendar 容量复核",
    "reminder_review": "提醒流程复核",
    "buyer_terms_review": "Buyer 条款复核",
    "conversion_mapping": "回传映射复核",
    "no_show_fix": "No-show 修复",
    "test_ready": "可小测",
    "scale_ready": "可扩量",
    "blocked": "阻止放量",
    "closed": "已关闭",
}

BUYER_CAPACITY_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "cap_refresh": "Cap 快照重拉",
    "hours_review": "营业时间复核",
    "schedule_review": "广告时段复核",
    "holiday_review": "假日日历复核",
    "routing_review": "Fallback / routing 复核",
    "reduce_budget": "建议降预算",
    "pause_traffic": "建议暂停流量",
    "test_ready": "可小测",
    "scale_ready": "可扩量",
    "blocked": "阻止放量",
    "closed": "已关闭",
}

CONVERSION_SIGNAL_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "tracking_fix": "追踪修复",
    "dedupe_fix": "去重修复",
    "value_review": "Value 复核",
    "lag_review": "Lag 复核",
    "goal_review": "Goal 复核",
    "secondary_only": "仅做 secondary",
    "primary_candidate": "Primary 候选",
    "bid_ready": "出价就绪",
    "blocked": "阻止放量",
    "closed": "已关闭",
}

CRM_VALUE_MAPPING_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "stage_map_review": "Stage 映射复核",
    "action_map_review": "Action 映射复核",
    "value_review": "Value 复核",
    "dedupe_fix": "去重修复",
    "import_qa": "导入 QA",
    "adjustment_review": "Adjustment 复核",
    "lag_review": "Lag 复核",
    "secondary_only": "仅做 secondary",
    "primary_candidate": "Primary 候选",
    "upload_candidate": "导入候选",
    "blocked": "阻止放量",
    "closed": "已关闭",
}

PING_POST_ROUTING_REVIEW_STATUSES = {
    "open": "待复核",
    "reviewed": "已复核",
    "consent_review": "Consent / disclosure 复核",
    "field_minimization": "字段最小化复核",
    "cap_refresh": "Cap 快照重拉",
    "routing_review": "Routing 复核",
    "fallback_review": "Fallback 复核",
    "buyer_feedback_review": "Buyer feedback 复核",
    "suppression_review": "Suppression / DNC 复核",
    "manual_test": "人工小测",
    "routing_ready": "Routing 就绪",
    "blocked": "阻止投放",
    "closed": "已关闭",
}

BLOCKED_AD_REVIEW_TERMS = (
    "cloaking",
    "cloak",
    "bypass review",
    "evade review",
    "review page",
    "user page",
    "googlebot",
    "adsbot",
    "cookie",
    "session token",
    "2fa",
    "mfa",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "account pool",
    "switch account",
    "ban evasion",
    "审核页",
    "用户页",
    "绕审核",
    "规避审核",
    "隐藏真实",
    "换号",
    "账号池",
    "封禁后",
    "代理池",
    "指纹",
    "cookie",
)

BLOCKED_LINK_PLAN_TERMS = (
    "cloaking",
    "cloak",
    "googlebot",
    "adsbot",
    "bot-only",
    "bot only",
    "review page",
    "user page",
    "bypass review",
    "evade review",
    "worker forward",
    "worker tunnel",
    "proxy pool",
    "fingerprint",
    "anti-detect",
    "antidetect",
    "hidden destination",
    "审核页",
    "用户页",
    "绕审核",
    "规避审核",
    "隐藏真实",
    "隐藏目的地",
    "worker转发",
    "代理池",
    "指纹",
    "反检测",
)

BLOCKED_ACCOUNT_TERMS = (
    "cookie login",
    "cookie operation",
    "cookie import",
    "cookie injection",
    "cookie reuse",
    "store cookie",
    "session token",
    "browser profile",
    "profile hosting",
    "login automation",
    "2fa bypass",
    "mfa bypass",
    "captcha solver",
    "challenge bypass",
    "proxy pool",
    "fingerprint profile",
    "anti-detect",
    "antidetect",
    "worker forward",
    "ban evasion",
    "evade ban",
    "account pool",
    "bulk account",
    "anti association",
    "anti-association",
    "cookie登录",
    "cookie操作",
    "cookie接管",
    "cookie注入",
    "cookie复用",
    "登录态",
    "session token",
    "浏览器profile",
    "浏览器 profile",
    "自动登录",
    "绕过2fa",
    "绕过 2fa",
    "绕过mfa",
    "验证码",
    "安全挑战",
    "代理池",
    "指纹profile",
    "指纹 profile",
    "反检测",
    "worker转发",
    "封禁后",
    "规避封禁",
    "绕过封禁",
    "换号继续",
    "账号池",
    "批量开户",
    "防关联",
    "不断号",
    "换壳",
)

BLOCKED_OFFER_ACTION_TERMS = (
    "cloaking",
    "cloak",
    "review page",
    "user page",
    "bypass review",
    "evade review",
    "googlebot",
    "adsbot",
    "cookie",
    "session token",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "anti-detect",
    "ban evasion",
    "switch account",
    "account pool",
    "cookie stuffing",
    "审核页",
    "用户页",
    "绕审核",
    "规避审核",
    "隐藏真实",
    "隐藏目的地",
    "代理池",
    "指纹",
    "worker转发",
    "反检测",
    "换号",
    "账号池",
    "封禁后",
    "cookie stuffing",
)

BLOCKED_SOURCE_QUALITY_TERMS = (
    "cloaking",
    "cloak",
    "review page",
    "user page",
    "bypass review",
    "evade review",
    "hide referrer",
    "hidden referrer",
    "hidden source",
    "fake source",
    "natural traffic",
    "organic simulation",
    "bot traffic",
    "click bot",
    "impression bot",
    "simulate browser",
    "session generator",
    "proxy pool",
    "fingerprint",
    "anti-detect",
    "antidetect",
    "worker forward",
    "cookie",
    "session token",
    "switch account",
    "account pool",
    "ban evasion",
    "cookie stuffing",
    "审核页",
    "用户页",
    "绕审核",
    "规避审核",
    "隐藏来源",
    "隐藏 referrer",
    "隐藏referer",
    "隐藏真实",
    "自然流量模拟",
    "模拟自然流量",
    "刷点击",
    "刷展示",
    "补点击",
    "补展示",
    "机器人流量",
    "代理池",
    "指纹",
    "反检测",
    "worker转发",
    "换号",
    "账号池",
    "封禁后",
)

BLOCKED_VENDOR_CONTRACT_TERMS = (
    "cloaking",
    "cloak",
    "review page",
    "user page",
    "bypass review",
    "evade review",
    "hide referrer",
    "hidden referrer",
    "hidden source",
    "undisclosed source",
    "undisclosed subnetwork",
    "undisclosed sub-network",
    "fake source",
    "natural traffic",
    "organic simulation",
    "bot traffic",
    "click bot",
    "impression bot",
    "simulate browser",
    "session generator",
    "proxy pool",
    "fingerprint",
    "anti-detect",
    "antidetect",
    "worker forward",
    "cookie",
    "session token",
    "switch account",
    "account pool",
    "ban evasion",
    "cookie stuffing",
    "审核页",
    "用户页",
    "绕审核",
    "规避审核",
    "隐藏来源",
    "未披露来源",
    "未披露子渠道",
    "隐藏真实",
    "自然流量模拟",
    "模拟自然流量",
    "刷点击",
    "刷展示",
    "补点击",
    "补展示",
    "机器人流量",
    "代理池",
    "指纹",
    "反检测",
    "worker转发",
    "换号",
    "账号池",
    "封禁后",
)

BLOCKED_QUERY_MINING_TERMS = (
    "simulate search",
    "search simulation",
    "fake search term",
    "click bot",
    "impression bot",
    "bot traffic",
    "auto click",
    "click task",
    "impression task",
    "proxy pool",
    "fingerprint",
    "anti-detect",
    "antidetect",
    "geo spoof",
    "cookie",
    "session token",
    "browser profile",
    "scrape cookie",
    "bypass privacy",
    "hidden query",
    "cloaking",
    "cloak",
    "review page",
    "user page",
    "switch account",
    "account pool",
    "ban evasion",
    "模拟搜索",
    "伪造搜索词",
    "刷搜索",
    "补搜索",
    "刷点击",
    "补点击",
    "刷展示",
    "补展示",
    "点击任务",
    "展示任务",
    "代理池",
    "指纹",
    "反检测",
    "伪装地区",
    "cookie",
    "登录态",
    "抓后台",
    "绕过隐私",
    "审核页",
    "用户页",
    "绕审核",
    "换号",
    "账号池",
    "封禁后",
)

BLOCKED_BULK_UPLOAD_TERMS = (
    "auto post",
    "auto apply",
    "one click publish",
    "cookie",
    "session token",
    "browser profile",
    "bypass review",
    "evade review",
    "review page",
    "user page",
    "cloaking",
    "cloak",
    "captcha",
    "2fa bypass",
    "mfa bypass",
    "security challenge",
    "click bot",
    "impression bot",
    "simulate traffic",
    "proxy pool",
    "fingerprint",
    "anti-detect",
    "worker forward",
    "switch account",
    "account pool",
    "ban evasion",
    "自动发布",
    "自动提交",
    "自动apply",
    "一键发布",
    "cookie",
    "登录态",
    "浏览器profile",
    "绕审核",
    "规避审核",
    "审核页",
    "用户页",
    "cloaking",
    "验证码",
    "绕过2fa",
    "安全挑战",
    "刷点击",
    "刷展示",
    "模拟流量",
    "代理池",
    "指纹",
    "反检测",
    "worker转发",
    "换号",
    "账号池",
    "封禁后",
)

BLOCKED_SCRIPT_SYNC_TERMS = (
    "cookie",
    "session token",
    "browser profile",
    "password",
    "otp",
    "2fa",
    "mfa",
    "captcha",
    "security challenge",
    "auto login",
    "auto apply",
    "auto post",
    "one click publish",
    "click bot",
    "impression bot",
    "simulate traffic",
    "fake click",
    "fake conversion",
    "fake revenue",
    "proxy pool",
    "fingerprint",
    "anti-detect",
    "worker forward",
    "cloaking",
    "review page",
    "user page",
    "switch account",
    "account pool",
    "ban evasion",
    "remote bot config",
    "cookie",
    "登录态",
    "浏览器profile",
    "密码",
    "验证码",
    "绕过2fa",
    "安全挑战",
    "自动登录",
    "自动发布",
    "自动提交",
    "自动apply",
    "刷点击",
    "补点击",
    "刷展示",
    "补展示",
    "模拟流量",
    "伪造转化",
    "伪造收入",
    "代理池",
    "指纹",
    "反检测",
    "worker转发",
    "审核页",
    "用户页",
    "绕审核",
    "换号",
    "账号池",
    "封禁后",
)

BLOCKED_TAXONOMY_TERMS = (
    "email=",
    "phone=",
    "ssn",
    "social security",
    "passport",
    "driver license",
    "date of birth",
    "dob=",
    "credit score",
    "bank account",
    "diagnosis",
    "symptom",
    "substance",
    "addiction",
    "mental health",
    "religion",
    "political",
    "cookie",
    "session token",
    "password",
    "otp",
    "captcha",
    "2fa",
    "mfa",
    "strip gclid",
    "remove gclid",
    "remove utm",
    "hide source",
    "hidden source",
    "cloaking",
    "review page",
    "user page",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "switch account",
    "ban evasion",
    "邮箱=",
    "手机号",
    "电话=",
    "身份证",
    "护照",
    "出生日期",
    "信用分",
    "银行卡",
    "诊断",
    "病症",
    "成瘾",
    "心理健康",
    "宗教",
    "政治",
    "cookie",
    "登录态",
    "密码",
    "验证码",
    "去掉gclid",
    "删除utm",
    "隐藏来源",
    "审核页",
    "用户页",
    "绕审核",
    "代理池",
    "指纹",
    "worker转发",
    "换号",
    "封禁后",
)

BLOCKED_ATTRIBUTION_TERMS = (
    "fake conversion",
    "fake revenue",
    "fabricate lift",
    "fake control",
    "click bot",
    "impression bot",
    "simulate traffic",
    "autosurf",
    "cookie",
    "session token",
    "browser profile",
    "auto apply winner",
    "auto scale winner",
    "hide source",
    "hidden source",
    "cloaking",
    "review page",
    "user page",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "switch account",
    "ban evasion",
    "伪造转化",
    "伪造收入",
    "伪造增量",
    "伪造对照组",
    "刷点击",
    "补点击",
    "刷展示",
    "补展示",
    "模拟流量",
    "自动应用winner",
    "自动扩量winner",
    "cookie",
    "登录态",
    "浏览器profile",
    "隐藏来源",
    "审核页",
    "用户页",
    "绕审核",
    "代理池",
    "指纹",
    "worker转发",
    "换号",
    "封禁后",
)

BLOCKED_CPL_VERTICAL_TERMS = (
    "fake lead",
    "fabricate lead",
    "fake qualification",
    "fake phone",
    "fake income",
    "fake license",
    "fake case",
    "fake appointment",
    "auto submit",
    "submit fake form",
    "form bot",
    "lead bot",
    "generate leads",
    "forge consent",
    "fake consent",
    "consent stuffing",
    "bypass certification",
    "bypass license",
    "cookie",
    "session token",
    "browser profile",
    "cloaking",
    "review page",
    "user page",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "switch account",
    "ban evasion",
    "伪造lead",
    "伪造 lead",
    "伪造线索",
    "伪造资质",
    "伪造电话",
    "伪造收入",
    "伪造案件",
    "伪造预约",
    "自动提交表单",
    "表单机器人",
    "线索机器人",
    "伪造同意",
    "伪造consent",
    "绕过认证",
    "绕过资质",
    "cookie",
    "登录态",
    "浏览器profile",
    "审核页",
    "用户页",
    "绕审核",
    "代理池",
    "指纹",
    "worker转发",
    "换号",
    "封禁后",
)

BLOCKED_LEAD_PRICING_TERMS = (
    "fake lead",
    "fabricate lead",
    "fake paid",
    "fake payout",
    "fake invoice",
    "fake report",
    "forge consent",
    "fake consent",
    "hide source",
    "hidden source",
    "cloak",
    "cloaking",
    "review page",
    "user page",
    "cookie",
    "session token",
    "browser profile",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "anti-detect",
    "auto negotiate",
    "auto routing",
    "auto route",
    "switch account",
    "ban evasion",
    "伪造lead",
    "伪造 lead",
    "伪造线索",
    "伪造结算",
    "伪造收入",
    "伪造付款",
    "伪造发票",
    "伪造报表",
    "伪造同意",
    "伪造consent",
    "隐藏来源",
    "审核页",
    "用户页",
    "绕审核",
    "cookie",
    "登录态",
    "浏览器profile",
    "代理池",
    "指纹",
    "worker转发",
    "反检测",
    "自动谈价",
    "自动改路由",
    "自动切换buyer",
    "自动切换 buyer",
    "换号",
    "封禁后",
)

BLOCKED_APPOINTMENT_LEAD_TERMS = (
    "fake appointment",
    "fake booking",
    "fabricate appointment",
    "fake showed",
    "fake show",
    "fake no-show",
    "fake paid",
    "simulate attendance",
    "simulate show",
    "auto call",
    "robocall",
    "mass sms",
    "sms blast",
    "bulk sms",
    "auto reminder without consent",
    "forge consent",
    "fake consent",
    "bypass consent",
    "calendar stuffing",
    "cookie",
    "session token",
    "browser profile",
    "cloaking",
    "review page",
    "user page",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "switch account",
    "ban evasion",
    "伪造预约",
    "伪造booking",
    "伪造 booking",
    "伪造到场",
    "伪造showed",
    "伪造 showed",
    "伪造付款",
    "伪造收入",
    "模拟到场",
    "自动外呼",
    "机器人外呼",
    "短信群发",
    "群发短信",
    "无同意提醒",
    "伪造同意",
    "伪造consent",
    "绕过同意",
    "补日历",
    "刷预约",
    "cookie",
    "登录态",
    "浏览器profile",
    "审核页",
    "用户页",
    "绕审核",
    "代理池",
    "指纹",
    "worker转发",
    "换号",
    "封禁后",
)

BLOCKED_BUYER_CAPACITY_TERMS = (
    "auto change budget",
    "auto adjust budget",
    "auto schedule",
    "auto routing",
    "auto route",
    "auto switch buyer",
    "auto call",
    "robocall",
    "mass sms",
    "sms blast",
    "fake lead",
    "fabricate lead",
    "fake call",
    "simulate call",
    "simulate lead",
    "補 lead",
    "cookie",
    "session token",
    "browser profile",
    "cloaking",
    "review page",
    "user page",
    "hidden fallback",
    "hide destination",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "anti-detect",
    "switch account",
    "ban evasion",
    "自动改预算",
    "自动调预算",
    "自动改时段",
    "自动改路由",
    "自动切换buyer",
    "自动切换 buyer",
    "自动外呼",
    "机器人外呼",
    "短信群发",
    "群发短信",
    "补lead",
    "补 lead",
    "补电话",
    "模拟通话",
    "伪造电话",
    "伪造线索",
    "cookie",
    "登录态",
    "浏览器profile",
    "审核页",
    "用户页",
    "隐藏目的地",
    "隐藏fallback",
    "隐藏 fallback",
    "绕审核",
    "代理池",
    "指纹",
    "worker转发",
    "反检测",
    "换号",
    "封禁后",
)

BLOCKED_CONVERSION_SIGNAL_TERMS = (
    "fake conversion",
    "fabricate conversion",
    "fake offline conversion",
    "fake postback",
    "fake lead",
    "training conversion",
    "seed conversion",
    "upload fake",
    "spoof gclid",
    "forged gclid",
    "forge gclid",
    "auto upload",
    "automatic upload",
    "auto change goal",
    "auto change conversion goal",
    "auto set primary",
    "cookie",
    "session token",
    "browser profile",
    "bypass consent",
    "bypass 2fa",
    "2fa",
    "mfa",
    "cloaking",
    "review page",
    "user page",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "anti-detect",
    "switch account",
    "ban evasion",
    "补转化",
    "补 conversion",
    "补postback",
    "补 postback",
    "伪造转化",
    "伪造conversion",
    "伪造 conversion",
    "伪造gclid",
    "伪造 gclid",
    "伪造点击id",
    "伪造点击 id",
    "刷转化",
    "刷表单",
    "刷lead",
    "刷 lead",
    "自动上传",
    "自动改goal",
    "自动改 goal",
    "自动改转化目标",
    "自动设primary",
    "自动设 primary",
    "绕过同意",
    "绕consent",
    "绕 consent",
    "登录态",
    "浏览器profile",
    "审核页",
    "用户页",
    "绕审核",
    "代理池",
    "指纹",
    "worker转发",
    "反检测",
    "换号",
    "封禁后",
)

BLOCKED_CRM_VALUE_MAPPING_TERMS = (
    "fake crm",
    "fake stage",
    "fake buyer feedback",
    "fake invoice",
    "fake paid",
    "fake offline conversion",
    "fake postback",
    "fabricate stage",
    "fabricate conversion",
    "fabricate lead",
    "generate gclid",
    "spoof gclid",
    "forged gclid",
    "fake click id",
    "auto upload",
    "automatic upload",
    "auto set primary",
    "auto change goal",
    "cookie",
    "session token",
    "browser profile",
    "bypass consent",
    "bypass 2fa",
    "2fa",
    "mfa",
    "cloaking",
    "review page",
    "user page",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "anti-detect",
    "switch account",
    "ban evasion",
    "伪造crm",
    "伪造 crm",
    "伪造阶段",
    "伪造买方反馈",
    "伪造buyer feedback",
    "伪造 buyer feedback",
    "伪造发票",
    "伪造付款",
    "伪造paid",
    "伪造 paid",
    "伪造转化",
    "补postback",
    "补 postback",
    "补转化",
    "生成gclid",
    "生成 gclid",
    "伪造gclid",
    "伪造 gclid",
    "伪造点击id",
    "伪造点击 id",
    "刷表单",
    "刷lead",
    "刷 lead",
    "自动上传",
    "自动设primary",
    "自动设 primary",
    "自动改goal",
    "自动改 goal",
    "绕过同意",
    "绕consent",
    "绕 consent",
    "登录态",
    "浏览器profile",
    "审核页",
    "用户页",
    "绕审核",
    "代理池",
    "指纹",
    "worker转发",
    "反检测",
    "换号",
    "封禁后",
)

BLOCKED_PING_POST_ROUTING_TERMS = (
    "fake lead",
    "fabricate lead",
    "generate lead",
    "补lead",
    "auto post",
    "automatic post",
    "auto submit",
    "automatic submit",
    "auto call",
    "robocall",
    "sms blast",
    "mass sms",
    "bypass consent",
    "bypass dnc",
    "bypass opt-out",
    "hidden buyer",
    "undisclosed shared",
    "fake consent",
    "cloaking",
    "review page",
    "user page",
    "cookie",
    "session token",
    "browser profile",
    "proxy pool",
    "fingerprint",
    "worker forward",
    "anti-detect",
    "switch account",
    "ban evasion",
    "伪造线索",
    "伪造lead",
    "伪造 lead",
    "补 lead",
    "自动提交",
    "自动post",
    "自动 post",
    "自动外呼",
    "群发短信",
    "绕过同意",
    "绕consent",
    "绕 consent",
    "绕dnc",
    "绕 dnc",
    "绕过dnc",
    "绕过 dnc",
    "绕过退订",
    "隐藏buyer",
    "隐藏 buyer",
    "未披露共享",
    "伪造同意",
    "登录态",
    "浏览器profile",
    "代理池",
    "指纹",
    "worker转发",
    "审核页",
    "用户页",
    "绕审核",
    "换号",
    "封禁后",
)


@bp.route("/")
def index():
    metrics = MetricDaily.query.order_by(MetricDaily.day.desc()).limit(200).all()
    totals = metric_totals(metrics)
    return render_template(
        "dashboard.html",
        totals=totals,
        offer_count=Offer.query.count(),
        campaign_count=CampaignDraft.query.count(),
        assessment_count=OpportunityAssessment.query.count(),
        risk_audit_count=RiskAudit.query.count(),
        source_count=ResearchSource.query.count(),
        task_count=TaskJob.query.count(),
        open_actions=OptimizationAction.query.filter_by(status="open").count(),
        recent_logs=_recent_logs(),
    )


@bp.route("/calculators", methods=["GET", "POST"])
def calculators():
    offers = Offer.query.order_by(Offer.name).all()
    if request.method == "POST":
        form = request.form
        result = calculate_opportunity(
            revenue_model=form.get("revenue_model", "CPA"),
            session_rpm=_float(form.get("session_rpm")),
            payout=_float(form.get("payout")),
            cvr_percent=_float(form.get("cvr_percent")),
            cpc=_float(form.get("cpc")),
            safety_factor=_float(form.get("safety_factor"), 0.6),
            target_clicks=_int(form.get("target_clicks"), 100),
            policy_score=_int(form.get("policy_score"), 70),
            content_score=_int(form.get("content_score"), 70),
            tracking_score=_int(form.get("tracking_score"), 70),
            source_score=_int(form.get("source_score"), 70),
            cash_buffer_days=_int(form.get("cash_buffer_days"), 14),
        )
        offer_id = form.get("offer_id")
        assessment = OpportunityAssessment(
            offer_id=int(offer_id) if offer_id else None,
            name=form["name"].strip(),
            revenue_model=form.get("revenue_model", "CPA"),
            session_rpm=decimal_value(form.get("session_rpm")),
            payout=decimal_value(form.get("payout")),
            cvr_percent=decimal_value(form.get("cvr_percent")),
            cpc=decimal_value(form.get("cpc")),
            safety_factor=decimal_value(form.get("safety_factor"), "0.6"),
            target_clicks=_int(form.get("target_clicks"), 100),
            policy_score=_int(form.get("policy_score"), 70),
            content_score=_int(form.get("content_score"), 70),
            tracking_score=_int(form.get("tracking_score"), 70),
            source_score=_int(form.get("source_score"), 70),
            cash_buffer_days=_int(form.get("cash_buffer_days"), 14),
            result=result,
            recommendation=result["recommendation"],
        )
        db.session.add(assessment)
        db.session.flush()
        add_audit(
            "opportunity_assessment",
            assessment.id,
            "create",
            f"Calculated opportunity score {result['opportunity_score']} for {assessment.name}.",
        )
        db.session.commit()
        flash("套利测算已保存。", "success")
        return redirect(url_for("main.calculators"))

    return render_template(
        "calculators.html",
        offers=offers,
        assessments=OpportunityAssessment.query.order_by(
            OpportunityAssessment.created_at.desc()
        ).all(),
    )


@bp.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "POST":
        offer = Offer(
            name=request.form["name"].strip(),
            vertical=request.form.get("vertical", "general").strip() or "general",
            country=request.form.get("country", "US").strip() or "US",
            language=request.form.get("language", "en").strip() or "en",
            payout_model=request.form.get("payout_model", "CPA"),
            payout_value=decimal_value(request.form.get("payout_value")),
            target_url=request.form["target_url"].strip(),
            tracking_url=request.form.get("tracking_url", "").strip() or None,
            policy_notes=request.form.get("policy_notes", "").strip() or None,
            status=request.form.get("status", "researching"),
        )
        db.session.add(offer)
        db.session.flush()
        add_audit("offer", offer.id, "create", f"Created offer {offer.name}.")
        db.session.commit()
        flash("Offer 已创建。", "success")
        return redirect(url_for("main.offer_detail", offer_id=offer.id))

    return render_template(
        "offers.html",
        offers=Offer.query.order_by(Offer.created_at.desc()).all(),
    )


@bp.route("/accounts", methods=["GET", "POST"])
def accounts():
    if request.method == "POST":
        account_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("platform", ""),
                request.form.get("customer_id", ""),
                request.form.get("sync_method", ""),
                request.form.get("status", ""),
                request.form.get("notes", ""),
            ]
        ).lower()
        if any(term in account_text for term in BLOCKED_ACCOUNT_TERMS):
            flash("账号配置包含规避封禁、账号池或防关联继续投放语义，请改走风险审计和修复/申诉流程。", "warning")
            return redirect(url_for("main.accounts"))
        account = AdsAccount(
            name=request.form["name"].strip(),
            platform=request.form.get("platform", "Google Ads").strip() or "Google Ads",
            customer_id=request.form.get("customer_id", "").strip() or None,
            sync_method=request.form.get("sync_method", "Google Ads Scripts").strip(),
            status=request.form.get("status", "active"),
            notes=request.form.get("notes", "").strip() or None,
        )
        db.session.add(account)
        db.session.flush()
        add_audit("ads_account", account.id, "create", f"Created account {account.name}.")
        db.session.commit()
        flash("广告账号配置已创建。", "success")
        return redirect(url_for("main.accounts"))

    return render_template(
        "accounts.html",
        accounts=AdsAccount.query.order_by(AdsAccount.created_at.desc()).all(),
    )


@bp.route("/offers/<int:offer_id>")
def offer_detail(offer_id: int):
    offer = Offer.query.get_or_404(offer_id)
    metrics = MetricDaily.query.filter_by(offer_id=offer.id).all()
    creative_claim_reviews = {
        creative.id: sorted(
            creative.claim_reviews,
            key=lambda item: (item.severity != "high", item.created_at),
        )
        for creative in offer.creatives
    }
    return render_template(
        "offer_detail.html",
        offer=offer,
        totals=metric_totals(metrics),
        creative_claim_reviews=creative_claim_reviews,
        claim_review_statuses=CLAIM_REVIEW_STATUSES,
    )


@bp.post("/offers/<int:offer_id>/crawl")
def crawl_offer(offer_id: int):
    offer = Offer.query.get_or_404(offer_id)
    result = audit_landing_page(offer)
    db.session.add(result.landing_page)
    db.session.flush()
    add_audit(
        "landing_page",
        result.landing_page.id,
        "crawl",
        f"Audited {offer.target_url}; quality score {result.landing_page.quality_score}.",
    )
    db.session.commit()
    if result.warnings:
        flash("采集完成，但存在质量提醒。", "warning")
    else:
        flash("落地页采集和审计已完成。", "success")
    return redirect(url_for("main.offer_detail", offer_id=offer.id))


@bp.post("/offers/<int:offer_id>/creatives/generate")
def generate_creatives(offer_id: int):
    offer = Offer.query.get_or_404(offer_id)
    payloads = generate_creative_sets(offer, offer.latest_landing_page)
    created = 0
    review_cases = 0
    creatives: list[CreativeSet] = []
    for payload in payloads:
        creative = CreativeSet(
            offer_id=offer.id,
            angle=payload["angle"],
            headlines=payload["headlines"],
            descriptions=payload["descriptions"],
            keywords=payload["keywords"],
        )
        db.session.add(creative)
        creatives.append(creative)
        created += 1
    db.session.flush()
    for creative in creatives:
        created_cases, _, _ = _sync_creative_claim_reviews(creative)
        review_cases += created_cases
    add_audit(
        "offer",
        offer.id,
        "creative_generate",
        f"Generated {created} creative sets and {review_cases} claim review cases.",
    )
    db.session.commit()
    flash("已生成 3 组创意、标题、描述、关键词，并创建 Claim 审核记录。", "success")
    return redirect(url_for("main.offer_detail", offer_id=offer.id))


@bp.post("/creatives/<int:creative_id>/claim-reviews/run")
def run_creative_claim_reviews(creative_id: int):
    creative = CreativeSet.query.get_or_404(creative_id)
    created, updated, total = _sync_creative_claim_reviews(creative)
    add_audit(
        "creative_claim_review",
        creative.id,
        "refresh",
        (
            f"Refreshed claim review for creative {creative.id}: "
            f"{created} created, {updated} updated, {total} current issues."
        ),
    )
    db.session.commit()
    flash("Claim 审核已刷新。记录只用于人审和证据留存，不自动修改素材或投放。", "success")
    return redirect(url_for("main.offer_detail", offer_id=creative.offer_id))


@bp.post("/claim-reviews/<int:review_id>/status")
def update_claim_review_status(review_id: int):
    review = CreativeClaimReview.query.get_or_404(review_id)
    status = request.form.get("review_status", "open")
    if status not in CLAIM_REVIEW_STATUSES:
        flash("Claim 审核状态不允许。", "warning")
        return redirect(url_for("main.offer_detail", offer_id=review.creative.offer_id))
    old_status = review.review_status
    review.review_status = status
    add_audit(
        "creative_claim_review",
        review.id,
        "status_update",
        f"Claim review {review.issue} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("Claim 审核状态已更新。状态只代表内部人审结果，不会自动发布广告。", "success")
    return redirect(url_for("main.offer_detail", offer_id=review.creative.offer_id))


def _sync_creative_claim_reviews(creative: CreativeSet) -> tuple[int, int, int]:
    issues = audit_creative_claims(creative, creative.offer.latest_landing_page)
    existing = {
        (review.asset_type, review.asset_text, review.issue): review
        for review in creative.claim_reviews
    }
    created = 0
    updated = 0
    for issue in issues:
        key = (issue["asset"], issue["text"], issue["issue"])
        review = existing.get(key)
        if review is None:
            review = CreativeClaimReview(
                creative_set_id=creative.id,
                asset_type=issue["asset"],
                asset_text=issue["text"],
                issue=issue["issue"],
                severity=issue["severity"],
                action=issue["action"],
                evidence=issue.get("evidence"),
                source_url=issue.get("source_url"),
            )
            db.session.add(review)
            created += 1
            continue

        review.severity = issue["severity"]
        review.action = issue["action"]
        review.evidence = issue.get("evidence")
        review.source_url = issue.get("source_url")
        updated += 1

    return created, updated, len(issues)


@bp.route("/ad-reviews", methods=["GET", "POST"])
def ad_reviews():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    creatives = CreativeSet.query.order_by(CreativeSet.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("object_type", ""),
                request.form.get("object_ref", ""),
                request.form.get("policy_topic", ""),
                request.form.get("final_url", ""),
                request.form.get("expanded_url", ""),
                request.form.get("finding", ""),
                request.form.get("change_summary", ""),
                request.form.get("appeal_text", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_AD_REVIEW_TERMS):
            flash("广告审核案例包含绕审核、Cookie、cloaking、换号或规避系统语义，请转入风险审计和修复流程。", "warning")
            return redirect(url_for("main.ad_reviews"))

        status = request.form.get("status", "open")
        if status not in AD_REVIEW_CASE_STATUSES:
            flash("广告审核案例状态不允许。", "warning")
            return redirect(url_for("main.ad_reviews"))

        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        creative_id = request.form.get("creative_set_id")
        evidence_urls = [
            item.strip()
            for item in request.form.get("evidence_urls", "").splitlines()
            if item.strip()
        ]
        case = AdReviewCase(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            creative_set_id=int(creative_id) if creative_id else None,
            object_type=request.form.get("object_type", "ad").strip() or "ad",
            object_ref=request.form.get("object_ref", "").strip() or None,
            policy_topic=request.form["policy_topic"].strip(),
            severity=request.form.get("severity", "medium").strip() or "medium",
            status=status,
            final_url=request.form.get("final_url", "").strip() or None,
            expanded_url=request.form.get("expanded_url", "").strip() or None,
            finding=request.form["finding"].strip(),
            change_summary=request.form["change_summary"].strip(),
            evidence_urls=evidence_urls,
            appeal_text=request.form.get("appeal_text", "").strip() or None,
            reviewer=request.form.get("reviewer", "").strip() or None,
        )
        db.session.add(case)
        db.session.flush()
        add_audit(
            "ad_review_case",
            case.id,
            "create",
            f"Created ad review case for {case.policy_topic}.",
        )
        db.session.commit()
        flash("广告审核案例已保存。该记录只用于证据包和人审，不自动提交申诉。", "success")
        return redirect(url_for("main.ad_reviews"))

    return render_template(
        "ad_reviews.html",
        cases=AdReviewCase.query.order_by(AdReviewCase.created_at.desc()).all(),
        offers=offers,
        campaigns=campaigns,
        creatives=creatives,
        status_options=AD_REVIEW_CASE_STATUSES,
    )


@bp.post("/ad-reviews/<int:case_id>/status")
def update_ad_review_status(case_id: int):
    case = AdReviewCase.query.get_or_404(case_id)
    status = request.form.get("status", "open")
    if status not in AD_REVIEW_CASE_STATUSES:
        flash("广告审核案例状态不允许。", "warning")
        return redirect(url_for("main.ad_reviews"))
    old_status = case.status
    case.status = status
    add_audit(
        "ad_review_case",
        case.id,
        "status_update",
        f"Ad review case {case.policy_topic} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("广告审核案例状态已更新。状态只代表内部证据包进度，不会自动提交申诉或改后台。", "success")
    return redirect(url_for("main.ad_reviews"))


@bp.route("/campaigns", methods=["GET", "POST"])
def campaigns():
    offers = Offer.query.order_by(Offer.name).all()
    creatives = CreativeSet.query.order_by(CreativeSet.created_at.desc()).all()
    if request.method == "POST":
        offer = Offer.query.get_or_404(int(request.form["offer_id"]))
        creative_id = request.form.get("creative_set_id")
        campaign = CampaignDraft(
            offer_id=offer.id,
            creative_set_id=int(creative_id) if creative_id else None,
            name=request.form["name"].strip(),
            channel=request.form.get("channel", "Google Search").strip(),
            daily_budget=decimal_value(request.form.get("daily_budget"), "30"),
            bid_strategy=request.form.get("bid_strategy", "Maximize Clicks").strip(),
            final_url=request.form.get("final_url", offer.target_url).strip(),
            notes=request.form.get("notes", "").strip() or None,
        )
        db.session.add(campaign)
        db.session.flush()
        add_audit("campaign", campaign.id, "create", f"Created campaign draft {campaign.name}.")
        db.session.commit()
        flash("投放草稿已创建。", "success")
        return redirect(url_for("main.campaigns"))

    return render_template(
        "campaigns.html",
        campaigns=CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all(),
        offers=offers,
        creatives=creatives,
        campaign_statuses=CAMPAIGN_DRAFT_STATUSES,
        preflight_by_campaign={
            campaign.id: campaign_preflight_blockers(campaign)
            for campaign in CampaignDraft.query.order_by(
                CampaignDraft.created_at.desc()
            ).all()
        },
    )


@bp.post("/campaigns/<int:campaign_id>/status")
def update_campaign_status(campaign_id: int):
    campaign = CampaignDraft.query.get_or_404(campaign_id)
    status = request.form.get("status", "draft")
    if status not in CAMPAIGN_DRAFT_STATUSES:
        flash("投放草稿状态不允许。", "warning")
        return redirect(url_for("main.campaigns"))
    old_status = campaign.status
    campaign.status = status
    add_audit(
        "campaign",
        campaign.id,
        "status_update",
        f"Campaign draft {campaign.name} status changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("投放草稿状态已更新。状态只代表内部评审进度，不会自动发布广告。", "success")
    return redirect(url_for("main.campaigns"))


@bp.route("/campaigns/<int:campaign_id>/export.csv")
def export_campaign(campaign_id: int):
    campaign = CampaignDraft.query.get_or_404(campaign_id)
    blockers = campaign_preflight_blockers(campaign)
    if blockers:
        add_audit(
            "campaign",
            campaign.id,
            "export_blocked",
            "CSV export blocked by preflight: " + " | ".join(blockers),
        )
        db.session.commit()
        flash("导出被上线前检查拦截：" + "；".join(blockers), "warning")
        return redirect(url_for("main.campaigns"))
    csv_text = campaign_to_google_ads_editor_csv(campaign)
    campaign.status = "exported"
    add_audit("campaign", campaign.id, "export_csv", "Exported Google Ads Editor CSV.")
    db.session.commit()
    filename = f"{campaign.name.lower().replace(' ', '-')}.csv"
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@bp.route("/campaigns/<int:campaign_id>/export.script.json")
def export_campaign_script(campaign_id: int):
    campaign = CampaignDraft.query.get_or_404(campaign_id)
    blockers = campaign_preflight_blockers(campaign)
    if blockers:
        add_audit(
            "campaign",
            campaign.id,
            "export_blocked",
            "Scripts export blocked by preflight: " + " | ".join(blockers),
        )
        db.session.commit()
        flash("导出被上线前检查拦截：" + "；".join(blockers), "warning")
        return redirect(url_for("main.campaigns"))
    payload = campaign_to_scripts_payload(campaign)
    add_audit(
        "campaign",
        campaign.id,
        "export_script_payload",
        "Exported Google Ads Scripts payload for manual review.",
    )
    db.session.commit()
    filename = f"{campaign.name.lower().replace(' ', '-')}.script.json"
    return Response(
        payload,
        mimetype="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@bp.route("/metrics/import", methods=["GET", "POST"])
def metrics_import():
    if request.method == "POST":
        csv_text = request.form.get("csv_text", "")
        file = request.files.get("csv_file")
        if file and file.filename:
            csv_text = file.read().decode("utf-8-sig")
        count = _import_metrics(csv_text)
        flash(f"已导入 {count} 行指标，并生成优化建议。", "success")
        return redirect(url_for("main.optimization"))

    return render_template("metrics_import.html")


@bp.route("/decision-windows", methods=["GET", "POST"])
def decision_windows():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        approved_revenue = decimal_value(request.form.get("approved_revenue"))
        paid_revenue = decimal_value(request.form.get("paid_revenue"))
        result = calculate_decision_window(
            data_status=request.form.get("data_status", "fresh"),
            revenue_status=request.form.get("revenue_status", "estimated"),
            conversion_lag_days=int(request.form.get("conversion_lag_days") or 0),
            approval_lag_days=int(request.form.get("approval_lag_days") or 0),
            settlement_lag_days=int(request.form.get("settlement_lag_days") or 0),
            sample_clicks=int(request.form.get("sample_clicks") or 0),
            approved_revenue=float(approved_revenue),
            paid_revenue=float(paid_revenue),
            source_quality=request.form.get("source_quality", "watch"),
            incident_state=request.form.get("incident_state", "clean"),
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = DecisionWindowReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            data_status=request.form.get("data_status", "fresh"),
            revenue_status=request.form.get("revenue_status", "estimated"),
            conversion_lag_days=int(request.form.get("conversion_lag_days") or 0),
            approval_lag_days=int(request.form.get("approval_lag_days") or 0),
            settlement_lag_days=int(request.form.get("settlement_lag_days") or 0),
            sample_clicks=int(request.form.get("sample_clicks") or 0),
            approved_revenue=approved_revenue,
            paid_revenue=paid_revenue,
            source_quality=request.form.get("source_quality", "watch"),
            incident_state=request.form.get("incident_state", "clean"),
            score=int(result["score"]),
            maturity=str(result["maturity"]),
            recommended_action=str(result["recommended_action"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in DECISION_WINDOW_STATUSES:
            flash("决策窗口状态不允许。", "warning")
            return redirect(url_for("main.decision_windows"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "decision_window_review",
            review.id,
            "create",
            f"Created decision window review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("决策窗口评审已保存。它只用于等待/止损/扩量判断，不自动改预算。", "success")
        return redirect(url_for("main.decision_windows"))

    return render_template(
        "decision_windows.html",
        reviews=DecisionWindowReview.query.order_by(
            DecisionWindowReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=DECISION_WINDOW_STATUSES,
    )


@bp.post("/decision-windows/<int:review_id>/status")
def update_decision_window_status(review_id: int):
    review = DecisionWindowReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in DECISION_WINDOW_STATUSES:
        flash("决策窗口状态不允许。", "warning")
        return redirect(url_for("main.decision_windows"))
    old_status = review.status
    review.status = status
    add_audit(
        "decision_window_review",
        review.id,
        "status_update",
        f"Decision window review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("决策窗口状态已更新。状态只代表内部处理进度，不会自动改预算。", "success")
    return redirect(url_for("main.decision_windows"))


@bp.route("/budget-pacing", methods=["GET", "POST"])
def budget_pacing():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        current_daily_budget = decimal_value(request.form.get("current_daily_budget"))
        proposed_daily_budget = decimal_value(request.form.get("proposed_daily_budget"))
        test_budget = decimal_value(request.form.get("test_budget"))
        hard_stop = decimal_value(request.form.get("hard_stop"))
        spend_to_date = decimal_value(request.form.get("spend_to_date"))
        approved_revenue = decimal_value(request.form.get("approved_revenue"))
        paid_revenue = decimal_value(request.form.get("paid_revenue"))
        safe_cpc = decimal_value(request.form.get("safe_cpc"))
        actual_cpc = decimal_value(request.form.get("actual_cpc"))
        overdelivery_buffer_percent = decimal_value(
            request.form.get("overdelivery_buffer_percent"),
            "20",
        )
        result = calculate_budget_pacing(
            current_daily_budget=float(current_daily_budget),
            proposed_daily_budget=float(proposed_daily_budget),
            test_budget=float(test_budget),
            hard_stop=float(hard_stop),
            spend_to_date=float(spend_to_date),
            approved_revenue=float(approved_revenue),
            paid_revenue=float(paid_revenue),
            safe_cpc=float(safe_cpc),
            actual_cpc=float(actual_cpc),
            sample_clicks=int(request.form.get("sample_clicks") or 0),
            data_status=request.form.get("data_status", "fresh"),
            revenue_status=request.form.get("revenue_status", "estimated"),
            source_quality=request.form.get("source_quality", "watch"),
            incident_state=request.form.get("incident_state", "clean"),
            cash_buffer_days=int(request.form.get("cash_buffer_days") or 0),
            overdelivery_buffer_percent=float(overdelivery_buffer_percent),
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = BudgetPacingReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            current_daily_budget=current_daily_budget,
            proposed_daily_budget=proposed_daily_budget,
            test_budget=test_budget,
            hard_stop=hard_stop,
            spend_to_date=spend_to_date,
            approved_revenue=approved_revenue,
            paid_revenue=paid_revenue,
            safe_cpc=safe_cpc,
            actual_cpc=actual_cpc,
            sample_clicks=int(request.form.get("sample_clicks") or 0),
            data_status=request.form.get("data_status", "fresh"),
            revenue_status=request.form.get("revenue_status", "estimated"),
            source_quality=request.form.get("source_quality", "watch"),
            incident_state=request.form.get("incident_state", "clean"),
            cash_buffer_days=int(request.form.get("cash_buffer_days") or 0),
            overdelivery_buffer_percent=overdelivery_buffer_percent,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            increase_percent=decimal_value(result["increase_percent"]),
            remaining_test_budget=decimal_value(result["remaining_test_budget"]),
            remaining_hard_stop=decimal_value(result["remaining_hard_stop"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in BUDGET_PACING_STATUSES:
            flash("预算评审状态不允许。", "warning")
            return redirect(url_for("main.budget_pacing"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "budget_pacing_review",
            review.id,
            "create",
            f"Created budget pacing review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("预算节奏评审已保存。它只生成内部预算建议，不自动改后台预算。", "success")
        return redirect(url_for("main.budget_pacing"))

    return render_template(
        "budget_pacing.html",
        reviews=BudgetPacingReview.query.order_by(
            BudgetPacingReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=BUDGET_PACING_STATUSES,
    )


@bp.post("/budget-pacing/<int:review_id>/status")
def update_budget_pacing_status(review_id: int):
    review = BudgetPacingReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in BUDGET_PACING_STATUSES:
        flash("预算评审状态不允许。", "warning")
        return redirect(url_for("main.budget_pacing"))
    old_status = review.status
    review.status = status
    add_audit(
        "budget_pacing_review",
        review.id,
        "status_update",
        f"Budget pacing review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("预算评审状态已更新。状态只代表内部审批进度，不会自动改广告后台。", "success")
    return redirect(url_for("main.budget_pacing"))


@bp.route("/portfolio-allocation", methods=["GET", "POST"])
def portfolio_allocation():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        monthly_media_budget = decimal_value(request.form.get("monthly_media_budget"))
        proposed_allocation = decimal_value(request.form.get("proposed_allocation"))
        spend_to_date = decimal_value(request.form.get("spend_to_date"))
        reported_revenue = decimal_value(request.form.get("reported_revenue"))
        pending_revenue = decimal_value(request.form.get("pending_revenue"))
        approved_revenue = decimal_value(request.form.get("approved_revenue"))
        finalized_revenue = decimal_value(request.form.get("finalized_revenue"))
        paid_revenue = decimal_value(request.form.get("paid_revenue"))
        deducted_revenue = decimal_value(request.form.get("deducted_revenue"))
        single_offer_exposure_percent = decimal_value(
            request.form.get("single_offer_exposure_percent")
        )
        single_source_exposure_percent = decimal_value(
            request.form.get("single_source_exposure_percent")
        )
        single_account_exposure_percent = decimal_value(
            request.form.get("single_account_exposure_percent")
        )
        single_partner_exposure_percent = decimal_value(
            request.form.get("single_partner_exposure_percent")
        )
        result = calculate_portfolio_allocation(
            portfolio_bucket=request.form.get("portfolio_bucket", "test"),
            monthly_media_budget=float(monthly_media_budget),
            proposed_allocation=float(proposed_allocation),
            spend_to_date=float(spend_to_date),
            reported_revenue=float(reported_revenue),
            pending_revenue=float(pending_revenue),
            approved_revenue=float(approved_revenue),
            finalized_revenue=float(finalized_revenue),
            paid_revenue=float(paid_revenue),
            deducted_revenue=float(deducted_revenue),
            single_offer_exposure_percent=float(single_offer_exposure_percent),
            single_source_exposure_percent=float(single_source_exposure_percent),
            single_account_exposure_percent=float(single_account_exposure_percent),
            single_partner_exposure_percent=float(single_partner_exposure_percent),
            cash_reserve_days=int(request.form.get("cash_reserve_days") or 0),
            source_quality=request.form.get("source_quality", "watch"),
            policy_risk=request.form.get("policy_risk", "medium"),
            incident_state=request.form.get("incident_state", "clean"),
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = PortfolioAllocationReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            portfolio_bucket=request.form.get("portfolio_bucket", "test"),
            monthly_media_budget=monthly_media_budget,
            proposed_allocation=proposed_allocation,
            spend_to_date=spend_to_date,
            reported_revenue=reported_revenue,
            pending_revenue=pending_revenue,
            approved_revenue=approved_revenue,
            finalized_revenue=finalized_revenue,
            paid_revenue=paid_revenue,
            deducted_revenue=deducted_revenue,
            single_offer_exposure_percent=single_offer_exposure_percent,
            single_source_exposure_percent=single_source_exposure_percent,
            single_account_exposure_percent=single_account_exposure_percent,
            single_partner_exposure_percent=single_partner_exposure_percent,
            cash_reserve_days=int(request.form.get("cash_reserve_days") or 0),
            source_quality=request.form.get("source_quality", "watch"),
            policy_risk=request.form.get("policy_risk", "medium"),
            incident_state=request.form.get("incident_state", "clean"),
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            allocation_percent=decimal_value(result["allocation_percent"]),
            remaining_monthly_budget=decimal_value(result["remaining_monthly_budget"]),
            cash_at_risk=decimal_value(result["cash_at_risk"]),
            revenue_quality_ratio=decimal_value(result["revenue_quality_ratio"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in PORTFOLIO_ALLOCATION_STATUSES:
            flash("组合分配状态不允许。", "warning")
            return redirect(url_for("main.portfolio_allocation"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "portfolio_allocation_review",
            review.id,
            "create",
            f"Created portfolio allocation review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("Portfolio 分配评审已保存。它只生成内部组合建议，不自动改预算或后台。", "success")
        return redirect(url_for("main.portfolio_allocation"))

    return render_template(
        "portfolio_allocation.html",
        reviews=PortfolioAllocationReview.query.order_by(
            PortfolioAllocationReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=PORTFOLIO_ALLOCATION_STATUSES,
    )


@bp.post("/portfolio-allocation/<int:review_id>/status")
def update_portfolio_allocation_status(review_id: int):
    review = PortfolioAllocationReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in PORTFOLIO_ALLOCATION_STATUSES:
        flash("组合分配状态不允许。", "warning")
        return redirect(url_for("main.portfolio_allocation"))
    old_status = review.status
    review.status = status
    add_audit(
        "portfolio_allocation_review",
        review.id,
        "status_update",
        f"Portfolio allocation review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("Portfolio 分配状态已更新。状态只代表内部审批进度，不会自动改广告后台。", "success")
    return redirect(url_for("main.portfolio_allocation"))


@bp.route("/offer-cap-payout", methods=["GET", "POST"])
def offer_cap_payout():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("offer_status", ""),
                request.form.get("cap_type", ""),
                request.form.get("cap_period", ""),
                request.form.get("buyer_capacity_status", ""),
                request.form.get("replacement_status", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_OFFER_ACTION_TERMS):
            flash("Offer 处理包含 Cookie、cloaking、换号、防关联或隐藏目的地语义，请改走风险审计和修复流程。", "warning")
            return redirect(url_for("main.offer_cap_payout"))

        cap_limit = decimal_value(request.form.get("cap_limit"))
        cap_used = decimal_value(request.form.get("cap_used"))
        expected_next_conversions = decimal_value(
            request.form.get("expected_next_conversions")
        )
        current_payout = decimal_value(request.form.get("current_payout"))
        new_payout = decimal_value(request.form.get("new_payout"))
        approval_rate_percent = decimal_value(request.form.get("approval_rate_percent"))
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        deduction_rate_percent = decimal_value(request.form.get("deduction_rate_percent"))
        same_intent_review = request.form.get("same_intent_review") == "on"
        result = calculate_offer_cap_review(
            offer_status=request.form.get("offer_status", "active"),
            cap_limit=float(cap_limit),
            cap_used=float(cap_used),
            expected_next_conversions=float(expected_next_conversions),
            current_payout=float(current_payout),
            new_payout=float(new_payout),
            approval_rate_percent=float(approval_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            deduction_rate_percent=float(deduction_rate_percent),
            days_since_cap_update=int(request.form.get("days_since_cap_update") or 0),
            buyer_capacity_status=request.form.get("buyer_capacity_status", "unknown"),
            replacement_status=request.form.get("replacement_status", "not_needed"),
            replacement_fit_score=int(request.form.get("replacement_fit_score") or 0),
            same_intent_review=same_intent_review,
            source_quality=request.form.get("source_quality", "watch"),
            policy_risk=request.form.get("policy_risk", "medium"),
        )
        offer_id = request.form.get("offer_id")
        replacement_offer_id = request.form.get("replacement_offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = OfferCapReview(
            offer_id=int(offer_id) if offer_id else None,
            replacement_offer_id=int(replacement_offer_id)
            if replacement_offer_id
            else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            offer_status=request.form.get("offer_status", "active"),
            cap_type=request.form.get("cap_type", "daily_conversion"),
            cap_period=request.form.get("cap_period", "daily"),
            cap_limit=cap_limit,
            cap_used=cap_used,
            expected_next_conversions=expected_next_conversions,
            current_payout=current_payout,
            new_payout=new_payout,
            approval_rate_percent=approval_rate_percent,
            paid_rate_percent=paid_rate_percent,
            deduction_rate_percent=deduction_rate_percent,
            days_since_cap_update=int(request.form.get("days_since_cap_update") or 0),
            buyer_capacity_status=request.form.get("buyer_capacity_status", "unknown"),
            replacement_status=request.form.get("replacement_status", "not_needed"),
            replacement_fit_score=int(request.form.get("replacement_fit_score") or 0),
            same_intent_review=same_intent_review,
            source_quality=request.form.get("source_quality", "watch"),
            policy_risk=request.form.get("policy_risk", "medium"),
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            cap_usage_percent=decimal_value(result["cap_usage_percent"]),
            cap_remaining=decimal_value(result["cap_remaining"]),
            effective_payout=decimal_value(result["effective_payout"]),
            safe_daily_media_cost=decimal_value(result["safe_daily_media_cost"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in OFFER_CAP_REVIEW_STATUSES:
            flash("Offer Cap 评审状态不允许。", "warning")
            return redirect(url_for("main.offer_cap_payout"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "offer_cap_review",
            review.id,
            "create",
            f"Created offer cap review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("Offer Cap / Payout 评审已保存。它只生成内部处理建议，不自动切换 Offer 或改预算。", "success")
        return redirect(url_for("main.offer_cap_payout"))

    return render_template(
        "offer_cap_payout.html",
        reviews=OfferCapReview.query.order_by(OfferCapReview.created_at.desc()).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=OFFER_CAP_REVIEW_STATUSES,
    )


@bp.post("/offer-cap-payout/<int:review_id>/status")
def update_offer_cap_payout_status(review_id: int):
    review = OfferCapReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in OFFER_CAP_REVIEW_STATUSES:
        flash("Offer Cap 评审状态不允许。", "warning")
        return redirect(url_for("main.offer_cap_payout"))
    old_status = review.status
    review.status = status
    add_audit(
        "offer_cap_review",
        review.id,
        "status_update",
        f"Offer cap review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("Offer Cap 评审状态已更新。状态只代表内部审批进度，不会自动改广告或联盟后台。", "success")
    return redirect(url_for("main.offer_cap_payout"))


@bp.route("/source-quality", methods=["GET", "POST"])
def source_quality():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("entity_type", ""),
                request.form.get("source_name", ""),
                request.form.get("publisher_name", ""),
                request.form.get("placement_ref", ""),
                request.form.get("subid", ""),
                request.form.get("network", ""),
                request.form.get("sample_url", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_SOURCE_QUALITY_TERMS):
            flash("来源质量评审包含 Cookie、cloaking、模拟流量、防关联、隐藏来源或换号语义，请改走风险审计和修复流程。", "warning")
            return redirect(url_for("main.source_quality"))

        cost = decimal_value(request.form.get("cost"))
        reported_revenue = decimal_value(request.form.get("reported_revenue"))
        approved_revenue = decimal_value(request.form.get("approved_revenue"))
        paid_revenue = decimal_value(request.form.get("paid_revenue"))
        deducted_revenue = decimal_value(request.form.get("deducted_revenue"))
        tracking_completeness_percent = decimal_value(
            request.form.get("tracking_completeness_percent")
        )
        invalid_click_rate_percent = decimal_value(
            request.form.get("invalid_click_rate_percent")
        )
        buyer_reject_rate_percent = decimal_value(
            request.form.get("buyer_reject_rate_percent")
        )
        result = calculate_source_quality_review(
            transparency_level=request.form.get("transparency_level", "partial"),
            tracking_completeness_percent=float(tracking_completeness_percent),
            intent_fit_score=_int(request.form.get("intent_fit_score")),
            clicks=_int(request.form.get("clicks")),
            sessions=_int(request.form.get("sessions")),
            cost=float(cost),
            reported_revenue=float(reported_revenue),
            approved_revenue=float(approved_revenue),
            paid_revenue=float(paid_revenue),
            deducted_revenue=float(deducted_revenue),
            invalid_click_rate_percent=float(invalid_click_rate_percent),
            complaint_count=_int(request.form.get("complaint_count")),
            buyer_reject_rate_percent=float(buyer_reject_rate_percent),
            policy_issue_state=request.form.get("policy_issue_state", "clean"),
            stop_control=request.form.get("stop_control", "partial"),
            consistency_days=_int(request.form.get("consistency_days")),
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = SourceQualityReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            entity_type=request.form.get("entity_type", "source"),
            source_name=request.form["source_name"].strip(),
            publisher_name=request.form.get("publisher_name", "").strip() or None,
            placement_ref=request.form.get("placement_ref", "").strip() or None,
            subid=request.form.get("subid", "").strip() or None,
            network=request.form.get("network", "").strip() or None,
            country=request.form.get("country", "").strip() or None,
            device=request.form.get("device", "").strip() or None,
            sample_url=request.form.get("sample_url", "").strip() or None,
            transparency_level=request.form.get("transparency_level", "partial"),
            tracking_completeness_percent=tracking_completeness_percent,
            intent_fit_score=_int(request.form.get("intent_fit_score")),
            clicks=_int(request.form.get("clicks")),
            sessions=_int(request.form.get("sessions")),
            cost=cost,
            reported_revenue=reported_revenue,
            approved_revenue=approved_revenue,
            paid_revenue=paid_revenue,
            deducted_revenue=deducted_revenue,
            invalid_click_rate_percent=invalid_click_rate_percent,
            complaint_count=_int(request.form.get("complaint_count")),
            buyer_reject_rate_percent=buyer_reject_rate_percent,
            policy_issue_state=request.form.get("policy_issue_state", "clean"),
            stop_control=request.form.get("stop_control", "partial"),
            consistency_days=_int(request.form.get("consistency_days")),
            score=int(result["score"]),
            quality_level=str(result["quality_level"]),
            recommended_action=str(result["recommended_action"]),
            click_session_rate=decimal_value(result["click_session_rate"]),
            approved_rate=decimal_value(result["approved_rate"]),
            paid_rate=decimal_value(result["paid_rate"]),
            deduction_rate=decimal_value(result["deduction_rate"]),
            paid_roi=decimal_value(result["paid_roi"]),
            approved_roi=decimal_value(result["approved_roi"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in SOURCE_QUALITY_REVIEW_STATUSES:
            flash("来源质量评审状态不允许。", "warning")
            return redirect(url_for("main.source_quality"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "source_quality_review",
            review.id,
            "create",
            f"Created source quality review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("来源质量评审已保存。它只生成名单治理和人工停源/恢复建议，不自动买量或改后台。", "success")
        return redirect(url_for("main.source_quality"))

    return render_template(
        "source_quality.html",
        reviews=SourceQualityReview.query.order_by(
            SourceQualityReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=SOURCE_QUALITY_REVIEW_STATUSES,
    )


@bp.post("/source-quality/<int:review_id>/status")
def update_source_quality_status(review_id: int):
    review = SourceQualityReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in SOURCE_QUALITY_REVIEW_STATUSES:
        flash("来源质量评审状态不允许。", "warning")
        return redirect(url_for("main.source_quality"))
    old_status = review.status
    review.status = status
    add_audit(
        "source_quality_review",
        review.id,
        "status_update",
        f"Source quality review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("来源质量状态已更新。状态只代表内部名单治理，不会自动改广告或供应商后台。", "success")
    return redirect(url_for("main.source_quality"))


@bp.route("/vendor-contracts", methods=["GET", "POST"])
def vendor_contracts():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("vendor_name", ""),
                request.form.get("vendor_type", ""),
                request.form.get("io_number", ""),
                request.form.get("line_item_ref", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_VENDOR_CONTRACT_TERMS):
            flash("供应商合同评审包含隐藏来源、Cookie、cloaking、模拟流量、防关联或换号语义，请改走风险审计和修复流程。", "warning")
            return redirect(url_for("main.vendor_contracts"))

        tracking_appendix = request.form.get("tracking_appendix") == "on"
        reporting_appendix = request.form.get("reporting_appendix") == "on"
        quality_clause = request.form.get("quality_clause") == "on"
        refund_clause = request.form.get("refund_clause") == "on"
        tracking_completeness_percent = decimal_value(
            request.form.get("tracking_completeness_percent")
        )
        discrepancy_rate_percent = decimal_value(
            request.form.get("discrepancy_rate_percent")
        )
        invalid_traffic_rate_percent = decimal_value(
            request.form.get("invalid_traffic_rate_percent")
        )
        buyer_reject_rate_percent = decimal_value(
            request.form.get("buyer_reject_rate_percent")
        )
        budget_cap = decimal_value(request.form.get("budget_cap"))
        spend_to_date = decimal_value(request.form.get("spend_to_date"))
        approved_revenue = decimal_value(request.form.get("approved_revenue"))
        paid_revenue = decimal_value(request.form.get("paid_revenue"))
        invoice_amount = decimal_value(request.form.get("invoice_amount"))
        disputed_amount = decimal_value(request.form.get("disputed_amount"))
        refund_credit_amount = decimal_value(request.form.get("refund_credit_amount"))
        makegood_value = decimal_value(request.form.get("makegood_value"))
        result = calculate_vendor_contract_review(
            contract_status=request.form.get("contract_status", "prospect"),
            source_detail_level=request.form.get("source_detail_level", "partial"),
            tracking_appendix=tracking_appendix,
            reporting_appendix=reporting_appendix,
            quality_clause=quality_clause,
            refund_clause=refund_clause,
            stop_control=request.form.get("stop_control", "partial"),
            tracking_completeness_percent=float(tracking_completeness_percent),
            report_delay_days=_int(request.form.get("report_delay_days")),
            discrepancy_rate_percent=float(discrepancy_rate_percent),
            invalid_traffic_rate_percent=float(invalid_traffic_rate_percent),
            buyer_reject_rate_percent=float(buyer_reject_rate_percent),
            approved_revenue=float(approved_revenue),
            paid_revenue=float(paid_revenue),
            spend_to_date=float(spend_to_date),
            invoice_amount=float(invoice_amount),
            disputed_amount=float(disputed_amount),
            refund_credit_amount=float(refund_credit_amount),
            makegood_value=float(makegood_value),
            dispute_response_days=_int(request.form.get("dispute_response_days")),
            payment_terms_days=_int(request.form.get("payment_terms_days")),
            refund_terms_status=request.form.get("refund_terms_status", "missing"),
            policy_issue_state=request.form.get("policy_issue_state", "clean"),
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = VendorContractReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            vendor_name=request.form["vendor_name"].strip(),
            vendor_type=request.form.get("vendor_type", "traffic_vendor"),
            io_number=request.form.get("io_number", "").strip() or None,
            line_item_ref=request.form.get("line_item_ref", "").strip() or None,
            contract_status=request.form.get("contract_status", "prospect"),
            pricing_model=request.form.get("pricing_model", "cpc"),
            source_detail_level=request.form.get("source_detail_level", "partial"),
            tracking_appendix=tracking_appendix,
            reporting_appendix=reporting_appendix,
            quality_clause=quality_clause,
            refund_clause=refund_clause,
            stop_control=request.form.get("stop_control", "partial"),
            tracking_completeness_percent=tracking_completeness_percent,
            report_delay_days=_int(request.form.get("report_delay_days")),
            discrepancy_rate_percent=discrepancy_rate_percent,
            invalid_traffic_rate_percent=invalid_traffic_rate_percent,
            buyer_reject_rate_percent=buyer_reject_rate_percent,
            budget_cap=budget_cap,
            spend_to_date=spend_to_date,
            approved_revenue=approved_revenue,
            paid_revenue=paid_revenue,
            invoice_amount=invoice_amount,
            disputed_amount=disputed_amount,
            refund_credit_amount=refund_credit_amount,
            makegood_value=makegood_value,
            dispute_response_days=_int(request.form.get("dispute_response_days")),
            payment_terms_days=_int(request.form.get("payment_terms_days")),
            refund_terms_status=request.form.get("refund_terms_status", "missing"),
            policy_issue_state=request.form.get("policy_issue_state", "clean"),
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            amount_at_risk=decimal_value(result["amount_at_risk"]),
            paid_roi=decimal_value(result["paid_roi"]),
            approved_roi=decimal_value(result["approved_roi"]),
            invoice_dispute_rate=decimal_value(result["invoice_dispute_rate"]),
            credit_coverage_rate=decimal_value(result["credit_coverage_rate"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in VENDOR_CONTRACT_REVIEW_STATUSES:
            flash("供应商合同评审状态不允许。", "warning")
            return redirect(url_for("main.vendor_contracts"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "vendor_contract_review",
            review.id,
            "create",
            f"Created vendor contract review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("供应商合同/争议评审已保存。它只生成证据包和人工处理建议，不自动采购流量或调用供应商后台。", "success")
        return redirect(url_for("main.vendor_contracts"))

    return render_template(
        "vendor_contracts.html",
        reviews=VendorContractReview.query.order_by(
            VendorContractReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=VENDOR_CONTRACT_REVIEW_STATUSES,
    )


@bp.post("/vendor-contracts/<int:review_id>/status")
def update_vendor_contract_status(review_id: int):
    review = VendorContractReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in VENDOR_CONTRACT_REVIEW_STATUSES:
        flash("供应商合同评审状态不允许。", "warning")
        return redirect(url_for("main.vendor_contracts"))
    old_status = review.status
    review.status = status
    add_audit(
        "vendor_contract_review",
        review.id,
        "status_update",
        f"Vendor contract review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("供应商合同状态已更新。状态只代表内部审批和争议治理，不会自动扣款、采购或改后台。", "success")
    return redirect(url_for("main.vendor_contracts"))


@bp.route("/query-mining", methods=["GET", "POST"])
def query_mining():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("keyword_text", ""),
                request.form.get("search_term", ""),
                request.form.get("campaign_ref", ""),
                request.form.get("ad_group_ref", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_QUERY_MINING_TERMS):
            flash("Query Mining 评审包含模拟搜索、Cookie 抓后台、代理/指纹、补点击、cloaking 或换号语义，请改走风险审计和修复流程。", "warning")
            return redirect(url_for("main.query_mining"))

        cost = decimal_value(request.form.get("cost"))
        approved_revenue = decimal_value(request.form.get("approved_revenue"))
        paid_revenue = decimal_value(request.form.get("paid_revenue"))
        buyer_reject_rate_percent = decimal_value(
            request.form.get("buyer_reject_rate_percent")
        )
        brand_or_official = request.form.get("brand_or_official") == "on"
        support_or_login = request.form.get("support_or_login") == "on"
        result = calculate_query_mining_review(
            query_intent=request.form.get("query_intent", "unknown"),
            keyword_match_type=request.form.get("keyword_match_type", "broad"),
            network=request.form.get("network", "google_search"),
            clicks=_int(request.form.get("clicks")),
            sessions=_int(request.form.get("sessions")),
            conversions=_int(request.form.get("conversions")),
            cost=float(cost),
            approved_revenue=float(approved_revenue),
            paid_revenue=float(paid_revenue),
            buyer_reject_rate_percent=float(buyer_reject_rate_percent),
            intent_fit_score=_int(request.form.get("intent_fit_score")),
            policy_risk=request.form.get("policy_risk", "medium"),
            revenue_status=request.form.get("revenue_status", "none"),
            data_status=request.form.get("data_status", "fresh"),
            conversion_lag_days=_int(request.form.get("conversion_lag_days")),
            brand_or_official=brand_or_official,
            support_or_login=support_or_login,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = QueryMiningReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            date_window=request.form.get("date_window", "").strip() or None,
            ads_customer_id=request.form.get("ads_customer_id", "").strip() or None,
            campaign_ref=request.form.get("campaign_ref", "").strip() or None,
            ad_group_ref=request.form.get("ad_group_ref", "").strip() or None,
            keyword_text=request.form.get("keyword_text", "").strip() or None,
            keyword_match_type=request.form.get("keyword_match_type", "broad"),
            search_term=request.form["search_term"].strip(),
            search_term_match_type=request.form.get(
                "search_term_match_type", ""
            ).strip()
            or None,
            query_intent=request.form.get("query_intent", "unknown"),
            network=request.form.get("network", "google_search"),
            device=request.form.get("device", "").strip() or None,
            country=request.form.get("country", "").strip() or None,
            landing_version=request.form.get("landing_version", "").strip() or None,
            source_file_hash=request.form.get("source_file_hash", "").strip() or None,
            clicks=_int(request.form.get("clicks")),
            sessions=_int(request.form.get("sessions")),
            conversions=_int(request.form.get("conversions")),
            cost=cost,
            approved_revenue=approved_revenue,
            paid_revenue=paid_revenue,
            buyer_reject_rate_percent=buyer_reject_rate_percent,
            intent_fit_score=_int(request.form.get("intent_fit_score")),
            policy_risk=request.form.get("policy_risk", "medium"),
            revenue_status=request.form.get("revenue_status", "none"),
            data_status=request.form.get("data_status", "fresh"),
            conversion_lag_days=_int(request.form.get("conversion_lag_days")),
            brand_or_official=brand_or_official,
            support_or_login=support_or_login,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            negative_match_type=str(result["negative_match_type"]),
            negative_level=str(result["negative_level"]),
            click_session_rate=decimal_value(result["click_session_rate"]),
            cpc=decimal_value(result["cpc"]),
            approved_rpv=decimal_value(result["approved_rpv"]),
            paid_rpv=decimal_value(result["paid_rpv"]),
            approved_roi=decimal_value(result["approved_roi"]),
            paid_roi=decimal_value(result["paid_roi"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in QUERY_MINING_REVIEW_STATUSES:
            flash("Query Mining 评审状态不允许。", "warning")
            return redirect(url_for("main.query_mining"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "query_mining_review",
            review.id,
            "create",
            f"Created query mining review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("Query Mining 评审已保存。它只生成待审核否定词、加词、拆组或页面建议，不自动搜索、点击或改后台。", "success")
        return redirect(url_for("main.query_mining"))

    return render_template(
        "query_mining.html",
        reviews=QueryMiningReview.query.order_by(
            QueryMiningReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=QUERY_MINING_REVIEW_STATUSES,
    )


@bp.post("/query-mining/<int:review_id>/status")
def update_query_mining_status(review_id: int):
    review = QueryMiningReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in QUERY_MINING_REVIEW_STATUSES:
        flash("Query Mining 评审状态不允许。", "warning")
        return redirect(url_for("main.query_mining"))
    old_status = review.status
    review.status = status
    add_audit(
        "query_mining_review",
        review.id,
        "status_update",
        f"Query mining review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("Query Mining 状态已更新。状态只代表内部审批，不会自动改否定词、关键词或广告后台。", "success")
    return redirect(url_for("main.query_mining"))


@bp.route("/bulk-upload", methods=["GET", "POST"])
def bulk_upload():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("export_type", ""),
                request.form.get("batch_id", ""),
                request.form.get("csv_hash", ""),
                request.form.get("payload_hash", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_BULK_UPLOAD_TERMS):
            flash("批量变更评审包含自动发布、Cookie、绕审核、模拟流量、防关联或换号语义，请改走风险审计和修复流程。", "warning")
            return redirect(url_for("main.bulk_upload"))

        expected_budget_delta = decimal_value(
            request.form.get("expected_budget_delta")
        )
        default_paused = request.form.get("default_paused") == "on"
        human_review = request.form.get("human_review") == "on"
        change_history_attached = request.form.get("change_history_attached") == "on"
        rollback_plan = request.form.get("rollback_plan") == "on"
        target_customer_confirmed = (
            request.form.get("target_customer_confirmed") == "on"
        )
        policy_review_complete = request.form.get("policy_review_complete") == "on"
        result = calculate_bulk_upload_review(
            export_type=request.form.get("export_type", "editor_csv"),
            preflight_status=request.form.get("preflight_status", "warnings"),
            row_count=_int(request.form.get("row_count")),
            keyword_count=_int(request.form.get("keyword_count")),
            ad_count=_int(request.form.get("ad_count")),
            expected_budget_delta=float(expected_budget_delta),
            url_change_count=_int(request.form.get("url_change_count")),
            default_paused=default_paused,
            human_review=human_review,
            preview_status=request.form.get("preview_status", "not_run"),
            editor_check_status=request.form.get("editor_check_status", "not_run"),
            post_status=request.form.get("post_status", "not_posted"),
            change_history_attached=change_history_attached,
            rollback_plan=rollback_plan,
            target_customer_confirmed=target_customer_confirmed,
            policy_review_complete=policy_review_complete,
            high_risk_change_count=_int(request.form.get("high_risk_change_count")),
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = BulkUploadReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            export_type=request.form.get("export_type", "editor_csv"),
            batch_id=request.form.get("batch_id", "").strip() or None,
            csv_hash=request.form.get("csv_hash", "").strip() or None,
            payload_hash=request.form.get("payload_hash", "").strip() or None,
            row_count=_int(request.form.get("row_count")),
            keyword_count=_int(request.form.get("keyword_count")),
            ad_count=_int(request.form.get("ad_count")),
            target_customer_id=request.form.get("target_customer_id", "").strip()
            or None,
            account_timezone=request.form.get("account_timezone", "").strip() or None,
            currency=request.form.get("currency", "").strip() or None,
            expected_budget_delta=expected_budget_delta,
            url_change_count=_int(request.form.get("url_change_count")),
            high_risk_change_count=_int(request.form.get("high_risk_change_count")),
            preflight_status=request.form.get("preflight_status", "warnings"),
            preview_status=request.form.get("preview_status", "not_run"),
            editor_check_status=request.form.get("editor_check_status", "not_run"),
            post_status=request.form.get("post_status", "not_posted"),
            default_paused=default_paused,
            human_review=human_review,
            change_history_attached=change_history_attached,
            rollback_plan=rollback_plan,
            target_customer_confirmed=target_customer_confirmed,
            policy_review_complete=policy_review_complete,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            budget_delta_percent=decimal_value(result["budget_delta_percent"]),
            change_scope=str(result["change_scope"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in BULK_UPLOAD_REVIEW_STATUSES:
            flash("批量变更评审状态不允许。", "warning")
            return redirect(url_for("main.bulk_upload"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "bulk_upload_review",
            review.id,
            "create",
            f"Created bulk upload review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("批量变更评审已保存。它只生成人工发布门禁和证据，不自动导入、发布或改后台。", "success")
        return redirect(url_for("main.bulk_upload"))

    return render_template(
        "bulk_upload.html",
        reviews=BulkUploadReview.query.order_by(
            BulkUploadReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=BULK_UPLOAD_REVIEW_STATUSES,
    )


@bp.post("/bulk-upload/<int:review_id>/status")
def update_bulk_upload_status(review_id: int):
    review = BulkUploadReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in BULK_UPLOAD_REVIEW_STATUSES:
        flash("批量变更评审状态不允许。", "warning")
        return redirect(url_for("main.bulk_upload"))
    old_status = review.status
    review.status = status
    add_audit(
        "bulk_upload_review",
        review.id,
        "status_update",
        f"Bulk upload review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("批量变更状态已更新。状态只代表内部审批，不会自动发布或应用变更。", "success")
    return redirect(url_for("main.bulk_upload"))


@bp.route("/scripts-sync", methods=["GET", "POST"])
def scripts_sync():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("auth_mode", ""),
                request.form.get("sync_type", ""),
                request.form.get("script_name", ""),
                request.form.get("customer_id", ""),
                request.form.get("query_or_report", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_SCRIPT_SYNC_TERMS):
            flash("Scripts 同步评审包含 Cookie、登录挑战、自动发布、伪造报表、模拟流量、防关联或换号语义，请改走风险审计和修复流程。", "warning")
            return redirect(url_for("main.scripts_sync"))

        change_history_checked = request.form.get("change_history_checked") == "on"
        preview_only = request.form.get("preview_only") == "on"
        human_review = request.form.get("human_review") == "on"
        source_snapshot_hash = request.form.get("source_snapshot_hash", "").strip()
        payload_hash = request.form.get("payload_hash", "").strip()
        result = calculate_script_sync_review(
            auth_mode=request.form.get("auth_mode", "scripts_authorized"),
            sync_type=request.form.get("sync_type", "metrics_daily"),
            data_status=request.form.get("data_status", "provisional"),
            revenue_status=request.form.get("revenue_status", "estimated"),
            freshness_minutes=_int(request.form.get("freshness_minutes")),
            row_count=_int(request.form.get("row_count")),
            error_count=_int(request.form.get("error_count")),
            warning_count=_int(request.form.get("warning_count")),
            source_snapshot_hash_present=bool(source_snapshot_hash),
            payload_hash_present=bool(payload_hash),
            change_history_checked=change_history_checked,
            external_change_count=_int(request.form.get("external_change_count")),
            conflict_status=request.form.get("conflict_status", "clean"),
            rerun_window_days=_int(request.form.get("rerun_window_days")),
            preview_only=preview_only,
            human_review=human_review,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = ScriptSyncReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            auth_mode=request.form.get("auth_mode", "scripts_authorized"),
            sync_type=request.form.get("sync_type", "metrics_daily"),
            script_name=request.form.get("script_name", "").strip() or None,
            customer_id=request.form.get("customer_id", "").strip() or None,
            date_range=request.form.get("date_range", "").strip() or None,
            account_timezone=request.form.get("account_timezone", "").strip() or None,
            currency=request.form.get("currency", "").strip() or None,
            query_or_report=request.form.get("query_or_report", "").strip() or None,
            source_snapshot_hash=source_snapshot_hash or None,
            payload_hash=payload_hash or None,
            row_count=_int(request.form.get("row_count")),
            error_count=_int(request.form.get("error_count")),
            warning_count=_int(request.form.get("warning_count")),
            freshness_minutes=_int(request.form.get("freshness_minutes")),
            rerun_window_days=_int(request.form.get("rerun_window_days")),
            data_status=request.form.get("data_status", "provisional"),
            revenue_status=request.form.get("revenue_status", "estimated"),
            conflict_status=request.form.get("conflict_status", "clean"),
            external_change_count=_int(request.form.get("external_change_count")),
            change_history_checked=change_history_checked,
            preview_only=preview_only,
            human_review=human_review,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            freshness_level=str(result["freshness_level"]),
            recommended_action=str(result["recommended_action"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in SCRIPT_SYNC_REVIEW_STATUSES:
            flash("Scripts 同步评审状态不允许。", "warning")
            return redirect(url_for("main.scripts_sync"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "script_sync_review",
            review.id,
            "create",
            f"Created script sync review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("Scripts 同步评审已保存。它只记录同步证据、冲突和人工导入门禁，不自动登录、apply 或改后台。", "success")
        return redirect(url_for("main.scripts_sync"))

    return render_template(
        "scripts_sync.html",
        reviews=ScriptSyncReview.query.order_by(
            ScriptSyncReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=SCRIPT_SYNC_REVIEW_STATUSES,
    )


@bp.post("/scripts-sync/<int:review_id>/status")
def update_scripts_sync_status(review_id: int):
    review = ScriptSyncReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in SCRIPT_SYNC_REVIEW_STATUSES:
        flash("Scripts 同步评审状态不允许。", "warning")
        return redirect(url_for("main.scripts_sync"))
    old_status = review.status
    review.status = status
    add_audit(
        "script_sync_review",
        review.id,
        "status_update",
        f"Script sync review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("Scripts 同步状态已更新。状态只代表内部审批和对账进度，不会自动 apply 或修改后台。", "success")
    return redirect(url_for("main.scripts_sync"))


@bp.route("/taxonomy-governance", methods=["GET", "POST"])
def taxonomy_governance():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("campaign_name", ""),
                request.form.get("ad_group_name", ""),
                request.form.get("labels_text", ""),
                request.form.get("utm_source", ""),
                request.form.get("utm_medium", ""),
                request.form.get("utm_campaign", ""),
                request.form.get("utm_id", ""),
                request.form.get("utm_content", ""),
                request.form.get("utm_term", ""),
                request.form.get("valuetrack_template", ""),
                request.form.get("custom_parameter_map", ""),
                request.form.get("subid_map", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_TAXONOMY_TERMS):
            flash("命名维度评审包含 PII、敏感属性、Cookie、隐藏来源、移除追踪、绕审核或换号语义，请改走风险审计和追踪修复流程。", "warning")
            return redirect(url_for("main.taxonomy_governance"))

        gclid_preserved = request.form.get("gclid_preserved") == "on"
        click_id_preserved = request.form.get("click_id_preserved") == "on"
        lowercase_normalized = request.form.get("lowercase_normalized") == "on"
        url_encoded = request.form.get("url_encoded") == "on"
        no_pii_in_url = request.form.get("no_pii_in_url") == "on"
        no_sensitive_attributes = request.form.get("no_sensitive_attributes") == "on"
        human_review = request.form.get("human_review") == "on"
        result = calculate_taxonomy_review(
            campaign_name=request.form.get("campaign_name", ""),
            ad_group_name=request.form.get("ad_group_name", ""),
            labels_text=request.form.get("labels_text", ""),
            utm_source=request.form.get("utm_source", ""),
            utm_medium=request.form.get("utm_medium", ""),
            utm_campaign=request.form.get("utm_campaign", ""),
            utm_id=request.form.get("utm_id", ""),
            utm_content=request.form.get("utm_content", ""),
            utm_term=request.form.get("utm_term", ""),
            valuetrack_template=request.form.get("valuetrack_template", ""),
            custom_parameter_map=request.form.get("custom_parameter_map", ""),
            subid_map=request.form.get("subid_map", ""),
            dimension_dictionary_version=request.form.get(
                "dimension_dictionary_version", ""
            ),
            parameter_map_version=request.form.get("parameter_map_version", ""),
            landing_version=request.form.get("landing_version", ""),
            link_version=request.form.get("link_version", ""),
            creative_version=request.form.get("creative_version", ""),
            payload_hash=request.form.get("payload_hash", ""),
            report_join_gap_count=_int(request.form.get("report_join_gap_count")),
            gclid_preserved=gclid_preserved,
            click_id_preserved=click_id_preserved,
            lowercase_normalized=lowercase_normalized,
            url_encoded=url_encoded,
            no_pii_in_url=no_pii_in_url,
            no_sensitive_attributes=no_sensitive_attributes,
            human_review=human_review,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = TaxonomyReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            campaign_name=request.form.get("campaign_name", "").strip(),
            ad_group_name=request.form.get("ad_group_name", "").strip(),
            labels_text=request.form.get("labels_text", "").strip() or None,
            utm_source=request.form.get("utm_source", "").strip() or None,
            utm_medium=request.form.get("utm_medium", "").strip() or None,
            utm_campaign=request.form.get("utm_campaign", "").strip() or None,
            utm_id=request.form.get("utm_id", "").strip() or None,
            utm_content=request.form.get("utm_content", "").strip() or None,
            utm_term=request.form.get("utm_term", "").strip() or None,
            valuetrack_template=request.form.get("valuetrack_template", "").strip()
            or None,
            custom_parameter_map=request.form.get("custom_parameter_map", "").strip()
            or None,
            subid_map=request.form.get("subid_map", "").strip() or None,
            dimension_dictionary_version=request.form.get(
                "dimension_dictionary_version", ""
            ).strip()
            or None,
            parameter_map_version=request.form.get(
                "parameter_map_version", ""
            ).strip()
            or None,
            landing_version=request.form.get("landing_version", "").strip() or None,
            link_version=request.form.get("link_version", "").strip() or None,
            creative_version=request.form.get("creative_version", "").strip()
            or None,
            payload_hash=request.form.get("payload_hash", "").strip() or None,
            report_join_gap_count=_int(request.form.get("report_join_gap_count")),
            gclid_preserved=gclid_preserved,
            click_id_preserved=click_id_preserved,
            lowercase_normalized=lowercase_normalized,
            url_encoded=url_encoded,
            no_pii_in_url=no_pii_in_url,
            no_sensitive_attributes=no_sensitive_attributes,
            human_review=human_review,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            missing_campaign_tokens=result["missing_campaign_tokens"],
            missing_utm_fields=result["missing_utm_fields"],
            missing_label_groups=result["missing_label_groups"],
            valuetrack_fields=result["valuetrack_fields"],
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in TAXONOMY_REVIEW_STATUSES:
            flash("命名维度评审状态不允许。", "warning")
            return redirect(url_for("main.taxonomy_governance"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "taxonomy_review",
            review.id,
            "create",
            f"Created taxonomy review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("命名维度评审已保存。它只记录命名、UTM/SubID、版本和 join key 证据，不自动改后台或隐藏来源。", "success")
        return redirect(url_for("main.taxonomy_governance"))

    return render_template(
        "taxonomy_governance.html",
        reviews=TaxonomyReview.query.order_by(TaxonomyReview.created_at.desc()).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=TAXONOMY_REVIEW_STATUSES,
    )


@bp.post("/taxonomy-governance/<int:review_id>/status")
def update_taxonomy_governance_status(review_id: int):
    review = TaxonomyReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in TAXONOMY_REVIEW_STATUSES:
        flash("命名维度评审状态不允许。", "warning")
        return redirect(url_for("main.taxonomy_governance"))
    old_status = review.status
    review.status = status
    add_audit(
        "taxonomy_review",
        review.id,
        "status_update",
        f"Taxonomy review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("命名维度状态已更新。状态只代表内部 QA 进度，不会自动改 campaign、URL 或后台标签。", "success")
    return redirect(url_for("main.taxonomy_governance"))


@bp.route("/attribution", methods=["GET", "POST"])
def attribution():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("test_type", ""),
                request.form.get("hypothesis", ""),
                request.form.get("treatment_scope", ""),
                request.form.get("control_scope", ""),
                request.form.get("split_method", ""),
                request.form.get("guardrail_metrics", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_ATTRIBUTION_TERMS):
            flash("归因增量评审包含伪造转化、补点击、隐藏来源、Cookie、cloaking、自动应用 winner 或换号语义，请改走风险审计和对账流程。", "warning")
            return redirect(url_for("main.attribution"))

        attributed_revenue = decimal_value(request.form.get("attributed_revenue"))
        treatment_revenue = decimal_value(request.form.get("treatment_revenue"))
        control_revenue = decimal_value(request.form.get("control_revenue"))
        ad_cost = decimal_value(request.form.get("ad_cost"))
        variable_cost = decimal_value(request.form.get("variable_cost"))
        confidence_level = decimal_value(request.form.get("confidence_level"))
        change_history_clean = request.form.get("change_history_clean") == "on"
        single_variable_test = request.form.get("single_variable_test") == "on"
        approved_paid_evidence = request.form.get("approved_paid_evidence") == "on"
        human_review = request.form.get("human_review") == "on"
        result = calculate_attribution_review(
            test_type=request.form.get("test_type", "geo_holdout"),
            holdout_quality=request.form.get("holdout_quality", "none"),
            revenue_status=request.form.get("revenue_status", "submitted"),
            data_status=request.form.get("data_status", "fresh"),
            attributed_revenue=float(attributed_revenue),
            treatment_revenue=float(treatment_revenue),
            control_revenue=float(control_revenue),
            ad_cost=float(ad_cost),
            variable_cost=float(variable_cost),
            attributed_conversions=_int(request.form.get("attributed_conversions")),
            incremental_conversions=_int(request.form.get("incremental_conversions")),
            sample_size=_int(request.form.get("sample_size")),
            confidence_level=float(confidence_level),
            brand_cannibalization_risk=request.form.get(
                "brand_cannibalization_risk", "medium"
            ),
            organic_cannibalization_risk=request.form.get(
                "organic_cannibalization_risk", "medium"
            ),
            remarketing_cannibalization_risk=request.form.get(
                "remarketing_cannibalization_risk", "medium"
            ),
            pmax_broad_overlap_risk=request.form.get(
                "pmax_broad_overlap_risk", "medium"
            ),
            change_history_clean=change_history_clean,
            single_variable_test=single_variable_test,
            approved_paid_evidence=approved_paid_evidence,
            human_review=human_review,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = AttributionReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            test_type=request.form.get("test_type", "geo_holdout"),
            attribution_model=request.form.get("attribution_model", "data_driven"),
            hypothesis=request.form.get("hypothesis", "").strip() or None,
            treatment_scope=request.form.get("treatment_scope", "").strip() or None,
            control_scope=request.form.get("control_scope", "").strip() or None,
            split_method=request.form.get("split_method", "").strip() or None,
            date_window=request.form.get("date_window", "").strip() or None,
            primary_metric=request.form.get("primary_metric", "").strip() or None,
            guardrail_metrics=request.form.get("guardrail_metrics", "").strip()
            or None,
            attributed_revenue=attributed_revenue,
            treatment_revenue=treatment_revenue,
            control_revenue=control_revenue,
            incremental_revenue=decimal_value(result["incremental_revenue"]),
            ad_cost=ad_cost,
            variable_cost=variable_cost,
            incremental_profit=decimal_value(result["incremental_profit"]),
            i_roas=decimal_value(result["i_roas"]),
            attributed_to_incremental_ratio=decimal_value(
                result["attributed_to_incremental_ratio"]
            ),
            attributed_conversions=_int(request.form.get("attributed_conversions")),
            incremental_conversions=_int(
                request.form.get("incremental_conversions")
            ),
            sample_size=_int(request.form.get("sample_size")),
            confidence_level=confidence_level,
            holdout_quality=request.form.get("holdout_quality", "none"),
            revenue_status=request.form.get("revenue_status", "submitted"),
            data_status=request.form.get("data_status", "fresh"),
            brand_cannibalization_risk=request.form.get(
                "brand_cannibalization_risk", "medium"
            ),
            organic_cannibalization_risk=request.form.get(
                "organic_cannibalization_risk", "medium"
            ),
            remarketing_cannibalization_risk=request.form.get(
                "remarketing_cannibalization_risk", "medium"
            ),
            pmax_broad_overlap_risk=request.form.get(
                "pmax_broad_overlap_risk", "medium"
            ),
            change_history_clean=change_history_clean,
            single_variable_test=single_variable_test,
            approved_paid_evidence=approved_paid_evidence,
            human_review=human_review,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in ATTRIBUTION_REVIEW_STATUSES:
            flash("归因增量评审状态不允许。", "warning")
            return redirect(url_for("main.attribution"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "attribution_review",
            review.id,
            "create",
            f"Created attribution review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("归因增量评审已保存。它只记录实验、holdout、iROAS 和蚕食证据，不自动创建实验或应用 winner。", "success")
        return redirect(url_for("main.attribution"))

    return render_template(
        "attribution.html",
        reviews=AttributionReview.query.order_by(
            AttributionReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=ATTRIBUTION_REVIEW_STATUSES,
    )


@bp.post("/attribution/<int:review_id>/status")
def update_attribution_status(review_id: int):
    review = AttributionReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in ATTRIBUTION_REVIEW_STATUSES:
        flash("归因增量评审状态不允许。", "warning")
        return redirect(url_for("main.attribution"))
    old_status = review.status
    review.status = status
    add_audit(
        "attribution_review",
        review.id,
        "status_update",
        f"Attribution review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("归因增量状态已更新。状态只代表内部评审，不会自动扩量、暂停或改后台。", "success")
    return redirect(url_for("main.attribution"))


@bp.route("/cpl-verticals", methods=["GET", "POST"])
def cpl_verticals():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("vertical", ""),
                request.form.get("subvertical", ""),
                request.form.get("buyer_type", ""),
                request.form.get("qualification_fields", ""),
                request.form.get("sensitive_fields", ""),
                request.form.get("reject_reason_map", ""),
                request.form.get("accepted_definition", ""),
                request.form.get("paid_definition", ""),
                request.form.get("policy_requirements", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_CPL_VERTICAL_TERMS):
            flash("CPL 垂类评审包含伪造 lead、自动提交表单、伪造 consent、绕认证、Cookie、cloaking、防关联或换号语义，请改走风险审计和修复流程。", "warning")
            return redirect(url_for("main.cpl_verticals"))

        payout_amount = decimal_value(request.form.get("payout_amount"))
        estimated_cpc = decimal_value(request.form.get("estimated_cpc"))
        landing_cvr_percent = decimal_value(request.form.get("landing_cvr_percent"))
        accepted_rate_percent = decimal_value(
            request.form.get("accepted_rate_percent")
        )
        qualified_rate_percent = decimal_value(
            request.form.get("qualified_rate_percent")
        )
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        deduction_rate_percent = decimal_value(
            request.form.get("deduction_rate_percent")
        )
        chargeback_rate_percent = decimal_value(
            request.form.get("chargeback_rate_percent")
        )
        required_fields_mapped = request.form.get("required_fields_mapped") == "on"
        reject_reason_map_ready = request.form.get("reject_reason_map_ready") == "on"
        accepted_definition_clear = (
            request.form.get("accepted_definition_clear") == "on"
        )
        paid_definition_clear = request.form.get("paid_definition_clear") == "on"
        pii_minimization = request.form.get("pii_minimization") == "on"
        license_required = request.form.get("license_required") == "on"
        license_evidence_present = (
            request.form.get("license_evidence_present") == "on"
        )
        human_review = request.form.get("human_review") == "on"
        result = calculate_cpl_vertical_review(
            vertical=request.form.get("vertical", "insurance"),
            payout_amount=float(payout_amount),
            estimated_cpc=float(estimated_cpc),
            landing_cvr_percent=float(landing_cvr_percent),
            accepted_rate_percent=float(accepted_rate_percent),
            qualified_rate_percent=float(qualified_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            deduction_rate_percent=float(deduction_rate_percent),
            chargeback_rate_percent=float(chargeback_rate_percent),
            feedback_lag_days=_int(request.form.get("feedback_lag_days")),
            contact_sla_minutes=_int(request.form.get("contact_sla_minutes")),
            required_fields_mapped=required_fields_mapped,
            reject_reason_map_ready=reject_reason_map_ready,
            accepted_definition_clear=accepted_definition_clear,
            paid_definition_clear=paid_definition_clear,
            consent_disclosure_status=request.form.get(
                "consent_disclosure_status", "missing"
            ),
            pii_minimization=pii_minimization,
            license_required=license_required,
            license_evidence_present=license_evidence_present,
            buyer_terms_status=request.form.get("buyer_terms_status", "missing"),
            source_quality=request.form.get("source_quality", "medium"),
            policy_risk=request.form.get("policy_risk", "medium"),
            data_sensitivity=request.form.get("data_sensitivity", "medium"),
            human_review=human_review,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = CplVerticalReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            vertical=request.form.get("vertical", "insurance"),
            subvertical=request.form.get("subvertical", "").strip() or None,
            country=request.form.get("country", "").strip() or None,
            buyer_type=request.form.get("buyer_type", "").strip() or None,
            payout_model=request.form.get("payout_model", "CPL"),
            payout_amount=payout_amount,
            estimated_cpc=estimated_cpc,
            landing_cvr_percent=landing_cvr_percent,
            accepted_rate_percent=accepted_rate_percent,
            qualified_rate_percent=qualified_rate_percent,
            paid_rate_percent=paid_rate_percent,
            deduction_rate_percent=deduction_rate_percent,
            chargeback_rate_percent=chargeback_rate_percent,
            feedback_lag_days=_int(request.form.get("feedback_lag_days")),
            contact_sla_minutes=_int(request.form.get("contact_sla_minutes")),
            qualification_fields=request.form.get("qualification_fields", "").strip()
            or None,
            sensitive_fields=request.form.get("sensitive_fields", "").strip() or None,
            reject_reason_map=request.form.get("reject_reason_map", "").strip()
            or None,
            accepted_definition=request.form.get(
                "accepted_definition", ""
            ).strip()
            or None,
            paid_definition=request.form.get("paid_definition", "").strip() or None,
            policy_requirements=request.form.get("policy_requirements", "").strip()
            or None,
            forbidden_claims=request.form.get("forbidden_claims", "").strip()
            or None,
            required_fields_mapped=required_fields_mapped,
            reject_reason_map_ready=reject_reason_map_ready,
            accepted_definition_clear=accepted_definition_clear,
            paid_definition_clear=paid_definition_clear,
            consent_disclosure_status=request.form.get(
                "consent_disclosure_status", "missing"
            ),
            pii_minimization=pii_minimization,
            license_required=license_required,
            license_evidence_present=license_evidence_present,
            buyer_terms_status=request.form.get("buyer_terms_status", "missing"),
            source_quality=request.form.get("source_quality", "medium"),
            policy_risk=request.form.get("policy_risk", "medium"),
            data_sensitivity=request.form.get("data_sensitivity", "medium"),
            human_review=human_review,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            effective_payout=decimal_value(result["effective_payout"]),
            expected_value_per_click=decimal_value(
                result["expected_value_per_click"]
            ),
            safe_cpc=decimal_value(result["safe_cpc"]),
            cpc_margin_percent=decimal_value(result["cpc_margin_percent"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in CPL_VERTICAL_REVIEW_STATUSES:
            flash("CPL 垂类评审状态不允许。", "warning")
            return redirect(url_for("main.cpl_verticals"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "cpl_vertical_review",
            review.id,
            "create",
            f"Created CPL vertical review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash("CPL 垂类评审已保存。它只记录资格、buyer acceptance、收入口径和政策证据，不生成 lead 或提交表单。", "success")
        return redirect(url_for("main.cpl_verticals"))

    return render_template(
        "cpl_verticals.html",
        reviews=CplVerticalReview.query.order_by(
            CplVerticalReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=CPL_VERTICAL_REVIEW_STATUSES,
    )


@bp.post("/cpl-verticals/<int:review_id>/status")
def update_cpl_vertical_status(review_id: int):
    review = CplVerticalReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in CPL_VERTICAL_REVIEW_STATUSES:
        flash("CPL 垂类评审状态不允许。", "warning")
        return redirect(url_for("main.cpl_verticals"))
    old_status = review.status
    review.status = status
    add_audit(
        "cpl_vertical_review",
        review.id,
        "status_update",
        f"CPL vertical review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("CPL 垂类状态已更新。状态只代表内部评审，不会自动生成 lead、改 routing 或改广告后台。", "success")
    return redirect(url_for("main.cpl_verticals"))


@bp.route("/lead-pricing", methods=["GET", "POST"])
def lead_pricing():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("buyer_name", ""),
                request.form.get("vertical", ""),
                request.form.get("geo", ""),
                request.form.get("source_type", ""),
                request.form.get("exclusivity", ""),
                request.form.get("payout_model", ""),
                request.form.get("qualification_definition", ""),
                request.form.get("rate_card_evidence", ""),
                request.form.get("negotiation_evidence", ""),
                request.form.get("reject_reason_summary", ""),
                request.form.get("invoice_terms", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_LEAD_PRICING_TERMS):
            flash(
                "Lead 定价评审包含伪造 lead/结算/发票/consent、隐藏来源、Cookie、cloaking、防关联、自动谈价或换号语义，请改走风险审计和证据修复流程。",
                "warning",
            )
            return redirect(url_for("main.lead_pricing"))

        headline_payout = decimal_value(request.form.get("headline_payout"))
        unit_payout = decimal_value(request.form.get("unit_payout"))
        proposed_payout = decimal_value(request.form.get("proposed_payout"))
        minimum_acceptable_payout = decimal_value(
            request.form.get("minimum_acceptable_payout")
        )
        estimated_cpc = decimal_value(request.form.get("estimated_cpc"))
        click_to_lead_rate_percent = decimal_value(
            request.form.get("click_to_lead_rate_percent")
        )
        accepted_rate_percent = decimal_value(
            request.form.get("accepted_rate_percent")
        )
        qualified_rate_percent = decimal_value(
            request.form.get("qualified_rate_percent")
        )
        approval_rate_percent = decimal_value(
            request.form.get("approval_rate_percent")
        )
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        return_rate_percent = decimal_value(request.form.get("return_rate_percent"))
        scrub_buffer_percent = decimal_value(request.form.get("scrub_buffer_percent"))
        chargeback_rate_percent = decimal_value(
            request.form.get("chargeback_rate_percent")
        )
        variable_cost_per_click = decimal_value(
            request.form.get("variable_cost_per_click")
        )
        tracking_cost_per_click = decimal_value(
            request.form.get("tracking_cost_per_click")
        )
        content_cost_per_click = decimal_value(
            request.form.get("content_cost_per_click")
        )
        cashflow_cost_percent = decimal_value(
            request.form.get("cashflow_cost_percent")
        )
        cap_limit = decimal_value(request.form.get("cap_limit"))
        expected_volume = decimal_value(request.form.get("expected_volume"))
        reject_reason_map_ready = request.form.get("reject_reason_map_ready") == "on"
        invoice_evidence = request.form.get("invoice_evidence") == "on"
        dispute_reserve_present = (
            request.form.get("dispute_reserve_present") == "on"
        )
        human_review = request.form.get("human_review") == "on"
        result = calculate_lead_pricing_review(
            payout_model=request.form.get("payout_model", "qualified_cpl"),
            headline_payout=float(headline_payout),
            unit_payout=float(unit_payout),
            proposed_payout=float(proposed_payout),
            minimum_acceptable_payout=float(minimum_acceptable_payout),
            estimated_cpc=float(estimated_cpc),
            click_to_lead_rate_percent=float(click_to_lead_rate_percent),
            accepted_rate_percent=float(accepted_rate_percent),
            qualified_rate_percent=float(qualified_rate_percent),
            approval_rate_percent=float(approval_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            return_rate_percent=float(return_rate_percent),
            scrub_buffer_percent=float(scrub_buffer_percent),
            chargeback_rate_percent=float(chargeback_rate_percent),
            variable_cost_per_click=float(variable_cost_per_click),
            tracking_cost_per_click=float(tracking_cost_per_click),
            content_cost_per_click=float(content_cost_per_click),
            cashflow_cost_percent=float(cashflow_cost_percent),
            cap_limit=float(cap_limit),
            expected_volume=float(expected_volume),
            return_window_days=_int(request.form.get("return_window_days")),
            payment_term_days=_int(request.form.get("payment_term_days")),
            quality_evidence_status=request.form.get(
                "quality_evidence_status", "missing"
            ),
            source_transparency=request.form.get("source_transparency", "partial"),
            consent_evidence=request.form.get("consent_evidence", "missing"),
            reject_reason_map_ready=reject_reason_map_ready,
            invoice_evidence=invoice_evidence,
            dispute_reserve_present=dispute_reserve_present,
            buyer_terms_status=request.form.get("buyer_terms_status", "missing"),
            human_review=human_review,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = LeadPricingReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            buyer_name=request.form.get("buyer_name", "").strip() or None,
            vertical=request.form.get("vertical", "b2b_saas"),
            geo=request.form.get("geo", "").strip() or None,
            source_type=request.form.get("source_type", "search"),
            exclusivity=request.form.get("exclusivity", "exclusive"),
            payout_model=request.form.get("payout_model", "qualified_cpl"),
            headline_payout=headline_payout,
            unit_payout=unit_payout,
            proposed_payout=proposed_payout,
            minimum_acceptable_payout=minimum_acceptable_payout,
            currency=request.form.get("currency", "USD").strip() or "USD",
            estimated_cpc=estimated_cpc,
            click_to_lead_rate_percent=click_to_lead_rate_percent,
            accepted_rate_percent=accepted_rate_percent,
            qualified_rate_percent=qualified_rate_percent,
            approval_rate_percent=approval_rate_percent,
            paid_rate_percent=paid_rate_percent,
            return_rate_percent=return_rate_percent,
            scrub_buffer_percent=scrub_buffer_percent,
            chargeback_rate_percent=chargeback_rate_percent,
            variable_cost_per_click=variable_cost_per_click,
            tracking_cost_per_click=tracking_cost_per_click,
            content_cost_per_click=content_cost_per_click,
            cashflow_cost_percent=cashflow_cost_percent,
            cap_limit=cap_limit,
            expected_volume=expected_volume,
            return_window_days=_int(request.form.get("return_window_days")),
            payment_term_days=_int(request.form.get("payment_term_days")),
            qualification_definition=request.form.get(
                "qualification_definition", ""
            ).strip()
            or None,
            rate_card_evidence=request.form.get("rate_card_evidence", "").strip()
            or None,
            negotiation_evidence=request.form.get(
                "negotiation_evidence", ""
            ).strip()
            or None,
            reject_reason_summary=request.form.get(
                "reject_reason_summary", ""
            ).strip()
            or None,
            invoice_terms=request.form.get("invoice_terms", "").strip() or None,
            quality_evidence_status=request.form.get(
                "quality_evidence_status", "missing"
            ),
            source_transparency=request.form.get("source_transparency", "partial"),
            consent_evidence=request.form.get("consent_evidence", "missing"),
            reject_reason_map_ready=reject_reason_map_ready,
            invoice_evidence=invoice_evidence,
            dispute_reserve_present=dispute_reserve_present,
            buyer_terms_status=request.form.get("buyer_terms_status", "missing"),
            human_review=human_review,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            effective_payout=decimal_value(result["effective_payout"]),
            paid_epc=decimal_value(result["paid_epc"]),
            safe_cpc=decimal_value(result["safe_cpc"]),
            margin_per_click=decimal_value(result["margin_per_click"]),
            reserve_amount=decimal_value(result["reserve_amount"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in LEAD_PRICING_REVIEW_STATUSES:
            flash("Lead 定价评审状态不允许。", "warning")
            return redirect(url_for("main.lead_pricing"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "lead_pricing_review",
            review.id,
            "create",
            f"Created lead pricing review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash(
            "Lead 定价评审已保存。它只记录 rate card、quality evidence、scrub reserve 和人工状态，不自动谈价、改 routing 或生成 lead。",
            "success",
        )
        return redirect(url_for("main.lead_pricing"))

    return render_template(
        "lead_pricing.html",
        reviews=LeadPricingReview.query.order_by(
            LeadPricingReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=LEAD_PRICING_REVIEW_STATUSES,
    )


@bp.post("/lead-pricing/<int:review_id>/status")
def update_lead_pricing_status(review_id: int):
    review = LeadPricingReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in LEAD_PRICING_REVIEW_STATUSES:
        flash("Lead 定价评审状态不允许。", "warning")
        return redirect(url_for("main.lead_pricing"))
    old_status = review.status
    review.status = status
    add_audit(
        "lead_pricing_review",
        review.id,
        "status_update",
        f"Lead pricing review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash(
        "Lead 定价状态已更新。状态只代表内部评审，不会自动谈价、切换 buyer、改 routing 或改广告后台。",
        "success",
    )
    return redirect(url_for("main.lead_pricing"))


@bp.route("/appointment-leads", methods=["GET", "POST"])
def appointment_leads():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("buyer_name", ""),
                request.form.get("vertical", ""),
                request.form.get("service_type", ""),
                request.form.get("geo", ""),
                request.form.get("appointment_platform", ""),
                request.form.get("payout_event", ""),
                request.form.get("status_map", ""),
                request.form.get("slot_policy", ""),
                request.form.get("reminder_policy", ""),
                request.form.get("no_show_reason_map", ""),
                request.form.get("conversion_mapping", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_APPOINTMENT_LEAD_TERMS):
            flash(
                "Appointment 评审包含伪造预约/到场/付款、自动外呼、短信群发、绕 consent、Cookie、cloaking、防关联或换号语义，请改走风险审计和修复流程。",
                "warning",
            )
            return redirect(url_for("main.appointment_leads"))

        payout_amount = decimal_value(request.form.get("payout_amount"))
        estimated_cpc = decimal_value(request.form.get("estimated_cpc"))
        click_to_request_rate_percent = decimal_value(
            request.form.get("click_to_request_rate_percent")
        )
        request_to_book_rate_percent = decimal_value(
            request.form.get("request_to_book_rate_percent")
        )
        confirmation_rate_percent = decimal_value(
            request.form.get("confirmation_rate_percent")
        )
        show_rate_percent = decimal_value(request.form.get("show_rate_percent"))
        completed_rate_percent = decimal_value(
            request.form.get("completed_rate_percent")
        )
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        cancel_rate_percent = decimal_value(request.form.get("cancel_rate_percent"))
        no_show_rate_percent = decimal_value(request.form.get("no_show_rate_percent"))
        duplicate_booking_rate_percent = decimal_value(
            request.form.get("duplicate_booking_rate_percent")
        )
        reschedule_rate_percent = decimal_value(
            request.form.get("reschedule_rate_percent")
        )
        reminder_cost_per_booking = decimal_value(
            request.form.get("reminder_cost_per_booking")
        )
        no_show_cost_per_booking = decimal_value(
            request.form.get("no_show_cost_per_booking")
        )
        available_slots = decimal_value(request.form.get("available_slots"))
        expected_bookings = decimal_value(request.form.get("expected_bookings"))
        payout_definition_clear = request.form.get("payout_definition_clear") == "on"
        duplicate_window_defined = (
            request.form.get("duplicate_window_defined") == "on"
        )
        no_show_reason_map_ready = (
            request.form.get("no_show_reason_map_ready") == "on"
        )
        calendar_capacity_evidence = (
            request.form.get("calendar_capacity_evidence") == "on"
        )
        reminder_template_reviewed = (
            request.form.get("reminder_template_reviewed") == "on"
        )
        offline_conversion_mapping_ready = (
            request.form.get("offline_conversion_mapping_ready") == "on"
        )
        human_review = request.form.get("human_review") == "on"
        result = calculate_appointment_lead_review(
            payout_event=request.form.get("payout_event", "showed"),
            payout_amount=float(payout_amount),
            estimated_cpc=float(estimated_cpc),
            click_to_request_rate_percent=float(click_to_request_rate_percent),
            request_to_book_rate_percent=float(request_to_book_rate_percent),
            confirmation_rate_percent=float(confirmation_rate_percent),
            show_rate_percent=float(show_rate_percent),
            completed_rate_percent=float(completed_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            cancel_rate_percent=float(cancel_rate_percent),
            no_show_rate_percent=float(no_show_rate_percent),
            duplicate_booking_rate_percent=float(duplicate_booking_rate_percent),
            reschedule_rate_percent=float(reschedule_rate_percent),
            reminder_cost_per_booking=float(reminder_cost_per_booking),
            no_show_cost_per_booking=float(no_show_cost_per_booking),
            available_slots=float(available_slots),
            expected_bookings=float(expected_bookings),
            lead_age_hours=_int(request.form.get("lead_age_hours")),
            slot_delay_hours=_int(request.form.get("slot_delay_hours")),
            calendar_capacity_status=request.form.get(
                "calendar_capacity_status", "unknown"
            ),
            timezone_status=request.form.get("timezone_status", "unclear"),
            reminder_consent_status=request.form.get(
                "reminder_consent_status", "missing"
            ),
            confirmation_process_status=request.form.get(
                "confirmation_process_status", "missing"
            ),
            buyer_terms_status=request.form.get("buyer_terms_status", "missing"),
            payout_definition_clear=payout_definition_clear,
            duplicate_window_defined=duplicate_window_defined,
            no_show_reason_map_ready=no_show_reason_map_ready,
            calendar_capacity_evidence=calendar_capacity_evidence,
            reminder_template_reviewed=reminder_template_reviewed,
            offline_conversion_mapping_ready=offline_conversion_mapping_ready,
            human_review=human_review,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = AppointmentLeadReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            buyer_name=request.form.get("buyer_name", "").strip() or None,
            vertical=request.form.get("vertical", "healthcare"),
            service_type=request.form.get("service_type", "").strip() or None,
            geo=request.form.get("geo", "").strip() or None,
            appointment_platform=request.form.get(
                "appointment_platform", ""
            ).strip()
            or None,
            payout_event=request.form.get("payout_event", "showed"),
            payout_amount=payout_amount,
            estimated_cpc=estimated_cpc,
            click_to_request_rate_percent=click_to_request_rate_percent,
            request_to_book_rate_percent=request_to_book_rate_percent,
            confirmation_rate_percent=confirmation_rate_percent,
            show_rate_percent=show_rate_percent,
            completed_rate_percent=completed_rate_percent,
            paid_rate_percent=paid_rate_percent,
            cancel_rate_percent=cancel_rate_percent,
            no_show_rate_percent=no_show_rate_percent,
            duplicate_booking_rate_percent=duplicate_booking_rate_percent,
            reschedule_rate_percent=reschedule_rate_percent,
            reminder_cost_per_booking=reminder_cost_per_booking,
            no_show_cost_per_booking=no_show_cost_per_booking,
            available_slots=available_slots,
            expected_bookings=expected_bookings,
            lead_age_hours=_int(request.form.get("lead_age_hours")),
            slot_delay_hours=_int(request.form.get("slot_delay_hours")),
            calendar_capacity_status=request.form.get(
                "calendar_capacity_status", "unknown"
            ),
            timezone_status=request.form.get("timezone_status", "unclear"),
            reminder_channel=request.form.get("reminder_channel", "email"),
            reminder_consent_status=request.form.get(
                "reminder_consent_status", "missing"
            ),
            confirmation_process_status=request.form.get(
                "confirmation_process_status", "missing"
            ),
            buyer_terms_status=request.form.get("buyer_terms_status", "missing"),
            status_map=request.form.get("status_map", "").strip() or None,
            slot_policy=request.form.get("slot_policy", "").strip() or None,
            reminder_policy=request.form.get("reminder_policy", "").strip() or None,
            no_show_reason_map=request.form.get(
                "no_show_reason_map", ""
            ).strip()
            or None,
            conversion_mapping=request.form.get(
                "conversion_mapping", ""
            ).strip()
            or None,
            payout_definition_clear=payout_definition_clear,
            duplicate_window_defined=duplicate_window_defined,
            no_show_reason_map_ready=no_show_reason_map_ready,
            calendar_capacity_evidence=calendar_capacity_evidence,
            reminder_template_reviewed=reminder_template_reviewed,
            offline_conversion_mapping_ready=offline_conversion_mapping_ready,
            human_review=human_review,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            expected_value_per_booking=decimal_value(
                result["expected_value_per_booking"]
            ),
            expected_value_per_click=decimal_value(
                result["expected_value_per_click"]
            ),
            safe_cpc=decimal_value(result["safe_cpc"]),
            cpc_margin_percent=decimal_value(result["cpc_margin_percent"]),
            safe_appointment_spend=decimal_value(
                result["safe_appointment_spend"]
            ),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in APPOINTMENT_LEAD_REVIEW_STATUSES:
            flash("Appointment 评审状态不允许。", "warning")
            return redirect(url_for("main.appointment_leads"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "appointment_lead_review",
            review.id,
            "create",
            f"Created appointment lead review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash(
            "Appointment 评审已保存。它只记录预约漏斗、slot capacity、reminder consent 和回传映射，不自动创建预约、外呼、群发短信或伪造到场。",
            "success",
        )
        return redirect(url_for("main.appointment_leads"))

    return render_template(
        "appointment_leads.html",
        reviews=AppointmentLeadReview.query.order_by(
            AppointmentLeadReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=APPOINTMENT_LEAD_REVIEW_STATUSES,
    )


@bp.post("/appointment-leads/<int:review_id>/status")
def update_appointment_lead_status(review_id: int):
    review = AppointmentLeadReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in APPOINTMENT_LEAD_REVIEW_STATUSES:
        flash("Appointment 评审状态不允许。", "warning")
        return redirect(url_for("main.appointment_leads"))
    old_status = review.status
    review.status = status
    add_audit(
        "appointment_lead_review",
        review.id,
        "status_update",
        f"Appointment lead review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash(
        "Appointment 状态已更新。状态只代表内部评审，不会自动创建预约、外呼、群发短信、改 routing 或改广告后台。",
        "success",
    )
    return redirect(url_for("main.appointment_leads"))


@bp.route("/buyer-capacity", methods=["GET", "POST"])
def buyer_capacity():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("buyer_name", ""),
                request.form.get("vertical", ""),
                request.form.get("geo", ""),
                request.form.get("buyer_timezone", ""),
                request.form.get("account_timezone", ""),
                request.form.get("user_timezone_scope", ""),
                request.form.get("call_center_timezone", ""),
                request.form.get("operating_hours", ""),
                request.form.get("cap_reset_rule", ""),
                request.form.get("holiday_calendar", ""),
                request.form.get("ad_schedule_summary", ""),
                request.form.get("no_buyer_reason_map", ""),
                request.form.get("routing_fallback_policy", ""),
                request.form.get("dayparting_basis", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_BUYER_CAPACITY_TERMS):
            flash(
                "Buyer Capacity 评审包含自动改预算/时段/routing、自动外呼、补 lead、Cookie、cloaking、防关联或换号语义，请改走风险审计和人工修复流程。",
                "warning",
            )
            return redirect(url_for("main.buyer_capacity"))

        cap_limit = decimal_value(request.form.get("cap_limit"))
        cap_used = decimal_value(request.form.get("cap_used"))
        elapsed_operating_day_percent = decimal_value(
            request.form.get("elapsed_operating_day_percent")
        )
        expected_next_hour_leads = decimal_value(
            request.form.get("expected_next_hour_leads")
        )
        expected_daily_leads = decimal_value(request.form.get("expected_daily_leads"))
        hourly_contact_capacity = decimal_value(
            request.form.get("hourly_contact_capacity")
        )
        current_hour_capacity_used = decimal_value(
            request.form.get("current_hour_capacity_used")
        )
        expected_paid_value_per_lead = decimal_value(
            request.form.get("expected_paid_value_per_lead")
        )
        accepted_rate_percent = decimal_value(
            request.form.get("accepted_rate_percent")
        )
        qualified_rate_percent = decimal_value(
            request.form.get("qualified_rate_percent")
        )
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        no_buyer_rate_percent = decimal_value(
            request.form.get("no_buyer_rate_percent")
        )
        missed_contact_rate_percent = decimal_value(
            request.form.get("missed_contact_rate_percent")
        )
        after_hours_lead_rate_percent = decimal_value(
            request.form.get("after_hours_lead_rate_percent")
        )
        cap_snapshot_evidence = request.form.get("cap_snapshot_evidence") == "on"
        buyer_hours_evidence = request.form.get("buyer_hours_evidence") == "on"
        ad_schedule_evidence = request.form.get("ad_schedule_evidence") == "on"
        call_reporting_evidence = (
            request.form.get("call_reporting_evidence") == "on"
        )
        no_buyer_tracking_ready = (
            request.form.get("no_buyer_tracking_ready") == "on"
        )
        missed_contact_tracking_ready = (
            request.form.get("missed_contact_tracking_ready") == "on"
        )
        dayparting_cohort_ready = (
            request.form.get("dayparting_cohort_ready") == "on"
        )
        fallback_buyer_reviewed = (
            request.form.get("fallback_buyer_reviewed") == "on"
        )
        human_review = request.form.get("human_review") == "on"

        result = calculate_buyer_capacity_review(
            cap_limit=float(cap_limit),
            cap_used=float(cap_used),
            elapsed_operating_day_percent=float(elapsed_operating_day_percent),
            expected_next_hour_leads=float(expected_next_hour_leads),
            expected_daily_leads=float(expected_daily_leads),
            hourly_contact_capacity=float(hourly_contact_capacity),
            current_hour_capacity_used=float(current_hour_capacity_used),
            expected_paid_value_per_lead=float(expected_paid_value_per_lead),
            accepted_rate_percent=float(accepted_rate_percent),
            qualified_rate_percent=float(qualified_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            no_buyer_rate_percent=float(no_buyer_rate_percent),
            missed_contact_rate_percent=float(missed_contact_rate_percent),
            after_hours_lead_rate_percent=float(after_hours_lead_rate_percent),
            cap_last_confirmed_hours=_int(
                request.form.get("cap_last_confirmed_hours")
            ),
            feedback_sla_hours=_int(request.form.get("feedback_sla_hours")),
            first_attempt_sla_minutes=_int(
                request.form.get("first_attempt_sla_minutes")
            ),
            cap_confidence_status=request.form.get(
                "cap_confidence_status", "unknown"
            ),
            hours_alignment_status=request.form.get(
                "hours_alignment_status", "missing"
            ),
            ad_schedule_alignment_status=request.form.get(
                "ad_schedule_alignment_status", "missing"
            ),
            timezone_alignment_status=request.form.get(
                "timezone_alignment_status", "missing"
            ),
            holiday_readiness_status=request.form.get(
                "holiday_readiness_status", "unknown"
            ),
            fallback_status=request.form.get("fallback_status", "missing"),
            source_quality_status=request.form.get("source_quality_status", "medium"),
            overdelivery_guardrail_status=request.form.get(
                "overdelivery_guardrail_status", "missing"
            ),
            cap_snapshot_evidence=cap_snapshot_evidence,
            buyer_hours_evidence=buyer_hours_evidence,
            ad_schedule_evidence=ad_schedule_evidence,
            call_reporting_evidence=call_reporting_evidence,
            no_buyer_tracking_ready=no_buyer_tracking_ready,
            missed_contact_tracking_ready=missed_contact_tracking_ready,
            dayparting_cohort_ready=dayparting_cohort_ready,
            fallback_buyer_reviewed=fallback_buyer_reviewed,
            human_review=human_review,
        )
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = BuyerCapacityReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            buyer_name=request.form.get("buyer_name", "").strip() or None,
            vertical=request.form.get("vertical", "b2b_saas"),
            geo=request.form.get("geo", "").strip() or None,
            buyer_timezone=request.form.get("buyer_timezone", "").strip()
            or "America/New_York",
            account_timezone=request.form.get("account_timezone", "").strip()
            or "UTC",
            user_timezone_scope=request.form.get(
                "user_timezone_scope", ""
            ).strip()
            or None,
            call_center_timezone=request.form.get(
                "call_center_timezone", ""
            ).strip()
            or None,
            cap_type=request.form.get("cap_type", "daily_buyer_cap"),
            cap_period=request.form.get("cap_period", "daily"),
            cap_limit=cap_limit,
            cap_used=cap_used,
            elapsed_operating_day_percent=elapsed_operating_day_percent,
            expected_next_hour_leads=expected_next_hour_leads,
            expected_daily_leads=expected_daily_leads,
            hourly_contact_capacity=hourly_contact_capacity,
            current_hour_capacity_used=current_hour_capacity_used,
            expected_paid_value_per_lead=expected_paid_value_per_lead,
            accepted_rate_percent=accepted_rate_percent,
            qualified_rate_percent=qualified_rate_percent,
            paid_rate_percent=paid_rate_percent,
            no_buyer_rate_percent=no_buyer_rate_percent,
            missed_contact_rate_percent=missed_contact_rate_percent,
            after_hours_lead_rate_percent=after_hours_lead_rate_percent,
            cap_last_confirmed_hours=_int(
                request.form.get("cap_last_confirmed_hours")
            ),
            feedback_sla_hours=_int(request.form.get("feedback_sla_hours")),
            first_attempt_sla_minutes=_int(
                request.form.get("first_attempt_sla_minutes")
            ),
            cap_confidence_status=request.form.get(
                "cap_confidence_status", "unknown"
            ),
            hours_alignment_status=request.form.get(
                "hours_alignment_status", "missing"
            ),
            ad_schedule_alignment_status=request.form.get(
                "ad_schedule_alignment_status", "missing"
            ),
            timezone_alignment_status=request.form.get(
                "timezone_alignment_status", "missing"
            ),
            holiday_readiness_status=request.form.get(
                "holiday_readiness_status", "unknown"
            ),
            fallback_status=request.form.get("fallback_status", "missing"),
            source_quality_status=request.form.get("source_quality_status", "medium"),
            overdelivery_guardrail_status=request.form.get(
                "overdelivery_guardrail_status", "missing"
            ),
            operating_hours=request.form.get("operating_hours", "").strip() or None,
            cap_reset_rule=request.form.get("cap_reset_rule", "").strip() or None,
            holiday_calendar=request.form.get("holiday_calendar", "").strip()
            or None,
            ad_schedule_summary=request.form.get(
                "ad_schedule_summary", ""
            ).strip()
            or None,
            no_buyer_reason_map=request.form.get(
                "no_buyer_reason_map", ""
            ).strip()
            or None,
            routing_fallback_policy=request.form.get(
                "routing_fallback_policy", ""
            ).strip()
            or None,
            dayparting_basis=request.form.get("dayparting_basis", "").strip()
            or None,
            cap_snapshot_evidence=cap_snapshot_evidence,
            buyer_hours_evidence=buyer_hours_evidence,
            ad_schedule_evidence=ad_schedule_evidence,
            call_reporting_evidence=call_reporting_evidence,
            no_buyer_tracking_ready=no_buyer_tracking_ready,
            missed_contact_tracking_ready=missed_contact_tracking_ready,
            dayparting_cohort_ready=dayparting_cohort_ready,
            fallback_buyer_reviewed=fallback_buyer_reviewed,
            human_review=human_review,
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            cap_usage_percent=decimal_value(result["cap_usage_percent"]),
            cap_remaining=decimal_value(result["cap_remaining"]),
            projected_end_of_day_usage_percent=decimal_value(
                result["projected_end_of_day_usage_percent"]
            ),
            safe_leads_remaining=decimal_value(result["safe_leads_remaining"]),
            safe_media_spend_remaining=decimal_value(
                result["safe_media_spend_remaining"]
            ),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in BUYER_CAPACITY_REVIEW_STATUSES:
            flash("Buyer Capacity 评审状态不允许。", "warning")
            return redirect(url_for("main.buyer_capacity"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "buyer_capacity_review",
            review.id,
            "create",
            f"Created buyer capacity review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash(
            "Buyer Capacity 评审已保存。它只记录 cap、hours、timezone、dayparting、no buyer 和人工状态，不自动改预算、时段、routing 或外呼。",
            "success",
        )
        return redirect(url_for("main.buyer_capacity"))

    return render_template(
        "buyer_capacity.html",
        reviews=BuyerCapacityReview.query.order_by(
            BuyerCapacityReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=BUYER_CAPACITY_REVIEW_STATUSES,
    )


@bp.post("/buyer-capacity/<int:review_id>/status")
def update_buyer_capacity_status(review_id: int):
    review = BuyerCapacityReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in BUYER_CAPACITY_REVIEW_STATUSES:
        flash("Buyer Capacity 评审状态不允许。", "warning")
        return redirect(url_for("main.buyer_capacity"))
    old_status = review.status
    review.status = status
    add_audit(
        "buyer_capacity_review",
        review.id,
        "status_update",
        f"Buyer capacity review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash(
        "Buyer Capacity 状态已更新。状态只代表内部评审，不会自动改预算、广告时段、routing、外呼或 buyer 后台。",
        "success",
    )
    return redirect(url_for("main.buyer_capacity"))


@bp.route("/conversion-signals", methods=["GET", "POST"])
def conversion_signals():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("vertical", ""),
                request.form.get("geo", ""),
                request.form.get("conversion_goal_name", ""),
                request.form.get("conversion_action_name", ""),
                request.form.get("traffic_scope", ""),
                request.form.get("goal_change_summary", ""),
                request.form.get("affected_campaigns", ""),
                request.form.get("value_mapping_notes", ""),
                request.form.get("dedupe_notes", ""),
                request.form.get("lag_notes", ""),
                request.form.get("diagnostics_notes", ""),
                request.form.get("rollback_plan", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_CONVERSION_SIGNAL_TERMS):
            flash(
                "转化信号评审包含伪造转化、自动上传/改 goal、Cookie 登录态、绕 consent、cloaking、防关联或换号语义，请改走风险审计和人工修复流程。",
                "warning",
            )
            return redirect(url_for("main.conversion_signals"))

        weekly_conversions = decimal_value(request.form.get("weekly_conversions"))
        weekly_approved_conversions = decimal_value(
            request.form.get("weekly_approved_conversions")
        )
        weekly_paid_conversions = decimal_value(
            request.form.get("weekly_paid_conversions")
        )
        reported_value_per_conversion = decimal_value(
            request.form.get("reported_value_per_conversion")
        )
        approved_rate_percent = decimal_value(
            request.form.get("approved_rate_percent")
        )
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        click_id_coverage_percent = decimal_value(
            request.form.get("click_id_coverage_percent")
        )
        offline_match_rate_percent = decimal_value(
            request.form.get("offline_match_rate_percent")
        )
        duplicate_rate_percent = decimal_value(
            request.form.get("duplicate_rate_percent")
        )
        average_lag_days = decimal_value(request.form.get("average_lag_days"))
        p95_lag_days = decimal_value(request.form.get("p95_lag_days"))
        primary_secondary_reviewed = (
            request.form.get("primary_secondary_reviewed") == "on"
        )
        value_mapping_reviewed = request.form.get("value_mapping_reviewed") == "on"
        transaction_id_dedupe_ready = (
            request.form.get("transaction_id_dedupe_ready") == "on"
        )
        offline_import_diagnostics_ready = (
            request.form.get("offline_import_diagnostics_ready") == "on"
        )
        conversion_lag_reviewed = (
            request.form.get("conversion_lag_reviewed") == "on"
        )
        segment_split_ready = request.form.get("segment_split_ready") == "on"
        consent_policy_reviewed = (
            request.form.get("consent_policy_reviewed") == "on"
        )
        bid_strategy_report_reviewed = (
            request.form.get("bid_strategy_report_reviewed") == "on"
        )
        change_history_evidence = (
            request.form.get("change_history_evidence") == "on"
        )
        human_review = request.form.get("human_review") == "on"

        result = calculate_conversion_signal_review(
            action_stage=request.form.get("action_stage", "submitted"),
            primary_status=request.form.get("primary_status", "secondary"),
            value_mode=request.form.get("value_mode", "expected"),
            bid_strategy=request.form.get("bid_strategy", "manual_cpc"),
            weekly_conversions=float(weekly_conversions),
            weekly_approved_conversions=float(weekly_approved_conversions),
            weekly_paid_conversions=float(weekly_paid_conversions),
            reported_value_per_conversion=float(reported_value_per_conversion),
            approved_rate_percent=float(approved_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            click_id_coverage_percent=float(click_id_coverage_percent),
            offline_match_rate_percent=float(offline_match_rate_percent),
            duplicate_rate_percent=float(duplicate_rate_percent),
            average_lag_days=float(average_lag_days),
            p95_lag_days=float(p95_lag_days),
            incident_count_30d=_int(request.form.get("incident_count_30d")),
            segment_granularity_status=request.form.get(
                "segment_granularity_status", "mixed"
            ),
            policy_consent_status=request.form.get(
                "policy_consent_status", "missing"
            ),
            customer_data_status=request.form.get("customer_data_status", "missing"),
            offline_import_status=request.form.get("offline_import_status", "none"),
            transaction_id_status=request.form.get(
                "transaction_id_status", "missing"
            ),
            lag_stability_status=request.form.get("lag_stability_status", "unknown"),
            bid_strategy_status=request.form.get("bid_strategy_status", "unknown"),
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
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = ConversionSignalReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            vertical=request.form.get("vertical", "b2b_saas"),
            geo=request.form.get("geo", "").strip() or None,
            conversion_goal_name=request.form.get(
                "conversion_goal_name", ""
            ).strip()
            or "unnamed_goal",
            conversion_action_name=request.form.get(
                "conversion_action_name", ""
            ).strip()
            or "unnamed_action",
            action_stage=request.form.get("action_stage", "submitted"),
            primary_status=request.form.get("primary_status", "secondary"),
            recommended_primary_status=str(result["recommended_primary_status"]),
            value_mode=request.form.get("value_mode", "expected"),
            bid_strategy=request.form.get("bid_strategy", "manual_cpc"),
            traffic_scope=request.form.get("traffic_scope", "search_exact"),
            weekly_conversions=weekly_conversions,
            weekly_approved_conversions=weekly_approved_conversions,
            weekly_paid_conversions=weekly_paid_conversions,
            reported_value_per_conversion=reported_value_per_conversion,
            approved_rate_percent=approved_rate_percent,
            paid_rate_percent=paid_rate_percent,
            click_id_coverage_percent=click_id_coverage_percent,
            offline_match_rate_percent=offline_match_rate_percent,
            duplicate_rate_percent=duplicate_rate_percent,
            average_lag_days=average_lag_days,
            p95_lag_days=p95_lag_days,
            incident_count_30d=_int(request.form.get("incident_count_30d")),
            segment_granularity_status=request.form.get(
                "segment_granularity_status", "mixed"
            ),
            policy_consent_status=request.form.get(
                "policy_consent_status", "missing"
            ),
            customer_data_status=request.form.get("customer_data_status", "missing"),
            offline_import_status=request.form.get("offline_import_status", "none"),
            transaction_id_status=request.form.get(
                "transaction_id_status", "missing"
            ),
            lag_stability_status=request.form.get("lag_stability_status", "unknown"),
            bid_strategy_status=request.form.get("bid_strategy_status", "unknown"),
            goal_change_summary=request.form.get(
                "goal_change_summary", ""
            ).strip()
            or None,
            affected_campaigns=request.form.get("affected_campaigns", "").strip()
            or None,
            value_mapping_notes=request.form.get(
                "value_mapping_notes", ""
            ).strip()
            or None,
            dedupe_notes=request.form.get("dedupe_notes", "").strip() or None,
            lag_notes=request.form.get("lag_notes", "").strip() or None,
            diagnostics_notes=request.form.get("diagnostics_notes", "").strip()
            or None,
            rollback_plan=request.form.get("rollback_plan", "").strip() or None,
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
            score_components=result["score_components"],
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            bid_readiness=str(result["bid_readiness"]),
            expected_paid_value_per_conversion=decimal_value(
                result["expected_paid_value_per_conversion"]
            ),
            safe_target_cpa=decimal_value(result["safe_target_cpa"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in CONVERSION_SIGNAL_REVIEW_STATUSES:
            flash("转化信号评审状态不允许。", "warning")
            return redirect(url_for("main.conversion_signals"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "conversion_signal_review",
            review.id,
            "create",
            f"Created conversion signal review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash(
            "转化信号评审已保存。它只记录 conversion action、primary/secondary、value、lag、diagnostics 和人工状态，不自动上传转化或修改 Ads goal。",
            "success",
        )
        return redirect(url_for("main.conversion_signals"))

    return render_template(
        "conversion_signals.html",
        reviews=ConversionSignalReview.query.order_by(
            ConversionSignalReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=CONVERSION_SIGNAL_REVIEW_STATUSES,
    )


@bp.post("/conversion-signals/<int:review_id>/status")
def update_conversion_signal_status(review_id: int):
    review = ConversionSignalReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in CONVERSION_SIGNAL_REVIEW_STATUSES:
        flash("转化信号评审状态不允许。", "warning")
        return redirect(url_for("main.conversion_signals"))
    old_status = review.status
    review.status = status
    add_audit(
        "conversion_signal_review",
        review.id,
        "status_update",
        f"Conversion signal review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash(
        "转化信号状态已更新。状态只代表内部评审，不会自动上传 offline conversion、改 primary/secondary、改出价或操作 Google Ads 后台。",
        "success",
    )
    return redirect(url_for("main.conversion_signals"))


@bp.route("/crm-value-mapping", methods=["GET", "POST"])
def crm_value_mapping():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("buyer_name", ""),
                request.form.get("vertical", ""),
                request.form.get("geo", ""),
                request.form.get("source_system", ""),
                request.form.get("buyer_feedback_source", ""),
                request.form.get("source_stage", ""),
                request.form.get("buyer_status", ""),
                request.form.get("conversion_action_name", ""),
                request.form.get("stage_mapping_notes", ""),
                request.form.get("conversion_action_notes", ""),
                request.form.get("value_mapping_notes", ""),
                request.form.get("transaction_id_notes", ""),
                request.form.get("import_qa_notes", ""),
                request.form.get("adjustment_notes", ""),
                request.form.get("lag_notes", ""),
                request.form.get("diagnostics_notes", ""),
                request.form.get("rollback_plan", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_CRM_VALUE_MAPPING_TERMS):
            flash(
                "CRM 映射评审包含伪造 CRM/Buyer Feedback、补 postback、自动上传/改 goal、Cookie 登录态、绕 consent、cloaking、防关联或换号语义，请改走风险审计和人工修复流程。",
                "warning",
            )
            return redirect(url_for("main.crm_value_mapping"))

        payout_amount = decimal_value(request.form.get("payout_amount"))
        approved_rate_percent = decimal_value(
            request.form.get("approved_rate_percent")
        )
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        return_rate_percent = decimal_value(request.form.get("return_rate_percent"))
        variable_cost_per_conversion = decimal_value(
            request.form.get("variable_cost_per_conversion")
        )
        weekly_stage_count = decimal_value(request.form.get("weekly_stage_count"))
        weekly_unique_leads = decimal_value(request.form.get("weekly_unique_leads"))
        rejected_count = decimal_value(request.form.get("rejected_count"))
        returned_count = decimal_value(request.form.get("returned_count"))
        duplicate_count = decimal_value(request.form.get("duplicate_count"))
        click_id_match_rate_percent = decimal_value(
            request.form.get("click_id_match_rate_percent")
        )
        import_success_rate_percent = decimal_value(
            request.form.get("import_success_rate_percent")
        )
        import_error_rate_percent = decimal_value(
            request.form.get("import_error_rate_percent")
        )
        average_stage_lag_days = decimal_value(
            request.form.get("average_stage_lag_days")
        )

        stage_taxonomy_reviewed = request.form.get("stage_taxonomy_reviewed") == "on"
        buyer_feedback_contract_reviewed = (
            request.form.get("buyer_feedback_contract_reviewed") == "on"
        )
        conversion_action_mapping_reviewed = (
            request.form.get("conversion_action_mapping_reviewed") == "on"
        )
        primary_secondary_reviewed = (
            request.form.get("primary_secondary_reviewed") == "on"
        )
        value_mode_reviewed = request.form.get("value_mode_reviewed") == "on"
        transaction_id_rule_ready = (
            request.form.get("transaction_id_rule_ready") == "on"
        )
        rejected_returned_excluded = (
            request.form.get("rejected_returned_excluded") == "on"
        )
        adjustment_policy_ready = (
            request.form.get("adjustment_policy_ready") == "on"
        )
        import_batch_qa_ready = request.form.get("import_batch_qa_ready") == "on"
        diagnostics_reviewed = request.form.get("diagnostics_reviewed") == "on"
        lag_profile_reviewed = request.form.get("lag_profile_reviewed") == "on"
        consent_policy_reviewed = (
            request.form.get("consent_policy_reviewed") == "on"
        )
        human_review = request.form.get("human_review") == "on"

        result = calculate_crm_value_mapping_review(
            standard_stage=request.form.get("standard_stage", "submitted"),
            conversion_action_role=request.form.get(
                "conversion_action_role", "secondary"
            ),
            value_mode=request.form.get("value_mode", "expected"),
            payout_amount=float(payout_amount),
            approved_rate_percent=float(approved_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            return_rate_percent=float(return_rate_percent),
            variable_cost_per_conversion=float(variable_cost_per_conversion),
            weekly_stage_count=float(weekly_stage_count),
            weekly_unique_leads=float(weekly_unique_leads),
            rejected_count=float(rejected_count),
            returned_count=float(returned_count),
            duplicate_count=float(duplicate_count),
            click_id_match_rate_percent=float(click_id_match_rate_percent),
            import_success_rate_percent=float(import_success_rate_percent),
            import_error_rate_percent=float(import_error_rate_percent),
            average_stage_lag_days=float(average_stage_lag_days),
            return_window_days=_int(request.form.get("return_window_days")),
            transaction_id_status=request.form.get(
                "transaction_id_status", "missing"
            ),
            adjustment_rule_status=request.form.get(
                "adjustment_rule_status", "missing"
            ),
            import_batch_status=request.form.get("import_batch_status", "draft"),
            diagnostics_status=request.form.get("diagnostics_status", "missing"),
            consent_status=request.form.get("consent_status", "missing"),
            pii_handling_status=request.form.get("pii_handling_status", "unknown"),
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
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = CrmValueMappingReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            buyer_name=request.form.get("buyer_name", "").strip() or None,
            vertical=request.form.get("vertical", "b2b_saas"),
            geo=request.form.get("geo", "").strip() or None,
            source_system=request.form.get("source_system", "").strip() or "crm",
            buyer_feedback_source=request.form.get(
                "buyer_feedback_source", ""
            ).strip()
            or None,
            source_stage=request.form.get("source_stage", "").strip()
            or "unknown_stage",
            standard_stage=request.form.get("standard_stage", "submitted"),
            buyer_status=request.form.get("buyer_status", "").strip() or None,
            conversion_action_name=request.form.get(
                "conversion_action_name", ""
            ).strip()
            or "unnamed_action",
            conversion_action_role=request.form.get(
                "conversion_action_role", "secondary"
            ),
            primary_recommendation=str(result["primary_recommendation"]),
            value_mode=request.form.get("value_mode", "expected"),
            recommended_upload_policy=str(result["recommended_upload_policy"]),
            payout_amount=payout_amount,
            approved_rate_percent=approved_rate_percent,
            paid_rate_percent=paid_rate_percent,
            return_rate_percent=return_rate_percent,
            variable_cost_per_conversion=variable_cost_per_conversion,
            weekly_stage_count=weekly_stage_count,
            weekly_unique_leads=weekly_unique_leads,
            rejected_count=rejected_count,
            returned_count=returned_count,
            duplicate_count=duplicate_count,
            click_id_match_rate_percent=click_id_match_rate_percent,
            import_success_rate_percent=import_success_rate_percent,
            import_error_rate_percent=import_error_rate_percent,
            average_stage_lag_days=average_stage_lag_days,
            return_window_days=_int(request.form.get("return_window_days")),
            transaction_id_status=request.form.get(
                "transaction_id_status", "missing"
            ),
            adjustment_rule_status=request.form.get(
                "adjustment_rule_status", "missing"
            ),
            import_batch_status=request.form.get("import_batch_status", "draft"),
            diagnostics_status=request.form.get("diagnostics_status", "missing"),
            consent_status=request.form.get("consent_status", "missing"),
            pii_handling_status=request.form.get("pii_handling_status", "unknown"),
            stage_mapping_notes=request.form.get(
                "stage_mapping_notes", ""
            ).strip()
            or None,
            conversion_action_notes=request.form.get(
                "conversion_action_notes", ""
            ).strip()
            or None,
            value_mapping_notes=request.form.get(
                "value_mapping_notes", ""
            ).strip()
            or None,
            transaction_id_notes=request.form.get(
                "transaction_id_notes", ""
            ).strip()
            or None,
            import_qa_notes=request.form.get("import_qa_notes", "").strip()
            or None,
            adjustment_notes=request.form.get("adjustment_notes", "").strip()
            or None,
            lag_notes=request.form.get("lag_notes", "").strip() or None,
            diagnostics_notes=request.form.get(
                "diagnostics_notes", ""
            ).strip()
            or None,
            rollback_plan=request.form.get("rollback_plan", "").strip() or None,
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
            score_components=result["score_components"],
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            expected_value=decimal_value(result["expected_value"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in CRM_VALUE_MAPPING_REVIEW_STATUSES:
            flash("CRM 映射评审状态不允许。", "warning")
            return redirect(url_for("main.crm_value_mapping"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "crm_value_mapping_review",
            review.id,
            "create",
            f"Created CRM value mapping review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash(
            "CRM 映射评审已保存。它只记录 stage mapping、value、transaction_id、import QA、adjustment 和人工状态，不自动上传转化或修改 Google Ads 后台。",
            "success",
        )
        return redirect(url_for("main.crm_value_mapping"))

    return render_template(
        "crm_value_mapping.html",
        reviews=CrmValueMappingReview.query.order_by(
            CrmValueMappingReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=CRM_VALUE_MAPPING_REVIEW_STATUSES,
    )


@bp.post("/crm-value-mapping/<int:review_id>/status")
def update_crm_value_mapping_status(review_id: int):
    review = CrmValueMappingReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in CRM_VALUE_MAPPING_REVIEW_STATUSES:
        flash("CRM 映射评审状态不允许。", "warning")
        return redirect(url_for("main.crm_value_mapping"))
    old_status = review.status
    review.status = status
    add_audit(
        "crm_value_mapping_review",
        review.id,
        "status_update",
        f"CRM value mapping review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash(
        "CRM 映射状态已更新。状态只代表内部评审，不会自动上传 offline conversion、改 primary/secondary、改 value 或操作广告后台。",
        "success",
    )
    return redirect(url_for("main.crm_value_mapping"))


@bp.route("/ping-post-routing", methods=["GET", "POST"])
def ping_post_routing():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        review_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("vertical", ""),
                request.form.get("geo", ""),
                request.form.get("buyer_group_name", ""),
                request.form.get("source_type", ""),
                request.form.get("form_version", ""),
                request.form.get("fields_sent_schema", ""),
                request.form.get("routing_rule_summary", ""),
                request.form.get("buyer_disclosure_notes", ""),
                request.form.get("cap_snapshot_notes", ""),
                request.form.get("reject_reason_map", ""),
                request.form.get("fallback_policy", ""),
                request.form.get("buyer_feedback_plan", ""),
                request.form.get("suppression_notes", ""),
                request.form.get("consent_evidence_notes", ""),
                request.form.get("incident_notes", ""),
                request.form.get("notes", ""),
                request.form.get("source_urls", ""),
            ]
        ).lower()
        if any(term in review_text for term in BLOCKED_PING_POST_ROUTING_TERMS):
            flash(
                "Ping/Post 评审包含伪造 lead、自动 post/提交、外呼/短信滥发、绕 consent/DNC、隐藏 buyer、Cookie 登录态、代理/指纹、cloaking 或换号语义；本系统只允许安全评审、QA 和审计记录。",
                "warning",
            )
            return redirect(url_for("main.ping_post_routing"))

        expected_bid_amount = decimal_value(request.form.get("expected_bid_amount"))
        fallback_payout_amount = decimal_value(
            request.form.get("fallback_payout_amount")
        )
        primary_buyer_cap_remaining = decimal_value(
            request.form.get("primary_buyer_cap_remaining")
        )
        buyer_accept_rate_percent = decimal_value(
            request.form.get("buyer_accept_rate_percent")
        )
        qualification_rate_percent = decimal_value(
            request.form.get("qualification_rate_percent")
        )
        paid_rate_percent = decimal_value(request.form.get("paid_rate_percent"))
        no_buyer_rate_percent = decimal_value(
            request.form.get("no_buyer_rate_percent")
        )
        reject_rate_percent = decimal_value(request.form.get("reject_rate_percent"))
        duplicate_rate_percent = decimal_value(
            request.form.get("duplicate_rate_percent")
        )
        complaint_rate_percent = decimal_value(
            request.form.get("complaint_rate_percent")
        )

        consent_version_evidence = (
            request.form.get("consent_version_evidence") == "on"
        )
        buyer_disclosure_reviewed = (
            request.form.get("buyer_disclosure_reviewed") == "on"
        )
        field_minimization_reviewed = (
            request.form.get("field_minimization_reviewed") == "on"
        )
        suppression_dnc_checked = (
            request.form.get("suppression_dnc_checked") == "on"
        )
        cap_snapshot_evidence = request.form.get("cap_snapshot_evidence") == "on"
        routing_rule_reviewed = request.form.get("routing_rule_reviewed") == "on"
        exclusive_shared_terms_reviewed = (
            request.form.get("exclusive_shared_terms_reviewed") == "on"
        )
        fallback_buyer_reviewed = (
            request.form.get("fallback_buyer_reviewed") == "on"
        )
        buyer_feedback_ready = request.form.get("buyer_feedback_ready") == "on"
        source_policy_reviewed = request.form.get("source_policy_reviewed") == "on"
        human_review = request.form.get("human_review") == "on"

        fields_sent_schema = request.form.get("fields_sent_schema", "").strip()
        routing_rule_summary = request.form.get("routing_rule_summary", "").strip()
        reject_reason_map = request.form.get("reject_reason_map", "").strip()
        fallback_policy = request.form.get("fallback_policy", "").strip()
        buyer_feedback_plan = request.form.get("buyer_feedback_plan", "").strip()
        incident_notes = request.form.get("incident_notes", "").strip()

        result = calculate_ping_post_routing_review(
            routing_mode=request.form.get("routing_mode", "ping_post"),
            lead_type=request.form.get("lead_type", "exclusive"),
            consent_scope=request.form.get("consent_scope", "single_buyer"),
            buyer_disclosure_status=request.form.get(
                "buyer_disclosure_status", "missing"
            ),
            ping_field_scope=request.form.get("ping_field_scope", "unknown"),
            pii_level=request.form.get("pii_level", "unknown"),
            suppression_status=request.form.get("suppression_status", "missing"),
            dnc_status=request.form.get("dnc_status", "missing"),
            cap_snapshot_status=request.form.get("cap_snapshot_status", "missing"),
            fallback_status=request.form.get("fallback_status", "missing"),
            buyer_feedback_status=request.form.get(
                "buyer_feedback_status", "missing"
            ),
            source_policy_status=request.form.get("source_policy_status", "unknown"),
            buyer_count=_int(request.form.get("buyer_count")),
            max_post_buyers=_int(request.form.get("max_post_buyers"), 1),
            pinged_buyers=_int(request.form.get("pinged_buyers")),
            accepted_buyers=_int(request.form.get("accepted_buyers")),
            posted_buyers=_int(request.form.get("posted_buyers")),
            primary_buyer_cap_remaining=float(primary_buyer_cap_remaining),
            cap_last_checked_minutes=_int(
                request.form.get("cap_last_checked_minutes")
            ),
            lead_age_minutes=_int(request.form.get("lead_age_minutes")),
            avg_ping_latency_ms=_int(request.form.get("avg_ping_latency_ms")),
            expected_bid_amount=float(expected_bid_amount),
            fallback_payout_amount=float(fallback_payout_amount),
            buyer_accept_rate_percent=float(buyer_accept_rate_percent),
            qualification_rate_percent=float(qualification_rate_percent),
            paid_rate_percent=float(paid_rate_percent),
            no_buyer_rate_percent=float(no_buyer_rate_percent),
            reject_rate_percent=float(reject_rate_percent),
            duplicate_rate_percent=float(duplicate_rate_percent),
            complaint_rate_percent=float(complaint_rate_percent),
            fields_sent_schema=fields_sent_schema,
            routing_rule_summary=routing_rule_summary,
            reject_reason_map=reject_reason_map,
            fallback_policy=fallback_policy,
            buyer_feedback_plan=buyer_feedback_plan,
            incident_notes=incident_notes,
            consent_version_evidence=consent_version_evidence,
            buyer_disclosure_reviewed=buyer_disclosure_reviewed,
            field_minimization_reviewed=field_minimization_reviewed,
            suppression_dnc_checked=suppression_dnc_checked,
            cap_snapshot_evidence=cap_snapshot_evidence,
            routing_rule_reviewed=routing_rule_reviewed,
            exclusive_shared_terms_reviewed=exclusive_shared_terms_reviewed,
            fallback_buyer_reviewed=fallback_buyer_reviewed,
            buyer_feedback_ready=buyer_feedback_ready,
            source_policy_reviewed=source_policy_reviewed,
            human_review=human_review,
        )

        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        review = PingPostRoutingReview(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            name=request.form["name"].strip(),
            vertical=request.form.get("vertical", "insurance"),
            geo=request.form.get("geo", "").strip() or None,
            buyer_group_name=request.form.get("buyer_group_name", "").strip()
            or None,
            source_type=request.form.get("source_type", "google_search"),
            form_version=request.form.get("form_version", "").strip() or None,
            routing_mode=request.form.get("routing_mode", "ping_post"),
            lead_type=request.form.get("lead_type", "exclusive"),
            consent_scope=request.form.get("consent_scope", "single_buyer"),
            buyer_disclosure_status=request.form.get(
                "buyer_disclosure_status", "missing"
            ),
            ping_field_scope=request.form.get("ping_field_scope", "unknown"),
            pii_level=request.form.get("pii_level", "unknown"),
            suppression_status=request.form.get("suppression_status", "missing"),
            dnc_status=request.form.get("dnc_status", "missing"),
            cap_snapshot_status=request.form.get("cap_snapshot_status", "missing"),
            fallback_status=request.form.get("fallback_status", "missing"),
            buyer_feedback_status=request.form.get(
                "buyer_feedback_status", "missing"
            ),
            source_policy_status=request.form.get("source_policy_status", "unknown"),
            buyer_count=_int(request.form.get("buyer_count")),
            max_post_buyers=_int(request.form.get("max_post_buyers"), 1),
            pinged_buyers=_int(request.form.get("pinged_buyers")),
            accepted_buyers=_int(request.form.get("accepted_buyers")),
            posted_buyers=_int(request.form.get("posted_buyers")),
            primary_buyer_cap_remaining=primary_buyer_cap_remaining,
            cap_last_checked_minutes=_int(
                request.form.get("cap_last_checked_minutes")
            ),
            lead_age_minutes=_int(request.form.get("lead_age_minutes")),
            avg_ping_latency_ms=_int(request.form.get("avg_ping_latency_ms")),
            expected_bid_amount=expected_bid_amount,
            fallback_payout_amount=fallback_payout_amount,
            buyer_accept_rate_percent=buyer_accept_rate_percent,
            qualification_rate_percent=qualification_rate_percent,
            paid_rate_percent=paid_rate_percent,
            no_buyer_rate_percent=no_buyer_rate_percent,
            reject_rate_percent=reject_rate_percent,
            duplicate_rate_percent=duplicate_rate_percent,
            complaint_rate_percent=complaint_rate_percent,
            fields_sent_schema=fields_sent_schema or None,
            routing_rule_summary=routing_rule_summary or None,
            buyer_disclosure_notes=request.form.get(
                "buyer_disclosure_notes", ""
            ).strip()
            or None,
            cap_snapshot_notes=request.form.get("cap_snapshot_notes", "").strip()
            or None,
            reject_reason_map=reject_reason_map or None,
            fallback_policy=fallback_policy or None,
            buyer_feedback_plan=buyer_feedback_plan or None,
            suppression_notes=request.form.get("suppression_notes", "").strip()
            or None,
            consent_evidence_notes=request.form.get(
                "consent_evidence_notes", ""
            ).strip()
            or None,
            incident_notes=incident_notes or None,
            consent_version_evidence=consent_version_evidence,
            buyer_disclosure_reviewed=buyer_disclosure_reviewed,
            field_minimization_reviewed=field_minimization_reviewed,
            suppression_dnc_checked=suppression_dnc_checked,
            cap_snapshot_evidence=cap_snapshot_evidence,
            routing_rule_reviewed=routing_rule_reviewed,
            exclusive_shared_terms_reviewed=exclusive_shared_terms_reviewed,
            fallback_buyer_reviewed=fallback_buyer_reviewed,
            buyer_feedback_ready=buyer_feedback_ready,
            source_policy_reviewed=source_policy_reviewed,
            human_review=human_review,
            score_components=result["score_components"],
            score=int(result["score"]),
            risk_level=str(result["risk_level"]),
            recommended_action=str(result["recommended_action"]),
            expected_payable_value_per_lead=decimal_value(
                result["expected_payable_value_per_lead"]
            ),
            safe_cpl=decimal_value(result["safe_cpl"]),
            blockers=result["blockers"],
            status=request.form.get("status", "open"),
            notes=request.form.get("notes", "").strip() or None,
            source_urls=source_urls,
        )
        if review.status not in PING_POST_ROUTING_REVIEW_STATUSES:
            flash("Ping/Post 评审状态不允许。", "warning")
            return redirect(url_for("main.ping_post_routing"))
        db.session.add(review)
        db.session.flush()
        add_audit(
            "ping_post_routing_review",
            review.id,
            "create",
            f"Created Ping/Post routing review {review.name} with score {review.score}.",
        )
        db.session.commit()
        flash(
            "Ping/Post 路由评审已保存。它只记录 consent、字段最小化、cap、buyer feedback、fallback 和审计状态，不自动 post lead、不外呼、不短信、不操作广告后台。",
            "success",
        )
        return redirect(url_for("main.ping_post_routing"))

    return render_template(
        "ping_post_routing.html",
        reviews=PingPostRoutingReview.query.order_by(
            PingPostRoutingReview.created_at.desc()
        ).all(),
        offers=offers,
        campaigns=campaigns,
        status_options=PING_POST_ROUTING_REVIEW_STATUSES,
    )


@bp.post("/ping-post-routing/<int:review_id>/status")
def update_ping_post_routing_status(review_id: int):
    review = PingPostRoutingReview.query.get_or_404(review_id)
    status = request.form.get("status", "open")
    if status not in PING_POST_ROUTING_REVIEW_STATUSES:
        flash("Ping/Post 评审状态不允许。", "warning")
        return redirect(url_for("main.ping_post_routing"))
    old_status = review.status
    review.status = status
    add_audit(
        "ping_post_routing_review",
        review.id,
        "status_update",
        f"Ping/Post routing review {review.name} changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash(
        "Ping/Post 状态已更新。状态只代表内部评审，不会自动 post lead、绕过 consent/DNC、外呼、短信或切换 buyer。",
        "success",
    )
    return redirect(url_for("main.ping_post_routing"))


@bp.route("/optimization")
def optimization():
    return render_template(
        "optimization.html",
        actions=OptimizationAction.query.order_by(
            OptimizationAction.created_at.desc()
        ).all(),
        status_options=OPTIMIZATION_ACTION_STATUSES,
    )


@bp.post("/optimization/<int:action_id>/status")
def update_optimization_status(action_id: int):
    action = OptimizationAction.query.get_or_404(action_id)
    status = request.form.get("status", "open")
    if status not in OPTIMIZATION_ACTION_STATUSES:
        flash("优化建议状态不允许。", "warning")
        return redirect(url_for("main.optimization"))
    old_status = action.status
    action.status = status
    add_audit(
        "optimization_action",
        action.id,
        "status_update",
        (
            f"Optimization action {action.action_type} status changed "
            f"from {old_status} to {status}."
        ),
    )
    db.session.commit()
    flash("优化建议状态已更新，只记录内部处理结果，不自动执行投放变更。", "success")
    return redirect(url_for("main.optimization"))


@bp.route("/sources", methods=["GET", "POST"])
def sources():
    if request.method == "POST":
        review_status = request.form.get("review_status", "candidate").strip() or "candidate"
        if review_status not in SOURCE_REVIEW_STATUSES:
            flash("来源复核状态不允许。", "warning")
            return redirect(url_for("main.sources"))
        source = ResearchSource(
            topic=request.form["topic"].strip(),
            capability=request.form.get("capability", "").strip() or None,
            title=request.form["title"].strip(),
            url=request.form["url"].strip(),
            publisher=request.form.get("publisher", "").strip() or "unknown",
            source_type=request.form.get("source_type", "policy").strip() or "policy",
            reliability=request.form.get("reliability", "primary").strip() or "primary",
            review_status=review_status,
            claim_summary=request.form["claim_summary"].strip(),
            notes=request.form.get("notes", "").strip() or None,
        )
        db.session.add(source)
        db.session.flush()
        add_audit("research_source", source.id, "create", f"Added source {source.title}.")
        db.session.commit()
        flash("来源记录已保存。", "success")
        return redirect(url_for("main.sources"))

    return render_template(
        "sources.html",
        sources=ResearchSource.query.order_by(
            ResearchSource.topic, ResearchSource.publisher, ResearchSource.title
        ).all(),
        capabilities=RISK_CAPABILITIES,
        source_statuses=SOURCE_REVIEW_STATUSES,
    )


@bp.post("/sources/<int:source_id>/status")
def update_source_status(source_id: int):
    source = ResearchSource.query.get_or_404(source_id)
    status = request.form.get("review_status", "candidate")
    if status not in SOURCE_REVIEW_STATUSES:
        flash("来源复核状态不允许。", "warning")
        return redirect(url_for("main.sources"))
    old_status = source.review_status
    source.review_status = status
    add_audit(
        "research_source",
        source.id,
        "status_update",
        f"Research source {source.title} status changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("来源复核状态已更新。状态只用于知识库维护，不触发广告后台操作。", "success")
    return redirect(url_for("main.sources"))


@bp.route("/risk-audits", methods=["GET", "POST"])
def risk_audits():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    if request.method == "POST":
        source_urls = [
            item.strip()
            for item in request.form.get("source_urls", "").splitlines()
            if item.strip()
        ]
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        audit = RiskAudit(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            capability=request.form["capability"],
            severity=request.form.get("severity", "medium"),
            status=request.form.get("status", "open"),
            finding=request.form["finding"].strip(),
            mitigation=request.form["mitigation"].strip(),
            source_urls=source_urls,
        )
        db.session.add(audit)
        db.session.flush()
        add_audit(
            "risk_audit",
            audit.id,
            "create",
            f"Created risk audit for {audit.capability}.",
        )
        db.session.commit()
        flash("风险审计记录已创建。", "success")
        return redirect(url_for("main.risk_audits"))

    return render_template(
        "risk_audits.html",
        audits=RiskAudit.query.order_by(RiskAudit.created_at.desc()).all(),
        offers=offers,
        campaigns=campaigns,
        capabilities=RISK_CAPABILITIES,
        status_options=RISK_AUDIT_STATUSES,
    )


@bp.post("/risk-audits/<int:audit_id>/status")
def update_risk_audit_status(audit_id: int):
    audit = RiskAudit.query.get_or_404(audit_id)
    status = request.form.get("status", "open")
    if status not in RISK_AUDIT_STATUSES:
        flash("风险审计状态不允许。", "warning")
        return redirect(url_for("main.risk_audits"))
    old_status = audit.status
    audit.status = status
    add_audit(
        "risk_audit",
        audit.id,
        "status_update",
        f"Risk audit {audit.capability} status changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("风险审计状态已更新。状态只代表内部处理进度，不会自动放行高风险动作。", "success")
    return redirect(url_for("main.risk_audits"))


@bp.route("/tasks", methods=["GET", "POST"])
def tasks():
    offers = Offer.query.order_by(Offer.name).all()
    campaigns = CampaignDraft.query.order_by(CampaignDraft.created_at.desc()).all()
    link_rules = LinkRule.query.order_by(LinkRule.created_at.desc()).all()
    if request.method == "POST":
        offer_id = request.form.get("offer_id")
        campaign_id = request.form.get("campaign_draft_id")
        link_rule_id = request.form.get("link_rule_id")
        task_type = request.form.get("task_type", "")
        is_valid_task_type, task_error = validate_task_type(task_type)
        if not is_valid_task_type:
            flash(task_error or "任务类型不允许。", "warning")
            return redirect(url_for("main.tasks"))
        is_valid_task_text, text_error = validate_task_text(
            request.form.get("name", ""),
            request.form.get("notes", ""),
        )
        if not is_valid_task_text:
            flash(text_error or "任务名称或备注包含不允许语义。", "warning")
            return redirect(url_for("main.tasks"))
        job = TaskJob(
            offer_id=int(offer_id) if offer_id else None,
            campaign_draft_id=int(campaign_id) if campaign_id else None,
            link_rule_id=int(link_rule_id) if link_rule_id else None,
            name=request.form["name"].strip(),
            task_type=task_type.strip(),
            schedule_mode=request.form.get("schedule_mode", "manual"),
            interval_minutes=_int(request.form.get("interval_minutes"), 1440),
            notes=request.form.get("notes", "").strip() or None,
        )
        db.session.add(job)
        db.session.flush()
        add_audit("task_job", job.id, "create", f"Created task {job.name}.")
        db.session.commit()
        flash("任务已创建。", "success")
        return redirect(url_for("main.tasks"))

    return render_template(
        "tasks.html",
        jobs=TaskJob.query.order_by(TaskJob.created_at.desc()).all(),
        offers=offers,
        campaigns=campaigns,
        link_rules=link_rules,
        task_types=TASK_TYPES,
    )


@bp.post("/tasks/<int:job_id>/run")
def run_task(job_id: int):
    job = TaskJob.query.get_or_404(job_id)
    result = run_task_job(job)
    add_audit(
        "task_job",
        job.id,
        "run",
        f"Ran task {job.name}: {result.get('message', 'no message')}",
    )
    db.session.commit()
    flash(result.get("message", "任务已执行。"), "success" if result["ok"] else "warning")
    return redirect(url_for("main.tasks"))


@bp.route("/links", methods=["GET", "POST"])
def links():
    offers = Offer.query.order_by(Offer.name).all()
    if request.method == "POST":
        candidate_urls = [
            item.strip()
            for item in request.form.get("candidate_urls", "").splitlines()
            if item.strip()
        ]
        link_plan_text = " ".join(
            [
                request.form.get("name", ""),
                request.form.get("current_url", ""),
                request.form.get("rotation_reason", ""),
                " ".join(candidate_urls),
            ]
        ).lower()
        if any(term in link_plan_text for term in BLOCKED_LINK_PLAN_TERMS):
            flash("链接计划包含 cloaking、审核规避或隐藏目的地语义，请改走风险审计。", "warning")
            return redirect(url_for("main.links"))
        rule = LinkRule(
            offer_id=int(request.form["offer_id"]),
            name=request.form["name"].strip(),
            current_url=request.form["current_url"].strip(),
            candidate_urls=candidate_urls,
            rotation_reason=request.form["rotation_reason"].strip(),
            frequency_minutes=int(request.form.get("frequency_minutes", "1440") or 1440),
            require_manual_review=True,
        )
        db.session.add(rule)
        db.session.flush()
        add_audit("link_rule", rule.id, "create", f"Created link plan {rule.name}.")
        db.session.commit()
        flash("链接轮换计划已创建，默认需要人工确认。", "success")
        return redirect(url_for("main.links"))

    return render_template(
        "links.html",
        offers=offers,
        link_rules=LinkRule.query.order_by(LinkRule.created_at.desc()).all(),
        link_statuses=LINK_RULE_STATUSES,
    )


@bp.post("/links/<int:rule_id>/status")
def update_link_status(rule_id: int):
    rule = LinkRule.query.get_or_404(rule_id)
    status = request.form.get("status", "draft")
    if status not in LINK_RULE_STATUSES:
        flash("链接计划状态不允许。", "warning")
        return redirect(url_for("main.links"))
    old_status = rule.status
    rule.status = status
    add_audit(
        "link_rule",
        rule.id,
        "status_update",
        f"Link plan {rule.name} status changed from {old_status} to {status}.",
    )
    db.session.commit()
    flash("链接计划状态已更新。状态只代表内部评审进度，不会自动改 Google Ads 后台。", "success")
    return redirect(url_for("main.links"))


@bp.post("/links/<int:rule_id>/rotate")
def rotate_link(rule_id: int):
    rule = LinkRule.query.get_or_404(rule_id)
    if not rule.candidate_urls:
        flash("没有候选 URL，无法执行。", "warning")
        return redirect(url_for("main.links"))
    if rule.status not in {"approved", "rotated"}:
        flash("链接计划尚未批准，不能轮换。请先完成人工审核。", "warning")
        return redirect(url_for("main.links"))
    old_url = rule.current_url
    next_url = rule.candidate_urls[0]
    remaining = rule.candidate_urls[1:] + [old_url]
    rule.current_url = next_url
    rule.candidate_urls = remaining
    rule.last_rotated_at = datetime.utcnow()
    rule.status = "rotated"
    add_audit(
        "link_rule",
        rule.id,
        "manual_rotate",
        f"Manual reviewed rotation: {old_url} -> {next_url}.",
    )
    db.session.commit()
    flash("链接已按人工审核流程轮换，并写入审计日志。", "success")
    return redirect(url_for("main.links"))


@bp.route("/logs")
def logs():
    return render_template("logs.html", logs=_recent_logs(limit=200))


@bp.route("/docs")
def docs_index():
    doc_path = Path(current_app.root_path).parent / "docs" / "docs_index.md"
    return _render_markdown_doc(doc_path, "文档入口和验收导航")


@bp.route("/doc/<path:filename>")
def docs_file(filename: str):
    docs_root = Path(current_app.root_path).parent / "docs"
    doc_path = (docs_root / filename).resolve()
    if not str(doc_path).startswith(str(docs_root.resolve())) or doc_path.suffix != ".md":
        flash("文档不存在。", "warning")
        return redirect(url_for("main.docs_index"))
    title = doc_path.stem.replace("_", " ")
    return _render_markdown_doc(doc_path, title)


@bp.route("/knowledge/<name>")
def knowledge(name: str):
    docs = {
        "docs_index": ("文档入口和验收导航", "docs_index.md"),
        "industry": ("Ads 套利行业知识库", "ads_arbitrage_industry.md"),
        "business_models": ("Ads 套利业务模式拆解手册", "ads_arbitrage_business_models.md"),
        "operations": ("Ads 套利运营手册", "ads_arbitrage_operations.md"),
        "evidence_matrix": ("Ads 套利来源证据矩阵", "ads_arbitrage_source_evidence_matrix.md"),
        "search_feed_parking": ("Search Arbitrage、Feed 与 Parking 模式手册", "search_arbitrage_feed_parking.md"),
        "rsoc_n2s": ("RSOC / N2S、Search Feed Partner 与相关搜索套利治理手册", "rsoc_n2s_search_feed_partner_governance.md"),
        "keyword_intent": ("关键词、搜索意图与选题研究手册", "keyword_intent_research.md"),
        "seasonality_forecasting": ("季节性、事件日历与需求预测手册", "seasonality_event_demand_forecasting.md"),
        "search_terms_mining": ("Search Terms、否定词与 Query Mining 治理手册", "search_terms_negative_keyword_query_mining.md"),
        "brand_trademark": ("品牌词、商标与竞品投放合规手册", "brand_bidding_trademark_competitor_policy.md"),
        "competitor_intelligence": ("竞品广告、SERP 与 Ads Transparency 情报手册", "competitor_ad_intelligence_serp_transparency.md"),
        "traffic_vendor": ("买量渠道与流量供应商尽调手册", "traffic_channel_vendor_due_diligence.md"),
        "inventory_controls": ("Google Ads 流量库存、版位与排除控制手册", "traffic_inventory_controls.md"),
        "source_quality_governance": ("Source、Publisher、Placement 质量评分与名单治理手册", "source_publisher_placement_quality_governance.md"),
        "vendor_contracts": ("流量供应商合同、IO、退款与争议治理手册", "traffic_vendor_contract_io_dispute_governance.md"),
        "audience_remarketing": ("受众定向、再营销与 Customer Match 合规手册", "audience_remarketing_customer_match_policy.md"),
        "affiliate_due_diligence": ("Affiliate Network / Lead Buyer 尽调与条款手册", "affiliate_network_due_diligence.md"),
        "lead_buyer_contracts": ("Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册", "lead_buyer_contract_io_paid_definition_governance.md"),
        "lead_quality": ("Lead 质量、Postback 对账与拒付管理手册", "lead_quality_postback_reconciliation.md"),
        "lead_call_tracking": ("Lead Form、电话线索、Call Tracking 与 TCPA 风险手册", "lead_form_call_tracking_tcpa_compliance.md"),
        "call_tracking_attribution": ("Call Tracking Number Pool、DNI 与电话归因治理手册", "call_tracking_dni_number_pool_attribution_governance.md"),
        "pay_per_call_routing": ("Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册", "pay_per_call_buyer_routing_duration_payout_governance.md"),
        "lead_consent_proof": ("Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册", "lead_consent_proof_certificate_evidence_governance.md"),
        "lead_form_funnel": ("Lead Form 漏斗、资格问题与移动端 UX 治理手册", "lead_form_funnel_qualification_ux.md"),
        "ping_post_leads": ("Ping/Post、Lead Buyer Routing 与线索市场治理手册", "ping_post_lead_marketplace_buyer_routing.md"),
        "lead_freshness": ("Lead Freshness、Aged Lead 与 Recontact Window 治理手册", "lead_freshness_aged_recontact_governance.md"),
        "lead_validation": ("Lead 验证、Suppression、去重与 PII 治理手册", "lead_validation_suppression_pii_governance.md"),
        "lead_contact_sla": ("Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册", "speed_to_lead_contact_sla_governance.md"),
        "experiment_design": ("实验设计、样本量与优化决策手册", "experiment_design_optimization.md"),
        "invalid_traffic_sop": ("无效流量识别、异常监控与来源隔离 SOP", "invalid_traffic_detection_sop.md"),
        "anomaly_alerting": ("异常监控、告警、止损队列与事故分诊手册", "anomaly_monitoring_alerting_stoploss_incident_triage.md"),
        "content_quality": ("内容生产、页面可信度与编辑质量手册", "content_production_editorial_quality.md"),
        "sensitive_verticals": ("敏感垂类政策与 Offer 准入手册", "sensitive_vertical_policy_playbook.md"),
        "metrics": ("Ads 套利指标字典与口径", "metric_dictionary.md"),
        "unit_economics": ("单位经济模型、Break-even 与安全边际手册", "unit_economics_margin_safety.md"),
        "verticals": ("Offer 与垂类评估手册", "offer_vertical_evaluation.md"),
        "cpl_vertical_economics": ("CPL 垂类经济、资格问题与 Buyer Acceptance 手册", "cpl_vertical_economics_qualification_playbook.md"),
        "insurance_leads": ("Insurance、Medicare / ACA 与 Final Expense Lead 治理手册", "insurance_medicare_aca_final_expense_lead_governance.md"),
        "loan_debt_leads": ("Loan、Mortgage、Credit 与 Debt Lead 治理手册", "loan_mortgage_credit_debt_lead_governance.md"),
        "legal_leads": ("Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理手册", "legal_case_intake_mass_tort_lead_governance.md"),
        "home_services_leads": ("Home Services、Solar 与 Local Services Lead 治理手册", "home_services_solar_local_services_lead_governance.md"),
        "education_leads": ("Education、Career Training 与 Student Lead 治理手册", "education_career_training_student_lead_governance.md"),
        "healthcare_leads": ("Healthcare、Medical Appointment 与 Clinic Lead 治理手册", "healthcare_medical_appointment_lead_governance.md"),
        "b2b_saas_leads": ("B2B SaaS、Professional Services 与 Demo Lead 治理手册", "b2b_saas_professional_services_lead_governance.md"),
        "crypto_investment_leads": ("Crypto、Investment 与 Trading Lead 治理手册", "crypto_investment_trading_lead_governance.md"),
        "employment_leads": ("Employment、Recruiting 与 Staffing Lead 治理手册", "employment_recruiting_staffing_lead_governance.md"),
        "gambling_leads": ("Gambling、Sweepstakes 与 Sports Betting Lead 治理手册", "gambling_sweepstakes_sports_betting_lead_governance.md"),
        "addiction_treatment_leads": ("Addiction Treatment、Rehab 与 Behavioral Health Lead 治理手册", "addiction_treatment_rehab_behavioral_health_lead_governance.md"),
        "government_services_leads": ("Government Services、Immigration 与 Public Benefits Lead 治理手册", "government_services_immigration_public_benefits_lead_governance.md"),
        "lead_pricing": ("Lead Pricing、Payout Negotiation 与结算安全垫治理手册", "lead_pricing_payout_negotiation_governance.md"),
        "appointment_leads": ("Appointment Lead、Booking、Show Rate 与 No-show 治理手册", "appointment_lead_booking_show_rate_governance.md"),
        "offer_cap_payout": ("Offer Cap、Payout、状态变更与替代 Offer 治理手册", "offer_cap_payout_status_governance.md"),
        "buyer_capacity": ("Buyer Capacity、Cap Pacing 与 Dayparting 治理手册", "buyer_capacity_cap_pacing_dayparting_governance.md"),
        "traffic_tracking": ("流量源与追踪归因手册", "traffic_source_tracking.md"),
        "native_presell": ("Native、Advertorial 与 Presell Page 套利手册", "native_advertorial_presell_compliance.md"),
        "click_session_revenue": ("Click -> Session -> Revenue 对账 SOP", "click_session_revenue_reconciliation.md"),
        "tracking_chain": ("追踪模板、URL 参数与跳转链 QA 手册", "tracking_template_redirect_chain_qa.md"),
        "taxonomy_governance": ("Campaign 命名、Labels、UTM/SubID 与维度治理手册", "campaign_taxonomy_naming_label_dimension_governance.md"),
        "attribution_incrementality": ("归因、增量性与流量蚕食治理手册", "attribution_incrementality_cannibalization.md"),
        "conversion_tracking": ("转化追踪、价值回传与 Attribution 手册", "conversion_tracking_value_feedback.md"),
        "conversion_signal_quality": ("转化信号质量与出价学习治理手册", "conversion_signal_quality_bidding_learning_governance.md"),
        "crm_value_mapping": ("CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册", "crm_buyer_feedback_offline_conversion_mapping.md"),
        "decision_windows": ("决策窗口、回传延迟与收入延迟治理手册", "decision_window_revenue_lag_governance.md"),
        "landing_quality": ("落地页质量、广告密度与 MFA 风险手册", "landing_page_quality_mfa.md"),
        "domain_assets": ("域名、站点资产与站群治理手册", "domain_site_asset_governance.md"),
        "landing_intelligence": ("落地页素材抽取、Offer Intelligence 与创意 Brief 手册", "landing_offer_intelligence_creative_brief.md"),
        "cashflow": ("回款、结算与现金流风险手册", "cashflow_settlement_risk.md"),
        "subscription_ltv": ("订阅、试用、退款、Chargeback 与 LTV 治理手册", "subscription_refund_ltv_chargeback_governance.md"),
        "revenue_reconciliation": ("发布商收入对账、Finalized Revenue 与扣量复盘手册", "revenue_reconciliation_adstack.md"),
        "creative_testing": ("广告创意生成、测试与优化手册", "creative_testing_optimization.md"),
        "creative_angle_library": ("Creative Angle Library、素材版本与反馈闭环手册", "creative_angle_library_feedback_loop.md"),
        "creative_claim_review": ("广告创意 Claim 审核与事实核查手册", "creative_claim_review_fact_checking.md"),
        "ad_review_appeal": ("Google Ads 广告审核、拒登、Policy Manager 与申诉证据包手册", "google_ads_ad_review_disapproval_appeal_playbook.md"),
        "ai_prompt_governance": ("AI Provider、Prompt 模板与创意成本治理手册", "ai_provider_prompt_cost_governance.md"),
        "link_rotation": ("链接计划与换链接合规手册", "link_rotation_compliance.md"),
        "campaign_launch": ("Google Ads 投放结构与安全自动化手册", "campaign_launch_automation.md"),
        "editor_csv_bulk": ("Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册", "google_ads_editor_csv_bulk_upload_governance.md"),
        "scripts_automation": ("Google Ads Scripts 安全自动化手册", "google_ads_scripts_safe_automation.md"),
        "scripts_data_sync": ("Google Ads Scripts 数据同步、快照与一致性手册", "google_ads_scripts_data_sync_consistency.md"),
        "task_orchestration": ("任务编排、安全审批、执行日志与事故复盘手册", "task_orchestration_approval_audit_runbook.md"),
        "recommendations_experiments": ("Google Ads Recommendations、Experiments 与 Auto-apply 优化治理手册", "google_ads_recommendations_experiments_auto_apply_governance.md"),
        "auction_bidding": ("Google Ads 竞价、Quality Score 与套利出价手册", "google_ads_auction_bidding_quality_score.md"),
        "ads_reporting": ("Google Ads 报表诊断、Search Terms 与 Change History 手册", "google_ads_reporting_diagnostics.md"),
        "search_automation": ("Search 自动化流量：AI Max、Broad Match 与 DSA 套利风险手册", "search_automation_ai_max_broad_match.md"),
        "pmax_demand_gen": ("Performance Max / Demand Gen 自动化流量与套利风险手册", "performance_max_demand_gen_automation.md"),
        "geo_localization": ("Geo、语言、本地化、时区与币种分层手册", "geo_language_localization_currency.md"),
        "budget_pacing": ("预算节奏、扩量与止损手册", "budget_pacing_scaling_stoploss.md"),
        "portfolio_allocation": ("Portfolio 预算分配、风险集中度与组合治理手册", "portfolio_budget_allocation_risk_concentration.md"),
        "account_governance": ("账号、MCC、付款与 Advertiser Verification 治理手册", "account_mcc_billing_verification_governance.md"),
        "account_health": ("账号健康、政策中心与申诉 SOP", "policy_account_health_sop.md"),
        "adsense_site_approval": ("AdSense 站点审核、Policy Center 与广告投放限制手册", "adsense_site_approval_policy_center.md"),
        "publisher_stack": ("发布商变现栈：AdSense / AdX / Google Ad Manager 手册", "publisher_monetization_stack.md"),
        "ad_quality": ("发布商广告质量、阻止控制与品牌安全手册", "publisher_ad_quality_blocking_controls.md"),
        "programmatic_supply_chain": ("程序化供应链透明度：ads.txt / sellers.json / schain 手册", "programmatic_supply_chain_transparency.md"),
        "gam_yield": ("GAM / AdX Yield、Floor Price 与 Pricing Rules 手册", "gam_adx_yield_floor_pricing.md"),
        "header_bidding": ("Header Bidding / Prebid.js 与广告栈延迟手册", "header_bidding_prebid_ad_stack.md"),
        "ad_placement": ("广告位、刷新、可见率与页面体验手册", "ad_placement_refresh_viewability.md"),
        "privacy_consent": ("隐私、Consent 与追踪合规手册", "privacy_consent_tracking.md"),
        "playbook": ("Ads 套利实战 Playbook", "ads_arbitrage_playbook.md"),
        "adxkit": ("ADXKit 功能与架构拆解", "adxkit_breakdown.md"),
        "redlines": ("高风险能力研究与合规替代方案", "high_risk_capability_research.md"),
        "risk_matrix": ("高风险能力风险矩阵与来源索引", "risk_matrix_and_sources.md"),
        "risk_completion": ("高风险能力逐点完成审计", "high_risk_completion_audit.md"),
        "risk_blueprint": ("高风险能力逐点调研与安全复刻蓝图", "high_risk_capability_safe_reproduction_blueprint.md"),
        "source_library": ("研究来源库", "source_library.md"),
        "traceability": ("原始需求追溯矩阵", "requirement_traceability_matrix.md"),
        "risk_index": ("高风险能力专题索引", "high_risk/README.md"),
        "acceptance": ("验收清单", "acceptance_checklist.md"),
        "risk_cookie": ("Ads Cookie 登录和后台操作研究", "high_risk/ads_cookie_backend_operation.md"),
        "risk_auth": ("自动绕过登录、2FA、安全挑战研究", "high_risk/automated_login_2fa_challenge_bypass.md"),
        "risk_invalid_traffic": ("补点击、刷展示、模拟自然流量研究", "high_risk/invalid_traffic_click_impression_simulation.md"),
        "risk_association": ("代理、指纹、Worker 转发规避关联检测研究", "high_risk/proxy_fingerprint_worker_association_evasion.md"),
        "risk_cloaking": ("Cloaking 或审核页/用户页不一致研究", "high_risk/cloaking_review_user_page_mismatch.md"),
        "risk_ban_evasion": ("为规避封禁创建或切换账号研究", "high_risk/ban_evasion_account_switching.md"),
        "design": ("系统设计文档", "system_design.md"),
        "usage": ("使用文档", "usage.md"),
        "development": ("开发文档", "development.md"),
    }
    if name not in docs:
        flash("文档不存在。", "warning")
        return redirect(url_for("main.index"))
    title, filename = docs[name]
    doc_path = Path(current_app.root_path).parent / "docs" / filename
    return _render_markdown_doc(doc_path, title)


def _render_markdown_doc(doc_path: Path, title: str):
    content = doc_path.read_text(encoding="utf-8") if doc_path.exists() else "Not found"
    return render_template(
        "knowledge.html",
        title=title,
        content=content,
        content_html=render_markdown(content),
    )


def _recent_logs(limit: int = 8):
    from .models import AuditLog

    return AuditLog.query.order_by(AuditLog.created_at.desc()).limit(limit).all()


def _import_metrics(csv_text: str) -> int:
    reader = csv.DictReader(StringIO(csv_text.strip()))
    count = 0
    for row in reader:
        if not row:
            continue
        metric = MetricDaily(
            offer_id=int(row["offer_id"]),
            campaign_draft_id=int(row["campaign_draft_id"])
            if row.get("campaign_draft_id")
            else None,
            day=datetime.strptime(row["day"], "%Y-%m-%d").date(),
            channel=row.get("channel", "Google Ads"),
            country=row.get("country", "US"),
            device=row.get("device", "all"),
            impressions=int(row.get("impressions") or 0),
            clicks=int(row.get("clicks") or 0),
            cost=decimal_value(row.get("cost")),
            conversions=int(row.get("conversions") or 0),
            revenue=decimal_value(row.get("revenue")),
        )
        db.session.add(metric)
        db.session.flush()
        for action in recommended_actions(metric):
            db.session.add(
                OptimizationAction(
                    offer_id=metric.offer_id,
                    campaign_draft_id=metric.campaign_draft_id,
                    severity=action["severity"],
                    action_type=action["action_type"],
                    message=action["message"],
                )
            )
        count += 1
    add_audit("metrics", None, "import", f"Imported {count} metric rows.")
    db.session.commit()
    return count


def _float(value: str | None, default: float = 0) -> float:
    if value in (None, ""):
        return default
    return float(value)


def _int(value: str | None, default: int = 0) -> int:
    if value in (None, ""):
        return default
    return int(float(value))
