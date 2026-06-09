# 任务编排、安全审批、执行日志与事故复盘手册
更新时间：2026-06-09

本文拆解 ADXKit 类系统里的“定时任务、执行状态、成功失败、日志”能力，并把它转成 Ads 套利团队可以落地的安全流程。任务编排不是为了无人值守接管 Google Ads 后台，而是为了把投放草稿、页面复核、Scripts payload、链接计划、指标对账和事故复盘做成可追踪、可审批、可回滚的运营闭环。

本文不提供 Ads Cookie 登录、自动绕过 2FA/安全挑战、补点击、刷展示、模拟自然流量、代理/指纹/Worker 规避关联、cloaking、审核页/用户页不一致、封禁后换号继续投放等执行方案。这些语义必须进入风险审计或事故复盘，而不是进入任务队列。

## 1. 为什么任务编排是套利风控核心

Ads 套利的利润来自很多小样本测试和少数正 ROI 组合。任务系统一旦失控，会把一个错误放大到预算、账号、站点、收入和政策风险上：

- 预算放大：错误的预算、出价或扩量任务会在回传延迟前先烧掉现金。
- 链接放大：错误的 Final URL、tracking template 或换链计划会造成审核、转化丢失或页面不一致。
- 创意放大：未经 Claim 审核的标题、描述和 AI 文案会制造误导、夸大或敏感垂类风险。
- 数据放大：重复导入、重复回传或错误归因会让优化模型学习到错误信号。
- 账号放大：登录失败、授权失败和安全挑战如果被后台任务反复重试，会从普通故障升级成账号安全事件。

因此，套利团队真正需要的不是“把所有动作自动化”，而是把每个动作变成：有输入证据、有风险等级、有审批人、有预览结果、有执行日志、有失败处理、有复盘结论。

## 2. ADXKit 对应点和安全完成形态

| ADXKit 类能力 | 行业需求 | 本系统完成形态 |
| --- | --- | --- |
| 定时任务 | 定期检查页面、链接、报表、Scripts payload 和指标 | `/tasks` 安全任务中心，支持手动执行和 interval 元数据 |
| 执行状态 | 看成功、失败、最后一次结果和次数 | `task_jobs.status`、`run_count`、`success_count`、`failure_count`、`last_result` |
| 日志 | 出问题后追踪是谁创建、执行了什么 | `/logs` 和 `audit_logs` 记录创建、导出、执行、换链等事件 |
| 批量操作 | 减少重复人工 | 只做 CSV、Scripts JSON、预览和人工确认，不接管浏览器 Cookie |
| 换链接 | 修复断链、UTM、同主题候选 URL | `/links` 只允许合规链接计划和人工确认 |
| 失败重试 | 不漏任务 | 仅对安全、幂等、非登录类任务重试；认证、挑战、无效流量缺口不重试 |

完成边界：可以复刻“任务治理系统”，不能复刻“用任务队列做账号接管、刷量或规避检测”。

## 3. 原理解释：一个安全任务由哪些对象组成

安全任务不是简单的 `cron + function`。至少包含七个对象：

| 对象 | 说明 | 示例字段 |
| --- | --- | --- |
| Intent | 任务目的 | 页面复核、CSV 导出检查、Scripts payload 预览、指标复核 |
| Scope | 影响范围 | offer_id、campaign_draft_id、link_rule_id、account customer id |
| Evidence | 输入证据 | landing snapshot、creative id、payload hash、source URL、CSV 文件名 |
| Approval | 放行状态 | reviewer、reviewed_at、approval_note、risk_level |
| Execution | 执行结果 | started_at、finished_at、status、error_code、result summary |
| External Trace | 外部平台证据 | Google Ads Change history、Scripts execution log、ChangeEvent id |
| Recovery | 失败和回滚 | rollback plan、freeze flag、incident id、postmortem link |

任务治理的本质是把“动作”拆成“可证明的意图”和“可审计的结果”。如果一个动作无法说明目的、范围、输入、审批和回滚，就不应该被自动执行。

## 4. 任务分级

| 等级 | 允许范围 | 默认策略 |
| --- | --- | --- |
| L0 只读 | 报表检查、页面读取、链接状态检查、素材风险提示 | 可定时运行，记录日志 |
| L1 预览 | 生成 CSV、Scripts JSON、Bulk upload preview、诊断报告 | 可运行，必须人工看结果 |
| L2 低风险写 | 添加否定词、暂停明显失败的小预算测试、修复可证明断链 | 需要阈值、审批和回滚点 |
| L3 高风险写 | 改预算、改 Final URL、启停 campaign、创建广告 | 双人复核，先 preview，再人工确认 |
| 禁止 | Cookie 登录、2FA/验证码处理、补点击、刷展示、模拟访问、代理/指纹规避、cloaking、封禁换号 | 不进入任务中心，进入风险审计或事故复盘 |

V1 只实现 L0/L1 和少量人工确认动作。L2/L3 即使未来扩展，也必须先补齐审批表、版本表、回滚字段和外部变更证据。

