# 为规避封禁创建或切换账号研究

更新时间：2026-06-09

## 1. 范围

本文研究为规避封禁、限制或审核处置而创建/切换账号的原理、风险和合规替代方案。本文不提供新账号批量创建、规避关联、付款资料规避、域名迁移规避或封禁后继续投放的操作流程。

## 2. 原理解释

平台的账号限制通常不是只针对登录名。平台可能同时关注：

- 广告主主体。
- MCC 管理关系。
- 付款资料。
- 域名和落地页。
- 素材、关键词、追踪模板。
- 业务模式和 Offer。
- 操作人员、设备和网络环境。
- 历史违规模式。

因此，封禁后换账号如果目的是继续相同违规或规避处置，本质是规避平台执行机制。

### 2.1 账号不是孤立资产

在广告平台视角，账号是业务图谱中的一个节点，而不是唯一对象。一次暂停或限制通常指向某个可修复问题：页面不一致、误导承诺、受限垂类无认证、付款异常、无效流量、身份验证问题、重复违规或规避系统。换账号如果没有修复问题，只是把同一个问题移动到新节点。

套利团队需要把“账号资产”分成三层：

- 经营主体：公司、合同、付款、税务、广告主验证、客户关系。
- 投放资产：域名、落地页、Offer、素材、关键词、追踪模板、转化事件。
- 执行资产：账号、MCC、用户、权限、脚本、导入记录、审计日志。

封禁治理应该从前两层找原因，再决定第三层如何恢复，而不是只在执行层换账号。

### 2.2 正常多账号管理 vs 规避封禁

| 维度 | 正常多账号管理 | 规避封禁换号 |
| --- | --- | --- |
| 业务原因 | 不同客户、品牌、地区、预算或合同 | 原账号受限后继续跑同一问题 |
| 资产隔离 | 真实主体、域名、页面、付款和权限清楚 | 共享违规页面、素材、Offer 或付款线索 |
| 处置方式 | 拒登后修复、申诉、记录复盘 | 不修复原因，迁移到新账号 |
| 审计证据 | 有负责人、变更记录、政策来源和修复证据 | 重点是“不断号”“快速恢复”“防关联” |

正常多账号不是问题，问题在于账号切换是否用于绕过平台已经做出的限制或政策执行。

### 2.3 恢复流程的原理

合规恢复的目标不是“让广告重新跑起来”，而是让平台和内部团队都能确认原始风险已降低：

1. 冻结相关投放和链接变更，防止问题扩散。
2. 收集拒登、暂停、Policy Center、邮件、页面截图、URL 链路、最近变更和指标异常。
3. 分类原因：目的地、误导、受限垂类、无效流量、付款、身份、账号安全或规避系统。
4. 修复资产：页面、广告文案、Offer、追踪、流量来源、权限或付款资料。
5. 保留证据：修复前后页面、变更记录、来源 URL、责任人、时间。
6. 走官方申诉或复审。
7. 更新内部准入规则和上线前审计清单。

### 2.4 账号暂停状态机

账号限制不是单一状态，处理前要先分类：

```text
policy_warning / strike
  -> ad_disapproval / limited_serving
  -> account_hold / temporary_suspension
  -> account_suspension
  -> appeal_pending
  -> reinstated / appeal_rejected
  -> postmortem / prevention
```

| 状态 | 含义 | 正确动作 | 错误动作 |
| --- | --- | --- | --- |
| policy warning / strike | 重复违规前的警告或处罚 | 立即修复、停相关资产 | 换账号继续跑同资产 |
| ad disapproval | 广告或资产不符合政策 | 修广告、页面、claim、URL | 复制到新账号 |
| limited serving / hold | 账号或站点被评估 | 停低质来源、补证据 | 刷量或换域名 |
| suspension | 账号被暂停投放 | 收集原因、修复、申诉 | 新开账号继续相同业务 |
| appeal pending | 申诉处理中 | 等待结果、补充准确证据 | 重复提交或并行换号 |
| reinstated | 恢复 | 复盘、更新准入和监控 | 立即恢复原高风险打法 |
| appeal rejected | 申诉未通过 | 补充分歧、重新修复、谨慎再申诉 | 账号池、付款资料规避 |

系统应把“受限后继续投放”的冲动转成证据、修复和申诉流程，而不是自动迁移预算、素材、域名或付款资料。

### 2.5 Related Account / Asset 风险

Google Ads account suspension 文档说明，关联账号也可能受影响；新建账号也可能被暂停。对套利团队而言，相关性不只来自账号 ID：

