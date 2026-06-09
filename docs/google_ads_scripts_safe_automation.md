# Google Ads Scripts 安全自动化手册

更新时间：2026-06-08

本文说明 Ads 套利系统中如何用 Google Ads Scripts 承接“批量投放草稿、检查 URL、导入结构化 payload、生成预览和审计记录”的诉求。它解释 Scripts 与 Cookie 后台操作、Google Ads API、Google Ads Editor CSV 的边界，并给出安全执行 SOP。

本文不提供 Cookie 登录后台、绕过 2FA、安全挑战、审核系统、自动规避封禁、补点击、刷展示、cloaking 或隐藏真实目的地的实现。

## 1. Scripts 的定位

Google Ads Scripts 是在 Google Ads 账号内由授权用户创建、授权和运行的脚本环境。它适合做：

- 报表读取。
- 结构化检查。
- URL 和参数 QA。
- 批量上传预览。
- 低风险建议生成。
- 人审后的有限批量变更。

它不适合做：

- 绕过账号登录。
- 复用 Cookie。
- 处理验证码、2FA 或安全挑战。
- 自动绕过审核。
- 隐藏最终目的地。
- 生成虚假点击、展示、session 或 conversion。

一句话：Scripts 是官方授权的账号内自动化，不是浏览器登录态接管。

## 2. Scripts vs Cookie 后台操作

| 维度 | Google Ads Scripts | Cookie 后台操作 |
| --- | --- | --- |
| 授权 | 由账号内用户授权脚本运行 | 复用浏览器会话 |
| 权限边界 | 受 Google Ads 用户权限、脚本能力和账号上下文限制 | 通常等同于登录用户可见权限 |
| 审计 | 脚本代码、运行日志、输入 payload 可归档 | 很难证明谁授权和执行了什么 |
| 稳定性 | 基于 Scripts 服务和 AdsApp/Bulk upload 能力 | 依赖 UI、会话、风控和前端接口变化 |
| 安全事件 | 授权失败按账号权限处理 | 容易触发会话迁移、cookie theft、安全挑战 |
| 适合用途 | 报表、预览、批量结构化变更 | 不适合作为系统集成边界 |

本系统的设计是：在 Flask 工作台里生成 payload，在 Google Ads Scripts 里由授权用户预览和执行。系统不保存 Google 登录凭据。

## 3. 安全执行等级

| 等级 | 示例 | 默认策略 |
| --- | --- | --- |
| L0 只读 | 拉报表、列 campaign、检查 URL | 可定时，但要记录日志 |
| L1 预览 | 读取 JSON payload、生成 bulk upload preview | 默认允许，需人审 |
| L2 低风险写 | 添加否定词、暂停明显失败的 ad group | 需明确阈值和审批 |
| L3 高风险写 | 改预算、改 Final URL、启停 campaign、创建广告 | 双人审核或手工确认 |
| 禁止 | Cookie 接管、处理 2FA、cloaking、补点击、规避封禁 | 不实现 |

建议第一版只做 L1：preview 和日志。L2/L3 必须先建立审批、回滚和审计字段。

## 4. Payload 合同

本系统 `/campaigns/<id>/export.script.json` 导出的 payload 必须包含：

```json
{
  "mode": "manual_review_required",
  "campaign": {
    "name": "...",
    "channel": "Google Search",
    "daily_budget": 30,
    "bid_strategy": "Maximize Clicks",
    "final_url": "https://example.com"
  },
  "offer": {
    "id": 1,
    "name": "...",
    "vertical": "...",
    "country": "US",
    "language": "en"
  },
  "creative": {
    "headlines": [],
    "descriptions": [],
    "keywords": []
  },
  "safety": {
    "no_cookie_automation": true,
    "requires_human_approval": true
  }
}
```

安全校验：

- `mode` 必须是 `manual_review_required`。
- `safety.no_cookie_automation` 必须是 `true`。
- `safety.requires_human_approval` 必须是 `true`。
- Final URL 必须是 HTTPS。
- headline / description 数量要符合 RSA 约束。
- keywords 必须是非空、可解释、非敏感违规词。
- budget 不得超过内部测试预算或硬止损。

## 5. Bulk Upload Preview 流程

推荐流程：

