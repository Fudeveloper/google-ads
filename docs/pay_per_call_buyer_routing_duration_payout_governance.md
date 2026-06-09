# Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册

更新时间：2026-06-09

本文解释 Pay-per-call / Call Lead / Local Services / Legal / Insurance / Healthcare / Home Services 等电话套利场景里，如何治理 call buyer、target、routing plan、IVR、call queue、buyer cap、hours、duplicate caller、qualified duration、payout/revenue、recording、complaint、buyer disposition 和 Google Ads 信号。它承接 [Call Tracking Number Pool、DNI 与电话归因治理手册](call_tracking_dni_number_pool_attribution_governance.md)、[Lead Pricing、Payout Negotiation 与结算安全垫治理手册](lead_pricing_payout_negotiation_governance.md)、[Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md) 和 [Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)，重点回答：为什么 qualified duration 只是计费门槛，不等于真实收入；call buyer routing 如何影响 payout、投诉和 Google Ads 学习；以及如何防止 missed call、重复 caller、错服务、IVR 放弃和短通话污染套利判断。

本文不是法律意见，也不提供补电话、模拟通话、循环拨打、机器人语音、伪造 duration、伪造 buyer disposition、绕过 DNC/TCPA/TSR、隐藏 caller identity、Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做 call routing 口径、buyer/target 条款、duration payout、cap/hours、重复 caller、recording/PII、对账、来源 URL、任务和人工审批。

## 1. 为什么 Pay-per-call 不是 Call Count 套利

Pay-per-call 的收入不是“来电数”，而是符合 buyer 条件的可计费电话：

```text
inbound call
  -> routed to eligible buyer
  -> answered / connected
  -> qualified duration or buyer qualification
  -> buyer accepts / disposition
  -> payout approved / paid
```

常见误判：

- Google Ads 显示 calls 增加，但 buyer 没接或未达到 duration。
- Duration 达标，但 buyer 判定 existing customer、wrong service、duplicate 或 low intent。
- 多个 buyer 都有 cap，但 routing 把高价值 caller 送到低价 buyer。
- IVR 问题导致 abandon，广告端仍看到 call start。
- Caller 重复拨打，系统重复计费或污染 campaign。
- Buyer 后续 scrub，但投放系统已经按 qualified duration 扩量。

Pay-per-call 的核心是 call routing + buyer payout + quality feedback，不是把电话时长做大。

## 2. 原理解释：Duration 是代理指标

Qualified duration 通常用于判断电话是否“足够长”，但它只是代理指标：

| 指标 | 能证明 | 不能证明 |
| --- | --- | --- |
| call connected | 有人接起 | 用户合格、buyer 可收款 |
| duration threshold | 通话达到门槛 | 服务匹配、成交、无投诉 |
| IVR completed | 用户走完菜单 | buyer 接通、销售合格 |
| buyer disposition | buyer 标注结果 | 一定已付款 |
| paid revenue | 可收款结果 | 未来不会有 dispute |

所以 Pay-per-call 优化应把 duration、buyer disposition、approved/paid、complaint 和 refund/scrub 连起来看。把 qualified duration 直接当最终收入，会让广告平台学习到“能拖长电话”的流量。

## 3. 核心对象地图

| 对象 | 含义 | 治理作用 |
| --- | --- | --- |
| call buyer | 购买合格电话的 buyer / advertiser | 决定 payout、hours、cap、qualification |
| target | 实际接听号码、队列、buyer endpoint | 决定 routing 和接通 |
| routing plan | waterfall、priority、auction、tag routing | 决定电话去哪 |
| call flow | IVR、menu、queue、recording、routing node | 决定 caller 体验和 drop-off |
| payout rule | duration、connected、disposition、sale | 决定可收款口径 |
| revenue rule | buyer 应付收入 | 和 publisher payout 区分 |
| duplicate caller rule | 重复来电窗口和处理 | 防止重复计费和污染 |
| buyer cap / hours | 可接电话数量和营业时间 | 决定预算和 dayparting |
| call disposition | buyer/agent 的真实结果 | 校准 duration |
| call dispute | buyer 扣量、拒付、投诉 | 进入证据包 |

## 4. Call Routing 模式

| 模式 | 原理 | 风险 |
| --- | --- | --- |
| Static target | 所有电话去一个 buyer | cap 满、hours closed 时浪费 |
| Waterfall | 顺序找可接 buyer | 前位 buyer 吃掉高质电话 |
| Priority routing | 按合同或质量优先 | 可能牺牲短期 payout |
| Revenue-based routing | 按预期 payout / EPC 选择 | 忽略投诉或 paid rate 会误导 |
| Tag / attribute routing | 按 geo、service、caller profile 选择 | 字段错误会错路由 |
| Split test routing | 分配给不同 buyer 测质量 | 样本和时间窗口要足够 |
| IVR-based routing | 用户按键或语音选择服务 | IVR 太长会 abandon |
| Cap-aware routing | 按 buyer cap、hours、capacity 调整 | cap snapshot 必须新鲜 |

Routing 不能只看最高 payout。有效 routing value：

