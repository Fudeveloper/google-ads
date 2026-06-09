# Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册

更新时间：2026-06-09

本文解释 CPL / Call Lead / Appointment Lead arbitrage 中，为什么“提交以后多久联系、谁联系、联系几次、在哪个时段联系、坐席是否接得住、是否尊重 DNC/opt-out”会直接决定 buyer acceptance、qualified rate、paid rate 和投诉风险。它承接 Lead 质量、电话 Lead、Ping/Post、Lead 验证和 CPL 垂类经济手册，重点补齐从 `accepted` 到 `contacted / qualified / booked / sold / paid` 的运营环节。

本文不是法律意见，也不提供自动拨号、短信群发、机器人外呼、伪造通话、补电话、模拟通话时长、绕过 consent/DNC/TCPA、隐藏 caller identity、cloaking、Cookie 后台接管或封禁后换号的方案。系统落地只做知识、字段、SLA、QA、审计、来源 URL 和人工审批。

## 1. 为什么 Speed-to-Lead 是 CPL 利润核心

很多 CPL 团队把亏损归因于“流量差”，但真正的损耗可能发生在提交后：

- Buyer 接收了 lead，但坐席没有及时打。
- 用户正在比较价格，5 分钟后已经被其他服务商联系。
- Call asset 点击很多，但 connected calls 少。
- Call duration 达不到 qualified threshold。
- 营业时间外继续买电话流量，missed call 上升。
- Shared lead 被多个 buyer 高频联系，引发投诉和 DNC。
- Google Ads 把短通话或 submitted lead 当成 primary conversion，继续优化到低价值流量。

Lead 的经济价值会随时间衰减。不同垂类衰减速度不同：

| 垂类 | 联系速度敏感度 | 说明 |
| --- | --- | --- |
| Emergency local services | 极高 | 用户需要立刻解决，missed call 直接损失 |
| Insurance / Medicare | 高 | 用户比较多个报价，晚联系会降低接通和成交 |
| Legal / accident | 高 | 案件线索有竞争和资格窗口 |
| Healthcare appointment | 中高 | 排期、保险和诊所容量影响 booked/showed |
| Education | 中 | 研究周期较长，但 follow-up 仍影响 qualified |
| B2B SaaS | 中低 | 销售周期长，更看重 MQL/SQL 质量 |

因此，CPL 的真实公式应该包含 contact layer：

```text
Paid EPC =
  Click-to-Lead Rate
  * Buyer Acceptance Rate
  * Contact Rate
  * Qualification Rate
  * Booked/Sold Rate
  * Paid Rate
  * Net Payout
```

## 2. 原理解释：联系治理不是骚扰或造假

联系治理的正确目标：

- 把用户希望被联系的 lead 尽快交给正确 buyer / team。
- 在 consent 和 disclosure 允许的渠道内联系。
- 避免营业时间外、cap 满、坐席不足时继续买高意图流量。
- 把 missed call、no answer、wrong number、short call、appointment no-show 等反馈回到 source、creative、landing 和出价。
- 让自动出价学习真实 qualified/paid，而不是 call clicks 或短通话。

错误做法：

- 自动外呼或短信轰炸验证号码。
- 用机器人通话或录音补 call duration。
- 用户 opt-out 后换渠道继续联系。
- 隐藏 caller identity 或 buyer identity。
- 为了报表把 missed call 记成 conversion。
- 让多个未披露 buyer 同时高频联系用户。

联系速度本身不是合规风险；没有 consent、没有频控、没有退订、没有 DNC、没有身份披露的联系才是风险。

## 3. 核心对象地图

