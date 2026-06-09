# Google Ads 广告审核、拒登、Policy Manager 与申诉证据包手册

更新时间：2026-06-09

本文聚焦广告级审核和拒登处理：广告、素材、关键词、Final URL、tracking template、落地页和政策主题如何被审核；拒登后如何定位原因、修复问题、准备证据包、提交申诉，并把结果反馈到套利运营的素材生成、换链接、批量导入和止损流程中。

本文不提供 Ads Cookie 登录、后台自动点击、2FA 绕过、审核规避、cloaking、补点击、代理指纹规避或封禁后换号执行方案。高风险点会被完整记录为行业知识、平台原理、风险识别、审计字段和合规替代流程。

## 1. 为什么广告审核是套利上线闸门

Ads 套利的利润来自买量成本、落地页变现、转化回传和回款之间的价差。广告审核决定的是“这组素材和这个目的地能不能进入真实流量拍卖”，所以它不是投放流程末端的小错误，而是上线闸门。

常见业务影响：

1. 批量生成素材后，如果 claim 没有页面证据，会带来高拒登率。
2. 换链接或改 tracking template 后，如果最终目的地、display URL、移动端体验或跳转链不一致，会触发目的地问题。
3. AI 批量改标题时，如果出现官方冒充、保证结果、虚假折扣、夸大排名、敏感垂类承诺，会触发 Misrepresentation、Editorial、Financial、Healthcare、Gambling 等政策问题。
4. 同一模板在多个 campaign 或账号重复触发相同拒登，会把单条广告问题升级为账号健康问题。
5. 没有证据包的重复 appeal 会浪费审核机会，也会让团队误判“平台误杀”，从而继续扩量相同错误。

正确目标不是“绕过审核”，而是把审核看成素材、页面、链接和投放结构的一致性检查。

## 2. Google Ads 审核原理

Google Ads 的公开说明显示，新建或修改广告/素材后通常会进入审核。审核会检查广告内容、关键词、目标页、图片、视频和其他资产是否符合政策。多数广告会在 1 个工作日内审核完成，复杂场景可能更久。

审核对象不是只有最终广告文案。套利团队必须把它拆成 7 类对象：

| 对象 | 审核关注点 | 常见套利问题 |
| --- | --- | --- |
| Ad | headline、description、display URL、business name、callout、sitelink 等 | 夸大收益、冒充官方、虚假稀缺、价格不一致 |
| Asset | 图片、视频、logo、business name、promotion、lead form 等 | 图片与 offer 不一致，品牌或资质暗示过强 |
| Keyword | 关键词主题、品牌词、敏感词、受限垂类 | 竞品词冒充、敏感垂类无认证 |
| Final URL | 用户点击后应到达的真实页面 | 页面不可达、地区不可用、移动端错误、桥页/MFA |
| Tracking template | 中间跳转、参数、parallel tracking、redirect chain | 参数丢失、最终页不一致、地域或设备分流异常 |
| Landing page | 页面内容、主体、披露、隐私、联系、原创性、广告密度 | 页面兑现不了广告 claim，缺少主体和条款 |
| Account context | 账号历史、付款、验证、政策重复问题 | 同一业务反复拒登后换壳扩量 |

Google Ads API 的政策相关对象也说明，广告实体可能带有 `PolicySummary`，政策主题可能以 `PolicyTopicEntry` 的形式出现。即使第一版系统不接官方 API，也应按这个思路保存“受影响对象 + policy topic + 证据 + 处理状态”。

## 3. 状态口径

团队内部不要只用“过了/没过”两个状态。建议统一以下口径：

| 状态 | 含义 | 运营动作 |
| --- | --- | --- |
| under_review | 新建或修改后等待审核 | 不扩量，不重复提交相同 payload |
| eligible | 可投放 | 进入小预算测试和指标观察 |
| eligible_limited | 可投但受政策或垂类限制 | 检查受限国家、受众、关键词、认证和敏感垂类规则 |
| disapproved | 拒登 | 冻结受影响对象，定位 policy topic，修复后提交 review/appeal |
| not_eligible | 不可投放或不符合要求 | 重新评估 offer、页面、资质和投放结构 |
| appeal_pending | 已提交申诉 | 不重复 appeal，不换壳重投同一问题 |
| appeal_rejected | 申诉失败 | 重新定位未修复项，不把失败归因于“审核误杀” |
| appeal_approved | 申诉成功 | 保存证据包，更新上线检查表和素材模板 |

