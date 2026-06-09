# Buyer Capacity、Cap Pacing 与 Dayparting 治理手册

更新时间：2026-06-09

本文解释 CPL / Call Lead / Appointment Lead / Local Services arbitrage 中，如何把 buyer capacity、daily/monthly/source cap、buyer operating hours、call center capacity、holiday calendar、Google Ads ad schedule、average daily budget、overdelivery、conversion lag 和 time zone 放到同一套预算节奏里。它承接 [Offer Cap、Payout、状态变更与替代 Offer 治理手册](offer_cap_payout_status_governance.md)、[Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)、[预算节奏、扩量与止损手册](budget_pacing_scaling_stoploss.md) 和 [Geo、语言、本地化、时区与币种分层手册](geo_language_localization_currency.md)，重点回答：buyer 接不住量时，投放系统该如何降速、限时段、限来源、暂停或改 routing，而不是继续买点击制造 no buyer、missed call、cap reached 和低价 fallback。

本文不是法律意见，也不提供自动外呼、补电话、模拟通话、补 lead、绕过 DNC/TCPA、Cookie 后台操作、cloaking、使用代理/指纹伪装地区或封禁后换号的方案。系统只做 capacity 记录、cap pacing、dayparting QA、来源 URL、审计、建议和人工审批。

## 1. 为什么 Buyer Capacity 决定 CPL 扩量上限

套利团队经常把 Google Ads 预算当成唯一节奏器，但 CPL 收入端还有一层更硬的约束：

```text
buyer can receive
buyer can contact
buyer can qualify
buyer can pay
```

如果 buyer 或 call center 接不住量，会出现：

- Google Ads 继续买高意图点击，但 buyer daily cap 已满。
- Call asset 在营业时间外展示，missed call 和短通话上升。
- Buyer 只在本地时间工作，Google Ads 账号时区错配导致夜间烧预算。
- 午休、换班、周末、节假日没有坐席，submitted 高但 qualified 低。
- Ping/Post 返回 no buyer 或 cap reached，但 campaign 没有降预算。
- 高价 buyer cap 满后流量自动落到低价 buyer，平均 payout 崩。
- 自动出价把 submitted / call click 当信号，学习到 buyer 无法服务的时段。

因此，CPL 扩量不是“预算 +30%”这么简单，而是：

```text
max safe spend =
  min(
    media cash limit,
    buyer capacity value,
    call center capacity value,
    cap remaining value,
    qualified feedback value,
    policy and complaint guardrail
  )
```

## 2. 原理解释：买量节奏必须跟接量节奏同步

Google Ads 控制的是广告展示和花费；buyer capacity 控制的是 lead 能否变成可收款机会。两者不同步时，广告平台不会自动知道 buyer 已经关门、cap 已满、坐席不足或某时段 no answer 很高。

关键差异：

| 层级 | 控制对象 | 典型延迟 |
| --- | --- | --- |
| Google Ads budget | 点击、展示、日均预算、出价 | 快 |
| Ad schedule | 星期和小时展示资格 | 快，但按账号时区 |
| Lead submission | 表单/电话/聊天生成 | 快 |
| Buyer accept / reject | cap、geo、字段、source 规则 | 分钟到小时 |
| Contact disposition | connected、no answer、wrong number | 小时到天 |
| Qualified / approved | 买方质量审核 | 天到周 |
| Paid | 发票和付款 | 周到月 |

所以 dayparting 不能只看某小时 Google Ads conversions。必须把该小时对应 lead 的后续 accepted、contacted、qualified、approved、paid、returned 重新归因回来。

## 3. 核心对象地图

