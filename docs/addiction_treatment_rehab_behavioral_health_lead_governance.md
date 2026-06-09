# Addiction Treatment、Rehab 与 Behavioral Health Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / CPA / Call Lead / Admissions Lead / Appointment Lead / Treatment Referral / Behavioral Health Lead 套利里，Addiction Treatment Lead、Drug Rehab Lead、Alcohol Rehab Lead、Detox Lead、Sober Living Lead、Opioid Treatment Lead、Mental Health / Co-occurring Disorder Lead、Recovery Support Lead 和 Crisis Hotline Lead 为什么是极高 payout、极高敏感数据、极高政策认证和极高伦理风险的垂类。它承接 [Healthcare、Medical Appointment 与 Clinic Lead 治理手册](healthcare_medical_appointment_lead_governance.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)、[Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](pay_per_call_buyer_routing_duration_payout_governance.md)、[Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md)、[隐私、Consent 与追踪合规手册](privacy_consent_tracking.md)、[敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md) 和 [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md)，重点回答：addiction treatment lead 的 certification、provider license、level of care、patient brokering、insurance verification、crisis/suicide handling、Part 2 confidentiality、HIPAA tracking、admission eligibility、call center routing、buyer acceptance、offline value mapping 和 Google Ads 信号应该如何治理。

本文不是医疗、法律或合规意见，也不提供诊断、治疗建议、患者转介规避、patient brokering、kickback、诱导入院、伪造保险/身份/诊断/病历、伪造 certification、绕过 LegitScript / Google Ads addiction services certification、危机热线冒充、自动外呼、短信群发、使用 Ads Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做行业知识、准入审计、字段最小化、claim 审核、来源 URL、consent/disclosure、buyer terms、reject reason、admission stage、offline value、风险任务和人工审批。

## 1. 为什么 Addiction Treatment Lead 是极高 payout 极高伦理风险垂类

Addiction treatment / rehab lead 的 payout 可能来自 treatment center、detox facility、residential program、IOP/PHP、telehealth provider、sober living、opioid treatment program、call center、referral network 或 admissions partner。一个有效 lead 可能进入保险验证、clinical assessment、admission、transport、treatment stay、claim billing 和 aftercare，因此商业价值很高。

```text
urgent search / family search
  -> treatment information / call / form
  -> certification and provider identity review
  -> crisis / safety triage
  -> privacy and consent context
  -> level-of-care / location / insurance fit
  -> admissions call
  -> clinical assessment
  -> insurance verification / payment fit
  -> admitted / arrived
  -> treatment started
  -> claim approved / paid
  -> retention / discharge / complaint
```

常见亏损和伤害路径：

- 页面或热线伪装成 SAMHSA、政府、非营利 crisis hotline、local facility 或 “independent helpline”，实际转卖给第三方 treatment center。
- Google Ads 需要 addiction services certification，但 advertiser / landing / call center / lead generator 未认证或域名不一致。
- 表单过度收集 SUD、mental health、medication、insurance、family details、crisis status 等高敏信息。
- Buyer 只按 admitted、arrived、treatment started 或 insurance-paid 结算，广告端按 call duration 或 form submit 学习。
- “free rehab”“covered by insurance”“same-day admission”“luxury treatment”“MAT available”“licensed clinicians” 等 claim 没有证据。
- Patient brokering、kickback、travel incentive、free rent、gift card、insurance harvesting、urine testing fraud 或 inappropriate referral 风险。
- 用户处于危机、自伤、overdose 或 withdrawal risk，但页面把紧急求助导向普通销售 funnel。

Addiction treatment lead 的核心是“合规认证 + 危机安全 + 隐私保护 + level-of-care fit + admission/paid 回传”，不是把痛苦搜索变成低成本转介。

## 2. 原理解释：Addiction Lead 是危机、隐私、治疗资格和付款路径的交接

成瘾治疗 lead 与普通医疗 lead 的差异在于，用户可能处于急性危机，信息可能受 HIPAA 和 42 CFR Part 2 语境保护，转介和付款可能涉及 patient brokering 或 kickback 风险，且治疗选择对用户和家庭后果很大。