1. 在系统里创建 Offer、创意组和 Campaign 草稿。
2. 导出 Scripts JSON payload。
3. 在 Google Ads 后台打开 Scripts，由授权用户粘贴 payload。
4. 运行 `scripts/google_ads_script_payload_preview.js`。
5. 脚本先验证 `no_cookie_automation` 和人审字段。
6. 默认只输出 bulk upload preview 或日志，不直接 apply。
7. 人工检查 campaign、ad group、keyword、RSA、Final URL、budget。
8. 通过后才手动执行或把 `PREVIEW_ONLY` 改为 `false`，并记录审批。
9. 回到本系统导入指标，复盘 ROI、RPV、reject、deduction 和 policy 状态。

注意：不同 Google Ads 账号、语言、脚本运行环境和 bulk upload 模板可能要求字段名调整。执行前必须用 Google 官方文档和 Ads preview 检查。

## 6. 审计日志要求

每次 Scripts 运行应记录：

- payload ID 或 campaign draft ID。
- 执行账号和 Customer ID。
- script name 和版本。
- 运行时间。
- preview / apply 模式。
- 创建或变更对象数量。
- 错误和 warning。
- 审批人和审批时间。
- 关联来源 URL。

如果未来接入 API 或自动回传，仍然必须保留同样审计字段。

## 7. 常见错误

| 错误 | 后果 | 处理 |
| --- | --- | --- |
| 直接 apply 未审核 payload | 大量错误广告上线 | 默认 preview，只允许人审后执行 |
| payload 缺少 safety 字段 | 无法证明不依赖 Cookie | 拒绝运行 |
| Final URL 不是 HTTPS | 审核和用户体验风险 | 拒绝运行并回到链接 QA |
| 文案夸张或页面无证据 | 拒登、低质量 lead、扣量 | 回到创意和落地页审计 |
| budget 过大 | 冷启动烧钱 | 对照预算节奏手册 |
| broad keywords 过宽 | 低意图流量涌入 | 先 phrase/exact 和否定词 |
| template 用于隐藏目的地 | Circumventing systems 风险 | 停止执行并做风险审计 |

## 8. 系统落地

当前系统已经支持：

- `/campaigns/<id>/export.script.json` 导出 payload。
- payload 里带 `no_cookie_automation` 和 `requires_human_approval`。
- `/tasks` 创建 Scripts JSON 导出检查任务。
- `/logs` 记录导出动作。
- `/sources` 记录 Scripts 授权、Bulk Upload、limits 等来源。
- `scripts/google_ads_script_payload_preview.js` 作为安全预览模板。

Scripts JSON 导出前会执行 campaign preflight：campaign 必须 approved/exported，Claim 审核不能处于 open/rewrite_required/blocked，广告审核案例不能处于 open/appeal_submitted/rejected。未通过时不生成 Scripts payload，并写入 `export_blocked` 审计日志；任务中心的 Scripts JSON 导出检查也使用同一规则。

当前系统不支持：

- 自动登录 Google Ads。
- 存储 Google 账号 Cookie、密码、验证码、恢复码。
- 自动处理安全挑战。
- 直接远程执行 Google Ads Scripts。
- 无人审自动 apply 高风险变更。

## 9. 未来扩展

安全扩展方向：

- `script_payload_versions`：保存 payload hash、version、reviewer、status。
- `script_run_logs`：记录 preview/apply 结果。
- `script_guardrails`：budget cap、allowed domains、blocked terms。
- `url_test_runs`：执行前检查 Final URL 和 tracking template。
- `negative_keyword_suggestions`：生成建议，不自动发布。

禁止扩展方向：

- Cookie 注入或浏览器 Profile 托管。
- 自动处理登录挑战。
- 审核页/用户页分流。
- 自动替换 Final URL 绕审核。
- 用补点击或虚假 conversion 训练出价。

## 10. 信息来源 URL

- Google Ads Scripts, Start guide: https://developers.google.com/google-ads/scripts/docs/start
- Google Ads Scripts, Authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- Google Ads Scripts, Bulk Upload: https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload
- Google Ads Scripts, Limits: https://developers.google.com/google-ads/scripts/docs/limits
- Google Ads Scripts, AdsApp reference: https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp
- Google Ads Scripts, BulkUpload reference: https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp_bulkupload
- Google Ads Scripts, Campaigns: https://developers.google.com/google-ads/scripts/docs/campaigns/campaigns
- Google Ads Scripts, Responsive Search Ads: https://developers.google.com/google-ads/scripts/docs/features/responsive-search-ads
- Google Ads Help, About tracking in Google Ads: https://support.google.com/google-ads/answer/6076199
- Google Ads Help, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads policies, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
