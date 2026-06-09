# Lead Freshness、Aged Lead 与 Recontact Window 治理手册

更新时间：2026-06-09

本文解释 CPL / Call Lead / Appointment Lead / Insurance / Home Services / Finance / Education 等 lead arbitrage 场景里，如何治理 lead freshness、lead age、fresh / real-time lead、exclusive lead、shared lead、aged lead、recycled lead、recontact window、consent refresh、DNC / opt-out、suppression、buyer acceptance、contact rate、payout tier 和 Google Ads 转化信号。它承接 [Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)、[Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md) 和 [Lead Pricing、Payout Negotiation 与结算安全垫治理手册](lead_pricing_payout_negotiation_governance.md)，重点回答：一条 lead 从 30 秒、5 分钟、1 小时、24 小时、7 天到 90 天后，为什么价值、联系策略、可售范围、合规证据和出价信号都必须变化。

本文不是法律意见，也不提供自动拨号、短信群发、补电话、伪造 lead age、刷新旧 consent、隐藏 aged lead 状态、绕过 DNC/TCPA/TSR、用代理/指纹伪装来源、Cookie 后台投放或 cloaking 的方案。系统只做 lead age 分桶、证据、合规检查、buyer 条款映射、质量评分、审计、任务和人工审批。

## 1. 为什么 Lead Freshness 决定 CPL 盈亏

Lead arbitrage 的收入端不是“有一条表单提交就有一笔收入”。Lead 的意图会随时间衰减：

```text
submit intent
  -> first response
  -> contact / no answer
  -> qualification
  -> buyer accept / reject
  -> appointment / sale / paid
```

时间越长，通常会出现：

- 用户已经联系了竞争对手。
- 用户忘记自己提交过表单，投诉率上升。
- 电话接通率和短信/邮件响应率下降。
- Buyer 将 aged lead 降价、拒收或要求单独披露。
- 原始 consent 范围、buyer disclosure、privacy policy 或 DNC 状态可能已经变化。
- Google Ads 仍把 submitted lead 当正向 conversion，继续买低意图时段或来源。

所以 lead freshness 是 CPL 的单位经济变量，不只是客服 SLA：

```text
effective_lead_value =
  payout
  * contact_probability_by_age
  * qualification_probability_by_age
  * payment_probability
  - complaint_risk_cost
  - return_or_scrub_risk
```

## 2. 原理解释：意图衰减不能靠补触达修复

Lead age 的本质是用户意图和可联系权利同时变化。团队不能把旧 lead 当成“便宜库存”，靠更高频电话、短信轰炸或换 buyer 来补收入。

正确理解：

| 维度 | 新鲜 lead | Aged / recycled lead |
| --- | --- | --- |
| 用户记忆 | 刚提交，知道请求内容 | 可能忘记或已解决问题 |
| 竞争状态 | 还在选择 | 可能已被多人联系 |
| buyer 价值 | 可高价、可独家 | 低价、需特殊条款 |
| consent 证据 | 与当前页面接近 | 需要验证旧证据、撤回和 DNC |
| 联系策略 | 快速、少量、相关 | 更谨慎、低频、先验证权限 |
| 出价信号 | 可作为 early signal | 不应混入 fresh lead primary conversion |

禁止把以下动作当成优化：

- 把旧 lead 重新提交成新 lead。
- 修改 timestamp 或 lead age bucket。
- 用新页面的 consent 覆盖旧 lead。
- 对 aged lead 使用自动拨号或短信群发来“恢复意图”。
- 隐藏 shared / aged 状态卖给 buyer。
- 用户 opt-out 后换主体、换渠道继续联系。

## 3. 核心对象地图

| 对象 | 含义 | 治理作用 |
| --- | --- | --- |
| original submit time | 用户第一次提交时间 | lead age 的起点 |
| lead age bucket | 0-5m、5-30m、same-day、1-7d 等 | 决定 payout、routing 和联系策略 |
| first response time | 首次联系或交接时间 | Speed-to-Lead 指标 |
| recontact window | 可再次联系的时间和频率边界 | 避免骚扰和投诉 |
| consent refresh | 是否需要重新取得或确认同意 | 防止旧 consent 无限复用 |
| suppression snapshot | DNC、opt-out、withdrawal、complaint 状态 | 决定是否可联系 |
| buyer freshness rule | buyer 合同中的 lead age 接收规则 | 决定可售和价格 |
| aged inventory source | aged lead 来源、原始页面、原始 buyer | 防止不明来源库存 |
| contact disposition | connected、no answer、wrong number、complaint | 校准 age 价值曲线 |
| freshness score | lead age、证据、suppression、buyer 条款评分 | 决定投放和 routing |