| 对象 | 解释 | 套利治理作用 |
| --- | --- | --- |
| buyer capacity profile | buyer 可接量、时区、营业时间、cap、SLA | 决定是否能买量 |
| cap snapshot | 某时刻 cap limit、used、remaining、reset time | 防止超 cap 买点击 |
| operating hours | buyer/call center 可联系时间 | 驱动 ad schedule 和 call schedule |
| call center shift | 坐席、班次、平均处理能力 | 判断每小时 lead 上限 |
| holiday calendar | 节假日、特殊关闭、缩短营业 | 防止假日烧预算 |
| ad schedule | Google Ads campaign 展示时段 | 需要和 buyer/user 时区对齐 |
| overdelivery exposure | 日均预算可能产生的超日节奏风险 | 设置内部 hard stop |
| no buyer event | 没有 buyer 可接收 | routing 和预算降速信号 |
| missed contact event | missed call、no answer、after hours | dayparting 和 staffing 信号 |
| capacity incident | cap 满、坐席不足、时区错配 | 进入 risk audit 和任务 |

## 4. Capacity Profile 设计

每个 buyer 或 buyer group 都要有 capacity profile：

```text
buyer_id
vertical
geo
timezone
operating_days
operating_hours
holiday_calendar
daily_lead_cap
monthly_lead_cap
source_cap
geo_cap
quality_cap
hourly_contact_capacity
first_attempt_sla_minutes
feedback_sla_hours
cap_reset_time
cap_update_frequency
status
evidence_url
reviewer
```

如果 buyer 没有提供实时 cap，也要保存最近一次确认时间：

```text
cap_last_confirmed_at
cap_confidence = fresh / stale / unknown
```

`unknown capacity` 不等于无限接量。未知 capacity 应降低预算、安全系数和 routing weight。

## 5. Cap 类型和 Reset 规则

Capacity 管理要区分：

| Cap | 作用 | 常见事故 |
| --- | --- | --- |
| daily buyer cap | buyer 每天最多接多少 lead | 下午已满，广告继续跑 |
| monthly cap | 月度合同或预算上限 | 月末突然全部 no buyer |
| source cap | 某 affiliate/source 上限 | 平均 cap 未满但某 source 超量 |
| geo cap | 州/城市/服务区上限 | bad geo 和 cap 混在一起 |
| hour cap | 某小时可接量 | 高峰冲垮坐席 |
| quality cap | 质量差触发软暂停 | 转化还在，但后续 scrub |
| call capacity | 可接电话或外呼数量 | missed call、no answer |
| appointment capacity | 日历可预约时段 | booked 多但 showed/paid 低 |

Reset 必须记录：

- reset timezone。
- reset hour。
- weekends / holiday 是否 reset。
- cap 是否按 accepted、qualified、approved 计算。
- returned lead 是否释放 cap。
- no buyer 是否进入 cap_used。

没有 reset 规则，就无法做 pacing。

## 6. Capacity Pacing 公式

基础公式：

```text
cap_usage_rate = cap_used / cap_limit
cap_remaining = cap_limit - cap_used
elapsed_day_ratio = elapsed_minutes_in_buyer_day / operating_minutes_today
projected_end_of_day_usage = cap_used / elapsed_day_ratio
```

Lead 预算上限：

```text
safe_leads_remaining =
  min(
    cap_remaining,
    hourly_contact_capacity_remaining,
    appointment_slots_remaining,
    source_quality_limit_remaining
  )

safe_media_spend_remaining =
  safe_leads_remaining
  * expected_paid_value_per_lead
  * safety_factor
```

触发动作：

| 条件 | 动作 |
| --- | --- |
| cap_usage_rate >= 70% | watch，不扩量 |
| cap_usage_rate >= 85% | 降预算，限制低质 source |
| projected_end_of_day_usage >= 100% | 停止新预算，准备合规 fallback |
| cap_remaining <= expected_next_hour_leads | 暂停或限时段 |
| cap_last_confirmed stale | 降低 safe spend |
| no buyer rate 上升 | 立即查 routing/cap |
| missed call rate 上升 | 查 hours、号码、坐席、call asset |
| after-hours lead 上升 | 修 ad schedule / call schedule |

## 7. Dayparting 的正确用法

Dayparting 应该回答：

```text
哪些时段的 paid value / cost 在 buyer 能服务的前提下更好？
```

而不是：

```text
哪个小时没有转化就关掉哪个小时？
```

可做 dayparting 的前提：

