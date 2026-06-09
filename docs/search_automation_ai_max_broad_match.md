# Search 自动化流量：AI Max、Broad Match 与 DSA 套利风险手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何理解 Google Search 自动化流量，包括 AI Max for Search campaigns、broad match、Smart Bidding、Dynamic Search Ads、automatically created assets、Final URL expansion、URL inclusions/exclusions、brand controls、negative keywords、search terms report 和 landing pages report。目标是让团队在扩大搜索覆盖时保留 query intent、页面一致性、素材证据和后端收入复盘，而不是把搜索自动化当成黑盒套利机器。

本文不提供隐藏最终 URL、绕过审核、cloaking、补点击、伪造搜索、自动搜索、品牌词规避或用低质页面承接自动化流量的方案。

## 1. 为什么 Search 自动化对套利关键

搜索套利最核心的变量是用户意图。Search 自动化会改变三件事：

1. 系统可能匹配团队没有手动写出的 query。
2. 系统可能组合或生成团队没有逐字审核过的资产。
3. 系统可能把用户送到同域内更相关但未充分审计的页面。

这对套利既有价值也危险：

- 价值：发现长尾 query、扩展非完全匹配词、降低人工建词成本。
- 风险：query 意图变宽、品牌/敏感词混入、页面和广告承诺错配、低质量 lead 增加、Smart Bidding 学错目标。

套利团队不能只看平均 CPA、CTR 或 Google Ads conversions；必须看 search term、landing page、asset claim、approved/paid revenue、refund、scrub、扣量和用户投诉。

## 2. 核心对象

| 对象 | 作用 | 套利风险 |
| --- | --- | --- |
| AI Max for Search | 用 Google AI 扩展搜索匹配、资产和 URL | 黑盒扩 query、生成资产、扩页面 |
| Broad match | 让关键词覆盖相关含义和变体 | 意图变宽，低质 query 增加 |
| Smart Bidding | 用转化和价值信号自动出价 | 如果回传低质转化，会优化到低质用户 |
| Dynamic Search Ads | 基于网站内容自动匹配搜索并生成标题 | 页面索引和内容质量决定 query 覆盖 |
| Automatically created assets | 基于广告、页面和账号内容生成资产 | 可能生成缺证据或过宽 claim |
| Final URL expansion | 将用户送到同域内更相关页面 | 未审页面进入流量，变成软性换链接 |
| URL inclusions / exclusions | 控制可用页面范围 | 规则不清会放大低质页面 |
| Brand controls | 控制品牌相关 query 或 brand inclusion/exclusion | 品牌词、竞品词、商标和 cannibalization |
| Search terms report | 观察实际搜索词和匹配 | 自动化扩量后的主要诊断证据 |

## 3. AI Max for Search 的工作边界

AI Max for Search campaigns 是 Search campaign 的一组自动化增强能力，用于扩大匹配、优化资产和改善最终 URL 选择。它不是 PMax；它仍然运行在 Search campaign 语境，但会让系统在 query、asset 和 landing page 层面承担更多决策。

套利团队要把 AI Max 拆成三个控制面：

1. Query 扩展：系统如何理解关键词、页面和用户意图。
2. Asset 扩展：系统是否生成或组合新 headline/description。
3. URL 扩展：系统是否把用户送到不同页面。

上线前必须记录：

- 哪些 campaign / ad group 开启 AI Max。
- 是否启用 final URL expansion。
- URL inclusions、URL exclusions 和 page feed 范围。
- 是否启用 brand inclusions / exclusions 或其他 brand controls。
- 是否启用自动生成资产。
- 使用哪些 primary conversion 和 conversion value。

## 4. Broad Match 与 Smart Bidding

Broad match 的价值在于覆盖更多相关搜索，而不是只匹配字面关键词。Google 官方通常建议 broad match 与 Smart Bidding 配合使用，因为出价系统会使用更多上下文信号。

套利风险在于：Smart Bidding 优化的是你交给它的目标。如果 primary conversion 是 submitted lead、浅层 click、低质量 sign-up 或未最终回款的事件，系统可能学习到“容易提交但不可收款”的用户。

Broad match 测试原则：

1. 不在未知 Offer 冷启动时直接大预算 broad。
2. 先建立 exact/phrase 或稳定 query 的 paid revenue 基线。
3. 使用 conversion value 或 offline conversion 反映 approved/paid revenue。
4. 每天看 search terms、negative keywords、geo/device、landing page 和 buyer feedback。
5. 设置 spend cap、query cap、bad term rule 和止损窗口。

