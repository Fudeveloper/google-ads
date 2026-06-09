# Ads Cookie 登录和后台操作研究

更新时间：2026-06-09

## 1. 范围

本文研究“用 Google Ads 登录 Cookie 操作后台”的技术本质、行业诉求、风险、平台安全逻辑和合规替代方案。本文不提供 Cookie 获取、导入、复用、注入、后台自动操作或会话接管的步骤和代码。

## 2. 原理解释

Cookie 是 HTTP 的状态机制。浏览器访问网站时，服务端可以通过 `Set-Cookie` 写入 Cookie；浏览器后续请求会按域名、路径、安全属性和 SameSite 规则携带 Cookie。登录系统常用 Cookie 或与 Cookie 绑定的会话凭据识别用户。

Google Ads 后台是登录态应用。用户登录后，浏览器持有的会话凭据代表该用户的访问身份。把这些凭据复制到脚本、服务端程序、自动化浏览器或其他设备，本质上是把浏览器登录态当作 API token 使用，但它没有官方 OAuth scope、API quota、可撤销授权、服务账号边界和清晰审计模型。

Cookie 常见安全属性：

- `Secure`：只通过 HTTPS 发送。
- `HttpOnly`：阻止 JavaScript 直接读取 Cookie，降低 XSS 盗取风险。
- `SameSite`：限制跨站请求携带 Cookie，降低 CSRF 风险。
- `Expires` / `Max-Age`：控制 Cookie 生命周期。

这些属性说明 Cookie 是敏感会话凭据，不适合作为团队自动化集成凭据。

### 2.1 后台操作链路的本质

Google Ads 后台操作通常不是单纯“带一个 Cookie 发请求”。一个真实后台会话会同时涉及：

- Google Account 登录态。
- Ads 前端页面加载和账号选择。
- 账号权限、MCC 关系和可访问 customer。
- 表单、异步接口、CSRF/XSRF 类保护和一次性页面状态。
- 敏感动作的二次确认，例如预算、用户邀请、URL 域名或批量变更。
- 操作审计、异常检测和安全挑战。

Cookie 接管类工具的核心问题，是把这一整套“用户在浏览器里完成的受保护交互”压缩成服务端或自动化浏览器的隐式执行。它缺少官方 API 的 scope、developer token、OAuth consent、quota、变更语义和可撤销授权，所以团队很难回答三个基本审计问题：谁授权、授权范围是什么、执行证据在哪里。

### 2.2 Cookie 自动化和官方授权的区别

| 维度 | Cookie 后台操作 | OAuth / Scripts / CSV |
| --- | --- | --- |
| 身份边界 | 复用用户会话 | 明确授权用户或人工导入 |
| 权限边界 | 依赖登录用户全部可用权限 | 可按 API scope、账号权限或人工导入控制 |
| 撤销方式 | 改密码、踢设备、吊销会话，影响面不清 | 撤销授权、移除用户、删除脚本或停止导入 |
| 审计 | 容易混同为用户浏览器行为 | 可记录导出、payload、审批人和执行人 |
| 稳定性 | UI、风控、会话状态变化即失效 | 接口/CSV/脚本语义更稳定 |

### 2.3 套利团队真正要解决的问题

Cookie 需求背后通常不是“必须拿 Cookie”，而是这些运营痛点：

- Campaign、ad group、关键词、广告素材、URL 要批量生成。
- 多账号状态、预算、拒登、转化和收入要汇总。
- 人工后台操作容易漏改、错改、没有版本记录。
- Google Ads API 前期接入成本高。
- 某些动作需要先人审再执行。

因此系统设计应把 Cookie 诉求拆成“草稿生成、变更对账、导出执行、审计留痕、指标导入”，而不是把登录态当集成接口。

### 2.4 Google Ads 后台对象模型

Ads 后台操作看起来是“点页面”，但业务对象不是页面按钮，而是一组可被审计的广告资产：

| 对象 | 常见动作 | 高风险原因 | 安全替代 |
| --- | --- | --- | --- |
| Manager / MCC | 选择 customer、切换子账号 | 账号边界、权限继承、付款和责任混淆 | `/accounts` 记录 customer、同步方式和负责人 |
| Campaign | 创建、暂停、预算、出价策略 | 直接影响花费和学习状态 | 草稿、CSV、Scripts payload、人工审批 |
| Ad group / keyword | 批量新增、否定、匹配类型 | 影响流量意图和查询面 | 命名维度、Search terms 复盘、批量导出 |
| Creative asset | RSA、sitelink、callout、image | 政策审核、claim、落地页一致性 | Claim review、素材版本、人工审核 |
| Final URL / tracking template | 换链接、参数、追踪模板 | cloaking、跳转链、归因丢失 | 链接计划、redirect QA、版本日志 |
| Conversion action | primary / secondary、价值、导入 | 出价学习会被错误信号污染 | conversion signal QA、offline import 诊断 |
| User / access | 邀请、移除、权限级别 | 账号接管和越权风险 | Google Ads access levels、访问审计 |

