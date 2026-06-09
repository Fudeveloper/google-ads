# Cloaking 或审核页/用户页不一致研究

更新时间：2026-06-09

## 1. 范围

本文研究 cloaking、审核页和用户页不一致、最终 URL 切换绕审核的原理、风险、识别逻辑和合规替代方案。本文不提供 cloaking 规则、Bot 识别、分流代码、审核绕过或差异化落地页实现。

## 2. 原理解释

Cloaking 是根据访问者身份或环境展示不同内容。例如：

- 审核系统看到页面 A，真实用户看到页面 B。
- 搜索引擎看到信息页，用户看到 Offer 或广告堆叠页。
- 某些国家、设备、IP、User-Agent、Cookie 看到不同最终页面。

正常的个性化和本地化不等于 cloaking。关键区别在于：是否为了欺骗审核、搜索引擎、平台或用户，让平台看到的承诺和用户实际看到的内容不一致。

### 2.1 差异化页面的判断边界

不同用户看到不同页面并不必然违规。电商按地区显示价格、SaaS 按语言显示文案、页面做 A/B 测试、移动端使用不同布局，都可能是正常产品逻辑。判断是否进入 cloaking，核心看四个一致性：

- 广告承诺一致：广告说的服务、价格、身份、限制和页面实际一致。
- 目的地一致：审核、抓取和用户最终到达的业务目的相同。
- 访问条件一致：不同地区/设备看到的是同主题本地化，而不是合规页和违规页。
- 变更记录一致：URL、页面版本、跳转链和审核记录可追溯。

如果差异化规则的目的或效果是让平台看到一个页面、真实用户看到另一个业务，就应按 cloaking 风险处理。

### 2.2 链路一致性

Ads 套利链路常包含广告 Final URL、tracking template、联盟跳转、landing page、offer page 和收入端页面。合规链路要能解释每一步：

- 为什么需要跳转。
- 每个中转域名由谁控制。
- 最终页面是否与广告文案一致。
- 用户是否能看到真实主体、价格、条款、隐私和退出路径。
- 审核人员、抓取系统和普通用户是否能到达同一业务目的地。

换链接功能的安全边界不是“能不能自动换”，而是“换到哪里、为什么换、谁批准、是否仍然同主题同承诺”。因此，本系统只保留候选 URL、人工确认、变更理由和回滚记录，不保存任何按 Bot、IP、地区、设备、Cookie 或 Referer 隐藏分流的规则。

### 2.3 常见误区

- 误区一：审核页合规、用户页激进，所以“只是转化优化”。实际是审核和用户不一致。
- 误区二：联盟 Offer 经常失效，所以任何自动换链都合理。实际需要同主题、同承诺、可追溯。
- 误区三：只对某些国家展示不同内容就是本地化。实际要看是否隐藏了受限产品、价格、身份或风险。
- 误区四：中转层不直接展示内容，所以没有政策风险。实际最终目的地和跳转链仍会被审计。

### 2.4 Review / User Consistency Matrix

页面一致性不是要求所有用户看到完全相同像素，而是要求平台审核、普通用户和不同环境下看到的业务承诺一致：

| 维度 | 允许差异 | 高风险差异 |
| --- | --- | --- |
| 语言 | 同服务的本地化语言 | 审核看到教育页，用户看到博彩/金融/成人/受限 Offer |
| 地区 | 合法地区价格、库存、合规披露 | 受限地区隐藏页面，目标用户看到受限服务 |
| 设备 | 响应式布局、移动端简化 | 移动端跳到完全不同业务或下载页 |
| A/B 测试 | 同主题、同承诺、可归档版本 | 版本 B 隐藏费用、身份、风险或不同 Offer |
| 追踪跳转 | 保留参数、可解释 click tracker | 中转层隐藏真实 Final URL 或按 Bot 分流 |
| Offer 替换 | 同主题、同资格、同 disclosure 的备用 Offer | 审核后切到更激进、不相关或未披露 Offer |
| 合规披露 | 格式和位置可不同但内容一致 | 审核页有披露，用户页隐藏披露 |

判断原则：广告承诺、业务主体、价格/费用、资格限制、风险披露、隐私/consent 和最终用户任务必须一致。

### 2.5 URL / Page Version 生命周期

安全换链接需要把 URL 当作版本化资产：

```text
link_change_request
  -> current_url_snapshot
  -> candidate_url_snapshot
  -> redirect_chain_qa
  -> claim / disclosure / offer consistency review
  -> manual approval
  -> scheduled change
  -> post-change crawl / screenshot / metrics check
  -> rollback or close
```

每次变更至少要保存：

