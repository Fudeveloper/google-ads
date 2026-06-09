# 高风险能力逐点调研与安全复刻蓝图

更新时间：2026-06-09

本文把 ADXKit 类产品公开叙事中最敏感的 6 个能力，逐点拆成行业诉求、原理解释、平台风险、系统落地、验收证据和信息来源 URL。这里的“复刻”不是跳过，也不是把危险动作写成可执行程序，而是把套利团队真正要解决的问题沉淀成可审计的知识、流程、数据结构和替代工作流。

完成口径：

- 复刻行业知识：说明为什么套利团队会提出这个需求。
- 复刻原理解释：说明广告系统、认证系统、会话系统、流量质量系统或账号治理系统背后的判断逻辑。
- 复刻安全替代：把需求落成草稿、导入导出、人工审核、风险审计、来源库和 SOP。
- 复刻验收证据：每个点都有 Markdown 专题、系统入口、审计字段和来源 URL。
- 不复刻执行型对抗：不交付 Cookie 接管、登录绕过、刷量、代理指纹规避、cloaking 或封禁规避实现。

## 1. 总体架构原则

ADXKit 类工具的公开卖点通常围绕“少登录、批量投放、快速换链接、AI 创意、自动优化、多账号隔离、脚本同步、流量自然化”展开。套利团队关心这些能力，本质上是因为业务同时面对四个约束：

1. 速度约束：Offer 生命周期短，素材、关键词、链接和预算需要快速迭代。
2. 利润约束：CPC、EPC、RPM、扣量、结算周期和现金流共同决定能不能扩量。
3. 平台约束：Google Ads、AdSense、AdX、GAM、Affiliate Network 和 Lead Buyer 都有政策、质量和结算规则。
4. 风险约束：账号、域名、落地页、追踪链、流量来源、付款资料和操作者之间会形成关联图谱。

因此系统设计采用两层架构：

| 层级 | 负责什么 | 可以自动化 | 必须人工或外部授权 |
| --- | --- | --- | --- |
| 准备层 | Offer、落地页、创意、关键词、投放草稿、ROI 测算、链接候选、来源记录 | 可以在本系统生成、导入、导出和打分 | 高风险 claim、预算、Final URL 和账号动作需要审批 |
| 执行层 | Google Ads 后台、Google Ads Editor、Google Ads Scripts、官方 API、人工审核、申诉 | 只使用授权、可审计、可回滚的连接方式 | 登录、2FA、安全挑战、政策申诉和封禁恢复不交给绕过程序 |

这套分层保留了套利业务需要的速度和知识沉淀，同时避免把系统做成会话接管、流量伪造或规避审核工具。

## 2. Ads Cookie 登录和后台操作

### 2.1 行业诉求

套利团队提出 Cookie 登录和后台操作，通常不是为了研究 Cookie 本身，而是为了解决这些运营问题：

- 账号多、Campaign 多，手工改预算、关键词、Final URL 和 Tracking Template 太慢。
- API 审批、开发或字段覆盖不完整时，希望用网页后台作为“事实上的接口”。
- 外包投手、素材团队或运营团队希望少走登录授权流程。
- 需要快速读取后台状态、拒登原因、报表和 Change History。

### 2.2 原理解释

HTTP Cookie 是浏览器和服务器之间维护状态的机制。登录态 Cookie、Session Token 或浏览器 Profile 一旦被复用，通常等同于把已认证会话交给另一个程序或操作者。对于 Google Ads 后台，Cookie 会话背后连接的是预算、付款、账号权限、Campaign、Ad Group、Keyword、Ad、Final URL、Conversion Goal 等有资金和政策后果的对象。

后台 UI 操作不是普通网页抓取。每次点击保存、启停、改预算、换链接或批量编辑，都可能产生真实投放效果、账单影响、政策审核和历史记录。如果程序绕过正式授权流程直接复用 Cookie，就难以证明操作者身份、权限范围、变更依据和回滚路径。

### 2.3 平台风险

Cookie 登录和后台接管的风险不只在技术层：