| 交接 | 说明 | 失败后果 |
| --- | --- | --- |
| Crisis handoff | 是否存在 overdose、自伤、withdrawal、suicide 或 emergency need | 延误紧急求助 |
| Privacy handoff | SUD / mental health 信息、call recording、tracking、sharing 是否被保护 | Part 2 / HIPAA / complaint risk |
| Provider handoff | treatment center、call center、lead generator、referral agency 角色是否清楚 | impersonation、misrepresentation |
| Eligibility handoff | level of care、location、insurance/payment、age、medical acuity 是否匹配 | buyer reject、unsafe referral |
| Admission handoff | call、assessment、verification、admitted、arrived、started、paid 是否拆开 | 浅层信号扩量亏损 |

建议测算：

```text
effective_addiction_lead_value =
  headline_payout
  * certification_pass_rate
  * provider_license_fit_rate
  * consent_privacy_pass_rate
  * clinical_fit_rate
  * insurance_or_payment_fit_rate
  * admissions_contact_rate
  * admitted_or_arrived_rate
  * treatment_started_rate
  * paid_after_clawback_rate
  - compliance_reserve
  - crisis_mishandling_risk
  - privacy_complaint_risk
  - patient_brokering_risk
```

如果 buyer 只愿意按 insurance-approved admission 付款，不应把 call duration、form submit 或 admissions call 作为 primary conversion。

## 3. Program / Service Type 地图

| Subvertical | 用户意图 | 典型资格字段 | 主要风险 |
| --- | --- | --- | --- |
| Detox | acute withdrawal, immediate help | substance category、location、medical acuity、insurance/payment | emergency handling、medical supervision、availability claim |
| Residential rehab | inpatient / residential treatment | state、level-of-care need、insurance/payment、age bucket | license、patient brokering、travel incentive |
| PHP / IOP | structured outpatient treatment | location/telehealth、schedule、clinical fit | level-of-care mismatch、billing claim |
| Sober living | recovery housing | location、rules fit、payment bucket | licensing/state rules、kickback/referral |
| OTP / methadone | opioid treatment program | location、OUD treatment need、OTP access | SAMHSA certification、Part 8, medication claim |
| MAT / MOUD | buprenorphine/naltrexone/methadone info | provider type、state、treatment need | prescription / clinical claim, scope |
| Telehealth SUD | virtual counseling / MAT | state, service type, age bucket | state licensure、privacy、medication limits |
| Crisis hotline / helpline | immediate support / referral | emergency indicator、location | government/nonprofit impersonation、safety |
| Dual diagnosis / mental health | co-occurring treatment | condition category、level of care | health targeting、claim risk、privacy |

## 4. Offer 准入、Google Ads Certification、LegitScript 和 Provider License

上线前必须回答：

- 该网站、app、call center、lead generator、referral agency 或 treatment provider 是否属于 Google Ads addiction services policy 范围？
- 是否需要 LegitScript addiction treatment certification 或 Google Ads healthcare/addiction certification？
- Google Ads account、certified domain、final URL、display URL、business name、call tracking number 和 landing provider 是否一致？
- Provider 是否有 state license / certification / accreditation / OTP certification / clinical staff credentials？
- Lead generator 是否被允许转介、收款、routing 或售卖 lead？是否存在 patient brokering / kickback 风险？
- Buyer terms 是否明确 accepted、admitted、arrived、started、insurance approved、paid、clawback 和 complaint handling？

默认拒绝：

- “先跑广告再补认证”“换域名绕 addiction flag”“用 mental health 泛页绕 rehab policy”。
- 没有真实 provider identity、license、location、privacy policy、clinical scope 和 crisis instruction。
- Call center 冒充政府、SAMHSA、local facility、nonprofit helpline 或 insurance advocate。
- Buyer 要求隐藏 lead source、隐瞒转介关系、按患者入院支付不透明回扣或提供 travel / gift / rent incentive。

## 5. Provider / Referral / Call Center 角色边界

Addiction treatment lead 里的角色必须写清：

| 角色 | 可做 | 高风险边界 |
| --- | --- | --- |
| Licensed treatment provider | 提供治疗信息、assessment、admission | 不能夸大 level of care、license、availability |
| Call center / admissions line | 接听、初筛、转接到 provider | 不能冒充独立 helpline 或 clinical provider |
| Lead generator | 收集 inquiry、转发给 buyer | 不能隐藏 commercial relationship 或 SUD data sharing |
| Referral agency | 推荐或匹配 provider | 需披露付费关系、资质和选择标准 |
| Sober living / recovery housing | 住宿和 recovery support | 不能伪装 clinical treatment |
| Crisis hotline | 危机支持 | 不能用销售 funnel 替代 emergency / 988 / SAMHSA resource |

