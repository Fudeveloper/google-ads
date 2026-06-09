# 异常监控、告警、止损队列与事故分诊手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何设计异常监控、告警、止损队列和事故分诊流程。它对应 ADXKit 类系统里的“数据同步、优化建议、任务状态、成功失败、换链接和执行日志”闭环：系统发现异常，生成可解释、可审批、可复盘的动作建议；人确认后再通过 Google Ads Editor、Scripts preview、后台手工或官方 API 执行。

本文不提供自动登录后台、Cookie 会话接管、绕过 2FA、安全挑战、刷点击、刷展示、模拟自然流量、代理/指纹规避、cloaking、审核页/用户页不一致或封禁规避账号切换。异常不能用补点击、补转化、隐藏页面或换号解决，只能用停量、隔离、修复、对账、申诉和复盘解决。

## 1. 为什么异常监控是套利生命线

Ads 套利的坏结果通常不会一次性出现，而是先出现早期信号：

- 花费突然上升，但 session、offer click 或 revenue 没有同步上升。
- CTR 异常高，CVR、RPV 或 paid revenue 很低。
- Google Ads clicks 和 server landing requests 差距变大。
- `gclid`、UTM、click_id、subid 丢失率升高。
- Offer 端 approved revenue 下降，reject/scrub/deduction 上升。
- Landing URL 变 404、证书失效、跳转剥离参数或目标国家不可访问。
- Policy Manager、AdSense Policy Center 或账号健康出现新 issue。
- Change History 显示预算、Final URL、conversion goal、bidding、asset 被改动。

异常监控的目标不是“自动替人做所有决定”，而是把风险从个人直觉变成可重复流程：

```text
metric snapshot / log / policy event
  -> anomaly rule
  -> alert severity
  -> triage owner
  -> safe containment
  -> evidence pack
  -> approved action
  -> postmortem and rule update
```

没有这个流程，套利团队会在回传延迟、扣量、预算 overdelivery、页面故障和政策事故之间反复猜原因。

## 2. 监控对象地图

| 层级 | 监控对象 | 关键问题 |
| --- | --- | --- |
| Spend | cost、served cost、billed cost、daily/monthly budget、pacing | 钱有没有超出测试和现金流边界 |
| Traffic | impressions、clicks、CTR、CPC、device、geo、network | 流量是否突然变质、变贵或偏离目标 |
| Landing | final URL、expanded URL、status code、latency、session rate | 点击后用户是否能到同一页面 |
| Tracking | `gclid`、UTM、click_id、subid、postback、transaction_id | 归因链路是否断裂 |
| Revenue | estimated、approved、finalized、paid、deduction、reject | 收入是否真实可收款 |
| Conversion | primary/secondary、conversion lag、value、window、attribution | 平台优化信号是否可靠 |
| Policy | ad review、Policy Manager、destination、misrepresentation、ad serving limit | 能否继续合规投放 |
| Change | Change History、Scripts log、Editor batch、payload hash | 异常前后是谁改了什么 |
| Task | job status、last_result、failure_count、retry_count | 系统任务是否把错误放大 |
| Source | publisher、placement、search term、query、traffic vendor、subid | 哪个来源该隔离或停量 |

行业经验：异常监控必须把平台指标、站内日志、变现报表和操作日志放在一起看。只看 Google Ads conversions 或只看 gross revenue，都会误判。

## 3. 告警分级

建议四级：

| 等级 | 含义 | 例子 | 处理 |
| --- | --- | --- | --- |
| L0 info | 记录观察，不打扰人 | ROI 正常波动、少量数据延迟 | 写入日报 |
| L1 watch | 需要观察或补证据 | CTR 上升但样本不足、conversion lag 未回填 | 标记 watch，等待窗口 |
| L2 action | 需要当天处理 | click/session gap、低 ROI、URL 速度变差 | 进入优化建议和任务队列 |
| L3 freeze | 需要立即冻结或停量 | 花费失控、Final URL 404、policy issue、疑似无效流量 | 暂停扩量、人工停量、保全证据 |

只有 L3 才需要即时打断人。过多 L1/L2 通知会让团队忽略真正事故。Google SRE 的监控原则也强调 alert 要低噪声、高信号，能明确说明“什么坏了”和“为什么需要人现在处理”。