- 数据按 buyer/user/account timezone 对齐。
- 至少覆盖多个星期和主要营业日。
- 回传延迟已按 cohort 归因到 lead creation time。
- 有 accepted、contacted、qualified、approved 或 paid 口径。
- 时段差异不是追踪断点、页面故障、节假日或 cap 满造成。

常见 dayparting 矩阵：

| 时段类型 | 建议 |
| --- | --- |
| buyer open + high contact + high paid | 保留或小幅加预算 |
| buyer open + high submitted + low qualified | 检查意图和表单 |
| buyer closed + high call click | 关闭 call-heavy 投放或改表单预约 |
| lunch/shift gap + no answer 高 | 降出价或补 staffing |
| weekend + buyer 不接 | 限制预算或只跑低紧急度表单 |
| holiday + no disposition | 暂停或转预约等待队列 |

Google Ads ad schedule 按账号时区生效；跨地区投放时必须把目标用户和 buyer 时区折算回来。

## 8. Google Ads Budget、Overdelivery 和内部 Hard Stop

Google Ads 平均日预算不是团队的硬花费上限。Google Ads 帮助页说明，在某些高流量日，campaign spend 可能高于 average daily budget，并由月度限制约束。因此 CPL 团队需要平台外 hard stop：

```text
internal_hard_stop =
  min(
    daily_cash_loss_limit,
    buyer_capacity_value_limit,
    cap_remaining_value_limit,
    policy_incident_limit
  )
```

内部 hard stop 要看：

- served cost。
- billed cost。
- cap remaining。
- accepted / no buyer。
- missed call / after-hours。
- source quality。
- conversion lag。

不要在 buyer closed 或 cap unknown 时依赖 average daily budget 自然控速。

## 9. 时区和日界线治理

至少有四个时区：

| 时区 | 作用 |
| --- | --- |
| Google Ads account timezone | ad schedule、日报和预算 |
| user local timezone | 用户是否处于合理联系时间 |
| buyer timezone | cap reset、operating hours |
| call center timezone | 坐席班次和联系能力 |

字段建议：

```text
account_timezone
user_timezone
buyer_timezone
call_center_timezone
lead_created_at_utc
lead_created_at_buyer_local
cap_reset_at_buyer_local
ad_schedule_timezone_basis
```

事故示例：

- 账号时区是 UTC，buyer 是 America/New_York，广告晚间仍展示。
- 用户在 California，但 buyer 按 Eastern time 外呼，过早或过晚联系。
- Cap reset 按 buyer 本地时间，日报按 Ads 账号时间，导致“超 cap”错判。
- Dayparting 用 upload time，而不是 lead created time。

## 10. No Buyer、Fallback 和 Routing 降级

No buyer 是收入端断流信号，不是小噪音。

常见原因：

- cap reached。
- buyer closed。
- geo/service mismatch。
- source not approved。
- quality hold。
- shared/exclusive policy 不匹配。
- consent scope 不允许转给该 buyer。
- buyer API / CRM 故障。

动作：

| 原因 | 动作 |
| --- | --- |
| cap reached | 降预算或暂停，切已审核 buyer |
| buyer closed | dayparting 或预约队列 |
| source not approved | 停源，补审批 |
| quality hold | 降 source，等 buyer feedback |
| API failure | 暂停 post，保留 lead，不重复发送 |
| consent mismatch | 不转售，进入合规队列 |

Fallback 不能变成 cloaking 或未披露转售。替代 buyer 必须同主题、同用户意图、同 consent/disclosure 范围，并且已通过条款和页面审核。

## 11. Capacity Quality Score

建议评分：

