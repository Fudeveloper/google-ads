# 账号健康、政策中心与申诉 SOP

更新时间：2026-06-08

本文说明 Google Ads / AdSense / 发布商变现场景中，如何处理广告拒登、目的地问题、账号暂停、广告投放限制、AdSense Policy Center 问题、验证任务、无效流量提醒和申诉流程。目标是用事实修复和证据申诉恢复合规投放，而不是通过换账号、换域名、Cookie 后台操作、cloaking 或隐藏真实目的地规避政策执行。

## 1. 核心原则

账号健康管理不是“封了再换”，而是持续管理下面 5 件事：

1. 政策状态：广告、关键词、资产、落地页、账号、发布商站点是否有 policy issue。
2. 业务真实性：主体、付款资料、网站、隐私条款、联系方式、服务范围是否一致。
3. 目的地体验：Final URL、页面内容、广告承诺、跳转链和用户体验是否一致。
4. 流量质量：是否有无效点击、异常展示、低停留、来源不透明、扣量和拒付。
5. 证据留存：每次修复、截图、账单、页面版本、来源 URL、申诉内容和结果是否归档。

原则：

- 先定位原因，再修复，再申诉。
- 不要在未修复时反复提交 appeal。
- 不要因为暂停就创建或切换账号继续同样业务。
- 不要用审核页/用户页不一致、换域名、代理、指纹或 Cookie 操作规避系统。
- 每次恢复都要形成复盘，更新上线检查表。

## 2. 常见状态字典

| 状态 | 典型含义 | 处理方向 |
| --- | --- | --- |
| Ad disapproved | 单条广告、资产或关键词违反政策或目标页问题 | 修复广告/资产/目标页后 appeal |
| Limited by policy | 广告可投但受限制 | 确认是否属于垂类限制或缺少认证 |
| Destination not working | 目标 URL 不可访问、跳转异常、移动端或地区不可用 | 修复 URL、服务器、证书、跳转和页面 |
| Account suspended | 账号级暂停 | 停止投放，定位原因，修复账号/网站/付款/验证问题后提交申诉 |
| Advertiser verification required | 需要验证广告主身份或业务操作 | 准备法定主体、付款资料、网站和业务证明 |
| AdSense policy issue | 发布商站点存在政策问题或监管/广告主偏好问题 | 在 Policy Center 中定位页面和问题，修复后请求 review |
| Ad serving limited | 广告服务受限，常见于流量质量或账号评估 | 降低风险来源，证明真实流量和内容质量 |
| Invalid traffic deduction | 收入因无效流量被扣减 | 查 source/subid、暂停异常来源、降低未来预算 |

## 3. 事件分级

| 等级 | 示例 | 响应时间 | 动作 |
| --- | --- | --- | --- |
| P0 | Google Ads 账号暂停、AdSense 账号 disabled、付款 hold | 立即 | 暂停所有相关投放，冻结变更，成立修复记录 |
| P1 | 站点 ad serving disabled、重大扣量、核心 campaign 全拒登 | 当天 | 暂停受影响来源，修复页面/URL/政策问题 |
| P2 | 单广告拒登、部分页面 policy issue、验证提醒 | 1-2 天 | 修复后提交 review，避免扩量 |
| P3 | 建议、警告、低优先级 advertiser preference | 周内 | 进入常规优化和风险审计 |

P0/P1 期间不要做：

- 新开账号继续同一业务。
- 快速换域名、换 Final URL、换支付资料。
- 批量提交模板化 appeal。
- 删除日志、删除页面、隐藏真实跳转链。

## 4. Google Ads 拒登处理流程

流程：

```text
发现拒登
  -> 读取政策原因和受影响对象
  -> 定位广告文案 / 资产 / 关键词 / Final URL / 页面
  -> 修复问题
  -> 保存修复前后证据
  -> 从账号内提交 appeal 或重新审核
  -> 跟踪 Policy manager 状态
  -> 复盘并更新创意/页面检查表
```

检查清单：

