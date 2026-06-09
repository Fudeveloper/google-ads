# Employment、Recruiting 与 Staffing Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / CPA / Job Board / Recruiting / Staffing / Temp Agency / Gig Work / Remote Work / Career Lead 套利里，Employment Lead、Job Applicant Lead、Staffing Lead、Recruiting Lead、Job Board Registration、Resume Lead、Interview Booking、Hiring Funnel Lead 和 Work-from-home / Business Opportunity Lead 为什么是高量、高信任、高欺诈和高歧视风险的垂类。它承接 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)、[敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)、[Lead Form 漏斗、资格问题与移动端 UX 治理手册](lead_form_funnel_qualification_ux.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)、[隐私、Consent 与追踪合规手册](privacy_consent_tracking.md)、[CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md) 和 [受众定向、再营销与 Customer Match 合规手册](audience_remarketing_customer_match_policy.md)，重点回答：就业 lead 的 real job order、employer / staffing agency authorization、job category、location / remote、pay claim、employment vs contractor、work authorization、protected-class targeting、resume data、background check、interview / placement / hire 回传、buyer acceptance 和 Google Ads 信号应该如何治理。

本文不是法律意见，也不提供虚假招聘、假 offer、简历抓取、伪造申请人资料、伪造工作经历/证书/背景调查、绕过就业广告定向限制、歧视性筛选、出售敏感简历数据、自动外呼、短信群发、使用 Ads Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做行业知识、字段最小化、职位真实性审计、claim 审核、来源 URL、consent/disclosure、buyer terms、reject reason、hiring stage、offline value、风险任务和人工审批。

## 1. 为什么 Employment Lead 是高量高信任垂类

就业 lead 的点击和表单量通常很大，因为用户有强烈需求：找工作、换工作、兼职、远程、临时工、卡车/护理/销售等高需求岗位、招聘会或求职平台注册。但一个 job lead 的真实价值不在于 submit，而在于是否进入可服务的申请、面试、入职或 billable placement。

```text
search intent
  -> job page / staffing page / application
  -> job authenticity and employer authorization
  -> qualification and consent
  -> valid applicant
  -> recruiter contacted
  -> screened / qualified
  -> interview scheduled
  -> interview attended
  -> offer / placement / hire
  -> start date / retention / paid
```

常见亏损路径：

- 页面写“remote data entry $35/hr immediate hire”，实际是泛招聘库、培训课、业务机会或过期岗位。
- Google Ads 触发 employment / HEC targeting 限制，仍按年龄、性别、邮编、家庭状态等做排除或出价。
- Buyer 只按 qualified applicant、interview attended、hire 或 start date 付款，广告端按 form submit 学习。
- 求职者被要求先付款、买设备、交押金、存支票、转账或提供银行/身份证信息。
- Staffing buyer 因 location、shift、license、experience、work authorization、duplicate、unreachable、no-show 或 failed background check 拒付。
- 低质流量来自 job scam、work-from-home scam、support query、student research、visa scam、government/postal job impersonation。

Employment lead 的核心是“真实职位 + 非歧视定向 + 资格最小化 + hiring stage 回传”，不是越多简历越好。

## 2. 原理解释：Employment Lead 是机会、资格、信任和雇佣回传的交接

就业广告影响用户能否接触工作机会，因此平台和监管关注“access to opportunities”。套利团队如果只追求低 CPL，容易买到虚假岗位、过期岗位、低工资误导、非法业务机会或歧视性定向。

| 交接 | 说明 | 失败后果 |
| --- | --- | --- |
| Opportunity handoff | 岗位是否真实、当前有效、授权发布、可申请 | fake job、ghost job、complaint |
| Qualification handoff | 经验、证书、地点、班次、work authorization、availability 是否匹配 | buyer reject、no-show |
| Fair access handoff | 定向、文案和筛选是否排除受保护群体或触发 HEC 限制 | policy restriction、discrimination risk |
| Trust handoff | pay、remote、benefits、fee、employment status、agency role 是否清楚 | misrepresentation、job scam |
| Hiring feedback handoff | valid applicant、screened、interview、offer、hire、start、paid 是否拆开 | 浅层信号扩量亏损 |

