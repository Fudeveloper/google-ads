# Google Ads Scripts 数据同步、快照与一致性手册
更新时间：2026-06-09

本文拆解 ADXKit 类产品常见的“Google Ads Script 15 分钟双向同步、无需 API 审批”叙事，并把它转成 Ads 套利团队可执行的同步治理方法。重点不是把 Google Ads 后台变成可被 Cookie 接管的镜像，而是用授权 Scripts、报表快照、人工审批、窗口重拉、Change history 和执行日志，建立可解释的数据闭环。

本文不提供 Ads Cookie 登录、后台 UI 接管、绕过 2FA/安全挑战、绕审核写入、补点击、刷展示、模拟自然流量、代理/指纹/Worker 规避关联、cloaking 或封禁换号等实现。

## 1. 为什么同步是套利系统的核心能力

Ads 套利不是只看一个后台的转化数。一个测试是否赚钱，至少要把以下数据对齐：

- Google Ads 花费、点击、展示、搜索词、素材和变更记录。
- 落地页 server request、GA4 session、跳转链和参数保留。
- Offer / affiliate / lead buyer 的 postback、approved revenue、rejected lead 和 paid revenue。
- AdSense / AdX / GAM 的 estimated revenue、finalized revenue、扣量和付款状态。
- 内部任务、创意、链接版本、审批和事故记录。

如果同步只做“每 15 分钟抓一次 Google Ads 数字”，会出现三个错误：

1. 把未稳定的当天数据当成可扩量依据。
2. 把 Google Ads conversion 当成最终可收款收入。
3. 忽略后台外部变更、链接变更和回传延迟。

同步系统的目标是让团队知道“这个数字来自哪里、何时抓取、是否稳定、和哪些外部证据一致”，而不是追求看起来实时。

## 2. ADXKit 对应点和完成形态

| ADXKit 类能力 | 行业含义 | 本系统完成形态 |
| --- | --- | --- |
| 15 分钟双向同步 | 定时读取 Google Ads 报表，并把结构化变更写回账号 | V1 只做 CSV / Scripts JSON / 手动导入和任务记录；写入必须 preview 和人工确认 |
| 无需 API 审批 | 用账号内 Google Ads Scripts 替代正式 API 开发者审批流程 | 只作为授权脚本方向，不保存 Cookie，不接管后台 UI |
| 多账号同步 | MCC 下多个 client account 批量读报表或生成检查结果 | 文档化 MCC/账号治理；V1 不做多租户和账号池 |
| 数据同步 | 把 cost、click、conversion、search term、change history 拉入工作台 | V1 已实现 `/scripts-sync` 同步评审工作台，并继续用 `/metrics/import` 导入真实指标 |
| 结构变更同步 | 创建 campaign/ad group/keyword/ad、改 URL 或预算 | V1 导出草稿和 payload；高风险写入必须人工审批 |
| 执行日志 | 看每次同步成功、失败、跳过和错误 | `/scripts-sync` 记录 script run、row count、errors、warnings、hash、冲突状态和状态流；`/logs` 留痕 |

完成边界：可以复刻“授权脚本同步和一致性治理”，不能复刻“Cookie 后台镜像、无人审批写入或规避平台控制”。

## 3. 原理解释：同步不是实时真相

同步系统有三层：

| 层 | 作用 | 风险 |
| --- | --- | --- |
| Raw snapshot | 保留某一时刻从 Google Ads / Offer / AdSense 拉到的原始数据 | 数据可能延迟、回填、被扣量或被无效流量过滤 |
| Normalized fact | 把 cost、click、session、revenue、conversion 统一到内部口径 | 字段含义不同会造成虚假 ROI |
| Decision view | 给投手看的暂停、扩量、换素材、换链接建议 | 如果直接用未稳定数据，会过早扩量或误杀测试 |

因此，15 分钟同步只能表示“系统有一个高频 heartbeat”，不能表示“指标已最终确定”。套利团队必须给每个指标加上数据状态：

- `provisional`：当天或最近几小时数据，只能预警，不能大幅扩量。
- `settling`：等待 conversion lag、postback、buyer feedback 或 revenue finalization。
- `finalized`：可以用于关账、模型训练和扩量复盘。
- `disputed`：和 server log、postback、Change history 或付款数据冲突。

## 4. 读同步：从 Google Ads 拉什么

推荐最小同步对象：

