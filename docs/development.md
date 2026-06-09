# 开发文档

更新时间：2026-06-09

## 1. 技术栈

- Python 3.11+。
- Flask 3。
- Flask-SQLAlchemy。
- MySQL 8 / SQLite 开发验证。
- PyMySQL。
- Requests + BeautifulSoup。

## 2. 项目结构

```text
adsworkbench/
  __init__.py          Flask app factory 和 CLI
  config.py            配置和 DATABASE_URL
  extensions.py        SQLAlchemy 扩展
  models.py            数据模型和 demo seed
  routes.py            页面路由和表单处理
  services/
    landing.py         落地页采集与审计
    creative.py        规则化创意生成
    claim_review.py    创意 claim 风险审查
    analytics.py       指标汇总与优化规则
    exporters.py       Google Ads Editor CSV 导出
    bulk_upload.py     Editor CSV / Bulk Upload 批量变更门禁评分
    script_sync.py     Google Ads Scripts 同步快照与冲突门禁评分
    taxonomy.py        Campaign 命名、UTM/SubID 和 join key 门禁评分
    attribution.py     归因增量、iROAS 和流量蚕食门禁评分
    cpl_vertical.py    CPL 垂类、资格字段和 buyer acceptance 门禁评分
    lead_pricing.py    Lead Pricing、Payout Negotiation 和 safe CPC 门禁评分
    appointment_lead.py Appointment Lead、show rate、no-show 和 safe CPC 门禁评分
    buyer_capacity.py  Buyer Capacity、cap pacing 和 dayparting 门禁评分
    ping_post_routing.py Ping/Post、buyer routing、consent、PII 和 cap 门禁评分
    conversion_signal.py 转化信号质量、primary/value/lag/dedupe 和出价准入评分
    crm_value_mapping.py CRM stage、buyer feedback、value mapping 和 import QA 门禁评分
    markdown_render.py  安全文档 Markdown 渲染
  templates/           Jinja 页面
  static/styles.css    管理台样式
docs/                  行业知识、拆解、设计、使用、开发文档
```

## 3. 配置

默认不设置 `DATABASE_URL` 时使用本地 SQLite：

```text
sqlite:///instance/ads_workbench.sqlite
```

MySQL 配置：

```env
DATABASE_URL=mysql+pymysql://ads_user:ads_password@127.0.0.1:3306/ads_workbench?charset=utf8mb4
SECRET_KEY=change-me
```

仓库提供 `.env.example`，与 `docker-compose.yml` 的 MySQL 默认库名、用户名和密码一致。复制为 `.env` 后即可本地运行 MySQL 版本；如果不设置 `DATABASE_URL`，应用会回落到 SQLite。

`.env.example` 只能放运行配置，不能新增 Google Ads Cookie、Session Token、浏览器 Profile、代理池、指纹配置、Worker 规避规则、账号池或封禁后换号资料。涉及这些语义的需求应进入高风险专题、来源库和风险审计，而不是进入配置项。

## 4. 数据模型

核心表：

- `offers`：Offer、垂类、国家、Payout、URL、政策备注。
- `ads_accounts`：Google Ads 账号配置和同步方式，不保存 Cookie。
- `opportunity_assessments`：套利测算输入、结果和机会评分。
- `landing_pages`：落地页采集和质量审计。
- `creative_sets`：创意角度、标题、描述、关键词。
- `creative_claim_reviews`：创意 Claim 审核记录，保存 issue、severity、evidence、source_url 和 review_status。
- `campaign_drafts`：投放草稿。
- `ad_review_cases`：广告审核、拒登和申诉证据包案例，保存 policy_topic、受影响对象、URL、证据、修复摘要和状态。
- `metrics_daily`：日级花费和收入指标。
- `optimization_actions`：规则生成的优化建议。
- `research_sources`：研究来源 URL、发布方、证据摘要、可信级别和复核状态。
- `risk_audits`：按高风险能力或受众/再营销/Customer Match 合规主题分类的上线前审计记录。
- `task_jobs`：安全任务中心，记录任务类型、执行次数、结果和调度信息。
- `bulk_upload_reviews`：Google Ads Editor CSV / Scripts Bulk Upload 批次、hash、preview、Editor check、人工审批、Change History 和回滚证据。
- `script_sync_reviews`：Google Ads Scripts 报表/快照同步、query hash、数据状态、Change History、冲突和重拉窗口证据。
- `taxonomy_reviews`：Campaign 命名、Labels、UTM、ValueTrack、SubID、版本和报表 join key 评审。
- `attribution_reviews`：归因增量、control/treatment、holdout、iROAS、增量利润和流量蚕食评审。
- `cpl_vertical_reviews`：CPL 垂类经济、资格字段、buyer acceptance、reject reason、safe CPC 和政策门禁评审。
- `lead_pricing_reviews`：Lead Pricing、headline/unit/proposed payout、scrub reserve、payment term、safe CPC、谈价证据和状态门禁评审。
- `appointment_lead_reviews`：Appointment Lead、Booking、Show Rate、No-show、calendar capacity、reminder consent、safe CPC 和状态门禁评审。
- `buyer_capacity_reviews`：Buyer Capacity、Cap Pacing、Dayparting、no buyer、missed contact、safe spend 和状态门禁评审。
- `ping_post_routing_reviews`：Ping/Post、buyer routing、consent/disclosure、PII 最小化、suppression/DNC、cap snapshot、fallback、buyer feedback、expected payable value、safe CPL 和状态门禁评审。
- `conversion_signal_reviews`：Conversion Signal、primary/secondary、value mode、match rate、dedupe、lag、policy/consent、bid readiness、safe target CPA 和状态门禁评审。
- `crm_value_mapping_reviews`：CRM stage、buyer feedback、conversion action role、value mode、transaction_id、import QA、adjustment、expected value 和状态门禁评审。
- `link_rules`：合规链接计划。
- `audit_logs`：审计日志。

第一版没有 `tenant_id`、`organization_id`、`user_id` 等多租户字段。

## 5. CLI

初始化表：

```bash
flask --app app db-init
```

插入示例数据：

```bash
flask --app app seed
```

启动：

```bash
flask --app app run --debug --port 5058
```

## 6. 开发验证

编译检查：

```bash
python -m compileall adsworkbench app.py scripts
```

快速 smoke test：

```bash
python scripts/smoke_test.py
```

研究文档验收：

```bash
python scripts/verify_research_docs.py
```

总体验收审计：

```bash
python scripts/acceptance_audit.py
```

`smoke_test.py` 会：

- 使用临时 SQLite。
- 初始化表。
- Seed 示例数据。
- 检查账号配置页面。
- 请求核心页面。
- 创建并检查套利测算记录。
- 创建并检查研究来源记录。
- 检查 CSV 和 Scripts JSON 导出。
- 创建并检查风险审计记录。
- 创建并执行任务中心任务。
- 通过测试客户端导入一行指标。
- 检查知识文档入口和高风险专题入口。

`verify_research_docs.py` 会检查高风险专题、行业手册、来源 URL、验收矩阵、`.env.example` 和 guardrail 文档不退化。

`acceptance_audit.py` 会汇总检查 Markdown 文档路由映射、关键验收文档、`.env.example`、单团队 schema、seed 核心数据、高风险来源覆盖、核心页面、Scripts 安全标记，以及账号 / 链接 / 任务的高风险语义拦截。

## 7. 扩展点

### 7.1 AI 创意生成

当前 `adsworkbench/services/creative.py` 是规则模板。后续可新增：

```text
services/ai_provider.py
```

建议接口：

```python
class CreativeProvider:
    def generate(self, offer, landing_page) -> list[dict]:
        ...
```

输出仍保持：

```python
{
    "angle": "...",
    "headlines": [...],
    "descriptions": [...],
    "keywords": [...],
}
```

生成器应优先使用 `LandingPage.raw_summary` 里的 `Claim snippets:`、`Proof/review snippets:`、`CTA texts:` 等证据行。任何 LLM Provider 都必须返回可追溯的 supporting snippet 或 blocked claim，不能把页面没有的价格、排名、保证、认证、用户数或官方关系写入广告资产。

