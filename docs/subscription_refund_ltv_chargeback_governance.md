# 订阅、试用、退款、Chargeback 与 LTV 治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何治理 subscription、free trial、intro offer、renewal、refund、chargeback、clawback、negative option、cancellation、cohort LTV 和 revenue quality。目标是把“首单转化”延伸到“真实可收回生命周期价值”，避免用高首单 payout、低价试用、pending revenue 或 gross LTV 做出价和扩量。本文不提供隐藏订阅条款、诱导误订、阻碍取消、伪造续费、规避 chargeback、隐藏退款政策、cloaking、补点击、伪造转化或 Cookie 后台操作方案。

## 1. 为什么首单 ROI 不等于真实 LTV

订阅、试用和连续付费类 Offer 的收入不是一次性事件：

```text
ad click
  -> trial signup / first order
  -> activation
  -> renewal
  -> refund / cancellation / chargeback
  -> net LTV
```

如果团队只看 trial signup 或 first purchase，容易误判：

- 免费/低价试用 CVR 很高，但续费率很低。
- 首月 payout 高，但退款和 chargeback 在 7-60 天后暴露。
- Google Ads conversion value 用 gross LTV，Smart Bidding 继续买低质量用户。
- 创意承诺“free / risk-free / cancel anytime”，页面披露和实际取消流程却不一致。
- Affiliate network 先记 pending，后续 advertiser 以质量、退款或投诉拒付。

订阅类套利必须用 cohort 看长期收入，而不是用首单转化看短期 ROI。

## 2. 原理解释：LTV 是收入曲线，不是固定数字

订阅 LTV 应按 cohort 计算：

```text
net_ltv =
  first_payment
  + renewal_revenue
  - refunds
  - chargebacks
  - clawbacks
  - payment_processing_cost
  - support_or_fulfillment_cost
```

如果只拿广告主给的 projected LTV 或 network payout 做模型，会忽略：

- 试用转正率。
- 第一次续费成功率。
- 月 1 / 月 2 / 月 3 留存。
- 退款和取消时间点。
- Chargeback 发生窗口。
- 客服和履约成本。
- 合规投诉导致的扣款。

正确模型是随时间成熟：

```text
Day 0: signup / first order
Day 7: trial conversion
Day 30: first renewal
Day 60: second renewal / refund window
Day 90+: stable retention or churn
```

## 3. 核心对象地图

| 对象 | 含义 | 套利治理重点 |
| --- | --- | --- |
| trial signup | 试用或低价首单 | 不等于长期收入 |
| activation | 用户真正使用或完成关键行为 | 预测留存质量 |
| renewal | 续费或再次扣款 | LTV 主要来源 |
| cancellation | 用户取消订阅 | 必须可解释且可记录 |
| refund | 商家主动退款 | 减少 net revenue |
| chargeback | 用户通过发卡行争议 | 风险高，可能引发账户和商户风控 |
| clawback | network/advertiser 追回佣金 | 影响 affiliate 收入 |
| cohort | 同一天/同周/同来源进入的用户组 | LTV 和退款曲线 |
| negative option | 用户不取消即继续收费的模式 | 必须强化披露和取消治理 |
| net LTV | 扣除退款、拒付、成本后的生命周期价值 | 出价和扩量依据 |

## 4. Trial / Subscription Funnel

建议把订阅漏斗拆开：

| 阶段 | 指标 | 风险 |
| --- | --- | --- |
| Click | CPC、query、source | 低意图、误导流量 |
| Signup | trial CVR、first payment | 被“免费/低价”吸引但无购买意图 |
| Activation | login、usage、setup complete | 用户不理解产品或价值 |
| Trial conversion | paid conversion rate | 试用结束前取消 |
| Renewal | month 1/2/3 retention | 首月后大量流失 |
| Refund | refund rate、reason | 价格/条款/功能不符 |
| Chargeback | dispute rate、reason | 账单描述不清、取消困难、误导 |
| Net LTV | cohort revenue minus losses | 真实可出价价值 |

投放优化不能停在 signup。至少要把 trial conversion、refund 和 chargeback 回写到来源、创意、query 和 landing version。

## 5. 披露、取消和退款边界

