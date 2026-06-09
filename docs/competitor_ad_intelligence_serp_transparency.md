# 竞品广告、SERP 与 Ads Transparency 情报手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何安全使用 Google Ads Transparency Center、Ad Preview and Diagnosis、Auction Insights、Keyword Planner、Google Trends、Search Terms Report、公开 SERP 截图和竞品落地页观察，建立关键词、创意角度、页面承诺、竞争强度和政策边界的情报流程。

目标不是复制竞品、点击竞品广告、仿冒品牌、批量抓取搜索结果或用代理模拟不同地区，而是把公开可见信息转成：市场地图、素材角度、claim 边界、页面证据要求、竞价压力、测试优先级和风险审计。

## 1. 为什么竞品广告情报是套利前置能力

Ads 套利不是只看自己的 CPC 和 RPV。一个 offer 能不能跑通，还受市场里其他广告主、公开素材承诺、页面形式、政策敏感度和 SERP 竞争密度影响。

竞品情报要回答：

1. 用户搜索某类 query 时，SERP 上有哪些广告承诺？
2. 市场主流 angle 是 price、comparison、eligibility、trust、speed 还是 local？
3. 哪些 claim 在垂类里常见，但可能需要资质、披露或页面证据？
4. Auction Insights 是否显示竞争突然变强，导致 CPC 上升或 impression share 下降？
5. 竞品落地页是否提供了更完整的比较、价格、FAQ、资质或披露？
6. 自己的页面和广告是否只是“跟风文案”，没有真正满足 query intent？
7. Offer 条款是否禁止品牌词、竞品词、coupon、direct linking 或某些流量来源？

套利团队使用竞品情报的正确方式：

```text
公开信号
  -> 市场假设
  -> 关键词/angle/页面 brief
  -> 政策和条款审查
  -> 小预算测试
  -> paid revenue / reject / deduction 复盘
```

不要把竞品情报变成：

- 批量复制广告文本。
- 点击竞品广告烧对方预算。
- 用竞品商标伪装官方。
- 抓取或重建个人搜索结果。
- 用代理、指纹、地理位置伪装规避平台限制。
- 用虚假投诉打击竞品。

## 2. 可用来源地图

| 来源 | 能说明 | 不能说明 |
| --- | --- | --- |
| Google Ads Transparency Center | 某些广告主的公开广告素材、广告主信息和广告可见性线索 | 不能完整说明出价、预算、转化、ROI、所有投放国家或真实花费 |
| Ad Preview and Diagnosis | 在指定位置、语言、设备等条件下预览搜索广告展示情况，诊断自己广告是否展示 | 不等于真实拍卖数据，也不应用来反复制造搜索量 |
| Auction Insights | 与你同场拍卖的竞争强度、impression share、overlap、top of page 等 | 不显示竞品预算、关键词、转化、利润 |
| Keyword Planner | 关键词规模、竞争和 bid 估算 | 不是真实 CPC 承诺，也不是合规准入 |
| Google Trends | 主题季节性、地区差异、相关查询 | 不是绝对搜索量和收入预测 |
| Search Terms Report | 自己真实触发 query 和效果 | 不显示所有 query，也不能拿来推断个人身份 |
| 公开 SERP 截图 | 某一时点的广告、自然结果、竞争语境 | 个性化、地区、时间和设备会变化 |
| 竞品落地页人工观察 | 页面承诺、披露、资质、CTA、内容深度 | 不等于竞品真实收入或转化 |
| Offer / affiliate terms | brand bidding、competitor bidding、流量限制 | 不自动覆盖 Google 政策或法律风险 |

## 3. Ads Transparency Center 用法

Google Ads Transparency Center 是面向公众的广告透明度工具，可用于查看广告主和公开广告信息。对套利团队来说，它的价值是理解市场里“别人正在公开表达什么”，而不是反推出竞品投放系统。

可记录字段：

| 字段 | 用途 |
| --- | --- |
| advertiser name | 判断广告主身份和披露方式 |
| advertiser domain | 判断品牌、联盟页、比较页或直客 |
| ad creative summary | 抽取 angle、claim、CTA 和语气 |
| format | Search、Display、YouTube 等素材形式 |
| observed date | 避免把过期素材当当前投放 |
| destination theme | 判断 landing 主题和广告承诺一致性 |
| policy note | 是否涉及金融、医疗、官方、商标、敏感垂类 |

使用边界：

- 可以人工记录公开素材和角度。
- 可以截图保存研究证据。
- 可以提炼“市场承诺”和“页面证据要求”。
- 不要批量抓取、绕过访问限制或构建对抗性监控。
- 不要复制竞品广告文本、图片、logo、页面结构或商标表达。
- 不要把透明度中心当作预算、转化或 ROI 数据源。

## 4. Ad Preview and Diagnosis 用法

Ad Preview and Diagnosis 工具用于预览广告在特定条件下是否可能展示，并诊断广告展示问题。套利团队可用它做上线前 QA：

- 指定国家/地区、语言、设备。
- 检查自己的广告是否可能展示。
- 检查 query、ad text 和 landing 是否符合预期。
- 避免用真实搜索反复触发广告展示。