### 7.1.1 Claim 审核

当前 `adsworkbench/services/claim_review.py` 对 generated headlines/descriptions 做只读风险提示，并把结果落入 `creative_claim_reviews`。扩展时建议：

- 在 `creative_claim_reviews` 上继续补 reviewer、reviewed_at、allowed_rewrite 和 blocked_reason。
- 把规则拆成可配置字典，按垂类维护 blocked claim 和 allowed rewrite。
- LLM 创意 provider 必须返回每条资产对应的 source snippet 或 blocked reason。
- 导出 CSV / Scripts JSON 前要求 high severity claim 有人工放行记录。

Claim 审核不能变成绕审核工具；它只能减少误导、缺证据和政策不一致。

### 7.1.2 广告审核、拒登和申诉证据包

当前 `/ad-reviews` 和 `ad_review_cases` 已实现只读和人工证据流程：

- `ad_review_cases`：记录 object_type、object_ref、policy_topic、status、severity、final_url、expanded_url、reviewer。
- 状态流：open、fixed、appeal_ready、appeal_submitted、approved、rejected、abandoned。
- 状态更新写入 `audit_logs`，只代表内部证据包进度。

后续可扩展 `policy_decision_snapshots`、`appeal_evidence_packages` 和 `policy_fix_actions`，分别记录 Policy Manager 截图、claim_map、page_evidence、change_summary、qa_results、appeal_text、reviewer、结果和修复动作。这些表用于拒登定位、证据包、复盘和素材模板治理。不要把它扩展成 Cookie 后台操作、自动绕过登录/2FA/安全挑战、cloaking、补点击、换号规避或自动批量申诉工具。

### 7.2 Google Ads 执行连接器

安全优先级：

1. Google Ads Editor CSV。
2. Google Ads Scripts。
3. 官方 Google Ads API。
4. 人工执行记录。

不实现：

- Cookie 注入。
- Session 复用。
- 绕过安全挑战。
- 自动操控后台 UI。

`adsworkbench/services/preflight.py` 是导出前闸门，路由导出和任务中心都必须调用同一套 `campaign_preflight_blockers()`。新增任何 CSV、Scripts、API 或批量操作连接器前，都要先检查 campaign 状态、Claim review 状态和 ad review case 状态；不能直接调用 exporter 绕过 preflight。

建议新增：

```text
services/connectors/google_ads_editor.py
services/connectors/google_ads_scripts.py
services/connectors/google_ads_api.py
```

所有连接器必须写入 `audit_logs`。

当前提供 `scripts/google_ads_script_payload_preview.js` 作为 Google Ads Scripts 预览模板。它默认 `PREVIEW_ONLY=true`、`ALLOW_APPLY=false`，只校验 `/campaigns/<id>/export.script.json` 的安全字段并创建 bulk upload preview。任何把它改成 apply 的版本，都必须先增加审批、预算上限、域名白名单、回滚记录和运行日志。

Google Ads Editor CSV / Bulk Upload 治理 V1 已有 `bulk_upload_reviews` 和 `/bulk-upload`，用于记录 batch_id、CSV hash、payload hash、目标账号确认、行数、关键词数、广告数、预算变化、URL 变化、preflight、Editor check、Bulk Upload preview、人工审核、Change History、回滚计划、score、risk_level、recommended_action、blockers、状态和来源 URL；状态更新写入 `audit_logs`。后续如果要拆更细，可以新增 `bulk_change_batches`、`bulk_change_rows`、`csv_export_versions`、`editor_review_decisions`、`bulk_upload_results` 和 `change_history_links`。导出器和工作台不应自动打开 Editor、自动登录 Google Ads、自动点击发布按钮或自动 apply Scripts Bulk Upload。修改 `calculate_bulk_upload_review()` 时，必须同步更新 `/bulk-upload` 表单、smoke test、acceptance audit 和本手册。

### 7.3 报表导入

可以为 AdSense、Ad Manager、联盟平台、GA4 增加导入器。原则：

