# Ads Arbitrage Workbench

这是一个围绕 Google Ads / AdSense / AdX 流量套利业务的单团队工作台草案与实现。当前优先级是行业知识、流程拆解和风控边界，其次才是系统实现。

重要边界：

高风险能力不是简单“不复刻”。本项目把它们复刻为行业知识、原理解释、平台规则、风险识别、审计字段、SOP、来源 URL 和安全替代流程；不交付会话接管、绕过安全、刷量、cloaking、规避关联或规避封禁等执行型对抗能力。

- Google Ads Cookie 复用、Cookie 注入、绕过 2FA、安全挑战或审核系统：以原理、风险、替代流程和审计模板形式完成，不交付会话接管或绕过实现。
- 补点击、刷量、虚假曝光、流量伪装、cloaking、规避关联检测：以行业知识、识别逻辑、来源 URL 和合规替代方案形式完成，不交付会造成无效流量或绕过平台规则的执行能力。
- 系统默认采用可审计的导入、导出、Google Ads Scripts、人工审核和任务编排方式。
- 第一版不做多租户，按单团队/单工作台设计。

## 快速运行

开发环境可直接使用 SQLite：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask --app app db-init
flask --app app seed
flask --app app run --debug --port 5058
```

使用 MySQL 时先启动数据库并复制配置样例：

```bash
docker compose up -d mysql
copy .env.example .env
flask --app app db-init
flask --app app seed
flask --app app run --debug --port 5058
```

`.env.example` 只包含 Flask 和 MySQL 连接配置，不包含 Google Ads Cookie、代理池、浏览器指纹、账号池或任何后台接管凭据。

## 验证命令

```bash
python -m compileall adsworkbench app.py scripts
python scripts/verify_research_docs.py
python scripts/smoke_test.py
python scripts/acceptance_audit.py
flask --app app seed
```

## 文档

- [文档入口和验收导航](docs/docs_index.md)
- [Ads 套利行业知识库](docs/ads_arbitrage_industry.md)
- [Ads 套利业务模式拆解手册](docs/ads_arbitrage_business_models.md)
- [Ads 套利运营手册](docs/ads_arbitrage_operations.md)
- [Ads 套利来源证据矩阵](docs/ads_arbitrage_source_evidence_matrix.md)
- [Search Arbitrage、Feed 与 Parking 模式手册](docs/search_arbitrage_feed_parking.md)
- [RSOC / N2S、Search Feed Partner 与相关搜索套利治理手册](docs/rsoc_n2s_search_feed_partner_governance.md)
- [关键词、搜索意图与选题研究手册](docs/keyword_intent_research.md)
- [季节性、事件日历与需求预测手册](docs/seasonality_event_demand_forecasting.md)
- [Search Terms、否定词与 Query Mining 治理手册](docs/search_terms_negative_keyword_query_mining.md)；系统入口 `/query-mining` 已实现 Query Mining Score、否定词/加词建议、状态流和审计日志
- [品牌词、商标与竞品投放合规手册](docs/brand_bidding_trademark_competitor_policy.md)
- [竞品广告、SERP 与 Ads Transparency 情报手册](docs/competitor_ad_intelligence_serp_transparency.md)
- [买量渠道与流量供应商尽调手册](docs/traffic_channel_vendor_due_diligence.md)
- [Google Ads 流量库存、版位与排除控制手册](docs/traffic_inventory_controls.md)
- [Source、Publisher、Placement 质量评分与名单治理手册](docs/source_publisher_placement_quality_governance.md)
- [流量供应商合同、IO、退款与争议治理手册](docs/traffic_vendor_contract_io_dispute_governance.md)；系统入口 `/vendor-contracts` 已实现 Vendor Contract Score、amount_at_risk、争议状态流和审计日志
- [受众定向、再营销与 Customer Match 合规手册](docs/audience_remarketing_customer_match_policy.md)
- [Affiliate Network / Lead Buyer 尽调与条款手册](docs/affiliate_network_due_diligence.md)
- [Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](docs/lead_buyer_contract_io_paid_definition_governance.md)
- [Lead 质量、Postback 对账与拒付管理手册](docs/lead_quality_postback_reconciliation.md)
- [Lead Form、电话线索、Call Tracking 与 TCPA 风险手册](docs/lead_form_call_tracking_tcpa_compliance.md)
- [Call Tracking Number Pool、DNI 与电话归因治理手册](docs/call_tracking_dni_number_pool_attribution_governance.md)
- [Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](docs/pay_per_call_buyer_routing_duration_payout_governance.md)
- [Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](docs/lead_consent_proof_certificate_evidence_governance.md)
- [Lead Form 漏斗、资格问题与移动端 UX 治理手册](docs/lead_form_funnel_qualification_ux.md)
- [Ping/Post、Lead Buyer Routing 与线索市场治理手册](docs/ping_post_lead_marketplace_buyer_routing.md)；系统入口 `/ping-post-routing` 已实现 consent/disclosure、字段最小化、PII、suppression/DNC、cap snapshot、fallback、buyer feedback、expected payable value、safe CPL、阻塞项和状态审计
- [Lead Freshness、Aged Lead 与 Recontact Window 治理手册](docs/lead_freshness_aged_recontact_governance.md)
- [Lead 验证、Suppression、去重与 PII 治理手册](docs/lead_validation_suppression_pii_governance.md)
- [Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](docs/speed_to_lead_contact_sla_governance.md)
- [实验设计、样本量与优化决策手册](docs/experiment_design_optimization.md)
- [无效流量识别、异常监控与来源隔离 SOP](docs/invalid_traffic_detection_sop.md)
- [异常监控、告警、止损队列与事故分诊手册](docs/anomaly_monitoring_alerting_stoploss_incident_triage.md)
- [内容生产、页面可信度与编辑质量手册](docs/content_production_editorial_quality.md)
- [敏感垂类政策与 Offer 准入手册](docs/sensitive_vertical_policy_playbook.md)
- [Ads 套利指标字典与口径](docs/metric_dictionary.md)
- [单位经济模型、Break-even 与安全边际手册](docs/unit_economics_margin_safety.md)
- [Offer 与垂类评估手册](docs/offer_vertical_evaluation.md)
- [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](docs/cpl_vertical_economics_qualification_playbook.md)；系统入口 `/cpl-verticals` 已实现资格字段、buyer acceptance、Vertical Fit Score、safe CPC、阻塞项和状态审计
- [Insurance、Medicare / ACA 与 Final Expense Lead 治理手册](docs/insurance_medicare_aca_final_expense_lead_governance.md)
- [Loan、Mortgage、Credit 与 Debt Lead 治理手册](docs/loan_mortgage_credit_debt_lead_governance.md)
- [Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理手册](docs/legal_case_intake_mass_tort_lead_governance.md)
- [Home Services、Solar 与 Local Services Lead 治理手册](docs/home_services_solar_local_services_lead_governance.md)
- [Education、Career Training 与 Student Lead 治理手册](docs/education_career_training_student_lead_governance.md)
- [Healthcare、Medical Appointment 与 Clinic Lead 治理手册](docs/healthcare_medical_appointment_lead_governance.md)
- [B2B SaaS、Professional Services 与 Demo Lead 治理手册](docs/b2b_saas_professional_services_lead_governance.md)
- [Crypto、Investment 与 Trading Lead 治理手册](docs/crypto_investment_trading_lead_governance.md)
- [Employment、Recruiting 与 Staffing Lead 治理手册](docs/employment_recruiting_staffing_lead_governance.md)
- [Gambling、Sweepstakes 与 Sports Betting Lead 治理手册](docs/gambling_sweepstakes_sports_betting_lead_governance.md)
- [Addiction Treatment、Rehab 与 Behavioral Health Lead 治理手册](docs/addiction_treatment_rehab_behavioral_health_lead_governance.md)
- [Government Services、Immigration 与 Public Benefits Lead 治理手册](docs/government_services_immigration_public_benefits_lead_governance.md)
- [Lead Pricing、Payout Negotiation 与结算安全垫治理手册](docs/lead_pricing_payout_negotiation_governance.md)；系统入口 `/lead-pricing` 已实现 headline/unit/proposed payout、effective payout、paid EPC、safe CPC、scrub reserve、payment term、Buyer cap、谈价证据、阻塞项和状态审计
- [Appointment Lead、Booking、Show Rate 与 No-show 治理手册](docs/appointment_lead_booking_show_rate_governance.md)；系统入口 `/appointment-leads` 已实现预约漏斗、show/paid value、calendar capacity、reminder consent、no-show、safe CPC、阻塞项和状态审计
- [Offer Cap、Payout、状态变更与替代 Offer 治理手册](docs/offer_cap_payout_status_governance.md)；系统入口 `/offer-cap-payout` 已实现 Offer Cap Score、阻塞项、状态流和审计日志
- [Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](docs/buyer_capacity_cap_pacing_dayparting_governance.md)；系统入口 `/buyer-capacity` 已实现 cap pacing、hours、timezone、ad schedule、holiday、no buyer、missed contact、safe spend、阻塞项和状态审计
- [流量源与追踪归因手册](docs/traffic_source_tracking.md)
- [Source、Publisher、Placement 质量评分与名单治理手册](docs/source_publisher_placement_quality_governance.md)；系统入口 `/source-quality` 已实现 Source Quality Score、allowlist/watchlist/quarantine/blocklist 状态流和审计日志
- [Native、Advertorial 与 Presell Page 套利手册](docs/native_advertorial_presell_compliance.md)
- [Click -> Session -> Revenue 对账 SOP](docs/click_session_revenue_reconciliation.md)
- [追踪模板、URL 参数与跳转链 QA 手册](docs/tracking_template_redirect_chain_qa.md)
- [Campaign 命名、Labels、UTM/SubID 与维度治理手册](docs/campaign_taxonomy_naming_label_dimension_governance.md)；系统入口 `/taxonomy-governance` 已实现命名、Labels、UTM、ValueTrack、SubID、版本 hash、join gap 和状态审计
- [归因、增量性与流量蚕食治理手册](docs/attribution_incrementality_cannibalization.md)；系统入口 `/attribution` 已实现 holdout、iROAS、增量利润、蚕食风险、阻塞项和状态审计
- [转化追踪、价值回传与 Attribution 手册](docs/conversion_tracking_value_feedback.md)
- [转化信号质量与出价学习治理手册](docs/conversion_signal_quality_bidding_learning_governance.md)；系统入口 `/conversion-signals` 已实现 Signal Quality Score、primary/secondary、value mode、match rate、dedupe、lag、policy/consent、bid readiness、safe target CPA、阻塞项和状态审计
- [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](docs/crm_buyer_feedback_offline_conversion_mapping.md)；系统入口 `/crm-value-mapping` 已实现 stage mapping、buyer feedback、conversion action role、primary recommendation、value mode、transaction_id、import QA、adjustment、diagnostics、expected value、阻塞项和状态审计
- [决策窗口、回传延迟与收入延迟治理手册](docs/decision_window_revenue_lag_governance.md)；系统入口 `/decision-windows` 已实现 Decision Window Score、阻塞项、状态流和审计日志
- [落地页质量、广告密度与 MFA 风险手册](docs/landing_page_quality_mfa.md)
- [域名、站点资产与站群治理手册](docs/domain_site_asset_governance.md)
- [落地页素材抽取、Offer Intelligence 与创意 Brief 手册](docs/landing_offer_intelligence_creative_brief.md)
- [回款、结算与现金流风险手册](docs/cashflow_settlement_risk.md)
- [订阅、试用、退款、Chargeback 与 LTV 治理手册](docs/subscription_refund_ltv_chargeback_governance.md)
- [发布商收入对账、Finalized Revenue 与扣量复盘手册](docs/revenue_reconciliation_adstack.md)
- [广告创意生成、测试与优化手册](docs/creative_testing_optimization.md)
- [Creative Angle Library、素材版本与反馈闭环手册](docs/creative_angle_library_feedback_loop.md)
- [广告创意 Claim 审核与事实核查手册](docs/creative_claim_review_fact_checking.md)
- [Google Ads 广告审核、拒登、Policy Manager 与申诉证据包手册](docs/google_ads_ad_review_disapproval_appeal_playbook.md)
- [AI Provider、Prompt 模板与创意成本治理手册](docs/ai_provider_prompt_cost_governance.md)
- [链接计划与换链接合规手册](docs/link_rotation_compliance.md)
- [Google Ads 投放结构与安全自动化手册](docs/campaign_launch_automation.md)
- [Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册](docs/google_ads_editor_csv_bulk_upload_governance.md)；系统入口 `/bulk-upload` 已实现批次 hash、preview、Editor check、人工审批、Change History、回滚计划、状态流和审计日志
- [Google Ads Scripts 安全自动化手册](docs/google_ads_scripts_safe_automation.md)
- [Google Ads Scripts 数据同步、快照与一致性手册](docs/google_ads_scripts_data_sync_consistency.md)；系统入口 `/scripts-sync` 已实现同步快照、query hash、freshness、Change history、冲突、重拉窗口、状态流和审计日志
- [任务编排、安全审批、执行日志与事故复盘手册](docs/task_orchestration_approval_audit_runbook.md)
- [Google Ads Recommendations、Experiments 与 Auto-apply 优化治理手册](docs/google_ads_recommendations_experiments_auto_apply_governance.md)
- [Google Ads 竞价、Quality Score 与套利出价手册](docs/google_ads_auction_bidding_quality_score.md)
- [Google Ads 报表诊断、Search Terms 与 Change History 手册](docs/google_ads_reporting_diagnostics.md)
- [Search 自动化流量：AI Max、Broad Match 与 DSA 套利风险手册](docs/search_automation_ai_max_broad_match.md)
- [Performance Max / Demand Gen 自动化流量与套利风险手册](docs/performance_max_demand_gen_automation.md)
- [Geo、语言、本地化、时区与币种分层手册](docs/geo_language_localization_currency.md)
- [预算节奏、扩量与止损手册](docs/budget_pacing_scaling_stoploss.md)；系统入口 `/budget-pacing` 已实现 Budget Pacing Score、阻塞项、状态流和审计日志
- [Portfolio 预算分配、风险集中度与组合治理手册](docs/portfolio_budget_allocation_risk_concentration.md)；系统入口 `/portfolio-allocation` 已实现 Portfolio Allocation Score、阻塞项、状态流和审计日志
- [账号、MCC、付款与 Advertiser Verification 治理手册](docs/account_mcc_billing_verification_governance.md)
- [账号健康、政策中心与申诉 SOP](docs/policy_account_health_sop.md)
- [AdSense 站点审核、Policy Center 与广告投放限制手册](docs/adsense_site_approval_policy_center.md)
- [发布商变现栈：AdSense / AdX / Google Ad Manager 手册](docs/publisher_monetization_stack.md)
- [发布商广告质量、阻止控制与品牌安全手册](docs/publisher_ad_quality_blocking_controls.md)
- [程序化供应链透明度：ads.txt / sellers.json / schain 手册](docs/programmatic_supply_chain_transparency.md)
- [GAM / AdX Yield、Floor Price 与 Pricing Rules 手册](docs/gam_adx_yield_floor_pricing.md)
- [Header Bidding / Prebid.js 与广告栈延迟手册](docs/header_bidding_prebid_ad_stack.md)
- [广告位、刷新、可见率与页面体验手册](docs/ad_placement_refresh_viewability.md)
- [隐私、Consent 与追踪合规手册](docs/privacy_consent_tracking.md)
- [Ads 套利实战 Playbook](docs/ads_arbitrage_playbook.md)
- [ADXKit 功能与架构拆解](docs/adxkit_breakdown.md)
- [高风险能力研究与合规替代方案](docs/high_risk_capability_research.md)
- [高风险能力专题索引](docs/high_risk/README.md)
- [高风险能力逐点调研与安全复刻蓝图](docs/high_risk_capability_safe_reproduction_blueprint.md)
- [高风险能力风险矩阵与来源索引](docs/risk_matrix_and_sources.md)
- [高风险能力逐点完成审计](docs/high_risk_completion_audit.md)
- [Ads 套利研究来源库](docs/source_library.md)
- [原始需求追溯矩阵](docs/requirement_traceability_matrix.md)
- [验收清单](docs/acceptance_checklist.md)
- [系统设计文档](docs/system_design.md)

## 已交付与已沉淀能力

下面能力分为两类：一类已经在 Flask 工作台中实现为页面、表、导入/导出、任务、链接计划、来源库或审计日志；另一类已经以行业知识、设计、SOP、来源 URL 和风险审计形态沉淀，后续可继续扩展为更细的数据表或连接器。它们不是“待补空白”，也不代表所有条目都已经做成自动执行能力。

- Offer 与变现配置管理
- 套利测算与机会评分
- 单位经济、break-even CPC、safe CPC、safety margin、test budget 和 hard stop 测算
- Google Ads 账号配置与同步方式记录
- 落地页质量采集与审计
- 域名、站点资产、过期域名、站点迁移、ads.txt 和 Final URL 风险治理
- 广告创意与关键词生成
- 创意 Claim 审核、事实核查、持久化 review case 和人工放行
- 广告审核、拒登、Policy Manager issue 和申诉证据包记录
- 投放草稿、CSV / Google Ads Scripts JSON 导出与人工确认
- 指标导入、利润分析与优化建议
- 发布商 estimated/finalized/paid revenue 对账和扣量复盘
- 订阅、试用、续费、退款、chargeback、clawback 和 cohort LTV 复盘
- Click -> Session -> Revenue 漏斗对账和差异诊断
- 归因、增量性、iROAS、holdout、lift 和流量蚕食复盘；`/attribution` 保存归因增量评审和审计状态
- Search terms、Auction Insights、Change history、Report Editor 和落地页/素材报表诊断
- 转化信号质量、primary/secondary、value feedback、Smart Bidding learning 和 bid strategy report 复盘
- 决策窗口、conversion lag、revenue lag、cohort maturity、stop-loss 和 wait-loss 复盘
- 季节性、事件日历、需求预测、预算 ramp 和季后退出复盘
- AI Max、Broad Match、Dynamic Search Ads、Final URL expansion、自动生成资产和 Search 自动化流量复盘
- Performance Max、Demand Gen、Final URL expansion、Search themes、Audience signals 和自动化流量复盘
- Geo、语言、本地化、设备、时区、币种和 bad geo 复盘
- Portfolio 预算分配、风险集中度、相关性和现金风险复盘；`/portfolio-allocation` 保存组合分配评审和审计状态
- 账号/MCC、付款资料、访问权限、Advertiser Verification 和代理关系治理
- AdSense 站点审核、Policy Center、ad serving limits 和恢复证据包
- 发布商广告质量、blocking controls、Ad review center、敏感分类和品牌安全复盘
- ads.txt、sellers.json、schain 和程序化供应链透明度复盘
- GAM/AdX yield、floor price、pricing rules、Open Bidding 和 fill/eCPM 复盘
- Header Bidding、Prebid.js、bidder、timeout、price granularity 和广告栈延迟复盘
- 广告位、Ad refresh、viewability、CLS 和页面体验复盘
- Offer cap、payout 版本、buyer capacity、替代 Offer 审核和预算联动评审
- Lead 质量、Postback 对账和拒付原因沉淀
- Ping/Post、buyer routing、consent/disclosure、PII 最小化、cap、fallback、buyer feedback 和 safe CPL 门禁评审
- Native / Advertorial / Presell Page 素材、披露、source 质量和后端收入复盘
- Source、Publisher、Placement 质量评分、名单治理、停源和恢复复盘
- 流量供应商合同、IO、refund、credit、makegood 和争议证据复盘
- 研究来源库和来源 URL 追踪
- 高风险能力审计记录
- 安全任务中心与执行日志
- 合规链接轮换计划和人工确认轮换
- 任务执行日志与审计记录

明确不交付的执行能力仍然包括：Cookie / Session 后台接管、登录或 2FA 绕过、补点击或刷展示、代理/指纹/Worker 规避关联、cloaking 分流、账号池和封禁后自动换号。
