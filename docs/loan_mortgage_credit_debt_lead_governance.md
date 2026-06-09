# Loan、Mortgage、Credit 与 Debt Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / CPA / Ping/Post / Call Lead 套利里，personal loan、mortgage / refinance、HELOC、credit card、credit repair、credit monitoring、debt relief、debt settlement、student loan debt relief 等金融 lead 为什么是高 payout、高合规风险、高拒付风险的垂类。它承接 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)、[Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)、[Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)、[Lead 验证、Suppression、去重与 PII 治理手册](lead_validation_suppression_pii_governance.md)、[转化信号质量与出价学习治理手册](conversion_signal_quality_bidding_learning_governance.md) 和 [敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)，重点回答：贷款/债务/信用 lead 的资格字段、buyer acceptance、financial disclosure、licensed lender / broker / lead generator 角色、FCRA/ECOA/TILA/TSR 边界、Google Ads HEC / Personalized Ads 限制、claim 审核和 offline value mapping 应该如何治理。

本文不是法律意见，也不提供伪造贷款申请、伪造收入/信用/身份、规避信审、隐藏 lender/buyer、冒充政府债务减免、信用修复保证、绕过 FCRA/ECOA/TILA/TCPA/DNC/TSR、自动外呼、短信群发、使用 Ads Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做行业知识、字段最小化、资格规则、来源 URL、consent/disclosure、buyer terms、reject reason、offline value、审计、任务和人工审批。

## 1. 为什么 Loan / Debt Lead 是高 payout 高风险垂类

金融 lead 的 payout 高，是因为一个合格 borrower、mortgage refinance、debt settlement client、credit card applicant 或 funded loan 可能带来很高 downstream value。但广告端看到的 submitted lead 和买方最终可收款之间隔着很长链路：

```text
search intent
  -> landing / comparison
  -> lead submit
  -> validation and consent proof
  -> eligibility / prequalification
  -> buyer accepted
  -> application started
  -> underwriting / verification
  -> approved / funded / enrolled
  -> paid revenue / chargeback / complaint
```

常见亏损路径：

- 用户提交表单，但州、loan amount、debt amount、credit range、income、homeowner、employment 或 debt type 不符合 buyer。
- 广告写 guaranteed approval、no credit check、erase debt、government debt relief、lowest rate，带来拒登、投诉或监管风险。
- Buyer 先 accepted，后续因 duplicate、low debt amount、bad credit/income fit、invalid consent、unreachable、non-serviceable state 或 fraud risk 退回。
- Mortgage / refinance lead 没有确认 lender/broker license、NMLS、州许可和广告披露。
- Debt relief / credit repair 使用“删除负面记录”“马上免债”“官方项目”等高风险 claim。
- Google Ads 按 submitted lead 学习，实际 paid revenue 延迟到 funded loan、enrolled debt program 或 invoice close 才出现。

金融 lead 的核心不是“收更多申请”，而是把 qualification、disclosure、buyer acceptance、offline status、投诉和回款状态分层治理。

## 2. 原理解释：金融 Lead 是 eligibility、disclosure 和 money flow 的交接

贷款/债务 lead 与普通咨询 lead 的差异在于，它可能影响消费者能否获得信贷、债务服务、住房相关金融产品或信用服务。用户会基于广告和页面作出财务决策，因此系统必须回答三件事：

| 问题 | 说明 | 失败后果 |
| --- | --- | --- |
| Eligibility | 用户是否符合该产品或 buyer 的基本接收条件 | 拒收、低 paid rate、投诉 |
| Disclosure | 页面是否清楚说明主体、费用、APR/rate 条件、限制、补偿关系和非保证结果 | misrepresentation、regulatory risk |
| Money flow | 收入按 lead、application、approval、funded、settled、paid 哪个事件计 | accepted 当 paid、现金流错判 |

正确测算应使用可收款净值：

```text
effective_financial_lead_value =
  headline_payout
  * eligibility_pass_rate
  * buyer_accept_rate
  * application_or_enrollment_rate
  * approval_or_funding_rate
  * paid_rate
  - compliance_reserve
  - complaint_reserve
  - return_or_scrub_reserve
  - payment_lag_cost
```

金融 lead 的优化不能只看表单 CVR。短表单会提高 submit，但可能降低 eligibility fit；过度字段会增加敏感数据处理、用户不信任和政策风险。每个字段都必须有明确 purpose。

