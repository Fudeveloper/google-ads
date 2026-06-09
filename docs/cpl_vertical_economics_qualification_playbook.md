# CPL 垂类经济、资格问题与 Buyer Acceptance 手册

更新时间：2026-06-09

本文说明 CPL / CPA lead arbitrage 中，不同垂类为什么不能用同一套 payout、CVR、表单和优化阈值管理。保险、贷款/债务、法律、本地服务、教育、医疗和 B2B lead 的 buyer acceptance、资格问题、合规披露、回传延迟、拒付原因和放量节奏完全不同。目标是把“选 Offer”推进到“理解垂类经济和 buyer 资格规则”。

本文不是法律意见，也不提供绕过垂类认证、伪造资质、隐藏广告主主体、伪造 lead、自动提交表单、规避 DNC/TCPA、cloaking、Cookie 后台接管或封禁后换号的方案。系统落地只做知识、字段、评分、QA、来源 URL、审计和人工审批。

## 1. 为什么 CPL 垂类不能只看 Payout

高 payout 垂类通常看起来很诱人：

```text
Lead payout: $40 - $300+
Google Ads CPC: $2 - $40+
Landing CVR: 3% - 25%
```

但真实利润取决于：

- 用户是否有明确需求和购买/咨询意图。
- lead 是否满足 buyer 的资格条件。
- buyer 是否能联系上用户。
- 该 source 是否符合 buyer / network 条款。
- 是否有 consent、disclosure、隐私政策和数据分享证据。
- 是否有执照、认证、地区、年龄、专业资质或官方关系限制。
- accepted lead 后续能否变成 qualified、billable、approved、paid。
- 用户投诉、退款、chargeback、DNC、scrub 是否会吞掉收入。

因此，垂类评估不能只问：

```text
Payout 多高？
CVR 多高？
CPC 多低？
```

要问：

```text
哪些资格问题决定 buyer 是否接收？
哪些 claim 会被拒登或投诉？
哪些用户状态不能被用于个性化定向？
多久才能知道 paid quality？
哪个 reject reason 会摧毁这个垂类？
```

## 2. 垂类经济的核心变量

| 变量 | 说明 | 对套利的影响 |
| --- | --- | --- |
| Intent strength | 用户是否正在主动解决问题 | 决定 CVR 和联系率 |
| Qualification depth | buyer 需要多少资格字段 | 字段多会降 CVR，但提升 acceptance |
| Payout variance | 不同 buyer、state、产品价格差异 | 决定 routing 和预算分层 |
| Contact urgency | 多久联系才有价值 | 影响 call center、时段、cap |
| Regulation level | 是否涉及许可、认证、敏感状态 | 决定页面、创意和账号风险 |
| Data sensitivity | 是否包含金融、健康、法律、身份数据 | 决定 PII、retention、sharing |
| Feedback lag | buyer 多久给 reject/paid 状态 | 决定决策窗口和放量速度 |
| Complaint cost | 投诉或 DNC 的代价 | 决定是否允许 shared lead |

垂类经济常见误判：

- 把 `submitted CPL` 当成 `paid CPL`。
- 把保险、法律、债务、本地服务都用同样表单问题。
- 在高监管垂类用“免费、保证、最高、官方、快速批准”这类强 claim。
- 忽略 buyer operating hours 和 contact speed。
- 用低意图 broad match 扩量，导致 accepted rate 和 paid rate 崩。
- 不等一个 buyer feedback / settlement window 就扩量。

## 3. 资格问题地图

资格问题不是越多越好，也不是越少越好。它的作用是降低 buyer reject，而不是为了收集更多隐私数据。

| 问题类型 | 示例 | 用途 | 风险 |
| --- | --- | --- | --- |
| Service need | 需要哪类服务/产品 | 匹配 buyer campaign | 选项误导会制造 low intent |
| Geo / service area | state、zip、city | 判断服务区、牌照、价格 | bad geo 和隐私风险 |
| Timeline | 立即、1 周内、30 天内 | 判断紧急程度和联系优先级 | 夸大 urgency 会投诉 |
| Eligibility | homeowner、insured、debt amount、case type | 判断 buyer 是否接收 | 敏感字段要最小化 |
| Contact preference | 电话、短信、邮件、时间段 | 降低 missed contact | 不能替代 consent |
| Consent scope | 谁联系、什么渠道、是否共享 | 合规 handoff | 模糊 consent 是高风险 |

