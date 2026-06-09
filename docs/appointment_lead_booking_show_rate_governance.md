# Appointment Lead、Booking、Show Rate 与 No-show 治理手册

更新时间：2026-06-09

本文解释 CPL / Call Lead / Appointment Lead / Local Services / Healthcare / Dental / Legal / Home Services / B2B Demo 等场景里，如何治理 appointment lead、booking、calendar availability、confirmation、reminder、reschedule、cancel、no-show、show rate、buyer capacity、payout model、offline conversion value 和 Google Ads 出价信号。它承接 [Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)、[Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md)、[Lead Freshness、Aged Lead 与 Recontact Window 治理手册](lead_freshness_aged_recontact_governance.md) 和 [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md)，重点回答：为什么“预约成功”不是最终收入，如何把 booked、confirmed、showed、treated/sold、paid 拆开，如何防止 no-show、日历容量不足、虚假预约、重复预约和浅层转化污染投放。

本文不是法律意见，也不提供自动外呼、短信群发、伪造预约、补日历、模拟到场、伪造 CRM 阶段、Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做预约状态、日历容量、提醒合规、到场反馈、来源 URL、风险评分、建议、任务和人工审批。

## 1. 为什么 Appointment Lead 是 CPL 的高风险利润层

Appointment 模式看起来比 raw lead 更接近收入，但它有一条更长的漏斗：

```text
submitted
  -> contacted
  -> qualified
  -> booked
  -> confirmed
  -> showed
  -> treated / demo completed / job completed
  -> approved
  -> paid
```

任一环节断掉，广告端看起来“转化好”，收入端却会亏：

- 表单 lead 很多，但日历没有空位，用户无法预约。
- booked 很多，但 reminder 不到位，show rate 低。
- 用户约了不符合服务区、保险、预算或资格的时段。
- Buyer 按 showed appointment 付款，但系统把 booked 当 paid。
- 周末/夜间预约进入队列，工作日才处理，意图已经衰减。
- 一个用户重复预约多个 slot，报表里变成多条机会。
- Google Ads 学到“容易 booked 的低意图流量”，而不是能 show / paid 的流量。

因此，Appointment Lead 的优化目标不是 `booked_count`，而是：

```text
net appointment value =
  showed_rate
  * qualified_after_show_rate
  * paid_rate
  * payout
  - reminder_cost
  - no_show_cost
  - complaint_or_reschedule_cost
```

## 2. 原理解释：Booking 是承诺，不是收入

Booking 只是用户和 buyer 对某个时间窗口的初步承诺。它和可收款收入之间至少隔着：

| 层级 | 意义 | 风险 |
| --- | --- | --- |
| booking requested | 用户请求预约 | 未确认、slot 不可用 |
| booked | 日历生成预约 | 可能重复、低资格、不符合服务 |
| confirmed | 用户或 buyer 确认 | 提醒和取消仍可能发生 |
| showed | 用户到场/接入 demo/完成上门 | no-show、late cancel |
| completed | 服务、咨询、demo 或评估完成 | 未必 qualified |
| approved / paid | buyer 或 advertiser 承认可付费 | 退回、争议、延迟 |

所以系统必须把 booked、showed、completed、paid 拆开。把 booked 直接回传为 primary conversion，会让广告平台奖励“会约但不到场”的流量。

## 3. 核心对象地图

| 对象 | 含义 | 治理作用 |
| --- | --- | --- |
| appointment request | 用户提出预约意图 | submitted 和 booked 的中间层 |
| calendar slot | 可约时间、地点、服务、人员 | 决定是否能履约 |
| booking event | 成功生成预约 | 需要唯一键和状态机 |
| confirmation event | 用户/买方确认 | 降低 no-show |
| reminder event | 邮件、短信、电话或日历提醒 | 需要 consent 和频控 |
| reschedule event | 改期 | 影响 lead age 和 capacity |
| cancel event | 取消 | 进入 no-show / cancel 归因 |
| show event | 到场、接通 demo 或完成上门 | 更接近收入信号 |
| no-show event | 未到场或未接入 | 进入来源和创意质量反馈 |
| buyer calendar capacity | buyer 可接预约量 | 决定预算和排期 |
| appointment quality score | 预约质量评分 | 决定扩量、暂停或降权 |

