# 文档入口和验收导航

更新时间：2026-06-09

本文是 Ads Arbitrage Workbench 的验收导航页。它不是新的业务规则，而是把现有行业知识、ADXKit 拆解、高风险专题、系统设计、使用文档、开发文档和验证命令串成一条可复现路径。

## 1. 先看什么

| 验收问题 | 文档入口 | 系统入口 |
| --- | --- | --- |
| Ads 套利是什么、有哪些模式、为什么需要止损和风控 | [Ads 套利行业知识库](ads_arbitrage_industry.md)、[Ads 套利业务模式拆解手册](ads_arbitrage_business_models.md)、[Ads 套利运营手册](ads_arbitrage_operations.md)、[Ads 套利来源证据矩阵](ads_arbitrage_source_evidence_matrix.md) | `/knowledge/industry`、`/knowledge/business_models`、`/knowledge/operations`、`/knowledge/evidence_matrix` |
| ADXKit 公开能力如何拆解，哪些已经复刻 | [ADXKit 功能与架构拆解](adxkit_breakdown.md)、[验收清单](acceptance_checklist.md)、[原始需求追溯矩阵](requirement_traceability_matrix.md) | `/knowledge/adxkit`、`/knowledge/acceptance`、`/knowledge/traceability` |
| 高风险功能是不是跳过了 | [高风险能力专题索引](high_risk/README.md)、[高风险能力逐点调研与安全复刻蓝图](high_risk_capability_safe_reproduction_blueprint.md)、[高风险能力逐点完成审计](high_risk_completion_audit.md)、[高风险能力研究与合规替代方案](high_risk_capability_research.md) | `/knowledge/risk_index`、`/knowledge/risk_blueprint`、`/knowledge/risk_completion`、`/knowledge/redlines` |
| 来源 URL 是否可追踪 | [Ads 套利研究来源库](source_library.md)、[高风险能力风险矩阵与来源索引](risk_matrix_and_sources.md) | `/sources`、`/knowledge/source_library`、`/knowledge/risk_matrix` |
| 系统如何启动和使用 | [使用文档](usage.md)、[系统设计文档](system_design.md)、[开发文档](development.md) | `/docs`、`/knowledge/usage`、`/knowledge/design`、`/knowledge/development` |

## 2. 端到端验收路径