设计原则：

- 第一屏让用户确认意图，后续再问必要资格。
- 资格字段必须和 buyer 规则对应，不为“以后可能有用”而收集。
- 敏感字段尽量用区间或选择题，不收详细说明。
- 每个问题都要能解释：如果没有它，会导致哪个 reject reason？
- 资格问题改变后，要生成 `form_version_id`，不能把新旧表单混在一起评估。

## 4. Insurance / Medicare / Health Plan Leads

常见子垂类：

- Auto insurance。
- Health insurance / ACA plan。
- Medicare / supplemental plan。
- Life insurance。
- Home / renters insurance。

经济特点：

- 用户搜索意图强，但核心词 CPC 高。
- Payout、buyer acceptance 和合格条件常按 state、age、coverage type、current status 差异很大。
- 电话联系速度很关键，错过窗口后转化率会快速下降。
- 健康/年龄/保险状态可能触发敏感数据和个性化广告边界。

常见资格字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| state / zip | 牌照、服务区、价格 | 不要误导不可服务地区 |
| coverage type | auto、health、Medicare、life | 匹配 buyer |
| current insured | 是否已有保险 | 不要承诺更低价格 |
| age bucket | Medicare / life 资格 | 敏感，需披露用途 |
| household / vehicle / property basics | 报价资格 | 避免过度收集 |
| contact permission | 电话/短信/邮件 | 与 TCPA/DNC 分开记录 |

常见 reject：

- bad state / bad zip。
- duplicate。
- invalid phone。
- outside enrollment / ineligible。
- low intent / user wanted information only。
- no consent / complaint。

页面和创意边界：

- 不承诺 guaranteed savings、guaranteed approval、lowest price。
- 不暗示官方 Medicare / Marketplace / insurer 关系，除非有明确授权。
- 披露这是 lead / comparison / referral service，说明谁可能联系。
- 不用健康状态、年龄困境、财务困境做不当个性化定向。

投放建议：

- 按 state、plan type、age/eligibility、device、call hours 分 campaign 或至少分 label。
- 先用长尾高意图 query，例如 quote、compare、agent、plan type。
- Open enrollment、special enrollment、Medicare enrollment 等窗口要单独建季节性计划。
- 不等 paid feedback 就扩量，是保险 lead 的典型亏损点。

## 5. Loan / Mortgage / Credit / Debt Leads

常见子垂类：

- Personal loan。
- Mortgage / refinance。
- Credit card。
- Debt relief / debt settlement。
- Credit repair / credit monitoring。

经济特点：

- Payout 高，CPC 高，政策和投诉风险也高。
- 资格字段直接影响 buyer 接收：credit range、debt amount、income、state、loan amount、homeowner。
- 信贷、住房、债务相关场景可能涉及 Personalized Ads、FCRA、CFPB、FTC 和州法边界。
- 回传延迟可能较长，first lead acceptance 不代表贷款/申请/成交。

常见资格字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| state | 牌照和服务区 | bad state 拒付常见 |
| loan/debt amount range | buyer eligibility | 用区间，避免过度收集 |
| credit range | 初筛 | 不要做误导性批准承诺 |
| employment/income range | 资格判断 | 敏感，需用途披露 |
| homeowner / property value | mortgage/refi | 可能触发 HEC 边界 |
| bankruptcy / hardship | debt 场景 | 高敏感，慎收 |

常见 reject：

- bad state / license mismatch。
- debt amount below threshold。
- credit range not accepted。
- duplicate。
- no consent。
- incentivized / low intent。
- misrepresentation complaint。

页面和创意边界：

- 不写 guaranteed approval、instant approval、erase debt、no risk、government program，除非可证明且合规。
- 明确费用、限制、资格、风险、第三方关系和数据用途。
- 对住房/就业/信贷相关广告，先审 Personalized Ads / HEC 定向限制。
- 如果 lead 数据用于 eligibility 或 consumer report 相关决策，要做 FCRA/律师评估。