```text
capacity_quality_score =
  cap_freshness              15
  hours_alignment            15
  contact_capacity_fit       20
  no_buyer_rate              15
  missed_contact_rate        10
  feedback_sla               10
  timezone_integrity          5
  holiday_readiness           5
  incident_history            5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可小幅扩量 |
| 70-84 | 保持预算，监控 cap |
| 55-69 | 限 source、限时段或降预算 |
| 35-54 | 暂停扩量，查 capacity |
| 0-34 | 暂停 buyer/routing，开事故 |

评分必须使用 mature feedback 校准。不能只看 buyer 口头说“还能接量”。

## 12. 事故诊断

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| spend 正常，accepted 突降 | cap 满、buyer API 故障、source 未批准 | 查 cap snapshot 和 buyer response |
| call clicks 高，connected 低 | 号码、营业时间、坐席不足、误点 | 查 call reporting 和 hours |
| submitted 高，no buyer 高 | routing 断、cap 满、geo mismatch | 暂停相关 source |
| 下午收入断崖 | daily cap 用完或换班缺口 | 降预算，查 pacing |
| 周末 paid 低 | buyer closed 或低质量 weekend intent | weekend dayparting |
| 某时段投诉高 | 联系时间不合适或 shared lead 频率高 | 查 user timezone 和 cadence |
| Google Ads conversions 好，paid 差 | shallow event 做 primary 或 after-hours lead | 改 signal 和 schedule |

事故复盘要保存：cap snapshot、buyer response、ad schedule、call reporting、Google Ads cost、lead timestamps、source/subid、timezone 和处理动作。

## 13. 系统落地

当前 V1 已实现专门工作台 `/buyer-capacity` 和数据表 `buyer_capacity_reviews`，不是只停留在通用来源、任务或指标页面。它把接量能力、cap pacing、时区、广告时段、holiday、no buyer、missed contact 和 fallback 统一成一个人工评审对象：先输入 cap、hours、expected lead、paid value、contact capacity、no buyer、missed contact、after-hours、证据状态和来源 URL，再由系统计算 Capacity Quality Score、projected usage、safe leads、safe media spend、risk_level、recommended_action 和 blockers。

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 buyer、cap、hours、timezone、ad schedule 和 fallback 策略 | `/buyer-capacity` |
| 计算 cap usage、projected usage、safe leads 和 safe media spend | `/buyer-capacity` |
| 审查 cap freshness、holiday、no buyer、missed contact、after-hours 和 cohort basis | `/buyer-capacity` |
| 更新 cap_refresh、hours_review、schedule_review、holiday_review、routing_review、reduce_budget、pause_traffic 等内部状态 | `/buyer-capacity/<id>/status`，写入 `/logs` |
| 保存 buyer hours、cap、capacity 来源 | `/sources` |
| 记录 cap 满、no buyer、after-hours、missed call 事故 | `/risk-audits` |
| 用 source_score 和 safety factor 降低机会评分 | `/calculators` |
| 导入每日成本、收入、accepted/paid 结果 | `/metrics/import` |
| 生成降预算、暂停、dayparting、capacity QA 建议 | `/optimization` |
| 创建 cap review、holiday check、buyer follow-up 任务 | `/tasks` |

`buyer_capacity_reviews` 的 V1 字段覆盖：

```text
buyer_name, vertical, geo,
buyer_timezone, account_timezone, user_timezone_scope, call_center_timezone,
cap_type, cap_period, cap_limit, cap_used, elapsed_operating_day_percent,
expected_next_hour_leads, expected_daily_leads,
hourly_contact_capacity, current_hour_capacity_used,
expected_paid_value_per_lead, accepted_rate, qualified_rate, paid_rate,
no_buyer_rate, missed_contact_rate, after_hours_lead_rate,
cap_last_confirmed_hours, feedback_sla_hours, first_attempt_sla_minutes,
cap_confidence_status, hours_alignment_status, ad_schedule_alignment_status,
timezone_alignment_status, holiday_readiness_status, fallback_status,
source_quality_status, overdelivery_guardrail_status,
operating_hours, cap_reset_rule, holiday_calendar, ad_schedule_summary,
no_buyer_reason_map, routing_fallback_policy, dayparting_basis,
evidence flags, score, risk_level, recommended_action,
cap_usage_percent, cap_remaining, projected_end_of_day_usage_percent,
safe_leads_remaining, safe_media_spend_remaining, blockers, status, source_urls
```

建议后续拆分表：

```text
buyer_capacity_profiles
buyer_operating_hours
buyer_holiday_calendars
buyer_cap_snapshots
buyer_capacity_pacing_daily
buyer_capacity_pacing_hourly
buyer_no_buyer_events
buyer_capacity_incidents
ad_schedule_alignment_reviews
capacity_quality_score_daily
```

核心字段：

```text
buyer_cap_snapshots:
  buyer_id, offer_id, cap_type, cap_scope, cap_limit,
  cap_used, cap_remaining, reset_at, timezone,
  retrieved_at, source_url, reviewer

