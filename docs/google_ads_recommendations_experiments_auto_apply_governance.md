# Google Ads Recommendations、Experiments 与 Auto-apply 优化治理手册

更新时间：2026-06-09

本文说明 Google Ads Recommendations、Optimization Score、Auto-apply、Custom Experiments、Ad Variations、Change History 和 Google Ads API Recommendation/Experiment 资源在 Ads 套利中的真实作用。目标是把“平台建议”和“自动优化”转成可验证、可拒绝、可复盘的实验治理流程，而不是把建议当成自动执行指令。

本文不提供 Cookie 后台操作、自动登录、自动绕过审核、自动接受所有推荐、补点击、刷展示、模拟转化、cloaking 或封禁后换号方案。系统只承载建议评审、实验计划、证据包、人工审批、导入导出和复盘。

## 1. 为什么 Recommendations 不能直接等于套利优化

Google Ads Recommendations 的公开定位是：根据账户历史、campaign 设置、Google 趋势和可用功能，给出可能改善出价、关键词、广告和效率的建议。Optimization Score 是账户或 campaign 设置表现潜力的估算。

这对普通广告主有参考价值，但对 Ads 套利不能直接等于利润优化，原因有 6 个：

1. Google Ads 看到的是平台内转化、转化值和点击成本，不一定看到最终 paid revenue、finalized revenue、buyer reject、scrub、refund 或扣量。
2. 套利利润取决于 `paid RPV - CPC`，不是 `conversions` 或 `optimization score`。
3. 推荐可能推动更宽匹配、更高预算、更多自动化广告资产、更多库存或更激进出价，这些动作会扩大流量，也会扩大亏损。
4. 自动建议依赖历史数据和平台趋势，不能理解联盟条款、feed partner 规则、AdSense finalized 扣量、lead buyer feedback 和账户风险。
5. Conversion lag、data freshness 和月度 finalized revenue 会让短期 CPA/ROAS 看起来“可扩量”，但真实收款可能滞后回落。
6. 高风险垂类、claim、落地页、tracking chain 和政策状态不是 Optimization Score 能完整表达的变量。

因此，套利团队的基本原则是：

- Recommendations 是待验证假设，不是自动执行命令。
- Optimization Score 是账户设置诊断，不是利润分数。
- Auto-apply 默认关闭，除非某个低风险建议已经有明确白名单、审批和回滚机制。
- Experiments 的成功指标必须绑定 paid revenue、finalized revenue、lead accept rate、扣量率和政策风险。

## 2. 核心对象

| 对象 | 平台含义 | 套利治理口径 |
| --- | --- | --- |
| Recommendation | Google Ads 自动生成的优化建议 | 待评审假设，需要分类、打分、审批 |
| Optimization Score | 0-100% 的设置优化估算 | 诊断信号，不进入利润公式 |
| Score uplift | 应用建议后可能增加的优化分 | 只能说明平台分数变化，不说明可收款 ROI |
| Auto-apply | 定期自动应用已选择类型的建议 | 高风险，V1 不启用自动写入 |
| Recommendation queue | 待自动应用或待评审的建议队列 | 每日巡检和变更风险来源 |
| Experiment | 从原 campaign 拆出测试版本并分配流量 | 验证单个假设，保留基线和分流证据 |
| Change History | 广告后台变更历史 | 判断建议、人工、脚本或导入造成的变更 |
| RecommendationService | API 读取、应用或 dismiss recommendations | 未来只读同步优先，写入必须审批 |

## 3. 推荐类型拆解

Google Ads 官方把 Recommendations 分成多类。套利团队建议按风险分层处理。

### 3.1 Repairs

Repairs 类建议通常用于修复无法投放、配置错误或政策问题。

例子：

- Fix your ad destinations。
- Fix your ad text。
- Fix disapproved assets。
- Fix conversion tracking。
- Complete advertiser verification。
- Fix Merchant Center suspension。

套利处理：

