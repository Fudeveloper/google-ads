# Google Ads 报表诊断、Search Terms 与 Change History 手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何用 Google Ads 报表把“亏在哪里、为什么亏、谁改动导致、下一步该停还是修”讲清楚。重点覆盖 Search terms report、Search terms insights、Auction Insights、Change history、Report Editor、segments、landing pages report、RSA asset report、bid strategy report、PMax 结果诊断、下载归档和系统落地。目标不是追求报表漂亮，而是形成可复盘、可止损、可扩量的诊断闭环。

## 1. 为什么报表诊断决定套利生死

套利团队每天面对的是不完整、不同时区、不同口径的数据：

```text
Google Ads clicks / cost
-> landing requests / GA4 sessions
-> offer clicks / postback
-> estimated revenue
-> approved / finalized / paid revenue
```

如果只看 campaign 总 ROI，很容易误判：

- 某个 search term 正在烧钱，但被 campaign 平均值掩盖。
- CPC 上升来自竞价对手，而不是创意变差。
- ROI 下降来自昨天改预算、改匹配方式或换页面，而不是市场变化。
- PMax 或 broad match 扩展到不相关查询，但报表没有分层。
- landing page 移动端体验差，导致点击到了但 session / conversion 断掉。

报表诊断的目的，是把每个亏损或增长拆到可行动维度：query、keyword、asset、landing page、device、location、hour、network、bid strategy、change event。

## 2. 报表诊断闭环

建议使用固定流程：

1. 先看目标：ROI、CPA、RPV、approved/paid revenue 是否过线。
2. 再分层：campaign、ad group、keyword/search term、asset、landing page、device、geo、hour、network。
3. 查变化：Change history 里是否有预算、出价、匹配、URL、素材、转化或目标调整。
4. 查竞争：Auction Insights 是否显示 impression share、overlap、outranking、top of page 变化。
5. 查页面：Landing pages report、server log、GA4 和页面审计是否一致。
6. 查自动化：bid strategy report、PMax insights、recommendations 是否解释了流量变化。
7. 形成动作：暂停、否定词、拆组、调预算、修页面、换素材、等回传、申诉或停测。

不要把平台建议直接当结论。Recommendations、optimization score、simulators 和 insights 是输入，不是套利团队的利润判决。

## 3. Search Terms Report

Search terms report 展示触发广告的真实搜索词及其表现。它是搜索套利、lead arbitrage 和信息页买量的第一诊断报表。

核心用途：

| 用途 | 判断 |
| --- | --- |
| 找否定词 | 花费高、意图不相关、无收入或低 lead quality |
| 找新关键词 | 有转化、有收入、query intent 清晰 |
| 判断 match type | broad/phrase 是否扩到错误意图 |
| 识别品牌/竞品风险 | 是否触发禁止的品牌、官方、商标或敏感词 |
| 解释低 ROI | 是否被低价值查询、免费/就业/政府/骗局等词消耗 |

套利团队要特别关注：

- `search_term` 是否和页面主题、Offer 和广告承诺一致。
- `keyword` / `match_type` 是否解释得通。
- 花费是否集中在少数无收入 query。
- Search terms 不完整时，是否至少用 search term insights、GA4 landing intent、server log 和页面 query 参数辅助判断。
- 不要为了“补齐不可见搜索词”去伪造点击、事件或查询。

## 4. Search Terms Insights 与 PMax

Search terms insights 会把搜索词聚合成类别和子类别，帮助理解用户搜索主题。对 Performance Max、AI-powered Search 和 broad match 场景尤其重要，因为流量扩展更难靠单一 keyword 解释。

可用来判断：

- 是否进入了不相关主题。
- 某类查询是否有高 spend、低 conversion 或低 paid revenue。
- 页面内容是否覆盖真实用户意图。
- 素材和 landing page 是否需要按意图分组。

限制：

- 类别是诊断入口，不是完整 query 级真相。
- PMax 的渠道和查询扩展需要和 channel performance、asset、landing page 和 conversion quality 一起看。
- 对套利业务，PMax 不能只看 Google Ads conversions；必须对到 paid / finalized revenue。

## 5. Auction Insights

Auction Insights 用于比较你和其他广告主在同一拍卖中的表现。它不是“谁是敌人名单”，而是解释竞争强度和 impression share 变化的工具。

常见指标解释：

