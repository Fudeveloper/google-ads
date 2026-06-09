# 账号、MCC、付款与 Advertiser Verification 治理手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何治理 Google Ads 账号、Manager Account / MCC、访问权限、付款资料、account budget、Advertiser Verification、业务操作验证、代理关系和账号健康证据。目标是把账号当作合规经营资产，而不是账号池、防关联资产或封禁后继续投放的消耗品。

本文不提供批量开户、账号池、付款资料规避、验证资料伪造、封禁后换号继续投放、Cookie 登录态共享、代理/指纹隔离账号或绕过 Google Ads 安全检查的方案。

## 1. 为什么账号治理是套利核心

Ads 套利通常现金流快、测试频繁、页面和 Offer 更换多。如果账号治理弱，利润模型会被下面问题击穿：

- 投放人员权限过大，误开预算、改付款或接受高风险 recommendations。
- 付款资料、网站主体、广告主披露和 Offer 主体不一致。
- 代理商或团队用一个付款 profile 跑多个无关业务，解释不清。
- 账号验证、业务操作验证或付款审核卡住，导致测试中断。
- 某个低质站点、页面、流量来源或违规 Offer 把整个账号/MCC 拖进暂停。
- 封禁后新开账号继续同一问题，升级为 circumventing systems / multiple account abuse。

账号治理的目标不是“多账号分散风险”，而是让主体、权限、付款、业务、网站、Offer、转化和证据能被解释。

## 2. 核心对象

| 对象 | 作用 | 套利风险 |
| --- | --- | --- |
| Google Ads account | 实际投放和账单账号 | 付款、验证、政策、转化和页面风险集中 |
| Manager Account / MCC | 管理多个广告账号 | 被误用成账号池或规避关联层 |
| Client account | MCC 下被管理的投放账号 | 业务主体、权限和付款关系要清楚 |
| Payments profile | 付款主体、地址、税务和付款方式 | 与网站/广告主主体不一致会触发验证或信任问题 |
| Account budget | 账号级预算控制 | 缺少上限会导致现金流和账单风险 |
| Access level | Admin、Standard、Read only、Billing 等权限 | 权限过宽会带来误操作、付款和验证风险 |
| Advertiser Verification | 身份、业务操作和披露验证 | 资料不一致、业务不透明或虚假信息会失败 |
| Agency / client relationship | 代理商、客户、付款方、服务方关系 | 代理商代跑多个无关客户时容易解释不清 |

## 3. MCC 是治理工具，不是账号池

Google Ads manager account 适合代理商或管理多个账号的团队集中查看、管理和报告。它的合规用途包括：

- 一个入口管理多个客户或业务线。
- 为团队成员设置不同访问级别。
- 集中查看账号状态、通知和报表。
- 管理客户账号和子 manager account。
- 支持账单、预算、权限和审计流程。

套利团队常见误区：

- 把 MCC 当作“封一个换一个”的账号池控制台。
- 为同一业务快速创建大量相似账号。
- 让不相关客户共用付款 profile、域名、追踪、素材或转化。
- 用子 MCC 隔离违规页面、违规付款、可疑流量或封禁历史。
- 只记录 customer ID，不记录业务主体、付款主体和风险边界。

MCC 结构设计原则：

1. 按真实业务主体、客户、品牌或地域拆分，而不是按规避检测拆分。
2. 每个 client account 都有 owner、业务说明、付款主体、网站、主要 Offer 和风险状态。
3. 高风险测试账号不和稳定业务共享页面、转化、付款、域名或流量来源。
4. 账号被暂停时先冻结变更和修复，不新建账号继续同一业务。

## 4. 访问权限和最小权限

Google Ads 和 manager account 都有访问级别。账号治理要把“能投放”和“能改付款/权限/验证”分开。

权限建议：

