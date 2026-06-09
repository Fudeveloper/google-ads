# 回款、结算与现金流风险手册

更新时间：2026-06-08

Ads 套利不是只看当天 ROI。很多团队死在“账面赚钱、现金断掉、月底扣量、付款被 hold”的环节。本文说明广告花费、AdSense/AdX 回款、联盟结算、扣量、拒付、预算安全垫和月度关账的行业逻辑。

## 1. 为什么现金流决定生死

套利的现金流通常是倒挂的：

```text
今天买量花费 -> 今天或本周扣广告费
今天产生收入 -> 次月或更晚确认
确认收入 -> 还可能被扣量、拒付、hold 或延迟支付
```

因此，不能只看：

```text
当天 ROI = (当天收入 - 当天花费) / 当天花费
```

更要看：

```text
可收回 ROI = (已批准收入 - 花费 - 扣量 - 退款 - 资金成本) / 花费
现金缺口天数 = 广告费支出日期 -> 收入到账日期
最低现金储备 = 日花费 * 现金缺口天数 + 应急储备
```

行业里最危险的情况是：前 7 天报表看起来赚钱，于是快速扩量；第 21-45 天才发现收入被扣、Offer 拒付、AdSense finalization 下调或付款被 hold。

## 2. 成本和收入时间差

| 项目 | 常见发生时间 | 风险 |
| --- | --- | --- |
| Google Ads 自动付款 | 广告投放后按账单周期或付款阈值扣款 | 花费先发生，卡/账户额度不够会停投或影响账号健康 |
| Google Ads 手动付款 | 先充值再消耗 | 不会超出充值额，但扩量受余额限制 |
| Google Ads 月结发票 | 先消费后按发票付款 | 需要信用资格，逾期付款会带来账号和财务风险 |
| AdSense/AdX 估算收入 | 当月持续产生 | 只是 estimated earnings，不等于可收款 |
| AdSense finalized earnings | 次月初确认上月收入 | 可能出现调整、扣减或 hold |
| AdSense 付款 | 达到阈值且无 hold 时通常在月中下旬发放 | 银行到账、税务、地址、支付方式都会影响 |
| 联盟 CPA/CPL | net 7 / net 15 / net 30 / net 45 等 | pending、rejected、scrub、quality review |
| 直客或 lead buyer | 合同周期 | 需要验收、发票、退款和坏账管理 |

结论：套利预算必须按“最晚到账时间”设计，而不是按“报表显示收入时间”设计。

## 3. 收入状态字典

| 状态 | 含义 | 能否用于扩量 |
| --- | --- | --- |
| `estimated` | 平台或追踪系统估算收入 | 只能参考，不能作为现金依据 |
| `pending` | 已产生事件，等待广告主/联盟审核 | 谨慎，需按历史批准率折扣 |
| `approved` | 已批准但未付款 | 可作为中等可信收入，仍要看付款风险 |
| `finalized` | 发布商平台已结算上月收入 | 可信度高，但仍可能有支付 hold |
| `paid` | 已到账 | 可作为真实现金流 |
| `deducted` | 因无效流量、政策、广告主违约等扣减 | 要进入扣量率模型 |
| `rejected` | Offer 拒付或 lead 不合格 | 不计收入，必须追踪原因 |
| `held` | 付款被暂缓 | 不可用于扩量，先处理 hold 原因 |

日报可以看 estimated/pending，周报要看 approved/finalized，月报和扩量额度必须看 paid/finalized/历史扣量。

## 4. 预算安全垫模型

基础公式：

```text
日最大花费 = 可动用现金 / (现金缺口天数 + 应急天数)
```

示例：

```text
可动用现金 = 30,000 USD
现金缺口天数 = 35 天
应急天数 = 10 天
日最大花费 = 30,000 / 45 = 666 USD
```

如果要考虑扣量和收入不确定性：

```text
安全收入 = estimated_revenue * approval_rate * (1 - deduction_rate)
现金安全系数 = paid_revenue / estimated_revenue
```

内部建议：

| 业务阶段 | 安全规则 |
| --- | --- |
| 冷启动 | 只用小预算，按 40%-60% 的收入安全系数测算 |
| 小样本验证 | 至少等待一个回传延迟窗口，不用 1 天 ROI 放量 |
| 结算前放量 | 要有 30-45 天现金储备，扣量储备至少 10%-30% |
| 经历稳定结算 | 可以提高日花费，但保留应急储备和来源隔离 |
| 出现扣量/hold | 停止扩量，收入按 paid 或 finalized 口径重算 |

## 5. 扣量和拒付管理

扣量不一定都来自平台恶意，常见原因包括：

