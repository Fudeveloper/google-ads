from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

HIGH_RISK_DOCS = [
    ROOT / "docs" / "high_risk" / "ads_cookie_backend_operation.md",
    ROOT / "docs" / "high_risk" / "automated_login_2fa_challenge_bypass.md",
    ROOT / "docs" / "high_risk" / "invalid_traffic_click_impression_simulation.md",
    ROOT / "docs" / "high_risk" / "proxy_fingerprint_worker_association_evasion.md",
    ROOT / "docs" / "high_risk" / "cloaking_review_user_page_mismatch.md",
    ROOT / "docs" / "high_risk" / "ban_evasion_account_switching.md",
]

REQUIRED_PHRASES = [
    "范围",
    "原理解释",
    "行业诉求",
    "风险",
    "系统落地",
    "ADXKit 对应点和完成形态",
    "功能拆解和安全完成清单",
    "信息来源 URL",
]

HIGH_RISK_REQUIRED_TOPICS = {
    ROOT / "docs" / "high_risk" / "ads_cookie_backend_operation.md": [
        "后台操作链路的本质",
        "Cookie 自动化和官方授权的区别",
        "套利团队真正要解决的问题",
        "Google Ads 后台对象模型",
        "后台操作生命周期",
        "审计字段设计",
        "SOP",
    ],
    ROOT / "docs" / "high_risk" / "automated_login_2fa_challenge_bypass.md": [
        "Step-up challenge",
        "账号协作和绕过登录的区别",
        "自动化设计原则",
        "认证链路状态机",
        "人机分工边界",
        "任务系统中的危险语义",
        "审计字段设计",
        "SOP",
    ],
    ROOT / "docs" / "high_risk" / "invalid_traffic_click_impression_simulation.md": [
        "信号污染路径",
        "追踪断点不等于缺点击",
        "自然流量的可解释性",
        "流量账本状态机",
        "异常诊断决策树",
        "供应商和来源证据",
        "审计字段设计",
        "SOP",
    ],
    ROOT / "docs" / "high_risk" / "proxy_fingerprint_worker_association_evasion.md": [
        "关联图谱原理",
        "合法隔离和规避关联的边界",
        "关联资产图谱",
        "供应商红旗话术",
        "Worker / Edge 的安全使用边界",
        "合法隔离证据包",
        "审计字段设计",
        "Association Risk Score",
        "SOP",
    ],
    ROOT / "docs" / "high_risk" / "cloaking_review_user_page_mismatch.md": [
        "差异化页面的判断边界",
        "链路一致性",
        "常见误区",
        "Review / User Consistency Matrix",
        "URL / Page Version 生命周期",
        "A/B 测试、本地化和 Cloaking 的边界",
        "Destination Consistency Score",
        "审计字段设计",
        "SOP",
    ],
    ROOT / "docs" / "high_risk" / "ban_evasion_account_switching.md": [
        "账号不是孤立资产",
        "正常多账号管理 vs 规避封禁",
        "恢复流程的原理",
        "账号暂停状态机",
        "Related Account / Asset 风险",
        "申诉证据包",
        "正常多账号准入清单",
        "审计字段设计",
        "Account Recovery Score",
        "SOP",
    ],
}

REQUIRED_INDEX_DOCS = [
    ROOT / "docs" / "docs_index.md",
    ROOT / "docs" / "source_library.md",
    ROOT / "docs" / "requirement_traceability_matrix.md",
    ROOT / "docs" / "risk_matrix_and_sources.md",
    ROOT / "docs" / "high_risk_capability_research.md",
    ROOT / "docs" / "high_risk_completion_audit.md",
    ROOT / "docs" / "high_risk_capability_safe_reproduction_blueprint.md",
    ROOT / "docs" / "adxkit_breakdown.md",
    ROOT / "docs" / "ads_arbitrage_business_models.md",
    ROOT / "docs" / "ads_arbitrage_source_evidence_matrix.md",
    ROOT / "docs" / "ads_arbitrage_operations.md",
    ROOT / "docs" / "search_arbitrage_feed_parking.md",
    ROOT / "docs" / "rsoc_n2s_search_feed_partner_governance.md",
    ROOT / "docs" / "keyword_intent_research.md",
    ROOT / "docs" / "seasonality_event_demand_forecasting.md",
    ROOT / "docs" / "search_terms_negative_keyword_query_mining.md",
    ROOT / "docs" / "brand_bidding_trademark_competitor_policy.md",
    ROOT / "docs" / "competitor_ad_intelligence_serp_transparency.md",
    ROOT / "docs" / "traffic_channel_vendor_due_diligence.md",
    ROOT / "docs" / "traffic_inventory_controls.md",
    ROOT / "docs" / "source_publisher_placement_quality_governance.md",
    ROOT / "docs" / "traffic_vendor_contract_io_dispute_governance.md",
    ROOT / "docs" / "audience_remarketing_customer_match_policy.md",
    ROOT / "docs" / "affiliate_network_due_diligence.md",
    ROOT / "docs" / "lead_buyer_contract_io_paid_definition_governance.md",
    ROOT / "docs" / "lead_quality_postback_reconciliation.md",
    ROOT / "docs" / "lead_form_call_tracking_tcpa_compliance.md",
    ROOT / "docs" / "call_tracking_dni_number_pool_attribution_governance.md",
    ROOT / "docs" / "pay_per_call_buyer_routing_duration_payout_governance.md",
    ROOT / "docs" / "lead_consent_proof_certificate_evidence_governance.md",
    ROOT / "docs" / "lead_form_funnel_qualification_ux.md",
    ROOT / "docs" / "ping_post_lead_marketplace_buyer_routing.md",
    ROOT / "docs" / "lead_freshness_aged_recontact_governance.md",
    ROOT / "docs" / "lead_validation_suppression_pii_governance.md",
    ROOT / "docs" / "speed_to_lead_contact_sla_governance.md",
    ROOT / "docs" / "experiment_design_optimization.md",
    ROOT / "docs" / "invalid_traffic_detection_sop.md",
    ROOT / "docs" / "anomaly_monitoring_alerting_stoploss_incident_triage.md",
    ROOT / "docs" / "content_production_editorial_quality.md",
    ROOT / "docs" / "sensitive_vertical_policy_playbook.md",
    ROOT / "docs" / "metric_dictionary.md",
    ROOT / "docs" / "unit_economics_margin_safety.md",
    ROOT / "docs" / "offer_vertical_evaluation.md",
    ROOT / "docs" / "cpl_vertical_economics_qualification_playbook.md",
    ROOT / "docs" / "insurance_medicare_aca_final_expense_lead_governance.md",
    ROOT / "docs" / "loan_mortgage_credit_debt_lead_governance.md",
    ROOT / "docs" / "legal_case_intake_mass_tort_lead_governance.md",
    ROOT / "docs" / "home_services_solar_local_services_lead_governance.md",
    ROOT / "docs" / "education_career_training_student_lead_governance.md",
    ROOT / "docs" / "healthcare_medical_appointment_lead_governance.md",
    ROOT / "docs" / "b2b_saas_professional_services_lead_governance.md",
    ROOT / "docs" / "crypto_investment_trading_lead_governance.md",
    ROOT / "docs" / "employment_recruiting_staffing_lead_governance.md",
    ROOT / "docs" / "gambling_sweepstakes_sports_betting_lead_governance.md",
    ROOT / "docs" / "addiction_treatment_rehab_behavioral_health_lead_governance.md",
    ROOT / "docs" / "government_services_immigration_public_benefits_lead_governance.md",
    ROOT / "docs" / "lead_pricing_payout_negotiation_governance.md",
    ROOT / "docs" / "appointment_lead_booking_show_rate_governance.md",
    ROOT / "docs" / "offer_cap_payout_status_governance.md",
    ROOT / "docs" / "buyer_capacity_cap_pacing_dayparting_governance.md",
    ROOT / "docs" / "traffic_source_tracking.md",
    ROOT / "docs" / "native_advertorial_presell_compliance.md",
    ROOT / "docs" / "click_session_revenue_reconciliation.md",
    ROOT / "docs" / "tracking_template_redirect_chain_qa.md",
    ROOT / "docs" / "campaign_taxonomy_naming_label_dimension_governance.md",
    ROOT / "docs" / "attribution_incrementality_cannibalization.md",
    ROOT / "docs" / "conversion_tracking_value_feedback.md",
    ROOT / "docs" / "conversion_signal_quality_bidding_learning_governance.md",
    ROOT / "docs" / "crm_buyer_feedback_offline_conversion_mapping.md",
    ROOT / "docs" / "decision_window_revenue_lag_governance.md",
    ROOT / "docs" / "landing_page_quality_mfa.md",
    ROOT / "docs" / "domain_site_asset_governance.md",
    ROOT / "docs" / "landing_offer_intelligence_creative_brief.md",
    ROOT / "docs" / "cashflow_settlement_risk.md",
    ROOT / "docs" / "subscription_refund_ltv_chargeback_governance.md",
    ROOT / "docs" / "revenue_reconciliation_adstack.md",
    ROOT / "docs" / "creative_testing_optimization.md",
    ROOT / "docs" / "creative_angle_library_feedback_loop.md",
    ROOT / "docs" / "creative_claim_review_fact_checking.md",
    ROOT / "docs" / "google_ads_ad_review_disapproval_appeal_playbook.md",
    ROOT / "docs" / "ai_provider_prompt_cost_governance.md",
    ROOT / "docs" / "link_rotation_compliance.md",
    ROOT / "docs" / "campaign_launch_automation.md",
    ROOT / "docs" / "google_ads_editor_csv_bulk_upload_governance.md",
    ROOT / "docs" / "google_ads_scripts_safe_automation.md",
    ROOT / "docs" / "google_ads_scripts_data_sync_consistency.md",
    ROOT / "docs" / "task_orchestration_approval_audit_runbook.md",
    ROOT / "docs" / "google_ads_recommendations_experiments_auto_apply_governance.md",
    ROOT / "docs" / "google_ads_auction_bidding_quality_score.md",
    ROOT / "docs" / "google_ads_reporting_diagnostics.md",
    ROOT / "docs" / "search_automation_ai_max_broad_match.md",
    ROOT / "docs" / "performance_max_demand_gen_automation.md",
    ROOT / "docs" / "geo_language_localization_currency.md",
    ROOT / "docs" / "budget_pacing_scaling_stoploss.md",
    ROOT / "docs" / "portfolio_budget_allocation_risk_concentration.md",
    ROOT / "docs" / "account_mcc_billing_verification_governance.md",
    ROOT / "docs" / "policy_account_health_sop.md",
    ROOT / "docs" / "adsense_site_approval_policy_center.md",
    ROOT / "docs" / "publisher_monetization_stack.md",
    ROOT / "docs" / "publisher_ad_quality_blocking_controls.md",
    ROOT / "docs" / "programmatic_supply_chain_transparency.md",
    ROOT / "docs" / "gam_adx_yield_floor_pricing.md",
    ROOT / "docs" / "header_bidding_prebid_ad_stack.md",
    ROOT / "docs" / "ad_placement_refresh_viewability.md",
    ROOT / "docs" / "privacy_consent_tracking.md",
]

URL_RE = re.compile(r"https?://[^\s)]+")


