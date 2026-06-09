# Source、Publisher、Placement 质量评分与名单治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何持续评估 source、publisher、placement、subid、network、campaign、landing version 和 offer 的质量，并把评分结果转成 allowlist、watchlist、quarantine、blocklist、retired 等名单动作。目标是用真实点击、真实 session、approved / paid revenue、扣量、投诉、无效流量和政策证据管理放量闸门；不是购买不可解释流量、隐藏来源、用代理/指纹/Worker 转发规避检测、补点击、刷展示或把异常流量伪装成自然流量。

## 1. 为什么来源质量评分是套利放量闸门

套利的表面公式很简单：

```text
profit = revenue - media_cost
```

但真实经营里，`revenue` 不是点击当天看到的一个数字，`media_cost` 也不是唯一风险。一个来源是否值得放量，至少取决于：

- 用户为什么会点击。
- 点击是否能形成可解释 session。
- session 是否产生真实广告价值、lead 价值或 search feed 价值。
- reported revenue 是否能变成 approved、finalized 或 paid revenue。
- 低质量来源是否带来 invalid traffic、ad serving limit、buyer quality hold、scrub、refund、complaint 或 policy issue。
- 出问题时能否按 publisher、placement、subid、campaign、device、geo 快速停源。

所以来源质量评分不是报表装饰，而是预算阀门。没有来源评分，团队只能看总 ROI；总 ROI 往往会掩盖坏来源、坏版位、坏国家、坏设备和坏页面版本。可扩量来源必须满足三个条件：

```text
可解释 -> 可追踪 -> 可停量
```

只满足便宜点击，不满足以上三个条件，不能进入放量。

## 2. 原理解释：来源质量由哪些信号决定

Source Quality Score 的本质是把多平台、不同延迟的数据压成一个“是否允许继续花钱”的运营判断。它不是机器学习黑盒，第一版应保持可解释：

```text
source quality =
  transparency
  + tracking completeness
  + intent fit
  + revenue quality
  + policy safety
  + stop-control
  + consistency
```

每个维度都必须能落到证据：

| 维度 | 原理 | 证据 |
| --- | --- | --- |
| transparency | 来源越透明，越能解释用户语境 | source、publisher、placement、sample URL、network、creative |
| tracking completeness | 参数越完整，越能串起点击到收入 | UTM、ValueTrack、click_id、subid、landing_version、offer_id |
| intent fit | 用户意图越接近页面和 offer，质量越稳定 | search term、placement theme、page topic、session behavior |
| revenue quality | 收入越接近 paid，越适合扩量 | reported、approved、finalized、paid、scrub、deduction |
| policy safety | 风险越低，长期账户和站点越稳定 | disapproval、Policy Center、invalid traffic、complaint |
| stop-control | 越能精确停量，事故损失越小 | block placement、exclude app、pause source、negative keyword |
| consistency | 越能跨日、跨设备、跨 geo 稳定，越能放大 | variance、pacing、weekday pattern、conversion lag |

套利团队容易犯的错误是只看 `CPC` 或 `CTR`。低 CPC 可能来自低意图、误点、激励、低质 publisher 或不可解释供应商；高 CTR 也可能来自误导素材、移动端误点或广告伪装。评分必须把“能不能收款”和“会不会扣量/封禁/投诉”放在点击指标前面。

## 3. 核心对象地图

| 对象 | 解释 | 质量治理作用 |
| --- | --- | --- |
| source | 流量来源总称，如 Google Search、Search Partners、Native vendor、newsletter buy | 放量、停源、预算分配的一层 |
| network | Google Search、Search Partners、Display、YouTube、Discover、Gmail、Native network 等 | 区分库存和意图 |
| publisher | 具体媒体、站点、app、newsletter、channel 或供应商下游 | 发现好坏媒体 |
| placement | website、app、video、channel、publisher placement id | placement exclusion、allowlist、blocklist 的核心 |
| subid | 第三方追踪或联盟链路中的可回传维度 | 连接 supplier report、postback、buyer feedback |
| campaign / ad group | 买量结构 | 保证预算、素材和出价可复盘 |
| creative angle | 用户点击动机 | 判断点击质量是否来自真实兴趣还是误导承诺 |
| landing_version | 页面版本 | 判断同一来源在不同页面上的承接差异 |
| offer | 变现对象 | 约束条款、cap、payout、allowed traffic |
| buyer_feedback | buyer 对 lead 或 conversion 的质量反馈 | approved、rejected、duplicate、incentivized、bad geo、complaint |
| exclusion / blocklist entry | 排除记录 | 防止坏来源重复进入预算 |

