# 归因、增量性与流量蚕食治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何区分 attribution credit、reported conversions、incremental lift、cannibalization、holdout、campaign experiment、brand/search/conversion lift 和 marginal profit。目标是避免把平台归因的转化全部当作广告新增收入，尤其是在品牌词、再营销、老用户、自然搜索需求、季节性高峰、PMax / Broad Match 和多渠道混跑场景中。本文不提供规避归因、隐藏来源、伪造转化、补点击、刷展示、模拟自然流量、cloaking 或 Cookie 后台操作方案。

## 1. 为什么归因不等于增量利润

Google Ads、GA4、联盟后台、CRM 和发布商报表都可能给同一笔收入分配 credit。归因回答的是：

```text
这次转化应该记给哪个广告互动、渠道、关键词或 campaign？
```

增量性回答的是：

```text
如果不投这笔广告，这次收入还会不会发生？
```

这两个问题不同。套利团队常见误判：

- 品牌词 campaign ROAS 很高，但很多用户本来就会搜索品牌或直接访问。
- 再营销 campaign CPA 很低，但可能只是抢了自然转化 credit。
- PMax 报告 conversions 上升，但部分来自既有 demand 或 brand demand。
- Broad Match 带来“新增 query”，但要确认是否真新增 paid revenue，而不是从 exact/phrase 或 SEO 中转移。
- 内容套利在旺季 ROI 变好，但增长可能来自季节需求，不一定来自素材或出价优化。

归因是报表分配，增量是因果差异。套利扩量应该看增量利润，而不是只看归因收入。

## 2. 原理解释：Attribution 分 credit，Incrementality 测 lift

Attribution model 根据规则或数据把转化 credit 分给触点。Google Ads 和 GA4 都支持数据驱动归因等模型，模型会影响 conversions、conversion value、CPA、ROAS 和自动出价学习。

Incrementality 用实验或准实验比较 treatment 和 control 的差异：

```text
incremental_conversions =
  conversions_treatment
  - expected_conversions_without_ads

incremental_profit =
  incremental_revenue
  - incremental_cost
```

归因数据适合日常优化，增量测试适合回答“这笔花费是否真的创造新增利润”。两者应配合使用：

| 层级 | 回答 | 用途 |
| --- | --- | --- |
| Attribution | 谁获得 credit | 日报、出价、路径诊断 |
| Incrementality | 是否真的新增 | 预算分配、渠道优先级 |
| Cannibalization | 抢了谁的 credit 或需求 | 防止品牌/自然/老用户被买量重买 |
| Marginal economics | 多花一美元是否仍赚钱 | 扩量和降预算 |

## 3. 核心对象地图

| 对象 | 含义 | 套利风险 |
| --- | --- | --- |
| attributed conversion | 平台归因给广告的转化 | 不一定增量 |
| incremental conversion | 因广告新增的转化 | 更适合预算决策 |
| control group | 未被实验广告影响的人群/地区/流量 | 需要干净且足够样本 |
| treatment group | 看到或进入实验广告的人群/地区/流量 | 需要和 control 可比 |
| holdout | 被保留不投或不展示的组 | 牺牲短期量换真实 lift |
| cannibalization | 广告抢了自然、品牌、老用户或其他 campaign 的 credit | 高 ROAS 假象 |
| iROAS | incremental revenue / cost | 衡量真实广告增量回报 |
| marginal CPA | incremental cost / incremental conversions | 判断扩量边际成本 |
| attribution window | 允许 credit 回溯的时间窗 | 窗口越长，抢功可能越大 |
| model comparison | 对比不同 attribution model | 识别 last click 偏差 |

## 4. 归因层：能用，但不要神化

Google Ads attribution model 会影响 conversion action 的 conversions 列、All conversions、出价策略和 model comparison 报表。GA4 attribution reports 也会按自己的模型分配 credit。

套利团队使用归因时要注意：

