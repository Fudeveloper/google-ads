# 高风险能力研究与合规替代方案

更新时间：2026-06-08

本文逐点研究以下 6 类能力：

1. Ads Cookie 登录和后台操作。
2. 自动绕过登录、2FA、安全挑战。
3. 补点击、刷展示、模拟自然流量。
4. 使用代理、指纹、Worker 转发来规避关联检测。
5. Cloaking 或审核页/用户页不一致。
6. 为规避封禁创建或切换账号。

说明：本文只做原理、风险、政策、识别逻辑和合规替代方案说明，不提供可执行绕过步骤、代码、Cookie 复用方法、刷量实现、cloaking 实现或规避封禁流程。

独立专题文档：

- [Ads Cookie 登录和后台操作](high_risk/ads_cookie_backend_operation.md)
- [自动绕过登录、2FA、安全挑战](high_risk/automated_login_2fa_challenge_bypass.md)
- [补点击、刷展示、模拟自然流量](high_risk/invalid_traffic_click_impression_simulation.md)
- [代理、指纹、Worker 转发规避关联检测](high_risk/proxy_fingerprint_worker_association_evasion.md)
- [Cloaking 或审核页/用户页不一致](high_risk/cloaking_review_user_page_mismatch.md)
- [为规避封禁创建或切换账号](high_risk/ban_evasion_account_switching.md)

## 1. Ads Cookie 登录和后台操作

### 1.1 原理

Cookie 是浏览器和服务器之间保存状态的机制。用户登录 Google Ads 后，浏览器会持有登录态相关 Cookie 或会话凭据；后续请求通过这些凭据让服务器识别用户身份。Cookie 常见安全属性包括 `Secure`、`HttpOnly`、`SameSite`，它们用于降低明文传输、脚本读取和跨站请求风险。

所谓“用 Ads Cookie 操作后台”，本质是把浏览器登录态当作自动化凭据使用，让脚本、服务端程序或自动化浏览器以该用户身份访问 Google Ads 后台。这和正常网页登录不同，因为它通常绕开了明确授权、OAuth 范围、审计和 API 配额模型。

### 1.2 行业诉求

投放团队想用 Cookie 操作后台，常见原因是：

- 不想申请 Google Ads API。
- 觉得官方 API 审批慢。
- 想复用已经登录的账号。
- 想用 UI 自动化覆盖 API 没开放或难用的功能。
- 想批量管理多个账号。

### 1.3 主要风险

- 会话凭据泄露后等同于账号被接管。
- 自动化程序可能触发安全挑战、账号锁定或异常登录。
- 无法清晰表达授权范围和最小权限。
- 很难做可靠审计：谁在什么时候以哪个账号执行了什么动作。
- 违反平台安全预期，容易和 cookie theft、未授权访问、绕过登录保护混在一起。

### 1.4 平台和安全视角

Google Ads 的账号安全文档把安全挑战用于保护账号免受 cookie theft 等风险；Google 也建议使用强密码、2-Step Verification、最小权限和账号访问管理。MDN 对 Cookie 的说明也强调 Cookie 常用于会话管理，安全属性是为了保护会话。

### 1.5 识别和风控逻辑

平台通常不会只看单个 Cookie，而会综合：

- 登录设备和地理位置。
- 浏览器、系统和网络环境变化。
- 请求频率、路径和时序。
- 是否有异常批量操作。
- 是否绕过正常 UI 交互路径。
- 是否出现会话被复制到不同环境的迹象。

这些信号的目的不是阻止正常用户，而是识别会话滥用和账号接管风险。

### 1.6 合规替代方案

本系统采用：

- Google Ads Editor CSV 导出。
- Google Ads Scripts JSON payload。
- 官方 Google Ads API 作为后续扩展。
- 人工审核和审计日志。
- 不保存 Cookie、浏览器 Profile、Session Token。

### 1.7 系统落地

已经落地：

- `ads_accounts` 表记录账号配置和同步方式。
- Campaign 支持 CSV 导出。
- Campaign 支持 Scripts JSON 导出。
- `audit_logs` 记录导出动作。
- 页面明确显示 `No Cookie Automation`。