```text
effective_call_value =
  payout
  * answer_rate
  * qualified_duration_rate
  * buyer_accept_rate
  * paid_rate
  - complaint_risk
  - duplicate_risk
  - missed_call_cost
```

## 5. Buyer / Target 条款

Pay-per-call buyer terms 至少保存：

```text
buyer_id
target_id
vertical
geo / service_area
hours_open
daily_call_cap
hourly_call_cap
duplicate_window_days
qualified_duration_seconds
billable_start_event
required_disposition
payout_amount
currency
return_window_days
recording_required
blocked_sources
evidence_required
```

必须区分：

- `revenue`：buyer 应付给平台/团队的钱。
- `payout`：支付给 publisher/source 的钱。
- `margin`：扣除 media cost、telephony cost、scrub reserve 后的净值。

如果 buyer 只按 `showed appointment` 或 `sale` 付款，duration 只能作为中间状态。

## 6. Duration Payout 和 Scrub

常见 duration 口径：

| 口径 | 风险 |
| --- | --- |
| 30s connected | 容易被短咨询、误拨、客服污染 |
| 60s / 90s qualified | 较稳，但仍非最终质量 |
| buyer disposition qualified | 更接近收入，但回传延迟 |
| sale / booked / paid | 最稳，但样本少、延迟长 |

常见 scrub reason：

| Reason | 含义 | 修复 |
| --- | --- | --- |
| duplicate caller | 重复来电 | caller hash + window |
| repeat within window | 同一用户短期重复 | 去重和 callback 识别 |
| wrong service | 服务不匹配 | query/landing/routing |
| wrong geo | 地区不服务 | geo filter |
| existing customer | 老客户 | 排除或单独计价 |
| short call | 未达阈值 | 不回传正向 |
| no buyer / missed | buyer 未接 | capacity 和 hours |
| complaint / DNC | 合规风险 | 暂停 source / buyer |

## 7. Duplicate Caller 和 Repeat Call

Pay-per-call 需要单独治理重复：

```text
caller_hash
first_call_time
last_call_time
duplicate_window
buyer_previously_routed
callback_flag
new_intent_flag
billable_flag
```

重复 caller 不一定无效：

- Callback 可能是同一个有效机会的后续沟通。
- 新服务请求可能可以重新计费。
- 售后或 existing customer 不应算新 lead。
- 同一 caller 在多个 buyer 间转卖容易产生投诉。

因此 duplicate rule 必须和 buyer terms、caller consent、service category 和 time window 绑定。

## 8. IVR、Call Flow 和 Caller Experience

IVR 能筛选服务类型，也能杀死利润：

| 节点 | 作用 | 风险 |
| --- | --- | --- |
| greeting | 披露和提示 | 太长导致 abandon |
| menu / gather | 收集服务意图 | 选项误导、无有效路径 |
| geo prompt | 确认地区 | 用户输入错误 |
| buyer lookup | 找可接 target | cap stale / no buyer |
| queue | 等待坐席 | abandon / missed |
| transfer | 转接 buyer | ring no answer |
| recording notice | 录音披露 | 过晚或不清楚 |

Call flow 要保存版本。任何 IVR 文案、按键、路由、队列、录音提示变更，都可能改变 call quality 和合规风险。

## 9. Recording、Compliance 和 Suppression

电话 buyer routing 必须遵守 consent、DNC、opt-out 和录音披露：

| 控制 | 要求 |
| --- | --- |
| caller identity | 不隐藏来电主体或 buyer |
| recording disclosure | 按地区和垂类保存版本 |
| DNC / opt-out | 联系前和投诉后同步 |
| sensitive vertical | 医疗、金融、法律更少保存原文录音 |
| PII minimization | caller phone hash，录音访问审计 |
| complaint response | 进入 risk audit 和 suppression sync |

不要用 IVR、预录音、AI 语音或自动化转接绕过用户同意和停止联系请求。

## 10. Google Ads 与 Pay-per-call 信号

建议拆信号：

| Signal | 用途 |
| --- | --- |
| call_asset_click | 诊断 |
| call_started | 诊断 |
| connected_call | 中间质量 |
| qualified_duration | 浅层优化候选 |
| buyer_qualified_call | 更适合 primary |
| booked_from_call | 强正向 |
| paid_call | 成熟价值 |
| duplicate / wrong_service / missed / complaint | 内部负向，不回传正向 |

原则：

- 不把 call click、short call、missed call、test call 设为 primary。
- Qualified duration 要用 buyer paid feedback 校准。
- Buyer scrub 后要调整内部 net value 或 conversion value。
- Call source、buyer、target、duration payout 和 final paid 必须可对账。

## 11. Call Buyer Quality Score

建议评分：