建议测算：

```text
effective_employment_lead_value =
  headline_payout
  * real_job_order_rate
  * eligibility_pass_rate
  * contact_rate
  * recruiter_screen_pass_rate
  * interview_scheduled_rate
  * interview_attended_rate
  * offer_or_hire_rate
  * start_or_paid_rate
  - compliance_reserve
  - no_show_cost
  - complaint_risk
  - payment_lag_cost
```

如果 buyer 的 paid event 是 hire / start date / retention，不应把 submitted 或 resume upload 设为 primary conversion。

## 3. Job / Buyer Type 地图

| Subvertical | 用户意图 | 典型资格字段 | 主要风险 |
| --- | --- | --- | --- |
| Direct employer hiring | 申请真实公司岗位 | location、experience、role fit、availability | ghost job、discrimination、pay transparency |
| Staffing / temp agency | 临时工、派遣、合同工 | city、shift、transport、certification、start window | agency fee、no-show、job order freshness |
| Job board / aggregator | 搜索岗位、创建 profile | job category、location、email consent | duplicate、过期岗位、lead resale |
| Gig / contractor | rideshare、delivery、freelance、field work | region、license/equipment bucket、schedule | contractor misclassification、earnings claim |
| Remote / work-from-home | 远程岗位、兼职 | role type、equipment、availability | job scam、business opportunity、fake check |
| Government / postal jobs | federal/postal application | official source verification | impersonation、paid application scam |
| Healthcare / CDL / skilled trade recruiting | 高需求岗位 | license/certification、state、experience | false pay, credential claim, training upsell |
| Franchise / business opportunity | income opportunity, owner-operator | investment amount, disclosure received | business opportunity rule、earnings claim |

## 4. 资格字段和数据最小化

就业 lead 字段要用于 job match，不是收集完整简历或敏感身份。

| 字段 | 用途 | 建议 |
| --- | --- | --- |
| job category | routing、intent | 必要 |
| zip / city / commute radius | local job match | 用 city/region，避免过细定向污染 |
| remote / onsite / hybrid | availability match | 不夸大 remote |
| experience bucket | qualification | 用年限范围，不收完整履历 |
| license / certification bucket | CDL、nursing、trade 等必要匹配 | 不收证件照片，先问是否持有 |
| shift / schedule | staffing fit | 可选 |
| work authorization bucket | legal eligibility | 谨慎，不做歧视性筛选 |
| pay expectation bucket | fit / transparency | 和 job posting pay range 对齐 |
| resume upload | detailed screening | 可选，保存 consent 和 retention |
| background check consent | 后续流程 | 不在 lead 阶段默认收敏感报告 |

不应默认收集：SSN、驾照照片、护照、I-9 文件、银行账号、完整出生日期、完整家庭地址、医疗/残障信息、犯罪记录、信用报告、完整简历抓取、社媒账号密码或政府登录信息。

## 5. Real Job Order、Employer Authorization 和 Ghost Job 风险

上线前要证明岗位真实：

- Employer / staffing agency / recruiter 的真实主体、地址、联系方式和授权关系。
- Job title、duties、location、remote status、pay range、employment type、schedule、benefits、required license、start window 是否来自有效 job order。
- Job posting 是否有 expiration / freshness / requisition id / buyer owner。
- 是否允许 third-party lead generation、shared lead、resume resale、job board distribution。
- Paid definition 是 valid applicant、qualified applicant、interview、hire、start date、retention 还是 invoice paid。

高风险信号：

- “立即录用”“无需面试”“先付费/买设备/交押金”“存支票再转账”“政府/邮政保证岗位”。
- 过期岗位、无 employer name、无职位地点、无 pay detail、职位描述和 landing 不一致。
- 用 remote/work-from-home 引流到 training、course、MLM、franchise、business opportunity 或 unrelated offer。

## 6. Google Ads、HEC / Employment Targeting 和 Personalized Ads 边界

Google 对美国/加拿大住房、就业、信贷类广告有特殊 personalized advertising targeting 限制。Employment ads 包括推广工作机会或雇佣某人从事工作。