- 先落 `metrics_daily`。
- 保留来源文件名和导入时间。
- 不覆盖原始记录，使用新增或版本化导入。
- AdSense/GAM/AdX 收入导入器要区分 estimated、finalized、paid 和 deduction，不要把当日 estimated revenue 直接作为扩量依据。
- 后续建议新增 `publisher_metrics_daily`、`revenue_settlements`、`reconciliation_runs`，分别保存日级收入、月度结算和对账批次。
- Offer cap / payout / status 治理 V1 已有 `offer_cap_reviews` 和 `/offer-cap-payout`，用于保存 paused/expired/quality_hold、payout 版本、cap_limit/cap_used/cap_remaining、buyer capacity、approval/paid/deduction、替代 Offer 审核状态、Offer Cap Score、risk_level、recommended_action、blockers、source_urls 和处理状态；状态更新写入 `audit_logs`，不自动登录联盟后台、不超 cap 继续灌量、不动态切未审核 Offer 或隐藏真实目的地。后续可拆分 `offer_status_snapshots`、`offer_payout_versions`、`offer_cap_snapshots`、`offer_replacement_plans`、`cap_pacing_alerts`。
- 广告位实验导入器可新增 `ad_layout_versions`、`publisher_ad_unit_daily`、`ad_refresh_tests`、`page_experience_audits`，用于记录广告位、viewability、CLS/LCP、refresh_type 和 finalized revenue。
- Click -> Session -> Revenue 对账可新增 `landing_request_daily`、`click_session_reconciliation_runs`、`postback_events`、`revenue_status_daily`，用于保存真实日志、GA4 sessions、postback 和收入状态差异。
- RSOC / N2S 报表可新增 `search_feed_partners`、`rsoc_page_reviews`、`rsoc_creative_rac_reviews`、`rsoc_funnel_daily`、`rsoc_query_group_daily`、`rsoc_source_quality_daily`、`rsoc_deduction_reports` 和 `rsoc_policy_incidents`，用于记录 Related Search 权限、PIF/RAC、上游创意、query intent、finalized RPV、deduction 和 feed partner 证据；不生成 feed 代码、不自动搜索或点击。
- Native / Advertorial / Presell 报表可新增 `native_campaign_sources`、`native_creative_angles`、`advertorial_page_reviews`、`presell_disclosure_checks`、`native_source_quality_daily`、`native_buyer_feedback_daily`、`native_policy_incidents`，用于保存 source/publisher/placement、素材角度、软文页、披露、buyer feedback、paid revenue 和政策事故证据。
- 单位经济模型可新增 `unit_economic_models`、`unit_economic_scenarios`、`break_even_snapshots`、`safety_factor_versions`、`test_budget_plans`、`unit_economic_decisions`、`model_assumption_audits`，用于保存 RPV/EPC、break-even CPC、safe CPC、safety margin、test budget、hard stop、stress case、cash buffer、decision 和 reviewer；新增自动化只能生成测算和审批任务，不直接买量或改预算。
- 季节性、事件日历与需求预测可新增 `event_calendars`、`seasonal_demand_forecasts`、`keyword_trend_snapshots`、`seasonal_readiness_checks`、`seasonal_budget_ramp_plans`、`seasonal_exit_rules`、`seasonality_adjustment_reviews`、`seasonal_postmortems`，用于保存官方日期、趋势证据、关键词 forecast、页面 readiness、预算 ramp、退出规则和季后 paid/finalized revenue 复盘。
- 预算节奏治理 V1 已有 `budget_pacing_reviews` 和 `/budget-pacing`，用于保存 current/proposed daily budget、test budget、hard stop、spend_to_date、safe/actual CPC、sample clicks、revenue maturity、cash buffer、overdelivery exposure、Budget Pacing Score、risk_level、recommended_action、blockers、source_urls 和处理状态；状态更新写入 `audit_logs`，不自动修改 `campaign_drafts.daily_budget` 或广告后台。后续可拆分 `budget_decision_log`、`pacing_rules`、`segment_metrics` 和 `settlement_metrics`。
- Source / Publisher / Placement 质量治理 V1 已有 `source_quality_reviews` 和 `/source-quality`，用于保存来源透明度、追踪完整性、intent fit、click/session、reported/approved/paid/deducted revenue、invalid clicks、complaints、buyer reject、policy issues、停源控制、Source Quality Score、recommended_action、blockers、名单状态和来源 URL；状态更新写入 `audit_logs`。后续可拆分 `traffic_sources`、`publisher_placements`、`source_quality_daily`、`source_quality_decisions`、`source_blocklist_entries`、`source_feedback_events`、`placement_exclusion_exports`、`source_retest_runs`。
- 流量供应商合同与争议治理 V1 已有 `vendor_contract_reviews` 和 `/vendor-contracts`，用于保存供应商、IO、line item、质量条款、tracking/reporting appendix、报表差异、invalid traffic、buyer reject、refund、credit、makegood、invoice、amount_at_risk、Vendor Contract Score、recommended_action、blockers、状态和 dispute evidence；状态更新写入 `audit_logs`。后续可拆分 `traffic_vendor_accounts`、`media_insertion_orders`、`media_io_line_items`、`vendor_tracking_appendices`、`vendor_report_imports`、`traffic_dispute_cases`、`traffic_dispute_evidence`、`vendor_credit_notes`、`makegood_plans`、`vendor_scorecards`、`contract_versions`。
- 转化信号质量治理 V1 已有 `conversion_signal_reviews` 和 `/conversion-signals`，用于保存 conversion goal/action、action_stage、primary_status、recommended_primary_status、value_mode、bid_strategy、weekly submitted/approved/paid、reported value、approved/paid rate、click_id coverage、offline match rate、duplicate rate、conversion lag、segment_granularity、policy/consent、customer_data、offline_import、transaction_id、bid_strategy_report、Signal Quality Score、bid_readiness、safe_target_cpa、recommended_action、blockers、source_urls 和处理状态；状态更新写入 `audit_logs`，不自动上传 offline conversion、不自动改 conversion goal/primary/出价、不用 Cookie 后台改 goal。后续可拆分 `conversion_signal_definitions`、`conversion_goal_versions`、`conversion_signal_quality_daily`、`offline_conversion_import_runs`、`offline_conversion_import_errors`、`bid_strategy_learning_snapshots`、`conversion_value_adjustments`、`conversion_signal_incidents`。
- 决策窗口治理 V1 已有 `decision_window_reviews` 和 `/decision-windows`，用于保存 freshness、conversion lag、approval lag、settlement lag、sample clicks、approved/paid revenue、source quality、incident state、Decision Window Score、maturity、recommended_action、blockers、source_urls 和处理状态；状态更新写入 `audit_logs`，不自动改预算或后台报表。后续可新增 `decision_window_profiles`、`conversion_lag_profiles`、`revenue_lag_profiles`、`cohort_maturity_daily`、`revenue_status_aging`、`budget_ramp_decisions`、`settlement_close_runs`、`decision_window_incidents`；新增导入器必须保存 source_file_hash、timezone、date range 和 data_status，不生成点击、展示、转化、postback 或收入。
- Google Ads 报表诊断可新增 `google_ads_report_snapshots`、`search_term_diagnostics`、`auction_insight_daily`、`change_history_events`、`landing_page_performance_daily`、`asset_performance_snapshots`、`bid_strategy_diagnostics`，用于保存人工导出的 Search terms、Auction Insights、Change history、landing pages、assets 和 bid strategy 报表证据。
- 订阅、试用和 LTV 治理可新增 `subscription_offer_terms`、`subscription_cohort_daily`、`subscription_ltv_snapshots`、`refund_chargeback_events`、`cancellation_flow_audits`、`billing_disclosure_versions`、`ltv_value_feedback_runs`、`subscription_quality_decisions`，用于保存 trial、renewal、refund、chargeback、clawback、net LTV、disclosure 和 cancellation evidence；新增导入器只消费真实结算和订单证据，不伪造续费、不隐藏取消、不规避 chargeback。
- Search Terms、否定词和 Query Mining V1 已有 `query_mining_reviews` 和 `/query-mining`，用于保存 keyword、match type、search term、device、network、approved/paid revenue、buyer reject、intent、policy risk、conversion lag、negative_match_type、negative_level、recommended_action、blockers、source_urls 和处理状态；状态更新写入 `audit_logs`。后续可拆分 `search_term_snapshots`、`query_mining_decisions`、`negative_keyword_registry`。新增导入器必须保留 source_file_hash、date range 和 timezone；新增导出器只能生成待审核 CSV/Scripts preview，不要自动点击广告、模拟搜索、绕过 query 隐私聚合或抓取 Cookie 后台。
- 归因、增量性和流量蚕食治理 V1 已有 `attribution_reviews` 和 `/attribution`，用于保存 attribution model、control/treatment、holdout、iROAS、incremental profit、brand/organic/remarketing/PMax cannibalization、reviewer 证据、blockers 和状态流；状态更新写入 `audit_logs`。后续可拆分 `attribution_model_versions`、`attribution_model_comparisons`、`incrementality_tests`、`holdout_groups`、`lift_study_snapshots`、`cannibalization_checks`、`incremental_revenue_daily`、`incrementality_decisions`。新增自动化只能生成实验计划和审计任务，不自动创建实验、不自动应用 winner、不伪造 control 或转化。
- Search 自动化报表诊断可新增 `search_automation_controls`、`search_query_diagnostics`、`search_url_expansion_reviews`、`search_asset_auto_generation_reviews`、`search_brand_control_snapshots`、`dsa_page_feed_versions`，用于保存 AI Max、Broad Match、DSA、Final URL expansion、自动生成资产、brand controls、negative keywords 和 paid revenue 证据。
- PMax / Demand Gen 报表诊断可新增 `pmax_campaign_controls`、`pmax_channel_performance_daily`、`pmax_search_theme_diagnostics`、`pmax_asset_group_snapshots`、`pmax_url_expansion_checks`、`demand_gen_audience_diagnostics`，用于保存 Final URL expansion、URL exclusions、Search themes、Audience signals、asset group、brand exclusions、channel/placement/asset/landing page report 和 paid revenue 证据。
- AI Provider 和 Prompt 治理可新增 `ai_providers`、`ai_model_profiles`、`prompt_templates`、`prompt_runs`、`ai_output_assets`、`creative_angle_library`、`ai_cost_daily`、`ai_review_decisions` 和 `prompt_regression_tests`，用于保存 provider/model/prompt version、input evidence hash、output hash、token usage、cost、review status 和回滚点；不把模型输出自动提交广告后台，不发送 PII、Cookie、验证码或账号凭据。
- Creative Angle Library 可新增 `creative_angles`、`creative_asset_versions`、`creative_feedback_events`、`angle_performance_snapshots` 和 `creative_banned_patterns`，用于保存 angle 状态、素材版本、policy status、paid RPV、reject、deduction、complaint 和 prompt 回写决策；不生成虚假评价、不夸大 claim、不自动投放，也不通过补点击或模拟访问验证素材。
- 竞品广告和 SERP 情报可新增 `competitor_market_snapshots`、`competitor_ad_observations`、`market_angle_briefs`，用于保存人工观察的 query、GEO、device、截图路径、广告主 domain、angle tags、claim risk 和页面差距；不做自动 SERP 抓取器、不点击竞品广告、不复制素材、不仿冒商标，也不用代理/指纹模拟地区。
- Geo/语言/本地化报表可新增 `geo_market_profiles`、`localized_page_versions`、`geo_device_metrics_daily`、`fx_rate_snapshots`、`timezone_reconciliation_runs`、`bad_geo_incidents`，用于保存 location options、语言、设备、时区、币种、汇率、bad geo 和本地化页面证据。
- Portfolio 组合治理 V1 已有 `portfolio_allocation_reviews` 和 `/portfolio-allocation`，用于保存 Core/Scale/Test/Explore/Quarantine 预算池、monthly media budget、proposed allocation、reported/pending/approved/finalized/paid/deducted revenue、单一 Offer/source/account/revenue partner 集中度、cash reserve、source quality、policy risk、incident state、Portfolio Allocation Score、risk_level、recommended_action、blockers、source_urls 和处理状态；状态更新写入 `audit_logs`，不自动修改 Google Ads 预算或后台。后续可拆分 `portfolio_budgets`、`portfolio_budget_allocations`、`portfolio_exposure_daily`、`portfolio_concentration_limits`、`portfolio_allocation_decisions`、`portfolio_cash_reserve_snapshots`、`portfolio_postmortems`。
- AdSense 站点审核和 Policy Center 可新增 `publisher_site_reviews`、`adsense_policy_center_issues`、`ad_serving_limit_events`、`publisher_site_readiness_checks`、`policy_review_requests`，用于保存站点审核、ad serving status、Policy Center issue、修复证据和 review 结果。
- 发布商广告质量可新增 `ad_quality_incidents`、`blocked_advertiser_domains`、`blocked_ad_categories`、`ad_review_center_snapshots`、`publisher_blocking_rule_versions`，用于保存竞品广告、低质广告、敏感分类、阻止动作和收入影响证据。
- 域名和站点资产治理可新增 `domain_assets`、`domain_history_checks`、`site_migration_plans`、`publisher_site_assets`、`ads_txt_asset_checks`、`final_url_change_reviews`、`domain_risk_audits`，用于保存域名用途、历史主题、过期域名风险、站点迁移、ads.txt、Final URL 变更和风险审计证据。
- 程序化供应链 QA 可新增 `publisher_sites`、`ads_txt_snapshots`、`sellers_json_checks`、`supply_chain_checks`、`demand_partner_accounts`，用于记录授权卖方、DIRECT/RESELLER、MCM、schain 和需求源证据。
- GAM/AdX yield 报表可新增 `gam_pricing_rule_versions`、`ad_unit_yield_daily`、`demand_partner_yield_daily`、`yield_experiments`、`line_item_delivery_snapshots`，用于记录 floor、pricing rule、line item、Open Bidding partner、fill、eCPM 和 finalized revenue。
- Header Bidding / Prebid.js 报表可新增 `header_bidding_stack_versions`、`header_bidding_bidder_daily`、`header_bidding_auction_daily`、`header_bidding_debug_events`，用于记录 bidder、timeout、price granularity、floor、bid/win/render、GAM fill、latency、consent、ads.txt 和 schain 状态。
- 报表导入只能消费官方报表、后台导出或人工审核后的 CSV，不能生成广告请求、点击、展示或任何模拟流量。