## 2. 自动绕过登录、2FA、安全挑战

### 2.1 原理

登录、2FA 和安全挑战是认证链路的一部分：

- 密码证明用户知道凭据。
- 2FA 证明用户同时持有第二因素，例如手机、硬件密钥或验证码。
- 安全挑战用于检测异常登录、Cookie 盗用、设备异常或高风险操作。

“自动绕过”通常意味着试图让脚本通过、规避或消除这些保护。这不是普通自动化，而是对账号保护机制的对抗。

### 2.2 行业诉求

常见诉求：

- 多账号批量登录。
- 减少人工处理安全挑战。
- 避免频繁 2FA。
- 在服务器或远程环境中长期保持登录。

### 2.3 主要风险

- 触及账号接管、未授权访问或安全机制规避。
- 可能导致账号锁定或访问权限收紧。
- 破坏团队内部责任边界：无法证明动作由真实授权人员执行。
- 对企业账号而言，会放大内部人员和外包团队风险。

### 2.4 平台和安全视角

Google Ads 安全建议包括启用 2-Step Verification、定期检查访问权限、管理用户角色、及时移除不需要的访问。安全挑战存在的目的就是保护账号，而不是需要被自动绕过的障碍。

### 2.5 合规替代方案

- 使用账号权限管理，而不是共享登录态。
- 使用官方 OAuth/API 授权，而不是保存登录会话。
- 把需要人工确认的动作设计为审核队列。
- 使用 Google Ads Scripts 在账号内由授权用户安装执行。
- 将高风险操作写入审计日志。

### 2.6 系统落地

当前系统把“执行”设计为：

```text
投放草稿 -> 人工审核 -> CSV / Script JSON 导出 -> 授权人员执行 -> 指标导入 -> 审计
```

这样保留效率，同时不尝试绕过登录或安全挑战。

## 3. 补点击、刷展示、模拟自然流量

### 3.1 原理

广告系统通常把点击、展示、会话、转化作为计费或质量评估信号。补点击或刷展示是人为制造或诱导这些信号，使广告主成本或发布商收入被抬高。

所谓“模拟自然流量”常见做法是试图伪造：

- 来源站点。
- IP 地区。
- 浏览器环境。
- 停留和滚动行为。
- 点击时间分布。
- 设备比例。

本文不提供这些实现方法。

### 3.2 行业诉求

在套利场景里，团队可能想通过补点击：

- 让联盟或广告平台数据看起来更自然。
- 弥补追踪断点。
- 拉高页面互动。
- 维持某些平台的流量比例。

这些诉求不能改变其本质风险：它会制造不真实的广告互动。

### 3.3 平台政策

Google AdSense 对 invalid traffic 的定义包括可能人为抬高广告主成本或发布商收入的点击和曝光。AdSense Program policies 禁止发布商点击自己的广告、鼓励他人点击、使用自动化点击工具、paid-to-click、paid-to-surf、autosurf、click-exchange 等流量来源。

### 3.4 识别和风控逻辑

平台会综合识别：

- 点击和展示时序异常。
- 地理位置、时区和语言不一致。
- 用户行为路径过于机械。
- 来源和转化质量不匹配。
- 高点击低停留或无转化。
- 供应商流量长期扣量。
- 设备、浏览器、IP、ASN 或 Referer 分布异常。

### 3.5 合规替代方案

- 只购买真实、有明确来源的用户流量。
- 用 UTM、SubID、GA4、服务端日志修复归因。
- 追踪断点用数据修复流程，不用补点击。
- 用页面质量、内容相关性和素材匹配提高真实互动。
- 对异常来源暂停、隔离、拉黑。

### 3.6 系统落地

系统实现的是：

- 指标导入。
- ROI/RPV/CPC 计算。
- 异常来源优化建议。
- 审计日志。

系统不实现点击任务、展示任务、自动浏览任务或自然流量模拟器。

## 4. 代理、指纹、Worker 转发用于规避关联检测

### 4.1 原理

代理改变网络出口；浏览器指纹来自设备、浏览器、字体、Canvas、WebGL、时区、语言、屏幕、插件等信号；Worker 或边缘函数可以作为请求中转层，改变请求路径或部署位置。