| 对象 | 作用 | 套利关注点 |
| --- | --- | --- |
| Lead event | 表单、电话、聊天或预约事件 | submitted 不等于 contacted |
| Contact permission | 用户允许的渠道、主体和范围 | 电话/短信/邮件要拆开 |
| Buyer / call center | 实际联系用户的人 | capacity、hours、quality feedback |
| Contact attempt | 一次电话、短信、邮件或人工任务 | channel、time、result、agent |
| SLA policy | 规定多久内联系、几次、何时停 | 不同垂类不同 SLA |
| Operating hours | buyer 或坐席可接时间 | 影响预算 pacing 和 call asset |
| Call tracking number | 归因和转接号码 | 不用于隐藏主体或造假电话 |
| Disposition | no answer、connected、qualified、booked 等 | 投放优化的真相层 |
| Suppression / DNC | 不可联系名单 | 必须先于再次联系检查 |
| Feedback lag | 状态回传延迟 | 决定何时扩量/停量 |

## 4. Contact Funnel 和状态机

建议状态机：

```text
submitted
  -> consent_validated
  -> routed_to_buyer_or_queue
  -> first_attempt_due
  -> first_attempted
  -> connected / no_answer / wrong_number / voicemail / opted_out
  -> qualified / not_qualified
  -> booked / application_started / quote_requested
  -> showed / sold / approved / paid
  -> rejected / complaint / dnc / chargeback
```

每个状态都要记录时间：

| 时间字段 | 用途 |
| --- | --- |
| submitted_at | 用户提交或来电时间 |
| routed_at | 进入 buyer / call center 时间 |
| first_attempt_due_at | SLA 截止时间 |
| first_attempt_at | 首次联系尝试 |
| first_connected_at | 首次接通 |
| qualified_at | 成为合格机会 |
| booked_at | 预约或申请 |
| paid_at | 可收款结果 |
| opt_out_at | 停止联系 |

核心时间指标：

```text
Speed to First Attempt = first_attempt_at - submitted_at
Speed to Connect = first_connected_at - submitted_at
Feedback Lag = buyer_feedback_received_at - submitted_at
```

## 5. SLA 类型

| SLA | 说明 | 示例 |
| --- | --- | --- |
| First attempt SLA | 多久内首次联系 | emergency 60 秒，insurance 5 分钟，B2B 4 小时 |
| Connect SLA | 多久内实际接通 | 24 小时内至少一次 connected |
| Attempt cadence SLA | 联系次数和间隔 | 3 天内 3 次，不同渠道分开 |
| Opt-out SLA | 用户拒绝后多久停止 | 立即停止并同步 buyer |
| DNC sync SLA | suppression 更新多快同步 | 当日或实时 |
| Feedback SLA | buyer 多久回传 disposition | 24h / 72h / 7d |
| Booking SLA | 接通后多久安排预约 | local service 当场，healthcare 1 天 |
| Dispute SLA | 错误 lead 多久申诉 | 按平台/合同窗口 |

SLA 不应只写在合同里，还要进入预算节奏：

- Buyer closed 时不要继续买 call-heavy 流量。
- Cap 或坐席容量不足时降低预算或暂停。
- Feedback SLA 逾期时降低 buyer/routing weight。
- Opt-out SLA 违约时立刻进入审计。

## 6. Contact Cadence 和频控

联系节奏要区分渠道：

| 渠道 | 适用 | 风险 |
| --- | --- | --- |
| 人工电话 | 高意图、需要咨询 | DNC/TCPA、录音披露、caller identity |
| 短信 | 预约提醒、用户明确同意 | TCPA、opt-out、频率 |
| 邮件 | 教育/B2B/低紧急度 | CAN-SPAM、unsubscribe、低响应 |
| 在线聊天 | 页面即时咨询 | 隐私和转交披露 |
| 预约日历 | healthcare/local/B2B | 可用时段和 no-show |

推荐策略：

- 先确认 consent scope，再决定渠道。
- 每次 attempt 前检查 suppression / DNC / opt-out。
- 高频联系要有上限、冷却时间和停止条件。
- Shared lead 更要严格限频，避免用户被多个 buyer 同时轰炸。
- 未接通不等于可以无限联系。

