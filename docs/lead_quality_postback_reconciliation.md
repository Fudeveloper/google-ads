# Lead 质量、Postback 对账与拒付管理手册

更新时间：2026-06-08

本文解释 CPA/CPL/Lead arbitrage 中“转化以后”的行业逻辑：一个表单、电话或咨询请求如何被记录、去重、分发、审核、回传、批准、拒付和结算。目标是帮助团队判断收入是否真实可收回，而不是只看 Google Ads conversions、联盟后台 pending conversions 或高 payout。本文不提供伪造 lead、Cookie stuffing、虚假表单、机器人提交、绕过买方风控、隐藏来源、cloaking 或封禁后换号的方案。

## 1. 为什么 Lead 质量是套利核心

CPL/CPA 套利的表面公式很简单：

```text
EPC = CVR * Payout
ROI = (Approved Revenue - Media Cost) / Media Cost
```

但真实经营里，`CVR * Payout` 只是报表第一层。最终能不能赚钱，取决于：

- Lead 是否真实、唯一、可联系。
- 用户是否理解自己提交了什么信息、谁会联系他。
- 来源是否符合 Offer 条款。
- 是否有 consent、privacy、disclosure 和数据使用说明。
- Buyer 是否能把 lead 变成下游销售或合格机会。
- 拒付原因能否按 source、campaign、keyword、landing page、subid 定位。

套利团队最容易犯的错误，是把“表单提交”当成“收入确认”。对 lead buyer 来说，表单提交只是质量审核的起点。

## 2. Lead 链路全流程

典型链路：

```text
Ad click
  -> Landing page
  -> Form / call / chat
  -> Validation
  -> Consent and disclosure record
  -> Ping / post / buyer routing
  -> Buyer accept or reject
  -> S2S postback
  -> Pending revenue
  -> Quality review
  -> Approved / rejected / scrubbed
  -> Invoice / payment / clawback
```

其中每一层都可能改变收入：

| 环节 | 关键问题 | 常见损失 |
| --- | --- | --- |
| Form | 用户是否真实表达兴趣 | 虚假、误导、低意图 lead |
| Validation | 电话、邮箱、地区、年龄、重复性是否合格 | invalid phone、duplicate、bad geo |
| Consent | 是否清楚说明谁会联系、用途和分享对象 | 投诉、合规拒付 |
| Routing | 卖给哪个 buyer、是否超过 cap | no buyer、cap reached、低价 buyer |
| Postback | click_id/subid/transaction_id 是否完整 | 丢转化、重复入账 |
| Quality review | Buyer 后台是否确认有效 | rejected、scrub、chargeback |
| Payment | net terms、发票和扣款 | 回款延迟、坏账 |

## 3. 线索质量分层

不要只看“提交数量”，要按质量漏斗看：

| 层级 | 说明 | 口径 |
| --- | --- | --- |
| Submitted lead | 用户提交表单或发起电话 | landing / CRM 原始记录 |
| Validated lead | 通过基础校验 | 非重复、电话/邮箱格式、地区、Offer 条件 |
| Accepted lead | 被 buyer 或 network 接收 | buyer accepted / initial postback |
| Qualified lead | 通过买方初审 | 可联系、有需求、符合资格 |
| Billable lead | 可计费或可开票 | approved / payable |
| Paid lead | 实际到账 | paid / finalized |

核心比率：

```text
Validation Rate = Validated Leads / Submitted Leads
Acceptance Rate = Accepted Leads / Validated Leads
Qualification Rate = Qualified Leads / Accepted Leads
Approval Rate = Approved Revenue / Pending Revenue
Paid Rate = Paid Revenue / Approved Revenue
```

投放优化应看 `Paid` 或至少 `Approved` 口径。只看 submitted 或 pending，会把低质量来源误判成高 ROI。

## 4. Postback 和对账原理

Postback 的作用，是让收入端把转化结果回传给追踪系统或买量系统。合格 postback 至少要能回答：