投放建议：

- 用 pre-qualification language，而不是 approval language。
- 把 debt amount / credit range / state 作为质量分层，不要只看表单 CVR。
- Buyer feedback 至少拆到 `accepted`、`application_started`、`funded/approved`、`paid`。
- 对 debt/credit 类，投诉率和 refund/chargeback 风险权重应高于短期 EPC。

## 6. Legal Leads

常见子垂类：

- Personal injury。
- Immigration。
- Criminal defense。
- Divorce / family law。
- Bankruptcy / tax relief。
- Employment law。

经济特点：

- 单 lead 或单 case 价值可能很高，但 qualification 严格。
- 地区、案件类型、事故日期、伤害程度、对方责任、是否已有律师等影响 buyer 是否接。
- 法律广告通常有州 bar / professional conduct / false or misleading communication 风险。
- 用户处于高压力场景，误导、夸大结果和过度联系更容易投诉。

常见资格字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| state / county | 执业地区 | 不可服务地区不能转发 |
| case type | PI、immigration、criminal 等 | 匹配律师或 firm |
| incident date | statute / urgency | 不要诱导虚假填写 |
| representation status | 是否已有律师 | 避免冲突和拒付 |
| injury / damages range | PI 资格 | 敏感，谨慎收集 |
| contact urgency | 回访优先级 | 不等于 consent |

常见 reject：

- wrong practice area。
- out of state / wrong county。
- case too old。
- already represented。
- no injury / low damages。
- invalid contact。
- duplicate。

页面和创意边界：

- 不承诺 guaranteed settlement、win your case、maximum compensation。
- 不伪装成政府、法院、官方援助或律师协会。
- 明确 lead service / referral / advertising relationship。
- 展示结果、评价或案例时要避免暗示每个用户会得到类似结果。

投放建议：

- 以 practice area + geo + urgency 拆广告组。
- 页面用资格问题筛掉 wrong case type，而不是增加 broad traffic。
- 法律 lead 更适合 lower volume / higher quality，不适合用低意图大词快速放量。
- Buyer feedback 要包括 retained、consult scheduled、qualified case，而不只是 accepted。

## 7. Home Services / Solar / Local Services Leads

常见子垂类：

- HVAC、plumbing、roofing、pest control、garage door。
- Solar、windows、bath remodel、flooring。
- Emergency local services。

经济特点：

- 本地意图强，call lead 价值高。
- 地区、营业时间、服务范围、license、job type、homeowner 状态决定 acceptance。
- Emergency query 转化快，但 call center / contractor 容量限制明显。
- Solar / remodel 等高客单价 lead 的资格和回传周期更长。

常见资格字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| zip / city | 服务区 | bad geo 和 fake local 风险 |
| service type | HVAC repair、roof replacement | 匹配 contractor |
| urgency | emergency、this week、planning | 决定 call priority |
| homeowner | solar/remodel 常用 | 不要过度推断身份 |
| property type | house/condo/business | 匹配服务 |
| project budget range | 高客单项目 | 避免误导报价 |

常见 reject：

- outside service area。
- wrong service type。
- renter not homeowner。
- duplicate。
- missed call / no answer。
- price shopping / low intent。
- contractor cap reached。

页面和创意边界：

- 不假装本地商家、官方维修或品牌授权。
- 不使用假地址、假评论、假营业地点。
- 明确这是匹配/转介/报价服务还是服务商本身。
- Emergency 场景不要夸大响应时间或保证立即到达。

投放建议：

- 强按 geo、hours、service type、device/call 分层。
- Call lead 要看 connected rate、qualified call duration、missed call、booked job。
- Contractor cap 和营业时间要和 budget pacing 绑定。
- 本地服务不宜用大范围泛词放量，否则 bad geo 和 wrong service 会吃掉利润。

## 8. Education / Career Training Leads

常见子垂类：

- College programs。
- Bootcamps / certification。
- Nursing / healthcare training。
- CDL / trade school。
- Continuing education。

经济特点：

- 用户研究周期较长，first form submit 到 enrollment / start date 有明显延迟。
- Payout 往往按 qualified lead、application、enrollment 或 start 口径变化。
- 就业、收入、录取、认证、学费、贷款和学生债务相关 claim 风险高。