这些对象必须在追踪 URL、报表导入和风险审计里保持一致。若 `source_id` 只存在供应商报表而没有进入 landing、postback 和收入对账，后续就无法判断来源质量。

## 4. 来源分层和不同治理重点

| 来源层 | 常见形态 | 主要质量风险 | 核心治理 |
| --- | --- | --- | --- |
| owned / organic | 自有内容、邮件、社媒账号 | 量小、归因混乱 | UTM、内容主题、页面质量 |
| Google Search | keyword、search term、match type | CPC 高、query drift、商标和敏感词 | search terms、negative keywords、approved revenue |
| Search Partners | partner search inventory | 来源透明度较低、质量波动 | network segment、source isolation、停量阈值 |
| Display / YouTube / Demand Gen | website、app、video、channel、Discover、Gmail | 误点、低意图、品牌安全 | placement report、content suitability、exclusions |
| Performance Max | 跨 inventory 自动化 | channel 混合、URL expansion、品牌词和再营销混入 | channel report、brand/URL/placement controls |
| Native / Content Discovery | publisher、widget、content recommendation | 标题党、MFA、页面不一致 | publisher list、creative claim review、landing QA |
| Social | feed、audience、creative | 素材承诺过强、低意图、归因延迟 | creative angle、session behavior、qualified conversion |
| Direct buy / Newsletter | 媒体直采、newsletter sponsorship | 供应商报表夸大、受众不清 | sample URL、UTM、first-order cap、refund terms |
| Traffic vendor | 中介、流量包、push/pop 等 | 不透明、bot、激励、代理、不可停量 | 严格尽调，默认小测或拒绝 |

原则：来源越黑盒，预算越小，阈值越严；来源越透明，越能进入 allowlist。

## 5. 质量指标

### 5.1 买量和到站指标

| 指标 | 用途 | 风险解释 |
| --- | --- | --- |
| impressions | 展示规模 | 只看展示不能判断价值 |
| clicks | 买量点击 | 可能包含无效点击或误点 |
| cost | 花费 | 要和 approved / paid revenue 对齐 |
| CPC | 点击成本 | 低 CPC 可能是低质来源 |
| CTR | 素材吸引力 | 异常高可能是误导或误点 |
| click -> session rate | 点击到站质量 | 低说明跳转、加载、无效点击或追踪问题 |
| landing load time | 页面承接 | 慢会造成 session 掉失 |
| bounce / engaged session | 意图质量 | 极低 engagement 说明低意图或异常 |
| device / geo mix | 来源结构 | 异常集中可能是低质库存或供应商问题 |

### 5.2 页面和下游行为指标

| 指标 | 用途 | 风险解释 |
| --- | --- | --- |
| page views / session | 内容消费 | 极高可能是翻页诱导或页面循环 |
| time on page | 内容匹配 | 极低说明误点或低意图 |
| outbound click rate | offer interest | 过低说明页面不匹配，过高要看是否误导 |
| ad requests / session | 发布商广告强度 | 异常高可能触发页面体验和无效流量风险 |
| ad CTR | 广告互动 | 远高于历史可能是误点、诱导或异常来源 |
| form submit / call click | lead 意图 | 要和 buyer quality 对齐 |

### 5.3 收入和结算指标

| 指标 | 用途 | 风险解释 |
| --- | --- | --- |
| reported revenue | 平台初始收入 | 不能直接当作最终 ROI |
| approved revenue | 网络或 buyer 初步认可收入 | 比 reported 更接近真实价值 |
| finalized revenue | 发布商月度关账收入 | 适合做长期来源评分 |
| paid revenue | 实际到账 | 最高可信口径 |
| rejection rate | lead 或 conversion 拒绝率 | 高说明低质来源、错 geo、重复或不合规 |
| scrub / deduction rate | 扣量比例 | 质量问题、无效流量或 buyer 调整 |
| effective payout | 实际 payout | 要按 source、geo、status 分层 |
| refund / clawback | 回滚收入 | 高风险来源不能放量 |

### 5.4 风险指标

