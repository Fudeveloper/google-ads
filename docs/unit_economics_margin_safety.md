# 单位经济模型、Break-even 与安全边际手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何用 CPC、RPV、EPC、RPM、CVR、payout、approval rate、deduction、conversion lag、cash buffer 和 safety factor 构建单位经济模型。目标是让团队在测试前知道“最高能买多贵的点击、最少要买多少样本、亏到哪里必须停、什么时候只是等待回传”，而不是只看后台推荐预算、平台优化分、单日 ROI 或 gross revenue。本文不提供补点击、刷展示、伪造转化、伪造收入、隐藏来源、cloaking、Cookie 后台改报表或封禁后换账号继续投放的方案。

## 1. 为什么单位经济是套利第一性原理

Ads 套利的本质不是“流量越多越好”，而是每一个付费点击是否能以足够概率转化为可收款收入：

```text
paid click cost
  -> landing arrival
  -> monetization event
  -> approved / finalized / paid revenue
  -> profit after risk discount
```

如果一个点击的真实可收回价值是 0.42 美元，而你花 0.60 美元购买它，再强的自动化也只会加速亏损。反过来，如果真实可收回价值是 0.70 美元，但回传延迟和扣量没有进入模型，团队也可能因为当天 ROI 难看而过早停掉好流量。

单位经济模型回答四个问题：

- Break-even：理论上最高能买多贵的点击。
- Safety margin：在扣量、拒付、延迟和波动后还剩多少安全垫。
- Test budget：为了获得可判断样本，愿意承担多少测试成本。
- Scale gate：什么证据证明可以扩量，而不是运气好。

## 2. 原理解释：利润来自可收款 RPV，而不是报表好看

基础公式：

```text
profit = revenue - cost
roi = profit / cost
roas = revenue / cost
rpv = revenue / paid_clicks
break_even_cpc = payable_rpv
safe_cpc = payable_rpv * safety_factor
safety_margin = (safe_cpc - actual_cpc) / safe_cpc
```

关键是 `revenue` 必须使用正确口径：

| 口径 | 能否用于扩量 |
| --- | --- |
| gross revenue | 只能做早期趋势 |
| reported revenue | 需要折扣 |
| pending revenue | 不宜直接扩量 |
| approved revenue | 可小幅扩量 |
| finalized revenue | 可作为成熟决策 |
| paid revenue | 可作为现金预算依据 |

单位经济模型不是追求精确到小数点，而是避免方向性错误：用 gross 当 net、用 submitted 当 paid、用 sessions 当 ads clicks、用 estimated 当 cash。

## 3. 核心对象地图

| 对象 | 含义 | 影响 |
| --- | --- | --- |
| paid click | 买量侧计费点击 | CPC、测试成本 |
| landing session | 实际到达页面的会话 | arrival rate、页面损耗 |
| monetization event | out click、ad request、lead、sale | CVR、RPM、EPC |
| revenue status | reported/pending/approved/finalized/paid | 是否能扩量 |
| deduction | 扣量、拒付、退款、无效流量 | 净收入 |
| lag profile | 回传、批准、结算和付款延迟 | 决策窗口 |
| safety factor | 风险折扣 | Safe CPC 和预算上限 |
| cash buffer | 可承受垫资天数 | 测试规模和回款风险 |
| sample size | 点击、转化、收入样本 | 误判概率 |

这些对象如果没有字段和版本，团队只能靠感觉判断“这个 Offer 还能不能跑”。

## 4. 三种业务模型公式

### 4.1 Display / AdSense / AdX 内容套利

```text
session_rpv = finalized_session_rpm / 1000
ads_click_rpv = session_rpv * landing_arrival_rate
safe_cpc = ads_click_rpv * safety_factor
```

如果 `session_rpm = 60`，`landing_arrival_rate = 0.80`：

```text
session_rpv = 60 / 1000 = 0.060
ads_click_rpv = 0.060 * 0.80 = 0.048
safe_cpc at 0.65 = 0.0312
```

内容套利通常 margin 很薄，不能只看当天 estimated RPM。必须看 finalized、deduction、viewability、ad density、CLS、source quality 和 invalid traffic 风险。

### 4.2 CPA / CPL Lead 套利

```text
gross_epc = payout * submitted_cvr
approved_epc = payout * submitted_cvr * approval_rate
paid_epc = payout * submitted_cvr * approval_rate * paid_rate
safe_cpc = paid_epc * safety_factor
```

如果 `payout = 45`，`submitted_cvr = 2%`，`approval_rate = 60%`，`paid_rate = 90%`：

```text
gross_epc = 45 * 0.02 = 0.90
paid_epc = 45 * 0.02 * 0.60 * 0.90 = 0.486
safe_cpc at 0.65 = 0.3159
```

如果团队只用 gross EPC 0.90 出价，实际会把 CPC 上限高估接近 3 倍。

### 4.3 Search Feed / RSOC / Parking

