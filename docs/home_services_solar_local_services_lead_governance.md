# Home Services、Solar 与 Local Services Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / Pay-per-call / Appointment / Local Services Ads / Ping/Post 套利里，Home Services Lead、Solar Lead、Contractor Lead、Emergency Local Services Lead 为什么是高意图、高响应要求、高退款/拒付风险的垂类。它承接 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)、[Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](pay_per_call_buyer_routing_duration_payout_governance.md)、[Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md)、[Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md)、[Call Tracking Number Pool、DNI 与电话归因治理手册](call_tracking_dni_number_pool_attribution_governance.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md) 和 [敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)，重点回答：本地服务 lead 的 service type、service area、contractor license/insurance、business hours、dispatch capacity、emergency intent、job booked、showed、quoted、sold、completed、charged lead、credit/dispute 和 Google Ads 信号应该如何治理。

本文不是法律意见，也不提供虚假本地地址、虚假 Google Business Profile、伪造 contractor license/insurance/reviews、冒充 Google Guaranteed/Screened、自动外呼、短信群发、补电话、伪造 job booked / showed / sold、使用 Ads Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做行业知识、字段最小化、服务范围、contractor/buyer terms、call/appointment 状态、来源 URL、claim review、审计、任务和人工审批。

## 1. 为什么 Home Services Lead 是高意图高运营风险垂类

Home services lead 的意图通常很强：用户搜索 “AC repair near me”、“emergency plumber”、“roof leak repair”、“solar quote”、“garage door repair” 时，经常是真的要马上联系服务商。但这类 lead 的价值不是电话或表单本身，而是能否变成可服务、可报价、可成交、可收款的 job：

```text
search / local intent
  -> call / form / message / booking
  -> service area fit
  -> service type fit
  -> contractor capacity
  -> appointment / dispatch
  -> showed / inspected
  -> quoted
  -> sold / signed
  -> completed / paid
  -> dispute / credit / refund outcome
```

常见亏损路径：

- 用户在服务区外，或者服务类型不匹配，例如找 appliance repair 却送给 HVAC buyer。
- 电话有效但 buyer closed、technician unavailable、cap full 或 after-hours 无人接。
- Emergency query 成本高，call duration 短但可能真实；如果只按 duration 判定，会误杀或误扩。
- Contractor 资质、insurance、license、service area 或 Google profile 不一致，导致停投、投诉或低信任。
- Solar lead 表单很多，但 roof ownership、shade、utility bill、credit/financing、homeowner、HOA 或 state incentive 不匹配。
- LSA / buyer 把一些 wrong service、outside service area、duplicate、spam 或 no-show lead 退回，但内部仍按 submitted/call 扩量。

本地服务套利的核心是 lead ops，而不是简单买流量。要把服务能力、响应速度、派单容量、工种匹配、资质和回款状态放在同一个决策窗口里。

## 2. 原理解释：Local Services Lead 是需求、地点、能力和信任的交接

本地服务 lead 的本质是四次交接：

| 交接 | 说明 | 失败后果 |
| --- | --- | --- |
| Need handoff | 用户的服务类型、紧急程度、问题描述 | wrong service、low intent |
| Location handoff | 地址/zip/城市是否在 buyer 服务区 | outside service area、浪费派单 |
| Capacity handoff | contractor 是否营业、是否有 technician、是否能预约 | missed call、no-show、after-hours lead |
| Trust handoff | 用户相信服务商资质、评价、价格和到场承诺 | 投诉、退款、低 close rate |

因此有效价值应按 job lifecycle 测算：

```text
effective_home_services_lead_value =
  headline_payout
  * service_area_fit
  * service_type_fit
  * answer_or_contact_rate
  * booked_job_rate
  * showed_or_dispatch_rate
  * quoted_rate
  * sold_or_completed_rate
  * paid_rate
  - no_show_cost
  - truck_roll_cost
  - complaint_or_credit_reserve
```

只看 call count、form submit、message lead 或 booked appointment 都会误导。一个短电话可能是高价值 emergency job；一个长电话也可能只是价格咨询、job advice 或 wrong service。