- 这类建议优先级高，但不等于可以自动修复。
- 拒登、目的地、认证、转化追踪问题要进入证据包和人工复核。
- 修复后再决定是否恢复预算，不要边修边扩量。

### 3.2 Bidding and budgets

出价和预算建议会影响消耗速度，是套利里最危险的一类。

例子：

- Raise budgets。
- Adjust CPA targets。
- Adjust ROAS targets。
- Switch to Maximize conversions / Maximize conversion value / Target CPA / Target ROAS。
- Use portfolio bid strategy。

套利处理：

- 默认进入 L2/L3 高风险审批。
- 必须看后端 paid revenue、conversion lag、扣量、geo/device/source 分层。
- 不允许因 Optimization Score 变高而直接加预算。
- Smart Bidding 只有在 primary conversion 和 conversion value 接近可收款价值时才考虑测试。

### 3.3 Keywords and targeting

关键词和定向建议可能带来新增流量，也可能稀释意图。

例子：

- Add broad match keywords。
- Add keywords。
- Expand to Search Partners。
- Use Display Expansion。
- Use optimized targeting。
- Add audiences。
- Remove conflicting negative keywords。
- Remove redundant keywords。

套利处理：

- `Add broad match`、`Search Partners`、`Display Expansion`、`optimized targeting` 必须先小预算实验。
- 删除否定词必须逐条核对 search terms 和 lead/revenue 记录。
- 删除 non-serving/redundant keywords 可以低风险评审，但仍保留变更证据。
- 新增关键词要绑定 intent、landing、offer 和政策审核。

### 3.4 Ads and assets

广告和素材建议会改变用户看到的承诺和落地路径。

例子：

- Improve responsive search ads。
- Add image assets。
- Add sitelinks / callouts / price assets。
- Use optimized ad rotation。
- Add dynamic image assets。
- Add dynamic search ads。

套利处理：

- 所有新增/修改 headline、description、image、sitelink、callout 都要做 Claim 审核。
- 动态素材和自动资产要检查 Final URL、页面证据和敏感垂类限制。
- 高 CTR 不代表高 paid RPV。

### 3.5 Measurement

衡量类建议通常更接近基础设施修复，但仍然可能改变优化目标。

例子：

- Set up conversion tracking。
- Upgrade conversion tracking。
- Set up conversion value measurement。
- Enhanced Conversions。
- Data-driven attribution。

套利处理：

- 优先修复断裂的追踪和价值回传。
- 任何 primary conversion、conversion value、attribution model 变更必须做版本记录。
- 不把低质量 lead、未付款注册、无效事件设为 primary conversion。

### 3.6 Automated campaigns

自动化 campaign 建议通常包括 Performance Max、AI Max 或其他自动化覆盖。

套利处理：

- 不适合冷启动未知 offer。
- 必须先有 URL exclusions、brand controls、negative keywords、asset claim 审核、channel 报告和 paid revenue 复盘。
- 不能用自动化 campaign 掩盖页面质量、claim、追踪或回款问题。

## 4. Auto-apply 治理

Google Ads Auto-apply 会定期应用选择的推荐类型，并提供 queue、history 和 Change History 查看。对套利团队来说，默认策略应该是：

```text
Auto-apply default = OFF
```

原因：

- auto-apply 是无人值守写入。
- 推荐类型会随时间变化。
- 自动应用可能新增关键词、扩大定向、改变出价目标、添加动态资产或修改广告轮播。
- 这些动作可能提高平台分数，却降低 paid RPV 或增加政策风险。

建议分级：

| 类别 | Auto-apply | 处理方式 |
| --- | --- | --- |
| 出价/预算 | 禁止 | 手动审批 + 实验 + 回滚 |
| 新增 broad match / Search Partners / Display Expansion | 禁止 | 小预算实验 |
| 新增广告资产 / 动态资产 | 禁止 | Claim 审核 + 页面证据 |
| conversion goal / value / attribution | 禁止 | 追踪负责人和财务口径审批 |
| 修复拒登/目的地 | 禁止自动 | 进入拒登证据包 |
| 删除 non-serving keyword | 可低风险评审 | 手动批量确认 |
| 删除重复 keyword | 可低风险评审 | 保留变更 diff |
| 移除 conflicting negative keyword | 慎重 | 逐条核对 search terms |

