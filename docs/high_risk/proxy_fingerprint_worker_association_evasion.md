# 代理、指纹、Worker 转发规避关联检测研究

更新时间：2026-06-09

## 1. 范围

本文研究代理、浏览器指纹和 Worker 转发在“规避关联检测”语境下的原理、风险和合规替代方案。本文不提供代理池搭建、指纹伪装、反检测浏览器配置、Worker 转发规避或账号隔离绕过实现。

## 2. 原理解释

### 2.1 代理

代理改变请求的网络出口。不同代理会呈现不同 IP、ASN、地理位置、延迟和网络信誉。代理本身可用于企业网络、测试地区可用性或安全网关，但用于隐藏真实操作者或绕过平台限制时风险很高。

### 2.2 浏览器指纹

浏览器指纹是由多种环境信号组合形成的识别特征，例如：

- User-Agent 和 Client Hints。
- 时区、语言、屏幕尺寸。
- 字体、Canvas、WebGL。
- 音频、硬件并发、设备内存。
- 插件、存储、权限状态。

指纹技术既可用于反欺诈，也可用于跨站跟踪。试图伪装或频繁切换指纹来规避检测，会进入对抗平台风控的语境。

### 2.3 Worker 转发

Cloudflare Workers 等边缘函数可以在边缘节点执行代码，处理请求、缓存、API 网关、A/B 测试等。技术本身中性。风险在于把它用作隐藏真实服务、拆分请求来源、绕过审核或规避账号关联的中转层。

### 2.4 关联图谱原理

平台关联检测通常不是“一个 IP 等于一个账号”这种单点规则，而是图谱问题。一个账号、域名、Offer、支付方式、素材、关键词、落地页、追踪模板、MCC、用户权限、操作节奏和历史违规都会形成边。代理、指纹和 Worker 只改变其中一小部分技术边，不会改变业务边。

常见关联层：

- 主体层：公司、个人、付款资料、税务资料、合同、广告主验证资料。
- 账号层：MCC、用户权限、邀请历史、管理关系、账号创建和操作节奏。
- 资产层：域名、落地页、Offer、品牌、页面模板、素材、关键词、tracking template。
- 流量层：来源、地理、设备、时段、转化质量、扣量和投诉。
- 基础设施层：IP、ASN、DNS、CDN、Worker、服务器、浏览器和设备信号。

所以“换 IP/换指纹/加 Worker”如果没有真实业务隔离，只是在技术层遮盖业务层重复。它不能把同一类违规 Offer、同一套页面、同一批素材和同一个付款主体变成独立合规业务。

### 2.5 合法隔离和规避关联的边界

| 用途 | 可接受方向 | 高风险方向 |
| --- | --- | --- |
| 地区测试 | 检查页面是否可访问、语言/价格是否正确 | 伪装账号运营地区或规避地区限制 |
| 企业网络 | 安全网关、访问日志、公司统一出口 | 用代理池隐藏真实操作者 |
| 边缘 Worker | 缓存、API 网关、性能优化、透明 A/B | 隐藏最终目的地、拆分审核路径、规避关联 |
| 浏览器环境 | 内部 QA 覆盖不同设备 | 伪造指纹让多个账号看起来无关 |

系统设计上，任何无法说明真实业务目的、只强调“防关联”“不被识别”“隔离封禁”的需求，都应进入风险审计，而不是进入执行排期。

### 2.6 关联资产图谱

关联风险不是“技术环境是否相同”的单点问题，而是业务、账号、资产、资金、流量和执行证据组成的图谱：

```text
business_entity
  -> manager_account / ads_account
  -> payment_profile / advertiser_verification
  -> domain / landing_page / offer
  -> tracking_template / final_url / worker_or_cdn
  -> creative / keyword / audience / campaign_structure
  -> traffic_source / publisher / placement / subid
  -> conversion / revenue / complaint / policy_event
  -> operator / access_user / change_history
```