禁止：

- 自动拨号或短信群发来“验证号码”。
- 用户拒绝后继续换渠道联系。
- 用预录音、AI 语音或自动化系统绕过人工边界。
- 把用户一次 consent 当成无限 buyer、无限渠道、无限次数的许可。

## 7. Operating Hours、时区和预算 Pacing

Lead contact 要把广告时区、用户时区、buyer 时区、call center 时区放在一起看。

常见事故：

| 事故 | 表现 | 修复 |
| --- | --- | --- |
| 营业时间外继续投放 | missed call 高、call duration 短 | dayparting / call schedule |
| 时区错配 | 晚上打给用户、投诉上升 | user timezone mapping |
| 坐席 lunch / shift gap | 某时段 no answer 高 | staffing and pacing |
| 节假日无坐席 | spend 有，qualified 无 | holiday calendar |
| Buyer cap 满但广告不停 | no buyer / fallback payout 低 | cap-aware budget |

运营原则：

- Call-heavy campaign 必须有 hours matrix。
- Google Ads schedule、call asset schedule、buyer hours 和 call center hours 要一致。
- 预算 ramp 不能超过 buyer/call center capacity。
- 高意图 emergency query 不应流向无法立即响应的 buyer。

## 8. Call Tracking、Call Reporting 和 Call Conversion

Google Ads call assets 和 call reporting 可以帮助衡量来电、通话时长、来电时间、呼叫者区号等指标。它们适合做归因和质量诊断，但不是最终收入。

推荐拆分：

| 指标 | 含义 | 是否可作为 primary conversion |
| --- | --- | --- |
| Call asset click | 点击电话入口 | 不建议 |
| Call started | 发起通话 | 不建议 |
| Connected call | 接通 | 中间指标 |
| Qualified duration | 达到业务时长阈值 | 可作为浅层转化 |
| Sales qualified call | 坐席确认合格 | 更适合 |
| Booked appointment | 预约成功 | 更适合 |
| Sold / paid call | 可收款 | 最适合 |

Call duration threshold 要按垂类设定：

- Emergency local services：短通话也可能有效，但要看 booked job。
- Insurance/legal：需要足够时间完成资格确认。
- Healthcare：要看 booked / showed。
- B2B：电话可能只是 discovery，不等于 revenue。

不要用机器人、循环拨打、虚假通话或内部员工电话制造 duration。

## 9. Call Center Capacity 和 Buyer Capacity

坐席容量影响 paid revenue：

```text
Capacity per hour =
  agents
  * average handled calls per agent per hour
  * qualification capacity factor
```

需要记录：

```text
buyer_id
queue_id
hours_open
agents_available
max_leads_per_hour
max_calls_per_hour
current_queue_depth
average_speed_to_answer
missed_call_rate
abandon_rate
cap_remaining
```

容量不足时的正确动作：

- 降低广告预算或暂停 call-heavy ad groups。
- 切换到预约表单或稍后联系，但要明示预期。
- 路由到有 capacity 且 consent 允许的 buyer。
- 降低该时段的 bid / campaign schedule。

错误动作：

- 继续买高意图电话流量，让 missed call 堆积。
- 把无人接听 call 计入有效 conversion。
- 用低价 fallback 接高价值 lead 但不调出价。

## 10. Disposition Taxonomy

不要只用 `contacted=true/false`。推荐 disposition：

| Disposition | 说明 | 投放动作 |
| --- | --- | --- |
| connected_qualified | 接通且合格 | 正向反馈 |
| connected_unqualified | 接通但不合格 | 修资格问题 |
| no_answer | 未接 | 查联系时间和坐席 |
| voicemail_left | 留言 | 观察后续回拨 |
| wrong_number | 错号 | 修表单/source |
| existing_customer | 现有客户 | 从 acquisition revenue 中排除 |
| duplicate | 重复 | 去重和 source 降权 |
| out_of_area | 服务区外 | 修 geo 和页面 |
| booked | 成功预约 | 正向反馈 |
| no_show | 未到场 | 查意图和提醒 |
| sold / paid | 可收款 | 出价学习 |
| opt_out / dnc | 停止联系 | suppression 同步 |
| complaint | 投诉 | 暂停 source 和 buyer audit |