## 3. Service Category 地图

| Subvertical | 用户意图 | 典型资格字段 | 主要风险 |
| --- | --- | --- | --- |
| HVAC | AC/furnace repair、installation、maintenance | zip、system type、urgency、homeowner、unit age bucket | 季节高峰、after-hours、no technician |
| Plumbing | leak、clog、water heater、emergency | zip、issue type、urgency、property type | emergency cost、wrong service、dispatch speed |
| Roofing | leak repair、replacement、storm damage | zip、roof type、damage type、homeowner、insurance interest | storm-chasing、insurance claim 误导 |
| Electrical | repair、panel、EV charger | zip、issue type、property type | license、安全风险 |
| Garage Door | broken spring、opener、door repair | zip、door issue、urgency | LSA 高筛查、价格投诉 |
| Pest Control | infestation、termite、wildlife | zip、pest type、property type | recurring service、license/chemical claim |
| Moving | local/long-distance、date、rooms | origin/destination、move date、size bucket | quote bait、license、damage投诉 |
| Cleaning / Maid | recurring / one-time | zip、property type、size bucket | no-show、background trust |
| Remodeling / Kitchen / Bath | estimate、project planning | homeowner、budget range、timeline、scope | low urgency、long sales cycle |
| Solar | solar quote、savings, battery, roof | homeowner、utility bill range、roof/shade, state | savings/tax incentive/financing misrepresentation |
| Lawn / Landscaping | maintenance、tree removal、irrigation | zip、property type、job type | seasonality、wrong equipment/capacity |

不要把 emergency plumbing、solar quote、roof replacement、cleaning 和 remodeling 放进同一个 form、buyer terms 或 conversion action。它们的 urgency、price、close cycle、资质和回款延迟都不同。

## 4. 资格字段和数据最小化

本地服务字段要服务于 service area、service type、capacity 和 appointment，不要过度收集家庭隐私。

| 字段 | 用途 | 最小化做法 | 风险提示 |
| --- | --- | --- | --- |
| zip / city / county | 服务区和 dispatch | zip/city 优先，完整地址只在预约/CRM 保存 | outside service area 高频拒收 |
| service type | HVAC、plumbing、solar 等 | 枚举 | 决定 buyer routing |
| issue type | leak、no cooling、roof damage 等 | 枚举或短描述 bucket | 不要求用户上传敏感照片 |
| urgency | emergency、same-day、flexible | 枚举 | 决定 call routing 和 after-hours |
| property type | single-family、condo、commercial | 枚举 | 某些 buyer 不接 commercial |
| homeowner / renter | solar、roof、remodel 常用 | yes/no/unknown | 不要推断身份或资产 |
| preferred appointment window | 安排上门 | 日期/time bucket | 不等于 confirmed booking |
| budget / project scope range | remodeling/solar 初筛 | range | 不承诺报价或 savings |
| contact channels | phone、SMS、email | 明确 opt-in scope | TCPA/DNC/opt-out |
| consent / buyer disclosure | 可联系和可分享证据 | version/hash/certificate ref | 争议证据核心 |

不要在广告套利系统里保存门锁密码、安防信息、完整住址、家庭成员信息、完整照片、身份证件、贷款文件、完整 utility bill 或 payment details。Solar、roofing、moving 等后续确实需要详细资料时，应由 contractor/buyer 的受控 CRM 处理。

## 5. Contractor / Buyer Eligibility、License、Insurance 和 Service Area

本地服务 lead 不能只看 buyer payout。Buyer 必须具备真实服务能力：

```text
business entity
trade license / contractor license
insurance / bonding
service categories
service area
business hours
after-hours policy
technician capacity
reviews / complaint history
pricing / estimate policy
buyer terms
```

关键治理：

- Contractor license、insurance、bonding、background checks 以地区和服务类别为准。
- Google Local Services Ads 参与者可能需要 screening、verification、license、insurance、background checks 和 review requirements。
- Google Business Profile / local profile 的地址、服务区、名称和现实业务要一致。
- 不用虚假地址、虚假服务区、虚假 DBA、虚假评价或借用他人资质做本地信任。
- Lead aggregator 或 appointment setter 不能暗示自己就是实际 contractor，除非真实如此。
- Buyer cap、营业时间、holiday、dispatch capacity 必须和广告时段/预算绑定。