把后台 UI 还原成对象模型后，就能看清：团队真正需要的是变更建模、审批、导出、执行证据和结果对账，而不是保存一个可无限复用的浏览器会话。

### 2.5 后台操作生命周期

安全完成形态应把一次后台变更拆成可追踪生命周期：

```text
需求提出
  -> 草稿生成
  -> policy / claim / URL / budget / conversion signal 检查
  -> 人工审批
  -> CSV / Scripts JSON / API payload 导出
  -> 授权人员在官方工具中执行
  -> Change history / Scripts log / 导入结果回填
  -> metrics import
  -> ROI / policy / incident 复盘
```

Cookie 后台接管的问题，是把“审批、授权、执行、证据、复盘”压缩成一个难以解释的远程会话。系统不应让“能点后台”替代“能证明为什么、谁批准、改了什么、结果如何”。

### 2.6 为什么 Cookie 不是 API

Cookie 登录态没有以下产品化集成能力：

- 没有 OAuth consent screen 明确授权用途。
- 没有可声明的 API scope 或 developer token 责任链。
- 没有稳定的资源语义、错误码、版本和变更日志合同。
- 没有可靠配额和重试边界。
- 没有天然的 payload 版本、dry run、preview 和 rollback 结构。
- 没有独立于自然人浏览器状态的权限撤销模型。

因此“Cookie 自动化更方便”只是在短期绕过接入成本；从套利团队的长期运营看，它会把账号安全、变更质量和责任归因问题全部推迟到事故发生时。

## 3. 行业诉求

投放团队想用 Ads Cookie 操作后台，通常是因为：

- Google Ads API 申请、审批、权限管理和开发成本较高。
- 某些后台 UI 功能没有被 API 完整覆盖。
- 希望复用人工已登录状态，减少二次登录。
- 想批量管理多个账号、Campaign、关键词、素材和 URL。
- 想绕过 API 配额、审批或字段限制。

这些诉求可以理解为效率诉求，但 Cookie 登录态不是合规的系统集成边界。

## 4. 风险

| 风险 | 说明 |
| --- | --- |
| 账号接管 | Cookie 泄露后可能等同于攻击者已登录 |
| 授权不可控 | Cookie 不表达“只能改预算”或“只能读报表”这种最小权限 |
| 审计困难 | 难以证明哪个自然人批准了哪个动作 |
| 安全挑战 | 会话在异常设备、网络或地理位置使用可能触发挑战 |
| 合规风险 | 容易与 cookie theft、未授权访问、绕过安全保护混同 |
| 运维风险 | UI 变更、风控策略变化会导致自动化不稳定 |

## 5. 平台安全逻辑

从平台角度，登录 Cookie 是用户会话，不是开放集成接口。平台通常会结合多种信号判断会话是否正常：

- 登录和操作设备。
- 网络位置和 ASN。
- 浏览器、系统和语言环境。
- 操作路径是否符合正常 UI 交互。
- 批量操作频率和时间间隔。
- 会话是否在多个环境间异常迁移。
- 账号权限、付款信息、历史风险状态。

这些检查的目标是保护广告账号和广告主资产。

本文只讨论这些信号的治理意义：当团队发现登录态共享、异常设备、异常批量修改或挑战频繁出现时，应转为账号安全事件、访问权限复核和操作审计。本文不提供绕过检测、伪装设备、迁移会话或压低安全挑战概率的方法。

## 6. 合规替代方案

建议优先级：

1. Google Ads Editor CSV：适合人工审核后批量导入。
2. Google Ads Scripts：适合账号内授权脚本同步、报表和有限批量修改。
3. 官方 Google Ads API：适合长期产品化集成。
4. 人工审核队列：适合预算、URL、账号结构这类高风险动作。

替代方案的关键不是“慢一点”，而是保留：

- 明确授权。
- 可撤销访问。
- 审计记录。
- 最小权限。
- 可测试的输入输出。

替代连接器决策树：

