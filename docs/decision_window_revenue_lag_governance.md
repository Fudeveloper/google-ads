# 决策窗口、回传延迟与收入延迟治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何治理 data freshness、conversion lag、offline import lag、buyer approval lag、AdSense / AdX finalized revenue、payment timeline、deduction、chargeback 和 campaign decision window。目标是把“什么时候可以判断亏损、什么时候可以扩量、什么时候必须等待回传、什么时候进入关账”讲清楚，而不是用当天 ROI、当天 conversions 或未结算 estimated revenue 做激进决策。本文不提供补点击、刷展示、伪造转化、补 postback、隐藏低质来源、换账号或用 Cookie 后台改报表的方案。

## 1. 为什么当天 ROI 是套利陷阱

套利团队每天看到的报表不是同一时间成熟的：

```text
clicks / cost
  -> landing requests
  -> conversions
  -> offline qualified / approved
  -> finalized revenue
  -> paid cash
```

Google Ads 的 clicks、impressions、cost 可能较快刷新，但 conversion、search terms、auction insights、conversion value、offline imports 和第三方收入会有不同处理时间。Lead buyer 可能几小时后才判定有效，CPA network 可能几天后 scrub，AdSense / AdX 可能次月才 finalized，最终付款又晚于 finalized。

如果只看当天 ROI，会出现四类错误：

- 早停：真实转化还没回填，把好 campaign 当坏 campaign 停掉。
- 早扩：submitted 或 estimated 很好看，后续 approved / paid 变差。
- 误判来源：低质 source 在提交阶段好看，拒付阶段暴露。
- 误修系统：把正常数据延迟当 tracking 事故，开始乱改 tag、URL、goal。

决策窗口治理的核心是：不同动作使用不同成熟度的数据。

## 2. 原理解释：数据刷新、转化延迟、收入延迟不是一回事

三个概念必须分开：

| 概念 | 含义 | 影响 |
| --- | --- | --- |
| data freshness | 平台报表何时刷新 | 当天报表是否完整 |
| conversion lag | 点击/展示到转化、转化到归因的延迟 | CPA/ROAS 是否过早判断 |
| revenue lag | reported 到 approved/finalized/paid 的延迟 | 是否能扩量和回款 |

示例：

```text
Day 0  click and cost
Day 0  submitted lead
Day 1  Google Ads conversion visible
Day 2  buyer accepted
Day 5  buyer approved or rejected
Day 30 AdSense finalized / network statement
Day 45 cash paid
```

Day 0 的 ROI 只能说明“花费和浅层反馈”，不能说明“可收款利润”。套利优化的正确问题不是“今天 ROI 是多少”，而是“这个预算单元处于哪个成熟窗口，可以做什么级别的动作”。

## 3. 核心对象地图

| 对象 | 说明 | 系统字段建议 |
| --- | --- | --- |
| click_time | 广告点击时间 | click_date、timezone |
| spend_time | Google Ads 花费记账时间 | cost_date、account_timezone |
| event_time | 用户提交或购买时间 | conversion_time |
| import_time | offline conversion 导入时间 | imported_at、source_file_hash |
| approval_time | buyer / network 批准时间 | approved_at |
| reject_time | buyer / network 拒付时间 | rejected_at、reason |
| finalized_time | AdSense/AdX/GAM finalization | finalized_month |
| payment_time | 现金到账时间 | paid_at |
| lag_p50 / p90 | 主要延迟分位数 | lag_profile |
| decision_window | 决策最短等待期 | min_wait_hours/days |
| data_status | 数据成熟状态 | fresh、partial、mature、settled |

没有时间轴字段，就没有可靠决策。只有一个 `day, conversions, revenue` 的表，适合 V1 简化，但不适合大规模自动扩量。

## 4. 三层窗口模型

建议把每个 campaign / source / offer 的判断分成三层：

| 窗口 | 典型长度 | 可做动作 | 不应做动作 |
| --- | --- | --- | --- |
| Freshness Window | 0-24 小时 | 检查花费、点击、重大断流、URL 错误 | 不用 ROI 做最终扩停 |
| Conversion Window | 1-7/14/30 天 | 看 conversion lag、qualified、approved 初步质量 | 不用 submitted 直接放量 |
| Settlement Window | 15-60+ 天 | 看 finalized/paid、扣量、拒付、现金流 | 不把 estimated 当可用利润 |

不同业务长度不同：

- Search lead：submitted 快，approved 可能慢。
- 电话 lead：通话时长快，buyer feedback 慢。
- CPA/CPL network：pending 到 approved 可能跨多天。
- AdSense/AdX：estimated 日报和 finalized 收入存在关账差异。
- Search feed / RSOC：gross revenue、deduction 和 final payable 需要 partner 口径。

## 5. Decision Window Score

