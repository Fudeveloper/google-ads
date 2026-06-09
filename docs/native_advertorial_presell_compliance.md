# Native、Advertorial 与 Presell Page 套利手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何管理 Native / Content Discovery 流量、Advertorial / Presell Page、内容推荐素材、商业披露、claim 审核、source / publisher 质量、Offer 跳转和后端收入复盘。目标是让团队把 Native 流量当作“半意图内容漏斗”来治理，而不是用标题党、假新闻、伪评价、桥页或低质广告密度页面套利。

本文不提供误导标题、假新闻样式、伪造评价、隐藏商业关系、cloaking、补点击、自动浏览、隐藏来源或规避 Native 平台审核的方案。

## 1. 为什么 Native 是套利高频场景

Native / Content Discovery 流量常见于内容推荐位、媒体站推荐模块、移动内容流、资讯 App 和 publisher network。它的用户心智不是主动搜索，也不是强社交关系，而是“被一个内容角度吸引”。

套利团队使用 Native 的原因：

- CPC 可能低于 Search。
- 素材角度可大量测试。
- 适合教育型、故事型、比较型、清单型页面。
- 可作为 CPA/CPL、affiliate、display RPM 或 search feed funnel 的入口。

但 Native 的风险也更集中：

- 用户意图弱，容易高 CTR 低 paid revenue。
- 标题党会提高点击但降低 lead 质量、增加投诉和退款。
- Advertorial 容易伪装成独立新闻、评测或医生/专家推荐。
- Presell page 容易变成桥页，只负责把用户推到 Offer。
- Publisher/source 质量不透明，扣量和无效流量风险滞后暴露。

## 2. 核心对象

| 对象 | 作用 | 套利风险 |
| --- | --- | --- |
| Native ad | 内容推荐素材、标题、缩略图、CTA | 标题党、误导图片、假新闻感 |
| Advertorial | 广告式文章或品牌内容页 | 商业关系披露不足、伪装编辑内容 |
| Presell page | Offer 前置教育/筛选页 | 桥页、夸大承诺、低原创价值 |
| Publisher / source | 展示 Native 广告的位置或媒体 | 质量不透明、bot、误点、低意图 |
| Widget / placement | 推荐模块或版位 | 误点、上下文不匹配、广告标识弱 |
| CTA / bridge link | 从内容页进入 Offer 的路径 | 隐藏目的地、跳转链不一致 |
| Disclosure | 广告、赞助、affiliate 或商业关系说明 | 不清楚会变成误导 |
| Postback / revenue | Offer 或广告收入回传 | 低质 lead、refund、scrub 滞后 |

## 3. Native Funnel 结构

典型 Native 套利链路：

```text
Native ad impression
  -> native click
  -> advertorial / presell page
  -> CTA click
  -> offer / form / search feed / monetization page
  -> conversion / ad revenue / postback
  -> approved / finalized / paid revenue
```

每一层都要能解释：

- 用户为什么点击。
- 页面是否兑现素材承诺。
- 用户是否知道这是广告、赞助或商业推荐。
- CTA 后面会发生什么。
- Offer 是否允许 Native / advertorial / presell 流量。
- source / publisher 能否按粒度停量。
- 后端收入是否最终可收款。

## 4. Advertorial 与 Presell Page 边界

Advertorial 可以是合规的商业内容，但必须透明。Presell page 可以帮助用户理解 Offer，但不能只是“下一步/继续/查看推荐”的桥页。

合格页面：

- 页面主题、标题、素材和 Offer 方向一致。
- 页面有实质内容：背景、比较、限制、适用/不适用人群、FAQ、风险提示。
- 广告/赞助/affiliate 关系清楚披露。
- 作者、更新时间、主体、联系方式、隐私和条款可见。
- CTA 描述真实下一步。
- 页面不是为了制造广告曝光、翻页或误点。

高风险页面：

