# Portfolio 预算分配、风险集中度与组合治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何把 Offer、campaign、country、device、traffic source、publisher、landing page、account、revenue partner 和 cashflow 看成一个投资组合，设计预算分配、风险预算、集中度限制、扩量阶梯和退出规则。目标是让团队用可收款收入和风险证据做组合经营，而不是把全部资金押到一个短期 ROI 好看的 campaign、单一来源、单一账号或单一结算方。本文不提供绕过预算、规避账单风控、自动补点击、刷展示、虚假转化、Cookie 后台无人改预算或封禁后换号继续放量的方案。

## 1. 为什么 Portfolio 治理是套利生存问题

单个 campaign ROI 为正，不代表业务安全。套利组合会同时承受：

- 广告花费先发生，收入后确认。
- 单一 Offer 突然降 payout、停 cap、暂停、拒付。
- 单一 traffic source 出现 invalid traffic、扣量、投诉或质量下滑。
- 单一账号、域名、站点或付款资料出现审核、限制或支付问题。
- 单一国家、设备、时段或 query cluster 竞争变贵。
- 单一变现方拖款、hold、finalized revenue 下调。

Portfolio 治理的目标是控制“相关风险的放大速度”。一个健康组合不是没有失败项，而是失败项足够小、可定位、可停量、不会吞掉现金流。

## 2. 原理解释：套利组合不是平均 ROI

很多团队看组合时只看：

```text
portfolio ROI = total profit / total cost
```

这会掩盖风险。正确做法是同时看：

```text
weighted ROI
cash at risk
revenue status mix
concentration exposure
correlation exposure
settlement lag
policy exposure
source quality exposure
```

示例：两个组合都显示 20% ROI：

| 组合 | 表面 ROI | 真实风险 |
| --- | --- | --- |
| A | 20% | 90% 花费来自一个 pending CPL Offer，buyer 还没 approved |
| B | 20% | 5 个来源、3 个 Offer、paid/finalized 口径稳定 |

组合 B 更健康。套利组合不能只追求平均值，要控制尾部风险和现金占用。

## 3. 核心对象地图

| 对象 | 风险作用 | 组合维度 |
| --- | --- | --- |
| offer | payout、cap、approval、reject、status | Offer exposure |
| traffic source | 流量质量和可停量性 | Source exposure |
| publisher / placement | 版位质量和无效流量 | Placement exposure |
| country / geo | CPC、payout、政策、本地化 | Geo exposure |
| device | mobile/desktop RPV、误点、表单质量 | Device exposure |
| landing_version | 页面质量、审核和 CVR | Landing exposure |
| ad account | 付款、验证、政策和预算 | Account exposure |
| revenue partner | AdSense/GAM/affiliate/lead buyer | Settlement exposure |
| cash pool | 可动用现金、信用额度、付款周期 | Liquidity exposure |
| policy class | 敏感垂类、个性化广告、官方服务 | Policy exposure |

这些对象要能在报表中 join。不能 join 的组合风险，只能靠感觉管理。

## 4. 组合分层：Core、Scale、Test、Explore、Quarantine

建议把预算池分成五类：

| 层级 | 含义 | 预算原则 |
| --- | --- | --- |
| Core | 已经历 paid/finalized，质量稳定 | 最大预算池，但仍有集中度上限 |
| Scale | approved/paid 初步稳定，正在扩量 | 每次增加 10%-30%，严控回传窗口 |
| Test | 小样本验证中的 Offer/source/page | 固定测试预算和硬止损 |
| Explore | 新垂类、新国家、新来源 | 小额学习，不追求当期利润 |
| Quarantine | 有扣量、拒付、投诉、policy 或追踪问题 | 暂停新增预算，只做诊断 |

不要把 Test 或 Explore 的短期高 ROI 当成 Core。Core 的标准是：真实可收款、可复盘、可停量、可通过政策和现金流审计。

