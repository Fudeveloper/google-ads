# 自动绕过登录、2FA、安全挑战研究

更新时间：2026-06-09

## 1. 范围

本文研究自动绕过登录、2FA 和安全挑战的原理、风险和替代方案。本文不提供验证码处理、2FA 接管、安全挑战绕过、账号恢复滥用或自动登录绕过流程。

## 2. 原理解释

认证链路通常由多个层次组成：

- 身份声明：用户输入账号。
- 知识因子：密码。
- 持有因子：手机、硬件安全密钥、Authenticator、一次性验证码。
- 环境评估：设备、位置、浏览器、网络、历史行为。
- 风险挑战：在异常场景下触发额外验证。

2FA 的目的不是增加操作摩擦，而是降低单一密码或单一 Cookie 泄露带来的账号接管风险。安全挑战通常在系统判断登录或操作存在异常时触发，例如新设备、新地区、可疑会话迁移、敏感操作或账号风险升高。

“自动绕过”意味着试图让程序通过、规避、压制或消除这些保护机制。它和普通自动化不同，因为它对抗的是账号安全边界。

### 2.1 Step-up challenge 的业务含义

安全挑战不是独立功能，而是认证系统在风险升高时触发的 step-up 保护。它通常用于回答：

- 当前操作者是否真的是账号所有者或授权用户？
- 当前设备、网络、地区和历史使用习惯是否一致？
- 当前动作是否敏感，例如预算、付款、用户权限、URL、账号结构或大批量变更？
- 会话是否可能来自 Cookie 迁移、凭据泄露、远程控制或异常自动化？

因此，“自动处理安全挑战”在行业里看起来像效率工具，实质上是在把平台设计给真实用户确认的安全边界外包给程序或供应商。

### 2.2 账号协作和绕过登录的区别

| 场景 | 合规协作 | 高风险绕过 |
| --- | --- | --- |
| 多人管理账号 | 使用访问级别、MCC、最小权限和审计 | 共用主账号、共用验证码、共用浏览器登录态 |
| 无人值守任务 | 生成草稿、导出 payload、授权人员执行 | 自动登录后台并处理挑战 |
| 外包投放 | 分配独立用户和限定权限 | 交付 Cookie、恢复码、2FA 设备或远程桌面 |
| 敏感变更 | 人工批准并记录证据 | 程序自动确认预算、URL、账号权限 |

### 2.3 自动化设计原则

系统应把“准备动作”和“授权执行”分开：

1. 准备动作可以自动化：生成创意、计算 ROI、导出 CSV、生成 Scripts JSON、跑页面审计。
2. 授权执行必须可追溯：由有权限的人在 Google Ads Editor、Scripts 或后台完成。
3. 敏感动作必须可回滚：预算、URL、账号权限、付款和批量修改要留变更前后快照。
4. 认证失败不是任务失败重试问题，而是账号安全事件，应进入人工处理和审计。

### 2.4 认证链路状态机

登录、2FA 和安全挑战可以被理解为一条状态机，而不是一个可以被“脚本补齐”的表单：

```text
identity_claim
  -> password_verified
  -> second_factor_required
  -> second_factor_verified
  -> risk_evaluation
  -> step_up_challenge_required?
  -> authorized_session
  -> sensitive_action_recheck?
  -> action_committed
  -> audit / change history
```

每个状态回答的问题不同：

| 状态 | 安全问题 | 系统应如何处理 |
| --- | --- | --- |
| identity_claim | 操作者是谁 | 不保存账号密码 |
| password_verified | 是否知道密码 | 不托管密码和登录会话 |
| second_factor_required | 是否持有第二因素 | 不收验证码、Authenticator secret、短信内容 |
| risk_evaluation | 环境和行为是否异常 | 异常转人工，不做伪装 |
| step_up_challenge_required | 是否需要真人确认 | 转账号安全事件 |
| authorized_session | 是否已经通过认证 | 仍不复制 Cookie 或浏览器 Profile |
| sensitive_action_recheck | 预算、付款、权限、URL 是否需二次确认 | 进入人工审批和外部执行证据 |

“自动绕过”的危险在于，它把 `second_factor_required`、`risk_evaluation` 和 `step_up_challenge_required` 这些安全状态当作普通程序分支处理。合规系统应做的是在这些状态出现时停止自动执行，并创建人工核验任务。

