# Call Tracking Number Pool、DNI 与电话归因治理手册

更新时间：2026-06-09

本文解释 CPL / Pay-per-call / Call Lead / Appointment Lead / Local Services / Legal / Insurance / Healthcare 等场景里，如何治理 call tracking number pool、Dynamic Number Insertion（DNI）、Google forwarding number、call asset、website call conversion、call duration、connected/missed call、unique caller、IVR、recording、CRM disposition、offline conversion import 和 buyer payout。它承接 [Lead Form、电话线索、Call Tracking 与 TCPA 风险手册](lead_form_call_tracking_tcpa_compliance.md)、[Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)、[Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md) 和 [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md)，重点回答：怎样把电话从“点击了电话按钮”拆到“真实来电、接通、合格、预约/成交、可收款”，而不是让短通话、错号、内部测试电话或归因重复污染广告出价。

本文不是法律意见，也不提供补电话、模拟通话、循环拨打、机器人语音、短信群发、绕过 DNC/TCPA/TSR、隐藏来电主体、Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做号码池配置记录、DNI QA、call log 对账、录音/隐私边界、call conversion mapping、来源 URL、风险评分、建议、任务和人工审批。

## 1. 为什么电话归因是套利利润层

Call-heavy arbitrage 的误区是把电话入口当成收入：

```text
call asset click
  -> phone dialed
  -> call connected
  -> sufficient duration
  -> qualified call
  -> booked / sold / paid
```

每一步都可能断：

- Call asset 点击后用户没有真正拨出。
- Google forwarding number 和第三方号码池同时存在，归因冲突。
- DNI 没有替换号码，手动拨号无法匹配 click。
- 号码池太小，多个访客看到同一号码，source/keyword 归因混淆。
- IVR 或转接链太长，missed call、abandon rate 上升。
- 通话时长达到阈值，但坐席判定 wrong service、existing customer 或 no sale。
- 录音没有披露或保存控制，纠纷时反而增加风险。
- Call conversion 被设成 primary，广告系统学习到短通话和误拨流量。

电话归因的目标是证明哪一批点击带来可收款电话，不是制造更多通话次数。

## 2. 原理解释：DNI 是号码到会话的映射

Dynamic Number Insertion 的核心原理是：用户进入页面时，脚本根据来源、campaign、click id、session 或 visitor，把页面上的业务号码替换成号码池中的一个 tracking number；来电发生时，call tracking 系统把 tracking number、call time、caller、session/click 信息、通话结果和 CRM 结果关联起来。

```text
ad click / source
  -> landing page session
  -> DNI assigns tracking number
  -> user calls tracking number
  -> call routes to business / buyer
  -> call log + session/click join
  -> disposition / paid feedback
```

DNI 不是：

- 不是隐藏真实业务主体。
- 不是规避 Google phone verification。
- 不是制造电话转化。
- 不是替代 consent、DNC、录音披露或 buyer feedback。
- 不是把所有来电都强行归因给 Google Ads。

## 3. 核心对象地图

| 对象 | 含义 | 治理作用 |
| --- | --- | --- |
| business number | 真实业务或 buyer 接听号码 | 主体一致和页面信任 |
| tracking number | 展示给用户的可归因号码 | 连接 call 和 source |
| number pool | 一组可动态分配号码 | 支撑 visitor/session 级归因 |
| DNI rule | 替换条件和范围 | 决定哪些来源替换号码 |
| Google forwarding number | Google Ads call reporting 使用的转接号码 | 支撑 call asset / call reporting |
| call asset | 广告内电话资产 | 广告层电话入口 |
| website call conversion | 网站上电话点击或号码来电转化 | 要区分 click 和 real call |
| call log | 来电时间、时长、状态、号码、录音 | 对账和质量判断 |
| call disposition | connected、qualified、wrong number、missed | 真实质量层 |
| offline conversion import | 把合格/成交电话回传 Ads | 替代 Cookie 后台操作 |

## 4. Google Forwarding Number vs 第三方号码池

