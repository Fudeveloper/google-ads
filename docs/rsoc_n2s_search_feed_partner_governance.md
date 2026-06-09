# RSOC / N2S、Search Feed Partner 与相关搜索套利治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何理解 RSOC（Related Search on Content）、N2S（Native to Search）、S2S（Search to Search）、Search feed partner、AdSense for Search、Related Search、PIF、RAC、query intent、funnel RPM、扣量、feed 权限和结算治理。目标是把“买量到相关搜索/搜索结果页”当作严格的搜索意图和发布商质量业务来管理，而不是把它做成桥页、误导搜索、广告点击诱导或低质 feed 灌量。

本文不提供 Search feed 接入代码、Related Search 绕审、诱导点击布局、预填搜索词、伪造 query、自动搜索、自动点击、刷 funnel、隐藏 upstream creative、绕过 RAC、低质内容批量生成或 feed partner 权限规避方案。系统只沉淀行业知识、字段、QA、审计、来源 URL、扣量复盘和合规替代流程。

## 1. 为什么 RSOC / N2S 是套利核心模式

展示广告套利通常按 impression 或页面广告点击变现；RSOC / N2S 类模式把用户从内容页、Native 素材或搜索广告带到“相关搜索词 / 搜索结果页 / 搜索广告”漏斗里。它的吸引力在于：

- 搜索广告商业意图更强，单次 ad click 可能高于普通 display revenue。
- Native、Social、Search 等上游流量可以被包装成内容入口或问题入口。
- 可按垂类、国家、设备、query group 和来源分层测试。
- 回收周期比 CPA/CPL 可能更快，但扣量、权限、政策和账户风险更集中。

真正的难点不是“怎么展示搜索广告”，而是证明每一步都有真实用户意图：

```text
Upstream ad / native card / paid search click
  -> content page or information page
  -> related search term click
  -> search results page on publisher site
  -> search ad click
  -> estimated revenue
  -> deductions / finalized revenue / payment
```

只要用户被误导、内容页没有独立价值、搜索词不是用户真实意图、广告多于结果、或上游创意没有如实传递，短期 RPM 就会被扣量、strike、feed 终止、AdSense/Google Ads 风险和广告主投诉吞掉。

## 2. 核心术语

| 术语 | 含义 | 治理重点 |
| --- | --- | --- |
| RSOC | Related Search on Content，内容页展示相关搜索词，点击后进入站内搜索结果页 | 需要 AFS 权限、页面内容相关、Related Search 不能成为页面焦点 |
| AFS | AdSense for Search | query 来源、搜索结果页、广告数量、代码/样式政策 |
| PIF | Product-Integrated Feature，例如 Related Search | 不得诱导误点、不得修改元素、需符合 PIF 政策 |
| RAC | referrerAdCreative，上游受控流量创意文本参数 | 受控流量来源需要完整、逐字传递创意文本 |
| N2S | Native to Search，从 Native/content discovery 素材进入搜索变现漏斗 | 上游创意、内容页、搜索词和结果页必须一致 |
| S2S | Search to Search，从付费搜索进入二级搜索变现漏斗 | 最容易被判为桥页/低价值目的地，需要特别谨慎 |
| Feed partner | 提供搜索广告需求、权限、结算或中间层服务的合作方 | 权限、条款、扣量、来源透明和审计 |
| Funnel RPM | Related search 第一屏 funnel revenue / funnel impressions * 1000 | 不等于最终可收款收入 |
| Clawback / deduction | feed 或平台因质量、无效流量、政策问题扣减收入 | 必须进入扩量模型 |

行业里会把 RSOC、N2S、S2S、search arbitrage、search feed、keyword feed、related search、feed arbitrage 混用。系统里建议统一记录模式字段，而不是只写“feed”：

```text
monetization_mode = rsoc | afs_search | n2s | s2s | parking | display
upstream_channel = native | search | social | direct | organic | email
feed_partner
search_enabled_site
content_page_url
results_page_url
rac_required
```

## 3. 官方政策边界

