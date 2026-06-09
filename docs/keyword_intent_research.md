# 关键词、搜索意图与选题研究手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何研究关键词、搜索意图、页面选题、匹配类型、否定词、搜索词报告和测试优先级。目标是找到真实用户意图，并把广告、页面、Offer、变现和追踪串起来；不是用宽泛词烧预算、用敏感词碰政策、用误导标题拉点击，或通过搜索词伪装进入高风险 feed/桥页模式。

## 1. 为什么关键词是套利入口

套利模型的第一层不是广告账户，而是用户意图：

```text
Query / Interest
-> Ad promise
-> Landing page task
-> Monetization event
-> Approved / finalized revenue
```

关键词研究要回答：

1. 用户到底想解决什么问题？
2. 这个问题能不能被页面真实回答？
3. 这个意图是否有商业价值？
4. CPC 是否低于可承受 RPV/EPC？
5. 该词是否涉及敏感政策、误导风险或 Offer 限制？
6. 数据能否按 campaign/ad group/keyword/search term 回溯？

如果关键词、广告承诺和页面任务不一致，CTR 越高，浪费和扣量风险越大。

## 2. 意图分层

| 意图层 | 用户状态 | 示例 | 适合页面 | 变现方式 |
| --- | --- | --- | --- | --- |
| 信息型 | 想理解问题 | `how does cloud backup work` | 指南、FAQ、清单 | 展示广告、newsletter、轻 CTA |
| 比较型 | 在比较方案 | `best cloud backup for small business` | 对比页、评测页 | Affiliate、Lead、展示广告 |
| 价格型 | 关心成本 | `cloud backup pricing calculator` | 计算器、报价解释 | CPA/CPL、Lead、工具转化 |
| 替代型 | 已有产品不满意 | `dropbox business alternative` | 替代方案页 | Affiliate、SaaS lead |
| 交易型 | 准备行动 | `buy payroll software` | Offer 页、表单页 | CPA/CPL/CPS |
| 支持型 | 已是用户，需要帮助 | `login`、`support`、`cancel` | 通常不适合套利 | 应否定或避免 |
| 敏感型 | 医疗、金融、身份、政府 | `debt relief approval`、`medical treatment` | 高审查内容 | 谨慎或拒绝 |

套利冷启动一般从“比较型、价格型、替代型”的长尾开始；信息型可做内容资产，交易型 CPC 往往高且政策压力大。

## 3. Keyword Planner 工作流

使用 Keyword Planner 时，建议分两步：

1. Discover new keywords：围绕页面主题、Offer、用户问题生成候选。
2. Forecast：按国家、语言、预算、出价看点击、花费和竞争估计。

输出表：

| 字段 | 用途 |
| --- | --- |
| keyword | 候选词 |
| intent_type | 信息/比较/价格/替代/交易/支持/敏感 |
| avg_monthly_searches | 需求规模 |
| competition | 竞争强度 |
| top_of_page_bid_low/high | CPC 参考 |
| target_country | 国家 |
| page_candidate | 对应页面 |
| offer_fit | 是否匹配 Offer |
| policy_risk | 政策风险 |
| test_priority | 测试优先级 |

注意：

- 低搜索量或敏感词可能不可发现或不可预测。
- Forecast 是估计，不是承诺。
- CPC 估计不等于实际可买成本。
- Keyword Planner 的词需要经过页面能力、政策和现金流再筛一遍。

## 4. Google Trends 用法

Google Trends 适合判断：

- 季节性。
- 地区差异。
- 同义词比较。
- 主题上升/下降。
- 相关查询和相关主题。

不要误用：

- Trends 是归一化兴趣，不是绝对搜索量。
- 不能直接把 Trends 分数当点击量。
- 小地区、小词可能波动很大。
- Trending query 不等于可投放、可变现或合规。

套利用法：

```text
Keyword Planner = 规模、CPC、竞争
Google Trends = 季节、地区、主题变化
Search terms report = 真实触发查询和浪费
GA4 / revenue = 页面和收入证明
```

## 5. Match Type 策略

Google Ads 常见匹配类型：

| Match type | 范围 | 冷启动建议 |
| --- | --- | --- |
| Exact | 最窄，匹配相同含义或非常接近意图 | 用于高信心长尾和已验证词 |
| Phrase | 中等，保留关键词含义但有更多变体 | 适合冷启动和扩展 |
| Broad | 最宽，可匹配相关含义和更多查询 | 等追踪、否定词和转化稳定后再测试 |

冷启动建议：

- 每个 ad group 只放一个意图簇。
- 先用 exact/phrase 买样本。
- broad match 必须配合强转化信号、否定词、预算上限和搜索词清理。
- 不要为了追量把无关意图混进一个 ad group。

## 6. 搜索词报告

关键词是你投的，search term 是用户真实搜的。两者不一样。

搜索词报告用于：

- 找出浪费查询。
- 发现新长尾词。
- 判断 match type 是否太宽。
- 判断广告和页面承诺是否误导。
- 发现政策敏感或不适合 Offer 的意图。