| 方案 | 优点 | 风险 |
| --- | --- | --- |
| Google forwarding number | 原生 call reporting、call duration、call start time、call status | 与第三方 CRM/电话系统归因可能断开 |
| 第三方 DNI number pool | 可做 visitor/session/source/keyword 归因，能接 CRM disposition | 需要号码池容量、脚本 QA、PII 和录音治理 |
| Dedicated source number | 简单稳定，适合渠道级归因 | 粒度粗，不适合高流量关键词级归因 |
| Manual call click tracking | 容易部署 | 只代表点击，不代表真实来电或接通 |

常见冲突：

- 广告 call asset 使用 Google forwarding number，落地页使用第三方 DNI，两个系统各自有 call log。
- Call asset 的 tracking number 没有通过 Google phone verification。
- Google Ads 只知道 call asset call，CRM 只知道最终接听号码，缺 join key。
- 第三方号码池向 Google Ads 导入 offline conversion，但没有足够匹配字段。

治理原则：先选清楚“谁是电话事实源”，再决定哪些状态回传给 Ads。

## 5. Number Pool 容量和分配规则

号码池太小会造成归因污染。至少保存：

```text
pool_id
pool_type
source_scope
country / region
number_count
swap_rule
session_timeout_minutes
visitor_stickiness
subdomain_scope
fallback_number
business_destination_number
created_at
reviewer
```

容量判断：

| 场景 | 风险 |
| --- | --- |
| 并发访客超过号码池 | 多个用户共享号码，keyword/session 归因混乱 |
| session timeout 太短 | 用户稍后拨打时号码已分给别人 |
| timeout 太长 | 号码占用过久，池容量不足 |
| 多地区共用号码 | 本地信任、合规和服务区错误 |
| fallback number 未配置 | DNI 失败时页面号码不一致 |

号码池不是越大越好。要按流量、会话时长、电话延迟和归因粒度确定，并监控 pool exhaustion、swap failure、manual dial mismatch。

## 6. Call Log Join Key

电话归因要能把这些表连起来：

```text
ad click
web session
DNI assignment
call log
CRM / buyer disposition
invoice / paid feedback
```

推荐 join keys：

| Key | 说明 |
| --- | --- |
| gclid / wbraid / gbraid / click_id | Ads 点击来源 |
| session_id / visitor_id | DNI 分配上下文 |
| tracking_number | 用户拨打号码 |
| destination_number | 实际接听号码 |
| call_start_time + timezone | 电话事实时间 |
| caller_hash | 去重和 repeat caller |
| call_id / provider_call_id | 电话系统唯一键 |
| campaign/ad_group/keyword/source/subid | 运营维度 |
| CRM lead_id / buyer_call_id | 后续 disposition |

注意：

- Caller phone 属于 PII，应 hash 或受控保存。
- 不要把完整 phone 写进 URL、UTM、subid、日志标题或 prompt。
- 时间戳必须带 timezone，避免 Google Ads、CRM、电话系统日报错位。
- 重复来电要区分 repeat caller、callback、new opportunity。

## 7. Call Disposition Taxonomy

不要只保存 `duration_seconds`。推荐状态：

| Disposition | 含义 | 信号处理 |
| --- | --- | --- |
| connected | 接通 | 中间信号 |
| qualified_duration | 达到时长阈值 | 浅层正向 |
| sales_qualified | 坐席确认合格 | 强正向 |
| booked | 预约或派单 | 强正向 |
| sold / paid | 可收款 | 最终正向 |
| missed | 未接 | 负向，查 capacity |
| abandoned | IVR/排队中放弃 | 负向，查队列 |
| wrong_number | 错号 | 负向，查页面/素材 |
| wrong_service | 服务不匹配 | 负向，查 query/landing |
| existing_customer | 老客户 | 不应算新 lead |
| spam / test | 垃圾或内部测试 | 排除 |
| complaint / dnc | 投诉或停止联系 | 事故和 suppression |

Call duration 只是代理指标。不同垂类阈值不同，且长通话也可能是投诉、客服或错误服务。

## 8. IVR、转接链和 Missed Call

Call tracking 常见事故不在广告，而在电话链路：