| 对象 | 关键字段 | 用途 |
| --- | --- | --- |
| Account | customer_id、currency、time_zone、status | 归因到账号、币种和时区 |
| Campaign | id、name、status、budget、bid strategy、network | 判断预算和结构 |
| Ad group | id、name、status、criterion、bid | 分析颗粒度 |
| Keyword / Search term | query、match type、cost、click、conversion | 否定词和意图复盘 |
| Ad / Asset | headline、description、asset status、performance label | 创意疲劳和 claim 风险 |
| Landing page | final_url、expanded url、mobile url | 页面质量和追踪 QA |
| Metrics daily | date、impressions、clicks、cost、conversions、conversion value | ROI 与止损 |
| Change event | user、time、resource、old/new value | 外部变更证据 |

Google Ads Scripts 的 `AdsApp.report()` 和 `AdsApp.search()` 都使用 GAQL 报表语境。`report()` 更适合表格导出，`search()` 更适合程序处理。同步设计时不要只保存聚合数，要保留 query、date range、customer_id、pulled_at 和 source hash。

## 5. 写同步：从工作台写回什么

写入分成四种：

| 类型 | 示例 | 默认策略 |
| --- | --- | --- |
| 建议 | 暂停、扩量、否定词、换素材 | 只写内部建议，不写回 Google Ads |
| 预览 | CSV、Scripts JSON、bulk upload preview | 允许生成，但必须人工检查 |
| 低风险写 | 小范围否定词、明确断链修复 | 需要审批、阈值、回滚点 |
| 高风险写 | 改预算、改 Final URL、启停 campaign、创建广告 | 双人复核，先 preview，再人工 apply |

ADXKit 类产品常说的“双向同步”，在合规设计里不应理解成“系统随时改后台”。更稳妥的定义是：工作台生成结构化 payload；授权用户在 Google Ads Scripts 或 Editor 中预览；通过审批后执行；执行后把 Change history、Scripts log 和指标变化同步回工作台。

## 6. 同步频率和数据新鲜度

15 分钟同步适合做：

- 任务状态 heartbeat。
- URL、页面、脚本执行结果检查。
- 花费快速预警。
- 导入文件是否到达的提醒。

15 分钟同步不适合做：

- 当天 ROAS 最终判断。
- buyer paid revenue 判断。
- AdSense / AdX finalized revenue 判断。
- conversion lag 未稳定时的大幅扩量。
- 无效流量扣量前的最终结论。

Google Ads performance data 不是即时稳定值。多数账号统计会有小时级延迟，一些指标每日处理；conversion lag 会让近期 CPA/ROAS 看起来偏差。套利系统应按窗口重拉：

| 窗口 | 策略 |
| --- | --- |
| Today | 每 15-60 分钟拉一次，只做预警和止损 |
| Yesterday | 每 1-3 小时重拉，处理延迟和修正 |
| Last 7 days | 每日重拉，处理 conversion lag、无效点击过滤和 postback 回填 |
| Month to date | 每日或关账前重拉，等待 finalized/paid revenue |

不要用“当前看起来 ROI 高”直接扩量，除非它已经通过回传延迟、收入状态和来源质量检查。

## 7. 多账号和 MCC 同步

Google Ads manager account scripts 可以在 MCC 下选择 client accounts，并支持并行处理多个账号。套利团队要注意：

- 第一版不做多租户，但可以记录多个 Google Ads customer id。
- 不要把 MCC 同步当成账号池、换号或规避封禁工具。
- 每个账号必须有 owner、业务主体、付款主体、网站、验证状态和访问权限记录。
- 多账号报表必须保留 `customer_id`、currency、time_zone，不能直接求平均 ROI。
- 并行同步要限制账号数量和执行时长，避免脚本限制或配额失败。

MCC 同步只解决“批量读取和批量检查”，不解决“账号关系解释不清”的合规问题。

## 8. 外部数据和中间存储

Google Ads Scripts 可以与 Google Sheets、Drive、JDBC 数据库和 URL Fetch 集成。对套利团队来说，安全用法是：

- Google Sheets：临时报表、执行状态、人工审批和小规模配置。
- MySQL：正式工作台数据仓库，保存版本和审计。
- URL Fetch：读取自有系统的 approved payload 或 inventory 状态。
- Email：发送任务摘要和异常提醒。

风险用法：

- 用外部接口下发 Cookie、验证码、账号凭证或浏览器 profile。
- 用远程配置按 bot/IP/fingerprint 切换页面。
- 用外部服务生成虚假点击、展示、访问或转化。
- 用 Worker/代理隐藏真实目的地或来源。

