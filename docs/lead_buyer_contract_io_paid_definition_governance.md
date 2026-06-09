# Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册

更新时间：2026-06-09

本文解释 CPL / CPA / Call Lead / Appointment Lead arbitrage 中，和 lead buyer、direct advertiser、affiliate network 或 lead marketplace 签约时，如何定义 accepted、qualified、billable、approved、paid、returned、scrub、return window、cap、exclusivity、reject reason、postback、invoice 和 dispute evidence。它承接 [Lead 质量、Postback 对账与拒付管理手册](lead_quality_postback_reconciliation.md)、[Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)、[Lead 验证、Suppression、去重与 PII 治理手册](lead_validation_suppression_pii_governance.md) 和 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)，重点回答：一条 lead 从被 buyer 接收到真正到账，中间每个状态怎么写进合同、系统和优化口径。

本文不是法律意见，也不提供伪造 lead、补提交、模拟电话、隐藏来源、绕过 buyer 风控、Cookie 后台操作、cloaking、规避账号封禁或规避平台检测的方案。系统只沉淀合同口径、来源 URL、QA、对账、证据包和人工审批。

## 1. 为什么 Buyer 合同口径决定 CPL 盈亏

CPL 套利最危险的错觉是：

```text
Google Ads conversion = revenue
buyer accepted = paid
lead submitted = billable
```

真实收入链路更长：

```text
Submitted lead
-> Validated lead
-> Posted / routed lead
-> Buyer accepted
-> Contact attempted
-> Contacted
-> Qualified
-> Billable / approved
-> Invoiced
-> Paid
-> Possible return / clawback
```

如果合同没有定义清楚，团队会出现这些亏损：

- Google Ads 学到大量 submitted lead，但 buyer 只付少数 qualified lead。
- Ping/Post 返回 accepted，月底却被 buyer 按 duplicate、bad geo、low intent、no contact 扣掉。
- Offer headline payout 很高，但 return window 长、scrub 不透明、payment term 慢。
- Call lead 只按短通话或 click-to-call 记转化，buyer 实际按 qualified call duration 或预约成功付款。
- Shared lead 被当成 exclusive lead 估值，导致投诉、重复和拒付。
- 没有 reason code、invoice、approval report 和 evidence pack，争议只能靠聊天记录。

合同口径不是法务后台杂事，而是投放算法、预算节奏、safe CPC、stop-loss 和现金流的基础输入。

## 2. 原理解释：接收、合格、可计费、已付款是四个不同事件

Lead buyer 合同的本质，是把同一条用户请求拆成四类事件：

| 事件 | 谁判断 | 典型含义 | 能否用于放量 |
| --- | --- | --- | --- |
| accepted | buyer/network 接口或运营 | buyer 初步接收，格式、cap、基础规则通过 | 只能说明能进入买方系统 |
| qualified | buyer 销售、审核或规则引擎 | 用户符合垂类、地区、需求、联系和资格标准 | 可以用于优化方向，但需看 approve rate |
| billable / approved | 合同或结算审核 | 达到可开票、可计费或可批准标准 | 可作为主要收入口径 |
| paid | 财务结算 | 发票付款到账，扣除 refund、credit、clawback | 扩量和现金预算的最终口径 |

因此同一条 lead 至少需要两个 ID：

```text
lead_id: 本系统或 CRM 内部 ID
buyer_lead_id / transaction_id: buyer 或 network 的交易 ID
```

并且至少保存这些时间：

```text
submitted_at
validated_at
posted_at
accepted_at
qualified_at
approved_at
invoiced_at
paid_at
returned_at
```

没有状态时间，就无法解释 conversion lag、buyer feedback lag、approval window 和 payment lag。没有交易 ID，就无法去重、对账和争议。

## 3. 核心对象地图