- 账号安全：Cookie 可能被视为敏感会话凭据，泄露或共享会扩大账号接管风险。
- 权限治理：绕过 Google Ads 用户访问级别和授权记录后，很难区分谁发起了变更。
- 审计缺口：自动 UI 操作如果没有内部审批、快照和外部 Change History 对齐，会导致责任不清。
- 政策风险：Final URL、预算、追踪模板和素材变更可能触发审核、规避系统或目的地不一致问题。

### 2.4 系统落地

本项目把该能力复刻为“授权执行前的准备和审计工作台”：

| 可交付能力 | 系统入口 | 说明 |
| --- | --- | --- |
| 账号同步方式记录 | `/accounts` | 记录 Customer ID、同步方式、状态、备注，不保存 Cookie、Session Token 或浏览器 Profile |
| 投放结构准备 | `/campaigns` | 生成 Campaign / Ad Group / Keyword / Ad / Final URL 草稿 |
| 安全导出 | `/campaigns/<id>/export.csv`、`/campaigns/<id>/export.script.json` | 交给 Google Ads Editor 或 Scripts 授权执行 |
| No Cookie Automation 标记 | Scripts JSON payload | 导出内容包含 `no_cookie_automation`，明确不依赖登录态接管 |
| 风险审计 | `/risk-audits` | 记录 Cookie 操作诉求、替代方案、来源 URL 和处理结果 |

不交付：Cookie 获取、导入、注入、复用、浏览器 Profile 托管、后台 UI 接管、保存密码、保存恢复码。

### 2.5 验收证据

- 专题文档：[Ads Cookie 登录和后台操作](high_risk/ads_cookie_backend_operation.md)
- 系统入口：`/accounts`、`/campaigns`、`/logs`、`/risk-audits`
- 自动检查：`scripts/acceptance_audit.py` 会拦截账号配置中的 Cookie / Session / Browser Profile 语义，并检查 Scripts JSON 的 `no_cookie_automation` 标记。

## 3. 自动绕过登录、2FA、安全挑战

### 3.1 行业诉求

套利团队提出自动绕过登录、2FA 或安全挑战，常见原因是：

- 定时任务需要无人值守执行。
- 多人协作时不想频繁索要验证码或确认身份。
- 账号分布在不同国家、设备和操作者之间，登录摩擦高。
- 外包团队希望直接处理后台任务，而不是走账号权限配置。

### 3.2 原理解释

2FA 和安全挑战是认证链路中的 step-up control。系统会在密码或 Cookie 之外，要求额外证明：当前操作者、设备、位置、行为和敏感动作是否可信。它的目的不是增加表单步骤，而是降低凭据泄露、会话迁移、异常设备、敏感变更和账号接管的风险。

安全挑战可以理解为状态机：

| 状态 | 触发条件 | 合规处理 |
| --- | --- | --- |
| 已授权 | 正常用户、正常设备、正常动作 | 按权限执行 |
| 需要二次确认 | 新设备、新位置、敏感预算/付款/权限/URL 动作 | 由授权用户完成确认 |
| 账号安全事件 | 异常登录、疑似接管、挑战失败、账号锁定 | 暂停自动化，进入安全复盘 |
| 权限不足 | 当前用户没有操作权 | 调整访问级别或使用正式授权 |

### 3.3 平台风险

绕过 2FA、验证码、安全挑战或确认身份，会把安全控制从“证明操作者可信”降级成“程序继续跑”。这会带来：

- 账号接管风险扩大。
- 外包或供应商越权操作风险。
- 付款、预算、URL、权限变更不可控。
- 触发 Google Ads 或 Google Account 的安全保护。

### 3.4 系统落地

本项目把该能力复刻为任务编排和人工授权：

| 可交付能力 | 系统入口 | 说明 |
| --- | --- | --- |
| 安全任务中心 | `/tasks` | 只允许落地页采集、创意生成、CSV / Scripts 导出、指标导入、优化建议等准备层任务 |
| 危险语义拦截 | `/tasks`、`adsworkbench/services/tasks.py` | 拦截 login、cookie、session、2FA、captcha、challenge、recovery 等语义 |
| 权限模型说明 | 文档 | 使用 Google Ads 访问级别、OAuth、Scripts 授权替代共享登录态 |
| 安全事件审计 | `/risk-audits` | 记录挑战触发原因、处理方式、证据 URL 和负责人 |