## 4. 指标异常规则

V1 规则先用简单、可解释的阈值，不用神秘黑箱。

| 规则 | 条件 | 可能原因 | 安全动作 |
| --- | --- | --- | --- |
| no revenue spend | clicks >= 30 且 revenue = 0 且 cost > 0 | Offer 不匹配、追踪断、无效流量、回传延迟 | pause_check，先隔离来源 |
| stop loss | cost >= 测试预算 或 ROI < 阈值 | CPC 过高、CVR 低、收入扣量 | stop_loss，降预算或暂停 |
| high CTR low RPV | CTR 高、RPV < CPC、clicks 达样本 | 标题党、source 低质、页面不兑现 | creative_mismatch |
| suspicious CTR | CTR 极高且无收入 | 激励/误点/异常 placement | invalid_traffic_review |
| click/session gap | Ads clicks 高、landing sessions 低 | URL、速度、parallel tracking、consent、跳转失败 | tracking_gap_review |
| postback gap | offer click 有，postback 无 | subid、click_id、buyer endpoint、去重错误 | postback_reconcile |
| revenue reversal | approved/finalized/paid 回落 | reject、scrub、deduction、invalid traffic | revenue_quality_review |
| conversion spike | conversions 暴涨但 paid revenue 不动 | primary conversion 配错、重复转化、低质 lead | conversion_signal_review |
| spend spike | served cost 快速超过计划 | budget 改动、智能出价、流量波动 | budget_freeze_review |
| policy event | disapproved/limited/ad serving limit | claim、destination、页面质量、账号健康 | policy_triage |

每条规则都要带上：

- 时间窗口。
- 样本阈值。
- 维度范围：offer、campaign、source、geo、device、landing version。
- 触发值和基准值。
- 需要的证据。
- 建议动作。
- 禁止动作。

## 5. 时间窗口和回传延迟

套利团队最容易犯的错误是“今天没收入就立刻判死刑”或“今天 ROI 高就立刻扩量”。Google Ads conversion lag 和收入结算延迟会让近期 CPA/ROAS、RPV、ROI 失真。

建议窗口：

| 场景 | 最小窗口 | 注意 |
| --- | --- | --- |
| URL 404、证书、跳转失败 | 立即 | 这是可验证故障，不等回传 |
| 花费超过硬止损 | 立即 | 现金安全优先 |
| 无收入点击 | 30-100 clicks 后 | 先查回传延迟和 click/session gap |
| Lead reject/scrub | buyer 回传周期后 | 不把 submitted lead 当 paid revenue |
| AdSense/AdX deduction | 月度 finalized 后 | estimated revenue 不用于最终扩量 |
| 智能出价学习期 | 1-2 个学习窗口 | 不在短期噪声中频繁改动 |
| GEO/device 分层 | 至少按同类样本比较 | 不把国家和设备混成平均值 |

原则：冻结风险可以快，扩量必须慢。止损看现金和故障，放量看 paid/finalized evidence。

## 6. 数据源和证据包

异常分诊要保留证据，不要只写“感觉不对”。

| 数据源 | 证据 |
| --- | --- |
| Google Ads report | date range、campaign/ad group、clicks、cost、conversions、conversion value |
| Google Ads Change History | 改动时间、对象、操作人、旧值/新值、client type |
| Google Ads Explanations | 大幅波动的可能原因，例如 budget、bidding、conversion delay、asset、eligibility |
| GA4 / server log | sessions、landing request、source/medium、URL 参数、device、country |
| Tracking log | expanded URL、tracking request、click_id、UTM、subid、status |
| Offer / buyer report | postback、approved、rejected、paid、reason code |
| AdSense/GAM/AdX | estimated/finalized/paid revenue、deduction、ad serving status |
| Policy tools | Policy Manager、Policy Center、disapproval、limited、appeal status |
| Task system | task type、payload hash、last_result、failure_count、audit log |
| Link registry | link_version、old URL、new URL、reviewer、rollback point |

证据包最少包含：

```text
alert_id
triggered_at
metric_window
object_scope
rule_name
trigger_values
baseline_values
linked_sources
change_history_refs
owner
decision
follow_up_task
postmortem_url
```

