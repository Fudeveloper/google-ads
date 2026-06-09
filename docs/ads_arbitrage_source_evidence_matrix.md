# Ads 套利来源证据矩阵

更新时间：2026-06-09

本文把 Ads 套利知识库中的核心判断逐条绑定到公开来源、系统落点和验收方式。它解决一个验收问题：这些结论不是“经验判断”，而是能说明来自哪个官方政策、开发文档、技术参考或目标产品公开页面。

来源类型：

- `primary_policy`：Google Ads、AdSense、Google Publisher Policies、FTC 等官方政策或帮助文档。
- `primary_dev`：Google Ads API、Google Ads Scripts、Google Ads Editor、Cloudflare、MDN、OWASP、W3C 等官方技术文档。
- `public_claim`：ADXKit 公开页面，只能证明“对方公开声称了什么”，不能证明其内部实现。
- `industry_reference`：行业术语、MFA 研究或市场资料，用于补充行业语境。

## 1. 关键结论和来源证据

| 结论 | 主要来源 URL | 来源类型 | 支撑什么判断 | 系统 / 文档落点 |
| --- | --- | --- | --- | --- |
| Google Ads 对只为展示广告、桥页、网关页、cloaking、低价值目的地和广告网络滥用有明确风险描述 | https://support.google.com/adspolicy/answer/6008942 | `primary_policy` | Ads 套利不能只做广告堆叠页或中转页，页面必须有独立用户价值 | [Ads 套利行业知识库](ads_arbitrage_industry.md)、[落地页质量、广告密度与 MFA 风险手册](landing_page_quality_mfa.md) |
| 隐藏真实目的地、向 Google 和用户展示不同内容、规避政策执行或多账号规避属于高风险 | https://support.google.com/adspolicy/answer/15938075 | `primary_policy` | 支撑 cloaking、审核页/用户页不一致、封禁后换号、隐藏链路和规避系统边界 | [高风险能力逐点调研与安全复刻蓝图](high_risk_capability_safe_reproduction_blueprint.md)、[Cloaking 专题](high_risk/cloaking_review_user_page_mismatch.md) |
| Final URL、页面可达性、目的地体验和广告承诺一致性是 Google Ads 审核核心 | https://support.google.com/adspolicy/answer/6368661 | `primary_policy` | 支撑换链接必须是同主题、同承诺、已审核候选 URL，而不是隐藏目的地 | [链接计划与换链接合规手册](link_rotation_compliance.md)、`/links` |
| AdSense 无效流量包括可能人为抬高广告主成本或发布商收入的点击和展示 | https://support.google.com/adsense/answer/16737 | `primary_policy` | 支撑补点击、刷展示、模拟自然流量不能作为系统功能 | [补点击/刷展示专题](high_risk/invalid_traffic_click_impression_simulation.md)、[无效流量 SOP](invalid_traffic_detection_sop.md) |
| AdSense Program policies 禁止自动点击工具、自动浏览、付费点击、鼓励点击等行为 | https://support.google.com/adsense/answer/48182 | `primary_policy` | 支撑任务中心禁止 click、impression、visit、traffic simulation 语义 | `/tasks`、`adsworkbench/services/tasks.py` |
| 发布商购买流量时仍要对流量质量负责 | https://support.google.com/adsense/answer/1348722 | `primary_policy` | 支撑“供应商发的流量”不能成为无效流量免责理由 | [流量供应商尽调手册](traffic_channel_vendor_due_diligence.md)、[Source 质量治理手册](source_publisher_placement_quality_governance.md) |
| Google 会使用自动系统和人工审核来过滤无效点击、展示和相关活动 | https://support.google.com/adsense/answer/1348752 | `primary_policy` | 支撑无效流量治理应做来源隔离、证据保留和复盘，而不是补量 | `/optimization`、[异常监控手册](anomaly_monitoring_alerting_stoploss_incident_triage.md) |
| Cookie 是 HTTP 状态机制，常用于会话管理 | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies | `primary_dev` | 支撑登录 Cookie / Session Token 是敏感会话材料，不应作为后台自动化接口 | [Ads Cookie 专题](high_risk/ads_cookie_backend_operation.md) |
| Session ID / Token 应按敏感凭据管理，需要安全生命周期和存储保护 | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | `primary_dev` | 支撑不保存、导入、复用、注入 Cookie 或 Session Token | `.env.example`、`/accounts` 语义拦截 |
| 2FA 和 MFA 是降低账号接管风险的安全控制 | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | `primary_dev` | 支撑系统不做验证码处理、OTP 接管或安全挑战绕过 | [自动绕过登录/2FA 专题](high_risk/automated_login_2fa_challenge_bypass.md)、`/tasks` |
| Google Ads 账号安全文档强调 2-Step Verification、访问审计和 cookie theft 风险 | https://support.google.com/google-ads/answer/2375456 | `primary_policy` | 支撑多人协作应走访问级别和授权，而不是共享登录态 | `/accounts`、[账号/MCC 治理手册](account_mcc_billing_verification_governance.md) |
| Google Ads 会在敏感或异常场景要求确认身份 | https://support.google.com/google-ads/answer/12865189 | `primary_policy` | 支撑安全挑战不能被任务系统自动绕过，应该进入人工确认和安全复盘 | `/risk-audits`、[任务编排手册](task_orchestration_approval_audit_runbook.md) |
| Google Ads 支持不同访问级别和账号权限 | https://support.google.com/google-ads/answer/9978556 | `primary_policy` | 支撑外包、投手、运营协作应使用权限模型而不是交付 Cookie / 2FA 设备 | [账号治理手册](account_mcc_billing_verification_governance.md) |
| Google Ads API 通过 OAuth 授权访问，不需要处理用户后台 Cookie | https://developers.google.com/google-ads/api/docs/oauth/overview | `primary_dev` | 支撑官方 API / OAuth 是长期连接器方向，虽然本 V1 不做 API 集成 | [系统设计文档](system_design.md)、[Google Ads Scripts 安全自动化手册](google_ads_scripts_safe_automation.md) |
| Google Ads Scripts 需要授权，适合有限批量处理和报表/草稿 payload | https://developers.google.com/google-ads/scripts/docs/authorization | `primary_dev` | 支撑 Scripts JSON 导出是可审计替代方案，不是 Cookie 后台接管 | `/campaigns/<id>/export.script.json` |
| Google Ads Editor 支持 CSV 准备、检查、发布和共享 proposed changes | https://support.google.com/google-ads/editor/answer/56368 | `primary_policy` | 支撑 CSV / Editor 作为人工审核型批量变更通道 | `/campaigns/<id>/export.csv`、[Editor CSV 治理手册](google_ads_editor_csv_bulk_upload_governance.md) |
| Change history 可用于回看账号变更 | https://support.google.com/google-ads/answer/9721634 | `primary_policy` | 支撑系统内 AuditLog 要和外部 Change History / Scripts Log 对齐 | `/logs`、[任务编排手册](task_orchestration_approval_audit_runbook.md) |
| Quality Score 是诊断广告相关性、预期 CTR 和落地页体验的工具 | https://support.google.com/google-ads/answer/6167118 | `primary_policy` | 支撑套利优化不能只追 CTR，要看广告承诺、关键词和页面匹配 | [Google Ads 竞价、Quality Score 与套利出价手册](google_ads_auction_bidding_quality_score.md) |
| Google Ads 数据存在 freshness、conversion lag 和 discrepancies，需要按窗口复盘 | https://support.google.com/google-ads/answer/2544985 | `primary_policy` | 支撑指标导入和优化不应把延迟误判为缺点击或缺转化 | `/metrics/import`、[决策窗口与收入延迟手册](decision_window_revenue_lag_governance.md) |
| 浏览器指纹可由多种环境信号组合而成 | https://coveryourtracks.eff.org/learn | `industry_reference` | 支撑指纹不是单一参数，伪造或频繁切换会进入规避检测语境 | [代理/指纹/Worker 专题](high_risk/proxy_fingerprint_worker_association_evasion.md) |
| W3C TAG 对未经授权追踪、指纹和跨站跟踪有治理风险说明 | https://www.w3.org/2001/tag/doc/unsanctioned-tracking/ | `primary_dev` | 支撑指纹和非授权追踪不是普通运营配置，应进入风险审计 | `/risk-audits` |
| Cloudflare Workers 是边缘函数平台，可用于缓存、路由、安全和性能 | https://developers.cloudflare.com/workers/ | `primary_dev` | 支撑 Worker 技术本身中性，但不能用于隐藏真实目的地或审核分流 | [代理/指纹/Worker 专题](high_risk/proxy_fingerprint_worker_association_evasion.md)、[Cloaking 专题](high_risk/cloaking_review_user_page_mismatch.md) |
| Google Ads 账号暂停应按原因修复和申诉 | https://support.google.com/google-ads/answer/2375414 | `primary_policy` | 支撑封禁后应做账号健康复盘和申诉证据包，而不是换号继续跑 | [封禁规避专题](high_risk/ban_evasion_account_switching.md)、`/risk-audits` |
| ADXKit 首页公开宣称 Google Ads 管理、Scripts 同步、AI 创意、补点击、换链接、代理/防关联等能力 | https://adxkit.com/ | `public_claim` | 只用于证明目标产品公开叙事和拆解对象，不证明内部实现 | [ADXKit 功能与架构拆解](adxkit_breakdown.md) |