### 2.5 人机分工边界

| 能自动化 | 必须人审 / 人工执行 | 禁止自动化 |
| --- | --- | --- |
| 生成 campaign / keyword / creative 草稿 | 启停 campaign、改预算、改 Final URL、改 conversion goal | 登录、验证码、2FA、captcha、安全挑战 |
| 跑 URL QA、claim review、ROI 计算 | 外部 Google Ads Editor / Scripts 执行确认 | 保存密码、恢复码、Authenticator secret |
| 生成 Scripts JSON 和 CSV | 账号权限变更、付款资料、用户邀请 | 远程浏览器长期保持登录 |
| 检测任务 payload 是否含禁词 | 异常登录、Confirm it is you、账号锁定 | 自动重试挑战或寻找替代账号 |

这条边界让团队保留自动化效率，但不把安全确认委托给程序、外包供应商或无审计的浏览器会话。

### 2.6 任务系统中的危险语义

任务中心最容易被误用为“后台机器人”。因此任务类型、payload 和描述里出现以下语义，应默认拒绝或转风险审计：

| 语义 | 风险解释 | 安全替代 |
| --- | --- | --- |
| login / signin / password | 涉及凭据托管 | 账号权限、OAuth、人工执行 |
| cookie / session / profile | 涉及会话接管 | CSV、Scripts、API |
| otp / 2fa / mfa / authenticator | 涉及第二因素接管 | 授权人员人工确认 |
| captcha / challenge / confirm | 涉及安全挑战绕过 | 账号安全事件 |
| recovery / backup code | 涉及账号恢复滥用 | 访问权限复核 |
| retry login / keep alive | 可能放大异常登录 | 停止任务并升级 |

## 3. 行业诉求

投放团队可能有这些诉求：

- 多账号批量登录，减少人工输入。
- 账号分布在不同国家、设备或外包团队。
- 希望服务器长期保持登录状态。
- 遇到安全挑战时不想等待人工处理。
- 想让无人值守任务持续修改广告。

这些诉求应该通过权限、审核队列、API、脚本和运维流程解决，而不是绕过认证保护。

## 4. 风险

| 风险 | 说明 |
| --- | --- |
| 账号安全 | 绕过或弱化 2FA 会扩大账号接管影响 |
| 合规和法律 | 可能被视为未授权访问或规避安全机制 |
| 团队治理 | 多人共享验证码或登录态会破坏责任归属 |
| 平台风控 | 异常挑战处理模式可能触发更强限制 |
| 数据安全 | 外包或工具供应商可能接触高敏凭据 |

## 5. 平台安全逻辑

Google Ads 安全建议强调：

- 启用 2-Step Verification。
- 使用强密码。
- 定期检查和移除不需要的账号访问。
- 给用户分配合适权限。
- 保护账号免受 cookie theft 和未授权访问。

这说明平台鼓励通过身份和权限治理来提升安全，而不是通过共享登录态或绕过挑战来提高效率。

从运营治理角度看，安全挑战和 MFA 不是“脚本失败原因”，而是账号风险信号。常见触发语境包括新设备、新地点、可疑会话迁移、敏感设置变更、权限/付款动作、异常批量操作或系统需要确认当前操作者身份。系统只能记录和升级这些信号，不应研究如何降低触发概率或自动通过挑战。

## 6. 合规替代方案

推荐做法：

- 用 Google Ads 账号访问权限分配角色。
- 使用 MCC 管理多客户账号。
- 通过 Google Ads API OAuth 授权访问。
- 通过 Google Ads Scripts 由授权用户安装脚本。
- 对高风险动作使用人工审核队列。
- 对外包人员使用最小权限账号。
- 定期审计账号访问。

替代方案的核心设计：

| 运营诉求 | 安全替代 |
| --- | --- |
| 减少频繁登录 | 使用个人账号 + 合理访问级别 + MCC，不共享主账号 |
| 定时执行检查 | 任务中心只跑页面 QA、导出检查、指标复核等低风险任务 |
| 批量修改广告 | CSV / Scripts payload，授权人员在官方工具中执行 |
| 多人协作 | Google Ads access levels、manager account、最小权限 |
| 外包投放 | 独立用户、限定权限、移除不需要访问、审计日志 |
| 后续产品化集成 | OAuth / Google Ads API / Scripts authorization |
| 安全挑战频繁 | 账号安全复核、设备/访问/供应商排查、人工处理 |

