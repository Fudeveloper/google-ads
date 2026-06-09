# 单团队 Ads 套利工作台系统设计

更新时间：2026-06-09

## 1. 设计目标

系统不是为了“自动点后台”，而是把 Ads 套利团队的知识、流程、指标和风控落成可执行工作台。

第一版目标：

- 单团队使用，不做多租户。
- 用 Flask + MySQL 实现核心数据和页面。
- 支持 Offer 管理、落地页审计、创意生成、投放草稿、指标导入、ROI 分析、归因增量评审、优化建议状态闭环、链接轮换和审计日志。
- 对 Google Ads 的执行默认使用 CSV 导出、Google Ads Scripts、人工审核。
- 不存储、不复用、不注入 Ads Cookie。

## 2. 系统边界

### 2.1 做

- 业务资料沉淀。
- 落地页信息采集。
- 落地页素材证据抽取和 claim/proof 创意核查。
- 追踪模板、URL 参数和跳转链 QA。
- 广告创意和关键词生成。
- 创意 claim 风险审查和事实核查提示。
- 投放草稿和导出。
- 花费/收入导入。
- 利润计算、归因增量评审和优化建议。
- 研究来源 URL 和证据摘要沉淀。
- 受众、再营销、Customer Match、Personalized Ads 和 Consent 边界审计。
- 合规链接版本管理。
- 审计日志。

### 2.2 高风险能力交付边界

以下能力不是“不研究、不复刻”，而是只复刻可用于培训、审计、SOP 和系统治理的部分：原理解释、行业诉求、平台规则、风险识别、审计字段、来源 URL 和合规替代流程。系统不交付执行型对抗能力。

- Cookie 自动化操作 Google Ads。
- 绕过官方登录、安全挑战、2FA、审核或账号限制。
- 补点击、刷量、虚假曝光。
- 代理、指纹、Worker 转发用于规避关联检测。
- cloaking、审核页和用户页不一致。
- 为规避封禁创建或切换账号。
- 多租户和员工权限第一版不做。

对应系统落地是：

- `/accounts` 记录账号配置、同步方式、状态备注和申诉复盘，不保存 Cookie、Session Token、浏览器 Profile、代理池或指纹配置。
- `/tasks` 只承接白名单内的安全任务，不把登录、2FA、安全挑战、点击、展示、访问、cloaking、换号或代理指纹语义作为任务类型。
- `/links` 只做同主题、已审核、人工确认的 Final URL / Tracking URL 维护，不做审核页和用户页双版本。
- `/metrics/import` 和 `/optimization` 用真实报表、来源隔离和对账修复处理异常，不用补点击或模拟自然流量修报表。
- `/risk-audits` 和 `/sources` 承接 6 个高风险能力的原理、来源 URL、审计字段、处理方案和 SOP。

## 3. 核心流程

```mermaid
flowchart TD
    Offer["录入 Offer"] --> Crawl["采集/审计落地页"]
    Crawl --> Creative["生成广告创意和关键词"]
    Creative --> Draft["创建投放草稿"]
    Draft --> Review["人工审核"]
    Review --> Export["导出 CSV / Script 任务"]
    Export --> Metrics["导入花费与收入"]
    Metrics --> Analyze["ROI 和风险分析"]
    Analyze --> Actions["优化建议"]
    Actions --> Log["审计日志"]
    Offer --> Links["链接轮换计划"]
    Links --> Log
```

## 4. 模块设计

### 4.1 Dashboard

展示：

- Offer 数量。
- 投放草稿数量。
- 最近 7 天花费、收入、利润、ROI。
- 高风险提醒：亏损、无收入消耗、链接异常、页面审计失败。
- 今日待处理任务。

### 4.2 Offer 管理

字段：

- 名称、垂类、国家、语言。
- Payout 模式：CPA、CPL、CPS、RevShare、Display RPM。
- Payout 金额或预估 Session RPM。
- 目标 URL、跟踪 URL。
- 政策备注、素材角度、状态。

Offer 运行中治理需要把 active/paused/expired/quality_hold、payout effective_from、daily/monthly/source/geo cap、cap_used/cap_remaining、buyer capacity、替代 Offer 审核状态和回滚计划放在同一条证据链里。第一版已实现 `/offer-cap-payout` 和 `offer_cap_reviews`：表中保存 offer/replacement/campaign 绑定、offer_status、cap_type、cap_period、cap_limit、cap_used、expected_next_conversions、current_payout、new_payout、approval_rate_percent、paid_rate_percent、deduction_rate_percent、days_since_cap_update、buyer_capacity_status、replacement_status、replacement_fit_score、same_intent_review、source_quality、policy_risk、score、risk_level、recommended_action、cap_usage_percent、cap_remaining、effective_payout、safe_daily_media_cost、blockers、status、notes 和 source_urls；`/offer-cap-payout/<id>/status` 更新 waiting_cap_update、reduce_budget、pause_traffic、manual_replacement_ready、closed 等内部状态并写入 `audit_logs`。后续可拆分 `offer_status_snapshots`、`offer_payout_versions`、`offer_cap_snapshots`、`offer_replacement_plans` 和 `cap_pacing_alerts`。系统不自动登录联盟后台、不超 cap 灌量、不用替代 Offer 做 cloaking 或规避拒付。

### 4.2.1 单位经济和机会测算

`/calculators` 是单位经济 V1。它接收 revenue model、Session RPM、payout、CVR、CPC、safety factor、target clicks、policy/content/tracking/source score 和 cash buffer，输出 RPV/EPC、break-even CPC、safe CPC、safety margin、expected revenue/cost/profit、ROI、min sample clicks、test budget、hard stop 和 opportunity score。

后续可扩展 `unit_economic_models`、`unit_economic_scenarios`、`break_even_snapshots`、`safety_factor_versions`、`test_budget_plans`、`unit_economic_decisions` 和 `model_assumption_audits`，用于保存 payout、approval rate、paid rate、deduction、landing arrival rate、cash buffer、stress case、decision 和 reviewer。系统只做测算、建议和审计，不自动买量、不补点击、不伪造转化或收入。

### 4.3 落地页审计

采集：

- HTTP 状态码。
- Title、meta description、H1/H2。
- 页面字数。
- 内链、外链数量。
- CTA texts、price/value snippets、claim snippets、proof/review snippets。
- 表单数量和用户输入字段数量。
- 是否存在 privacy/contact/about 关键词。
- 页面与 Offer 的主题摘要。

评分：

- 相关性。
- 原创/信息量的粗略代理指标。
- 透明度。
- 导航可用性。
- 技术可达性。

额外输出：

- `raw_summary` 保留 CTA、价格/价值、claim、proof/review 和 form signals。
- 如果 claim 存在但 proof 弱，写入 warning，要求创意事实核查。
- 后续可拆为 `landing_evidence` 表，记录 snippet、claim_type、source_selector 和 risk_level。

### 4.4 创意生成

输入：

- Offer 信息。
- 落地页标题、描述、标题结构和素材证据摘要。
- 国家、语言、用户意图。

输出：

- 15 个标题。
- 4 个描述。
- 30 个关键词。
- 3 组广告角度：问题解决、对比选择、清单/指南。
- Claim 审核提示：guarantee、official、best/top/#1、free、discount、review、scarcity、editorial style 等。

第一版使用规则模板生成，后续可接 AI Provider。

创意生成原则是 evidence-first：系统可以基于页面已有 claim/proof/CTA 改写广告标题和描述，但不能新增页面没有的价格、折扣、排名、认证、用户评价、官方关系或保证结果。强声明必须回到落地页 evidence 做人工核查。

第一版 Claim 审核已经落为 `creative_claim_reviews` 表，记录 creative_set、asset_type、asset_text、issue、severity、action、evidence、source_url 和 review_status。生成创意时会创建审核记录，也可以通过 `/creatives/<id>/claim-reviews/run` 刷新；状态通过 `/claim-reviews/<id>/status` 更新为 open、approved、rewrite_required、blocked 或 dismissed，并写入 `audit_logs`。它不写后台、不自动删除或改写资产、不自动提交广告。

广告审核和拒登治理已经落为 `ad_review_cases` 表和 `/ad-reviews` 页面，用于记录广告、素材、关键词、Final URL、tracking template、policy topic、申诉证据包和修复动作。状态流为 open、fixed、appeal_ready、appeal_submitted、approved、rejected、abandoned，并写入 `audit_logs`。系统只做状态记录、证据包、QA 和复盘，不通过 Cookie 操作后台，不自动提交 appeal，不自动绕过登录/2FA/安全挑战，不用换账号、cloaking 或动态目的地规避政策执行。后续可继续扩展 `policy_decision_snapshots`、`appeal_evidence_packages`、`ad_review_events` 和 `policy_fix_actions`。

AI Provider 和 Prompt 治理后续可扩展 `ai_providers`、`ai_model_profiles`、`prompt_templates`、`prompt_runs`、`ai_output_assets`、`creative_angle_library`、`ai_cost_daily`、`ai_review_decisions` 和 `prompt_regression_tests`。这些表用于记录 provider/model/prompt version、input evidence hash、output hash、token usage、cost、review status 和回滚点；系统不把模型输出自动提交到 Google Ads，不把 PII、Cookie、验证码或账号凭据发送给模型。

Creative Angle Library 可扩展 `creative_angles`、`creative_asset_versions`、`creative_feedback_events`、`angle_performance_snapshots` 和 `creative_banned_patterns`，用于保存 angle 定义、素材版本、页面证据 hash、policy status、paid RPV、buyer reject、AdSense deduction、投诉和复盘决策。它只服务于素材迭代、Prompt 回写、人工审核和回滚，不生成虚假评价、不夸大 claim、不自动提交广告后台，也不通过补点击或模拟访问验证素材。

竞品广告和 SERP 情报可扩展 `competitor_market_snapshots`、`competitor_ad_observations` 和 `market_angle_briefs`，用于保存人工观察的 query、country、language、device、截图路径、广告主 domain、angle tags、claim risk、页面差距和 brief 结论。系统只做公开情报记录和创意 brief，不点击竞品广告、不批量抓取 SERP/Transparency Center、不复制素材、不仿冒品牌，也不用代理/指纹模拟地区。

### 4.5 投放草稿

字段：

- Campaign 名称、渠道、国家、语言、预算、出价策略。
- Ad Group 名称、关键词。
- 广告标题、描述、最终 URL。
- 审核状态：draft、reviewing、approved、exported、paused。

导出：

- Google Ads Editor CSV。
- Google Ads Scripts JSON payload。

Scripts JSON payload 配套 `scripts/google_ads_script_payload_preview.js`。该模板默认只做安全校验和 bulk upload preview，要求 `no_cookie_automation=true`、`requires_human_approval=true`，不直接 apply 高风险变更。

投放草稿状态流为 draft、reviewing、approved、exported、paused、rejected。状态变化用于内部审批和审计，写入 `audit_logs`；导出 CSV 或 Scripts JSON 只是生成待审核 payload，不代表系统已经向 Google Ads 发布广告。

Google Ads Editor CSV 和 Bulk Upload 的批量变更边界见 [Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册](google_ads_editor_csv_bulk_upload_governance.md)。第一版已实现 `/bulk-upload` 和 `bulk_upload_reviews`：表中保存 offer/campaign 绑定、export_type、batch_id、csv_hash、payload_hash、row_count、keyword_count、ad_count、target_customer_id、account_timezone、currency、expected_budget_delta、url_change_count、high_risk_change_count、preflight_status、preview_status、editor_check_status、post_status、default_paused、human_review、change_history_attached、rollback_plan、target_customer_confirmed、policy_review_complete、Bulk Upload Score、risk_level、recommended_action、budget_delta_percent、change_scope、blockers、status、notes 和 source_urls；`/bulk-upload/<id>/status` 更新 preview_ready、approved_for_manual_post、posted_manual、partial_error、rollback_review、blocked 等内部状态并写入 `audit_logs`。新建结构建议默认 paused，并把 Editor 检查、Bulk Upload preview、Change history 和失败行写回审计链；系统不自动打开 Editor、不自动登录 Google Ads、不自动点击发布按钮。

Campaign 命名、Labels、UTM/SubID 和维度治理 V1 已实现 `/taxonomy-governance` 和 `taxonomy_reviews`：表中保存 campaign/ad group name、labels、UTM、ValueTrack、custom parameter、SubID map、dimension dictionary version、parameter map version、landing/link/creative version、payload hash、report join gap、gclid/click_id 保留、PII/敏感属性检查、Taxonomy Score、risk_level、recommended_action、blockers、status、notes 和 source_urls；状态更新写入 `audit_logs`。后续可拆分 `dimension_dictionary`、`campaign_name_registry`、`tracking_parameter_maps`、`label_snapshots`、`version_registry` 和 `report_join_audits`。这些表用于保存 campaign/ad group 命名枚举、label 快照、UTM/ValueTrack/custom parameter/subid 映射、landing/link/creative/payload hash 以及报表 join 缺口；不作为多租户模型，也不保存 Cookie、代理池、浏览器指纹或后台登录凭据。详细规则见 [Campaign 命名、Labels、UTM/SubID 与维度治理手册](campaign_taxonomy_naming_label_dimension_governance.md)。

### 4.6 指标导入和 ROI 分析

导入字段：

- 日期、Offer、Campaign、Ad Group、渠道、国家、设备。
- impressions、clicks、cost、conversions、revenue。

计算：

- CPC = cost / clicks。
- CTR = clicks / impressions。
- CVR = conversions / clicks。
- RPV = revenue / clicks。
- Profit = revenue - cost。
- ROI = profit / cost。

建议规则：

- 有消耗无收入：暂停检查。
- ROI 小于止损阈值：降预算或暂停。
- ROI 高且样本足够：可扩量。
- CTR 高但 RPV 低：检查素材承诺和页面匹配。
- CPC 高且 Quality Score/页面审计差：先修页面和相关性。

CPA/CPL/Lead arbitrage 里，第一版指标表只保存聚合收入；业务上必须区分 submitted、accepted、approved、rejected、paid。短期可以用 CSV 导入 approved/paid revenue 和 `/risk-audits` 记录拒付原因；后续可扩展 `lead_quality_daily` 和 `lead_rejection_summary`，把 buyer feedback、postback 状态和 reject reason 纳入预算建议。

Lead Buyer 合同口径后续可扩展 `lead_buyer_contracts`、`lead_buyer_ios`、`lead_buyer_offer_terms`、`lead_status_definitions`、`lead_return_windows`、`lead_reject_reason_codes`、`lead_buyer_cap_snapshots`、`lead_buyer_postback_events`、`lead_buyer_invoice_lines`、`lead_buyer_payment_receipts` 和 `lead_return_dispute_cases`。这些表用于保存 accepted、qualified、billable、approved、paid、return window、scrub、invoice、payment 和 dispute evidence；系统不自动生成 lead、不补字段、不模拟联系、不绕过 buyer 风控。

转化信号质量治理需要把 conversion action、conversion goal、primary/secondary、conversion value、offline import、Enhanced Conversions、conversion lag 和 bid strategy learning 放到同一个审计视角。V1 已实现 `/conversion-signals` 和 `conversion_signal_reviews`：表中保存 offer/campaign 绑定、conversion_goal_name、conversion_action_name、action_stage、primary_status、recommended_primary_status、value_mode、bid_strategy、traffic_scope、weekly conversions/approved/paid、reported value、approved/paid rate、click_id coverage、offline match rate、duplicate rate、average/p95 lag、incident_count、segment_granularity、policy_consent、customer_data、offline_import、transaction_id、lag_stability、bid_strategy_status、goal_change_summary、affected_campaigns、value/dedupe/lag/diagnostics notes、rollback_plan、evidence flags、score_components、Signal Quality Score、risk_level、recommended_action、bid_readiness、expected_paid_value、safe_target_cpa、blockers、status、notes 和 source_urls；`/conversion-signals/<id>/status` 更新 tracking_fix、dedupe_fix、value_review、lag_review、goal_review、secondary_only、primary_candidate、bid_ready、blocked 等内部状态并写入 `audit_logs`。后续可扩展 `conversion_signal_definitions`、`conversion_goal_versions`、`conversion_signal_quality_daily`、`offline_conversion_import_runs`、`offline_conversion_import_errors`、`bid_strategy_learning_snapshots`、`conversion_value_adjustments` 和 `conversion_signal_incidents`。这些表只保存信号定义、评分、导入诊断、学习状态和事故复盘，不自动登录后台、不接管 Cookie、不自动改 conversion goal、不伪造转化或刷量。

CRM 阶段和 buyer feedback 映射 V1 已实现 `/crm-value-mapping` 和 `crm_value_mapping_reviews`：表中保存 offer/campaign 绑定、buyer_name、vertical、geo、source_system、buyer_feedback_source、source_stage、standard_stage、buyer_status、conversion_action_name、conversion_action_role、primary_recommendation、value_mode、recommended_upload_policy、payout、approved/paid/return rate、variable_cost、weekly_stage_count、weekly_unique_leads、rejected/returned/duplicate、click_id_match_rate、import_success/error、average_stage_lag、return_window、transaction_id_status、adjustment_rule_status、import_batch_status、diagnostics_status、consent_status、PII handling、stage/action/value/transaction/import/adjustment/lag/diagnostics notes、rollback_plan、evidence flags、score_components、CRM Mapping Score、risk_level、recommended_action、expected_value、blockers、status、notes 和 source_urls；`/crm-value-mapping/<id>/status` 更新 stage_map_review、action_map_review、value_review、dedupe_fix、import_qa、adjustment_review、lag_review、secondary_only、primary_candidate、upload_candidate、blocked 等内部状态并写入 `audit_logs`。后续可扩展 `crm_stage_maps`、`buyer_feedback_stage_maps`、`conversion_action_maps`、`offline_conversion_import_batches`、`offline_conversion_import_rows`、`conversion_value_versions`、`conversion_adjustment_events`、`conversion_diagnostics_snapshots`、`lead_value_calibration_runs` 和 `crm_ads_signal_incidents`。这些表用于保存 stage mapping、value mode、transaction_id、batch hash、diagnostics、match rate、returned/rejected adjustment 和 reviewer；系统不自动上传、不自动改 primary、不生成 lead、不补 postback、不伪造 conversion。

决策窗口治理需要把 data freshness、conversion lag、approval lag、settlement lag 和 payment lag 变成预算动作前的状态机。第一版已实现 `/decision-windows` 和 `decision_window_reviews`：表中保存 offer/campaign 绑定、data_status、revenue_status、conversion_lag_days、approval_lag_days、settlement_lag_days、sample_clicks、approved_revenue、paid_revenue、source_quality、incident_state、score、maturity、recommended_action、blockers、status、notes 和 source_urls；`/decision-windows/<id>/status` 更新 waiting、ramp_ready、blocked、closed 等内部处理状态并写入 `audit_logs`。它只产生等待、止损、小幅扩量或关闭建议，不自动改预算、不调用 Cookie 后台、不生成点击、展示、转化或收入。后续可扩展 `decision_window_profiles`、`conversion_lag_profiles`、`revenue_lag_profiles`、`cohort_maturity_daily`、`revenue_status_aging`、`budget_ramp_decisions`、`settlement_close_runs` 和 `decision_window_incidents`。

预算节奏治理需要把 current budget、proposed budget、test budget、hard stop、safe CPC、actual CPC、sample clicks、revenue maturity、cash buffer 和 overdelivery exposure 放到同一个扩量门禁里。第一版已实现 `/budget-pacing` 和 `budget_pacing_reviews`：表中保存 current_daily_budget、proposed_daily_budget、test_budget、hard_stop、spend_to_date、approved_revenue、paid_revenue、safe_cpc、actual_cpc、sample_clicks、data_status、revenue_status、source_quality、incident_state、cash_buffer_days、overdelivery_buffer_percent、score、risk_level、recommended_action、increase_percent、remaining_test_budget、remaining_hard_stop、blockers、status、notes 和 source_urls；`/budget-pacing/<id>/status` 更新 approved_for_manual_change、reduced、blocked、closed 等内部处理状态并写入 `audit_logs`。它只给人工预算评审提供证据，不修改 `campaign_drafts.daily_budget`，不自动登录后台，不自动应用 Recommendations，也不绕过账单、预算或账号风控。

电话和表单 Lead 后续可扩展 `lead_form_versions`、`lead_consent_events`、`lead_call_events`、`call_tracking_numbers`、`lead_buyer_handoffs`、`lead_status_history`、`lead_suppression_events`、`lead_compliance_audits` 和 `call_recording_reviews`。这些表用于 consent 证据、DNC/撤回同意、录音披露、call duration、buyer handoff、approved/paid 状态和投诉复盘；第一版不保存完整 PII、不保存录音、不做自动外呼或短信群发。

