# 落地页素材抽取、Offer Intelligence 与创意 Brief 手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何从 Offer 页面、落地页、竞品页面和变现页面中抽取可用于广告创意、关键词、页面 QA 和政策审计的素材。目标是让 AI 创意生成建立在页面证据、真实承诺和合规边界上，而不是凭空编写夸张广告。

本文不提供绕过 robots、登录墙、付费墙、验证码、安全挑战、反爬系统、账号权限或平台审核的采集方法；不提供批量抓取个人数据、评价造假、虚假背书或误导性文案生成方法。

## 1. 为什么素材抽取重要

ADXKit 类产品强调“输入 Offer URL -> 采集标题、描述、用户评价 -> AI 生成广告创意”。这背后的真正价值不是爬页面本身，而是把落地页上的可证明信息变成广告资产：

- 用户问题：页面解决什么需求。
- 价值主张：价格、功能、节省、速度、保障、比较维度。
- 证据：评论、评分、案例、数据、认证、编辑说明。
- 风险：夸张承诺、敏感垂类、价格误导、官方关系误导。
- 转化路径：CTA、表单、Offer URL、隐私披露、下一步动作。

创意生成如果没有 evidence，就会倾向于泛化、夸张或编造，短期可能提高 CTR，长期会带来低 RPV、拒付、扣量、拒登和账号风险。

## 2. 可抽取字段

建议抽取字段：

| 字段 | 用途 | 风险检查 |
| --- | --- | --- |
| Title / meta description | 页面主题和广告相关性 | 标题是否和 Offer 一致 |
| H1 / H2 | 页面结构和用户意图 | 是否只是桥页或广告堆叠 |
| CTA texts | 用户下一步动作 | CTA 后是否到同主题 Offer |
| Price / value snippets | 价格、折扣、payout、费用、百分比 | 是否需要页面证据和地区限制 |
| Claim snippets | best、trusted、free、guarantee、save 等声明 | 是否有证据，是否夸张 |
| Proof / review snippets | 评价、评分、案例、用户数、认证 | 是否真实、可披露、可引用 |
| Form fields | lead 收集复杂度 | 是否收集敏感数据或缺隐私政策 |
| Disclosure links | privacy、terms、about、contact、advertising disclosure | 透明度和目的地体验 |
| External links | CTA、联盟链接、广告链接 | 是否存在桥页、隐藏跳转或不一致 |

本系统第一版将这些字段整理进 `LandingPage.raw_summary`，用于人工审核和规则创意生成，不保存个人身份信息。

## 3. Evidence-first Creative

广告文案应按“证据 -> 声明 -> 创意”生成：

```text
页面证据
-> 可验证声明
-> 广告 headline / description
-> 人工事实核查
-> 投放草稿
```

示例：

| 页面证据 | 可用文案方向 | 不应生成 |
| --- | --- | --- |
| 页面列出 5 个比较维度 | Compare plans by price, fit, features | Best guaranteed plan |
| 页面有明确 pricing table | Review pricing before you choose | Save 70% today |
| 页面有 editorial disclosure | Independent comparison guide | Official provider |
| 页面有 user reviews | Read user review signals | Thousands love it，除非页面确实证明 |
| 页面没有价格 | Learn cost factors | Lowest price |

原则：AI 可以改写、组合和压缩页面信息，但不能创造页面没有的认证、价格、收益、用户数、排名或官方关系。

## 4. Claim / Proof Matrix

每条强声明都要有证明：

| 声明类型 | 需要证据 | 高风险缺口 |
| --- | --- | --- |
| Best / top / #1 | 方法论、评测标准、时间、样本 | 没有排名依据 |
| Free | 免费范围、限制、是否需要付款 | 免费试用被写成完全免费 |
| Save / discount | 原价、折扣、时间、地区 | 虚构节省金额 |
| Guaranteed | 保证条款、例外、退款政策 | 绝对承诺 |
| Trusted / secure | 安全说明、认证、隐私政策 | 空泛可信声明 |
| Reviews / rating | 评论来源、数量、时间、披露 | 评价造假或不可验证 |
| Official / certified | 授权、认证、政府/品牌关系 | 冒充官方 |

如果页面有 claim 但没有 proof，创意生成只能使用弱表达，例如 “review options”、“compare factors”、“learn what to check”，不能使用强背书。

## 5. Review / Testimonial 边界

评价和用户证明是高价值素材，也是高风险素材：

- 必须真实、可验证。
- 需要清楚披露商业关系、赞助、affiliate 关系或激励。
- 不应选择性剪裁导致误导。
- 不应把个别体验写成普遍结果。
- 金融、健康、减重、收益、职业等敏感垂类更要保守。
- 不能自动生成假评价或虚构用户数。

