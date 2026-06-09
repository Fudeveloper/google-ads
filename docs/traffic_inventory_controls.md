# Google Ads 流量库存、版位与排除控制手册

更新时间：2026-06-08

本文解释 Google Ads 中 Search、Search Partners、Display、Demand Gen、YouTube、Performance Max、placement exclusions、content suitability、brand exclusions、Final URL expansion 和 channel reporting 在 Ads 套利里的作用。目标是让团队把“库存来源”和“出价目标”分开管理，避免把 Google Search、Search Partners、Display、YouTube、Discover、Gmail、PMax 混成一个平均 ROI。本文不提供隐藏来源、代理/指纹规避、Worker 转发、cloaking、刷展示、补点击或购买不可解释低价流量的方案。

## 1. 为什么库存控制重要

套利团队经常看到这样的误判：

- Google Search ROI 好，打开 Search Partners 后整体 ROI 变差，却不知道是哪部分变差。
- Display 点击便宜，但 sessions、lead quality 或 finalized revenue 很差。
- Demand Gen 素材 CTR 好，后端 approved revenue 不稳定。
- PMax 报表 ROI 好，但主要来自品牌词、再营销或低透明库存。
- Final URL expansion 把用户送到不适合变现或不符合 Offer 条款的页面。
- 某些 app、site、YouTube channel 或 parked domain 带来大量点击和低质量收入。

库存控制的核心不是“把所有不确定流量都关掉”，而是：

```text
先分层 -> 单独测试 -> 保留可解释库存 -> 排除不可解释/不可收款库存 -> 再放量
```

## 2. Google Ads 库存分层

| 库存 | 用户意图 | 透明度 | 套利风险 |
| --- | --- | --- | --- |
| Google Search | 主动搜索 | 高，search terms 可复盘 | CPC 高，政策严格 |
| Search Partners | 类搜索/合作伙伴 | 中，质量波动 | 来源差异、parked/search partner 质量 |
| Display Network | 浏览内容时触达 | 中，placement 可看但量大 | 误点、低意图、app/site 质量 |
| YouTube | 视频消费场景 | 中，channel/video 可排除 | 注意力和点击意图不稳定 |
| Demand Gen | YouTube、Discover、Gmail 等视觉库存 | 中到低 | 素材驱动、归因长、低意图 |
| Performance Max | 跨 Google inventory 自动化 | 逐步增强但仍混合 | 早期难定位 source、品牌词和自动 URL 风险 |

测试原则：不要把不同意图和透明度的库存混在一个冷启动预算里。套利冷启动要先建立 Google Search 或单一渠道基线，再逐个打开扩展库存。

## 3. Search Partners 控制

Search Partners 可带来额外搜索网络流量，但质量可能和 Google Search 不同。

准入条件：

- Google Search 本体已有稳定基线。
- URL 参数保留 `{network}`、campaign、ad group、keyword、device。
- 能按 network segment 复盘 clicks、sessions、conversions、approved revenue。
- Offer 条款允许该来源。

停量信号：

- Search Partners 花费占比高，但 approved revenue 低。
- click -> session 差异显著高于 Google Search。
- 搜索词/来源不可解释。
- 扣量、无效流量或 buyer feedback 集中在 Search Partners。
- 与 Search 本体混跑后无法判断真实 ROI。

建议动作：

- 冷启动阶段关闭或单独测试。
- 稳定后小预算打开。
- 不把 Search Partners 的平均 CPC 当作 Search 本体 CPC。
- 对 parked domain、低质 partner 或异常来源做排除和审计。

## 4. Display、YouTube 与 Demand Gen

Display / YouTube / Demand Gen 是“素材和场景驱动”的库存，不是用户主动查询。套利团队需要额外关注：

- 是否有真实内容承接，而不是高广告密度页面。
- 是否有移动端误点。
- placement 是否可解释。
- 页面是否能承接低意图流量。
- consent、personalized ads 和敏感垂类限制是否满足。
- 后端 approved / paid revenue 是否跟得上 reported conversions。

常见排除维度：