| 图谱层 | 典型证据 | 合法隔离需要证明 |
| --- | --- | --- |
| 业务主体 | 公司、合同、税务、广告主验证 | 不同客户、不同品牌、不同法律关系 |
| 账号关系 | MCC、用户权限、邀请历史、Change history | 独立负责人、权限最小化、可审计管理 |
| 支付和结算 | payment profile、发票、收款路径 | 真实付款责任和结算边界 |
| 域名和页面 | domain、WHOIS/registrar、模板、内容 | 独立站点目的、原创内容、真实产品 |
| Offer 和素材 | payout、buyer、creative claim、关键词 | 不重复违规 Offer 或误导素材 |
| 追踪链路 | final URL、tracking template、redirect hops | 链路透明、一致、可解释 |
| 流量质量 | source、placement、geo、device、deduction | 可解释真实来源和停源机制 |
| 操作行为 | 操作人、时间、工具、审批 | 不共享账号、不隐藏操作者 |

如果无法在业务主体、Offer、页面、资金和操作责任上证明独立，只靠代理、指纹或 Worker 改变基础设施层，通常不能构成合规隔离。

### 2.7 供应商红旗话术

以下话术应默认进入 high risk：

| 话术 | 风险解释 | 系统动作 |
| --- | --- | --- |
| 防关联、养号、过风控 | 明确以规避检测为目的 | 拒绝执行，建风险审计 |
| 独享指纹、环境隔离、批量开账号 | 可能规避账号限制或责任归属 | 账号健康复盘 |
| Worker 隐藏真实落地页 | 可能隐藏目的地或 cloaking | 链路 QA 和政策审计 |
| 封号后快速切换环境继续跑 | 规避封禁和原问题修复 | 停止，走申诉和修复 |
| 真人环境模拟、设备池 | 对抗平台识别和无效流量检测 | 供应商拉黑或尽调 |
| 代理池不限量、低价全球 IP | 流量/账号质量和安全风险 | 禁止接入账号后台 |

供应商如果不能提供合法用途、合同主体、数据处理边界、日志、停用机制和不规避平台政策承诺，不应进入执行链路。

### 2.8 Worker / Edge 的安全使用边界

Worker、CDN、反向代理和边缘函数的安全用途通常是：

- 缓存静态资源，降低延迟。
- API 网关、鉴权、rate limit、日志和可观测性。
- A/B 测试，但用户和审核看到的业务承诺一致。
- 地区化内容，但不改变 offer identity、policy disclosure 或最终目的地。
- 安全 header、bot 防护和故障兜底。

高风险用途包括：

- 按 AdsBot、IP、User-Agent、Cookie、指纹或账号状态切换页面。
- 隐藏真实 Final URL、Offer、跳转链或广告主身份。
- 把同一违规页面包装成多个看似无关的入口。
- 为封禁后换域名、换账号或换路径继续相同问题。

本系统可以记录 Worker 用途说明和 URL QA 结果，但不保存 Worker 转发脚本、分流规则、隐藏链路或规避关联配置。

## 3. 行业诉求

投放团队可能希望：

- 多账号看起来互不相关。
- 不同账号使用不同网络出口。
- 隔离脚本同步和后台操作。
- 避免封禁后的关联处置。
- 让审核、用户、平台看到不同路径。

这些诉求大多不是正常业务隔离，而是对抗性规避。

## 4. 风险

| 风险 | 说明 |
| --- | --- |
| 规避系统 | 目的若是隐藏关联或绕过限制，容易触及平台红线 |
| 资产扩大受损 | 多账号、域名、付款方式可能被统一关联 |
| 供应商风险 | 代理和指纹工具可能接触敏感账号环境 |
| 数据质量下降 | 真实归因、审计和排错复杂化 |
| 稳定性差 | IP 信誉、Worker 路由、指纹一致性都会影响投放 |

## 5. 平台识别逻辑