| 指标 | 用途 | 风险解释 |
| --- | --- | --- |
| invalid clicks / invalid click rate | Google Ads 无效点击诊断 | 上升要隔离 campaign/source |
| Policy Center issue | 发布商政策问题 | 需要停源、修页面和保存证据 |
| ad serving limit | 站点广告服务限制 | 常与来源质量、无效流量和新站信任有关 |
| disapproval / appeal | 广告审核风险 | 素材、页面、URL 或垂类不一致 |
| complaint rate | 用户或合作方投诉 | 常比收入指标更早暴露问题 |
| buyer quality warning | buyer 对 lead/source 提醒 | 必须进入名单治理 |
| cap quality hold | offer cap 或质量 hold | 说明供应商或来源不适合继续灌量 |

## 6. Source Quality Score 模型

第一版建议 100 分模型，保持人工可解释：

```text
transparency              20
tracking_completeness     15
intent_fit                15
revenue_quality           20
policy_safety             15
stop_control              10
consistency                5
```

### 6.1 打分说明

| 维度 | 满分条件 | 低分条件 |
| --- | --- | --- |
| transparency | 提供 publisher、placement、sample URL、creative、source id | 只给总点击或要求隐藏 referrer |
| tracking_completeness | click_id、subid、ValueTrack、landing_version、offer_id 完整 | 参数缺失、postback 断裂、报表无法 join |
| intent_fit | search term 或媒体主题与页面/offer 一致 | 用户语境不明、素材承诺和页面不一致 |
| revenue_quality | approved/paid ROI 稳定，扣量低 | reported 好看但 approved/paid 差 |
| policy_safety | 无 invalid traffic、投诉、Policy issue | 出现无效流量、ad serving limit、审核问题 |
| stop_control | 能按 source/publisher/placement/subid 停 | 只能整体停量或供应商拒绝明细 |
| consistency | 至少跨 7-14 天稳定 | 单日爆量、波动异常、时段集中 |

### 6.2 评分到动作

| 分数 | 等级 | 动作 |
| --- | --- | --- |
| 90-100 | allowlist scale | 可小步扩量，继续监控 finalized / paid |
| 75-89 | allowlist test | 可维持测试预算，等待更多结算证据 |
| 60-74 | watchlist | 不扩量，补数据或缩小预算 |
| 40-59 | quarantine | 暂停新增预算，只做诊断和回款等待 |
| 0-39 | blocklist | 停源，保存证据，禁止复测除非有明确修复 |

红线规则覆盖分数：只要出现以下任一情况，直接 quarantine 或 blocklist：

- 供应商要求隐藏来源、去掉 UTM、去掉 click_id 或转成“自然流量”。
- 供应商提供补点击、模拟浏览、代理、指纹、Worker 转发、防扣量、防封号话术。
- 多次出现 invalid traffic、扣量、投诉或 buyer 拒付且无法解释。
- 素材、页面、审核页和用户页不一致。
- Offer 条款明确禁止该来源。

## 7. 名单体系

名单不是静态黑白名单，而是带证据、有效期和复审条件的决策记录。

| 名单 | 含义 | 进入条件 | 退出条件 |
| --- | --- | --- | --- |
| allowlist | 已验证可持续测试或放量 | 评分高、approved/paid 稳定、无重大风险 | 指标恶化或 policy issue |
| watchlist | 需要观察 | 数据不足、轻微波动、低样本 | 样本补足后升/降级 |
| quarantine | 暂停新增预算 | 扣量、投诉、无效流量、追踪断裂 | 修复并通过小预算复测 |
| blocklist | 禁止继续买量 | 红线、重复质量事故、来源不透明 | 原则上不恢复，除非换供应商和证据链 |
| retired | 不再使用但非黑名单 | offer 结束、source 无量、合同结束 | 新机会重新尽调 |

每条名单记录至少包含：

```text
entity_type: source / publisher / placement / subid / campaign / vendor
entity_id
status
reason_code
evidence_window
metrics_snapshot
source_urls
owner
review_due_at
decision_log
```

## 8. Placement / Publisher 诊断

Display、YouTube、Demand Gen、PMax、Native 和 Direct buy 都需要 placement 级诊断。

常见问题和判断：