建议给每个预算单元计算 `Decision Window Score`：

```text
decision_window_score =
  data_freshness_ready       15
  conversion_lag_covered     20
  approval_lag_covered       20
  revenue_status_maturity    20
  sample_size_ready          10
  source_quality_stable       5
  change_history_clean        5
  incident_free               5
```

动作建议：

| Score | 状态 | 动作 |
| --- | --- | --- |
| 85-100 | Mature / settled | 可进入 Core 或 Scale 评审 |
| 70-84 | Mostly mature | 可小幅调预算，保守扩量 |
| 55-69 | Partial | 只做诊断和小额测试 |
| 35-54 | Early | 等待回传，不做大动作 |
| 0-34 | Unsafe | 冻结扩量或进入事故排查 |

## 6. 业务模式窗口参考

| 模式 | 初始信号 | 成熟信号 | 决策建议 |
| --- | --- | --- | --- |
| Search content arbitrage | clicks、sessions、ad requests | finalized/paid RPM、deduction | 日报看趋势，扩量看 finalized RPV |
| CPL lead | submitted、accepted | approved、paid、reject reason | submitted 只用于诊断，不直接扩量 |
| Call lead | call start、duration | qualified call、buyer payout、complaint | 短通话不能做 primary 扩量 |
| Native / advertorial | CTR、CTA click | approved/paid、refund/scrub | 高 CTR 低 paid 要降级素材或来源 |
| Search feed / RSOC | search action、gross RPC | payable revenue、deduction | gross feed RPM 不能替代结算口径 |
| PMax / Demand Gen | platform conversions | channel/asset/page + paid revenue | 自动化流量必须等待更长窗口 |

## 7. Budget Ramp 和等待规则

扩量前必须同时满足：

- cost、click、conversion 报表刷新完成。
- conversion lag 已覆盖主要 p50/p90。
- approved 或 paid revenue 达到最小样本。
- 最近没有 conversion goal、bid strategy、Final URL、tracking template 或 page version 大改。
- source quality 和 reject/scrub 没有异常。
- cash reserve 能覆盖未结算 exposure。

建议 ramp：

```text
early window: no scale, only observe
partial window: +0% to +10%, only if hard stop exists
mature window: +10% to +30%, wait another lag cycle
settled window: portfolio review, possible Core allocation
```

不要在同一天连续加预算、改目标 CPA、换页面、换创意和换 link。多变量同时变更会让延迟窗口失去解释性。

## 8. Stop-loss 与 Wait-loss 的区别

不是所有亏损都应该立刻停。

| 现象 | 更像 Stop-loss | 更像 Wait-loss |
| --- | --- | --- |
| 花费异常飙升 | 是 | 否 |
| URL 404、tracking 断 | 是 | 否 |
| click 高 session 低 | 是，先查链路 | 否 |
| Day 0 conversions 少 | 不一定 | 是，等 lag |
| submitted 高 approved 低 | 是，降预算或停源 | 否 |
| paid revenue 未到账 | 不一定 | 等 settlement，但控制 cash risk |
| Change history 刚改 strategy | 不一定 | 等 learning window |

Wait-loss 不是放任亏损，而是用硬预算上限等待数据成熟。Stop-loss 是发现结构性风险后立即止血。

## 9. Cohort 和 Aging 表

建议每个来源按 cohort 看成熟过程：

```text
cohort_date, offer_id, source_id, campaign_id,
cost_day0, submitted_day0,
qualified_day1, approved_day3, rejected_day7,
finalized_day30, paid_day45,
approval_rate, deduction_rate, paid_roi
```

看 cohort 比看自然日总表更可靠，因为自然日混合了不同成熟度：

- 今天的 cost。
- 昨天的 conversions。
- 上周的 approved。
- 上月的 finalized。

日报可以看运营异常，扩量和关账必须看 cohort maturity。

## 10. 常见事故和诊断

| 事故 | 原因 | 处理 |
| --- | --- | --- |
| 今天 ROI 暴跌 | 转化还没回填、报表延迟 | 查 data freshness 和 lag，不急改 |
| 今天 ROI 暴涨 | submitted 或重复 postback | 查 primary、dedupe 和 value |
| 扩量后几天亏损 | buyer reject 延迟暴露 | 降预算、停源、更新 source score |
| 月底收入下调 | invalid traffic、deduction、finalized 调整 | 用 finalized 口径复盘，不拿 estimated 扩量 |
| 报表互相不一致 | attribution、timezone、tag、lookback | 建对账表，不强求完全相等 |
| 学习期反复 | 连续改 goal、budget、bid strategy | 冻结大改，重建观察窗口 |

## 11. 系统落地