| 关联层 | 常见证据 | 处理 |
| --- | --- | --- |
| Identity | advertiser verification、business name、documents | 保持真实一致，不伪造主体 |
| Payment | payment profile、card、billing address、tax info | 不用付款资料规避 |
| Manager | MCC、admin ownership、user access | 记录真实代理/客户关系 |
| Destination | domain、landing page、tracking chain、Final URL | 修复页面和链路，不换壳 |
| Offer | 垂类、buyer、payout、terms、policy scope | 停高风险 Offer 或补资质 |
| Creative | claim、素材模板、关键词、广告承诺 | 修 claim 和证据 |
| Traffic | source、invalid traffic、deduction、complaint | 停源、隔离、复盘 |
| Operator | user、agency、external vendor、change history | 权限审计、责任人复盘 |

如果同一问题仍在这些层级存在，换账号只是扩大事故面。

### 2.6 申诉证据包

申诉不是“多写几句解释”，而是证明问题已被理解、修复和防止复发。建议证据包：

| 证据 | 说明 |
| --- | --- |
| suspension notice | 邮件、账号通知、Policy Center 截图 |
| affected assets | campaign、ad、keyword、URL、domain、offer |
| root cause classification | destination、misrepresentation、billing、verification、invalid traffic、security、circumvention |
| before / after snapshots | 页面、广告、URL、披露、资质、付款/验证材料 |
| change history | 修复动作、时间、执行人 |
| source URLs | Google policy、垂类资质、官方证明 |
| prevention controls | 上线前 checklist、任务拦截、审批、监控 |
| related account review | 相关账号是否也修复和合规 |
| reviewer and owner | 负责人、审核人、后续跟踪人 |

证据包的目标是让“为什么会发生、改了什么、以后如何避免”都可验证。

### 2.7 正常多账号准入清单

新账号或多账号只有在真实业务需要下才合理：

- 不同客户或广告主，有不同合同和授权。
- 不同品牌或产品线，有独立站点和商业目的。
- 不同地区实体或付款主体，有真实经营和税务/付款边界。
- 不同团队权限需要，有 MCC、访问级别和审计。
- 不同垂类资质或 certification 要求，需要独立合规资料。

不合理信号：

- 原账号暂停后立即复制 campaign、domain、offer、creative。
- 新账号使用相同受限页面、相同误导 claim、相同异常流量来源。
- 供应商承诺“不断号”“包恢复”“防关联开户”。
- 用不同付款资料、代理关系或假主体掩盖同一业务。

## 3. 行业诉求

团队可能有这些诉求：

- 账号受限后不想停投。
- 高风险 Offer 想分散到多个账号。
- 想保留主账号健康度。
- 想绕过审核学习期或历史质量问题。
- 外包团队希望快速恢复投放。

这些诉求应该通过修复问题、申诉和合规账号治理解决。

## 4. 主要风险

| 风险 | 说明 |
| --- | --- |
| 快速关联 | 新账号可能因业务和技术信号相似被关联 |
| 资产扩大受损 | 域名、付款、MCC、团队账号都可能受影响 |
| 原因未修复 | 页面、素材、流量或付款问题继续存在 |
| 现金流风险 | 账号限制、扣款争议和拒付会叠加 |
| 团队治理失败 | 责任不清，复盘缺失 |

## 5. 平台政策视角

Google Ads 的 Circumventing systems 政策关注广告主是否试图绕过审核、限制或执行机制。Advertising network abuse 也关注滥用广告网络、桥页、cloaking、arbitrage 等问题。封禁后切换账号继续相同问题，通常会被看作规避而不是修复。

Google Ads account suspensions overview 还强调，账号暂停可能来自政策、付款、未授权活动等多类原因；暂停账号不能投放，关联账号或新建账号也可能受影响；恢复路径是理解原因、修复问题、完成必要验证并提交申诉。系统设计应尊重这个流程。

## 6. 合规替代方案

正确流程：

1. 暂停相关投放。
2. 汇总账号通知、拒登原因、Policy Center 信息。
3. 审计落地页、广告承诺、追踪链路、付款资料、流量来源。
4. 修复明确问题。
5. 保留修复证据。
6. 使用官方申诉或复审流程。
7. 复盘并更新内部红线。

正常多账号管理可以使用：

- MCC。
- 角色权限。
- 客户/品牌/产品线的真实隔离。
- 审计日志。

账号治理替代方案：

| 诉求 | 不安全做法 | 安全替代 |
| --- | --- | --- |
| 账号受限后恢复收入 | 新开账号复制资产 | 停投、修复、申诉、复盘 |
| 多客户管理 | 共用一个主账号或账号池 | MCC、访问级别、客户授权 |
| 保护主账号 | 高风险 Offer 分散到小号 | 垂类准入、资质、页面审核、预算隔离 |
| 付款失败 | 换付款资料继续跑 | 修付款问题、核对 billing、官方流程 |
| 验证失败 | 换主体或假资料 | 完成 advertiser verification 和业务关系证明 |
| 重复拒登 | 换域名/换号 | 修素材、页面、claim、tracking chain |