| 对象 | 作用 | 套利关注点 |
| --- | --- | --- |
| buyer master agreement | 长期合作主协议 | 数据使用、合规、付款、争议、保密、责任 |
| insertion order / campaign term | 单个 offer、垂类、地区、价格和周期 | payout、cap、source、qualification、return window |
| lead specification | 字段、格式、必填、PII、consent | 决定 accepted 和 rejected 的基础 |
| qualification rule | buyer 判断合格的业务规则 | 影响 paid EPC 和表单设计 |
| acceptance response | buyer 接口或人工接收结果 | 不等于 approved 或 paid |
| reject reason code | 退回、拒付、扣量原因 | 必须能按 source/subid 复盘 |
| return window | buyer 可退回 lead 的期限 | 决定收入成熟度和现金安全垫 |
| cap snapshot | buyer 当时的日/月/source cap 状态 | 解释 cap reached、no buyer、over cap |
| postback contract | 状态、金额、ID 和时间回传字段 | 连接 Ads、tracker、CRM 和 buyer report |
| invoice package | approved count、unit price、credit、tax、付款 | 财务确认收入 |
| dispute case | 对扣量、拒付、退款的证据流程 | 防止口头争议 |

## 4. Lead 状态机和定义

建议合同和系统统一使用以下状态：

| 状态 | 定义 | 常见证据 |
| --- | --- | --- |
| submitted | 用户提交表单、电话、聊天或预约请求 | landing log、form version、call log |
| validated | 通过格式、重复、geo、suppression、consent 检查 | validation report、consent version |
| posted | 已按合同发送给 buyer 或 marketplace | post request id、payload hash |
| accepted | buyer 接口返回 accepted 或人工接收 | buyer response、buyer_lead_id |
| rejected_initial | buyer 初始拒收 | reject reason、cap snapshot |
| contacted | buyer 完成有效联系尝试或接通 | call disposition、CRM status |
| qualified | 符合买方资格或通话质量标准 | qualification code、call duration、sales note |
| approved / billable | 买方确认可计费或进入结算 | approval report、invoice line |
| paid | 实际付款到账 | remittance、bank record、payment report |
| returned / scrubbed | 在 return window 内被退回或扣量 | return reason、credit memo |
| voided | 因错误、重复、撤回同意或合规问题作废 | audit note、privacy request |

关键原则：

- `accepted` 只能说明 lead 进入 buyer 系统，不代表质量通过。
- `qualified` 必须和合同规则对应，不应由投放团队随意改名。
- `approved` 和 `paid` 要区分，approved revenue 仍可能延迟、抵扣或追回。
- `returned` 必须保存原 approved 状态、退回时间、原因和金额。
- 禁止用重复 postback 或手工补 event 修饰状态。

## 5. 合同和 IO 必填条款

每个 lead buyer 合同或 IO 至少要写清：

| 条款 | 必填内容 | 为什么重要 |
| --- | --- | --- |
| parties | 收款方、付款方、buyer、network、processor | 多层合作时确定谁有付款责任 |
| vertical and offer | 垂类、产品、服务、地区、语言 | 防止 wrong service 和 bad geo |
| payout model | raw CPL、qualified CPL、pay-per-call、appointment、CPA、revshare | 决定优化目标 |
| unit price | payout、tier、geo/device/quality 价格 | 避免 headline payout 误算 |
| lead definition | submitted、accepted、qualified、billable、paid 的定义 | 避免状态混用 |
| lead fields | 必填字段、格式、PII、字段用途 | 降低 reject 和隐私风险 |
| consent and disclosure | 谁联系、渠道、分享对象、隐私政策、同意文本版本 | 支撑合规和投诉处理 |
| allowed traffic | Search、non-brand、native、email、social、direct buy 等 | 防止来源不符被拒付 |
| prohibited traffic | brand bidding、incent、bot、proxy、cloaking、sub-network 等 | 写入红线 |
| exclusivity | exclusive、shared、aged、recycled lead | 影响价格、投诉和重复 |
| cap and hours | daily/monthly cap、source cap、buyer hours、pause SLA | 防止超 cap 不付款 |
| return window | buyer 可退回 lead 的天数和条件 | 决定收入成熟期 |
| reject reasons | reason code、字段、例子、证据要求 | 支撑 source 复盘 |
| reporting | 日报、周报、月报、字段、时区、final report 日期 | 避免月底黑箱 scrub |
| postback | lead_id、transaction_id、status、payout、currency、timestamps | 支撑自动对账 |
| invoice and payment | net terms、threshold、invoice package、credit memo | 支撑现金流 |
| dispute | 争议窗口、证据包、回复 SLA、最终口径 | 防止无证据扣量 |
| data retention | 保存期限、删除、访问、PII 最小化 | 降低数据责任 |