- 同一个实验中不要中途切换 attribution model。
- Google Ads、GA4、affiliate 和 CRM 的 attribution scope 不同，不要强行让数字相等。
- Data-driven attribution 是模型输出，不是增量实验。
- Last click 可能低估早期触点，也可能高估品牌词和低漏斗流量。
- 归因窗口越长，越要检查是否把本来会发生的转化记给广告。
- 自动出价会使用相关 conversion 数据，因此 attribution model 改动需要学习窗口和版本记录。

归因适合回答“哪类 query、asset、page、device 看起来参与了转化”，不适合单独回答“广告带来了多少新增利润”。

## 5. 增量层：Lift、Holdout 和实验

增量测量的核心是比较两组：

```text
treatment: 看到或被投放广告
control: 没看到或被保留不投
lift = treatment_outcome - control_outcome
```

可用设计：

| 设计 | 适合场景 | 风险 |
| --- | --- | --- |
| Google Ads custom experiment | Search/Display/Video campaign 变量测试 | 不是所有 campaign 类型可用 |
| Lift study | Brand/Search/Conversion lift | 需要资格、预算和样本 |
| Geo holdout | 国家/州/城市分区 | 地区差异和季节性干扰 |
| Audience holdout | 再营销、Customer Match、老用户 | 隐私、样本和重叠风险 |
| Time-based pause test | 小团队临时判断 | 容易被季节、竞价和趋势污染 |
| Campaign split | Broad/PMax/asset/goal 变化 | 需要防止预算和学习期干扰 |

实验原则：

- 预先写 hypothesis、success metric 和 guardrail metrics。
- 控制组必须尽量不受 treatment 影响。
- 指标优先用 approved/paid/finalized revenue，而不是 submitted conversions。
- 样本不足或 confidence interval 太宽时，不要宣布 winner。
- 实验中不要同时改页面、出价、goal、预算和素材。

## 6. Cannibalization 类型

| 类型 | 表现 | 诊断 |
| --- | --- | --- |
| Brand cannibalization | 品牌词 ROAS 极高 | 查 direct/organic brand search 是否下降 |
| Organic cannibalization | Paid search 增长，SEO/Direct 下降 | 看 GA4 channel、Search Console、brand demand |
| Campaign cannibalization | Broad/PMax 抢 exact/phrase | 看 search terms、incremental queries、overlap |
| Remarketing cannibalization | 再营销 CPA 很低 | 做 audience holdout 或排除近期高意向用户 |
| Seasonal cannibalization | 旺季广告表现变好 | 用去年同期、Trends、event calendar 对照 |
| Partner cannibalization | 多联盟/多 buyer 重复计 | transaction_id、dedupe、exclusive/shared lead |
| Geo cannibalization | 新地区扩量抢老地区 budget | 分区预算和 cohort 对照 |

蚕食不一定是坏事。品牌保护、竞品防守和再营销可能有战略意义。但套利团队必须把它和“新增利润”分开预算，否则会把本来免费的需求买成付费需求。

## 7. Incrementality Score

建议给 campaign 或 source 计算 `Incrementality Score`：

```text
incrementality_score =
  holdout_quality             20
  incremental_revenue_signal  25
  cannibalization_risk        20
  sample_and_confidence       15
  revenue_maturity            10
  operational_cleanliness     10
```

评分解释：

| 维度 | 高分表现 | 低分表现 |
| --- | --- | --- |
| holdout quality | control/treatment 干净可比 | 只看前后对比 |
| incremental revenue | paid/finalized lift 明确 | 只有 attributed conversions |
| cannibalization risk | brand/organic/direct 未明显下滑 | 其他免费渠道同步下降 |
| sample confidence | 样本足、区间窄、窗口完整 | 低样本或跑 1-2 天 |
| revenue maturity | approved/paid 已成熟 | 只有 submitted/pending |
| operational clean | 实验期变量少、Change history 干净 | 多变量同时改 |

动作建议：

| Score | 动作 |
| --- | --- |
| 85-100 | 可作为 Scale / Core 证据 |
| 70-84 | 可小幅扩量，继续复测 |
| 55-69 | 只做 Test，不进入主预算 |
| 35-54 | 归因可能偏高，需 holdout |
| 0-34 | 高蚕食或无增量，不扩量 |