```text
call_buyer_quality_score =
  answer_rate                 15
  qualified_duration_rate     15
  buyer_accept_rate           15
  paid_rate                   20
  duplicate_scrub_rate        10
  complaint_rate              10
  cap_hours_freshness         10
  disposition_feedback_sla     5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可小幅增加 routing weight |
| 70-84 | 正常路由，继续监控 |
| 55-69 | 限量，查 scrub 和 missed |
| 35-54 | 降权或只保留人工审核 |
| 0-34 | 暂停 buyer/target，开事故 |

评分必须按 source、geo、hour、buyer、target、routing plan 拆分。平均值会掩盖某些 buyer 或时段的亏损。

## 12. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 call buyer、target、routing、payout 来源资料 | `/sources` |
| 记录 duplicate、missed、wrong service、complaint 事故 | `/risk-audits` |
| 用 safe CPC 和 source_score 降低机会评分 | `/calculators` |
| 导入 connected、qualified、buyer accepted、paid | `/metrics/import` |
| 生成降预算、换 buyer、修 IVR、降 routing weight 建议 | `/optimization` |
| 创建 buyer terms review、call routing QA、duration payout QA 任务 | `/tasks` |

建议后续表：

```text
call_buyer_accounts
call_targets
call_routing_plans
call_flow_versions
call_buyer_cap_snapshots
call_duration_payout_rules
call_duplicate_rules
call_buyer_disposition_events
call_buyer_quality_daily
call_dispute_cases
```

核心字段：

```text
call_duration_payout_rules:
  buyer_id, target_id, vertical, geo, duration_seconds,
  payout_amount, revenue_amount, duplicate_window_days,
  required_disposition, effective_from, source_url, reviewer

call_buyer_disposition_events:
  provider_call_id, buyer_id, target_id, caller_hash,
  duration_seconds, disposition, billable_flag,
  payout_amount, revenue_amount, reject_reason, evidence_ref
```

系统不自动拨号、不生成 synthetic calls、不伪造 duration、buyer disposition、recording 或 payout，只做 QA、建议、任务和审计。

## 13. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI 看板 | 展示 call started、connected、qualified、accepted、paid、duplicate、missed |
| 自动优化 | 根据 buyer quality、cap、hours、paid feedback 生成 routing 建议 |
| 自动投放 | 生成 call conversion QA 和预算草稿，不用 Cookie 后台 |
| 换链接 / routing | 只建议合规 buyer/target，保留人工审批 |
| 任务中心 | buyer terms review、routing QA、duration payout audit |
| 风险审计 | duplicate caller、duration scrub、IVR abandon、complaint、no buyer |

完成标准：

- 能解释 pay-per-call、call buyer、target、routing plan 和 duration payout。
- 能说明 qualified duration 为什么不是最终收入。
- 能治理 duplicate caller、buyer cap、hours、IVR abandon 和 missed call。
- 能把 buyer paid feedback 映射到 Google Ads 信号。
- 明确不交付补电话、模拟通话、机器人语音、伪造 disposition、Cookie 后台操作或规避检测。

## 14. QA 清单

上线 pay-per-call 流程前检查：

- Buyer/target 是否有 hours、cap、geo、service、duration 和 payout rule。
- Routing plan 是否处理 no buyer、cap full、hours closed 和 fallback。
- IVR / call flow 是否有版本、录音披露、abandon 监控。
- Duplicate caller 是否按 buyer terms、caller hash 和 window 处理。
- Qualified duration 是否和 buyer paid feedback 对齐。
- Missed、wrong service、existing customer、test call 是否不计正向收入。
- Payout、revenue、publisher payout 和 margin 是否分开。
- DNC、opt-out、suppression 和 complaint 是否能同步。
- 是否没有自动拨号、补电话、模拟通话或伪造 duration/disposition。

## 15. 信息来源 URL

- Google Ads Help, About call assets: https://support.google.com/google-ads/answer/2453991
- Google Ads Help, About call reporting: https://support.google.com/google-ads/answer/2454052
- Google Ads Help, Phone call conversion tracking: https://support.google.com/google-ads/answer/6100664
- Google Ads API, call_view fields: https://developers.google.com/google-ads/api/fields/v18/call_view
- Google Ads API, Conversion action categories: https://developers.google.com/google-ads/api/docs/conversions/categories
- Ringba Support, Call Flows with Ringba: https://support.ringba.com/hc/en-us/articles/17989801271703-Call-Flows-with-Ringba
- Ringba Support, Campaigns: https://support.ringba.com/hc/en-us/articles/17882602101783-Campaigns-Video
- Ringba Support, Targets: https://support.ringba.com/hc/en-us/articles/17882949857943-Targets-Video
- Ringba Support, Call Details Report Events Reference: https://support.ringba.com/hc/en-us/articles/33636912201751-Call-Details-Report-Events-Reference
- Retreaver, Pay Per Call Campaign Roadmap: https://retreaver.com/call-tracking/pay-per-call
- Retreaver, Introduction: https://learn.retreaver.com/guides/introduction
- Retreaver, Pay-Per-Call Features: https://learn.retreaver.com/guides/retreaver-pay-per-call-features-to-optimize-your-conversion-performance
- Invoca, Call Routing Software: https://www.invoca.com/product/call-routing
- CallRail Help, Dynamic number insertion overview: https://support.callrail.com/hc/en-us/articles/5711814948877-Dynamic-number-insertion-overview
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FTC, Protecting Personal Information: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