Google Related Search for content pages 的公开说明强调：Related Search 展示与内容页相关的搜索词，用户点击后进入发布商站内搜索结果页，并在第二屏通过相关 search ads 产生收入。它不是任意页面的高 CPC 词触发器，也不是把内容页伪装成搜索页的工具。

关键边界：

- 需要 AdSense for Search 相关权限和必要的合同/账号经理流程。
- Related Search 单元要和页面内容相关，不能成为页面唯一焦点。
- 页面需要有足够文本内容，不能只有 Related Search 或少量低价值内容。
- 每个 Related Search term 点击必须进入与该 term 相关的站内搜索结果页。
- Related Search term 发给 Google 的请求应与用户点击的 term 一致。
- Partner-provided terms 必须为了相关性，不得为了高 CPC、特定广告或人为提高展示/点击/转化。
- 搜索广告只能放在搜索结果页，并且要清楚区分广告和自然结果。
- 不能激励用户搜索、点击或观看广告。
- Search ads 请求和 ad unit 数量必须满足对应桌面/移动政策。
- 不能 backfill、混合或交替使用不允许的 Google 广告请求类型来填同一 placement。

对套利团队，最重要的是：Google 的广告网络滥用政策也会关注 bridge/gateway、arbitrage、低价值目的地、cloaking 和规避审核。即使 feed partner 允许某种流量，Google Ads 买量目的地仍然要有真实内容、可访问性、广告承诺一致性和用户价值。

## 4. 上游流量、RAC 和创意一致性

从 2025-11-01 起，Google 帮助页说明：当用户从你控制的来源进入 Related Search for Content 页面时，包括第三方 network、service 或 affiliate，需通过 `referrerAdCreative` 参数提供上游创意文本。

运营上要把 RAC 当成“上游承诺证据”，而不是一个可随便填的参数：

```text
upstream_platform
campaign_id
creative_id
creative_title
creative_description
creative_transcript
rac_text
rac_hash
destination_page_url
review_status
```

RAC 风险例子：

| 上游真实创意 | 错误做法 | 风险 |
| --- | --- | --- |
| “Free cruises to the Bahamas” | 只传 “Bahama cruises” | 隐藏 free 承诺，误导系统判断 |
| “We are hiring drivers today” | 目标页没有招聘列表 | 身份和可履约承诺不一致 |
| “Government loan forgiveness 2026” | 页面只有泛金融文章 | 政府/贷款 claim 不可兑现 |
| Influencer 视频口播 | 只传短标题，不传口播/屏幕文字 | RAC 不完整 |

上游流量治理原则：

- Creative 只能承诺目标页能直接满足的内容。
- 如果页面主要是资讯，只能用 learn / compare / review / discover 一类弱承诺。
- 不用倒计时、免费、现金、录取、雇佣、贷款批准、政府补贴等不可控强承诺。
- Native / social / search 的素材和目标页标题、正文、related terms、results page 要一致。
- 不要为了提高 CTR 隐藏商业关系、伪装官方或制造紧迫感。

## 5. Content Page 不是桥页

合格 RSOC 内容页至少应有独立价值。用户即使不点击 related term，也能得到基本信息、比较、步骤、限制、FAQ 或决策帮助。

内容页 QA：

- 标题和正文主题一致。
- 首屏有可读内容，不是只有 Related Search 单元。
- Related Search 是补充导航，不是页面任务本身。
- 页面不使用 “click here / search now / get best offer” 等诱导语把注意力指向 PIF。
- 页面有作者/更新时间/主体/隐私/联系信息。
- 敏感垂类有免责声明、资格限制和来源。
- 移动端不让 Related Search 或广告遮挡正文。
- 对从 paid source 来的用户和 organic 用户展示 substantially same 页面。

高风险页面：

- 只有标题、图片、Related Search 单元，没有实质内容。
- 内容和 related terms 无关，只借高价关键词变现。
- 上游创意承诺“申请/领取/免费”，目标页却只是搜索词列表。
- 用弹窗、箭头、按钮样式或假导航诱导点击 Related Search。
- 审核/organic 用户看到内容页，paid 用户看到 ad-heavy 搜索桥页。

