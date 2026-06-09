# Education、Career Training 与 Student Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / CPA / Ping/Post / Appointment Lead 套利里，Education Lead、Career Training Lead、College Lead、Trade School Lead、Bootcamp Lead、Student Inquiry 为什么是高 payout、长回传、高 claim 风险的垂类。它承接 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)、[Lead Form 漏斗、资格问题与移动端 UX 治理手册](lead_form_funnel_qualification_ux.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)、[Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)、[Lead Freshness、Aged Lead 与 Recontact Window 治理手册](lead_freshness_aged_recontact_governance.md)、[CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md) 和 [敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)，重点回答：教育 lead 的 program interest、school buyer、campus / online modality、state authorization、accreditation、admissions eligibility、financial aid、job placement / salary claim、student loan、military/veteran targeting、buyer acceptance、enrollment funnel、offline value mapping 和 Google Ads 信号应该如何治理。

本文不是法律意见，也不提供伪造学生资料、伪造学历/成绩/FAFSA/身份、冒充学校/政府/奖学金机构、虚假 accreditation、保证录取、保证就业、保证薪资、伪造 enrollment、自动外呼、短信群发、使用 Ads Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做行业知识、字段最小化、招生 claim 审核、来源 URL、consent/disclosure、buyer terms、reject reason、offline value、审计、任务和人工审批。

## 1. 为什么 Education Lead 是高 payout 长回传垂类

Education lead 的 payout 可能来自学校、program aggregator、招生平台、职业培训机构、bootcamp、证书项目或 continuing education buyer。一个合格 inquiry 可能带来申请、enrollment、tuition、financial aid 和长期 student value，但 submitted lead 到可收款之间链路很长：

```text
search intent
  -> program inquiry
  -> validation and consent proof
  -> admissions eligibility
  -> school / program match
  -> advisor contact
  -> application started
  -> accepted / admitted
  -> enrollment agreement
  -> class start
  -> census / paid tuition
  -> retention / withdrawal / refund outcome
```

常见亏损路径：

- 用户只想查资料或免费课程，却被送进高成本招生 funnel。
- Program interest、education level、state、campus distance、online availability 或 license eligibility 不匹配 buyer。
- 页面承诺 guaranteed admission、job placement、salary outcome、accreditation、financial aid 或 scholarship，但没有可验证来源。
- 学校或 training program 不在用户所在州授权招生，或 program completion 不满足执照/认证要求。
- Buyer 先 accepted，后续因 unreachable、underage/no guardian, no diploma/GED、bad state、low intent、duplicate、no consent 或 already enrolled 拒付。
- Google Ads 按 lead submit 或 advisor call 学习，但真实收入要等 application、enrollment、class start、census 或 paid tuition。

Education lead 的核心是“招生资格 + program fit + claim proof + enrollment feedback”，不是表单越多越好。

## 2. 原理解释：Education Lead 是意图、资格、项目承诺和招生回传的交接

教育 lead 的特殊性在于：用户的选择会影响时间、金钱、贷款、职业路径和 credential。套利团队如果只看 CVR，会把预算推向低门槛、低意图、易投诉的 lead。

| 交接 | 说明 | 失败后果 |
| --- | --- | --- |
| Intent handoff | 用户想要学位、证书、短课、转行、继续教育还是免费资料 | low intent、wrong program |
| Eligibility handoff | 用户学历、年龄、州、语言、licensure、campus/online 条件是否匹配 | buyer reject、招生投诉 |
| Claim handoff | 页面关于 accreditation、job placement、salary、financial aid 的承诺是否可证明 | misrepresentation、FTC/ED 风险 |
| Enrollment handoff | submitted 到 application、admitted、enrolled、started、paid 的真实状态 | 浅层信号扩量亏损 |

建议测算：

```text
effective_education_lead_value =
  headline_payout
  * program_fit_rate
  * eligibility_pass_rate
  * contact_rate
  * application_start_rate
  * enrollment_rate
  * class_start_or_paid_rate
  - compliance_reserve
  - withdrawal_or_refund_risk
  - complaint_risk
  - payment_lag_cost
```

教育 lead 的 paid feedback 可能很慢，尤其是 degree、bootcamp、CDL、nursing/allied health、cosmetology 和 continuing education。预算 ramp 要按 mature cohort，而不是按当天 submitted lead。

