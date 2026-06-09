# 原始需求追溯矩阵

更新时间：2026-06-09

本文用于把用户原始目标逐条追溯到当前交付物。它不是新的业务规则，而是验收索引：每一项需求都要能找到文档、系统入口、数据表或验证脚本。

原始目标摘要：

1. 收集 Google Ads / AdSense / AdX 套利相关信息以及主要流程。
2. 拆解 `https://adxkit.com/` 的功能、设计、架构。
3. 第一版不要多租户。
4. 重点是 Ads 套利行业知识，而不是系统本身。
5. 完成 ADXKit 公开页面核心功能，并配套使用、开发文档。
6. 高风险能力不是“不复刻”，而是逐点调研、解释原理、沉淀知识、审计字段、SOP、来源 URL 和安全替代流程。

## 1. 验收总览

| 原始要求 | 当前完成形态 | 主要证据 | 系统入口 / 验证 |
| --- | --- | --- | --- |
| Ads 套利说明完善 | 已形成行业知识库、业务模式、实战 playbook、运营手册、指标字典、单位经济、现金流、流量源、搜索套利、RSOC/N2S、Lead-gen、发布商变现等文档体系 | [Ads 套利行业知识库](ads_arbitrage_industry.md)、[Ads 套利业务模式拆解手册](ads_arbitrage_business_models.md)、[Ads 套利实战 Playbook](ads_arbitrage_playbook.md)、[Ads 套利来源证据矩阵](ads_arbitrage_source_evidence_matrix.md) | `/knowledge/industry`、`/knowledge/business_models`、`/knowledge/playbook`、`/knowledge/evidence_matrix` |
| 收集主要流程 | 已沉淀从 Offer 评估、页面建设、创意生成、投放草稿、导出、指标导入、优化、换链接、风险审计、来源记录、日志复盘的端到端流程 | [文档入口和验收导航](docs_index.md)、[使用文档](usage.md)、[Ads 套利运营手册](ads_arbitrage_operations.md) | `/docs`、`/knowledge/usage`、`/logs` |
| 拆解 ADXKit 功能 | 已按公开页面拆解多账号、Scripts 同步、广告层级、落地页采集、AI 创意、投放提交、任务、换链接、补点击、代理、防关联、多租户等能力 | [ADXKit 功能与架构拆解](adxkit_breakdown.md)、[验收清单](acceptance_checklist.md) | `/knowledge/adxkit`、`/knowledge/acceptance` |
| 拆解 ADXKit 设计和架构 | 已给出业务流程、推断架构、模块职责、可复刻能力和不交付边界 | [ADXKit 功能与架构拆解](adxkit_breakdown.md)、[系统设计文档](system_design.md) | `/knowledge/adxkit`、`/knowledge/design` |
| 不做多租户 | V1 schema 和路由均按单团队工作台设计，没有 `tenant_id`、`organization_id`、`user_id` 字段 | [系统设计文档](system_design.md)、[开发文档](development.md) | `scripts/acceptance_audit.py` 检查 no multi-tenant columns |
| Flask + MySQL 实现 | 已实现 Flask 应用、SQLAlchemy 模型、`.env.example` MySQL 连接、docker-compose MySQL、页面和 CLI seed | [开发文档](development.md)、[README](../README.md)、`.env.example` | `python -m flask --app app db-init`、`python -m flask --app app seed` |
| 使用文档 | 已覆盖启动、Offer、测算、页面采集、创意、草稿导出、指标导入、优化建议、风险审计、来源库、任务中心、链接计划、日志 | [使用文档](usage.md) | `/knowledge/usage` |
| 开发文档 | 已覆盖目录结构、配置、数据模型、服务层、验证命令、安全边界和扩展规则 | [开发文档](development.md) | `/knowledge/development` |
| 来源 URL 记录 | 已有 Markdown 来源库、证据矩阵、`ResearchSource` seed 数据和 `/sources` 页面；来源可标记 candidate、accepted、needs_update、archived 并写入审计日志 | [Ads 套利研究来源库](source_library.md)、[Ads 套利来源证据矩阵](ads_arbitrage_source_evidence_matrix.md) | `/sources`、`/sources/<id>/status`、`ResearchSource` seed 526 条 |
| 高风险能力逐点完成 | 已把 6 个高风险点转成专题研究、原理解释、系统替代、审计字段、SOP、来源 URL 和验收审计 | [高风险能力逐点调研与安全复刻蓝图](high_risk_capability_safe_reproduction_blueprint.md)、[高风险能力逐点完成审计](high_risk_completion_audit.md)、[高风险能力专题索引](high_risk/README.md) | `/knowledge/risk_blueprint`、`/knowledge/risk_completion`、`/knowledge/risk_index` |