1. 启动系统：按 [使用文档](usage.md) 复制 `.env.example`，选择 SQLite 或 MySQL，执行 `flask --app app db-init` 和 `flask --app app seed`。
2. 核对来源：进入 `/knowledge/evidence_matrix`，确认套利模型、平台红线、Cookie/认证、无效流量、cloaking、封禁恢复和官方自动化替代方案都有来源 URL。
3. 配置账号：进入 `/accounts`，确认只记录 Google Ads Customer ID、同步方式、状态备注和申诉复盘，不保存 Cookie、Session Token、浏览器 Profile、代理池或指纹配置。
4. 录入 Offer：进入 `/offers`，填写垂类、国家、Payout、目标 URL、Tracking URL 和政策备注。
5. 测算机会：进入 `/calculators`，查看 RPV/EPC、break-even CPC、safe CPC、safety margin、test budget、hard stop 和 opportunity score。
6. 做 CPL 垂类评审：进入 `/cpl-verticals`，记录 vertical、qualification map、buyer terms、accepted/paid 口径、safe CPC、Vertical Fit Score 和 blockers。
7. 做 Lead 定价评审：进入 `/lead-pricing`，记录 headline/unit/proposed payout、accepted/qualified/approved/paid、return/scrub/chargeback、Buyer cap、payment term、safe CPC、reserve、谈价证据和 blockers；预约型 Offer 进入 `/appointment-leads`，记录 payout event、request/book/confirm/show/paid 漏斗、calendar capacity、reminder consent、buyer terms、safe CPC、safe appointment spend 和 blockers；接量约束进入 `/buyer-capacity`，记录 cap、hours、timezone、ad schedule、holiday、no buyer、missed contact、safe leads 和 safe media spend；Ping/Post 路由进入 `/ping-post-routing`，记录 consent/disclosure、ping field schema、PII、suppression/DNC、cap、fallback、buyer feedback、expected payable value、safe CPL 和 blockers；自动出价前进入 `/conversion-signals`，记录 primary/secondary、value、match、dedupe、lag、consent、diagnostics、bid readiness 和 blockers；CRM 回传前进入 `/crm-value-mapping`，记录 stage mapping、buyer feedback、transaction_id、import QA、adjustment、expected value 和 blockers。
8. 采集页面和生成创意：进入 Offer 详情页，执行落地页采集、素材证据抽取、创意生成和 Claim 审核。
9. 创建投放草稿：进入 `/campaigns`，导出 Google Ads Editor CSV 或 Google Ads Scripts JSON payload。
10. 做批量变更门禁：进入 `/bulk-upload`，记录 batch/hash、target customer、preview、Editor check、人工审批、Change History、回滚计划和阻塞项。
11. 做 Scripts 同步治理：进入 `/scripts-sync`，记录 report/search 快照、query hash、freshness、data_status、revenue_status、Change history、冲突和重拉窗口。
12. 做命名维度治理：进入 `/taxonomy-governance`，记录 campaign/ad group name、labels、UTM、ValueTrack、SubID、版本、payload hash 和 report join gap。
13. 做归因增量评审：进入 `/attribution`，记录 test type、control/treatment、holdout、iROAS、incremental profit、蚕食风险、blockers 和状态。
14. 处理广告审核：进入 `/ad-reviews`，记录 Policy Manager issue、policy topic、受影响对象、证据 URL、修复摘要和申诉状态。
15. 导入指标：进入 `/metrics/import`，导入真实成本、点击、转化和收入数据。
16. 处理优化建议：进入 `/optimization`，按 stop-loss、creative mismatch、invalid traffic review 等建议做人工决策。
17. 做搜索词治理：进入 `/query-mining`，记录 query、keyword、match type、approved/paid revenue、buyer reject、policy risk、否定词建议和阻塞项。
18. 判断决策窗口：进入 `/decision-windows`，记录 data freshness、conversion lag、approval lag、settlement lag、approved/paid revenue 和阻塞项，再决定 waiting、ramp_ready、blocked 或 closed。
19. 做 Offer Cap / Payout 评审：进入 `/offer-cap-payout`，记录 cap limit/used、payout 版本、approval/paid/deduction、buyer capacity、替代 Offer 审核和阻塞项。
20. 做来源质量评审：进入 `/source-quality`，记录 source、publisher、placement、subid、buyer feedback、approved/paid/deduction、invalid clicks、complaints、policy issue、停源控制和阻塞项。
21. 做供应商合同/争议评审：进入 `/vendor-contracts`，记录 vendor、IO、tracking/reporting appendix、质量条款、invoice、disputed amount、refund/credit/makegood、amount at risk 和阻塞项。
22. 做预算节奏评审：进入 `/budget-pacing`，记录当前日预算、建议日预算、test budget、hard stop、safe CPC、actual CPC、收入成熟度、现金缓冲和阻塞项。
23. 做组合预算评审：进入 `/portfolio-allocation`，记录 Core/Scale/Test/Explore/Quarantine、月度媒体预算、建议分配、revenue status mix、集中度、现金缓冲和阻塞项。
24. 做链接维护：进入 `/links`，只做同主题、已审核、人工确认的 Final URL / Tracking URL 维护。
25. 做风险审计：进入 `/risk-audits`，逐项审计 Cookie、2FA、安全挑战、无效流量、代理/指纹/Worker、cloaking 和封禁规避风险。
26. 记录来源：进入 `/sources`，为每个行业判断、政策边界或高风险结论记录来源 URL、发布方、可信级别和证据摘要。
27. 查看审计链：进入 `/logs`，确认 Offer、CPL 垂类、Lead 定价、Appointment、Buyer Capacity、Ping/Post Routing、Conversion Signal、CRM Value Mapping、页面采集、创意生成、草稿导出、Bulk Upload、Scripts 同步、命名维度、归因增量、指标导入、Query Mining、决策窗口、Offer Cap、来源质量、供应商合同、预算节奏、组合分配、链接轮换和任务执行都有留痕。