正确用法：

| 场景 | 动作 |
| --- | --- |
| 上线前确认广告展示语境 | 使用工具截图，不点击广告 |
| 本地化检查 | 对目标 GEO / language / device 做少量 QA |
| 拒登或不展示排查 | 结合 Policy Manager、keyword status 和 budget |
| SERP 语境观察 | 记录同页广告承诺和自然结果类型 |

不正确用法：

- 高频查询制造 impression。
- 点击自己或竞品广告。
- 用代理池模拟多地区用户。
- 用搜索结果差异做 cloaking 规则。

## 5. Auction Insights 解读

Auction Insights 显示你和其他广告主在同一拍卖中的相对表现。它适合解释竞争强度变化：

| 指标 | 套利解释 |
| --- | --- |
| Impression share | 预算、排名或覆盖是否限制展示 |
| Overlap rate | 哪些域名经常和你同场竞争 |
| Position above rate | 对方广告是否经常排在你上方 |
| Top of page rate | 顶部展示竞争程度 |
| Abs. top of page rate | 第一位置竞争强度 |
| Outranking share | 你超过对方的比例 |

套利动作不能只有“加价”。如果竞争变强，应先问：

- 自己的 Quality Score 是否下降？
- landing page 是否比竞品弱？
- query 是否过宽，吸引了高价低质流量？
- 是否应转向长尾、替代型、信息型或更窄 GEO？
- 竞品是否在用更清楚的 CTA 或更完整的披露？
- paid RPV 是否足以支撑加价？

Auction Insights 不能用来：

- 推断竞品真实预算或利润。
- 制作仿冒广告。
- 组织点击竞品广告。
- 做虚假投诉或商标滥诉。

## 6. SERP 采样和市场地图

SERP 采样要少量、可解释、可复盘。

采样字段：

| 字段 | 示例 |
| --- | --- |
| query | `cloud backup pricing small business` |
| country / location | US / California |
| language | English |
| device | mobile / desktop |
| date_time | 2026-06-09 10:00 |
| observed_ads | 广告主、domain、headline 摘要 |
| organic_types | guide、comparison、calculator、official、forum |
| common_angles | comparison、price、trust、speed |
| risky_claims | official、guaranteed、free、#1 |
| page_gap | 自己页面缺少价格、FAQ、资质、披露 |
| action | 新建 page brief、否定词、angle test、hold |

采样原则：

- 固定 query、地区、语言、设备。
- 不点击广告。
- 保存截图和记录时间。
- 不把个性化结果当普遍事实。
- 不用批量自动化绕过搜索访问限制。
- 从 SERP 观察用户任务，而不是复制文案。

## 7. 竞品素材拆解方法

竞品广告不是模板库，而是市场信号。拆解时用“功能标签”，不复制原文。

| 标签 | 观察点 |
| --- | --- |
| angle | comparison、price、eligibility、trust、guide、local |
| claim strength | weak、medium、strong |
| evidence needed | price table、license、review source、FAQ、terms |
| CTA | compare、learn、check、get quote、apply |
| trust marker | rating、editorial disclosure、certification、contact |
| risk marker | official、guaranteed、free、limited time、best |
| landing type | offer、presell、comparison、calculator、lead form |
| disclosure | affiliate、advertising、editorial、privacy |

输出应该是 brief，而不是抄写：

```text
市场观察：竞品多用 comparison + pricing angle。
页面要求：需要价格表、限制条件、更新时间和 affiliate disclosure。
可测试角度：弱 claim 的 "Compare factors before choosing"。
禁止：不要写 "best guaranteed price"、不要暗示官方。
```

## 8. 品牌和商标边界

竞品情报经常会诱导团队买品牌词或写比较页。必须先过四层检查：

1. Google Ads 商标政策。
2. Offer / affiliate terms。
3. 当地法律和商标风险。
4. 用户是否会误认官方或授权关系。

允许的方向：

- 真实替代方案页面。
- 有原创维度的对比页。
- 信息型说明页面。
- 条款允许的 reseller / compatibility 场景。

禁止方向：

- 冒充官方、support、login、customer service。
- 使用竞品 logo、近似域名、颜色和页面布局制造混淆。
- 页面没有比较内容却投 `brand alternative`。
- Offer 禁止 brand bidding 仍投品牌/竞品词。
- 被投诉后换域名、换账号或 cloaking 继续投。

## 9. 情报到创意和页面 brief

竞品情报最终要进入 brief：

| 输入 | 输出 |
| --- | --- |
| 多数竞品强调价格 | 页面补价格解释、限制和更新时间 |
| 多数竞品强调官方/认证 | 检查自己是否有真实资质；没有则禁用 official/certified |
| SERP 自然结果都是指南 | 先做信息页或 checklist，不硬推表单 |
| Auction Insights 显示竞争强 | 选长尾、窄 GEO、提高页面相关性 |
| 透明度中心显示大量相似 claim | 找差异化 angle，不复制 |
| 竞品 landing 有明确披露 | 自己页面补 affiliate / ads disclosure |
| Search terms 出现支持/login | 加否定词或单独排除 |

内部产物：

