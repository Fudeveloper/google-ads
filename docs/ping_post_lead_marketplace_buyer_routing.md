# Ping/Post、Lead Buyer Routing 与线索市场治理手册

更新时间：2026-06-09

本文解释 CPL / CPA / Lead arbitrage 中的 lead marketplace 机制：为什么一个表单提交不是简单转发给 buyer，而是要经过 ping、bid、cap、buyer routing、exclusive/shared 边界、consent、post、reject、feedback 和结算确认。目标是帮助团队理解线索市场的真实经济模型、质量风险和可审计流程。

本文不是法律意见，也不提供绕过 consent、伪造 lead、自动提交表单、隐藏来源、规避 DNC/TCPA、补点击、刷展示、cloaking、Cookie 后台接管或规避账号关联的执行方案。系统落地只做知识、字段、评分、审计、QA、对账和人工审批。

## 1. 为什么 Ping/Post 和 Buyer Routing 是 CPL 套利核心

Lead arbitrage 的表面动作是“买点击，收 lead，卖给 buyer”。但在成熟市场里，真正决定利润的不是 submitted lead 数量，而是：

- 哪些 buyer 愿意接这条 lead。
- buyer 愿意出多少钱。
- buyer 是否还有 daily / monthly cap。
- 这条 lead 是 exclusive、shared、aged 还是重复线索。
- 用户是否明确知道谁会联系自己、为什么联系、用什么渠道联系。
- lead 被接收后能否成为 qualified、billable、paid。
- 拒绝原因能否回传到 source、campaign、keyword、creative、landing 和 form version。

如果团队只看表单 CVR，会把预算推向“容易提交但无人接、低价接、低意图、投诉高、结算扣量大”的来源。Ping/Post 和 routing 的作用，是在提交后几百毫秒到几秒内判断这条 lead 有没有合规买方、最佳买方和可收回收入。

核心公式要从单一 payout 变成 expected payable value：

```text
Expected EPC =
  Lead Submit Rate
  * Buyer Acceptance Rate
  * Expected Accepted Payout
  * Qualification Rate
  * Approval/Paid Rate
  * Compliance Survival Factor
```

对套利团队来说，`no buyer`、`cap reached`、`duplicate`、`bad geo`、`no consent` 和 `shared lead complaint` 都是利润模型的一部分，不是技术异常。

## 2. 原理解释：Lead Marketplace 不是简单表单转发

线索市场的基本结构如下：

```text
Ad click
  -> Landing page / Lead form
  -> Validation and consent evidence
  -> Ping with minimum necessary fields
  -> Buyer matching, cap check, bid / accept / reject
  -> Routing decision
  -> Post full lead to selected buyer(s)
  -> Buyer response and buyer lead ID
  -> Postback / status feedback
  -> Quality review, scrub, invoice, paid
```

关键点：

- `Ping` 是“询价和匹配”，通常只发送足够判断资格、地区、产品、cap 和出价的最小字段。
- `Post` 是“交付完整线索”，只应在 consent、buyer disclosure、routing 结果和数据最小化条件满足后发生。
- `Accept` 不等于 `Paid`。Buyer 初始接受只代表愿意收这条 lead，后续仍可能因为重复、联系不上、低意图、投诉、资格不符或政策问题拒付。
- `Routing` 不只是技术分发，它决定收入、用户体验、投诉责任、buyer 关系和数据处理义务。
- `Buyer feedback` 必须回写投放决策，否则 Google Ads 会被 submitted lead 或浅层 conversion 训练偏。

## 3. 核心对象地图

| 对象 | 作用 | 套利关注点 |
| --- | --- | --- |
| Lead source | 广告、关键词、publisher、creative、landing | 质量、投诉、重复、bad geo、低意图 |
| Lead form version | 字段、文案、consent、披露版本 | 是否和 buyer / offer / privacy 一致 |
| Ping request | 初步匹配数据 | 最小必要字段、不可带完整 PII 到过多 buyer |
| Buyer | 直接广告主、代理、呼叫中心、aggregator | payout、cap、合规、反馈、付款 |
| Buyer campaign | buyer 的某个产品/地区/资格规则 | geo、vertical、hours、cap、price |
| Routing rule | waterfall、auction、priority、exclusive/shared | 收入最大化与合规边界 |
| Bid response | buyer 的 accept/reject/bid/cap/no-buyer | 有效 EPC、no buyer 风险 |
| Post event | 完整 lead 交付 | consent、buyer disclosure、buyer lead ID |
| Suppression / DNC | 不可联系或不可出售名单 | 投诉、撤回同意、重复购买 |
| Buyer feedback | contacted、qualified、sold、approved、paid、reject | 真实利润和优化闭环 |