系统记录 provider_role、buyer_role、clinical_scope、source_url、disclosure_version、reviewer 和 decision。

## 6. Crisis、Suicide、Overdose 和 Emergency Handling

成瘾治疗页面必须避免把紧急风险延误到营销流程：

- 如果用户表达 overdose、自伤、suicide、severe withdrawal、medical emergency，应提示紧急服务 / crisis line，而不是继续优化 lead submit。
- 页面可以提供 SAMHSA / 988 / emergency resources，但不能冒充这些官方资源。
- Call scripts 要有 crisis escalation SOP；普通 sales agent 不应提供医疗诊断或危机干预。
- Crisis event 不应被上传为广告优化信号或用于 retargeting。
- 高危页面要减少 friction，但不能牺牲 disclosure、privacy 和 emergency routing。

系统只记录 crisis_policy_review 和 escalation_sop，不自动处理危机对话。

## 7. HIPAA、42 CFR Part 2、Tracking 和 SUD Data 边界

Substance use disorder treatment records 可能受到 42 CFR Part 2 特别保护；医疗页面 tracking 也可能把 PHI / IIHI 泄露给广告或分析平台。

治理规则：

- 不把 substance category、drug name、detox need、insurance, SUD status、mental health status、location + treatment intent 写入 URL、UTM、subid、event name、pixel parameter 或 call tracking label。
- 对 lead form、chat、call recording、CRM、postback、webhook、email、SMS、analytics、session replay、ad platform upload 建 tracking inventory。
- Enhanced conversions、offline conversion import、Customer Match 只使用允许字段，不上传 SUD/PHI/Part 2 语境信息。
- Call recording 必须有 disclosure、consent、access control 和 retention。
- Buyer handoff 必须说明数据用途、分享对象、retention、revocation / opt-out / deletion 路径。

系统默认将 SUD lead 字段标为高敏，要求更短 retention、更严格访问和更少共享。

## 8. Patient Brokering、Kickback、Travel Incentive 和 Ethical Referral 风险

高风险行为：

- 以现金、礼品、旅行、房租、免费住宿、保险报销等诱导用户选择特定 treatment center。
- Call center 或 lead generator 按入院、保险账单、尿检或治疗天数收取未披露回扣。
- 用虚假保险福利、虚假 “free treatment”、虚假 “covered 100%” 诱导入院。
- 反复转送患者到不同 facility / sober living / lab testing 以产生账单。
- 隐藏 affiliate / referral / ownership relationship。

系统应将这类 offer 标记为 reject，不进入创意生成、链接计划或投放任务。

## 9. Qualification Fields 和数据最小化

| 字段 | 用途 | 建议 |
| --- | --- | --- |
| location / state | license, facility availability, time zone | 必要，尽量粗粒度 |
| service need | detox, residential, IOP, OTP, MAT, counseling | 用 category，不收详细病史 |
| age bucket | adult/adolescent program fit | 不收完整 DOB |
| insurance/payment bucket | buyer eligibility | 不收保单号、SSN、card |
| immediate safety need | crisis routing | 用 safety prompt，不做广告回传 |
| preferred contact method | consent scope | 版本化保存 |
| substance category | level-of-care fit | 仅必要时粗分类，严格保护 |
| co-occurring need | dual diagnosis fit | 高敏，谨慎收集 |

不应默认收集：SSN、完整 DOB、保险卡照片、医疗记录、处方、详细用药、诊断、家庭成员病史、身份证件、银行卡、住址细节、法院/刑事记录。

## 10. Creative / Landing Claim Review

高风险 claim：

- “free rehab”“insurance covers everything”“same-day admission guaranteed”。
- “licensed doctors 24/7”“luxury treatment”“100% success rate”“cure addiction”。
- “near me”但没有当地 facility 或真实服务范围。
- “official helpline”“SAMHSA-approved”“government program”但无真实关系。
- “MAT available”“methadone/buprenorphine treatment”但 provider scope / OTP certification 不匹配。