ADXKit 类工具如果提供“审核后一键提交”“自动投放”“批量换链接”，真实瓶颈就在这些状态口径。没有状态机，自动化只会把同一错误放大。

## 4. Policy Manager 的作用

Policy Manager 是广告账号里集中查看政策问题和申诉状态的入口。它的价值不是“批量点申诉”，而是把每个问题归档成可处理事件：

| 信息 | 为什么重要 |
| --- | --- |
| policy topic | 决定要查哪条政策，不同政策的修复证据不同 |
| affected object | 是广告、素材、关键词、目标页还是账号问题 |
| status | 区分拒登、受限、待审核、申诉中、已解决 |
| appeal history | 避免重复提交模板化申诉 |
| review result | 用于复盘素材模板、页面 brief、链接变更和账号健康 |

套利团队常犯的错误是只看“campaign 不花钱”，不看 Policy Manager。正确做法是先把 policy issue 变成工单，再处理素材、页面或链接。

## 5. 常见拒登类型和原理

### 5.1 Destination requirements

目的地要求关注用户点击广告后能否到达可用、清晰、一致的页面。

常见触发：

- Final URL 无法访问、超时、SSL 错误、移动端不可用。
- display URL、广告承诺和实际页面主题不一致。
- tracking template 或跳转链导致最终页不同。
- 页面需要下载、登录或额外步骤才能看到广告承诺。
- 地区、设备、浏览器、语言不同导致用户看到不同内容。

套利处理原则：

- 换链接前做 Final URL、expanded URL、移动端、主要 GEO 和参数保留 QA。
- 不用“审核页/用户页不一致”处理拒登。
- 页面不可达不是投放问题，是上线阻断问题。

### 5.2 Misrepresentation

Misrepresentation 关注广告或页面是否误导用户，尤其是主体、价格、资格、官方关系、结果承诺、费用和重要限制。

常见触发：

- “官方”“政府授权”“最佳”“保证通过”“限时免费”等 claim 缺少证据。
- affiliate 或 lead gen 页面没有清楚说明自己不是最终服务方。
- 页面隐藏价格、资格、取消、退款、地理限制或广告性质。
- AI 素材把页面没有的信息编成广告卖点。

套利处理原则：

- 每条强 claim 都要绑定 proof snippet。
- affiliate、advertorial、lead form 需要披露商业关系和后续联系。
- 用户点击广告后看到的主体和承诺必须与广告一致。

### 5.3 Editorial requirements 和 Text ad requirements

编辑和文字广告要求关注文案质量、标点、大小写、语法、重复、花哨格式、不可识别文本、诱导性表达和广告资产格式。

常见触发：

- 全大写、重复感叹号、过度符号、奇怪空格。
- 模板拼接导致语义不通。
- 标题和描述塞满关键词但没有真实信息。
- 动态文本插入导致竞品、品牌或敏感词失控。

套利处理原则：

- 生成素材后先做格式 lint，再做 claim 审核。
- 不要把高 CTR 的夸张文案直接当成可扩量资产。
- 批量导入前抽样检查最长 headline、最长 description 和动态替换结果。

### 5.4 Trademarks 和品牌词

品牌词本身不一定绝对禁止，但广告文本、落地页、display URL、业务关系和用户感知会影响风险。

常见触发：

- 文案暗示自己是品牌官方。
- 竞品词流量落到不相关或误导性页面。
- domain、display URL 或 business name 让用户误以为是商标方。

套利处理原则：

- 品牌词投放必须和 offer 条款、商标政策、页面披露一致。
- affiliate 页面要明确关系，不做官方冒充。
- 竞品词不是低价流量池，而是高投诉和拒登风险源。

### 5.5 Unacceptable business practices

不可接受商业行为关注严重误导、欺骗、隐藏身份、错误展示业务模式等问题。

常见触发：

- 伪装成官方机构、品牌或服务入口。
- 隐藏费用或诱导用户提交敏感信息。
- 页面让用户误以为必须立即行动，否则损失权益。
- 技术支持、金融、医疗、政府服务等高敏垂类缺少资质或真实主体。

套利处理原则：

- 落地页必须说明“谁提供服务、谁收集信息、用户会发生什么”。
- lead buyer 或 affiliate network 不愿提供披露要求时，不应上线。
- 高佣金不抵消政策和退款/投诉风险。

### 5.6 Circumventing systems

规避系统是高风险政策方向，关注绕过审核、隐藏真实目的地、cloaking、多账号规避、动态替换违规内容等行为。

常见触发：