订阅、试用和 negative option 场景的核心合规要求是：用户要清楚知道自己什么时候、为什么、被谁、按多少钱收费，以及如何取消。

页面和流程应检查：

- 是否清楚展示价格、试用长度、续费金额和周期。
- 是否说明试用结束后会自动收费。
- 是否明确取消方式、取消截止时间和联系方式。
- 是否展示退款政策、资格限制和处理时间。
- CTA 文案是否和实际收费一致。
- 账单 descriptor 是否能让用户识别商家。
- 是否避免把重要限制藏在深层页面或小字里。
- 是否保留用户同意、订单、取消和退款记录。

这不是法律意见；团队应按目标国家、垂类、付款方式和广告平台要求让合规/法务确认。系统只做清单、证据和风险审计。

## 6. LTV Cohort 模型

建议按 cohort 保存：

```text
cohort_date, offer_id, campaign_id, source_id, country, device,
signups, activated_users, trial_converted,
renewal_m1, renewal_m2, renewal_m3,
gross_revenue, refunds, chargebacks, clawbacks,
net_revenue, ad_cost, net_ltv_per_user, paid_roi
```

核心公式：

```text
trial_to_paid_rate = paid_users / trial_signups
renewal_rate_m1 = renewal_m1 / paid_users
refund_rate = refunded_orders / paid_orders
chargeback_rate = chargebacks / paid_orders
net_ltv_per_signup = net_revenue / signups
safe_cpa = net_ltv_per_signup * safety_factor
```

不要用全局平均 LTV 决定所有来源。不同 source、query、creative、country、device 的 LTV 和退款曲线可能完全不同。

## 7. Refund、Chargeback、Clawback 分类

| 类型 | 常见原因 | 投放含义 |
| --- | --- | --- |
| duplicate billing | 用户认为重复扣款 | 账单和订阅状态需排查 |
| unclear renewal | 用户不知道会自动续费 | 页面披露或 CTA 有问题 |
| poor fit | 产品不符合广告承诺 | 创意/页面 claim 过强 |
| hard cancellation | 取消流程困难 | 高合规和平台风险 |
| bad source | 来源低意图或激励流量 | 降 source score 或停源 |
| payment fraud | 盗卡、异常支付 | 风控和流量质量问题 |
| network clawback | advertiser 追回佣金 | payout 不可收回，需要回写模型 |

退款不是单纯财务损失，它是流量、创意、页面、定价、产品匹配和合规的综合反馈。

## 8. Subscription Quality Score

建议给订阅 Offer 或 source 计算 `Subscription Quality Score`：

```text
subscription_quality_score =
  disclosure_clarity        20
  cancellation_access       15
  trial_to_paid_quality     15
  renewal_retention         15
  refund_chargeback_safety  15
  source_intent_quality     10
  billing_evidence           5
  complaint_history          5
```

动作建议：

| Score | 动作 |
| --- | --- |
| 85-100 | 可进入 Core 或 Scale 评审 |
| 70-84 | 可小幅扩量，继续观察 cohort |
| 55-69 | 只做 Test，等待续费和退款窗口 |
| 35-54 | 降预算，修披露、创意或 source |
| 0-34 | 停测或拒绝 |

## 9. 与 Smart Bidding 和转化回传的关系

订阅类 Offer 不应只把 signup 或 first payment 作为唯一 primary conversion。更合理的信号层级：

| 信号 | 用途 |
| --- | --- |
| trial_signup | secondary / 诊断 |
| first_payment | 冷启动 primary 候选，需折扣 |
| trial_to_paid | 自动出价候选 |
| renewal_m1 | 高质量价值信号 |
| net_ltv_30/60/90 | tROAS / LTV 出价候选 |
| refund/chargeback | 负向复盘，不作为正向 primary |

Value feedback 应使用 expected net LTV，而不是 gross projected LTV。退款、chargeback 和 clawback 要回写到 unit economics、source quality 和 creative feedback。

## 10. 常见事故