## 5. 风险预算模型

月度预算应拆成：

```text
monthly_cash_available
- fixed_operating_cost
- debt / payment obligations
- emergency_reserve
= deployable_media_budget

deployable_media_budget:
  core_budget
  scale_budget
  test_budget
  explore_budget
  reserved_stoploss_budget
```

建议初始比例：

| 阶段 | Core | Scale | Test | Explore | Reserve |
| --- | --- | --- | --- | --- | --- |
| 冷启动 | 0%-20% | 0%-20% | 40%-60% | 10%-20% | 20%-30% |
| 有稳定收入 | 40%-60% | 15%-25% | 10%-20% | 5%-10% | 15%-25% |
| 成熟组合 | 60%-75% | 10%-20% | 5%-10% | 0%-5% | 10%-20% |

Reserve 不是闲钱，而是用来覆盖回传延迟、退款、扣量、支付失败、账号限制和紧急停源后的现金缺口。

## 6. 集中度限制

建议设置硬上限：

| 集中对象 | 建议上限 | 原因 |
| --- | --- | --- |
| 单一 Offer 花费占比 | 25%-40% | 防 payout/cap/status 突变 |
| 单一 traffic source 花费占比 | 25%-40% | 防来源质量事故 |
| 单一 publisher/placement | 10%-20% | 防版位无效流量或扣量 |
| 单一 country | 30%-50% | 防政策、CPC、季节和本地化风险 |
| 单一 account | 40%-60% | 防付款、验证、审核或账号限制 |
| 单一 revenue partner | 40%-60% | 防拖款、hold、finalized 下调 |
| pending / estimated revenue 占比 | < 50% | 防账面盈利、现金断裂 |
| sensitive vertical 花费占比 | 视资质更低 | 防政策和投诉集中 |

这些比例不是固定法律，应按团队现金、行业、账号成熟度和历史扣量调整。但必须有上限，而不是“哪个赚钱就全砸过去”。

## 7. 相关性风险

表面上多个 campaign 可能其实是同一个风险：

| 表面分散 | 实际相关风险 |
| --- | --- |
| 5 个 campaign | 同一个 Offer、同一个 buyer |
| 3 个国家 | 同一个 landing template、同一政策 claim |
| 多个 source | 同一个 traffic broker 下游 |
| 多个账号 | 同一付款资料、同一主体、同一域名资产 |
| 多个页面 | 同一个广告栈和同一 AdSense account |
| 多个 keyword cluster | 同一敏感主题或官方服务误导风险 |

Portfolio 复盘要做 correlation map：

```text
campaign -> offer -> buyer -> payout/cap
campaign -> source -> publisher -> placement
campaign -> account -> payment_profile -> advertiser_verification
landing -> domain -> adsense_site -> policy_center
creative -> claim -> proof -> policy_class
```

相关风险高的预算要合并计算 exposure，不要按 campaign 数量假装分散。

## 8. Revenue Status Mix

组合收入要按状态分层：

| 状态 | 可用于组合扩量吗 |
| --- | --- |
| estimated | 只能看趋势，不进入长期预算上限 |
| pending | 按历史 approval rate 折扣 |
| approved | 可用于小幅扩量，但看付款风险 |
| finalized | 可用于中长期模型 |
| paid | 可用于现金预算和核心池 |
| disputed / held | 不用于扩量，先处理风险 |
| rejected / deducted | 进入损失和来源评分 |

组合健康指标：

```text
paid_revenue_ratio = paid_revenue / total_reported_revenue
approved_or_better_ratio = (approved + finalized + paid) / total_reported_revenue
deduction_ratio = deducted_revenue / reported_revenue
pending_exposure = pending_revenue / monthly_media_cost
```

如果 ROI 主要来自 estimated 或 pending，组合还没有被证明。

## 9. Allocation Score

建议给每个预算单元算 Allocation Score：