## 3. Program / School Type 地图

| Subvertical | 用户意图 | 典型资格字段 | 主要风险 |
| --- | --- | --- | --- |
| Degree / online college | 学位、转学、在线大学 | degree level、program interest、state、prior education | accreditation、transfer credit、financial aid |
| Career / trade school | 技能培训、职业证书 | program interest、campus distance、education level、start window | job placement、license eligibility、tuition |
| Bootcamp | coding/data/cyber bootcamp | background level、schedule、financing interest | salary/job guarantee、ISA/loan disclosure |
| CDL / truck driving | 商用驾驶培训 | state、license status、age bucket、driving record bucket | job placement、license requirement |
| Nursing / allied health | 医疗助理、CNA、LPN、surgical tech | state、education level、clinical requirement | licensure, accreditation, certification eligibility |
| Cosmetology / beauty | 美容、美发、美甲 | state、campus distance、license goal | state licensing hours and outcomes |
| Continuing education / certification | CE credits、professional certificate | profession, license state, credit need | accreditation/approval and transferability |
| Tutoring / test prep | SAT/ACT/GED/English | learner age bucket、subject、goal | minors, parental consent, guarantee claims |
| Military / veteran education | GI Bill, veteran training | veteran status if user voluntarily provides | VA/GI Bill claim and targeted marketing risk |
| Student loan / financial aid help | FAFSA, repayment, debt relief | federal/private loan type | government impersonation, fees for free processes |

不要把 degree、bootcamp、CDL、nursing、cosmetology、tutoring 和 student loan help 放进同一个 form、buyer terms 或 conversion action。它们的资格、监管、claim 和 paid definition 完全不同。

## 4. 资格字段和数据最小化

教育 lead 字段要帮助 program matching，不要收集超出招生初筛的敏感信息。

| 字段 | 用途 | 最小化做法 | 风险提示 |
| --- | --- | --- | --- |
| program interest | 匹配 school/program buyer | 枚举 | 避免把泛教育 query 直接送 buyer |
| degree / credential goal | degree、certificate、license、CE | 枚举 | 不承诺 credential outcome |
| state / zip / campus distance | state authorization、campus fit | state/zip/city，完整地址只在学校 CRM | bad state / too far |
| modality | online、campus、hybrid | 枚举 | Online program 也可能有 state limits |
| education level | HS diploma/GED、college credits | bucket | 不要收成绩单 |
| age bucket / guardian need | minor/adult eligibility | bucket | 未成年人需额外 consent |
| start window | now、3 months、6 months | 枚举 | 决定 buyer follow-up |
| schedule | full-time、part-time、evening | 枚举 | bootcamp/trade school fit |
| financial aid interest | 是否想了解资助 | yes/no/unknown | 不承诺 aid/loan/scholarship |
| military/veteran interest | 用户自愿提供 | yes/no/unknown | 不用敏感身份做诱导 |
| contact channels | phone、SMS、email | 明确 opt-in scope | TCPA/DNC/CAN-SPAM |
| consent / disclosure version | 招生联系和 buyer disclosure | version/hash/certificate ref | 争议证据核心 |

不要在套利系统里保存 SSN、FAFSA login、完整出生日期、成绩单、移民文件、完整 financial aid application、loan account、payment information、未成年人完整 PII 或不必要家庭信息。

## 5. Accreditation、State Authorization、Licensure 和 Transferability

教育 lead 的资质 claim 要比普通 Offer 更严：

```text
school entity
program name
credential type
accreditation status
state authorization
licensure / certification eligibility
transfer credit rules
financial aid eligibility
program outcome source
reviewer
source_url
```

治理原则：

- 只有能证明的 accreditation / approval / authorization 才能写。
- 不把 corporate registration、business license 或平台 listing 说成教育 accreditation。
- 对 nursing、cosmetology、CDL、teacher certification 等 licensure-bound programs，要说明完成课程不一定自动取得 license。
- Transfer credit claim 要说明接收学校决定，不承诺可转学分。
- Online program 也可能受 state authorization、clinical placement 或 licensure state 限制。
- Financial aid eligibility 不能写成“所有人都有补贴/贷款/奖学金”。

