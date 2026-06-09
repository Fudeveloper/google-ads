# 转化信号质量与出价学习治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何治理 conversion action、conversion goal、primary / secondary、conversion value、offline conversion、enhanced conversion、bid strategy learning 和 bid strategy report。重点不是“有没有转化追踪”，而是“出价系统正在学习什么”。目标是把可收款、可解释、可复盘的 approved / paid / finalized value 作为优化依据，而不是让 Smart Bidding、Broad Match、PMax 或 Demand Gen 学到 submitted lead、误触、重复 postback、gross value 或 pending revenue。本文不提供伪造转化、补点击、刷展示、刷表单、Cookie 后台改 goal、规避 consent、绕过审核或用多账号规避学习事故的方案。

## 1. 为什么转化信号质量决定套利出价学习

Ads 套利不是单纯买点击再看报表。现代 Google Ads 投放越来越多依赖自动化出价、广泛匹配、PMax、Demand Gen、自动资产和推荐系统。这些系统的共同输入是：

```text
auction-time signals
  + conversion action / goal
  + primary or secondary setting
  + conversion value
  + attribution and lag
  + historical quality
  -> bidding and traffic expansion decisions
```

如果 primary conversion 是浅层提交，系统会寻找更多容易提交的人；如果 conversion value 是 gross payout，系统会忽略扣量、拒付和退款；如果多个 Offer 混用一个目标，系统会把不同 payout、国家、buyer quality 和回传延迟混成平均值。套利团队看到的结果通常是：Google Ads conversions 上升，但 approved revenue、paid revenue 或 finalized revenue 没有上升。

因此，转化信号质量是套利行业里比“自动投放按钮”更底层的能力。它决定：

- Smart Bidding 学的是 submitted、qualified、approved 还是 paid。
- tCPA / tROAS 的目标是否由可收款收入倒推。
- Broad Match、AI Max、PMax 是否能安全放量。
- 异常时该等回传、改 goal、降预算还是停源。
- 后台 recommendations 能否进入实验，而不是直接应用。

## 2. 原理解释：Smart Bidding 学的是你喂给它的目标

Smart Bidding 是自动出价策略的一类，围绕转化或转化价值进行优化。套利团队可以把它理解成一个“目标函数执行器”：它不会知道你的真实毛利、buyer 是否拒付、AdSense 是否后续扣量，也不会自动理解哪个 lead 真的能收款。它会使用你配置为可用于出价的 conversion action、goal 和 value 来判断哪些拍卖机会更值得买。

错误目标会产生三种后果：

| 错误目标 | 系统学习结果 | 套利后果 |
| --- | --- | --- |
| Button click / form open 做 primary | 买更多浅层互动 | CTR/CVR 好看，收入差 |
| Submitted lead 做 primary | 买更多低门槛表单 | buyer reject、scrub、投诉上升 |
| Gross payout 做 value | 系统高估 ROI | tROAS 目标虚高，真实利润下滑 |
| 重复 postback 不去重 | 系统以为某些来源价值翻倍 | 预算流向异常 source |
| 多 Offer 共用目标 | 高低质量混合学习 | 好 Offer 被拖累，差 Offer 获量 |
| 回传延迟不稳定 | 近期表现误读 | 频繁改目标导致学习期反复 |

正确原则是：先让系统看见真实业务结果，再给自动化扩量权限。自动出价不是用来修复信号质量的工具；它会放大信号质量。

## 3. 核心对象地图

| 对象 | 含义 | 套利治理重点 |
| --- | --- | --- |
| conversion action | 一个具体转化动作 | 名称、来源、去重、价值、是否用于 bidding |
| conversion goal | 多个 actions 的目标集合 | 是否混入不同质量层级或不同 Offer |
| primary conversion | 用于出价和默认 conversions 列 | 必须接近 qualified / approved / paid |
| secondary conversion | 观察口径，不作为主要出价目标 | 适合 micro event、submitted、诊断事件 |
| conversion value | 转化价值 | 应使用 expected paid value 或 net value |
| offline conversion | 后端或线下结果导入 | 把 CRM / buyer / settlement 状态反馈给 Ads |
| enhanced conversion | 使用哈希用户提供数据增强匹配 | 必须满足同意、政策和数据最小化 |
| attribution window | 转化归因窗口 | 影响短期 CPA/ROAS 判断 |
| conversion lag | 点击到转化、转化到回传的延迟 | 决定等待窗口和扩量节奏 |
| bid strategy report | 自动出价诊断报表 | 看 learning、limited、target changes、top signals |
| change history | 后台变更证据链 | 记录 goal、value、strategy 和 budget 变化 |

## 4. 信号分层：从 Micro Event 到 Paid Revenue

建议把信号分成六层，不要全部塞进一个 conversion action：

| 层级 | 示例 | 适合用途 | 是否适合 primary |
| --- | --- | --- | --- |
| Micro event | scroll、CTA click、search action、form start | 页面诊断、漏斗分析 | 通常不适合 |
| Submitted | 表单提交、电话拨打、chat lead | 冷启动观察、初筛 | 质量稳定前不适合 |
| Accepted | buyer/network 接收 | 初步质量 | 视拒付率谨慎使用 |
| Qualified | 符合资格、可联系、有效需求 | Smart Bidding 候选 | 较适合 |
| Approved | buyer 批准、佣金确认 | tCPA / Max Conversions 候选 | 适合 |
| Paid / finalized | 已付款、最终收入 | tROAS / 组合扩量 | 最适合 |

行业里常见的误判是“有转化量才有学习”。更准确的说法是：有足够高质量、足够稳定、足够接近可收款目标的转化量，自动出价才有意义。如果 submitted lead 很多但 approved rate 低，系统学到的是低质量 lead 的共同特征。

## 5. Signal Quality Score

建议给每个 conversion action 或 goal 计算 `Signal Quality Score`：

```text
signal_quality_score =
  value_closeness_to_paid        25
  match_and_attribution_quality  15
  deduplication_integrity        15
  lag_stability                  10
  sample_volume                  10
  segment_granularity            10
  policy_and_consent_safety      10
  incident_history                5
```

评分说明：

| 维度 | 高分表现 | 低分表现 |
| --- | --- | --- |
| value closeness | value 来自 approved/paid/finalized | value 是 gross payout 或固定猜测 |
| match quality | gclid/gbraid/wbraid/transaction_id 保留完整 | 点击 ID 丢失、归因率波动大 |
| deduplication | transaction_id 去重，重复 postback 被拦截 | thank-you page、server postback 双计 |
| lag stability | 回传延迟可预测，报表等待窗口明确 | 今天快、明天慢，频繁补导 |
| sample volume | 同一 goal 有足够稳定样本 | 低样本下频繁切策略 |
| segment granularity | 按 Offer、country、buyer、page 分层 | 所有垂类混一个目标 |
| policy and consent | 满足 customer data、consent、隐私披露 | PII 进 URL、绕同意、敏感垂类乱传 |
| incident history | 近期无重复、错币种、错 goal | 刚发生目标污染或价值事故 |

动作建议：

| Score | 动作 |
| --- | --- |
| 85-100 | 可用于 tCPA / tROAS / PMax 扩量候选 |
| 70-84 | 可小规模自动出价，但保留预算上限 |
| 55-69 | 只做观察或 Maximize Clicks / Manual CPC 测试 |
| 35-54 | 先修 tracking、value、dedupe、lag |
| 0-34 | 不得作为 primary 或自动出价输入 |

## 6. Primary / Secondary 治理

Primary 和 secondary 不是标签美化，而是出价权限控制。

治理规则：

- Micro event 默认 secondary。
- Submitted lead 默认 secondary，除非历史 approved / paid 质量已稳定。
- Qualified / approved / paid 可进入 primary 候选。
- 不同 payout、国家、buyer、表单质量、回传延迟差异很大的 Offer，不应共用同一个 primary。
- 改 primary/secondary 需要记录原因、日期、影响 campaign 和预期观察窗口。
- 改 goal 后不要立即大幅扩预算，应等待 learning 和 conversion lag。

版本记录建议：

```text
conversion_goal_version:
  goal_name
  included_actions
  primary_actions
  secondary_actions
  effective_from
  affected_campaigns
  expected_lag_days
  reviewer
  reason
  rollback_plan
```

## 7. Value Feedback 设计

Value feedback 要回答一个问题：这个转化对业务真实值多少钱？

推荐口径：

| 场景 | 低质量 value | 推荐 value |
| --- | --- | --- |
| CPL submitted | 全额 payout | payout * expected approval_rate * paid_rate |
| Qualified lead | 固定高价 | buyer/country/source 分层 expected value |
| Approved lead | gross payout | approved payout - expected clawback |
| Sale | 订单毛额 | 扣退款、佣金、税费、拒付后的 net value |
| AdSense / AdX | estimated earnings | finalized 或 paid revenue |
| Search feed | gross RPC/RPM | 扣量后 payable revenue |

示例：

```text
expected_lead_value =
  payout
  * accepted_rate
  * qualified_rate
  * approved_rate
  * paid_rate

net_sale_value =
  gross_revenue
  - refund
  - chargeback
  - affiliate_fee
  - variable_fulfillment_cost
```

价值事故常见原因：

- 币种错，把 USD 当成本地币或反过来。
- value 小数点错。
- postback 重复，value 翻倍。
- 同一 lead 同时进入 submitted 和 approved primary。
- buyer 后续 reject 没有负向或修正反馈。
- estimated revenue 没有在 finalized 后修正。

## 8. Offline Conversion 与 Enhanced Conversion 边界

Offline conversion 的价值在于把广告点击后的后端状态导回系统，例如 qualified、approved、paid、rejected。它适合 CPL、电话线索、线下成交、CRM 审核、affiliate buyer feedback 和延迟结算场景。

安全边界：

- 只导入真实发生、可证明、可去重的转化。
- conversion time 使用真实业务事件时间，时区一致。
- 使用 transaction_id 或等效唯一键防重复。
- 上传结果要保存行数、成功数、错误、match rate 和 diagnostics。
- 不用离线导入伪造不存在的转化，也不为了训练算法补转化。

Enhanced Conversions 用哈希用户提供数据增强匹配。它不是绕过用户同意、恢复被拒绝标识或规避浏览器限制的工具。

治理要求：

- 满足 Google Ads customer data policies。
- 页面和表单有隐私、同意和数据用途披露。
- 不把 PII 放进 URL、UTM、subid 或公开日志。
- 对健康、金融、住房、就业、信贷等敏感垂类额外审查。
- 记录 consent state、数据字段、hash 方式和诊断结果。

## 9. Learning Period 和 Bid Strategy Report

自动出价策略在目标、预算、转化动作、转化价值或流量结构发生重大变化后，通常需要重新学习。套利团队不要把学习期中的短期波动当成最终 ROI，也不要在学习期内连续改多个变量。

Bid strategy report 重点看：

| 项目 | 判断 |
| --- | --- |
| status | 是否 learning、limited、misconfigured 或 stable |
| target changes | tCPA/tROAS 是否频繁改变 |
| conversion delay | 最近数据是否还没回填 |
| top signals | 是否集中到低质量设备、geo、audience |
| budget limited | 是否预算限制导致学习不足 |
| conversion action mix | 是否混入 submitted 或重复转化 |

基本规则：

- 改 conversion goal 前先截图/导出当前 report。
- 改 goal、value 或 bid strategy 后设置观察窗口。
- 观察窗口至少覆盖主要 conversion lag。
- 学习期内避免同时改预算、关键词、页面和目标。
- 若转化污染严重，先冻结扩量，再修信号，不要继续喂错误数据。

## 10. 常见信号污染

| 污染类型 | 表现 | 诊断 | 修复 |
| --- | --- | --- | --- |
| double fire | conversions/value 暴涨 | tag、server postback、thank-you page 重复 | 去重、保留原始记录、修 action |
| shallow primary | lead 数量涨，paid revenue 不涨 | submitted / micro event 是否 primary | 降为 secondary，导入 approved |
| gross value | tROAS 看似稳定，利润差 | gross、net、paid 口径混用 | 改 expected/net value |
| wrong currency | value 异常倍增或缩小 | currency、timezone、source 文件 | 修映射，重跑导入 |
| stale value | buyer payout 已变，value 未变 | payout version、effective date | 按版本回填 |
| mixed offers | 某 campaign 学到错误人群 | goal action 混多个垂类/国家 | 分 goal 或分 campaign |
| delayed reject | 扩量后才发现拒付 | reject/scrub 延迟 | 等待窗口，降低预算 |
| low match rate | offline conversion 归因少 | click ID、window、time、consent | 修追踪链和导入格式 |
| source pollution | 某 source 高转化低质量 | source/subid buyer feedback | 停源、隔离、拉入 watchlist |

原则：数据修复要保留原始记录、修正记录和解释。不要删除坏数据假装没发生，也不要用补点击、补转化或新账号覆盖事故。

## 11. 自动出价准入矩阵

| 策略 / 流量 | 最低信号要求 | 不满足时的替代 |
| --- | --- | --- |
| Manual CPC | 可追踪 click、cost、基本 revenue | 小预算测试 |
| Maximize Clicks with cap | 页面和 source 质量可控 | 先买样本，不看短期转化 |
| Maximize Conversions | primary 接近 qualified/approved，样本稳定 | 保持 capped clicks 或 manual |
| Target CPA | approved CPA 可估，拒付率稳定 | 先导入 approved/paid |
| Maximize Conversion Value | value 可信，去重和币种稳定 | 用内部 ROI 建议，不给出价系统 |
| Target ROAS | paid/finalized value 稳定，lag 可预测 | 继续小额测试 |
| Broad Match / AI Max | high-quality primary、否定词、search term 复盘 | phrase/exact 分层测试 |
| PMax / Demand Gen | conversion value 接近可收款，URL/asset/report 可复盘 | Search 小规模验证 |

准入不是一次性门槛。每次更换 Offer、buyer、国家、页面、source 或 payout，都要重新评估。

## 12. 信号事故响应

当发现 conversions/value 异常、primary 配错、重复 postback、gross value 误导或 paid revenue 断层时，按下面顺序处理：

```text
detect anomaly
-> freeze scale
-> preserve raw evidence
-> identify polluted actions and affected campaigns
-> move shallow or polluted action to secondary if needed
-> isolate source / offer / page / buyer segment
-> import corrected value or status where allowed
-> wait for lag and learning window
-> record postmortem and guardrail
```

不要做：

- 不用虚假转化“平滑”学习期。
- 不用补点击或刷展示修复 CVR。
- 不删除原始事故记录。
- 不通过换账号、换域名、cloaking 或 Cookie 后台操作绕开历史问题。
- 不在未解释污染前直接把预算加到另一个黑盒 campaign。

## 13. 系统落地

当前系统可承接 V1：

| 行业动作 | 系统位置 |
| --- | --- |
| 评审 conversion goal/action、primary、value、match、dedupe、lag、policy、diagnostics 和 bid readiness | `/conversion-signals` |
| 导入 cost、clicks、conversions、revenue | `/metrics/import` |
| 用 ROI、RPV、CVR 生成优化建议 | `/optimization` |
| 记录 Offer payout、tracking URL、policy notes | `/offers` |
| 记录转化、出价、官方文档和来源 URL | `/sources` |
| 记录 conversion signal 污染、goal 变更、拒付和事故 | `/risk-audits` |
| 导出 CSV/Scripts payload 让授权人审查 | `/campaigns` |
| 记录自动化任务和审计日志 | `/tasks`、`/logs` |

V1 已实现 `conversion_signal_reviews`，保存 conversion goal/action、action stage、primary/secondary、recommended primary status、value mode、weekly approved/paid、click ID coverage、offline match rate、duplicate rate、conversion lag、policy/consent、customer data、offline import diagnostics、transaction_id、bid strategy report、Signal Quality Score、bid readiness、expected paid value、safe target CPA、blockers、状态流和 source_urls；状态更新写入 `audit_logs`，不自动上传 offline conversion、不自动改 Google Ads goal、primary/secondary 或出价。

后续可拆分表：

```text
conversion_signal_definitions
conversion_goal_versions
conversion_signal_quality_daily
offline_conversion_import_runs
offline_conversion_import_errors
bid_strategy_learning_snapshots
conversion_value_adjustments
conversion_signal_incidents
conversion_goal_change_evidence
```

字段示例：

