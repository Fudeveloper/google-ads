# 季节性、事件日历与需求预测手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何用季节性、事件日历、Google Trends、Keyword Planner、Google Ads Insights、Search Terms、历史收入和官方行业日历来规划选题、页面、创意、预算和止损。目标是提前识别短期需求窗口，按可收款 ROI 有节奏地进入和退出；不是用热点词制造误导点击、蹭敏感事件、伪装地区、补点击、刷展示或用 Cookie 后台无人值守追热点。

## 1. 为什么季节性是套利利润窗口

很多套利机会不是全年稳定存在，而是在短时间内需求、CPC、广告主预算、用户紧迫感和下游 payout 同时变化。常见窗口包括：

- 税务、退税、报税软件、会计服务。
- 保险开放注册、Medicare、健康计划、牙科/视力保险。
- 假日购物、黑五网一、返校、母亲节、父亲节。
- 旅游旺季、航班酒店、签证、租车、旅行保险。
- 本地服务季节，例如 HVAC、除虫、屋顶、草坪、搬家。
- 金融周期，例如报税贷款、债务咨询、信用卡转账、贷款利率变化。
- B2B 预算季、财年末采购、软件替换和合规截止日期。

季节性窗口的利润来自“提前准备”，不是高峰当天才建 campaign。高峰当天开始做页面、追踪、审核和来源尽调，通常已经错过低成本学习窗口；高峰过后还按高峰预算继续跑，则会把利润还给市场。

## 2. 原理解释：需求曲线、竞争曲线和收入曲线不同步

季节性判断必须同时看三条曲线：

```text
demand curve: 用户搜索/兴趣什么时候上升和下降
competition curve: 广告主出价、CPC、预算什么时候变贵
revenue curve: approved/paid/finalized revenue 什么时候回填
```

常见错判：

- Trends 上升，但 Keyword Planner 显示 CPC 已经高到超过安全 RPV。
- Search volume 上升，但 Offer cap 很小，放量后超 cap 拒付。
- 当天 ROI 看起来高，但 conversion lag、refund、scrub 和 finalized revenue 还没回填。
- 热点词带来 CTR，但页面不能真实满足意图，导致 low RPV、投诉或政策风险。
- 季节结束后 search volume 还在，但用户意图已从“购买/申请”变成“支持/退款/取消”。

因此，季节性预测不是“看到热度就投”，而是：

```text
事件日历 -> 关键词意图 -> 页面 readiness -> 审核和追踪 -> 小预算学习
-> 高峰预算阶梯 -> 回传/扣量复盘 -> 退出和复盘
```

## 3. 核心对象地图

| 对象 | 解释 | 套利用途 |
| --- | --- | --- |
| event_calendar | 税季、开放注册、购物节、返校、行业展会等日期 | 决定准备和投放节奏 |
| vertical | 税务、保险、旅游、教育、本地服务等 | 决定政策、页面和 payout |
| query_cluster | 一组同意图关键词和相关搜索 | 连接需求、创意和页面 |
| demand_signal | Trends、Keyword Planner、Insights、search terms、历史数据 | 判断需求是否真实上升 |
| readiness_gate | 页面、追踪、审核、Offer、cap、source、cashflow 是否就绪 | 决定能不能进场 |
| ramp_plan | 预算、出价、国家、设备、素材的扩量计划 | 控制风险放大速度 |
| exit_rule | 高峰后何时降预算、否定词、停 campaign | 防止季后烧钱 |
| postmortem | 季后复盘 | 更新下一季模型和预算 |

## 4. 信息来源地图

| 来源 | 用途 | 误用风险 |
| --- | --- | --- |
| Google Trends | 看相对兴趣、地区、季节、相关查询 | 不是绝对搜索量，不等于收入 |
| Keyword Planner | 看关键词规模、竞争和 forecast | 预测不是承诺，CPC 会随竞争变化 |
| Google Ads Insights page | 看账户相关趋势、需求变化和市场洞察 | 不是套利放量许可 |
| Search terms report | 看真实触发查询和季后意图变化 | 受隐私阈值和聚合影响 |
| Auction Insights | 看竞争强度变化 | 不能推断竞品利润 |
| Historical metrics | 看去年/上季同窗口表现 | 账号、页面、Offer、CPC 可能已变 |
| Official calendars | 税务、医保、节假日、行业截止日期 | 要用最新官方日期，不能凭旧年记忆 |
| Revenue settlement | 看 approved/paid/finalized 滞后 | 高峰当天 reported revenue 可能过乐观 |