Affiliate/评测页应把“编辑判断”“商业关系”“用户评价”“广告主声明”分开，不要混成一个看似客观的排序。

## 6. 表单与 Lead 风险

落地页或 Offer 页出现表单时，需要额外检查：

- 收集哪些字段：姓名、电话、邮箱、地址、收入、健康、信用、债务等。
- 是否有隐私政策和数据用途说明。
- 是否说明数据会分享给广告主、lead buyer 或合作方。
- CTA 是否清楚说明提交后会发生什么。
- 是否有 consent checkbox 或必要披露。
- 是否使用敏感信息做广告个性化、Customer Match 或再营销。

表单越深入，创意越不能夸张。低质量表单 lead 会在 buyer feedback、reject、scrub 和 chargeback 中体现。

## 7. 素材抽取工作流

推荐流程：

1. 录入 Offer：垂类、国家、payout、目标 URL、tracking URL、政策备注。
2. 采集落地页：title、description、H1/H2、word count、links、CTA、claim、proof、price、forms。
3. 做证据矩阵：每条 claim 是否有 proof。
4. 生成创意 brief：allowed claims、blocked claims、required disclosures、CTA path。
5. AI 生成 headline / description / keyword。
6. 人工事实核查：逐条回到页面证据。
7. 创建 campaign draft。
8. 导出 CSV / Scripts JSON。
9. 指标导入后复盘 CTR、RPV、CVR、reject、policy warning。

## 8. 常见事故

| 事故 | 表现 | 修复 |
| --- | --- | --- |
| AI 编出页面没有的折扣 | CTR 高但拒登或投诉 | 创意必须引用 price/proof snippets |
| 标题使用“official” | 触发 misrepresentation | 只有明确授权才可使用 |
| 把 comparison 写成排名 | 用户误导，扣量或拒付 | 写清评估维度和时间 |
| 用户评价不可验证 | FTC / 平台披露风险 | 添加来源、披露或不用评价 |
| CTA 和页面承诺不一致 | click 高、RPV 低 | 修 CTA path 和 Final URL |
| 表单收集敏感数据无披露 | 政策和隐私风险 | 补隐私、consent 和数据说明 |

## 9. 本系统落地

当前系统已经增强：

- `/offers/<id>/crawl` 会抽取 title、description、H1/H2、word count、link counts。
- 采集摘要增加 CTA texts、price/value snippets、claim snippets、proof/review snippets、form counts。
- 如果发现 claim 但 proof 弱，会写入 warning。
- 创意生成会把落地页摘要中的 claim/proof/CTA 作为上下文线索。
- Offer 详情页显示 `raw_summary`，供人工审核。

当前系统不做：

- 不爬登录墙、验证码、付费墙或反爬保护内容。
- 不采集个人身份信息。
- 不生成假评价、假评分、假价格、假认证。
- 不绕过 robots、IP 限制、安全挑战或平台权限。
- 不把敏感用户数据放进创意、URL、subid 或日志。

建议后续扩展：

- `landing_evidence` 表：claim_type、snippet、source_selector、risk_level。
- `creative_claim_map`：headline -> supporting_snippet。
- `review_disclosure_check`：评价来源、商业关系、激励披露。
- `form_privacy_check`：字段、敏感度、privacy/consent 状态。

## 10. QA 清单

| 检查项 | 放行标准 |
| --- | --- |
| 页面主题 | Title/H1/description 与 Offer 和广告承诺一致 |
| CTA | CTA 后的 Offer 或下一步动作可解释 |
| Claim | 强声明有页面证据 |
| Proof | 评价、评分、案例、认证可验证 |
| Price | 价格、折扣、免费范围有条件说明 |
| Form | 隐私政策、数据用途、consent 和敏感字段已审查 |
| Disclosure | affiliate / ads / editorial disclosure 清楚 |
| AI 创意 | 不新增页面没有的事实 |
| Risk | misrepresentation、sensitive vertical、destination risk 已审计 |

## 11. 信息来源 URL

- Google Ads, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads, Destination experience: https://support.google.com/adspolicy/answer/16427615
- Google Ads, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads, Text ad requirements: https://support.google.com/adspolicy/answer/6021630
- Google Ads, Editorial requirements: https://support.google.com/adspolicy/answer/6021546
- Google Search Central, Creating helpful content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central, Spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Google Search Quality Rater Guidelines: https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf
- FTC Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides
- FTC, Endorsements, influencers, and reviews: https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews
