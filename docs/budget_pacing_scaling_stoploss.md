# 预算节奏、扩量与止损手册

更新时间：2026-06-08

本文说明 Ads 套利业务里如何设计测试预算、日预算、硬止损、预算节奏、扩量规则、dayparting、geo/device 分层和组合资金分配。目标是让团队用可收款 ROI 和风险证据做预算决策，而不是被短期报表、平台推荐或单日波动带着走。

本文不提供绕过预算限制、规避账单风控、虚假转化、补点击、刷展示、模拟自然流量或用 Cookie 自动改后台预算的方案。

## 1. 为什么预算节奏是套利核心

套利业务的亏损常常不是“模型从一开始就错”，而是预算节奏错：

- 冷启动样本不足，却因为 1 天 ROI 正而猛加预算。
- 收入是 pending / estimated，尚未经历 approved / finalized / paid。
- 广告平台平均日预算允许流量日波动，实际花费可能高于当天预期。
- Smart Bidding / PMax / broad match 在预算加大后探索更多低质流量。
- 扩量同时改素材、页面、国家、设备和出价，导致复盘无法归因。
- 扣量、拒付、invalid traffic 和 buyer feedback 在扩量后才暴露。

预算节奏的本质是控制“未知风险的放大速度”。一个好套利团队不是永远不亏，而是每个未知假设都只用合适大小的钱去验证。

## 2. 预算层级

预算应分层，而不是只看 Google Ads campaign daily budget：

```text
账户现金上限
-> 月度风险预算
-> Offer 测试预算
-> Country / Channel / Device 预算
-> Campaign 日预算
-> Ad Group / Keyword / Creative 样本预算
-> 当日硬止损
```

| 层级 | 控制对象 | 常见错误 |
| --- | --- | --- |
| 账户现金上限 | 最多可承受的广告费和回款缺口 | 用 estimated revenue 当可用现金 |
| 月度风险预算 | 本月允许亏损的测试资金 | 把所有预算押给一个未结算 Offer |
| Offer 测试预算 | 验证一个 payout / page / traffic 组合 | payout 高就直接高预算 |
| Country / Device | 国家、设备、语言、时区差异 | 不分层导致好坏流量混在一起 |
| Campaign | Google Ads 预算和出价策略 | 日预算当成绝对上限 |
| Keyword / Creative | 单个意图或素材角度 | 一个泛词或标题党吃掉测试预算 |
| 当日硬止损 | 当天最大可损失金额 | 等报表晚间回传后才发现超支 |

Google Ads 的平均日预算是平台层面的节奏设置，不是团队的财务风控系统。套利团队必须在平台外维护内部预算表和硬止损。

## 3. 测试预算公式

基础公式：

```text
最小点击样本 = max(统计样本需求, 垂类经验下限)
测试预算 = 最小点击样本 * 预估 CPC
硬止损 = 测试预算 * 1.1 ~ 1.3
安全 CPC = 可收款 RPV * 安全系数
```

CPA/CPL：

```text
可收款 EPC = payout * CVR * approval_rate * paid_rate
测试预算 = max(目标点击 * 预估 CPC, 目标转化数 / CVR * 预估 CPC)
```

展示/AdSense/AdX：

```text
可收款 RPV = finalized_revenue / paid_clicks
测试预算 = 目标 paid clicks * 预估 CPC
```

Search feed / parking：

```text
可收款 RPV = search_action_rate * ad_ctr * rpc * (1 - deduction_rate)
```

建议阶段：

| 阶段 | 预算规则 |
| --- | --- |
| 冷启动 | 只买足够判断追踪、页面和初始 RPV 的样本 |
| 小样本验证 | 达到最小点击或最小转化，但不按当天 ROI 扩量 |
| 质量验证 | 等待一个回传窗口和初步 reject/scrub 反馈 |
| 小幅扩量 | 每次预算增加 10%-30%，保留同一测试结构 |
| 稳定放量 | 至少经历一次结算或稳定 approved/paid 反馈 |

## 4. Pacing 规则

预算 pacing 是决定“今天花多少钱、什么时候停、什么时候等”的过程。

日内 pacing：