Google Ads Scripts 报表同步治理 V1 已有 `script_sync_reviews` 和 `/scripts-sync`，用于保存 auth_mode、sync_type、script_name、customer_id、date_range、account_timezone、currency、query_or_report、source_snapshot_hash、payload_hash、row_count、error_count、warning_count、freshness_minutes、rerun_window_days、data_status、revenue_status、conflict_status、external_change_count、Change History 检查、preview/read-only 门禁、人工审核、score、risk_level、recommended_action、blockers、状态和来源 URL；状态更新写入 `audit_logs`。后续如果拆分数据仓库，可以新增 `google_ads_sync_runs`、`google_ads_metric_snapshots`、`google_ads_change_events`、`google_ads_object_versions`、`sync_conflicts`、`revenue_state_daily` 和 `script_execution_logs`。修改 `calculate_script_sync_review()` 时，必须同步更新 `/scripts-sync` 表单、smoke test、acceptance audit 和文档；不要把同步器做成 Cookie 后台镜像、无人审批写入器、补点击脚本或伪造报表工具。

Google Ads Recommendations / Experiments 扩展前先阅读 [Google Ads Recommendations、Experiments 与 Auto-apply 优化治理手册](google_ads_recommendations_experiments_auto_apply_governance.md)。建议新增 `google_ads_recommendation_reviews`、`google_ads_experiment_plans`、`auto_apply_snapshots` 和 `recommendation_change_links`，用于保存 recommendation type、risk_level、backend_revenue_evidence、decision、experiment hypothesis、split、primary_metric、guardrail metrics 和 Change History 证据。V1 不要接无人值守 auto-apply，不要自动调用 Cookie 后台或自动改预算、出价、关键词、资产、Final URL、conversion goal。

转化信号质量 V1 已有 `calculate_conversion_signal_review()`、`/conversion-signals` 和 `conversion_signal_reviews`。任何 conversion goal、primary/secondary、value mode、offline import 或 bid strategy learning 记录都必须保存 reviewer、人审状态、affected_campaigns、diagnostics、change_history、rollback_plan 和 source_urls；修改评分器时必须同步更新 `/conversion-signals` 表单、smoke test、acceptance audit 和 [转化信号质量与出价学习治理手册](conversion_signal_quality_bidding_learning_governance.md)。自动化只能生成 signal QA、学习期复盘、事故响应和人工审批任务，不自动改后台、不生成虚假 conversion、不把 shallow event 设为 primary。

CRM 阶段和 Offline Conversion Value Mapping V1 已有 `calculate_crm_value_mapping_review()`、`/crm-value-mapping` 和 `crm_value_mapping_reviews`。任何 CRM stage、buyer feedback、conversion action、value mode、offline import batch 或 adjustment 记录都必须保存 source_system、source_stage、standard_stage、buyer_status、conversion_action_role、primary_recommendation、value_mode、transaction_id_status、import_batch_status、diagnostics_status、adjustment_rule_status、consent/PII 状态、rollback_plan 和 source_urls；修改评分器时必须同步更新 `/crm-value-mapping` 表单、smoke test、acceptance audit 和 [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md)。后续可拆分 `crm_stage_maps`、`buyer_feedback_stage_maps`、`conversion_action_maps`、`offline_conversion_import_batches`、`conversion_value_versions`、`conversion_adjustment_events` 或 `conversion_diagnostics_snapshots`；不要自动上传、不自动改 primary、不用 rejected/returned 做正向转化、不补 postback、不生成虚假 click_id 或 conversion。

Lead Buyer 合同口径扩展前先阅读 [Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md)。新增 `lead_buyer_ios`、`lead_status_definitions`、`lead_return_windows`、`lead_reject_reason_codes`、`lead_buyer_postback_events`、`lead_buyer_invoice_lines` 或 `lead_return_dispute_cases` 时，必须保存 accepted_definition、qualified_definition、billable_definition、return_window_days、allowed_return_reasons、transaction_id、invoice/payment evidence、source_file_hash 和 reviewer；不要把 accepted 当 paid，不生成 lead、不补 postback、不伪造通话或联系状态、不自动争议、不通过 Cookie 后台修改买方或广告平台数据。

Call Tracking / DNI 扩展前先阅读 [Call Tracking Number Pool、DNI 与电话归因治理手册](call_tracking_dni_number_pool_attribution_governance.md)。新增 `call_tracking_number_pools`、`dni_assignment_events`、`call_log_events`、`call_disposition_events`、`call_recording_reviews`、`call_attribution_reconciliations` 或 `call_conversion_maps` 时，必须保存 pool_id、provider_call_id、tracking_number_hash、caller_hash、call_start_at、timezone、duration_seconds、disposition、recording_status、crm_lead_id、source_url、reviewer 和 decision；不要自动拨打电话、不模拟通话、不伪造 duration/recording/disposition、不把完整电话号码写入 URL/subid/log/prompt、不把 call click 默认设为 primary conversion。

Pay-per-call / Call Buyer Routing 扩展前先阅读 [Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](pay_per_call_buyer_routing_duration_payout_governance.md)。新增 `call_buyer_accounts`、`call_targets`、`call_routing_plans`、`call_flow_versions`、`call_duration_payout_rules`、`call_duplicate_rules`、`call_buyer_disposition_events` 或 `call_dispute_cases` 时，必须保存 buyer_id、target_id、routing_plan_id、qualified_duration_seconds、duplicate_window_days、payout_amount、revenue_amount、buyer_hours、cap_limit、disposition、source_url、reviewer 和 decision；不要补电话、不模拟通话、不伪造 duration/disposition/payout、不用机器人或循环拨打制造 qualified call。

