# Affiliate Network / Lead Buyer 尽调与条款手册

更新时间：2026-06-08

本文说明 CPA/CPL/CPS/RevShare 套利中，如何评估 affiliate network、direct advertiser、lead buyer、Offer 条款、流量限制、扣量、拒付、cap、回款和披露义务。目标是让团队在买量前确认“这笔收入是否真实可收回”，而不是只看高 payout。本文不提供隐藏流量来源、冒充品牌、绕过 brand bidding 限制、伪造 lead、制造转化、Cookie stuffing、cloaking 或封禁后换号继续跑的方案。

## 1. 为什么网络尽调很关键

联盟套利的账面公式很简单：

```text
EPC = CVR * Payout
Profit per click = EPC - CPC
```

但真实可收款公式更复杂：

```text
Net EPC = CVR * Payout * approval_rate * (1 - deduction_rate)
Net profit = Net EPC - CPC - tracking_cost - cashflow_cost
```

如果网络或广告主条款不清楚，高 payout 可能只是陷阱：

- 月末统一 scrub，不解释原因。
- 禁止 Google Ads、brand bidding、native、incent，但投手没看清。
- Lead 先显示 pending，30 天后大比例 rejected。
- Cap 很小，扩量后超出部分不付。
- Payout 按国家、设备、质量等级变化，但报表没拆明细。
- 广告主要求隐藏来源或不允许第三方追踪。

## 2. 合作对象分层

| 对象 | 优点 | 风险 | 适合阶段 |
| --- | --- | --- | --- |
| Direct advertiser | 沟通直接、条款可谈、反馈快 | 合同和技术对接成本高 | 有稳定量和垂类经验 |
| Affiliate network | Offer 多、上手快、postback 标准化 | 扣量、条款复杂、信息经多层转述 | 冷启动和多 Offer 测试 |
| Lead buyer | 能给质量反馈、可做垂类深度 | 拒付规则严格、数据合规要求高 | CPL/本地服务/金融等 |
| Sub-network | 容易拿到 Offer | 透明度差、二手条款、付款链长 | 谨慎，只做小测 |
| White-label / reseller | 页面和品牌可包装 | 冒充、误导、主体不清风险 | 需强披露和授权证明 |

判断原则：层级越多，越要降低安全系数，要求更强的来源、结算和拒付证据。

## 3. Offer 条款清单

每个 Offer 进入测试前必须记录：

| 条款 | 需要确认 |
| --- | --- |
| Payout model | CPA / CPL / CPS / RevShare / hybrid |
| Payout value | 国家、设备、质量等级是否不同价 |
| Allowed traffic | Search、Social、Native、Display、Email、SEO、Direct buy |
| Prohibited traffic | Brand bidding、incent、pop、push、adult、toolbars、contextual、sub-network |
| Brand bidding | 是否允许 bidding on brand / misspelling / competitor |
| Creative restrictions | 是否允许自写文案、图片、比较、价格、折扣 |
| Landing page | 是否必须用官方页、预落地页、审批页 |
| Tracking | click_id、subid、postback、transaction_id |
| Conversion definition | submit、qualified lead、sale、first deposit、approved account |
| Approval window | pending 多久、何时变 approved |
| Rejection reasons | duplicate、invalid phone、bad geo、low intent、fraud、policy |
| Cap | daily/monthly cap、quality cap、source cap |
| Payment terms | net 7 / net 15 / net 30 / threshold / hold |
| Compliance | disclosures、privacy、consent、regulated vertical requirements |

没有这些信息，不进入放量。

## 4. 流量限制解读

常见限制：

| 限制 | 含义 | 风险 |
| --- | --- | --- |
| No brand bidding | 不可买广告主品牌词或近似词 | 违反会拒付或封号 |
| No competitor bidding | 不可买竞品品牌词 | 容易触发投诉和政策风险 |
| No incentivized traffic | 不可用奖励诱导用户提交 | Lead 质量和合规风险 |
| No pop / push | 不可用弹窗、推送来源 | 低质量点击和误导 |
| No social | 不允许社交买量 | 来源不匹配会拒付 |
| No native | 不允许内容推荐流量 | 标题党和低意图风险 |
| No sub-network | 不允许二级分发 | 来源不可控 |
| Pre-approval required | 素材/页面需先审批 | 未审批上线可能不付款 |

条款里的“allowed”不等于“所有方式都能放量”。例如允许 Search，不代表允许 brand bidding；允许 Native，不代表允许误导标题。

## 5. Payout、Cap 和 Scrub

关键概念：

- `gross conversions`：追踪系统看到的总转化。
- `pending conversions`：等待质量审核。
- `approved conversions`：确认可计费。
- `rejected conversions`：拒付。
- `scrub rate`：被广告主或网络扣掉的比例。
- `cap`：每日、每月或来源级别可接受转化上限。

公式：

```text
approval_rate = approved_conversions / gross_conversions
scrub_rate = rejected_conversions / gross_conversions
approved_revenue = approved_conversions * payout
```

放量前要知道：

- Cap 超了是否自动拒付。
- 周末/节假日是否暂停接收。
- 质量审核多久返回。
- 重复 lead 如何判定。
- 同手机号、同 email、同 household 是否算重复。
- rejected 是否提供 reason code。