如果页面声称 accredited、approved、licensed、financial aid eligible、job placement rate 或 salary outcome，必须保存来源 URL、更新时间和适用 program。

## 6. Job Placement、Salary、Career Outcome 和 Guarantee 风险

教育 lead 最容易踩的是职业结果承诺：

| Claim | 高风险写法 | 安全写法方向 |
| --- | --- | --- |
| Job placement | “Guaranteed job after graduation” | “Ask about job placement rates and methodology” |
| Salary | “Earn $80k after bootcamp” | “Outcomes vary by program, location and individual background” |
| Certification | “Become certified in 8 weeks” | “Program completion may prepare you for eligible exams” |
| Financial aid | “Free school with aid” | “Financial aid may be available to those who qualify” |
| Accreditation | “Government approved degree” | “Verify accreditation with ED/recognized sources” |
| Transfer credits | “Credits transfer anywhere” | “Transfer decisions are made by receiving institutions” |
| Admissions | “Everyone accepted” | “Admission requirements vary by school/program” |
| Fast career change | “Start earning immediately” | “Timeline and outcomes vary” |

Job placement、graduation rate、salary、debt、licensure pass rate 和 employment outcome 应使用学校、ED、FTC 指引或可验证数据源。不要让 AI 创意生成页面没有的工资、就业率、ranking 或 accreditation。

## 7. Financial Aid、Student Loan、Scholarship 和 GI Bill 风险

Education lead 经常和 money flow 绑定：

| 场景 | 风险 |
| --- | --- |
| FAFSA / federal aid | 冒充政府、收费代办免费事项 |
| Student loan | 混入 debt relief / repayment scam |
| Scholarship matching | 虚假奖学金、lead bait |
| GI Bill / veteran education | 军人/退伍军人身份敏感和 benefit claim |
| Income share / bootcamp financing | 费用、退款、就业承诺和 loan-like disclosure |
| Tuition discount | 限时折扣、隐藏费用、不可退条款 |

治理要求：

- 页面明确 school / lead generator / marketplace 身份。
- Financial aid wording 使用“may be available to those who qualify”类条件表达。
- FAFSA 和 federal student aid 要引用 official Federal Student Aid 来源。
- 不收 FSA ID、loan servicer login、SSN 或完整 financial aid records。
- 对 student loan debt relief，按金融/债务专题高风险处理，不混入普通教育 lead。

## 8. Lead Delivery：Form、Call、Appointment、Application 和 Enrollment

教育 lead 交付形态：

| 形态 | 价值来源 | 治理重点 |
| --- | --- | --- |
| Form CPL | 用户提交项目咨询 | program fit、consent、buyer disclosure |
| Call lead | 用户电话咨询招生 | call disposition、advisor availability |
| Appointment / advisor call | 预约招生顾问 | booked 不等于 completed/enrolled |
| Application started | 用户开始申请 | 更强 signal，但仍非收入 |
| Accepted / admitted | 学校录取 | 受资格、资料和学校判断影响 |
| Enrollment agreement | 用户签署 enrollment | 更接近价值 |
| Class started / census | 用户开始上课并过统计点 | 常用于 paid definition |
| Paid tuition / invoice | 可收款收入 | 最终校准 |

Routing value：

```text
education_routing_value =
  payout
  * program_fit_rate
  * eligibility_pass_rate
  * contact_rate
  * application_rate
  * enrollment_rate
  * class_start_or_paid_rate
  - complaint_risk
  - withdrawal_or_refund_risk
  - payment_lag_cost
```

如果 buyer 只按 enrolled 或 class started 付款，submitted lead 和 advisor appointment 都只能作为中间信号。

## 9. Buyer Acceptance、Reject Reason 和 Enrollment Funnel

常见状态机：

```text
submitted
  -> validation_passed
  -> program_fit
  -> buyer_accepted
  -> advisor_contacted
  -> application_started
  -> application_submitted
  -> admitted / accepted
  -> enrollment_agreement_signed
  -> class_started / census
  -> paid / returned / withdrawn
```

常见 reject reason：