Ping/Post 和 buyer routing V1 已有 `calculate_ping_post_routing_review()`、`/ping-post-routing` 和 `ping_post_routing_reviews`。任何 routing mode、exclusive/shared/aged、buyer cap、fallback、ping field schema、buyer feedback 或 lead marketplace 判断都必须保存 consent/disclosure 版本、PII level、fields sent schema、buyer response/reject reason、cap snapshot、suppression/DNC、source policy、expected payable value、safe CPL、human_review 和 source_urls。修改评分器时必须同步更新 `/ping-post-routing` 表单、smoke test、acceptance audit 和 [Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)。后续可拆分 `lead_ping_events`、`buyer_bid_responses`、`lead_post_events`、`lead_cap_snapshots`、`buyer_feedback_events` 或 `lead_consent_share_records`；不要在 URL、subid、日志或测试数据里写入完整 PII，不做未披露 shared lead、不自动 post lead、不自动外呼或短信、不绕过 DNC/TCPA、不用 Ads Cookie 后台操作。

Lead Freshness / Aged Lead 扩展前先阅读 [Lead Freshness、Aged Lead 与 Recontact Window 治理手册](lead_freshness_aged_recontact_governance.md)。新增 `lead_age_snapshots`、`lead_recontact_policies`、`aged_lead_inventory_batches`、`aged_lead_buyer_terms`、`lead_age_quality_daily` 或 `lead_recycled_handoff_history` 时，必须保存 original_submit_time、lead_age_bucket、consent_version、suppression_status、buyer_terms_version、payout_tier、contact_disposition、source_url、reviewer 和 decision；不要伪造 timestamp，不自动拨号/短信群发，不把 aged/recycled lead 当 fresh lead，不用旧 consent 绕过 DNC/opt-out。

Lead Form 漏斗扩展前先阅读 [Lead Form 漏斗、资格问题与移动端 UX 治理手册](lead_form_funnel_qualification_ux.md)。新增 `lead_form_versions`、`lead_form_fields`、`lead_form_step_events`、`lead_form_error_events` 或 `lead_form_quality_scores` 时，必须保存 field purpose、required_by、reject_reason_prevented、pii_level、disclosure_version、consent_version、cta_version、mobile_layout_version 和 reviewer；不要保存真实 phone/email/name/address 测试数据，不自动提交表单、不补字段、不隐藏 disclosure、不把 submitted lead 默认设为 primary conversion。

Lead Consent Proof 扩展前先阅读 [Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)。新增 `lead_consent_versions`、`lead_consent_events`、`lead_certificate_refs`、`lead_page_snapshots`、`buyer_disclosure_versions`、`lead_suppression_sync_events` 或 `lead_consent_dispute_cases` 时，必须保存 consent_text_hash、certificate_provider、certificate_ref_hash、form_version、buyer_disclosure_version、contact_channels_allowed、submit_timezone、suppression_status、source_url、reviewer 和 decision；不要伪造 certificate，不自动 post 给未披露 buyer，不把完整 PII 写入 URL/subid/log/prompt，不用旧 consent 绕过 DNC/opt-out。

Lead validation 和 suppression 扩展前先阅读 [Lead 验证、Suppression、去重与 PII 治理手册](lead_validation_suppression_pii_governance.md)。新增 `lead_validation_events`、`lead_identifier_hashes`、`lead_suppression_records`、`lead_privacy_requests`、`lead_retention_policies` 或 `lead_export_reviews` 时，必须使用字段白名单、hash/salt 策略、PII 最小化、retention/deletion、access log 和 reviewer；测试数据不得包含真实 phone/email/name/address，系统不得自动生成用户资料、补填字段、绕过 DNC/TCPA、忽略 opt-out 或把 invalid/duplicate/suppressed lead 回传为正向 conversion。

Speed-to-Lead 和联系 SLA 扩展前先阅读 [Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)。新增 `lead_contact_attempts`、`lead_contact_dispositions`、`call_center_capacity_snapshots`、`lead_callback_tasks`、`lead_opt_out_sync_events` 或 `call_recording_qa_reviews` 时，必须保存 consent/suppression 检查、attempt channel、disposition、agent/team、hours、capacity、reviewer 和 source evidence；不要接自动拨号器、短信群发、机器人通话、录音文件存储、虚假 call duration 或任何绕过 DNC/TCPA 的逻辑。

Buyer Capacity / Dayparting V1 已有 `calculate_buyer_capacity_review()`、`/buyer-capacity` 和 `buyer_capacity_reviews`。任何接量、cap pacing、dayparting、call-heavy 或 fallback 判断都必须保存 buyer、vertical、geo、buyer/account/user/call-center timezone、cap limit/used、elapsed day、expected next-hour/daily leads、hourly contact capacity、expected paid value、accepted/qualified/paid、no buyer、missed contact、after-hours、cap freshness、hours/ad schedule/timezone/holiday、fallback policy、source quality、overdelivery guardrail、human_review 和 source_urls。修改评分器时必须同步更新 `/buyer-capacity` 表单、smoke test、acceptance audit 和 [Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md)；不要自动改 Google Ads 后台、不自动外呼、不补 lead、不用 fallback 做 cloaking 或未披露转售。

Appointment Lead V1 已有 `calculate_appointment_lead_review()`、`/appointment-leads` 和 `appointment_lead_reviews`。任何预约型 Offer、booking payout 或 showed/paid value 测试都必须保存 buyer、vertical、service、geo、appointment platform、payout_event、request/book/confirm/show/complete/paid rate、cancel/no-show/duplicate/reschedule、calendar capacity、slot delay、reminder consent、buyer terms、offline conversion mapping、human_review 和 source_urls。修改评分器时必须同步更新 `/appointment-leads` 表单、smoke test、acceptance audit 和 [Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md)；不要把 booked 当 paid，不自动创建预约、不自动外呼或群发短信、不伪造 showed/paid、不把 booked 默认回传为 primary conversion。

CPL 垂类经济 V1 已有 `calculate_cpl_vertical_review()`、`/cpl-verticals` 和 `cpl_vertical_reviews`。任何垂类测试都必须保存 vertical/subvertical、payout model、payout、estimated CPC、landing CVR、accepted/qualified/paid rate、deduction/chargeback、feedback lag、contact SLA、qualification field purpose、reject reason map、accepted definition、paid definition、buyer terms、consent/disclosure、PII 最小化、license/certification evidence、forbidden claims、policy sources、human_review 和 source_urls。修改评分器时必须同步更新 `/cpl-verticals` 表单、smoke test、acceptance audit 和 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)；不要把不同垂类共用同一套质量阈值，不生成虚假资质、官方关系、收益/批准/胜诉承诺，也不自动绕过受限垂类认证。

Insurance / Medicare / ACA / Final Expense Lead 扩展前先阅读 [Insurance、Medicare / ACA 与 Final Expense Lead 治理手册](insurance_medicare_aca_final_expense_lead_governance.md)。新增 `insurance_vertical_profiles`、`insurance_qualification_fields`、`insurance_enrollment_windows`、`insurance_buyer_terms`、`insurance_buyer_acceptance_events`、`insurance_claim_reviews`、`insurance_license_authorization_refs` 或 `insurance_offline_value_maps` 时，必须保存 subvertical、state/county、eligibility bucket、enrollment window source URL、licensed agent/broker 或 buyer authorization reference、consent/disclosure version、reject reason、offline stage、reviewer 和 decision；不要冒充 Medicare/Marketplace/carrier，不生成虚假资质、保证省钱/批准 claim，不自动外呼/短信群发，不把 submitted、duration 或 booked 默认当 paid revenue。

Loan / Mortgage / Credit / Debt Lead 扩展前先阅读 [Loan、Mortgage、Credit 与 Debt Lead 治理手册](loan_mortgage_credit_debt_lead_governance.md)。新增 `financial_vertical_profiles`、`financial_qualification_fields`、`financial_disclosure_versions`、`financial_buyer_terms`、`financial_buyer_acceptance_events`、`financial_claim_reviews`、`financial_license_authorization_refs`、`financial_comparison_ranking_reviews` 或 `financial_offline_value_maps` 时，必须保存 subvertical、state、loan/debt/credit bucket、license_or_authorization_ref、financial disclosure version、buyer disclosure version、compensation/ranking disclosure、reject reason、offline stage、source_url、reviewer 和 decision；不要伪造贷款申请、收入、信用、身份或资质，不冒充 lender/government/servicer，不自动外呼/短信群发，不把 submitted、accepted、prequalified 或 duration 默认当 funded/paid revenue。

