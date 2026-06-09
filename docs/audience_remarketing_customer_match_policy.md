# 受众定向、再营销与 Customer Match 合规手册

更新时间：2026-06-08

本文说明 Google Ads 受众定向、再营销、Customer Match、PMax audience signals、optimized targeting 和 Personalized Ads 政策在 Ads 套利业务中的使用边界。本文不提供用户名单抓取、未经授权数据上传、敏感人群推断、规避个性化广告限制或 Customer Match 自动同步实现。

## 1. 为什么受众控制重要

套利团队常把重点放在 CPC、RPV、ROI 和链接轮换上，但受众控制会直接影响三个结果：

- 买量质量：同一关键词或素材，在不同受众、再营销名单和扩量设置下，CPC、CVR、lead 质量可能完全不同。
- 政策风险：金融、健康、债务、住房、就业、信贷、药品、博彩等垂类很容易触发 Personalized Ads 或受限垂类规则。
- 数据闭环：PMax、Demand Gen、Display、YouTube 和 Search 的自动化优化会使用转化、页面、素材、受众信号和第一方数据。如果输入低质 lead 或不合规名单，系统会朝错误方向学习。

受众不是“越精准越好”。在套利业务里，受众的核心问题是：这些人为什么与 Offer 有真实、合规、可解释的关系；数据来源是否有同意；广告内容是否暗示掌握了用户的敏感身份或困境。

## 2. Audience Segment 基础

Google Ads 使用 audience segments 统一描述多种受众能力。常见类型包括：

| 类型 | 业务含义 | 套利使用边界 |
| --- | --- | --- |
| Affinity | 长期兴趣和生活方式倾向 | 适合较宽泛内容站或品牌型测试，不适合证明强购买意图 |
| In-market | 正在研究或计划购买某类产品 | 适合 Offer 初测，但要防止垂类和广告承诺错配 |
| Detailed demographics | 教育、房产、父母阶段等广义人口特征 | 住房、就业、信贷等场景要特别检查限制 |
| Custom segments | 用关键词、URL、app 描述理想受众 | 不要用敏感身份、健康困境、负面财务状态等词构建 |
| Your data segments | 过去访问、app 用户、视频观看、转化者等再营销数据 | 依赖 tag、consent、隐私披露和名单质量 |
| Customer Match | 使用客户直接提供的线上/线下数据 | 只允许第一方、合规收集、可披露、可授权的数据 |

行业误区：

- 把 in-market 当成强购买承诺。它只是平台估计的意图，不保证转化。
- 把 custom segments 当关键词替代品。它更像受众描述，不等于 Search exact match。
- 把再营销名单当“低价流量池”。如果名单来自低质点击或误导页面，再营销只会放大低质样本。
- 把 Customer Match 当第三方名单上传器。Customer Match 的基础是用户直接向你分享的数据和明确的数据使用权。

## 3. Targeting、Observation、Signals 和 Expansion

受众相关设置经常被混用，必须分清：

| 概念 | 含义 | 对套利优化的影响 |
| --- | --- | --- |
| Targeting | 限定广告主要触达的人群或内容范围 | 会收窄流量，可能提高相关性，也可能让样本太小 |
| Observation | 观察某受众表现，不限制覆盖 | 适合 Search/Shopping 初期观察 RPV、CVR、lead 质量 |
| Audience signals | 给自动化系统的学习提示 | 在 PMax 里不是硬性定向，系统可触达信号外人群 |
| Optimized targeting | 系统在手动信号之外寻找更可能转化的人群 | 可能带来扩量，也可能把低质转化放大 |
| Exclusions | 排除已有客户、低质来源、无关名单或合规禁区 | 比盲目加受众更重要，尤其在 lead 和再营销场景 |

套利测试建议：

1. Search 先用 Observation 观察受众差异，不急着收窄。
2. Display / Demand Gen / Video 要把 optimized targeting 是否开启记录进测试表。
3. PMax 的 audience signals 只当训练输入，不当确定性人群控制。
4. 对高风险 Offer，先审查垂类是否允许 advertiser-curated audiences，再决定是否使用再营销、Customer Match、custom segments。

## 4. Remarketing / Your Data Segments

Google Ads 里 “remarketing” 术语逐步被 “your data” 或 “your data segments” 替代。原理是：用户访问网站、app、视频或与业务互动后，被加入符合条件的 segment，后续广告可用这些 segment 做触达、观察、排除或信号。

再营销在套利里的正确用途：

- 排除已转化用户，减少重复 lead。
- 观察不同页面访问者的后续 RPV 和 lead quality。
- 对高质量内容访问者做同主题后续触达。
- 对低质来源、误点来源或投诉来源做排除。

再营销的风险：

- 页面没有隐私政策、Cookie/Consent 披露或 tag 说明。
- 用户只是被误导点击，并没有真实兴趣。
- 用健康、债务、法律、身份等敏感行为构建名单。
- 广告文案暗示“我们知道你有某个疾病、债务、身份或个人困境”。
- 跨 Offer 混用名单，例如把贷款 lead 名单用于无关金融或保险 Offer。