审核要求：

- 每个 facility、license、accreditation、level of care、insurance、availability、clinical staff、MAT/MOUD claim 都有 proof URL。
- 页面要说明 provider / referral / lead generator role、商业关系、隐私用途、crisis emergency guidance。
- 不把 recovery testimonial 写成典型结果或保证疗效。
- 不使用恐惧、羞辱、绝望或家属压力型文案。

## 11. Call Routing、Pay-per-call、Admissions 和 Buyer Acceptance

Addiction treatment 常见 call lead / admissions payout：

| Stage | 说明 | 风险 |
| --- | --- | --- |
| call click / connected | 用户接通 | duration 不等于 qualified |
| qualified call | 基本地理/服务/consent 通过 | clinical fit 未确认 |
| admissions consult | 与 buyer/admissions 通话 | sales pressure risk |
| clinical assessment | 评估 level of care | 需专业人员 |
| insurance verification | payer/payment fit | sensitive data |
| pre-admission | 计划入院 / transport | patient brokering risk |
| arrived / admitted | 到院 / 入院 | still not paid |
| treatment started | 开始治疗 | billing / retention |
| paid / claim approved | 可收款 | clawback / complaint |

状态机：

```text
lead_submit_or_call
  -> consent_privacy_pass
  -> crisis_triage_pass
  -> provider_scope_match
  -> admissions_contact
  -> clinical_assessment
  -> insurance_or_payment_verified
  -> pre_admission
  -> arrived_or_admitted
  -> treatment_started
  -> approved_paid_after_clawback
```

不能把 call duration、admissions call、insurance verification 或 pre-admission 自动当成 paid treatment value。

## 12. Buyer Acceptance、Reject Reason 和 Payment Risk

常见 reject reason：

| Reject reason | 解释 | 对投放的动作 |
| --- | --- | --- |
| no_certification | 缺 Google / LegitScript / provider evidence | 停投 |
| out_of_scope | 不属于 buyer level of care | query / landing 修正 |
| bad_geo | 州/地区不服务 | geo 调整 |
| insurance_not_accepted | payer 不匹配 | 页面披露和预筛 |
| no_payment_fit | self-pay / financing 不匹配 | 预算和支付说明 |
| medical_acuity_too_high | 需要 emergency / hospital | crisis SOP |
| underage_no_program | 年龄不匹配 | age bucket / routing |
| duplicate | 重复 lead / call | suppression |
| unreachable | 联系不上 | consent / speed-to-lead |
| no_show_or_no_arrival | 未到院 | source / reminder review |
| patient_brokering_risk | referral/payment 不透明 | reject |
| privacy_complaint | 数据用途投诉 | 停投和事故复盘 |

Buyer terms 必须包含 paid definition、return/clawback window、complaint handling、allowed sources、call recording、data sharing、patient brokering warranty 和 privacy obligations。

## 13. Consent、TCPA、CAN-SPAM、DNC 和 Sensitive Contact

联系策略：

- Call/text/email consent 要说明 who contacts、for what treatment/referral purpose、whether shared with providers、how to opt out。
- DNC、unsubscribe、STOP reply、revocation 和 suppression 要同步到 buyer。
- 不群发 “urgent rehab admission” 或 shame/fear-based remarketing。
- 对家属提交 lead，要区分 patient consent、family contact 和 emergency resource。
- Call recording、CRM notes、chat transcript 都按高敏 health/SUD data 管理。

系统不做自动外呼、短信群发、绕 DNC、补 consent 或伪造联系记录。

## 14. Offline Value Mapping

Conversion action 建议：

| Stage | 是否建议 primary | 原因 |
| --- | --- | --- |
| page view / call click | no | 只是兴趣 |
| form submit / call connected | no / secondary | 高噪音、高敏 |
| qualified call | secondary | 早期质量 |
| admissions consult | secondary | 未确认 clinical fit |
| clinical assessment completed | primary candidate | 更接近服务匹配 |
| insurance/payment verified | primary candidate | 更接近 paid |
| arrived / admitted | primary candidate | 接近 buyer value |
| treatment started | primary | 更接近收入 |
| paid / claim approved after clawback | primary | 最接近利润 |

保守权重：