## 4. Lead Age 分桶

建议所有 lead 都保存 `original_submit_time`，并按业务分桶：

| Bucket | 典型含义 | 操作建议 |
| --- | --- | --- |
| real-time / 0-60s | 即时提交 | 适合高价值 buyer、call-heavy 和快速回访 |
| 1-5m | 高新鲜度 | 仍可优先联系和高价 routing |
| 5-30m | 意图开始衰减 | 监控 first response SLA |
| 30m-2h | 中等衰减 | 降低 bid / routing priority |
| same-day | 当天 lead | 需看垂类和时段 |
| 1-7d | aged early | 需要 buyer terms、consent 和 suppression 复查 |
| 8-30d | aged | 低价、低频、强审计 |
| 31-90d | aged deep | 通常只能在明确合同和 consent 下低强度处理 |
| 90d+ | stale / archive | 默认不联系，除非有明确 refresh 和合法依据 |

不同垂类不能共用分桶。本地服务、保险、债务、教育、B2B demo、医疗咨询的意图半衰期不同。

## 5. Fresh、Exclusive、Shared、Aged、Recycled 的差异

| 类型 | 价值来源 | 风险 |
| --- | --- | --- |
| fresh lead | 即时需求和明确意图 | call center 不及时会浪费 |
| exclusive lead | 单一 buyer、低打扰 | buyer fit 和 cap 失败时价值损失 |
| shared lead | 多 buyer 竞争，总收入可能高 | 投诉、DNC、披露不足 |
| aged lead | 低价补量或再激活 | 低响应、旧 consent、投诉 |
| recycled lead | 曾被拒收、未售出或再次处理 | duplicate、no consent、buyer distrust |

Fresh 不等于 exclusive，aged 也不等于违法。关键是：是否真实披露、是否符合原始 consent、是否通过 suppression、buyer 是否知道 age、价格是否按 age 调整、用户是否仍有合理预期。

## 6. Buyer Terms 和 Payout Tier

Buyer 合同必须写清：

```text
accepted_lead_age_max
fresh_lead_definition
aged_lead_definition
exclusive_window
shared_allowed
recycled_allowed
lead_age_discount
return_reason_no_consent
return_reason_stale
suppression_refresh_required
evidence_required
```

常见 tier：

| Tier | 口径 | 价格处理 |
| --- | --- | --- |
| real-time exclusive | 例如 0-5m 且只给一个 buyer | 最高 payout |
| same-day exclusive | 当天独家 | 中高 payout |
| same-day shared | 当天共享 | 降价或按 buyer cap |
| 1-7d aged | 明示 aged | 低 payout，强证据 |
| 8d+ aged / recycled | 明示来源和 age | 通常不进主流优化信号 |

不要用 headline payout 测算 aged inventory。要用 effective payout：

```text
effective_aged_payout =
  gross_payout
  * accepted_rate_by_age
  * contacted_rate_by_age
  * qualified_rate_by_age
  * paid_rate
  - complaint_reserve
  - scrub_reserve
```

## 7. Recontact Window 和频控

Recontact window 是“何时、通过什么渠道、用什么频率、由谁再联系”的规则。

| 场景 | 推荐规则 |
| --- | --- |
| 未接通 fresh lead | 按 consent scope、业务时间和 contact cadence 少量重试 |
| same-day no answer | 降低频率，避免跨时区夜间联系 |
| 1-7d aged | 先查 consent、DNC、opt-out、buyer terms，再低频联系 |
| 8d+ aged | 默认人工复核，不进入自动队列 |
| 用户 opt-out / DNC | 停止对应渠道，生成 suppression sync |
| complaint | 停 source/buyer/form version，生成证据包 |

Recontact 必须停止于：