- `market_map`：垂类、关键词簇、主要广告主、广告角度。
- `claim_boundary`：可用 claim、弱化 claim、禁止 claim。
- `page_gap_list`：页面缺失内容、披露、FAQ、价格、资质。
- `angle_test_plan`：要测的 angle、关键词、页面版本、成功指标。
- `risk_audit`：商标、Misrepresentation、Destination、敏感垂类风险。

## 10. 系统落地

当前系统已有承载点：

| 能力 | 位置 |
| --- | --- |
| 关键词意图和选题 | `keyword_intent_research.md` |
| 品牌/竞品/商标边界 | `brand_bidding_trademark_competitor_policy.md` |
| 报表和 Auction Insights 诊断 | `google_ads_reporting_diagnostics.md` |
| 创意角度库 | `creative_angle_library_feedback_loop.md` |
| 页面素材抽取和 brief | `landing_offer_intelligence_creative_brief.md` |
| 风险审计和来源库 | `/risk-audits`、`/sources` |

后续可扩展：

```sql
CREATE TABLE competitor_market_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  query_text VARCHAR(255) NOT NULL,
  country VARCHAR(64),
  language VARCHAR(64),
  device VARCHAR(32),
  observed_at DATETIME NOT NULL,
  source_type VARCHAR(64) NOT NULL,
  screenshot_path TEXT,
  notes TEXT,
  created_at DATETIME NOT NULL
);

CREATE TABLE competitor_ad_observations (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  snapshot_id BIGINT NOT NULL,
  advertiser_name VARCHAR(255),
  advertiser_domain VARCHAR(255),
  observed_headline_summary TEXT,
  observed_description_summary TEXT,
  angle_tags JSON,
  claim_risk_tags JSON,
  landing_type VARCHAR(64),
  disclosure_observed BOOLEAN,
  created_at DATETIME NOT NULL
);

CREATE TABLE market_angle_briefs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  offer_id BIGINT,
  keyword_theme VARCHAR(255),
  market_summary TEXT,
  allowed_claims JSON,
  blocked_claims JSON,
  page_gaps JSON,
  angle_test_plan JSON,
  reviewer VARCHAR(128),
  created_at DATETIME NOT NULL
);
```

V1 边界：

- 可以保存人工观察、截图路径、角度标签和 brief。
- 可以把公开来源 URL 绑定到风险审计。
- 不点击竞品广告。
- 不批量抓取 SERP 或透明度中心。
- 不用代理/指纹模拟地区。
- 不复制竞品素材、页面、logo 或商标表达。
- 不用虚假投诉作为竞争手段。

## 11. QA 清单

| 检查项 | 通过标准 |
| --- | --- |
| 来源合法 | 来自公开页面、官方工具、人工导出或授权报表 |
| 不点击广告 | 只截图、记录和分析，不制造点击 |
| 不复制素材 | 只抽象 angle 和 claim 类型 |
| 地区/设备记录 | SERP 采样保留 country、language、device、time |
| 商标审查 | brand/competitor/official/support/login 词已审 |
| 页面差距 | brief 明确自己页面需要补什么 |
| 证据要求 | 强 claim 有 proof requirement |
| 实验计划 | 情报转成小预算可验证假设 |
| 风险记录 | Misrepresentation、Destination、Trademarks 和 Offer terms 已审 |
| 反馈闭环 | 结果回写到 angle library、关键词和页面 brief |

## 12. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本系统完成形态 |
| --- | --- |
| 落地页采集 | 只采集自己和公开可访问页面，生成 evidence brief |
| AI 创意生成 | 以市场 angle 和页面证据生成候选，不复制竞品 |
| 优化建议 | 把 Auction Insights、Search terms、SERP 观察转成待验证假设 |
| 自动投放 | 不根据竞品情报自动投放，仍走草稿、导出、人工审核 |
| 换链接 | 不用竞品情报做 cloaking 或审核绕过 |
| 来源库 | 保存官方工具、政策和透明度来源 URL |

## 13. 信息来源 URL

- Google Ads Transparency Center: https://adstransparency.google.com/
- Google Safety Center, Ads and data: https://safety.google/ads-and-data/
- Google Blog, Ads Transparency Center: https://blog.google/technology/safety-security/ads-transparency-center/
- Google Ads Help, Ad Preview and Diagnosis tool: https://support.google.com/google-ads/answer/148778
- Google Ads Help, Auction insights: https://support.google.com/google-ads/answer/2579754
- Google Ads Help, Use Keyword Planner: https://support.google.com/google-ads/answer/7337243
- Google Ads Help, About the search terms report: https://support.google.com/google-ads/answer/2472708
- Google Trends Help, FAQ about Google Trends data: https://support.google.com/trends/answer/4365533
- Google Ads Help, About advertiser verification: https://support.google.com/google-ads/answer/9008739
- Google Ads Policy, Trademarks: https://support.google.com/adspolicy/answer/6118
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Policy, Unacceptable business practices: https://support.google.com/adspolicy/answer/15938071
- FTC, Native Advertising: A Guide for Businesses: https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses
- FTC, Endorsements, influencers, and reviews: https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews

