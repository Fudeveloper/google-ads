# Search Arbitrage、Feed 与 Parking 模式手册

更新时间：2026-06-08

本文解释 Ads 套利里的 search arbitrage、search feed、AdSense for Search / Custom Search Ads、Search Partners 和 parked domain 模式。目标是帮助团队理解“买来的搜索或类搜索意图如何变成搜索广告收入”，以及为什么这类模式对 query intent、页面价值、广告标识、Search ads 政策和目的地质量要求非常高。本文不提供预填充查询诱导、虚假搜索、自动搜索、点击诱导、parking 低质流量灌入、cloaking、桥页或绕过 feed 审核的方案。

## 1. 模式定义

### 1.1 Search arbitrage

Search arbitrage 是用付费流量获得用户，再通过搜索广告、搜索结果页或相关搜索页变现。核心公式：

```text
Search RPV = Search ads revenue / paid clicks
Gross Profit = Search ads revenue - traffic acquisition cost
ROI = Gross Profit / traffic acquisition cost
```

常见路径：

```text
Google Ads / Native / Social click
  -> Search-like landing page
  -> User query or related search
  -> Search results page with ads
  -> Ad click revenue
```

合法与否不取决于“是否有搜索广告”，而取决于：用户是否有真实搜索意图、页面是否有真实结果和价值、广告是否清楚标识、query 是否真实来自用户动作、流量是否真实可解释。

### 1.2 Search feed / AFS / CSA

Search feed 通常指发布商或合作伙伴通过被批准的搜索广告产品，在自己站点搜索结果页展示搜索广告。Google 的 Search ads 是 AdSense for Search 功能，允许在站点搜索结果页用用户查询展示相关广告；Custom Search Ads web implementation 需要有 active permission 才能使用。

行业里“feed 权限”很值钱，是因为搜索广告预算和用户意图更接近，RPM/EPC 可能高于普通展示广告。但 feed 权限也意味着更严格的政策、query 来源、结果页内容、广告展示和流量质量要求。

### 1.3 Parking / Parked domain

Parked domain 是已注册但没有充分开发的网站。Google Ads 帮助文档说明，Search Partner Network 可以包含 parked domain search results；但 Google Ads 政策不允许广告链接到只展示广告列表和链接、没有独特有价值内容的 parked domain。

截至 2026-06-08，Google Ads 帮助文档还说明：新账号自 2024 年 10 月起默认不在 parked domains 展示广告，现有账号自 2025 年 3 月起也默认 opt out，若广告主希望展示需要在内容适宜性设置中 opt in。

## 2. 经济模型

Search/feed 套利不是简单的 `CPC < RPM/1000`。它至少有四层漏斗：

```text
Paid traffic click
  -> Search page visit
  -> Search / related search action
  -> Search ad impression
  -> Search ad click
  -> Feed revenue
  -> Finalized / payable revenue
```

关键指标：

| 指标 | 说明 |
| --- | --- |
| TAC | Traffic Acquisition Cost，买量成本 |
| Search action rate | 点击买量广告后产生真实搜索动作的比例 |
| Ad request rate | 搜索动作产生合规搜索广告请求的比例 |
| Ad CTR | 搜索广告点击率 |
| RPC / CPC out | 每次搜索广告点击收入 |
| RPV | 每个买量点击或 session 的收入 |
| Deduction rate | 因无效流量、低质查询或政策问题产生的扣量 |
| Finalized margin | 经 finalized / paid 后的真实毛利 |

简化公式：

```text
Search RPV = Search action rate * Ad CTR * RPC * (1 - deduction rate)
Max TAC = Search RPV * safety factor
```

安全系数要比普通内容页更保守，因为 search feed 的扣量、质量审核和权限风险更集中。冷启动不建议超过 `0.4 - 0.6`，稳定期也应等一个以上结算周期后再提高预算。

## 3. 参与方和利益链