常见资格字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| program interest | 专业/课程 | 匹配 school buyer |
| education level | 入学资格 | 不要歧视或误导 |
| location / online preference | 校区/在线 | 明确可选项 |
| start timeline | 意图强度 | 不要制造虚假 urgency |
| financial aid interest | 后续流程 | 避免承诺资助或贷款结果 |
| contact channel | 招生联系 | 仍需 consent |

常见 reject：

- wrong program。
- bad geo / campus not available。
- low intent。
- duplicate。
- unreachable。
- not qualified。
- complaint about misleading job/income claim。

页面和创意边界：

- 不夸大就业率、工资、证书价值、录取概率。
- 明确学校/项目关系、费用、时长、认证和适用条件。
- 对学生贷款减免、债务 relief 要极其谨慎，避免冒充政府或官方渠道。

投放建议：

- 把 `program + location + start timeline` 当成质量维度。
- 不只看 form submit，要等 contacted、qualified、application、enrolled。
- Career outcome claim 必须有来源和适用条件。
- 对 broad education query 做内容页筛选，避免低意图 lead 直接进 buyer。

## 9. Healthcare / Appointment Leads

常见子垂类：

- Dental、vision、mental health、urgent care、specialist appointment。
- Medical devices、clinics、telehealth。
- Non-prescription wellness service。

经济特点：

- 用户需求明确，但健康数据敏感。
- Google Ads healthcare policies、personalized advertising 和地区认证可能适用。
- Appointment lead 的价值取决于 booked、showed、treated、paid，不只是 submitted。

常见资格字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| location | clinic/service area | 避免 bad geo |
| service need | dental implant、therapy、urgent visit | 避免诊断承诺 |
| insurance / payment type | buyer eligibility | 敏感，需最小化 |
| appointment timeline | 排期 | 不保证可约 |
| symptoms category | 初筛 | 不收详细病史 |

常见 reject：

- out of service area。
- wrong service。
- insurance not accepted。
- no-show / unreachable。
- health claim complaint。
- duplicate。

页面和创意边界：

- 不承诺 cure、guaranteed result、diagnosis、before/after miracle。
- 不基于用户敏感健康状态做个性化定向。
- 不收集不必要病史或诊断详情。
- 明确服务范围、资质、隐私和专业建议边界。

投放建议：

- 以 condition content 做教育时，避免把读者状态用于 targeting。
- 转化口径至少到 booked/qualified appointment。
- 对诊所类 lead，call hours、calendar availability、insurance accepted 会直接影响 paid rate。

## 10. B2B SaaS / Professional Services Leads

常见子垂类：

- CRM、security、backup、HR、accounting、marketing software。
- Agencies、consulting、managed services。

经济特点：

- 合规风险相对低，但 sales cycle 长。
- Buyer 更看重 company size、role、industry、budget、timeline。
- Search CPC 可能高，尤其是竞品词和 high-intent software comparison。

常见资格字段：

| 字段 | 用途 | 注意 |
| --- | --- | --- |
| company size | ICP 匹配 | 不要过度收集个人数据 |
| role / department | buyer persona | 可选，避免歧视 |
| use case | pain point | 匹配 buyer |
| current tool | migration / competitor | 商标和竞品表达谨慎 |
| timeline / budget | sales qualification | 不要承诺价格 |

常见 reject：

- student / consumer。
- company too small。
- wrong industry。
- no budget。
- duplicate。
- competitor support query。

页面和创意边界：

- 竞品比较要真实、可核查，不暗示官方关系。
- 不用 fake review、fake rating、fake customer logo。
- Pricing、trial、feature claim 要和目标页面一致。

投放建议：

- B2B lead 要看 MQL、SQL、opportunity、won revenue，而不是 form submit。
- Long-tail problem query 可比 generic software query 更稳定。
- 对竞品词要单独做商标和页面披露审计。

## 11. Vertical Fit Score

建议新增垂类适配评分：