如果 service area、license state、insurance certificate、business name、landing entity 或 call script 不一致，先暂停 source/campaign，进入 `/risk-audits`。

## 6. Service Area、Hours、Dispatch Capacity 和 Emergency Lead

Local services 的利润常死在容量上：

| 事故 | 结果 | 修复 |
| --- | --- | --- |
| after-hours lead 无人接 | call click / call start 有，job 没有 | ad schedule、call routing、after-hours buyer |
| cap reached | lead 送到无容量 buyer | cap snapshot、fallback disclosure |
| service area 太宽 | outside area / truck roll cost 高 | zip/city allowlist |
| wrong service | buyer 不接该工种 | query negative、form field、routing |
| no technician | 用户等太久或取消 | capacity pacing、dayparting |
| no-show / late cancel | appointment 浅层好看 | reminder、confirmation、buyer feedback |
| price shopper | 长电话但低 close | disposition taxonomy |

Emergency local services 的 call window 很短。建议拆：

```text
call_started
connected
service_area_fit
service_type_fit
dispatch_available
job_booked
technician_dispatched
showed
sold_or_completed
paid
```

不要用统一 duration 门槛判断所有本地服务；plumbing emergency、roofing estimate、solar quote 和 remodeling consultation 的有效通话长度完全不同。

## 7. Lead Delivery：Form、Call、Pay-per-call、Booking 和 Quote

| 形态 | 价值来源 | 治理重点 |
| --- | --- | --- |
| Form CPL | 用户提交服务请求 | service type、zip、consent、buyer acceptance |
| Call lead | 用户主动来电 | answer rate、disposition、call recording disclosure |
| Pay-per-call | 按 qualified call / duration / disposition 计费 | duration 需校准 job outcome |
| Message lead | 用户发消息或 request quote | 响应 SLA、price shopper、service fit |
| Booking lead | 用户预约时间 | booked 不等于 showed/sold |
| Quote / estimate | contractor 报价 | quote 不等于 signed job |
| Completed job | 服务完成 | 更接近 paid value |

Routing value：

```text
local_services_routing_value =
  payout
  * service_area_fit
  * service_type_fit
  * answer_rate
  * booked_rate
  * show_or_dispatch_rate
  * sold_or_completed_rate
  * paid_rate
  - credit_or_refund_risk
  - complaint_risk
  - truck_roll_cost
```

如果系统只优化 submitted、call click 或 booked，会奖励低门槛、低成交、易投诉 source。

## 8. Google Local Services Ads、Charged Lead、Credit 和 Dispute

Google Local Services Ads 按 lead 计费，不等于所有 lead 都可盈利。需要理解：

- valid lead 与内部 qualified lead 不完全相同。
- charged lead 可能后续 credit，也可能因规则不适用而不退。
- outside service area、wrong service、duplicate、spam、no contact、price shopper、advice-seeking 等要进入 disposition。
- LSA lead cost 要与 booked job、sold job、completed job 和 paid value 对账。
- LSA screening / verification / badge 不是 buyer 自己资质治理的替代。

系统建议保存：

```text
lsa_lead_id
lead_type
charged_status
credit_status
credit_reason
service_category
service_area_match
buyer_disposition
booked_job_status
sold_or_completed_status
paid_value
source_url
```

不要把 Google credit 或 dispute 当作利润治理的唯一机制。内部仍要做 source、query、service type、hour、buyer 和 capacity 级别复盘。

## 9. Solar Lead 特殊风险

Solar lead 常见 payout 高，但资格和 claim 风险也高：

| 维度 | 资格 / 风险 |
| --- | --- |
| homeowner | 租客通常不能直接决定安装 |
| roof condition / shade / direction | 影响产能和可行性 |
| utility bill range | 影响 savings estimate |
| state / utility / net metering | 影响 incentive 和回本 |
| financing / lease / PPA / cash | 影响 ownership、tax credit 和长期义务 |
| HOA / permit | 影响安装 |
| credit / PACE / loan | 触发金融披露和房屋 lien 风险 |