## 5. Dynamic Search Ads 与页面索引风险

Dynamic Search Ads 会基于网站内容匹配相关搜索，并动态生成广告标题。它适合结构清晰、内容充分、页面主题一致的网站；不适合页面薄、主题跳跃、Offer 页混杂或广告密度高的站点。

对套利团队，DSA 风险来自页面库：

- 旧页面、测试页、过期 Offer 页被匹配。
- 页面标题、H1、内容里有夸张 claim，动态标题放大误导。
- 多国家/多语言页面混在同一域，query 和语言错配。
- Affiliate / lead gen 页面没有足够原创价值，进入 destination 或 bridge page 风险。

DSA / page feed 使用原则：

- 只把已审页面放入 page feed。
- 排除 test、admin、thank-you、policy issue、thin page、expired offer 页面。
- 页面 title / H1 / meta 不写无证据强声明。
- DSA search terms 与 landing page performance 每日归档。

## 6. Final URL Expansion 与 URL 控制

Search 自动化中的 Final URL expansion 和 PMax 类似，都会影响用户最终到达页面。对套利业务，这个功能非常敏感，因为页面就是承诺、追踪、合规和收入模型的交汇点。

安全使用前提：

- 同域所有可投页面都通过落地页质量审计。
- URL inclusions 精确到可投目录或 page feed。
- URL exclusions 覆盖隐私页、关于页、文章索引页、过期页、低质页、未本地化页、广告密度测试页和敏感垂类未审页。
- tracking template、Final URL suffix、auto-tagging 和 postback 能在 expanded URL 上保留。
- 用户、Google 审核和实际访问者看到的业务目的保持一致。

不要把 Final URL expansion 当成换链接、cloaking 或审核绕过工具。

## 7. Automatically Created Assets 与 Claim 风险

自动生成资产可能基于落地页、现有广告和账号内容生成 headline 或 description。它的风险不是“AI 生成”本身，而是生成内容是否有页面证据、是否符合政策、是否与用户最终看到的页面一致。

套利团队要审查：

- 是否出现 best、#1、official、guaranteed、free、save、approved、instant 等强声明。
- 是否暗示官方关系、认证、补贴、政府身份或品牌授权。
- 是否把页面上的弱证据写成强承诺。
- 是否在金融、医疗、住房、就业、信贷等敏感垂类触发个性化广告或披露问题。
- 是否和 DSA / Final URL expansion 叠加后，让资产和最终页面错配。

系统落地应把 automatically created assets 当成候选，需要进入 Claim 审核和人工放行，而不是自动投放。

## 8. Brand Controls、Negative Keywords 和 Query 治理

自动化扩量后，query 治理是利润和账号安全的核心。

必须维护三类库：

| 库 | 用途 |
| --- | --- |
| Negative keywords | 排除低意图、误导、免费、投诉、退款、招聘、下载、成人等 query |
| Brand controls | 控制品牌词、竞品词、官方关系和商标风险 |
| Sensitive query blocklist | 金融困境、医疗症状、身份、儿童、成人、博彩等敏感方向 |

风险信号：

- Search terms 出现不允许的品牌词、官方词、政府词或竞品误导词。
- Broad / AI Max 带来大量“free、login、support、refund、scam、complaint”等 query。
- Query CTR 高但 approved/paid revenue 低。
- Search ROI 好看，但来自品牌词或本来会自然转化的用户。
- Negative keywords 只按 cost 维护，不按 refund、scrub、complaint 和 policy 维护。

## 9. 报表和诊断

Search 自动化复盘至少看：

- Search terms report：query、match type、keyword、cost、conversion、paid revenue。
- AI Max reporting：AI Max 带来的匹配、资产、URL 和控制项影响。
- Landing pages report：expanded URL、mobile speed、cost、conversion、paid revenue。
- Asset report：headline/description 表现和 claim 风险。
- Change history：谁开启 AI Max、broad、DSA、ACA、URL expansion 或 recommendation。
- Bid strategy report：learning、limited、conversion lag、目标变化。
- Offline conversion / buyer feedback：approved、rejected、paid、refund、scrub。

异常诊断矩阵：

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| Cost 上升，paid revenue 不升 | broad / AI Max 扩到低意图 query | 查 search terms，补 negative，降预算 |
| CTR 高，CVR 高，paid revenue 低 | conversion action 太浅 | 改 value / offline conversion，暂停低质 query |
| Landing page 分散 | Final URL expansion 或 DSA 页面范围过宽 | 查 landing pages report，收紧 inclusions/exclusions |
| 品牌词贡献高 | Brand cannibalization 或竞品/商标风险 | 查 brand controls，拆品牌和非品牌 |
| 素材被拒或投诉 | ACA / DSA title 生成过宽 claim | 停自动资产，做 Claim 审核 |

