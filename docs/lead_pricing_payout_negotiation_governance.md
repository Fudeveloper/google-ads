# Lead Pricing、Payout Negotiation 与结算安全垫治理手册

更新时间：2026-06-09

本文解释 CPL / CPA / Call Lead / Appointment Lead arbitrage 中，lead buyer、affiliate network、direct advertiser 和 lead marketplace 如何给 lead 定价，投放团队如何用质量证据、来源透明、buyer feedback、return window、scrub rate、cap、exclusivity 和 payment term 判断真实可赚空间。它承接 [Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md)、[Lead 质量、Postback 对账与拒付管理手册](lead_quality_postback_reconciliation.md)、[CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md) 和 [单位经济模型、Break-even 与安全边际手册](unit_economics_margin_safety.md)，重点回答：不同 payout model 本质上把哪些风险转移给谁，套利团队怎样用成熟 paid 数据谈价，而不是被 headline payout 诱导扩量。

本文不是法律或财务建议，也不提供伪造 lead、模拟通话、补转化、隐藏来源、cloaking、Cookie 后台操作、绕过 buyer 风控、规避 DNC/TCPA 或封禁后换号的方案。系统只做定价口径、证据、QA、来源 URL、审计和人工审批。

## 1. 为什么 Lead Pricing 决定套利天花板

套利利润不是由最高 payout 决定，而是由扣量后可收款 EPC 决定：

```text
paid_epc =
  click_to_lead_rate
  * accepted_rate
  * qualified_rate
  * approval_rate
  * paid_rate
  * unit_payout

profit_per_click =
  paid_epc
  - cpc
  - tracking_cost
  - content_cost
  - cashflow_cost
  - dispute_loss_reserve
```

很多亏损来自把定价模型看成一个数字：

- `$80 CPL` 实际只付 qualified lead，submitted lead 不值钱。
- `accepted lead payout` 看似高，但 14 天 return window 后 scrub 30%。
- Pay-per-call 只付 qualified call duration，不付 call click 或 missed call。
- Appointment payout 高，但 no-show / cancel 后被退回。
- RevShare 看似长期价值高，但 refund、chargeback、payment lag 和 attribution 很长。
- 高 payout buyer cap 很小，低价 buyer 才有容量，平均 payout 不能扩量。

所以定价治理的目标不是追最高单价，而是找到可稳定收款、可解释拒付、可扩量的 net value。

## 2. 原理解释：定价模型是风险分配机制

每种 payout model 都在买卖双方之间分配风险：

| 模型 | Buyer 承担 | Publisher / 投放方承担 |
| --- | --- | --- |
| Raw CPL | 更多质量风险 | 较少后端审核风险，但投诉和退回仍存在 |
| Qualified CPL | 只付合格风险较小 | 表单、来源、意图和联系质量风险更大 |
| Pay-per-call | 接电话和销售转化风险 | 通话时长、错服务、误点、missed call 风险 |
| Appointment | 到店/咨询前流程风险 | booked、showed、cancel/no-show 风险 |
| CPA / Sale | 销售风险较低 | 长延迟、低样本、退款和销售团队影响 |
| RevShare | 持续运营风险共享 | 现金流、LTV、退款、归因和结算透明风险 |
| Hybrid | 双方分摊 | 对账和重复计费复杂度更高 |

价格越靠近最终收入事件，单价通常越高，但回传越慢、样本越少、现金风险越大。价格越靠近前端 submit，单价通常越低，但可以更快学习和优化。

## 3. 核心对象地图

| 对象 | 解释 | 套利治理作用 |
| --- | --- | --- |
| pricing model | raw CPL、qualified CPL、call、appointment、CPA、revshare | 决定优化目标和延迟窗口 |
| unit payout | 每个可计费事件的价格 | 需要按 geo、buyer、quality、tier 版本化 |
| rate card | 按垂类、地区、类型、质量定义的价格表 | 谈判和预算输入 |
| floor / minimum payout | 最低可接受价格 | 防止高成本 source 被低价 buyer 吞掉 |
| tiered payout | 按量、质量、exclusive、state 或 buyer 等级变化 | 防止平均 payout 误导 |
| scrub buffer | 预留拒付/退回/扣量安全垫 | 进入 safe CPC |
| return window | buyer 可退回 lead 的期限 | 决定收入成熟期 |
| cap / capacity | buyer 可接收数量和预算 | 决定扩量上限 |
| exclusivity | exclusive、shared、aged、recycled | 决定价格、投诉和重复风险 |
| payment term | net 7/15/30/45、threshold、hold | 决定现金流成本 |
| quality evidence | approved/paid、reject reason、contact rate、complaint | 谈价和保价依据 |
| dispute reserve | 争议中金额和历史损失 | 防止把 pending 当利润 |