Disposition 必须能回到 `source + campaign + keyword + creative + landing + form_version + buyer + agent/team`。

## 11. Recording、QA 和 AI 质检边界

录音和质检可以帮助判断 low intent、错误服务、坐席话术和投诉，但风险也高。

治理要求：

- 录音前有适用地区要求的披露。
- 保存 recording disclosure version。
- 不把录音随意发给广告、创意或外包团队。
- 对敏感金融、健康、法律数据做访问控制。
- AI 质检只处理脱敏或授权数据，不把完整 PII、Cookie、账号凭据发给模型。

可做：

- 抽样标注 call disposition。
- 记录 agent script version。
- 检查是否夸大承诺、未披露 buyer、未处理 opt-out。
- 把聚合问题反馈到 creative brief。

不做：

- 用 AI 语音冒充人工。
- 用合成通话制造 qualified duration。
- 将录音作为普通附件散发。

## 12. Contact Quality Score

建议新增联系质量评分：

```text
Contact Quality Score =
  0.20 * speed_to_first_attempt
  + 0.15 * connected_rate
  + 0.15 * qualified_contact_rate
  + 0.15 * capacity_fit
  + 0.10 * opt_out_dnc_safety
  + 0.10 * disposition_freshness
  + 0.10 * booked_or_sold_rate
  + 0.05 * recording_qa_safety
```

评分解释：

| 维度 | 看什么 |
| --- | --- |
| speed_to_first_attempt | 是否在垂类 SLA 内首次联系 |
| connected_rate | 接通率 |
| qualified_contact_rate | 接通后合格比例 |
| capacity_fit | 广告量是否匹配坐席/cap |
| opt_out_dnc_safety | opt-out、DNC、complaint 是否可控 |
| disposition_freshness | buyer/call center 是否及时回传 |
| booked_or_sold_rate | 是否形成真实机会 |
| recording_qa_safety | 录音披露、质检和话术合规 |

动作阈值：

| 分数 | 动作 |
| --- | --- |
| 85-100 | 可小步放量 |
| 70-84 | 保持预算，修 disposition 或 capacity |
| 50-69 | 降预算，限制时段或 buyer |
| < 50 | 暂停 call-heavy source，进入审计 |

## 13. 常见事故和修复

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| call clicks 高，connected 低 | 号码错误、营业时间、坐席不足、误点 | 查 call reporting、号码和 hours |
| connected 高，qualified 低 | query/creative 低意图，资格问题缺失 | 修关键词、表单和页面承诺 |
| qualified 高，paid 低 | buyer 后续处理差、回款慢、scrub | 查 buyer feedback 和 paid definition |
| missed call 高 | capacity 不足或排班错 | 降预算、改 schedule |
| no answer 高 | 联系太晚、时间不合适、号码质量差 | 查 speed-to-lead 和 source |
| complaint/DNC 高 | 频控差、buyer 未披露、shared lead 过度联系 | 立即暂停并同步 suppression |
| opt-out 后仍联系 | suppression 同步失败 | 事故处理和 buyer audit |
| short call 多 | 误点、错服务、价格不匹配 | 修 ad copy、CTA、landing |

## 14. Google Ads 与出价信号边界

出价信号建议：

- 不把 call asset click 当 primary conversion。
- 不把所有 call started 当有效 lead。
- qualified duration 可做中间 conversion，但需要后续 buyer feedback 校准。
- 更好的 primary 是 sales qualified call、booked appointment、approved/paid lead。
- missed call、wrong number、no answer、opt-out、DNC、complaint 不应作为正向 conversion。
- 营业时间外或 capacity 不足时，自动出价可能学到错误信号，需要 schedule / budget guardrail。

