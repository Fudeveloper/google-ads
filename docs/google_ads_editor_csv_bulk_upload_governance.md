# Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册
更新时间：2026-06-09

本文拆解 ADXKit 类系统里的“广告层级批量管理、一键提交投放、CSV / Scripts 导出”能力，并把它转成 Ads 套利团队可执行的 Google Ads Editor / Bulk Upload 治理流程。它的目标是：让 Offer、创意、关键词、Final URL 和预算草稿可以批量准备、人工检查、离线导入、分批发布和回流审计，而不是用 Cookie 接管 Google Ads 后台。

本文不提供 Ads Cookie 登录、后台 UI 自动点击、绕过 2FA/安全挑战、绕审核发布、补点击、刷展示、模拟自然流量、cloaking、代理/指纹/Worker 规避关联或封禁后换号继续投放的实现。

## 1. 为什么 Editor / CSV 是套利团队的安全核心

Ads 套利每天会生成大量小测试：不同 Offer、国家、关键词意图、创意角度、页面版本和预算。完全手工创建太慢，用 Cookie 自动操作后台又会带来账号安全、审计缺失和平台规则风险。Google Ads Editor / CSV / Bulk Upload 的价值在于：

- 把重复创建 campaign、ad group、keyword、ad 和 URL 的工作前置到工作台。
- 让投手在 Google Ads Editor 或 Bulk Upload Preview 中检查字段和错误。
- 把真正的发布动作留给授权用户。
- 保留导出文件、版本、审核人、发布时间和 Change history。
- 支持回滚和事故复盘。

一句话：Editor / CSV 是“批量准备 + 人工授权执行”，不是无人后台接管。

## 2. ADXKit 对应点和完成形态

| ADXKit 类能力 | 行业含义 | 本系统完成形态 |
| --- | --- | --- |
| 广告层级管理 | Campaign、ad group、keyword、ad 批量生成 | `/campaigns` 投放草稿和 CSV 导出 |
| 一键提交投放 | 从草稿到 Google Ads 后台执行 | V1 不自动提交；导出 CSV / Scripts JSON 后人工执行 |
| 批量操作 | 批量添加关键词、广告、URL 和预算 | 只做草稿和导出，正式写入需要 Editor/Preview/人工确认 |
| 执行结果 | 看成功、失败和错误 | 通过 Editor 检查、Bulk Upload 结果、Change history 和 `/logs` 对齐 |
| 链接更新 | 批量改 Final URL 或 tracking 参数 | 只允许合规链接计划和人工确认，不做审核页/用户页分流 |

完成边界：复刻批量构建和可审计发布流程，不复刻后台自动点击、Cookie 会话复用或绕审核写入。

## 3. 原理解释：Editor / CSV 工作流

安全流程应分成 8 步：

1. Draft：工作台生成 campaign draft、creative set、keyword list 和 final_url。
2. Evidence：绑定落地页摘要、Claim 审核、关键词意图、预算测算和来源 URL。
3. Export：导出 Google Ads Editor CSV 或 Scripts bulk upload payload。
4. Offline Review：投手在 Editor / spreadsheet 中检查字段、匹配类型、预算、URL、状态和政策风险。
5. Preview / Check：使用 Editor 检查变更或 Bulk Upload preview 发现错误。
6. Approve：人工确认发布范围、预算影响、链接影响和回滚方案。
7. Post / Apply：授权用户在 Google Ads Editor、Google Ads 后台或 Scripts 中发布。
8. Reconcile：把发布结果、Change history、错误报告和后续指标导回工作台。

任何跳过 4-6 步的“自动发布”，都容易把模板错误放大成账号级事故。

## 4. 适合 CSV / Editor 的操作

| 操作 | 适合程度 | 注意点 |
| --- | --- | --- |
| 创建测试 campaign / ad group | 高 | 状态建议默认 paused 或 limited budget |
| 批量添加 phrase/exact 关键词 | 高 | 先排除品牌词、敏感词和低意图词 |
| 批量添加 RSA 文案候选 | 中 | 必须做 Claim 审核和页面证据映射 |
| 批量添加否定词 | 高 | 需要保留 search term 来源和原因 |
| 更新 tracking template / Final URL suffix | 中 | 必须做参数保留和跳转链 QA |
| 修改 Final URL | 高风险 | 需要链接计划、页面一致性和审批 |
| 修改预算和出价 | 高风险 | 需要预算上限、止损阈值和回滚点 |
| 启停 campaign | 高风险 | 需要变更原因和影响范围 |

不适合 CSV / Editor 直接自动发布的操作：

- 大范围预算扩量。
- 未审核的新垂类或敏感垂类。
- 页面没有 proof 的强声明创意。
- 改 Final URL 绕过审核。
- 用不同页面承接 Google 审核和真实用户。
- 封禁、拒登、账号限制后换账号或换域名继续投。

## 5. CSV 字段合同

本系统当前导出的 CSV 是简化草稿，字段包括：