- 上午花费过快但无收入：先查 tracking、页面可达和 click_id，不急着加预算。
- 某时段 CPC 激增：记录时段，不立即全局降价。
- 下午/晚上回传延迟明显：不要用午间 ROI 直接停掉全部 campaign。
- 当日花费接近硬止损：暂停或降预算，等收入和日志对齐。

跨日 pacing：

- 新 campaign 至少观察 1-3 天或一个回传窗口。
- 每天只改少数变量，避免预算、出价、素材、页面和目标同时变。
- 扩量后设置 24h、72h、7d 复核点。
- 遇到平台拒登、扣量、付款异常、账号验证、invalid traffic 通知，停止扩量。

月度 pacing：

- 用 paid/finalized/approved 收入更新预算上限。
- 对 estimated/pending 收入打折。
- 给扣量、退款、拒付和资金成本留安全垫。
- 不让单一来源、单一 Offer、单一账号吃掉过高预算占比。

## 5. 放量阶梯

放量不是“ROI 正就加预算”。建议使用阶梯：

| 阶梯 | 条件 | 动作 |
| --- | --- | --- |
| S0 观察 | 页面、追踪、政策、来源未验证 | 小预算，收集点击和日志 |
| S1 保留 | CPC、CTR、RPV 初步合理 | 继续同预算，补样本 |
| S2 小扩 | ROI 正，样本中等，未见扣量 | 预算 +10%-30%，不同时大改结构 |
| S3 稳定 | 已过回传窗口，approved/paid 可信 | 扩关键词、国家、素材或预算 |
| S4 组合扩量 | 多来源、多页面稳定 | 建组合预算上限和来源占比 |
| S5 暂停扩量 | reject、scrub、deduction、policy 或 cash risk 升高 | 停止加预算，先复盘 |

放量顺序：

1. 扩同类长尾关键词，而不是直接上泛词。
2. 扩相邻国家或语言前先审页面、政策和 payout。
3. 扩设备前先看 mobile/desktop RPV、CPC、lead quality 差异。
4. 扩库存前先分清 Search、Search Partners、Display、Demand Gen、PMax。
5. 扩 PMax 前先确认 conversion action 和 URL 控制。

## 6. Dayparting 和时段控制

Ad schedule / dayparting 用于控制广告在一周中哪些日期和时段展示。套利团队应把时段当分析维度，而不是玄学开关。

适合做时段控制的情况：

- Call lead、服务预约、客服跟进有营业时间限制。
- 某些时段 CPC 高、lead reject 高、buyer 接通率低。
- 收入端按工作时间审核或接线，夜间 lead 质量明显差。
- 国家/时区跨区投放，Google Ads 账号时区和用户本地时区不同。

不适合过早 dayparting 的情况：

- 冷启动样本不足。
- 回传延迟超过一天，无法判断小时级 ROI。
- 同时改了关键词、素材、预算和页面。
- 只是因为某个小时没有转化就关闭。

操作原则：

- 先按小时/星期几观察 cost、clicks、CPC、conversion、approved revenue。
- 至少累积多个周期再调时段。
- 调整后保留实验记录，避免把正常波动误判成规律。

## 7. Geo / Device 分层

国家、地区、设备是套利预算最重要的三类分层。它们影响：

- CPC 和竞争强度。
- 语言、页面可信度和本地政策。
- 移动端表单完成率。
- 电话接通、buyer 处理和 lead approval。
- AdSense/AdX RPM、viewability 和广告体验。

Geo 分层：

- 国家不要混在一个预算池，尤其是 payout、语言、政策不同的地区。
- 美国州、加拿大省、英国地区等可在有样本后细分。
- 本地服务、金融、医疗、博彩等要检查地区认证和投放限制。
- 低 CPC 地区如果 paid revenue 低，不能用 gross conversion 扩量。

Device 分层：

- Mobile CTR 高但 RPV 低：常见于误点、页面慢、表单难填或低质量点击。
- Desktop CPC 高但 lead quality 好：可能适合高 intent / B2B / financial lead。
- Tablet 样本小：一般先合并观察，不急着单独预算。
- 设备调整要看 approved / paid revenue，不只看 submitted conversions。