如果 buyer 不愿意定义 accepted、qualified、approved 和 paid，只给“月底按质量结算”，这不是高 payout offer，而是高不确定性 offer。

## 6. Accepted 规则和初始拒收

accepted 通常由接口、ping/post、CRM 或买方运营系统判断。它回答的是：

```text
buyer 是否愿意把这条 lead 接进自己的处理队列？
```

常见 accepted 前置规则：

- 字段完整。
- phone/email 格式通过。
- geo 在服务范围内。
- service type 在 buyer 类目内。
- lead 未超过 cap。
- lead 不在 buyer duplicate window 内。
- consent/disclosure 文本符合 buyer 要求。
- source、landing page、creative 在已批准范围内。

常见初始拒收：

| 拒收 | 含义 | 系统动作 |
| --- | --- | --- |
| missing field | 必填字段缺失 | 修字段合同，不补造用户数据 |
| invalid format | 电话、邮箱、zip 格式错误 | 优化表单验证 |
| bad geo | 不在服务区 | 修广告 geo、页面说明和表单筛选 |
| wrong vertical | 服务类目不匹配 | 修关键词、广告承诺和表单选项 |
| cap reached | 当日/月/source cap 满 | 降预算或切到允许的替代 buyer |
| duplicate | buyer 去重窗口内重复 | 强化去重和 source 复盘 |
| source not approved | 流量来源不在合同允许范围 | 停止该 source，补审批 |

不要把 initial reject 隐藏起来。初始拒收是 buyer contract、form schema、campaign targeting 和 routing 的早期反馈。

## 7. Qualified 和 Billable 定义

qualified 是 buyer 的业务质量判断。不同垂类差异很大：

| 垂类 | 常见 qualified 条件 | 风险 |
| --- | --- | --- |
| Insurance | 服务州、年龄、coverage、有效电话、愿意报价 | 误导省钱承诺会带来投诉 |
| Debt / loan | debt range、state、income/credit eligibility、联系成功 | 金融披露和资格声明高风险 |
| Legal | case type、incident date、jurisdiction、未代理 | 不能承诺结果或冒充律所 |
| Local services | service area、job type、timeline、owner/decision maker | wrong service/area 会退单 |
| Education | program interest、location、age/education level、consent | 招生和联系频控敏感 |
| Healthcare | service type、location、合规许可、隐私边界 | 不应过度收集健康信息 |
| B2B | company size、role、budget、timeline、business email | low intent 和 fake business 信息 |

billable / approved 应写成明确规则，而不是“buyer determines quality at sole discretion”。

更可执行的写法：

```text
Billable lead means a unique lead that:
1. matches the approved vertical, geo, and service criteria;
2. contains the required fields listed in Schedule A;
3. includes the consent and disclosure text version approved in Schedule B;
4. is not a duplicate under the duplicate window in Schedule C;
5. is not returned within the return window for one of the allowed reason codes.
```

系统不需要替代律师起草合同，但必须把这些口径做成 checklist 和字段，而不是只存一个 payout 数字。

## 8. Return Window、Scrub 和 Clawback

return window 是 buyer 可以在一定时间内退回 lead、扣量或要求 credit 的期限。它通常来自：