巡检节奏：

- 每日查看 Recommendation queue 和即将自动应用的建议。
- 每周导出 Change History，过滤 recommendation、auto apply、Google Ads Scripts、Editor/Bulk Upload 相关变更。
- 每月复盘哪些建议被接受、拒绝、实验、回滚。

## 5. 建议评审矩阵

每条建议进入系统后，先做评审，不直接执行。

| 维度 | 问题 |
| --- | --- |
| 建议类型 | Repairs / Bidding / Budget / Keyword / Asset / Measurement / Automated campaign |
| 影响对象 | Account / Campaign / Ad group / Keyword / Asset / Conversion action |
| 预算影响 | 是否提高日预算、目标 CPA、目标 ROAS 或出价自由度 |
| 流量影响 | 是否扩大 query、network、geo、device、audience 或 placement |
| 素材影响 | 是否新增 claim、动态素材、图片、sitelink、business name |
| 追踪影响 | 是否改变 primary conversion、value、attribution、tag |
| 政策影响 | 是否触发敏感垂类、品牌、claim、目的地或拒登风险 |
| 后端收入 | 是否有 paid revenue、finalized revenue、lead accept 证据支持 |
| 数据新鲜度 | 是否已等待 conversion lag 和收入回填 |
| 回滚能力 | 是否能恢复原预算、出价、关键词、资产或目标 |

建议结论：

| 结论 | 含义 |
| --- | --- |
| accept_safe | 低风险修复，可手动执行 |
| test_required | 需要实验验证 |
| reject | 与业务目标、政策或后端收入冲突 |
| defer | 数据不足，等待回传或月度关账 |
| incident_review | 已经造成异常消耗、拒登、扣量或追踪事故 |

## 6. Experiments 原理和套利用法

Custom Experiments 可以从原 campaign 创建实验版本，拆分原 campaign 的流量和预算，用于比较实验和基线。官方说明里，Search campaign 可选择 cookie-based split 或 search-based split；同一 campaign 通常只能同时运行一个实验。

套利实验不是“开了就看 Google Ads conversions”。正确做法：

1. 单一假设：一次只测试一个主变量。
2. 保留基线：不要在实验期间同时改原 campaign 的预算、出价、页面和素材。
3. 预设成功指标：paid RPV、paid ROI、approved lead rate、deduction rate、policy incident rate。
4. 等待窗口：考虑 conversion lag、finalized revenue 和 buyer feedback。
5. 决策记录：胜出、失败、继续观察、回滚都要有证据。

可实验变量：

| 变量 | 示例 | 风险 |
| --- | --- | --- |
| Match type | phrase vs broad | query 扩散、低意图 |
| Bid strategy | manual CPC vs target CPA | 消耗失控、优化目标错 |
| Landing page | lp-a vs lp-b | 页面质量、拒登、扣量 |
| Creative angle | price vs trust vs speed | claim 风险、低质 lead |
| Network | Search only vs Search Partners | source 质量差异 |
| Geo/device split | US mobile vs desktop | bad geo、时区、设备差异 |
| Conversion goal | lead submit vs approved lead value | 优化错目标 |

## 7. 实验设计流程

```text
提出假设
  -> 绑定 offer、campaign、landing version、creative version
  -> 定义主指标和护栏指标
  -> 检查政策、追踪、预算和回滚
  -> 创建实验或人工拆分测试
  -> 运行到最小样本和等待窗口
  -> 对账 Google Ads cost -> sessions -> offer clicks -> paid revenue
  -> 结论：promote / rollback / continue / archive
  -> 更新关键词、素材、页面和推荐白名单
```