## 5. 事件日历构建

事件日历至少包含：

```text
event_name
vertical
country / state
language
official_source_url
preparation_start
creative_deadline
review_deadline
test_start
peak_start
peak_end
cooldown_end
policy_notes
offer_cap_notes
cashflow_notes
```

建议节奏：

| 时间 | 动作 |
| --- | --- |
| T-90 到 T-60 | 选 vertical、查官方日期、评估 payout、页面需求和政策 |
| T-60 到 T-30 | 做页面、创意 brief、追踪、来源尽调、合同/IO |
| T-30 到 T-14 | 小预算 Search/Native/Social 测试，收 search terms 和 paid/approved 信号 |
| T-14 到 T-7 | 扩素材、补否定词、检查 cap、预算和现金安全 |
| T-7 到 Peak | 按阶梯扩量，不同时大改页面、预算、出价和来源 |
| Peak 后 1-7 天 | 降预算、清理季后 query，等待 revenue lag |
| Peak 后 14-45 天 | 用 approved/paid/finalized 复盘，更新下一季模型 |

## 6. Demand Score 模型

建议 100 分：

```text
trend_lift              15
keyword_volume          15
cpc_affordability       15
commercial_intent       15
offer_cap_payout_fit    10
content_readiness       10
tracking_readiness       8
policy_safety            7
source_quality           5
```

评分解释：

| 维度 | 高分条件 | 低分条件 |
| --- | --- | --- |
| trend_lift | Trends、Insights、search terms 同向上升 | 只有单日噪声或社媒热点 |
| keyword_volume | Keyword Planner 有足够规模 | 量小且不可预测 |
| cpc_affordability | top bid / actual CPC 低于安全 RPV | CPC 已经压缩利润 |
| commercial_intent | query 明确比较、报价、申请、购买 | query 只是新闻、八卦或支持 |
| offer_cap_payout_fit | cap、payout、allowed traffic 支持窗口 | cap 小、payout 不稳、禁止该来源 |
| content_readiness | 页面能真实承接需求 | 只靠桥页或广告堆叠 |
| tracking_readiness | click_id、subid、postback、收入状态完整 | 只能看总点击 |
| policy_safety | 素材、页面和垂类合规 | 敏感事件、误导、官方冒充风险高 |
| source_quality | 来源可解释、可停量 | 不透明、不可停、低质供应商 |

进入季节性小测：总分 >= 75，且 content_readiness、tracking_readiness、policy_safety 不能低于各自 70%。

## 7. Vertical Calendar 示例

这些是示例模板，不是固定日期。具体日期要以当年官方来源为准。

| 垂类 | 需求窗口 | 主要 query | 风险 |
| --- | --- | --- | --- |
| Tax / refund | 报税季、延期截止日前 | tax filing, refund tracker, tax software, tax calculator | 官方冒充、敏感金融 claim、refund 误导 |
| Health insurance | 开放注册、特殊注册期 | health insurance quote, marketplace plan, dental insurance | HEC / Personalized Ads、资质和披露 |
| Medicare | 年度选择期、计划比较期 | medicare advantage plans, part d compare | 年龄、医疗、官方关系误导 |
| Holiday shopping | 黑五、网一、圣诞前 | best gifts, coupon, deal, shipping deadline | 折扣真实性、库存和退款 |
| Back to school | 返校前 4-8 周 | laptop for students, school supplies, tutoring | 儿童/学生数据和广告披露 |
| Travel | 假日前、暑期、春假 | cheap flights, travel insurance, hotel deals | 价格变动、取消/退款、低质 aggregator |
| Local services | 天气和季节触发 | AC repair, pest control, roofing, moving | 本地资质、call lead 质量、营业时间 |

