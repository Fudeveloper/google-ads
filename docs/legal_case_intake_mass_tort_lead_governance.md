# Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / Pay-per-call / Appointment / Ping/Post 套利里，Legal Lead、Personal Injury Lead、Mass Tort Lead、Case Intake、Attorney Consultation Lead 为什么是高 payout、高资格门槛、高伦理和投诉风险的垂类。它承接 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)、[Lead Form、电话线索、Call Tracking 与 TCPA 风险手册](lead_form_call_tracking_tcpa_compliance.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)、[Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md)、[Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](pay_per_call_buyer_routing_duration_payout_governance.md)、[Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md) 和 [敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)，重点回答：法律 lead 的 practice area、jurisdiction、case type、incident date、injury / damages、representation status、attorney / firm / intake center / lead generator 边界、lawyer advertising、solicitation、confidentiality、buyer acceptance、retainer status、offline value mapping 和 Google Ads 信号应该如何治理。

本文不是法律意见，也不提供伪造案件、伪造事故、伪造伤害、冒充律师/律所/法院/政府、未经授权法律建议、规避律师广告规则、隐藏 lead generator 身份、自动外呼、短信群发、补电话、伪造 signed retainer、使用 Ads Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做行业知识、字段最小化、资格口径、来源 URL、buyer terms、consent/disclosure、claim review、case status、审计、任务和人工审批。

## 1. 为什么 Legal Lead 是高 payout 高拒付垂类

Legal lead 的 payout 高，是因为一个合格案件可能带来高额 attorney fee、contingency fee、settlement、class / mass tort referral fee 或长期 case value。但用户提交表单到律所真正愿意收案之间，存在多层筛选：

```text
search intent
  -> landing / intake form / call
  -> consent and disclosure
  -> intake qualified
  -> conflict / jurisdiction / practice fit
  -> attorney review
  -> consultation booked / completed
  -> retainer signed
  -> case accepted / filed / active
  -> fee event / paid revenue
```

常见亏损路径：

- 用户提交很多，但事故地点、诉讼时效、injury severity、medical treatment、damages、liability、defendant type 或 state 不符合 buyer。
- 用户已经有律师，或者案件存在 conflict / duplicate / non-compete / prior representation。
- Mass tort 页面把“你可能有资格”写成“你一定能获得赔偿”，引发投诉和拒登。
- Intake center 把电话时长、booked consultation 或 attorney review 当 paid revenue，实际律所只按 signed retainer 或 accepted case 付款。
- 广告和落地页暗示 official court、government program、guaranteed compensation、no fee unless win 但未说明条件。
- 敏感 legal issue 被用于再营销、受众名单或个性化文案，造成隐私和政策风险。

法律 lead 的核心不是“多拿案件表单”，而是把 case qualification、attorney review、retainer、paid event、consent、disclosure 和投诉复盘连接起来。

## 2. 原理解释：Legal Lead 是案件资格、律师边界和信任的交接

法律 lead 与普通咨询 lead 的差异在于：用户可能披露敏感事实，并期待法律帮助。即使系统只是 lead generator，也要把“信息收集、转交、初筛、法律建议、代理关系、保密义务”分清楚。

| 交接 | 说明 | 失败后果 |
| --- | --- | --- |
| Intent handoff | 用户想咨询某个 legal issue | 低意图、错误 practice area |
| Case qualification | 地区、案件类型、日期、伤害、证据、被告和 representation status | buyer reject、低 signed rate |
| Trust handoff | 用户知道谁在收集信息、谁会联系、是否已形成律师客户关系 | 投诉、bar advertising risk |
| Attorney review | 合格 lead 进入律师或律所判断 | signed retainer 延迟、冲突检查 |
| Revenue handoff | 收入口径从 submitted 到 retainer/case accepted/paid fee | accepted 当 paid，扩量误判 |

建议用以下公式理解法律 lead 净值：

```text
effective_legal_lead_value =
  headline_payout
  * jurisdiction_fit
  * case_type_fit
  * intake_qualified_rate
  * attorney_review_pass_rate
  * consultation_or_retainer_rate
  * paid_rate
  - conflict_risk
  - complaint_risk
  - return_or_scrub_reserve
  - payment_lag_cost
```

Legal lead 不适合只按 submitted CVR 扩量。真正的单位经济要等 case intake 和 buyer feedback 成熟后判断。

## 3. Practice Area / Case Type 地图