| 指标 | 套利判断 |
| --- | --- |
| Impression share | 是否因为预算、排名或覆盖不足错失展示 |
| Overlap rate | 哪些竞品经常和你同场出现 |
| Position above rate | 对方广告是否经常排在你上方 |
| Top of page rate | 顶部展示机会变化 |
| Abs. top of page rate | 最高位竞争强度 |
| Outranking share | 你超过对方的比例 |

如果 CPC 上升、impression share 下降、top of page 下降，可能是竞争变强、Quality Score 变差、预算受限或 bid strategy 学习变化。动作不一定是加价；也可能是换长尾、拆国家、修 landing page、提高相关性或停掉无利润 query。

## 6. Change History

Change history 可以查看过去账号、campaign、ad group 等层级的变更。对套利来说，它是事故复盘的证据链：

- 谁改了预算。
- 谁改了 bid strategy。
- 谁改了 keyword match type。
- 谁改了 ad asset、final URL、tracking template。
- 谁接受了 recommendation。
- 哪天导入了批量修改。

复盘方法：

```text
performance drop time
-> check change history +- 72 hours
-> classify change type
-> compare affected segments
-> decide rollback / wait / split / fix
```

不能只看报表跌了就换 Offer 或补点击。先看是否有人改了结构、预算、出价、URL、转化目标、资产或否定词。

## 7. Report Editor 和 Segments

Report Editor 可以保存、下载和分段报表。套利团队至少要固定这些分层：

| 分层 | 为什么看 |
| --- | --- |
| Day / hour / day of week | 发现时段波动、回传延迟和预算节奏问题 |
| Device | 移动端误点、页面速度、lead 质量差异 |
| Location | 国家、州、省、市和 Offer 允许地区是否一致 |
| Network | Search、Search Partners、Display、PMax channel 差异 |
| Keyword / search term | 意图和成本来源 |
| Landing page | 页面版本、Final URL expansion、404 或错页 |
| Conversion action | primary / secondary、submitted / approved / paid 混用 |

报表下载要求：

- 保留原始 CSV 文件名、下载时间、账号、时区和日期范围。
- 不覆盖旧文件。
- 每次优化动作要能追溯到报表版本。
- 指标导入时标注 estimated、approved、finalized 或 paid 口径。

## 8. Landing Pages Report

Landing pages report 用于评估落地页表现，并能暴露实际扩展 URL、移动端体验和页面问题。

套利团队要看：

- 点击是否进入预期 Final URL。
- expanded landing page 是否出现异常路径、404、参数污染或错误语言。
- mobile speed、valid clicks、conversions 和 revenue 是否按页面版本差异明显。
- Final URL expansion 是否把流量送到不适合套利目标的页面。
- 页面主题、广告承诺和 query intent 是否一致。

如果 clicks 高、sessions 低或 landing page 报表出现异常 URL，先查 tracking template、Final URL suffix、parallel tracking、redirect chain、server log 和页面速度，不要用补点击或伪造事件修报表。

## 9. RSA / Asset Report

Responsive Search Ads 会组合多个 headline 和 description。Asset report 可以帮助比较素材表现，但不能脱离 query、landing page 和政策语境。

套利团队使用方式：

- 把 asset 分为 intent、proof、price、risk reducer、CTA 等类型。
- 低表现 asset 先查是否不相关、过度承诺、语义太泛或被政策限制。
- 高表现 asset 也要过 Claim / Proof 审核，不能因为 CTR 高就放大不实承诺。
- 不要频繁同时改所有资产，否则 Change history 很难解释波动。

RSA 诊断要和 Search terms、landing page、Quality Score、conversion quality 一起看。

## 10. Bid Strategy Report

Smart Bidding 和 portfolio strategy 会引入学习期、目标变化、预算限制、conversion lag 和 top signals。Bid strategy report 用于判断自动出价是否在稳定学习，还是被错误目标和低质量回传带偏。

套利团队重点看：

- 目标 CPA / ROAS 是否基于 paid revenue，而不是 submitted conversions。
- 转化量是否足够支持自动出价。
- conversion lag 是否导致短期 CPA 虚高或 ROAS 虚低。
- top signals 是否集中在某些设备、地区、时段或受众。
- 调整目标后是否给足学习窗口。

如果回传质量差，Smart Bidding 会把预算推向“容易提交但不可收款”的流量。先修 conversion action 和 value feedback，再扩预算。