| 角色 | 建议权限 | 原因 |
| --- | --- | --- |
| 投放执行 | Standard 或受控操作 | 可建草稿、调预算，但不能管理付款或权限 |
| 报表/财务 | Read only / Billing | 查看账单、付款、花费和发票 |
| 审核负责人 | Admin 或审批权限 | 控制验证、权限、关键变更和申诉 |
| 外部代理 | 最小必要权限 | 避免代理获得客户付款、验证和所有权控制 |
| 临时协作 | 限时 Read only / Standard | 到期移除，避免长期遗留访问 |

高风险信号：

- 多人共用一个 Google 登录或 Cookie。
- 用个人账号长期保管所有客户权限。
- 投放人员同时拥有付款 profile、验证、权限管理和预算全权限。
- 离职、外包或代理关系结束后未移除访问。
- 账号暂停后先删人、删记录、转移资产，而不是做证据包。

## 5. 付款资料、账单与 Account Budget

Google Ads 常见付款设置包括自动付款、手动付款和月结发票。套利团队要把付款设置纳入现金流和账号健康，而不是只看能否扣款。

治理要点：

- 付款 profile 的主体、地址、税务资料、网站主体和广告主验证资料一致。
- Billing access 与投放权限分离；付款变更需要审批。
- 自动付款要记录阈值、扣款日期、备用付款方式和失败处理。
- 手动付款要记录余额、充值计划和停投阈值。
- 月结发票要记录信用额度、账期、发票、付款截止日和逾期风险。
- account budget 用于账号级支出边界，不替代 campaign/dayparting 止损。

套利场景常见事故：

- Google Ads 花费先发生，联盟/AdSense 收入晚到账，现金流断裂。
- 付款失败导致 campaign 停止，影响学习期和账号健康。
- 付款主体和网站主体不一致，触发 advertiser verification 或业务真实性问题。
- 多个无关业务共用付款 profile，导致一个业务问题影响其他账号。

## 6. Advertiser Verification 与业务操作验证

Advertiser Verification 不是形式填表。它要求主体、付款、网站、业务、广告披露和实际服务能相互解释。

准备材料：

| 项目 | 要求 |
| --- | --- |
| 法定主体 | 公司/个人名称与付款 profile、网站披露一致 |
| 网站 | 联系方式、隐私政策、服务条款、退款/取消政策清楚 |
| 业务说明 | 谁提供产品/服务，谁收款，用户得到什么 |
| 代理关系 | 代理商、客户、付款方和广告披露关系清楚 |
| 授权证明 | 客户授权、品牌授权、垂类许可、合同或发票 |
| 变更记录 | 付款 profile、域名、业务线或账号结构变化有记录 |

常见失败原因：

- 付款资料主体、网站主体和广告主主体不一致。
- 代理商没有客户授权或披露不清。
- 页面像 lead gen / affiliate，但广告主身份伪装成官方。
- 敏感行业缺少许可、资质或地区说明。
- 提交虚假信息或隐瞒业务关系，升级为规避系统风险。

## 7. 代理关系和客户管理

代理商或内部运营团队可以管理多个账号，但必须解释清楚关系。

合格代理关系：

- 每个客户有合同、授权、服务范围和付款责任说明。
- 客户网站、广告主披露、付款 profile 和账号归属清楚。
- 代理只获得必要访问权限。
- 客户离开时有交接、权限移除和数据归档。
- 不把代理 MCC 当成给不相关 Offer 批量开号的工厂。

高风险代理关系：

- 代理商用自己的付款资料跑多个无关客户。
- 客户不知道实际广告内容、页面或流量来源。
- 账号被暂停后代理直接换客户账号、换域名、换付款继续投。
- 代理不提供 change history、账单、广告资产或来源证据。

## 8. 账号结构与业务隔离

正常隔离：

- 不同法人主体。
- 不同客户。
- 不同国家/币种/付款方式。
- 不同风险等级或垂类。
- 不同发布商/联盟合同和收入结算。

高风险隔离：

- 同一违规业务复制到多个账号。
- 封禁后换号继续投。
- 用多个账号测试同一高风险页面以碰审核概率。
- 用不同付款资料、域名、MCC、代理或指纹掩盖同一控制人。

判断标准：