| 维度 | 用途 |
| --- | --- |
| Website placement | 排除低质站点、无关站点、异常 publisher |
| App placement | 排除误点高、低意图或儿童/游戏类 app |
| YouTube channel/video | 排除不适合品牌或低质量内容 |
| Topic/content exclusions | 排除敏感内容类别 |
| Content suitability | 统一管理品牌安全和适宜性设置 |
| Excluded content keywords | 避免在不适合主题周边展示 |

注意：排除会限制可投放库存，不能用“全排光”的方式代替策略。排除的依据应来自数据：高成本低收入、投诉、政策风险、低质量 session、扣量或不适合品牌。

## 5. Performance Max 库存控制

PMax 是跨 Google Ads inventory 的自动化 campaign。它适合已有清晰目标、稳定转化和可承受探索成本的业务；不适合用来在套利冷启动阶段寻找未知机会。

PMax 前置条件：

- conversion action 代表 approved/paid 或至少 qualified value。
- Offer、页面、国家、语言和价值口径稳定。
- Search、Display 或其他单渠道已有基线。
- 有预算承受学习和探索。
- 可以接受一定程度的库存混合和归因复杂性。

需要重点配置：

- Brand exclusions：避免品牌词、竞品词或不允许的品牌 query。
- Negative keywords：排除不合适查询，尤其是低质量和敏感词。
- Final URL expansion：确认是否允许自动选择其他页面。
- URL exclusions：排除 careers、support、about、privacy、非商业页、不合规页。
- Page feeds：约束或提示可用页面，但要理解和 Final URL expansion 的关系。
- Content suitability / placement exclusions：控制不适合展示环境。
- Channel performance report：观察 PMax 在 Search、YouTube、Discover、Gmail 等 channel 的贡献。
- Asset report：淘汰弱素材，避免误导性高 CTR。

高风险信号：

- PMax ROI 看似很好，但主要来自品牌词或再营销。
- 没有 approved/paid value，只优化 submitted lead。
- Final URL expansion 把用户送到不该投放的页面。
- Search、Display、YouTube 表现被混成平均值。
- Channel report 显示某 channel 消耗高但后端收入低。

## 6. Final URL Expansion 和 URL 控制

Final URL expansion 允许 Google 根据用户搜索意图把用户送到同域名更相关的页面，并可能生成动态文案。它可以提高覆盖，但对套利团队风险很大。

风险：

- 送到未审核页面。
- 送到 About、Blog、Support、Privacy、Careers 等非转化页面。
- 送到不符合 Offer 条款、垂类资质或披露要求的页面。
- 动态文案和页面承诺出现不一致。
- 多个 Offer 或多个国家页面被混用。

控制原则：

- 单 Offer / 单国家 / 单页面测试时，优先关闭 Final URL expansion 或严格用 URL exclusions。
- 需要多页面覆盖时，使用 page feeds、URL exclusions 和清晰页面标签。
- 所有可被投放页面都必须通过落地页审计。
- 不让 PMax 或 AI Max 自动选择未审页面来解决转化问题。

## 7. Content Suitability 和 Placement Exclusions

Content suitability 是 Google Ads 管理展示环境、内容类别和 excluded placements 的集中入口。Google Ads 文档说明，placement exclusions 可防止广告展示在不适合的 videos、channels、websites、apps 等位置；account-level placement exclusions 可以覆盖 Display Network、YouTube 或 Search Partner Network 中不想出现的位置。

套利团队的排除层级：

| 层级 | 用途 |
| --- | --- |
| Account-level exclusions | 全账号都不想投的站点、app、channel |
| MCC/shared lists | 跨客户或多账号复用黑名单，第一版系统不做多租户但可记录策略 |
| Campaign-level exclusions | 某个垂类、国家、Offer 的临时排除 |
| URL exclusions | PMax / Search AI URL 扩展时排除页面 |
| Brand exclusions | PMax / Search 中控制品牌 query |
| Negative keywords | Search / PMax query 控制 |

排除原因必须记录：

- 政策不适合。
- 低质量 session。
- 高花费无 approved revenue。
- app/placement 误点。
- 用户投诉。
- brand/competitor/official/support/login 风险。
- 站点内容不适合品牌或敏感垂类。

## 8. 报表和诊断

每天至少分这些维度看：

```text
campaign
network / channel
device
country
placement / app / site / YouTube channel
keyword / search term / brand category
landing page
conversion action
reported / approved / paid revenue
```