## 3. ADXKit 核心能力对应入口

| ADXKit 公开能力 | 本项目入口 | 主要文档 |
| --- | --- | --- |
| 多账号 / MCC 管理 | `/accounts`、`/risk-audits` | [账号、MCC、付款与 Advertiser Verification 治理手册](account_mcc_billing_verification_governance.md) |
| 落地页采集和 Offer Intelligence | `/offers`、Offer 详情页 | [落地页素材抽取、Offer Intelligence 与创意 Brief 手册](landing_offer_intelligence_creative_brief.md) |
| AI 创意生成和 Claim 审核 | Offer 详情页 | [广告创意生成、测试与优化手册](creative_testing_optimization.md)、[广告创意 Claim 审核与事实核查手册](creative_claim_review_fact_checking.md) |
| Campaign / Ad Group / Keyword / Ad 草稿 | `/campaigns` | [Google Ads 投放结构与安全自动化手册](campaign_launch_automation.md) |
| 广告审核、拒登和申诉证据包 | `/ad-reviews` | [Google Ads 广告审核、拒登、Policy Manager 与申诉证据包手册](google_ads_ad_review_disapproval_appeal_playbook.md) |
| CSV / Scripts 导出与 Bulk Upload 门禁 | `/campaigns/<id>/export.csv`、`/campaigns/<id>/export.script.json`、`/bulk-upload` | [Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册](google_ads_editor_csv_bulk_upload_governance.md)、[Google Ads Scripts 安全自动化手册](google_ads_scripts_safe_automation.md) |
| Google Ads Scripts 数据同步治理 | `/scripts-sync` | [Google Ads Scripts 数据同步、快照与一致性手册](google_ads_scripts_data_sync_consistency.md) |
| Campaign 命名、Labels、UTM/SubID 与维度治理 | `/taxonomy-governance` | [Campaign 命名、Labels、UTM/SubID 与维度治理手册](campaign_taxonomy_naming_label_dimension_governance.md) |
| 归因、增量性与流量蚕食治理 | `/attribution` | [归因、增量性与流量蚕食治理手册](attribution_incrementality_cannibalization.md) |
| CPL 垂类经济、资格问题与 Buyer Acceptance | `/cpl-verticals` | [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md) |
| Lead Pricing、Payout Negotiation 与结算安全垫 | `/lead-pricing` | [Lead Pricing、Payout Negotiation 与结算安全垫治理手册](lead_pricing_payout_negotiation_governance.md) |
| Appointment Lead、Booking、Show Rate 与 No-show | `/appointment-leads` | [Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md) |
| Buyer Capacity、Cap Pacing 与 Dayparting | `/buyer-capacity` | [Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md) |
| Ping/Post 与 Lead Buyer Routing | `/ping-post-routing` | [Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md) |
| 转化信号质量与出价学习 | `/conversion-signals` | [转化信号质量与出价学习治理手册](conversion_signal_quality_bidding_learning_governance.md) |
| CRM 阶段与 Offline Conversion Value Mapping | `/crm-value-mapping` | [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md) |
| Search Terms、否定词和 Query Mining | `/query-mining` | [Search Terms、否定词与 Query Mining 治理手册](search_terms_negative_keyword_query_mining.md) |
| Offer Cap、Payout、状态变更和替代 Offer | `/offer-cap-payout` | [Offer Cap、Payout、状态变更与替代 Offer 治理手册](offer_cap_payout_status_governance.md) |
| Source、Publisher、Placement 质量治理 | `/source-quality` | [Source、Publisher、Placement 质量评分与名单治理手册](source_publisher_placement_quality_governance.md) |
| 流量供应商合同、IO 和争议治理 | `/vendor-contracts` | [流量供应商合同、IO、退款与争议治理手册](traffic_vendor_contract_io_dispute_governance.md) |
| 指标同步、利润分析、优化建议、预算门禁和组合分配 | `/metrics/import`、`/optimization`、`/decision-windows`、`/budget-pacing`、`/portfolio-allocation` | [单位经济模型、Break-even 与安全边际手册](unit_economics_margin_safety.md)、[决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md)、[预算节奏、扩量与止损手册](budget_pacing_scaling_stoploss.md)、[Portfolio 预算分配、风险集中度与组合治理手册](portfolio_budget_allocation_risk_concentration.md) |
| 定时任务和执行日志 | `/tasks`、`/logs` | [任务编排、安全审批、执行日志与事故复盘手册](task_orchestration_approval_audit_runbook.md) |
| 换链接 | `/links` | [链接计划与换链接合规手册](link_rotation_compliance.md)、[追踪模板、URL 参数与跳转链 QA 手册](tracking_template_redirect_chain_qa.md) |