## 9. 冲突治理

同步冲突常见于：

- 投手在 Google Ads 后台手工改了预算，但工作台还拿旧预算生成 payload。
- 链接计划刚换 URL，Google Ads 里 Final URL 仍是旧版本。
- Scripts preview 通过，但 apply 前已有外部变更。
- conversion action、primary/secondary 状态被改，ROI 口径突然变化。
- 时区、币种或 FX rate 不一致，导致日级利润误判。

推荐冲突字段：

| 字段 | 说明 |
| --- | --- |
| `source_version_hash` | 同步读取时目标对象 hash |
| `payload_hash` | 准备写入的 payload hash |
| `last_seen_change_at` | 最近一次 Google Ads Change history 时间 |
| `approved_at` | 审批时间 |
| `apply_deadline` | 超过窗口必须重新预览 |
| `conflict_status` | clean、stale_payload、external_change、manual_review |

如果审批后发现目标对象已变，默认拒绝 apply，重新拉取快照并重新生成 payload。

## 10. 对账口径

同步到工作台后，不要把所有数字塞进一个 ROI。建议分层：

| 层 | 主来源 | 稳定性 |
| --- | --- | --- |
| Cost / Click | Google Ads reports | 小时级延迟，可能有 invalid adjustment |
| Session | server log / GA4 | 受 consent、ad blocker、tag、parallel tracking 影响 |
| Lead / Conversion | Google Ads conversion / postback / CRM | 受回传延迟和归因窗口影响 |
| Approved revenue | affiliate / buyer feedback | 常晚于 submitted conversion |
| Finalized / paid revenue | AdSense / AdX / GAM / finance | 月度或结算后稳定 |

套利判断应优先用 paid 或 approved revenue；如果只有 Google Ads conversion value，就必须标注为 `provisional`。

## 11. 失败处理和重试

安全重试：

- 报表读取超时。
- URL Fetch 临时失败。
- MySQL 写入冲突。
- CSV 文件格式错误后人工修复再导入。

禁止重试：

- 登录失败。
- 2FA、captcha、安全挑战。
- Cookie/session 过期。
- 封禁、账号暂停、验证失败。
- click/session/revenue 缺口。

这些问题不能通过同步脚本“多试几次”解决。认证问题进入账号安全；收入差异进入对账；政策问题进入风险审计。

## 12. 系统落地

当前 V1 已支持：

- `/campaigns/<id>/export.csv`：导出 Google Ads Editor CSV。
- `/campaigns/<id>/export.script.json`：导出 Scripts JSON payload，包含人工审核和 no-cookie 字段。
- `scripts/google_ads_script_payload_preview.js`：授权账号内 preview 模板。
- `/scripts-sync`：记录 Google Ads Scripts report/search、Change history、Sheets/Drive/内部导入证据、query hash、source snapshot hash、row count、error/warning、freshness、data_status、revenue_status、conflict_status、external_change_count、rerun window、preview/read-only 门禁和人工审核。
- `/scripts-sync/<id>/status`：更新 snapshot_ready、rerun_required、conflict_review、approved_for_import、imported_manual、blocked 等内部状态并写入 `/logs`。
- `/metrics/import`：人工导入日级 cost、click、conversion、revenue。
- `/tasks`：创建安全复核、导出检查、指标复核任务。
- `/logs`：记录导出、任务、换链和指标导入审计。
- `/sources`：记录同步设计和政策来源 URL。

`script_sync_reviews` 只代表同步证据和人工导入门禁，不会自动运行 Google Ads Scripts、不会自动 apply mutates、不会接管 Google Ads UI，也不会把当天 ROI 当最终收入。表单文本如果包含 Cookie、Session Token、浏览器 Profile、验证码、2FA、安全挑战、自动登录、自动发布、伪造转化、伪造收入、补点击、刷展示、代理/指纹/Worker、防关联、cloaking 或换号语义，会被拦截并改走风险审计。

V1 评分维度：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| auth mode / sync type | 16 | 授权 Scripts、人工导入、Sheets bridge 和不同同步对象的风险不同 |
| data / revenue status | 30 | provisional/settling/estimated 不能直接支持扩量 |
| freshness / row count | 16 | 同步快照要有 pulled_at 新鲜度和合理行数 |
| errors / warnings | 10 | script run 错误和大量 warning 必须先修 |
| hash evidence | 10 | source snapshot hash 与 payload/query hash 用于复盘一致性 |
| Change history / conflict | 20 | 外部变更、stale payload 和 manual_review 会阻止 apply/import |
| rerun / preview / human review | 18 | 需要重拉窗口、read-only / preview 门禁和人工审核 |