## 5. Customer Match

Customer Match 允许广告主使用客户直接提供的线上/线下数据触达或再触达客户。关键不是“能不能上传”，而是名单来源、同意、披露、账号资格和用途是否合规。

### 5.1 数据来源原则

可接受方向：

- 用户在你的网站、app、线下门店、表单、账户、订阅或会员计划中直接提供信息。
- 隐私政策披露会把数据分享给第三方用于广告测量或广告服务。
- 在法律或 Google 政策要求时取得同意。
- 通过 Google 批准的 API 或界面上传。

高风险方向：

- 购买、租用、抓取或拼接第三方名单。
- 从联盟、lead buyer、外包团队拿到但没有清楚授权的数据。
- 上传儿童、未成年人或面向儿童站点收集的数据。
- 上传与敏感类别相关的转化或名单。
- 用过窄地理、人口或行为条件把名单压成非常小的人群。

### 5.2 Hashing 和匹配

Customer Match 过程里，email、phone、first name、last name 等私人客户数据会以 SHA256 等方式哈希或被 Google 处理。哈希不是合规豁免：即使数据被哈希，上传前仍然需要第一方来源、隐私披露、同意和用途合法。

套利团队常见误区是“哈希后就不是个人数据”。正确理解是：哈希降低传输和匹配暴露风险，但不能改变数据来源和使用权问题。

### 5.3 本系统边界

当前系统不实现：

- Customer Match 文件上传。
- 客户名单存储。
- PII 字段、email、phone、姓名、地址存储。
- CRM 自动同步。
- 跨 Offer 名单拼接。

当前系统只记录：

- 是否计划使用受众或再营销。
- Offer 垂类是否涉及 Personalized Ads 限制。
- 风险审计和来源 URL。
- 用指标导入评估真实表现，而不是上传名单扩量。

## 6. Personalized Ads 敏感类别

Personalized Ads 政策把某些兴趣、身份、困境和机会类场景视为敏感。套利团队尤其要注意：

| 类别 | 风险例子 | 安全处理 |
| --- | --- | --- |
| Health / medical | 减肥药、处方药、疾病治疗、医疗器械 lead | 检查医疗政策、认证和是否允许个性化定向 |
| Negative financial status | 债务、低信用、破产、紧急贷款 | 不用困境标签或名单定向用户 |
| Identity and belief | 种族、宗教、政治、性取向、边缘群体 | 不构建、不推断、不暗示掌握这些身份 |
| Relationship hardship | 离婚、分居、情感困境 | 不用个人困境做再营销或 custom segment |
| Adult / sexual interests | 成人、性相关兴趣 | 避免个性化定向和敏感数据使用 |
| Housing / employment / credit | 房屋买卖租赁、招聘、信贷和贷款 | 美国/加拿大场景要检查 HEC 定向限制 |
| Minors / child-directed | 未满 13 岁或儿童导向站点收集数据 | 不上传、不建名单、不做个性化广告 |

判断规则：

- 广告内容和落地页是否属于敏感类别。
- 使用的是 Google 预定义受众，还是广告主自己上传/构建的受众。
- 受众是否来自用户行为、客户名单、custom segment 或再营销。
- 广告是否暗示掌握了用户的敏感信息。

敏感垂类并非一定不能投，但不能把“用户的敏感状态”当作个性化定向依据。

## 7. PMax Audience Signals

Performance Max 的 audience signals 是给 Google AI 的提示，不是硬性定向。Google 官方说明 PMax 可在信号之外寻找更可能转化的人群，以满足投放目标。

套利场景里的关键风险：

- 如果 primary conversion 是低质量 lead，PMax 会学习“更容易产生低质 lead 的人群”。
- 如果 audience signal 混入低质再营销、误点访客或不合规 Customer Match，系统可能放大错误信号。
- 如果 Final URL expansion、asset group、URL exclusions 和 brand exclusions 没有治理，PMax 可能把预算带到不符合套利模型的页面或品牌词。
- 如果只看短期 CPA，不看 buyer feedback、scrub、finalized revenue，会误以为 PMax 正 ROI。

PMax audience signals 使用原则：

1. 先确认 conversion action 是真实、可回款、可对账的事件。
2. 优先输入高质量页面访问者、真实客户、已验证 high-quality lead，而不是全部流量。
3. 对敏感垂类先做 Personalized Ads 和 Customer Match 政策审计。
4. 报表里同时看 campaign、asset group、channel、search term insights、placement/URL 控制和最终收入。

## 8. Optimized Targeting 和扩量风险

Optimized targeting 会在手动选择的受众之外寻找更可能转化的人群；在 Display、Video、Demand Gen 等场景里，系统可能使用页面、素材、已有信号和转化目标进行扩展。

对套利业务来说，optimized targeting 的风险不在“扩量”本身，而在目标函数：