关联检测通常不靠单一信号，而是多维组合：

- 账号资料。
- 付款资料。
- MCC 或管理关系。
- 域名、落地页、追踪参数。
- 素材、关键词、预算和操作节奏。
- 网络出口、设备和浏览器信号。
- 历史封禁和新账号行为相似度。

因此，仅改变 IP 或指纹通常无法消除业务层关联。

系统里不需要也不应该沉淀平台检测细节或规避参数。治理重点是“我们自己的业务是否能被真实解释”：

| 问题 | 合规回答 |
| --- | --- |
| 为什么有多个账号？ | 不同客户、品牌、地区、产品线或合同边界 |
| 为什么有不同域名？ | 不同站点目的、内容体系、用户任务和品牌 |
| 为什么使用 CDN / Worker？ | 性能、安全、缓存、日志、API 网关或透明实验 |
| 为什么使用不同网络出口？ | 企业网络、员工地点、合规测试或访问控制 |
| 谁操作了变更？ | 独立用户权限、审批记录、Change history |
| 出现限制后做了什么？ | 修复原因、申诉证据、停止问题来源，而不是切换环境继续跑 |

## 6. 合规替代方案

- 使用 MCC 和官方权限管理。
- 按真实客户、品牌、产品线隔离账号。
- 使用独立付款、合同、域名和内容资产，且保持真实业务关系。
- 用 Google Ads Scripts/API/CSV 做可审计同步。
- 建立账号健康评分和风险复盘。
- 不把代理、指纹、Worker 作为规避检测工具。

合法隔离证据包：

| 证据 | 用途 |
| --- | --- |
| business_owner | 证明账号归属和负责人 |
| advertiser_verification_status | 证明主体和广告主身份 |
| manager_account_relation | 证明 MCC / agency 管理边界 |
| payment_profile_reference | 证明付款责任和结算主体 |
| domain_owner_and_purpose | 证明域名、品牌和页面目的 |
| offer_contract_or_buyer_terms | 证明推广对象和付费定义 |
| creative_and_claim_review | 证明素材没有重复误导或规避 |
| link_chain_qa | 证明 Final URL、tracking 和 Worker 链路一致 |
| source_quality_history | 证明流量来源真实可解释 |
| incident_and_appeal_record | 证明受限后先修复和申诉 |

## 7. 本系统落地

系统支持：

- 账号配置记录。
- 同步方式记录。
- 审计日志。
- URL 和 Campaign 导出记录。
- `/risk-audits` 记录关联风险、供应商红旗、处理方案和来源 URL。
- `/links` 记录真实候选 URL、人工确认和版本日志，不做隐藏链路。
- `/sources` 保存 EFF、W3C、Cloudflare、Google Ads 政策和账号治理来源。

系统不支持：

- 代理供应商配置。
- 指纹浏览器配置。
- Worker 转发脚本。
- 规避关联检测策略。
- 反检测浏览器 profile。
- Worker / CDN 分流规则。
- 为规避封禁的账号切换任务。

建议后续扩展实体表：

| 表 | 用途 | 禁止字段 |
| --- | --- | --- |
| `association_risk_reviews` | account、domain、offer、payment、operator、risk score | proxy endpoint、fingerprint profile |
| `business_isolation_evidence` | customer、brand、contract、domain purpose、owner | 伪造主体或虚假合同 |
| `edge_usage_reviews` | Worker/CDN 用途、cache、安全、QA evidence | bot split、hidden final URL |
| `vendor_red_flag_reviews` | supplier claim、contract、data access、decision | 防关联配置、账号环境包 |
| `account_recovery_cases` | restriction、root cause、fix、appeal evidence | ban evasion account map |

## 8. ADXKit 对应点和完成形态

ADXKit 公开页面提到代理管理、随机指纹、独立 Script、Worker 转发、防关联等能力。套利团队关注这些点，通常是因为账号、域名、素材、付款资料、落地页和操作环境之间存在关联风险。但如果目标是“让平台看不出同一业务或同一操作者”，就进入对抗性规避场景。