## 4. Appointment 状态机

推荐状态：

```text
submitted
validated
eligible_for_booking
booking_requested
booked
confirmed
reminded
rescheduled
cancelled
no_show
showed
completed
approved
paid
returned
```

状态治理：

| 状态 | 是否正向信号 | 注意事项 |
| --- | --- | --- |
| booking_requested | 否 | 用户还没拿到真实 slot |
| booked | 中间信号 | 不等于 showed 或 paid |
| confirmed | 中间信号 | 可用于提醒效果分析 |
| rescheduled | 中性 | 多次 reschedule 可能是低意图 |
| cancelled | 负向或中性 | 区分用户取消、buyer 取消、不可服务 |
| no_show | 负向 | 回写 source、creative、slot、reminder |
| showed | 强正向 | 仍需看 completed / approved |
| paid | 最终正向 | 用于成熟价值校准 |

## 5. Calendar Capacity 和 Slot 质量

Appointment arbitrage 不只要 buyer capacity，还要 slot capacity：

| Slot 维度 | 风险 |
| --- | --- |
| 时间 | 夜间、周末、节假日 show rate 可能不同 |
| 距离 | 线下服务距离过远会 no-show |
| 服务类型 | 用户选的服务和 buyer 服务不匹配 |
| 人员/地点 | 特定医生、律师、技师、sales rep 可用性 |
| lead age | 新鲜 lead 更适合快速 slot |
| reminder channel | 没有短信/邮件 consent 会影响提醒 |
| preparation | 医疗、金融、B2B demo 可能需要资料准备 |

Calendar capacity 必须和广告预算联动：

```text
safe appointment spend =
  available qualified slots
  * expected show rate
  * expected paid value
  * safety factor
```

如果 slot 不足，正确动作是降预算、限时段、限来源、切换预约队列或暂停，而不是继续买 submitted lead。

## 6. Reminder、Confirmation 和 Consent

提醒能降低 no-show，但不能绕过 consent。不同渠道要拆开：

| 渠道 | 适用 | 风险 |
| --- | --- | --- |
| email reminder | 大多数预约 | CAN-SPAM、退订、低打开 |
| SMS reminder | 医疗、本地服务、demo | TCPA、opt-out、频率 |
| manual call | 高价值预约 | DNC/TCPA、录音披露 |
| calendar invite | B2B、在线咨询 | 隐私、时区、误发 |
| app / provider notification | 预约平台 | provider 条款和数据分享 |

提醒规则要记录：

```text
reminder_channel
consent_scope
send_time_relative_to_slot
timezone
template_version
opt_out_status
delivery_status
response_status
```

禁止：

- 用短信群发轰炸 no-show。
- 用户 opt-out 后继续提醒。
- 用自动语音或机器人通话规避人工边界。
- 把 reminder success 伪造成 showed 或 paid。

## 7. No-show、Cancel 和 Reschedule 归因

No-show 不是单一原因。建议按原因拆：

| 原因 | 可能修复 |
| --- | --- |
| bad fit | 改资格问题、服务区、保险/预算字段 |
| slot too far | 更近日期、更高优先级、日历容量 |
| weak intent | 修改创意、页面、CTA 和 source |
| reminder missing | 修 reminder workflow 和 consent |
| timezone mismatch | 修用户时区和日历显示 |
| buyer cancelled | 查 buyer capacity 和 staffing |
| duplicate booking | 去重和唯一键 |
| price surprise | 页面披露、估价和 buyer 话术 |
| service unavailable | 修 routing 和 calendar service mapping |

No-show 要回写到 source、keyword/query、creative angle、landing version、form version、buyer、slot type 和 reminder template。

## 8. Appointment Payout 和结算口径

合同必须写清：

```text
payout_event = booked | confirmed | showed | completed | paid
show_definition
late_cancel_definition
no_show_definition
reschedule_window
valid_slot_definition
duplicate_booking_window
calendar_capacity_commitment
return_window_days
evidence_required
```

常见价格风险：

| 模式 | 风险 |
| --- | --- |
| paid on booked | buyer 可能后续大量 clawback |
| paid on showed | 回传慢，但质量更好 |
| paid on completed consult | 样本少、延迟长 |
| bonus on sale / treatment | 对账复杂，归因争议 |