## 2. 从来源到系统边界的推导

### 2.1 为什么系统可以做投放准备，但不接管后台登录

MDN 和 OWASP 说明 Cookie / Session 是状态和会话管理机制，Google Ads 账号安全文档强调访问审计、2-Step Verification 和 cookie theft 风险。结合 Google Ads API OAuth、Scripts Authorization 和 Google Ads Editor 的官方批量管理资料，可以推导出：

- 可做：Offer 录入、机会测算、创意生成、投放草稿、CSV / Scripts JSON 导出、审计日志。
- 不做：保存 Cookie、注入 Cookie、复用 Session Token、托管浏览器 Profile、自动确认登录挑战。
- 系统证据：`.env.example` 没有 Cookie / Proxy / Fingerprint 配置，`/accounts` 拦截 Cookie / Session 语义，Scripts payload 包含 `no_cookie_automation`。

### 2.2 为什么系统可以做链接计划，但不做 cloaking

Google Ads 的 Destination requirements 要求目的地体验和广告承诺一致；Circumventing systems 明确把隐藏真实目的地、向 Google 和用户展示不同内容、规避审核和限制列为高风险。由此可以推导出：

- 可做：断链修复、UTM 更新、同主题已审核候选 URL、人工确认轮换、URL 版本日志。
- 不做：审核页/用户页双版本、Bot 分流、Google IP / User-Agent / Cookie / 指纹分流、隐藏真实 Final URL。
- 系统证据：`/links` 默认人工确认，链接计划会拦截 cloaking、worker forward、proxy pool、hidden destination 等语义。