- 用户明确拒绝或 opt-out。
- DNC / suppression 命中。
- Buyer 条款禁止 aged 或 recycled lead。
- Consent scope 不覆盖当前 buyer / channel。
- Lead age 超过合同或隐私政策允许窗口。
- 投诉率、no answer、wrong number 超阈值。

## 8. Consent Refresh 和证据链

旧 lead 的核心问题不是“还在数据库里”，而是“是否仍可联系、可分享、可出售”。必须复查：

| 检查项 | 说明 |
| --- | --- |
| original consent version | 当时同意文本和 buyer disclosure |
| certificate / page snapshot | TrustedForm / Jornaya 类证据或内部快照 |
| privacy policy version | 原始页面的数据用途和保留说明 |
| consent scope | 电话、短信、邮件、自动化技术、buyer 范围 |
| opt-out / withdrawal | 是否撤回或停止联系 |
| DNC / suppression | 联系前最新 suppression 状态 |
| buyer terms | buyer 是否接受 aged、shared、recycled |

Consent refresh 不是“把旧 lead 重新打一次新勾”。如果要重新取得同意，必须是清晰、真实、可证明、非默认勾选，并且不能伪装成用户原始提交。

## 9. Google Ads 与转化信号边界

Fresh lead 和 aged lead 不应混入同一个 primary conversion：

| 信号 | 风险 |
| --- | --- |
| submitted lead | 容易奖励低门槛、低意图表单 |
| accepted aged lead | buyer 可能只是先收，后续 scrub |
| recontact success | 可能反映联系策略，不代表新流量质量 |
| recycled lead revenue | 不应归因到当前广告点击 |
| paid fresh lead | 更适合作为优化价值 |

建议：

- Fresh lead、aged lead、recycled lead 分 conversion action 或内部状态。
- Recontact revenue 不要回传给当前 Google Ads click，除非有明确归因和真实 click_id。
- Aged inventory 的收入不要污染新广告 source / keyword / creative 的 RPV。
- Google Ads lead form 下载窗口、CRM 导出窗口和 buyer feedback lag 要单独记录。

## 10. Freshness Quality Score

建议评分：

```text
freshness_quality_score =
  lead_age_fit              20
  first_response_sla        15
  buyer_age_terms_fit       15
  consent_age_fit           15
  suppression_freshness     15
  contact_disposition_fit   10
  payout_tier_integrity      5
  complaint_history          5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可优先 routing / 小幅扩量 |
| 70-84 | 正常处理，抽样检查 |
| 55-69 | 降低 buyer weight 或 source budget |
| 35-54 | 只允许人工复核和低频 recontact |
| 0-34 | 停止 routing，进入 suppression / dispute review |

评分必须按 mature feedback 校准：contacted、qualified、approved、paid、returned、complaint、DNC/opt-out。

## 11. 事故诊断

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| Fresh lead paid 下降 | first response 慢、buyer capacity 不足 | 查 SLA、call center、cap |
| Same-day lead reject 上升 | buyer age rule 变更或 timezone 错 | 查 buyer terms 和 submit time |
| Aged lead complaint 高 | consent 不覆盖、用户已忘记、共享过度 | 暂停 aged routing |
| Recycled lead duplicate 高 | 未记录原始 buyer / post count | 查 handoff history |
| Google Ads ROI 虚高 | aged revenue 归到新点击 | 修归因和 conversion action |
| Buyer 扣 no consent | 旧证据缺失或 disclosure 不覆盖 | 生成 evidence pack |
| Opt-out 后仍联系 | suppression sync 失败 | 开事故，通知 buyer |

事故复盘必须保存：original_submit_time、lead_age_bucket、consent version、certificate ref、suppression snapshot、buyer terms、handoff history、contact disposition、source/subid、campaign、处理动作。

## 12. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 aged lead 来源、buyer 条款和政策资料 | `/sources` |
| 记录 stale lead、no consent、DNC、complaint 事故 | `/risk-audits` |
| 用 source_score 和 safety factor 降低机会评分 | `/calculators` |
| 导入 accepted、qualified、paid、returned、complaint | `/metrics/import` |
| 生成暂停 aged source、降预算、review consent 建议 | `/optimization` |
| 创建 recontact QA、suppression sync、buyer terms review 任务 | `/tasks` |

建议后续表：

```text
lead_freshness_profiles
lead_age_snapshots
lead_recontact_policies
lead_recontact_attempts
aged_lead_inventory_batches
aged_lead_buyer_terms
lead_age_quality_daily
lead_recycled_handoff_history
lead_freshness_incidents
```

核心字段：

```text
lead_age_snapshots:
  lead_id, original_submit_time, observed_at,
  lead_age_seconds, lead_age_bucket, source_id,
  form_version, consent_version, suppression_status,
  buyer_terms_version, decision