## 7. 本系统落地

系统支持：

- 账号配置和状态备注。
- 审计日志。
- Offer 政策备注。
- 页面审计。
- 链接轮换记录。
- 指标异常复盘。
- `/risk-audits` 记录账号暂停、封禁规避、相关账号和申诉证据。
- `/sources` 保存 suspended account、circumventing systems、access levels、advertiser verification 等来源。

系统不支持：

- 封禁后自动切换账号。
- 新账号批量创建。
- 规避关联检测。
- 绕过封禁继续投放。
- 付款资料规避。
- 账号池、买号、租号或批量开户链接。
- 自动迁移 campaign 到新账号。

建议后续扩展实体表：

| 表 | 用途 | 禁止字段 |
| --- | --- | --- |
| `account_health_cases` | suspension、warning、verification、billing、security case | new account workaround |
| `account_incident_evidence` | notice、policy、asset、screenshot、source URL、owner | fake document |
| `related_account_reviews` | MCC、payment、domain、offer、operator、risk status | evasion map |
| `appeal_packages` | root cause、fix summary、evidence、submission status | mass appeal spam |
| `account_governance_profiles` | owner、business entity、payment profile、verification | account pool |

## 8. ADXKit 对应点和完成形态

ADXKit 公开页面涉及多账号管理、MCC、独立 Script、防关联和账号隔离等叙事。多账号管理本身可以是正常需求，例如不同客户、不同品牌、不同产品线需要独立预算和权限。但如果多账号的目的变成“某个账号受限后换一个账号继续同样问题”，就属于规避处置，而不是业务隔离。

合规账号治理流程：

1. 账号受限后先暂停相关投放，不继续扩大相同问题。
2. 收集 Policy Center、邮件通知、拒登原因、落地页截图、追踪链路、付款资料和最近变更日志。
3. 复盘触发原因：页面承诺、目的地、素材、流量来源、无效流量、付款或身份资料。
4. 修复明确问题，并保留证据。
5. 使用官方复审或申诉流程。
6. 复盘 SOP，更新内部红线和上线前审计模板。

正常多账号管理的证据：

- 真实客户、品牌、产品线、付款主体或合同不同。
- 账号之间没有共享违规页面、违规素材、隐藏跳转或异常流量来源。
- 使用 MCC、访问级别、审计日志和负责人制度。
- 被拒登或暂停时优先修复，而不是换壳继续投放。

本项目完成形态：

- `/accounts` 记录账号配置、Customer ID、同步方式、状态和备注。
- `/risk-audits` 记录封禁规避风险、修复方案和申诉证据。
- `/sources` 记录 Circumventing systems、账号访问级别、账号安全、申诉流程等来源。
- 审计日志记录账号、链接、指标和投放草稿的关键变更。

验收标准：

- 系统没有新账号注册、批量开户、付款资料切换或账号池管理功能。
- 系统没有封禁后自动换账号继续投放的任务类型。
- 高风险审计支持把账号切换诉求标为 high。
- 文档明确“修复和申诉”优先于“换号继续跑”。

## 9. 功能拆解和安全完成清单

把“为规避封禁创建或切换账号”拆成业务诉求后，可安全交付的是账号健康、证据包和申诉复盘，而不是账号池：

| 子能力 | 行业想解决的问题 | 本项目安全完成形态 |
| --- | --- | --- |
| 账号状态管理 | 知道哪个账号可投、受限、待修复 | `/accounts` 记录状态、同步方式和备注 |
| 风险分类 | 判断是拒登、暂停、验证、付款、无效流量还是页面问题 | 账号健康 SOP、风险审计、来源 URL |
| 修复证据包 | 申诉前需要证明问题已修复 | 文档要求保留截图、URL、变更记录、政策来源、责任人和时间 |
| 正常多账号治理 | 不同客户、品牌、地区或预算需要隔离 | MCC、访问级别、负责人、真实业务隔离说明 |
| 复盘闭环 | 防止同类问题再次出现 | `/logs`、Offer 政策备注、页面审计和上线前清单 |

安全验收点：

- 系统不包含批量开户、账号池、付款资料切换、封禁后自动换号或迁移投放的功能。
- 新增账号必须有真实业务原因，而不是“旧账号被封继续跑同一 Offer”。
- 账号受限后的默认流程是暂停、收集证据、修复、申诉、复盘。
- 风险审计中出现“规避封禁”“不断号”“换壳继续投”“防止关联处置”等表述时默认 high。
- 使用多账号时，证据应能说明客户、品牌、域名、付款、权限和负责人边界。