治理规则：

- 如果广告或 landing 涉及 jobs、careers、hiring、staffing、recruiting、employment opportunity，先按 employment scope 审核。
- 美国/加拿大就业广告不要使用受限定向或排除，例如 zip code、gender、age、parental status、marital status、demographic targeting 等。
- 不用 remarketing / Customer Match / similar audience 去重新定向特定敏感求职状态的人群，除非确认政策允许且 consent / privacy 充分。
- 不按年龄、性别、家庭状态、族裔、宗教、残障、怀孕、国籍等 protected class 做出价、排除、文案或表单筛选。
- Location targeting 应按政策允许的粒度、岗位服务范围和公平访问原则使用。

Employment lead 的出价优化应基于合规的 search intent、job category、geo 合规分层和 hiring stage feedback，而不是利用敏感人群属性。

## 7. Job Scam、Work-from-home 和 Business Opportunity 风险

FTC 对 job scams、work-from-home、business opportunity 有明确消费者教育和规则语境。Employment lead 页面应特别避免：

- 向求职者收费，承诺“付费保证入职”。
- 要求先买设备、培训包、认证、软件、名单或背景调查，再获得工作。
- 发送假支票、要求转账、购买礼品卡或加密货币。
- 使用政府、邮政、联邦岗位名义收费。
- 把 business opportunity、MLM、franchise、affiliate scheme、coaching program 伪装成 job。
- 使用夸张 earnings claim：每天几百美元、被动收入、无需经验高收入。

如果是 business opportunity，而不是 employment job，必须单独标注，不进入普通 job lead 口径。

## 8. EEOC、Job Ads、Recruitment 和 Discrimination 边界

就业广告和招聘不能显示偏好或劝退受保护群体。风险包括：

- 文案写 young、recent graduate、female only、native English only、able-bodied、single、no children 等。
- Recruitment 只投向或只展示给同质人群，造成不公平排除。
- Screening question 与岗位无关，却排除 protected class。
- 背景调查、测试、语言要求、学历要求、体能要求没有 job-related / business necessity 依据。
- Employment agency 遵从歧视性 employer request。

系统落地：

- 每个 job ad / landing claim 保存 reviewer 和 source URL。
- 对 exclusionary wording、protected-class targeting、unjustified requirements 设 redline。
- 对 background check、criminal history、credit report、medical/genetic information 另建人审。

## 9. Pay、Benefits、Remote、Contractor 和 Classification 风险

求职者最容易被 pay、remote、benefits 和 employment status 误导。

治理规则：

- Pay range、commission、tips、bonus、piece rate、draw、guarantee pay 要写清适用条件。
- Remote / hybrid 要说明 location restriction、equipment、travel、time zone、onsite training。
- Employee、contractor、1099、owner-operator、franchise、business opportunity 不能混用。
- Contractor / gig offer 要避免把 earnings claim 写成 guaranteed wage。
- Benefits claim 要说明 eligibility、waiting period、full-time/part-time 限制。
- State / city pay transparency 规则可能影响 job posting，系统要保存 target geo 和 pay disclosure review。

## 10. Background Check、Resume Data 和 Candidate Privacy

Resume 和 applicant data 是个人数据，可能包含地址、电话、教育、工作经历、证书、移民/签证暗示、残障/医疗暗示、照片等。

治理规则：

- Resume upload 要有隐私政策、分享对象、retention、delete request 和 buyer handoff。
- Background check 不能在 lead 阶段暗示“已批准”或“必过”。
- 如果使用第三方 background report，需评估 FCRA / consent / adverse action 流程。
- 不要在 URL、UTM、subid、event name 中写入 job seeker identity、resume details、work authorization 或 background check status。
- 不出售或共享简历给未披露 buyer，不把一份简历自动投递到无关岗位。

## 11. Lead Delivery：Form、Call、Resume Upload、Interview 和 Hire

常见 delivery 模式：