Call Tracking、DNI 和电话归因治理后续可扩展 `call_tracking_number_pools`、`call_tracking_numbers`、`dni_assignment_events`、`call_log_events`、`call_disposition_events`、`call_recording_reviews`、`call_attribution_reconciliations`、`call_conversion_maps` 和 `call_quality_daily`。这些表用于保存 number pool、DNI swap、Google forwarding number、provider_call_id、tracking_number_hash、caller_hash、duration、disposition、recording status、CRM ID 和 Call Attribution Quality Score；系统不自动拨打电话、不制造 call duration、不伪造录音或 disposition、不自动改 conversion action。

Pay-per-call 和 Call Buyer Routing 治理后续可扩展 `call_buyer_accounts`、`call_targets`、`call_routing_plans`、`call_flow_versions`、`call_buyer_cap_snapshots`、`call_duration_payout_rules`、`call_duplicate_rules`、`call_buyer_disposition_events`、`call_buyer_quality_daily` 和 `call_dispute_cases`。这些表用于保存 buyer/target、routing plan、IVR/call flow、duration payout、duplicate caller、buyer cap/hours、buyer disposition、revenue/payout 和 Call Buyer Quality Score；系统不自动拨号、不生成 synthetic calls、不伪造 duration/disposition/recording/payout。

Lead Consent Proof 和证据链治理后续可扩展 `lead_consent_versions`、`lead_consent_events`、`lead_certificate_refs`、`lead_page_snapshots`、`buyer_disclosure_versions`、`lead_suppression_sync_events`、`lead_consent_dispute_cases` 和 `consent_proof_quality_daily`。这些表用于保存 consent text hash、certificate/token 引用、page snapshot hash、buyer disclosure、contact channel scope、DNC/opt-out、handoff evidence 和 dispute evidence pack；系统不伪造 consent，不自动 post 给未披露 buyer，不把 PII 写入 URL/subid/log/prompt。

Lead Form 漏斗后续可扩展 `lead_form_versions`、`lead_form_fields`、`lead_form_step_events`、`lead_form_error_events`、`lead_form_abandon_events`、`lead_form_consent_blocks`、`lead_form_disclosure_versions`、`lead_form_quality_scores` 和 `form_buyer_feedback_daily`。这些表用于字段用途、分步漏斗、错误率、放弃率、disclosure/consent 版本、mobile UX 和 buyer feedback；默认不保存完整 PII，不自动提交表单、不补字段、不伪造 lead。

Ping/Post 和 buyer routing V1 已实现 `/ping-post-routing` 和 `ping_post_routing_reviews`。系统保存 routing mode、lead type、consent scope、buyer disclosure、ping field scope、PII level、suppression/DNC、cap snapshot、fallback、buyer feedback、source policy、buyer count、pinged/accepted/posted buyers、cap remaining、lead age、ping latency、expected bid、fallback payout、accept/qualification/paid/no-buyer/reject/duplicate/complaint rate、fields sent schema、routing rule、reject reason map、fallback policy、buyer feedback plan、consent evidence、Routing Quality Score、expected payable value、safe CPL、blockers、status 和 source_urls；状态更新写入 `audit_logs`。后续可拆分 `lead_buyer_accounts`、`lead_routing_rules`、`lead_ping_events`、`buyer_bid_responses`、`lead_post_events`、`lead_cap_snapshots`、`buyer_feedback_events`、`lead_consent_share_records`、`lead_suppression_checks` 和 `routing_quality_decisions`。这些表用于更细地记录最小化 ping 字段、buyer bid/accept/reject、exclusive/shared/aged 边界、cap snapshot、no buyer、consent 分享证据和 Routing Quality Score；系统不做未披露转售、不保存不必要完整 PII、不自动 post lead、不自动外呼或短信、不绕过 DNC/TCPA、不用 Cookie 后台操作。

Lead Freshness、Aged Lead 和 Recontact Window 治理后续可扩展 `lead_freshness_profiles`、`lead_age_snapshots`、`lead_recontact_policies`、`lead_recontact_attempts`、`aged_lead_inventory_batches`、`aged_lead_buyer_terms`、`lead_age_quality_daily`、`lead_recycled_handoff_history` 和 `lead_freshness_incidents`。这些表用于保存 original_submit_time、lead_age_bucket、first_response_time、consent age、suppression snapshot、buyer age terms、payout tier、contact disposition 和 Freshness Quality Score；系统不自动拨号、不短信群发、不伪造 timestamp、不把 aged lead 当 fresh lead、不刷新旧 consent。

Lead validation、suppression 和 PII 治理后续可扩展 `lead_validation_rules`、`lead_validation_events`、`lead_identifier_hashes`、`lead_duplicate_checks`、`lead_suppression_records`、`lead_privacy_requests`、`lead_retention_policies`、`lead_data_access_logs`、`lead_export_reviews`、`lead_validation_score_daily` 和 `buyer_reject_reason_maps`。这些表用于保存字段白名单、hash 去重、suppression/DNC/opt-out 状态、privacy request、retention/deletion、访问审计和 reject reason 修复闭环；默认不保存完整 PII，不把 PII 写入 URL/subid/log/prompt，不生成或补填用户资料。

Speed-to-Lead 和联系 SLA 治理后续可扩展 `lead_contact_sla_policies`、`lead_contact_attempts`、`lead_contact_dispositions`、`call_center_capacity_snapshots`、`buyer_operating_hours`、`lead_callback_tasks`、`lead_opt_out_sync_events`、`call_recording_qa_reviews` 和 `contact_quality_score_daily`。这些表用于记录 first attempt SLA、attempt cadence、call disposition、capacity、missed call、DNC/opt-out sync、recording QA 和 Contact Quality Score；系统不自动拨号、不短信群发、不保存录音文件、不伪造通话或 call duration。

Buyer Capacity 和 Dayparting V1 已实现 `/buyer-capacity` 和 `buyer_capacity_reviews`：表中保存 offer/campaign 绑定、buyer_name、vertical、geo、buyer/account/user/call-center timezone、cap_type、cap_period、cap_limit、cap_used、elapsed_operating_day_percent、expected_next_hour_leads、expected_daily_leads、hourly_contact_capacity、current_hour_capacity_used、expected_paid_value_per_lead、accepted/qualified/paid rate、no_buyer/missed_contact/after_hours rate、cap_last_confirmed、feedback_sla、first_attempt_sla、cap_confidence、hours/ad_schedule/timezone/holiday alignment、fallback_status、source_quality、overdelivery_guardrail、operating_hours、cap_reset_rule、holiday_calendar、ad_schedule_summary、no_buyer_reason_map、routing_fallback_policy、dayparting_basis、evidence flags、Capacity Quality Score、risk_level、recommended_action、cap_usage、projected usage、safe leads、safe media spend、blockers、status、notes 和 source_urls；`/buyer-capacity/<id>/status` 更新 cap_refresh、hours_review、schedule_review、holiday_review、routing_review、reduce_budget、pause_traffic、test_ready、scale_ready、blocked 等内部状态并写入 `audit_logs`。后续可拆分 `buyer_capacity_profiles`、`buyer_operating_hours`、`buyer_holiday_calendars`、`buyer_cap_snapshots`、`buyer_capacity_pacing_daily`、`buyer_capacity_pacing_hourly`、`buyer_no_buyer_events`、`buyer_capacity_incidents`、`ad_schedule_alignment_reviews` 和 `capacity_quality_score_daily`。这些表用于保存 cap、reset、hours、holiday、capacity、no buyer、after-hours、timezone、ad schedule 和 Capacity Quality Score；系统不自动登录后台、不自动改 schedule/预算/routing、不自动外呼或补 lead。

Appointment Lead 和 Booking 治理 V1 已实现 `/appointment-leads` 和 `appointment_lead_reviews`：表中保存 offer/campaign 绑定、buyer_name、vertical、service_type、geo、appointment_platform、payout_event、payout_amount、estimated_cpc、click_to_request/request_to_book/confirmation/show/completed/paid rate、cancel/no-show/duplicate/reschedule rate、reminder/no-show cost、available_slots、expected_bookings、lead_age、slot_delay、calendar_capacity_status、timezone_status、reminder_channel、reminder_consent_status、confirmation_process_status、buyer_terms_status、status_map、slot_policy、reminder_policy、no_show_reason_map、conversion_mapping、payout_definition_clear、duplicate_window_defined、calendar/reminder/offline evidence、Booking Quality Score、risk_level、recommended_action、expected value、safe CPC、safe appointment spend、blockers、status、notes 和 source_urls；`/appointment-leads/<id>/status` 更新 triage、calendar_review、reminder_review、buyer_terms_review、test_ready、scale_ready、blocked 等内部状态并写入 `audit_logs`。后续可拆分 `appointment_booking_events`、`appointment_status_history`、`appointment_slot_inventory`、`appointment_reminder_events`、`appointment_no_show_events`、`appointment_buyer_terms`、`appointment_quality_daily`、`calendar_capacity_snapshots` 和 `appointment_conversion_maps`。这些表用于保存 booked、confirmed、showed、paid、cancel/no-show、calendar capacity、slot timezone、reminder consent、buyer payout event 和 Booking Quality Score；系统不自动创建预约、不群发提醒、不伪造 showed/paid、不把 booked 默认设为 primary conversion。

CPL 垂类经济 V1 已实现 `/cpl-verticals` 和 `cpl_vertical_reviews`：表中保存 offer/campaign 绑定、vertical、subvertical、country、buyer_type、payout_model、payout_amount、estimated_cpc、landing_cvr_percent、accepted/qualified/paid rate、deduction/chargeback、feedback_lag_days、contact_sla_minutes、qualification_fields、sensitive_fields、reject_reason_map、accepted_definition、paid_definition、policy_requirements、forbidden_claims、required_fields_mapped、reject_reason_map_ready、consent_disclosure_status、PII 最小化、license_required、license_evidence_present、buyer_terms_status、source_quality、policy_risk、data_sensitivity、human_review、Vertical Fit Score、risk_level、recommended_action、effective_payout、expected_value_per_click、safe_cpc、cpc_margin_percent、blockers、status、notes 和 source_urls；`/cpl-verticals/<id>/status` 更新 field_mapping、buyer_terms_review、policy_review、test_ready、scale_ready、blocked 等内部状态并写入 `audit_logs`。后续可拆分 `vertical_profiles`、`vertical_qualification_fields`、`vertical_reject_reason_maps`、`vertical_policy_requirements`、`vertical_buyer_acceptance_benchmarks`、`vertical_feedback_lag_profiles`、`vertical_fit_scores` 和 `vertical_test_plans`。这些表用于区分保险、贷款/债务、法律、本地服务、教育、医疗、B2B 等不同 lead 的资格字段、paid definition、reject reason、policy requirement、feedback lag 和 Vertical Fit Score；不保存不必要 PII，不伪造资质，不自动绕过垂类认证或审核。