```text
paid_roi                  25
approved_revenue_quality  15
source_quality            15
policy_safety             15
cashflow_lag              10
concentration_headroom    10
operational_readiness      5
learning_value             5
```

动作建议：

| Score | 动作 |
| --- | --- |
| 85-100 | Core 保留或小幅扩量 |
| 70-84 | Scale，受集中度和回传窗口约束 |
| 55-69 | Test/Watch，不扩量 |
| 35-54 | Quarantine，暂停新增预算 |
| 0-34 | Stop，归档或拉黑 |

learning_value 只适用于 Explore/Test，不能用“学习价值”长期掩盖亏损。

## 10. 组合扩量规则

扩量前必须同时满足：

- paid / finalized 或至少 approved revenue 支撑。
- source quality 不低于 watchlist。
- 未超过 Offer、source、account、partner 集中度上限。
- conversion lag、buyer feedback、deduction window 已等待。
- cash reserve 足够覆盖最坏回款延迟。
- 最近没有 high severity policy、invalid traffic、payment 或 tracking incident。

组合扩量顺序：

1. 扩同一来源中的 proven query / placement。
2. 扩相邻 query、creative angle 或 landing version。
3. 扩相邻国家/设备。
4. 扩新 source。
5. 扩新 Offer 或新 revenue partner。

越往后，越要降低预算步长和提高证据要求。

## 11. 组合降风险和退出规则

出现以下情况，必须降低组合风险：

- 单一 Offer、source、account 或 buyer 超过集中度上限。
- pending/estimated revenue 占比过高。
- AdSense finalized 下调、buyer reject 或 deduction 增加。
- source quality 降级到 quarantine。
- account verification、payment failure、Policy Center 或 disapproval 增加。
- cash reserve 低于未来 14-30 天媒体费。
- 同时多个 campaign 因同一 root cause 异常。

退出动作：

```text
freeze scale budget
-> reduce test/explore spend
-> cap single exposure
-> pause weak segments
-> wait for revenue settlement
-> update allocation score
-> postmortem
```

不要用开新账号、新域名、隐藏来源或换链接来掩盖组合风险。

## 12. 系统落地

当前系统已实现 Portfolio 组合治理 V1：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer、payout、状态和政策限制 | `/offers` |
| 以 source_score、cash_buffer_days、safety_factor 做机会测算 | `/calculators` |
| 导入 cost、click、conversion、revenue | `/metrics/import` |
| 用 dashboard 看总成本、收入、ROI | `/` |
| 用优化建议处理亏损和 stop-loss | `/optimization` |
| 记录组合预算池、建议分配、revenue status mix、集中度和现金缓冲 | `/portfolio-allocation` |
| 用风险审计记录集中风险、扣量和账号问题 | `/risk-audits` |
| 用来源库记录依据和规则 | `/sources` |

V1 表：

```text
portfolio_allocation_reviews
```

核心字段：

```text
portfolio_allocation_reviews:
  offer_id, campaign_draft_id, name, portfolio_bucket,
  monthly_media_budget, proposed_allocation, spend_to_date,
  reported_revenue, pending_revenue, approved_revenue,
  finalized_revenue, paid_revenue, deducted_revenue,
  single_offer_exposure_percent, single_source_exposure_percent,
  single_account_exposure_percent, single_partner_exposure_percent,
  cash_reserve_days, source_quality, policy_risk, incident_state,
  score, risk_level, recommended_action, allocation_percent,
  remaining_monthly_budget, cash_at_risk, revenue_quality_ratio,
  blockers, status, notes, source_urls
```

状态流：

```text
open -> reviewed -> waiting
open -> approved_for_manual_allocation
open -> reduce_exposure
open -> quarantine
open -> closed
```

`/portfolio-allocation/<id>/status` 只更新内部处理状态并写入 `audit_logs`。它不会自动修改 Google Ads daily budget、account budget、bid strategy、Final URL、link rule、buyer routing 或发布商后台。