Appointment 的 safe CPC 必须用 showed/paid，而不是 booked：

```text
safe_cpc =
  payout
  * booked_rate
  * show_rate
  * paid_rate
  * safety_factor
  / click_to_lead_rate
```

## 9. Google Ads 与 Offline Conversion

建议把 appointment 阶段拆成不同信号：

| Conversion action | 用途 |
| --- | --- |
| appointment_request | secondary 或内部 |
| booked_appointment | early signal，谨慎使用 |
| confirmed_appointment | 中间质量 |
| showed_appointment | 更适合 primary 候选 |
| completed_consult / paid | 成熟价值回传 |
| no_show / cancel | 内部负向或 value adjustment |

不要把 no-show、cancel 或 buyer rejected 的 booking 留在正向 value 里。若后续 return、refund、clawback 或 no-show 修正了价值，应在内部净值模型或 conversion adjustment 流程里处理。

## 10. Booking Quality Score

建议评分：

```text
booking_quality_score =
  slot_fit                 15
  lead_age_fit             10
  qualification_fit        15
  reminder_integrity       10
  confirmation_rate        10
  show_rate                20
  paid_rate                10
  complaint_cancel_rate    10
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可小幅扩量 |
| 70-84 | 正常投放，抽样 QA |
| 55-69 | 限 source / slot / buyer |
| 35-54 | 暂停扩量，查 no-show |
| 0-34 | 暂停 booking flow，开事故 |

评分必须使用 mature feedback 校准。不能只看 booked conversion。

## 11. 常见事故和修复

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| booked 高，showed 低 | 提醒失败、低意图、slot 太远 | 查 reminder 和 slot age |
| confirmed 高，paid 低 | 资格问题不够、服务不匹配 | 查 buyer reject reason |
| 某 buyer no-show 高 | 地点远、容量差、话术差 | 降 routing weight |
| 某 creative no-show 高 | 过度承诺、误导价格/速度 | 回写 Angle Library |
| 周末预约差 | 用户时段意图弱或 buyer closed | dayparting / calendar |
| 重复预约多 | 去重失败或多表单入口 | 建唯一键和 duplicate window |
| Ads 学到低质 booking | booked 做 primary | 改 showed/paid value mapping |

## 12. 系统落地

当前 V1 已实现专门工作台 `/appointment-leads` 和数据表 `appointment_lead_reviews`，不是只停留在通用来源、任务或指标页面。它把预约套利里最容易被误判的 `booked -> showed -> paid` 链路落成一个人工评审对象：先输入 payout event、漏斗率、no-show/cancel、calendar capacity、reminder consent、buyer terms 和 offline mapping，再由系统计算 Booking Quality Score、expected value、safe CPC、safe appointment spend、risk_level、recommended_action 和 blockers。

| 行业动作 | 系统位置 |
| --- | --- |
| 保存预约平台、服务类型、buyer、payout event 和预约价值假设 | `/appointment-leads` |
| 计算 expected value per booking/click、safe CPC 和 safe appointment spend | `/appointment-leads` |
| 审查 calendar capacity、slot delay、timezone、reminder consent、buyer terms 和 offline mapping | `/appointment-leads` |
| 更新 triage、calendar_review、reminder_review、buyer_terms_review、test_ready、scale_ready、blocked 等内部状态 | `/appointment-leads/<id>/status`，写入 `/logs` |
| 保存预约平台、Calendar、buyer slot 来源资料 | `/sources` |
| 记录 no-show、cancel、duplicate、slot mismatch 事故 | `/risk-audits` |
| 用 safe CPC 和 source_score 调整机会评分 | `/calculators` |
| 导入 booked、confirmed、showed、paid 指标 | `/metrics/import` |
| 生成暂停 source、修 reminder、降预算建议 | `/optimization` |
| 创建 reminder QA、calendar capacity review 任务 | `/tasks` |

`appointment_lead_reviews` 的 V1 字段覆盖：

```text
buyer_name, vertical, service_type, geo, appointment_platform,
payout_event, payout_amount, estimated_cpc,
click_to_request, request_to_book, confirmation, show, completed, paid,
cancel, no_show, duplicate_booking, reschedule,
available_slots, expected_bookings, lead_age_hours, slot_delay_hours,
calendar_capacity_status, timezone_status, reminder_channel,
reminder_consent_status, confirmation_process_status, buyer_terms_status,
status_map, slot_policy, reminder_policy, no_show_reason_map,
conversion_mapping, quality evidence flags, score, risk_level,
recommended_action, expected_value_per_booking, expected_value_per_click,
safe_cpc, safe_appointment_spend, blockers, status, source_urls
```

建议后续拆分表：

```text
appointment_booking_events
appointment_status_history
appointment_slot_inventory
appointment_reminder_events
appointment_no_show_events
appointment_buyer_terms
appointment_quality_daily
calendar_capacity_snapshots
appointment_conversion_maps
```

核心字段：

```text
appointment_booking_events:
  appointment_id, lead_id, buyer_id, slot_start_at,
  slot_timezone, service_type, location_id, booking_status,
  confirmation_status, reminder_policy_id, source_url,
  reviewer, decision