## 7. 止损队列

止损队列不是自动停投机器人，而是“待处理风险动作列表”。它应该能把异常变成明确动作：

| 动作类型 | 示例 | 默认执行方式 |
| --- | --- | --- |
| monitor | 样本不足，继续观察 | 不执行后台变更 |
| pause_check | 点击有量但无收入 | 人工检查后暂停或隔离 |
| stop_loss | ROI 跌破阈值 | 人工降预算/暂停，记录原因 |
| tracking_gap_review | click/session/postback 断裂 | 任务中心检查 URL 和参数 |
| creative_mismatch | CTR 高但 RPV 低 | 回写 angle，改素材或页面 |
| policy_triage | 拒登、受限或 ad serving limit | 进入申诉/修复证据包 |
| source_quarantine | source/publisher/subid 异常 | 隔离来源，停止扩量 |
| rollback_link | URL 变更导致故障 | 回到上一 link_version |
| conversion_signal_review | primary conversion 或 value 异常 | 检查 conversion action |

每条动作要有状态：

```text
open -> reviewing -> approved -> executed -> verified -> closed
open -> rejected -> documented
```

V1 系统里的 `/optimization` 已经是这个队列的第一版：`recommended_actions()` 生成 `pause_check`、`stop_loss`、`creative_mismatch`、`invalid_traffic_review`、`source_quality_review` 和 `monitor`。后续可把它升级为独立 alert/incident 模块。

## 8. 事故分诊流程

推荐流程：

```text
Detect
-> Classify
-> Contain
-> Diagnose
-> Reconcile
-> Fix
-> Verify
-> Postmortem
-> Rule update
```

解释：

| 阶段 | 要做什么 |
| --- | --- |
| Detect | 规则、报表、任务失败或人工发现异常 |
| Classify | 判定是预算、流量、追踪、收入、页面、政策、账号还是系统任务 |
| Contain | 冻结扩量、降预算、暂停来源、回滚链接，不做刷量补洞 |
| Diagnose | 查 Change History、URL、logs、postback、Policy Manager 和 buyer report |
| Reconcile | 对齐 cost、click、session、offer click、postback、paid revenue |
| Fix | 修 URL、参数、页面、素材、conversion action、source 或预算 |
| Verify | 用新窗口确认指标恢复 |
| Postmortem | 记录时间线、根因、影响、预防项 |
| Rule update | 把根因转成阈值、QA、审批或任务模板 |

事故分诊的重点是“先止血，后归因”。但止血不等于规避：不能用换账号、cloaking、后台 Cookie 自动操作、补点击或隐藏目的地来盖住事故。

## 9. 常见异常和诊断矩阵

| 表现 | 优先检查 | 处理 |
| --- | --- | --- |
| cost 快速上升 | budget、bid strategy、Change History、network、search terms | 冻结扩量，按预算手册降风险 |
| clicks 高 sessions 低 | Final URL、tracking template、parallel tracking、速度、consent、server log | URL QA，修追踪，不补访问 |
| sessions 高 offer clicks 低 | CTA、页面承诺、移动端体验、广告密度 | 修页面，回写 landing version |
| offer clicks 高 postback 低 | subid、click_id、transaction_id、buyer endpoint | 对账 postback，不伪造转化 |
| conversions 高 paid revenue 低 | primary conversion、lead quality、buyer reject、deduction | 改 conversion goal，停低质 source |
| CTR 高 CVR 低 | ad promise、angle、query intent、source quality | 素材降级，改关键词或页面 |
| revenue 突然回撤 | finalized、deduction、invalid traffic、reject reason | 等结算，做收入复盘 |
| policy issue | ad text、destination、misrepresentation、editorial、sensitive vertical | 修复证据包和申诉 |
| URL 在目标 GEO 失败 | CDN、DNS、WAF、geo restriction、SSL、robots | 修可访问性，不做隐藏页 |
| task 连续失败 | payload hash、权限、Scripts limits、execution logs | 停重试，修任务模板 |

## 10. 告警规则设计原则

好的规则应该：

