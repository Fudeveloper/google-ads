# 高风险能力逐点完成审计

更新时间：2026-06-09

本文用于验收 ADXKit 类产品中 6 个高风险能力的“复刻完成形态”。这些点不是被跳过，而是被拆成可交付和不可交付两层：

- 可交付：行业诉求、技术原理、平台规则、风险识别、审计字段、SOP、来源 URL、系统安全替代能力。
- 不交付：Cookie 会话接管、绕过登录/2FA/安全挑战、补点击/刷展示/模拟自然流量、代理/指纹/Worker 规避关联、cloaking 分流、为规避封禁创建或切换账号。

## 1. 完成口径

高风险能力的完成不是“把危险动作做出来”，而是把业务团队真正需要解决的问题沉淀到系统里：

1. 为什么行业会提出这个需求。
2. 这个需求背后的广告系统、认证系统、流量质量或账号治理原理是什么。
3. 平台为什么会把某些实现方式视为无效流量、规避系统、账号安全或审核风险。
4. 正常业务场景与规避场景的边界在哪里。
5. 系统已经交付哪些可审计替代能力。
6. 依据哪些来源 URL。

## 2. 逐点完成审计

| 高风险点 | 行业真实诉求 | 已完成的知识复刻 | 已完成的系统形态 | 不交付边界 |
| --- | --- | --- | --- | --- |
| Ads Cookie 登录和后台操作 | 减少登录、批量改后台、同步投放数据 | Cookie/会话原理、Google Ads 后台对象模型、操作生命周期、OAuth/Scripts/CSV 区别、审计字段和 SOP | `/accounts` 记录账号同步方式，CSV / Scripts JSON 导出，`/logs` 留痕，`/risk-audits` 审计 | 不获取、导入、复用、注入 Cookie；不做后台 UI 接管 |
| 自动绕过登录、2FA、安全挑战 | 无人值守任务、多人协作、减少人工登录 | Step-up challenge、认证链路状态机、人机分工边界、危险任务语义、访问级别、任务授权和安全事件 SOP | `/tasks` 手动任务中心，任务白名单，执行日志，安全文档 | 不处理验证码，不接管 2FA，不绕过确认身份或安全挑战 |
| 补点击、刷展示、模拟自然流量 | 让报表看起来自然、弥补追踪断点、提高短期收入 | 广告计费信号、无效流量定义、信号污染、流量账本状态机、异常诊断、供应商证据、追踪断点和扣量机制 | `/metrics/import` 导入真实指标，`/optimization` 异常建议，Click -> Session -> Revenue 对账 SOP，来源隔离和风险审计 | 不生成点击、展示、访问、Referer、停留时长或行为路径 |
| 代理、指纹、Worker 转发规避关联检测 | 多账号隔离、隐藏来源、拆分请求链路 | 代理/指纹/Worker 中性原理、关联资产图谱、合法隔离证据、供应商红旗、Worker 安全边界和 Association Risk Score | `/risk-audits` 记录关联风险，账号配置记录真实业务主体和同步方式 | 不做代理池、指纹 profile、反检测浏览器配置或 Worker 规避脚本 |
| Cloaking 或审核页/用户页不一致 | 绕过审核、换最终页、按人群展示不同页面 | 差异化页面边界、Review/User 一致性矩阵、URL 生命周期、Final URL / tracking chain QA、Destination Consistency Score 和 SOP | `/links` 合规链接计划，候选 URL、人工确认、版本日志；追踪链 QA 文档 | 不做 Bot 分流、审核页/用户页双版本、隐藏目的地或违规换链 |
| 为规避封禁创建或切换账号 | 受限后继续投放、分散风险、保留现金流 | 账号图谱、正常多账号管理 vs 规避封禁、账号暂停状态机、Related Account 风险、申诉证据包、Account Recovery Score 和 SOP | `/accounts` 状态备注，`/risk-audits` 账号健康审计，账号健康 SOP 和证据包 | 不做批量开户、账号池、付款资料规避、封禁后自动换号 |

## 3. 已完成专题

| 专题 | 完成内容 |
| --- | --- |
| [Ads Cookie 登录和后台操作](high_risk/ads_cookie_backend_operation.md) | 后台操作链路、Google Ads 后台对象模型、后台操作生命周期、Cookie 自动化和官方授权区别、套利团队真实诉求、审计字段、SOP 和替代连接器 |
| [自动绕过登录、2FA、安全挑战](high_risk/automated_login_2fa_challenge_bypass.md) | Step-up challenge、认证链路状态机、账号协作边界、人机分工、任务危险语义、审计字段和安全事件 SOP |
| [补点击、刷展示、模拟自然流量](high_risk/invalid_traffic_click_impression_simulation.md) | 信号污染路径、流量账本状态机、追踪断点、异常诊断、供应商证据、自然流量可解释性、审计字段和无效流量治理 SOP |
| [代理、指纹、Worker 转发规避关联检测](high_risk/proxy_fingerprint_worker_association_evasion.md) | 关联图谱原理、关联资产图谱、供应商红旗、Worker 安全边界、合法隔离证据、审计字段和 SOP |
| [Cloaking 或审核页/用户页不一致](high_risk/cloaking_review_user_page_mismatch.md) | 差异化页面边界、Review/User 一致性矩阵、URL 生命周期、链路一致性、Destination Consistency Score、审计字段和 SOP |
| [为规避封禁创建或切换账号](high_risk/ban_evasion_account_switching.md) | 账号不是孤立资产、正常多账号 vs 规避封禁、账号暂停状态机、Related Account 风险、申诉证据包、审计字段和恢复 SOP |