appointment_no_show_events:
  appointment_id, no_show_reason, cancel_reason,
  lead_age_bucket, reminder_status, buyer_disposition,
  source_id, creative_angle, landing_version, action
```

系统不自动创建虚假预约、不自动外呼或群发短信、不伪造 showed/paid、不通过 Cookie 后台改 conversion action 或预算。

## 13. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI 看板 | 分 submitted、booked、confirmed、showed、paid、no-show |
| 自动优化 | 根据 show rate、slot capacity、no-show 生成降速建议 |
| 自动投放 | 生成 conversion signal QA 和预算草稿，不用 Cookie 后台 |
| 换链接 / routing | 只建议 calendar capacity、consent 和 buyer terms 允许的 buyer |
| 任务中心 | reminder QA、calendar capacity review、buyer no-show follow-up |
| 风险审计 | duplicate booking、slot mismatch、no-show、cancel、false booked |

完成标准：

- 能解释 booked、confirmed、showed、completed、paid 的差异。
- 能说明 no-show 为什么是 source / creative / slot / reminder 的联合结果。
- 能把 appointment calendar capacity 和预算节奏绑定。
- 能设计 showed/paid 优先的 offline conversion value mapping。
- 明确不交付自动外呼、短信群发、伪造预约、补到场、Cookie 后台操作或规避检测。

## 14. QA 清单

上线 appointment lead 流程前检查：

- 是否区分 booking requested、booked、confirmed、showed、paid。
- Calendar slot 是否有 timezone、service、location、buyer capacity。
- Buyer 合同是否定义 payout event、show、no-show、cancel 和 return window。
- Reminder 是否有 consent scope、template version、opt-out 和发送状态。
- No-show 是否能回写 source、creative、landing、buyer 和 slot type。
- 是否防止 duplicate booking 和重复回传。
- 是否把 booked 和 showed/paid 分开做 conversion action 或内部状态。
- 是否没有自动外呼、短信群发、伪造 showed、补预约或隐藏 cancel。

## 15. 信息来源 URL

- Google Calendar Help, Create an appointment schedule: https://support.google.com/calendar/answer/10729749
- Google Calendar Help, Learn about appointment schedules: https://support.google.com/calendar/answer/11608416
- Google Business Profile Help, Set up bookings through a provider: https://support.google.com/business/answer/7475773
- Reserve with Google: https://www.google.com/maps/reserve/
- Google Local Services Help: https://support.google.com/localservices/
- Google Local Services Ads, How leads work: https://support.google.com/localservices/answer/7195435
- Google Ads Help, Set up an ad schedule: https://support.google.com/google-ads/answer/6372656
- Google Ads Help, About call reporting: https://support.google.com/google-ads/answer/2454052
- Google Ads Help, Phone call conversion tracking: https://support.google.com/google-ads/answer/6100664
- Google Ads Help, Conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads API, Upload conversion adjustments: https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments
- Google Ads Help, Offline conversion import discrepancies and errors: https://support.google.com/google-ads/answer/13321563
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- Calendly, How to reduce no-shows with email and text reminders: https://calendly.com/blog/guide-calendly-reminders/
- Calendly, Reduce no-show rates in sales: https://calendly.com/blog/reduce-no-show-rates-sales
- Square Support, Set up Reserve with Google: https://squareup.com/help/us/en/article/6567-reserve-with-google
