# CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册

更新时间：2026-06-09

本文解释 CPL / CPA / Call Lead / Appointment Lead arbitrage 中，如何把 CRM stage、buyer feedback、affiliate postback、invoice、paid revenue 映射成 Google Ads 可学习的 conversion action、primary / secondary、offline conversion、conversion value、conversion adjustment 和诊断报表。它承接 [转化追踪、价值回传与 Attribution 手册](conversion_tracking_value_feedback.md)、[转化信号质量与出价学习治理手册](conversion_signal_quality_bidding_learning_governance.md)、[Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md) 和 [决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md)，重点回答：后端哪些状态可以回传给 Ads，回传成什么事件、什么 value、什么时候可用于出价，以及 rejected / returned 如何避免污染学习。

本文不提供伪造 offline conversion、补 postback、刷表单、模拟成交、Cookie 后台操作、绕过 consent、隐藏低质来源或规避账号封禁的方案。系统只做字段映射、导入 QA、诊断、审计、来源 URL 和人工审批。

## 1. 为什么 CRM 阶段映射决定自动出价质量

Google Ads 自动化无法直接知道你的 buyer 是否真的付款。它只能学习你回传给它的目标：

```text
ad click
-> lead submitted
-> CRM stage
-> buyer feedback
-> offline conversion import
-> Google Ads bidding signal
```

如果 stage mapping 错了，会出现：

- submitted lead 很多，buyer paid 很少，但 Smart Bidding 继续放大低质来源。
- accepted 被当成 approved，return window 后大批 scrub。
- qualified 和 paid 混成一个 conversion action，value 口径不稳定。
- rejected / returned 没有修正，历史低质来源继续获得预算。
- 同一 lead 的 submitted、qualified、approved 各上传一次且都 primary，系统重复计值。
- buyer feedback 延迟时，投手用当天 conversions 过早扩量。

正确的 CRM 映射目标是：让 Ads 学到更接近真实可收款价值的信号，同时保留浅层事件用于诊断，而不是把所有状态都当成正向转化。

## 2. 原理解释：CRM Stage 不是 Ads Conversion Action

CRM stage 是业务生命周期，Ads conversion action 是广告系统的学习输入。两者不能一比一硬套。

| CRM / Buyer stage | 业务含义 | Ads 信号建议 |
| --- | --- | --- |
| form_started | 用户开始表单 | 内部诊断，不上传或 secondary |
| submitted | 用户提交 | secondary，冷启动观察 |
| validated | 基础校验通过 | secondary 或内部质量事件 |
| accepted | buyer 接收 | early signal，谨慎使用 value |
| contacted | buyer 联系成功 | 可作为 lead quality 候选 |
| qualified | 符合买方资格 | primary 候选 |
| appointment_scheduled | 预约成功 | appointment 模式 primary 候选 |
| approved / billable | 可计费或批准 | primary / value feedback 候选 |
| paid | 实际付款 | mature value 和扩量依据 |
| rejected / returned | 拒付或退回 | 不上传正向；用于 adjustment 或内部负反馈 |

一个良好的 mapping 层会把 CRM 事件拆成三类：

```text
diagnostic events: form_start, submitted, validation_pass
optimization events: qualified, approved, billable
settlement events: paid, returned, clawback
```

诊断事件帮助找问题；优化事件帮助出价；结算事件帮助预算和价值校准。不要让诊断事件直接主导出价。

## 3. 核心对象地图

| 对象 | 作用 | 套利关注点 |
| --- | --- | --- |
| lead_id | 内部 lead 唯一 ID | 连接表单、CRM、buyer、postback |
| click_id / gclid / gbraid / wbraid | 广告点击或互动标识 | Offline conversion 匹配 |
| transaction_id | 转化去重 ID | 防重复上传和状态更新 |
| crm_stage | CRM 当前阶段 | 不能直接等于 Ads 事件 |
| buyer_status | accepted、qualified、approved、paid、returned | 真实质量和收入 |
| conversion_action_map | stage 到 Ads action 的映射 | primary/secondary 和命名治理 |
| value_mode | zero、expected、approved、paid、net | 控制 tROAS 学习 |
| import batch | 每次上传文件或 API run | QA、错误、match rate、回滚 |
| adjustment event | value 修正、retraction、restatement | 处理 return、refund、clawback |
| lag profile | stage 到回传的延迟分布 | 决定等待窗口和扩量节奏 |
| diagnostics | 导入错误、匹配率、重复率 | 防止信号断层 |