| Reject reason | 含义 | 修复动作 |
| --- | --- | --- |
| bad state / not authorized | 学校不能在该州招生 | geo/state filter |
| wrong program | buyer 不提供该项目 | program selector、negative query |
| no diploma / GED | 入学资格不符 | education level 前置 |
| underage / no guardian | 未成年人流程不完整 | age bucket、guardian consent |
| too far from campus | 到校距离不合理 | campus distance filter |
| online unavailable | program 不支持在线或该州在线 | modality filter |
| low intent | 只想免费资料、工作机会或 scholarship | content funnel、CTA 调整 |
| no consent / invalid disclosure | 招生联系证据不足 | consent proof |
| duplicate / already enrolled | 已在 buyer 系统中 | hash 去重、buyer duplicate window |
| unreachable / no-show | 招生顾问联系失败 | speed-to-lead、cadence |
| financial aid mismatch | 期待免费或不符合 aid | claim review、copy 修正 |

`buyer_accepted` 只是接收，不代表 application 或 enrollment。扩量前要等 application、enrollment、class start 或 paid cohort 成熟。

## 10. Google Ads、Personalized Ads 和 Misrepresentation 边界

Education lead 常见 Google Ads 风险：

| 政策面 | 风险 | 治理 |
| --- | --- | --- |
| Misrepresentation | school identity、accreditation、cost、financial aid、career outcome 不清 | entity、program、cost、credential、claim source 清楚 |
| Personalized advertising | 敏感身份、财务困难、未成年人、宗教/身份相关教育 | 不用敏感属性或困境做诱导定向 |
| Destination requirements | 广告、landing、form、buyer handoff 一致 | 不做 cloaking、隐藏学校或跳转 |
| Lead form assets | 隐私政策、字段、敏感数据和用户 consent | 字段最小化、清楚 disclosure |
| Customer data policies | enhanced conversions / lead upload | consent、hash、用户提供数据安全处理 |

教育广告可以做 program matching，但不能让用户误以为 Google、政府、学校、FAFSA、奖学金机构或 accreditor 背书了你的 lead page。

## 11. Consent、TCPA、CAN-SPAM、DNC 和 Student Data

教育 lead 后续联系常跨 phone、SMS、email 和 advisor call：

- 电话/SMS 要有明确 contact channel consent。
- Email marketing 要有 unsubscribe 和 CAN-SPAM 边界。
- 未成年人和 K-12/tutoring 场景要更谨慎，默认不收不必要 student PII。
- Aged education lead 不能无限 recontact；要按 consent age、buyer terms 和 suppression 审核。
- 多 school/buyer sharing 必须在 disclosure 中说明。
- 不把 full name、phone、email、program、financial aid interest 和 education status 写入 URL、subid、prompt 或日志。

证据字段：

```text
consent_version
buyer_disclosure_version
school_or_program_disclosure_version
contact_channels_allowed
submit_time
timezone
suppression_status
page_snapshot_hash
source_url
```

## 12. Creative / Landing Claim Review

| Claim | 高风险写法 | 安全写法方向 |
| --- | --- | --- |
| Admission | “Get accepted today” | “Review admissions requirements” |
| Job | “Guaranteed job placement” | “Ask about placement support and outcomes” |
| Salary | “Start earning $80k” | “Career outcomes vary” |
| Aid | “Free tuition” | “Financial aid may be available to those who qualify” |
| Accreditation | “Government certified degree” | “Verify accreditation and program approval” |
| Fast completion | “Become a nurse in weeks” | “Program length and licensure vary” |
| Scholarship | “Claim your scholarship” | “Check eligibility and application requirements” |
| Ranking | “Best bootcamp” | “Compare program factors and outcomes” |

Landing page 必备检查：

- school / marketplace / lead generator 身份清楚。
- program name、credential、modality、state limitation、cost/fee、financial aid、privacy policy 有明确入口。
- accreditation、job placement、salary、licensure、transfer credit、scholarship、military/veteran benefit 有来源和条件。
- Form CTA 不暗示已经录取、已经获得资助或已经保证工作。
- 用户看到的页面和审核/爬虫看到的页面一致。

## 13. Offline Value Mapping

建议分层：