不交付：验证码识别、OTP 自动输入、2FA 接管、安全挑战绕过、恢复码保存、自动登录后台。

### 3.5 验收证据

- 专题文档：[自动绕过登录、2FA、安全挑战](high_risk/automated_login_2fa_challenge_bypass.md)
- 系统入口：`/tasks`、`/risk-audits`、`/logs`
- 自动检查：`scripts/acceptance_audit.py` 会提交包含 Cookie / 2FA / challenge 语义的任务备注，并确认系统拒绝保存。

## 4. 补点击、刷展示、模拟自然流量

### 4.1 行业诉求

补点击、刷展示或模拟自然流量的诉求，通常来自短期报表压力和追踪误解：

- 报表看起来“不自然”，想让点击、展示、CTR、停留时间、跳出率更平滑。
- Tracking 掉数、Postback 延迟、Revenue lag 或买方扣量后，误以为“补一点流量”能修复账。
- 想提高 AdSense / AdX 侧收入或降低广告主侧 CPA 表面值。
- 流量供应商或外包团队用“自然化”包装低质或虚假流量。

### 4.2 原理解释

广告套利的核心账本是 Click -> Session -> Conversion -> Revenue -> Settlement。每一层都可能有延迟、过滤、扣量和归因差异。缺失点击或收入不等于应该补点击，而应该先判断：

- 点击是否来自真实广告系统或真实流量来源。
- Session 是否可在 analytics、server log、tracking platform 中解释。
- Conversion 是否有 buyer / affiliate network / CRM 的状态回传。
- Revenue 是 estimated、finalized、paid 还是 disputed。
- 扣量来自无效流量、重复线索、低质量来源、追踪断点还是结算规则。

人为点击、展示或行为模拟会污染竞价学习、质量评估、发布商收入、广告主成本和结算证据。短期报表可能变好，长期会让模型学习错误、来源评分失真、申诉证据变弱。

### 4.3 平台风险

无效流量风险包括：

- 人为抬高广告主成本或发布商收入。
- 自动点击、自动浏览、点击交换或诱导点击。
- 使用脚本、机器人、低质供应商或伪造行为路径。
- 把追踪断点、回传延迟或扣量问题错误处理成“补流量”。

### 4.4 系统落地

本项目把该能力复刻为真实指标治理和异常诊断：

| 可交付能力 | 系统入口 | 说明 |
| --- | --- | --- |
| 真实指标导入 | `/metrics/import` | 导入成本、点击、展示、转化和收入，不生成虚假流量 |
| ROI / RPV / CPC 分析 | `/optimization` | 根据真实数据给出 stop-loss、来源隔离、素材错配、追踪检查建议 |
| 流量账本 SOP | 文档 | 用 Click -> Session -> Revenue 对账解释差异 |
| 来源质量治理 | `/sources`、相关知识文档 | 记录供应商、source、placement、geo、device、deduction 和证据 |

不交付：点击任务、展示任务、自动访问、Referer 伪造、停留时长模拟、滚动/鼠标行为模拟、自然用户路径生成。

### 4.5 验收证据

- 专题文档：[补点击、刷展示、模拟自然流量](high_risk/invalid_traffic_click_impression_simulation.md)
- 系统入口：`/metrics/import`、`/optimization`、`/sources`、`/risk-audits`
- 自动检查：任务系统禁用 click、impression、visit、traffic simulation 等危险语义。

## 5. 代理、指纹、Worker 转发规避关联检测

### 5.1 行业诉求

代理、浏览器指纹、Worker 转发和“防关联”常被包装成多账号运营基础设施。真实诉求通常包括：

- 多账号、多域名、多 Offer 同时投放，担心被判相关。
- 账号受限后希望继续投放同一业务。
- 想隐藏操作者、服务器、真实落地页或追踪链。
- 用边缘 Worker 做转发、缓存、A/B 测试或地区可用性检查。