- 触发后能说明具体对象和行动。
- 有最小样本量，避免一两个点击就告警。
- 有时间窗口，避免 conversion lag 造成误杀。
- 按 source、geo、device、campaign、landing version 分层。
- 与业务可承受损失相关，例如现金预算、paid RPV、reject rate。
- 能去重，同一个根因不要生成十几条重复 alert。
- 能沉默已知维护窗口。
- 能升级：watch 多次触发后变 action，action 未处理变 freeze。

坏规则：

- “ROI 低一点就报警”，没有样本量。
- “CTR 异常就加预算”，只看点击。
- “Google Ads conversion 增长就扩量”，不看 paid revenue。
- “tracking error 就自动重复提交”，可能放大错误。
- “所有异常都自动改后台”，没有审批和回滚。

## 11. 系统落地

当前 V1 已有：

| 能力 | 位置 |
| --- | --- |
| 指标导入 | `/metrics/import` |
| 基于指标生成建议 | `adsworkbench/services/analytics.py` |
| 优化/止损队列 | `/optimization`，`optimization_actions` |
| 链接计划和人工轮换 | `/links`，`link_rules` |
| 任务状态和手动执行 | `/tasks`，`task_jobs` |
| 风险审计 | `/risk-audits` |
| 审计日志 | `/logs` |
| 来源库 | `/sources` |

后续建议新增：

```sql
CREATE TABLE alert_rules (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  rule_key VARCHAR(96) NOT NULL UNIQUE,
  metric_scope VARCHAR(64) NOT NULL,
  severity VARCHAR(16) NOT NULL,
  threshold_json JSON NOT NULL,
  min_sample_json JSON NOT NULL,
  lookback_window VARCHAR(32) NOT NULL,
  cooldown_minutes INT NOT NULL DEFAULT 1440,
  safe_action_type VARCHAR(64) NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);

CREATE TABLE alert_events (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  rule_id BIGINT NOT NULL,
  offer_id BIGINT NULL,
  campaign_draft_id BIGINT NULL,
  object_scope JSON NOT NULL,
  triggered_at DATETIME NOT NULL,
  metric_window VARCHAR(64) NOT NULL,
  trigger_values JSON NOT NULL,
  baseline_values JSON NULL,
  severity VARCHAR(16) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'open',
  evidence_urls JSON NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE TABLE incident_cases (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  incident_key VARCHAR(96) NOT NULL UNIQUE,
  severity VARCHAR(16) NOT NULL,
  category VARCHAR(64) NOT NULL,
  owner VARCHAR(96) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'triage',
  started_at DATETIME NOT NULL,
  contained_at DATETIME NULL,
  resolved_at DATETIME NULL,
  root_cause TEXT,
  impact_summary TEXT,
  postmortem TEXT,
  created_at DATETIME NOT NULL
);

CREATE TABLE incident_evidence_links (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  incident_id BIGINT NOT NULL,
  evidence_type VARCHAR(64) NOT NULL,
  evidence_url TEXT NOT NULL,
  evidence_hash VARCHAR(64) NULL,
  notes TEXT,
  created_at DATETIME NOT NULL
);
```

这些表只保存规则、事件、证据和复盘，不保存 Cookie、代理、指纹、验证码、账号凭据，也不执行未经审批的后台写入。

## 12. ADXKit 对应点和完成形态

| ADXKit 类能力 | 行业需求 | 本系统完成形态 |
| --- | --- | --- |
| 数据同步 | 定期发现 cost/revenue/URL/task 异常 | `/metrics/import`、未来 sync snapshots |
| 优化建议 | 把异常转成下一步动作 | `/optimization` 生成 stop_loss、pause_check 等 |
| 任务状态 | 看任务成功失败和日志 | `/tasks`、`/logs` |
| 换链接监控 | URL 出错时回滚或修复 | `/links`、link_version、audit log |
| 一键执行 | 快速处理异常 | 只做审批后的 CSV/Scripts preview/人工执行 |
| 风险动作 | 防关联、补点击、隐藏页 | 不实现，只做审计和合规替代 |

完成标准：

- 每个异常有明确指标、证据、责任人和状态。
- 每个止损动作有审批和回滚点。
- 每次修复后有验证窗口。
- 每次严重事故有 postmortem。
- 每条规则有来源和业务解释。

