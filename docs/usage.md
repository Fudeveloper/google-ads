# 使用文档

更新时间：2026-06-09

本文说明如何用 Ads Arbitrage Workbench 跑一次单团队 Ads 套利测试闭环。

## 1. 启动

开发环境可先用 SQLite 验证：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask --app app db-init
flask --app app seed
flask --app app run --debug --port 5058
```

生产或接近生产环境使用 MySQL：

```bash
docker compose up -d mysql
copy .env.example .env
flask --app app db-init
flask --app app seed
flask --app app run --debug --port 5058
```

`.env.example` 只提供 Flask 和 MySQL 连接配置。不要把 Google Ads Cookie、Session Token、浏览器 Profile、代理池、指纹配置、Worker 规避规则或账号池资料写入 `.env`。

然后打开：

```text
http://127.0.0.1:5058
```

## 2. 一次完整业务流程

### 2.1 配置广告账号

进入 `广告账号` 页面，记录 Google Ads 账号、Customer ID 和同步方式。

推荐同步方式：

- Google Ads Editor CSV。
- Google Ads Scripts。
- Official Google Ads API。
- Manual Review。

账号页只保存配置和备注，不保存 Cookie、浏览器 Profile 或 Session Token。

账号配置可以记录 paused、needs_fix、appeal_submitted、suspended 等状态，用于修复证据和申诉复盘；不要把账号页当成账号池、封禁后换号或防关联继续投放的管理器。出现这类诉求应进入 `风险审计`，按修复和申诉流程处理。

账号/MCC、付款和验证信息要一起治理。每个账号建议在备注里写明 owner、业务主体、付款主体、MCC 层级、主要网站、Advertiser Verification 状态、代理/客户关系和 account budget 边界；不要用多个账号、多个付款资料或代理关系掩盖同一高风险业务。方法见 [账号、MCC、付款与 Advertiser Verification 治理手册](account_mcc_billing_verification_governance.md)。

### 2.2 录入 Offer

进入 `Offer` 页面，填写：

- 名称：Offer 或页面主题。
- 垂类：金融、SaaS、保险、教育、本地服务等。
- 国家和语言：用于创意和关键词生成。
- Payout 模式：CPA、CPL、CPS、RevShare 或 Display RPM。
- Payout/RPM：用于利润核算。
- 目标 URL：用户最终看到的页面。
- Tracking URL：联盟或内部跟踪链接。
- 政策备注：广告平台、联盟平台、页面承诺的限制。

建议：政策备注不要空。套利业务很多亏损不是公式问题，而是审核、扣量和无效流量问题。

Offer 运行中还要持续确认 cap、payout 和 status。daily/monthly/source/geo cap 快满、payout 变更、Offer paused/expired、buyer quality hold 或 payment hold 都应先进入 `/offer-cap-payout` 记录 cap limit/used、expected next conversions、当前/新 payout、approval/paid/deduction、buyer capacity、替代 Offer 审核和来源 URL。系统会生成 Offer Cap Score、risk_level、recommended_action、cap_remaining、effective_payout、safe_daily_media_cost 和 blockers；状态可标记为 waiting_cap_update、reduce_budget、pause_traffic、manual_replacement_ready 或 closed。状态只写审计日志，不自动改预算、不自动切换 Offer、不操作联盟后台。不要把替代 Offer 用作 cloaking、超 cap 继续灌量或规避拒付；详细方法见 [Offer Cap、Payout、状态变更与替代 Offer 治理手册](offer_cap_payout_status_governance.md)。

来源质量要和 Offer 状态一起看。进入 `/source-quality` 可以把 source、publisher、placement、subid、network、geo、device、sample URL、透明度、tracking 完整度、intent fit、click/session、reported/approved/paid/deducted revenue、invalid clicks、complaints、buyer reject、policy issue、停源控制和来源 URL 固化成评审记录。系统会生成 Source Quality Score、quality_level、recommended_action、click_session_rate、approved_rate、paid_rate、deduction_rate、paid_roi、approved_roi 和 blockers；allowlist 可进入小步扩量审批，watchlist 不扩量，quarantine 暂停新增预算，blocklist 禁止复测。状态只代表内部名单治理，不会自动买量、改广告后台、隐藏来源或模拟访问。详细方法见 [Source、Publisher、Placement 质量评分与名单治理手册](source_publisher_placement_quality_governance.md)。

外部供应商、媒体直采和 newsletter buy 在首投前要先进入 `/vendor-contracts` 记录 vendor、IO、line item、contract status、pricing、来源明细、tracking appendix、reporting appendix、quality clause、refund / credit / makegood clause、stop control、reporting discrepancy、invalid traffic、buyer reject、invoice、disputed amount、payment terms、policy issue 和来源 URL。系统会生成 Vendor Contract Score、risk_level、recommended_action、amount_at_risk、paid_roi、approved_roi、invoice_dispute_rate、credit_coverage_rate 和 blockers；状态可标记为 preapproved、active_test、active_scale、watchlist、dispute_open、suspended、blocked 或 closed。不要只凭聊天承诺买流量；无法提供来源明细、无法按 source 停量、拒绝追踪参数或要求隐藏来源的供应商，不能进入扩量。详细方法见 [流量供应商合同、IO、退款与争议治理手册](traffic_vendor_contract_io_dispute_governance.md)。

### 2.3 做套利测算

进入 `套利测算` 页面，输入：

- 收入模型：CPA/CPL/CPS/Display RPM。
- Session RPM 或 Payout。
- CVR。
- 买量 CPC。
- 安全系数。
- 目标点击。
- 政策、内容、追踪、来源分。
- 现金缓冲天数。

系统会计算：

- RPV/EPC。
- 盈亏平衡 CPC。
- 安全 CPC。
- 安全边际。
- 预期收入、成本、利润、ROI。
- 最小样本点击。
- 测试预算。
- 硬止损。
- 机会评分和建议动作。

建议：只有 `test` 或 `small_test` 的机会才进入投放草稿；`hold` 和 `reject` 先修页面、素材、追踪或流量来源。Break-even CPC 必须基于可收款 RPV/EPC，Safe CPC 要乘以 safety factor，Safety Margin 低于 10% 时只适合极小样本测试。公式、情景分析和 hard stop 方法见 [单位经济模型、Break-even 与安全边际手册](unit_economics_margin_safety.md)。

多个机会同时运行时，要把预算分成 Core、Scale、Test、Explore 和 Quarantine。不要只看单个 campaign ROI；还要看单一 Offer、source、account、revenue partner、country 和 pending revenue 是否过度集中。进入 `/portfolio-allocation` 可以录入 portfolio bucket、monthly media budget、proposed allocation、reported/pending/approved/finalized/paid/deducted revenue、集中度、现金缓冲、来源质量、policy 风险和事故状态，系统会生成 Portfolio Allocation Score、risk_level、recommended_action、cash_at_risk、revenue_quality_ratio 和 blockers。状态可标记为 waiting、approved_for_manual_allocation、reduce_exposure、quarantine 或 closed；状态只写审计日志，不自动改预算。组合预算方法见 [Portfolio 预算分配、风险集中度与组合治理手册](portfolio_budget_allocation_risk_concentration.md)。

### 2.4 采集和审计落地页

进入 Offer 详情，点击“采集”。

系统会记录：

- HTTP 状态。
- Title、Description、H1/H2。
- 页面字数。
- 内链和外链数量。
- CTA texts、price/value snippets、claim snippets、proof/review snippets。
- 表单数量和用户可填写字段数量。
- 透明度信号，例如 privacy、contact、about、terms。
- 与 Offer 名称和垂类的粗略相关性。

质量分不是 Google 官方分数，只是内部审计指标。低分页面不建议进入买量测试。

落地页摘要会把素材证据写入 `raw_summary`。如果页面有强声明但没有评价、案例、评分、认证、编辑披露或其他 proof，系统会提示先做事实核查。详细方法见 [落地页素材抽取、Offer Intelligence 与创意 Brief 手册](landing_offer_intelligence_creative_brief.md)。

生成 brief 前可以做少量公开竞品情报：查看 SERP 语境、Ads Transparency Center、Ad Preview and Diagnosis、Auction Insights、Keyword Planner 和 Trends，把市场 angle、页面差距和 claim 边界整理成 brief。不要点击竞品广告、批量抓取、复制文案、仿冒商标或用代理模拟地区；方法见 [竞品广告、SERP 与 Ads Transparency 情报手册](competitor_ad_intelligence_serp_transparency.md)。

季节性选题要提前做事件日历：用官方日期、Google Trends、Keyword Planner、Insights、search terms 和历史 paid revenue 判断需求窗口，再安排页面、创意、审核、测试预算、peak ramp 和 post-peak exit。不要把 Trends 分数当点击量，也不要在季节结束后继续按高峰预算烧支持、退款、取消类 query；详细方法见 [季节性、事件日历与需求预测手册](seasonality_event_demand_forecasting.md)。

### 2.5 生成创意和关键词

进入 Offer 详情，点击“生成”。

系统会生成 3 组角度：

- Problem Solution：解决问题型。
- Comparison：对比选择型。
- Guide Checklist：指南清单型。

每组包含：

- 15 个标题。
- 4 个描述。
- 30 个关键词。

生成结果需要人工审核，重点检查：

- 是否夸大收益。
- 是否暗示官方关系。
- 是否和落地页承诺一致。
- 是否会把用户引到与广告不一致的页面。
- 是否把页面没有的价格、折扣、认证、排名、评价或用户数写进创意。

创意生成会优先读取落地页摘要中的 claim/proof/CTA 线索。原则是 evidence-first：AI 或规则模板只能改写、压缩和组合已有证据，不能凭空补“best、guaranteed、official、save 70%”之类强声明。

Offer 详情页还会在每组创意下显示 `Claim 审核`。生成创意时系统会创建持久化审核记录，也可以点击 `刷新 Claim 审核` 重新按当前落地页 evidence 扫描。它会提示 guarantee、official、best/top/#1、free、save/discount、review/rating、scarcity、异常标点/大写等风险，并显示是否在落地页摘要中找到 price/proof/claim evidence 和对应来源 URL。

每条 Claim 审核记录可以标记为 `待复核/open`、`可保留/approved`、`需降级改写/rewrite_required`、`已阻止/blocked` 或 `已关闭/dismissed`。状态只代表内部人审结论，并写入 `/logs`；它不会自动修改 headline/description，不会自动提交 Google Ads，不会为了通过审核切换页面或换账号。详细方法见 [广告创意 Claim 审核与事实核查手册](creative_claim_review_fact_checking.md)。

创意上线后不要只保留“当前赢家”。建议把 angle、素材版本、landing version、关键词主题、拒登结果、paid RPV、buyer reject、AdSense deduction 和投诉反馈都回写到角度库，避免下次 AI 又生成同样的风险 claim。方法见 [Creative Angle Library、素材版本与反馈闭环手册](creative_angle_library_feedback_loop.md)。

广告被拒登或受限时，先不要换域名、换账号或重复提交同一套素材。进入 `广告审核` 页面创建案例，记录 Policy Manager 截图或证据 URL、policy topic、受影响对象、Final URL、expanded URL、页面证据、修改记录和申诉文字，再按 [Google Ads 广告审核、拒登、Policy Manager 与申诉证据包手册](google_ads_ad_review_disapproval_appeal_playbook.md) 做修复、申诉和复盘。

广告审核案例可以标记为 `待处理/open`、`已修复/fixed`、`申诉证据就绪/appeal_ready`、`已提交申诉/appeal_submitted`、`已通过/approved`、`申诉失败/rejected` 或 `已放弃/abandoned`。状态只表示内部证据包进度，并写入 `/logs`；系统不会自动提交 appeal，不会自动登录 Google Ads，不会通过 cloaking、Worker、换账号、换域名或隐藏目的地处理拒登。

如果后续接入多模型 AI Provider，必须把 prompt template、model、input evidence hash、output hash、token usage、estimated cost、review status 和 blocked reason 记录下来。AI 只能生成候选，不自动提交广告；Prompt 模板和成本治理见 [AI Provider、Prompt 模板与创意成本治理手册](ai_provider_prompt_cost_governance.md)。

### 2.6 创建投放草稿

进入 `投放草稿` 页面，选择 Offer 和创意组。

填写：

- Campaign 名称。
- 渠道。
- 日预算。
- 出价策略。
- Final URL。

草稿默认不会直接投放。页面可把草稿标记为 `草稿`、`评审中`、`已批准`、`已导出`、`暂停` 或 `拒绝`，这些状态只代表内部评审进度。点击 `CSV` 可导出 Google Ads Editor 风格 CSV；点击 `Script JSON` 可导出给 Google Ads Scripts 使用的结构化 payload。两种方式都需要投手或审核人确认。

导出前系统会执行 campaign preflight：草稿必须是 `已批准` 或 `已导出`；绑定创意不能存在 `待复核/open`、`需降级改写/rewrite_required` 或 `已阻止/blocked` 的 Claim 审核；绑定 campaign 的广告审核案例不能还处于 `open`、`appeal_submitted` 或 `rejected`。如果不满足，CSV、Scripts JSON 和任务中心里的导出检查都会被拦截，并写入 `/logs`。这道闸门只阻止不完整证据包进入人工导出流程，不会自动修改素材、提交广告或操作后台。

CSV 导出后，进入 `/bulk-upload` 为这个批次创建发布门禁记录：填写 batch/hash、目标 Customer ID、时区、币种、行数、关键词数、广告数、预算变化、URL 变化、preflight、Editor check、Bulk Upload preview、人工审核、默认 paused、回滚计划和来源 URL。系统会生成 Bulk Upload Score、risk_level、recommended_action 和 blockers；状态可标记为 preview_ready、approved_for_manual_post、posted_manual、partial_error、rollback_review、blocked 或 closed，并写入 `/logs`。这一步只管理证据和人工审批，不会自动导入、发布或修改 Google Ads 后台。完整流程见 [Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册](google_ads_editor_csv_bulk_upload_governance.md)。

如果使用 Scripts 流程，先阅读 [Google Ads Scripts 安全自动化手册](google_ads_scripts_safe_automation.md)，再把导出的 JSON 粘贴到 [Google Ads Scripts payload preview 模板](../scripts/google_ads_script_payload_preview.js)。模板默认 `PREVIEW_ONLY=true`、`ALLOW_APPLY=false`，用于在授权账号内预览和检查，不会使用 Cookie 或自动接管后台。

如果使用 Scripts 做报表同步，进入 `/scripts-sync` 记录同步评审：auth mode、sync type、script name、customer_id、date_range、query/report、source snapshot hash、payload/query hash、row count、freshness、errors、warnings、data_status、revenue_status、Change history、external changes、conflict_status、rerun window 和来源 URL。系统会生成 Script Sync Score、risk_level、freshness_level、recommended_action 和 blockers；状态可标记为 snapshot_ready、rerun_required、conflict_review、approved_for_import、imported_manual、blocked 或 closed，并写入 `/logs`。不要把“15 分钟同步”理解成实时最终收入；Google Ads conversions、buyer approved revenue 和 finalized/paid revenue 要分开看。同步原则见 [Google Ads Scripts 数据同步、快照与一致性手册](google_ads_scripts_data_sync_consistency.md)。

投放草稿导出前还要进入 `/taxonomy-governance` 创建命名维度评审，确认 campaign name、ad group name、label、UTM、ValueTrack、custom parameter、subid、landing_version、link_version、creative_version 和 payload_hash 都能回到同一套维度字典。系统会生成 Taxonomy Score、risk_level、recommended_action、缺失 token、缺失 UTM、缺失 label group 和 blockers；状态可标记为 dictionary_ready、mapping_fix、export_ready、qa_failed、blocked 或 closed，并写入 `/logs`。不要用 `测试1`、`过审版`、临时 subid 或手工改名来承接批量投放；命名和参数治理见 [Campaign 命名、Labels、UTM/SubID 与维度治理手册](campaign_taxonomy_naming_label_dimension_governance.md)。

### 2.7 导入指标

进入 `指标导入` 页面，上传或粘贴 CSV。

字段：

```csv
offer_id,campaign_draft_id,day,channel,country,device,impressions,clicks,cost,conversions,revenue
1,1,2026-06-08,Google Ads,US,desktop,1000,80,45.00,2,84.00
```

导入后系统计算：

- CPC。
- CTR。
- CVR。
- RPV。
- Profit。
- ROI。

如果 Google Ads clicks、server landing requests、GA4 sessions、offer clicks、postback 或收入对不上，先按 [Click -> Session -> Revenue 对账 SOP](click_session_revenue_reconciliation.md) 分层排查。差异可能来自 URL 展开、parallel tracking、tag、consent、ad blocker、数据刷新、postback 延迟或 finalized revenue 扣量；不要用补点击、模拟访问或伪造 event 修报表。

RSOC / N2S / Related Search 场景不要只看 gross funnel RPM。上线前先确认 AFS/Related Search 权限、content page 独立价值、RAC 上游创意文本、PIF 布局、query intent、search results page 相关性和扣量规则；扩量依据应是 finalized RPV。流程见 [RSOC / N2S、Search Feed Partner 与相关搜索套利治理手册](rsoc_n2s_search_feed_partner_governance.md)。

Native / Advertorial / Presell Page 流量要单独复盘 source、publisher、placement、creative、landing version、CTA click、approved/paid revenue 和 refund/scrub。标题、缩略图、软文页、披露和 Offer 下一步必须一致；不要用假新闻、伪评价、隐藏商业关系或桥页制造点击。方法见 [Native、Advertorial 与 Presell Page 套利手册](native_advertorial_presell_compliance.md)。

Google Ads 报表复盘要把 Search terms、Auction Insights、Change history、Report Editor、landing pages、RSA assets 和 bid strategy report 放在同一条诊断链里看。看到 ROI 下降时，先查 query、device、geo、network、landing page、改动历史和回传质量，再决定否定词、暂停、拆组、修页面或等回传窗口。方法见 [Google Ads 报表诊断、Search Terms 与 Change History 手册](google_ads_reporting_diagnostics.md)。

归因收入不等于增量利润。品牌词、再营销、老用户、PMax、Broad Match 和旺季流量很容易把本来会发生的转化记到广告上；扩量前进入 `/attribution` 记录 test type、control/treatment、holdout quality、attributed revenue、incremental revenue、iROAS、incremental profit、sample、confidence、Change history、approved/paid 证据和 cannibalization risk。系统会生成 score、risk_level、recommended_action 和 blockers；状态更新只写审计日志，不自动创建实验、不应用 winner、不改后台。方法见 [归因、增量性与流量蚕食治理手册](attribution_incrementality_cannibalization.md)。

Search Terms 复盘不要只做“花钱无转化就否定”。进入 `/query-mining` 可以把 query、keyword、match type、device、network、landing version、source file hash、clicks、sessions、conversions、approved/paid revenue、buyer reject、conversion lag、data status、revenue status 和 policy flags 放在同一条评审里。系统会生成 Query Mining Score、risk_level、recommended_action、negative_match_type、negative_level、click_session_rate、CPC、approved/paid RPV、approved/paid ROI 和 blockers，再决定 negative、promote exact/phrase、split ad group、page brief、hold 或 pause。状态只代表内部审批，不会自动搜索、点击、改后台、绕过隐私聚合或用代理伪装地区。完整方法见 [Search Terms、否定词与 Query Mining 治理手册](search_terms_negative_keyword_query_mining.md)。

自动出价前要单独看转化信号质量。不要只问“有没有 conversion action”，而要进入 `/conversion-signals` 记录 conversion goal/action、action stage、当前 primary/secondary、value mode、weekly submitted/approved/paid、click ID coverage、offline match rate、duplicate rate、conversion lag、segment 粒度、policy/consent、customer data、offline import diagnostics、transaction_id、bid strategy report、Change History 和 rollback plan。系统会生成 Signal Quality Score、recommended primary status、bid readiness、expected paid value、safe target CPA、recommended_action 和 blockers；状态可标记为 tracking_fix、dedupe_fix、value_review、lag_review、goal_review、secondary_only、primary_candidate、bid_ready 或 blocked。状态更新只写 `/logs`，不自动上传 offline conversion、不改 primary/secondary、不改出价、不操作 Google Ads 后台。Signal Quality Score、准入矩阵和事故响应见 [转化信号质量与出价学习治理手册](conversion_signal_quality_bidding_learning_governance.md)。

CRM 和 buyer feedback 不要直接一股脑上传给 Ads。先进入 `/crm-value-mapping` 把 buyer 字段映射成 submitted、accepted、qualified、approved、paid、returned 等标准阶段，再记录 conversion action role、primary recommendation、value mode、payout、approved/paid/return rate、weekly stage rows、unique lead、rejected/returned/duplicate、click ID match rate、import success/error、stage lag、return window、transaction_id、adjustment rule、import batch、diagnostics、consent、PII handling、rollback plan 和 source URLs。系统会生成 CRM Mapping Score、recommended_upload_policy、expected value、recommended_action 和 blockers；状态可标记为 stage_map_review、action_map_review、value_review、dedupe_fix、import_qa、adjustment_review、lag_review、secondary_only、primary_candidate、upload_candidate 或 blocked。状态更新只写 `/logs`，不自动上传 offline conversion、不改 primary/secondary、不改 value、不操作 Google Ads 后台；rejected/returned 不应继续作为正向转化。映射方法见 [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md)。

决策前还要判断数据成熟度。当天 cost/click 可以用于发现断流、URL 错误和花费异常，但不能直接证明 ROI；扩量要等 conversion lag、buyer approval、finalized/paid revenue 或至少主要 cohort maturity 进入可判断窗口。进入 `/decision-windows` 可录入 data_status、revenue_status、lag、样本点击、approved/paid revenue、来源质量和事故状态，系统会生成 Decision Window Score、maturity、recommended_action 和 blockers，并允许把状态更新为 waiting、ramp_ready、blocked 或 closed；状态更新只写审计日志，不自动改预算。stop-loss、wait-loss、budget ramp 和关账窗口见 [决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md)。

Search 自动化不要只看“新增转化”。开启 AI Max、Broad Match、Dynamic Search Ads、Final URL expansion 或 automatically created assets 前，要先确认 primary conversion、conversion value、URL inclusions/exclusions、page feed、brand controls、negative keywords、search terms、landing pages、asset claim 和 paid revenue 都能复盘。方法见 [Search 自动化流量：AI Max、Broad Match 与 DSA 套利风险手册](search_automation_ai_max_broad_match.md)。

PMax / Demand Gen 不适合冷启动未知 Offer。测试前先确认 primary conversion 和 conversion value 接近可收款价值，再检查 Final URL expansion、URL exclusions / page feed、Search themes、Audience signals、Brand exclusions、asset group、channel / placement / asset / landing page reports 和 paid revenue；不要只看 Google Ads conversions 或 CTR。方法见 [Performance Max / Demand Gen 自动化流量与套利风险手册](performance_max_demand_gen_automation.md)。

Geo、语言和设备不要混成一个平均 ROI。扩国家、切语言、调 device bid adjustment 或做 dayparting 前，要确认 location options、页面本地化、Offer 允许地区、bad geo、账号时区、收入时区、成本币种、收入币种和汇率日期。方法见 [Geo、语言、本地化、时区与币种分层手册](geo_language_localization_currency.md)。

CPA/CPL/Lead 场景不要只把 `conversions` 当成最终收入。建议把 buyer feedback 或联盟结算按同一 CSV 口径拆成 approved/rejected/paid revenue 后再导入，或者在 `/risk-audits` 记录拒付、scrub、duplicate、bad geo、invalid phone 等原因。相关口径见 [Lead 质量、Postback 对账与拒付管理手册](lead_quality_postback_reconciliation.md)。

签 Lead Buyer 或 direct advertiser 合同前，先把 accepted、qualified、billable、approved、paid、return window、allowed return reason、duplicate window、cap、invoice package 和 payment term 写清。`accepted` 不能直接当 paid revenue；扩量要等 mature cohort 的 approved/paid 或至少 return window 后的净值。合同口径见 [Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md)。

谈 lead payout 时不要只看 headline CPL。Raw CPL、qualified CPL、pay-per-call、appointment、CPA、revshare 会把质量、联系、退款、回款和样本风险分给不同一方；测算要用 effective payout、scrub buffer、return window、payment term 和 cap。谈价前先进入 `/lead-pricing` 保存 headline/unit/proposed payout、accepted/qualified/approved/paid、return/scrub/chargeback、Buyer cap、quality evidence、source transparency、invoice terms 和 source URLs。系统会生成 paid EPC、safe CPC、reserve、risk_level、recommended_action 和 blockers；状态更新只写审计日志，不自动谈价、不改 buyer routing、不生成 lead 或改广告后台。方法见 [Lead Pricing、Payout Negotiation 与结算安全垫治理手册](lead_pricing_payout_negotiation_governance.md)。

Appointment lead 不要把 booked 当 paid。预约流程要拆 submitted、booked、confirmed、showed、completed、approved、paid、cancel 和 no-show，并把 calendar capacity、slot timezone、reminder consent、duplicate booking、show rate 和 buyer payout event 写进状态机。预约型 Offer 上线前先进入 `/appointment-leads` 保存 payout event、漏斗率、no-show/cancel、slot capacity、reminder consent、buyer terms、offline mapping 和 source URLs；系统会生成 expected value per booking/click、safe CPC、safe appointment spend、risk_level、recommended_action 和 blockers，状态更新只写审计日志，不自动创建预约、外呼、群发短信、伪造到场或改广告后台。详细方法见 [Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md)。

CPL 垂类不要共用同一套表单、出价和止损线。保险、贷款/债务、法律、本地服务、教育、医疗和 B2B 的资格字段、buyer acceptance、feedback lag、reject reason 和合规 claim 都不同；新 Offer 进入测试前进入 `/cpl-verticals` 写 vertical profile、qualification map、accepted/paid definition、buyer terms、consent/disclosure、PII 最小化、forbidden claims 和 source URLs。系统会生成 effective payout、EV/click、safe CPC、Vertical Fit Score、risk_level、recommended_action 和 blockers；状态更新只写审计日志，不自动生成 lead、提交表单、改 routing 或改广告后台。垂类模板见 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)。

保险 lead 要单独建 profile。Medicare、ACA / Marketplace、Final Expense、Auto 和 Home insurance 的资格字段、licensed agent/broker、carrier/plan claim、开放注册、buyer acceptance、reject reason、consent proof 和 offline value 都不同；不要用 submitted lead、qualified duration 或 booked appointment 直接当 paid revenue。上线前按 [Insurance、Medicare / ACA 与 Final Expense Lead 治理手册](insurance_medicare_aca_final_expense_lead_governance.md) 检查官方关系、Google Ads/CMS/Marketplace/Medicare 来源、claim、字段最小化和 buyer terms。

贷款/债务/信用 lead 也要单独建 profile。Personal loan、mortgage/refi、HELOC、credit card、debt relief、credit repair 和 student loan relief 的资格字段、financial disclosure、licensed lender/broker/lead generator、HEC/Personalized Ads、CFPB/FTC/FCRA/ECOA/TILA 边界、buyer acceptance 和 paid definition 都不同；不要把 submitted、buyer accepted、prequalified 或 call duration 直接当 funded/paid revenue。上线前按 [Loan、Mortgage、Credit 与 Debt Lead 治理手册](loan_mortgage_credit_debt_lead_governance.md) 检查 claim、rate/APR/fee/term、government relationship、sorting/compensation disclosure、字段最小化和 offline value mapping。

法律 lead 要把案件资格和律师边界分开治理。Personal injury、mass tort、immigration、criminal、family、bankruptcy 等 practice area 的 jurisdiction、incident date、injury/damages、representation status、attorney review、retainer signed、case accepted 和 paid definition 都不同；不要把 submitted、intake qualified、consultation booked 或 call duration 直接当 paid case。上线前按 [Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理手册](legal_case_intake_mass_tort_lead_governance.md) 检查 attorney/law firm/intake center/lead generator 角色、lawyer advertising、solicitation、confidentiality、official relationship、claim 和 offline value mapping。

本地服务 lead 要把服务区、工种和派单能力放在第一位。HVAC、plumbing、roofing、garage door、moving、cleaning、remodeling 和 solar 的 service area、contractor license/insurance、business hours、technician capacity、emergency intent、booked/showed/quoted/sold/completed 和 credit/dispute 口径都不同；不要把 call click、submitted、booked 或 LSA charged lead 直接当 paid job。上线前按 [Home Services、Solar 与 Local Services Lead 治理手册](home_services_solar_local_services_lead_governance.md) 检查 service area、contractor identity、虚假本地/虚假 badge、solar savings、free estimate、review claim、capacity 和 offline value mapping。

教育 lead 要把项目承诺和招生回传放在第一位。Degree、career school、trade school、bootcamp、CDL、nursing/allied health、cosmetology、continuing education 和 test prep 的 program interest、state authorization、accreditation、licensure、transferability、admissions eligibility、financial aid、student loan、job placement/salary claim 和 enrollment funnel 都不同；不要把 submitted inquiry、application started 或 advisor call 直接当 paid enrollment。上线前按 [Education、Career Training 与 Student Lead 治理手册](education_career_training_student_lead_governance.md) 检查学校主体、授权/认证来源、职业结果 claim、贷款/资助 claim、字段最小化、buyer terms 和 offline value mapping。

医疗 lead 要把隐私、服务匹配和到诊价值拆开。Dental、vision、mental health、urgent care、specialist、telehealth、clinic lead 和 medical device inquiry 的 service need、provider license、insurance/payment fit、PHI/health data、tracking、health claim、appointment booked/confirmed/showed/treated/paid 口径都不同；不要把 submitted、call duration、appointment requested 或 booked 直接当 paid patient。上线前按 [Healthcare、Medical Appointment 与 Clinic Lead 治理手册](healthcare_medical_appointment_lead_governance.md) 检查 Google healthcare policy、PHI/Tracking、health claim proof、字段最小化、consent、buyer terms 和 offline value mapping。

B2B SaaS / 专业服务 lead 要把 ICP 和销售阶段放在第一位。CRM、security、HR、finance、marketing software、developer tools、agency、consulting 和 MSP 的 company size、industry、role/persona、use case、budget/timeline、buyer committee、MQL/SAL/SQL/opportunity/won 和 PQL 口径都不同；不要把 download、webinar signup、free trial、form submit 或 demo request 直接当 paid pipeline。上线前按 [B2B SaaS、Professional Services 与 Demo Lead 治理手册](b2b_saas_professional_services_lead_governance.md) 检查 trademark/competitor query、software policy、customer logo/review/security claim、pricing/trial、consent、reject reason 和 offline value mapping。

Crypto / 投资 / 交易 lead 默认按极高风险处理。Exchange、wallet、coin trust、forex/CFD、investment adviser、broker、signals、AI trading、newsletter 和 crypto education 的 Google Ads certification、地区/监管注册、risk disclosure、fraud red flag、KYC、funded account、first trade、paid/clawback 口径都不同；不要把 lead submit、app install、signup 或 KYC started 直接当 paid investor。上线前按 [Crypto、Investment 与 Trading Lead 治理手册](crypto_investment_trading_lead_governance.md) 检查 crypto / financial / complex speculative policy、license/registration、收益和风险 claim、fraud red flag、敏感数据和 offline value mapping。

招聘 / Staffing lead 要先证明岗位真实和定向合规。Direct hire、staffing、job board、gig、remote/work-from-home、government/postal、healthcare/CDL recruiting 和 business opportunity 的 job order、employer authorization、HEC / employment targeting、pay/remote claim、worker classification、resume/background data、interview/hire/start/paid 口径都不同；不要把 lead submit、resume upload、call connected 或 interview scheduled 直接当 paid placement。上线前按 [Employment、Recruiting 与 Staffing Lead 治理手册](employment_recruiting_staffing_lead_governance.md) 检查 ghost job、job scam、work-from-home、EEOC wording、candidate privacy、buyer terms 和 offline value mapping。

Gambling / 抽奖 / Sports Betting lead 必须先过地区许可和平台认证。Casino、sportsbook、social casino、sweepstakes casino、fantasy sports、lottery、affiliate bonus 和 review site 的 product type、Google certification、operator license、age gate、geolocation、self-exclusion、responsible gambling、bonus terms、sweepstakes rules、KYC/deposit/wager/NGR/paid 口径都不同；不要把 app install、registration 或 bonus claimed 直接当 paid player。上线前按 [Gambling、Sweepstakes 与 Sports Betting Lead 治理手册](gambling_sweepstakes_sports_betting_lead_governance.md) 检查 license/geo、age、responsible gambling、bonus/odds claim、affiliate disclosure、paid/clawback 和 offline value mapping。

成瘾治疗 / Rehab lead 要按最高敏医疗 lead 处理。Detox、residential、IOP/PHP、sober living、OTP、MAT/MOUD、telehealth SUD 和 crisis helpline 的 Google/LegitScript certification、provider/referral role、facility license、Part 2/HIPAA tracking、crisis routing、patient brokering、insurance verification、admitted/started/paid 口径都不同；不要把 call duration、form submit、admissions consult 或 insurance verification 直接当 paid treatment。上线前按 [Addiction Treatment、Rehab 与 Behavioral Health Lead 治理手册](addiction_treatment_rehab_behavioral_health_lead_governance.md) 检查 certification、provider identity、privacy、crisis SOP、claim proof、buyer terms 和 offline value mapping。

政府服务 / Immigration / Public Benefits lead 要先证明官方关系和费用透明。Passport、visa、USCIS、DMV、vital records、Social Security、tax / IRS help、public benefits 和 grants 的 Google government documents and services policy、certification、authorized provider、not a government website disclosure、notario / accredited representative、official fee、service fee、identity data、application filed、issued document 和 paid/refund 口径都不同；不要把 lead submit、eligibility quiz、document checklist 或 call connected 直接当政府结果。上线前按 [Government Services、Immigration 与 Public Benefits Lead 治理手册](government_services_immigration_public_benefits_lead_governance.md) 检查 official relationship、fee/refund、authorization、identity data minimization、claim proof、buyer terms 和 offline value mapping。

Lead Form 不要只优化 submitted CVR。每次改字段、顺序、CTA、disclosure 或 consent，都要生成 form version，并同时看 validation pass、buyer accepted、contacted、qualified、paid、complaint 和 opt-out；字段必须有 purpose 和 reject reason 映射。表单漏斗方法见 [Lead Form 漏斗、资格问题与移动端 UX 治理手册](lead_form_funnel_qualification_ux.md)。

Consent proof 不要只保存 `consent=true`。表单、Ping/Post 和 buyer handoff 要保存 consent version、buyer disclosure version、certificate/token、page snapshot/hash、submit time、suppression 状态和证据来源；TrustedForm/Jornaya 类证据只能作为证据链的一部分，不能替代 DNC、opt-out、撤回同意、合同和法律判断。证据链方法见 [Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)。

Ping/Post 场景要把 submitted、pinged、posted、accepted、no buyer、cap reached、duplicate、approved 和 paid 拆开。上线前进入 `/ping-post-routing` 记录 routing mode、lead type、consent scope、buyer disclosure、ping field scope、PII level、suppression/DNC、cap snapshot、fallback、buyer feedback、source policy、buyer count、pinged/accepted/posted buyers、cap remaining、lead age、ping latency、expected bid、fallback payout、accept/qualification/paid/no-buyer/reject/duplicate/complaint rate、fields sent schema、routing rule、reject reason map、fallback policy、buyer feedback plan、consent evidence 和 source URLs。系统会生成 Routing Quality Score、expected payable value、safe CPL、recommended_action 和 blockers；状态可标记为 consent_review、field_minimization、cap_refresh、routing_review、fallback_review、buyer_feedback_review、suppression_review、manual_test、routing_ready 或 blocked。状态更新只写 `/logs`，不自动 post lead、不自动外呼/短信、不绕过 consent/DNC、不操作 buyer 或 Google Ads 后台。详细机制见 [Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)。

Fresh lead、same-day lead、aged lead 和 recycled lead 不能共用同一套 payout、routing 和 conversion signal。每条 lead 必须保存 original_submit_time、lead_age_bucket、first_response_time、consent version、suppression snapshot 和 buyer age terms；aged revenue 不要归因到当前广告点击或新 source 的 RPV。Lead 时效治理见 [Lead Freshness、Aged Lead 与 Recontact Window 治理手册](lead_freshness_aged_recontact_governance.md)。

Lead 验证不要做成“补全缺失字段”。上线前要把 schema、consent、format、duplicate、suppression/DNC/opt-out、geo/offer eligibility、source policy、buyer cap 和 PII 最小化拆成独立状态；invalid、duplicate、suppressed、no consent 和 bad geo 不应进入正向 conversion。字段、保留期、删除、访问控制和 reject reason 修复见 [Lead 验证、Suppression、去重与 PII 治理手册](lead_validation_suppression_pii_governance.md)。

Speed-to-Lead 要和预算节奏绑定。Call-heavy campaign 上线前先确认 buyer/call center hours、first attempt SLA、attempt cadence、call disposition、missed call、qualified call duration、DNC/opt-out sync 和 capacity；不要把 call click、短通话、missed call 或 no answer 当成 paid revenue。联系策略见 [Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)。

Buyer 接量能力要和广告时段、预算、call asset schedule 和 routing 绑定。Cap unknown、cap stale、buyer closed、holiday、no buyer、missed call 或 after-hours lead 上升时，先降预算/限时段/暂停 source，不要让 Google Ads 继续按 submitted 或 call click 学习。上线前进入 `/buyer-capacity` 保存 cap limit/used、elapsed day、next-hour lead、hourly contact capacity、expected paid value、accepted/qualified/paid、no buyer、missed contact、after-hours、cap freshness、hours/ad schedule/timezone/holiday、fallback policy 和 source URLs；系统会生成 Capacity Quality Score、projected usage、safe leads、safe media spend、risk_level、recommended_action 和 blockers，状态更新只写审计日志，不自动改预算、时段、routing、外呼或 buyer 后台。详细方法见 [Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md)。

电话和表单 Lead 要单独审 consent、buyer disclosure、DNC/撤回同意、call duration、missed call、recording disclosure 和 CRM 状态；不要把所有 submitted lead 或短通话都设为 primary conversion。字段、状态机和 QA 见 [Lead Form、电话线索、Call Tracking 与 TCPA 风险手册](lead_form_call_tracking_tcpa_compliance.md)。

Call-heavy campaign 要先确认 Google forwarding number、第三方 DNI、号码池、call asset、business number 和 CRM call log 的事实源。不要把 call click、短通话、missed call、wrong number、test call 或 existing customer 当成 paid lead；电话归因要保存 provider_call_id、tracking_number、call_start_at、duration、disposition、CRM ID 和 offline conversion mapping。详细方法见 [Call Tracking Number Pool、DNI 与电话归因治理手册](call_tracking_dni_number_pool_attribution_governance.md)。

Pay-per-call 不要只看 qualified duration。Call buyer routing 要保存 buyer/target、routing plan、IVR/call flow version、buyer hours/cap、duplicate caller rule、duration payout、buyer disposition、paid revenue 和 scrub reason；duration 达标但 wrong service、existing customer、duplicate 或 complaint 的电话不能当净收入。机制见 [Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](pay_per_call_buyer_routing_duration_payout_governance.md)。

AdSense/AdX/GAM 场景不要把当日 estimated revenue 直接当作可扩量收入。建议区分 estimated/finalized/paid revenue、deduction_rate、finalization_ratio，并按 [发布商收入对账、Finalized Revenue 与扣量复盘手册](revenue_reconciliation_adstack.md) 做月度关账。

订阅、试用和连续付费 Offer 不要只看 signup、first payment 或 projected LTV。建议按 cohort 导入 trial_to_paid、renewal、refund、chargeback、clawback 和 net LTV，并把高退款/高争议来源写入 `/risk-audits`。披露、取消、退款和 LTV 口径见 [订阅、试用、退款、Chargeback 与 LTV 治理手册](subscription_refund_ltv_chargeback_governance.md)。

AdSense 新站、站点审核失败、Policy Center issue 或 ad serving limit 要先按站点健康处理，不要急着换域名、换账号或继续扩低质来源。记录 site review status、Policy Center issue、affected URLs、ad serving status、traffic source 和修复证据；流程见 [AdSense 站点审核、Policy Center 与广告投放限制手册](adsense_site_approval_policy_center.md)。

发布商广告质量也要进入复盘。遇到竞品广告、诈骗/仿冒广告、敏感分类、用户投诉或低质广告时，记录 advertiser domain、creative、页面 URL、国家、设备、处理动作和收入影响；不要点击广告制造证据。流程见 [发布商广告质量、阻止控制与品牌安全手册](publisher_ad_quality_blocking_controls.md)。

发布商广告位实验要把 page_template、ad_layout_version、viewability、ad CTR、CLS、estimated/finalized revenue 和扣量放在一起看。不要用自动刷新、误点位置或堆广告制造短期 RPM；广告位、Ad refresh 和页面体验的复盘口径见 [广告位、刷新、可见率与页面体验手册](ad_placement_refresh_viewability.md)。

域名和站点资产不要当成一次性壳。换 root domain、subdomain、tracking domain、Final URL 或站点变现账号前，要检查历史主题、过期域名/站点声誉滥用风险、AdSense site status、ads.txt、seller ID、Policy Center、Final URL 和用户实际看到的页面。换域名不能用来绕过拒登、封禁、ad serving limit 或低质内容问题；方法见 [域名、站点资产与站群治理手册](domain_site_asset_governance.md)。

如果接入 AdX/GAM、Open Bidding、Header Bidding、MCM 或第三方需求源，先检查 ads.txt、sellers.json、schain、DIRECT/RESELLER 和 seller ID 是否能解释。供应链不透明会影响 fill、CPM、买方信任和 finalized revenue；具体 QA 见 [程序化供应链透明度：ads.txt / sellers.json / schain 手册](programmatic_supply_chain_transparency.md)。

GAM/AdX yield 实验不要只看 eCPM。调 floor、unified pricing rules、Open Bidding 或 line item priority 时，要同时看 fill、coverage、viewability、session RPM、estimated/finalized revenue 和扣量，并保留规则版本和回滚点。方法见 [GAM / AdX Yield、Floor Price 与 Pricing Rules 手册](gam_adx_yield_floor_pricing.md)。

Header Bidding / Prebid.js 实验不要只看 bidder CPM。接入或暂停 bidder、调整 auction timeout、price granularity、floor、User ID 或 consent 配置时，要同时看 bid rate、win rate、render rate、GAM fill、viewability、CLS/LCP、session RPM、estimated/finalized revenue 和供应链 QA。方法见 [Header Bidding / Prebid.js 与广告栈延迟手册](header_bidding_prebid_ad_stack.md)。

季节性 campaign 的预算要分 pre-season learning、peak ramp 和 post-peak exit。高峰前用小预算验证 query、页面、CPC 和初始收入；高峰期每次只小幅加预算并等待回传；高峰后按 exit rule 收紧关键词和预算，保留 paid/finalized 数据给下一季复盘。

周报和月报要加组合视角：单一来源、单一 Offer、单一账号或单一结算方吃掉太多预算时，即使总 ROI 为正，也应冻结扩量、等待 paid/finalized 回填，并把弱项转入 watch 或 quarantine。

进入 `/portfolio-allocation` 可以把组合层面的预算证据固化成评审记录。建议每周或每次大额分配前记录 monthly_media_budget、proposed_allocation、spend_to_date、revenue status mix、single_offer/source/account/partner exposure、cash_reserve_days、source_quality、policy_risk、incident_state 和 source_urls。系统只给出 Portfolio 分配建议和阻塞项，不会自动登录后台、改 Google Ads budget、切账号、换链接或隐藏来源。

进入 `/budget-pacing` 可以把预算变更前的证据固化成评审记录。建议每次扩量、降预算或暂停前都记录 current_daily_budget、proposed_daily_budget、test_budget、hard_stop、spend_to_date、safe_cpc、actual_cpc、sample_clicks、data_status、revenue_status、source_quality、incident_state、cash_buffer_days 和 source_urls。系统会生成 Budget Pacing Score、risk_level、recommended_action 和 blockers；状态可以标记为 waiting、approved_for_manual_change、reduced、blocked 或 closed。这个状态只代表内部审批进度，不会自动改 campaign daily budget、出价、时段或后台 Recommendations。

### 2.8 查看优化建议

进入 `优化建议` 页面。

系统当前内置规则：

- 点击足够但无收入：暂停或隔离来源。
- ROI 低于止损阈值：降预算或暂停。
- ROI 高且样本足够：小幅扩量并补素材。
- CTR 高但 RPV 低：检查素材承诺是否过宽或标题党。

这些规则是业务提醒，不是自动执行。

每条优化建议可以在页面上标记为 `待处理`、`转人工处理`、`已解决` 或 `已关闭`。状态更新只写入内部审计日志，用来表示团队是否已经看过、转给负责人、完成修复或判断不处理；它不会自动改预算、启停 campaign、接受 Google Ads Recommendations、换链接、补点击或触发任何后台操作。

把 `/optimization` 当成异常监控和止损队列的 V1：`pause_check`、`stop_loss`、`creative_mismatch`、`invalid_traffic_review` 等动作要先补证据，再决定暂停、降预算、隔离来源、修追踪或回写素材。不要用补点击、模拟转化、重复提交后台或换账号来“修”异常。告警分级、证据包、事故分诊和 postmortem 方法见 [异常监控、告警、止损队列与事故分诊手册](anomaly_monitoring_alerting_stoploss_incident_triage.md)。

来源评分是止损动作的原因层：同一个 ROI 告警，要继续拆 source、publisher、placement、subid、device、geo、landing_version 和 offer status。不能解释或不能按维度停量的来源，不进入扩量；出现隐藏来源、补量、代理/指纹、Worker 转发或 cloaking 话术时，直接进入风险审计和 blocklist。

如果异常来源涉及供应商付款或退款，先暂停相关 line item，锁定日期和时区，保存 vendor report、server log、postback、invoice、creative、landing screenshot 和 buyer feedback，再开 dispute case。不要在没有 evidence pack 的情况下口头争议，也不要用同一坏来源的 makegood 补投继续扩大损失。

Google Ads 后台的 Recommendations、Optimization Score 和 Auto-apply 也按同一原则处理：建议只是待验证假设，不代表 paid revenue 或 finalized revenue 会改善。出价、预算、broad match、Search Partners、动态资产、conversion goal、PMax/AI Max 等建议必须先进入评审或实验，不要自动接受。详细方法见 [Google Ads Recommendations、Experiments 与 Auto-apply 优化治理手册](google_ads_recommendations_experiments_auto_apply_governance.md)。

### 2.9 做高风险审计

进入 `风险审计` 页面，针对 Offer 或投放草稿逐项检查：

- Ads Cookie 登录和后台操作。
- 自动绕过登录、2FA、安全挑战。
- 补点击、刷展示、模拟自然流量。
- 代理、指纹、Worker 转发规避关联检测。
- cloaking 或审核页/用户页不一致。
- 为规避封禁创建或切换账号。
- 受众、再营销、Customer Match、PMax audience signals、Personalized Ads 和 consent 边界。

每条记录要写明发现、处理方案和来源 URL。高风险项默认不放行，需要暂停、修复或拒绝。

审计记录保存后，可以在列表里把处理进度标记为 `待处理/open`、`已复核/reviewed`、`已缓解/mitigated` 或 `已拒绝/rejected`。这些状态只代表内部审计进度和证据处理结果，并会写入 `/logs`；它不会自动放行 Cookie 操作、登录挑战绕过、补点击、代理/指纹/Worker 规避、cloaking 或封禁后换号。

受众类审计重点看：

- 数据是否第一方直接收集，是否有隐私政策、同意和退订/删除路径。
- Offer 是否涉及健康、金融困境、住房、就业、信贷、成人、儿童或其他 Personalized Ads 敏感类别。
- Customer Match 是否只是上传购买名单、联盟名单或来源不清的 lead。
- PMax audience signals 和 optimized targeting 是否被误认为硬性定向。

### 2.10 记录研究来源

进入 `来源库` 页面，记录每个行业知识判断或高风险能力判断的信息来源。

建议字段：

- 主题：例如 `补点击、刷展示、模拟自然流量`、`Lead 质量、Postback 对账与拒付管理`。
- 高风险能力：选择对应能力，普通行业知识可不绑定。
- 受众、再营销、Customer Match 等合规主题也可以绑定 `audience_remarketing_customer_match_policy`。
- 落地页素材抽取和创意事实核查可使用 `落地页素材抽取、Offer Intelligence 与创意 Brief`。
- 标题、URL、发布方。
- 来源类型：policy、official_api、technical_reference、product_page 等。
- 可信级别：primary、public_claim、industry_reference、secondary。
- 复核状态：candidate、accepted、needs_update、archived。
- 证据摘要：这条来源支撑了哪个定义、边界或判断。

来源保存后，可以在列表中把状态标记为 `待复核/candidate`、`已采纳/accepted`、`需更新/needs_update` 或 `已归档/archived`。这个状态用于管理知识库维护节奏：待复核表示还不能作为关键判断的唯一依据，已采纳表示可以被文档和审计引用，需更新表示 URL 或政策内容可能变化，已归档表示仅保留历史记录。状态更新会写入 `/logs`。

`来源库` 用于资料沉淀和审计，不用于自动执行广告后台动作。`已采纳` 不等于自动放行投放、链接、账号、Cookie 操作或高风险能力；它只说明该来源已经被团队复核为可引用证据。

### 2.11 使用任务中心

进入 `任务中心` 页面，可以创建以下安全任务：

- 落地页审计复核。
- 创意生成。
- CSV 导出检查。
- Scripts JSON 导出检查。
- 链接计划检查。
- 指标复核。

第一版任务由人工点击“执行一次”，系统记录成功/失败、执行次数、结果和审计日志。它不自动登录 Google Ads，不执行 Cookie 操作，不做补点击或自动浏览。

创建任务前先判断任务等级：页面读取、导出检查、Scripts payload 预览属于低风险；改预算、改 Final URL、启停 campaign、创建广告属于高风险，必须有审批、payload 版本、回滚计划和外部 Change history / Scripts log 证据。系统会检查任务类型、任务名称和备注；包含登录接管、Cookie、Session Token、2FA、安全挑战、补点击、模拟流量、代理池、指纹、Worker 转发、cloaking 或换号语义的任务会被拒绝创建。认证失败、2FA、安全挑战、click/session/revenue 缺口不能通过后台任务重试或补量处理，应进入账号安全、追踪 QA、来源隔离或事故复盘。完整方法见 [任务编排、安全审批、执行日志与事故复盘手册](task_orchestration_approval_audit_runbook.md)。

### 2.12 创建链接计划

进入 `链接计划` 页面。

合规用途：

- 断链修复。
- UTM 更新。
- 已审核、同主题 URL 的 A/B 测试。
- 同主题备用链接维护。

不允许把链接计划用于：

- 审核页和用户页不一致。
- cloaking。
- 绕过广告平台审核。
- 把广告承诺切换到不相关页面。

系统默认 `require_manual_review=True`，所有链接计划都需要人工确认。页面可把计划标记为 `草稿`、`评审中`、`已批准`、`已轮换`、`暂停` 或 `拒绝`。只有 `已批准` 或已经轮换过的计划才能继续执行轮换；草稿、评审中、暂停和拒绝状态会被系统拦截。

批准后可以点击“人工确认轮换”，系统会把当前 URL 换成候选 URL，并把旧 URL 放回候选池，整个动作写入审计日志。状态和轮换都只是内部链接计划记录，不会自动登录 Google Ads 后台或隐藏目的地。

换链接或导出投放草稿前，建议对照 [追踪模板、URL 参数与跳转链 QA 手册](tracking_template_redirect_chain_qa.md) 检查 Final URL、tracking template、Final URL suffix、ValueTrack、`gclid`/`click_id`、postback 和 redirect chain。出现 click/session/revenue 对不上时，先查参数和跳转链，不用补点击或模拟访问修报表。

### 2.13 查看审计日志

进入 `审计日志` 页面，查看：

- Offer 创建。
- 落地页采集。
- 创意生成。
- 草稿导出。
- 指标导入。
- 链接计划创建。

审计日志用于复盘和风控，不建议删除。

## 3. 日常运营节奏

每日：

- 导入昨日或当日指标。
- 看 ROI、CPC、RPV。
- 处理高严重级别优化建议。
- 检查无收入消耗、异常 CTR、异常流量来源。

每周：

- 复盘垂类和国家组合。
- 更新创意池。
- 检查页面质量和政策备注。
- 汇总亏损来源和扩量候选。

每月：

- 做平台收入、联盟收入和买量成本对账。
- 更新合规红线。
- 清理不再测试的 Offer。
- 复盘扣量、拒付、审核和账户限制案例。

## 4. 合规使用边界

本系统不提供也不建议：

- Google Ads Cookie 操作后台。
- 自动绕过登录、2FA、安全挑战或审核。
- 补点击、刷展示、模拟自然流量。
- 代理/IP/指纹/Worker 转发用于规避关联检测。
- cloaking 和审核页/用户页不一致。
- 为规避封禁创建或切换账号。

建议使用：

- Google Ads Editor CSV。
- Google Ads Scripts。
- 官方 API。
- 人工审核和执行。
- 可追溯的导入导出流程。