1. 是否有真实业务理由。
2. 是否有一致的主体和付款证据。
3. 是否共享违规页面、素材、Offer、追踪链或低质流量。
4. 是否在暂停/拒登后继续相同问题。
5. 是否能向 Google、客户和内部财务解释。

## 9. 账号事件和证据包

每个账号应保留：

- customer ID、MCC 层级、owner、业务线、国家、币种。
- 付款 profile、付款设置、account budget、发票和付款记录。
- 用户访问级别、代理/客户关系、权限变更记录。
- Advertiser Verification 状态、提交资料、结果和补件记录。
- Policy Manager、Change history、拒登、暂停和申诉记录。
- 主要域名、Final URL、tracking domain、Offer、转化 action。
- 高风险事件、处理人、处理方案和来源 URL。

账号暂停、付款失败、验证失败或重大拒登时，先冻结：

- 新建 campaign。
- 新增账号。
- 换域名/换 Final URL。
- 换付款资料。
- 扩预算。
- 自动任务。

然后建立证据包，再决定修复、申诉、暂停业务或下线 Offer。

## 10. 系统落地

当前 V1 用已有模块落地：

| 需求 | 当前页面 / 文档 |
| --- | --- |
| 记录 Google Ads / MCC / 账号状态和同步方式 | `/accounts` |
| 阻止账号池、批量开号、封禁后换号语义 | `/accounts` 表单安全校验 |
| 记录付款、验证、MCC、代理关系备注 | `/accounts` 的 notes / status |
| 记录高风险账号事件和来源 URL | `/risk-audits` |
| 记录官方政策和帮助文档来源 | `/sources` |
| 记录导出、任务、链接、指标变更 | `/logs` |
| 使用 CSV / Scripts / 手工审批替代 Cookie 后台操作 | `/campaigns`、`/tasks`、开发文档 |

后续可新增表：

```text
account_governance_profiles
mcc_hierarchy_snapshots
account_access_reviews
billing_profile_checks
advertiser_verification_cases
agency_client_relationships
account_budget_controls
account_incident_evidence
```

这些表只用于账号资产治理、权限审计、付款和验证证据留存，不用于批量建号、账号池、规避封禁或防关联操作。

## 11. QA 清单

- 每个账号有 owner、业务主体、付款主体、网站和主要 Offer。
- MCC 层级按真实业务关系建立，不按规避检测建立。
- 访问权限遵循最小权限，离职/外包/代理结束后移除。
- Admin、Billing、Advertiser Verification 权限有审批和复核。
- 付款 profile、网站主体、广告主验证和发票信息一致。
- account budget、付款阈值、信用额度和现金流止损记录清楚。
- 代理关系有合同、授权、付款责任和广告披露说明。
- 账号暂停后不新建账号继续同一业务。
- 账号问题能关联到页面、素材、付款、验证、流量来源或政策来源。
- `/risk-audits` 中记录高风险账号事件和处理结论。

## 12. 信息来源 URL

- Google Ads Help, About Google Ads manager accounts: https://support.google.com/google-ads/answer/6139186
- Google Ads Help, Create a Google Ads manager account: https://support.google.com/google-ads/answer/7459399
- Google Ads Help, Manager account access levels: https://support.google.com/google-ads/answer/9977851
- Google Ads Help, About access levels in your Google Ads account: https://support.google.com/google-ads/answer/9978556
- Google Ads Help, Manage access to your Google Ads account: https://support.google.com/google-ads/answer/6372672
- Google Ads Help, About payment settings: https://support.google.com/google-ads/answer/2375432
- Google Ads Help, About payments profile link types: https://support.google.com/google-ads/answer/15758513
- Google Ads Help, Create an account budget: https://support.google.com/google-ads/answer/2375395
- Google Ads Help, Secure your Google Ads account: https://support.google.com/google-ads/answer/2375456
- Google Ads Policies, Advertiser verification: https://support.google.com/adspolicy/answer/9703665
- Google Ads Policies, Tasks required for Advertiser verification: https://support.google.com/adspolicy/answer/15577076
- Google Ads Policies, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