注意：季节性页面不能暗示官方身份、保证结果、虚假稀缺、虚假折扣或不存在的资质。

## 8. Keyword Planner、Trends 和 Insights 的组合用法

推荐流程：

```text
Google Trends:
  比较主题和地区，找上升窗口和相关查询

Keyword Planner:
  拉关键词、volume、competition、top bid、forecast

Google Ads Insights:
  看账户相关趋势、需求变化、search interest 线索

Search Terms:
  用真实 query 修正意图、否定词和页面 brief

Revenue:
  用 approved/paid/finalized 证明是否值得下季继续
```

不要这样用：

- 用 Trends 100 分直接估算点击量。
- 只因为 Insights 提示需求上升就自动加预算。
- 用 Keyword Planner forecast 当作 CPA 或 ROI 承诺。
- 不看 Search Terms 就上 broad match。
- 不看 approved / paid revenue 就把季节窗口判断为成功。

## 9. Budget Ramp 和 Exit Rules

季节性预算建议分三段：

| 阶段 | 预算动作 | 风控 |
| --- | --- | --- |
| pre-season learning | 小预算，买足样本 | 验证追踪、页面、query、CPC、初始收入 |
| peak ramp | 每次加 10%-30%，按 source/geo/device 分层 | 每 24h/72h 复核，等待 lag |
| post-peak exit | 降预算、收紧关键词、清理 query | 防止支持/退款/取消意图消耗 |

Exit triggers：

- Trends 和 search volume 明显回落。
- Search terms 从购买/申请变为支持、取消、退款、投诉。
- CPC 上升但 approved / paid RPV 下降。
- Offer cap 接近上限或 buyer quality warning 增加。
- refund、scrub、deduction、invalid traffic、policy issue 上升。
- 页面或素材不再匹配季后用户需求。

季后不要立刻把所有数据归零。保留历史 query、creative、landing_version、source_quality 和 paid revenue，用于下一季 T-90 规划。

## 10. Smart Bidding Seasonality Adjustment 边界

Google Ads 的 seasonality adjustment 是给 Smart Bidding 的短期转化率变化提示，适合已知的短时促销或大促活动。套利团队要注意：

- 它不是需求预测器。
- 它不修复低质量 conversion value。
- 它不适合覆盖很长的常规季节波动。
- 它必须基于真实、可收款 conversion 信号。
- 如果回传的是 submitted lead、pending revenue 或误触点击，调整只会放大错误。

V1 系统只记录 seasonality adjustment review 和人工审批建议，不自动调用后台，也不使用 Cookie 操作。

## 11. 内容、创意和审核节奏

季节性素材必须提前准备：

| 阶段 | 内容动作 |
| --- | --- |
| T-60 | 页面主题、页面结构、信息来源、披露、FAQ |
| T-45 | 创意 angle、headline、description、claim proof |
| T-30 | 页面 QA、速度、移动端、tracking、privacy/terms |
| T-14 | 广告审核、拒登修复、否定词、source QA |
| Peak | 少量素材迭代，不大改承诺 |
| Post-peak | 更新页面或转为 evergreen content |

页面更新要保留版本号。税季、保险、旅游和折扣页面尤其要避免旧日期、旧价格、旧资格条件、旧政策或过期 Offer。

## 12. 系统落地

当前系统可承接 V1：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录官方日历、趋势来源和判断依据 | `/sources` |
| 用关键词、CPC、CVR、RPV 做机会测算 | `/calculators` |
| 生成季节性创意和 campaign 草稿 | `/offers`、`/campaigns` |
| 导入测试期和高峰期指标 | `/metrics/import` |
| 用优化建议管理止损和季后退出 | `/optimization` |
| 记录政策、来源、合同和争议风险 | `/risk-audits` |
| 安排页面更新、报表复核和季后复盘 | `/tasks` |

建议后续表：

```text
event_calendars
seasonal_demand_forecasts
keyword_trend_snapshots
seasonal_readiness_checks
seasonal_budget_ramp_plans
seasonal_exit_rules
seasonality_adjustment_reviews
seasonal_postmortems
```