## 3. Subvertical 地图

| Subvertical | 用户意图 | 典型资格字段 | 主要风险 |
| --- | --- | --- | --- |
| Personal loan | 借款、合并账单、应急资金 | state、loan amount range、credit range、income range、employment range | guaranteed approval、APR/fee 披露、credit hardship targeting |
| Mortgage / Refinance | 房贷、再融资、购房贷款 | state、property type、homeowner、loan amount、property value range、mortgage balance | HEC 定向限制、NMLS/license、rate/APR claim |
| HELOC / Home equity | 房屋净值贷款或信用额度 | homeowner、property state/value、mortgage balance、credit range | 住房信贷政策、误导 equity claim |
| Credit card | 比较信用卡、预审 | credit range、income range、reward interest | approval/bonus/fee/APR misrepresentation |
| Debt relief / debt settlement | 降低债务、债务咨询 | unsecured debt amount range、state、debt type、hardship range | advance fee、erase debt、government program 冒充 |
| Credit repair | 修复信用记录 | credit issue category、state | 保证删除负面记录、CROA/FTC 风险极高 |
| Credit monitoring / score | 查询信用分或监控 | consent、identity handoff boundary | 免费试用/订阅披露、FCRA 数据边界 |
| Student loan debt relief | 学生贷款还款或减免帮助 | federal/private loan type、state、servicer context | 冒充政府、收费代办免费事项 |
| Auto loan / title loan | 车辆贷款、再融资或质押 | state、vehicle range、loan amount、income | 高 APR、title loan 地区限制 |

不要把 personal loan、mortgage、debt relief、credit repair 和 student loan relief 放进同一个 landing、consent、buyer disclosure 和 conversion action。它们的政策、字段和 paid definition 完全不同。

## 4. 资格字段和数据最小化

金融 lead 字段要用 range 和 bucket，避免在广告套利系统里处理完整敏感信息。

| 字段 | 用途 | 最小化做法 | 风险提示 |
| --- | --- | --- | --- |
| state / zip | lender/buyer 服务地区、license、rate availability | 州优先，zip 只在必要时保存 hash/CRM | bad state 是高频 reject |
| loan amount range | buyer minimum / maximum | 区间 | 不承诺 approval 或固定 rate |
| debt amount range | debt relief eligibility | 区间，不保存具体账户 | 低 debt amount 常被拒收 |
| debt type | unsecured、credit card、medical、student、tax 等 | 枚举 | 某些 debt type 不可接 |
| credit range | 初筛 buyer fit | self-reported bucket | 不要做 credit decision 或承诺结果 |
| income range | affordability / buyer fit | 区间 | 不要收证明文件 |
| employment range | 稳定收入初筛 | 枚举 | 避免歧视和过度收集 |
| homeowner / property value range | mortgage/refi/HELOC | 粗分层 | HEC 和 housing credit 边界 |
| bankruptcy / hardship | debt 场景初筛 | 默认不收，必要时粗分层 | 高敏感，容易被误用 |
| consent / disclosure version | 可联系、可分享、可转售证据 | version/hash/certificate ref | 争议证据核心 |

不要在广告套利系统中收集完整 SSN、银行账号、工资单、税表、完整信用报告、完整出生日期、完整住址、完整账户号码或身份证件。需要这些信息时，应由授权 lender、broker、servicer 或合规申请系统在受控环境处理。

## 5. Eligibility、Reject Reason 和 Buyer Acceptance

金融 buyer acceptance 常见状态：

```text
submitted
  -> validation_passed
  -> eligibility_passed
  -> pinged / posted
  -> buyer_accepted
  -> contacted
  -> application_started
  -> prequalified / approved
  -> funded / enrolled / account_opened
  -> approved_revenue / paid
  -> returned / clawback / complaint
```

常见 reject reason：

| Reject reason | 含义 | 修复动作 |
| --- | --- | --- |
| bad state / license mismatch | buyer 不服务该州或无许可 | geo gating、buyer routing |
| amount below threshold | loan/debt amount 太低 | 字段前置、query/landing 调整 |
| credit range not accepted | 不符合 buyer credit band | 不要承诺 approval；分 buyer |
| income / employment mismatch | 收入或就业不符合 | eligibility copy、字段解释 |
| wrong debt type | secured/tax/student/medical debt 不接 | debt type 分流 |
| no homeowner / property mismatch | mortgage/HELOC 条件不符 | homeowner routing |
| duplicate | buyer 已收到或窗口内重复 | hash 去重、duplicate window |
| unreachable / invalid phone | 无法联系 | validation、form UX、SLA |
| no consent / invalid disclosure | 证据不足 | consent version、buyer disclosure |
| misleading claim complaint | 用户认为被误导 | claim review、source quarantine |
| fraud / synthetic risk | 信息异常或疑似欺诈 | source audit、不要补字段 |