- 新闻站外观，但没有真实媒体主体或清楚广告披露。
- 医生、专家、用户故事或评分不可验证。
- “本地人震惊”“银行不想让你知道”“政府新政策”等制造假权威。
- 页面只用长故事诱导用户点击，缺少事实、来源和限制。
- Offer 页面、审核页面和用户实际页面不一致。
- 广告密度高，内容价值低，接近 MFA 或 bridge page。

## 5. 素材、缩略图和 Claim 审核

Native 素材通常依赖 curiosity gap，但 curiosity gap 不能变成虚假承诺。

审核维度：

| 维度 | 检查问题 |
| --- | --- |
| 标题 | 是否暗示无法证明的结果、身份、官方关系或紧迫性 |
| 图片 | 是否使用误导 before/after、名人、医生、品牌或假截图 |
| 地域 | 是否暗示本地政策、补贴、资格或价格但页面无证据 |
| 数字 | 是否有真实来源支持 savings、rating、approval rate、income |
| 评价 | 是否真实、可追踪、有披露，不是 AI 伪造 |
| 敏感垂类 | 金融、医疗、博彩、住房就业信贷是否满足额外披露 |
| 下一步 | CTA 是否描述真实动作，而不是诱导误点 |

安全表达不是把标题写得无聊，而是把强承诺降级成可验证的学习/比较角度。例如：

- 不写 “Erase debt today”，写 “Questions to ask before choosing debt relief options”。
- 不写 “Doctors hate this trick”，写 “What to compare before choosing treatment options”。
- 不写 “Government pays homeowners”，写 “Review eligibility factors for home programs”。

## 6. 披露和商业关系

FTC Native Advertising guidance 强调，广告如果看起来像新闻、评测、文章、推荐或其他非广告内容，广告性质必须清楚、显著地披露。披露不能藏在页脚、灰色小字或点击后才看到。

披露原则：

- 靠近标题、推荐、评分、CTA 或广告模块。
- 用用户能理解的词：Advertisement、Sponsored、Paid advertisement、Affiliate disclosure。
- 不用模糊词替代，例如 “Partner content” 如果用户仍不明白是广告，就不够清楚。
- 页面中有佣金、排名、推荐、评分、样品、赞助或商业关系时，要明确说明。
- 移动端、sticky CTA、弹窗和广告模块不能遮挡披露。

对套利团队，披露不是“转化损失”，而是减少 misrepresentation、投诉、拒付、账号暂停和长期扣量的基础控制。

## 7. Source / Publisher 质量治理

Native 流量质量差异极大。不能只看 network 总 ROI，要拆到 publisher、source、placement、widget、creative、geo 和 device。

必须记录字段：

```text
network
campaign
creative_id
publisher_id
source_id
placement_id
widget_id
geo
device
landing_version
offer_id
click_id / subid
cost
sessions
cta_clicks
conversions
approved_revenue
paid_revenue
refund / scrub reason
```

高风险 source 信号：

- 点击量高但 session 低。
- session 高但 CTA click 极低。
- CTA click 高但 approved / paid revenue 低。
- 某 source 的 refund、duplicate、bad geo、invalid phone、complaint 高。
- publisher/source 不透明，只能整体买包，不能停单点。
- 流量突然放大但 finalized revenue 或 buyer feedback 下调。

处理原则：

- 新 source 独立预算和 source id。
- 先白名单小测，再逐步扩量。
- 不可解释 source 先暂停，不用补点击或模拟自然访问“稀释”。
- 供应商拒绝提供 source 维度时，按高风险降级。

## 8. Offer 条款和 Buyer Feedback

Native 被允许，不代表任何 Native 做法都被允许。Offer 条款可能限制：

- Native / advertorial / presell 是否允许。
- 是否允许 brand bidding、direct linking、email、social、search、incent。
- 是否需要素材或页面预审。
- 是否禁止夸张 claim、before/after、fake news、survey/quiz、celebrity。
- 是否要求隐私政策、disclosure、lead consent。
- 是否按 qualified lead、approved lead、sale、first payment 结算。

Native 测试前要确认：