## 4. 主要定价模型

| 模型 | 计费事件 | 适合场景 | 主要风险 |
| --- | --- | --- | --- |
| Raw CPL | submitted / accepted lead | 冷启动、小额测试、低风险垂类 | buyer 后续可能降价或提高 scrub |
| Validated CPL | 通过基础校验 lead | 有标准 validation pipeline | validation 不能替代 buyer qualification |
| Qualified CPL | buyer qualified lead | 高价值垂类、buyer 反馈成熟 | 回传慢、样本少、表单摩擦更高 |
| Exclusive CPL | 独占 lead | 高意图、本地服务、保险、法律 | consent、buyer fit、重复和投诉风险高 |
| Shared CPL | 可卖多个 buyer | marketplace、低价 volume | 用户被多方联系、投诉和重复风险 |
| Aged / Recycled Lead | 旧 lead 或再处理 lead | 低价补量、二次触达 | 意图衰减、DNC/opt-out 和投诉风险 |
| Pay-per-call | qualified call | 本地服务、法律、保险、医疗预约 | 短通话、错服务、坐席容量和录音披露 |
| Appointment | booked / showed appointment | 医疗、本地服务、B2B demo | no-show、cancel、calendar capacity |
| CPA / Sale | approved sale / account | 金融、订阅、电商、SaaS | 长延迟、退款、chargeback、低样本 |
| RevShare | net revenue share | 订阅、金融、长期客户价值 | LTV 不透明、现金流慢、归因争议 |
| Hybrid | CPL + bonus / revshare | buyer 愿意共担风险 | 对账复杂、bonus 条件易争议 |

定价模型要和 campaign goal 一致。Pay-per-call 不应优化到 call click；Appointment 不应只看 submitted form；CPA 不应用 Day 0 signup 直接放量。

## 5. Rate Card 和价格版本

Lead pricing 必须版本化：

```text
rate_card_id
buyer_id
vertical
geo
source_type
exclusivity
payout_model
unit_price
currency
qualification_definition
return_window_days
payment_term_days
effective_from
effective_to
evidence_url
reviewer
```

Rate card 不应只有一个 headline price。至少拆：

- 国家、州、城市或服务区。
- buyer / advertiser。
- source type：Search、non-brand、native、email、direct buy。
- quality tier：raw、validated、qualified、exclusive、appointment。
- device 或 call hours。
- cap / daily volume。
- return window 和 payment term。

如果 buyer 只给“最高 $120/lead”，系统应保存为 `headline_payout`，不能直接用于 safe CPC。

## 6. Effective Payout 和 Safe CPC

Effective payout:

```text
effective_payout =
  unit_payout
  * accepted_rate
  * qualified_rate
  * approval_rate
  * paid_rate
  * (1 - return_rate)
```

Safe CPC:

```text
safe_cpc =
  click_to_lead_rate
  * effective_payout
  * safety_factor
  - variable_cost_per_click
```

示例：

```text
headline CPL: 80
click_to_lead_rate: 4%
accepted_rate: 90%
qualified_rate: 55%
approval_rate: 85%
paid_rate: 95%
return_rate: 10%
safety_factor: 0.70

effective_payout = 80 * .90 * .55 * .85 * .95 * .90 = 28.77
safe_cpc = .04 * 28.77 * .70 = 0.805
```

这个例子里，`$80 payout` 最终只支撑约 `$0.80` safe CPC。若用 headline payout 直接算，投放会严重高估。

## 7. Payout Negotiation：用什么证据谈价

谈价不是说“我能给量”。Buyer 真正会为这些证据付更高价格：