ad_schedule_alignment_reviews:
  campaign_id, buyer_id, account_timezone, buyer_timezone,
  user_timezone_scope, ad_schedule_json, buyer_hours_json,
  mismatch_summary, decision, reviewer
```

系统不自动登录 Google Ads 或 buyer 后台，不自动改 schedule、预算或 routing，只生成 QA、建议、任务和审计记录。

## 14. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| 自动优化 | 根据 cap、hours、no buyer、missed call 生成降速建议 |
| ROI 看板 | 展示 spend、accepted、no buyer、capacity、paid 的时段视图 |
| 换链接 / routing | 只在 buyer capacity、consent、披露和条款允许时建议 fallback |
| 自动投放 | 生成 ad schedule / budget draft，不用 Cookie 后台 |
| 任务中心 | cap refresh、holiday check、buyer capacity follow-up |
| 风险审计 | after-hours spend、cap reached、stale cap、capacity incident |

完成标准：

- 能解释 buyer capacity、call center capacity、cap、hours 和 ad schedule 的关系。
- 能用 cap pacing 计算 safe spend remaining。
- 能说明 dayparting 为什么要按 paid/qualified cohort，而不是当天 conversions。
- 能处理 no buyer、cap reached、after-hours、missed call 和 stale cap。
- 明确不交付自动外呼、补 lead、Cookie 后台改预算、cloaking 或封禁规避。

## 15. QA 清单

上线 call-heavy 或 lead-heavy campaign 前检查：

- Buyer operating hours、call center hours、ad schedule 是否一致。
- Google Ads account timezone、buyer timezone、user timezone 是否映射。
- Daily/monthly/source/geo/hour cap 是否已记录。
- Cap reset 规则、reset timezone 和 cap update frequency 是否明确。
- Buyer/call center hourly capacity 是否支撑预算。
- Holiday calendar 是否已同步到 schedule。
- Call asset schedule 是否和 buyer hours 一致。
- No buyer、cap reached、missed call 是否能进入报表。
- Dayparting 是否基于 mature accepted/qualified/paid cohort。
- Internal hard stop 是否考虑 Google Ads overdelivery。
- Fallback buyer 是否同主题、已审核、consent/disclosure 允许。
- 是否没有自动拨号、补电话、模拟通话或绕过 DNC/TCPA。

## 16. 信息来源 URL

- Google Ads Help, Set up an ad schedule: https://support.google.com/google-ads/answer/6372656
- Google Ads Help, About ad scheduling: https://support.google.com/google-ads/answer/2404244
- Google Ads Help, About overdelivery and your average daily budget: https://support.google.com/google-ads/answer/1704443
- Google Ads Help, Budgets overview: https://support.google.com/google-ads/answer/10486536
- Google Ads Help, Budget report: https://support.google.com/google-ads/answer/10702522
- Google Ads Help, About bid adjustments: https://support.google.com/google-ads/answer/2732132
- Google Ads Help, About location targeting: https://support.google.com/google-ads/answer/1722043
- Google Ads Help, About call assets: https://support.google.com/google-ads/answer/2453991
- Google Ads Help, About call reporting: https://support.google.com/google-ads/answer/2454052
- Google Ads Help, Phone call conversion tracking: https://support.google.com/google-ads/answer/6100664
- Google Ads Help, Conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Time lag report: https://support.google.com/google-ads/answer/6239119
- Google Local Services Ads, Platform policies: https://support.google.com/localservices/answer/6224841
- Google Local Services Ads, How leads work: https://support.google.com/localservices/answer/7195435
- Google Ads API, Account budgets: https://developers.google.com/google-ads/api/docs/billing/account-budgets
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