这些对象要和广告维度绑定：`gclid / click_id / campaign / ad_group / keyword / creative / landing / source / subid / form_version / consent_version / buyer / routing_rule`。

## 4. Direct Post vs Ping/Post

Direct Post：

- 用户提交后，系统直接把完整 lead 发给固定 buyer 或 CRM。
- 适合单一 buyer、单一 offer、明确 consent、固定 payout 和稳定 cap 的场景。
- 优点是简单、延迟低、字段映射少。
- 缺点是 buyer cap、reject、no buyer 或 payout 变化会直接影响收入，缺乏价格发现。

Ping/Post：

- 先以有限字段 ping 多个 buyer 或 buyer group。
- buyer 根据规则返回 accept / reject / bid / cap / duplicate / invalid。
- 系统根据价格、优先级、exclusive/shared、cap、质量、合规和历史 paid rate 选择 post 对象。
- 适合多 buyer、动态价格、地区差异、cap 不稳定和 lead auction 场景。
- 缺点是合规复杂、延迟更高、日志和数据最小化要求更强。

选择规则：

| 场景 | 推荐 |
| --- | --- |
| 单一直接广告主，固定合同，固定价格 | Direct Post |
| 多 buyer 同时买同类 lead | Ping/Post |
| Buyer cap 波动大 | Ping/Post + cap snapshot |
| 用户只同意单一主体联系 | Direct Post 或单 buyer routing |
| 需要 exclusive 高价 lead | Ping/Post 只能选一个 buyer post |
| Consent 没有披露 buyer group | 不应 shared post |

Direct Post 不是低级形态，Ping/Post 也不是自动更高级。套利团队要根据 consent、buyer 合同、cap、价格发现和反馈能力选择。

## 5. Ping 字段和数据最小化

Ping 的原则是 minimum necessary：只发送 buyer 判断资格、地区、产品、cap 和出价所必需的数据。不要在 ping 阶段把完整姓名、完整电话、邮箱、地址、敏感健康/金融详情发送给一批未知 buyer。

常见 ping 字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| vertical / product_type | 匹配 buyer campaign | 必须和页面承诺一致 |
| geo / state / zip3 | 地区资格和价格 | 避免过度精细定位 |
| lead_age_seconds | 新鲜度 | aged lead 要单独披露 |
| source_type | search、native、social、organic 等 | 不能隐藏禁用来源 |
| consent_scope | 是否可电话/短信/邮件/指定 buyer 联系 | 不是一个布尔值 |
| form_version_id | 披露和字段版本 | 便于争议复盘 |
| partial phone hash / email hash | 重复检测 | 避免明文过度扩散 |
| service intent | 用户选择的需求 | 不要夸大成购买意向 |
| requested_contact_time | 坐席容量和时区 | 影响联系率 |

高风险字段：

- 完整电话、完整邮箱、完整地址。
- SSN、身份证、银行卡、医疗病史、精确信贷状态。
- 通过 URL、subid、日志标题或前端可见参数传递的 PII。
- 用户未披露会被多个 buyer 接收的信息。

Ping 请求本身也要可审计：

```text
ping_event_id
lead_event_id
routing_rule_id
buyer_campaign_id
fields_sent_schema
pii_level
consent_version_id
source_policy_status
request_time
response_time
buyer_response_code
bid_amount
reject_reason
cap_snapshot_id
```

## 6. Post、Buyer Accept 和 Reject

Post 是把可交付 lead 发送给被选中的 buyer。一个合格 post 事件至少要记录：

- post 给哪个 buyer / buyer campaign。
- 使用哪个 routing rule。
- 用户看到的 buyer disclosure 或 buyer group disclosure。
- 发送了哪些字段，字段来自哪个 form version。
- buyer 返回的 lead ID、状态、价格和 reject reason。
- 是否 exclusive、shared、aged 或 transfer。
- 后续状态更新如何关联。

Buyer 初始响应常见类型：