高风险 claim：

- “free solar panels”。
- “government will pay for your solar”。
- “guaranteed savings”。
- “eliminate your electric bill”。
- “limited state program ends today”。
- “no cost, no catch”。

Solar 页面要说明：系统大小、屋顶条件、当地 utility、net metering、融资方式、lease/PPA、tax credit 资格和长期合同会影响结果。不要把 lead form 做成“立即获得政府补贴”的误导入口。

## 10. Home Improvement Scam、Review、Price 和 Claim 风险

Home services 页面和创意要避免：

| Claim | 高风险写法 | 安全写法方向 |
| --- | --- | --- |
| Price | “$49 any repair” | “Service call and final price depend on diagnosis” |
| Speed | “Technician in 15 minutes guaranteed” | “Same-day availability may vary by area and schedule” |
| License | “Fully licensed everywhere” | “License and service availability vary by location” |
| Review | “5-star rated” without source | “See current reviews on verified profile” |
| Solar savings | “Cut bills by 90% guaranteed” | “Savings depend on usage, system size, utility rates and contract” |
| Storm / roofing | “Insurance will cover it” | “Coverage depends on policy, inspection and insurer” |
| Free estimate | 隐藏 trip fee / diagnostic fee | 说明 estimate、service call 和 diagnostic policy |
| Local | 虚假 city page / fake address | 真实 service area 和 business identity |

FTC 曾针对 home improvement lead marketing 做过执法，说明向服务商销售 lead 时，lead quality、source、intent 和 billing claim 也不能误导。套利系统既要保护用户，也要保护 buyer/contractor 不被低质或错误 lead 伤害。

## 11. Google Ads、Local Services 和 Business Profile 边界

| 政策/产品面 | 风险 | 治理 |
| --- | --- | --- |
| Local Services platform policies | 服务商、agency、lead generation、aggregator 都要遵守 | 不伪造资质、价格、服务范围或身份 |
| Screening and verification | license、insurance、background、business registration | 保存资质来源和到期日期 |
| Business Profile guidelines | 地址、服务区、业务名称、现实世界一致性 | 不建虚假地址或 city doorway profiles |
| Misrepresentation | 价格、折扣、资质、官方 badge、服务能力不清 | claim/proof 审核 |
| Destination requirements | 广告、landing、form、buyer handoff 一致 | 不做 cloaking 或隐藏真实目的地 |
| Customer data policies | lead / enhanced conversions 数据处理 | consent、hash、最小化 |

Google Guaranteed / Google Screened / Verified badge 不能被第三方 landing 随意借用或暗示。只有真实通过相关筛查并符合显示范围时才能表达。

## 12. Consent、TCPA、DNC、Recording 和 Home Access

本地服务 lead 的 contact governance：

- 电话、短信、email 要按 consent scope 联系。
- 用户 opt-out、DNC 或投诉后要同步 suppression。
- Call recording notice 要按地区和 buyer terms 审核。
- 不自动拨号、不群发短信、不机器人语音追 emergency lead。
- 上门服务涉及家庭地址和安全，完整地址、门禁、家庭信息不进入广告套利系统。
- 发送给 contractor 的信息遵循最小必要原则：service type、zip、appointment window、contact token、consent status、special note bucket。

证据字段：

```text
consent_version
buyer_disclosure_version
contact_channels_allowed
submit_time
timezone
suppression_status
page_snapshot_hash
source_url
```

## 13. Offline Value Mapping

建议分层：

| Stage | Ads 信号建议 | 说明 |
| --- | --- | --- |
| submitted lead | secondary / diagnostic | 不直接扩量 |
| connected call / message | diagnostic | 联系建立 |
| service_area_fit | quality middle | 服务区匹配 |
| service_type_fit | quality middle | 工种匹配 |
| job_booked | stronger | 预约/派单已生成 |
| confirmed appointment | stronger | 用户确认 |
| technician_dispatched / showed | strong | 更接近真实成本和价值 |
| quoted / estimate_sent | strong | 有报价 |
| sold / signed | primary candidate | 更接近收入 |
| completed / paid | final calibration | 最终 value |
| outside area / wrong service / duplicate / complaint | internal negative | 不回传正向 |