```text
Vertical Fit Score =
  0.20 * paid_unit_economics
  + 0.15 * buyer_acceptance_predictability
  + 0.15 * qualification_clarity
  + 0.15 * policy_compliance_margin
  + 0.10 * source_intent_fit
  + 0.10 * feedback_lag_tolerance
  + 0.10 * complaint_risk_control
  + 0.05 * team_experience
```

评分解释：

| 维度 | 看什么 |
| --- | --- |
| paid_unit_economics | paid EPC、safe CPC、回款周期 |
| buyer_acceptance_predictability | buyer 规则是否清楚，reject reason 是否透明 |
| qualification_clarity | 资格字段能否清楚映射到 buyer 规则 |
| policy_compliance_margin | 是否需要认证、许可、强披露或高风险 claim |
| source_intent_fit | query/source 是否匹配垂类真实意图 |
| feedback_lag_tolerance | 现金流能否等到 qualified/paid feedback |
| complaint_risk_control | DNC、opt-out、shared lead、敏感数据是否可控 |
| team_experience | 团队是否懂该垂类语言、季节性和 buyer 规则 |

动作阈值：

| 分数 | 动作 |
| --- | --- |
| 85-100 | 可小预算进入 structured test |
| 70-84 | 先补 buyer rules、页面披露或 feedback mapping |
| 55-69 | 只做研究，不进入 paid test |
| < 55 | 拒绝 |

## 12. 垂类测试模板

```text
Vertical:
Sub-vertical:
Country / state:
Buyer type:
Payout model:
Accepted definition:
Paid definition:
Primary reject reasons:
Required qualification fields:
Consent / disclosure version:
Sensitive data fields:
Allowed sources:
Forbidden claims:
Policy certifications:
Expected feedback lag:
Minimum sample:
Hard stop:
Scale rule:
```

成功标准不要只写 ROI：

- `accepted_rate >= target`。
- `qualified_rate >= target`。
- `paid_rate >= target`。
- `complaint_rate <= threshold`。
- `duplicate_rate <= threshold`。
- `bad_geo_rate <= threshold`。
- `buyer_feedback_delay <= threshold`。
- `safe_cpc >= observed_cpc * margin`。

## 13. 系统落地

当前系统已实现 `/cpl-verticals` V1 工作台和 `cpl_vertical_reviews` 表，用于把 CPL 垂类经济、资格字段、Buyer Acceptance、回传延迟、政策边界和放量阈值落成可审计记录。

| 需求 | 当前位置 |
| --- | --- |
| Offer 垂类、国家、payout、限制和政策备注 | `/offers` |
| 单位经济、break-even、safe CPC | `/calculators` |
| CPL 垂类 profile、资格字段、reject reason、accepted/paid 口径 | `/cpl-verticals` |
| Vertical Fit Score、effective payout、EV/click、safe CPC 和 blockers | `adsworkbench/services/cpl_vertical.py` |
| buyer terms、consent/disclosure、PII 最小化、许可/认证证据和人审状态 | `cpl_vertical_reviews` |
| Lead 质量、Ping/Post、验证和 suppression 知识 | `/knowledge/lead_quality`、`/knowledge/ping_post_leads`、`/knowledge/lead_validation` |
| buyer feedback 和 paid revenue 导入 | `/metrics/import` |
| 风险审计和来源 URL | `/risk-audits`、`/sources` |
| field_mapping、buyer_terms_review、policy_review、test_ready、scale_ready、blocked 等状态 | `/cpl-verticals/<id>/status`，状态写入 `/logs` |

`CplVerticalReview` 主要字段：

```text
name, offer_id, campaign_draft_id, vertical, subvertical, country,
buyer_type, payout_model, payout_amount, estimated_cpc,
landing_cvr_percent, accepted_rate_percent, qualified_rate_percent,
paid_rate_percent, deduction_rate_percent, chargeback_rate_percent,
feedback_lag_days, contact_sla_minutes, qualification_fields,
sensitive_fields, reject_reason_map, accepted_definition,
paid_definition, policy_requirements, forbidden_claims,
required_fields_mapped, reject_reason_map_ready,
accepted_definition_clear, paid_definition_clear,
consent_disclosure_status, pii_minimization, license_required,
license_evidence_present, buyer_terms_status, source_quality,
policy_risk, data_sensitivity, human_review, score, risk_level,
recommended_action, effective_payout, expected_value_per_click,
safe_cpc, cpc_margin_percent, blockers, status, notes, source_urls
```