当前系统可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 导入日级 cost、clicks、conversions、revenue | `/metrics/import` |
| 生成 ROI、RPV、stop-loss 和异常建议 | `/optimization` |
| 保存 Decision Window Score、成熟度、建议动作和阻塞项 | `/decision-windows`、`decision_window_reviews` |
| 更新 waiting、ramp_ready、blocked、closed 等内部处理状态 | `/decision-windows/<id>/status`，写入 `/logs` |
| 记录延迟、扣量、关账和来源解释 | `/risk-audits` |
| 保存官方来源和 partner 规则 | `/sources` |
| 用任务中心安排周报、关账、回传复查 | `/tasks` |

V1 已实现 `decision_window_reviews`，用于保存单次预算/投放判断所需的 data status、revenue status、conversion lag、approval lag、settlement lag、样本点击、approved / paid revenue、source quality、incident state、score、maturity、recommended action、blockers、source URLs 和人工状态。它是扩量前的评审记录，不会自动修改预算、出价、URL、conversion goal 或后台报表。

后续可扩展表：

```text
decision_window_profiles
conversion_lag_profiles
revenue_lag_profiles
cohort_maturity_daily
revenue_status_aging
budget_ramp_decisions
settlement_close_runs
decision_window_incidents
```

字段示例：

```text
decision_window_profiles:
  offer_id, source_id, revenue_model,
  freshness_wait_hours, conversion_wait_days,
  approval_wait_days, settlement_wait_days,
  p50_lag_hours, p90_lag_hours,
  min_sample_clicks, min_approved_revenue,
  ramp_rule, stoploss_rule
```

系统只生成窗口、评分、等待建议、止损建议和复盘任务；不生成点击、展示、转化或收入，不修改平台报表，不用 Cookie 后台覆盖历史数据。

## 12. ADXKit 对应点和完成形态

ADXKit 类工具常强调自动优化和自动放量。Decision Window 治理对应的是：任何自动化动作前先判断数据成熟度。

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| 自动扩量 | 先检查 conversion/revenue lag 和 cohort maturity |
| ROI dashboard | 展示 fresh、partial、mature、settled 状态 |
| 优化建议 | 区分 stop-loss 和 wait-loss |
| 任务中心 | 安排 lag review、monthly close、settlement check |
| 链接计划 | link_version 变化后重置观察窗口 |
| AI 创意优化 | winner 判断等待 paid/approved revenue |

功能拆解和安全完成清单：

- 完成 data freshness、conversion lag、revenue lag 的原理拆解。
- 完成三层窗口、Decision Window Score、ramp 和 stop/wait 决策模型。
- 完成 cohort aging、事故诊断、系统落地和来源 URL。
- 不实现补点击、补展示、伪造转化、伪造收入、Cookie 后台改报表或规避封禁。

## 13. QA 清单

- 今天的 cost/click 是否已经达到 freshness 可判断状态。
- Search terms、Auction Insights、conversion value 是否可能仍在延迟刷新。
- 主要 conversion lag 的 p50/p90 是否已覆盖。
- offline conversion import 是否已经处理完成并检查错误。
- buyer approval / reject 窗口是否已过。
- AdSense/AdX/GAM 是否使用 finalized 或 paid，而不是只看 estimated。
- 最近 72 小时是否有 goal、budget、bid strategy、URL、link_version、page_version 或 tracking 变更。
- 当前动作是 stop-loss、wait-loss、ramp 还是 close。
- 是否用 cohort 表而不是自然日总表做扩量判断。
- 是否记录 cash at risk 和 pending exposure。
- 是否禁止用补点击、伪造 event、换账号或隐藏来源修复短期 ROI。

## 14. 信息来源 URL

- Google Ads Help, About data freshness: https://support.google.com/google-ads/answer/2544985
- Google Ads Help, Data discrepancies: factors and troubleshooting: https://support.google.com/google-ads/answer/7457111
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, About conversion delay estimates: https://support.google.com/google-ads/answer/14545572
- Google Ads Help, Find your bid strategy reports: https://support.google.com/google-ads/answer/7074568
- Google Ads Help, Evaluate automated bid strategy performance: https://support.google.com/google-ads/answer/10167267
- Google Ads Help, Budget report: https://support.google.com/google-ads/answer/10702522
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
- Google Ads Help, Monitor experiments: https://support.google.com/google-ads/answer/6318747
- Google Ads API, Reporting overview: https://developers.google.com/google-ads/api/docs/reporting/overview
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads Help, Fix discrepancies and errors in offline conversion imports: https://support.google.com/google-ads/answer/13321563
- Google AdSense Help, Payment timelines: https://support.google.com/adsense/answer/7164703
- Google AdSense Help, Deductions from earnings FAQs: https://support.google.com/adsense/answer/2808531
- Google SRE Book, Managing Incidents: https://sre.google/sre-book/managing-incidents/
- Google SRE Book, Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