- 哪一次点击产生了这条 lead：`click_id`、`gclid`、`subid`。
- 哪个 Offer、buyer、campaign、landing page 产生了它。
- 金额是多少：`payout`、币种、是否 pending。
- 唯一交易是什么：`transaction_id` 或 `lead_id`。
- 什么时候发生：click time、lead time、postback time、approval time。
- 状态是什么：pending、accepted、qualified、approved、rejected、paid。

推荐字段：

| 字段 | 用途 |
| --- | --- |
| `click_id` | 点击级归因 |
| `subid1-source` | 来源、placement 或 publisher |
| `subid2-campaign` | Campaign / ad group / keyword |
| `subid3-landing` | Landing page version |
| `lead_id` | CRM 或 buyer 线索 ID |
| `transaction_id` | 去重和付款对账 |
| `payout` | 初始或批准金额 |
| `status` | pending/approved/rejected/paid |
| `reject_reason` | 重复、无效、低意图、地区、政策等 |

去重原则：

- 同一 `transaction_id` 不重复计收入。
- 同一 `lead_id` 的状态更新要覆盖而不是叠加。
- `pending` 到 `approved/rejected` 是状态迁移，不是新增转化。
- 不同平台时区不同，日报必须保留原始时间和归一化时间。

## 5. 拒付和 Scrub 原因

常见拒付原因：

| 类型 | 说明 | 排查方向 |
| --- | --- | --- |
| Duplicate | 用户重复提交或跨 publisher 重复 | 电话/email hash、buyer 去重窗口 |
| Invalid contact | 电话不通、邮箱无效、虚假姓名 | 表单验证、OTP、输入质量 |
| Bad geo | 国家、州、省、市不符合 Offer | geo 参数、页面语言、广告定位 |
| Low intent | 用户不知道自己提交给谁、需求弱 | 文案承诺、页面披露、表单问题 |
| Restricted source | 违反 no search、no brand、no incentivized 等条款 | source/subid 分段 |
| Policy issue | 敏感垂类、误导、资质、披露不足 | 页面和广告政策审计 |
| Fraud / bot | 自动提交、异常模式、虚假数据 | 流量来源、日志、风控 |
| Cap exceeded | 超过日 cap/月 cap 或 buyer 预算 | cap 监控、暂停规则 |

如果 network 或 buyer 只给总扣量，不给原因或无法按 subid 定位，应该降低该 Offer/source 的评分。无法解释的扣量不是“运营噪音”，而是放量风险。

## 6. Buyer Feedback 闭环

高质量套利团队会和 buyer 建立反馈字段，而不是只收一个 postback。

建议最小反馈：

- `accepted/rejected`。
- `reject_reason`。
- `contacted`：是否接通。
- `qualified`：是否符合资格。
- `sold/closed`：是否成交或进入销售机会。
- `refund/chargeback`：是否退款或追回。
- `quality_score`：buyer 内部评分。
- `buyer_comment`：可读说明。

反馈使用方式：

| 反馈 | 投放动作 |
| --- | --- |
| invalid phone 高 | 增加验证、减少低质来源、检查表单激励 |
| duplicate 高 | 排查重复曝光、跨渠道去重、限制再营销 |
| bad geo 高 | 修地理定向、页面国家说明、Offer 限制 |
| low intent 高 | 改广告承诺、加页面筛选问题 |
| no buyer/cap | 加 cap 监控或降低预算 |
| contacted 高但 qualified 低 | 调整关键词意图和表单筛选 |
| approved 高但 paid 慢 | 调整现金流安全系数 |

## 7. 表单、隐私和披露

Lead 不是普通点击，通常包含姓名、电话、邮箱、地址、财务、健康、教育或服务需求等个人信息。页面必须让用户理解：