| 证据 | 为什么能提价 |
| --- | --- |
| paid rate 稳定 | buyer 支付后损失少 |
| qualified rate 高 | 销售团队节省时间 |
| contact rate 高 | 电话/短信/邮件能联系到真实用户 |
| reject reason 透明 | 问题可定位可修复 |
| source/subid 透明 | buyer 能判断风险 |
| exclusive lead | 重复和抢单少 |
| consent/disclosure 证据完整 | 投诉和合规风险低 |
| speed-to-lead 配合 | 联系窗口更短 |
| geo / vertical fit 稳定 | buyer 成交率更高 |
| low complaint / opt-out | 长期合作风险低 |
| invoice / dispute 准时 | 财务和运营成本低 |

谈价前建议准备：

```text
last_30_days:
  submitted, accepted, qualified, approved, paid
  reject_reason_breakdown
  return_rate
  complaint_rate
  contact_rate
  source_mix
  form_version
  consent_version
  payment_status
```

不要用伪造质量、隐藏来源或切换账号制造“好看报表”。这种做法会把短期加价变成长期拒付和封禁。

## 8. Scrub Buffer、Return Window 和 Reserve

Scrub buffer 是对未来扣量/退回的预留。它不是悲观，而是让预算不被未成熟 revenue 误导。

建议字段：

```text
expected_scrub_rate
return_window_days
historical_return_rate_p50
historical_return_rate_p90
dispute_success_rate
payment_hold_rate
cash_reserve_days
```

预算使用：

| 状态 | 可用比例建议 |
| --- | --- |
| submitted / accepted | 20%-40% value |
| qualified 但未过 return window | 40%-65% value |
| approved 但未 paid | 60%-80% value |
| paid / settled | 80%-95% value |

如果 buyer 的 return report 经常在月末集中出现，就不能用日内 accepted revenue 扩量。必须等 return window 或至少用历史 p90 scrub buffer 折扣。

## 9. Tiered Payout、Floor、Cap 和 Step Rules

常见 tier:

| Tier | 说明 | 风险 |
| --- | --- | --- |
| volume tier | 月量越高单价越高 | 可能诱导过快扩低质来源 |
| quality tier | qualified/paid rate 达标提价 | 需要透明质量报表 |
| geo tier | 高价值州/城市更高价 | bad geo 会拉低平均 payout |
| source tier | Search non-brand 高价，native/social 低价 | 来源混跑导致结算争议 |
| exclusive tier | exclusive 高价，shared 低价 | consent 和重复风险 |
| time tier | 营业时间内 lead 更高价 | dayparting 和 buyer hours 关键 |

Floor price 在 lead 场景里不是广告位 floor，而是最低可接受 buyer payout：

```text
minimum_acceptable_payout =
  media_cost_per_lead / target_margin
  + expected_scrub_reserve
  + operational_cost
```

当 buyer bid 低于 floor：

- 不卖给该 buyer。
- 降低 Google Ads 预算。
- 切到已审核、同主题、合规的替代 buyer。
- 保留为 content / SEO nurture，而不是强行低价卖。

Cap 和 tier 需要一起看。高 tier 单价如果 cap 很小，不能支撑全量预算。

## 10. Buyer Mix、Routing 和价格瀑布

Lead marketplace 常见价格瀑布：

```text
exclusive premium buyer
-> qualified buyer pool
-> standard CPL buyer
-> shared buyer group
-> aged / nurture / no sale
```

治理原则：

- 先满足用户 consent 和 buyer disclosure，再考虑最高价格。
- 不把不符合 buyer 规则的 lead 强行卖给高价 buyer。
- 不为了更高价把 shared lead 伪装成 exclusive。
- `no buyer` 是重要信号，不应隐藏。
- buyer mix 改变后，历史 payout 和 paid rate 不能混用。

Routing 评价不只看最高 bid：

```text
buyer_value_score =
  expected_payout
  * paid_rate
  * contact_fit
  * compliance_fit
  * capacity_fit
  - dispute_risk
  - payment_lag_cost
```

## 11. Contract、Invoice 和 Payment Term

价格条款至少写清：

| 条款 | 内容 |
| --- | --- |
| payout model | raw CPL、qualified CPL、call、appointment、CPA、revshare |
| billable definition | 什么状态可计费 |
| unit price / tier | 价格、币种、geo/source/tier |
| cap | daily/monthly/source/buyer cap |
| return window | 可退回期限、reason code、证据 |
| scrub report | 字段、频率、时区、最终日期 |
| invoice package | approved count、credit、return、tax、period |
| payment term | net days、threshold、hold、付款方式 |
| adjustment | refund、credit、clawback、dispute |
| evidence | postback、transaction_id、lead_id、call disposition |