- 无法联系。
- 电话虚假或错误。
- 重复 lead。
- bad geo / wrong service。
- 用户投诉未同意。
- 已经有服务商或已解决需求。
- buyer 认为低意图或被误导。
- 合同禁止来源或未审批素材。
- fraud / bot / synthetic lead。

合同要写清：

| 项目 | 建议口径 |
| --- | --- |
| window length | 例如 7、14、30 天，按 lead received 或 month end 计算 |
| allowed reasons | 只有列明 reason code 可退回 |
| evidence | buyer 需要提供何种 evidence 或 CRM disposition |
| dispute deadline | 发布方收到 return report 后多少天可争议 |
| credit method | 从当期 invoice 扣减、下期 credit、还是现金退款 |
| cap impact | returned lead 是否释放 cap |
| postback update | return 必须用同一 transaction_id 更新状态 |

scrub rate 的公式：

```text
scrub_rate = returned_or_rejected_leads / accepted_leads
net_paid_epc = payout * submitted_cvr * acceptance_rate * approval_rate * paid_rate
```

不要用 `accepted_leads * payout` 估算安全 CPC。要用成熟 cohort 的 approved / paid 口径。

## 9. Pricing Model 和优化目标

不同计价模式要求不同的优化目标：

| 模式 | 收入事件 | 优化时看什么 |
| --- | --- | --- |
| Raw CPL | submitted 或 accepted lead | validation、complaint、return window |
| Qualified CPL | buyer qualified lead | qualification rate、reject reason |
| Pay-per-call | qualified call | call duration、disposition、missed call |
| Appointment | scheduled 或 showed appointment | show rate、cancel rate、calendar capacity |
| CPA / sale | approved sale or account | sales lag、refund、chargeback |
| RevShare | net revenue share | cohort LTV、refund、clawback |
| Hybrid | base CPL + bonus | bonus definition、reporting lag |

套利团队不要把所有 offer 都折算成一个静态 payout。至少要保存：

```text
payout_model
headline_payout
expected_approval_rate
expected_paid_rate
expected_return_rate
payment_term_days
return_window_days
safe_cpc_factor
```

模型越靠后结算，越需要更长观察窗口和更低初始预算。

## 10. Exclusive、Shared、Aged 和 Recycled Lead

同一条 lead 的出售方式会改变价格和风险：

| 类型 | 含义 | 风险 |
| --- | --- | --- |
| exclusive | 只卖给一个 buyer | 价格高，但 consent 和 buyer fit 要更严格 |
| shared | 可卖给多个 buyer | 投诉、重复联系、buyer disclosure 更敏感 |
| aged | 过了一段时间再售卖 | 意图衰减、contact rate 下降 |
| recycled | 曾经拒收或未成交再处理 | 重复、投诉和合规风险更高 |
| appointment | 预约或咨询时段 | 坐席和 calendar capacity 影响付款 |

合同必须说明：

- 是否允许 shared lead。
- 最多分享给几个 buyer。
- 是否需要列明 buyer 或 buyer category。
- 用户是否知道会被多个服务商联系。
- buyer 是否允许 aged 或 recycled lead。
- duplicate window 如何跨 buyer 计算。

不要把 shared/aged/recycled 伪装成 exclusive；这通常会把短期 revenue 变成长周期投诉和拒付。

## 11. Postback、Reporting 和 Invoice 对账

最小 postback 字段：

```text
lead_id
buyer_lead_id
transaction_id
click_id / gclid / subid
status
reject_reason
payout
currency
event_time
status_updated_at
buyer_id
offer_id
```

日报字段：

```text
date
timezone
offer_id
buyer_id
source
campaign
landing_version
form_version
submitted
validated
posted
accepted
initial_rejected
qualified
approved
returned
paid
gross_revenue
approved_revenue
paid_revenue
reject_reason_breakdown
```

Invoice package 至少包含：

- invoice period。
- approved lead count。
- unit price / tier。
- returned lead count and amount。
- credit memo。
- tax / fees。
- payment term。
- remittance reference。
- final approval report。