### 2.3 为什么系统可以做指标导入和异常诊断，但不补点击

AdSense Invalid traffic 和 Program policies 说明，人为抬高广告主成本或发布商收入的点击/展示、自动点击、自动浏览、付费点击和鼓励点击都是高风险。数据差异、转化延迟和收入延迟应通过报表窗口、追踪 QA、来源隔离和结算复盘处理。

- 可做：真实指标导入、RPV / EPC / ROI 计算、stop-loss、来源隔离、追踪链 QA、供应商争议证据。
- 不做：点击任务、展示任务、自动浏览、Referer 伪造、停留时长模拟、行为路径模拟。
- 系统证据：`/metrics/import` 只导入真实 CSV，`/optimization` 只生成建议，`/tasks` 禁止 click / impression / traffic simulation 语义。

### 2.4 为什么系统可以做账号健康审计，但不做封禁后换号

Google Ads 的 Circumventing systems 和账号暂停修复文档共同说明：账号受限后应理解原因、修复问题、提交申诉或停止问题业务。把封禁当作“换号继续跑”的容量问题，会把原本的质量或政策问题升级为规避系统问题。

- 可做：账号状态记录、限制原因、修复动作、申诉证据、Related Account 风险复盘。
- 不做：账号池、批量开户、付款资料规避、同 Offer 换壳继续跑。
- 系统证据：`/accounts` 保存状态和备注，不保存账号池；账号配置会拦截 account pool、ban evasion、bulk account、换号继续等语义。