```text
conversion_signal_definitions:
  action_name, goal_name, event_layer, primary_state,
  value_mode, value_source, dedupe_key, owner,
  expected_lag_days, consent_requirements, policy_notes

conversion_signal_quality_daily:
  day, action_name, offer_id, campaign_id, country,
  submitted, qualified, approved, paid, rejected,
  gross_value, expected_value, paid_value,
  duplicate_rate, match_rate, lag_p50_hours,
  signal_quality_score, decision

bid_strategy_learning_snapshots:
  campaign_id, strategy_type, target_cpa, target_roas,
  status, status_reason, top_signals, conversion_lag_note,
  captured_at, evidence_url
```

系统只生成定义、评分、事故和审批任务，不自动登录 Ads 后台、不接管 Cookie、不自动改 conversion goal、不伪造转化、不刷量、不绕过 consent 或审核。

## 14. ADXKit 对应点和完成形态

ADXKit 类工具常强调“自动投放、自动优化、自动换链接、批量测 Offer”。转化信号质量治理对应的是：给所有自动化加一层训练数据闸门。

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| 自动优化 | 优化前检查 primary / value / lag / dedupe |
| 自动投放 | 只有高分 signal 才允许进入扩量候选 |
| AI 创意生成 | 创意 winner 必须用 paid/approved revenue 回写 |
| 换链接 | link_version 变更后观察 conversion quality，不做 cloaking |
| 任务中心 | 生成 signal QA、offline import、learning report 复盘任务 |
| ROI dashboard | 同时展示 Google Ads conversions 和 approved/paid revenue |

功能拆解和安全完成清单：

- 完成转化信号原理解释。
- 完成 signal layer、primary/secondary、value feedback 和 learning period 的操作模型。
- 完成 Signal Quality Score、准入矩阵、事故响应和 `/conversion-signals` V1 工作台。
- 完成来源 URL、来源库、系统设计和验收入口。
- 不实现 Cookie 后台修改 conversion action。
- 不实现伪造 conversion、补点击、刷展示或模拟自然流量。
- 不实现通过代理、指纹、Worker、cloaking 或账号切换规避系统学习和审核。

## 15. QA 清单

上线或扩量前检查：

- 每个 primary conversion 是否接近 qualified、approved、paid 或 finalized。
- submitted、CTA click、scroll、form start 是否保持 secondary。
- conversion value 是否使用 expected/net/paid 口径，而不是 gross payout。
- transaction_id 或等效键是否能去重。
- gclid/gbraid/wbraid、UTM、click_id 是否在跳转链中保留。
- offline conversion import 是否有错误、match rate 和 diagnostics。
- enhanced conversion 是否满足 customer data、consent 和隐私披露。
- conversion lag 是否进入扩量等待窗口。
- bid strategy report 是否处于稳定状态，而不是 learning / limited / misconfigured。
- Change history 是否记录 goal、value、budget、strategy 和 URL 变更。
- Broad Match、AI Max、PMax 或 Demand Gen 是否有足够高质量 primary 和 paid revenue 证据。
- 近期是否存在 double fire、wrong currency、gross/net 混用、duplicate postback 或 buyer reject 激增。
- 事故修复是否保留原始证据和 postmortem。
- 是否明确禁止用补点击、伪造转化、Cookie 后台操作或换账号来修复信号事故。

## 16. 信息来源 URL

- Google Ads Help, About Smart Bidding: https://support.google.com/google-ads/answer/7065882
- Google Ads Help, Determine a bid strategy based on your goals: https://support.google.com/google-ads/answer/2472725
- Google Ads Help, About primary and secondary conversion actions: https://support.google.com/google-ads/answer/11461796
- Google Ads Help, About conversion goals: https://support.google.com/google-ads/answer/10995103
- Google Ads Help, About conversion measurement: https://support.google.com/google-ads/answer/1722022
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads Help, Fix discrepancies and errors in offline conversion imports: https://support.google.com/google-ads/answer/13321563
- Google Ads Help, About enhanced conversions: https://support.google.com/google-ads/answer/9888656
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Find your bid strategy reports: https://support.google.com/google-ads/answer/7074568
- Google Ads Help, Evaluate automated bid strategy performance: https://support.google.com/google-ads/answer/10167267
- Google Ads Help, Use broad match with Smart Bidding: https://support.google.com/google-ads/answer/12159290
- Google Ads Help, About Performance Max campaigns: https://support.google.com/google-ads/answer/10724817
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
- Google Ads API, Bidding strategy types: https://developers.google.com/google-ads/api/docs/campaigns/bidding/strategy-types