```text
search_action_rpv =
  search_action_rate
  * ad_click_rate
  * rpc
  * (1 - deduction_rate)

safe_cpc = search_action_rpv * safety_factor
```

Search feed 不能只看 gross RPC 或 funnel RPM。query intent、RAC / 上游创意、content page、deduction、partner terms 和 payable revenue 都会影响真实 RPV。

## 5. Safety Factor 设计

Safety factor 是风险折扣，不是随便填的保守数字。

建议范围：

| 场景 | safety factor |
| --- | --- |
| 新 Offer / 新 source / 新页面 | 0.35-0.55 |
| 有初步 submitted，但 approved 未稳定 | 0.45-0.60 |
| approved revenue 稳定，paid 未完成 | 0.55-0.70 |
| finalized / paid 稳定一个结算周期 | 0.65-0.85 |
| 长期 Core，扣量低，现金强 | 0.75-0.90 |

Safety factor 应考虑：

- revenue status 是否成熟。
- conversion / revenue lag 长度。
- deduction、reject、refund、chargeback。
- source quality 和 invalid traffic。
- policy risk 和页面质量。
- cash buffer 和回款周期。
- 样本量和方差。

安全系数不是为了让模型好看；它是为了让错误估计不会立刻烧穿现金。

## 6. Margin of Safety

`Safety Margin` 衡量实际 CPC 距离安全上限还有多远：

```text
safety_margin = (safe_cpc - actual_cpc) / safe_cpc
```

解释：

| Safety Margin | 判断 |
| --- | --- |
| > 30% | 有较好缓冲，可小测或保守扩量 |
| 10%-30% | 可测试，但要严格等待窗口和止损 |
| 0%-10% | 接近红线，只能小样本 |
| < 0% | CPC 超过安全上限，不应扩量 |

注意：margin 高不一定能扩量。还要看来源是否合规、样本是否足够、收入是否 matured、cash buffer 是否覆盖回款周期。

## 7. Sensitivity Analysis

套利模型最容易被四个变量击穿：

| 变量 | 小变化造成的影响 |
| --- | --- |
| CPC | 成本线性上升，薄利模型最敏感 |
| CVR / approval rate | CPA/CPL paid EPC 快速下滑 |
| RPM / RPC | 内容和 search feed 收入波动 |
| deduction / reject | gross 好看但 payable 变差 |

测试前建议做三档情景：

```text
base_case:
  cpc, cvr, rpm, approval_rate 使用当前估计

bad_case:
  cpc +20%
  cvr or rpm -20%
  deduction +10%

stress_case:
  cpc +30%
  approval_rate -30%
  payment lag +15 days
```

只有 base case 盈利不够；bad case 不能迅速爆亏，才值得进入真实买量测试。

## 8. Test Budget 和硬止损

测试预算不是“今天愿意花多少”，而是为了取得最小判断样本愿意承担的风险。

```text
min_sample_clicks =
  max(100, expected_conversions_needed / expected_cvr)

test_budget = min_sample_clicks * actual_cpc
hard_stop = test_budget * 1.2
```

CPA/CPL 建议至少追求 3-5 个预期有效转化的样本；Display / AdSense / AdX 要覆盖多个时段、设备和 source segment；高延迟 Offer 要拆开 Freshness Window、Conversion Window 和 Settlement Window。

硬止损规则：

- cost 达到 hard_stop 且没有成熟收入证据：停止扩量，进入诊断。
- CPC 超过 safe_cpc：不扩量，先降成本或提高 RPV。
- submitted 好但 approved 差：停源或降预算。
- estimated 好但 finalized 差：重算 safety factor 和 deduction。
- tracking / URL / consent 断：立即停，不等待样本。

## 9. Break-even 决策矩阵

| 情况 | 判断 | 动作 |
| --- | --- | --- |
| actual_cpc < safe_cpc，收入 matured | 经济模型可行 | 小幅扩量 |
| actual_cpc < safe_cpc，收入未成熟 | 可能可行 | 等窗口，不急扩 |
| actual_cpc 接近 safe_cpc | 缓冲不足 | 小样本或优化页面/source |
| actual_cpc > safe_cpc | 买量过贵 | 降 bid、换词、换 source、停测 |
| break_even_cpc 为 0 | 收入口径缺失 | 不买量，先补追踪和估算 |
| ROI 正但 cash buffer 不足 | 现金风险高 | 降预算或延长结算观察 |

单位经济模型要和 policy、content、tracking、source quality 一起看。经济可行但政策高风险，不是可跑；政策合规但经济不可行，也不是可跑。

## 10. 与出价策略的关系

出价策略应由单位经济倒推：

| 策略 | 单位经济要求 |
| --- | --- |
| Manual CPC | actual_cpc 必须低于 safe_cpc |
| Maximize Clicks with cap | cap 不高于 safe_cpc |
| Maximize Conversions | primary conversion 的 paid EPC 支撑 CPC |
| Target CPA | target CPA 低于 expected approved value |
| Target ROAS | target ROAS 基于 net/paid value |
| PMax / Broad Match | paid value、lag、deduction 和 source quality 已稳定 |