如果无法从 call center 或 buyer 拿到 disposition，就不应在 call-heavy campaign 上快速扩量。

## 15. 系统落地

当前 V1 可用：

| 需求 | 当前位置 |
| --- | --- |
| 记录 call lead、buyer handoff、DNC 风险知识 | `/knowledge/lead_call_tracking` |
| 记录 lead quality、reject reason 和 buyer feedback | `/knowledge/lead_quality`、`/risk-audits` |
| 导入 cost、conversion、paid revenue | `/metrics/import` |
| 生成预算和止损建议 | `/optimization` |
| 保存来源 URL 和政策依据 | `/sources` |

后续可扩展表：

```text
lead_contact_sla_policies
lead_contact_attempts
lead_contact_dispositions
call_center_capacity_snapshots
buyer_operating_hours
lead_callback_tasks
lead_opt_out_sync_events
call_recording_qa_reviews
contact_quality_score_daily
```

这些表只保存 SLA、attempt、disposition、capacity、opt-out sync、QA 和聚合评分。第一版不保存录音文件，不做自动外呼、短信群发、机器人通话、虚假 call duration、Cookie 后台操作或规避 DNC/TCPA。

## 16. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本项目完成形态 |
| --- | --- |
| 自动投放优化 | 用 Contact Quality Score、missed call、qualified call、paid feedback 生成建议 |
| 任务调度 | 生成人工 callback / QA / buyer feedback 任务，不自动拨号 |
| 数据同步 | 导入 call reporting、CRM disposition、buyer feedback |
| 换链接 / routing | 只在 capacity、hours、consent、buyer disclosure 允许时做合规 fallback |
| 创意优化 | 把 short call、wrong service、low intent 反馈到创意和页面 |
| 高风险电话操作 | 不做自动外呼、短信群发、补电话、机器人通话或隐藏 caller identity |

## 17. QA 清单

- 每个 call-heavy campaign 是否有 buyer/call center hours。
- Google Ads schedule、call asset schedule、buyer hours 是否一致。
- 是否记录 submitted、first attempt、connected、qualified、booked、paid 的时间。
- 是否有 first attempt SLA、attempt cadence、feedback SLA、opt-out SLA。
- 每次联系前是否检查 consent、DNC、opt-out、suppression。
- Shared lead 是否有限频和 buyer disclosure。
- Call duration threshold 是否按垂类定义。
- 是否区分 call click、connected call、qualified call、booked、paid。
- Missed call、wrong number、no answer 是否能回到 source 和 campaign。
- 坐席容量不足时是否能降预算或暂停。
- 录音是否有披露、保留期、访问控制和 QA 状态。
- 是否禁止自动外呼、短信群发、伪造通话、补电话和 Cookie 后台。

## 18. 信息来源 URL

- Google Ads Help, About call assets: https://support.google.com/google-ads/answer/2453991
- Google Ads Help, About call reporting: https://support.google.com/google-ads/answer/2454052
- Google Ads Help, About phone call conversion tracking: https://support.google.com/google-ads/answer/6100664
- Google Ads Help, Create call ads: https://support.google.com/google-ads/answer/6341403
- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Help, Local Services Ads platform policies: https://support.google.com/localservices/answer/6224841
- Google Ads Help, How lead costs and credits work in Local Services Ads: https://support.google.com/localservices/answer/7436333
- Google Ads Help, About ad scheduling: https://support.google.com/google-ads/answer/2404244
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- FTC, Q&A for Telemarketers & Sellers About DNC Provisions in TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- FTC, CAN-SPAM Act: A Compliance Guide for Business: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FCC, TCPA one-to-one consent rule court response / deletion order: https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- eCFR, 16 CFR 310.5 Recordkeeping requirements: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5