这些技术本身并不天然违规：

- 代理可以用于企业网络、测试不同地区可用性。
- 指纹研究可以用于隐私保护和反欺诈。
- Cloudflare Workers 可以用于边缘计算、缓存、A/B 测试和 API 网关。

风险出现在用途：如果目的是规避平台关联检测、封禁、审核或安全系统，就进入对抗性规避。

### 4.2 行业诉求

投放团队可能想用这些技术：

- 隔离多个账号。
- 避免被识别为同一操作者。
- 改变地区或出口。
- 分散脚本或接口调用来源。
- 绕过封禁后的关联判断。

### 4.3 主要风险

- 被归类为规避系统或规避封禁。
- 账号资产被统一处置。
- 供应商和外包人员掌握敏感访问路径。
- 排错困难，真实归因和审计变差。
- 一旦策略失败，影响范围可能比单账号更大。

### 4.4 识别和风控逻辑

平台和反欺诈系统通常看多维关联：

- 账号信息、付款资料、域名、站点、落地页。
- 网络出口、ASN、代理质量。
- 设备和浏览器信号。
- 操作时序、批量模式。
- 素材、关键词、URL、追踪参数相似性。
- 历史封禁和新账号行为相似度。

单纯换 IP 或换指纹，不能真正消除业务层关联。

### 4.5 合规替代方案

- 用官方 MCC、用户权限和角色管理多账号。
- 做真实业务隔离：不同客户、不同域名、不同结算、不同团队职责。
- 记录账号用途、负责人、权限和执行日志。
- 用 Scripts/API/CSV 的明确授权方式同步。
- 对账号健康做预警，不做对抗性规避。

### 4.6 系统落地

系统只记录：

- 账号配置。
- 同步方式。
- 审计日志。

不实现代理池、指纹池、Worker 转发规避、账号关联绕过。

## 5. Cloaking 或审核页/用户页不一致

### 5.1 原理

Cloaking 是根据访问者身份、设备、地区、User-Agent、IP、Cookie 或其他信号，向不同访问者展示不同内容。例如审核系统看到合规页面，真实用户看到另一个页面。

Google Search Central 将 cloaking 定义为向用户和搜索引擎展示不同内容的做法；Google Ads 的 Advertising network abuse 政策也把 cloaking、bridge/gateway 目的地、试图规避审核系统列为问题。

### 5.2 行业诉求

套利团队可能想用 cloaking：

- 提高审核通过率。
- 隐藏真实 Offer。
- 对不同地区或设备展示不同变现页面。
- 在审核后切换到更激进页面。

### 5.3 主要风险

- 属于高风险平台规避行为。
- 可能导致广告拒登、账号限制或封禁。
- 影响域名、支付资料、团队账号的长期可信度。
- 与用户承诺不一致，会造成投诉和低质量流量。

### 5.4 识别和风控逻辑

平台可以从多个角度检测：

- 多地区、多设备、多 User-Agent 抓取。
- 审核后持续复查。
- 用户投诉和行为异常。
- 最终 URL 和中间跳转链路变化。
- 页面内容、广告承诺和变现目标不一致。
- JavaScript 或服务端规则导致内容分歧。

### 5.5 合规替代方案

- 只做透明 A/B 测试，且广告承诺一致。
- 最终 URL、展示 URL、页面主题保持一致。
- 链接轮换只用于断链修复、UTM 更新、已审核同主题页面测试。
- 每次 URL 变化记录原因和审核人。
- 对页面版本做可追溯归档。

### 5.6 系统落地

系统实现：

- 链接计划。
- 候选 URL 记录。
- 人工确认轮换。
- 审计日志。

系统不实现按审核 Bot、地区、设备、IP 或指纹展示不同页面。

## 6. 为规避封禁创建或切换账号

### 6.1 原理

平台封禁或限制通常不是只针对某个登录账号，而可能关联：

- 业务主体。
- 付款方式。
- 域名和落地页。
- 素材和关键词。
- 操作人员。
- 设备、网络和行为模式。
- 历史违规模式。