## 5. 审批原则

审批不是签名形式，而是防止错误扩散的闸门。建议规则：

- 谁创建，谁不能单独批准高风险写入。
- 同一任务必须绑定具体 Offer、投放草稿、链接计划或报表批次，不能用“all accounts”“all campaigns”这类模糊范围。
- 审批前必须看到输入摘要、目标对象、预算影响、链接影响、政策风险和 rollback plan。
- 审批记录必须保留来源 URL。政策问题要引用 Google Ads 政策、Scripts 文档或内部 SOP。
- 超过预算阈值、改 Final URL、开启自动化流量或改变 primary conversion 的任务，默认 L3。

审批结论建议只有四种：`approve_preview`、`approve_apply`、`needs_fix`、`reject`。不要用“先跑看看”替代审批。

## 6. Google Ads 安全执行通道

### 6.1 Google Ads Scripts

Google Ads Scripts 是账户内授权脚本环境，适合做报表、检查、预览和有限批量变更。它的安全意义在于：

- 需要授权用户在 Google Ads 语境内授权。
- 有脚本执行限制和运行日志。
- 可以通过 Bulk Upload 先 preview，再 apply。
- 可以把 payload、脚本版本和执行结果归档。

本系统的 Scripts 方向是：Flask 里生成 `manual_review_required` payload，授权用户把 payload 放进 Scripts preview 模板，先看预览，再决定是否人工 apply。系统不保存 Google 登录 Cookie，不远程控制浏览器后台。

### 6.2 Change History 与 ChangeEvent

Google Ads 后台的 Change history 和 Google Ads API 的 change event/change status 能帮助追踪“谁在什么时候改了什么”。套利团队应把它当作外部审计证据：

- 内部任务日志记录：我们计划做什么、输入是什么、审批是谁。
- Scripts log 记录：脚本实际跑了什么、错误是什么。
- Change history 记录：Google Ads 里最终发生了什么变更。
- 指标日报记录：变更后 cost、click、conversion、revenue、ROI 怎么变化。

事故复盘时不要只看本系统日志，也要拉取 Change history、Scripts execution log、导出的报表和页面截图。

### 6.3 Google Ads API

如果未来接入官方 API，仍然要遵循同一套治理：先 `validate_only` 或 dry run，再处理 partial failure，再写入审计日志。API 不是绕过审批的理由，反而更需要幂等键、变更版本和失败隔离。

## 7. 执行日志字段

建议每次任务执行至少记录：

- `task_id`、`task_type`、`task_name`。
- `risk_level`、`approval_status`、`reviewer`。
- `offer_id`、`campaign_draft_id`、`link_rule_id`。
- `input_hash`、`payload_version`、`source_urls`。
- `started_at`、`finished_at`、`duration_ms`。
- `status`：queued、running、success、failed、blocked、cancelled。
- `result_summary`：对象数量、跳过数量、warning、error。
- `external_trace`：Google Ads script name、execution id、Change history 时间范围。
- `rollback_plan`、`incident_id`。

日志的目标不是“有一行记录”，而是让三天后的人能回答：为什么跑、谁批准、跑了什么、有没有外部变更、怎么恢复。

## 8. 幂等、重试和去重

任务系统最容易出错的地方是重复执行。安全原则：

- 用 `idempotency_key = task_type + scope + payload_hash + target_version` 去重。
- 写入前先读取当前状态，确认目标仍然和审批时一致。
- 只对网络超时、读取失败、导出失败这类安全错误重试。
- 对预算、Final URL、conversion action、账号状态类任务不做无限重试。
- 认证失败、2FA、安全挑战、captcha、login required 必须转人工，不允许后台重试。
- revenue/click/session 对账缺口不能通过补点击、补展示、模拟访问来修复，只能通过追踪 QA、数据回补、来源隔离和报表说明处理。

重试的默认上限建议是 2 到 3 次，并且每次都记录原因和结果。

## 9. 事故响应流程

当任务造成异常，按下面顺序处理：

1. Freeze：暂停同类型任务、相关链接计划和相关扩量建议。
2. Snapshot：导出任务日志、Scripts log、Change history、指标日报、页面截图和 payload。
3. Triage：判断是预算、链接、创意、追踪、报表、政策还是账号问题。
4. Contain：暂停受影响 campaign、回退 URL、撤销 payload、隔离流量来源或停止导入。
5. Reconcile：按 click -> session -> revenue、estimated -> finalized、buyer feedback 逐层对账。
6. Postmortem：写清时间线、触发条件、影响范围、根因、修复动作和预防项。
7. Guardrail：把根因转成阈值、白名单、审批规则或校验脚本。

复盘重点不是追责，而是把下一次同类错误挡在执行前。

## 10. 禁止任务语义

任务名称、类型、备注、payload 或未来扩展配置中，如果出现以下语义，应拒绝创建或转为风险审计：