## 11. 异常诊断矩阵

| 现象 | 优先查 |
| --- | --- |
| Cost 突增，revenue 不变 | Change history、budget、match type、Search terms、PMax expansion |
| CPC 上升 | Auction Insights、Quality Score、competitor、bid strategy |
| Clicks 正常，sessions 低 | Landing pages report、redirect chain、server log、mobile speed |
| Conversions 上升，paid revenue 不升 | conversion action、lead quality、postback、buyer feedback |
| CTR 上升，RPV 下降 | 素材承诺错配、低意图 query、误点或低质量版位 |
| Search terms 变泛 | broad match、PMax、Final URL expansion、negative keywords |
| 改动后 1-2 天波动 | Change history、learning、conversion lag，不急着连续大改 |
| 竞品压制明显 | Auction Insights、long-tail strategy、QS、landing relevance |

## 12. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 导入日级 cost/clicks/conversions/revenue | `/metrics/import` |
| 记录 Search terms、Auction Insights、Change history 复盘结论 | `/risk-audits` |
| 将报表来源、官方帮助和诊断规则沉淀 | `/sources` |
| 对亏损 segment 生成暂停/检查建议 | `/optimization` |
| 将 URL、tracking 和 landing page 问题关联到链接计划 | `/links` 和相关文档 |

后续可扩展表：

```text
google_ads_report_snapshots
search_term_diagnostics
auction_insight_daily
change_history_events
landing_page_performance_daily
asset_performance_snapshots
bid_strategy_diagnostics
```

建议字段：

```text
account_id
campaign_id
ad_group_id
date_range
report_type
downloaded_at
timezone
search_term
keyword
match_type
device
location
network
landing_page_url
asset_text
change_type
changed_by
cost
clicks
conversions
approved_revenue
paid_revenue
diagnosis
action
evidence_url
```

系统边界：

- 不用报表缺口作为补点击、模拟访问或伪造转化的理由。
- 不自动接受 Google Ads recommendations。
- 不绕过 Search terms 可见性限制去重建个人身份或敏感查询。
- 不把 Change history 当作追责工具外泄个人账号信息；只做内部审计。
- 不用 Cookie 后台操作抓报表；后续如自动化，应走官方 API、Scripts 或人工导出。

## 13. QA 清单

- 每日复盘至少包含 cost、clicks、conversions、approved/paid revenue 和 ROI。
- Search terms 按 spend、conversion、paid revenue 和 intent 分组。
- 否定词动作保留 query、原因、层级和日期。
- Auction Insights 只用于解释竞争，不用于商标误导或仿冒。
- Change history 与性能波动时间线一起归档。
- Report Editor 导出保留账号、日期范围、时区和文件版本。
- Landing pages report 出现异常 URL 时先查追踪链和 Final URL expansion。
- RSA asset 高 CTR 也必须经过 Claim / Proof 审核。
- Bid strategy 判断必须考虑 conversion lag 和回传质量。
- 所有优化动作能回溯到报表证据，不凭单日总 ROI 大幅扩量。

## 14. 信息来源 URL

- Google Ads Help, About the search terms report: https://support.google.com/google-ads/answer/2472708
- Google Ads Help, About search terms insights: https://support.google.com/google-ads/answer/11386930
- Google Ads Help, Use auction insights to compare performance: https://support.google.com/google-ads/answer/2579754
- Google Ads Help, About change history: https://support.google.com/google-ads/answer/19888
- Google Ads Help, Create custom reports in Report Editor: https://support.google.com/google-ads/answer/7489070
- Google Ads Help, Measure your results: https://support.google.com/google-ads/answer/6172626
- Google Ads Help, Evaluate the performance of your landing pages: https://support.google.com/google-ads/answer/7543502
- Google Ads Help, About campaign level asset reporting for responsive search ads: https://support.google.com/google-ads/answer/9781208
- Google Ads Help, How to find your bid strategy reports: https://support.google.com/google-ads/answer/7074568
- Google Ads Help, Evaluate your automated bid strategy's performance: https://support.google.com/google-ads/answer/10167267
- Google Ads Help, Evaluate Performance Max results: https://support.google.com/google-ads/answer/16279166
- Google Ads Help, About the Insights page: https://support.google.com/google-ads/answer/10256472