## 4. 高风险能力完成入口

这些能力不是“不复刻”，而是复刻为行业诉求、技术原理、平台规则、识别方法、审计字段、SOP、来源 URL 和合规替代流程。

| 高风险点 | 专题 | 系统替代入口 |
| --- | --- | --- |
| Ads Cookie 登录和后台操作 | [专题](high_risk/ads_cookie_backend_operation.md) | `/accounts`、CSV / Scripts JSON、`/logs`、`/risk-audits` |
| 自动绕过登录、2FA、安全挑战 | [专题](high_risk/automated_login_2fa_challenge_bypass.md) | `/tasks`、人工执行、OAuth / Scripts / 权限模型 |
| 补点击、刷展示、模拟自然流量 | [专题](high_risk/invalid_traffic_click_impression_simulation.md) | `/metrics/import`、`/optimization`、来源隔离和对账 SOP |
| 代理、指纹、Worker 转发规避关联检测 | [专题](high_risk/proxy_fingerprint_worker_association_evasion.md) | `/risk-audits`、账号配置、合法隔离证据 |
| Cloaking 或审核页/用户页不一致 | [专题](high_risk/cloaking_review_user_page_mismatch.md) | `/links`、候选 URL、人工确认和 URL 版本日志 |
| 为规避封禁创建或切换账号 | [专题](high_risk/ban_evasion_account_switching.md) | `/accounts`、`/risk-audits`、账号健康证据包 |

总蓝图：[高风险能力逐点调研与安全复刻蓝图](high_risk_capability_safe_reproduction_blueprint.md)，系统入口为 `/knowledge/risk_blueprint`。它把 6 个点统一整理为行业诉求、原理解释、平台风险、系统落地、验收证据和来源 URL。

## 5. 验证命令

```powershell
.\.venv\Scripts\python -m compileall adsworkbench app.py scripts
.\.venv\Scripts\python scripts\verify_research_docs.py
.\.venv\Scripts\python scripts\smoke_test.py
.\.venv\Scripts\python scripts\acceptance_audit.py
.\.venv\Scripts\python -m flask --app app seed
```

`acceptance_audit.py` 会汇总检查 Markdown 文档路由映射、关键验收文档、`.env.example`、单团队 schema、seed 核心数据、高风险来源覆盖、核心页面、Scripts 安全标记，以及账号 / 链接 / 任务的高风险语义拦截。

验收时还应确认 `/docs`、`/knowledge/adxkit`、`/knowledge/acceptance`、`/knowledge/risk_completion`、`/knowledge/risk_index`、`/bulk-upload`、`/scripts-sync`、`/taxonomy-governance`、`/attribution`、`/cpl-verticals`、`/lead-pricing`、`/appointment-leads`、`/buyer-capacity`、`/ping-post-routing`、`/conversion-signals`、`/crm-value-mapping`、`/query-mining`、`/decision-windows`、`/offer-cap-payout`、`/source-quality`、`/vendor-contracts`、`/budget-pacing`、`/portfolio-allocation`、`/sources` 和 `/risk-audits` 可以正常访问。

## 6. 信息来源 URL

- ADXKit homepage: https://adxkit.com/
- Google Ads, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads, Secure your Google Ads account: https://support.google.com/google-ads/answer/2375456
- Google Ads Scripts, Authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- Google Ads Scripts, Reports: https://developers.google.com/google-ads/scripts/docs/concepts/reports
- Google Ads Scripts, Execution logs: https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs
- Google Ads Editor, Prepare a CSV file: https://support.google.com/google-ads/editor/answer/56368
- AdSense, Invalid traffic: https://support.google.com/adsense/answer/16737