| 问题 | 可能信号 | 建议动作 |
| --- | --- | --- |
| mobile accidental clicks | mobile CTR 高，session engagement 低 | 排除 app/placement，检查素材和按钮 |
| low intent publisher | click 多，outbound/lead/revenue 低 | watchlist 或 blocklist |
| bad geo mix | 非目标国家集中 | source 降级，修 location targeting |
| MFA inventory | 内容少、广告密度高、跳转多、用户价值弱 | 不作为优质 publisher 放量 |
| parked / thin content | 页面语境弱或无真实内容 | 排除，检查 Search Partners/PMax 来源 |
| adult/gambling/sensitive mismatch | 品牌安全不适合 | content suitability 或 placement exclusion |
| repeated complaints | 用户或 buyer 投诉集中 | quarantine，保存截图和 URL |
| high reported low paid | 短期收入好，结算扣量高 | 只按 paid 口径评分 |

Placement 排除要避免两个极端：一是看到单日亏损就乱排，二是明知低质量仍因短期 RPM 继续投。正确做法是记录样本窗口、金额、来源、页面和结算证据。

## 9. SubID 和 buyer feedback 闭环

Affiliate、CPL、call lead、search feed 和部分 Native 场景里，buyer feedback 是来源质量的真相层之一。Google Ads 或 tracking 平台只能告诉你点击、session 和转化；buyer 才能告诉你 lead 是否可用、是否重复、是否错 geo、是否激励、是否投诉、是否最终付款。

闭环字段：

```text
click_id
subid1..subid5
offer_id
source_id
publisher_id
placement_id
lead_id / transaction_id
buyer_status
reject_reason
approved_revenue
paid_revenue
feedback_at
```

常见 reject reason 映射：

| buyer reason | 来源解释 | 动作 |
| --- | --- | --- |
| duplicate | 重复 lead 或同用户重复提交 | 检查表单、来源、频控 |
| bad geo | 国家/州不符合 offer | 修 targeting，停坏 geo source |
| incentive | 用户因奖励提交 | block 供应商或 subid |
| invalid phone/email | 表单质量差或 bot | 加验证，停低质 placement |
| no intent | 用户不知道自己提交了什么 | 检查素材和页面披露 |
| complaint | 用户投诉 | quarantine，保存证据 |
| cap exceeded | 超 cap 后继续送量 | 连接 cap pacing 和预算 |

不要用“换链接”绕过 buyer feedback。替代 Offer 必须同意图、同披露、同来源准入，并在系统里保留版本和审批记录。

## 10. 停源、恢复和复测流程

### 10.1 停源流程

```text
发现异常
-> 确认维度：source / publisher / placement / subid / campaign / device / geo
-> 保存指标快照和页面证据
-> 暂停或降低预算
-> 写入 risk-audits
-> 更新名单状态
-> 联系供应商或 buyer
-> 等待 approved / finalized / paid 结果
-> 决定 block / quarantine / watchlist / allowlist
```

必须保存：

- 日期、时区、预算窗口。
- campaign、source、publisher、placement、subid、geo、device。
- clicks、sessions、cost、reported、approved、paid、deduction。
- invalid clicks、policy issue、complaint、buyer feedback。
- tracking URL、Final URL、landing version、creative angle。
- 供应商报表和沟通记录。

### 10.2 恢复流程

恢复不是“觉得差不多了再开”。必须满足：

1. 异常原因明确。
2. 供应商或内部修复有证据。
3. 追踪字段完整。
4. 复测预算小于原预算。
5. 复测窗口独立标记。
6. 不和稳定来源混跑。
7. 恢复后用 approved / paid 复盘。

红线来源不建议恢复。红线包括伪造流量、代理/指纹、隐藏来源、cloaking、补点击、绕过审核、封禁规避和重复拒付。

## 11. 与 Google Ads 控制对应

| 质量问题 | Google Ads / 发布商控制 | 系统动作 |
| --- | --- | --- |
| Search query 偏移 | Search terms report、negative keywords、match type | query mining、否定词建议 |
| Search Partners 质量差 | network segment、campaign isolation | source_score 降级，单独停量 |
| Display / YouTube 低质版位 | placement exclusions、account-level exclusions、placement lists | blocklist entry、导出排除清单 |
| PMax channel 异常 | channel performance report、brand exclusions、URL exclusions、search themes | PMax 诊断记录 |
| Final URL expansion 误送页面 | URL exclusions、page feeds、Final URL expansion controls | landing_version 审核和 URL QA |
| 品牌安全问题 | content suitability、sensitive category、excluded content keywords | policy_safety 降分 |
| 无效点击 | invalid clicks、invalid click rate、billing credit | invalid traffic review |
| 发布商无效流量 | traffic segmentation、Policy Center、ad serving limits | source isolation、risk audit |