| 模式 | 适用 | 风险 |
| --- | --- | --- |
| Form lead | staffing、job board、recruiting | low intent、duplicate、unreachable |
| Resume upload | direct employer、agency | data privacy、over-sharing |
| Call lead | high urgency staffing | call duration 不等于 qualified applicant |
| Application start | job board / employer ATS | abandonment、invalid applicant |
| Interview booking | staffing / direct hire | no-show、availability mismatch |
| Hire / start date | CPA / recruitment | long lag、clawback、retention risk |

状态机至少拆开：

```text
lead_submit
  -> valid_contact
  -> job_match
  -> recruiter_contacted
  -> screened
  -> qualified_applicant
  -> application_submitted
  -> interview_scheduled
  -> interview_attended
  -> offer
  -> hired
  -> start_date
  -> retention_or_paid
```

不能把 lead submit、resume upload、call connected、application started 或 interview scheduled 自动当成 paid employment lead。

## 12. Buyer Acceptance、Reject Reason 和 Hiring Funnel

常见 reject reason：

| Reject reason | 解释 | 对投放的动作 |
| --- | --- | --- |
| job_not_available | 岗位过期/已招满 | 停止对应 landing / keyword |
| bad_geo | 不在工作地点/通勤范围 | 地理和页面说明调整 |
| wrong_role | 职位类别不匹配 | query / landing 修正 |
| insufficient_experience | 经验不符合 | qualification field 调整 |
| license_missing | 缺 CDL / healthcare / trade license | 预筛字段 |
| schedule_mismatch | 班次/可用时间不匹配 | shift field / ad copy |
| work_auth_mismatch | work authorization 不符合 | 谨慎合规处理 |
| duplicate | 重复申请人 | suppression |
| unreachable | 联系不上 | speed-to-lead 和 consent |
| no_show | 面试未到 | reminder / source quality |
| failed_background | 背调或资格失败 | buyer terms，谨慎记录 |
| complaint_or_scam | 用户投诉职位虚假/收费 | 停投和事故复盘 |

Reject reason 要回写到 campaign、keyword、search term、landing、job order 和 buyer。

## 13. Consent、TCPA、CAN-SPAM、DNC 和 Candidate Communication

就业 follow-up 常见电话、短信、邮件、WhatsApp、chat。治理规则：

- Call/text/email consent scope 要说明 who contacts、for which job category、shared with whom、how to opt out。
- DNC、unsubscribe、stop reply 和 suppression 要同步给 buyer / agency。
- 不群发无关岗位，不把一个 job application 自动转卖给多个无披露 buyer。
- Email 要符合商业邮件身份、地址、subject、unsubscribe 要求。
- 电话/短信要记录 consent、time、purpose 和 opt-out。

系统不做自动外呼、短信群发、绕 DNC 或补 consent。

## 14. Creative / Landing Claim Review

上线前审核表：

| 审核项 | 通过标准 |
| --- | --- |
| Employer identity | 真实 employer / agency / recruiter 角色清楚 |
| Job order | requisition、job title、location、status、source URL |
| Pay claim | pay range、commission、bonus、tips、conditions 清楚 |
| Remote claim | remote/hybrid/onsite、location/timezone/travel 限制清楚 |
| Employment type | employee、contractor、franchise、business opportunity 不混淆 |
| Fee | 求职者不为保证工作预付费；business opportunity 单独披露 |
| Targeting | employment / HEC targeting 审核通过 |
| Anti-discrimination | 无 protected-class preference 或 discouragement |
| Data privacy | resume / contact / background data 最小化 |
| Offline value | submit、screened、interview、hire、start、paid 拆开 |

## 15. Offline Value Mapping

Employment lead 的 conversion action 建议：

| Stage | 是否建议 primary | 原因 |
| --- | --- | --- |
| page view / job detail view | no | 只是兴趣 |
| lead submit / resume upload | no / secondary | 浅层、重复和低质风险高 |
| valid contact | secondary | 数据质量 |
| job match | secondary | 初步资格 |
| recruiter screened | secondary / primary candidate | 质量更好 |
| qualified applicant | primary candidate | 接近 buyer value |
| interview scheduled | secondary | no-show 风险 |
| interview attended | primary candidate | 更接近 hire |
| offer / hired | primary | 接近收入 |
| start date / retention / paid | primary | 最接近真实利润 |