Postback 是运营对账，不是财务付款证明。invoice 和 remittance 才能证明 paid。

## 12. Dispute Evidence 和扣量争议流程

争议流程：

```text
收到 return / scrub report
-> 锁定日期、时区、buyer、offer、source
-> 取出 lead_id / transaction_id 列表
-> 对照 consent、field schema、validation、cap、postback、call disposition
-> 分 reason code 判断是否符合合同
-> 生成 dispute evidence pack
-> 在争议窗口内提交 buyer
-> 记录 final resolution: accept return / reverse return / credit / policy fix
```

Evidence pack 包含：

- buyer contract、IO、terms、邮件确认和版本。
- lead spec、field schema、consent text hash、disclosure version。
- submitted_at、posted_at、accepted_at、returned_at。
- buyer response、postback、status history。
- validation result、duplicate check、suppression check。
- source、campaign、keyword、ad、landing page、form version。
- call log 或 CRM disposition，但不保存不必要录音和完整敏感内容。
- cap snapshot、buyer hours、routing decision。
- invoice、return report、credit memo、payment report。

原则：

- 能证明的争议才争议。
- 合同允许且证据充分的 return 要接受，并把原因回写优化。
- 不用伪造通话、补提交、改时间戳或重复 postback 解决扣量。
- 对不透明 scrub 的 buyer 降低评分，必要时停测。

## 13. Google Ads 与转化信号边界

Google Ads 优化不应该学习“最容易提交表单的人”，而应该尽量学习更接近真实可收款价值的状态。

建议：

| 状态 | Google Ads 用法 |
| --- | --- |
| submitted | 可作为 secondary 或观察指标 |
| accepted | 可用于 early signal，但不能直接等于 revenue |
| qualified | 更适合 primary，但要有去重和延迟窗口 |
| approved / billable | 高质量 primary conversion 候选 |
| paid | 适合 value feedback 和预算决策，但延迟长 |
| returned / rejected | 不上传为正向转化，作为内部负反馈 |

回传原则：

- 使用真实的 click ID、GCLID/GBRAID/WBRAID 或 enhanced conversions for leads 可支持的匹配方式。
- transaction_id 去重。
- conversion time 使用真实业务事件时间。
- conversion value 使用 expected、approved 或 paid 口径时要标明。
- 不通过 Cookie 后台操作导入虚假转化。
- 不把 rejected、short call、missed call、duplicate 或投诉 lead 当作正向主转化。

如果 buyer feedback lag 长，可以建立两层信号：

```text
early_qualified_signal: qualified probability
mature_paid_signal: approved / paid revenue after return window
```

早期信号用于冷启动方向，成熟信号用于扩量和安全 CPC。

## 14. 系统落地

当前 V1 可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 buyer 合同、来源、条款和 URL | `/sources` |
| 记录拒付、scrub、return、争议和合规风险 | `/risk-audits` |
| 在 Offer 中记录 payout、policy notes、restrictions | `/offers` |
| 用 approval/paid rate 调整 safe CPC | `/calculators` |
| 导入 accepted/approved/paid revenue 日报 | `/metrics/import` |
| 把低 paid rate、scrub、reject reason 转成优化建议 | `/optimization` |
| 创建合同复核、争议、暂停、回款任务 | `/tasks` |

建议后续表：

```text
lead_buyer_contracts
lead_buyer_ios
lead_buyer_offer_terms
lead_status_definitions
lead_return_windows
lead_reject_reason_codes
lead_buyer_cap_snapshots
lead_buyer_postback_events
lead_buyer_invoice_lines
lead_buyer_payment_receipts
lead_return_dispute_cases
```

核心字段示例：