这些控制只能用于真实质量治理，不能用于隐藏来源、对抗审核或规避关联检测。

## 12. 系统落地

当前系统已经实现 V1 来源质量工作台。`/source-quality` 会把 source、publisher、placement、subid、network、geo、device、sample URL、透明度、追踪完整度、intent fit、click/session、reported / approved / paid / deducted revenue、invalid clicks、complaints、buyer reject、policy issue、停源控制和样本天数保存到 `source_quality_reviews`，并计算 Source Quality Score、quality_level、recommended_action、click_session_rate、approved_rate、paid_rate、deduction_rate、paid_roi、approved_roi 和 blockers。

| 行业动作 | 系统位置 |
| --- | --- |
| 做来源质量评分和名单治理 | `/source-quality`，`source_quality_reviews` |
| 更新 allowlist / watchlist / quarantine / blocklist / retest 状态 | `/source-quality/<id>/status`，写入 `/logs` |
| 录入来源质量资料和官方政策 | `/sources` |
| 记录异常来源、停源、扣量和投诉 | `/risk-audits` |
| 在机会测算中加入来源分 | `/calculators` 的 `source_score` |
| 导入每日 cost、click、conversion、revenue | `/metrics/import` |
| 生成亏损、低收入和无效流量检查建议 | `/optimization` |
| 管理换链接但要求人工审核 | `/links` |
| 留存审计日志 | `/logs` |

`source_quality_reviews` 的状态只代表内部名单治理，不会自动修改 Google Ads placement exclusion、negative keyword、publisher 后台或联盟后台。表单文本如果包含 Cookie、cloaking、隐藏来源、模拟自然流量、补点击、刷展示、代理/指纹/Worker、防关联、封禁换号等语义，会被拦截并改走风险审计与修复流程。

V1 字段：

```text
source_quality_reviews:
  offer_id, campaign_draft_id, name, entity_type,
  source_name, publisher_name, placement_ref, subid,
  network, country, device, sample_url,
  transparency_level, tracking_completeness_percent,
  intent_fit_score, clicks, sessions, cost,
  reported_revenue, approved_revenue, paid_revenue,
  deducted_revenue, invalid_click_rate_percent,
  complaint_count, buyer_reject_rate_percent,
  policy_issue_state, stop_control, consistency_days,
  score, quality_level, recommended_action,
  click_session_rate, approved_rate, paid_rate,
  deduction_rate, paid_roi, approved_roi,
  blockers, status, notes, source_urls
```

V1 评分权重保持可解释：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| 来源透明 | 20 | full / partial / opaque，对应能否解释 source、publisher、placement |
| 追踪完整 | 15 | UTM、ValueTrack、subid、landing version、postback 是否能串起来 |
| 意图匹配 | 15 | query、placement theme、页面和 Offer 是否同意图 |
| 收入质量 | 20 | approved、paid、deduction、ROI 是否支持扩量 |
| 政策安全 | 15 | invalid click、投诉、buyer reject、policy issue 是否可控 |
| 停源控制 | 10 | 能否按 source / placement / subid 精确停量 |
| 稳定性 | 5 | 样本天数和跨日表现是否足够 |

recommended_action 的含义：

| 动作 | 含义 |
| --- | --- |
| allowlist_scale | 透明、可追踪、有 paid / approved 支撑，可进入小幅扩量审批 |
| allowlist_test | 基本合格，但仍需小预算测试或等待更多 paid evidence |
| watchlist_no_scale | 可继续观察，不加预算 |
| quarantine_diagnose | 暂停新增预算，排查追踪、来源、buyer feedback 或政策问题 |
| blocklist_stop | 停源或禁止复测，除非有独立修复证据和复测审批 |

后续可把 V1 表拆分为更细的事实表和决策表：

```text
traffic_sources
publisher_placements
source_quality_daily
source_quality_decisions
source_blocklist_entries
source_feedback_events
placement_exclusion_exports
source_retest_runs
```

关键字段建议：

```text
traffic_sources:
  id, name, source_type, vendor_name, allowed_channels,
  tracking_requirements, status, owner, notes

publisher_placements:
  id, source_id, publisher_name, placement_type, placement_url,
  google_ads_placement, app_id, youtube_channel, status

source_quality_daily:
  day, source_id, publisher_id, placement_id, campaign_id,
  clicks, sessions, cost, reported_revenue, approved_revenue,
  paid_revenue, rejects, deductions, invalid_clicks,
  complaints, policy_issues, score

source_quality_decisions:
  entity_type, entity_id, old_status, new_status,
  reason_code, evidence_window, metrics_snapshot, source_urls,
  approved_by, decided_at
```