不要因为平台推荐“提高预算”或“切换 tROAS”就跳过单位经济。后台建议是输入，不是套利利润判决。

## 11. 系统落地

当前系统已经支持 V1 测算：

| 字段/动作 | 系统位置 |
| --- | --- |
| revenue model、RPM、payout、CVR、CPC | `/calculators` |
| safety factor、target clicks、cash buffer | `/calculators` |
| break-even CPC、safe CPC、safety margin | `/calculators` |
| expected revenue/cost/profit、ROI | `/calculators` |
| test budget、hard stop、opportunity score | `/calculators` |
| cost/click/conversion/revenue 导入 | `/metrics/import` |
| 优化建议和止损动作 | `/optimization` |
| 来源、政策和模型依据 | `/sources` |
| 风险审计和事故复盘 | `/risk-audits` |

后续可扩展表：

```text
unit_economic_models
unit_economic_scenarios
break_even_snapshots
safety_factor_versions
test_budget_plans
unit_economic_decisions
model_assumption_audits
```

字段示例：

```text
unit_economic_models:
  offer_id, source_id, country, device, revenue_model,
  payout, submitted_cvr, approval_rate, paid_rate,
  session_rpm, deduction_rate, landing_arrival_rate,
  actual_cpc, break_even_cpc, safe_cpc, safety_margin,
  safety_factor, cash_buffer_days, decision, reviewer
```

系统只做测算、评分、建议和审计，不自动买量、不自动补量、不伪造收入、不通过 Cookie 后台改预算或出价。

## 12. ADXKit 对应点和完成形态

ADXKit 类工具的“批量测试、自动优化、自动投放”必须建立在单位经济之上。否则批量只是批量烧钱。

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| Offer 批量测试 | 每个 Offer 先有 break-even、safe CPC 和 hard stop |
| 自动优化 | 优化动作必须引用 RPV/EPC、safety margin 和成熟收入 |
| 自动投放 | 只导出待审核草稿，不无人值守买量 |
| ROI dashboard | 区分 gross、reported、approved、finalized、paid |
| 换链接 | link version 变化后重新计算 RPV 和 safety factor |
| AI 创意生成 | 创意 winner 用 paid RPV，而不是 CTR |

功能拆解和安全完成清单：

- 完成三种业务模型的单位经济公式。
- 完成 safety factor、safety margin、sensitivity analysis 和 test budget 模型。
- 完成 break-even 决策矩阵、出价策略映射和系统落地。
- 完成来源 URL、来源库、验收入口和计算器字段映射。
- 不实现补点击、刷展示、伪造转化、伪造收入、Cookie 后台自动改预算或规避封禁。

## 13. QA 清单

- RPV/EPC 的分母是否明确：ads clicks、sessions、offer clicks 还是 impressions。
- revenue 是否区分 gross、reported、pending、approved、finalized、paid。
- Break-even CPC 是否基于 payable RPV，而不是 gross。
- Safe CPC 是否应用 safety factor。
- actual CPC 是否低于 safe CPC。
- Safety margin 是否大于最低阈值。
- deduction、reject、refund、chargeback 是否进入模型。
- conversion lag 和 revenue lag 是否进入测试周期。
- sample clicks 是否足够，不用单日少量数据扩量。
- cash buffer 是否覆盖回款周期和 hard stop。
- 平台 recommendations 是否经过单位经济复核。
- 是否禁止通过补点击、伪造转化或换账号修正负 ROI。

## 14. 信息来源 URL

- Google Ads Help, Determine a bid strategy based on your goals: https://support.google.com/google-ads/answer/2472725
- Google Ads Help, About Smart Bidding: https://support.google.com/google-ads/answer/7065882
- Google Ads Help, Set a target ROAS bid strategy: https://support.google.com/google-ads/answer/6268637
- Google Ads Help, About conversion values: https://support.google.com/google-ads/answer/3419241
- Google Ads Help, About conversion measurement: https://support.google.com/google-ads/answer/1722022
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Budget report: https://support.google.com/google-ads/answer/10702522
- Google Ads Help, Performance Planner: https://support.google.com/google-ads/answer/9230124
- Google Ads Help, Measure your results: https://support.google.com/google-ads/answer/6172626
- Google Ads API, Metrics fields: https://developers.google.com/google-ads/api/fields/v23/metrics
- Google Ads API, Bidding strategy types: https://developers.google.com/google-ads/api/docs/campaigns/bidding/strategy-types
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google AdSense Help, Metrics glossary: https://support.google.com/adsense/answer/2735899
- Google AdSense Management API, Metrics and Dimensions: https://developers.google.com/adsense/management/metrics-dimensions
- Google AdSense Help, Payment timelines: https://support.google.com/adsense/answer/7164703
- Google AdSense Help, Deductions from earnings FAQs: https://support.google.com/adsense/answer/2808531