## 4. Stage Taxonomy：先统一业务阶段

建议先定义内部标准阶段，再映射各 buyer 的字段：

| 标准阶段 | 来源字段示例 | 说明 |
| --- | --- | --- |
| submitted | form_submit、lead_created | 用户提交或电话线索生成 |
| validation_pass | valid_phone、not_duplicate、geo_ok | 基础校验通过 |
| accepted | buyer_accepted、post_success | buyer 初步接收 |
| initial_reject | buyer_reject、cap_reached | buyer 初始拒收 |
| contacted | call_connected、email_replied | 有效联系 |
| qualified | qualified_lead、valid_call、meets_criteria | 符合业务资格 |
| approved | approved、billable、payable | 可计费或批准 |
| paid | paid、settled、remitted | 实际付款到账 |
| returned | returned、scrubbed、voided | 退回或扣量 |
| dispute_open | disputed、appeal_open | 争议中 |
| final_closed | final_accepted、final_rejected | 争议或结算终态 |

每个 buyer 字段都要映射到标准阶段，而不是直接进入 Ads：

```text
buyer_a.status = "A" -> accepted
buyer_b.disposition = "QL" -> qualified
network.status = "approved" -> approved
invoice.line_status = "paid" -> paid
```

这个映射必须版本化，因为 buyer 改字段、改 reason code 或改审核规则，会改变 Ads 学习输入。

## 5. Ads Conversion Action Mapping

建议命名：

```text
lead_submitted_{vertical}_{geo}
lead_accepted_{vertical}_{geo}
lead_qualified_{vertical}_{geo}
lead_approved_{vertical}_{geo}
lead_paid_{vertical}_{geo}
```

Mapping 矩阵：

| 标准阶段 | action | primary | value | 用途 |
| --- | --- | --- | --- | --- |
| submitted | lead_submitted_* | 否 | 0 或低 expected | 漏斗观察 |
| validation_pass | lead_validated_* | 否 | 0 或低 expected | 表单质量诊断 |
| accepted | lead_accepted_* | 谨慎 | expected accepted value | 冷启动 early signal |
| contacted | lead_contacted_* | 视垂类 | expected qualified value | 电话/销售质量 |
| qualified | lead_qualified_* | 可 | expected paid value | 自动出价候选 |
| approved | lead_approved_* | 可 | approved payout - expected return | tCPA/tROAS 候选 |
| paid | lead_paid_* | 可 | paid net value | 成熟价值校准 |
| returned | none / adjustment | 否 | negative adjustment 或 retract | 修正历史价值 |

原则：

- 同一 campaign 的 primary 不应同时包含 submitted 和 approved。
- 不同 payout、geo、buyer、垂类差异大时拆 action 或至少拆 value source。
- accepted 可用作 early signal，但不能在 scrub 不稳定时作为唯一 primary。
- paid 延迟长，适合 value calibration 和扩量依据，不一定适合冷启动唯一信号。

## 6. Value Mode 和金额口径

Value mode 建议分层：

| mode | 公式 | 使用场景 |
| --- | --- | --- |
| zero | 0 | 只记录 event，不参与 value |
| expected | payout * p(approved) * p(paid) | 早期 qualified / accepted |
| approved | approved_amount - expected_return | 已批准但未过 return window |
| paid | paid_amount | 实际付款到账 |
| net | paid - refund - clawback - variable_cost | tROAS 和组合利润 |

示例：

```text
accepted_expected_value =
  payout * historical_qualified_rate * historical_approval_rate * historical_paid_rate

approved_expected_value =
  approved_payout * (1 - expected_return_rate)

net_paid_value =
  paid_amount - refund - chargeback - variable_cost
```

value 不能只用 headline payout。至少要按以下维度校准：

- buyer。
- vertical。
- country / state。
- source / publisher / placement。
- form version。
- return window。
- payment term。
- paid rate。

## 7. Transaction ID、去重和状态更新

每个可回传事件必须有稳定去重键。

推荐：

```text
transaction_id = lead_id + ":" + conversion_stage
```

如果同一 lead 的 qualified、approved、paid 是不同 conversion action，可以各自有不同 transaction_id。不要让同一 action 重复上传同一个 transaction_id。

状态更新原则：

- pending 到 approved 是状态迁移，不是新增 submitted。
- approved 到 returned 应通过 adjustment 或内部价值修正处理。
- 同一 stage 重跑导入必须 idempotent。
- file hash、row hash、payload hash 要保存，便于证明没有重复上传。
- 错误修复要保留原始 batch，不覆盖历史证据。