保守权重：

```text
lead_submit = 0.03
valid_contact = 0.08
job_match = 0.15
screened = 0.25
qualified_applicant = 0.40
interview_attended = 0.65
hire = 0.85
start_or_paid = 1.00
```

权重要按 job category、buyer、geo 和 source 单独校准。

## 16. Employment Lead Quality Score

建议评分：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| Job authenticity | 20 | real job order、freshness、authorization |
| Fair access / policy fit | 20 | HEC targeting、anti-discrimination |
| Qualification fit | 15 | experience、license、schedule、geo |
| Claim proof | 15 | pay、remote、benefit、employment type |
| Candidate data hygiene | 10 | resume、background、retention、sharing |
| Hiring stage quality | 10 | screened、interview、hire、start |
| Source quality | 10 | scam、duplicate、complaint、invalid traffic |

```text
employment_lead_quality_score =
  job_authenticity * 0.20
  + fair_access_policy_fit * 0.20
  + qualification_fit * 0.15
  + claim_proof * 0.15
  + candidate_data_hygiene * 0.10
  + hiring_stage_quality * 0.10
  + source_quality * 0.10
```

低于 75 不扩量；低于 65 只允许诊断；出现收费求职、虚假政府/邮政岗位、fake check、protected-class exclusion、private data abuse 或 job scam complaint 时暂停。

## 17. 系统落地

本系统当前完成的是知识、审核和设计形态：

- `/knowledge/employment_leads` 展示本手册。
- `/sources` 保存 Google、FTC、EEOC、DOL、IRS、CareerOneStop、USAJobs 等来源。
- `/risk-audits` 记录 HEC targeting、job order、pay/remote claim、work-from-home scam、business opportunity、EEOC wording、classification、resume privacy、background check、hiring stage mapping。
- `/offers` 保存垂类、目标 URL、tracking URL、policy notes、creative angles。
- `/calculators` 使用 safety factor、policy score、tracking score、source score 评估是否可测试。
- `/metrics/import` 允许导入 qualified applicant、interview attended、hire、start、paid，不把 submitted 默认当收入。

后续如果要实体表，应优先建：

| 表 | 用途 |
| --- | --- |
| `employment_vertical_profiles` | job category、buyer type、paid definition、geo |
| `employment_job_orders` | employer、requisition、title、location、pay、freshness |
| `employment_qualification_fields` | field、purpose、sensitivity、reject reason |
| `employment_claim_reviews` | pay、remote、benefit、employment type、fee claim |
| `employment_targeting_reviews` | HEC / protected-class / location targeting 审核 |
| `employment_candidate_events` | lead、screened、qualified、interview、hire、start、paid |
| `employment_reject_reason_maps` | buyer reject、source action、job order action |
| `employment_offline_value_maps` | stage、weight、Google Ads conversion mapping |

## 18. ADXKit 对应点和完成形态

| ADXKit 类能力 | Employment lead 安全完成形态 |
| --- | --- |
| Offer 管理 | 增加 job category、buyer type、job order、paid definition |
| 创意生成 | 生成 angle 前先做 pay/remote/job authenticity/anti-discrimination redline |
| 自动优化 | 基于 qualified applicant、interview、hire、start、paid 和 reject reason，不基于 submit |
| 自动投放 | 只产出人工审核的结构、CSV、任务，不做 Cookie 后台操作 |
| 换链接 | 只做真实 Final URL 变更 QA，不做 ghost job、cloaking 或岗位伪装 |
| 来源库 | 保存 Google/FTC/EEOC/DOL/IRS/CareerOneStop 等来源和摘要 |
| 风险审计 | 对 HEC targeting、job scam、pay claim、resume privacy、background check、buyer acceptance 建审计项 |

## 19. QA 清单