Payment term 直接影响现金流成本。`Net 45` 的高 payout 不一定优于 `Net 7` 的中等 payout，尤其是 Google Ads 账单先花钱、buyer 后付款的套利模式。

## 12. Google Ads 与出价边界

定价模型影响 Ads 的目标：

| Pricing model | 更合适的 Ads 信号 |
| --- | --- |
| Raw CPL | submitted secondary + accepted/validated QA |
| Qualified CPL | qualified primary 候选 |
| Pay-per-call | qualified call / call duration threshold |
| Appointment | booked/showed appointment |
| CPA / sale | approved sale / paid value |
| RevShare | expected net LTV，成熟后校准 |

边界：

- 不把 headline payout 当 conversion value。
- 不把 buyer accepted 当 paid value。
- 不把 short call、missed call、no answer 当 qualified call。
- 不把 returned、duplicate、complaint lead 继续作为正向信号。
- 不通过 Cookie 后台、伪造 offline conversion 或重复 postback 改善 tCPA/tROAS。

## 13. 系统落地

当前系统已实现 `/lead-pricing` V1 工作台和 `lead_pricing_reviews` 表，用于把 Lead Pricing、Payout Negotiation、scrub reserve、return window、payment term 和 buyer cap 变成可审计的投放前定价门禁。

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 pricing model、buyer、vertical、geo、source、exclusivity 和 source URL | `/lead-pricing`、`lead_pricing_reviews`、`/sources` |
| 区分 headline payout、approved unit payout、proposed payout 和 floor payout | `/lead-pricing` 表单字段和列表 |
| 用 accepted、qualified、approval、paid、return、scrub、chargeback 计算 effective payout | `calculate_lead_pricing_review()` |
| 用 click-to-lead、operating cost、cashflow cost 和 70% safety factor 计算 paid EPC 与 safe CPC | `lead_pricing_reviews.effective_payout`、`paid_epc`、`safe_cpc`、`margin_per_click` |
| 保存 rate card、谈价证据、reject reason summary、invoice / payment terms | `/lead-pricing` 文本证据字段 |
| 记录 quality evidence、source transparency、consent evidence、invoice evidence、dispute reserve、buyer terms、人审 | `/lead-pricing` 证据状态和 checkbox |
| 生成 Lead Pricing Score、risk_level、recommended_action、blockers | `adsworkbench/services/lead_pricing.py` |
| 内部状态流和审计 | `/lead-pricing/<id>/status` 写入 `audit_logs` |
| 查看 ADXKit 对应完成形态 | `/knowledge/lead_pricing` |

`lead_pricing_reviews` 核心字段：

```text
offer_id, campaign_draft_id, name, buyer_name,
vertical, geo, source_type, exclusivity, payout_model,
headline_payout, unit_payout, proposed_payout, minimum_acceptable_payout, currency,
estimated_cpc, click_to_lead_rate_percent,
accepted_rate_percent, qualified_rate_percent, approval_rate_percent, paid_rate_percent,
return_rate_percent, scrub_buffer_percent, chargeback_rate_percent,
variable_cost_per_click, tracking_cost_per_click, content_cost_per_click, cashflow_cost_percent,
cap_limit, expected_volume, return_window_days, payment_term_days,
qualification_definition, rate_card_evidence, negotiation_evidence,
reject_reason_summary, invoice_terms,
quality_evidence_status, source_transparency, consent_evidence,
reject_reason_map_ready, invoice_evidence, dispute_reserve_present,
buyer_terms_status, human_review,
score, risk_level, recommended_action,
effective_payout, paid_epc, safe_cpc, margin_per_click, reserve_amount,
blockers, status, notes, source_urls
```

V1 评分器的关键原则：