| Subvertical | 用户意图 | 典型资格字段 | 主要风险 |
| --- | --- | --- | --- |
| Personal Injury / Auto Accident | 事故赔偿、受伤咨询 | accident state/date、injury severity、medical treatment、fault、insurance、representation | 夸大赔偿、诉讼时效、已有律师 |
| Mass Tort / Product Liability | 药品、医疗器械、产品伤害 | product/drug exposure、diagnosis/injury、date range、state、proof | “一定赔偿”、过期 campaign、医疗敏感数据 |
| Workers' Compensation | 工伤权益 | work state、injury date、employer status、medical treatment、representation | 州规则差异、雇佣/医疗敏感 |
| Social Security Disability | disability benefits 咨询 | application/denial status、work history bucket、condition category | 政府关系误导、医疗敏感 |
| Immigration | 签证、身份、移民咨询 | country/language、case type、deadline、current status bucket | 冒充政府、身份敏感、UPL |
| Criminal / DUI | 刑事或 DUI 咨询 | charge type、court date、jurisdiction、representation | 紧急 solicitation、保密和身份敏感 |
| Bankruptcy / Tax Debt | 债务、破产、税务 | state、debt range、asset/income bucket、deadline | 金融/法律双重敏感 |
| Family Law | divorce、custody、support | state、case stage、court date、children flag bucket | 高敏感、冲突、投诉 |
| Employment / Labor | wrongful termination、discrimination、wage claim | state、event date、employer size bucket、claim type | 就业敏感、HEC / discrimination claim |
| Medical Malpractice | 医疗事故咨询 | state、incident date、injury severity、provider type | 医疗敏感、证据和时效复杂 |

不要把 personal injury、mass tort、immigration、criminal、family 和 bankruptcy 放进同一个 landing、form、buyer terms 或 conversion action。每个 practice area 的资格字段、拒收原因和收入口径都不同。

## 4. 资格字段和数据最小化

法律 lead 字段要“够判断资格，但不收完整案情”：

| 字段 | 用途 | 最小化做法 | 风险提示 |
| --- | --- | --- | --- |
| state / jurisdiction | 匹配律师执业地区和案件地点 | 州/县优先，地址只在必要系统保存 | wrong jurisdiction 高频拒收 |
| practice area / case type | 匹配 buyer / firm | 枚举 | 错 practice area 会污染 routing |
| incident / diagnosis / charge date bucket | 时效和 campaign eligibility | 日期范围或 month/year | 不提供诉讼时效判断 |
| injury / damages severity bucket | 初筛案件价值 | 粗分层 | 避免详细医疗记录 |
| medical treatment flag | PI / malpractice / mass tort 初筛 | yes/no/bucket | 医疗敏感 |
| fault / liability indicators | 事故责任初筛 | 枚举，不做法律结论 | 不能给法律判断 |
| representation status | 是否已有律师 | yes/no/unknown | 避免干扰既有代理关系 |
| court date / deadline bucket | 紧急程度 | 日期范围 | 不承诺能处理所有 deadline |
| evidence / documentation flag | 是否有 police report、photos、notice 等 | yes/no/bucket | 不上传原始文件到套利系统 |
| contact channels | phone、SMS、email | 明确 opt-in scope | TCPA/DNC/opt-out |
| consent / disclosure version | 可联系、可转交证据 | version/hash/certificate ref | 争议证据核心 |

不要在广告套利工作台里保存完整病历、警察报告、法院文件、身份证件、完整住址、完整 immigration status 文件、犯罪记录细节、未加密录音或完整法律叙述。需要细节时，应由合规 intake / CRM / 律所系统在受控权限下处理。

## 5. Eligibility、Reject Reason 和 Buyer Acceptance

法律 lead 的状态机：

```text
submitted
  -> validation_passed
  -> intake_qualified
  -> buyer_accepted
  -> conflict_check_pending
  -> attorney_reviewed
  -> consultation_booked
  -> consultation_completed
  -> retainer_signed
  -> case_accepted
  -> active_case / filed / fee_event
  -> paid / returned / conflict / complaint
```

常见 reject reason：