```text
tracking number
  -> provider routing
  -> IVR
  -> queue
  -> buyer / call center
  -> CRM disposition
```

要记录：

```text
ivr_path
queue_id
destination_number
forwarding_steps
ring_duration
answer_status
abandon_time
recording_status
agent_id / buyer_id
```

事故例子：

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| Google Ads calls 高，CRM calls 低 | GFN 与第三方系统断开 | 对账 call_start_time 和 destination |
| clicks 高，calls 低 | call click tracking，不是真实 call | 改 call conversion |
| calls 高，missed 高 | capacity、routing、IVR、营业时间 | 降预算和修路由 |
| duration 高，paid 低 | 错服务、投诉、客服电话 | 查 disposition |
| number swap 失败 | DNI 脚本、CMP、缓存、SPA、号码池 | 前端 QA |
| 重复 caller 高 | 再营销、售后、老客户 | 去重和排除 |

## 9. Call Recording、PII 和合规边界

录音是 QA 和争议证据，但也是高风险数据。

必须记录：

```text
recording_enabled
recording_disclosure_version
jurisdiction_basis
recording_consent_status
recording_retention_days
recording_access_policy
redaction_status
deletion_request_status
```

原则：

- 先确认电话、短信、自动拨号、预录音和录音披露规则。
- 敏感垂类不要把健康、金融、法律、身份信息进入不必要报表。
- 录音文件不要默认进入 AI prompt、普通日志或公开任务。
- 只保存 QA 结论和必要引用，访问录音要审计。
- 投诉、opt-out、DNC 后同步 suppression。

## 10. Google Ads Call Conversion Mapping

建议拆 conversion action：

| Conversion action | 用途 |
| --- | --- |
| call_asset_click | secondary 或仅诊断 |
| call_started | 内部诊断 |
| connected_call | 中间质量 |
| qualified_duration | 浅层 primary 候选 |
| sales_qualified_call | 更适合 primary |
| booked_from_call | 强正向 |
| paid_call | 成熟价值 |
| missed / wrong_service / complaint | 内部负向，不做正向回传 |

回传原则：

- 不把 call click 当 payable lead。
- 不把 missed call、short call、wrong number、internal test 计为正向。
- 对 CRM 后续 confirmed/paid 的电话，可以用 offline conversions 或内部净值模型。
- 若后续 no-show、refund、returned，应通过 adjustment 或内部 value 修正。
- Primary conversion 应和 buyer 付款口径一致，至少要用 mature feedback 校准。

## 11. Call Attribution Quality Score

建议评分：

```text
call_attribution_quality_score =
  number_pool_integrity       15
  dni_swap_accuracy           15
  click_call_join_rate        15
  call_disposition_freshness  15
  qualified_call_rate         15
  missed_call_rate_guardrail  10
  pii_recording_controls      10
  offline_value_integrity      5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可小幅扩量 |
| 70-84 | 正常投放，抽样 QA |
| 55-69 | 限 source / keyword / hour |
| 35-54 | 暂停扩量，查号码池和 routing |
| 0-34 | 暂停 call-heavy campaign，开事故 |

评分必须用 paid / rejected / complaint 反校准，不能只看 call count。

## 12. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 call tracking / DNI / GFN 来源资料 | `/sources` |
| 记录 missed call、wrong number、DNI mismatch 事故 | `/risk-audits` |
| 用 safe CPC 和 source_score 调整机会评分 | `/calculators` |
| 导入 calls、qualified calls、booked、paid | `/metrics/import` |
| 生成降预算、修号码池、修 conversion mapping 建议 | `/optimization` |
| 创建 DNI QA、phone verification、call log reconciliation 任务 | `/tasks` |

建议后续表：

```text
call_tracking_number_pools
call_tracking_numbers
dni_assignment_events
call_log_events
call_disposition_events
call_recording_reviews
call_attribution_reconciliations
call_conversion_maps
call_quality_daily
```

核心字段：

```text
dni_assignment_events:
  session_id, click_id, source, campaign_id, keyword,
  tracking_number_hash, assigned_at, expires_at,
  pool_id, landing_url, swap_status, reviewer