后续可拆分表：

```text
portfolio_budgets
portfolio_budget_allocations
portfolio_exposure_daily
portfolio_concentration_limits
portfolio_allocation_decisions
portfolio_cash_reserve_snapshots
portfolio_postmortems
```

字段示例：

```text
portfolio_exposure_daily:
  day, offer_id, source_id, account_id, revenue_partner,
  country, device, policy_class, cost, reported_revenue,
  approved_revenue, finalized_revenue, paid_revenue,
  pending_revenue, deduction, allocation_score

portfolio_concentration_limits:
  entity_type, entity_id, max_cost_share, max_pending_share,
  max_policy_risk_share, reason, approved_by
```

系统只生成组合评分、预算建议和风险审计，不自动登录后台、不自动改预算、不规避付款或账号风控。

## 13. ADXKit 对应点和完成形态

ADXKit 类工具常强调“批量测、自动优化、自动放量”。Portfolio 治理对应的是：自动化之前先管理风险预算。

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI dashboard | 同时展示 revenue status、cash at risk 和 concentration |
| 自动扩量 | `/portfolio-allocation` 生成 allocation decision，不无人值守加预算 |
| 多 Offer 管理 | 按 payout、cap、approval、paid revenue 分层 |
| source 管理 | 来源质量和集中度共同决定预算 |
| 任务中心 | 生成周报、月度关账、集中度审计任务 |
| 链接计划 | 只在已审核、同意图、同来源准入下切换 |

完成标准：

- 能解释为什么平均 ROI 不足以证明组合安全。
- 能定义 Core、Scale、Test、Explore、Quarantine 预算池。
- 能给出集中度限制、相关性风险和 revenue status mix。
- 能在 `/portfolio-allocation` 保存 Portfolio Allocation Score、risk_level、recommended_action、blockers、source_urls 和状态流。
- 能把组合预算连接到 source quality、cashflow、risk audits、decision windows、budget pacing 和 optimization。
- 明确不实现 Cookie 后台预算接管、绕过账单风控、补点击、伪造转化或封禁规避。

## 14. QA 清单

每周组合复盘检查：

- 单一 Offer、source、publisher、account、country、revenue partner 是否超上限。
- ROI 是否主要来自 pending 或 estimated。
- paid/finalized revenue 是否支撑 Core 预算。
- 最近 7/14/30 天 deduction、reject、refund、hold 是否上升。
- source quality 是否有 watchlist/quarantine 占比上升。
- 是否有同一 root cause 影响多个 campaign。
- cash reserve 是否覆盖最坏回款延迟。
- Test/Explore 是否有硬止损，是否被当成 Core 放量。
- 是否保留失败实验和停源 postmortem。
- 是否禁止用换账号、隐藏来源、cloaking 或补量修复组合风险。

## 15. 信息来源 URL

- Google Ads Help, Budget report: https://support.google.com/google-ads/answer/10702522
- Google Ads Help, About spending limits: https://support.google.com/google-ads/answer/10486637
- Google Ads Help, Create an account budget: https://support.google.com/google-ads/answer/2375395
- Google Ads API, Account budgets: https://developers.google.com/google-ads/api/docs/billing/account-budgets
- Google Ads Help, Performance Planner: https://support.google.com/google-ads/answer/9230124
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Data discrepancies: https://support.google.com/google-ads/answer/7457111
- Google Ads Help, Find your bid strategy reports: https://support.google.com/google-ads/answer/7074568
- Google Ads Help, About manager accounts: https://support.google.com/google-ads/answer/6139186
- Google AdSense Help, Payment timelines: https://support.google.com/adsense/answer/7164703
- Google AdSense Help, Deductions from earnings FAQs: https://support.google.com/adsense/answer/2808531
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google SRE Book, Managing Incidents: https://sre.google/sre-book/managing-incidents/