| Reject reason | 含义 | 修复动作 |
| --- | --- | --- |
| wrong jurisdiction | 不在服务州/县/法院 | geo gating、routing rule |
| wrong practice area | 用户问题不属于 buyer practice | keyword/query/landing 分流 |
| incident too old | 可能超出 buyer 接收窗口 | 日期 bucket 前置，不给法律结论 |
| low injury / no damages | 案件价值不足 | qualification copy、case type 分层 |
| no medical treatment | PI / malpractice 常见拒收 | 字段前置、素材承诺修正 |
| already represented | 已有律师 | 停止转售或特殊流程 |
| conflict / adverse party | 律所有利益冲突 | buyer feedback 和 evidence |
| duplicate / prior lead | 已收到或窗口内重复 | hash 去重、buyer duplicate window |
| unreachable / no-show | 无法联系或未到咨询 | speed-to-lead 和 appointment QA |
| no consent / bad disclosure | 用户未授权联系或转交 | consent proof、buyer disclosure |
| misleading claim complaint | 赔偿、官方关系、胜诉承诺误导 | claim review、source quarantine |

`intake qualified`、`buyer accepted` 或 `consultation booked` 都不是最终收入。很多法律 buyer 只按 signed retainer、case accepted 或更晚的 fee event 付款。

## 6. Attorney、Law Firm、Intake Center、Lead Generator 和 Referral 边界

Legal lead 页面必须清楚区分角色：

| 角色 | 可以表达 | 不应表达 |
| --- | --- | --- |
| Lead generator | 收集咨询请求并转交给律师/律所 | 冒充律所、律师协会、法院、政府 |
| Intake center | 接听、初筛、安排咨询 | 提供未授权法律建议或承诺结果 |
| Attorney / law firm | 在执业范围内提供法律服务 | 未授权州不得暗示可服务 |
| Referral service | 按规则介绍律师 | 隐藏 referral fee、排序和筛选逻辑 |
| Advertising network / publisher | 提供流量或内容 | 暗示律师推荐或法律评价 |

系统要保存：

```text
entity_name
role_type
firm_or_attorney_ref
licensed_jurisdictions
practice_area_scope
referral_or_lead_gen_disclosure
compensation_disclosure
attorney_client_relationship_disclaimer
reviewer
source_url
```

原则：

- 不暗示用户提交表单就已经形成 attorney-client relationship。
- 不由非律师或未经授权人员提供个案法律建议。
- Lead generator / referral / intake 的补偿和排序逻辑要可审计。
- 对 prospective client 信息要按最小必要、访问控制和保留期处理。
- 不用 buyer payout 伪装成“最佳律师推荐”的唯一依据。

## 7. Lawyer Advertising、Solicitation、Testimonials 和 Review 风险

法律广告需要特别审查：

| 风险 | 示例 | 治理 |
| --- | --- | --- |
| False or misleading communication | “Guaranteed settlement”、“Best injury lawyer” | 禁止无法证明或绝对化 claim |
| Solicitation | 对特定事故/案件人群直接施压联系 | 审查 contact cadence、来源和用户主动意图 |
| Testimonials / results | “We got $1M for clients like you” | 标注条件、避免暗示相同结果 |
| Specialty / expertise | “Certified specialist” | 只有可证明资格才写 |
| Fee claim | “No fee unless we win” | 说明条件、费用和成本责任 |
| Government / court | “Official legal aid / court help” | 明确第三方身份，不冒充官方 |
| Comparative ranking | “Top rated / best match” | 保存排序依据和来源 |

广告、landing、call script、intake question 和 buyer handoff 必须一致。不要让广告承诺免费评估，但电话里强推收费服务或未披露转交给多个律所。

## 8. Mass Tort、Class Action、Settlement 和 Government/Court Claim 风险

Mass tort / class action / settlement 类页面常见风险：

- 把“可能符合”写成“你一定有资格”。
- 用 settlement amount、deadline、drug/device name 或 diagnosis 制造恐慌。
- 使用 government、court、official settlement、claims administrator 等词制造官方关系。
- 长期保留过期 campaign、过期 defendant、过期 filing deadline 或过期 eligibility window。
- 收集详细医疗/处方/诊断资料但无必要 disclosure 和访问控制。

治理要求：

```text
campaign_name
case_type
defendant_or_product
eligibility_window
incident_or_exposure_date_bucket
injury_or_diagnosis_bucket
official_source_url
page_update_date
attorney_or_firm_review
claim_review_decision
```

如果页面讨论 settlement、deadline、class action 或 official claim process，必须引用官方 court / settlement administrator / firm review / reliable source，并说明第三方身份。

## 9. Call、Form、Appointment、Pay-per-call 和 Retainer

法律 lead 常见交付形态：