| Stage | Ads 信号建议 | 说明 |
| --- | --- | --- |
| submitted lead | secondary / diagnostic | 不直接扩量 |
| validation_passed | diagnostic | 格式和字段通过 |
| program_fit | middle quality | 专业/地区/模式匹配 |
| buyer_accepted | middle quality | 仍可能无联系或拒付 |
| advisor_contacted | stronger | 招生联系成功 |
| application_started | strong | 用户进入申请 |
| application_submitted | strong | 更成熟 |
| admitted / accepted | primary candidate | 更接近价值 |
| enrollment_signed | primary candidate | 重要价值事件 |
| class_started / census | mature primary | 常用于 paid definition |
| paid tuition / invoice | final calibration | 最终 value |
| rejected / no consent / duplicate / complaint | internal negative | 不回传正向 |

不要把 submitted、advisor call、application started 或 buyer accepted 默认当 paid education revenue。

## 14. Education Lead Quality Score

建议评分：

```text
education_lead_quality_score =
  program_fit_rate             15
  eligibility_fit              15
  accreditation_claim_fit      10
  financial_aid_claim_fit      10
  consent_disclosure_quality   10
  contact_or_advisor_rate      10
  application_enrollment_rate  15
  class_start_or_paid_rate     10
  complaint_withdrawal_risk     5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可按 mature enrolled/paid value 小幅扩量 |
| 70-84 | 正常测试，继续收集 enrollment feedback |
| 55-69 | 限量，查 program fit、claim、contact 和 buyer terms |
| 35-54 | 暂停扩量，修 school/program、disclosure、fields 或 source |
| 0-34 | 停 source / buyer / landing，开风险审计 |

评分必须按 program、school buyer、state、modality、source、creative angle、form version、lead age 和 contact channel 拆分。

## 15. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 ED/FTC/FSA/Google 来源 | `/sources` |
| 记录 accreditation、job placement、salary、financial aid、school identity 风险 | `/risk-audits` |
| 用 policy_score、source_score 和 safe CPC 做小预算测算 | `/calculators` |
| 保存 Offer 垂类、国家、policy notes、tracking URL | `/offers` |
| 生成低风险创意和人工审核投放草稿 | Offer 详情页、`/campaigns` |
| 导入 application、enrollment、class started、paid revenue | `/metrics/import` |
| 生成暂停、限量、查 claim、查 enrollment feedback 建议 | `/optimization` |
| 保存任务和审批痕迹 | `/tasks`、`/logs` |

后续可扩展表：

```text
education_vertical_profiles
education_program_profiles
education_qualification_fields
school_buyer_profiles
school_authorization_refs
education_claim_reviews
education_financial_aid_reviews
education_lead_events
education_reject_reason_maps
education_enrollment_stage_events
education_offline_value_maps
education_quality_daily
```

关键字段：

```text
program_interest
credential_goal
school_or_program_id
state
modality
education_level_bucket
start_window
financial_aid_interest
buyer_terms_version
accreditation_source_url
state_authorization_source_url
claim_review_status
consent_version
disclosure_version
offline_stage
reject_reason
paid_value
source_url
reviewer
decision
```

## 16. ADXKit 对应点和完成形态

| ADXKit 能力 | Education lead 场景完成形态 | 不交付内容 |
| --- | --- | --- |
| Offer 管理 | program、school buyer、state、modality、paid definition、accreditation/authorization 来源 | 冒充学校/政府/FAFSA 或伪造 accreditation |
| 落地页采集 | 抽取 job placement、salary、financial aid、accreditation、transfer credit claim | cloaking、隐藏真实 school/buyer |
| AI 创意生成 | 生成“比较项目、了解要求、咨询问题”类低风险素材并进入 claim review | 保证录取、保证就业、保证资助 |
| 投放草稿 | 按 program/state/modality/lead age 拆 campaign/ad group | Cookie 后台自动投放或绕过审核 |
| 换链接 | 只做同 program、同披露、同资格条件、已审核 URL 轮换 | 用换链跳到未披露学校或资助页 |
| 任务中心 | accreditation review、financial aid claim review、buyer feedback 导入、source quarantine | 自动外呼、短信轰炸、伪造学生资料或 enrollment |
| 来源库 | ED、FTC、FSA、Google 官方来源可追踪 | 用二手招生话术替代官方来源 |

完成口径：把教育 lead 的行业知识、招生资格、学校/lead generator 边界、accreditation、job/薪资/资助 claim、buyer acceptance、enrollment/paid value 和系统审计做完整；不做对抗平台、绕过登录、伪造学生资料或制造虚假流量。

## 17. QA 清单

上线前逐项检查：

- `program_interest` 是否明确：degree、bootcamp、CDL、nursing、cosmetology、tutoring 等不能混用。
- 页面主体是否真实：school、program marketplace、lead generator、advertiser 角色是否清楚。
- Accreditation、state authorization、licensure、financial aid、job placement、salary、transfer credit claim 是否有来源 URL。
- 是否避免 guaranteed admission、guaranteed job、guaranteed salary、free tuition、government scholarship 等强承诺。
- 是否说明 financial aid may be available to those who qualify。
- 是否避免收 FSA ID、SSN、loan login、完整成绩单、完整未成年人 PII。
- Consent 是否包含 contact channel、school/buyer disclosure、version/hash 和页面证据。
- 多 school / shared lead 是否在 disclosure 和 buyer terms 中说明。
- Buyer terms 是否写明 accepted、application、admitted、enrolled、class started、paid definition。
- Aged education lead 是否与 fresh lead 分 conversion action、payout tier 和 attribution。
- Offline value 是否按 advisor contact、application、admitted、enrolled、class started、paid 分层。
- Google Ads primary conversion 是否使用成熟、可收款、低投诉的事件。
- 不使用 Ads Cookie 后台操作、自动登录、cloaking、代理/指纹规避、补点击或封禁规避。

## 18. 信息来源 URL

| 来源 | URL | 用途 |
| --- | --- | --- |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑学校主体、accreditation、费用、资助、就业结果和重要限制透明度 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑敏感身份、未成年人、财务困难、宗教/身份相关教育等个性化广告边界 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Ads Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户提供数据、enhanced conversions、consent 和安全处理 |
| FTC, Guides for Private Vocational and Distance Education Schools | https://www.ftc.gov/legal-library/browse/rules/private-vocational-distance-education-schools | 支撑 vocational / distance education 的 accreditation、就业前景、入学资格和 deceptive sales claim |
| eCFR, 16 CFR Part 254 Guides for Private Vocational and Distance Education Schools | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-254 | 支撑现行 vocational school guides 条文引用 |
| FTC, Choosing a Vocational School or Certificate Program | https://consumer.ftc.gov/articles/choosing-vocational-school-or-certificate-program | 支撑 job placement、accreditation、licensing、cost、financial aid 和职业培训用户教育 |
| FTC, Choosing a College: Questions To Ask | https://consumer.ftc.gov/choosing-college-questions-ask | 支撑 college selection、accreditation、cost、graduation 和 job outcome 问题 |
| FTC, College Degree Scams | https://consumer.ftc.gov/articles/college-degree-scams | 支撑虚假 degree、假 accreditation 和 diploma mill 风险 |
| U.S. Department of Education, College Accreditation | https://www.ed.gov/laws-and-policy/higher-education-laws-and-policy/college-accreditation | 支撑 accreditation 来源和认可框架 |
| U.S. Department of Education, Find a College or Educational Program | https://www.ed.gov/higher-education/find-college-or-educational-program | 支撑 College Scorecard、College Navigator 和 program comparison 官方入口 |
| U.S. Department of Education, College Affordability and Transparency | https://www.ed.gov/higher-education/paying-college/college-affordability-and-transparency | 支撑 cost、debt、graduation rate、College Scorecard 和 College Navigator |
| College Navigator, NCES | https://nces.ed.gov/collegenavigator/ | 支撑 program、tuition、aid、admissions、accreditation、graduation rate 查询 |
| College Scorecard | https://collegescorecard.ed.gov/ | 支撑 cost、fields of study、graduation、debt、earnings 和 school comparison |
| Federal Student Aid, Avoid student loan debt relief scams | https://studentaid.gov/resources/scams | 支撑 student loan relief、政府冒充和收费代办风险 |
| Federal Student Aid, Preparing for College | https://studentaid.gov/resources/prepare-for-college | 支撑 college planning、financial aid 和官方学生资源 |
| FTC, How Student Loans Work and How To Avoid Scams | https://consumer.ftc.gov/articles/how-student-loans-work-how-avoid-scams | 支撑 student loan、financial aid 和教育债务 claim 风险 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑教育 lead 后续 email 联系、unsubscribe 和商业邮件边界 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