call_log_events:
  provider_call_id, tracking_number_hash, caller_hash,
  destination_number_hash, call_start_at, timezone,
  duration_seconds, connected_status, recording_status,
  disposition, crm_lead_id, buyer_id
```

系统不自动拨打电话、不制造 call duration、不伪造录音或 disposition、不通过 Cookie 后台改 conversion action，只生成 QA、建议、任务和审计记录。

## 13. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI 看板 | 分 call click、connected、qualified、booked、paid、missed、complaint |
| 自动优化 | 根据 missed call、qualified call、paid feedback 生成降速建议 |
| 自动投放 | 生成 call conversion QA 和预算草稿，不用 Cookie 后台 |
| 换链接 / routing | 只建议有 capacity、consent 和号码归因证据的 buyer |
| 任务中心 | DNI QA、number pool review、phone verification、call log reconciliation |
| 风险审计 | number swap failed、GFN mismatch、short call primary、recording issue |

完成标准：

- 能解释 Google forwarding number、第三方 DNI、号码池和 call asset 的差异。
- 能说明 call click、connected call、qualified duration、sales qualified call、paid call 的关系。
- 能设计 call log join key 和 offline conversion mapping。
- 能识别 DNI 失败、号码池不足、IVR/转接和 missed call 事故。
- 明确不交付补电话、模拟通话、机器人语音、Cookie 后台操作或规避检测。

## 14. QA 清单

上线 call-heavy campaign 前检查：

- Call asset、landing page、business number、tracking number 是否主体一致。
- Google forwarding number 与第三方 DNI 是否会造成归因冲突。
- 号码池容量是否匹配并发访客、session timeout 和拨打延迟。
- DNI 是否在移动端、SPA、缓存、CMP、跨子域环境正常替换。
- Call conversion 是否区分 click、connected、qualified、booked、paid。
- Call log 是否有 provider_call_id、timezone、duration、disposition 和 CRM ID。
- Missed、wrong number、existing customer、test call 是否排除正向 conversion。
- 录音披露、保留期、访问控制和删除流程是否明确。
- 电话和短信是否检查 DNC、opt-out、suppression 和 consent。
- 是否没有补电话、模拟通话、伪造 duration 或隐藏号码主体。

## 15. 信息来源 URL

- Google Ads Help, About call assets: https://support.google.com/google-ads/answer/2453991
- Google Ads Help, About call reporting: https://support.google.com/google-ads/answer/2454052
- Google Ads Help, About phone call conversion tracking: https://support.google.com/google-ads/answer/6100664
- Google Ads Help, Measure the calls you receive: https://support.google.com/google-ads/answer/6197479
- Google Ads Help, About call campaigns: https://support.google.com/google-ads/answer/7159344
- Google Ads API, CallAsset: https://developers.google.com/google-ads/api/reference/rpc/v21/CallAsset
- Google Ads API, call_view fields: https://developers.google.com/google-ads/api/fields/v18/call_view
- Google Ads API, Conversion action categories: https://developers.google.com/google-ads/api/docs/conversions/categories
- Google Analytics Help, Avoid sending PII: https://support.google.com/analytics/answer/6366371
- Google Ads Policy, Data collection and use: https://support.google.com/adspolicy/answer/6020956
- CallRail Help, Dynamic number insertion overview: https://support.callrail.com/hc/en-us/articles/5711814948877-Dynamic-number-insertion-overview
- CallRail Help, Visitor tracking basics: https://support.callrail.com/hc/en-us/articles/5712712532109-Visitor-tracking-basics
- CallRail Help, Create a website pool: https://support.callrail.com/hc/en-us/articles/5711655270029-Create-a-website-pool
- Twilio, What is Dynamic Number Insertion: https://www.twilio.com/docs/glossary/what-is-dynamic-number-insertion
- Twilio, Call Attribution: https://www.twilio.com/docs/glossary/what-is-call-attribution
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FTC, Protecting Personal Information: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- NIST SP 800-122, Guide to Protecting the Confidentiality of PII: https://csrc.nist.gov/pubs/sp/800/122/final