Legal Case Intake / Mass Tort / Personal Injury Lead 扩展前先阅读 [Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理手册](legal_case_intake_mass_tort_lead_governance.md)。新增 `legal_vertical_profiles`、`legal_qualification_fields`、`legal_case_type_rules`、`legal_attorney_buyer_terms`、`legal_intake_events`、`legal_attorney_review_events`、`legal_claim_reviews`、`legal_referral_disclosure_versions` 或 `legal_offline_value_maps` 时，必须保存 practice_area、jurisdiction、case_type、incident_date_bucket、representation_status、attorney/law firm/intake/lead generator role、disclosure/consent version、attorney_review_status、retainer_status、reject_reason、offline_stage、source_url、reviewer 和 decision；不要伪造案件/事故/伤害，不冒充律师/律所/法院/政府，不提供未经授权法律建议，不自动外呼/短信群发，不把 submitted、intake qualified、booked 或 duration 默认当 paid case。

Home Services / Solar / Local Services Lead 扩展前先阅读 [Home Services、Solar 与 Local Services Lead 治理手册](home_services_solar_local_services_lead_governance.md)。新增 `home_service_vertical_profiles`、`contractor_buyer_profiles`、`contractor_license_refs`、`service_area_rules`、`dispatch_capacity_snapshots`、`home_service_lead_events`、`home_service_disposition_events`、`lsa_credit_dispute_events`、`solar_qualification_reviews` 或 `home_service_offline_value_maps` 时，必须保存 service_category、service_type、zip/city、service_area_match、urgency、contractor license/insurance ref、hours/capacity status、lead disposition、booked/showed/sold/completed status、credit_status、source_url、reviewer 和 decision；不要伪造本地地址、Google badge、license、insurance、review、job outcome，不自动外呼/短信群发，不把 submitted、call click、booked 或 LSA charged lead 默认当 paid job。

Education / Career Training / Student Lead 扩展前先阅读 [Education、Career Training 与 Student Lead 治理手册](education_career_training_student_lead_governance.md)。新增 `education_vertical_profiles`、`education_program_profiles`、`education_authorization_refs`、`education_qualification_fields`、`education_claim_reviews`、`education_buyer_terms`、`education_enrollment_events`、`education_reject_reason_maps` 或 `education_offline_value_maps` 时，必须保存 program_type、school_type、state、modality、authorization/accreditation/licensure source URL、program fit、eligibility bucket、claim proof、financial aid/student loan disclosure、buyer acceptance status、application/enrollment/class start/paid stage、reviewer 和 decision；不要伪造学生资料、学历、成绩、FAFSA、身份、授权、认证、录取、就业、薪资或 enrollment，不自动外呼/短信群发，不把 inquiry、application 或 advisor call 默认当 paid enrollment。

Healthcare / Medical Appointment / Clinic Lead 扩展前先阅读 [Healthcare、Medical Appointment 与 Clinic Lead 治理手册](healthcare_medical_appointment_lead_governance.md)。新增 `healthcare_vertical_profiles`、`healthcare_provider_refs`、`healthcare_qualification_fields`、`healthcare_claim_reviews`、`healthcare_tracking_reviews`、`healthcare_appointment_events`、`healthcare_reject_reason_maps` 或 `healthcare_offline_value_maps` 时，必须保存 service_type、provider/clinic role、state/city、license/insurance/source URL、field sensitivity、privacy/consent version、tracking review、claim proof、appointment status、showed/treated/paid stage、reject_reason、reviewer 和 decision；不要伪造医生/诊所/资质/保险网络/预约/到诊/治疗结果，不收集不必要 PHI，不把健康状态写入 URL/event/subid，不自动外呼/短信群发，不把 submitted、duration、requested 或 booked 默认当 paid patient。

B2B SaaS / Professional Services / Demo Lead 扩展前先阅读 [B2B SaaS、Professional Services 与 Demo Lead 治理手册](b2b_saas_professional_services_lead_governance.md)。新增 `b2b_vertical_profiles`、`b2b_qualification_fields`、`b2b_account_fit_rules`、`b2b_persona_rules`、`b2b_claim_reviews`、`b2b_pipeline_events`、`b2b_reject_reason_maps` 或 `b2b_offline_value_maps` 时，必须保存 category、ICP、company size、industry、role/persona、use_case、consent version、claim proof、MQL/SAL/SQL/opportunity/won/PQL stage、reject_reason、source_url、reviewer 和 decision；不要伪造公司、职位、预算、采购意向、客户 logo、review、security certification 或 pipeline，不抓取/滥用个人联系人，不自动外呼/短信群发，不把 download、trial、form submit 或 demo request 默认当 paid pipeline。

Crypto / Investment / Trading Lead 扩展前先阅读 [Crypto、Investment 与 Trading Lead 治理手册](crypto_investment_trading_lead_governance.md)。新增 `financial_offer_profiles`、`financial_license_refs`、`financial_claim_reviews`、`financial_risk_disclosures`、`financial_lead_events`、`financial_reject_reason_maps` 或 `financial_offline_value_maps` 时，必须保存 product_type、target_geo、certification_requirement、license_or_registration_ref、risk_disclosure_version、claim proof、lead/signup/KYC/funded/trade/paid/chargeback stage、reject_reason、source_url、reviewer 和 decision；不要伪造监管资质、收益、KYC、交易、入金、提现或 paid event，不收 seed phrase/private key/KYC 文件，不绕 Google/地区认证，不自动外呼/短信群发，不把 submit、install、signup 或 KYC started 默认当 paid investor。

Employment / Recruiting / Staffing Lead 扩展前先阅读 [Employment、Recruiting 与 Staffing Lead 治理手册](employment_recruiting_staffing_lead_governance.md)。新增 `employment_vertical_profiles`、`employment_job_orders`、`employment_qualification_fields`、`employment_claim_reviews`、`employment_targeting_reviews`、`employment_candidate_events`、`employment_reject_reason_maps` 或 `employment_offline_value_maps` 时，必须保存 job_category、buyer_type、employer/recruiter role、job_order_source_url、pay/remote/employment_type proof、HEC/targeting review、candidate data sensitivity、lead/screened/qualified/interview/hire/start/paid stage、reject_reason、reviewer 和 decision；不要伪造岗位、雇主、简历、证书、面试、入职或 paid event，不做歧视性筛选，不收不必要 SSN/证件/银行信息，不自动外呼/短信群发，不把 submit、resume upload、call connected 或 interview scheduled 默认当 paid placement。

Gambling / Sweepstakes / Sports Betting Lead 扩展前先阅读 [Gambling、Sweepstakes 与 Sports Betting Lead 治理手册](gambling_sweepstakes_sports_betting_lead_governance.md)。新增 `gambling_offer_profiles`、`gambling_license_refs`、`gambling_claim_reviews`、`gambling_responsible_messages`、`gambling_lead_events`、`gambling_reject_reason_maps` 或 `gambling_offline_value_maps` 时，必须保存 product_type、target_geo、Google certification、operator license、age/geo/self-exclusion controls、responsible gambling message、bonus/sweepstakes terms proof、registration/KYC/deposit/wager/NGR/paid stage、reject_reason、reviewer 和 decision；不要伪造 license、age、geo、KYC、deposit、wager、NGR 或 paid event，不绕 certification/geo/self-exclusion，不收 payment/KYC 高敏资料，不自动外呼/短信群发，不把 install、registration 或 bonus claimed 默认当 paid player。