| 证据 | 用途 |
| --- | --- |
| current_url / candidate_url | 新旧 URL 是否同主题同承诺 |
| expanded_final_url | 实际到达地址 |
| redirect hops | 中转链是否透明、参数是否保留 |
| page snapshot / hash | 版本留痕和争议证据 |
| mobile / desktop check | 设备差异是否只是布局差异 |
| geo / language check | 本地化是否合理，不隐藏受限内容 |
| claim / disclosure review | 广告承诺、费用、资格、风险披露一致 |
| approval / rollback | 谁批准、何时生效、如何恢复 |

这是一套 QA 和证据流程，不是自动寻找审核系统差异或构造分流规则。

### 2.6 A/B 测试、本地化和 Cloaking 的边界

| 场景 | 安全条件 | 进入 cloaking 风险的条件 |
| --- | --- | --- |
| A/B 测试 | 同 Offer、同 claim、同 disclosure，随机或实验平台透明 | 对审核/Google 展示版本 A，对用户展示违规版本 B |
| 本地化 | 同业务目的，只翻译语言、币种、合法地区条款 | 用地区隐藏政策限制、费用或受限产品 |
| 断链修复 | 404/5xx 修复到同主题替代页 | 修到不相关或更激进 Offer |
| Tracking update | 参数或 tracker 变更不改变最终内容 | tracker 根据 Bot/IP/UA/Cookie 改最终页 |
| Offer cap fallback | 同主题、已审核、同 consent/disclosure 范围 | cap 满后把用户卖到未披露垂类 |

只要规则的目的或效果是“让审核看到一个合规故事，让真实用户看到另一个业务”，就应标记为 cloaking 风险。

### 2.7 Destination Consistency Score

建议在链接计划或风险审计里使用一致性评分：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| Ad promise match | 25 | 广告文案、关键词、页面 H1/CTA 和 Offer 是否一致 |
| Final URL transparency | 20 | display/final/expanded URL、redirect chain 是否可解释 |
| Review/user parity | 20 | 审核、普通用户、移动/桌面、目标 geo 是否同业务 |
| Disclosure parity | 15 | 费用、身份、风险、privacy/consent 是否一致 |
| Version evidence | 10 | snapshot、hash、approval、rollback 是否存在 |
| Source / complaint risk | 10 | 投诉、拒登、扣量、buyer reject 是否关联该 URL |

低分动作不是隐藏链路，而是暂停、修页面、补披露、回滚或重新审核。

## 3. 行业诉求

套利团队可能想用 cloaking：

- 提高广告审核通过率。
- 隐藏真实 Offer。
- 审核后切换到更激进页面。
- 对不同地区展示不同变现页面。
- 避免某些页面被平台或广告主看到。

这些诉求直接指向审核规避。

## 4. 平台政策和风险

Google Search Central 的 spam policies 将 cloaking 定义为向用户和搜索引擎展示不同内容。Google Ads Advertising network abuse 政策也提到 cloaking、bridge/gateway 目的地、试图规避审核系统等问题。

风险：

- 广告拒登。
- 账号限制。
- 域名信任下降。
- 用户投诉。
- 联盟拒付。
- 多账号关联处置。

## 5. 识别逻辑

平台可以通过多种方式识别：

- 多地区、多设备、多 User-Agent 访问。
- 审核前后重复抓取。
- 用户投诉和页面行为异常。
- 跳转链路变化。
- 最终 URL 与显示 URL 不一致。
- 广告文案和落地页主题不一致。
- JavaScript 或服务端规则导致内容分歧。

识别重点不是“用了跳转就是违规”，而是“是否让审核看到的内容和用户实际看到的内容不一致”。

系统只沉淀高层 QA 和风险信号，不保存或推导可用于规避审核的识别规则：

| 信号 | 解释 | 系统动作 |
| --- | --- | --- |
| expanded URL 与记录不一致 | 跳转链或 Final URL 被动态改变 | 停止换链，跑 redirect QA |
| mobile / desktop 业务不同 | 不是响应式布局，而是不同 Offer | 风险审计 high |
| geo 看到受限内容差异 | 可能是地区规避而非本地化 | 检查政策和 disclosure |
| 审核后短期内切 URL | 可能规避审核 | 需要变更理由、审批和截图 |
| 中转域不可解释 | 可能隐藏最终目的地 | 绑定 source URL 和 owner |
| 用户投诉“不是广告说的内容” | 广告承诺和页面不一致 | 停投、回滚、复盘 |

## 6. 合规替代方案

允许和推荐：

- 透明 A/B 测试。
- 同主题、同承诺页面版本。
- 已审核 URL 之间的断链修复。
- UTM 更新。
- 页面版本归档。
- 每次 URL 变化保留原因、审核人和时间。
- Link checker / redirect QA。
- 页面截图、HTML hash、mobile / desktop 检查。
- Final URL、tracking template、Final URL suffix 和 ValueTrack 参数 QA。

