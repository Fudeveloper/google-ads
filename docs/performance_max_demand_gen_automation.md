# Performance Max / Demand Gen 自动化流量与套利风险手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何理解 Performance Max（PMax）、Demand Gen、Final URL expansion、Search themes、Audience signals、Asset groups、Brand exclusions、channel performance、placement report、optimized targeting、自动化素材组合和转化价值回传。目标是让团队在使用 Google AI 扩量时保留可解释性和止损边界，而不是把不透明自动化流量当成稳定套利收入。

## 1. 为什么自动化 Campaign 对套利既有价值也危险

PMax 和 Demand Gen 的共同点是：系统会使用目标、素材、页面、受众信号和历史转化，在多个库存或视觉场景里寻找可能转化的用户。

这对套利有价值：

- 可以扩大 Google Ads 库存覆盖。
- 能利用素材、页面和转化信号寻找新流量。
- 可能比手动关键词更快找到边缘意图。
- 可在 YouTube、Discover、Gmail、Display、Search、Maps 等场景获得增量。

但风险同样高：

- 流量来源和 query 透明度低于标准 Search。
- PMax 可能吃掉品牌词、再营销或原本会自然转化的用户。
- Final URL expansion 可能把用户送到不适合套利目标的页面。
- Audience signals 是提示，不是硬性定向边界。
- 自动化会放大错误 conversion action 和低质量 value feedback。
- 素材组合可能产生和页面证据不一致的承诺。
- Demand Gen / Display / YouTube 流量可能带来高点击低收入、低意图或延迟转化。

所以自动化 Campaign 的核心不是“开不开”，而是能否证明：新增花费带来了可收款增量，而不是吃掉已有需求或制造低质量转化。

## 2. 核心对象

| 对象 | 作用 | 套利团队要理解什么 |
| --- | --- | --- |
| Performance Max | 单一 campaign 覆盖多个 Google Ads 渠道 | 自动化强，控制和可解释性要靠报表和排除 |
| Demand Gen | 面向 YouTube、Discover、Gmail 等视觉/需求生成场景 | 更依赖素材、受众和页面承接 |
| Asset group | PMax 中素材、受众信号和 URL 组合单元 | 应按 Offer、意图、国家、页面版本拆分 |
| Audience signals | 给自动化系统的受众提示 | 不是硬性 targeting，不能当合规边界 |
| Search themes | 告诉 PMax 相关搜索主题 | 是提示，不等于只投这些查询 |
| Final URL expansion | 自动选择更相关 landing page | 可能扩到不适合的 URL，需要 exclusions/page feed |
| Brand exclusions | 控制品牌相关 Search/Shopping 覆盖 | 用于减少品牌/竞品/合作方混淆 |
| Channel performance report | 看 PMax 在不同渠道表现 | 判断钱是否跑到低质量库存 |
| Placement report | 查看 PMax 展示位置 | 用于排查 Display/YouTube/partner 质量 |

## 3. PMax 适用与不适用场景

适合测试：

- 已有清晰 conversion action 和 value feedback。
- 页面、Offer、国家、语言和转化质量稳定。
- 有足够素材和页面证据支撑不同渠道展示。
- 能按 finalized / paid revenue 对账。
- 能接受一段学习期和不完全透明的报表。

不适合冷启动：

- 没有可靠转化或转化价值。
- 只有 submitted lead，没有 approved / paid 反馈。
- 页面质量、政策、站点审核或 tracking 还不稳定。
- Offer 只能接受非常窄的关键词或地区。
- 敏感垂类、品牌条款、竞品词限制很严格。
- 团队无法承受自动化跑偏带来的预算损失。

套利团队常见失败，是把 PMax 用在“还没弄清楚真实 RPV 的新 Offer”，然后系统学到的是容易提交、低质量、不可收款的用户。

## 4. Final URL Expansion 与 URL 控制

Final URL expansion 会让系统根据用户意图，把用户送到最终 URL 之外更相关的页面。它可能提高覆盖，也可能破坏套利链路。

风险：

- 用户被送到未审核、未本地化或不适合该 Offer 的页面。
- tracking template / final URL suffix / postback 参数丢失。
- 页面主题和广告承诺不一致。
- 站点内低质量或薄页面被自动选中。
- 不同国家/语言混用页面，导致 bad geo 或拒付。

控制方法：

- 使用 URL exclusions 排除不应投放的页面。
- 使用 page feed 或 curated URL list 控制可用 URL。
- 按 asset group 绑定主题、国家、语言和页面版本。
- 变更前后保存 expanded landing page 和 channel report。
- 对 sensitive vertical、lead gen、affiliate 页面，默认更严格控制 URL。