Addiction Treatment / Rehab / Behavioral Health Lead 扩展前先阅读 [Addiction Treatment、Rehab 与 Behavioral Health Lead 治理手册](addiction_treatment_rehab_behavioral_health_lead_governance.md)。新增 `addiction_offer_profiles`、`addiction_provider_refs`、`addiction_privacy_reviews`、`addiction_claim_reviews`、`addiction_admissions_events`、`addiction_reject_reason_maps` 或 `addiction_offline_value_maps` 时，必须保存 service_type、provider/referral role、certification/license source URL、Part 2/HIPAA tracking review、crisis SOP、claim proof、call/assessment/verification/admitted/started/paid stage、reject_reason、reviewer 和 decision；不要伪造 provider、certification、license、insurance、clinical assessment、admission、treatment start 或 paid event，不绕 LegitScript/Google certification，不收不必要 SUD/PHI 高敏资料，不自动外呼/短信群发，不把 call duration、form submit 或 admissions call 默认当 paid treatment。

Government Services / Immigration / Public Benefits Lead 扩展前先阅读 [Government Services、Immigration 与 Public Benefits Lead 治理手册](government_services_immigration_public_benefits_lead_governance.md)。新增 `government_service_profiles`、`government_authorization_refs`、`government_fee_disclosures`、`government_claim_reviews`、`government_identity_data_reviews`、`government_service_events`、`government_reject_reason_maps` 或 `government_offline_value_maps` 时，必须保存 service_type、agency、geo、official relationship、certification / authorization source URL、professional role、official fee、service fee、refund policy、claim proof、identity data review、lead/consult/prepared/filed/receipt/issued/paid stage、reject_reason、reviewer 和 decision；不要冒充政府或授权方，不伪造 USCIS/IRS/SSA/DMV/passport/vital records 关系，不提供未经授权法律/移民/税务建议，不收不必要 SSN/passport/A-number/tax/benefit/login 文件，不把 quiz、lead submit、call connected 或 document checklist 默认当 issued / paid outcome。

Lead Pricing 和 payout negotiation V1 已有 `calculate_lead_pricing_review()`、`/lead-pricing` 和 `lead_pricing_reviews`。任何谈价、rate card 或 payout 测试都必须保存 buyer、vertical、geo、source_type、exclusivity、payout_model、headline/unit/proposed/floor payout、accepted/qualified/approval/paid rate、return/scrub/chargeback、cap、expected volume、return window、payment term、quality evidence、source transparency、consent evidence、invoice evidence、dispute reserve、buyer terms、human_review 和 source_urls。修改评分器时必须同步更新 `/lead-pricing` 表单、smoke test、acceptance audit 和 [Lead Pricing、Payout Negotiation 与结算安全垫治理手册](lead_pricing_payout_negotiation_governance.md)；不要把 headline payout 当 safe CPC，不自动谈价、不自动改 buyer routing、不伪造质量或隐藏来源。

决策窗口扩展前先阅读 [决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md)。现有 `calculate_decision_window()` 是保守评分器，新增字段或规则时必须同步更新 `/decision-windows` 表单、smoke test、acceptance audit 和文档。任何 budget ramp、pause、wait、close 或 settlement 决策都必须绑定 data_status、lag_profile、cohort_date、revenue_status 和 evidence_url；自动化只能生成建议和任务，不把当天 ROI 当最终利润，不通过补量、伪造转化或改历史报表填平延迟。

预算节奏扩展前先阅读 [预算节奏、扩量与止损手册](budget_pacing_scaling_stoploss.md)。现有 `calculate_budget_pacing()` 是保守评分器，新增规则时必须同步更新 `/budget-pacing` 表单、smoke test、acceptance audit 和文档。任何 budget ramp、pause、reduce、dayparting 或 bid adjustment 决策都必须绑定 test_budget、hard_stop、safe_cpc、actual_cpc、revenue_status、cash_buffer_days、source_urls 和 reviewer；自动化只能生成人工审批建议，不自动改 Google Ads daily budget、bid strategy、ad schedule 或后台 Recommendations。

Offer Cap / Payout 扩展前先阅读 [Offer Cap、Payout、状态变更与替代 Offer 治理手册](offer_cap_payout_status_governance.md)。现有 `calculate_offer_cap_review()` 是保守评分器，新增字段或规则时必须同步更新 `/offer-cap-payout` 表单、smoke test、acceptance audit 和文档。任何 cap、payout、paused、expired、quality_hold 或 replacement offer 决策都必须绑定 source_urls、effective_from/captured_at、cap scope、approval/paid/deduction 口径和 reviewer；自动化只能生成人工审批建议，不自动登录 affiliate network、Google Ads 或发布商后台，不自动切换未审核 Offer，不通过隐藏目的地、cloaking 或换号处理 cap 或拒付。

单位经济模型扩展前先阅读 [单位经济模型、Break-even 与安全边际手册](unit_economics_margin_safety.md)。任何 break-even、safe CPC、safety factor、test budget 或 hard stop 结果都必须保存输入假设、收入状态、样本窗口和版本；计算结果只能进入投放草稿、审批和风险审计，不自动买量、不用后台 Cookie 改预算、不把 gross revenue 当 payable revenue。

归因增量 V1 已有 `calculate_attribution_review()`、`/attribution` 和 `attribution_reviews`。任何 attributed revenue、incremental revenue、iROAS、holdout 或 lift 结论都必须保存 control/treatment、date range、split method、revenue maturity、sample、confidence、Change history、approved/paid evidence、human_review 和 source_urls。修改评分器时必须同步更新 `/attribution` 表单、smoke test、acceptance audit 和 [归因、增量性与流量蚕食治理手册](attribution_incrementality_cannibalization.md)；系统不得用补点击、伪造转化、隐藏来源、Cookie 后台操作或多账号切换制造 lift。

订阅 LTV 扩展前先阅读 [订阅、试用、退款、Chargeback 与 LTV 治理手册](subscription_refund_ltv_chargeback_governance.md)。任何 trial、renewal、refund、chargeback、clawback 或 net LTV 导入都必须保存 cohort、source_file_hash、order/status evidence、timezone 和 reviewer；系统不得隐藏价格/续费条款，不得阻碍取消，不得用伪造续费或换账号处理争议。

Campaign 命名、Labels、UTM/SubID 与维度治理 V1 已有 `taxonomy_reviews` 和 `/taxonomy-governance`，用于保存 campaign/ad group name、labels、UTM、ValueTrack、custom parameter、SubID map、dimension dictionary version、parameter map version、landing/link/creative version、payload hash、report join gap、gclid/click_id 保留、PII/敏感属性检查、Taxonomy Score、risk_level、recommended_action、blockers、状态和来源 URL；状态更新写入 `audit_logs`。后续如果拆分数据仓库，可以新增 `dimension_dictionary`、`campaign_name_registry`、`tracking_parameter_maps`、`label_snapshots`、`version_registry` 和 `report_join_audits`。修改 `calculate_taxonomy_review()` 时，必须同步更新 `/taxonomy-governance` 表单、smoke test、acceptance audit 和文档。新增导入器或导出器时必须先写字段合同和 QA，不要把 campaign name、label 或 subid 当作唯一事实来源，也不要把 PII、Cookie、验证码、账号凭据或敏感属性写入 URL 参数。

季节性需求预测扩展前先阅读 [季节性、事件日历与需求预测手册](seasonality_event_demand_forecasting.md)。新增导入器只能保存人工导出的 Keyword Planner、Trends、Insights、Search Terms 或官方日历证据，必须记录 source_url、retrieved_on、country、language、timezone、query_cluster 和数据窗口；新增自动化只能生成 readiness、budget ramp、exit rule 和 postmortem 建议，不自动追热点、不用 Cookie 后台改预算、不用代理/指纹伪装地区、不生成误导季节性 claim。

Search Terms / Query Mining 扩展前先阅读 [Search Terms、否定词与 Query Mining 治理手册](search_terms_negative_keyword_query_mining.md)。现有 `calculate_query_mining_review()` 是保守评分器，新增字段或规则时必须同步更新 `/query-mining` 表单、smoke test、acceptance audit 和文档。任何导入器都必须保留 source_file_hash、date range、timezone、customer/campaign/ad_group、keyword、match type、search_term、network、device、geo 和 revenue status；任何导出器只能生成待审核 negative keyword、exact/phrase promotion、split ad group 或 page brief，不自动登录后台、不模拟搜索、不点击广告、不绕过 search terms 隐私聚合、不用代理/指纹伪装地区。