```text
lead_or_call = 0.02
qualified_call = 0.08
admissions_consult = 0.15
clinical_assessment = 0.30
insurance_verified = 0.45
admitted = 0.65
treatment_started = 0.85
paid_after_clawback = 1.00
```

权重必须按 facility、level of care、payer、geo、source 和 complaint/clawback 窗口校准。

## 15. Addiction Lead Quality Score

建议评分：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| Certification / license fit | 25 | Google / LegitScript / state / OTP / provider evidence |
| Privacy and Part 2 controls | 20 | SUD data、tracking、call recording、sharing |
| Crisis and ethical routing | 15 | emergency / 988 / SAMHSA / no sales pressure |
| Clinical and payment fit | 15 | level of care、insurance/payment、acuity |
| Claim proof | 10 | license、availability、insurance、MAT/MOUD、success claim |
| Offline value quality | 10 | assessment、admitted、started、paid |
| Source quality | 5 | complaint、duplicate、invalid traffic |

```text
addiction_lead_quality_score =
  certification_license_fit * 0.25
  + privacy_part2_controls * 0.20
  + crisis_ethical_routing * 0.15
  + clinical_payment_fit * 0.15
  + claim_proof * 0.10
  + offline_value_quality * 0.10
  + source_quality * 0.05
```

低于 85 不扩量；低于 75 只允许研究；出现 no certification、patient brokering、fake helpline、privacy leakage、crisis mishandling 或 kickback signal 时暂停。

## 16. 系统落地

本系统当前完成的是知识、审核和设计形态：

- `/knowledge/addiction_treatment_leads` 展示本手册。
- `/sources` 保存 Google、LegitScript、SAMHSA、HHS、CDC、state licensing 和 patient brokering 来源。
- `/risk-audits` 记录 certification、provider license、Part 2、HIPAA tracking、crisis routing、patient brokering、claim proof、admissions stage、paid definition。
- `/offers` 保存垂类、目标 URL、tracking URL、policy notes、creative angles。
- `/calculators` 使用更低 safety factor 和更高 policy score 要求评估是否可测。
- `/metrics/import` 允许导入 assessment、verified、admitted、started、paid after clawback，不把 call duration 默认当收入。

后续如果要实体表，应优先建：

| 表 | 用途 |
| --- | --- |
| `addiction_offer_profiles` | service type、provider role、certification、paid definition |
| `addiction_provider_refs` | license、LegitScript、accreditation、OTP、state source URL |
| `addiction_privacy_reviews` | Part 2、HIPAA tracking、call recording、sharing |
| `addiction_claim_reviews` | facility、level-of-care、insurance、MAT/MOUD、availability proof |
| `addiction_admissions_events` | call、assessment、verification、admitted、started、paid |
| `addiction_reject_reason_maps` | buyer reject、patient brokering、privacy complaint、clinical fit |
| `addiction_offline_value_maps` | stage、weight、Google Ads conversion mapping |

## 17. ADXKit 对应点和完成形态

| ADXKit 类能力 | Addiction treatment lead 安全完成形态 |
| --- | --- |
| Offer 管理 | 增加 provider role、certification、license、level of care、paid definition |
| 创意生成 | 生成 angle 前先做 helpline、insurance、license、clinical claim redline |
| 自动优化 | 基于 assessment/admitted/started/paid 和 privacy/complaint，不基于 call duration |
| 自动投放 | 只产出人工审核的结构、CSV、任务，不做 Cookie 后台操作 |
| 换链接 | 只做真实 Final URL 变更 QA，不做 mental health 泛页绕 addiction policy |
| 来源库 | 保存 Google/LegitScript/SAMHSA/HHS/CDC/state licensing 等来源和摘要 |
| 风险审计 | 对 certification、Part 2、patient brokering、crisis routing、claim proof、paid definition 建审计项 |

## 18. QA 清单