Insurance、Medicare / ACA 和 Final Expense Lead 治理后续可扩展 `insurance_vertical_profiles`、`insurance_qualification_fields`、`insurance_offer_eligibility_rules`、`insurance_enrollment_windows`、`insurance_buyer_terms`、`insurance_buyer_acceptance_events`、`insurance_reject_reason_maps`、`insurance_claim_reviews`、`insurance_license_authorization_refs`、`insurance_consent_reviews`、`insurance_offline_value_maps` 和 `insurance_quality_daily`。这些表用于保存 subvertical、state/county、coverage type、eligibility bucket、open enrollment / SEP / Medicare window、official source URL、licensed agent/broker 或 buyer authorization reference、buyer accepted/qualified/paid 口径、reject reason、consent/disclosure、claim review、offline stage 和 Insurance Lead Quality Score；系统不冒充 Medicare/Marketplace/carrier，不保存不必要敏感数据，不自动外呼或短信群发，不把 submitted、duration 或 booked 默认当 paid revenue。

Loan、Mortgage、Credit 和 Debt Lead 治理后续可扩展 `financial_vertical_profiles`、`financial_qualification_fields`、`financial_offer_eligibility_rules`、`financial_disclosure_versions`、`financial_buyer_terms`、`financial_buyer_acceptance_events`、`financial_reject_reason_maps`、`financial_claim_reviews`、`financial_license_authorization_refs`、`financial_comparison_ranking_reviews`、`financial_offline_value_maps` 和 `financial_quality_daily`。这些表用于保存 subvertical、state、loan/debt/credit bucket、homeowner/property bucket、license/NMLS 或 buyer authorization reference、financial disclosure、buyer disclosure、compensation/ranking disclosure、buyer accepted/application/funded/paid 口径、reject reason、claim review、offline stage 和 Financial Lead Quality Score；系统不伪造申请、收入、信用、身份或资质，不冒充 lender/government/servicer，不保存不必要敏感数据，不自动外呼或短信群发，不把 submitted、accepted、prequalified 或 duration 默认当 funded/paid revenue。

Legal Case Intake、Mass Tort 和 Personal Injury Lead 治理后续可扩展 `legal_vertical_profiles`、`legal_qualification_fields`、`legal_case_type_rules`、`legal_attorney_buyer_terms`、`legal_intake_events`、`legal_attorney_review_events`、`legal_reject_reason_maps`、`legal_claim_reviews`、`legal_referral_disclosure_versions`、`legal_conflict_check_snapshots`、`legal_offline_value_maps` 和 `legal_quality_daily`。这些表用于保存 practice_area、state/jurisdiction、case_type、incident date bucket、injury/damages bucket、representation status、attorney/law firm/intake center/lead generator role、disclosure/consent、attorney reviewed、retainer signed、case accepted、reject reason、claim review、offline stage 和 Legal Lead Quality Score；系统不伪造案件、事故、伤害或 signed retainer，不冒充律师/律所/法院/政府，不保存不必要敏感案情，不自动外呼或短信群发，不把 submitted、intake qualified、booked 或 duration 默认当 paid case。

Home Services、Solar 和 Local Services Lead 治理后续可扩展 `home_service_vertical_profiles`、`home_service_qualification_fields`、`contractor_buyer_profiles`、`contractor_license_refs`、`service_area_rules`、`dispatch_capacity_snapshots`、`home_service_lead_events`、`home_service_disposition_events`、`lsa_credit_dispute_events`、`home_service_claim_reviews`、`solar_qualification_reviews`、`home_service_offline_value_maps` 和 `home_service_quality_daily`。这些表用于保存 service_category、service_type、zip/city、service_area_match、urgency、property/homeowner bucket、contractor license/insurance、business hours/capacity、disposition、booked/showed/quoted/sold/completed、LSA credit/dispute、solar savings claim、paid value 和 Home Services Lead Quality Score；系统不伪造本地地址、Google badge、license、insurance、review 或 job outcome，不保存家庭门禁/完整地址等不必要敏感信息，不自动外呼或短信群发，不把 submitted、call click、booked 或 LSA charged lead 默认当 paid job。

Education、Career Training 和 Student Lead 治理后续可扩展 `education_vertical_profiles`、`education_program_profiles`、`education_authorization_refs`、`education_qualification_fields`、`education_buyer_terms`、`education_buyer_acceptance_events`、`education_reject_reason_maps`、`education_claim_reviews`、`education_financial_aid_disclosure_versions`、`education_enrollment_events`、`education_offline_value_maps` 和 `education_quality_daily`。这些表用于保存 program_type、school_type、campus/online modality、state authorization、accreditation、licensure/transferability proof、program interest、eligibility bucket、financial aid/student loan disclosure、application/enrollment/class start/paid stage、reject reason、claim review、offline stage 和 Education Lead Quality Score；系统不伪造学生资料、学历、成绩、FAFSA、身份、授权、认证、录取、就业、薪资或 enrollment，不保存不必要教育/财务敏感数据，不自动外呼或短信群发，不把 inquiry、application started 或 advisor call 默认当 paid enrollment。

Healthcare、Medical Appointment 和 Clinic Lead 治理后续可扩展 `healthcare_vertical_profiles`、`healthcare_provider_refs`、`healthcare_qualification_fields`、`healthcare_claim_reviews`、`healthcare_tracking_reviews`、`healthcare_appointment_events`、`healthcare_buyer_terms`、`healthcare_reject_reason_maps`、`healthcare_offline_value_maps` 和 `healthcare_quality_daily`。这些表用于保存 service_type、provider/clinic role、state/city、license/insurance/source URL、field sensitivity、PHI/health data classification、privacy/consent version、tracking review、health claim proof、appointment requested/booked/confirmed/showed/treated/paid、reject reason、offline value 和 Healthcare Lead Quality Score；系统不伪造医生、诊所、资质、保险网络、预约、到诊或治疗结果，不保存不必要 PHI，不把健康状态写入 URL/event/subid，不自动外呼或短信群发，不把 submitted、call duration、requested 或 booked 默认当 paid patient。

B2B SaaS、Professional Services 和 Demo Lead 治理后续可扩展 `b2b_vertical_profiles`、`b2b_qualification_fields`、`b2b_account_fit_rules`、`b2b_persona_rules`、`b2b_claim_reviews`、`b2b_pipeline_events`、`b2b_reject_reason_maps`、`b2b_offline_value_maps` 和 `b2b_quality_daily`。这些表用于保存 category、ICP、company size、industry、role/persona、use case、budget/timeline bucket、consent/disclosure、trademark/software/customer logo/security claim proof、raw/valid/MQL/SAL/SQL/opportunity/won/PQL stage、reject reason、offline value 和 B2B Lead Quality Score；系统不伪造公司、职位、预算、采购意向、客户 logo、review、security certification 或 pipeline，不抓取/滥用个人联系人，不自动外呼或短信群发，不把 download、trial、form submit 或 demo request 默认当 paid pipeline。

Crypto、Investment 和 Trading Lead 治理后续可扩展 `financial_offer_profiles`、`financial_license_refs`、`financial_claim_reviews`、`financial_risk_disclosures`、`financial_lead_events`、`financial_reject_reason_maps`、`financial_offline_value_maps` 和 `financial_quality_daily`。这些表用于保存 product_type、target_geo、Google certification、license/registration、risk disclosure、performance/testimonial/regulator claim proof、lead/signup/KYC/funded/first trade/paid/chargeback stage、reject reason、offline value 和 Crypto / Investment Lead Quality Score；系统不伪造监管资质、收益、KYC、交易、入金、提现或 paid event，不收 seed phrase/private key/KYC 文件，不绕 Google/地区认证，不自动外呼或短信群发，不把 submit、install、signup 或 KYC started 默认当 paid investor。

Employment、Recruiting 和 Staffing Lead 治理后续可扩展 `employment_vertical_profiles`、`employment_job_orders`、`employment_qualification_fields`、`employment_claim_reviews`、`employment_targeting_reviews`、`employment_candidate_events`、`employment_reject_reason_maps`、`employment_offline_value_maps` 和 `employment_quality_daily`。这些表用于保存 job_category、buyer_type、employer/recruiter role、job order、pay/remote/employment type proof、HEC/targeting review、candidate data sensitivity、lead/screened/qualified/interview/hire/start/paid stage、reject reason、offline value 和 Employment Lead Quality Score；系统不伪造岗位、雇主、简历、证书、面试、入职或 paid event，不做歧视性筛选，不保存不必要 SSN/证件/银行信息，不自动外呼或短信群发，不把 submit、resume upload、call connected 或 interview scheduled 默认当 paid placement。

Gambling、Sweepstakes 和 Sports Betting Lead 治理后续可扩展 `gambling_offer_profiles`、`gambling_license_refs`、`gambling_claim_reviews`、`gambling_responsible_messages`、`gambling_lead_events`、`gambling_reject_reason_maps`、`gambling_offline_value_maps` 和 `gambling_quality_daily`。这些表用于保存 product_type、target_geo、Google certification、operator license、age/geo/self-exclusion controls、responsible gambling message、bonus/sweepstakes terms proof、registration/KYC/deposit/wager/NGR/paid stage、reject reason、offline value 和 Gambling Lead Quality Score；系统不伪造 license、age、geo、KYC、deposit、wager、NGR 或 paid event，不绕 certification/geo/self-exclusion，不保存 payment/KYC 高敏资料，不自动外呼或短信群发，不把 install、registration 或 bonus claimed 默认当 paid player。