- 如果转化事件太浅，例如 click-out、form start、无效 lead，系统会优化浅层行为。
- 如果 revenue 回传滞后，短期 CPA 可能误导扩量。
- 如果来源质量没有隔离，系统会把低质来源当作可扩展模式。
- 如果 Offer 属于敏感垂类，扩量前需要确认受众能力是否允许使用。

建议把 optimized targeting 作为实验变量：

- 开启/关闭要记录。
- 单独看 spend、CPC、CVR、RPV、lead reject rate、scrub、finalized revenue。
- 不要和素材、落地页、国家、预算同时大改。
- 一旦出现高量低质，先检查 conversion action 和 traffic source，不要继续放量。

## 9. 套利场景风险清单

上线前检查：

- Offer 是否涉及健康、金融困境、债务、住房、就业、信贷、药品、博彩、成人或儿童相关内容。
- 是否计划使用 Customer Match、再营销、custom segments、lookalike/类似扩展或 advertiser-curated audiences。
- 数据是否第一方收集，是否有隐私政策、同意、退订和数据删除流程。
- 是否存在跨 Offer、跨广告主、跨联盟的名单混用。
- 是否使用过窄地理、年龄、性别、婚姻、父母状态、邮编或名单条件。
- 广告文案是否暗示知道用户的疾病、债务、身份、婚姻、信仰或困境。
- PMax / optimized targeting 的 primary conversion 是否真实代表可回款价值。
- 是否把再营销低成本误判为新客增长。

停用条件：

- 名单来源说不清。
- 没有隐私披露或同意依据。
- 垂类属于敏感类别却计划使用 advertiser-curated audiences。
- Customer Match 只是为了上传购买名单或联盟名单。
- PMax 扩量后 lead reject、scrub、投诉或扣量升高。

## 10. 系统落地

当前系统已经支持：

- `/offers` 记录垂类、国家、政策备注和目标 URL。
- `/campaigns` 记录投放草稿、预算、渠道和 Final URL。
- `/metrics/import` 导入真实花费、点击、转化和收入。
- `/optimization` 按 ROI、RPV、CPC 等指标给出优化建议。
- `/risk-audits` 记录受众、再营销、Customer Match、Personalized Ads 风险。
- `/sources` 记录 Google Ads 官方来源、政策和开发文档。

当前系统不做：

- PII / customer list 存储。
- Customer Match 上传。
- CRM 同步。
- 自动创建或同步再营销名单。
- 敏感受众推断。

安全扩展方向：

- 给 Offer 增加“是否使用受众/再营销/Customer Match”的审计字段。
- 给 Campaign 草稿增加“audience_mode: observation / targeting / signal / exclusion”的备注字段。
- 在风险审计里新增 `audience_remarketing_customer_match_policy` 能力类型。
- 未来若接入官方 API，只上传经过人工审批、来源清楚、同意完整、非敏感的数据，并记录哈希前字段清单和审批证据；第一版不实现。

## 11. QA 清单

| 检查项 | 放行标准 |
| --- | --- |
| 垂类政策 | 不属于禁投或受限未认证类别；敏感类已审查 Personalized Ads |
| 数据来源 | 第一方直接收集，来源、时间、同意和隐私披露可证明 |
| Customer Match | 账号资格、名单规模、更新周期、敏感类别和用途已审查 |
| 再营销 | tag、consent、隐私政策、名单含义、排除逻辑清楚 |
| PMax signals | 只作为提示，不作为硬性定向；conversion action 质量已验证 |
| Optimized targeting | 作为实验变量记录，能按真实收入和 lead quality 复盘 |
| 文案 | 不暗示知道用户敏感身份、困境、健康或财务状态 |
| 审计 | 来源 URL、处理方案、责任人和复盘记录进入 `/risk-audits` |

## 12. 信息来源 URL

- Google Ads, About audience segments: https://support.google.com/google-ads/answer/2497941
- Google Ads, About "Targeting" and "Observation" settings: https://support.google.com/google-ads/answer/7365594
- Google Ads, About audience segments in Audience manager: https://support.google.com/google-ads/answer/7558048
- Google Ads, About Customer Match: https://support.google.com/google-ads/answer/6379332
- Google Ads, Customer Match policy: https://support.google.com/google-ads/answer/6299717
- Google Ads, About the customer matching process: https://support.google.com/google-ads/answer/7474263
- Google Ads, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads, Personalized advertising policy: https://support.google.com/adspolicy/answer/143465
- Google Ads, Housing, employment, and credit FAQ: https://support.google.com/adspolicy/answer/9997418
- Google Ads, About audience signals for Performance Max campaigns: https://support.google.com/google-ads/answer/14530785
- Google Ads, About Performance Max campaigns: https://support.google.com/google-ads/answer/10724817
- Google Ads, About optimized targeting: https://support.google.com/google-ads/answer/10537509
- Google tag, Consent mode overview: https://developers.google.com/tag-platform/security/concepts/consent-mode