## 13. QA 清单

上线一个新 offer 或 campaign 前：

- 是否设置测试预算、硬止损和最大可亏损金额。
- 是否能导入 cost/click/session/offer click/postback/revenue。
- 是否有 campaign、landing、link、creative、subid 维度。
- 是否区分 estimated、approved、finalized、paid revenue。
- 是否有 URL、tracking、postback 和 policy 证据。
- 是否定义 L2/L3 触发条件。
- 是否知道谁可以批准停量、降预算、换链接。

每日检查：

- open L2/L3 alert 是否处理。
- 昨日 cost 是否超过计划。
- click/session/postback/revenue 是否断裂。
- new policy issue 是否出现。
- Change History 是否有未登记改动。
- task failure 是否连续出现。
- source/publisher/subid 是否有异常集中。

每周复盘：

- 哪些 alert 是噪声，要降级或加样本阈值。
- 哪些事故漏报，要新增规则。
- 哪些规则触发后没有人处理，要明确 owner。
- 哪些 stop_loss 动作太慢，要前移监控点。
- 哪些扩量依据用了 estimated revenue，要纠正。

## 14. 信息来源 URL

| 来源 | URL | 用法 |
| --- | --- | --- |
| Google Ads Help, About spending limits | https://support.google.com/google-ads/answer/10486637 | 支撑 average daily budget、daily spending limit、monthly spending limit 和 served/billed cost 监控 |
| Google Ads Help, Set up automated rules | https://support.google.com/google-ads/answer/2472779 | 支撑自动规则存在执行延迟和条件设计，V1 只做建议和审批 |
| Google Ads Help, Common ways to use automated rules | https://support.google.com/google-ads/answer/2497710 | 支撑按时间、预算、成本和状态自动化的风险边界 |
| Google Ads Help, Data discrepancies: Factors and troubleshooting | https://support.google.com/google-ads/answer/7457111 | 支撑 Google Ads、GA4、第三方和内部报表差异的诊断 |
| Google Ads Help, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑近期 CPA/ROAS/RPV/ROI 告警要考虑 conversion delay |
| Google Ads Help, Invalid clicks: Definition | https://support.google.com/google-ads/answer/42995 | 支撑异常点击和无效流量分诊，不用补点击修报表 |
| Google Ads Help, About explanations | https://support.google.com/google-ads/answer/9000655 | 支撑大幅波动可以结合 explanations 看 budget、bidding、conversion delay、asset、eligibility 和 Change history |
| Google Ads Help, About change history | https://support.google.com/google-ads/answer/19888 | 支撑异常前后按变更时间线查预算、关键词、URL、素材和操作人 |
| Google Ads API, Change event | https://developers.google.com/google-ads/api/docs/change-event | 支撑未来通过官方 API 读取变更事件用于事故证据 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑报表同步、快照和维度分段 |
| Google Ads Scripts, Limits | https://developers.google.com/google-ads/scripts/docs/limits | 支撑任务执行和重试不能无视 Scripts 配额、时间和账号限制 |
| Google Ads Scripts, Execution logs | https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs | 支撑任务失败需要保存脚本日志和错误证据 |
| Google Analytics Help, Analytics Insights | https://support.google.com/analytics/answer/9443595 | 支撑 automated/custom insights、email alerts 和异常检测思路 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 URL、landing、可访问性、crawlability 和 destination mismatch 告警 |
| PageSpeed Insights API | https://developers.google.com/speed/docs/insights/v5/get-started | 支撑未来页面速度和体验监控 |
| Google SRE Book, Monitoring Distributed Systems | https://sre.google/sre-book/monitoring-distributed-systems/ | 支撑低噪声告警、black-box/white-box monitoring 和四个黄金信号 |
| Google SRE Workbook, Alerting on SLOs | https://sre.google/workbook/alerting-on-slos/ | 支撑告警窗口、错误预算和可行动告警设计 |
| Google SRE Book, Managing Incidents | https://sre.google/sre-book/managing-incidents/ | 支撑事故角色、分诊、协作和恢复流程 |
| Google SRE Book, Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ | 支撑无责复盘、根因和预防项 |