清理节奏：

| 阶段 | 频率 | 动作 |
| --- | --- | --- |
| 冷启动 1-3 天 | 每天 | 加否定词、暂停偏离意图词 |
| 小样本 1-2 周 | 每 2-3 天 | 把好 search terms 提升为 exact/phrase |
| 稳定期 | 每周 | 清理浪费、复盘新增趋势 |
| 扩量期 | 每天或隔天 | 防 broad 或新来源烧预算 |

## 7. 否定词体系

否定词分三层：

| 层级 | 用途 | 示例 |
| --- | --- | --- |
| Account negative list | 全账号不想要 | `jobs`、`free movie`、`torrent` |
| Campaign negative | 该国家/Offer/页面不适合 | `government login` |
| Ad group negative | 防止意图串组 | compare 组否定 `support`、`login` |

套利常见否定词类别：

- 支持/登录：`login`、`support`、`customer service`。
- 求职：`jobs`、`career`、`salary`。
- 免费/破解：`free download`、`crack`、`torrent`。
- 不相关行业：和 Offer 无关的品牌、地名、服务。
- 政策敏感：医疗保证、金融高风险、政府官方身份误导等。

注意：否定词也会误杀高质量长尾。新增前先看该词的 sessions、revenue、Offer fit 和页面任务。

## 8. 页面选题矩阵

每个关键词簇要落到页面，不要只落到广告：

| 关键词簇 | 页面类型 | 必备内容 |
| --- | --- | --- |
| “best / compare / vs” | 对比页 | 比较维度、适用人群、限制、披露 |
| “cost / pricing / calculator” | 计算器页 | 输入项、估算逻辑、限制说明 |
| “how to / guide” | 指南页 | 步骤、FAQ、注意事项、下一步 |
| “alternative” | 替代方案页 | 替代理由、适合/不适合、证据 |
| “near me / local” | 本地页 | 服务范围、联系方式、资质、隐私 |
| “apply / quote / sign up” | 表单页 | 条件、流程、隐私、真实服务主体 |

页面不能支持的关键词，不要投。

## 9. 政策和敏感词筛查

关键词进入测试前检查：

- 是否涉及医疗、金融、博彩、官方服务、法律、成人、药品、技术支持等敏感垂类。
- 是否暗示保证批准、保证收益、官方身份或虚假稀缺。
- 是否和 Offer 禁止来源冲突，例如 brand bidding、incent、competitor bidding。
- 是否会把用户带到与广告承诺不一致的页面。
- 是否会诱导用户点击广告而不是完成页面任务。

敏感词不一定不能投，但需要：

- 更完整页面证据。
- 认证或许可证。
- 更保守文案。
- 更严格的人审和风险审计。

## 10. 测试优先级评分

建议 100 分：

| 维度 | 分值 |
| --- | --- |
| 商业价值 | 20 |
| CPC 可承受性 | 15 |
| 页面可满足度 | 20 |
| Offer fit | 15 |
| 政策风险低 | 15 |
| 数据可追踪 | 10 |
| 季节/地区稳定 | 5 |

进入小预算测试：

- 总分 >= 75。
- 页面可满足度 >= 15/20。
- 政策风险不能低于 10/15。
- 追踪字段完整。

## 11. 系统落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer 和关键词限制 | `/offers` |
| 根据 Offer 生成关键词候选 | Offer 详情页创意生成 |
| 用 CPC、CVR、RPM 测算测试预算 | `/calculators` |
| 把关键词组织进 Campaign 草稿 | `/campaigns` |
| 导出 Google Ads Editor CSV | `/campaigns/<id>/export.csv` |
| 导入结果和收入 | `/metrics/import` |
| 根据成本/收入生成优化建议 | `/optimization` |
| 记录敏感词和来源证据 | `/risk-audits`、`/sources` |

当前系统没有单独的关键词库表，V1 把关键词存在 `creative_sets.keywords` 和 Campaign 导出中。后续可扩展 `keyword_research` 表，但仍只做研究、评分、导出和审计，不做后台 Cookie 操作或自动扩词上线。

## 12. 信息来源 URL

- Google Ads Help, Use Keyword Planner: https://support.google.com/google-ads/answer/7337243
- Google Ads Help, Google Ads keyword matching: https://support.google.com/google-ads/answer/14996023
- Google Ads Help, About negative keywords: https://support.google.com/google-ads/answer/2453972
- Google Ads Help, About the search terms report: https://support.google.com/google-ads/answer/2472708
- Google Ads Help, Get negative keyword ideas using the search terms report: https://support.google.com/google-ads/answer/7102466
- Google Trends Help, Compare Trends search terms: https://support.google.com/trends/answer/4359550
- Google Trends Help, FAQ about Google Trends data: https://support.google.com/trends/answer/4365533
- Google Trends Help, Find related searches: https://support.google.com/trends/answer/4355000
- Google Ads policies, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads policies, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads policies, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