主指标建议：

| 业务类型 | 主指标 | 护栏指标 |
| --- | --- | --- |
| Search arbitrage | paid RPV、paid ROI | Search term drift、bounce、policy issue |
| Lead gen | approved lead CPA、paid revenue | reject rate、duplicate、bad geo、TCPA complaint |
| AdSense/AdX | finalized session RPM | invalid traffic、deduction rate、viewability |
| Native presell | paid revenue per session | refund/scrub、publisher complaints、claim risk |

## 8. 平台建议到内部优化动作的转换

平台建议应转换成内部动作，而不是原样执行。

| 平台建议 | 内部动作 |
| --- | --- |
| Raise budgets | 触发预算节奏和止损评审 |
| Add broad match keywords | 生成 broad match 小预算实验 |
| Adjust CPA target | 检查 paid CPA、conversion lag 和目标值 |
| Add assets | 生成 asset review case 和 claim/proof 检查 |
| Fix destination | 进入广告拒登/目的地证据包 |
| Remove conflicting negatives | 打开 search terms 和否定词冲突评审 |
| Set up conversion value | 进入 conversion value 口径设计 |
| Create PMax / AI Max | 进入自动化流量准入评审 |

## 9. Change History 和事故复盘

Recommendations 和 Auto-apply 的关键风险是“谁改了什么”。Change History 应成为安全日志。

复盘字段：

| 字段 | 用途 |
| --- | --- |
| change_time | 判断异常消耗或拒登发生前后的变更 |
| actor | 区分人工、Google Ads、Scripts、Editor、API |
| change_type | budget、bid、keyword、asset、conversion、targeting |
| recommendation_id | 关联原始建议 |
| before/after | 支持回滚 |
| cost_delta | 变更后消耗变化 |
| paid_revenue_delta | 变更后可收款收入变化 |
| policy_delta | 拒登、受限、投诉变化 |
| rollback_status | 是否恢复 |

事故触发：

- auto-apply 后 CPC 或 cost 激增。
- 新增 broad match 带来低意图 query。
- 删除 negative keyword 导致 bad geo 或竞品词扩散。
- conversion goal 变更后 Smart Bidding 优化到低价值事件。
- 动态素材或自动资产触发拒登。

## 10. 系统落地

当前系统已有：

| 模块 | 可承载内容 |
| --- | --- |
| `/optimization` | 内部规则优化建议 |
| `/metrics/import` | 导入 cost、clicks、conversions、revenue |
| `/campaigns` | 保存草稿、预算、关键词和广告结构 |
| `/risk-audits` | 记录高风险建议和拒绝原因 |
| `/tasks` | 保存检查任务、执行日志和事故复盘 |
| `/sources` | 保存官方 Google Ads / API 来源 |
| `/knowledge/experiment_design` | 通用实验设计方法 |

后续建议新增表：

```sql
CREATE TABLE google_ads_recommendation_reviews (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  account_alias VARCHAR(128),
  recommendation_key VARCHAR(255) NOT NULL,
  recommendation_type VARCHAR(128) NOT NULL,
  affected_object_type VARCHAR(64),
  affected_object_ref VARCHAR(128),
  risk_level VARCHAR(16) NOT NULL,
  expected_score_uplift DECIMAL(8,2),
  expected_cost_delta DECIMAL(12,2),
  backend_revenue_evidence TEXT,
  decision VARCHAR(32) NOT NULL,
  reviewer VARCHAR(128),
  decision_reason TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);

CREATE TABLE google_ads_experiment_plans (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  experiment_key VARCHAR(128) NOT NULL,
  campaign_ref VARCHAR(128) NOT NULL,
  hypothesis TEXT NOT NULL,
  test_variable VARCHAR(128) NOT NULL,
  split_method VARCHAR(64),
  split_percent DECIMAL(5,2),
  primary_metric VARCHAR(64) NOT NULL,
  guardrail_metrics_json JSON,
  start_at DATETIME,
  end_at DATETIME,
  status VARCHAR(32) NOT NULL,
  result_decision VARCHAR(32),
  result_summary TEXT
);

CREATE TABLE auto_apply_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  account_alias VARCHAR(128),
  recommendation_type VARCHAR(128) NOT NULL,
  auto_apply_enabled BOOLEAN NOT NULL,
  captured_at DATETIME NOT NULL,
  source_note TEXT
);
```