- 无效点击、无效展示、机器人、自动访问。
- 流量来源不符合 Offer 限制，例如禁止 brand bidding、incent、pop、push、adult。
- 地区、设备、年龄或用户属性不符合广告主要求。
- lead 无效：电话不通、重复、虚假信息、低质量咨询。
- 结算周期内广告主违约或拖欠。
- 页面内容、广告承诺或流量来源触发政策审核。

管理方式：

1. 所有 Offer 必须记录允许和禁止流量来源。
2. 所有 source/subid 必须可回溯到 campaign、creative、placement、device。
3. 每个结算周期记录 `gross_revenue`、`approved_revenue`、`paid_revenue`、`deduction_reason`。
4. 新来源未经历结算前，不能按 100% 收入扩量。
5. 对无原因扣量的变现方降低评分或停测。

## 6. 月度关账流程

每月固定关账：

| 步骤 | 动作 | 输出 |
| --- | --- | --- |
| 1 | 锁定上月广告花费 | Cost by account/campaign/day |
| 2 | 锁定站内 session 和 click_id 数据 | Source/session/click reconciliation |
| 3 | 拉取 AdSense/AdX finalized earnings | Finalized revenue |
| 4 | 拉取联盟 approved/paid/rejected 报表 | Approved revenue and rejected reasons |
| 5 | 计算扣量率和付款延迟 | Deduction and payment lag |
| 6 | 按 source/offer/page 复盘 ROI | Keep / pause / retest |
| 7 | 更新预算上限和安全系数 | Next month budget cap |
| 8 | 归档账单、截图、报表和风险记录 | Audit evidence |

关账后才更新长期模型：

```text
历史批准率
历史扣量率
平均回款天数
最大回款天数
来源质量评分
Offer 可靠性评分
可承受 CPC / CPA
```

## 7. 止损触发器

立即停止扩量：

- 任一来源出现异常高 CTR/CVR、低停留、零收入。
- 结算方出现 invalid traffic、policy、deduction、hold 通知。
- 收入从 estimated 到 finalized 下调超过预设阈值。
- 某 Offer 拒付原因无法解释或无法按 subid 定位。
- 广告账号出现付款失败、账单异常、预算超限或账号限制。
- 现金储备低于未来 14-30 天广告费。

建议阈值：

| 指标 | 警戒 | 停止扩量 |
| --- | --- | --- |
| estimated -> finalized 下调 | > 10% | > 25% |
| CPA/CPL 拒付率 | > 15% | > 30% |
| 单来源收入占比 | > 40% | > 60% |
| 现金储备天数 | < 30 天 | < 14 天 |
| 支付延迟 | > 7 天 | > 15 天 |
| 未解释扣量 | 任意出现 | 连续 2 个周期 |

## 8. 付款与账号治理

Google Ads 支付失败、AdSense hold 或联盟拖款都不是“运营小事”，它们会影响业务连续性。

治理建议：

- 付款权限和投放权限分开，最小权限协作。
- 不共享登录态或 Cookie；账单、税务、付款资料由授权人员管理。
- 保存每次付款、发票、账单、结算、扣量和申诉证据。
- 预算上限不要只依赖广告平台日预算，还要有外部现金流表。
- 任何高风险来源必须有单独 source id，不能混进主业务线。

## 9. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer payout、限制和状态 | `/offers` |
| 用安全系数、目标点击和现金缓冲评估机会 | `/calculators` |
| 导入每日 cost、clicks、conversions、revenue | `/metrics/import` |
| 查看 dashboard 总成本、收入、ROI | `/` |
| 对亏损、低收入和异常来源生成优化建议 | `/optimization` |
| 记录扣量、hold、支付和来源证据 | `/risk-audits`、`/sources` |
| 通过任务中心安排周报/月度关账 | `/tasks` |
| 通过审计日志追踪关键动作 | `/logs` |

当前系统没有完整财务模块，但已经把现金流关键字段放进测算和指标导入：`cost`、`revenue`、`cash_buffer_days`、`safety_factor`。后续可扩展 `settlement_status`、`approved_revenue`、`paid_revenue`、`deduction_rate`、`payment_due_date`，但仍不需要 Cookie 后台接管或规避式自动化。

## 10. 信息来源 URL

- Google Ads Help, About payment settings: https://support.google.com/google-ads/answer/2375432
- Google Ads Help, Create an account budget: https://support.google.com/google-ads/answer/2375395
- Google Ads API, Account Budget: https://developers.google.com/google-ads/api/docs/billing/account-budgets
- Google AdSense Help, Payment timelines: https://support.google.com/adsense/answer/7164703
- Google AdSense Help, Payments FAQs: https://support.google.com/adsense/answer/7164701
- Google AdSense Help, Payment thresholds: https://support.google.com/adsense/answer/1709871
- Google AdSense Help, Deductions from earnings FAQs: https://support.google.com/adsense/answer/2808531
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Help, Use of online advertising to get new users to the site: https://support.google.com/adsense/answer/1348722