## 2. ADXKit 核心能力追溯

| ADXKit 公开能力 | 业务原理 | 当前系统形态 | 当前文档形态 | 验收证据 |
| --- | --- | --- | --- | --- |
| Offer 管理 | 套利测试从 Offer / 垂类 / payout / geo / URL / policy note 开始 | `/offers`、`offers` 表 | [Offer 与垂类评估手册](offer_vertical_evaluation.md)、[Affiliate Network / Lead Buyer 尽调与条款手册](affiliate_network_due_diligence.md) | smoke test 访问 `/offers` 和 Offer detail |
| 落地页采集和 Offer Intelligence | 从页面提取 title、description、H1、CTA、claim、proof、form 和质量信号 | Offer 详情页 crawl、`landing_pages` 表 | [落地页素材抽取、Offer Intelligence 与创意 Brief 手册](landing_offer_intelligence_creative_brief.md)、[落地页质量、广告密度与 MFA 风险手册](landing_page_quality_mfa.md) | seed + smoke test 验证 Offer detail 和 Claim 审核 |
| AI 创意生成 | 基于页面证据生成 headline、description、keyword 和 angle，不凭空造 claim，并把强声明风险落为可复核的 Claim review case | Offer 详情页 generate creatives、`creative_sets` 表、`creative_claim_reviews` 表、`/claim-reviews/<id>/status` | [广告创意生成、测试与优化手册](creative_testing_optimization.md)、[广告创意 Claim 审核与事实核查手册](creative_claim_review_fact_checking.md) | smoke test 和 acceptance audit 验证创意生成、Claim 审核来源 URL、状态流和审计日志 |
| 广告审核、拒登和申诉证据包 | 把 Policy Manager issue、policy topic、受影响对象、URL、修复摘要、证据 URL 和申诉文字转成可复盘案例 | `/ad-reviews`、`ad_review_cases` 表、`/ad-reviews/<id>/status` | [Google Ads 广告审核、拒登、Policy Manager 与申诉证据包手册](google_ads_ad_review_disapproval_appeal_playbook.md) | smoke test 和 acceptance audit 验证案例创建、危险语义拦截、状态流和审计日志 |
| Campaign / Ad Group / Keyword / Ad 草稿 | 把 Offer、创意、关键词组织成可审核投放结构，并记录草稿评审状态 | `/campaigns`、`campaign_drafts` 表，状态更新写入 `/logs` | [Google Ads 投放结构与安全自动化手册](campaign_launch_automation.md) | smoke test 验证状态流和 CSV / Scripts export route |
| Google Ads Editor CSV | 用人工审核的批量导入替代后台接管，并在导出前检查 campaign、Claim review 和 ad review case 状态 | `/campaigns/<id>/export.csv`、`services/preflight.py` | [Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册](google_ads_editor_csv_bulk_upload_governance.md) | smoke test 检查 preflight block 和 CSV header |
| Google Ads Editor / Bulk Upload 批量变更治理 | 批量发布前必须确认 batch/hash、目标账号、预算变化、URL 变化、preview、Editor check、人工审批、Change History 和回滚证据 | `/bulk-upload`、`bulk_upload_reviews` 表、`/bulk-upload/<id>/status`、`audit_logs` | [Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册](google_ads_editor_csv_bulk_upload_governance.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、状态流和审计日志 |
| Google Ads Scripts JSON | 用授权 Scripts payload 和 preview 替代 Cookie UI 自动化，并在导出前检查 campaign、Claim review 和 ad review case 状态 | `/campaigns/<id>/export.script.json`、`scripts/google_ads_script_payload_preview.js`、`services/preflight.py` | [Google Ads Scripts 安全自动化手册](google_ads_scripts_safe_automation.md)、[Google Ads Scripts 数据同步、快照与一致性手册](google_ads_scripts_data_sync_consistency.md) | acceptance audit 检查 `no_cookie_automation` 和 export preflight |
| Google Ads Scripts 数据同步治理 | 同步结果必须保存 customer、date range、query/report、snapshot hash、freshness、row count、data/revenue status、Change history、冲突和重拉窗口 | `/scripts-sync`、`script_sync_reviews` 表、`/scripts-sync/<id>/status`、`audit_logs` | [Google Ads Scripts 数据同步、快照与一致性手册](google_ads_scripts_data_sync_consistency.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、状态流和审计日志 |
| Campaign 命名、Labels、UTM/SubID 与维度治理 | 批量投放前必须确认命名 token、label group、UTM、ValueTrack、SubID、版本 hash、join key、PII/敏感属性和人审 | `/taxonomy-governance`、`taxonomy_reviews` 表、`/taxonomy-governance/<id>/status`、`audit_logs` | [Campaign 命名、Labels、UTM/SubID 与维度治理手册](campaign_taxonomy_naming_label_dimension_governance.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、状态流和审计日志 |
| 归因、增量性与流量蚕食治理 | 归因 credit 不等于新增收入，扩量前必须看 control/treatment、holdout、iROAS、incremental profit 和 brand/organic/remarketing/PMax 蚕食 | `/attribution`、`attribution_reviews` 表、`/attribution/<id>/status`、`audit_logs` | [归因、增量性与流量蚕食治理手册](attribution_incrementality_cannibalization.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、状态流和审计日志 |
| CPL 垂类经济与资格问题 | 不同 CPL 垂类不能共用 payout、CVR、资格字段和放量阈值，必须按 buyer acceptance、reject reason、feedback lag、policy risk 和 paid definition 管理 | `/cpl-verticals`、`cpl_vertical_reviews` 表、`/cpl-verticals/<id>/status`、`audit_logs` | [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、状态流和审计日志 |
| Lead Pricing 与 Payout Negotiation | Headline payout 不能直接作为可出价价值，必须经过 accepted/qualified/approved/paid、return/scrub、payment term、cap、source transparency 和谈价证据折算 | `/lead-pricing`、`lead_pricing_reviews` 表、`/lead-pricing/<id>/status`、`audit_logs` | [Lead Pricing、Payout Negotiation 与结算安全垫治理手册](lead_pricing_payout_negotiation_governance.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、safe CPC、blockers、状态流和审计日志 |
| Appointment Lead、Booking、Show Rate 与 No-show | 预约套利不能把 booked 当 paid，必须按 request/book/confirm/show/complete/paid、calendar capacity、reminder consent、no-show/cancel、buyer terms 和 offline mapping 计算可出价价值 | `/appointment-leads`、`appointment_lead_reviews` 表、`/appointment-leads/<id>/status`、`audit_logs` | [Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md) | smoke test 和 acceptance audit 验证危险语义拦截、safe CPC、safe appointment spend、blockers、状态流和审计日志 |
| Buyer Capacity、Cap Pacing 与 Dayparting | 接量能力决定 CPL 扩量上限，必须把 buyer cap、hours、timezone、ad schedule、holiday、no buyer、missed contact、fallback 和 overdelivery guardrail 接到预算门禁 | `/buyer-capacity`、`buyer_capacity_reviews` 表、`/buyer-capacity/<id>/status`、`audit_logs` | [Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md) | smoke test 和 acceptance audit 验证危险语义拦截、safe leads、safe media spend、blockers、状态流和审计日志 |
| Ping/Post 与 Lead Buyer Routing | Lead marketplace 不能把 submitted 或 accepted 当 paid，必须按 consent/disclosure、字段最小化、suppression/DNC、buyer cap、exclusive/shared/aged、fallback、reject reason 和 buyer feedback 计算可收款价值 | `/ping-post-routing`、`ping_post_routing_reviews` 表、`/ping-post-routing/<id>/status`、`audit_logs` | [Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md) | smoke test 和 acceptance audit 验证危险语义拦截、unsafe PII/consent 阻断、Routing Quality Score、expected payable value、safe CPL、blockers、状态流和审计日志 |
| 转化信号质量与出价学习 | 自动投放和 Smart Bidding 只能学习真实、可去重、接近 approved/paid 的信号，必须把 primary/secondary、value、match、dedupe、lag、consent 和 diagnostics 放到扩量门禁 | `/conversion-signals`、`conversion_signal_reviews` 表、`/conversion-signals/<id>/status`、`audit_logs` | [转化信号质量与出价学习治理手册](conversion_signal_quality_bidding_learning_governance.md) | smoke test 和 acceptance audit 验证危险语义拦截、shallow primary 降级、Signal Quality Score、bid readiness、safe target CPA、blockers、状态流和审计日志 |
| CRM 阶段与 Offline Conversion Value Mapping | Buyer feedback 不能直接上传给 Ads，必须先标准化 stage、排除 rejected/returned 正向信号、定义 transaction_id、value mode、adjustment 和 import QA | `/crm-value-mapping`、`crm_value_mapping_reviews` 表、`/crm-value-mapping/<id>/status`、`audit_logs` | [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md) | smoke test 和 acceptance audit 验证危险语义拦截、returned positive 阻断、CRM Mapping Score、upload policy、expected value、blockers、状态流和审计日志 |
| Search Terms、否定词和 Query Mining | 真实 query 必须连接 keyword、match type、network、device、landing、approved/paid revenue、buyer reject、policy risk 和 conversion lag 后再做 negative、promote、split、page brief 或 pause 决策 | `/query-mining`、`query_mining_reviews` 表、`/query-mining/<id>/status`、`audit_logs` | [Search Terms、否定词与 Query Mining 治理手册](search_terms_negative_keyword_query_mining.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、否定词状态流和审计日志 |
| Offer Cap、Payout 和替代 Offer | 预算动作必须跟 cap、payout version、buyer capacity、approval/paid/deduction 和已审核替代 Offer 证据联动 | `/offer-cap-payout`、`offer_cap_reviews` 表、`/offer-cap-payout/<id>/status`、`audit_logs` | [Offer Cap、Payout、状态变更与替代 Offer 治理手册](offer_cap_payout_status_governance.md) | smoke test 和 acceptance audit 验证创建、blockers、状态流和审计日志 |
| Source / Publisher / Placement 质量治理 | 放量前必须确认来源透明、追踪完整、intent fit、approved/paid revenue、deduction、invalid clicks、complaints、buyer reject、policy issue 和停源控制 | `/source-quality`、`source_quality_reviews` 表、`/source-quality/<id>/status`、`audit_logs` | [Source、Publisher、Placement 质量评分与名单治理手册](source_publisher_placement_quality_governance.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、名单状态流和审计日志 |
| 流量供应商合同、IO 和争议治理 | 外部采购必须把 IO、tracking/reporting appendix、质量条款、invoice、refund/credit/makegood、dispute evidence 和 amount_at_risk 接入放量门禁 | `/vendor-contracts`、`vendor_contract_reviews` 表、`/vendor-contracts/<id>/status`、`audit_logs` | [流量供应商合同、IO、退款与争议治理手册](traffic_vendor_contract_io_dispute_governance.md) | smoke test 和 acceptance audit 验证创建、危险语义拦截、blockers、争议状态流和审计日志 |
| 指标同步和利润分析 | 套利判断依赖真实 cost、click、conversion、revenue、lag 和 deduction | `/metrics/import`、Dashboard、`metrics_daily` 表 | [单位经济模型、Break-even 与安全边际手册](unit_economics_margin_safety.md)、[决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md) | smoke test 指标导入和 `/optimization` |
| 决策窗口和收入成熟度 | 扩量前必须区分 data freshness、conversion lag、approval lag、settlement lag、approved/paid revenue 和事故状态 | `/decision-windows`、`decision_window_reviews` 表、`/decision-windows/<id>/status`、`audit_logs` | [决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md) | smoke test 和 acceptance audit 验证创建、blockers、状态流和审计日志 |
| 预算节奏和扩量门禁 | 扩量前必须核对 current/proposed budget、test budget、hard stop、safe/actual CPC、收入成熟度、现金缓冲和 overdelivery 风险 | `/budget-pacing`、`budget_pacing_reviews` 表、`/budget-pacing/<id>/status`、`audit_logs` | [预算节奏、扩量与止损手册](budget_pacing_scaling_stoploss.md) | smoke test 和 acceptance audit 验证创建、blockers、状态流和审计日志 |
| Portfolio 组合分配和风险集中度 | 组合预算必须区分 Core/Scale/Test/Explore/Quarantine、revenue status mix、单一 Offer/source/account/partner 集中度、现金缓冲和事故状态 | `/portfolio-allocation`、`portfolio_allocation_reviews` 表、`/portfolio-allocation/<id>/status`、`audit_logs` | [Portfolio 预算分配、风险集中度与组合治理手册](portfolio_budget_allocation_risk_concentration.md) | smoke test 和 acceptance audit 验证创建、blockers、状态流和审计日志 |
| 优化建议 | 把 ROI、RPV、CPC、样本量、追踪异常和来源质量转成待审动作，并记录内部处理状态 | `/optimization`、`optimization_actions` 表，状态更新写入 `/logs` | [异常监控、告警、止损队列与事故分诊手册](anomaly_monitoring_alerting_stoploss_incident_triage.md)、[Google Ads Recommendations、Experiments 与 Auto-apply 优化治理手册](google_ads_recommendations_experiments_auto_apply_governance.md) | smoke test 验证导入后生成优化建议并更新状态 |
| 任务中心和日志 | 批量系统需要任务状态、执行次数、失败原因和审计链 | `/tasks`、`task_jobs` 表、`/logs`、`audit_logs` 表 | [任务编排、安全审批、执行日志与事故复盘手册](task_orchestration_approval_audit_runbook.md) | smoke test + guardrail check |
| 换链接 | 正常维护是断链修复、UTM 更新、同主题候选 URL、评审状态、批准后人工确认和版本日志 | `/links`、`link_rules` 表，状态更新和轮换写入 `/logs` | [链接计划与换链接合规手册](link_rotation_compliance.md)、[追踪模板、URL 参数与跳转链 QA 手册](tracking_template_redirect_chain_qa.md) | acceptance audit 拦截 worker/proxy/cloaking 链接计划，并检查未批准不能轮换 |
| 来源库 | 行业知识和政策边界要能追溯来源 URL，并能区分待复核、已采纳、需更新和已归档来源 | `/sources`、`/sources/<id>/status`、`research_sources` 表、`audit_logs` 表 | [Ads 套利研究来源库](source_library.md)、[Ads 套利来源证据矩阵](ads_arbitrage_source_evidence_matrix.md) | acceptance audit 检查 source counts 和 source status |
| 风险审计 | 高风险需求要进入发现、缓解、来源、状态和负责人流程，状态更新写入审计日志但不自动放行动作 | `/risk-audits`、`/risk-audits/<id>/status`、`risk_audits` 表、`audit_logs` 表 | [高风险能力风险矩阵与来源索引](risk_matrix_and_sources.md) | smoke test 和 acceptance audit |

## 3. 高风险能力追溯

| 高风险点 | 用户要求的完成方式 | 当前完成证据 | 系统替代入口 | 不交付边界 |
| --- | --- | --- | --- | --- |
| Ads Cookie 登录和后台操作 | 需要研究原理和操作诉求，而不是简单排除 | [Ads Cookie 登录和后台操作研究](high_risk/ads_cookie_backend_operation.md)、[高风险能力逐点调研与安全复刻蓝图](high_risk_capability_safe_reproduction_blueprint.md) | `/accounts`、CSV / Scripts JSON、`/logs`、`/risk-audits` | 不获取、导入、复用、注入 Cookie，不接管后台 UI |
| 自动绕过登录、2FA、安全挑战 | 拆解认证链路、状态机和人工/自动边界 | [自动绕过登录、2FA、安全挑战研究](high_risk/automated_login_2fa_challenge_bypass.md) | `/tasks`、`/risk-audits` | 不处理验证码、OTP、恢复码或安全挑战绕过 |
| 补点击、刷展示、模拟自然流量 | 解释无效流量、信号污染和追踪断点处理 | [补点击、刷展示、模拟自然流量研究](high_risk/invalid_traffic_click_impression_simulation.md) | `/metrics/import`、`/optimization`、来源隔离 SOP | 不生成点击、展示、访问、Referer、停留时长或行为路径 |
| 代理、指纹、Worker 转发规避关联检测 | 解释中性技术、关联图谱和合法隔离证据 | [代理、指纹、Worker 转发规避关联检测研究](high_risk/proxy_fingerprint_worker_association_evasion.md) | `/risk-audits`、`/accounts`、`/links` | 不保存代理池、指纹 profile、Worker 规避脚本 |
| Cloaking 或审核页/用户页不一致 | 解释差异化页面边界、Review/User 一致性和 URL 生命周期 | [Cloaking 或审核页/用户页不一致研究](high_risk/cloaking_review_user_page_mismatch.md) | `/links`、`/risk-audits`、`/logs` | 不做 Bot 分流、双版本页面或隐藏目的地 |
| 为规避封禁创建或切换账号 | 解释账号图谱、暂停状态机、Related Account 和申诉证据包 | [为规避封禁创建或切换账号研究](high_risk/ban_evasion_account_switching.md) | `/accounts`、`/risk-audits` | 不做账号池、批量开户、付款资料规避或封禁后自动换号 |

## 4. 行业知识覆盖追溯

| 知识域 | 当前文档 | 为什么重要 |
| --- | --- | --- |
| 基本模型和公式 | [Ads 套利行业知识库](ads_arbitrage_industry.md)、[Ads 套利业务模式拆解手册](ads_arbitrage_business_models.md) | 定义 CPC、RPV、EPC、RPM、ROI、safety margin 和套利差价来源 |
| 流量采购和来源质量 | [买量渠道与流量供应商尽调手册](traffic_channel_vendor_due_diligence.md)、[Source、Publisher、Placement 质量评分与名单治理手册](source_publisher_placement_quality_governance.md) | 套利成败常取决于来源透明、扣量、投诉、placement 和 buyer feedback |
| Search / RSOC / Feed | [Search Arbitrage、Feed 与 Parking 模式手册](search_arbitrage_feed_parking.md)、[RSOC / N2S 手册](rsoc_n2s_search_feed_partner_governance.md) | Google 生态套利的重要细分模式，必须理解 feed 权限、query intent 和 finalized revenue |
| Lead-gen 和 CPL 垂类 | [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md) 及各垂类手册 | Lead 套利需要按 qualification、buyer acceptance、reject reason 和 paid outcome 优化 |
| 创意、页面和 claim | [落地页素材抽取、Offer Intelligence 与创意 Brief 手册](landing_offer_intelligence_creative_brief.md)、[广告创意 Claim 审核与事实核查手册](creative_claim_review_fact_checking.md) | 高 CTR 如果来自夸张 claim，会损害收入口径、政策状态和长期账号健康 |
| 指标、归因和回传延迟 | [Ads 套利指标字典与口径](metric_dictionary.md)、[Click -> Session -> Revenue 对账 SOP](click_session_revenue_reconciliation.md)、[决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md) | 防止把数据延迟、追踪断点和扣量误判为需要补点击或刷量 |
| 现金流和结算 | [回款、结算与现金流风险手册](cashflow_settlement_risk.md)、[发布商收入对账、Finalized Revenue 与扣量复盘手册](revenue_reconciliation_adstack.md) | 套利失败常不是 gross ROI 不够，而是 paid revenue、deduction、payback cycle 和 cash buffer 不够 |
| 平台政策和来源证据 | [Ads 套利来源证据矩阵](ads_arbitrage_source_evidence_matrix.md)、[Ads 套利研究来源库](source_library.md) | 把行业判断和系统边界绑定到公开来源 URL，减少“拍脑袋规则” |

## 5. 自动验收追溯

| 验收脚本 | 覆盖内容 |
| --- | --- |
| `python -m compileall adsworkbench app.py scripts` | Python 语法和模块可编译 |
| `python scripts/verify_research_docs.py` | 高风险专题、核心行业手册、来源 URL、README、使用/开发/系统设计关键短语 |
| `python scripts/smoke_test.py` | 核心页面、知识页面、Offer、创意、Claim review case、广告审核案例、CSV/Scripts 导出、Bulk Upload 治理、Scripts 同步治理、命名维度治理、归因增量治理、CPL 垂类治理、Lead Pricing 治理、Appointment Lead 治理、Buyer Capacity 治理、Conversion Signal 治理、CRM Value Mapping 治理、Query Mining、决策窗口、预算节奏、来源质量、供应商合同争议、来源库、风险审计、任务、链接、指标导入 |
| `python scripts/acceptance_audit.py` | 文档路由映射、验收文档、`.env.example`、单团队 schema、seed 核心数据、高风险来源覆盖、核心页面、Bulk Upload、Scripts 同步、命名维度、归因增量、CPL 垂类、Lead Pricing、Appointment Lead、Buyer Capacity、Conversion Signal、CRM Value Mapping、Query Mining、决策窗口、预算节奏、来源质量和供应商合同争议状态流、guardrails |
| `python -m flask --app app seed` | 当前数据库可插入 demo 数据、来源库、高风险记录和核心对象 |

## 6. 当前已知边界

- ADXKit 来源是 `https://adxkit.com/` 公开页面，属于 `public_claim`，只能用于拆解其公开宣称的能力，不证明其内部真实实现。
- 高风险能力按知识、原理、审计、SOP、来源 URL 和安全替代流程完成，不交付执行型对抗能力。
- V1 是单团队工作台，不做多租户、不做员工权限、不做账号池。
- 系统使用 CSV / Google Ads Scripts JSON / 人工审核作为执行前准备形态；不保存 Google Ads Cookie、Session Token、浏览器 Profile、代理池、指纹配置或 Worker 规避规则。

## 7. 信息来源 URL

- ADXKit homepage: https://adxkit.com/
- Google Ads, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads, Secure your Google Ads account: https://support.google.com/google-ads/answer/2375456
- Google Ads, Confirm it is you: https://support.google.com/google-ads/answer/12865189
- Google Ads API, OAuth overview: https://developers.google.com/google-ads/api/docs/oauth/overview
- Google Ads Scripts, Authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- Google Ads Scripts, Reports: https://developers.google.com/google-ads/scripts/docs/concepts/reports
- Google Ads Scripts, Execution logs: https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs
- Google Ads Editor, Prepare a CSV file: https://support.google.com/google-ads/editor/answer/56368
- AdSense, Invalid traffic: https://support.google.com/adsense/answer/16737
- AdSense, Program policies: https://support.google.com/adsense/answer/48182
- MDN, Using HTTP cookies: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- Cloudflare Workers documentation: https://developers.cloudflare.com/workers/