| 形态 | 价值来源 | 治理重点 |
| --- | --- | --- |
| Form CPL | 用户提交咨询请求 | qualification fields、consent、representation status |
| Call lead | 用户主动来电 | recording disclosure、intake disposition、sensitive info |
| Pay-per-call | 按 qualified duration 或 intake outcome 计费 | duration 只是代理，必须看 case fit |
| Appointment | booked consultation | booked 不等于 completed / retained |
| Signed retainer | 用户与律所签约 | 更接近 buyer value |
| Case accepted / filed | 律所正式收案 | 适合作为成熟 value signal |

Routing value：

```text
legal_routing_value =
  payout
  * jurisdiction_fit
  * practice_area_fit
  * intake_qualified_rate
  * attorney_review_pass_rate
  * retainer_rate
  * paid_rate
  - conflict_risk
  - complaint_risk
  - missed_call_cost
```

如果 buyer closed、attorney unavailable、conflict rate 高、no-show 高或 signed retainer 延迟异常，应先限量和修复 intake，而不是让 Google Ads 继续按 submitted lead 学习。

## 10. Consent、TCPA、DNC、Recording 和 Confidentiality

法律 lead 的 consent proof 至少保存：

```text
lead_id
form_version
consent_text_hash
buyer_disclosure_version
attorney_client_disclaimer_version
contact_channels_allowed
submit_timestamp
timezone
page_snapshot_hash
privacy_policy_version
suppression_check_status
source_url
```

电话和录音治理：

- call recording notice 要按地区和 buyer terms 审核。
- 录音、transcript、case notes 可能包含敏感 legal / medical / identity facts，默认不进入广告套利系统。
- 用户 opt-out、DNC、撤回同意或投诉后，停止对应渠道并同步 suppression。
- Aged legal lead 不应用旧 consent 无限转售或重新触达。
- 不使用自动拨号、机器人语音或短信群发绕过 consent、DNC、TCPA 或 professional conduct 要求。

Confidentiality 角度：

- 即使尚未形成 attorney-client relationship，prospective client 信息也要谨慎处理。
- 对 buyer、intake vendor、广告团队和 AI prompt 的访问范围做最小化。
- 不把完整案情、姓名、电话、法院文件、病历、犯罪或移民细节写入 URL、subid、log 或 prompt。

## 11. Google Ads 政策和 Local Services Ads 边界

法律 lead 常见 Google Ads 风险：

| 政策面 | 风险 | 治理 |
| --- | --- | --- |
| Personalized advertising | 法律问题、犯罪、身份、健康、财务困境等敏感状态 | 不用敏感困境做受众和文案暗示 |
| Misrepresentation | 主体、官方关系、结果、费用、资格不清 | 页面 disclosure、entity、role、fee claim 清晰 |
| Destination requirements | 广告、Final URL、landing、表单和实际体验一致 | 不做 cloaking、隐藏跳转或审核页/用户页不一致 |
| Local Services Ads / Google Screened | 律师和本地服务可能涉及筛查、license、reviews | 不把 LSA lead credit 口径当普通 CPL |
| Customer data policies | 导入 lead / enhanced conversions 时需要同意和安全处理 | 使用 hash、最小化和 consent evidence |

Google Ads 不是案件资格判断系统。`lead form submit`、`call click`、`call duration` 都只是浅层信号，必须用 intake qualified、attorney reviewed、retainer signed、case accepted 和 paid feedback 校准。

## 12. Creative / Landing Claim Review

| Claim | 高风险写法 | 安全写法方向 |
| --- | --- | --- |
| Outcome | “Guaranteed compensation” | “Discuss eligibility factors with a qualified attorney” |
| Amount | “Get up to $500,000” | “Past results do not guarantee future outcomes” |
| Official | “Official court claim site” | “Independent information / attorney advertising disclosure” |
| Fee | “100% free lawyer” | “Consultation availability and fees vary; review terms” |
| Urgency | “Last chance today” | “Deadlines vary by jurisdiction and facts” |
| Specialty | “Certified expert” | Only if verifiable and jurisdictionally valid |
| Mass tort | “Everyone who used X qualifies” | “Eligibility depends on exposure, injury, dates and other facts” |
| Criminal / immigration | “We can stop deportation/jail” | “Options depend on individual facts and law” |

Landing page 必备检查：

- entity、role、attorney advertising / lead generator disclosure、privacy policy、contact method 清楚。
- 不制造法院、政府、legal aid、bar association 或 settlement administrator 官方关系。
- 不承诺胜诉、赔偿金额、移民结果、刑事结果或债务/税务结果。
- 表单字段用 bucket；不收完整案情和高敏感文件。
- 用户看到的页面和审核/爬虫看到的页面一致。