| 响应 | 含义 | 投放动作 |
| --- | --- | --- |
| accepted | buyer 接收 lead | 进入后续质量/付款观察 |
| rejected_duplicate | buyer 已见过该用户 | 查重复来源、去重窗口 |
| rejected_bad_geo | 地区不符合 | 修广告定位、页面国家说明 |
| rejected_invalid_contact | 联系方式无效 | 修表单验证和来源质量 |
| rejected_no_consent | 同意证据不足 | 停止该流程，审 consent |
| rejected_cap_reached | buyer cap 满 | 降预算、换合法 fallback |
| rejected_low_intent | 用户意图弱 | 修 query、creative、form question |
| no_bid / no_buyer | 没有 buyer 接 | 降估值或暂停 source |

不要把 rejected lead 继续“换壳”卖给未披露 buyer，也不要用补点击、伪造通话或模拟下游行为修报表。正确做法是回到 source、页面、consent、buyer cap 和质量模型。

## 7. Exclusive / Shared / Aged Lead 边界

Exclusive lead：

- 一条 lead 只卖给一个 buyer。
- 通常价格高，投诉和数据扩散风险较低。
- 适合高价值、高监管或 buyer 要求强的垂类。
- 需要记录排他窗口、buyer、价格和是否允许后续转售。

Shared lead：

- 一条 lead 可以给多个 buyer。
- 单价可能低，但总收入可能高。
- 用户被多人联系，投诉、DNC、撤回同意和披露风险显著上升。
- 必须清楚说明可能联系的主体或主体类别，并按适用规则处理 consent、opt-out 和 suppression。

Aged lead：

- 不是实时新提交，可能来自历史表单、未售出库存或旧线索再营销。
- 价格低、联系率低、投诉风险高。
- 必须区分 lead age、原始 consent、是否仍可联系、是否已撤回、是否过 DNC/suppression。

治理原则：

| 类型 | 必备字段 |
| --- | --- |
| Exclusive | exclusive_window、buyer_id、post_count=1、resale_allowed |
| Shared | max_buyer_count、buyer_disclosure_version、contact_frequency_guard |
| Aged | original_submit_time、lead_age_bucket、consent_refresh_status、suppression_check |

共享不是技术开关，而是用户预期和合规承诺。页面写“合作伙伴可能联系你”但没有解释范围、主体、用途和渠道，在电话/短信场景尤其危险。

## 8. Buyer Routing：waterfall、auction、priority、cap、bid

常见 routing 模式：

| 模式 | 原理 | 风险 |
| --- | --- | --- |
| Waterfall | 按顺序询问 buyer，前一个拒绝再问下一个 | 早位 buyer 吃掉高质 lead，后位 buyer 质量差 |
| Auction / RTB | 多 buyer 同时或近实时出价，选择最高有效价值 | 合规、延迟和字段最小化更复杂 |
| Priority | 按合同、战略关系或质量优先级路由 | 可能牺牲短期价格 |
| Weighted split | 按比例分给多个 buyer | 需要稳定质量反馈 |
| Exclusive first, shared fallback | 先找独家高价，失败再共享 | 必须符合用户披露和合同 |
| Cap-aware routing | 按 buyer cap、时段、坐席容量调整 | cap 数据必须及时 |

不要只按最高 bid 排序。有效 routing value 应考虑：

```text
Effective Buyer Value =
  Bid or Payout
  * Buyer Acceptance Rate
  * Qualification Rate
  * Paid Rate
  * Payment Reliability
  * Complaint Survival Factor
  * Contract Risk Factor
```

一个出价高但拒付、投诉、付款慢或反馈差的 buyer，实际价值可能低于低价但稳定的直接 buyer。

推荐 routing 决策顺序：

1. Consent / disclosure 是否允许该 buyer 或 buyer group。
2. Offer 条款是否允许当前 source、geo、device、creative 和 form。
3. Suppression / DNC / opt-out 是否通过。
4. Buyer campaign 是否匹配垂类、地区、资格、营业时间。
5. Cap、budget、坐席容量是否可接。
6. 历史 paid rate、reject reason、complaint rate 是否在阈值内。
7. 价格、优先级、exclusive/shared 策略。
8. Post 后保存 buyer response 和后续 feedback。

## 9. Lead Cap、Buyer Capacity 和 No Buyer 风险

Cap 是 lead marketplace 最容易被低估的利润风险。常见 cap：

- Buyer daily lead cap。
- Buyer monthly budget cap。
- Geo / state cap。
- Source / publisher cap。
- Hour-of-day / business hours cap。
- Product / qualification cap。
- Exclusive lead cap。
- Complaint / bad quality triggered cap。