## 8. Conversion Adjustment、Return 和 Clawback

当后续出现 return、refund、clawback 或误传 value 时，需要修正，而不是继续上传正向转化掩盖。

常见调整：

| 情况 | 动作 |
| --- | --- |
| buyer return lead | 调低 approved value 或撤回对应 conversion |
| refund / chargeback | 上传价值调整或内部 net value 修正 |
| duplicate upload | 使用 transaction_id 排查并修正重复批次 |
| wrong currency | 重新计算并记录 corrected batch |
| wrong conversion time | 记录事故，修正导入规则 |
| accepted 后未 qualified | 不上传 approved/paid；保留 early signal 质量下降 |

调整策略要谨慎：不是所有平台和 action 都适合频繁调整。系统至少要内部保存 returned / rejected 负反馈，并在预算和 source score 中扣减。

## 9. Import Batch QA 和 Diagnostics

每次 offline import 都要保存：

```text
batch_id
source_file_name
source_file_hash
row_count
unique_transaction_count
conversion_action
date_range
timezone
uploaded_at
success_count
error_count
partial_failure
match_rate
diagnostics_url_or_snapshot
reviewer
```

QA 清单：

- conversion action 是否正确。
- conversion time 是否用业务事件时间，而不是上传时间。
- currency 是否一致。
- transaction_id 是否去重。
- click_id 是否来自真实广告点击。
- 是否过滤 rejected、returned、suppressed、duplicate。
- value mode 是否符合当前阶段。
- 是否保存错误行和修复结果。
- 是否在 Google Ads diagnostics 中检查 match/error。

导入失败时，不要用凭空生成 click ID、指纹、代理或 Cookie 去补匹配率。修正应该回到 tracking chain、表单保存、同意、跳转链和字段合同。

## 10. Lag Profile 和导入节奏

不同阶段的回传延迟不同：

| 阶段 | 典型延迟 | 使用建议 |
| --- | --- | --- |
| submitted | 分钟到小时 | 诊断，不直接放量 |
| accepted | 小时到 1 天 | early signal，需折扣 value |
| qualified | 1-7 天 | 初步出价候选 |
| approved | 3-30 天 | 主要优化依据 |
| paid | 15-60+ 天 | 预算和价值校准 |
| returned | return window 内 | 负反馈和 source score |

导入节奏建议：

```text
daily: qualified / approved preliminary import
weekly: return and adjustment review
monthly: paid / invoice reconciliation import
after close: mature value calibration
```

不要因为 paid 太慢就把 submitted 永久设为 primary。可以使用 expected value early signal，但必须用成熟 cohort 校准。

## 11. Buyer Feedback 到优化动作

把 buyer feedback 映射成动作：

| 反馈 | Ads / 运营动作 |
| --- | --- |
| accepted 高，qualified 低 | 降 submitted 权重，检查关键词意图和表单问题 |
| invalid phone 高 | 修输入验证，不补造号码 |
| bad geo 高 | 修 location targeting、landing copy、geo field |
| duplicate 高 | 排查 source、再营销、跨 buyer 重复 |
| low intent 高 | 修创意承诺、CTA、disclosure |
| approved 高，paid 慢 | 控制 cash buffer，不急扩 |
| returned 高 | 调低 expected value，source 进 watchlist |
| complaint 高 | 暂停 source/creative，审 consent 和 disclosure |

不要把 buyer feedback 只存在聊天记录里。它必须回写到 lead、source、campaign、landing、creative、form version 和 conversion action map。

## 12. 系统落地

当前 V1 可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 评审 CRM stage、buyer feedback、conversion action、value mode、transaction_id、import QA 和 adjustment | `/crm-value-mapping` |
| 保存来源和 Google Ads / buyer feedback 文档 | `/sources` |
| 导入聚合 cost、conversions、revenue | `/metrics/import` |
| 记录 rejected、returned、scrub、mapping incident | `/risk-audits` |
| 生成 stop-loss、quality review、signal QA 建议 | `/optimization` |
| 创建 offline import QA、invoice close、value calibration 任务 | `/tasks` |
| 在 docs 中管理 mapping SOP | `/knowledge/crm_value_mapping` |