| 字段 | 用途 |
| --- | --- |
| `Campaign` | 投放草稿名称 |
| `Ad group` | 当前用 Offer vertical 作为广告组语境 |
| `Keyword` | 关键词候选 |
| `Match type` | 默认 Phrase，后续可扩展 Exact/Broad |
| `Final URL` | 用户最终到达页面 |
| `Daily budget` | 日预算 |
| `Bid strategy` | 出价策略 |
| `Headline 1..15` | RSA 标题候选 |
| `Description 1..4` | RSA 描述候选 |

建议后续扩展字段：

- `Campaign status`：默认 paused。
- `Ad group status`：默认 paused。
- `Labels`：offer、country、vertical、test batch。
- `Tracking template` / `Final URL suffix`：明确参数。
- `Custom parameter`：追踪维度。
- `Review status`：internal only，用于导出前审计，不一定导入 Google Ads。
- `Payload hash`：内部版本标识。

字段合同必须稳定。任何新增字段，都要在开发文档、使用文档、测试和导出样例中同步更新。

## 6. 版本、审批和回滚

每个 CSV / Bulk Upload 批次建议记录：

- `batch_id`：内部批次编号。
- `campaign_draft_id`、`offer_id`、`creative_set_id`。
- `csv_hash` / `payload_hash`。
- `row_count`、`keyword_count`、`ad_count`。
- `created_by`、`reviewed_by`、`approved_at`。
- `target_customer_id`、`account_timezone`、`currency`。
- `expected_budget_delta`。
- `url_change_count`。
- `preview_result`、`editor_check_result`。
- `post_status`：not_posted、posted、partial_error、rolled_back。
- `change_history_window`。

回滚策略：

- 新建结构默认 paused，确认无误后再启用。
- URL、预算、出价和 conversion action 变更必须保留前值。
- 如果 Editor / Bulk Upload 出现部分失败，不要手工补一半就结束；要记录失败行和修复批次。
- 大批量变更按国家、Offer、账号或 campaign 分批发布，避免一次性放大错误。

## 7. Bulk Upload 与 Editor 的区别

| 维度 | Google Ads Editor | Google Ads Bulk Upload / Scripts Bulk Upload |
| --- | --- | --- |
| 操作方式 | 桌面离线编辑后发布 | 后台或脚本上传 spreadsheet / payload |
| 人工检查 | 强，适合投手逐项看 | 依赖 preview、日志和结果文件 |
| 自动化程度 | 中，适合人审批量 | 高，必须加 guardrails |
| 风险点 | 人工误选账号或发布范围 | 脚本直接 apply、字段映射错误 |
| 适合用途 | 批量创建和修改草稿 | 批量预览、批量导入、低风险规则化变更 |

V1 更推荐 Editor CSV，因为它天然把“导出”和“发布”分开。Scripts Bulk Upload 可以作为后续增强，但必须默认 preview，不自动 apply。

## 8. 常见事故模式

| 事故 | 根因 | 预防 |
| --- | --- | --- |
| 广告创建到错误账号 | customer_id 未记录或投手导入错账号 | CSV 批次绑定 customer_id，发布前人工确认 |
| 大预算直接上线 | 默认 enabled，预算字段错误 | 默认 paused，预算上限检查 |
| URL 指向旧页面或错页面 | 草稿生成后链接被改 | 发布前做 redirect chain 和 final URL QA |
| 标题夸大或无证据 | AI 文案未做 Claim 审核 | 导出前阻断 high severity claim |
| 关键词过宽 | broad match 或低意图词未审核 | 关键词意图分层，默认 phrase/exact，小预算测试 |
| 部分失败被忽略 | 上传结果只看整体成功 | 保存失败行和 error message |
| 后台手工修改覆盖草稿 | 审批后外部变更 | 发布前拉 Change history，发现冲突重新审批 |

## 9. 上线前 QA 清单

导出 CSV / Bulk Upload 前检查：

- Offer 是否通过准入评分。
- 落地页是否可访问、HTTPS、与广告承诺一致。
- Final URL、tracking template、Final URL suffix 是否通过 QA。
- 创意是否完成 Claim 审核。
- 关键词是否完成意图和品牌词/敏感词筛查。
- 日预算是否在测试上限内。
- campaign / ad group 默认状态是否安全。
- CSV 是否有 batch_id、hash、row_count 和 reviewer。
- 目标账号、时区、币种是否确认。
- 是否有回滚方案和 Change history 对齐窗口。

## 10. 系统落地

当前系统已实现 V1 批量变更治理工作台。`/bulk-upload` 会把 Google Ads Editor CSV、Scripts Bulk Upload preview 或后台 Bulk Upload preview 的批次证据保存到 `bulk_upload_reviews`，字段包括 offer/campaign 绑定、export_type、batch_id、csv_hash、payload_hash、row_count、keyword_count、ad_count、target_customer_id、account_timezone、currency、expected_budget_delta、url_change_count、high_risk_change_count、preflight_status、preview_status、editor_check_status、post_status、default_paused、human_review、change_history_attached、rollback_plan、target_customer_confirmed、policy_review_complete、score、risk_level、recommended_action、budget_delta_percent、change_scope、blockers、status、notes 和 source_urls。