V1 边界：

- 可以保存 recommendation review。
- 可以保存实验计划和结论。
- 可以提醒检查 Auto-apply 设置。
- 可以把 Change History 作为外部证据登记。
- 不自动调用 Cookie 后台或自动接受建议。
- 不自动改预算、出价、关键词、Final URL、conversion goal 或受众。

## 11. QA 清单

| 检查项 | 通过标准 |
| --- | --- |
| Auto-apply | 默认关闭，若开启必须有白名单和审批记录 |
| 建议分类 | 每条建议属于明确类型和风险等级 |
| 后端收入 | paid/finalized revenue 或 buyer feedback 支撑 |
| 数据窗口 | 等待 conversion lag 和收入回填 |
| 政策风险 | claim、landing、Final URL、垂类和拒登状态已检查 |
| 预算影响 | 预算和出价变更有 stop-loss |
| 流量影响 | query、network、geo、device、audience 已分层 |
| 实验设计 | 单一假设、基线、分流、成功指标、护栏指标 |
| 变更证据 | Change History、payload hash、reviewer 和回滚点 |
| 复盘 | 结论回写到关键词、素材、页面和建议白名单 |

## 12. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本系统完成形态 |
| --- | --- |
| 优化建议 | 内部规则 + Recommendations 评审矩阵 |
| 自动投放 | 草稿、CSV/Scripts payload、人工审批和 Change History，不自动接受建议 |
| 定时任务 | 只跑检查和同步，不跑无人值守预算/关键词/资产写入 |
| 数据同步 | 把 recommendations、experiments、change history 作为未来只读同步对象 |
| 扩量/止损 | 以 paid revenue、deduction、reject、policy risk 为核心，而不是 Optimization Score |
| 实验复盘 | 实验计划、结果、回滚和素材/页面/关键词反馈闭环 |

## 13. 信息来源 URL

- Google Ads Help, About recommendations: https://support.google.com/google-ads/answer/3448398
- Google Ads Help, Check your optimization score: https://support.google.com/google-ads/answer/9061547
- Google Ads Help, Types of recommendations: https://support.google.com/google-ads/answer/3416396
- Google Ads Help, Apply or dismiss recommendations: https://support.google.com/google-ads/answer/10169817
- Google Ads Help, About applying recommendations automatically: https://support.google.com/google-ads/answer/10279006
- Google Ads Help, Manage auto-apply recommendations: https://support.google.com/google-ads/answer/10276359
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
- Google Ads Help, Set up a custom experiment: https://support.google.com/google-ads/answer/6261395
- Google Ads Help, Monitor experiments: https://support.google.com/google-ads/answer/6318747
- Google Ads Help, Set up ad variations: https://support.google.com/google-ads/answer/7438541
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, About data freshness: https://support.google.com/google-ads/answer/2544985
- Google Ads API, Optimization score and recommendations: https://developers.google.com/google-ads/api/docs/recommendations
- Google Ads API, Recommendation overview: https://developers.google.com/google-ads/api/docs/recommendations/overview
- Google Ads API, Take actions on recommendations: https://developers.google.com/google-ads/api/docs/recommendations/action
- Google Ads API, Recommendation error handling and testing: https://developers.google.com/google-ads/api/docs/recommendations/error-handling
- Google Ads API, Experiments overview: https://developers.google.com/google-ads/api/docs/experiments/overview
- Google Ads API, Change event: https://developers.google.com/google-ads/api/docs/change-event