| 检查项 | 问题 |
| --- | --- |
| 广告文案 | 是否有误导、夸大、官方伪装、虚假价格、保证结果 |
| 资产 | Sitelink、callout、image、business name 是否与页面一致 |
| Final URL | 是否可访问，是否与 display URL 和广告承诺一致 |
| Tracking template | 是否导致最终页面不一致或参数丢失 |
| 页面内容 | 是否有原创内容、隐私、联系信息、披露和移动端可用性 |
| 垂类政策 | 金融、医疗、博彩、官方服务、技术支持等是否需认证 |

申诉文字应说明：

- 受影响对象是什么。
- 原因理解是什么。
- 具体修改了哪些页面、广告或资产。
- 为什么现在符合政策。
- 附上可验证的 URL、截图、政策来源或业务证明。

不要写：

- “Please approve ASAP”。
- “We did nothing wrong”但没有证据。
- “Competitors are doing it too”。
- “We changed domain/account”作为解决方案。

## 5. Google Ads 账号暂停处理

账号暂停要先停止动作，避免扩大风险。

第一小时：

1. 保存暂停通知、账号 ID、时间、暂停原因、受影响账号和付款资料。
2. 停止自动导入、预算调整、链接轮换和新增 campaign。
3. 导出当前 campaign、ads、keywords、Final URL、tracking template、billing 状态。
4. 确认是否有付款失败、验证未完成、恶意软件、规避系统、虚假陈述、可疑付款或业务真实性问题。

修复阶段：

| 类别 | 修复证据 |
| --- | --- |
| 付款问题 | 已付款截图、账单、付款资料一致性 |
| 验证问题 | 主体证件、商业登记、付款资料、网站主体一致 |
| 目的地问题 | 页面可访问、HTTPS、无误导跳转、内容与广告一致 |
| 虚假陈述 | 明确服务主体、价格、退款、条款、联系方式、资质 |
| 规避系统 | 移除审核分流、隐藏跳转、多账号绕过、cloaking 风险 |
| 恶意软件 | 安全扫描、清理记录、主机和插件修复证明 |

申诉阶段：

- 只在修复完成后提交。
- 用事实和证据，不用情绪化话术。
- 不要多次重复提交相同内容。
- 提交后跟踪状态和回复，补充证据时保持一致口径。
- 若失败，重新定位未解决项，而不是立即换号。

## 6. Advertiser Verification SOP

广告主验证常见要求：

- 验证广告主身份。
- 验证业务操作。
- 验证付款资料和广告披露信息。
- 在特定垂类提供许可、资质或业务关系证明。

准备清单：

| 项目 | 要求 |
| --- | --- |
| 法定主体 | 公司名称、个人姓名、注册资料与付款资料一致 |
| 网站 | 公司名、联系方式、隐私政策、服务条款、退款/取消政策清楚 |
| 业务说明 | 谁提供服务、谁付款、谁运营广告、用户得到什么 |
| 证明材料 | 营业执照、税务资料、许可证、授权书、发票或合同 |
| 代理关系 | 代理商、客户、付款 profile 和广告披露关系说明 |

常见失败点：

- 付款资料主体和网站主体不一致。
- 网站没有真实联系方式或政策页。
- 代理商用自己付款资料跑多个不相关客户。
- 业务描述和实际页面/Offer 不一致。
- 敏感行业缺少许可或资质。

## 7. AdSense Policy Center SOP

AdSense / 发布商侧要区分：

| 类型 | 影响 |
| --- | --- |
| Policy issue | 必须修复，否则相关页面/站点不会获得广告服务，重复问题可能导致账号暂停 |
| Regulatory issue | 不一定违规，但会影响广告需求或显示 |
| Advertiser preference | 广告主偏好导致广告减少，通常不是政策违规 |

处理流程：

1. 打开 Policy Center，按 disabled ad serving、affected ad requests、站点或页面优先级排序。
2. 点开 issue details，查看问题类型、位置和截图。
3. 修复页面：内容、广告位置、无效流量来源、隐私/监管、广告密度或诱导点击。
4. 对页面级 issue 批量或单独 request review。
5. 记录 review status：under review、rejected、resolved。
6. 如果 review rejected，重新看 issue details，补修后再提交。

重要原则：