## 8. Bid Adjustment 和预算联动

Bid adjustment 可按设备、地点、时间等维度调整出价。它不是利润修复魔法，而是预算分配工具。

使用前提：

- 该维度有足够样本。
- 指标按同一 revenue 状态对齐。
- 已排除 tracking 断点、页面可达、时区和货币问题。
- 变更有记录，能回滚。

安全公式：

```text
维度安全 CPC = 维度可收款 RPV * 安全系数
建议 bid adjustment = 维度安全 CPC / 当前 CPC - 1
```

示例：

```text
mobile paid RPV = 0.42
desktop paid RPV = 0.90
safety factor = 0.65
mobile safe CPC = 0.27
desktop safe CPC = 0.59
```

如果当前 mobile CPC 是 0.45，desktop CPC 是 0.52，则 mobile 应降价或暂停，desktop 可以保留或小扩。

## 9. 回传延迟和判断窗口

回传延迟是扩量误判的最大来源之一。不同收入端延迟不同：

| 收入端 | 常见延迟 | 扩量含义 |
| --- | --- | --- |
| AdSense estimated | 当日可见 | 不能作为最终收入 |
| AdSense finalized | 次月初 | 可用于长期预算模型 |
| CPA pending | 实时或当日 | 只是事件，不等于批准 |
| CPL buyer feedback | 1-14 天 | 决定 lead 质量和可收款 |
| Offline conversion | 数小时到数天 | 影响 Smart Bidding 学习 |
| 直客付款 | 合同周期 | 决定现金上限 |

判断规则：

- 短回传业务：可用 24-72 小时窗口判断初步 ROI。
- 长回传业务：先用 leading indicators，预算更保守。
- 有 reject/scrub 的业务：扩量前必须等 quality feedback。
- Smart Bidding：primary conversion 越接近 paid/approved，预算越可放大。

## 10. Stop-loss 触发器

立即停量或降预算：

- 达到测试预算且无收入或无有效 postback。
- CPC 高于安全 CPC 20%-30% 且无改善路径。
- RPV 连续下降，且不是回传延迟导致。
- PMax / optimized targeting 扩量后 reject、scrub、投诉或扣量升高。
- Search Partners / Display / placement 出现不可解释低质流量。
- 账号收到 policy、billing、verification、invalid traffic 通知。
- 现金储备低于预设天数。

不要停错：

- 刚上线几个小时没有转化，但历史 lag 通常为 24-48 小时。
- 周末 buyer 不审核，周一集中回传。
- 小样本里单个大额转化导致 ROI 暂时极端。
- 货币、时区或 click_id 映射错误造成收入看似缺失。

## 11. Portfolio 资金分配

套利组合不应只追求单个 campaign ROI，而要控制整体风险：

| 组合规则 | 建议 |
| --- | --- |
| 单 Offer 占比 | 冷启动不超过总测试预算 10%-20% |
| 单账号占比 | 避免一个账号承载全部现金流 |
| 单来源占比 | 未结算前不超过总花费 20%-40% |
| 单国家占比 | 看政策和 payout 稳定性 |
| 单收入方占比 | 避免一个 buyer 或平台拒付拖垮全局 |
| 风险预算 | 高政策风险垂类只用隔离测试预算 |

组合决策看：

- expected profit。
- approved / finalized profit。
- cash gap。
- policy risk。
- invalid traffic risk。
- operational load。

## 12. 系统落地

当前系统支持：

- `/calculators`：用 CPC、CVR、payout、安全系数、目标点击和现金缓冲计算测试预算、硬止损、机会评分。
- `/campaigns`：记录 campaign daily budget、bid strategy、channel、Final URL。
- `/metrics/import`：导入 day、country、device、cost、clicks、conversions、revenue。
- `/optimization`：对 ROI 低、有消耗无收入、CTR 高 RPV 低等情况生成建议。
- `/decision-windows`：记录 data freshness、conversion lag、approval lag、settlement lag、approved/paid revenue 和扩量前成熟度。
- `/budget-pacing`：保存预算节奏评审，计算 Budget Pacing Score、risk_level、recommended_action、increase_percent、remaining_test_budget、remaining_hard_stop 和 blockers。
- `/risk-audits`：记录扣量、回传延迟、预算超限、PMax 扩量、Customer Match 或政策风险。
- `/tasks`：安排日报、周报、关账、链接检查和指标复核。