## 4. 系统验收路径

1. 进入 `/knowledge/risk_index`，查看 6 个专题的完成矩阵。
2. 进入 `/knowledge/redlines`，查看总研究文档和汇总表。
3. 进入 `/knowledge/risk_matrix`，查看风险等级、审计字段和来源索引。
4. 进入 `/sources`，用对应 topic 查询来源 URL。
5. 进入 `/risk-audits`，按高风险能力创建审计记录，填写发现、处理方案和来源 URL。
6. 在 `/accounts`、`/tasks`、`/links`、`/metrics/import`、`/optimization` 页面验证安全替代能力。

## 5. 当前完成证据

| Capability | 专题文档 | 来源库记录 | 系统替代形态 | 验收证据 |
| --- | --- | ---: | --- | --- |
| `ads_cookie_backend_operation` | [Ads Cookie 登录和后台操作](high_risk/ads_cookie_backend_operation.md) | 8 | `/accounts`、CSV / Scripts JSON、`/logs`、`/risk-audits` | 后台对象模型、操作生命周期、审计字段、SOP、No Cookie Automation |
| `automated_login_2fa_challenge_bypass` | [自动绕过登录、2FA、安全挑战](high_risk/automated_login_2fa_challenge_bypass.md) | 9 | `/tasks` 安全白名单、人工执行、OAuth / Scripts / 权限模型 | 认证状态机、危险任务语义、审计字段、安全事件 SOP |
| `invalid_traffic_click_impression_simulation` | [补点击、刷展示、模拟自然流量](high_risk/invalid_traffic_click_impression_simulation.md) | 15 | `/metrics/import`、`/optimization`、来源隔离、对账 SOP | 流量账本、异常诊断、供应商证据、无效流量 SOP |
| `proxy_fingerprint_worker_association_evasion` | [代理、指纹、Worker 转发规避关联检测](high_risk/proxy_fingerprint_worker_association_evasion.md) | 8 | `/risk-audits`、账号配置、真实业务隔离证据 | 关联资产图谱、供应商红旗、Association Risk Score、SOP |
| `cloaking_review_user_page_mismatch` | [Cloaking 或审核页/用户页不一致](high_risk/cloaking_review_user_page_mismatch.md) | 8 | `/links`、候选 URL、人工确认、URL 版本日志 | Review/User 一致性矩阵、URL 生命周期、Destination Consistency Score、SOP |
| `ban_evasion_account_switching` | [为规避封禁创建或切换账号](high_risk/ban_evasion_account_switching.md) | 10 | `/accounts`、`/risk-audits`、账号健康证据包 | 账号暂停状态机、Related Account 风险、申诉证据包、Account Recovery Score |

当前数据库 `ResearchSource` 总数为 526，其中 6 个高风险 capability 合计 58 条来源记录。来源记录只用于审计和知识沉淀，不触发后台登录、点击、代理、分流或账号切换。

## 6. 验证命令

```powershell
.\.venv\Scripts\python -m compileall adsworkbench app.py scripts
.\.venv\Scripts\python scripts\verify_research_docs.py
.\.venv\Scripts\python scripts\smoke_test.py
.\.venv\Scripts\python -m flask --app app seed
```

验收时还应查询 6 个 capability 的 `ResearchSource` 数量，确认来源库覆盖没有退化。

## 7. 信息来源 URL

- ADXKit homepage: https://adxkit.com/
- Google Ads, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads, Secure your Google Ads account: https://support.google.com/google-ads/answer/2375456
- Google Ads, Confirm it is you: https://support.google.com/google-ads/answer/12865189
- Google Ads, About access levels in your Google Ads account: https://support.google.com/google-ads/answer/9978556
- Google Ads API, OAuth overview: https://developers.google.com/google-ads/api/docs/oauth/overview
- Google Ads Scripts, Authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- MDN, Using HTTP cookies: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- AdSense, Invalid traffic: https://support.google.com/adsense/answer/16737
- AdSense, Program policies: https://support.google.com/adsense/answer/48182
- AdSense, How Google prevents invalid traffic: https://support.google.com/adsense/answer/1348752
- EFF, Cover Your Tracks: https://coveryourtracks.eff.org/learn
- W3C TAG, Unsanctioned Web Tracking: https://www.w3.org/2001/tag/doc/unsanctioned-tracking/
- Cloudflare Workers documentation: https://developers.cloudflare.com/workers/
- Google Search Central, Spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Google Ads, Fix a suspended Google Ads account: https://support.google.com/google-ads/answer/2375414