- `/campaigns` 创建投放草稿。
- `/campaigns/<id>/export.csv` 导出 Google Ads Editor 风格 CSV。
- `/campaigns/<id>/export.script.json` 导出 Scripts payload。
- `/bulk-upload` 记录 CSV / Scripts / Bulk Upload 批次、hash、preview、Editor check、人工审批、回滚计划和 Change History 证据。
- `/bulk-upload/<id>/status` 更新 preview_ready、approved_for_manual_post、posted_manual、partial_error、rollback_review、blocked 等内部状态并写入 `/logs`。
- `/tasks` 创建 CSV 导出检查任务。
- `/logs` 记录 CSV 导出审计。
- `/risk-audits` 记录高风险能力和政策问题。

CSV 导出前会执行 campaign preflight：campaign 必须 approved/exported，Claim 审核不能处于 open/rewrite_required/blocked，广告审核案例不能处于 open/appeal_submitted/rejected。未通过时不生成 CSV，并写入 `export_blocked` 审计日志。

`bulk_upload_reviews` 只代表内部人工发布门禁，不会自动打开 Google Ads Editor、自动登录 Google Ads、自动点击发布按钮或自动 apply Scripts Bulk Upload。表单文本如果包含自动发布、Cookie、Session Token、浏览器 profile、绕审核、cloaking、补点击、刷展示、代理/指纹/Worker、防关联、封禁换号等语义，会被拦截并改走风险审计与修复流程。

V1 评分维度：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| export type | 8 | Editor CSV 风险最低，Scripts / Bulk Upload 必须 preview |
| campaign preflight | 15 | campaign、Claim review、ad review case 是否允许导出 |
| change scope | 10 | rows、keywords、ads 是否属于小批次 |
| budget delta | 10 | 预算变化是否在安全阈值内 |
| URL changes | 8 | Final URL / tracking 变化必须走链接和目的地 QA |
| default paused | 8 | 新建结构默认 paused，避免大预算直接上线 |
| human review | 8 | 人工审核是正式发布前的硬门禁 |
| preview / Editor check | 23 | preview 和 Editor check 不能有未处理错误 |
| post / reconciliation | 10 | posted 后必须回填 Change History 和失败行 |

recommended_action 的含义：

| 动作 | 含义 |
| --- | --- |
| approve_manual_post | 小批次、预检和 preview 通过，可由授权人员人工发布 |
| run_editor_or_preview_check | 需要先跑 Editor check 或 Bulk Upload preview |
| fix_preflight_before_export | 先修 campaign preflight、Claim review 或 ad review case |
| fix_preview_errors | 先修 preview / Editor 错误行 |
| manual_review_high_risk_changes | 预算、URL、状态或 conversion action 变化需要高风险人审 |
| reconcile_partial_failure | 处理部分失败、错误行和修复批次 |
| hold_for_review | 证据不足或 blockers 未清，不能发布 |

当前 V1 不做：

- 自动登录 Google Ads。
- 自动导入 Google Ads Editor。
- 自动点击后台发布按钮。
- 自动处理登录、2FA、captcha 或安全挑战。
- 无人审批 apply 高风险变更。
- 补点击、刷展示、模拟访问或伪造转化。

## 11. 后续数据模型建议

| 表 | 用途 |
| --- | --- |
| `bulk_change_batches` | 保存 batch、目标账号、CSV hash、row_count、状态 |
| `bulk_change_rows` | 保存每一行对象类型、目标资源、错误和发布结果 |
| `csv_export_versions` | 保存导出版本、字段合同和 diff |
| `editor_review_decisions` | 保存 reviewer、approval、blocked reason |
| `bulk_upload_results` | 保存 preview/apply 结果、失败行、error message |
| `change_history_links` | 保存外部变更窗口和 ChangeEvent 摘要 |

这些表服务于批量变更治理，不服务于后台接管或绕审核发布。

## 12. 信息来源 URL

- ADXKit homepage: https://adxkit.com/
- Google Ads Editor Help: https://support.google.com/google-ads/editor
- Google Ads Editor, Prepare a CSV file: https://support.google.com/google-ads/editor/answer/56368
- Google Ads Editor, Check changes before posting: https://support.google.com/google-ads/editor/answer/56370
- Google Ads Editor, Review recent account changes: https://support.google.com/google-ads/editor/answer/30582
- Google Ads Editor, Share proposed changes: https://support.google.com/google-ads/editor/answer/38664
- Google Ads Editor, Post changes: https://support.google.com/google-ads/editor/answer/30583
- Google Ads Help, Bulk uploads: https://support.google.com/google-ads/answer/10702433
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
- Google Ads Scripts, Bulk upload: https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload
- Google Ads Scripts, Preview mode: https://developers.google.com/google-ads/scripts/docs/preview
- Google Ads API, Partial failures: https://developers.google.com/google-ads/api/docs/best-practices/partial-failures
- Google Ads policy, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads policy, Destination requirements: https://support.google.com/adspolicy/answer/6368661