V1 已实现 `budget_pacing_reviews`，字段包括 offer、campaign draft、current_daily_budget、proposed_daily_budget、test_budget、hard_stop、spend_to_date、approved_revenue、paid_revenue、safe_cpc、actual_cpc、sample_clicks、data_status、revenue_status、source_quality、incident_state、cash_buffer_days、overdelivery_buffer_percent、score、risk_level、recommended_action、increase_percent、remaining_test_budget、remaining_hard_stop、blockers、status、notes 和 source_urls。状态更新写入 `/logs`，只代表内部审批进度，不会自动改 Google Ads daily budget、bid strategy、ad schedule 或后台任何对象。

Budget Pacing Score 的原则：

- 建议预算增加超过 30% 会触发 ramp guardrail。
- data_status 仍是 fresh / partial 时，不允许把短期 ROI 当扩量证据。
- revenue_status 仍是 estimated / submitted / accepted 时，不能把它当可收款利润。
- spend_to_date 接近或超过 hard_stop 时，优先止损或降预算。
- actual CPC 高于 safe CPC 20% 以上时，先修成本、页面或来源，不扩量。
- sample clicks、cash buffer、source quality 和 incident state 都进入阻塞项。

建议后续安全扩展：

- `budget_decision_log`：可从 V1 `budget_pacing_reviews` 拆分为 old_budget、new_budget、safe_cpc、reason、reviewer、approval_time。
- `pacing_rules`：daily_hard_stop、test_budget、cash_stop、review_window。
- `segment_metrics`：hour_of_day、day_of_week、geo、device、network。
- `settlement_metrics`：estimated、approved、finalized、paid、deducted。

不做：

- 不用 Cookie 自动登录后台改预算。
- 不绕过账单、付款或账号安全检查。
- 不用补点击或虚假转化影响出价学习。
- 不用 cloaking、代理或换账号处理低质流量。

## 13. QA 清单

| 检查项 | 放行标准 |
| --- | --- |
| 测试预算 | 有最小样本、预估 CPC、硬止损和现金缓冲 |
| 日预算 | 小于当日可承受损失，考虑 overdelivery |
| 扩量条件 | 已过回传窗口，approved/paid 或 finalized 口径可信 |
| 分层 | country、device、channel、network、campaign 可回溯 |
| Dayparting | 小时/星期数据足够，时区和回传延迟已校正 |
| Bid adjustment | 以可收款 RPV 倒推，不以 gross conversion 决定 |
| PMax / Smart Bidding | primary conversion 接近可收款价值 |
| Stop-loss | 达到阈值可快速暂停、降预算或隔离来源 |
| 审计 | 每次预算提升、降价、停量、扩量有理由和记录 |

## 14. 信息来源 URL

- Google Ads Help, Budgets overview: https://support.google.com/google-ads/answer/10486536
- Google Ads Help, About overdelivery and your average daily budget: https://support.google.com/google-ads/answer/1704443
- Google Ads Help, Budget report: https://support.google.com/google-ads/answer/10702522
- Google Ads Help, Create an account budget: https://support.google.com/google-ads/answer/2375395
- Google Ads API, Account Budget: https://developers.google.com/google-ads/api/docs/billing/account-budgets
- Google Ads Help, About ad scheduling: https://support.google.com/google-ads/answer/6372656
- Google Ads Help, About bid adjustments: https://support.google.com/google-ads/answer/2732132
- Google Ads Help, About location targeting: https://support.google.com/google-ads/answer/1722043
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Time lag report: https://support.google.com/google-ads/answer/6239119
- Google Ads Help, Experiments page: https://support.google.com/google-ads/answer/10682377
- Google Ads Help, About Performance Planner: https://support.google.com/google-ads/answer/9230124
- Google Ads Help, Conversion windows: https://support.google.com/google-ads/answer/3123169