### 9.1 审计字段设计

| 字段 | 说明 |
| --- | --- |
| capability | 固定为 `ban_evasion_account_switching` |
| trigger | suspension、strike、verification failed、billing issue、policy warning、vendor proposal |
| account_scope | customer id、MCC、business entity、payment profile、owner |
| affected_assets | domains、landing pages、campaigns、ads、keywords、tracking URLs、offers |
| root_cause | policy、destination、misrepresentation、billing、verification、invalid traffic、security、circumvention |
| requested_action | new account、switch account、copy campaign、appeal、fix assets、pause |
| related_account_review | 是否有相同 identity、payment、domain、offer、operator |
| evidence_pack | notice、screenshots、change history、policy URL、repair proof |
| safe_path | pause、repair、appeal、verification、access review、postmortem |
| decision | rejected、repair_first、appeal_pending、reinstated、closed |
| reviewer | 审核人 |
| follow_up | 更新准入、阻断供应商、账号权限复核、页面/流量/付款修复 |

### 9.2 Account Recovery Score

建议用恢复评分决定是否继续投入修复，而不是换号：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| Root cause clarity | 25 | 是否清楚暂停/拒登/验证失败原因 |
| Asset remediation | 25 | 页面、素材、追踪、流量、付款是否已修复 |
| Evidence completeness | 20 | 通知、截图、变更、来源、责任人是否齐全 |
| Related account compliance | 15 | 相关账号是否也合规 |
| Prevention control | 15 | 是否更新准入、审批、监控和培训 |

低分说明证据不足或修复不完整，不是去创建新账号。

### 9.3 SOP

1. 账号出现 warning、hold、suspension、verification failure 时，冻结相关投放和换链。
2. 收集账号通知、Policy Center、邮件、受影响资产、最近 14-30 天变更和指标异常。
3. 分类根因：政策、目的地、误导、受限垂类、无效流量、付款、验证、账号安全或规避系统。
4. 修复根因：页面、claim、资质、tracking、source、payment、access、verification。
5. 审查相关账号：是否共享 identity、payment、domain、offer、creative、operator 或 source。
6. 生成申诉证据包，只提交准确、诚实、可验证的说明。
7. 申诉处理中不创建新账号复制同一业务；等待结果或补充证据。
8. 恢复后进入 postmortem：更新红线、上线前 checklist、任务拦截和账号权限。
9. 申诉未通过时，不进入账号池；重新核实根因、补修复证据或停止该业务。

### 9.4 通过/拒绝例子

| 需求 | 判断 | 处理 |
| --- | --- | --- |
| 客户 A 和客户 B 分别有独立合同和付款主体 | 可通过 | MCC + 访问级别 + 账号档案 |
| 同品牌不同国家有真实实体和本地站点 | 可审慎通过 | 保存 business / domain / payment evidence |
| 原账号因 cloaking 暂停，想复制 campaign 到新号 | 拒绝 | 修复 cloaking，走申诉 |
| 付款异常后换卡换号继续跑 | 拒绝 | 修付款和 billing 资料 |
| 验证失败后换主体资料 | 拒绝 | 补真实 verification 证据 |
| 外包供应商承诺“包过封号、不断号” | 拒绝 | 供应商风险审计 |

## 10. 信息来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑不允许通过创建或使用其他账号规避政策执行、限制或暂停 |
| Google Ads account suspensions overview | https://support.google.com/google-ads/answer/9841640 | 支撑暂停原因、关联账号/新账号风险、申诉、验证和 read-only 状态 |
| Google Ads Policy, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑桥页、cloaking、arbitrage、低价值目的地和广告网络滥用风险 |
| Google Ads Help, About access levels in your Google Ads account | https://support.google.com/google-ads/answer/9978556 | 支撑通过访问级别和权限治理协作，而不是共享或切换账号 |
| Google Ads Help, Manager account access levels | https://support.google.com/google-ads/answer/9977851 | 支撑 MCC / manager account 权限边界和 ownership 关系 |
| Google Ads Help, Secure your Google Ads account | https://support.google.com/google-ads/answer/2375456 | 支撑账号安全、未授权活动、安全设置和访问审计 |
| Google Ads Advertiser verification document requirements | https://support.google.com/adspolicy/answer/9872280 | 支撑 advertiser verification、身份/业务资料和真实主体证明 |
| Google Ads API, Advertiser identity verification | https://developers.google.com/google-ads/api/docs/account-management/advertiser-identity-verification | 支撑 verification program 是官方账号治理对象，而不是换主体绕过 |
| ADXKit homepage | https://adxkit.com/ | 仅用于记录其公开页面提到多账号、防关联和独立 Script 等功能话术 |