```text
lead_buyer_ios:
  buyer_id, offer_id, vertical, geo, payout_model,
  unit_price, accepted_definition, qualified_definition,
  billable_definition, return_window_days, payment_terms,
  allowed_sources, prohibited_sources, exclusive_shared_policy,
  cap_rules, reporting_timezone, approved_by, status

lead_buyer_postback_events:
  lead_id, buyer_lead_id, transaction_id, status,
  status_reason, payout, currency, event_time,
  received_at, payload_hash, source_url, raw_payload_ref

lead_return_dispute_cases:
  buyer_id, io_id, lead_id, transaction_id, return_reason,
  amount_at_risk, evidence_window, dispute_deadline,
  status, final_resolution, owner, source_urls
```

系统不自动生成 lead、不补字段、不模拟联系、不自动争议、不绕过 buyer 风控，只做口径、审计、对账和人工任务。

## 15. ADXKit 对应点和完成形态

ADXKit 类工具常强调 ROI、自动优化、换链接和广告自动投放。Lead buyer 合同口径是这些功能的收入地基：

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI 看板 | 分开显示 submitted、accepted、qualified、approved、paid |
| 自动优化 | 根据 mature paid cohort、reject reason 和 return window 生成建议 |
| 换链接 | 只在 buyer/offer 条款允许、cap 可用、页面已审核时建议替代 |
| 创意生成 | Claim 和 CTA 必须匹配 buyer qualification 和 disclosure |
| 自动投放 | 使用 approved/paid signal 的人工审批草稿，不用 Cookie 后台 |
| 来源评分 | 把 source 的 scrub、return、complaint、paid rate 写入评分 |
| 任务中心 | 生成 invoice QA、return dispute、buyer feedback follow-up |

完成标准：

- 能解释 accepted、qualified、billable、approved、paid、returned 的区别。
- 能把 payout、return window、scrub、cap 和 payment term 放进 safe CPC。
- 能让 buyer report、postback、invoice 和 paid receipt 对上同一 transaction_id。
- 能把 reject reason 回写到 source、campaign、landing、form、creative。
- 明确不交付 Cookie 后台操作、伪造转化、补 lead、绕过审核或规避封禁。

## 16. QA 清单

签 buyer 合同或首投前检查：

- 是否定义 submitted、accepted、qualified、approved、paid。
- 是否明确 buyer 可退回 lead 的 reason code 和 return window。
- 是否定义 duplicate window、exclusive/shared/aged policy。
- 是否明确 payout model、unit price、tier、geo/device 差异。
- 是否明确 allowed traffic 和 prohibited traffic。
- 是否允许 Google Ads Search、non-brand、landing page 和 tracking 参数。
- 是否要求素材、landing、form、disclosure 或 consent 预审。
- 是否能按 source、campaign、landing、form version 返回 reject reason。
- 是否有 cap、buyer hours、pause SLA 和 cap exceeded 处理方式。
- 是否有 postback 字段、transaction_id、status update 和 payout。
- 是否有 reporting timezone、final report 日期和 invoice package。
- 是否有 dispute window、证据要求和回复 SLA。
- 是否把 paid revenue 而不是 accepted count 用于扩量。
- 是否把用户投诉、撤回同意、删除请求和 suppression 写进流程。

## 17. 信息来源 URL

- FTC, Follow the Lead workshop: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- FTC, Staff Perspective: Follow the Lead: https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf
- FTC, .com Disclosures: https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising
- FTC, Protecting Personal Information: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- eCFR, 16 CFR 310.5 Recordkeeping requirements: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5
- Google Ads, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Policy, Data collection and use: https://support.google.com/adspolicy/answer/6020956
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads Help, About enhanced conversions for leads: https://support.google.com/google-ads/answer/11021502
- TUNE, Offer Payouts and Caps: https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps
- TUNE Dev Hub, OfferConversionCap: https://developers.tune.com/network-models/offerconversioncap/
- Everflow API, Get Offer: https://developers.everflow.io/docs/affiliate/offers/
- Voluum, Conversion Status: https://doc.voluum.com/article/conversion-status
- Voluum, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