## 10. 实验和止损

Search 自动化实验建议：

1. 先用 exact/phrase 或小范围 broad 建立 query 和 paid revenue 基线。
2. 单独 campaign 或 ad group 测 AI Max / DSA / broad，不和稳定业务混跑。
3. 设置测试预算、最大 CPA、最大亏损和最短观察窗口。
4. 每日导出 search terms、landing pages、assets、change history。
5. 用 approved/paid revenue 判断，不用 submitted conversion 单独判断。
6. 发现低质 query、页面错配、brand cannibalization 或 refund 增加时立即降预算或暂停。

不要让自动化实验自动接受 recommendations。Recommendations 可以作为输入，但需要人审、预算上限和回滚点。

## 11. 系统落地

当前 V1 可用已有模块落地：

| 需求 | 当前页面 / 文档 |
| --- | --- |
| 记录 campaign 是否使用 broad / AI Max / DSA | `/campaigns` 的备注和 [Google Ads 投放结构手册](campaign_launch_automation.md) |
| 记录 Final URL、tracking template 和 URL QA | [追踪模板、URL 参数与跳转链 QA 手册](tracking_template_redirect_chain_qa.md) |
| 生成和审核创意资产 | `/offers/<id>`、Claim 审核、[创意 Claim 审核手册](creative_claim_review_fact_checking.md) |
| 导入 search terms / landing pages / asset report | `/metrics/import` 和 [Google Ads 报表诊断手册](google_ads_reporting_diagnostics.md) |
| 记录高风险 query、brand、URL 或 claim 问题 | `/risk-audits` |
| 保存来源 URL | `/sources` |

后续可新增表：

```text
search_automation_controls
search_query_diagnostics
search_url_expansion_reviews
search_asset_auto_generation_reviews
search_brand_control_snapshots
dsa_page_feed_versions
```

这些表只做报表、审计、建议和人工审批，不自动开启 AI Max、broad、DSA、Final URL expansion 或 automatically created assets。

## 12. QA 清单

- AI Max / broad / DSA 是否单独测试，而不是直接混进稳定 campaign。
- primary conversion 是否代表 approved/paid revenue。
- Final URL expansion、URL inclusions、URL exclusions 和 page feed 是否记录。
- 所有可投页面是否通过落地页质量和 Claim 审核。
- Automatically created assets 是否进入人审，不直接自动投放。
- Search terms 是否每日按 cost、paid revenue、refund、scrub、policy issue 复盘。
- Brand controls、negative keywords 和 sensitive query blocklist 是否维护。
- Change history 是否记录谁开启或修改自动化功能。
- Bid strategy report 是否解释 learning、limited、conversion lag 和目标变化。
- 止损规则是否在预算、query、页面、brand 和 paid revenue 层面都能触发。

## 13. 信息来源 URL

- Google Ads Help, About AI Max for Search campaigns: https://support.google.com/google-ads/answer/15910187
- Google Ads Help, Set up AI Max in Search campaigns: https://support.google.com/google-ads/answer/15909989
- Google Ads Help, FAQs about AI Max for Search campaigns: https://support.google.com/google-ads/answer/15913066
- Google Ads Help, Final URL expansion in Search campaigns: https://support.google.com/google-ads/answer/16230205
- Google Ads Help, Search targeting and controls for AI Max / Search: https://support.google.com/google-ads/answer/16672776
- Google Ads Help, About broad match: https://support.google.com/google-ads/answer/2407779
- Google Ads Help, Use broad match with Smart Bidding: https://support.google.com/google-ads/answer/12159290
- Google Ads Help, About Smart Bidding: https://support.google.com/google-ads/answer/7065882
- Google Ads Help, About Dynamic Search Ads: https://support.google.com/google-ads/answer/2471185
- Google Ads Help, About automatically created assets: https://support.google.com/google-ads/answer/11259373
- Google Ads Help, About the search terms report: https://support.google.com/google-ads/answer/2472708
- Google Ads Help, About negative keywords: https://support.google.com/google-ads/answer/2453972
- Google Ads Help, Evaluate landing page performance: https://support.google.com/google-ads/answer/7543502
- Google Ads Help, About change history: https://support.google.com/google-ads/answer/19888