- 审核页和用户页不一致。
- 根据 User-Agent、IP、地理位置、cookie 或时间展示不同内容以影响审核。
- 被拒登后不修复原因，只换域名、换账号或换跳转链继续投。
- 用代理、指纹或 Worker 转发隐藏真实关联和目的地。

系统处理原则：

- 记录原理、识别信号、审计字段和事故 SOP。
- 不实现 Cookie 接管、cloaking、代理指纹规避或换号规避封禁。
- 链接计划只能用于断链修复、合规 A/B、参数修复和已审核同主题页面切换。

### 5.7 敏感垂类限制

金融、医疗、赌博、住房/就业/信贷、个性化广告、政府服务、技术支持等垂类有额外限制或认证要求。

常见触发：

- 金融 offer 缺少地区资格、费用、风险、许可信息。
- 医疗页面做未经证实的疗效承诺。
- 赌博或博彩相关内容投向未授权地区。
- 个性化广告使用敏感属性或不当受众。

套利处理原则：

- 先做 offer 准入，再做素材生成。
- 没有资质的垂类不要靠文案规避。
- 受限垂类必须记录国家、认证、广告主主体、页面披露和投放限制。

## 6. 拒登处理流程

建议所有拒登事件按下面流程处理：

```text
发现拒登
  -> 冻结受影响 campaign/ad group/ad/asset/link rule
  -> 保存 Policy Manager 截图、policy topic、对象 ID 和时间
  -> 判断对象类型：文案 / 素材 / 关键词 / Final URL / tracking / 页面 / 账号上下文
  -> 对照广告 claim 和落地页证据
  -> 修复真实问题
  -> 做 URL、移动端、GEO、参数、页面披露和 claim/proof QA
  -> 准备申诉证据包
  -> 提交 appeal 或重新请求审核
  -> 跟踪结果并复盘到素材库、页面 brief、换链规则和任务日志
```

分工建议：

| 角色 | 负责内容 |
| --- | --- |
| Media buyer | 冻结投放、导出受影响对象、保存状态 |
| Creative/editor | 修改标题、描述、图片、business name、claim |
| Landing page owner | 修复页面证据、披露、速度、可访问性 |
| Tracking owner | 检查 tracking template、redirect chain、参数和最终页 |
| Compliance reviewer | 判断 policy topic、准备证据包和申诉文字 |
| Operator | 提交 review/appeal，记录结果和复盘 |

## 7. 申诉证据包模板

申诉证据包要能让外部审核者理解“问题是什么、改了什么、为什么现在合规”。建议字段：

| 字段 | 示例 |
| --- | --- |
| case_id | AR-REVIEW-2026-06-09-001 |
| platform | Google Ads |
| account_id | 仅记录内部别名或授权账号 ID，不保存 cookie |
| campaign/ad_group/ad/asset/keyword_id | 受影响对象 ID |
| policy_topic | Destination requirements / Misrepresentation / Editorial 等 |
| status_before | disapproved / eligible_limited |
| detected_at | 发现时间 |
| final_url | 广告后台 Final URL |
| expanded_url | 带 tracking template 和参数后的最终落地 URL |
| screenshots | 广告后台、Policy Manager、落地页、移动端截图 |
| claim_map | headline/description -> landing proof snippet |
| page_evidence | 联系方式、隐私政策、条款、价格、资质、披露 |
| change_summary | 修改了哪些广告、资产、页面、URL 或披露 |
| qa_results | HTTP、移动端、GEO、参数、跳转链、页面一致性 |
| appeal_text | 简短事实陈述，不写模板化抱怨 |
| reviewer | 内部复核人 |
| submitted_at/result_at | 提交和结果时间 |
| source_urls | 引用的政策和内部手册 URL |

申诉文字建议结构：

```text
我们理解该广告被标记为 [policy topic]。
受影响对象是 [ad/asset/final URL]。
我们已完成以下修复：
1. [具体修改]
2. [具体修改]
3. [页面或证据位置]
当前 Final URL 为 [URL]，广告承诺与页面内容一致。
附件/截图显示 [证据]。
请重新审核。
```

不要写：

- Please approve ASAP。
- 我们没有违规，但是没有解释和证据。
- 竞争对手也这样做。
- 我们已经换域名/换账号。
- 用户看不到这些问题。

## 8. 什么时候不该申诉

以下场景不应直接提交 appeal：