- `headline_payout` 只做展示和谈价上下文，不能单独进入 safe CPC。
- 如果没有 approved `unit_payout`，只能用 `proposed_payout` 做候选测算，并且 buyer terms 未 approved 时会触发 blocker。
- `effective_payout = payout * accepted * qualified * approval * paid * retained_rate`。
- `retained_rate = 1 - return_rate - scrub_buffer - chargeback_rate`，下限为 0。
- `safe_cpc = paid_epc * 0.70 - variable_cost - tracking_cost - content_cost - cashflow_cost`。
- Buyer cap、return window、payment term、source transparency、consent evidence、invoice evidence、reject reason map 和 dispute reserve 都会影响 blockers。

后续如果要拆分更细表，可从 `lead_pricing_reviews` 拆出 `lead_pricing_rate_cards`、`lead_payout_versions`、`lead_pricing_tiers`、`lead_pricing_floor_rules`、`lead_scrub_reserve_profiles`、`lead_buyer_price_negotiations`、`lead_pricing_experiments`、`lead_payment_term_profiles` 和 `lead_buyer_value_score_daily`。拆分时必须保留 evidence URL、reviewer、effective date、status audit 和单团队边界。

系统不自动谈价、不自动改 buyer routing、不自动上传 conversion value、不生成 lead 或电话，只生成证据、评分、建议和人工状态。

## 14. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| ROI 看板 | 展示 headline payout、effective payout、approved/paid EPC |
| 自动优化 | 根据 scrub buffer、paid rate、cap 和 payment term 生成预算建议 |
| 换链接 | 只切到价格、cap、垂类、披露都已审核的 buyer/offer |
| 自动投放 | 使用 effective payout 和 safe CPC 的人工审批草稿 |
| 创意生成 | 不生成不被 buyer pricing/qualification 支撑的价格或承诺 |
| 任务中心 | 生成谈价、invoice QA、return window close、rate card review |

完成标准：

- 能解释 raw CPL、qualified CPL、pay-per-call、appointment、CPA、revshare 的风险差异。
- 能用 accepted/qualified/approved/paid 计算 effective payout 和 safe CPC。
- 能解释 scrub buffer、return window、payment term 为什么要进入预算。
- 能用质量证据谈 payout，而不是用隐藏来源或伪造质量。
- 明确不交付 Cookie 后台操作、伪造 lead、补转化、cloaking 或规避封禁。

## 15. QA 清单

测试新 buyer 或谈新价格前检查：

- 是否明确 payout model 和 billable definition。
- unit price 是否按 geo、buyer、source、quality tier 拆开。
- 是否有 return window、allowed return reason 和 scrub report 字段。
- 是否知道 payment term、threshold、hold 和 invoice package。
- 是否有 accepted、qualified、approved、paid 的历史 cohort 数据。
- 是否计算 effective payout，而不是 headline payout。
- 是否为 pending/approved 未 paid revenue 设置 scrub reserve。
- 是否保存 rate card、邮件确认、后台截图或 API snapshot。
- 是否能按 source/subid 返回 reject reason。
- 是否有 cap、buyer hours 和 capacity。
- 是否把 short call、missed call、duplicate、returned 排除出正向 value。
- 是否没有为了谈价隐藏来源、伪造 quality、补 postback 或换账号。

## 16. 信息来源 URL

- FTC, Follow the Lead workshop: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- FTC, Staff Perspective: Follow the Lead: https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf
- FTC, .com Disclosures: https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising
- FTC, Protecting Personal Information: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- Google Ads, About conversion values: https://support.google.com/google-ads/answer/3419241
- Google Ads, Determine a bid strategy based on your goals: https://support.google.com/google-ads/answer/2472725
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads Help, About enhanced conversions for leads: https://support.google.com/google-ads/answer/11021502
- Google Local Services Ads, Lead costs and credits: https://support.google.com/localservices/answer/7436333
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Financial products and services: https://support.google.com/adspolicy/answer/2464998
- Google Ads Policy, Healthcare and medicines: https://support.google.com/adspolicy/answer/176031
- TUNE, Offer Payouts and Caps: https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps
- TUNE Dev Hub, OfferConversionCap: https://developers.tune.com/network-models/offerconversioncap/
- Everflow API, Get Offer: https://developers.everflow.io/docs/affiliate/offers/
- Voluum, Tracking Payouts: https://doc.voluum.com/en/tracking_payout.html
- Voluum, Conversion Status: https://doc.voluum.com/article/conversion-status
- Voluum, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