`buyer_accepted` 只是中间状态，不能直接当 paid revenue。对贷款 lead，`funded` 或 buyer paid invoice 更接近真实价值；对 debt relief，`enrolled`、first payment 或 settled revenue 才能校准 payout。

## 6. Licensed Lender、Broker、Lead Generator 和 Marketplace 边界

金融 lead 页面要清楚区分角色：

| 角色 | 可以表达 | 不应表达 |
| --- | --- | --- |
| Lead generator | 收集咨询请求并转交给合作方 | 冒充 lender、servicer、government program 或 credit bureau |
| Comparison marketplace | 展示多个产品/合作方信息 | 把最高出价 buyer 伪装成最适合用户 |
| Broker / loan originator | 在授权范围内撮合或发起贷款 | 未授权州不得暗示可服务 |
| Lender / servicer | 提供或服务金融产品 | 未授权不得使用品牌、rate 或 approval claim |
| Debt relief provider | 提供债务服务 | 不得承诺消除债务、提前收费或冒充政府 |

Mortgage / loan originator 场景要保存：

```text
entity_name
role_type
license_or_nmls_ref
states_covered
product_scope
compensation_disclosure
partner_or_buyer_disclosure
rate_claim_source
reviewer
source_url
```

如果页面按推荐、排序、精选、最适合、最佳匹配展示 buyer 或产品，必须保存排序逻辑和补偿关系。不要把 buyer payout、bid 或 cap 当作“用户最佳选择”的唯一依据。

## 7. Financial Product Comparison 和 Steering 风险

很多金融套利页面本质是 comparison shopping 或 lead marketplace。风险在于：用户以为系统按其利益排序，但实际按广告主出价、buyer cap、payout 或 routing priority 排序。

治理原则：

- 明示平台身份：lead generator、comparison marketplace、broker 或 advertiser。
- 明示是否收到补偿，以及补偿是否影响排序、展示或推荐。
- 排序字段要可审计：APR/rate、fee、term、approval odds、buyer payout、cap、availability 不要混成黑箱。
- 不使用“best”“top”“guaranteed”“pre-approved”等无法证明或需严格定义的词。
- 对 mortgage、loan、credit card 等产品，rate/APR、fee、term、qualification 和 availability 必须有来源和日期。
- 如果只展示部分合作方，不能暗示覆盖全市场。

系统应保存：

```text
comparison_page_version
ranking_policy_version
compensation_disclosure_version
eligible_partner_set
ranking_inputs
excluded_partner_reason
source_url
reviewer
```

## 8. Debt Relief、Credit Repair 和 Student Loan Relief 特殊风险

这些子垂类通常比普通 personal loan 更危险。

| 场景 | 高风险 claim | 治理 |
| --- | --- | --- |
| Debt relief / settlement | erase debt、settle for pennies、government debt program | 说明风险、费用、结果不保证、资格条件 |
| Credit repair | remove negative items guaranteed、raise score fast | 避免结果保证，保存 CROA/FTC 审核 |
| Student loan relief | Biden forgiveness、official federal program、pay us to apply | 引用 Federal Student Aid，避免冒充政府或收费代办免费事项 |
| Tax debt relief | IRS approved、settle tax debt guaranteed | 需单独监管和资质审查 |

不要把用户的财务困境当成恐吓或羞辱性文案。不要使用“我们知道你欠债”“你的信用很差也能通过”这类个性化暗示。

## 9. Google Ads 政策、HEC 和 Personalized Ads

金融 lead 常踩 Google Ads 政策：