## 13. Offline Value Mapping

法律 lead 建议分层：

| Stage | Ads 信号建议 | 说明 |
| --- | --- | --- |
| submitted lead | secondary / diagnostic | 只看漏斗，不直接扩量 |
| validation_passed | diagnostic | 格式和基础字段通过 |
| intake_qualified | middle quality | 初筛符合 practice/jurisdiction |
| buyer_accepted | middle quality | 仍可能 conflict/return |
| attorney_reviewed | strong | 律师或律所完成初评 |
| consultation_booked | strong but not final | booked 不等于 completed |
| consultation_completed | stronger | 用户完成咨询 |
| retainer_signed | primary candidate | 更接近收入 |
| case_accepted / active | primary candidate | 成熟价值 |
| fee_event / paid invoice | final calibration | 用于最终 value |
| rejected / conflict / complaint | internal negative | 不回传正向，进入 risk audit |

成熟投放建议用 conservative staged value：

```text
submitted_value < intake_qualified_value < attorney_reviewed_value < retainer_value < paid_value
```

不要把电话时长、预约 booked、intake qualified 或 buyer accepted 默认当 paid legal revenue。

## 14. Legal Lead Quality Score

建议评分：

```text
legal_lead_quality_score =
  jurisdiction_fit             15
  practice_area_fit            15
  case_qualification_fit       18
  consent_disclosure_quality   12
  attorney_review_pass_rate    12
  retainer_or_case_accept_rate 15
  complaint_conflict_risk       8
  source_claim_integrity        5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可按 mature retained / paid value 小幅扩量 |
| 70-84 | 正常测试，继续收集 attorney feedback |
| 55-69 | 限量，查 reject reason、source、claim 和 intake |
| 35-54 | 暂停扩量，修 jurisdiction、case filter、disclosure 或 buyer |
| 0-34 | 停 source / buyer / landing，开风险审计 |

评分必须按 practice area、state/jurisdiction、buyer/firm、lead age、source、creative angle、form version、intake vendor 和 hour 拆分。

## 15. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 ABA/Google/FTC/FCC/DNC 来源 | `/sources` |
| 记录 legal claim、official relationship、attorney disclosure 风险 | `/risk-audits` |
| 用 policy_score、source_score 和 safe CPC 做小预算测算 | `/calculators` |
| 保存 Offer 垂类、国家、policy notes、tracking URL | `/offers` |
| 生成低风险创意和人工审核投放草稿 | Offer 详情页、`/campaigns` |
| 导入 intake qualified、retainer、case accepted、paid revenue | `/metrics/import` |
| 生成暂停、限量、查 claim、查 buyer feedback 建议 | `/optimization` |
| 保存任务和审批痕迹 | `/tasks`、`/logs` |

后续可扩展表：

```text
legal_vertical_profiles
legal_qualification_fields
legal_case_type_rules
legal_attorney_buyer_terms
legal_intake_events
legal_attorney_review_events
legal_reject_reason_maps
legal_claim_reviews
legal_referral_disclosure_versions
legal_conflict_check_snapshots
legal_offline_value_maps
legal_quality_daily
```

关键字段：

```text
practice_area
state_or_jurisdiction
case_type
incident_date_bucket
injury_or_damages_bucket
representation_status
buyer_or_firm_id
buyer_terms_version
disclosure_version
consent_version
attorney_review_status
retainer_status
reject_reason
offline_stage
paid_value
source_url
reviewer
decision
```

## 16. ADXKit 对应点和完成形态

| ADXKit 能力 | Legal lead 场景完成形态 | 不交付内容 |
| --- | --- | --- |
| Offer 管理 | practice area、jurisdiction、buyer terms、retainer/paid definition、disclosure 来源 | 冒充律师、律所、法院、政府或法律援助 |
| 落地页采集 | 抽取赔偿、胜诉、官方、fee、deadline、testimonial 和 mass tort claim | cloaking、隐藏真实 firm/buyer |
| AI 创意生成 | 生成“了解资格因素、咨询问题清单”类低风险素材并进入 claim review | 保证胜诉、保证赔偿、恐吓式法律文案 |
| 投放草稿 | 按 practice area / jurisdiction / buyer fit 拆 campaign/ad group | Cookie 后台自动投放或绕过认证 |
| 换链接 | 只做同主题、同披露、同资格条件、已审核 URL 轮换 | 用换链跳到未披露律所或双版本页面 |
| 任务中心 | disclosure 更新、claim review、buyer feedback 导入、source quarantine | 自动外呼、短信轰炸、伪造案件或补电话 |
| 来源库 | ABA、Google、FTC、FCC、DNC 来源可追踪 | 用营销博客替代律师规则或官方来源 |

完成口径：把法律 lead 的行业知识、案件资格、律师/lead generator 边界、广告 claim、buyer acceptance、retainer/paid value 和系统审计做完整；不做对抗平台、绕过登录、伪造案件、冒充律所或制造虚假流量。

## 17. QA 清单

上线前逐项检查：

- `practice_area` 是否明确：PI、mass tort、immigration、criminal、family、bankruptcy 等不能混用。
- 页面主体是否真实：attorney、law firm、lead generator、intake center、referral service 是否清楚。
- 是否说明提交表单不一定形成 attorney-client relationship。
- 是否避免法院、政府、legal aid、bar association、settlement administrator 官方关系误导。
- 是否避免 guaranteed win、guaranteed compensation、specific settlement amount、certified specialist、no fee unless win 等未限定 claim。
- jurisdiction、incident date、injury/damages、representation status 是否用最小必要字段。
- 是否避免收集完整案情、病历、法院文件、犯罪/移民细节或完整 PII。
- Consent 是否包含 contact channel、buyer disclosure、version/hash 和页面证据。
- Buyer terms 是否写明 intake qualified、attorney reviewed、consultation completed、retainer signed、case accepted、paid definition。
- Pay-per-call 是否保存 intake disposition，而不是只看 duration。
- Aged legal lead 是否与 fresh lead 分 conversion action、payout tier 和 attribution。
- Offline value 是否按 intake、attorney review、consultation、retainer、case accepted、paid 分层。
- Google Ads primary conversion 是否使用成熟、可收款、低投诉的事件。
- 不使用 Ads Cookie 后台操作、自动登录、cloaking、代理/指纹规避、补点击或封禁规避。

## 18. 信息来源 URL

| 来源 | URL | 用途 |
| --- | --- | --- |
| ABA Model Rule 7.1, Communications Concerning a Lawyer's Services | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communications_concerning_a_lawyers_services/ | 支撑法律服务广告不能 false or misleading |
| ABA Model Rule 7.2, Communications Concerning a Lawyer's Services: Specific Rules | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_2_communications_concerning_a_lawyers_services_specific_rules/ | 支撑律师广告、lead generator、推荐和联系方式披露边界 |
| ABA Model Rule 7.3, Solicitation of Clients | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_3_solicitation_of_clients/ | 支撑 solicitation、实时联系和压力式获取客户风险 |
| ABA Model Rule 1.18, Duties to Prospective Client | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_18_duties_to_prospective_client/ | 支撑 prospective client 信息和初次咨询资料处理 |
| ABA Model Rule 1.6, Confidentiality of Information | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_6_confidentiality_of_information/ | 支撑敏感案件信息、录音和访问控制边界 |
| ABA Model Rule 5.4, Professional Independence of a Lawyer | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_5_4_professional_independence_of_a_lawyer/ | 支撑非律师、fee sharing、referral 和 lead generator 边界 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑法律问题、身份、健康、财务困境等敏感状态的个性化广告边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑官方关系、费用、资格、结果和主体透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Policy, Unacceptable business practices | https://support.google.com/adspolicy/answer/6020954 | 支撑欺骗性法律服务、虚假资质和不可信业务模式审查 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Local Services Ads, How leads work | https://support.google.com/localservices/answer/7195435 | 支撑 LSA lead、charged lead、valid lead 和服务地区语境 |
| Google Local Services Ads, Google Screened | https://support.google.com/localservices/answer/9376651 | 支撑法律/专业服务筛查、license、reviews 和 Google Screened 语境 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、DNC、拒绝联系和记录治理 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | 支撑 testimonials、reviews、past results 和 material connection 披露 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
| FTC, Enforcement Policy Statement on Deceptively Formatted Advertisements | https://www.ftc.gov/legal-library/browse/commission-policy-statement-enforcement-policy-statement-deceptively-formatted-advertisements | 支撑 advertorial、伪装新闻/评测/公益法律信息的格式风险 |
| Legal Services Corporation, Find Legal Aid | https://www.lsc.gov/about-lsc/what-legal-aid/get-legal-help | 支撑不要冒充 legal aid、官方公益法律服务或政府援助 |