## 7. 本系统落地

系统将执行链路设计为：

```text
投放草稿 -> 审核 -> CSV / Scripts JSON -> 授权人员执行 -> 指标导入 -> 审计
```

这样保留了自动化准备能力，但不接管登录、不绕过 2FA、不处理安全挑战。

已落地：

- `/tasks` 任务中心拒绝 login、cookie、2FA、captcha、challenge、session、recovery 等任务语义。
- `/logs` 记录任务创建、拒绝、执行结果和导出动作。
- `/risk-audits` 记录认证挑战、共享登录态、外包访问、权限过大和异常登录风险。
- `/accounts` 只保存账号配置、同步方式和备注，不保存密码、Cookie、Profile 或恢复码。
- Scripts payload preview 模板默认 `PREVIEW_ONLY=true`，不远程登录后台。

建议后续扩展实体表：

| 表 | 用途 | 禁止字段 |
| --- | --- | --- |
| `access_review_cases` | 用户、角色、MCC、访问理由、复核状态 | password、OTP、backup code |
| `auth_incident_events` | Confirm it is you、challenge、lockout、unusual login | challenge answer、captcha token |
| `task_safety_reviews` | task_type、payload_hash、blocked_keyword、decision | browser profile、session token |
| `manual_execution_evidence` | 执行人、官方工具、Change history / Scripts log | copied login state |

## 8. ADXKit 对应点和完成形态

ADXKit 类产品常把“少登录后台、任务自动执行、脚本自动同步”作为效率卖点。这里需要区分：

- 合规自动化：已授权的 Scripts、API、CSV 导入、人工确认后的任务记录。
- 高风险自动化：自动处理验证码、接管 2FA、绕过安全挑战、复用登录态。

本项目完成形态：

- 任务中心只执行安全任务，例如导出检查、页面复核、指标复核。
- 账号协作依赖 Google Ads 访问级别、MCC 或官方 OAuth 授权。
- 高风险动作进入 `/risk-audits`，默认需要暂停、修复或拒绝。
- 不保存验证码、一次性密码、恢复码、浏览器登录状态或安全挑战答案。

验收标准：

- `task_jobs` 的任务类型白名单不包含登录、2FA、验证码、安全挑战处理。
- 所有执行结果写入审计日志。
- `/sources` 至少记录 Google Ads 安全、账号访问级别、OAuth、Scripts 授权等来源。

## 9. 功能拆解和安全完成清单

把“自动绕过登录、2FA、安全挑战”拆成业务诉求后，可安全交付的是任务编排、权限治理和异常处理，而不是挑战处理器：

| 子能力 | 行业想解决的问题 | 本项目安全完成形态 |
| --- | --- | --- |
| 批量准备任务 | 不想反复人工创建素材和结构 | Offer、创意、Campaign 草稿和导出自动化 |
| 定时提醒 | 不想漏掉复核、导入、换链、对账 | `/tasks` 只创建安全任务，例如导出检查、页面复核、指标复核 |
| 授权执行 | 需要证明动作由有权限的人执行 | CSV / Scripts JSON 后由授权人员确认执行 |
| 安全异常处理 | 遇到挑战、锁定或可疑登录时要有 SOP | 文档和风险审计要求暂停、核验账号访问、保留证据 |
| 访问治理 | 外包或多人协作需要边界 | 使用 Google Ads 访问级别、MCC、最小权限和定期审计 |

安全验收点：

- 任务类型白名单不得出现登录、验证码、OTP、2FA、challenge、recovery、cookie refresh 等动作。
- 系统不保存一次性验证码、恢复码、安全问题答案、短信内容、Authenticator secret 或登录状态。
- 任何“自动登录失败后重试”的需求都按账号安全事件处理，而不是当作普通任务失败。
- 账号协作文档指向访问级别、OAuth、Scripts 和人工审核，而不是共享主账号。
- 审计记录应能说明某个 payload 何时生成、谁审核、谁到官方后台执行。

### 9.1 审计字段设计

| 字段 | 说明 |
| --- | --- |
| capability | 固定为 `automated_login_2fa_challenge_bypass` |
| trigger | login failed、2FA requested、Confirm it is you、captcha、account locked、vendor asked for code |
| account_scope | customer id、MCC、业务主体、负责人 |
| actor | 内部员工、外包、工具、供应商、未知 |
| requested_automation | 想自动做什么：登录、重试、验证码、挑战、远程浏览器、定时后台动作 |
| safe_path | access review、OAuth、Scripts、CSV、manual execution、incident response |
| risk_findings | 共享账号、权限过大、验证码共享、恢复码泄露、异常设备、无审计 |
| decision | rejected、manual_only、access_fix、security_incident、api_backlog |
| evidence_url | Google Ads 安全、访问级别、OAuth、Scripts、OWASP / NIST 来源 |
| reviewer | 审核人 |
| follow_up | 移除访问、启用 2SV、重置凭据、申请 API、改任务类型 |

### 9.2 SOP

1. 任何登录、2FA、captcha、challenge、recovery 相关任务请求先拒绝自动执行。
2. 判断触发原因：正常权限协作、账号异常、供应商要求、脚本误用还是真实账号安全事件。
3. 如果只是运营效率诉求，转为 CSV、Scripts、API、人工审批或访问级别调整。
4. 如果出现 Confirm it is you、账号锁定、异常登录、共享验证码或恢复码暴露，创建安全事件。
5. 复核 Google Ads 访问用户、MCC 权限、外包账号、最近变更和执行证据。
6. 清理不需要访问，必要时重置密码、撤销会话、启用或强化 2-Step Verification。
7. 复盘后把任务系统的 blocked keyword、任务白名单和培训文档更新。

### 9.3 通过/拒绝例子

| 需求 | 判断 | 处理 |
| --- | --- | --- |
| 每天提醒人工导入 CSV 并记录结果 | 可通过 | `/tasks` 安全任务 + `/logs` |
| 定时生成 Scripts payload 并让授权人员预览 | 可通过 | preview-only payload + 人工执行 |
| 自动输入 2FA 验证码继续跑任务 | 拒绝 | 记录风险审计，改为人工确认 |
| 登录失败后自动换浏览器 Profile 重试 | 拒绝 | 账号安全事件 |
| 外包要求共享恢复码以便无人值守 | 拒绝 | 访问权限治理和供应商风险复核 |
| 账号出现 Confirm it is you | 升级 | 停止自动任务，人工核验账号安全 |

## 10. 信息来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, Secure your Google Ads account | https://support.google.com/google-ads/answer/2375456 | 支撑 2-Step Verification、账号安全、访问审计和 cookie theft 风险语境 |
| Google Ads Help, Confirm it is you | https://support.google.com/google-ads/answer/12865189 | 支撑敏感或异常场景下的身份确认和安全挑战逻辑 |
| Google Ads Help, About access levels in your Google Ads account | https://support.google.com/google-ads/answer/9978556 | 支撑按访问级别协作，而不是共享登录态或验证码 |
| Google Ads Help, Manager account access levels | https://support.google.com/google-ads/answer/9977851 | 支撑 MCC / manager account 权限边界 |
| Google Account Help, Turn on 2-Step Verification | https://support.google.com/accounts/answer/185839 | 支撑 2SV 是账号保护机制，不应被外包给自动化 |
| Google Ads API OAuth overview | https://developers.google.com/google-ads/api/docs/oauth/overview | 支撑通过 OAuth 授权访问 Google Ads API |
| Google Ads Scripts, Authorization | https://developers.google.com/google-ads/scripts/docs/authorization | 支撑 Scripts 需要授权，适合作为账号内可审计自动化 |
| Google Ads Scripts, Start guide | https://developers.google.com/google-ads/scripts/docs/start | 支撑 Scripts 的官方执行入口和边界 |
| OWASP Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | 支撑认证失败、安全响应和凭据保护原则 |
| OWASP Multifactor Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | 支撑 MFA 因子、恢复流程和不可弱化第二因素的治理 |
| NIST SP 800-63B, Authentication and Authenticator Management | https://pages.nist.gov/800-63-4/sp800-63b.html | 支撑认证器、会话和风险管理的数字身份参考 |