### 5.2 原理解释

代理、指纹和 Worker 都是中性技术：

- 代理改变网络出口或访问路径。
- 浏览器指纹由 User-Agent、字体、屏幕、时区、Web API、Canvas、设备能力等多类信号组合而成。
- Worker / Edge Function 可以在边缘节点处理请求、缓存、路由和安全逻辑。

但广告平台的关联判断通常不是单点规则，而是图谱问题。账号、MCC、域名、落地页、Offer、素材、关键词、Final URL、Tracking URL、付款资料、登录用户、操作节奏、转化质量、投诉和历史违规都会形成边。只改 IP、指纹或 Worker，不会改变业务主体、资金、页面、Offer 和流量质量之间的实质关联。

### 5.3 平台风险

高风险信号包括：

- 用代理池隐藏真实操作者或后台登录来源。
- 用指纹浏览器让多个相关账号看起来无关。
- 用 Worker 隐藏真实 Final URL、Offer、落地页或审核链路。
- 账号受限后换代理、换指纹、换账号继续跑同一问题业务。

### 5.4 系统落地

本项目把该能力复刻为关联风险审计和合法隔离证据：

| 可交付能力 | 系统入口 | 说明 |
| --- | --- | --- |
| 关联资产图谱 | 文档和 `/risk-audits` | 盘点 account、MCC、domain、offer、payment、operator、tracking、source、complaint |
| 合法隔离证据包 | 文档 | 证明业务主体、预算、页面、Offer、流量来源和责任人真实独立 |
| Worker 用途审查 | `/risk-audits` | 只记录安全、性能、缓存、QA、可用性用途，不保存规避脚本 |
| 链路透明 QA | `/links` 和追踪链文档 | 记录候选 URL、版本、人工确认和一致性 |

不交付：代理池、IP 轮换、指纹 Profile、反检测浏览器配置、Worker 分流脚本、关联规避策略、账号运营伪装。

### 5.5 验收证据

- 专题文档：[代理、指纹、Worker 转发规避关联检测](high_risk/proxy_fingerprint_worker_association_evasion.md)
- 系统入口：`/accounts`、`/links`、`/risk-audits`、`/sources`
- 自动检查：账号、链接和任务表单会拦截 proxy pool、fingerprint、anti-detect、worker forward、防关联等语义。

## 6. Cloaking 或审核页/用户页不一致

### 6.1 行业诉求

套利业务经常需要换链接、做 A/B 测试、按国家语言展示不同页面、修复追踪链或切换 Offer。风险在于，有些团队会把这些正常操作升级成审核页/用户页不一致：

- 审核时展示合规页面，真实用户看到另一套页面。
- 按 AdsBot、Googlebot、IP、User-Agent、Cookie、地理、设备或时间分流。
- 广告审核后把 Final URL 或跳转链换成高风险页面。
- 用 Worker、反向代理或 tracking redirect 隐藏真实目的地。

### 6.2 原理解释

合规的本地化、A/B 测试和链接维护，核心是“同一广告承诺下，Google 审核和用户看到的目的地一致、可达、可解释”。差异化页面是否安全，应看：

- 差异是否由语言、币种、库存、设备适配或真实实验驱动。
- 是否所有用户和审核系统都能看到同等主题、同等承诺、同等商业主体的页面。
- Final URL、Tracking Template、Redirect、Landing Page 和 Offer 是否一致。
- 是否保留页面版本、上线时间、审批人、截图、URL QA 和回滚证据。

### 6.3 平台风险

Google Ads 的 Circumventing systems 和 Destination requirements 都把隐藏真实目的地、向 Google 和用户展示不同内容、规避审核、恶意或误导性跳转视为高风险。Cloaking 不只是“技术分流”，而是广告承诺、审核证据和用户体验不一致。

### 6.4 系统落地

本项目把该能力复刻为链接计划和目的地一致性治理：