需要区分三类正常用途：

- 地区可用性测试：确认页面在目标国家能否打开、语言和价格是否正确。
- 企业安全网关：公司统一出口、访问控制、日志审计。
- 边缘服务：缓存、API 网关、A/B 测试、性能优化。

和三类高风险用途：

- 为封禁后继续投放而隔离账号关联。
- 伪装操作来源、设备、浏览器环境或真实业务主体。
- 让审核、用户、广告平台、联盟平台看到不同路径或不同内容。

本项目完成形态：

- 记录账号、域名、Offer、Campaign、链接计划和审计日志，方便复盘真实关联。
- 允许在文档中解释代理、指纹、Worker 的中性技术原理。
- 允许把“用途不清的代理/Worker/指纹需求”写入风险审计。
- 不保存代理供应商、指纹配置、Worker 转发脚本或规避关联策略。

验收标准：

- 数据库没有代理池、指纹 profile、Worker 路由规则等执行表。
- `/sources` 可记录 EFF、W3C、Cloudflare、Google Ads 政策来源。
- `/risk-audits` 可把“规避关联检测”标为 high 并写处理方案。
- 链接计划只做同主题已审核 URL 维护，不做链路隐藏。

## 9. 功能拆解和安全完成清单

把“代理、指纹、Worker 防关联”拆成业务诉求后，可安全交付的是关联风险复盘和真实业务隔离说明，而不是规避工具：

| 子能力 | 行业想解决的问题 | 本项目安全完成形态 |
| --- | --- | --- |
| 关联资产盘点 | 看清账号、域名、Offer、素材、付款和追踪之间的关系 | 账号、Offer、Campaign、链接和审计日志形成可复盘记录 |
| 地区可用性检查 | 确认页面在目标国家可打开、语言价格正确 | 文档说明只做 QA，不把代理作为账号运营伪装 |
| 边缘服务解释 | Worker 可用于缓存、API 网关、A/B 或性能 | 文档解释中性用途，不保存 Worker 规避路由 |
| 账号治理 | 多客户、多品牌、多产品线需要真实隔离 | MCC、权限、负责人、同步方式和风险审计 |
| 事故复盘 | 账号受限后查清业务层重复问题 | `/risk-audits` 记录风险、证据、处理方案和来源 URL |

安全验收点：

- 数据库不包含代理供应商 API key、代理池、IP 轮换、指纹 profile、反检测浏览器 profile 或 Worker 分流规则。
- 对“防关联”的需求必须记录真实业务原因：不同客户、不同品牌、不同合同、不同域名或不同负责人。
- 如果需求只表达“不被平台识别”“封禁后继续跑”“隐藏真实主体”，应标记为 high。
- 合法 QA 可以记录页面可用性问题，但不得把代理、指纹或 Worker 用于账号运营伪装。
- 链接计划和投放草稿必须能解释最终目的地和业务主体，不依赖隐藏中转。

### 9.1 审计字段设计

| 字段 | 说明 |
| --- | --- |
| capability | 固定为 `proxy_fingerprint_worker_association_evasion` |
| trigger | proxy vendor、fingerprint browser、Worker forwarding、anti-association claim、account restriction |
| asset_scope | account、MCC、domain、offer、payment、operator、tracking URL |
| stated_purpose | 地区 QA、企业网关、性能、缓存、安全、A/B、账号隔离、防关联 |
| legitimate_evidence | 合同、品牌、客户、域名目的、Worker 用途、QA 证据 |
| red_flags | 防关联、隐藏主体、封禁后继续跑、代理池、指纹 profile、审核分流 |
| safe_path | access governance、link QA、business isolation evidence、account health SOP |
| decision | rejected、info_only、qa_only、manual_review、incident_response |
| evidence_url | Google Ads policy、EFF、W3C、Cloudflare、access levels 来源 |
| reviewer | 审核人 |
| follow_up | 停用供应商、清理账号权限、修复页面、申诉、更新风险矩阵 |