异常监控、告警和止损队列扩展前先阅读 [异常监控、告警、止损队列与事故分诊手册](anomaly_monitoring_alerting_stoploss_incident_triage.md)。建议新增 `alert_rules`、`alert_events`、`incident_cases` 和 `incident_evidence_links`，用于保存 rule_key、metric_scope、threshold_json、trigger_values、evidence_urls、owner、containment、root_cause 和 postmortem。规则必须有样本阈值、时间窗口、cooldown 和安全动作类型；L3 只能生成冻结/停量/回滚建议和证据包，不要自动登录后台、补点击、伪造 conversion、切换账号或隐藏目的地。

来源质量治理扩展前先阅读 [Source、Publisher、Placement 质量评分与名单治理手册](source_publisher_placement_quality_governance.md)。现有 `calculate_source_quality_review()` 是保守评分器，新增字段或规则时必须同步更新 `/source-quality` 表单、smoke test、acceptance audit 和文档。任何导入器都必须保留 source_file_hash、date range、timezone、source_id、publisher_id、placement_id、subid、campaign_id、device、geo 和 landing_version；任何导出器只能生成待审核 placement exclusion、negative keyword、停源或恢复建议，不自动买量、不自动改 Google Ads 后台、不隐藏来源、不生成代理/指纹/Worker 转发配置。

Portfolio 组合治理扩展前先阅读 [Portfolio 预算分配、风险集中度与组合治理手册](portfolio_budget_allocation_risk_concentration.md)。现有 `calculate_portfolio_allocation()` 是保守评分器，新增字段或规则时必须同步更新 `/portfolio-allocation` 表单、smoke test、acceptance audit 和文档。所有 exposure 计算都必须区分 reported、pending、approved、finalized、paid、deducted、held，不得把 estimated revenue 直接作为可用现金；任何自动化只能生成 allocation decision 和人工审批任务，不自动登录后台改预算、不绕过账单风控、不用新账号或隐藏来源掩盖组合风险。

流量供应商合同与争议治理扩展前先阅读 [流量供应商合同、IO、退款与争议治理手册](traffic_vendor_contract_io_dispute_governance.md)。现有 `calculate_vendor_contract_review()` 是保守评分器，新增字段或规则时必须同步更新 `/vendor-contracts` 表单、smoke test、acceptance audit 和文档。合同和 IO 附件可以保存文件引用、hash、版本、审批人和关键条款摘要，但不要在数据库保存供应商后台密码、Cookie、个人敏感数据或未授权客户名单；dispute case 只能生成证据包、credit/refund/makegood 记录和人工任务，不自动扣款、不自动威胁供应商、不生成低质量 makegood 流量。

### 7.3.1 账号治理扩展

账号/MCC/付款/验证治理可新增 `account_governance_profiles`、`mcc_hierarchy_snapshots`、`account_access_reviews`、`billing_profile_checks`、`advertiser_verification_cases`、`agency_client_relationships`、`account_budget_controls`、`account_incident_evidence`，用于记录 owner、业务主体、付款主体、访问权限、Advertiser Verification、代理关系、account budget 和事故证据。这些表只做资产治理、权限审计和证据留存，不做批量建号、账号池、规避封禁或防关联操作。

### 7.4 页面质量审计

可扩展：

- Lighthouse/Pagespeed 指标。
- 广告密度检测。
- 截图归档。
- 页面主题分类。
- 隐私和条款链接验证。
- 独立 `landing_evidence` 表：记录 CTA、price/value、claim、proof/review、form、disclosure 等 snippet。
- `creative_claim_map`：记录每条 headline/description 对应的 proof snippet 和人工核查状态。
- `review_disclosure_check`：检查用户评价、评分、案例、affiliate disclosure 和激励关系披露。

### 7.4.1 追踪链 QA

可扩展安全检查：

- 展开 tracking template 和 Final URL suffix。
- 检查 `gclid`、UTM、click_id、subid 是否保留。
- 记录 redirect hops、status code、duration 和最终页面。
- 对 postback transaction_id 做去重测试。

这些检查只能用于测量、排错和审计，不能用于按 AdsBot、IP、Cookie、设备指纹或账号状态分流页面。

### 7.5 任务调度

当前 `task_jobs` 只做任务记录和手动执行。后续可接：

- APScheduler：适合单机 interval 任务。
- Celery/RQ：适合多进程和重试队列。
- 外部 cron：适合部署简单任务。

无论使用哪种调度器，都必须写入 `audit_logs`，并且任务类型不能执行 Cookie 接管、补点击、cloaking 或规避封禁动作。

任务类型、任务名称和任务备注都必须通过 `services/tasks.py` 的白名单和危险语义检查。任何包含 login、password、OTP、2FA、captcha、challenge、recovery、cookie、session、token refresh、click、impression、visit、traffic、referer、scroll、bounce、autosurf、proxy pool、fingerprint、worker forward、cloaking、account pool 或 ban evasion 语义的任务都应被拒绝创建；认证失败应作为账号安全事件进入人工处理，追踪或收入缺口应进入对账和来源隔离，而不是后台任务重试或补量。

扩展任务调度前先对照 [任务编排、安全审批、执行日志与事故复盘手册](task_orchestration_approval_audit_runbook.md)。生产化版本建议增加 `task_approvals`、`task_run_logs`、`task_payload_versions`、`external_change_events`、`incident_reviews` 和 `automation_guardrails`，用于保存审批、输入 hash、外部变更证据、回滚点和事故复盘，而不是扩大后台自动写入范围。

### 7.6 研究来源库

`research_sources` 用来把行业知识的来源 URL 结构化保存。建议新增资料时至少填写：

- `topic`：研究主题。
- `capability`：如果属于高风险能力或受众/再营销合规主题，填对应能力标识。
- `title`、`url`、`publisher`。
- `source_type`：policy、official_api、technical_reference、product_page 等。
- `reliability`：primary、public_claim、industry_reference、secondary。
- `review_status`：candidate、accepted、needs_update、archived。
- `claim_summary`：该来源支撑的判断。

来源库只做证据追踪，不触发广告后台动作。`review_status` 只表示知识库维护进度，状态变更写入 `audit_logs`，不能作为自动投放、自动换链接、Cookie 操作或高风险能力放行条件。

## 8. 安全和合规约束

代码层必须避免：

- 存储 Ads Cookie、浏览器 Profile、Session Token。
- 存储代理指纹用于规避检测。
- 生成补点击任务。
- 自动拨号、短信群发、伪造电话、绕过 consent/DNC/TCPA 或把用户数据转售给未披露买方。
- 生成 cloaking 或审核绕过配置。
- 自动改最终 URL 绕审核。
- 存储 Customer Match 名单、PII、email、phone 或未经授权的客户数据。

如果未来新增自动执行功能，必须满足：

- 明确的人工审核状态。
- 审计日志。
- 可回滚。
- 使用官方或可接受的导入/脚本方式。
- 对最终 URL 与广告承诺做一致性检查。

链接计划创建时会拒绝明显包含 cloaking、Googlebot/AdsBot、审核页/用户页、绕审核、隐藏真实目的地等语义的输入。这类需求应进入 `/risk-audits`，而不是保存为可轮换链接计划。

账号配置创建时会拒绝明显包含 Cookie 登录、Cookie 操作、Session Token、浏览器 Profile、自动登录、2FA / MFA 绕过、安全挑战绕过、代理池、指纹 Profile、Worker 转发、账号池、批量开户、规避封禁、防关联、封禁后换号继续投放等语义的输入。账号页用于状态备注、修复证据和申诉复盘，不是会话接管、封禁规避、防关联或账号池管理器。

## 9. 常见问题

### 9.1 为什么默认 SQLite？

为了本地快速验证。正式部署仍按用户要求支持 MySQL，通过 `DATABASE_URL` 切换。

### 9.2 为什么没有多租户？

用户已明确第一版先不要多租户。当前系统面向单团队工作台。

### 9.3 为什么不做 Cookie 操作？

Ads Cookie 操作会触及账号安全、未授权访问、2FA 绕过、安全挑战和 cookie theft 风险。系统目标是业务知识和可审计流程，不是绕过平台安全机制。