如果广告预算没有同步 cap，结果会变成：

- 高峰时段继续买点击，但 buyer 已经不接。
- 系统把高意图 lead 卖给低价 fallback。
- no buyer 和 cap reached 被误记为普通转化。
- Google Ads 按 submitted lead 学习，预算推高亏损流量。

系统应保存 cap snapshot：

```text
cap_snapshot_id
buyer_id
buyer_campaign_id
cap_type
cap_limit
cap_used
cap_remaining
effective_from
source_of_truth
checked_at
staleness_seconds
```

运营规则：

| 事件 | 动作 |
| --- | --- |
| primary buyer cap < 20% | 降低 campaign pacing 或触发人工检查 |
| no buyer rate 上升 | 暂停扩量，查 buyer availability |
| cap reached 但广告继续花费 | 记录预算事故 |
| fallback payout 低于 safe CPC 模型 | 停止该 source 或改出价 |
| buyer feedback 延迟 | 降低该 buyer 的 routing weight |

## 10. Consent、Disclosure、TCPA、DNC 和数据分享

Lead routing 的合规问题不在“能不能技术发送”，而在“用户是否清楚理解并同意”。尤其在美国电话、短信和自动化联系场景，要同时考虑 TCPA、FCC、FTC Telemarketing Sales Rule、Do Not Call、州法和合同要求。

要拆开的字段：

```text
consent_scope
contact_channel_allowed
seller_name
buyer_name_or_group
buyer_list_url
disclosure_text_hash
privacy_policy_url
tcpa_language_version
dnc_disclosure_version
consent_time
consent_source_url
revocation_time
suppression_status
```

原则：

- Consent 不是“有 checkbox 就够”。要保存用户看到的文案、页面版本、时间、渠道、buyer disclosure 和适用范围。
- 电话、短信、邮件、人工外呼、自动拨号、预录音或 AI 语音不是同一种权限。
- Shared lead 必须比 exclusive lead 更严格，因为用户会被多个主体联系。
- 用户撤回同意、进入 DNC 或投诉后，要停止后续 routing，并向已接收 buyer 同步 suppression。
- 不要把完整 PII 放进广告 URL、UTM、subid、公开报表、普通日志或无需访问的 BI 表。

截至 2026-06-09，FCC 曾经针对 lead generator 的 one-to-one consent 规则已经受法院裁决影响并由 2025 年 FCC 文件删除；这不代表可以模糊 consent，而是意味着系统必须记录法规来源日期，并以当前 FCC/eCFR/FTC/律师意见为准持续更新。

## 11. Payout Selection 和 Effective EPC

Ping/Post 的收入口径不能只取最高 `bid_amount`。至少要保存这些价格：

| 价格 | 含义 |
| --- | --- |
| list payout | 合同或平台显示价格 |
| bid amount | buyer ping response 出价 |
| accepted payout | post 后 buyer 初始确认金额 |
| adjusted payout | 后续质量/地区/字段调整金额 |
| approved payout | 审核后可计费金额 |
| paid payout | 实际到账金额 |

Effective EPC 示例：

```text
Lead Submit Rate = submitted / clicks
Routed Rate = posted / submitted
Accepted Rate = accepted / posted
Approved Rate = approved / accepted
Paid Rate = paid / approved
Effective Payable Payout = paid_revenue / submitted
```

投放优化建议：

- Google Ads primary conversion 不应使用 submitted lead，除非仅做浅层观察。
- 自动出价学习更适合 approved、qualified、sold 或 paid 口径。
- buyer 的 `accepted` 可以作为中间指标，但不能直接当利润。
- no buyer / cap reached 要从 conversion 中分离出来，避免污染出价。
- 每个 buyer、routing rule 和 source 都要有 paid-rate 折扣。

## 12. Buyer Feedback 闭环

高质量 lead arbitrage 的关键是把 buyer 结果回到广告优化：

```text
buyer_response
  -> contact_attempted
  -> contacted
  -> qualified
  -> appointment / quote / application
  -> sold / approved
  -> paid
  -> refund / chargeback / complaint
```

建议反馈字段：

| 字段 | 用途 |
| --- | --- |
| buyer_lead_id | 对账和争议 |
| buyer_status | 状态迁移 |
| reject_reason | source / form / geo 修复 |
| contact_attempt_count | 坐席和联系策略 |
| contacted_at | 联系率和时间延迟 |
| qualified_flag | 意图和资格 |
| sale_value | LTV 或成交价值 |
| chargeback_flag | 退款/拒付风险 |
| complaint_flag | consent 和 buyer 行为风险 |
| feedback_received_at | 延迟治理 |