## 6. Lead Quality

CPL 最容易出现“转化多但收不到钱”。

Lead 质量维度：

| 维度 | 好 lead | 差 lead |
| --- | --- | --- |
| 真实身份 | 电话/email 可联系 | 假号码、临时邮箱 |
| 意图 | 明确要咨询/报价/申请 | 被误导提交 |
| 地区 | 符合服务范围 | 不在服务范围 |
| 条件 | 符合年龄、收入、资质、需求 | 不符合基础条件 |
| 独占性 | 未重复卖给多家 | 重复、过期、二手 |
| 合规 | 有同意和隐私披露 | 未授权收集或转售 |

页面要避免：

- 暗示 guaranteed approval。
- 把广告伪装成官方机构。
- 隐藏价格、资格、限制和数据接收方。
- 为了提高 submit rate 省略关键说明。

## 7. Affiliate Disclosure

如果页面包含 affiliate link、推荐、评测、排名或佣金关系，用户应清楚知道团队可能获得佣金或商业利益。

披露原则：

- 清楚、明显、靠近相关内容。
- 不只藏在 footer 或 terms。
- 不用含糊词绕开，例如只写“合作伙伴”但不说明商业关系。
- 推荐、排名和评分方法要能解释。
- 不冒充广告主、官方、政府、银行、保险公司或认证机构。

披露不是“降低转化”的负担，而是降低 misrepresentation、用户投诉和长期账号风险。

## 8. 网络 / 广告主尽调问题

上线前问：

| 问题 | 合格回答 | 高风险回答 |
| --- | --- | --- |
| 你们是 direct advertiser 还是 network | 明确层级和付款方 | 不说明，或多层转包 |
| Offer 是否允许 Google Ads | 明确允许/禁止和限制 | “一般可以，别太明显” |
| 是否允许 brand bidding | 明确规则和品牌词清单 | 含糊，或让你自己试 |
| 是否要审核 landing/creative | 有审批流程和 SLA | 没有审批，但事后扣量 |
| 拒付原因如何返回 | 有 reason code 和样例 | 月底统一 scrub |
| Cap 如何处理 | 有 daily/monthly/source cap | 超 cap 后不说明 |
| Postback 字段 | click_id、payout、status、transaction_id 清楚 | 只给总数 |
| 回款 | payment term、threshold、hold 明确 | 拖款或条件不清 |
| 合规 | 有 privacy、consent、disclosure 要求 | 要求隐藏来源或主体 |

## 9. 合同和邮件确认模板

```text
Offer:
Advertiser / Network:
Country:
Payout model and value:
Allowed traffic:
Prohibited traffic:
Brand bidding:
Creative / landing approval:
Daily / monthly cap:
Approval window:
Rejection reason format:
Postback parameters:
Payment term:
Minimum payout threshold:
Compliance / disclosure requirements:

Please confirm that traffic from Google Ads Search with non-brand keywords,
pre-approved landing pages, and click_id/subid tracking is allowed.
```

把确认邮件、聊天记录、IO、terms、Offer screenshot 存档。未来扣量时，这些是复盘证据。

## 10. 测试和放量规则

冷启动：

- 先用单一国家、单一来源、单一页面版本。
- 每个 source/campaign/creative 有独立 subid。
- 不在第一天按 gross conversions 放量。
- 等待 approval window 后再调整安全系数。

放量条件：

- approval_rate 稳定。
- rejection reasons 可解释。
- source 和 creative 能定位质量差异。
- cap 有余量。
- 回款没有异常 hold。
- 页面和流量限制没有变更。

停量条件：

- rejected > 阈值且无法定位原因。
- 网络拒绝提供 reason code。
- 广告主反馈来源低质或违规。
- Offer 条款突然变化。
- 付款延迟或 hold 未解释。
- 要求隐藏来源、换号、绕过审核或 cloaking。

## 11. 系统落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer payout、限制、状态 | `/offers` |
| 用 payout、CVR、CPC、safety_factor 测算机会 | `/calculators` |
| 生成投放草稿和追踪 URL | `/campaigns` |
| 导入 conversions 和 revenue | `/metrics/import` |
| 根据 ROI 和低收入生成优化建议 | `/optimization` |
| 记录网络条款、邮件确认和来源 URL | `/sources`、`/risk-audits` |
| 记录回款、扣量、拒付复盘 | 现金流手册、风险审计、日志 |

V1 不实现：

- 联盟后台 Cookie 登录。
- 自动伪造 lead 或转化。
- Cookie stuffing。
- 隐藏来源或绕过 brand bidding 限制。
- 自动切换账号继续跑被拒 Offer。

## 12. 信息来源 URL

- FTC, The FTC's Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides
- FTC, Endorsements, Influencers, and Reviews: https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews
- FTC, Disclosures 101 for Social Media Influencers: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- FTC, Guides Concerning the Use of Endorsements and Testimonials in Advertising: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255
- Google Ads policies, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads policies, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads policies, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads policies, Financial products and services: https://support.google.com/adspolicy/answer/2464998
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Help, Use of online advertising to get new users to the site: https://support.google.com/adsense/answer/1348722