因此，为规避封禁而创建或切换账号，本质是试图绕过平台处置，而不是解决原始违规或质量问题。

### 6.2 行业诉求

常见诉求：

- 账号受限后继续投放。
- 避免停机损失。
- 将高风险 Offer 分散到多个账号。
- 保留主账号健康度。

### 6.3 主要风险

- 新账号被快速关联和限制。
- 付款主体、域名、团队资产受牵连。
- 复盘被跳过，原始违规继续扩大。
- 业务不可持续，现金流和账号资产风险增大。

### 6.4 平台视角

Google Ads 政策中的 circumventing systems 和 advertising network abuse，核心就是防止广告主绕过审核、限制或平台执行机制。封禁后换账号规避处置，通常会被视为规避系统。

### 6.5 合规替代方案

- 先暂停投放，定位原因。
- 检查政策、页面、素材、付款、追踪、流量来源。
- 使用官方申诉流程。
- 保留修复证据和变更记录。
- 建立账号健康清单，避免重复违规。
- 正常多账号管理使用 MCC 和权限，而不是规避封禁。

### 6.6 系统落地

系统可以支持：

- 账号配置记录。
- 账号状态备注。
- 审计日志。
- 风险复盘文档。

系统不支持：

- 封禁后自动切换账号。
- 新账号批量创建。
- 规避关联检测。
- 为绕过政策限制迁移投放。

## 7. 汇总表

| 能力 | 技术本质 | ADXKit 对应公开能力 | 主要风险 | 合规替代 |
| --- | --- | --- | --- | --- |
| Ads Cookie 操作后台 | 复用浏览器会话凭据 | 无需 API、少登录后台 | 账号接管、未授权访问、审计缺失 | CSV、Scripts、官方 API、人工审核 |
| 绕过 2FA/安全挑战 | 对抗认证保护 | 自动任务、批量执行 | 安全机制规避、账号锁定 | OAuth、权限管理、人工确认 |
| 补点击/刷展示 | 制造广告计费或质量信号 | 补点击算法、模拟自然流量 | 无效流量、扣量、封禁 | 真实流量、归因修复、来源隔离 |
| 代理/指纹/Worker 规避 | 改变网络和设备表征 | 代理、随机指纹、Worker、防关联 | 规避系统、资产关联处置 | MCC、真实隔离、审计 |
| Cloaking | 向审核和用户展示不同内容 | 换链接、最终到达页采集、中转层 | 审核规避、账号限制 | 一致页面、透明 A/B、版本记录 |
| 规避封禁换号 | 绕过平台处置 | 多账号管理、防关联、独立 Script | 快速关联、资产扩大受损 | 原因修复、申诉、健康清单 |

逐点完成矩阵见 [高风险能力专题索引](high_risk/README.md)。结构化来源索引见 [Ads 套利研究来源库](source_library.md)，系统页面为 `/sources`。

## 8. 资料来源 URL

- Google Ads policies, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads policies, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Secure your Google Ads account: https://support.google.com/google-ads/answer/2375456
- Google AdSense Program policies: https://support.google.com/adsense/answer/48182
- Definition of invalid traffic: https://support.google.com/adsense/answer/16737
- Use of online advertising to get new users to the site: https://support.google.com/adsense/answer/1348727
- How Google prevents invalid traffic: https://support.google.com/adsense/answer/1348752
- Google Search Central spam policies, cloaking: https://developers.google.com/search/docs/essentials/spam-policies
- Google Ads Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads account access levels: https://support.google.com/google-ads/answer/9978556
- Fix a suspended Google Ads account: https://support.google.com/google-ads/answer/2375414
- Google Ads API OAuth overview: https://developers.google.com/google-ads/api/docs/oauth/overview
- Google Ads Scripts authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- MDN, HTTP cookies: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
- MDN, Set-Cookie header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
- Cloudflare Workers documentation: https://developers.cloudflare.com/workers/
- EFF Cover Your Tracks, browser fingerprinting: https://coveryourtracks.eff.org/learn
- W3C TAG, Unsanctioned Web Tracking: https://www.w3.org/2001/tag/doc/unsanctioned-tracking/
- ADXKit homepage: https://adxkit.com/