反馈使用：

- duplicate 高：查跨渠道重复、hash 去重、buyer 去重窗口。
- bad geo 高：查 Google location options、页面国家、zip 校验。
- invalid contact 高：查表单激励、字段校验、低质 source。
- low intent 高：查 query、广告承诺、页面标题、表单问题。
- complaint 高：暂停 source，审 consent、buyer disclosure、联系频率。
- no buyer 高：查 cap、buyer availability、fallback 价格。
- paid rate 低：降低 routing weight 和出价上限。

## 13. 常见事故：duplicate、bad geo、no buyer、cap reached、low intent、投诉、chargeback

| 事故 | 表面现象 | 根因 | 第一动作 |
| --- | --- | --- | --- |
| Duplicate | buyer 大量拒绝 | 用户重复、跨 source 重复、转售历史 | 建 hash 去重、按 source 查重复率 |
| Bad geo | accepted 低 | 广告定位、页面国家、邮编误导 | 修 location targeting 和表单验证 |
| No buyer | submitted 高但无收入 | cap 满、buyer 不匹配、时段不接 | 降预算、关 source、更新 cap |
| Cap reached | 高峰后收入断崖 | 买量 pacing 和 buyer capacity 脱节 | 加 cap snapshot 和 stop rule |
| Low intent | qualified 低 | 文案夸大、用户不懂谁联系 | 修 claim、披露和筛选问题 |
| Complaint | DNC/TCPA 风险 | consent 不清、shared lead 过度联系 | 立即暂停并同步 suppression |
| Chargeback / scrub | 结算扣量 | buyer 质量差、source 差、合同不清 | 查 evidence、降权 buyer/source |
| Missing feedback | pending 堆积 | buyer 没有状态回传 | 降低信任，暂停扩量 |

事故复盘必须按 `source + campaign + keyword + creative + landing + form_version + buyer + routing_rule` 拆，不要只看 offer 总量。

## 14. Routing Quality Score

可以用一个可解释评分来约束自动化建议：

```text
Routing Quality Score =
  0.20 * consent_integrity
  + 0.15 * buyer_match_rate
  + 0.15 * cap_freshness
  + 0.15 * acceptance_rate
  + 0.15 * paid_rate
  + 0.10 * feedback_freshness
  + 0.10 * complaint_safety
```

评分解释：

| 维度 | 看什么 |
| --- | --- |
| consent_integrity | disclosure、buyer scope、channel、timestamp 是否完整 |
| buyer_match_rate | ping 后可接 buyer 比例 |
| cap_freshness | cap snapshot 是否新鲜 |
| acceptance_rate | post 后 buyer 接收率 |
| paid_rate | approved / paid 口径 |
| feedback_freshness | buyer 是否及时回传状态 |
| complaint_safety | DNC、投诉、退款、scrub 是否低 |

动作阈值：

| 分数 | 动作 |
| --- | --- |
| 85-100 | 可稳定放量，但仍受 cap 和结算窗口限制 |
| 70-84 | 小步扩量，观察 buyer feedback |
| 50-69 | 保持或降预算，修 source/form/buyer |
| < 50 | 暂停 source 或 routing rule，进入审计 |

## 15. 系统落地

当前 V1 已经支持：

| 需求 | 当前位置 |
| --- | --- |
| Offer payout、国家、限制、政策备注 | `/offers` |
| 成本、转化、收入 CSV 导入 | `/metrics/import` |
| ROI、RPV、CPC、CVR 优化建议 | `/optimization` |
| 来源质量、政策和证据记录 | `/sources`、`/risk-audits` |
| Lead 质量与电话 Lead 知识 | `/knowledge/lead_quality`、`/knowledge/lead_call_tracking` |
| Ping/Post routing 门禁 | `/ping-post-routing`，`ping_post_routing_reviews` |

`/ping-post-routing` V1 已实现为安全评审工作台，而不是可执行 post lead 工具。它保存：