| 角色 | 目标 | 风险 |
| --- | --- | --- |
| Traffic buyer | 低价买入真实意图 | 标题党、低意图、无效流量 |
| Publisher / arbitrage operator | 把用户导向搜索或结果页 | 页面价值不足、桥页、政策违规 |
| Feed provider / syndication partner | 提供搜索广告需求和结算 | query 质量、publisher 质量、合规责任 |
| Google / search ads provider | 保护广告主和用户体验 | 无效点击、query 操纵、低质流量 |
| Advertiser | 获得真实潜在客户 | 为低意图或误导流量付费 |

长期可持续的模式必须让广告主也有价值。只要下游广告主长期亏损、投诉或低转化，短期 RPM 再高也会变成扣量、限制、feed 终止或账号风险。

## 4. Search ads 政策要点

Google AdSense Search ads policies 里有几条对套利尤其关键：

- 传给 Google 的 query variable 必须匹配用户搜索意图。
- 搜索广告只能用于由清晰用户搜索意图返回的搜索结果页。
- 每个用户动作只允许一个 Search ads 请求。
- 广告代码只能用于搜索结果页。
- 广告必须清楚标识，并与搜索结果区分。
- 不能激励用户搜索或看广告。
- 广告应补充搜索结果，而不是成为结果本身。
- 广告数量不应超过用户查询对应的搜索结果数量。

这些要求说明：search feed 不是“任意页面变现组件”，也不是“把关键词塞进 URL 触发高价广告”的工具。它依赖真实用户查询、真实搜索结果和清楚广告标识。

## 5. Google Ads 买量到搜索页的风险

当 Google Ads 作为买量来源时，目标页还要符合 Google Ads destination requirements 和 advertising network abuse 政策。

高风险信号：

- 目的地主要为了展示广告或把用户送往其他广告页。
- 原创内容少，广告比内容多。
- 页面是 bridge、gateway、doorway 或中间页。
- 广告承诺和最终搜索/广告页主题不一致。
- 页面诱导用户点击搜索广告。
- 用户没有真实查询动作，却被带到预填 query 的广告结果页。
- 审核页和真实用户页不一致。

合规方向：

- 先提供清晰主题、工具、目录、比较或站内搜索价值。
- 用户明确输入或选择查询。
- 搜索结果和广告清楚区分。
- 页面能解释为什么用户需要搜索结果，而不是只为了广告点击。
- 广告 Final URL、tracking template、landing page 和最终搜索页一致可审计。

## 6. Parked domains 和 Search Partners

Parked domains 在广告生态里有两种不同视角：

- 广告主视角：可能通过 Search Partner Network 在 parked domain search results 展示广告；Google Ads 提供内容适宜性和排除工具。
- 站点/发布商视角：如果广告链接到只展示广告列表和链接、没有独特有价值内容的 parked domain，会触发目的地质量和 parked domain 政策风险。

Google Ads 的 parked domain 帮助文档说明，parked domain 通常几乎没有内容，可能只是保留地址、等待开发或注册过期。对套利团队来说，这意味着：

- 不能把 parked page 当成高质量落地页。
- 不能用只有广告链接的域名作为 Google Ads 目标页。
- 若买量报告显示大量 parked domain inventory，要单独评估质量和排除。
- 域名词、错拼词、过期域流量如果无法解释用户意图，应按高风险处理。

## 7. Query Intent 和结果页质量

Search/feed 套利的质量核心是 query intent。

合格 query：

- 来自用户明确输入、点击真实搜索控件或合规相关搜索功能。
- 与页面主题、广告承诺和用户预期一致。
- 能返回真实、有用、可区分的搜索结果。
- 不是程序批量生成、预填充、诱导或隐藏修改。

不合格 query：

- 用户没有搜索，只是被自动跳到 query 页。
- Query 被系统替换成高价词。
- 用户点的是“查看结果”，实际触发广告请求。
- 页面只有广告，没有足够自然结果或内容。
- 用误导素材把低意图用户带到高价商业 query。

结果页质量清单：

| 项目 | 要求 |
| --- | --- |
| 查询来源 | 可证明是用户动作 |
| 搜索结果 | 有真实非广告结果，不只广告 |
| 广告标识 | 广告和自然结果明显区分 |
| 数量比例 | 广告不压过结果 |
| 页面主题 | 与广告承诺一致 |
| 导航 | 用户能返回、修改查询、访问隐私和条款 |
| 速度 | 移动端可用，不靠延迟诱导误点 |
| 日志 | 保留 query、source、session、ad request、收入和扣量口径 |