| 政策面 | 风险 | 治理 |
| --- | --- | --- |
| Financial products and services | 贷款、债务、金融服务的披露、地区、认证和禁投项 | 保存政策来源、产品类型、地区规则和页面披露 |
| Housing, employment, and credit | 美国/加拿大住房、就业、信贷类广告定向限制 | Mortgage、credit、loan 类 campaign 单独审 targeting |
| Personalized advertising | 财务困难、债务、信用状态等敏感状态不能被不当个性化使用 | 不用 hardship、low credit、debt behavior 做受众或文案暗示 |
| Misrepresentation | 费用、利率、资格、政府关系、广告主身份不清 | 主体、费用、限制、资格、补偿关系透明 |
| Unacceptable business practices | 欺骗性或不可信业务模式 | 拒绝冒充政府、虚假资质、隐藏条款 |
| Destination requirements | landing、Final URL、跳转和广告一致 | 不做 cloaking、隐藏 buyer、审核页/用户页不一致 |

不要把 credit、debt、mortgage 或 housing related lead 与宽泛 remarketing / customer list 混用。美国/加拿大 HEC 场景尤其要审 location、age、gender、parental status、marital status、ZIP、similar segments 等定向限制。

## 10. FCRA、ECOA、TILA、TSR 和 DNC 边界

金融 lead 需要额外合规判断：

| 规则 / 领域 | 与 lead arbitrage 的关系 |
| --- | --- |
| FCRA / Regulation V | 如果使用 consumer report 或将数据用于信贷、就业、住房、保险等资格决策，不能按普通营销 lead 处理 |
| ECOA / Regulation B | 信贷资格、预审、拒绝、歧视风险和 adverse action 需要专业评估 |
| TILA / Regulation Z | APR、rate、payment、term 等触发性信贷广告 claim 需要准确披露 |
| TSR / Telemarketing | 电话销售、debt relief、advance fee、DNC 和记录保存风险 |
| TCPA / DNC | 自动电话、短信、人工外呼和 opt-out/suppression |
| GLBA / Privacy | 金融数据共享、privacy notice、safeguards 和数据最小化 |

系统默认只做 lead generation 审计和状态记录，不做 credit decision、consumer report 拉取、adverse action 自动化或贷款申请审批。涉及这些动作时，应进入独立合规/律师评估。

## 11. Consent、Disclosure 和证据链

金融 lead 的 consent proof 至少保存：

```text
lead_id
form_version
consent_text_hash
financial_disclosure_version
buyer_disclosure_version
contact_channels_allowed
submit_timestamp
timezone
page_snapshot_hash
privacy_policy_version
suppression_check_status
source_url
```

Disclosure 要覆盖：

- 谁在收集信息。
- 是否是 lender、broker、lead generator、comparison marketplace 或 third-party advertiser。
- 谁可能联系用户，以及通过电话、短信、邮件还是其他渠道。
- 是否收到补偿，以及补偿是否影响展示、排序或转交。
- 产品结果不保证；rate、APR、fee、term、approval、debt reduction 取决于资格和 buyer。
- Privacy policy、数据分享、删除/opt-out 和联系方式。

不要用“提交即同意所有合作伙伴联系”替代具体 buyer disclosure。Shared lead、aged lead 和 recontact lead 必须有单独标记和 buyer terms。

## 12. Creative / Landing Claim Review

| Claim | 高风险写法 | 安全写法方向 |
| --- | --- | --- |
| Approval | “Guaranteed approval” | “Check eligibility factors” |
| Credit | “Bad credit? Approved instantly” | “Credit profile may affect available options” |
| Debt relief | “Erase debt today” | “Compare questions to ask before debt relief” |
| Government | “Official student loan forgiveness” | “Review official federal resources first” |
| Rate | “Lowest APR guaranteed” | “Rates vary by lender, credit, amount and term” |
| Mortgage | “Everyone qualifies for refinance” | “Eligibility and rates vary by property and borrower profile” |
| Credit repair | “Remove negative items fast” | “Understand your rights and dispute process” |
| Fee | “Free help” while monetized by buyer | Disclose compensation and possible product costs |

Landing page 必备检查：

- 页面主体、角色、联系方式、privacy policy、financial disclosure、buyer disclosure 清楚。
- Rate/APR/fee/term claim 有来源、日期和适用条件。
- 不使用政府标识、官方名词、相似域名或视觉设计制造官方关系。
- CTA 不暗示 approval、funding、debt reduction 或 credit score improvement 已经确定。
- 表单字段有 purpose，不收过度敏感数据。
- 用户看到的页面和审核/爬虫看到的页面一致。

## 13. Offline Value Mapping

金融 lead 建议分层回传：