| 场景 | 首选方式 | 原因 |
| --- | --- | --- |
| 批量创建或修改广告结构 | Google Ads Editor CSV | 可人工检查、可导入、可回滚 |
| 周期报表、有限批量动作 | Google Ads Scripts | 在授权账号内运行，有 preview/log 语义 |
| 长期产品化读写 | Google Ads API / OAuth | scope、token、quota、版本和错误模型清楚 |
| 高风险动作：预算、Final URL、conversion goal | 人工审批 + 官方工具执行 | 保留责任人和外部 Change history |
| 临时诊断和报表汇总 | 导出报表或手工导入 | 避免为了读数接管后台 |

不建议把 Playwright、Selenium、远程浏览器、浏览器 Profile 托管或服务端 Cookie jar 作为 Ads 后台连接器；即使技术上能打开页面，也无法解决授权范围、账号安全和变更审计问题。

## 7. 本系统落地

已实现：

- 广告账号配置页记录同步方式。
- 投放草稿 CSV 导出。
- Google Ads Scripts JSON payload 导出。
- 审计日志记录导出和变更。
- 页面明确标记 `No Cookie Automation`。
- `/tasks` 拦截 login、cookie、session、2FA、captcha、challenge 等任务语义。
- `/risk-audits` 记录 Cookie 后台操作风险、处理方案和来源 URL。
- `scripts/google_ads_script_payload_preview.js` 默认 preview-only，不使用 Cookie 或远程浏览器。

不实现：

- Cookie 存储。
- Cookie 导入。
- 浏览器 Profile 托管。
- 后台 UI 接管。
- 会话共享和绕过登录。
- 远程浏览器托管。
- 自动重放后台请求。
- 保存验证码、恢复码、密码或浏览器 Profile。

建议后续扩展实体表：

| 表 | 用途 | 禁止字段 |
| --- | --- | --- |
| `account_sync_profiles` | customer id、MCC、同步方式、负责人、授权状态 | cookie、session token、password |
| `ad_change_drafts` | campaign/ad/keyword/url/conversion 草稿 | login state、browser profile |
| `ad_change_approvals` | reviewer、decision、risk notes、rollback plan | OTP、captcha、recovery code |
| `external_execution_evidence` | CSV file hash、Scripts log、Change history link | copied cookie、raw browser storage |
| `account_security_incidents` | challenge、unusual login、access review、remediation | 绕过脚本、代理指纹配置 |

## 8. ADXKit 对应点和完成形态

ADXKit 公开页面强调“无需 API 审批”和通过脚本降低人工后台操作。本项目对这类诉求的处理是：

- 可以拆解为什么团队想绕过 API：审批、字段覆盖、批量操作和上线速度。
- 可以实现投放草稿、CSV 导出、Google Ads Scripts JSON payload 和人工审核队列。
- 可以记录账号同步方式、执行人、导出时间和审计日志。
- 不能实现 Cookie 获取、Cookie 注入、Cookie 复用、浏览器 Profile 托管或后台 UI 接管。

验收标准：

- `/accounts` 只记录账号配置和同步方式，不出现 Cookie 字段。
- `/campaigns` 可以导出 CSV 和 Scripts JSON。
- `/risk-audits` 可记录 Cookie 操作风险和来源 URL。
- `/sources` 可记录 MDN、Google Ads 安全文档、Google Ads API/OAuth 等来源。

## 9. 功能拆解和安全完成清单

把“Ads Cookie 登录后台”拆开看，真正可产品化的不是 Cookie 本身，而是后台操作前后的业务对象：

| 子能力 | 行业想解决的问题 | 本项目安全完成形态 |
| --- | --- | --- |
| 账号选择 | 运营要知道哪个 Customer ID、MCC、国家、币种和同步方式 | `/accounts` 记录账号配置、同步方式、状态和备注 |
| 投放变更准备 | 批量生成 Campaign、Ad Group、Keyword、Ad、Final URL | `/campaigns` 生成草稿，导出 CSV / Scripts JSON |
| 人工授权执行 | 高风险动作需要有人确认 | 导出后由授权人员在 Google Ads Editor、Scripts 或后台执行 |
| 结果对账 | 执行后要知道数据是否跑通 | `/metrics/import` 导入真实指标，Dashboard 和优化页计算 ROI |
| 留痕审计 | 要知道谁生成、谁导出、依据是什么 | `/logs` 记录导出和关键动作，`/sources` 记录来源 URL |
| 安全事件 | 登录挑战、异常设备、权限混乱需要复盘 | `/risk-audits` 记录账号安全事件、处理方案和来源 |

安全验收点：

- 数据模型不包含 Cookie、Session Token、浏览器 Profile、验证码或恢复码字段。
- 导出 payload 只包含广告结构、关键词、创意和 URL，不包含登录态。
- Google Ads Scripts JSON 带有 `no_cookie_automation` 标记，用来提醒执行链路不依赖 Cookie。
- Cookie 相关诉求只能进入 `/risk-audits`，处理方案应指向 CSV、Scripts、API、人工审核或账号权限治理。
- 开发扩展时如果需要读取 Google Ads 数据，应优先走 OAuth / API / Scripts 授权，而不是复用浏览器会话。