| 可交付能力 | 系统入口 | 说明 |
| --- | --- | --- |
| 合规链接计划 | `/links` | 候选 URL 必须是同主题、已审核、人工确认 |
| 手动轮换留痕 | `/links/<id>/rotate`、`/logs` | 轮换记录 old URL、new URL、时间和审计日志 |
| Review/User 一致性矩阵 | 文档 | 判断 A/B 测试、本地化、设备适配和 cloaking 边界 |
| Tracking chain QA | 文档 | 检查 Final URL、tracking template、redirect hops、UTM/SubID 一致性 |

不交付：Bot 分流、审核页/用户页双版本、隐藏目的地、审核后切违规页、按 Google IP/User-Agent/Cookie/指纹展示不同页面。

### 6.5 验收证据

- 专题文档：[Cloaking 或审核页/用户页不一致](high_risk/cloaking_review_user_page_mismatch.md)
- 系统入口：`/links`、`/risk-audits`、`/logs`
- 自动检查：`scripts/acceptance_audit.py` 会提交 worker forward / proxy pool 链接计划并确认被拒绝。

## 7. 为规避封禁创建或切换账号

### 7.1 行业诉求

封禁或账号限制会直接影响现金流，所以团队常提出账号池、批量开户、自动换号或“不断号”诉求。真实业务问题通常是：

- 不知道账号为什么被限制。
- 缺少政策、付款、身份验证、落地页、流量来源和历史变更证据。
- Offer、域名、付款资料、操作者或追踪链在多个账号之间重复。
- 想把封禁当成容量问题，而不是质量和合规问题。

### 7.2 原理解释

广告账号不是孤立资产。平台可能把账号、MCC、付款资料、广告主身份、域名、落地页、Offer、素材、关键词、转化、用户权限、登录行为、投诉和历史违规串成关联图谱。封禁后的关键不是“换壳继续跑”，而是回答：

- 原始限制原因是什么。
- 违规或风险对象是否已经停止或修复。
- 新账号是否真实独立，还是沿用同一问题资产。
- 是否有可验证的申诉证据和修复记录。

### 7.3 平台风险

封禁后创建或切换账号继续同一问题业务，可能构成规避系统或多账号规避。风险包括：

- 相关账号被连续限制。
- 付款资料、域名、落地页和广告主身份被纳入更大范围审查。
- 原本可以申诉修复的问题变成对抗平台执行。
- 数据和结算证据失真，团队无法定位真实原因。

### 7.4 系统落地

本项目把该能力复刻为账号健康和恢复证据包：

| 可交付能力 | 系统入口 | 说明 |
| --- | --- | --- |
| 账号状态记录 | `/accounts` | 记录 active、paused、limited、suspended 等状态和备注 |
| 账号健康 SOP | 文档 | 按政策、付款、验证、域名、流量来源、Change History 复盘 |
| 申诉证据包 | `/risk-audits` 和文档 | 记录限制原因、修复动作、截图/URL/来源和负责人 |
| 正常多账号准入 | 文档 | 只接受真实业务、不同主体、清晰权限、独立资金和合法代理关系 |

不交付：批量开户、账号池、付款资料规避、封禁后自动换号、同 Offer 换壳继续跑、规避 related-account 审查。

### 7.5 验收证据

- 专题文档：[为规避封禁创建或切换账号](high_risk/ban_evasion_account_switching.md)
- 系统入口：`/accounts`、`/risk-audits`、`/logs`
- 自动检查：账号配置会拦截 ban evasion、account pool、bulk account、封禁后、换号继续、账号池等语义。

## 8. 统一验收矩阵

| 高风险点 | 原理解释是否完成 | MD 专题 | 系统完成形态 | 自动验收 |
| --- | --- | --- | --- | --- |
| Ads Cookie 登录和后台操作 | 是：Cookie、会话、后台对象、操作生命周期 | `docs/high_risk/ads_cookie_backend_operation.md` | `/accounts`、CSV / Scripts JSON、`/risk-audits` | 账号危险语义拦截、No Cookie Automation |
| 自动绕过登录、2FA、安全挑战 | 是：step-up challenge、认证状态机、人机边界 | `docs/high_risk/automated_login_2fa_challenge_bypass.md` | `/tasks`、`/risk-audits` | 任务危险语义拦截 |
| 补点击、刷展示、模拟自然流量 | 是：流量账本、无效流量、追踪断点、扣量 | `docs/high_risk/invalid_traffic_click_impression_simulation.md` | `/metrics/import`、`/optimization` | 禁止点击/展示/访问模拟任务 |
| 代理、指纹、Worker 转发规避关联检测 | 是：关联图谱、中性技术、合法隔离证据 | `docs/high_risk/proxy_fingerprint_worker_association_evasion.md` | `/risk-audits`、`/accounts`、`/links` | 账号/链接/任务危险语义拦截 |
| Cloaking 或审核页/用户页不一致 | 是：目的地一致性、Review/User 矩阵、URL 生命周期 | `docs/high_risk/cloaking_review_user_page_mismatch.md` | `/links`、`/logs`、`/risk-audits` | 链接计划危险语义拦截 |
| 为规避封禁创建或切换账号 | 是：账号图谱、暂停状态机、Related Account、申诉证据 | `docs/high_risk/ban_evasion_account_switching.md` | `/accounts`、`/risk-audits` | 账号危险语义拦截 |

## 9. 来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| ADXKit homepage | https://adxkit.com/ | 作为 public claim 来源，用于拆解其公开宣称的 Google Ads 管理、Scripts、AI 创意、换链接、代理、防关联等产品叙事 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑隐藏真实目的地、向 Google 和用户展示不同内容、多账号规避和规避政策执行的风险边界 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑 arbitrage、桥页、低价值目的地、cloaking 和广告网络滥用语境 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目的地体验、页面可达性和广告承诺一致性要求 |
| Google Ads, Secure your Google Ads account | https://support.google.com/google-ads/answer/2375456 | 支撑账号安全、2-Step Verification、访问审计和 Cookie theft 风险语境 |
| Google Ads, Confirm it is you | https://support.google.com/google-ads/answer/12865189 | 支撑敏感或异常场景下的确认身份和安全挑战逻辑 |
| Google Ads, About access levels | https://support.google.com/google-ads/answer/9978556 | 支撑用账号访问级别和权限模型协作，而不是共享登录态 |
| Google Ads API, OAuth overview | https://developers.google.com/google-ads/api/docs/oauth/overview | 支撑 API 通过 OAuth 授权，不需要处理用户后台登录 Cookie |
| Google Ads Scripts, Authorization | https://developers.google.com/google-ads/scripts/docs/authorization | 支撑 Scripts 是授权执行通道，需要用户确认和权限范围 |
| Google Ads Editor, Prepare a CSV file | https://support.google.com/google-ads/editor/answer/56368 | 支撑 CSV / Editor 作为人工审核型批量变更方式 |
| MDN, Using HTTP cookies | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies | 支撑 Cookie 是 HTTP 状态和会话管理机制 |
| OWASP Session Management Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | 支撑 Session ID / Token 是敏感凭据，需要安全生命周期和存储保护 |
| OWASP Multifactor Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | 支撑 MFA 因子、恢复流程和不可弱化第二因素的治理 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑人为抬高广告主成本或发布商收入的点击和展示属于无效流量风险 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑禁止自动点击、自动浏览、鼓励点击、付费点击等行为 |
| AdSense, How Google prevents invalid traffic | https://support.google.com/adsense/answer/1348752 | 支撑 Google 使用自动系统和人工审核过滤无效活动 |
| EFF, Cover Your Tracks | https://coveryourtracks.eff.org/learn | 支撑浏览器指纹由多种环境信号组合而成，可用于识别或跟踪 |
| W3C TAG, Unsanctioned Web Tracking | https://www.w3.org/2001/tag/doc/unsanctioned-tracking/ | 支撑未经同意的指纹和追踪带来的隐私与治理风险 |
| Cloudflare Workers documentation | https://developers.cloudflare.com/workers/ | 支撑 Worker / Edge Function 的中性用途：边缘执行、缓存、路由、安全和性能 |
| Google Ads, Fix a suspended account | https://support.google.com/google-ads/answer/2375414 | 支撑账号暂停后的修复、申诉和原因复盘路径 |