## 6. Search Results Page 和 Query Intent

Search results page 的价值来自真实 query intent。广告应补充搜索结果，而不是替代搜索结果。

结果页治理字段：

```text
query
query_source = user_search | related_search_click | alternative_query
results_count
ads_count
organic_results_count
search_term_exact_match
results_relevance_score
ad_label_visible
user_action_id
request_count_per_action
```

关键原则：

- 不预填用户没有明确选择的 query。
- 不修改、扩展、过滤用户点击的 Related Search term 来触发更高价广告。
- 不为同一用户动作发多次搜索广告请求。
- 搜索结果页要有相关自然结果或站内结果。
- 广告数和自然结果数、桌面/移动单位数要符合 Search ads policies。
- 不用激励、奖励、积分或误导按钮推动用户搜索或点击广告。

如果 query intent 很弱，短期仍可能有 ad click，但广告主转化差、扣量和 feed 权限风险会滞后出现。

## 7. Feed Partner 尽调

Search feed partner 不是普通 affiliate network。它往往同时控制权限、样式、报表、结算、扣量和政策解释。尽调要问：

| 问题 | 必须拿到的答案 |
| --- | --- |
| 权限来源 | 直接 AFS 权限、managed partner、reseller，还是不透明中间层 |
| 允许流量 | Native、Search、Social、Organic、Push、Email 是否允许 |
| 禁止内容 | 金融、医疗、博彩、成人、政府、招聘等限制 |
| RAC / upstream creative | 是否要求完整创意、口播、屏幕文字、参数传递 |
| 页面审核 | mock-up、content page、results page、移动端、样式是否预审 |
| Reporting | funnel request、funnel click、ad click、gross revenue、deduction、finalized revenue |
| Deduction | 无效流量、低质量来源、广告主投诉、政策问题如何扣量 |
| Payout | estimated、finalized、net terms、reserve、threshold、chargeback |
| 停量粒度 | 是否可按 source、campaign、publisher、creative 停止 |
| 证据 | 政策文档、邮件确认、样式批准、结算样例 |

如果 partner 无法解释权限、拒绝提供流量限制、只承诺高 RPM、不提供扣量规则或要求隐藏来源，按高风险处理。

## 8. 经济模型和扣量

RSOC/N2S 不能用单一 CPC 和 RPM 判断。

```text
content_page_views
  * related_search_click_rate
  * search_results_ad_click_rate
  * gross_ad_click_epc
  * revenue_share
  * finalized_ratio
  - traffic_cost
  - tooling / content / review cost
```

核心指标：

| 指标 | 含义 | 用法 |
| --- | --- | --- |
| CPV / CPC | 上游流量成本 | 按 channel、source、geo、device 拆分 |
| Related search CTR | 内容页到搜索页点击率 | 过高可能是诱导点击或内容弱 |
| SERP ad CTR | 搜索结果页广告点击率 | 要和 query relevance 一起看 |
| Gross RPV | 预估收入 / upstream visit | 冷启动观察，不用于扩量上限 |
| Finalized RPV | 扣量后收入 / upstream visit | 扩量依据 |
| Deduction rate | 扣量 / gross revenue | 风控核心 |
| RAC coverage | 需要 RAC 的访问中参数完整比例 | 低于阈值暂停 |
| Complaint / strike | 政策事故 | 优先于 ROI |

安全 CPC：

```text
safe_cpc = finalized_rpv * safety_factor
```

新 source、new geo、new vertical、new creative 默认 safety factor 应低；至少等一个结算/扣量周期后再提高预算。

## 9. 常见事故诊断

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| Funnel CTR 异常高 | PIF 太突出、诱导语、移动端误点 | 暂停页面版本，截图审计 |
| Related terms 不展示 | 页面未被 crawl、robots 阻挡、内容不足、参数干扰 | 查 crawl、ignoredPageParams、正文质量 |
| Gross revenue 高，finalized 低 | 无效流量、广告主价值差、来源质量差 | 按 source/geo/device/query 隔离 |
| RAC 缺失 | 上游平台未传、creative 没有版本化 | 停受控流量，修参数和证据 |
| Strike / RAF 降级 | 非合规来源、RAC 不准确、PIF 诱导点击 | 停量，做证据包和页面修复 |
| Search page ad-only | 自然结果不足或结果不相关 | 补结果质量，降广告密度 |
| Paid search 亏损 | Quality Score、CPC 上升、feed EPC 下降 | 查 query、landing、finalized RPV |