- routing mode、lead type、buyer group、source type、form version。
- consent scope、buyer disclosure、ping field scope、PII level。
- suppression/DNC、cap snapshot、fallback、buyer feedback、source policy。
- buyer count、max post buyers、pinged/accepted/posted buyers、cap remaining、lead age、ping latency。
- expected bid、fallback payout、accept/qualified/paid/no-buyer/reject/duplicate/complaint rate。
- fields sent schema、routing rule summary、buyer disclosure notes、reject reason map、fallback policy、buyer feedback plan、suppression notes、consent evidence。
- Routing Quality Score、expected payable value per lead、safe CPL、recommended action、blockers、status、source URLs。

状态流包括 open、reviewed、consent_review、field_minimization、cap_refresh、routing_review、fallback_review、buyer_feedback_review、suppression_review、manual_test、routing_ready、blocked 和 closed。状态更新只写入 `/logs`，不自动 post lead、不自动外呼/短信、不绕过 consent/DNC、不切换 buyer、不操作广告后台。

后续可扩展表：

```text
lead_buyer_accounts
lead_routing_rules
lead_ping_events
buyer_bid_responses
lead_post_events
lead_cap_snapshots
buyer_feedback_events
lead_consent_share_records
lead_suppression_checks
routing_quality_decisions
```

安全边界：

- 不保存不必要完整 PII。
- 不把 PII 放入 URL、subid、日志标题或公开报表。
- 不自动外呼、短信群发、伪造 lead 或补 conversion。
- 不做 Cookie 登录、后台接管、2FA 绕过或审核规避。
- 不做 cloaking 或审核页/用户页不一致。
- 自动化只生成 QA、评分、预算建议、审批任务和审计记录。

## 16. ADXKit 对应点和完成形态

ADXKit 类工具在套利团队里常被期待做“自动投放、换链接、创意、落地页、数据同步、任务调度、Cookie 后台操作”。本项目对 Ping/Post 和 buyer routing 的完成形态是：

| ADXKit 类能力 | 本项目完成形态 |
| --- | --- |
| Offer / buyer 管理 | 用文档和未来 `lead_buyer_accounts` 设计解释 buyer、cap、payout、feedback |
| 自动换链接 | 只做合规 link rotation 和 fallback 审计，不做 cloaking |
| 自动投放优化 | 用 paid/approved/buyer feedback 口径给预算建议，不直接改后台 |
| 数据同步 | 通过 CSV/API 合规导入 buyer feedback，不用 Ads Cookie |
| 创意优化 | 把 low intent、complaint、reject reason 回到 creative brief |
| 高风险后台操作 | 只做风险原理、审计和安全替代，不交付会话接管 |

这意味着“核心功能”不是复制对抗动作，而是复制套利业务真正需要的判断链：lead 是否可卖、卖给谁、是否合规、能否回款、该不该继续买这类点击。

## 17. QA 清单

- Offer 条款是否允许当前 source、geo、form、lead type 和 buyer handoff。
- 页面是否清楚说明收集主体、联系主体、用途、渠道和隐私政策。
- Shared lead 是否有比 exclusive lead 更明确的 buyer disclosure。
- Ping 是否只发送最小必要字段。
- Post 是否只发给 consent 和 routing 允许的 buyer。
- 是否保存 buyer response、buyer lead ID、bid、reject reason、cap snapshot。
- 是否区分 submitted、posted、accepted、qualified、approved、paid。
- 是否把 no buyer、cap reached、duplicate、bad geo、no consent 从 conversion 里拆出来。
- 是否有 suppression / DNC / opt-out 同步流程。
- 是否按 source、keyword、creative、landing、form version 和 buyer 复盘质量。
- 是否把 paid/approved feedback 作为出价学习依据，而不是 submitted lead。
- 是否禁止 Cookie 后台、绕过登录、安全挑战、刷量、cloaking 和规避封禁。

## 18. 信息来源 URL

- FTC, Follow the Lead: An FTC Workshop on Lead Generation: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- FTC, Staff Perspective: Follow the Lead: https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- FTC, .com Disclosures: How to Make Effective Disclosures in Digital Advertising: https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising
- FCC, TCPA one-to-one consent rule court response / deletion order: https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- eCFR, 16 CFR 310.5 Recordkeeping requirements: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5
- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Policies, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policies, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Voluum Documentation, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
- TUNE, Offer Payouts and Caps: https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps
- Everflow API, Get Offer: https://developers.everflow.io/docs/affiliate/offers/
- PingTree Documentation, Ping Post: https://docs.pingtree.com/documentation/campaign/distribution/ping-post
- ActiveProspect, LeadConduit: https://activeprospect.com/products/leadconduit/