## 3. 证据强度分级

| 证据强度 | 例子 | 用法 |
| --- | --- | --- |
| A：官方政策直接命中 | Google Ads Circumventing systems、AdSense Invalid traffic、Destination requirements | 可作为系统不交付边界和上线拦截依据 |
| B：官方技术文档支撑实现方向 | Google Ads API OAuth、Scripts Authorization、Google Ads Editor CSV、MDN Cookies、OWASP Session | 可作为安全替代方案和系统架构依据 |
| C：行业参考解释背景 | EFF 指纹说明、IAB / Jounce MFA 术语 | 用于解释行业语境，不单独作为政策判定 |
| D：目标产品公开声明 | ADXKit homepage | 只能用于拆解“对方公开宣称的能力”，不能证明其真实内部架构 |

验收时应优先引用 A 和 B；C 用来补充原理，D 只用于 ADXKit 对标。

## 4. 验收使用方法

第三方验收时，可以按这个顺序检查：

1. 从 [文档入口和验收导航](docs_index.md) 进入端到端路径。
2. 对照本矩阵确认每个核心判断都有来源 URL。
3. 进入 [ADXKit 功能与架构拆解](adxkit_breakdown.md) 看公开能力和本项目入口。
4. 进入 [高风险能力逐点调研与安全复刻蓝图](high_risk_capability_safe_reproduction_blueprint.md) 看 6 个高风险点的完成形态。
5. 在系统中访问 `/sources`、`/risk-audits`、`/links`、`/tasks`、`/accounts`、`/campaigns`、`/metrics/import`、`/optimization`。
6. 运行：

```powershell
.\.venv\Scripts\python scripts\verify_research_docs.py
.\.venv\Scripts\python scripts\smoke_test.py
.\.venv\Scripts\python scripts\acceptance_audit.py
```

## 5. 信息来源 URL

- ADXKit homepage: https://adxkit.com/
- Google Ads, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads, Secure your Google Ads account: https://support.google.com/google-ads/answer/2375456
- Google Ads, Confirm it is you: https://support.google.com/google-ads/answer/12865189
- Google Ads, About access levels in your Google Ads account: https://support.google.com/google-ads/answer/9978556
- Google Ads, Change history: https://support.google.com/google-ads/answer/9721634
- Google Ads, About Quality Score: https://support.google.com/google-ads/answer/6167118
- Google Ads, About data freshness: https://support.google.com/google-ads/answer/2544985
- Google Ads, Fix a suspended Google Ads account: https://support.google.com/google-ads/answer/2375414
- Google Ads API, OAuth overview: https://developers.google.com/google-ads/api/docs/oauth/overview
- Google Ads Scripts, Authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- Google Ads Editor, Prepare a CSV file: https://support.google.com/google-ads/editor/answer/56368
- AdSense, Invalid traffic: https://support.google.com/adsense/answer/16737
- AdSense, Program policies: https://support.google.com/adsense/answer/48182
- AdSense, Online advertising to get new users: https://support.google.com/adsense/answer/1348722
- AdSense, How Google prevents invalid traffic: https://support.google.com/adsense/answer/1348752
- MDN, Using HTTP cookies: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP Multifactor Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
- EFF, Cover Your Tracks: https://coveryourtracks.eff.org/learn
- W3C TAG, Unsanctioned Web Tracking: https://www.w3.org/2001/tag/doc/unsanctioned-tracking/
- Cloudflare Workers documentation: https://developers.cloudflare.com/workers/