- 谁在收集信息。
- 为什么收集。
- 会分享给谁。
- 谁会联系用户。
- 是否会有电话、短信、邮件或第三方服务商联系。
- 用户是否可以选择退出或撤回。
- 隐私政策、条款和联系方式在哪里。

敏感垂类要更谨慎，例如金融、医疗、法律、政府服务、教育、就业、住房和信贷。Google Ads Lead Form 要求广告主具备良好政策历史、合格垂类，并提供隐私政策链接；Google Ads customer data policies 也要求披露数据分享和在法律要求下取得同意。

## 8. 质量防线

上线前：

- Offer 条款写清允许来源、国家、设备、brand bidding、incent、cap 和拒付原因。
- Landing page 明确主体、服务、价格/费用、限制、隐私、第三方关系。
- 表单问题只收必要信息，不收无法保护或无法解释的敏感信息。
- 追踪字段能定位到 source、campaign、keyword、landing version。
- Buyer 能按 subid 返回拒付原因。

测试期：

- 每日看 submitted、validated、accepted、approved、rejected。
- 每日按 source/subid 看 reject reason。
- 出现异常拒付时暂停该 source，而不是靠补点击、换链接或换账号掩盖。
- 至少等一个审核/结算周期后再扩大预算。

放量期：

- 设 cap 和 pacing，避免超出 buyer 接收能力。
- 建立 quality score，不让高 volume 低 quality 来源吃掉预算。
- 对 buyer 反馈慢或拒付不透明的 Offer 降低安全系数。
- 保存 invoice、approval、reject report 和申诉证据。

## 9. 决策阈值

建议阈值：

| 指标 | 黄色预警 | 红色暂停 |
| --- | --- | --- |
| Duplicate rate | > 10% | > 20% |
| Invalid contact rate | > 15% | > 30% |
| Bad geo rate | > 5% | > 10% |
| Low intent rejection | > 15% | > 25% |
| Approval rate | < 75% | < 50% |
| Unexplained scrub | 任意出现 | 连续 2 个周期 |
| Buyer feedback delay | > 7 天 | > 14 天且无法解释 |
| Paid rate | < 90% approved | < 75% approved |

这些阈值不是固定法律或平台规则，而是运营风控起点。不同垂类应根据 payout、监管、回款周期和历史质量调整。

## 10. 系统落地

当前系统已经支持的部分：

| 业务动作 | 系统位置 |
| --- | --- |
| 记录 Offer payout、国家、限制、政策备注 | `/offers` |
| 按 payout、CVR、CPC 测算 EPC/ROI | `/calculators` |
| 生成投放草稿和 URL 参数 | `/campaigns` |
| 导入 cost、clicks、conversions、revenue | `/metrics/import` |
| 按 ROI、RPV、CPC、CTR、CVR 生成优化建议 | `/optimization` |
| 记录拒付、扣量、来源和政策依据 | `/risk-audits`、`/sources` |

后续可扩展但仍安全的能力：

- `lead_quality_daily` 表：source、campaign、offer、submitted、accepted、approved、rejected、paid。
- `lead_rejection_summary` 表：reject reason、count、amount、buyer、subid。
- CSV 导入 buyer feedback，而不是接收不透明黑箱。
- Quality score 进入 Offer 评分和预算建议。
- 审计页保存 invoice、reject report 和申诉证据链接。

不做：

- 不伪造 lead。
- 不自动提交表单。
- 不绕过 buyer 风控。
- 不隐藏或篡改 source/subid。
- 不用补点击或模拟自然流量修拒付。
- 不用 cloaking 或换号解决质量问题。

## 11. 信息来源 URL

- FTC, Follow the Lead: An FTC Workshop on Lead Generation: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- FTC, Staff Perspective: Follow the Lead: https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf
- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Policies, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policies, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads Policies, Financial products and services: https://support.google.com/adspolicy/answer/2464998
- Google Ads API, Manage offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Voluum Documentation, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
- FTC, Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides
- CFPB, Digital comparison-shopping circular: https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/