关键字段：

```text
event_calendars:
  event_name, vertical, country, official_source_url,
  preparation_start, test_start, peak_start, peak_end,
  cooldown_end, policy_notes, owner

seasonal_demand_forecasts:
  event_id, query_cluster, trend_score, keyword_volume,
  forecast_clicks, forecast_cost, safe_cpc,
  expected_approved_revenue, readiness_score,
  recommendation
```

这些表只做预测、计划、审计和复盘，不自动追热点、不自动生成误导素材、不自动改预算或出价。

## 13. ADXKit 对应点和完成形态

ADXKit 类工具可能会把趋势监控、选品、创意生成、自动投放和 ROI 优化整合在一起。安全完成形态是：

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| 趋势/热点发现 | 保存 Trends、Keyword Planner、Insights 和官方日历证据 |
| 自动生成季节性创意 | 生成 brief 和草稿，必须 claim review 和人审 |
| 自动投放 | 生成 campaign 草稿、CSV/Scripts preview，不 Cookie 后台自动改 |
| 自动扩量 | 生成 ramp 建议和 stop-loss，等待 approved/paid 数据 |
| 自动换链接 | 只允许同意图、同垂类、已审核季节性链接 |
| 季后复盘 | 保存 postmortem、paid revenue、source quality 和下一季动作 |

完成标准：

- 能解释需求、竞争和收入回传不同步。
- 能把季节性事件转成页面、关键词、素材、预算和退出规则。
- 能说明 Trends、Keyword Planner、Insights、Search Terms、official calendar 的差异。
- 明确不实现自动追热点、误导创意、伪装地区、补点击、刷展示、Cookie 后台控制或 cloaking。

## 14. QA 清单

季节性 campaign 上线前检查：

- 官方日期和事件窗口是否来自当年官方来源。
- Trends 只是相对兴趣，是否已用 Keyword Planner 和历史数据校验。
- 关键词是否分信息、比较、价格、交易、支持、敏感意图。
- 页面是否有新日期、新价格、新资格、新披露和真实下一步。
- Offer payout、cap、allowed traffic 是否支持高峰窗口。
- source、publisher、placement、subid 是否可追踪和停量。
- 预算 ramp 是否分 pre-season、peak、post-peak。
- 是否设置 exit rule 和季后否定词。
- 是否考虑 conversion lag、buyer feedback、finalized revenue 和扣量。
- 是否禁止官方冒充、虚假折扣、虚假稀缺、误导热点和敏感事件蹭流量。

## 15. 信息来源 URL

- Google Ads Help, Use Keyword Planner: https://support.google.com/google-ads/answer/7337243
- Google Ads Help, Get forecasts with Keyword Planner: https://support.google.com/google-ads/answer/3022575
- Google Trends Help, FAQ about Google Trends data: https://support.google.com/trends/answer/4365533
- Google Trends Help, Compare Trends search terms: https://support.google.com/trends/answer/4359550
- Google Trends Help, Find related searches: https://support.google.com/trends/answer/4355000
- Google Ads Help, About the Insights page: https://support.google.com/google-ads/answer/10256472
- Google Ads Help, About demand forecasts on the Insights page: https://support.google.com/google-ads/answer/10787044
- Google Ads Help, About seasonality adjustments: https://support.google.com/google-ads/answer/10369906
- Google Ads Help, Budget report: https://support.google.com/google-ads/answer/10702522
- Google Ads Help, About ad scheduling: https://support.google.com/google-ads/answer/6372656
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, About the search terms report: https://support.google.com/google-ads/answer/2472708
- Google Ads Help, Auction insights: https://support.google.com/google-ads/answer/2579754
- Google Ads Help, Evaluate automated bid strategy performance: https://support.google.com/google-ads/answer/10167267
- IRS, Tax Time Guide: https://www.irs.gov/newsroom/tax-time-guide
- HealthCare.gov, Dates and deadlines for 2026 health insurance: https://www.healthcare.gov/quick-guide/dates-and-deadlines/