def main() -> None:
    missing: list[str] = []

    for path in HIGH_RISK_DOCS:
        text = path.read_text(encoding="utf-8")
        for phrase in REQUIRED_PHRASES:
            if phrase not in text:
                missing.append(f"{path.relative_to(ROOT)} missing phrase: {phrase}")
        urls = URL_RE.findall(text)
        if len(urls) < 4:
            missing.append(
                f"{path.relative_to(ROOT)} should contain at least 4 source URLs, found {len(urls)}"
            )
        if "不提供" not in text and "不实现" not in text:
            missing.append(
                f"{path.relative_to(ROOT)} should explicitly state non-implementation boundary"
            )
        for phrase in HIGH_RISK_REQUIRED_TOPICS[path]:
            if phrase not in text:
                missing.append(f"{path.relative_to(ROOT)} missing principle topic: {phrase}")

    for path in REQUIRED_INDEX_DOCS:
        text = path.read_text(encoding="utf-8")
        if "https://" not in text:
            missing.append(f"{path.relative_to(ROOT)} should contain source URLs")

    source_library = (ROOT / "docs" / "source_library.md").read_text(encoding="utf-8")
    for label in [
        "ADXKit homepage",
        "Circumventing systems",
        "Definition of invalid traffic",
        "Cloudflare Workers",
        "Google Search spam policies",
        "Google Ads, About lead form assets",
        "Google Ads, About call assets",
        "Google Ads, About call reporting",
        "FTC, Complying with the Telemarketing Sales Rule",
        "FCC, TCPA one-to-one consent rule deletion order",
        "Voluum, Parameters in Postback URLs",
        "Google AdSense, Search ads policies",
        "Google AdSense, Related search for content pages",
        "Google AdSense, AFS Product-Integrated Feature policies",
        "Google Custom Search Ads implementation guide",
        "Google Ads, Parked domain site",
        "Google Ads, How the Google Ads auction works",
        "Google Ads, About Quality Score for Search campaigns",
        "Google Ads, Trademarks",
        "Google Ads, Counterfeit goods",
        "Google Ads, Primary and secondary conversion actions",
        "Google Ads API, Manage offline conversions",
        "Google Ads, About content suitability",
        "Google Ads, PMax channel performance report",
        "Google Ads, About audience segments",
        "Google Ads, Customer Match policy",
        "Google Ads, About audience signals for Performance Max campaigns",
        "Google Ads, Budget report",
        "Google Ads, About ad scheduling",
        "Google Ads, About bid adjustments",
        "Google Ads, About parallel tracking",
        "Google Ads, Final URL suffix",
        "Google Ads, Destination experience",
        "Google Ads, Editorial requirements",
        "Google Ads, Misrepresentation",
        "Google Ads, Trademarks",
        "Google Ads, Unacceptable business practices",
        "FTC, Endorsement Guides",
        "FTC, Endorsements, influencers, and reviews",
        "Google Ads Scripts, Limits",
        "Google Ads Scripts, AdsApp reference",
        "Google Ads Scripts, BulkUpload reference",
        "Google Ads Editor, Prepare a CSV file",
        "Google Ads Editor, Check changes before posting",
        "Google Ads Editor, Review recent account changes",
        "Google Ads Editor, Share proposed changes",
        "Google Ads Editor, Post changes",
        "Google Ads Help, Bulk uploads",
        "Google Ads Scripts, Reports",
        "Google Ads Scripts, Manager account scripts",
        "Google Ads Scripts, External data integration",
        "Google Ads, About data freshness",
        "Google Ads, Data discrepancies",
        "Google Ads, About conversion lag reporting",
        "Google Ads API, Reporting overview",
        "Google Ads, Using scripts to make automated changes",
        "Google Ads Scripts, Execution logs",
        "Google Ads Scripts, Preview mode",
        "Google Ads, Change history",
        "Google Ads API, Change event",
        "Google Ads API, Partial failures",
        "Google SRE, Postmortem culture",
        "Google SRE, Managing incidents",
        "NIST, AI Risk Management Framework",
        "OWASP, Top 10 for LLM Applications",
        "Google AdSense Help, Payment timelines",
        "Google AdSense Management API, Metrics and Dimensions",
        "Google Ad Manager API, Reporting",
        "Google Ad Manager API, ReportService",
    ]:
        if label not in source_library:
            missing.append(f"source_library.md missing source label: {label}")

    completion_audit = (ROOT / "docs" / "high_risk_completion_audit.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "完成口径",
        "逐点完成审计",
        "已完成专题",
        "系统验收路径",
        "当前完成证据",
        "验证命令",
        "信息来源 URL",
        "不交付",
    ]:
        if phrase not in completion_audit:
            missing.append(f"high_risk_completion_audit.md missing phrase: {phrase}")
    if len(URL_RE.findall(completion_audit)) < 12:
        missing.append(
            "high_risk_completion_audit.md should contain at least 12 source URLs"
        )

    adxkit_breakdown = (ROOT / "docs" / "adxkit_breakdown.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "核心能力验收矩阵",
        "公开能力和行业原理",
        "系统证据",
        "文档证据和来源 URL",
        "不交付边界",
        "验收结论",
        "高风险能力不是空白排除项",
    ]:
        if phrase not in adxkit_breakdown:
            missing.append(f"adxkit_breakdown.md missing phrase: {phrase}")
    if len(URL_RE.findall(adxkit_breakdown)) < 12:
        missing.append("adxkit_breakdown.md should contain at least 12 source URLs")

    acceptance_checklist = (ROOT / "docs" / "acceptance_checklist.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "ADXKit 核心验收证据矩阵",
        "公开能力已经复刻到哪里",
        "高风险能力按知识、原理、审计、SOP、来源 URL 和安全替代流程完成",
        "来源 URL 验收位置",
        "不交付执行性绕过能力",
        "python scripts/acceptance_audit.py",
        "acceptance_audit.py` 汇总检查文档映射",
    ]:
        if phrase not in acceptance_checklist:
            missing.append(f"acceptance_checklist.md missing phrase: {phrase}")

    env_example_path = ROOT / ".env.example"
    if not env_example_path.exists():
        missing.append(".env.example is required for MySQL setup")
    else:
        env_example = env_example_path.read_text(encoding="utf-8")
        for phrase in [
            "SECRET_KEY=change-me",
            "DATABASE_URL=mysql+pymysql://ads_user:ads_password@127.0.0.1:3306/ads_workbench?charset=utf8mb4",
        ]:
            if phrase not in env_example:
                missing.append(f".env.example missing phrase: {phrase}")
        for forbidden in ["COOKIE", "SESSION_TOKEN", "PROXY", "FINGERPRINT", "ACCOUNT_POOL"]:
            if forbidden in env_example.upper():
                missing.append(f".env.example should not contain high-risk config: {forbidden}")

    system_design = (ROOT / "docs" / "system_design.md").read_text(encoding="utf-8")
    for phrase in [
        "代理、指纹、Worker 转发用于规避关联检测",
        "为规避封禁创建或切换账号",
        "/accounts` 记录账号配置、同步方式、状态备注和申诉复盘",
        "/risk-audits` 和 `/sources` 承接 6 个高风险能力",
        "能运行 `scripts/acceptance_audit.py`",
    ]:
        if phrase not in system_design:
            missing.append(f"system_design.md missing phrase: {phrase}")

    usage_doc = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
    for phrase in [
        ".env.example` 只提供 Flask 和 MySQL 连接配置",
        "代理/IP/指纹/Worker 转发用于规避关联检测",
        "为规避封禁创建或切换账号",
        "系统会检查任务类型、任务名称和备注",
        "包含登录接管、Cookie、Session Token、2FA、安全挑战、补点击、模拟流量、代理池、指纹、Worker 转发、cloaking 或换号语义的任务会被拒绝创建",
    ]:
        if phrase not in usage_doc:
            missing.append(f"usage.md missing phrase: {phrase}")

    development_doc = (ROOT / "docs" / "development.md").read_text(encoding="utf-8")
    for phrase in [
        "仓库提供 `.env.example`",
        "不能新增 Google Ads Cookie、Session Token、浏览器 Profile、代理池、指纹配置、Worker 规避规则、账号池或封禁后换号资料",
        "任务类型、任务名称和任务备注都必须通过 `services/tasks.py` 的白名单和危险语义检查",
        "账号配置创建时会拒绝明显包含 Cookie 登录、Cookie 操作、Session Token、浏览器 Profile",
        "python scripts/acceptance_audit.py",
        "`acceptance_audit.py` 会汇总检查 Markdown 文档路由映射",
    ]:
        if phrase not in development_doc:
            missing.append(f"development.md missing phrase: {phrase}")

    task_service = (ROOT / "adsworkbench" / "services" / "tasks.py").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "FORBIDDEN_TASK_TEXT_TERMS",
        "validate_task_text",
        "proxy/fingerprint",
        "account switching semantics",
    ]:
        if phrase not in task_service:
            missing.append(f"tasks.py missing guardrail phrase: {phrase}")

    markdown_renderer = (
        ROOT / "adsworkbench" / "services" / "markdown_render.py"
    ).read_text(encoding="utf-8")
    for phrase in [
        "def render_markdown",
        "doc-table",
        "def _normalize_href",
        'return f"/doc/{clean}"',
    ]:
        if phrase not in markdown_renderer:
            missing.append(f"markdown_render.py missing phrase: {phrase}")

    routes_py = (ROOT / "adsworkbench" / "routes.py").read_text(encoding="utf-8")
    for phrase in [
        '@bp.route("/doc/<path:filename>")',
        "def _render_markdown_doc",
        "render_markdown(content)",
    ]:
        if phrase not in routes_py:
            missing.append(f"routes.py missing Markdown doc route phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in [
        "copy .env.example .env",
        "python scripts/verify_research_docs.py",
        "python scripts/acceptance_audit.py",
        "已交付与已沉淀能力",
        "下面能力分为两类",
        "不包含 Google Ads Cookie、代理池、浏览器指纹、账号池或任何后台接管凭据",
    ]:
        if phrase not in readme:
            missing.append(f"README.md missing phrase: {phrase}")
    if "## 计划中的系统能力" in readme:
        missing.append("README.md should not describe delivered scope as planned system capability")

    docs_index = (ROOT / "docs" / "docs_index.md").read_text(encoding="utf-8")
    for phrase in [
        "文档入口和验收导航",
        "端到端验收路径",
        "ADXKit 核心能力对应入口",
        "高风险能力完成入口",
        "这些能力不是“不复刻”",
        "验证命令",
        "acceptance_audit.py` 会汇总检查 Markdown 文档路由映射",
        "信息来源 URL",
    ]:
        if phrase not in docs_index:
            missing.append(f"docs_index.md missing phrase: {phrase}")
    if len(URL_RE.findall(docs_index)) < 6:
        missing.append("docs_index.md should contain at least 6 source URLs")

    operations = (ROOT / "docs" / "ads_arbitrage_operations.md").read_text(
        encoding="utf-8"
    )
    for phrase in ["日报", "周报", "月报", "预算", "止损", "追踪和对账", "事故复盘"]:
        if phrase not in operations:
            missing.append(f"ads_arbitrage_operations.md missing phrase: {phrase}")
    if len(URL_RE.findall(operations)) < 8:
        missing.append("ads_arbitrage_operations.md should contain at least 8 source URLs")

    metrics = (ROOT / "docs" / "metric_dictionary.md").read_text(encoding="utf-8")
    for phrase in [
        "买量指标",
        "页面指标",
        "变现指标",
        "利润指标",
        "样本和显著性",
        "回传延迟",
        "扣量和拒付",
        "字段命名建议",
    ]:
        if phrase not in metrics:
            missing.append(f"metric_dictionary.md missing phrase: {phrase}")
    if len(URL_RE.findall(metrics)) < 6:
        missing.append("metric_dictionary.md should contain at least 6 source URLs")

    unit_economics = (
        ROOT / "docs" / "unit_economics_margin_safety.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么单位经济是套利第一性原理",
        "原理解释：利润来自可收款 RPV，而不是报表好看",
        "核心对象地图",
        "三种业务模型公式",
        "Safety Factor 设计",
        "Margin of Safety",
        "Sensitivity Analysis",
        "Test Budget 和硬止损",
        "Break-even 决策矩阵",
        "与出价策略的关系",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "功能拆解和安全完成清单",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in unit_economics:
            missing.append(f"unit_economics_margin_safety.md missing phrase: {phrase}")
    if len(URL_RE.findall(unit_economics)) < 14:
        missing.append("unit_economics_margin_safety.md should contain at least 14 source URLs")

    verticals = (ROOT / "docs" / "offer_vertical_evaluation.md").read_text(
        encoding="utf-8"
    )
    for phrase in ["评估维度", "评分模型", "常见垂类判断", "Offer 资料清单", "测试设计", "拒绝标准"]:
        if phrase not in verticals:
            missing.append(f"offer_vertical_evaluation.md missing phrase: {phrase}")
    if len(URL_RE.findall(verticals)) < 6:
        missing.append("offer_vertical_evaluation.md should contain at least 6 source URLs")

    cpl_vertical_economics = (
        ROOT / "docs" / "cpl_vertical_economics_qualification_playbook.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 CPL 垂类不能只看 Payout",
        "垂类经济的核心变量",
        "资格问题地图",
        "Insurance / Medicare / Health Plan Leads",
        "Loan / Mortgage / Credit / Debt Leads",
        "Legal Leads",
        "Home Services / Solar / Local Services Leads",
        "Education / Career Training Leads",
        "Healthcare / Appointment Leads",
        "B2B SaaS / Professional Services Leads",
        "Vertical Fit Score",
        "垂类测试模板",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in cpl_vertical_economics:
            missing.append(
                f"cpl_vertical_economics_qualification_playbook.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(cpl_vertical_economics)) < 16:
        missing.append(
            "cpl_vertical_economics_qualification_playbook.md should contain at least 16 source URLs"
        )

    insurance_leads = (
        ROOT / "docs" / "insurance_medicare_aca_final_expense_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Insurance Lead 是高 payout 高拒付垂类",
        "原理解释：保险 Lead 是资格、授权和信任的交接",
        "Subvertical 地图",
        "资格字段和数据最小化",
        "Eligibility、Reject Reason 和 Buyer Acceptance",
        "Licensed Agent、Broker、Carrier 和官方关系边界",
        "Enrollment Window：Medicare / ACA / Final Expense",
        "Call、Form、Appointment 和 Pay-per-call",
        "Consent、TCPA、DNC 和证据链",
        "Google Ads 政策和受众边界",
        "CMS、Marketplace 和 Medicare Marketing",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Insurance Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in insurance_leads:
            missing.append(
                "insurance_medicare_aca_final_expense_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(insurance_leads)) < 18:
        missing.append(
            "insurance_medicare_aca_final_expense_lead_governance.md should "
            "contain at least 18 source URLs"
        )

    loan_debt_leads = (
        ROOT / "docs" / "loan_mortgage_credit_debt_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Loan / Debt Lead 是高 payout 高风险垂类",
        "原理解释：金融 Lead 是 eligibility、disclosure 和 money flow 的交接",
        "Subvertical 地图",
        "资格字段和数据最小化",
        "Eligibility、Reject Reason 和 Buyer Acceptance",
        "Licensed Lender、Broker、Lead Generator 和 Marketplace 边界",
        "Financial Product Comparison 和 Steering 风险",
        "Debt Relief、Credit Repair 和 Student Loan Relief 特殊风险",
        "Google Ads 政策、HEC 和 Personalized Ads",
        "FCRA、ECOA、TILA、TSR 和 DNC 边界",
        "Consent、Disclosure 和证据链",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Financial Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in loan_debt_leads:
            missing.append(
                "loan_mortgage_credit_debt_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(loan_debt_leads)) < 18:
        missing.append(
            "loan_mortgage_credit_debt_lead_governance.md should "
            "contain at least 18 source URLs"
        )

    legal_leads = (
        ROOT / "docs" / "legal_case_intake_mass_tort_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Legal Lead 是高 payout 高拒付垂类",
        "原理解释：Legal Lead 是案件资格、律师边界和信任的交接",
        "Practice Area / Case Type 地图",
        "资格字段和数据最小化",
        "Eligibility、Reject Reason 和 Buyer Acceptance",
        "Attorney、Law Firm、Intake Center、Lead Generator 和 Referral 边界",
        "Lawyer Advertising、Solicitation、Testimonials 和 Review 风险",
        "Mass Tort、Class Action、Settlement 和 Government/Court Claim 风险",
        "Call、Form、Appointment、Pay-per-call 和 Retainer",
        "Consent、TCPA、DNC、Recording 和 Confidentiality",
        "Google Ads 政策和 Local Services Ads 边界",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Legal Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in legal_leads:
            missing.append(
                "legal_case_intake_mass_tort_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(legal_leads)) < 18:
        missing.append(
            "legal_case_intake_mass_tort_lead_governance.md should "
            "contain at least 18 source URLs"
        )

    home_services_leads = (
        ROOT / "docs" / "home_services_solar_local_services_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Home Services Lead 是高意图高运营风险垂类",
        "原理解释：Local Services Lead 是需求、地点、能力和信任的交接",
        "Service Category 地图",
        "资格字段和数据最小化",
        "Contractor / Buyer Eligibility、License、Insurance 和 Service Area",
        "Service Area、Hours、Dispatch Capacity 和 Emergency Lead",
        "Lead Delivery：Form、Call、Pay-per-call、Booking 和 Quote",
        "Google Local Services Ads、Charged Lead、Credit 和 Dispute",
        "Solar Lead 特殊风险",
        "Home Improvement Scam、Review、Price 和 Claim 风险",
        "Google Ads、Local Services 和 Business Profile 边界",
        "Consent、TCPA、DNC、Recording 和 Home Access",
        "Offline Value Mapping",
        "Home Services Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in home_services_leads:
            missing.append(
                "home_services_solar_local_services_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(home_services_leads)) < 18:
        missing.append(
            "home_services_solar_local_services_lead_governance.md should "
            "contain at least 18 source URLs"
        )

    education_leads = (
        ROOT / "docs" / "education_career_training_student_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Education Lead 是高 payout 长回传垂类",
        "原理解释：Education Lead 是意图、资格、项目承诺和招生回传的交接",
        "Program / School Type 地图",
        "资格字段和数据最小化",
        "Accreditation、State Authorization、Licensure 和 Transferability",
        "Job Placement、Salary、Career Outcome 和 Guarantee 风险",
        "Financial Aid、Student Loan、Scholarship 和 GI Bill 风险",
        "Lead Delivery：Form、Call、Appointment、Application 和 Enrollment",
        "Buyer Acceptance、Reject Reason 和 Enrollment Funnel",
        "Google Ads、Personalized Ads 和 Misrepresentation 边界",
        "Consent、TCPA、CAN-SPAM、DNC 和 Student Data",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Education Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in education_leads:
            missing.append(
                "education_career_training_student_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(education_leads)) < 18:
        missing.append(
            "education_career_training_student_lead_governance.md should "
            "contain at least 18 source URLs"
        )

    healthcare_leads = (
        ROOT / "docs" / "healthcare_medical_appointment_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Healthcare Lead 是高 payout 高隐私垂类",
        "原理解释：Healthcare Lead 是需求、资格、隐私和到诊价值的交接",
        "Service / Provider Type 地图",
        "资格字段和数据最小化",
        "Provider / Buyer Eligibility、License、Insurance Network 和 Service Area",
        "Google Ads、Healthcare Policy 和 Personalized Ads 边界",
        "HIPAA、PHI、Tracking 和 Health Data 边界",
        "Health Claim、FDA / FTC、Before-after 和 Testimonial 风险",
        "Lead Delivery：Form、Call、Appointment、Telehealth 和 Pay-per-call",
        "Buyer Acceptance、Reject Reason 和 Appointment Funnel",
        "Consent、TCPA、CAN-SPAM、DNC、Recording 和 Patient Communication",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Healthcare Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in healthcare_leads:
            missing.append(
                "healthcare_medical_appointment_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(healthcare_leads)) < 20:
        missing.append(
            "healthcare_medical_appointment_lead_governance.md should "
            "contain at least 20 source URLs"
        )

    b2b_saas_leads = (
        ROOT / "docs" / "b2b_saas_professional_services_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 B2B SaaS Lead 是高 CPC 长销售周期垂类",
        "原理解释：B2B Lead 是 ICP、Intent、Buyer Committee 和 Pipeline 回传的交接",
        "Product / Service Type 地图",
        "资格字段和数据最小化",
        "ICP、Firmographic、Role 和 Buyer Committee",
        "MQL、SAL、SQL、Opportunity、Closed Won 和 PQL",
        "Google Ads、Trademark、Competitor Query 和 Software Policy 边界",
        "Lead Form、Consent、B2B Personal Data 和 Follow-up",
        "Creative / Landing Claim Review",
        "Pricing、Trial、Contract 和 Subscription 风险",
        "Buyer Acceptance、Reject Reason 和 Sales Feedback",
        "Offline Value Mapping",
        "B2B Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in b2b_saas_leads:
            missing.append(
                "b2b_saas_professional_services_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(b2b_saas_leads)) < 20:
        missing.append(
            "b2b_saas_professional_services_lead_governance.md should "
            "contain at least 20 source URLs"
        )

    crypto_investment_leads = (
        ROOT / "docs" / "crypto_investment_trading_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Crypto / Investment Lead 是极高 payout 极高风险垂类",
        "原理解释：Financial Lead 是信任、资质、风险披露和资金行为的交接",
        "Product / Offer Type 地图",
        "Offer 准入、Certification、License 和 Jurisdiction",
        "资格字段和数据最小化",
        "Google Ads、Crypto、Financial Products 和 Complex Speculative 边界",
        "Investment Claim、Performance、Testimonials 和 Social Proof 风险",
        "Scam Red Flags、Fraud Pattern 和拒绝标准",
        "Lead Delivery：Form、Call、App Install、KYC、Deposit 和 Funded Account",
        "Buyer Acceptance、Reject Reason 和 Payment Risk",
        "Consent、Privacy、KYC、AML 和 Sensitive Financial Data",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Crypto / Investment Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in crypto_investment_leads:
            missing.append(
                "crypto_investment_trading_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(crypto_investment_leads)) < 20:
        missing.append(
            "crypto_investment_trading_lead_governance.md should "
            "contain at least 20 source URLs"
        )

    employment_leads = (
        ROOT / "docs" / "employment_recruiting_staffing_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Employment Lead 是高量高信任垂类",
        "原理解释：Employment Lead 是机会、资格、信任和雇佣回传的交接",
        "Job / Buyer Type 地图",
        "资格字段和数据最小化",
        "Real Job Order、Employer Authorization 和 Ghost Job 风险",
        "Google Ads、HEC / Employment Targeting 和 Personalized Ads 边界",
        "Job Scam、Work-from-home 和 Business Opportunity 风险",
        "EEOC、Job Ads、Recruitment 和 Discrimination 边界",
        "Pay、Benefits、Remote、Contractor 和 Classification 风险",
        "Background Check、Resume Data 和 Candidate Privacy",
        "Lead Delivery：Form、Call、Resume Upload、Interview 和 Hire",
        "Buyer Acceptance、Reject Reason 和 Hiring Funnel",
        "Consent、TCPA、CAN-SPAM、DNC 和 Candidate Communication",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Employment Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in employment_leads:
            missing.append(
                "employment_recruiting_staffing_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(employment_leads)) < 20:
        missing.append(
            "employment_recruiting_staffing_lead_governance.md should "
            "contain at least 20 source URLs"
        )

    gambling_leads = (
        ROOT / "docs" / "gambling_sweepstakes_sports_betting_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Gambling Lead 是高 payout 强监管垂类",
        "原理解释：Gambling Lead 是许可、年龄、地区、风险披露和资金行为的交接",
        "Product / Offer Type 地图",
        "Offer 准入、Google Certification、License 和 Jurisdiction",
        "Age Gate、Geolocation、KYC 和 Self-exclusion",
        "Google Ads、Gambling and Games、Personalized Ads 边界",
        "Sweepstakes、Prize Promotion、Lottery 和 Contest 风险",
        "Bonus、Free Bet、Odds、Winnings 和 Influencer Claim 风险",
        "Lead Delivery：Registration、KYC、Deposit、Wager 和 NGR",
        "Buyer Acceptance、Reject Reason 和 Payment Risk",
        "Consent、Privacy、Payment Data 和 Sensitive Categories",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Gambling Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in gambling_leads:
            missing.append(
                "gambling_sweepstakes_sports_betting_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(gambling_leads)) < 20:
        missing.append(
            "gambling_sweepstakes_sports_betting_lead_governance.md should "
            "contain at least 20 source URLs"
        )

    addiction_treatment_leads = (
        ROOT / "docs" / "addiction_treatment_rehab_behavioral_health_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Addiction Treatment Lead 是极高 payout 极高伦理风险垂类",
        "原理解释：Addiction Lead 是危机、隐私、治疗资格和付款路径的交接",
        "Program / Service Type 地图",
        "Offer 准入、Google Ads Certification、LegitScript 和 Provider License",
        "Provider / Referral / Call Center 角色边界",
        "Crisis、Suicide、Overdose 和 Emergency Handling",
        "HIPAA、42 CFR Part 2、Tracking 和 SUD Data 边界",
        "Patient Brokering、Kickback、Travel Incentive 和 Ethical Referral 风险",
        "Qualification Fields 和数据最小化",
        "Creative / Landing Claim Review",
        "Call Routing、Pay-per-call、Admissions 和 Buyer Acceptance",
        "Buyer Acceptance、Reject Reason 和 Payment Risk",
        "Consent、TCPA、CAN-SPAM、DNC 和 Sensitive Contact",
        "Offline Value Mapping",
        "Addiction Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in addiction_treatment_leads:
            missing.append(
                "addiction_treatment_rehab_behavioral_health_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(addiction_treatment_leads)) < 20:
        missing.append(
            "addiction_treatment_rehab_behavioral_health_lead_governance.md should "
            "contain at least 20 source URLs"
        )

    government_services_leads = (
        ROOT
        / "docs"
        / "government_services_immigration_public_benefits_lead_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Government Services Lead 是高意图高误导垂类",
        "原理解释：Government Services Lead 是官方关系、资格、费用和身份数据的交接",
        "Service / Document Type 地图",
        "Offer 准入、Authorization、Certification 和 Official Relationship",
        "Google Ads、Government Documents and Official Services 边界",
        "Immigration、Notario、Accredited Representative 和 Unauthorized Practice 风险",
        "Tax、IRS、Debt Relief 和 Professional Advice 边界",
        "Public Benefits、Free Money、Grant 和 Eligibility Claim 风险",
        "Qualification Fields 和身份数据最小化",
        "Fee、Refund、Processing Time 和 Approval Claim Review",
        "Lead Delivery：Form、Call、Consultation、Application 和 Issued Document",
        "Buyer Acceptance、Reject Reason 和 Payment Risk",
        "Consent、Privacy、Identity Data 和 Security",
        "Creative / Landing Claim Review",
        "Offline Value Mapping",
        "Government Services Lead Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in government_services_leads:
            missing.append(
                "government_services_immigration_public_benefits_lead_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(government_services_leads)) < 20:
        missing.append(
            "government_services_immigration_public_benefits_lead_governance.md "
            "should contain at least 20 source URLs"
        )

    lead_pricing = (
        ROOT / "docs" / "lead_pricing_payout_negotiation_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Lead Pricing 决定套利天花板",
        "原理解释：定价模型是风险分配机制",
        "核心对象地图",
        "主要定价模型",
        "Rate Card 和价格版本",
        "Effective Payout 和 Safe CPC",
        "Payout Negotiation：用什么证据谈价",
        "Scrub Buffer、Return Window 和 Reserve",
        "Tiered Payout、Floor、Cap 和 Step Rules",
        "Buyer Mix、Routing 和价格瀑布",
        "Contract、Invoice 和 Payment Term",
        "Google Ads 与出价边界",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in lead_pricing:
            missing.append(
                "lead_pricing_payout_negotiation_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(lead_pricing)) < 14:
        missing.append(
            "lead_pricing_payout_negotiation_governance.md should contain "
            "at least 14 source URLs"
        )

    appointment_leads = (
        ROOT / "docs" / "appointment_lead_booking_show_rate_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Appointment Lead 是 CPL 的高风险利润层",
        "原理解释：Booking 是承诺，不是收入",
        "核心对象地图",
        "Appointment 状态机",
        "Calendar Capacity 和 Slot 质量",
        "Reminder、Confirmation 和 Consent",
        "No-show、Cancel 和 Reschedule 归因",
        "Appointment Payout 和结算口径",
        "Google Ads 与 Offline Conversion",
        "Booking Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in appointment_leads:
            missing.append(
                "appointment_lead_booking_show_rate_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(appointment_leads)) < 18:
        missing.append(
            "appointment_lead_booking_show_rate_governance.md should "
            "contain at least 18 source URLs"
        )

    offer_cap_payout = (
        ROOT / "docs" / "offer_cap_payout_status_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Cap 和 Payout 是套利风险核心",
        "核心对象",
        "Offer 生命周期",
        "Cap 类型",
        "Cap Pacing 计算",
        "Payout 版本和 Effective Payout",
        "状态变更触发器",
        "替代 Offer 和 Fallback 规则",
        "Cap 和预算联动",
        "对账和结算窗口",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in offer_cap_payout:
            missing.append(
                f"offer_cap_payout_status_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(offer_cap_payout)) < 12:
        missing.append(
            "offer_cap_payout_status_governance.md should contain at least 12 source URLs"
        )

    buyer_capacity = (
        ROOT / "docs" / "buyer_capacity_cap_pacing_dayparting_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Buyer Capacity 决定 CPL 扩量上限",
        "原理解释：买量节奏必须跟接量节奏同步",
        "核心对象地图",
        "Capacity Profile 设计",
        "Cap 类型和 Reset 规则",
        "Capacity Pacing 公式",
        "Dayparting 的正确用法",
        "Google Ads Budget、Overdelivery 和内部 Hard Stop",
        "时区和日界线治理",
        "No Buyer、Fallback 和 Routing 降级",
        "Capacity Quality Score",
        "事故诊断",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in buyer_capacity:
            missing.append(
                "buyer_capacity_cap_pacing_dayparting_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(buyer_capacity)) < 14:
        missing.append(
            "buyer_capacity_cap_pacing_dayparting_governance.md should "
            "contain at least 14 source URLs"
        )

    traffic = (ROOT / "docs" / "traffic_source_tracking.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "流量源尽调清单",
        "追踪字段命名",
        "ValueTrack",
        "GA4",
        "S2S Postback",
        "对账表",
        "停量条件",
        "信息来源 URL",
    ]:
        if phrase not in traffic:
            missing.append(f"traffic_source_tracking.md missing phrase: {phrase}")
    if len(URL_RE.findall(traffic)) < 8:
        missing.append("traffic_source_tracking.md should contain at least 8 source URLs")

    native_presell = (
        ROOT / "docs" / "native_advertorial_presell_compliance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Native 是套利高频场景",
        "核心对象",
        "Native Funnel 结构",
        "Advertorial 与 Presell Page 边界",
        "素材、缩略图和 Claim 审核",
        "披露和商业关系",
        "Source / Publisher 质量治理",
        "Offer 条款和 Buyer Feedback",
        "报表和诊断",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in native_presell:
            missing.append(
                f"native_advertorial_presell_compliance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(native_presell)) < 10:
        missing.append(
            "native_advertorial_presell_compliance.md should contain at least 10 source URLs"
        )

    click_session = (
        ROOT / "docs" / "click_session_revenue_reconciliation.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么差异是常态",
        "对账漏斗",
        "Click -> Landing Request",
        "Landing Request -> GA4 Session",
        "Session -> Offer Click / Ad Request",
        "Conversion / Revenue Delay",
        "异常诊断矩阵",
        "数据修复原则",
        "对账工作流",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in click_session:
            missing.append(
                f"click_session_revenue_reconciliation.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(click_session)) < 12:
        missing.append(
            "click_session_revenue_reconciliation.md should contain at least 12 source URLs"
        )

    tracking_chain = (ROOT / "docs" / "tracking_template_redirect_chain_qa.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么追踪模板决定成败",
        "Google Ads URL 层级",
        "Tracking Template 原理",
        "Final URL Suffix 和参数合并",
        "Parallel Tracking",
        "Auto-tagging、GCLID、GBRAID、WBRAID",
        "Redirect Chain QA",
        "QA 流程",
        "常见事故和诊断",
        "换链接和模板变更边界",
        "系统落地",
        "信息来源 URL",
    ]:
        if phrase not in tracking_chain:
            missing.append(f"tracking_template_redirect_chain_qa.md missing phrase: {phrase}")
    if len(URL_RE.findall(tracking_chain)) < 10:
        missing.append("tracking_template_redirect_chain_qa.md should contain at least 10 source URLs")

    taxonomy_governance = (
        ROOT / "docs" / "campaign_taxonomy_naming_label_dimension_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么命名和维度治理是套利底座",
        "核心对象地图",
        "Campaign 命名规范",
        "Labels 使用原则",
        "UTM、ValueTrack、Custom Parameter 与 SubID 映射",
        "维度字典",
        "版本号和 Hash",
        "报表 Join Keys",
        "常见事故",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in taxonomy_governance:
            missing.append(
                "campaign_taxonomy_naming_label_dimension_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(taxonomy_governance)) < 16:
        missing.append(
            "campaign_taxonomy_naming_label_dimension_governance.md should contain at least 16 source URLs"
        )

    attribution_incrementality = (
        ROOT / "docs" / "attribution_incrementality_cannibalization.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么归因不等于增量利润",
        "原理解释：Attribution 分 credit，Incrementality 测 lift",
        "核心对象地图",
        "归因层：能用，但不要神化",
        "增量层：Lift、Holdout 和实验",
        "Cannibalization 类型",
        "Incrementality Score",
        "iROAS 和边际利润",
        "场景 SOP",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "功能拆解和安全完成清单",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in attribution_incrementality:
            missing.append(
                f"attribution_incrementality_cannibalization.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(attribution_incrementality)) < 12:
        missing.append(
            "attribution_incrementality_cannibalization.md should contain at least 12 source URLs"
        )

    conversion_tracking = (
        ROOT / "docs" / "conversion_tracking_value_feedback.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么转化追踪决定套利成败",
        "Conversion Action 架构",
        "事件命名和字段规范",
        "Click ID 与归因",
        "Offline Conversions",
        "Enhanced Conversions",
        "Conversion Value 设计",
        "Attribution Window 和 Conversion Lag",
        "Attribution Model",
        "数据 QA 和诊断",
        "信息来源 URL",
    ]:
        if phrase not in conversion_tracking:
            missing.append(f"conversion_tracking_value_feedback.md missing phrase: {phrase}")
    if len(URL_RE.findall(conversion_tracking)) < 10:
        missing.append("conversion_tracking_value_feedback.md should contain at least 10 source URLs")

    conversion_signal_quality = (
        ROOT / "docs" / "conversion_signal_quality_bidding_learning_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么转化信号质量决定套利出价学习",
        "原理解释：Smart Bidding 学的是你喂给它的目标",
        "核心对象地图",
        "信号分层：从 Micro Event 到 Paid Revenue",
        "Signal Quality Score",
        "Primary / Secondary 治理",
        "Value Feedback 设计",
        "Offline Conversion 与 Enhanced Conversion 边界",
        "Learning Period 和 Bid Strategy Report",
        "常见信号污染",
        "自动出价准入矩阵",
        "信号事故响应",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "功能拆解和安全完成清单",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in conversion_signal_quality:
            missing.append(
                "conversion_signal_quality_bidding_learning_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(conversion_signal_quality)) < 14:
        missing.append(
            "conversion_signal_quality_bidding_learning_governance.md should contain at least 14 source URLs"
        )

    crm_value_mapping = (
        ROOT / "docs" / "crm_buyer_feedback_offline_conversion_mapping.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 CRM 阶段映射决定自动出价质量",
        "原理解释：CRM Stage 不是 Ads Conversion Action",
        "核心对象地图",
        "Stage Taxonomy：先统一业务阶段",
        "Ads Conversion Action Mapping",
        "Value Mode 和金额口径",
        "Transaction ID、去重和状态更新",
        "Conversion Adjustment、Return 和 Clawback",
        "Import Batch QA 和 Diagnostics",
        "Lag Profile 和导入节奏",
        "Buyer Feedback 到优化动作",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in crm_value_mapping:
            missing.append(
                "crm_buyer_feedback_offline_conversion_mapping.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(crm_value_mapping)) < 14:
        missing.append(
            "crm_buyer_feedback_offline_conversion_mapping.md should "
            "contain at least 14 source URLs"
        )

    decision_windows = (
        ROOT / "docs" / "decision_window_revenue_lag_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么当天 ROI 是套利陷阱",
        "原理解释：数据刷新、转化延迟、收入延迟不是一回事",
        "核心对象地图",
        "三层窗口模型",
        "Decision Window Score",
        "业务模式窗口参考",
        "Budget Ramp 和等待规则",
        "Stop-loss 与 Wait-loss 的区别",
        "Cohort 和 Aging 表",
        "常见事故和诊断",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "功能拆解和安全完成清单",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in decision_windows:
            missing.append(
                "decision_window_revenue_lag_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(decision_windows)) < 14:
        missing.append(
            "decision_window_revenue_lag_governance.md should contain at least 14 source URLs"
        )

    landing = (ROOT / "docs" / "landing_page_quality_mfa.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "Google Ads 目的地体验",
        "广告密度",
        "MFA 风险识别",
        "内容质量评分",
        "页面上线检查表",
        "广告位置实验",
        "信息来源 URL",
    ]:
        if phrase not in landing:
            missing.append(f"landing_page_quality_mfa.md missing phrase: {phrase}")
    if len(URL_RE.findall(landing)) < 8:
        missing.append("landing_page_quality_mfa.md should contain at least 8 source URLs")

    domain_assets = (ROOT / "docs" / "domain_site_asset_governance.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么域名和站点资产是套利核心",
        "核心对象",
        "域名生命周期与历史风险",
        "Expired Domain Abuse / Site Reputation Abuse",
        "Parking / Feed / Search Arbitrage 边界",
        "站点组合与资产隔离",
        "站点迁移、换域名与封禁规避边界",
        "AdSense / Publisher 站点审核与 ads.txt",
        "Google Ads Destination 与 Final URL",
        "域名尽调清单",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in domain_assets:
            missing.append(f"domain_site_asset_governance.md missing phrase: {phrase}")
    if len(URL_RE.findall(domain_assets)) < 12:
        missing.append(
            "domain_site_asset_governance.md should contain at least 12 source URLs"
        )

    landing_intelligence = (
        ROOT / "docs" / "landing_offer_intelligence_creative_brief.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么素材抽取重要",
        "可抽取字段",
        "Evidence-first Creative",
        "Claim / Proof Matrix",
        "Review / Testimonial 边界",
        "表单与 Lead 风险",
        "素材抽取工作流",
        "常见事故",
        "本系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in landing_intelligence:
            missing.append(
                f"landing_offer_intelligence_creative_brief.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(landing_intelligence)) < 10:
        missing.append(
            "landing_offer_intelligence_creative_brief.md should contain at least 10 source URLs"
        )

    cashflow = (ROOT / "docs" / "cashflow_settlement_risk.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "现金流决定生死",
        "收入状态字典",
        "预算安全垫模型",
        "扣量和拒付管理",
        "月度关账流程",
        "止损触发器",
        "信息来源 URL",
    ]:
        if phrase not in cashflow:
            missing.append(f"cashflow_settlement_risk.md missing phrase: {phrase}")
    if len(URL_RE.findall(cashflow)) < 8:
        missing.append("cashflow_settlement_risk.md should contain at least 8 source URLs")

    subscription_ltv = (
        ROOT / "docs" / "subscription_refund_ltv_chargeback_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么首单 ROI 不等于真实 LTV",
        "原理解释：LTV 是收入曲线，不是固定数字",
        "核心对象地图",
        "Trial / Subscription Funnel",
        "披露、取消和退款边界",
        "LTV Cohort 模型",
        "Refund、Chargeback、Clawback 分类",
        "Subscription Quality Score",
        "与 Smart Bidding 和转化回传的关系",
        "常见事故",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "功能拆解和安全完成清单",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in subscription_ltv:
            missing.append(
                "subscription_refund_ltv_chargeback_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(subscription_ltv)) < 10:
        missing.append(
            "subscription_refund_ltv_chargeback_governance.md should contain at least 10 source URLs"
        )

    revenue_reconciliation = (ROOT / "docs" / "revenue_reconciliation_adstack.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么收入对账是套利生命线",
        "收入状态模型",
        "对账粒度",
        "AdSense 对账",
        "GAM / AdX 对账",
        "扣量复盘",
        "Click -> Session -> Revenue 对账",
        "月度关账",
        "报表字段规范",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in revenue_reconciliation:
            missing.append(f"revenue_reconciliation_adstack.md missing phrase: {phrase}")
    if len(URL_RE.findall(revenue_reconciliation)) < 12:
        missing.append("revenue_reconciliation_adstack.md should contain at least 12 source URLs")

    creative = (ROOT / "docs" / "creative_testing_optimization.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "创意输入材料",
        "Responsive Search Ads",
        "Ad Strength",
        "动态关键词插入",
        "政策和事实检查",
        "优化决策树",
        "创意 QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in creative:
            missing.append(f"creative_testing_optimization.md missing phrase: {phrase}")
    if len(URL_RE.findall(creative)) < 8:
        missing.append("creative_testing_optimization.md should contain at least 8 source URLs")

    creative_angle_library = (
        ROOT / "docs" / "creative_angle_library_feedback_loop.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Angle Library 是套利复利资产",
        "核心对象",
        "Angle 分类法",
        "素材版本规则",
        "资产表现口径",
        "反馈事件分类",
        "Angle 生命周期",
        "Prompt / Angle 回写机制",
        "版本和哈希",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in creative_angle_library:
            missing.append(
                f"creative_angle_library_feedback_loop.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(creative_angle_library)) < 14:
        missing.append(
            "creative_angle_library_feedback_loop.md should contain at least 14 source URLs"
        )

    claim_review = (ROOT / "docs" / "creative_claim_review_fact_checking.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么 Claim 审核是套利核心",
        "Claim 生命周期",
        "Claim 风险分类",
        "Evidence Map",
        "Google Ads 政策映射",
        "FTC / Review / Testimonial 边界",
        "敏感垂类 Claim",
        "RSA / AI 素材审核",
        "审核工作流",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in claim_review:
            missing.append(f"creative_claim_review_fact_checking.md missing phrase: {phrase}")
    if len(URL_RE.findall(claim_review)) < 12:
        missing.append(
            "creative_claim_review_fact_checking.md should contain at least 12 source URLs"
        )

    ad_review_appeal = (
        ROOT / "docs" / "google_ads_ad_review_disapproval_appeal_playbook.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么广告审核是套利上线闸门",
        "Google Ads 审核原理",
        "Policy Manager 的作用",
        "Destination requirements",
        "Misrepresentation",
        "Circumventing systems",
        "拒登处理流程",
        "申诉证据包模板",
        "什么时候不该申诉",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in ad_review_appeal:
            missing.append(
                "google_ads_ad_review_disapproval_appeal_playbook.md missing "
                f"phrase: {phrase}"
            )
    if len(URL_RE.findall(ad_review_appeal)) < 16:
        missing.append(
            "google_ads_ad_review_disapproval_appeal_playbook.md should contain at least 16 source URLs"
        )

    ai_prompt = (ROOT / "docs" / "ai_provider_prompt_cost_governance.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么 AI 配置是套利核心能力",
        "Provider 抽象和多模型路由",
        "Prompt 模板结构",
        "Evidence-first 输出合同",
        "Prompt Library 和 Angle Library",
        "成本控制和 ROI 口径",
        "幻觉、Prompt Injection 和数据安全",
        "创意、关键词和本地化的不同任务",
        "人审和发布闸门",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in ai_prompt:
            missing.append(f"ai_provider_prompt_cost_governance.md missing phrase: {phrase}")
    if len(URL_RE.findall(ai_prompt)) < 10:
        missing.append(
            "ai_provider_prompt_cost_governance.md should contain at least 10 source URLs"
        )

    links = (ROOT / "docs" / "link_rotation_compliance.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "链接层级",
        "合理换链接场景",
        "目的地一致性原则",
        "链接变更流程",
        "轮换和 A/B 测试",
        "事故处理",
        "信息来源 URL",
    ]:
        if phrase not in links:
            missing.append(f"link_rotation_compliance.md missing phrase: {phrase}")
    if len(URL_RE.findall(links)) < 8:
        missing.append("link_rotation_compliance.md should contain at least 8 source URLs")

    campaign_launch = (ROOT / "docs" / "campaign_launch_automation.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "投放结构的目标",
        "Google Ads 层级",
        "Campaign 拆分原则",
        "搜索词报告与否定词",
        "预算和出价",
        "Google Ads Editor CSV 流程",
        "Google Ads Scripts / API 安全自动化",
        "上线检查表",
        "信息来源 URL",
    ]:
        if phrase not in campaign_launch:
            missing.append(f"campaign_launch_automation.md missing phrase: {phrase}")
    if len(URL_RE.findall(campaign_launch)) < 10:
        missing.append("campaign_launch_automation.md should contain at least 10 source URLs")

    editor_csv_bulk = (
        ROOT / "docs" / "google_ads_editor_csv_bulk_upload_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Editor / CSV 是套利团队的安全核心",
        "ADXKit 对应点和完成形态",
        "原理解释：Editor / CSV 工作流",
        "适合 CSV / Editor 的操作",
        "CSV 字段合同",
        "版本、审批和回滚",
        "Bulk Upload 与 Editor 的区别",
        "常见事故模式",
        "上线前 QA 清单",
        "系统落地",
        "后续数据模型建议",
        "信息来源 URL",
    ]:
        if phrase not in editor_csv_bulk:
            missing.append(
                f"google_ads_editor_csv_bulk_upload_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(editor_csv_bulk)) < 14:
        missing.append(
            "google_ads_editor_csv_bulk_upload_governance.md should contain at least 14 source URLs"
        )

    scripts_automation = (ROOT / "docs" / "google_ads_scripts_safe_automation.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "Scripts 的定位",
        "Scripts vs Cookie 后台操作",
        "安全执行等级",
        "Payload 合同",
        "Bulk Upload Preview 流程",
        "审计日志要求",
        "常见错误",
        "系统落地",
        "未来扩展",
        "信息来源 URL",
    ]:
        if phrase not in scripts_automation:
            missing.append(f"google_ads_scripts_safe_automation.md missing phrase: {phrase}")
    if len(URL_RE.findall(scripts_automation)) < 10:
        missing.append("google_ads_scripts_safe_automation.md should contain at least 10 source URLs")

    scripts_data_sync = (
        ROOT / "docs" / "google_ads_scripts_data_sync_consistency.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么同步是套利系统的核心能力",
        "ADXKit 对应点和完成形态",
        "原理解释：同步不是实时真相",
        "读同步：从 Google Ads 拉什么",
        "写同步：从工作台写回什么",
        "同步频率和数据新鲜度",
        "多账号和 MCC 同步",
        "外部数据和中间存储",
        "冲突治理",
        "对账口径",
        "失败处理和重试",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in scripts_data_sync:
            missing.append(
                f"google_ads_scripts_data_sync_consistency.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(scripts_data_sync)) < 16:
        missing.append(
            "google_ads_scripts_data_sync_consistency.md should contain at least 16 source URLs"
        )

    script_template = (ROOT / "scripts" / "google_ads_script_payload_preview.js").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "PREVIEW_ONLY = true",
        "ALLOW_APPLY = false",
        "no_cookie_automation",
        "manual_review_required",
        "previewBulkUpload_",
        "upload.preview()",
    ]:
        if phrase not in script_template:
            missing.append(f"google_ads_script_payload_preview.js missing phrase: {phrase}")

    auction_bidding = (
        ROOT / "docs" / "google_ads_auction_bidding_quality_score.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "竞价不是单纯价高者得",
        "Ad Rank 和实际 CPC",
        "Quality Score 的正确用法",
        "Impression Share、Budget 和 Rank",
        "预算和 Overdelivery",
        "出价策略选择",
        "Smart Bidding 的套利风险",
        "套利出价公式",
        "Optimization Score 和 Recommendations",
        "信息来源 URL",
    ]:
        if phrase not in auction_bidding:
            missing.append(
                f"google_ads_auction_bidding_quality_score.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(auction_bidding)) < 10:
        missing.append(
            "google_ads_auction_bidding_quality_score.md should contain at least 10 source URLs"
        )

    ads_reporting = (ROOT / "docs" / "google_ads_reporting_diagnostics.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么报表诊断决定套利生死",
        "报表诊断闭环",
        "Search Terms Report",
        "Search Terms Insights 与 PMax",
        "Auction Insights",
        "Change History",
        "Report Editor 和 Segments",
        "Landing Pages Report",
        "RSA / Asset Report",
        "Bid Strategy Report",
        "异常诊断矩阵",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in ads_reporting:
            missing.append(f"google_ads_reporting_diagnostics.md missing phrase: {phrase}")
    if len(URL_RE.findall(ads_reporting)) < 12:
        missing.append(
            "google_ads_reporting_diagnostics.md should contain at least 12 source URLs"
        )

    search_automation = (
        ROOT / "docs" / "search_automation_ai_max_broad_match.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Search 自动化对套利关键",
        "核心对象",
        "AI Max for Search 的工作边界",
        "Broad Match 与 Smart Bidding",
        "Dynamic Search Ads 与页面索引风险",
        "Final URL Expansion 与 URL 控制",
        "Automatically Created Assets 与 Claim 风险",
        "Brand Controls、Negative Keywords 和 Query 治理",
        "报表和诊断",
        "实验和止损",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in search_automation:
            missing.append(
                f"search_automation_ai_max_broad_match.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(search_automation)) < 12:
        missing.append(
            "search_automation_ai_max_broad_match.md should contain at least 12 source URLs"
        )

    pmax_demand_gen = (
        ROOT / "docs" / "performance_max_demand_gen_automation.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么自动化 Campaign 对套利既有价值也危险",
        "核心对象",
        "PMax 适用与不适用场景",
        "Final URL Expansion 与 URL 控制",
        "Search Themes 和 Brand Exclusions",
        "Audience Signals 不是硬性定向",
        "Asset Groups、素材和 Claim 风险",
        "Demand Gen 的特殊风险",
        "报表和诊断",
        "实验和止损",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in pmax_demand_gen:
            missing.append(
                f"performance_max_demand_gen_automation.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(pmax_demand_gen)) < 12:
        missing.append(
            "performance_max_demand_gen_automation.md should contain at least 12 source URLs"
        )

    geo_localization = (ROOT / "docs" / "geo_language_localization_currency.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么 Geo / Language 是套利核心变量",
        "核心对象",
        "Location Targeting 和 Presence / Interest",
        "Language Targeting 与页面本地化",
        "Device 分层",
        "时区、Dayparting 和回传延迟",
        "币种、汇率和 ROI",
        "Geo 扩量流程",
        "Bad Geo 诊断",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in geo_localization:
            missing.append(f"geo_language_localization_currency.md missing phrase: {phrase}")
    if len(URL_RE.findall(geo_localization)) < 10:
        missing.append(
            "geo_language_localization_currency.md should contain at least 10 source URLs"
        )

    budget_pacing = (ROOT / "docs" / "budget_pacing_scaling_stoploss.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么预算节奏是套利核心",
        "预算层级",
        "测试预算公式",
        "Pacing 规则",
        "放量阶梯",
        "Dayparting 和时段控制",
        "Geo / Device 分层",
        "Bid Adjustment 和预算联动",
        "回传延迟和判断窗口",
        "Stop-loss 触发器",
        "Portfolio 资金分配",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in budget_pacing:
            missing.append(f"budget_pacing_scaling_stoploss.md missing phrase: {phrase}")
    if len(URL_RE.findall(budget_pacing)) < 10:
        missing.append("budget_pacing_scaling_stoploss.md should contain at least 10 source URLs")

    portfolio_allocation = (
        ROOT / "docs" / "portfolio_budget_allocation_risk_concentration.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Portfolio 治理是套利生存问题",
        "原理解释",
        "核心对象地图",
        "组合分层：Core、Scale、Test、Explore、Quarantine",
        "风险预算模型",
        "集中度限制",
        "相关性风险",
        "Revenue Status Mix",
        "Allocation Score",
        "组合扩量规则",
        "组合降风险和退出规则",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in portfolio_allocation:
            missing.append(
                f"portfolio_budget_allocation_risk_concentration.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(portfolio_allocation)) < 12:
        missing.append(
            "portfolio_budget_allocation_risk_concentration.md should contain at least 12 source URLs"
        )

    account_governance = (
        ROOT / "docs" / "account_mcc_billing_verification_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么账号治理是套利核心",
        "核心对象",
        "MCC 是治理工具，不是账号池",
        "访问权限和最小权限",
        "付款资料、账单与 Account Budget",
        "Advertiser Verification 与业务操作验证",
        "代理关系和客户管理",
        "账号结构与业务隔离",
        "账号事件和证据包",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in account_governance:
            missing.append(
                f"account_mcc_billing_verification_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(account_governance)) < 10:
        missing.append(
            "account_mcc_billing_verification_governance.md should contain at least 10 source URLs"
        )

    account_health = (ROOT / "docs" / "policy_account_health_sop.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "常见状态字典",
        "事件分级",
        "Google Ads 拒登处理流程",
        "Google Ads 账号暂停处理",
        "Advertiser Verification SOP",
        "AdSense Policy Center SOP",
        "无效流量和扣量响应",
        "证据包模板",
        "申诉质量评分",
        "信息来源 URL",
    ]:
        if phrase not in account_health:
            missing.append(f"policy_account_health_sop.md missing phrase: {phrase}")
    if len(URL_RE.findall(account_health)) < 10:
        missing.append("policy_account_health_sop.md should contain at least 10 source URLs")

    adsense_site_approval = (
        ROOT / "docs" / "adsense_site_approval_policy_center.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么站点审核决定收入起点",
        "核心状态",
        "站点连接与审核流程",
        "站点 Ready 不是只看文章数量",
        "Policy Center 状态",
        "Ad Serving Limits",
        "购买流量责任",
        "恢复和 Review 流程",
        "常见事故",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in adsense_site_approval:
            missing.append(
                f"adsense_site_approval_policy_center.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(adsense_site_approval)) < 12:
        missing.append(
            "adsense_site_approval_policy_center.md should contain at least 12 source URLs"
        )

    publisher_stack = (ROOT / "docs" / "publisher_monetization_stack.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "产品层级",
        "核心概念",
        "Auto ads 与手动广告单元",
        "广告位策略",
        "AdSense / AdX / GAM 指标对账",
        "可见率和延迟",
        "发布商风险红线",
        "变现实验流程",
        "信息来源 URL",
    ]:
        if phrase not in publisher_stack:
            missing.append(f"publisher_monetization_stack.md missing phrase: {phrase}")
    if len(URL_RE.findall(publisher_stack)) < 10:
        missing.append("publisher_monetization_stack.md should contain at least 10 source URLs")

    ad_quality = (
        ROOT / "docs" / "publisher_ad_quality_blocking_controls.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么广告质量影响套利",
        "核心对象",
        "Blocking Controls 的收入权衡",
        "Ad Review Center 工作流",
        "General / Sensitive Categories",
        "竞品广告和品牌安全",
        "低质广告、诈骗和恶意广告处理",
        "Ad Manager Protections 和高级场景",
        "监控指标",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in ad_quality:
            missing.append(f"publisher_ad_quality_blocking_controls.md missing phrase: {phrase}")
    if len(URL_RE.findall(ad_quality)) < 10:
        missing.append(
            "publisher_ad_quality_blocking_controls.md should contain at least 10 source URLs"
        )

    supply_chain = (
        ROOT / "docs" / "programmatic_supply_chain_transparency.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么供应链透明度影响套利",
        "核心对象",
        "ads.txt 原理和 QA",
        "sellers.json 原理和 QA",
        "schain / SupplyChain Object",
        "DIRECT、RESELLER、MCM 和套利团队边界",
        "对套利模型的影响",
        "QA 工作流",
        "常见事故",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in supply_chain:
            missing.append(f"programmatic_supply_chain_transparency.md missing phrase: {phrase}")
    if len(URL_RE.findall(supply_chain)) < 10:
        missing.append(
            "programmatic_supply_chain_transparency.md should contain at least 10 source URLs"
        )

    gam_yield = (ROOT / "docs" / "gam_adx_yield_floor_pricing.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么 Yield 决定收入上限",
        "核心对象",
        "Floor Price 不是越高越好",
        "Unified Pricing Rules",
        "Dynamic Allocation 和 Line Item Priority",
        "Open Bidding / Header Bidding 边界",
        "Yield 实验设计",
        "Floor 调整决策树",
        "常见事故",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in gam_yield:
            missing.append(f"gam_adx_yield_floor_pricing.md missing phrase: {phrase}")
    if len(URL_RE.findall(gam_yield)) < 10:
        missing.append(
            "gam_adx_yield_floor_pricing.md should contain at least 10 source URLs"
        )

    header_bidding = (ROOT / "docs" / "header_bidding_prebid_ad_stack.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么 Header Bidding 影响套利收入",
        "核心链路",
        "Prebid.js 与 GAM 的协作",
        "Price Granularity 和 Line Item",
        "Auction Timeout、延迟和页面体验",
        "Floor、竞价密度和 Fill",
        "Consent、User ID 与隐私边界",
        "ads.txt、sellers.json 与 schain",
        "调试和对账",
        "常见事故",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in header_bidding:
            missing.append(f"header_bidding_prebid_ad_stack.md missing phrase: {phrase}")
    if len(URL_RE.findall(header_bidding)) < 12:
        missing.append(
            "header_bidding_prebid_ad_stack.md should contain at least 12 source URLs"
        )

    ad_placement = (ROOT / "docs" / "ad_placement_refresh_viewability.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么广告位优化是套利核心",
        "指标漏斗",
        "广告位设计原则",
        "Ad refresh 边界",
        "Viewability 与 Active View",
        "Lazy loading 与页面体验",
        "Auto ads 与手动广告单元实验",
        "异常复盘",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in ad_placement:
            missing.append(f"ad_placement_refresh_viewability.md missing phrase: {phrase}")
    if len(URL_RE.findall(ad_placement)) < 12:
        missing.append(
            "ad_placement_refresh_viewability.md should contain at least 12 source URLs"
        )

    privacy_consent = (ROOT / "docs" / "privacy_consent_tracking.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "数据分类",
        "Consent Mode 基础",
        "CMP、TCF 和发布商产品",
        "Google Ads 与 GA4 测量",
        "UTM、Click ID 与 Postback",
        "隐私政策和页面披露",
        "常见事故",
        "上线检查表",
        "信息来源 URL",
    ]:
        if phrase not in privacy_consent:
            missing.append(f"privacy_consent_tracking.md missing phrase: {phrase}")
    if len(URL_RE.findall(privacy_consent)) < 10:
        missing.append("privacy_consent_tracking.md should contain at least 10 source URLs")

    business_models = (ROOT / "docs" / "ads_arbitrage_business_models.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "总体分类",
        "内容/展示广告套利",
        "搜索套利",
        "联盟 / CPA / CPL 套利",
        "垂直内容站套利",
        "域名 / Parking / Feed 模式",
        "流量转售和低质中转",
        "模式选择评分",
        "决策树",
        "信息来源 URL",
    ]:
        if phrase not in business_models:
            missing.append(f"ads_arbitrage_business_models.md missing phrase: {phrase}")
    if len(URL_RE.findall(business_models)) < 10:
        missing.append("ads_arbitrage_business_models.md should contain at least 10 source URLs")

    search_feed = (ROOT / "docs" / "search_arbitrage_feed_parking.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "模式定义",
        "Search feed / AFS / CSA",
        "Parking / Parked domain",
        "经济模型",
        "Search ads 政策要点",
        "Google Ads 买量到搜索页的风险",
        "Query Intent 和结果页质量",
        "流量来源准入",
        "测试和放量 SOP",
        "信息来源 URL",
    ]:
        if phrase not in search_feed:
            missing.append(f"search_arbitrage_feed_parking.md missing phrase: {phrase}")
    if len(URL_RE.findall(search_feed)) < 10:
        missing.append("search_arbitrage_feed_parking.md should contain at least 10 source URLs")

    rsoc_n2s = (
        ROOT / "docs" / "rsoc_n2s_search_feed_partner_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 RSOC / N2S 是套利核心模式",
        "核心术语",
        "官方政策边界",
        "上游流量、RAC 和创意一致性",
        "Content Page 不是桥页",
        "Search Results Page 和 Query Intent",
        "Feed Partner 尽调",
        "经济模型和扣量",
        "常见事故诊断",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in rsoc_n2s:
            missing.append(
                f"rsoc_n2s_search_feed_partner_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(rsoc_n2s)) < 12:
        missing.append(
            "rsoc_n2s_search_feed_partner_governance.md should contain at least 12 source URLs"
        )

    keyword_intent = (ROOT / "docs" / "keyword_intent_research.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "意图分层",
        "Keyword Planner 工作流",
        "Google Trends 用法",
        "Match Type 策略",
        "搜索词报告",
        "否定词体系",
        "页面选题矩阵",
        "政策和敏感词筛查",
        "测试优先级评分",
        "信息来源 URL",
    ]:
        if phrase not in keyword_intent:
            missing.append(f"keyword_intent_research.md missing phrase: {phrase}")
    if len(URL_RE.findall(keyword_intent)) < 10:
        missing.append("keyword_intent_research.md should contain at least 10 source URLs")

    seasonality = (
        ROOT / "docs" / "seasonality_event_demand_forecasting.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么季节性是套利利润窗口",
        "原理解释",
        "核心对象地图",
        "信息来源地图",
        "事件日历构建",
        "Demand Score 模型",
        "Vertical Calendar 示例",
        "Keyword Planner、Trends 和 Insights 的组合用法",
        "Budget Ramp 和 Exit Rules",
        "Smart Bidding Seasonality Adjustment 边界",
        "内容、创意和审核节奏",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in seasonality:
            missing.append(
                f"seasonality_event_demand_forecasting.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(seasonality)) < 14:
        missing.append(
            "seasonality_event_demand_forecasting.md should contain at least 14 source URLs"
        )

    search_terms_mining = (
        ROOT / "docs" / "search_terms_negative_keyword_query_mining.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Search Terms 是 Search 套利的真相层",
        "Search Term vs Keyword",
        "Match Type 和 Query Drift",
        "Search Terms Report 工作流",
        "Query 决策矩阵",
        "否定词体系",
        "Query Promotion",
        "Query Sculpting 和拆组",
        "Search Terms Insights 与隐私聚合",
        "PMax、AI Max、Broad 和 DSA 场景",
        "政策和品牌边界",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in search_terms_mining:
            missing.append(
                "search_terms_negative_keyword_query_mining.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(search_terms_mining)) < 16:
        missing.append(
            "search_terms_negative_keyword_query_mining.md should contain at least 16 source URLs"
        )

    brand_trademark = (
        ROOT / "docs" / "brand_bidding_trademark_competitor_policy.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "概念分层",
        "四层规则模型",
        "Google Ads 商标政策要点",
        "Offer 条款比平台政策更细",
        "竞品投放的合规边界",
        "Misrepresentation 和冒充风险",
        "Counterfeit 和仿牌边界",
        "关键词准入和否定词",
        "证据包",
        "信息来源 URL",
    ]:
        if phrase not in brand_trademark:
            missing.append(f"brand_bidding_trademark_competitor_policy.md missing phrase: {phrase}")
    if len(URL_RE.findall(brand_trademark)) < 10:
        missing.append(
            "brand_bidding_trademark_competitor_policy.md should contain at least 10 source URLs"
        )

    competitor_intelligence = (
        ROOT / "docs" / "competitor_ad_intelligence_serp_transparency.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么竞品广告情报是套利前置能力",
        "可用来源地图",
        "Ads Transparency Center 用法",
        "Ad Preview and Diagnosis 用法",
        "Auction Insights 解读",
        "SERP 采样和市场地图",
        "竞品素材拆解方法",
        "品牌和商标边界",
        "情报到创意和页面 brief",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in competitor_intelligence:
            missing.append(
                "competitor_ad_intelligence_serp_transparency.md missing "
                f"phrase: {phrase}"
            )
    if len(URL_RE.findall(competitor_intelligence)) < 14:
        missing.append(
            "competitor_ad_intelligence_serp_transparency.md should contain at least 14 source URLs"
        )

    traffic_vendor = (
        ROOT / "docs" / "traffic_channel_vendor_due_diligence.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "渠道分层",
        "Google Search",
        "Search Partners",
        "Display / Demand Gen",
        "Performance Max",
        "Native / Content Discovery",
        "流量供应商尽调表",
        "小预算测试流程",
        "信息来源 URL",
    ]:
        if phrase not in traffic_vendor:
            missing.append(f"traffic_channel_vendor_due_diligence.md missing phrase: {phrase}")
    if len(URL_RE.findall(traffic_vendor)) < 10:
        missing.append("traffic_channel_vendor_due_diligence.md should contain at least 10 source URLs")

    inventory_controls = (ROOT / "docs" / "traffic_inventory_controls.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "为什么库存控制重要",
        "Google Ads 库存分层",
        "Search Partners 控制",
        "Display、YouTube 与 Demand Gen",
        "Performance Max 库存控制",
        "Final URL Expansion 和 URL 控制",
        "Content Suitability 和 Placement Exclusions",
        "报表和诊断",
        "库存实验设计",
        "信息来源 URL",
    ]:
        if phrase not in inventory_controls:
            missing.append(f"traffic_inventory_controls.md missing phrase: {phrase}")
    if len(URL_RE.findall(inventory_controls)) < 10:
        missing.append("traffic_inventory_controls.md should contain at least 10 source URLs")

    source_quality = (
        ROOT / "docs" / "source_publisher_placement_quality_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么来源质量评分是套利放量闸门",
        "原理解释",
        "核心对象地图",
        "来源分层",
        "质量指标",
        "Source Quality Score 模型",
        "名单体系",
        "Placement / Publisher 诊断",
        "SubID 和 buyer feedback 闭环",
        "停源、恢复和复测流程",
        "与 Google Ads 控制对应",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in source_quality:
            missing.append(
                f"source_publisher_placement_quality_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(source_quality)) < 16:
        missing.append(
            "source_publisher_placement_quality_governance.md should contain at least 16 source URLs"
        )

    vendor_contracts = (
        ROOT / "docs" / "traffic_vendor_contract_io_dispute_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么合同和 IO 是套利风控资产",
        "原理解释",
        "核心对象地图",
        "合作类型和条款重点",
        "IO 必备条款",
        "Tracking Appendix 和 Reporting Appendix",
        "质量条款和禁止流量",
        "报表差异和口径",
        "Refund、Credit 和 Makegood",
        "争议处理流程",
        "供应商评分和合同状态",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in vendor_contracts:
            missing.append(
                f"traffic_vendor_contract_io_dispute_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(vendor_contracts)) < 14:
        missing.append(
            "traffic_vendor_contract_io_dispute_governance.md should contain at least 14 source URLs"
        )

    audience_remarketing = (
        ROOT / "docs" / "audience_remarketing_customer_match_policy.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么受众控制重要",
        "Audience Segment 基础",
        "Targeting、Observation、Signals 和 Expansion",
        "Remarketing / Your Data Segments",
        "Customer Match",
        "Personalized Ads 敏感类别",
        "PMax Audience Signals",
        "Optimized Targeting 和扩量风险",
        "套利场景风险清单",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in audience_remarketing:
            missing.append(
                f"audience_remarketing_customer_match_policy.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(audience_remarketing)) < 10:
        missing.append(
            "audience_remarketing_customer_match_policy.md should contain at least 10 source URLs"
        )

    affiliate_due = (ROOT / "docs" / "affiliate_network_due_diligence.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "合作对象分层",
        "Offer 条款清单",
        "流量限制解读",
        "Payout、Cap 和 Scrub",
        "Lead Quality",
        "Affiliate Disclosure",
        "网络 / 广告主尽调问题",
        "合同和邮件确认模板",
        "测试和放量规则",
        "信息来源 URL",
    ]:
        if phrase not in affiliate_due:
            missing.append(f"affiliate_network_due_diligence.md missing phrase: {phrase}")
    if len(URL_RE.findall(affiliate_due)) < 10:
        missing.append("affiliate_network_due_diligence.md should contain at least 10 source URLs")

    lead_buyer_contracts = (
        ROOT / "docs" / "lead_buyer_contract_io_paid_definition_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Buyer 合同口径决定 CPL 盈亏",
        "原理解释：接收、合格、可计费、已付款是四个不同事件",
        "核心对象地图",
        "Lead 状态机和定义",
        "合同和 IO 必填条款",
        "Accepted 规则和初始拒收",
        "Qualified 和 Billable 定义",
        "Return Window、Scrub 和 Clawback",
        "Pricing Model 和优化目标",
        "Exclusive、Shared、Aged 和 Recycled Lead",
        "Postback、Reporting 和 Invoice 对账",
        "Dispute Evidence 和扣量争议流程",
        "Google Ads 与转化信号边界",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in lead_buyer_contracts:
            missing.append(
                "lead_buyer_contract_io_paid_definition_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(lead_buyer_contracts)) < 14:
        missing.append(
            "lead_buyer_contract_io_paid_definition_governance.md should "
            "contain at least 14 source URLs"
        )

    lead_quality = (
        ROOT / "docs" / "lead_quality_postback_reconciliation.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Lead 质量是套利核心",
        "Lead 链路全流程",
        "线索质量分层",
        "Postback 和对账原理",
        "拒付和 Scrub 原因",
        "Buyer Feedback 闭环",
        "表单、隐私和披露",
        "质量防线",
        "决策阈值",
        "信息来源 URL",
    ]:
        if phrase not in lead_quality:
            missing.append(f"lead_quality_postback_reconciliation.md missing phrase: {phrase}")
    if len(URL_RE.findall(lead_quality)) < 10:
        missing.append("lead_quality_postback_reconciliation.md should contain at least 10 source URLs")

    lead_call_tracking = (
        ROOT / "docs" / "lead_form_call_tracking_tcpa_compliance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么电话和表单 Lead 是套利高风险资产",
        "核心对象",
        "Google Ads Lead Form 与网站表单",
        "电话线索和 Call Tracking",
        "Consent to Contact、TCPA 和 DNC",
        "Call Recording 与披露",
        "表单字段、验证和数据最小化",
        "Buyer Handoff、Ping/Post 和 CRM 状态",
        "质量、拒付和投诉诊断",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in lead_call_tracking:
            missing.append(
                f"lead_form_call_tracking_tcpa_compliance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(lead_call_tracking)) < 12:
        missing.append(
            "lead_form_call_tracking_tcpa_compliance.md should contain at least 12 source URLs"
        )

    call_tracking_attribution = (
        ROOT / "docs" / "call_tracking_dni_number_pool_attribution_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么电话归因是套利利润层",
        "原理解释：DNI 是号码到会话的映射",
        "核心对象地图",
        "Google Forwarding Number vs 第三方号码池",
        "Number Pool 容量和分配规则",
        "Call Log Join Key",
        "Call Disposition Taxonomy",
        "IVR、转接链和 Missed Call",
        "Call Recording、PII 和合规边界",
        "Google Ads Call Conversion Mapping",
        "Call Attribution Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in call_tracking_attribution:
            missing.append(
                "call_tracking_dni_number_pool_attribution_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(call_tracking_attribution)) < 18:
        missing.append(
            "call_tracking_dni_number_pool_attribution_governance.md should "
            "contain at least 18 source URLs"
        )

    pay_per_call = (
        ROOT / "docs" / "pay_per_call_buyer_routing_duration_payout_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Pay-per-call 不是 Call Count 套利",
        "原理解释：Duration 是代理指标",
        "核心对象地图",
        "Call Routing 模式",
        "Buyer / Target 条款",
        "Duration Payout 和 Scrub",
        "Duplicate Caller 和 Repeat Call",
        "IVR、Call Flow 和 Caller Experience",
        "Recording、Compliance 和 Suppression",
        "Google Ads 与 Pay-per-call 信号",
        "Call Buyer Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in pay_per_call:
            missing.append(
                "pay_per_call_buyer_routing_duration_payout_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(pay_per_call)) < 16:
        missing.append(
            "pay_per_call_buyer_routing_duration_payout_governance.md should "
            "contain at least 16 source URLs"
        )

    consent_proof = (
        ROOT / "docs" / "lead_consent_proof_certificate_evidence_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Consent Proof 是 CPL 收款资产",
        "原理解释：证据链证明的是页面上下文",
        "核心对象地图",
        "TrustedForm / Jornaya 类证据",
        "Consent Certificate 生命周期",
        "字段和哈希",
        "Buyer 交接和 Ping/Post 边界",
        "DNC、Opt-out、撤回同意和投诉",
        "争议证据包",
        "Consent Proof Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in consent_proof:
            missing.append(
                "lead_consent_proof_certificate_evidence_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(consent_proof)) < 16:
        missing.append(
            "lead_consent_proof_certificate_evidence_governance.md should "
            "contain at least 16 source URLs"
        )

    lead_form_funnel = (
        ROOT / "docs" / "lead_form_funnel_qualification_ux.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么表单漏斗决定 CPL 盈亏",
        "原理解释：摩擦、意图和质量的取舍",
        "核心对象地图",
        "单步表单 vs 分步表单",
        "字段分层和用途说明",
        "资格问题设计",
        "披露、Consent 和 CTA 位置",
        "移动端 UX 和可访问性",
        "Form Versioning 和实验设计",
        "Abandon、Error 和 Low Intent 诊断",
        "表单质量评分",
        "Google Ads 与转化信号边界",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in lead_form_funnel:
            missing.append(
                f"lead_form_funnel_qualification_ux.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(lead_form_funnel)) < 14:
        missing.append(
            "lead_form_funnel_qualification_ux.md should contain at least 14 source URLs"
        )

    ping_post_leads = (
        ROOT / "docs" / "ping_post_lead_marketplace_buyer_routing.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Ping/Post 和 Buyer Routing 是 CPL 套利核心",
        "原理解释：Lead Marketplace 不是简单表单转发",
        "核心对象地图",
        "Direct Post vs Ping/Post",
        "Ping 字段和数据最小化",
        "Post、Buyer Accept 和 Reject",
        "Exclusive / Shared / Aged Lead 边界",
        "Buyer Routing：waterfall、auction、priority、cap、bid",
        "Lead Cap、Buyer Capacity 和 No Buyer 风险",
        "Consent、Disclosure、TCPA、DNC 和数据分享",
        "Payout Selection 和 Effective EPC",
        "Buyer Feedback 闭环",
        "Routing Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in ping_post_leads:
            missing.append(
                f"ping_post_lead_marketplace_buyer_routing.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(ping_post_leads)) < 16:
        missing.append(
            "ping_post_lead_marketplace_buyer_routing.md should contain at least 16 source URLs"
        )

    lead_freshness = (
        ROOT / "docs" / "lead_freshness_aged_recontact_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Lead Freshness 决定 CPL 盈亏",
        "原理解释：意图衰减不能靠补触达修复",
        "核心对象地图",
        "Lead Age 分桶",
        "Fresh、Exclusive、Shared、Aged、Recycled 的差异",
        "Buyer Terms 和 Payout Tier",
        "Recontact Window 和频控",
        "Consent Refresh 和证据链",
        "Google Ads 与转化信号边界",
        "Freshness Quality Score",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in lead_freshness:
            missing.append(
                "lead_freshness_aged_recontact_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(lead_freshness)) < 18:
        missing.append(
            "lead_freshness_aged_recontact_governance.md should "
            "contain at least 18 source URLs"
        )

    lead_validation = (
        ROOT / "docs" / "lead_validation_suppression_pii_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Lead Validation / Suppression 是套利核心",
        "原理解释：验证不是造假",
        "数据分类与 PII 最小化",
        "Validation Pipeline",
        "Phone / Email / Address / Geo 校验",
        "Duplicate、Householding 与跨 Buyer 去重",
        "Suppression、DNC、Opt-out 与撤回同意",
        "Data Broker、数据转售和用户权利",
        "Retention、Deletion、Disposal 和访问控制",
        "Lead Validation Score",
        "Buyer Reject Reason 到修复动作",
        "Google Ads 与出价信号边界",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in lead_validation:
            missing.append(
                f"lead_validation_suppression_pii_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(lead_validation)) < 18:
        missing.append(
            "lead_validation_suppression_pii_governance.md should contain at least 18 source URLs"
        )

    lead_contact_sla = (
        ROOT / "docs" / "speed_to_lead_contact_sla_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Speed-to-Lead 是 CPL 利润核心",
        "原理解释：联系治理不是骚扰或造假",
        "核心对象地图",
        "Contact Funnel 和状态机",
        "SLA 类型",
        "Contact Cadence 和频控",
        "Operating Hours、时区和预算 Pacing",
        "Call Tracking、Call Reporting 和 Call Conversion",
        "Call Center Capacity 和 Buyer Capacity",
        "Disposition Taxonomy",
        "Recording、QA 和 AI 质检边界",
        "Contact Quality Score",
        "常见事故和修复",
        "Google Ads 与出价信号边界",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in lead_contact_sla:
            missing.append(
                f"speed_to_lead_contact_sla_governance.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(lead_contact_sla)) < 14:
        missing.append(
            "speed_to_lead_contact_sla_governance.md should contain at least 14 source URLs"
        )

    experiment_design = (ROOT / "docs" / "experiment_design_optimization.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "测试假设模板",
        "测试单元",
        "样本量和最小预算",
        "显著性和实际意义",
        "回传延迟和收入延迟",
        "实验分流",
        "优化动作分级",
        "停量、保留、扩量规则",
        "复盘口径",
        "信息来源 URL",
    ]:
        if phrase not in experiment_design:
            missing.append(f"experiment_design_optimization.md missing phrase: {phrase}")
    if len(URL_RE.findall(experiment_design)) < 10:
        missing.append("experiment_design_optimization.md should contain at least 10 source URLs")

    invalid_traffic_sop = (ROOT / "docs" / "invalid_traffic_detection_sop.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "无效流量的两面",
        "核心监控指标",
        "异常信号分级",
        "来源隔离",
        "检测流程",
        "异常来源处理",
        "供应商黑名单条件",
        "Google Ads invalid clicks",
        "AdSense / AdX invalid traffic",
        "信息来源 URL",
    ]:
        if phrase not in invalid_traffic_sop:
            missing.append(f"invalid_traffic_detection_sop.md missing phrase: {phrase}")
    if len(URL_RE.findall(invalid_traffic_sop)) < 10:
        missing.append("invalid_traffic_detection_sop.md should contain at least 10 source URLs")

    anomaly_alerting = (
        ROOT / "docs" / "anomaly_monitoring_alerting_stoploss_incident_triage.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么异常监控是套利生命线",
        "监控对象地图",
        "告警分级",
        "指标异常规则",
        "时间窗口和回传延迟",
        "数据源和证据包",
        "止损队列",
        "事故分诊流程",
        "常见异常和诊断矩阵",
        "告警规则设计原则",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in anomaly_alerting:
            missing.append(
                "anomaly_monitoring_alerting_stoploss_incident_triage.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(anomaly_alerting)) < 18:
        missing.append(
            "anomaly_monitoring_alerting_stoploss_incident_triage.md should contain at least 18 source URLs"
        )

    content_quality = (
        ROOT / "docs" / "content_production_editorial_quality.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "编辑系统 vs 内容工厂",
        "页面 Brief 模板",
        "内容类型和质量标准",
        "事实核查和来源",
        "E-E-A-T 和可信度",
        "AI 辅助内容边界",
        "披露、作者和更新",
        "页面 QA 清单",
        "内容复盘",
        "信息来源 URL",
    ]:
        if phrase not in content_quality:
            missing.append(f"content_production_editorial_quality.md missing phrase: {phrase}")
    if len(URL_RE.findall(content_quality)) < 10:
        missing.append("content_production_editorial_quality.md should contain at least 10 source URLs")

    sensitive_verticals = (
        ROOT / "docs" / "sensitive_vertical_policy_playbook.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "准入原则",
        "垂类风险分层",
        "金融、信贷和债务",
        "医疗、健康和药品",
        "博彩、游戏和抽奖",
        "住房、就业、信贷 Personalized Ads",
        "政府文件、官方服务和公共服务",
        "第三方技术支持",
        "准入评分",
        "信息来源 URL",
    ]:
        if phrase not in sensitive_verticals:
            missing.append(f"sensitive_vertical_policy_playbook.md missing phrase: {phrase}")
    if len(URL_RE.findall(sensitive_verticals)) < 10:
        missing.append("sensitive_vertical_policy_playbook.md should contain at least 10 source URLs")

    task_orchestration = (
        ROOT / "docs" / "task_orchestration_approval_audit_runbook.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么任务编排是套利风控核心",
        "ADXKit 对应点和安全完成形态",
        "原理解释：一个安全任务由哪些对象组成",
        "任务分级",
        "审批原则",
        "Google Ads 安全执行通道",
        "执行日志字段",
        "幂等、重试和去重",
        "事故响应流程",
        "禁止任务语义",
        "系统落地",
        "QA 清单",
        "信息来源 URL",
    ]:
        if phrase not in task_orchestration:
            missing.append(
                f"task_orchestration_approval_audit_runbook.md missing phrase: {phrase}"
            )
    if len(URL_RE.findall(task_orchestration)) < 14:
        missing.append(
            "task_orchestration_approval_audit_runbook.md should contain at least 14 source URLs"
        )

    recommendations_experiments = (
        ROOT
        / "docs"
        / "google_ads_recommendations_experiments_auto_apply_governance.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "为什么 Recommendations 不能直接等于套利优化",
        "核心对象",
        "推荐类型拆解",
        "Auto-apply 治理",
        "建议评审矩阵",
        "Experiments 原理和套利用法",
        "实验设计流程",
        "平台建议到内部优化动作的转换",
        "Change History 和事故复盘",
        "系统落地",
        "ADXKit 对应点和完成形态",
        "信息来源 URL",
    ]:
        if phrase not in recommendations_experiments:
            missing.append(
                "google_ads_recommendations_experiments_auto_apply_governance.md "
                f"missing phrase: {phrase}"
            )
    if len(URL_RE.findall(recommendations_experiments)) < 16:
        missing.append(
            "google_ads_recommendations_experiments_auto_apply_governance.md should contain at least 16 source URLs"
        )

    if missing:
        print("Research doc verification failed:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)

    print("Research doc verification passed.")


if __name__ == "__main__":
    main()