### 9.1 审计字段设计

当团队提出“用 Cookie 操作后台”或发现相关供应商能力时，审计记录至少包含：

| 字段 | 说明 |
| --- | --- |
| capability | 固定为 `ads_cookie_backend_operation` |
| requested_action | 想读报表、改预算、建广告、换 URL、同步状态还是批量导出 |
| account_scope | customer id / MCC / 业务主体 / 负责人 |
| why_cookie_requested | API 审批、字段覆盖、上线速度、批量操作、登录便利等原因 |
| safe_connector | CSV、Scripts、API、手工导入、人工后台执行 |
| risk_findings | 会话共享、权限过大、无审批、无回滚、无日志、安全挑战 |
| decision | rejected、mitigated、manual_only、api_backlog |
| evidence_url | Google / MDN / OWASP / 内部 SOP 来源 |
| reviewer | 审核人 |
| follow_up | API 申请、权限整理、Scripts preview、CSV 模板、账号安全复核 |

### 9.2 SOP

1. 收到 Cookie 后台操作需求时，先问业务目的，而不是问 Cookie 从哪里来。
2. 把需求归类为读数据、建结构、改预算、换 URL、修追踪、查拒登或账号协作。
3. 选择 CSV / Scripts / API / 人工后台执行中的最低风险路径。
4. 生成草稿或 payload，并保存版本、hash、reviewer 和回滚计划。
5. 授权人员在官方工具中执行，执行后回填 Change history、Scripts log 或导入结果。
6. 指标通过 `/metrics/import` 进入系统，不通过 Cookie 抓后台。
7. 如果出现登录挑战、异常设备、权限混乱或供应商要求共享会话，转账号安全事件。

### 9.3 通过/拒绝例子

| 需求 | 判断 | 处理 |
| --- | --- | --- |
| 批量创建 200 个关键词和 30 条广告 | 可替代 | 生成 Google Ads Editor CSV 或 Scripts JSON |
| 每小时抓后台报表截图 | 不建议 | 改为报表导出、API / Scripts 或手工导入 |
| 用远程浏览器保持登录并自动改预算 | 拒绝 | 改为预算草稿、审批、官方工具执行 |
| 供应商要求上传 Google 登录 Cookie | 拒绝 | 记录风险审计，改用只读报表或官方授权 |
| 账号频繁出现 Confirm it is you | 安全事件 | 检查访问权限、设备、共享登录和供应商操作 |

## 10. 信息来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| MDN, HTTP cookies | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies | Cookie 是 HTTP 状态机制，常用于会话管理 |
| MDN, Set-Cookie header | https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie | `Secure`、`HttpOnly`、`SameSite`、`Expires` / `Max-Age` 等属性说明 Cookie 的安全边界 |
| OWASP Session Management Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | 会话 ID 应视为敏感凭据，需要生命周期、传输和存储保护 |
| Google Ads Help, Secure your Google Ads account | https://support.google.com/google-ads/answer/2375456 | 支撑账号安全、2-Step Verification、访问审计和 cookie theft 风险语境 |
| Google Ads Help, Confirm it is you | https://support.google.com/google-ads/answer/12865189 | 支撑敏感或异常场景下的身份确认和安全挑战逻辑 |
| Google Ads Help, About access levels in your Google Ads account | https://support.google.com/google-ads/answer/9978556 | 支撑通过账号访问级别协作，而不是共享登录态 |
| Google Ads Help, Manager account access levels | https://support.google.com/google-ads/answer/9977851 | 支撑 MCC / manager account 权限边界和账号协作治理 |
| Google Ads API docs, Get started | https://developers.google.com/google-ads/api/docs/start | 官方 API 是长期产品化集成方向 |
| Google Ads API OAuth overview | https://developers.google.com/google-ads/api/docs/oauth/overview | API 集成应通过 OAuth 授权，而不是处理登录 Cookie |
| Google Ads Scripts, Start guide | https://developers.google.com/google-ads/scripts/docs/start | Scripts 是账号内授权脚本方向，可作为有限自动化替代 |
| Google Ads Scripts, Authorization | https://developers.google.com/google-ads/scripts/docs/authorization | Scripts 需要授权，适合作为可审计替代方案 |
| Google Ads Editor Help | https://support.google.com/google-ads/editor | Google Ads Editor 支撑人工审核型批量编辑和导入导出 |