## 8. iROAS 和边际利润

增量指标：

```text
incremental_revenue =
  revenue_treatment
  - revenue_control_adjusted

iROAS =
  incremental_revenue / ad_cost

incremental_profit =
  incremental_revenue
  - ad_cost
  - variable_cost
```

CPA/CPL：

```text
incremental_cpa =
  incremental_cost / incremental_approved_conversions
```

Display / AdSense：

```text
incremental_rpv =
  incremental_finalized_revenue / incremental_paid_clicks
```

如果 attributed ROAS = 3.0，但 iROAS = 0.8，说明报表 credit 很漂亮，但广告没有创造足够新增收入。套利预算应该由 iROAS 和 incremental profit 决定，而不是只由 attributed ROAS 决定。

## 9. 场景 SOP

### 9.1 品牌词

- 先确认是否有商标/Offer 条款权限。
- 按 brand exact、brand phrase、competitor、generic 拆开。
- 看 direct、organic brand、Search Console query 和 paid brand 同期变化。
- 必要时做短期 geo holdout 或 budget holdout。
- 品牌防守预算和套利扩量预算分开。

### 9.2 再营销和 Customer Match

- 区分新客、老客、已访问、已提交、已购买。
- 对高意向人群做 holdout 或频控。
- 不把低 CPA 再营销直接等同于新增获客。
- 遵守 personalized ads、Customer Match 和 consent 边界。

### 9.3 Broad Match / AI Max / PMax

- 看 incremental queries、search terms insights、channel/asset/page reports。
- 检查是否抢 exact/phrase、brand、SEO 或已有 PMax 的量。
- 只在 high-quality primary conversion 和 paid revenue 稳定后扩。
- 用 experiment 或分阶段 ramp 观察边际 CPA/ROAS。

### 9.4 内容套利和 Search Feed

- 对照自然流量、站内搜索、直接访问和季节需求。
- Search feed gross revenue 必须和 payable / finalized 对齐。
- 不把季节高峰里的自然需求增长全记给买量。
- 对 source 做 cohort，比较 holdout source 或低预算 baseline。

## 10. 系统落地

当前系统已实现 `/attribution` V1 工作台和 `attribution_reviews` 表，用于把归因、增量性和流量蚕食判断落成可审计记录。

| 行业动作 | 系统位置 |
| --- | --- |
| 记录实验假设、测试类型和 attribution model | `/attribution` |
| 保存 treatment/control/holdout 设计 | `/attribution` 的 treatment_scope、control_scope、split_method、date_window |
| 计算 incremental revenue、incremental profit 和 iROAS | `adsworkbench/services/attribution.py` |
| 标记 brand、organic/direct、remarketing、PMax/Broad 蚕食风险 | `attribution_reviews` |
| 保存 holdout quality、revenue maturity、data maturity、sample 和 confidence | `attribution_reviews` |
| 更新 holdout_planned、experiment_running、evidence_ready、cannibalization_review、blocked 等状态 | `/attribution/<id>/status`，状态写入 `/logs` |
| 记录 Google Ads experiments、lift studies、GA4 attribution、Change history 和内部证据 URL | `source_urls` 字段和 `/sources` |
| 导入 cost/click/conversion/revenue | `/metrics/import` |
| 用 optimization actions 标记可能的蚕食或等待窗口 | `/optimization`、`/decision-windows` |
| 用任务中心安排 holdout 复盘和月度增量审计 | `/tasks` |

`AttributionReview` 主要字段：

```text
name, offer_id, campaign_draft_id, test_type, attribution_model,
hypothesis, treatment_scope, control_scope, split_method, date_window,
primary_metric, guardrail_metrics, attributed_revenue,
treatment_revenue, control_revenue, incremental_revenue, ad_cost,
variable_cost, incremental_profit, i_roas,
attributed_to_incremental_ratio, attributed_conversions,
incremental_conversions, sample_size, confidence_level,
holdout_quality, revenue_status, data_status,
brand_cannibalization_risk, organic_cannibalization_risk,
remarketing_cannibalization_risk, pmax_broad_overlap_risk,
change_history_clean, single_variable_test, approved_paid_evidence,
human_review, score, risk_level, recommended_action, blockers,
status, notes, source_urls
```