评分逻辑：

- `effective_payout = payout * accepted_rate * qualified_rate * paid_rate * retained_rate`。
- `expected_value_per_click = effective_payout * landing_cvr`。
- `safe_cpc = expected_value_per_click * 0.65`。
- accepted / qualified / paid 过低、deduction / chargeback 过高、feedback lag 过长、contact SLA 过慢都会生成 blockers。
- 缺 qualification field map、reject reason map、accepted / paid definition、buyer terms、consent disclosure、PII 最小化或人审会阻止放量。
- 高政策风险、高数据敏感、需要许可但无证据时进入 high risk。

后续若需要拆分数据仓库，可扩展 `vertical_profiles`、`vertical_qualification_fields`、`vertical_reject_reason_maps`、`vertical_policy_requirements`、`vertical_buyer_acceptance_benchmarks`、`vertical_feedback_lag_profiles`、`vertical_fit_scores` 和 `vertical_test_plans`。这些表只保存垂类规则、资格字段定义、policy requirement、reject reason、benchmark、测试计划和评分，不保存不必要 PII，不自动生成 lead，不自动绕过垂类认证或审核。

## 14. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本项目完成形态 |
| --- | --- |
| Offer / 垂类管理 | 用 vertical profile 和 qualification map 管理不同 CPL 垂类 |
| 创意生成 | 按垂类 claim 边界和资格问题生成保守 brief |
| 自动投放优化 | 使用 paid/qualified/buyer reject 分垂类调整预算建议 |
| 换链接 | 只允许同垂类、同意图、同 consent/disclosure 的合规 fallback |
| Buyer routing | 按垂类资格、state、cap、feedback lag 和 paid rate 选择 buyer |
| 高风险后台操作 | 不做 Cookie 登录、cloaking、伪造资质、封禁换号或虚假 lead |

## 15. QA 清单

- 这个垂类是否需要 Google Ads 认证、许可证或地区限制。
- 页面是否说明真实主体、第三方关系、费用、资格、数据用途和 buyer handoff。
- 资格字段是否能映射到 buyer acceptance，不收集无关敏感数据。
- 是否区分 submitted、accepted、qualified、approved、paid。
- 是否有垂类专属 reject reason map。
- 是否有 DNC/opt-out/suppression 和 privacy request 处理。
- 创意是否避免 guaranteed、official、lowest、instant、risk-free、maximum 等不可证强 claim。
- 是否按 state/geo、service type、device、hours、buyer cap 拆分预算。
- 是否等待一个垂类 feedback lag / settlement window 再扩量。
- 是否禁止绕过认证、隐藏 source、cloaking、伪造 lead 和 Cookie 后台操作。

## 16. 信息来源 URL

- Google Ads Policy, Financial products and services: https://support.google.com/adspolicy/answer/2464998
- Google Ads Policy, Healthcare and medicines: https://support.google.com/adspolicy/answer/176031
- Google Ads Policy, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads Policy, Housing, employment, and credit FAQ: https://support.google.com/adspolicy/answer/9997418
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Help, Local Services Ads platform policies: https://support.google.com/localservices/answer/6224841
- Google Ads Help, How lead costs and credits work in Local Services Ads: https://support.google.com/localservices/answer/7436333
- FTC, Follow the Lead: An FTC Workshop on Lead Generation: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- FTC, Staff Perspective: Follow the Lead: https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf
- FTC, .com Disclosures: How to Make Effective Disclosures in Digital Advertising: https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, CAN-SPAM Act: A Compliance Guide for Business: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- CFPB, Digital comparison-shopping circular: https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/
- CFPB, Regulation V / Fair Credit Reporting Act: https://www.consumerfinance.gov/rules-policy/regulations/1022/
- Federal Student Aid, Avoid student loan debt relief scams: https://studentaid.gov/resources/scams
- ABA, Model Rule 7.1 Communications Concerning a Lawyer's Services: https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communications_concerning_a_lawyers_services/