不要把 Final URL expansion 当作换链接或 cloaking 工具。用户、审核和平台看到的业务目的必须一致。

## 5. Search Themes 和 Brand Exclusions

Search themes 可以给 PMax 提供额外主题提示，帮助系统理解用户可能使用的词语。它不是关键词匹配，也不是硬性只投这些词。

使用原则：

- Search themes 应来自真实 keyword research、search terms、页面内容和 Offer intent。
- 不放品牌词、竞品词、官方词，除非 Offer 条款和政策允许。
- 不用误导、敏感、夸大或和页面不一致的主题诱导系统扩量。
- Search themes 变化要和 search term insights、channel performance、paid revenue 一起复盘。

Brand exclusions 用于降低 PMax 在 Search/Shopping 中覆盖某些品牌词的风险。对套利团队尤其重要：

- 避免吃掉已有品牌流量，误判为 PMax 增量。
- 避免触发 Offer 的 no brand bidding / no competitor bidding 条款。
- 避免用户误以为页面是官方或授权渠道。
- 让 prospecting 和 brand capture 的预算分开。

## 6. Audience Signals 不是硬性定向

Audience signals 是给自动化系统的提示，帮助它更快找到可能转化的用户。它不等同于传统严格定向。

套利风险：

- 系统可能超出初始受众寻找转化。
- Remarketing 信号可能导致 PMax 捕获已经会转化的用户。
- Customer Match / your data segments 需要 consent、隐私披露和数据来源合规。
- 敏感垂类不能用健康、金融困境、身份特征等敏感信号做个性化广告。

使用建议：

- 区分 prospecting、remarketing、customer list 和 in-market 信号。
- 不把敏感词、诊断、债务困境、身份或健康状况作为受众信号。
- 用排除、brand exclusions、geo/language、URL 控制和 conversion value 共同约束。
- 把 PMax 的结果和非 PMax Search、GA4、CRM/buyer paid revenue 对账。

## 7. Asset Groups、素材和 Claim 风险

PMax 和 Demand Gen 都高度依赖素材。素材越多，组合越复杂，越需要 Claim / Proof 审核。

Asset group 设计：

| 拆分方式 | 适合 |
| --- | --- |
| Offer / product | 不同 payout、页面和资格 |
| Intent | 信息型、比较型、购买型、lead 型 |
| Country / language | 本地化页面和政策差异 |
| Page version | 不同 landing page 证据和 CTA |
| Audience angle | 不同用户问题、但不涉及敏感身份 |

风险：

- headline 和 image 组合后产生页面没有证明的承诺。
- 视频或图片暗示官方、保证、前后对比、医疗/金融结果。
- Demand Gen 素材像内容推荐，容易标题党。
- 自动生成或自动增强素材和落地页内容不一致。

所有素材都要进入 Claim / Proof 审核，不因为系统自动组合就放弃人工边界。

## 8. Demand Gen 的特殊风险

Demand Gen 面向更多视觉和内容消费场景，用户意图通常弱于 Search。套利团队需要重新定义成功指标：

```text
impressions
clicks
engaged sessions
offer clicks
qualified leads
approved / paid revenue
assisted conversions
```

风险点：

- 高点击低收入，尤其是强视觉素材或泛兴趣。
- YouTube / Discover / Gmail 用户不是主动搜索，页面承接要求更强。
- optimized targeting 可能扩大到手动受众之外。
- 素材疲劳和低意图点击会很快抬高成本。
- 对 lead gen，submitted conversion 不能代表 paid revenue。

Demand Gen 更适合有强素材、强页面承接、明确 remarketing / prospecting 目标和足够预算做素材实验的团队。不适合用来“便宜买流量再靠发布商广告变现”而不看用户意图。

## 9. 报表和诊断

PMax / Demand Gen 诊断至少看：

| 报表 | 诊断问题 |
| --- | --- |
| Channel performance report | 花费和结果在哪些渠道产生 |
| Search terms insights | 查询主题是否与 Offer 一致 |
| Placement report | 是否出现低质 placement 或不适合页面 |
| Asset performance | 哪些素材可能带来低质量点击 |
| Landing page / expanded URL | 是否被送到正确页面 |
| Change history | 是否改了目标、素材、URL、预算或 exclusions |
| Conversion action report | 是否优化到错误转化 |
| CRM / buyer feedback | submitted 是否变成 approved / paid |

诊断矩阵：