评分逻辑：

- 干净的 geo holdout、campaign experiment、lift study 得分更高；pre/post 因缺少 control 得分很低。
- `incremental_revenue = treatment_revenue - control_revenue`。
- `i_roas = incremental_revenue / ad_cost`。
- `incremental_profit = incremental_revenue - ad_cost - variable_cost`。
- submitted/accepted 或 fresh/partial 数据会阻止扩量。
- brand/organic/remarketing/PMax-Broad 高蚕食风险会进入 high risk。
- 缺 Change history、单变量测试、approved/paid 证据或人工审核会生成 blockers。

系统只保存测试计划、证据、评分和决策，不自动创建实验、不自动应用 winner、不隐藏来源、不伪造 control、不用 Cookie 后台操作。

## 11. ADXKit 对应点和完成形态

ADXKit 类工具的“自动优化、自动放量、ROI 看板”必须回答一个问题：这些收入是新增的，还是只是被广告抢了 credit？

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI dashboard | 同时展示 attributed 和 incremental 视角 |
| 自动优化 | 高蚕食风险先进入 holdout 或人工评审 |
| 自动投放 | 品牌、再营销、PMax 扩量必须有增量证据 |
| AI 创意 | winner 不能只看 CTR 或 attributed conversions |
| 任务中心 | 安排 lift、holdout、model comparison 和 cannibalization audit |
| 换链接 | link/page 变化后重置归因和增量观察窗口 |

功能拆解和安全完成清单：

- 完成 attribution、incrementality、cannibalization 的原理解释。
- 完成 lift、holdout、experiment、iROAS、Incrementality Score 和场景 SOP。
- 完成系统落地、来源 URL、验收入口和 seed 来源。
- 不实现伪造转化、补点击、刷展示、隐藏来源、cloaking、Cookie 后台操作或自动应用实验 winner。

## 12. QA 清单

- 当前 ROI 是 attributed 还是 incremental。
- Brand、organic、direct 是否同步下降。
- 再营销是否只是抢了即将转化的人群。
- PMax / Broad 是否抢了 exact、phrase、brand 或 SEO query。
- 是否有 control / holdout，而不是只看前后对比。
- 实验期是否没有同时改预算、出价、goal、页面和素材。
- 指标是否用 approved/paid/finalized，而不是 submitted。
- confidence interval 是否足够窄，样本是否足够。
- attribution model 改动是否有版本和学习窗口。
- Change history 是否干净。
- 是否禁止用补点击、伪造转化或隐藏来源制造 lift。

## 13. 信息来源 URL

- Google Ads Help, About attribution models: https://support.google.com/google-ads/answer/6259715
- Google Ads Help, About data-driven attribution: https://support.google.com/google-ads/answer/6394265
- Google Analytics Help, Get started with attribution: https://support.google.com/analytics/answer/10596866
- Google Ads Help, About lift studies: https://support.google.com/google-ads/answer/16104408
- Google Ads Help, Set up a custom experiment: https://support.google.com/google-ads/answer/6261395
- Google Ads Help, Monitor your experiments: https://support.google.com/google-ads/answer/6318747
- Google Ads API, Create experiments: https://developers.google.com/google-ads/api/docs/experiments/experiments
- Google Ads Help, About Brand Lift: https://support.google.com/google-ads/answer/9049825
- Google Ads Help, About search terms insights: https://support.google.com/google-ads/answer/11386930
- Google Ads Help, Use broad match with Smart Bidding: https://support.google.com/google-ads/answer/12159290
- Google Ads Help, About Performance Max campaigns: https://support.google.com/google-ads/answer/10724817
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Customer Match policy: https://support.google.com/adspolicy/answer/6299717
- Google Ads Help, Personalized advertising: https://support.google.com/adspolicy/answer/143465