## 8. 流量来源准入

允许测试的来源应满足：

- 用户意图能解释。
- 广告素材不夸大、不误导。
- 来源可按 source / placement / keyword / creative 分段。
- 价格和质量合理，不是异常低价黑箱流量。
- 可以停量、限量、排除和复盘。

拒绝来源：

- autosurf、paid-to-search、paid-to-click、click exchange。
- bot、自动浏览、激励搜索、奖励点击。
- 来源不透明、只承诺大流量低价格。
- 需要代理、指纹、cloaking、Worker 转发隐藏来源。
- 要求预填 query 或修改用户查询。

## 9. 测试和放量 SOP

冷启动：

1. 只选一个国家、一个页面主题、一个真实搜索意图。
2. 固定 search partner / feed / buyer 规则，确认是否允许该流量来源。
3. 使用小预算，保留 source、query、landing version、ad request 和 revenue 日志。
4. 不用短期 estimated RPM 判断放量。

日常复盘：

| 信号 | 判断 |
| --- | --- |
| Search action rate 很低 | 买量素材和页面意图不一致 |
| Ad CTR 异常高 | 检查广告标识、误点、结果数量比例 |
| Revenue 高但 finalized 下调 | 质量或无效流量问题 |
| Query 分布过窄或过商业 | 检查是否被系统诱导或替换 |
| 某 source 扣量高 | 暂停并隔离 |
| 用户投诉 | 审计承诺、广告标识和隐私披露 |

放量前：

- 至少经过一个结算周期。
- 扣量可解释且可按来源定位。
- Search ads 政策检查通过。
- Google Ads destination / advertising network abuse 审计通过。
- 不依赖任何补点击、自动搜索、预填 query 或 cloaking。

## 10. 系统落地

当前系统可支持：

| 业务动作 | 系统位置 |
| --- | --- |
| 记录 Search/feed/Parking Offer、国家、限制和政策备注 | `/offers` |
| 用 RPV、CPC、扣量和安全系数测算可买流量成本 | `/calculators` |
| 记录落地页标题、描述、H1、链接和质量分 | Offer 详情页落地页采集 |
| 导入真实 cost、clicks、revenue 和 conversions | `/metrics/import` |
| 对异常 ROI、CTR、RPV 生成优化建议 | `/optimization` |
| 对 query intent、bridge page、parked domain、无效流量做审计 | `/risk-audits` |
| 保存 Search ads、AFS、CSA、parked domain 和目的地政策来源 | `/sources` |

后续可扩展但仍安全的能力：

- `search_feed_daily`：source、query_group、search_actions、ad_requests、ad_clicks、revenue、deduction。
- `query_quality_summary`：query、intent、source、result_count、ad_count、approval_status。
- 页面审计增加广告/结果比例字段。
- 指标导入支持 finalized revenue 和 estimated revenue 区分。

不做：

- 不生成预填 query 链接。
- 不模拟用户搜索。
- 不自动点击搜索广告。
- 不做 paid-to-search、autosurf、click exchange。
- 不把 parked domain 或桥页作为 Google Ads 目标页。
- 不做 cloaking 或审核页/用户页不一致。

## 11. 信息来源 URL

- Google AdSense Help, Search ads policies: https://support.google.com/adsense/answer/7003954
- Google AdSense Help, About Search ads: https://support.google.com/adsense/answer/9000515
- Google for Developers, AdSense Custom Search Ads Web Implementation: https://developers.google.com/custom-search-ads/web/
- Google Ads Help, Search partners definition: https://support.google.com/google-ads/answer/2616017
- Google Ads Help, Parked domain site: https://support.google.com/google-ads/answer/50002
- Google Ads Help, Exclude specific webpages and videos: https://support.google.com/google-ads/answer/2454012
- Google Ads Policies, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Policies, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads Policies, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google AdSense Help, AdSense Program policies: https://support.google.com/adsense/answer/48182
- Google Publisher Policies: https://support.google.com/publisherpolicies/answer/10437486
- Jounce Media terminology: https://jouncemedia.com/resources/terminology