| 场景 | 正确处理 |
| --- | --- |
| 页面仍然不可达 | 先修复 URL、证书、服务器、移动端和地区访问 |
| 广告 claim 没有证据 | 修改 claim 或补充真实页面证据 |
| 只是换域名 | 先修复原始问题，换域名不能作为合规理由 |
| tracking 链仍会分流到不同页面 | 修复一致性，保留 expanded URL 证据 |
| 受限垂类缺少认证 | 先完成认证或停止该垂类 |
| 账号级暂停 | 按账号健康 SOP 处理，不用广告级 appeal 混淆问题 |
| 同模板多条广告同时拒登 | 先停模板，抽样修复，再小批量恢复 |

## 9. 套利团队最常见的拒登根因

### 9.1 创意生成过度优化 CTR

AI 或模板为了提高 CTR，容易生成“官方”“最佳”“保证”“免费”“限时”“无需资质”“立即领取”等强刺激 claim。短期看 CTR 变高，长期会提高拒登、低质量 lead、投诉、扣量和账号风险。

治理方法：

- creative brief 必须包含 allowed claims、blocked claims、proof snippets。
- 每条 headline 和 description 进入 claim/proof 审核。
- 高 CTR 素材必须看 RPV、bounce、投诉、拒登率和 lead reject。

### 9.2 换链接破坏目的地一致性

链接计划如果只看 EPC/RPV，容易把广告承诺切到不同主题、不同主体或不可达页面。Google 的目的地要求关注用户最终到达内容，tracking 中间层不是免责层。

治理方法：

- link rule 必须保存旧 URL、新 URL、变更原因、QA 结果和人工审批。
- 不允许“为过审临时切审核页”。
- 批量换 Final URL 前先小批量审核和回滚预案。

### 9.3 批量导入放大同一错误

Editor CSV、Bulk Upload 或 Scripts payload 可以提高效率，但也会把模板错误复制到大量对象。

治理方法：

- 上传前做 policy lint、claim review、URL QA 和 row-level preview。
- 先少量对象测试审核结果，再扩大导入。
- 保存每次 payload 版本和 Change history 证据。

### 9.4 Presell / advertorial 缺少披露

Native 或 advertorial 页面常见问题是像新闻、测评、官方指南，但没有清楚广告披露、商业关系、主体、联系方式和用户下一步会发生什么。

治理方法：

- 页面顶部和 CTA 附近保留广告/商业关系披露。
- 不伪装成独立媒体、官方通知或政府服务。
- 页面 claim 和 offer 页面条款一致。

## 10. 系统落地

当前系统已经具备这些承载点：

| 系统能力 | 对应审核治理 |
| --- | --- |
| Offer 管理 | 保存垂类、国家、语言、payout、目标 URL 和状态 |
| 落地页采集 | 保存 title、description、CTA、proof/review/price/form 摘要 |
| 创意生成 | 基于 offer 和落地页生成 headline/description |
| Claim 审核 | 提示 guarantee、official、free、discount、scarcity 等强 claim |
| Campaign draft | 保存投放草稿、关键词、预算、出价、广告结构 |
| Editor CSV / Scripts JSON 导出 | 做人工确认、预览、批量变更治理 |
| 广告审核案例 | 保存 policy topic、受影响对象、Final URL、expanded URL、证据 URL、修复摘要、申诉文字和状态 |
| 链接计划 | 做断链修复、合规 A/B、URL 变更审计 |
| 任务中心 | 做检查类任务、审批、执行日志和事故复盘 |
| 来源库 | 保存官方政策、开发者文档和行业资料 URL |

当前 V1 已实现 `ad_review_cases`，第一版仍然单团队，不做多租户：

```sql
CREATE TABLE ad_review_cases (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  offer_id BIGINT,
  campaign_draft_id BIGINT,
  creative_set_id BIGINT,
  object_type VARCHAR(32) NOT NULL,
  object_ref VARCHAR(180),
  policy_topic VARCHAR(255) NOT NULL,
  severity VARCHAR(16) NOT NULL,
  status VARCHAR(32) NOT NULL,
  final_url TEXT,
  expanded_url TEXT,
  finding TEXT NOT NULL,
  change_summary TEXT NOT NULL,
  evidence_urls JSON NOT NULL,
  appeal_text TEXT,
  reviewer VARCHAR(128),
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

后续可扩展更细数据表：

```sql
CREATE TABLE policy_decision_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  case_id BIGINT NOT NULL,
  raw_status VARCHAR(128),
  raw_policy_topic VARCHAR(255),
  source_url TEXT,
  screenshot_path TEXT,
  captured_at DATETIME NOT NULL
);