| Stage | Ads 信号建议 | 说明 |
| --- | --- | --- |
| submitted lead | secondary / diagnostic | 只看漏斗，不扩量 |
| validation_passed | diagnostic | 格式和字段通过 |
| eligibility_passed | middle quality | 初步符合 buyer |
| buyer_accepted | middle quality | 仍可能 scrub |
| contacted / qualified call | stronger | 联系成功但非收入 |
| application_started | strong | 用户进入申请流程 |
| prequalified / conditionally approved | strong but sensitive | 需合规审核和 buyer 来源 |
| approved / funded / account_opened | primary candidate | 更接近可收款 |
| enrolled debt program / first payment | primary candidate | debt relief 更适用 |
| paid / invoice closed | final calibration | 用于 mature value |
| rejected / returned / complaint | internal negative | 不回传正向，进入 risk audit |

不要把 submitted、accepted、prequalified、duration 或 booked call 默认当 paid revenue。金融产品的 paid feedback 延迟可能很长，预算 ramp 要等 mature cohort 或使用 conservative staged value。

## 14. Financial Lead Quality Score

建议评分：

```text
financial_lead_quality_score =
  eligibility_fit             18
  disclosure_and_claim_fit    15
  consent_proof_quality       12
  buyer_accept_rate           12
  application_or_enroll_rate  15
  funded_or_paid_rate         15
  complaint_and_return_risk    8
  source_transparency          5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可按 mature paid value 小幅扩量 |
| 70-84 | 正常测试，继续收集 buyer feedback |
| 55-69 | 限量，查 reject reason、source、claim 和 buyer terms |
| 35-54 | 暂停扩量，修 eligibility、disclosure、routing 或页面 |
| 0-34 | 停 source / buyer / landing，开风险审计 |

评分必须按 subvertical、state、buyer、lead age、source、creative angle、form version、loan/debt amount bucket 和 credit range bucket 拆分。

## 15. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 Google/CFPB/FTC/NMLS/FSA 来源 | `/sources` |
| 记录金融 claim、官方关系、license、HEC targeting 风险 | `/risk-audits` |
| 用 policy_score、source_score 和 safe CPC 做小预算测算 | `/calculators` |
| 保存 Offer 垂类、国家、policy notes、tracking URL | `/offers` |
| 生成低风险创意和人工审核投放草稿 | Offer 详情页、`/campaigns` |
| 导入 accepted、application、funded、paid revenue | `/metrics/import` |
| 生成暂停、限量、查 claim、查 buyer feedback 建议 | `/optimization` |
| 保存任务和审批痕迹 | `/tasks`、`/logs` |

后续可扩展表：

```text
financial_vertical_profiles
financial_qualification_fields
financial_offer_eligibility_rules
financial_disclosure_versions
financial_buyer_terms
financial_buyer_acceptance_events
financial_reject_reason_maps
financial_claim_reviews
financial_license_authorization_refs
financial_comparison_ranking_reviews
financial_offline_value_maps
financial_quality_daily
```

关键字段：

```text
subvertical
state
loan_amount_bucket
debt_amount_bucket
credit_range_bucket
income_range_bucket
homeowner_flag
buyer_id
buyer_terms_version
license_or_authorization_ref
disclosure_version
consent_version
reject_reason
offline_stage
paid_value
source_url
reviewer
decision
```

## 16. ADXKit 对应点和完成形态

| ADXKit 能力 | 金融 lead 场景完成形态 | 不交付内容 |
| --- | --- | --- |
| Offer 管理 | subvertical、state、payout、buyer terms、license/disclosure 来源 | 伪造 lender、broker、政府或信贷资质 |
| 落地页采集 | 抽取 approval、rate、debt erase、government、fee、ranking claim | cloaking、隐藏真实 buyer |
| AI 创意生成 | 生成“比较、资格因素、问题清单”类低风险素材并进入 claim review | guaranteed approval、erase debt、no credit check 等强承诺 |
| 投放草稿 | 按 subvertical/state/HEC 风险拆 campaign/ad group | Cookie 后台自动投放或绕过认证 |
| 换链接 | 只做同主题、同披露、同资格条件、已审核 URL 轮换 | 用换链跳到未披露 lender/buyer |
| 任务中心 | disclosure 更新、claim review、buyer feedback 导入、source quarantine | 自动外呼、短信轰炸、伪造申请或刷量 |
| 来源库 | Google/CFPB/FTC/NMLS/FSA 官方来源可追踪 | 用二手传闻替代政策或监管来源 |

完成口径：把金融 lead 的行业知识、资格、披露、buyer acceptance、reject reason、offline value 和系统审计做完整；不做对抗平台、绕过登录、伪造申请、规避信审或制造虚假流量。

## 17. QA 清单

上线前逐项检查：

- `subvertical` 是否明确：personal loan、mortgage、HELOC、debt relief、credit repair、student loan relief 不能混用。
- 页面主体是否真实：lead generator、broker、lender、marketplace、servicer 或 advertiser 是否清楚。
- 是否有 license/NMLS/authorization 或明确“不直接放款”的 disclosure。
- Financial disclosure、buyer disclosure、privacy policy、联系方式和更新日期是否清楚。
- Rate/APR/fee/term/approval/debt reduction claim 是否有来源、日期、条件和限制。
- 是否避免 guaranteed approval、erase debt、government program、no credit check、lowest rate、fix credit fast 等强承诺。
- HEC / Personalized Ads 是否审过，尤其是美国/加拿大 mortgage、credit、loan 场景。
- 字段是否用 range/bucket，是否避免 SSN、银行账号、完整信用报告等敏感数据。
- Consent 是否包含 contact channel、buyer disclosure、version/hash 和页面证据。
- Buyer terms 是否写明 accepted、qualified、billable、return window、duplicate window、paid definition。
- Ping/Post 是否只发送最小必要字段，并保存 shared/exclusive/aged 标记。
- Offline value 是否按 accepted、application、approved、funded/enrolled、paid 分层。
- Google Ads primary conversion 是否使用成熟、可收款、低投诉的事件。
- 不使用 Ads Cookie 后台操作、自动登录、cloaking、代理/指纹规避、补点击或封禁规避。

## 18. 信息来源 URL

| 来源 | URL | 用途 |
| --- | --- | --- |
| Google Ads Policy, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑贷款、债务、信用、金融服务广告的披露、地区规则、认证和禁投项 |
| Google Ads Policy, Housing, employment, and credit FAQ | https://support.google.com/adspolicy/answer/9997418 | 支撑美国/加拿大住房、就业、信贷广告定向限制 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑财务困难、债务、信用状态等敏感个性化定向边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑费用、资格、主体、政府关系和结果承诺透明度 |
| Google Ads Policy, Unacceptable business practices | https://support.google.com/adspolicy/answer/6020954 | 支撑欺骗性金融服务、虚假资质和不可信业务模式审查 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| CFPB, Digital comparison-shopping circular | https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/ | 支撑金融产品比较、推荐排序、补偿驱动导流和消费者误导风险 |
| CFPB, Regulation V / Fair Credit Reporting Act | https://www.consumerfinance.gov/rules-policy/regulations/1022/ | 支撑 consumer report、信贷/保险/就业/住房资格判断边界 |
| CFPB, Regulation B / Equal Credit Opportunity Act | https://www.consumerfinance.gov/rules-policy/regulations/1002/ | 支撑信贷资格、歧视风险和 adverse action 相关边界 |
| CFPB, Regulation Z / Truth in Lending Act | https://www.consumerfinance.gov/rules-policy/regulations/1026/ | 支撑 APR、rate、payment、term 等信贷广告披露 |
| CFPB, Mortgage resources | https://www.consumerfinance.gov/consumer-tools/mortgages/ | 支撑 mortgage / refinance 用户教育和页面 claim 审核 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、debt relief、DNC、advance fee 和记录治理 |
| FTC, Credit Repair: How to Help Yourself | https://consumer.ftc.gov/articles/credit-repair-how-help-yourself | 支撑 credit repair claim、用户权利和保证修复风险 |
| FTC, Mortgage and foreclosure rescue scams | https://consumer.ftc.gov/articles/mortgage-and-foreclosure-rescue-scams | 支撑 mortgage relief、foreclosure rescue 和政府/收费误导风险 |
| Federal Student Aid, Avoid student loan debt relief scams | https://studentaid.gov/resources/scams | 支撑 student loan relief、官方项目和收费代办风险 |
| NMLS Consumer Access | https://www.nmlsconsumeraccess.org/ | 支撑 mortgage loan originator、lender、broker license 查询 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上金融广告披露、真实陈述和 claim proof |