- 是否确认 provider / call center / lead generator / referral agency 角色？
- 是否确认 Google Ads addiction services / LegitScript certification 是否适用？
- 是否有 provider license、state source、facility address、level of care 和 clinical scope 证据？
- 是否有 crisis / emergency / 988 / SAMHSA resource handling，不冒充官方 hotline？
- 是否没有 patient brokering、kickback、travel/rent/gift incentive 或隐藏 referral fee？
- 是否不收 SSN、保险卡照片、KYC、详细病史、处方、身份证、银行卡等不必要高敏数据？
- 是否不把 SUD/PHI/Part 2 信息写入 URL、event、subid、pixel、postback？
- 是否每个 insurance、free treatment、same-day admission、MAT/MOUD、success/luxury claim 都有 proof URL？
- 是否拆开 call、assessment、insurance verified、admitted、started、paid after clawback？
- 是否不使用 Ads Cookie 登录、不绕 2FA、不刷量、不用代理/指纹规避、不做 cloaking、不为规避封禁换号？

## 19. 信息来源 URL

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑 addiction services certification、healthcare policy 和 restricted medical content 边界 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑 addiction、health、sensitive interest 和 remarketing / audience 边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 facility identity、insurance、official relationship、availability 和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| LegitScript, Addiction Treatment Certification Process | https://www.legitscript.com/certification/addiction-treatment-certification/addiction-treatment-certification-process/ | 支撑 addiction treatment advertising certification、provider/referral scope 和 platform trust |
| LegitScript, Addiction Treatment Certification FAQ | https://www.legitscript.com/service/certification/addiction-treatment/addiction-treatment-certification-faq/ | 支撑哪些服务/lead generator/referral agency 可能进入 certification 范围 |
| SAMHSA, Find Substance Use Disorder Treatment | https://www.samhsa.gov/substance-use/treatment/find-treatment/ | 支撑 official treatment locator、treatment options 和 public resource |
| FindTreatment.gov | https://findtreatment.gov/locator | 支撑 treatment facility lookup 和 official SAMHSA locator |
| SAMHSA, Find Help | https://www.samhsa.gov/find-help | 支撑 National Helpline、crisis / treatment support 和官方资源 |
| SAMHSA, Opioid Treatment Program Directory | https://www.samhsa.gov/find-help/locators/opioid-treatment-program-directory | 支撑 OTP certification / directory 和 provider verification |
| SAMHSA, Become an Opioid Treatment Program | https://www.samhsa.gov/substance-use/treatment/opioid-treatment-program/become-otp | 支撑 OTP certification、42 CFR Part 8 和 accreditation 语境 |
| HHS, Understanding Confidentiality of SUD Patient Records / Part 2 | https://www.hhs.gov/hipaa/for-professionals/special-topics/hipaa-part-2/index.html | 支撑 42 CFR Part 2、SUD patient record confidentiality 和 complaint path |
| HHS, Fact Sheet 42 CFR Part 2 Final Rule | https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html | 支撑 2024 Part 2 final rule 和 HIPAA alignment |
| HHS OCR, HIPAA Privacy Rule Marketing | https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/marketing/index.html | 支撑 PHI marketing、authorization 和 treatment communication boundary |
| HHS OCR, Use of Online Tracking Technologies | https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html | 支撑医疗页面 pixel、analytics、tracking tech 和 PHI 泄露风险 |
| HHS / FTC, Collecting, Using, or Sharing Consumer Health Information? | https://www.hhs.gov/hipaa/for-professionals/special-topics/hipaa-ftc-act/index.html | 支撑 HIPAA / FTC Act、health data claims 和 deceptive authorization 风险 |
| CDC, Treatment of Opioid Use Disorder | https://www.cdc.gov/overdose-prevention/treatment/opioid-use-disorder.html | 支撑 OUD evidence-based treatment、MOUD 和 treatment referral 语境 |
| CDC, Opioid Use Disorder: Treating | https://www.cdc.gov/overdose-prevention/hcp/clinical-care/opioid-use-disorder-treating.html | 支撑 clinician treatment、arrange care 和 evidence-based OUD care |
| SAMHSA, ASAM National Practice Guideline for OUD | https://www.samhsa.gov/resource/ebp/asam-national-practice-guideline-treatment-opioid-use-disorder | 支撑 OUD guideline 和 evidence-based practice 语境 |
| California DHCS, Licensing and Certification Division | https://www.dhcs.ca.gov/providers-partners/licensing-and-certification-division/ | 支撑 state provider licensing / certification 语境 |
| Florida Statutes 817.505, Patient brokering prohibited | https://www.flsenate.gov/Laws/Statutes/2024/0817.505 | 支撑 patient brokering、kickback 和 referral payment 风险 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