| 禁止语义 | 为什么禁止 | 合规替代 |
| --- | --- | --- |
| login、signin、password、cookie、session | 涉及会话接管和凭证风险 | 使用授权的 Scripts、API、Editor CSV、人工操作记录 |
| otp、2fa、mfa、captcha、challenge、recovery | 涉及安全挑战绕过 | 转账号安全事件和人工确认 |
| click、impression、visit、traffic、scroll、bounce、autosurf | 涉及无效流量或报表污染 | 做对账、追踪 QA、来源隔离 |
| proxy、fingerprint、worker evasion | 涉及规避关联检测 | 做合法权限隔离、账号治理和审计 |
| cloaking、review page、user page mismatch | 涉及审核和用户页不一致 | 做链接一致性、Final URL QA、页面质量修复 |
| ban evasion、account pool、switch account | 涉及规避政策执行 | 做暂停原因修复、证据包和申诉 |

这也是本系统 `services/tasks.py` 白名单和禁用关键词的设计依据。

## 11. 系统落地

当前 V1 已实现：

- `/tasks`：创建安全任务，记录类型、绑定对象、调度模式、执行次数和最后结果。
- `/tasks/<id>/run`：手动执行一次安全任务。
- `TaskJob`：保存状态、run_count、success_count、failure_count、last_result、next_run_at。
- `services/tasks.py`：任务类型白名单和禁用关键词拦截。
- `/logs`：记录任务创建和执行审计。
- `/campaigns/<id>/export.script.json`：生成带 `no_cookie_automation` 和 `requires_human_approval` 的 payload。
- `/links`：链接计划默认人工确认。

任务中心的 CSV / Scripts 导出检查也会调用 campaign preflight。未批准 campaign、未放行 Claim 审核或未关闭广告审核案例时，任务会失败并把 blockers 写入 `last_result`；任务中心不能绕过导出路由的上线前闸门。

当前 V1 不做：

- 自动登录 Google Ads。
- 存储 Cookie、密码、验证码、恢复码或浏览器 Profile。
- 自动处理安全挑战。
- 远程执行 Google Ads Scripts。
- 自动 apply 高风险写入。
- 自动补点击、补展示或模拟自然访问。

## 12. 后续数据模型建议

如果要把任务中心从 V1 提升到更完整的生产系统，建议新增：

| 表 | 用途 |
| --- | --- |
| `task_approvals` | 保存审批状态、审批人、审批意见、风险等级 |
| `task_run_logs` | 保存每次执行的 started_at、finished_at、input_hash、result_json |
| `task_payload_versions` | 保存 payload hash、diff、版本和回滚点 |
| `external_change_events` | 保存 Change history 或 ChangeEvent 摘要 |
| `incident_reviews` | 保存事故时间线、影响、根因和预防项 |
| `automation_guardrails` | 保存预算上限、域名白名单、禁止词、重试上限 |

这些表服务于审计和风控，不服务于规避平台检测。

## 13. QA 清单

上线一个新任务类型前，逐项确认：

- 是否属于 L0/L1，还是 L2/L3/禁止。
- 是否有明确 scope，而不是全局模糊执行。
- 是否能 dry run 或 preview。
- 是否有输入 hash 和 payload 版本。
- 是否有人工审批字段。
- 是否能写入 `audit_logs`。
- 是否能从 Change history 或 Scripts log 找到外部证据。
- 是否有回滚或冻结动作。
- 是否不会处理登录、Cookie、2FA、captcha 或安全挑战。
- 是否不会生成点击、展示、访问、滚动、跳出或虚假转化。
- 是否不会根据 bot、IP、指纹、Cookie 或审核状态分流页面。

任何一项答不上来，就先不要自动化。

## 14. 信息来源 URL

- ADXKit homepage: https://adxkit.com/
- Google Ads Help, Using scripts to make automated changes: https://support.google.com/google-ads/answer/188712
- Google Ads Scripts, Authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- Google Ads Scripts, Limits: https://developers.google.com/google-ads/scripts/docs/limits
- Google Ads Scripts, Bulk upload: https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload
- Google Ads Scripts, Execution logs: https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs
- Google Ads Scripts, Preview mode: https://developers.google.com/google-ads/scripts/docs/concepts/preview
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
- Google Ads API, Change event: https://developers.google.com/google-ads/api/docs/change-event
- Google Ads API, Mutating overview: https://developers.google.com/google-ads/api/docs/mutating/overview
- Google Ads API, Partial failures: https://developers.google.com/google-ads/api/docs/best-practices/partial-failures
- Google Ads API, Quotas: https://developers.google.com/google-ads/api/docs/best-practices/quotas
- Google Ads policy, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads policy, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google SRE, Postmortem culture: https://sre.google/sre-book/postmortem-culture/
- Google SRE, Managing incidents: https://sre.google/sre-book/managing-incidents/
- Google SRE Workbook, Postmortem culture: https://sre.google/workbook/postmortem-culture/