不建议：

- 审核页和用户页不同。
- 根据 Bot/地区/设备切换到不相关内容。
- 广告承诺与最终页面不一致。
- 审核通过后切换到违规 Offer。

合规换链接决策表：

| 换链原因 | 是否可接受 | 必要证据 |
| --- | --- | --- |
| 原 URL 404 / 5xx | 可接受 | 错误截图、候选 URL 同主题、回滚记录 |
| UTM / subid 更新 | 可接受 | 参数 diff、expanded URL 不变 |
| 同主题 A/B 测试 | 可接受 | 实验版本、同 claim/disclosure、样本窗口 |
| Offer cap fallback | 高审慎 | 同垂类、同 consent、同披露、buyer terms |
| 审核后换激进页面 | 不接受 | 记录 high risk，拒绝 |
| 按 Bot/IP/UA/Cookie 分流 | 不接受 | 记录 high risk，拒绝 |

## 7. 本系统落地

系统实现：

- 链接计划。
- 候选 URL。
- 人工确认轮换。
- 审计日志。
- `/risk-audits` 记录 cloaking、destination mismatch、隐藏目的地和审核规避风险。
- 链接计划禁止 unsafe name / URL / description 语义进入执行。

系统不实现：

- Bot 识别。
- 地区/设备/IP cloaking。
- 审核绕过分流。
- 自动最终 URL 替换绕审核。
- 审核页 / 用户页双版本配置。
- 按 Bot、IP、User-Agent、Cookie、Referer 或账号状态分流。

建议后续扩展实体表：

| 表 | 用途 | 禁止字段 |
| --- | --- | --- |
| `destination_consistency_reviews` | ad promise、final URL、page snapshot、decision | bot routing rule |
| `url_version_snapshots` | URL、HTML hash、screenshot hash、timestamp | hidden user page |
| `redirect_chain_runs` | hop、status、parameter retention、expanded URL | cloaking split logic |
| `link_change_approvals` | reviewer、reason、rollback、evidence | review/user branch |
| `destination_incidents` | complaint、disapproval、mismatch、root cause | bypass recipe |

## 8. ADXKit 对应点和完成形态

ADXKit 公开页面提到“换链接”“设置频率”“采集最终到达页”“Worker 转发”等能力。套利团队确实需要链接维护：Offer 失效、联盟 tracking 参数变化、UTM 更新、A/B 测试、地区页面切换都会发生。但链接维护和 cloaking 的边界在于：广告承诺、审核页面、最终页面、用户看到的内容是否保持一致。

合规换链接的判断标准：

- 新旧 URL 属于同一主题、同一承诺、同一业务目的。
- 最终页面可被正常访问，不依赖隐藏规则。
- 用户看到的页面和审核、抓取、平台检查看到的页面一致。
- 变更原因清晰，例如断链修复、UTM 更新、同主题 A/B 测试。
- 变更有人工确认、时间、责任人和回滚方案。

高风险换链接信号：

- 审核时展示信息页，用户点击后展示不相关 Offer。
- 根据 IP、User-Agent、Cookie、地区、设备、Referer 展示不同业务内容。
- 审核通过后自动切换到更激进页面。
- 广告文案承诺和最终页面主题不一致。
- 使用中转层隐藏真实最终目的地。

本项目完成形态：

- `link_rules` 保存当前 URL、候选 URL、轮换原因、人工确认要求和轮换日志。
- “人工确认轮换”只移动候选 URL，不生成隐藏分流规则。
- 风险审计可记录 cloaking、目的地不一致和审核规避风险。
- 来源库记录 Google Search spam policies、Google Ads destination requirements、Circumventing systems。

验收标准：

- 链接计划默认 `require_manual_review=True`。
- 系统没有 Bot 识别、IP/地区/设备差异化分流或审核页/用户页双版本配置。
- 每次轮换写入审计日志。
- 文档明确区分 A/B 测试、本地化与 cloaking。

## 9. 功能拆解和安全完成清单

把“cloaking / 审核页和用户页不一致”拆成业务诉求后，可安全交付的是链接治理、页面版本和透明测试，而不是隐藏分流：