CREATE TABLE appeal_evidence_packages (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  case_id BIGINT NOT NULL,
  claim_map_json JSON,
  page_evidence_json JSON,
  change_summary TEXT,
  qa_results_json JSON,
  appeal_text TEXT,
  reviewer VARCHAR(128),
  submitted_at DATETIME,
  result_status VARCHAR(32),
  result_note TEXT
);

CREATE TABLE policy_fix_actions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  case_id BIGINT NOT NULL,
  action_type VARCHAR(64) NOT NULL,
  target_ref VARCHAR(128),
  before_value TEXT,
  after_value TEXT,
  reason TEXT,
  created_by VARCHAR(128),
  created_at DATETIME NOT NULL
);
```

执行边界：

- 系统可以生成证据包、检查清单、修复建议和导出 payload。
- 系统可以记录后台手工提交的结果。
- 系统不保存 Ads Cookie、浏览器 profile、session token。
- 系统不自动绕过登录、2FA、安全挑战或审核。
- 系统不自动创建/切换账号来处理拒登。
- 系统不生成 cloaking、补点击、刷展示或规避关联检测任务。

## 11. QA 清单

上线前检查：

| 检查项 | 通过标准 |
| --- | --- |
| Policy topic | 已明确可能触发的政策类型 |
| Claim/proof | 每条强 claim 有页面证据或已删改 |
| Final URL | HTTP 200、HTTPS 正常、移动端可访问 |
| Expanded URL | tracking 后最终页和广告承诺一致 |
| Display URL | 与实际域名和业务主体一致 |
| Page identity | 主体、联系方式、隐私、条款、披露清楚 |
| Sensitive vertical | 国家、认证、资质和受众限制已确认 |
| Bulk payload | CSV/Scripts payload 已预览，row-level 错误已处理 |
| Link rule | 换链理由、旧/新 URL、QA 和回滚点已保存 |
| Appeal package | 拒登后有截图、policy topic、修改记录和证据 |
| Incident review | 重复拒登会进入复盘，不继续扩量 |

## 12. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本系统完成形态 |
| --- | --- |
| 广告创意生成 | 生成后进入 Claim 审核和政策 QA |
| 广告优化 | 不只看 CTR/CPC，也看拒登率、受限率、lead reject、扣量和页面证据 |
| 自动投放 | 通过草稿、CSV、Scripts JSON、预览和人工确认承载，不做 Cookie 后台自动点击 |
| 换链接 | 通过 link rule、目的地一致性 QA 和人工审批承载，不做 cloaking |
| 审核后提交 | 通过 ad review case、证据包、状态跟踪和复盘承载 |
| 来源沉淀 | 官方政策、开发者文档和内部复盘进入 source library |

## 13. 信息来源 URL

- Google Ads Help, About the ad review process: https://support.google.com/google-ads/answer/1722120
- Google Ads Help, Fix a disapproved ad or appeal a policy decision: https://support.google.com/google-ads/answer/9338593
- Google Ads Help, Submit a campaign for policy review: https://support.google.com/google-ads/answer/9456683
- Google Ads Help, About Policy Manager: https://support.google.com/google-ads/answer/9675313
- Google Ads Policy, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Editorial requirements: https://support.google.com/adspolicy/answer/6021546
- Google Ads Policy, Text ad requirements: https://support.google.com/adspolicy/answer/6021630
- Google Ads Policy, Trademarks: https://support.google.com/adspolicy/answer/6118
- Google Ads Policy, Unacceptable business practices: https://support.google.com/adspolicy/answer/15938071
- Google Ads Policy, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads Policy, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads Policy, Financial products and services: https://support.google.com/adspolicy/answer/2464998
- Google Ads Policy, Healthcare and medicines: https://support.google.com/adspolicy/answer/176031
- Google Ads Policy, Gambling and games: https://support.google.com/adspolicy/answer/15132179
- Google Ads API, Policy support: https://developers.google.com/google-ads/api/support/policy
- Google Ads API, PolicyTopicEntry reference: https://developers.google.com/google-ads/api/reference/rpc/latest/PolicyTopicEntry
- Google Ads API, PolicySummary reference: https://developers.google.com/google-ads/api/reference/rpc/latest/PolicySummary
- Google Ads API, PolicyViolationKey reference: https://developers.google.com/google-ads/api/reference/rpc/latest/PolicyViolationKey
- Google Ads API, Change event: https://developers.google.com/google-ads/api/docs/change-event