- 是否确认 employer / staffing agency / recruiter 的真实主体和授权？
- 是否有 real job order、requisition、location、pay、freshness 和 expiration？
- 是否确认广告属于或不属于 employment / HEC scope？
- 是否没有使用受限 demographic / zip / marital / parental / age / gender targeting？
- 是否没有 protected-class preference、recent graduate、young、female only 等排除性文案？
- 是否没有求职者预付费、fake check、government/postal impersonation、business opportunity 伪装？
- 是否 pay、remote、benefits、contractor/employee、commission、bonus claim 有 proof URL？
- 是否只收必要 candidate data，且 resume/background data 有 consent、retention、sharing 和 deletion？
- 是否拆开 submit、valid、screened、qualified、interview、hire、start、paid？
- 是否不使用 Ads Cookie 登录、不绕 2FA、不刷量、不用代理/指纹规避、不做 cloaking、不为规避封禁换号？

## 20. 信息来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑 employment opportunity / hiring 相关个性化广告和 HEC targeting 限制 |
| Google Ads Policy, Housing, employment, and credit FAQ | https://support.google.com/adspolicy/answer/9997418 | 支撑美国/加拿大 employment ads scope、policy acceptance 和 appeal 语境 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑职位真实性、主体、费用、薪资、远程和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Ads Policy, Lead form requirements | https://support.google.com/adspolicy/answer/9472930 | 支撑 lead form 内容限制、字段和敏感垂类边界 |
| Google Ads Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑 Customer Match、用户提供数据、披露和 consent |
| FTC, Job Scams | https://consumer.ftc.gov/articles/job-scams | 支撑 job scam、placement firm fee、government/postal job scam 和求职安全 |
| FTC, Job and Money-Making Scams | https://consumer.ftc.gov/features/job-and-money-making-scams | 支撑 job scam、work-from-home、money-making scheme 风险 |
| FTC, Business Opportunity Rule | https://www.ftc.gov/legal-library/browse/rules/business-opportunity-rule | 支撑 business opportunity、work-at-home disclosure 和 earnings claim 语境 |
| FTC, Selling a Work-at-Home or Other Business Opportunity | https://www.ftc.gov/business-guidance/resources/selling-work-home-or-other-business-opportunity-revised-rule-may-apply-you-1 | 支撑 work-at-home / bizopp disclosure、language 和 earnings claim |
| FTC, Taking the Ploy out of Employment Scams | https://www.ftc.gov/business-guidance/blog/2023/01/taking-ploy-out-employment-scams | 支撑 fake check、job opportunity scam 和 business guidance |
| EEOC, Prohibited Employment Policies/Practices | https://www.eeoc.gov/prohibited-employment-policiespractices | 支撑 job ad、recruitment、application、protected-class discrimination 边界 |
| EEOC, Recruiting, Hiring, or Promoting Employees | https://www.eeoc.gov/employers/small-business/3-im-recruiting-hiring-or-promoting-employees | 支撑招聘、筛选、测试、背景调查和小企业 hiring guidance |
| EEOC, Background Checks | https://www.eeoc.gov/background-checks | 支撑 background check 和 equal employment opportunity 边界 |
| FTC, Background Checks: What Employers Need to Know | https://www.ftc.gov/business-guidance/resources/background-checks-what-employers-need-know | 支撑 employment background reports、written permission、FCRA 和 adverse action |
| DOL, Misclassification of Employees as Independent Contractors | https://www.dol.gov/agencies/whd/flsa/misclassification | 支撑 employee vs independent contractor 和 FLSA misclassification 风险 |
| IRS, Independent Contractor or Employee | https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-self-employed-or-employee | 支撑 worker classification、behavioral/financial/control 判断 |
| CareerOneStop, Job Search | https://www.careeronestop.org/JobSearch/job-search.aspx | 支撑 DOL-sponsored job search 资源和可信求职来源 |
| CareerOneStop, 3 Tips to Avoid Job Scams | https://blog.careeronestop.org/3-tips-to-avoid-job-scams/ | 支撑求职骗局、预付费和非法活动警示 |
| USA.gov, How to Find a Job | https://www.usa.gov/job-help | 支撑政府 job search、CareerOneStop 和 official resource |
| USAJOBS | https://www.usajobs.gov/ | 支撑 federal government job official source |
| USPS Inspection Service, Government Employment Scams | https://www.uspis.gov/news/scam-article/usps-government-employment-scams | 支撑 postal/government job impersonation 和收费骗局 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑求职后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