Solar 可单独扩展：

```text
submitted
  -> homeowner_qualified
  -> site_survey_booked
  -> site_survey_completed
  -> proposal_sent
  -> contract_signed
  -> installed
  -> paid
```

不要把 booked appointment、qualified duration 或 LSA charged lead 默认当 paid job。

## 14. Home Services Lead Quality Score

建议评分：

```text
home_services_lead_quality_score =
  service_area_fit          15
  service_type_fit          15
  capacity_hours_fit        12
  answer_or_contact_rate    10
  booked_job_rate           12
  show_or_dispatch_rate     12
  sold_or_completed_rate    12
  complaint_credit_risk      7
  license_claim_integrity    5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可按 mature paid value 小幅扩量 |
| 70-84 | 正常测试，继续收集 job outcome |
| 55-69 | 限量，查 service area、wrong service、capacity |
| 35-54 | 暂停扩量，修 routing、hours、buyer 或 landing |
| 0-34 | 停 source / buyer / landing，开风险审计 |

评分必须按 service category、zip/city、buyer、hour、lead type、source、creative angle、form version 和 urgency 拆分。

## 15. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 Google LSA、GBP、FTC、DOE 来源 | `/sources` |
| 记录服务资质、虚假本地、价格/solar claim 风险 | `/risk-audits` |
| 用 policy_score、source_score 和 safe CPC 做小预算测算 | `/calculators` |
| 保存 Offer 垂类、国家、policy notes、tracking URL | `/offers` |
| 生成低风险创意和人工审核投放草稿 | Offer 详情页、`/campaigns` |
| 导入 booked、showed、quoted、sold、completed、paid revenue | `/metrics/import` |
| 生成暂停、限量、查 service area、查 buyer capacity 建议 | `/optimization` |
| 保存任务和审批痕迹 | `/tasks`、`/logs` |

后续可扩展表：

```text
home_service_vertical_profiles
home_service_qualification_fields
contractor_buyer_profiles
contractor_license_refs
service_area_rules
dispatch_capacity_snapshots
home_service_lead_events
home_service_disposition_events
lsa_credit_dispute_events
home_service_claim_reviews
solar_qualification_reviews
home_service_offline_value_maps
home_service_quality_daily
```

关键字段：

```text
service_category
service_type
zip_or_city
service_area_match
urgency
property_type
homeowner_bucket
buyer_or_contractor_id
license_or_insurance_ref
hours_capacity_status
lead_type
disposition
booked_status
showed_or_dispatched_status
sold_or_completed_status
credit_status
paid_value
source_url
reviewer
decision
```

## 16. ADXKit 对应点和完成形态

| ADXKit 能力 | Home services 场景完成形态 | 不交付内容 |
| --- | --- | --- |
| Offer 管理 | service category、service area、buyer terms、contractor license/insurance、paid definition | 虚假地址、虚假资质、伪造 Google badge |
| 落地页采集 | 抽取价格、速度、资质、评价、service area、solar savings claim | cloaking、doorway city page、隐藏真实 contractor |
| AI 创意生成 | 生成“服务范围、预约、报价因素”类低风险素材并进入 claim review | 保证价格、保证到达、保证 savings |
| 投放草稿 | 按 service category、zip/city、urgency、hours 拆 campaign/ad group | Cookie 后台自动投放或绕过验证 |
| 换链接 | 只做同服务、同地区、同披露、已审核 URL 轮换 | 用换链跳到未披露 buyer 或错服务页 |
| 任务中心 | license/insurance 到期、capacity 更新、credit dispute、source quarantine | 自动外呼、短信轰炸、伪造 job 或补电话 |
| 来源库 | Google LSA/GBP、FTC、DOE 来源可追踪 | 用二手 lead seller 话术替代官方来源 |

完成口径：把本地服务 lead 的行业知识、服务资格、contractor/buyer 边界、service area、capacity、appointment/job outcome、credit/dispute、offline value 和系统审计做完整；不做对抗平台、绕过登录、伪造资质或制造虚假流量。

## 17. QA 清单

上线前逐项检查：

- `service_category` 是否明确：HVAC、plumbing、roofing、solar、cleaning、moving 等不能混用。
- service area 是否与 buyer/contractor 真实服务范围一致。
- contractor license、insurance、bonding、business name 和 landing entity 是否一致。
- 是否避免虚假 Google Guaranteed / Screened / Verified / local badge。
- 页面是否清楚说明 lead generator / contractor / aggregator 角色。
- 价格、到达时间、free estimate、same-day、solar savings、tax incentive 等 claim 是否有证据和条件。
- Business hours、after-hours、holiday、cap 和 technician capacity 是否与广告时段绑定。
- Form 字段是否避免完整地址、门禁、家庭成员、完整照片和 payment details。
- Consent 是否包含 contact channel、buyer disclosure、version/hash 和页面证据。
- Call tracking 是否保存 disposition，而不是只看 duration。
- Appointment 是否区分 booked、confirmed、showed、quoted、sold、completed、paid。
- LSA charged / credited lead 是否与内部 buyer feedback 对账。
- Solar 是否单独检查 homeowner、roof/shade、utility bill、financing/lease/PPA 和 tax incentive claim。
- Google Ads primary conversion 是否使用成熟、可收款、低投诉的事件。
- 不使用 Ads Cookie 后台操作、自动登录、cloaking、代理/指纹规避、补点击或封禁规避。

## 18. 信息来源 URL

| 来源 | URL | 用途 |
| --- | --- | --- |
| Google Local Services Ads, How leads work | https://support.google.com/localservices/answer/7195435 | 支撑 valid lead、charged lead、lead type、budget、credits 和 LSA lead 口径 |
| Google Local Services Ads, Understand the screening and verification process | https://support.google.com/localservices/answer/6226575 | 支撑 background、business registration、insurance、license、review requirements 和持续复审 |
| Google Local Services Ads, How providers qualify | https://support.google.com/localservices/answer/6230381 | 支撑 Local Services provider screening、license、insurance 和 verification 语境 |
| Google Local Services Ads, Business screening and verification requirements | https://support.google.com/localservices/answer/12174778 | 支撑美国本地服务商 background、license、insurance 和 category-specific requirements |
| Google Ads Policy, Local Services platform policies | https://support.google.com/adspolicy/answer/6245891 | 支撑 service provider、agency、lead generation、aggregator 的 Local Services 平台政策 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑价格、服务范围、资质、badge、官方关系和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Business Profile, Guidelines for representing your business | https://support.google.com/business/answer/3038177 | 支撑真实业务名称、地址、service area 和本地业务资料一致性 |
| FTC, How To Avoid a Home Improvement Scam | https://consumer.ftc.gov/articles/how-avoid-home-improvement-scam | 支撑 contractor、合同、付款、pressure tactic 和 home improvement scam claim 审核 |
| FTC, Solar Power for Your Home | https://consumer.ftc.gov/articles/solar-power-your-home | 支撑 solar savings、lease/PPA、tax credit、PACE financing、roof/utility 条件和 installer 评估 |
| DOE, Homeowner's Guide to Going Solar | https://www.energy.gov/eere/solar/homeowners-guide-going-solar | 支撑 solar consumer education、financing、scam awareness 和官方资源 |
| FTC, HomeAdvisor lead marketing order | https://www.ftc.gov/node/80302 | 支撑 home improvement lead seller 不能误导服务商关于 lead quality、source 和 billing |
| FTC, Advertising FAQ's: A Guide for Small Business | https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business | 支撑 truth-in-advertising、material claim 和 substantiation |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | 支撑 reviews、testimonials、ratings 和 material connection 披露 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、DNC、拒绝联系和记录治理 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
| FTC, Consumer Reviews and Testimonials Final Rule | https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers | 支撑虚假评价、购买评价和 review claim 风险 |