Addiction Treatment、Rehab 和 Behavioral Health Lead 治理后续可扩展 `addiction_offer_profiles`、`addiction_provider_refs`、`addiction_privacy_reviews`、`addiction_claim_reviews`、`addiction_admissions_events`、`addiction_reject_reason_maps`、`addiction_offline_value_maps` 和 `addiction_quality_daily`。这些表用于保存 service_type、provider/referral role、certification/license source URL、Part 2/HIPAA tracking review、crisis SOP、claim proof、call/assessment/verification/admitted/started/paid stage、reject reason、offline value 和 Addiction Lead Quality Score；系统不伪造 provider、certification、license、insurance、clinical assessment、admission、treatment start 或 paid event，不绕 LegitScript/Google certification，不保存不必要 SUD/PHI 高敏资料，不自动外呼或短信群发，不把 call duration、form submit 或 admissions call 默认当 paid treatment。

Government Services、Immigration 和 Public Benefits Lead 治理后续可扩展 `government_service_profiles`、`government_authorization_refs`、`government_fee_disclosures`、`government_claim_reviews`、`government_identity_data_reviews`、`government_service_events`、`government_reject_reason_maps`、`government_offline_value_maps` 和 `government_quality_daily`。这些表用于保存 service_type、agency、geo、official relationship、Google certification / government authorization / professional role source URL、official fee、service fee、refund policy、approval/expedite/benefit claim proof、identity data minimization、lead/consult/prepared/filed/receipt/issued/paid stage、reject reason、offline value 和 Government Services Lead Quality Score；系统不冒充政府或授权 provider，不伪造 USCIS/IRS/SSA/DMV/passport/vital records 关系，不提供未经授权法律/移民/税务建议，不保存不必要 SSN/passport/A-number/tax/benefit/login 文件，不自动外呼或短信群发，不把 quiz、lead submit、call connected 或 document checklist 默认当 issued / paid outcome。

Lead Pricing 和 payout negotiation V1 已实现 `/lead-pricing` 和 `lead_pricing_reviews`：表中保存 offer/campaign 绑定、buyer_name、vertical、geo、source_type、exclusivity、payout_model、headline_payout、unit_payout、proposed_payout、minimum_acceptable_payout、currency、estimated_cpc、click_to_lead_rate_percent、accepted/qualified/approval/paid rate、return_rate_percent、scrub_buffer_percent、chargeback_rate_percent、variable/tracking/content cost、cashflow_cost_percent、cap_limit、expected_volume、return_window_days、payment_term_days、qualification_definition、rate_card_evidence、negotiation_evidence、reject_reason_summary、invoice_terms、quality_evidence_status、source_transparency、consent_evidence、reject_reason_map_ready、invoice_evidence、dispute_reserve_present、buyer_terms_status、human_review、Lead Pricing Score、risk_level、recommended_action、effective_payout、paid_epc、safe_cpc、margin_per_click、reserve_amount、blockers、status、notes 和 source_urls；`/lead-pricing/<id>/status` 更新 rate_card_review、evidence_needed、buyer_terms_review、reserve_review、negotiation_ready、test_ready、blocked 等内部状态并写入 `audit_logs`。后续可拆分 `lead_pricing_rate_cards`、`lead_payout_versions`、`lead_pricing_tiers`、`lead_pricing_floor_rules`、`lead_scrub_reserve_profiles`、`lead_buyer_price_negotiations`、`lead_pricing_experiments`、`lead_payment_term_profiles` 和 `lead_buyer_value_score_daily`。系统不自动谈价、不自动改 routing、不自动上传 conversion value、不生成 lead 或转化。

发布商变现套利里，当前 `metrics_daily.revenue` 是简化聚合字段，导入时优先使用 approved、finalized 或 paid 口径。若只能拿到 estimated revenue，应记录 safety factor、deduction_rate 和 finalization_ratio，等月度关账后再决定扩量。后续建议扩展 `publisher_metrics_daily`、`revenue_settlements` 和 `reconciliation_runs`，把 AdSense/GAM/AdX 日报、次月 finalized revenue、付款状态、扣量原因和来源隔离动作拆开保存。

订阅、试用和连续付费 Offer 需要把 signup、activation、renewal、refund、chargeback、clawback 和 net LTV 按 cohort 保存。第一版通过 `/offers`、`/calculators`、`/metrics/import`、`/risk-audits` 和 `/sources` 承接；后续可扩展 `subscription_offer_terms`、`subscription_cohort_daily`、`subscription_ltv_snapshots`、`refund_chargeback_events`、`cancellation_flow_audits`、`billing_disclosure_versions`、`ltv_value_feedback_runs` 和 `subscription_quality_decisions`。这些表只做证据、评分和回传建议，不隐藏条款、不阻碍取消、不伪造续费、不规避 chargeback。

来源质量治理需要把 source、publisher、placement、subid、buyer feedback、approved/paid revenue、deduction、invalid clicks、complaints 和 policy issues 连到同一个评分和名单记录。第一版已实现 `/source-quality` 和 `source_quality_reviews`：表中保存 offer/campaign 绑定、entity_type、source_name、publisher_name、placement_ref、subid、network、country、device、sample_url、transparency_level、tracking_completeness_percent、intent_fit_score、clicks、sessions、cost、reported/approved/paid/deducted revenue、invalid_click_rate_percent、complaint_count、buyer_reject_rate_percent、policy_issue_state、stop_control、consistency_days、Source Quality Score、quality_level、recommended_action、click_session_rate、approved_rate、paid_rate、deduction_rate、paid_roi、approved_roi、blockers、status、notes 和 source_urls；`/source-quality/<id>/status` 更新 allowlist、watchlist、quarantine、blocklist、retest 等内部名单状态并写入 `audit_logs`。后续可拆分 `traffic_sources`、`publisher_placements`、`source_quality_daily`、`source_quality_decisions`、`source_blocklist_entries`、`source_feedback_events` 和 `placement_exclusion_exports`。这些表只生成评分、名单、停源/恢复证据和排除清单建议，不买流量、不模拟访问、不通过 Cookie 后台改 placement。

流量供应商合同与争议治理应把 vendor、IO、line item、tracking appendix、reporting appendix、invoice、refund、credit、makegood 和 dispute case 与来源质量记录关联。第一版已实现 `/vendor-contracts` 和 `vendor_contract_reviews`：表中保存 offer/campaign 绑定、vendor_name、vendor_type、io_number、line_item_ref、contract_status、pricing_model、source_detail_level、tracking_appendix、reporting_appendix、quality_clause、refund_clause、stop_control、tracking_completeness_percent、report_delay_days、discrepancy_rate_percent、invalid_traffic_rate_percent、buyer_reject_rate_percent、budget_cap、spend_to_date、approved/paid revenue、invoice_amount、disputed_amount、refund_credit_amount、makegood_value、dispute_response_days、payment_terms_days、refund_terms_status、policy_issue_state、Vendor Contract Score、risk_level、recommended_action、amount_at_risk、paid_roi、approved_roi、invoice_dispute_rate、credit_coverage_rate、blockers、status、notes 和 source_urls；`/vendor-contracts/<id>/status` 更新 preapproved、active_test、active_scale、watchlist、dispute_open、suspended、blocked 等内部状态并写入 `audit_logs`。后续可拆分 `traffic_vendor_accounts`、`media_insertion_orders`、`media_io_line_items`、`vendor_tracking_appendices`、`vendor_report_imports`、`traffic_dispute_cases`、`traffic_dispute_evidence`、`vendor_credit_notes`、`makegood_plans` 和 `vendor_scorecards`。系统只保存合同和证据，不自动采购流量、不调用供应商 API 灌量。

广告位收益实验需要单独记录 page_template、ad_layout_version、ad_unit、position、viewable_impressions、ad_clicks、estimated/finalized revenue、CLS/LCP 和 refresh_type。后续可扩展 `ad_layout_versions`、`publisher_ad_unit_daily`、`ad_refresh_tests` 和 `page_experience_audits`；这些表只用于报表、审计和优化建议，不生成广告刷新、展示、点击或误点诱导能力。

Click -> Session -> Revenue 对账需要把 Google Ads clicks、server landing requests、GA4 sessions、offer clicks、postback、estimated/finalized revenue 拆开保存。后续可扩展 `landing_request_daily`、`click_session_reconciliation_runs`、`postback_events`、`revenue_status_daily` 和 `source_quality_segments`；所有修复必须保留原始记录和证据，不生成点击、session、conversion 或 postback。

RSOC / N2S 漏斗可扩展 `search_feed_partners`、`rsoc_page_reviews`、`rsoc_creative_rac_reviews`、`rsoc_funnel_daily`、`rsoc_query_group_daily`、`rsoc_source_quality_daily`、`rsoc_deduction_reports`、`rsoc_policy_incidents` 和 `search_feed_settlement_runs`，用于记录 AFS/Related Search 权限、PIF/RAC、上游创意、content page、query group、funnel RPM、finalized RPV、deduction、strike 和 partner 结算证据。系统只做审计和对账，不生成 feed 代码、不自动搜索、不点击广告、不修改 Google 返回元素。

Native / Advertorial / Presell 漏斗可扩展 `native_campaign_sources`、`native_creative_angles`、`advertorial_page_reviews`、`presell_disclosure_checks`、`native_source_quality_daily`、`native_buyer_feedback_daily` 和 `native_policy_incidents`，用于记录 source/publisher/placement、素材角度、标题/缩略图 claim、软文页内容、商业披露、CTA、buyer feedback、paid revenue、refund/scrub 和政策事故。系统只做复盘、审计和建议，不生成误导素材、不隐藏商业关系、不模拟点击或低质自然流量。

季节性和事件日历治理需要把官方日期、Google Trends、Keyword Planner、Insights、Search Terms、历史 paid revenue、Offer cap、页面 readiness、预算 ramp 和 post-peak exit 连接起来。第一版通过文档、`/sources`、`/calculators`、`/campaigns`、`/optimization` 和 `/tasks` 承接；后续可扩展 `event_calendars`、`seasonal_demand_forecasts`、`keyword_trend_snapshots`、`seasonal_readiness_checks`、`seasonal_budget_ramp_plans`、`seasonal_exit_rules`、`seasonality_adjustment_reviews` 和 `seasonal_postmortems`。这些表只做计划、审计和复盘，不自动追热点、不自动改预算或生成误导素材。

Google Ads 报表诊断可扩展 `google_ads_report_snapshots`、`search_term_diagnostics`、`auction_insight_daily`、`change_history_events`、`landing_page_performance_daily`、`asset_performance_snapshots` 和 `bid_strategy_diagnostics`，用于把 Search terms、Auction Insights、Change history、Report Editor、landing pages、RSA assets 和 bid strategy report 关联到 ROI 诊断和优化动作。系统只做导入、证据留存和建议，不自动接受 recommendations，不用 Cookie 后台抓报表。