| 事故 | 表现 | 处理 |
| --- | --- | --- |
| signup 暴涨，续费差 | 创意吸引低意图试用 | 降预算，改 claim，等 cohort |
| refund 激增 | 页面承诺和产品不符 | 修披露/页面，暂停素材 |
| chargeback 上升 | 账单或取消争议 | 停 source，审取消流程和 descriptor |
| first payment ROI 好，90 天 LTV 差 | 留存质量差 | 降 safe CPA，改回传 value |
| network clawback | advertiser 追回佣金 | 更新 paid_rate，停违规来源 |
| 取消 query 变多 | 用户售后需求上升 | 检查产品匹配和支持页面 |

## 11. 系统落地

当前系统可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer、payout、政策和状态 | `/offers` |
| 用 safety factor、cash buffer、safe CPC 做测算 | `/calculators` |
| 导入 cost、conversions、revenue | `/metrics/import` |
| 记录退款、chargeback、clawback 事故 | `/risk-audits` |
| 保存 FTC、Google Ads、network 条款来源 | `/sources` |
| 用任务中心安排 cohort 复盘和月度关账 | `/tasks` |

后续可扩展表：

```text
subscription_offer_terms
subscription_cohort_daily
subscription_ltv_snapshots
refund_chargeback_events
cancellation_flow_audits
billing_disclosure_versions
ltv_value_feedback_runs
subscription_quality_decisions
```

字段示例：

```text
subscription_cohort_daily:
  cohort_date, offer_id, source_id, campaign_id,
  signups, first_payments, renewal_m1, renewal_m2, renewal_m3,
  refunds, chargebacks, clawbacks, gross_revenue,
  net_revenue, ad_cost, net_ltv_per_signup,
  refund_rate, chargeback_rate, decision
```

系统只做记录、评分、审计和回传建议，不自动隐藏条款、不阻碍取消、不伪造续费、不规避 chargeback。

## 12. ADXKit 对应点和完成形态

ADXKit 类工具如果只看短期 conversions，会高估订阅和试用 Offer。安全完成形态是把后端 LTV、退款和 chargeback 放入优化闭环。

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI dashboard | 同时展示 first payment、renewal、refund、chargeback、net LTV |
| 自动优化 | signup winner 必须等待 cohort LTV |
| AI 创意 | 禁止夸大 free、risk-free、cancel anytime 等无证据 claim |
| 自动投放 | 订阅 Offer 需要 disclosure QA 和 refund window |
| 任务中心 | 安排 30/60/90 天 LTV cohort 复盘 |
| 来源治理 | 高退款/高 chargeback source 降级或停源 |

功能拆解和安全完成清单：

- 完成 trial/subscription funnel、LTV cohort、refund/chargeback/clawback 原理解释。
- 完成披露、取消、退款、value feedback 和 Smart Bidding 信号边界。
- 完成系统落地、来源 URL、验收入口和 seed 来源。
- 不实现隐藏订阅条款、阻碍取消、伪造续费、规避 chargeback、cloaking、Cookie 后台操作或补点击。

## 13. QA 清单

- 价格、试用长度、续费周期和续费金额是否清楚。
- 自动续费和取消截止时间是否明确。
- 退款政策、限制和处理时间是否可见。
- CTA 是否与实际收费一致。
- Billing descriptor 是否可识别。
- 是否保留同意、订单、取消、退款和 dispute 证据。
- LTV 是否按 cohort、source、campaign、country、device 分层。
- Refund、chargeback、clawback 是否回写到 source quality 和 unit economics。
- Smart Bidding 是否没有把 trial signup 直接当长期 value。
- 高退款/高 chargeback source 是否进入 quarantine。
- 是否禁止隐藏取消入口、诱导误订或用换账号/换域名处理投诉。

## 14. 信息来源 URL

- FTC, Negative Option Rule: https://www.ftc.gov/legal-library/browse/rules/negative-option-rule
- FTC, Restore Online Shoppers' Confidence Act: https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act
- FTC, Enforcement Policy Statement Regarding Negative Option Marketing: https://www.ftc.gov/legal-library/browse/federal-register-notices/enforcement-policy-statement-regarding-negative-option-marketing
- FTC, .com Disclosures: https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising
- FTC, Advertising and Marketing on the Internet: https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Unacceptable business practices: https://support.google.com/adspolicy/answer/15938071
- Google Ads Policy, Editorial requirements: https://support.google.com/adspolicy/answer/6021546
- Google Ads Help, About conversion values: https://support.google.com/google-ads/answer/3419241
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