| 子能力 | 行业想解决的问题 | 本项目安全完成形态 |
| --- | --- | --- |
| Offer 失效修复 | 原链接 404、跳转错误、联盟参数变化 | `/links` 记录当前 URL、候选 URL、变更理由和人工确认 |
| A/B 测试 | 同主题页面需要比较转化和收入 | 仅允许同承诺、同业务目的、可追溯页面版本 |
| UTM/追踪更新 | 参数调整不应破坏最终页面 | 链接计划记录追踪 URL、候选 URL 和轮换日志 |
| 页面一致性检查 | 广告承诺、展示 URL、Final URL 和最终页面要一致 | 落地页审计、链接文档、风险审计 |
| 事故回滚 | 换链后出现拒登或投诉要能恢复 | 审计日志保留变更前后、时间、原因和责任人 |

安全验收点：

- `link_rules` 默认要求人工确认，不自动按 Bot、地区、设备、IP、Cookie、Referer 或 User-Agent 分流。
- 候选 URL 必须是同主题、同承诺、同业务目的，且能被普通访问和审核访问看到一致内容。
- 系统不保存审核页/用户页双版本配置，不生成 cloaking 规则。
- 风险审计中出现“审核通过后切换”“隐藏真实 Offer”“只给 Google 看合规页”等表述时默认 high。
- A/B 测试文档要求广告承诺一致、页面版本可归档、指标按真实用户样本评估。

### 9.1 审计字段设计

| 字段 | 说明 |
| --- | --- |
| capability | 固定为 `cloaking_review_user_page_mismatch` |
| trigger | link change、destination mismatch、disapproval、user complaint、review/user mismatch claim |
| ad_scope | account、campaign、ad group、ad、keyword、final URL |
| url_scope | current_url、candidate_url、expanded_final_url、tracking_template |
| stated_reason | 断链修复、UTM 更新、A/B、fallback、审核后切换、隐藏 Offer |
| consistency_findings | ad promise、offer、price、disclosure、identity、geo/device parity |
| evidence | screenshot、HTML hash、redirect hops、policy URL、approval log |
| safe_path | rollback、page fix、link QA、manual approval、stop campaign |
| decision | rejected、approved_manual、rollback、quarantine、incident_response |
| reviewer | 审核人 |
| follow_up | 更新链接计划、修 tracking、申诉证据、素材回滚、风险培训 |

### 9.2 SOP

1. 任何换链接需求先记录 current URL、candidate URL、变更理由和负责人。
2. 跑 expanded URL 和 redirect chain QA，确认参数保留和最终目的地一致。
3. 对比广告文案、关键词、页面 H1/CTA、费用、资格、隐私/consent 和风险披露。
4. 检查 mobile / desktop、目标 geo / language、普通访问和审核访问是否同业务目的。
5. 保存页面 snapshot / hash、审批人、时间和回滚计划。
6. 如果发现审核页/用户页不同、隐藏真实 Offer、按 Bot/IP/UA/Cookie 分流，立即拒绝并创建 high 风险审计。
7. 换链后监控拒登、投诉、buyer reject、RPV 和 redirect error，必要时回滚。

### 9.3 通过/拒绝例子

| 需求 | 判断 | 处理 |
| --- | --- | --- |
| 原 landing 404，换到同主题同披露页面 | 可通过 | 保存 QA、审批和回滚 |
| 更新 UTM，不改变 expanded Final URL | 可通过 | 参数 diff 和测试记录 |
| 同一 Offer 的 headline A/B 测试 | 可通过 | 版本归档和一致性检查 |
| 审核通过后切到更高 payout 不相关 Offer | 拒绝 | high risk，停止换链 |
| Googlebot 看合规页，用户看受限页 | 拒绝 | high risk，cloaking |
| 只在移动端跳到 app install / sweepstakes | 拒绝或重审 | 检查广告承诺和披露 |

## 10. 信息来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Search Central, Spam policies | https://developers.google.com/search/docs/essentials/spam-policies | 支撑 cloaking 是向用户和搜索引擎展示不同内容以操纵或误导的做法 |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑向 Google 和用户展示不同内容、隐藏真实目的地、规避审核和政策执行的红线 |
| Google Ads Policy, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑 cloaking、bridge/gateway destinations、低价值目的地和广告网络滥用风险 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目的地可达、页面体验和广告承诺一致性 |
| Google Ads Scripts, Link Checker solution | https://developers.google.com/google-ads/scripts/docs/solutions/link-checker | 支撑链接检查应是 QA 和提醒，而不是分流或隐藏目的地 |
| Google Ads Help, Set up tracking with ValueTrack parameters | https://support.google.com/google-ads/answer/6305348 | 支撑 tracking 参数应服务归因，不改变用户最终业务目的 |
| Google Ads Help, About tracking in Google Ads | https://support.google.com/google-ads/answer/6076199 | 支撑 Final URL、tracking template 和 URL options 的追踪边界 |
| ADXKit homepage | https://adxkit.com/ | 仅用于记录其公开页面提到换链接、最终到达页和 Worker 等功能话术 |