recommended_action 的含义：

| 动作 | 含义 |
| --- | --- |
| approve_manual_import | 快照、hash、Change history、数据成熟度和人审均通过，可人工导入或用于复盘 |
| snapshot_ready | 快照可用于诊断，但仍需看 blockers 和收入成熟度 |
| rerun_or_reconcile | 需要重拉窗口或对账，不用于扩量 |
| rerun_snapshot_before_apply | 有 stale payload 或外部变更，先重拉并重新 preview |
| fix_script_errors | 先修 Scripts 错误或导出错误 |
| reconcile_dispute | 数据争议先对账，不用于预算动作 |
| hold_for_human_review | 缺人审或证据不足，不能进入导入/决策 |

当前 V1 不做：

- 自动登录 Google Ads。
- 保存 Google Cookie、密码、验证码、恢复码或浏览器 Profile。
- 远程操控 Google Ads UI。
- 无人审批 apply 变更。
- 伪造点击、展示、session、conversion 或 revenue。

## 13. 后续数据模型建议

| 表 | 作用 |
| --- | --- |
| `google_ads_sync_runs` | 每次同步的 customer_id、date_range、query、status、row_count、pulled_at |
| `google_ads_metric_snapshots` | 保存原始 Google Ads 日级快照和 hash |
| `google_ads_change_events` | 保存 ChangeEvent / Change history 摘要 |
| `google_ads_object_versions` | campaign/ad group/keyword/ad 的结构版本 |
| `sync_conflicts` | 保存 stale payload、外部变更和人工处理结果 |
| `revenue_state_daily` | 区分 provisional、settling、finalized、paid、disputed |
| `script_execution_logs` | 保存 script name、mode、preview/apply、warnings、errors |

这些表用于数据一致性和审计，不用于 Cookie 后台同步。

## 14. QA 清单

上线同步流程前检查：

- 是否明确是读同步、预览写入还是正式写入。
- 是否记录 customer_id、currency、time_zone 和 date_range。
- 是否保存 pulled_at、query、payload_hash 和 source_version_hash。
- 是否区分 provisional、settling、finalized 和 paid。
- 是否设置窗口重拉，不把当天数据当最终值。
- 是否能从 Change history / ChangeEvent 查到外部变更。
- 是否把 Google Ads conversions 和 buyer paid revenue 分开。
- 是否把 invalid traffic、conversion lag、postback delay 写入解释口径。
- 是否不会处理登录、Cookie、2FA、captcha 或安全挑战。
- 是否不会补点击、刷展示、模拟访问或伪造转化。
- 是否不会根据 bot/IP/Cookie/指纹/审核状态分流页面。

## 15. 信息来源 URL

- ADXKit homepage: https://adxkit.com/
- Google Ads Scripts, Reports: https://developers.google.com/google-ads/scripts/docs/concepts/reports
- Google Ads Scripts, Manager account scripts: https://developers.google.com/google-ads/scripts/docs/concepts/manager-scripts
- Google Ads Scripts, External data integration: https://developers.google.com/google-ads/scripts/docs/integrations/external-data
- Google Ads Scripts, Limits: https://developers.google.com/google-ads/scripts/docs/limits
- Google Ads Scripts, Execution logs: https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs
- Google Ads Scripts, Preview mode: https://developers.google.com/google-ads/scripts/docs/preview
- Google Ads Scripts, Mutate: https://developers.google.com/google-ads/scripts/docs/concepts/mutate
- Google Ads Scripts, Bulk upload: https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload
- Google Ads Scripts, Link Checker solution: https://developers.google.com/google-ads/scripts/docs/solutions/link-checker
- Google Ads Help, About data freshness: https://support.google.com/google-ads/answer/2544985
- Google Ads Help, Data discrepancies: https://support.google.com/google-ads/answer/7457111
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads API, Reporting overview: https://developers.google.com/google-ads/api/docs/reporting/overview
- Google Ads API, Google Ads Query Language: https://developers.google.com/google-ads/api/docs/query/overview
- Google Ads API, Change event: https://developers.google.com/google-ads/api/docs/change-event
- Google Ads API, API limits and quotas: https://developers.google.com/google-ads/api/docs/best-practices/quotas
- Google Ads policy, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