- 如果移除广告代码，问题可能不再展示，但这不是恢复变现的修复。
- 如果继续买低质量流量，Policy Center 通过也可能再次触发。
- 如果来源不可解释，先停量再请求 review。

## 8. 无效流量和扣量响应

发现 invalid traffic、ad serving limited、扣量或收入异常时：

1. 停止或隔离最近新增来源、placement、publisher、subid。
2. 对比 clicks、sessions、ad requests、revenue、CTR、viewability、time on page。
3. 检查是否存在激励访问、自动浏览、误导按钮、广告伪装、过高广告密度。
4. 保存供应商报表、source id、日志、页面截图和变更记录。
5. 更新预算安全系数和来源评分。
6. 对不可解释或拒绝提供明细的供应方永久降级或停用。

不要通过“补自然流量”“刷真实用户行为”“代理模拟访问”来掩盖异常。这样会把收入扣量风险升级为账号风险。

## 9. 证据包模板

```text
事件 ID：
发现时间：
平台：Google Ads / AdSense / AdX / Affiliate
账号 / 站点 / Campaign：
政策原因：
受影响 URL / 广告 / 资产：

修复前证据：
- 通知截图：
- 页面截图：
- URL / tracking template：
- 指标异常：

修复动作：
1.
2.
3.

修复后证据：
- 页面截图：
- 可访问 URL：
- 政策来源 URL：
- 变更记录：

申诉内容：
提交时间：
Review status：
结果：
复盘和预防：
```

## 10. 申诉质量评分

| 维度 | 低质量 | 高质量 |
| --- | --- | --- |
| 原因理解 | 不知道为什么被拒 | 精确到政策、页面和对象 |
| 修复动作 | 只说“已修复” | 列出具体 URL、字段、页面、证据 |
| 业务真实性 | 主体不清楚 | 主体、付款、网站、服务和披露一致 |
| 风险来源 | 继续跑同样来源 | 已暂停异常 source/subid 并记录 |
| 语气 | 情绪化、威胁、模板化 | 简洁、事实、证据 |
| 重复提交 | 未改动就反复 appeal | 每次申诉都有新增修复证据 |

内部建议：申诉前由非执行人复核一次证据包，确认“修复已经完成，而不是准备修复”。

## 11. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录账号状态和同步方式 | `/accounts` |
| 记录 Offer、页面、政策备注 | `/offers` |
| 审计页面质量和目的地 | Offer 详情页落地页采集 |
| 记录风险事件、原因、修复和来源 URL | `/risk-audits` |
| 记录官方政策和证据来源 | `/sources` |
| 安排 URL 检查、报表检查、导出检查 | `/tasks` |
| 查看变更和执行日志 | `/logs` |
| 在验收中确认高风险边界 | `/knowledge/acceptance` |

系统不做：

- 不存储或复用登录 Cookie。
- 不自动绕过登录、2FA、安全挑战。
- 不创建账号池或封禁后换号继续投放。
- 不用 cloaking 或审核页/用户页不一致来处理拒登。
- 不模拟点击、展示、访问或转化来掩盖流量质量问题。

## 12. 信息来源 URL

- Google Ads Help, Fix a disapproved ad or appeal a policy decision: https://support.google.com/google-ads/answer/9338593
- Google Ads Help, About Policy Manager: https://support.google.com/google-ads/answer/9675313
- Google Ads Help, Google Ads account suspensions overview: https://support.google.com/adspolicy/answer/2375414
- Google Ads Help, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads Help, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Help, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Help, Advertiser verification: https://support.google.com/adspolicy/answer/9703665
- Google Ads Help, Tasks required for Advertiser verification: https://support.google.com/adspolicy/answer/15577076
- Google Ads API, Ad disapprovals and account recovery issues: https://developers.google.com/google-ads/api/support/policy
- Google AdSense Help, Understand policy issues, regulatory issues, advertiser preferences, and ad serving statuses: https://support.google.com/adsense/answer/15689616
- Google AdSense Help, Fix policy issues that affect ad serving: https://support.google.com/adsense/answer/7003627
- Google AdSense Help, AdSense Program policies: https://support.google.com/adsense/answer/48182
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