### 9.2 Association Risk Score

建议把“是否需要隔离”改成“是否能证明真实隔离”：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| Business identity clarity | 25 | 客户、品牌、合同、广告主验证是否清楚 |
| Offer and landing independence | 20 | Offer、页面、素材、claim 是否真实独立 |
| Payment and account governance | 20 | 付款、MCC、用户权限和责任边界 |
| Link chain transparency | 15 | Final URL、tracking、Worker/CDN 是否透明一致 |
| Source and revenue quality | 10 | 流量来源、扣量、投诉、paid revenue |
| Incident history | 10 | 是否有封禁、拒登、重复规避记录 |

低分不是去买代理或换指纹，而是暂停、补证据、修业务、申诉或拒绝。

### 9.3 SOP

1. 看到“防关联”“指纹浏览器”“Worker 转发”“代理池”等需求，先记录为风险审计。
2. 询问真实业务目的：地区 QA、企业安全、性能，还是账号规避。
3. 盘点 account、MCC、domain、offer、payment、operator、tracking、source、complaint 的关联图谱。
4. 如果是合法 QA / 安全 / 性能用途，只允许保存目的、证据、URL QA 和负责人。
5. 如果目的是隐藏主体、封禁后继续跑、审核分流或规避检测，拒绝进入执行。
6. 对账号受限场景，进入账号健康 SOP：查原因、修复、申诉、停止问题来源。
7. 把供应商话术、来源 URL、处理方案和 reviewer 写入 `/risk-audits`。

### 9.4 通过/拒绝例子

| 需求 | 判断 | 处理 |
| --- | --- | --- |
| 用 CDN 缓存图片和静态 JS | 可通过 | 记录性能用途和 QA |
| 用 Worker 做透明 API 网关和 rate limit | 可通过 | 保存用途、域名和日志说明 |
| 用代理检查目标国家页面是否加载 | 只限 QA | 不用于账号登录和投放操作 |
| 用指纹浏览器管理多个受限账号 | 拒绝 | 账号健康审计和申诉 |
| 用 Worker 对审核和用户展示不同页面 | 拒绝 | 转 cloaking 风险 |
| 封禁后换代理、换指纹、换账号继续同 Offer | 拒绝 | 转封禁规避风险 |

## 10. 信息来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Cloudflare Workers documentation | https://developers.cloudflare.com/workers/ | 支撑 Workers 是边缘 serverless 平台，可用于 API、缓存、任务和边缘逻辑 |
| EFF Cover Your Tracks, browser fingerprinting | https://coveryourtracks.eff.org/learn | 支撑浏览器指纹由多种环境信号组合而成，可用于识别或跟踪 |
| W3C TAG, Unsanctioned Web Tracking | https://www.w3.org/2001/tag/doc/unsanctioned-tracking/ | 支撑指纹和非授权追踪的隐私与治理风险 |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑隐藏真实目的地、规避政策执行、向 Google 和用户展示不同内容等红线 |
| Google Ads Policy, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑桥页、网关页、低价值目的地、广告网络滥用和隐藏链路风险 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑最终 URL、页面可达、目的地体验和广告承诺一致性 |
| Google Ads Help, About access levels in your Google Ads account | https://support.google.com/google-ads/answer/9978556 | 支撑通过访问级别和用户权限协作，而不是共享环境或隐藏操作者 |
| Google Ads Help, Fix a suspended Google Ads account | https://support.google.com/google-ads/answer/2375414 | 支撑受限后应修复问题和申诉，而不是切换环境继续投放 |
| Google Search Central, Spam policies | https://developers.google.com/search/docs/essentials/spam-policies | 支撑隐藏重定向、cloaking、低价值页面等跨 Google 生态的内容风险背景 |