V1 已实现 `crm_value_mapping_reviews`，保存 source system、buyer feedback source、source stage、standard stage、buyer status、conversion action role、primary recommendation、value mode、payout、approved/paid/return rate、transaction_id、import QA、diagnostics、adjustment rule、PII/consent、CRM Mapping Score、recommended upload policy、expected value、blockers、状态流和 source_urls；状态更新写入 `audit_logs`，不自动上传 offline conversion、不自动改 primary/secondary、不自动改 value 或广告后台。

后续可拆分表：

```text
crm_stage_maps
buyer_feedback_stage_maps
conversion_action_maps
offline_conversion_import_batches
offline_conversion_import_rows
conversion_value_versions
conversion_adjustment_events
conversion_diagnostics_snapshots
lead_value_calibration_runs
crm_ads_signal_incidents
```

核心字段：

```text
conversion_action_maps:
  vertical, geo, buyer_id, crm_stage, standard_stage,
  conversion_action_name, primary_recommendation,
  value_mode, expected_value_formula, effective_from,
  reviewer, source_urls

offline_conversion_import_batches:
  batch_id, source_system, source_file_hash, date_range,
  conversion_action, row_count, success_count, error_count,
  match_rate, diagnostics_ref, uploaded_by, reviewed_by

conversion_adjustment_events:
  transaction_id, conversion_action, adjustment_type,
  old_value, new_value, reason_code, evidence_ref,
  adjustment_time, reviewer
```

系统不自动上传、不自动改 primary、不自动修正历史、不生成 lead 或 postback，只做 mapping、QA、诊断、建议和人工审批。

## 13. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| 自动优化 | 用 qualified/approved/paid mapping 生成建议，不让 submitted 主导 |
| ROI 看板 | 展示 stage funnel、value mode、match rate、lag profile |
| 自动投放 | 使用人工审批的 conversion action map 和 value mode |
| 创意优化 | winner 依据 mature paid/approved value，而不是 CTR 或 submit |
| 换链接 | 换前确认 buyer、stage、postback、value mapping 不断 |
| 任务自动化 | 生成 offline import QA、diagnostics review、adjustment review |

完成标准：

- 能解释 CRM stage、buyer status、Ads conversion action 的区别。
- 能给出 submitted、accepted、qualified、approved、paid 的映射矩阵。
- 能解释 expected、approved、paid、net value 的使用场景。
- 能记录 transaction_id、batch hash、diagnostics、match rate 和错误行。
- 能处理 returned/rejected 的负反馈，不用补 postback 或伪造转化。
- 完成 `/crm-value-mapping` V1 工作台、CRM Mapping Score、upload policy、expected value、blockers 和状态审计。

## 14. QA 清单

上线或改 mapping 前检查：

- 每个 conversion action 是否有 owner、stage、value mode 和 source evidence。
- submitted 是否仍是 secondary 或低权重。
- qualified / approved / paid 是否来自真实 CRM 或 buyer feedback。
- transaction_id 是否稳定且去重。
- conversion time 是否是真实业务时间。
- value 是否按 buyer、geo、vertical、source 校准。
- rejected、returned、suppressed、duplicate 是否被排除或修正。
- import batch 是否保存 file hash、row count、error、match rate。
- diagnostics 是否检查并存档。
- 改 primary/value 后是否有观察窗口和 rollback plan。
- 是否没有把 PII 写入 URL、subid、日志、prompt 或公开报表。
- 是否没有通过 Cookie 后台、代理、指纹或绕过 consent 改善匹配率。

## 15. 信息来源 URL

- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads API, Enhanced conversions for leads: https://developers.google.com/google-ads/api/docs/conversions/enhanced-conversions/leads
- Google Ads API, Upload conversion adjustments: https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments
- Google Ads Help, About conversion tracking: https://support.google.com/google-ads/answer/1722022
- Google Ads Help, About conversion goals: https://support.google.com/google-ads/answer/10995103
- Google Ads Help, Set up enhanced conversions for leads: https://support.google.com/google-ads/answer/11021502
- Google Ads Help, Fix discrepancies and errors in offline conversion imports: https://support.google.com/google-ads/answer/13321563
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Time lag report: https://support.google.com/google-ads/answer/6239119
- Google Ads, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google tag, Consent mode overview: https://developers.google.com/tag-platform/security/concepts/consent-mode
- Google Analytics, Data freshness: https://support.google.com/analytics/answer/11198161
- FTC, Protecting Personal Information: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- FTC, Follow the Lead workshop: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- Voluum, Conversion Status: https://doc.voluum.com/article/conversion-status
- Voluum, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