| 现象 | 优先查 |
| --- | --- |
| PMax ROI 高但 Search 下滑 | 品牌/再营销 cannibalization、brand exclusions |
| Clicks 高 sessions 低 | Final URL expansion、页面速度、跳转链、移动端 |
| Conversions 高 paid revenue 低 | conversion action、lead quality、value feedback |
| Spend 跑到 Display/Video | channel report、placement report、asset mix |
| Search themes 后流量变泛 | search term insights、negative/brand controls |
| Demand Gen CTR 高 ROI 低 | 素材标题党、低意图受众、页面承接差 |

## 10. 实验和止损

建议实验原则：

1. 不用 PMax / Demand Gen 冷启动验证未知 Offer。
2. 先有 Search 或稳定来源的 paid revenue 基线。
3. 独立预算，不和 Search 核心 campaign 混在一个预算池。
4. 明确 prospecting / remarketing / brand capture 的目标。
5. 固定 conversion action 和 value 口径。
6. 记录 asset group、URL controls、search themes、audience signals、brand exclusions。
7. 至少覆盖 conversion lag，再看 paid / finalized revenue。

止损条件：

- 花费达到测试预算但无 approved / paid revenue。
- 不相关 URL、query theme 或 placement 占比高。
- brand cannibalization 明显。
- bad geo、invalid lead、duplicate、low intent 上升。
- Policy、destination、misrepresentation 或 user complaint 风险出现。

## 11. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 PMax/Demand Gen 风险和控制项 | `/risk-audits` |
| 导入 cost/clicks/conversions/revenue 做 ROI | `/metrics/import` |
| 保存 Search terms、channel、landing page 诊断来源 | `/sources` |
| 在创意和 Claim 审核中处理素材组合风险 | Offer 详情页和创意手册 |
| 在链接计划中记录 URL 变更和候选页面 | `/links` |

后续可扩展表：

```text
pmax_campaign_controls
pmax_channel_performance_daily
pmax_search_theme_diagnostics
pmax_asset_group_snapshots
pmax_url_expansion_checks
demand_gen_audience_diagnostics
```

建议字段：

```text
campaign_id
campaign_type
asset_group
country
language
final_url_expansion_enabled
page_feed_used
url_exclusion_summary
search_themes
audience_signal_summary
brand_exclusions
channel
placement
cost
clicks
conversions
approved_revenue
paid_revenue
diagnosis
action
```

系统边界：

- 不自动开启 PMax / Demand Gen。
- 不自动接受 recommendations 或自动改预算。
- 不生成 misleading assets、cloaking URL 或违规 search themes。
- 不用虚假转化、补点击或模拟用户训练 Smart Bidding。
- 不绕过品牌词、敏感垂类、consent 或目标页政策。

## 12. QA 清单

- PMax / Demand Gen 有独立预算和测试目标。
- Conversion action 代表可收款价值，或至少能回传 approved / paid revenue。
- Final URL expansion、page feed、URL exclusions 记录清楚。
- Asset groups 按 Offer、国家、语言、页面或意图分层。
- Search themes 来自真实关键词和页面，不含禁止品牌/敏感误导词。
- Audience signals 不包含敏感身份、健康、金融困境或未经同意数据。
- Brand exclusions 和 Search/Shopping 边界已检查。
- Channel performance、placement、asset、landing page 和 Change history 已归档。
- Demand Gen 不只看 CTR，必须看 engaged session、offer click、paid revenue。
- 出现跑偏时先暂停或收窄，不用补转化或虚假信号训练系统。

## 13. 信息来源 URL

- Google Ads Help, About Performance Max campaigns: https://support.google.com/google-ads/answer/10724817
- Google Ads Help, Evaluate Performance Max results: https://support.google.com/google-ads/answer/16279166
- Google Ads Help, About the channel performance report for Performance Max: https://support.google.com/google-ads/answer/16260130
- Google Ads Help, About Performance Max channels: https://support.google.com/google-ads/answer/16683501
- Google Ads Help, About Final URL expansion: https://support.google.com/google-ads/answer/16672777
- Google Ads Help, Search targeting and controls for Performance Max: https://support.google.com/google-ads/answer/16672776
- Google Ads Help, Use search themes with Performance Max: https://support.google.com/google-ads/answer/14767319
- Google Ads Help, Set up your asset group and assets: https://support.google.com/google-ads/answer/15864535
- Google Ads Help, About audience signals for Performance Max campaigns: https://support.google.com/google-ads/answer/14530785
- Google Ads Help, About Demand Gen campaigns: https://support.google.com/adwords/answer/6105478
- Google Ads Help, Demand Gen audiences overview: https://support.google.com/google-ads/answer/15594567
- Google Ads Help, About optimized targeting: https://support.google.com/google-ads/answer/10537509