lead_recontact_policies:
  vertical, country, channel, age_bucket,
  max_attempts, cooldown_hours, allowed_hours,
  consent_refresh_required, suppression_check_required,
  reviewer, source_url
```

系统不自动拨号、不短信群发、不伪造 lead age、不刷新旧 consent、不把 aged lead 当 fresh lead、不用 Cookie 后台改 conversion 或预算。

## 13. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI 看板 | 分 fresh / same-day / aged / recycled 看 accepted、paid、complaint |
| 自动优化 | 根据 lead age、buyer terms、suppression 和 paid rate 生成降速建议 |
| 换链接 / routing | 只建议符合 consent、age、buyer terms 的 fallback |
| 自动投放 | 生成预算和 conversion signal QA，不用 Cookie 后台 |
| 任务中心 | recontact QA、aged inventory review、suppression sync、buyer terms review |
| 风险审计 | stale lead、no consent、DNC、complaint、age mismatch |

完成标准：

- 能解释 lead age 为什么影响 contact、qualification、payout 和投诉。
- 能区分 fresh、exclusive、shared、aged、recycled lead。
- 能说明 recontact window、consent refresh、DNC/opt-out 和 suppression 的关系。
- 能把 aged revenue 从新广告投放信号里拆开。
- 明确不交付自动外呼、短信群发、伪造 age、补 lead、Cookie 后台操作或规避检测。

## 14. QA 清单

上线 aged / recontact 流程前检查：

- 是否保存 original_submit_time、lead_age_bucket 和 timezone。
- Buyer 合同是否允许 aged、shared、recycled lead。
- Payout tier 是否按 age、exclusive/shared、contact result 分开。
- 原始 consent、buyer disclosure 和 certificate 是否可查。
- 是否在每次联系前刷新 DNC、opt-out、suppression。
- Recontact policy 是否有 max attempts、cooldown、allowed hours。
- Aged lead 是否不会进入 fresh lead primary conversion。
- Recycled lead 是否保存原始 buyer、post count 和 reject reason。
- 投诉、DNC、no consent 是否能触发停止和 evidence pack。
- 是否没有自动拨号、短信群发、伪造 timestamp 或隐藏 aged 状态。

## 15. 信息来源 URL

- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads API, LeadFormAsset: https://developers.google.com/google-ads/api/reference/rpc/v19/LeadFormAsset
- Google Ads Help, About call reporting: https://support.google.com/google-ads/answer/2454052
- Google Ads Help, Phone call conversion tracking: https://support.google.com/google-ads/answer/6100664
- Google Ads Help, Conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, About data freshness: https://support.google.com/google-ads/answer/2544985
- Google Ads Policy, Data collection and use: https://support.google.com/adspolicy/answer/6020956
- Google Analytics Help, Avoid sending PII: https://support.google.com/analytics/answer/6366371
- ActiveProspect, TrustedForm: https://activeprospect.com/products/trustedform/
- ActiveProspect, Jornaya TCPA Guardian LeadConduit integration: https://activeprospect.com/leadconduit/integrations/jornaya/tcpa_guardian/
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- FTC, Q&A for Telemarketers & Sellers About DNC: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FCC, TCPA one-to-one consent rule court response / deletion order: https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- eCFR, 16 CFR 310.5 Recordkeeping requirements: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5
- NIST SP 800-122, Guide to Protecting the Confidentiality of PII: https://csrc.nist.gov/pubs/sp/800/122/final
- Aged Lead Sales, TCPA compliance for aged leads: https://agedleadsales.com/blog/tcpa-compliance-calling-aged-leads
- InsureLeads, Aged Lead glossary: https://www.getinsureleads.com/glossary/aged-lead