不要只看 Google Ads 的 aggregate ROI。套利判断要加上：

- Click -> session。
- Session -> outbound / lead / revenue。
- Reported -> approved。
- Approved -> paid。
- Deduction / scrub。
- Policy warning / complaint。
- Placement quality。

PMax 复盘要拆：

- Channel performance report。
- Asset group / asset report。
- Search terms / insights。
- Brand exclusions 是否有效。
- URL expansion 实际落地页。
- Account-level placement exclusions 是否覆盖异常库存。

## 9. 库存实验设计

冷启动顺序建议：

1. Google Search phrase/exact 建基线。
2. Search Partners 单独小预算测试。
3. Display / Demand Gen 用独立页面和素材角度测试。
4. PMax 只在 conversion value、后端质量和页面库稳定后测试。
5. 每次只打开一个新增库存层。

测试前必须写明：

- 测试库存是什么。
- 为什么用户会有意图。
- 预算和硬止损。
- 需要哪些 URL 参数。
- 可按什么维度停量。
- 哪些 placements、brands、URLs、topics 预先排除。
- 用 approved/paid 还是 reported revenue 做结论。

## 10. 系统落地

当前系统支持：

| 业务动作 | 系统位置 |
| --- | --- |
| 记录 campaign channel、预算、bid strategy 和 Final URL | `/campaigns` |
| 导入 network/channel 层成本、点击、收入 | `/metrics/import` |
| 对 ROI、CTR、CPC、RPV 异常生成建议 | `/optimization` |
| 记录库存控制、placement exclusion、PMax 风险来源 | `/sources`、`/risk-audits` |
| 用链接计划记录 Final URL / candidate URL 变更 | `/links` |
| 用任务中心安排 URL、CSV、Script JSON 和指标复核 | `/tasks` |

后续可扩展但仍安全的能力：

- `inventory_controls`：network、placement、exclusion_type、reason、evidence_url。
- `placement_performance_daily`：placement、cost、sessions、approved_revenue、deduction。
- `pmax_channel_daily`：channel、cost、conversions、value、approved_value。
- `url_expansion_audit`：expanded_url、allowed、excluded、reviewer。
- Campaign export 前提示 Final URL expansion、brand exclusion 和 placement risk。

不做：

- 不隐藏来源或剥离追踪参数。
- 不用代理、指纹或 Worker 改变库存识别。
- 不自动购买不可解释流量。
- 不用 cloaking 解决低质量 placement。
- 不补点击、刷展示或模拟自然流量来掩盖低质量库存。

## 11. 信息来源 URL

- Google Ads Help, About content suitability: https://support.google.com/google-ads/answer/12764663
- Google Ads Help, Exclude placements at the account level: https://support.google.com/google-ads/answer/7331110
- Google Ads Help, Exclude specific webpages and videos: https://support.google.com/google-ads/answer/2454012
- Google Ads Help, Use placement exclusion lists across your accounts: https://support.google.com/google-ads/answer/9162992
- Google Ads Help, About Performance Max campaigns: https://support.google.com/google-ads/answer/10724817/about-performance-max-campaigns
- Google Ads Help, Search targeting & controls for Performance Max: https://support.google.com/google-ads/answer/16672776
- Google Ads Help, About the channel performance report for Performance Max: https://support.google.com/google-ads/answer/16260130
- Google Ads Help, About Final URL expansion in Performance Max: https://support.google.com/google-ads/answer/14337539
- Google Ads Help, About URL exclusion in Performance Max: https://support.google.com/google-ads/answer/14337773
- Google Ads Help, Apply brand exclusions to Performance Max or Search campaigns: https://support.google.com/google-ads/answer/14505308
- Google Ads Help, How to use brand suitability features in Performance Max: https://support.google.com/google-ads/answer/13607727
- Google Ads Help, About asset reporting in Performance Max: https://support.google.com/google-ads/answer/10725056
- Google Ads Help, About Display ads and the Google Display Network: https://support.google.com/google-ads/answer/2404190
- Google Ads Help, Create a Demand Gen campaign: https://support.google.com/google-ads/answer/13695389
- Google Ads Policies, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