V1 不直接调用 Google Ads 后台修改 placement exclusions，也不做 Cookie 操作。系统只生成评分、名单、审计和导出建议；实际投放变更通过人工审核、Google Ads Editor、官方 API 或 Scripts 安全通道完成。

## 13. ADXKit 对应点和完成形态

ADXKit 类工具通常会把套利团队需要的自动化包装成“找来源、换链接、看 ROI、放量、优化”的工作台能力。对来源质量这一点，本系统的安全完成形态是：

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| source / offer 表现看板 | 用导入指标和来源评分解释，不抓 Cookie 后台 |
| 自动优化来源 | `/source-quality` 生成 allowlist、watchlist、quarantine、blocklist 建议，不自动绕过平台 |
| placement / publisher 管理 | 保存 placement evidence、Source Quality Score、blockers 和状态流，不做规避检测 |
| link rotation | 只允许同意图、已审核替代链接，记录原因和人工审计 |
| traffic quality monitor | 监控 click/session/revenue/deduction/complaint，不补量 |
| scale checklist | 以 allowlist、cap、paid revenue、policy safety 为扩量条件 |

完成标准：

- 有完整原理解释和来源 URL。
- 能说明 source、publisher、placement、subid、buyer feedback 的关系。
- 能把来源分数转成名单动作。
- `/source-quality` 能保存评审、计算 blockers、更新状态并写入 `/logs`。
- 能解释 Google Ads placement exclusion、content suitability、PMax channel report、Search terms 与来源治理的关系。
- 能指导系统未来拆表和导出排除清单。
- 明确不实现代理、指纹、Worker 转发、cloaking、刷量、Cookie 后台操作和封禁规避。

## 14. QA 清单

上线或放量前逐项检查：

- 是否知道该流量从哪里来，用户为什么点击。
- 是否有 source、publisher、placement 或 subid。
- 是否允许 UTM、ValueTrack、click_id、subid 和 postback。
- 是否能按来源停量，而不是只能整体停预算。
- Offer 条款是否允许该来源、国家、设备和页面类型。
- 素材承诺、landing page、offer、最终链接是否一致。
- 是否有 click -> session、session -> revenue、reported -> approved -> paid 漏斗。
- 是否有 cap、payout、status 变更监控。
- 是否有 invalid clicks、Policy Center、ad serving limit、complaint 监控。
- 是否记录名单状态、原因、证据窗口和复审日期。
- 是否只按 paid/approved 口径扩量，而不是按单日 reported revenue 扩量。
- 是否禁止隐藏来源、补点击、模拟自然流量、代理/指纹、Worker 转发和 cloaking。

## 15. 信息来源 URL

- Google AdSense Help, Traffic provider checklist: https://support.google.com/adsense/answer/3332805
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google AdSense Help, Set up a traffic segmentation plan: https://support.google.com/adsense/answer/2583698
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google Ads Help, Managing invalid traffic: https://support.google.com/google-ads/answer/11182074
- Google Ads Help, Exclude placements at the account level: https://support.google.com/google-ads/answer/7331110
- Google Ads Help, Exclude specific webpages and videos: https://support.google.com/google-ads/answer/2454012
- Google Ads Help, Use placement exclusion lists: https://support.google.com/google-ads/answer/9162992
- Google Ads Help, About content suitability: https://support.google.com/google-ads/answer/12764663
- Google Ads Help, About the Google Display Network: https://support.google.com/google-ads/answer/2404190
- Google Ads Help, View Performance Max channel performance reporting: https://support.google.com/google-ads/answer/16260130
- Google Ads Help, Search targeting and brand controls in Performance Max: https://support.google.com/google-ads/answer/16672776
- Google Ads Help, About the search terms report: https://support.google.com/google-ads/answer/2472708
- Google Ads Help, About ValueTrack parameters: https://support.google.com/google-ads/answer/2375447
- Voluum, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
- IAB UK, A guide to identifying Made for Advertising websites: https://www.iabuk.com/news-article/guide-identifying-made-advertising-websites
- IAB UK, Made for Advertising website definition: https://www.iabuk.com/jargon-buster/made-advertising-mfa-website
- Google Ads Policy, Destination requirements: https://support.google.com/adspolicy/answer/6368661