1. Advertiser / network 是否允许 presell page。
2. 页面 claim 是否需要预审。
3. 数据收集和 postback 是否符合 consent / privacy 要求。
4. Scrub、reject、refund、chargeback 原因是否可拿到。
5. 收入是否能按 source / creative / landing version 回传。

## 9. 报表和诊断

Native 诊断不要只看 CPC 和 CTR。

核心报表：

- Creative report：标题、图片、angle、CTR、CPC、session rate。
- Source / publisher report：cost、sessions、CTA click、CVR、paid revenue。
- Landing report：scroll、time on page、CTA click、bounce、ad density。
- Offer / postback report：submitted、approved、rejected、paid、refund、scrub。
- Finalized revenue：AdSense/GAM/AdX 场景必须等扣量和 finalization。
- Complaint / policy report：用户投诉、平台拒登、素材禁用、source 问题。

诊断矩阵：

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| CTR 高，session 低 | 误点、低质 source、加载慢 | 查 source、设备、页面速度 |
| Session 高，CTA 低 | 素材承诺和页面不一致 | 改 presell 内容和 CTA |
| CTA 高，approved 低 | lead 质量差或 claim 过宽 | 查 buyer feedback，降级 claim |
| Revenue 高，finalized 低 | 无效流量或广告位问题 | 隔离 source，等 finalized |
| 投诉上升 | 标题党、披露不足、敏感 claim | 停素材，重审 disclosure |

## 10. 系统落地

当前 V1 可用已有模块落地：

| 需求 | 当前页面 / 文档 |
| --- | --- |
| 记录 Offer 是否允许 Native / advertorial / presell | `/offers` 和 [Affiliate 尽调手册](affiliate_network_due_diligence.md) |
| 采集 presell page 和内容证据 | `/offers/<id>/crawl` |
| 审核素材 claim 和披露 | Claim 审核、[创意 Claim 审核手册](creative_claim_review_fact_checking.md) |
| 记录 source / publisher / creative 指标 | `/metrics/import` |
| 生成暂停、降预算、换素材建议 | `/optimization` |
| 记录误导、披露不足、低质 source 风险 | `/risk-audits` |
| 保存 FTC、Google、Native 平台来源 | `/sources` |

后续可新增表：

```text
native_campaign_sources
native_creative_angles
advertorial_page_reviews
presell_disclosure_checks
native_source_quality_daily
native_buyer_feedback_daily
native_policy_incidents
```

这些表只做素材、页面、source、披露和收入复盘，不生成误导素材、不模拟点击、不隐藏来源、不绕过平台审核。

## 11. QA 清单

- Native 平台、publisher、source、placement 维度可追踪。
- Offer 条款明确允许 Native / advertorial / presell。
- 页面不是低价值桥页或 MFA 堆页。
- 标题、图片、CTA 和页面内容一致。
- 广告、赞助、affiliate、佣金或商业关系披露清楚且靠近推荐/CTA。
- 用户评价、评分、专家、案例和数字 claim 有来源。
- 敏感垂类有额外资质、限制、风险和隐私披露。
- Click -> session -> CTA click -> conversion -> paid revenue 能按 source 对账。
- Buyer feedback、scrub、refund、chargeback 能反馈到 source 和 creative。
- 低质 source 可单点暂停，而不是只能整体买包。

## 12. 信息来源 URL

- FTC, Native Advertising: A Guide for Businesses: https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses
- FTC, Enforcement Policy Statement on Deceptively Formatted Advertisements: https://www.ftc.gov/legal-library/browse/commission-policy-statement-enforcement-policy-statement-deceptively-formatted-advertisements
- FTC, Disclosures 101 for Social Media Influencers: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- FTC, Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides
- eCFR, Endorsements and Testimonials in Advertising: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255
- Google Ads, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads, Editorial requirements: https://support.google.com/adspolicy/answer/6021546
- Google Ads, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Publisher Policies: https://support.google.com/publisherpolicies/answer/10437486
- Taboola Advertising Policies: https://www.taboola.com/policies/advertising-policies
- Outbrain Advertising Guidelines: https://www.outbrain.com/guidelines/advertising-guidelines/