Search Terms、否定词和 Query Mining 需要把真实 query、keyword、match type、network、device、landing version、cost、clicks、sessions、approved/paid revenue、buyer reject、intent fit、policy risk 和 conversion lag 放在同一个决策记录里。第一版已实现 `/query-mining` 和 `query_mining_reviews`：表中保存 offer/campaign 绑定、date_window、ads_customer_id、campaign_ref、ad_group_ref、keyword_text、keyword_match_type、search_term、search_term_match_type、query_intent、network、device、country、landing_version、source_file_hash、clicks、sessions、conversions、cost、approved_revenue、paid_revenue、buyer_reject_rate_percent、intent_fit_score、policy_risk、revenue_status、data_status、conversion_lag_days、brand_or_official、support_or_login、Query Mining Score、risk_level、recommended_action、negative_match_type、negative_level、click_session_rate、cpc、approved_rpv、paid_rpv、approved_roi、paid_roi、blockers、status、notes 和 source_urls；`/query-mining/<id>/status` 更新 negative_proposed、promotion_proposed、page_brief、risk_review、applied 等内部状态并写入 `audit_logs`。后续可拆分 `search_term_snapshots`、`query_mining_decisions` 和 `negative_keyword_registry`。它把真实 query 转成 negative、promote exact/phrase、split ad group、page brief、hold 或 pause 决策；系统只做报表导入、审核、CSV/Scripts preview 和复盘，不模拟搜索、不点击广告、不绕过搜索词隐私聚合、不用代理/指纹伪装地区。

归因、增量性和流量蚕食治理 V1 已实现 `/attribution` 和 `attribution_reviews`：表中保存 offer/campaign 绑定、test_type、attribution_model、hypothesis、treatment_scope、control_scope、split_method、date_window、primary_metric、guardrail_metrics、attributed_revenue、treatment_revenue、control_revenue、incremental_revenue、ad_cost、variable_cost、incremental_profit、i_roas、attributed_to_incremental_ratio、attributed/incremental conversions、sample_size、confidence_level、holdout_quality、revenue_status、data_status、brand/organic/remarketing/PMax-Broad cannibalization risk、Change history、single_variable_test、approved_paid_evidence、human_review、score、risk_level、recommended_action、blockers、status、notes 和 source_urls；`/attribution/<id>/status` 更新 holdout_planned、experiment_running、evidence_ready、small_ramp、scale_ready、cannibalization_review、blocked 等内部状态并写入 `audit_logs`。后续可拆分 `attribution_model_versions`、`attribution_model_comparisons`、`incrementality_tests`、`holdout_groups`、`lift_study_snapshots`、`cannibalization_checks`、`incremental_revenue_daily` 和 `incrementality_decisions`。系统只保存实验计划、证据和评审结论，不自动创建实验、不自动应用 winner、不伪造 control 或转化。

Google Ads Recommendations 和 Experiments 治理可扩展 `google_ads_recommendation_reviews`、`google_ads_experiment_plans`、`auto_apply_snapshots` 和 `recommendation_change_links`，用于保存 optimization score、recommendation type、受影响对象、风险等级、后端收入证据、实验假设、流量拆分、成功指标、Auto-apply 状态和 Change History 证据。系统只把平台建议转成待评审假设，不自动接受 recommendations，不无人值守改预算、出价、关键词、资产、conversion goal 或 Final URL。

异常监控、告警和止损队列可扩展 `alert_rules`、`alert_events`、`incident_cases` 和 `incident_evidence_links`，用于保存 rule_key、metric_scope、severity、threshold_json、lookback_window、trigger_values、evidence_urls、owner、containment、root_cause 和 postmortem。当前 `/optimization` 与 `optimization_actions` 是规则建议队列的 V1；系统允许把建议状态标记为 open、manual_review、resolved 或 dismissed，并把状态变化写入审计日志。状态变化只代表内部处理进度，不自动用 Cookie 后台改预算、补点击、伪造转化、切换账号或隐藏目的地。后续升级也只生成可审批动作。详细流程见 [异常监控、告警、止损队列与事故分诊手册](anomaly_monitoring_alerting_stoploss_incident_triage.md)。

Search 自动化诊断可扩展 `search_automation_controls`、`search_query_diagnostics`、`search_url_expansion_reviews`、`search_asset_auto_generation_reviews`、`search_brand_control_snapshots` 和 `dsa_page_feed_versions`，用于保存 AI Max、Broad Match、DSA、Final URL expansion、automatically created assets、brand controls、negative keywords、search terms、landing pages、claim review 和 paid revenue 证据。系统只做导入、审计、建议和人工审批记录，不自动开启 Search 自动化功能，不接受绕过审核、隐藏 URL 或伪造搜索流量的做法。

PMax / Demand Gen 自动化流量诊断可扩展 `pmax_campaign_controls`、`pmax_channel_performance_daily`、`pmax_search_theme_diagnostics`、`pmax_asset_group_snapshots`、`pmax_url_expansion_checks` 和 `demand_gen_audience_diagnostics`，用于保存 Final URL expansion、URL exclusions、Search themes、Audience signals、asset group、brand exclusions、channel/placement/asset/landing page report 和 paid revenue 证据。系统只做导入、复盘、止损建议和人工审批记录，不自动开启 PMax/Demand Gen，不用黑盒自动化替代可解释测试。

Geo、本地化、时区和币种分层可扩展 `geo_market_profiles`、`localized_page_versions`、`geo_device_metrics_daily`、`fx_rate_snapshots`、`timezone_reconciliation_runs` 和 `bad_geo_incidents`，用于记录 target country、language、device、location options、account timezone、source timezone、account currency、offer currency、fx rate、localized page 和 bad geo 证据。系统只做分层对账和审计，不用代理、指纹或 cloaking 伪装地区。

Portfolio 组合治理需要把 Offer、source、publisher、account、country、device、revenue partner、policy class、cash reserve 和 revenue status 放到同一个 exposure 视角。第一版已实现 `/portfolio-allocation` 和 `portfolio_allocation_reviews`：表中保存 portfolio_bucket、monthly_media_budget、proposed_allocation、spend_to_date、reported/pending/approved/finalized/paid/deducted revenue、单一 Offer/source/account/revenue partner 集中度、cash_reserve_days、source_quality、policy_risk、incident_state、Portfolio Allocation Score、risk_level、recommended_action、allocation_percent、remaining_monthly_budget、cash_at_risk、revenue_quality_ratio、blockers、status、notes 和 source_urls；`/portfolio-allocation/<id>/status` 更新 approved_for_manual_allocation、reduce_exposure、quarantine、waiting、closed 等内部状态并写入 `audit_logs`。它只生成组合分配建议和风险证据，不自动改预算、不登录后台、不绕过账单或账号风控。后续可拆分 `portfolio_budgets`、`portfolio_budget_allocations`、`portfolio_exposure_daily`、`portfolio_concentration_limits`、`portfolio_allocation_decisions`、`portfolio_cash_reserve_snapshots` 和 `portfolio_postmortems`。

账号/MCC/付款/验证治理可扩展 `account_governance_profiles`、`mcc_hierarchy_snapshots`、`account_access_reviews`、`billing_profile_checks`、`advertiser_verification_cases`、`agency_client_relationships`、`account_budget_controls` 和 `account_incident_evidence`，用于记录 owner、业务主体、付款主体、MCC 层级、访问权限、Advertiser Verification、代理/客户关系、account budget、付款和账号事故证据。系统只做账号资产治理和审计，不批量建号、不维护账号池、不用付款资料或代理关系规避政策执行。

AdSense 站点审核和 Policy Center 可扩展 `publisher_site_reviews`、`adsense_policy_center_issues`、`ad_serving_limit_events`、`publisher_site_readiness_checks` 和 `policy_review_requests`，用于记录 site review status、connection method、ads.txt、crawler access、policy issue type、ad serving status、affected URLs、traffic source、fix summary 和 review result。系统只做证据留存和恢复 SOP，不批量建站、不换域名规避审核、不生成流量。

发布商广告质量可扩展 `ad_quality_incidents`、`blocked_advertiser_domains`、`blocked_ad_categories`、`ad_review_center_snapshots` 和 `publisher_blocking_rule_versions`，用于记录 advertiser domain、creative summary、category、incident type、country/device、evidence、block/report 动作和 revenue impact。系统只做审计和证据留存，不点击广告、不模拟用户、不滥用投诉打击竞品。

域名和站点资产治理可扩展 `domain_assets`、`domain_history_checks`、`site_migration_plans`、`publisher_site_assets`、`ads_txt_asset_checks`、`final_url_change_reviews` 和 `domain_risk_audits`，用于记录 root domain、subdomain、tracking domain、站点用途、历史主题、过期域名风险、站点迁移、AdSense / GAM / AdX site status、ads.txt、seller ID、Final URL 变更和风险结论。系统只做资产台账、迁移计划、QA 和审计，不批量建站、不镜像站、不用换域名规避拒登、封禁或广告服务限制。

程序化供应链透明度可扩展 `publisher_sites`、`ads_txt_snapshots`、`sellers_json_checks`、`supply_chain_checks` 和 `demand_partner_accounts`，用于记录 domain、seller ID、DIRECT/RESELLER、sellers.json、schain、MCM 和 demand partner 关系。系统只能做 QA、证据留存和风险审计，不伪造 seller、ads.txt、sellers.json 或 schain。

GAM/AdX yield 实验可扩展 `gam_pricing_rule_versions`、`ad_unit_yield_daily`、`demand_partner_yield_daily`、`yield_experiments` 和 `line_item_delivery_snapshots`，用于记录 floor price、unified pricing rules、line item priority、Open Bidding partner、fill、eCPM、session RPM 和 finalized revenue。系统只做报表和审计，不自动调价、不制造请求/展示/点击，也不绕过买方过滤。

Header Bidding / Prebid.js 可扩展 `header_bidding_stack_versions`、`header_bidding_bidder_daily`、`header_bidding_auction_daily` 和 `header_bidding_debug_events`，用于记录 stack version、Prebid version、bidder、timeout、price granularity、floor、bid rate、win rate、render rate、GAM fill、viewability、CLS/LCP、consent、ads.txt 和 schain。系统只做 QA、报表和审计，不自动生成站点端 bidder 代码、不写入 GAM、不绕过 consent 或供应链透明要求。

### 4.7 链接轮换

合规用途：

- 已审核 URL 之间做 A/B 测试。
- 修复断链。
- 更新 UTM。
- 同主题 Offer 备用链接切换。

限制：

- 不允许审核页和用户页不一致。
- 每个链接版本记录原因、操作者、时间、目标 URL。
- 轮换任务默认需要人工确认。
- 链接计划状态流为 draft、reviewing、approved、rotated、paused、rejected；只有 approved 或 rotated 状态可以执行人工轮换。

### 4.7.1 追踪链 QA

上线、导出或换链接前，团队需要检查 Final URL、tracking template、Final URL suffix、ValueTrack、auto-tagging、parallel tracking、redirect chain 和 postback 参数是否一致。第一版用文档、来源库、风险审计和链接计划落地；后续可扩展 `url_test_runs`、`redirect_hops` 和 `tracking_templates` 表，但仍不做 cloaking、Cookie 后台接管或隐藏跳转。

### 4.8 审计日志

记录：

- 创建 Offer。
- 采集页面。
- 生成创意。
- 创建和导出投放草稿。
- 更新投放草稿评审状态。
- 导入指标。
- 生成优化建议。
- 更新优化建议状态。
- 链接轮换。

### 4.9 来源库

用途：

- 把 ADXKit 公开页面、Google Ads 政策、AdSense 无效流量政策、Lead Form / postback / buyer feedback 来源、MDN/OWASP/W3C 等资料沉淀为结构化来源。
- 每条来源记录主题、能力、URL、发布方、证据摘要、可信级别、复核状态和检索日期。
- 支撑高风险审计和 Markdown 文档更新。

边界：

- 来源库只记录资料，不触发后台登录、点击、流量、代理或 Worker 动作。
- 复核状态只表达知识库维护进度：candidate、accepted、needs_update、archived；状态更新写入审计日志，不触发投放动作。
- 产品公开页面只作为“产品宣称”的证据，不作为合规判断的唯一依据。

## 5. 数据模型

```mermaid
erDiagram
    offers ||--o{ landing_pages : has
    offers ||--o{ creatives : has
    offers ||--o{ campaign_drafts : has
    offers ||--o{ link_rules : has
    campaign_drafts ||--o{ metrics_daily : has
    offers ||--o{ metrics_daily : has
    offers ||--o{ optimization_actions : has
    audit_logs }o--|| offers : references

    offers {
      int id
      string name
      string vertical
      string country
      string language
      string payout_model
      decimal payout_value
      string target_url
      string tracking_url
      string status
    }

    landing_pages {
      int id
      int offer_id
      string url
      int http_status
      string title
      text description
      int word_count
      int internal_links
      int external_links
      int quality_score
    }

    creatives {
      int id
      int offer_id
      string angle
      json headlines
      json descriptions
      json keywords
      string status
    }

    creative_claim_reviews {
      int id
      int creative_set_id
      string asset_type
      string issue
      string severity
      string review_status
      string source_url
    }

    campaign_drafts {
      int id
      int offer_id
      string name
      string channel
      decimal daily_budget
      string bid_strategy
      string status
    }

    ad_review_cases {
      int id
      int campaign_draft_id
      string object_type
      string policy_topic
      string status
      string final_url
      string expanded_url
    }

    metrics_daily {
      int id
      int offer_id
      int campaign_draft_id
      date day
      int impressions
      int clicks
      decimal cost
      int conversions
      decimal revenue
    }

    publisher_metrics_daily {
      int id
      int offer_id
      date day
      string platform
      string channel
      decimal estimated_revenue
      decimal finalized_revenue
      decimal paid_revenue
      decimal deduction_rate
    }

    revenue_settlements {
      int id
      int offer_id
      string platform
      string month
      decimal estimated_revenue
      decimal finalized_revenue
      decimal paid_revenue
      string settlement_status
    }

    reconciliation_runs {
      int id
      string month
      string platform
      string status
      datetime started_at
      datetime finished_at
    }

    ad_layout_versions {
      int id
      int offer_id
      string page_template
      string version_name
      text notes
      string status
    }

    publisher_ad_unit_daily {
      int id
      int offer_id
      date day
      string ad_unit
      string position
      int ad_requests
      int ad_impressions
      int viewable_impressions
      decimal estimated_revenue
      decimal finalized_revenue
    }

    ad_refresh_tests {
      int id
      int offer_id
      string refresh_type
      int refresh_interval_seconds
      string review_status
    }

    click_session_reconciliation_runs {
      int id
      date day
      string source
      int ads_clicks
      int landing_requests
      int ga4_sessions
      int offer_clicks
      decimal estimated_revenue
      decimal finalized_revenue
      string gap_reason
    }

    postback_events {
      int id
      string click_id
      string transaction_id
      string event_status
      decimal payout
      datetime postback_time
    }

    ads_txt_snapshots {
      int id
      string domain
      string seller_system_domain
      string seller_id
      string relationship_type
      string status
      datetime checked_at
    }

    sellers_json_checks {
      int id
      string seller_system_domain
      string seller_id
      string seller_type
      string seller_name
      string seller_domain
      string status
    }

    supply_chain_checks {
      int id
      string domain
      string schain_complete
      string nodes_summary
      string status
    }

    gam_pricing_rule_versions {
      int id
      string domain
      string rule_name
      decimal floor_price
      string targeting_summary
      string status
    }

    ad_unit_yield_daily {
      int id
      date day
      string ad_unit
      string country
      string device
      int ad_requests
      int impressions
      decimal ecpm
      decimal estimated_revenue
      decimal finalized_revenue
    }

    yield_experiments {
      int id
      string experiment_name
      string pricing_rule_version
      string status
      datetime started_at
      datetime ended_at
    }

    native_campaign_sources {
      int id
      string network
      string publisher_id
      string source_id
      string placement_id
      string status
    }

    native_creative_angles {
      int id
      string campaign_id
      string creative_id
      string angle
      string claim_risk
      string review_status
    }

    advertorial_page_reviews {
      int id
      string page_url
      string disclosure_status
      string claim_review_status
      datetime reviewed_at
    }

    native_source_quality_daily {
      int id
      date day
      string source_id
      decimal cost
      int sessions
      decimal paid_revenue
      string action
    }

    google_ads_report_snapshots {
      int id
      string account_id
      string report_type
      string date_range
      string timezone
      datetime downloaded_at
    }

    search_term_diagnostics {
      int id
      string campaign_id
      string ad_group_id
      string search_term
      string match_type
      decimal cost
      decimal paid_revenue
      string action
    }

    auction_insight_daily {
      int id
      date day
      string campaign_id
      string competitor_domain
      decimal impression_share
      decimal overlap_rate
      decimal outranking_share
    }

    change_history_events {
      int id
      string account_id
      string change_type
      string changed_by
      datetime changed_at
      text evidence_summary
    }

    search_automation_controls {
      int id
      string campaign_id
      boolean ai_max_enabled
      boolean broad_match_enabled
      boolean dsa_enabled
      datetime reviewed_at
    }

    search_query_diagnostics {
      int id
      date day
      string campaign_id
      string search_term
      decimal cost
      decimal paid_revenue
      string action
    }

    search_url_expansion_reviews {
      int id
      string campaign_id
      string expanded_url
      string inclusion_rule
      string risk_decision
      datetime reviewed_at
    }

    search_asset_auto_generation_reviews {
      int id
      string campaign_id
      string asset_text
      string claim_risk
      string review_status
      datetime reviewed_at
    }

    pmax_campaign_controls {
      int id
      string campaign_id
      boolean final_url_expansion_enabled
      text url_exclusions
      text brand_exclusions
      datetime reviewed_at
    }

    pmax_channel_performance_daily {
      int id
      date day
      string campaign_id
      string channel
      decimal cost
      decimal conversions
      decimal paid_revenue
    }

    pmax_asset_group_snapshots {
      int id
      string campaign_id
      string asset_group
      text audience_signals
      text asset_claim_summary
      datetime captured_at
    }

    geo_market_profiles {
      int id
      string country
      string language
      string location_option
      string account_timezone
      string account_currency
    }

    localized_page_versions {
      int id
      string country
      string language
      string page_url
      string localization_status
      datetime reviewed_at
    }

    geo_device_metrics_daily {
      int id
      date day
      string country
      string device
      decimal cost
      decimal paid_revenue
      int bad_geo_count
    }

    fx_rate_snapshots {
      int id
      date rate_date
      string base_currency
      string quote_currency
      decimal fx_rate
    }

    account_governance_profiles {
      int id
      string customer_id
      string mcc_customer_id
      string business_owner
      string advertiser_entity
      string status
    }

    mcc_hierarchy_snapshots {
      int id
      string manager_customer_id
      string client_customer_id
      string relationship_type
      datetime captured_at
    }

    account_access_reviews {
      int id
      string customer_id
      string user_email
      string access_level
      string review_decision
      datetime reviewed_at
    }

    advertiser_verification_cases {
      int id
      string customer_id
      string verification_status
      string advertiser_entity
      text evidence_summary
      datetime updated_at
    }

    publisher_site_reviews {
      int id
      string site_domain
      string review_status
      string connection_method
      datetime review_requested_at
      datetime reviewed_at
    }

    adsense_policy_center_issues {
      int id
      string site_domain
      string issue_type
      string ad_serving_status
      string affected_urls
      int affected_ad_requests
    }

    ad_serving_limit_events {
      int id
      string site_domain
      string limit_reason
      string traffic_source
      datetime started_at
      datetime resolved_at
    }

    policy_review_requests {
      int id
      string issue_type
      string fix_summary
      string review_status
      datetime submitted_at
    }

    ad_quality_incidents {
      int id
      string site_domain
      string page_url
      string advertiser_domain
      string incident_type
      string action
    }

    blocked_advertiser_domains {
      int id
      string site_domain
      string advertiser_domain
      string reason
      datetime blocked_at
    }

    blocked_ad_categories {
      int id
      string site_domain
      string category
      string category_type
      string reason
    }

    publisher_blocking_rule_versions {
      int id
      string site_domain
      string rule_version
      text change_summary
      datetime changed_at
    }

    domain_assets {
      int id
      string root_domain
      string asset_type
      string business_owner
      string vertical
      string status
    }

    domain_history_checks {
      int id
      string root_domain
      string historical_topic
      string risk_level
      text evidence_summary
      datetime checked_at
    }

    site_migration_plans {
      int id
      string old_domain
      string new_domain
      string migration_reason
      string approval_status
      datetime planned_at
    }

    final_url_change_reviews {
      int id
      string campaign_id
      string old_final_url
      string new_final_url
      string risk_decision
      datetime reviewed_at
    }

    header_bidding_stack_versions {
      int id
      string domain
      string stack_version
      string prebid_version
      int timeout_ms
      string price_granularity
      string status
    }

    header_bidding_bidder_daily {
      int id
      date day
      string bidder
      string ad_unit
      string country
      string device
      int bid_requests
      int bid_responses
      int wins
      int renders
      decimal net_revenue
    }

    header_bidding_debug_events {
      int id
      string stack_version
      string event_type
      string evidence_summary
      string status
    }

    research_sources {
      int id
      string topic
      string capability
      string title
      string url
      string publisher
      string source_type
      string reliability
      string review_status
      text claim_summary
      date retrieved_on
    }
```

## 6. 技术架构

```mermaid
flowchart LR
    Browser["浏览器"] --> Flask["Flask Web"]
    Flask --> Services["业务服务层"]
    Services --> SQLAlchemy["SQLAlchemy ORM"]
    SQLAlchemy --> MySQL["MySQL"]
    Services --> Fetcher["Landing Page Fetcher"]
    Services --> Generator["Creative Generator"]
    Services --> ClaimReview["Claim Review"]
    Services --> Analyzer["ROI Analyzer"]
    Services --> Exporter["CSV / Script Exporter"]
```

组件：

- Flask：页面、表单、API。
- SQLAlchemy：ORM 和迁移基础。
- PyMySQL：MySQL 驱动。
- BeautifulSoup：落地页解析。
- Requests：页面抓取。
- APScheduler 或简单任务表：后续做定时任务。

Google Ads Scripts 同步的设计边界见 [Google Ads Scripts 数据同步、快照与一致性手册](google_ads_scripts_data_sync_consistency.md)。第一版已实现 `/scripts-sync` 和 `script_sync_reviews`：表中保存 auth_mode、sync_type、script_name、customer_id、date_range、account_timezone、currency、query_or_report、source_snapshot_hash、payload_hash、row_count、error_count、warning_count、freshness_minutes、rerun_window_days、data_status、revenue_status、conflict_status、external_change_count、change_history_checked、preview_only、human_review、Script Sync Score、risk_level、freshness_level、recommended_action、blockers、status、notes 和 source_urls；`/scripts-sync/<id>/status` 更新 snapshot_ready、rerun_required、conflict_review、approved_for_import、imported_manual、blocked 等内部状态并写入 `audit_logs`。同步结果按 Today / Yesterday / Last 7 days / Month to date 做窗口重拉；写入方向仍然走 preview、审批、Change history 和审计日志。

## 7. 路由设计

| 路由 | 方法 | 功能 |
| --- | --- | --- |
| `/` | GET | Dashboard |
| `/accounts` | GET/POST | 广告账号配置 |
| `/calculators` | GET/POST | 套利测算与机会评分 |
| `/offers` | GET/POST | Offer 列表和创建 |
| `/offers/<id>` | GET | Offer 详情 |
| `/offers/<id>/crawl` | POST | 采集落地页 |
| `/offers/<id>/creatives/generate` | POST | 生成创意 |
| `/creatives/<id>/claim-reviews/run` | POST | 刷新创意 Claim 审核记录 |
| `/claim-reviews/<id>/status` | POST | 更新 Claim 审核人审状态并写入审计日志 |
| `/campaigns` | GET/POST | 投放草稿 |
| `/ad-reviews` | GET/POST | 广告审核、拒登和申诉证据包案例 |
| `/ad-reviews/<id>/status` | POST | 更新广告审核案例状态并写入审计日志 |
| `/campaigns/<id>/export.csv` | GET | 导出 CSV |
| `/campaigns/<id>/export.script.json` | GET | 导出 Google Ads Scripts JSON payload |
| `/bulk-upload` | GET/POST | Editor CSV / Bulk Upload 批量变更门禁 |
| `/bulk-upload/<id>/status` | POST | 更新批量变更状态并写入审计日志 |
| `/scripts-sync` | GET/POST | Google Ads Scripts 同步快照与冲突治理 |
| `/scripts-sync/<id>/status` | POST | 更新 Scripts 同步评审状态并写入审计日志 |
| `/taxonomy-governance` | GET/POST | Campaign 命名、Labels、UTM/SubID 与 join key 治理 |
| `/taxonomy-governance/<id>/status` | POST | 更新命名维度评审状态并写入审计日志 |
| `/metrics/import` | GET/POST | 指标导入 |
| `/optimization` | GET | 优化建议 |
| `/attribution` | GET/POST | 归因、增量性与流量蚕食评审 |
| `/attribution/<id>/status` | POST | 更新归因增量评审状态并写入审计日志 |
| `/cpl-verticals` | GET/POST | CPL 垂类经济、资格字段与 Buyer Acceptance 评审 |
| `/cpl-verticals/<id>/status` | POST | 更新 CPL 垂类评审状态并写入审计日志 |
| `/lead-pricing` | GET/POST | Lead Pricing、Payout Negotiation、scrub reserve 和 safe CPC 评审 |
| `/lead-pricing/<id>/status` | POST | 更新 Lead Pricing 评审状态并写入审计日志 |
| `/appointment-leads` | GET/POST | Appointment Lead、Booking、Show Rate、No-show 和 safe CPC 评审 |
| `/appointment-leads/<id>/status` | POST | 更新 Appointment Lead 评审状态并写入审计日志 |
| `/buyer-capacity` | GET/POST | Buyer Capacity、Cap Pacing、Dayparting、no buyer 和 safe spend 评审 |
| `/buyer-capacity/<id>/status` | POST | 更新 Buyer Capacity 评审状态并写入审计日志 |
| `/ping-post-routing` | GET/POST | Ping/Post、Buyer Routing、consent、PII、cap、fallback 和 buyer feedback 评审 |
| `/ping-post-routing/<id>/status` | POST | 更新 Ping/Post Routing 评审状态并写入审计日志 |
| `/conversion-signals` | GET/POST | Conversion Signal、primary/secondary、value、dedupe、lag 和 bid readiness 评审 |
| `/conversion-signals/<id>/status` | POST | 更新 Conversion Signal 评审状态并写入审计日志 |
| `/crm-value-mapping` | GET/POST | CRM stage、Buyer Feedback、Value Mapping、Import QA 和 Adjustment 评审 |
| `/crm-value-mapping/<id>/status` | POST | 更新 CRM Value Mapping 评审状态并写入审计日志 |
| `/sources` | GET/POST | 研究来源库 |
| `/sources/<id>/status` | POST | 更新来源复核状态并写入审计日志 |
| `/risk-audits` | GET/POST | 高风险能力审计记录 |
| `/risk-audits/<id>/status` | POST | 更新风险审计处理进度并写入审计日志 |
| `/tasks` | GET/POST | 安全任务中心 |
| `/tasks/<id>/run` | POST | 手动执行一次任务 |
| `/links` | GET/POST | 链接轮换计划 |
| `/links/<id>/rotate` | POST | 人工确认后轮换当前 URL |
| `/logs` | GET | 审计日志 |
| `/docs` | GET | 文档入口 |

`/risk-audits/<id>/status` 的状态流只表达内部处理进度：open、reviewed、mitigated、rejected。状态更新会写入 `audit_logs`，但不会自动放行高风险能力，也不会触发后台登录、Cookie 操作、流量模拟、代理/指纹配置、链接 cloaking 或换号。

CSV / Scripts JSON 导出和任务中心的导出检查共用 `services/preflight.py`。导出前必须满足 campaign 已批准、Claim 审核无 open/rewrite_required/blocked、广告审核案例无 open/appeal_submitted/rejected；失败时写入 `audit_logs` 的 `export_blocked`，不生成可用于上传的 payload。

任务中心的设计边界见 [任务编排、安全审批、执行日志与事故复盘手册](task_orchestration_approval_audit_runbook.md)。任何后续调度器、队列或自动执行器，都必须先满足任务分级、审批记录、payload 版本、幂等键、外部 Change history / Scripts log 证据和事故复盘字段要求；认证挑战、Cookie 接管、补点击、cloaking、规避封禁等语义不能成为任务类型。

## 8. MySQL 配置

`.env` 示例：

```env
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=mysql+pymysql://ads_user:ads_password@127.0.0.1:3306/ads_workbench?charset=utf8mb4
```

初始化：

```bash
flask --app app db-init
flask --app app seed
flask --app app run --debug --port 5058
```

## 9. 验收口径

文档验收：

- Ads 套利定义、模式、指标、公式、流程、风险、SOP 完整。
- ADXKit 功能拆解清楚，区分可复刻和不可复刻部分。
- 系统设计能解释为什么每个功能服务于业务流程。

系统验收：

- 能创建 Offer。
- 能记录 Google Ads 账号和同步方式。
- 能保存套利测算并输出安全 CPC、测试预算、硬止损和机会评分。
- 能采集落地页并生成审计结果。
- 能生成 15 标题、4 描述、30 关键词。
- 能创建投放草稿并导出 CSV / Scripts JSON。
- 能导入指标并计算 ROI。
- 能创建归因增量评审，计算 incremental revenue、iROAS、incremental profit、blockers，并记录状态审计。
- 能创建 CPL 垂类评审，计算 effective payout、safe CPC、Vertical Fit Score、blockers，并记录状态审计。
- 能生成优化建议。
- 能按 6 类高风险能力和受众/再营销/Customer Match 合规主题创建风险审计记录。
- 能创建任务并记录安全执行结果。
- 能创建合规链接轮换计划并通过人工确认记录轮换。
- 能查看审计日志。
- 能运行 `scripts/acceptance_audit.py`，汇总证明文档映射、验收文档、`.env.example`、单团队 schema、seed 核心数据、高风险来源覆盖、核心页面、Scripts 安全标记和高风险 guardrail。

## 10. 后续可扩展

- 接入官方 Google Ads API 或 Google Ads Scripts 回传。
- 接入 OpenAI/Claude/Gemini 等 LLM 生成创意。
- 增加 GA4、AdSense、Ad Manager、联盟平台报表导入。
- 增加页面截图、速度评分、广告密度检测。
- 增加单团队内角色权限，但仍不做 SaaS 多租户。