修复原则：先停异常来源和页面版本，再保留证据。不要用更多流量、自动搜索、点击任务或 cloaking 去“补”模型。

## 10. 系统落地

当前 V1 可用模块：

| 需求 | 当前页面 / 文档 |
| --- | --- |
| 记录 Search feed / RSOC / N2S Offer 和 partner 条款 | `/offers`、`/sources` |
| 记录上游创意、目标页、claim 和页面证据 | `/offers/<id>/crawl`、Claim 审核 |
| 导入成本、点击、收入、扣量后收入 | `/metrics/import` |
| 记录 RAC、PIF、桥页、误导来源、扣量事故 | `/risk-audits` |
| 输出暂停、降预算、隔离 source 建议 | `/optimization` |
| 衔接基础 Search Feed 知识 | [Search Arbitrage、Feed 与 Parking 模式手册](search_arbitrage_feed_parking.md) |

后续可扩展表：

```text
search_feed_partners
rsoc_page_reviews
rsoc_creative_rac_reviews
rsoc_funnel_daily
rsoc_query_group_daily
rsoc_source_quality_daily
rsoc_deduction_reports
rsoc_policy_incidents
search_feed_settlement_runs
```

这些表只用于 QA、证据、对账、扣量复盘和人工决策；不生成 AFS/RSOC 代码、不接入 feed、不自动搜索、不修改 Google 返回元素、不隐藏上游创意。

## 11. QA 清单

- 是否有合法 AFS / Related Search 权限或 partner 书面确认。
- content page 是否有足够独立内容，且 Related Search 不是页面焦点。
- 上游 creative 是否逐字完整记录，RAC 是否覆盖所有受控来源。
- traffic source 是否准确描述目标页，不承诺无法直接兑现的 offer。
- paid 用户和 organic 用户看到的页面是否 substantially same。
- partner-provided terms 是否只为相关性，不为高 CPC 或特定广告。
- search results page 是否有相关自然结果，广告清晰标识。
- 是否按 user action 控制 search ad request，避免重复请求。
- 是否按 source、creative、query group、geo、device 查看 finalized RPV。
- deduction、strike、complaint、RAF 状态是否能触发停量。
- feed partner 是否提供结算、扣量、权限和流量限制证据。
- 系统没有自动搜索、点击、刷 funnel、cloaking 或绕 RAC 功能。

## 12. 信息来源 URL

- Google AdSense Help, Related search for your content pages: https://support.google.com/adsense/answer/10233819
- Google AdSense Help, AdSense for Search Product-Integrated Feature policies: https://support.google.com/adsense/answer/14638581
- Google AdSense Help, AdSense for Search policies: https://support.google.com/adsense/answer/1354757
- Google AdSense Help, Search ads policies: https://support.google.com/adsense/answer/7003954
- Google for Developers, AdSense Custom Search Ads implementation guide: https://developers.google.com/custom-search-ads/s/docs/implementation-guide
- Google AdSense Help, Search ads parameter descriptions: https://support.google.com/adsense/answer/9055049
- Google AdSense Help, AdSense for Search Restricted Access Features: https://support.google.com/adsense/answer/16262554
- Google AdSense Help, Policy violations in scope for Restricted Access Features: https://support.google.com/adsense/answer/16269587
- Google Ads Policies, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads Policies, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Publisher Policies: https://support.google.com/publisherpolicies/answer/10437486
- Google Publisher Restrictions: https://support.google.com/publisherpolicies/answer/10437795
- Jounce Media, Terminology: https://jouncemedia.com/resources/terminology
- Coinis Glossary, RSOC: https://coinis.com/glossary/rsoc-related-search-on-content
- Coinis Glossary, Native to Search: https://coinis.com/glossary/native-to-search
