# Insurance、Medicare / ACA 与 Final Expense Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / Pay-per-call / Appointment / Ping/Post 套利里，Insurance Lead、Medicare Lead、ACA / Marketplace Lead、Final Expense / Life Insurance Lead 为什么是高 payout、高政策风险、高拒付风险的垂类。它承接 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)、[Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)、[Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)、[Lead Freshness、Aged Lead 与 Recontact Window 治理手册](lead_freshness_aged_recontact_governance.md)、[Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](pay_per_call_buyer_routing_duration_payout_governance.md) 和 [敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)，重点回答：保险 lead 的资格字段、授权主体、开放注册、买方验收、拒收原因、合规 claim、电话/表单路由和 Google Ads 信号应该如何治理。

本文不是法律意见，也不提供未授权保险销售、冒充 Medicare / Marketplace / carrier、自动外呼、短信群发、补电话、伪造 lead、伪造 consent、伪造 licensed agent、隐藏 buyer disclosure、绕过 TCPA/DNC/TSR、使用 Ads Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做垂类知识、字段最小化、资格口径、来源 URL、证据链、buyer acceptance、reject reason、offline value mapping、审计、任务和人工审批。

## 1. 为什么 Insurance Lead 是高 payout 高拒付垂类

保险 lead 的 payout 往往高，是因为买方的下游价值高：一个 health plan、Medicare Advantage / supplement、life insurance 或 final expense policy 一旦成交，可能带来长期保费、续佣或高客单价服务机会。但套利团队不能把高 payout 直接当利润。保险 lead 的真实价值来自：

```text
consumer intent
  -> eligibility fit
  -> licensed / authorized sales path
  -> consent and disclosure proof
  -> contact / quote / application
  -> policy / enrollment / paid commission
  -> retention and complaint outcome
```

常见亏损路径：

- 表单提交很多，但用户不在可服务州、年龄段、coverage 类型或 enrollment window 内。
- 广告承诺“免费”“最高补贴”“官方 Medicare”或“保证省钱”，带来拒登、投诉和 buyer scrub。
- 买方只按 application started、policy issued、enrolled、paid premium 或 retained policy 付款，团队却按 submitted lead 扩量。
- Medicare / ACA 页面没有区分官方政府站点、licensed agent、broker、carrier 和第三方 lead generator。
- 电话达到 duration，但 buyer 判断 wrong plan、duplicate、already enrolled、existing customer、no consent 或 non-serviceable state。
- Fresh lead、aged lead、shared lead 和 recontact lead 混在同一优化信号里，导致 Google Ads 学到低意图用户。

保险 lead 的核心不是“收更多电话和表单”，而是把用户资格、授权链路、承诺边界、同意证据、买方验收和回款状态连成闭环。

## 2. 原理解释：保险 Lead 是资格、授权和信任的交接

普通 CPL 可以只问用户是否想咨询某个服务；保险 CPL 还要处理资格和授权。用户不是在买一个通用商品，而是在进入一个受监管的决策：计划类型、地区、年龄、收入、健康、现有 coverage、注册窗口和 licensed agent 都会影响用户能否被合法、准确、及时地服务。

保险 lead 的本质是三次交接：

| 交接 | 说明 | 失败后果 |
| --- | --- | --- |
| 意图交接 | 用户想比较、报价、咨询或注册 | 低意图 lead、误填、投诉 |
| 资格交接 | 用户的州、年龄、coverage、窗口和基本需求匹配 buyer | bad geo、age mismatch、wrong plan、no buyer |
| 授权交接 | 用户知道谁会联系、为何联系、通过什么渠道联系 | no consent、DNC/opt-out、TCPA/TSR 风险 |

这也是保险垂类不能用单一 CVR 优化的原因。一个很短的表单可能提高 submitted CVR，但会牺牲 eligibility、contact rate、buyer acceptance、paid rate 和投诉率。一个很长的表单可能提高质量，但也会降低流量转化并增加敏感数据处理风险。

建议用以下公式理解利润：

```text
effective_insurance_lead_value =
  headline_payout
  * eligibility_pass_rate
  * contact_rate
  * buyer_accept_rate
  * application_or_policy_rate
  * paid_rate
  - compliance_reserve
  - complaint_reserve
  - scrub_reserve
  - delayed_payment_cost
```

## 3. Subvertical 地图

保险 lead 不是一个垂类，而是一组差异很大的子垂类：

| Subvertical | 用户意图 | 典型资格字段 | 主要风险 |
| --- | --- | --- | --- |
| Health / ACA / Marketplace | 比较健康保险、检查补贴资格、开放注册 | 州、zip/county、household size、income range、current coverage、SEP/OEP | 冒充官方、补贴承诺、敏感属性、开放注册日期错误 |
| Medicare Advantage / Supplement / Part D | 比较 Medicare 计划、药物计划、补充保险 | 年龄/Medicare eligibility、zip/county、current Medicare status、plan type | CMS marketing、TPMO disclosure、官方关系误导、年龄定向边界 |
| Final Expense / Life Insurance | 寿险或丧葬费用保障咨询 | 年龄段、州、coverage amount range、tobacco/health range、beneficiary intent | 保证批准、无体检夸大、老年用户投诉、licensed producer |
| Auto Insurance | 车险报价比较 | 州、zip、vehicle range、current insured、driver count | 价格保证、虚假低价、敏感 financial targeting |
| Home / Renters Insurance | 房屋或租客保险报价 | 州、zip、property type、current insured | 价格/coverage 误导、房屋/信贷敏感用途 |
| Dental / Vision / Supplemental | 补充健康相关计划 | 州、coverage type、current coverage | 医疗/健康 claim、福利误导 |

套利团队需要先写 `vertical_profile`，不要把 Medicare、ACA、Final Expense 和 Auto Insurance 放在同一个 landing、同一套 consent、同一套 buyer terms 和同一个 conversion action 里。

## 4. 资格字段和数据最小化

保险 lead 的字段要服务于资格判断和 buyer routing，而不是越多越好。字段设计原则：

- 只收当前资格和 routing 必须字段。
- 用 range / bucket 替代细粒度敏感信息。
- 每个字段保存 purpose、required_by、reject_reason_prevented 和 retention。
- 表单展示要说明数据用途、联系主体和渠道。
- 不把完整 PII 写入 URL、subid、日志、prompt 或测试数据。

建议字段地图：

| 字段 | 用途 | 最小化做法 | 风险提示 |
| --- | --- | --- | --- |
| state / zip / county | 服务地区、计划可用性、buyer routing | zip 可以哈希或只在 CRM 保存 | wrong geo 是高频拒收原因 |
| age bucket / DOB eligibility | Medicare / life eligibility | 优先年龄段；DOB 只在必要时由合规系统保存 | 年龄是敏感/受保护属性相关字段 |
| coverage type | health、Medicare、life、auto、home | 枚举 | 用于分 buyer 和页面承诺 |
| current coverage | 是否已有保险、Medicare status | 枚举，不要问过多细节 | existing customer / already enrolled |
| household / income range | ACA subsidy context | range，不保存具体收入除非必要 | 不承诺补贴或低价 |
| tobacco / health range | life/final expense 初筛 | 粗分层，不收诊断细节 | 医疗敏感数据和歧视风险 |
| contact channels | phone、SMS、email | 明确 opt-in scope | TCPA/DNC/opt-out |
| consent / buyer disclosure | 证明可联系和可分享 | version/hash/certificate ref | 争议证据核心 |
| preferred time / language | 提高联系体验 | 枚举 | 与 buyer hours/dayparting 绑定 |

不要收集完整 SSN、完整 Medicare number、完整处方清单、诊断详情、精确收入证明、银行卡或支付信息来做广告套利 lead。需要这些信息时，应由合规的 carrier/broker/enrollment 系统在受控环境里处理。

## 5. Eligibility、Reject Reason 和 Buyer Acceptance

保险 buyer 的 acceptance 不是“表单能提交”。常见状态：

```text
submitted
  -> validation_passed
  -> eligibility_passed
  -> pinged / routed
  -> buyer_accepted
  -> contacted
  -> quoted / application_started
  -> enrolled / policy_issued
  -> approved / paid
  -> retained / chargeback_or_scrub
```

常见 reject reason：

| Reject reason | 含义 | 修复动作 |
| --- | --- | --- |
| bad state / county | buyer 不服务该地区或计划不可用 | geo gating、landing copy、routing rule |
| age mismatch | 不符合 Medicare/life 年龄 | 字段前置、页面文案修正 |
| wrong coverage type | 用户要 auto，送给 health buyer | intent 分流、query negative |
| outside enrollment window | 不在 OEP/SEP/AEP 或无 qualifying event | 官方日期表、seasonal budget |
| duplicate lead | 重复提交或已被 buyer 收过 | hash 去重、buyer duplicate window |
| existing customer / already enrolled | 老客户或已注册 | buyer terms、exclusion feedback |
| no consent / invalid consent | 同意文本、buyer disclosure 或证据不足 | consent version、certificate、page snapshot |
| unreachable / wrong phone | 联系失败 | validation、lead form UX、contact SLA |
| misleading claim complaint | 用户认为广告夸大、冒充官方或隐瞒限制 | claim review、landing audit、source quarantine |
| low intent / incentive | 用户为赠品或误导 CTA 提交 | creative angle、CTA、source quality |

系统必须保存 buyer 的原始反馈和 evidence URL。不要把 rejected、returned、duplicate、unreachable 或 complaint lead 回传为正向 primary conversion。

## 6. Licensed Agent、Broker、Carrier 和官方关系边界

保险 lead 页面必须清楚区分以下角色：

| 角色 | 可以表达 | 不应表达 |
| --- | --- | --- |
| Lead generator | 收集咨询请求并转交给合作方 | 冒充 carrier、政府、Marketplace、Medicare |
| Licensed agent / broker | 在授权州提供保险咨询或销售 | 暗示所有计划、所有 carrier 或官方代表身份 |
| Carrier | 保险公司或计划提供方 | 未授权不得使用商标和官方口吻 |
| Government / Marketplace / Medicare | 官方政府服务或信息 | 第三方页面不得制造官方隶属关系 |

上线前要保存：

```text
entity_name
role_type
license_or_authorization_ref
states_covered
carrier_relationship_scope
agent_or_broker_disclosure
official_relationship_claim
reviewer
source_url
```

对于 Medicare / ACA 页面，尤其要避免：

- 使用 official、government、Medicare-approved、Marketplace enrollment center 等可能误导官方关系的表达，除非确有授权且可证明。
- 用政府标识、相似域名或视觉元素制造官方站点印象。
- 暗示用户一定能获得补贴、省钱、通过或注册成功。
- 用“limited time”“last chance”等强紧迫感制造不准确压力。

## 7. Enrollment Window：Medicare / ACA / Final Expense

Insurance lead 的季节性不是普通流量波动，而是资格窗口变化。

| 垂类 | 窗口逻辑 | 投放治理 |
| --- | --- | --- |
| ACA / Marketplace | Open Enrollment、Special Enrollment Period、州差异 | 使用 HealthCare.gov 或州官方日期；页面显示年份和更新时间 |
| Medicare Advantage / Part D | Initial Enrollment、Annual Enrollment、Medicare Advantage Open Enrollment、Special Enrollment | 用 Medicare.gov / CMS 来源维护日期；不要错用旧年文案 |
| Medicare Supplement | 受 Medigap open enrollment、州规则和 underwriting 影响 | 不承诺无条件可买或最低价 |
| Final Expense / Life | 不依赖 OEP，但受年龄、健康、州和 underwriting 影响 | 不用开放注册话术误导 |
| Auto / Home | 季节性较弱，更多受续保周期和区域价格影响 | 不用健康/政府福利话术 |

广告预算、landing copy、buyer capacity、call center hours 和 conversion action 要跟窗口绑定。窗口前可以做 research / comparison / reminder 类内容，但不要让用户以为已经处在可注册窗口。

## 8. Call、Form、Appointment 和 Pay-per-call

保险 lead 常见交付形态：

| 形态 | 价值来源 | 治理重点 |
| --- | --- | --- |
| Form CPL | 用户提交咨询请求 | 字段最小化、consent、buyer acceptance、reject reason |
| Ping/Post | 多 buyer 报价或接收 | ping 最小化字段、buyer disclosure、exclusive/shared 标记 |
| Call lead | 用户主动来电 | call tracking、recording disclosure、qualified duration、buyer disposition |
| Pay-per-call | 按 qualified call / duration / disposition 计费 | duration 只是代理指标，必须看 paid outcome |
| Appointment | 预约 agent / broker 咨询 | booked 不等于 showed/paid，需 reminder consent |

Routing 不能只看最高 payout。保险场景的 routing value 应考虑：

```text
insurance_routing_value =
  payout
  * state_plan_fit
  * agent_availability
  * contact_or_answer_rate
  * buyer_accept_rate
  * application_or_policy_rate
  * paid_rate
  - complaint_risk
  - no_consent_risk
  - capacity_risk
```

如果 buyer closed、cap stale、no licensed agent available 或 enrollment window 不匹配，应先降预算、暂停 source 或改成信息型内容，而不是用 fallback 把用户送到未披露 buyer。

## 9. Consent、TCPA、DNC 和证据链

保险 lead 的 consent proof 是收款资产和投诉防线。至少保存：

```text
lead_id
form_version
consent_text_hash
buyer_disclosure_version
contact_channels_allowed
submit_timestamp
timezone
ip_hash / user_agent_hash if retained
certificate_provider / certificate_ref_hash
page_snapshot_hash
privacy_policy_version
suppression_check_status
source_url
```

治理原则：

- Consent 文案要清楚说明谁可能联系、通过什么渠道联系、联系目的是什么。
- 不能用预勾选、隐藏条款或笼统“合作伙伴”掩盖真实买方范围。
- 用户 opt-out、DNC、撤回同意、投诉后，要同步 suppression。
- Aged lead 不能用旧 consent 无限触达；要按 lead age、buyer terms 和 suppression 重新审查。
- TrustedForm / Jornaya 类证据只能证明页面上下文的一部分，不能替代法律判断、buyer disclosure、DNC/opt-out 和合同。

不要通过换主体、换 buyer、换电话、换短信平台或重新 timestamp 来绕过 opt-out / DNC / TCPA / TSR。

## 10. Google Ads 政策和受众边界

保险 lead 在 Google Ads 上常踩四类政策：

| 政策面 | 风险 | 治理 |
| --- | --- | --- |
| Health insurance ads / Healthcare policy | 某些健康保险广告需要认证或受限制 | 先确认目标国家、产品类型和认证要求 |
| Personalized advertising | 健康、财务困难、受保护属性等敏感定向限制 | 不用敏感属性、年龄焦虑、疾病状态做个性化诱导 |
| Misrepresentation | 冒充官方、隐藏费用/主体/资格限制、夸大结果 | 页面主体、商业关系、限制、资格和更新日期清晰 |
| Financial products/services | 保险/金融相关披露、费用、条款透明度 | 不承诺保证批准、最低价、最高补贴或固定省钱 |
| Destination requirements | 广告、Final URL、landing、表单和实际体验一致 | 不做 cloaking、隐藏跳转、审核页/用户页不一致 |

Google Ads 不是保险资格判断系统。广告平台看到的 submitted lead、call click 或 page conversion 只是浅层信号，必须用 buyer paid feedback、complaint、reject reason 和 offline value 校准。

## 11. CMS、Marketplace 和 Medicare Marketing

Medicare / ACA 相关页面需要额外严谨：

- Medicare、Medicaid、Marketplace、HealthCare.gov、state exchange、CMS 等官方名词只能按事实使用。
- 页面要说明第三方身份、不是政府站点，除非确有官方授权。
- Medicare Advantage、Part D、Medigap、ACA plan 的比较和注册要由合适的 licensed/authorized 主体执行。
- TPMO、agent/broker、web-broker、direct enrollment、enhanced direct enrollment 等角色各有披露和记录要求，不能用 lead generator 文案代替。
- Medicare / ACA 开放注册日期、SEP 条件、计划可用性、补贴资格和 carrier/plan 信息必须用官方或授权来源维护。
- 不用“所有人都可获得”“每月 $0”“免费福利”“政府给你钱”等泛化承诺做转化诱饵。

系统里应该把 `official_source_url`、`review_year`、`window_type`、`state_exchange_flag`、`broker_authorization_ref`、`tpm_disclosure_version` 和 `reviewer` 保存到页面/Offer 审计记录中。

## 12. Creative / Landing Claim Review

保险创意和落地页要按 claim 类型审核：

| Claim | 高风险写法 | 安全写法方向 |
| --- | --- | --- |
| 价格/补贴 | “Get $0 health insurance guaranteed” | “Check available plan options and subsidy eligibility” |
| 官方关系 | “Official Medicare enrollment site” | “Independent resource; not a government website” |
| 省钱 | “Save $500 today” | “Compare factors that may affect your premium” |
| 批准/承保 | “Guaranteed approval” | “Coverage availability and underwriting vary” |
| 时间紧迫 | “Last chance for everyone” | “Enrollment periods and eligibility vary by situation” |
| 覆盖范围 | “All carriers / all plans” | “Participating carriers or plans vary by area” |
| 健康状态 | “Diabetics get special benefits” | 避免敏感健康状态诱导；用用户主动查询的教育内容 |

Landing page 必备检查：

- 页面主体、商业关系、第三方身份、联系方式、隐私政策清晰。
- 表单 CTA 不暗示购买、注册或批准已经完成。
- 年份、日期、计划可用性、州/县限制和资格条件有来源 URL。
- 素材、关键词、landing、buyer disclosure 和 call script 说法一致。
- 用户看到的页面和审核/爬虫看到的页面一致。

## 13. Offline Value Mapping

保险套利不能只回传 submitted lead。建议分层：

| Stage | Ads 信号建议 | 说明 |
| --- | --- | --- |
| page view / click to call | 诊断 | 不设 primary |
| submitted lead | 浅层诊断或 secondary | 用于漏斗，不直接扩量 |
| validation_passed | 质量诊断 | 排除格式错误和无资格 |
| buyer_accepted | 中间信号 | 仍可能 scrub |
| contacted / qualified_call | 较强信号 | 需去重和 consent |
| quoted / application_started | 强信号 | 适合作为 value feedback 候选 |
| enrolled / policy_issued | 强正向 | 适合作为成熟 primary 或 value |
| paid / retained | 最稳价值 | 用于最终 LTV / paid value 校准 |
| rejected / duplicate / complaint | 内部负向 | 不回传正向，可用于 source quarantine |

对于延迟长的 insurance paid feedback，可以先用 staged value，但必须定期用 mature cohort 校准：

```text
submitted_value < accepted_value < qualified_value < application_value < paid_value
```

不要把 buyer accepted、duration 达标或预约 booked 直接等同于 paid commission。

## 14. Insurance Lead Quality Score

建议评分：

```text
insurance_lead_quality_score =
  eligibility_fit               18
  consent_proof_quality         15
  buyer_accept_rate             15
  contact_or_answer_rate        10
  application_or_policy_rate    15
  paid_rate_or_net_value        15
  complaint_and_optout_risk      7
  source_claim_integrity         5
```

动作建议：

| Score | 动作 |
| --- | --- |
| 85-100 | 可按 mature paid value 小幅扩量 |
| 70-84 | 正常测试，继续收集 buyer feedback |
| 55-69 | 限量，查 reject reason、source 和 claim |
| 35-54 | 暂停扩量，修 eligibility、consent、routing 或页面 |
| 0-34 | 停 source / buyer / landing，开风险审计 |

评分必须按 subvertical、state/county、buyer、lead age、source、creative angle、form version 和 hour 拆分。平均分会掩盖某些州、年龄段、买方或素材角度的投诉。

## 15. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存保险政策、CMS/Marketplace/Medicare 来源 | `/sources` |
| 记录保险垂类准入、claim、official relationship 风险 | `/risk-audits` |
| 用 safe CPC、source_score、policy_score 测算小预算 | `/calculators` |
| 保存 Offer 垂类、国家、政策备注、tracking URL | `/offers` |
| 生成广告草稿和人工审核素材 | `/campaigns`、Offer 详情页 |
| 导入 accepted、qualified、application、paid revenue | `/metrics/import` |
| 生成暂停、限量、查 claim、查 source、等回传建议 | `/optimization` |
| 保存任务和人工审批痕迹 | `/tasks`、`/logs` |

后续可扩展表：

```text
insurance_vertical_profiles
insurance_qualification_fields
insurance_offer_eligibility_rules
insurance_enrollment_windows
insurance_buyer_terms
insurance_buyer_acceptance_events
insurance_reject_reason_maps
insurance_claim_reviews
insurance_license_authorization_refs
insurance_consent_reviews
insurance_offline_value_maps
insurance_quality_daily
```

关键字段：

```text
subvertical
state
county_or_zip_prefix
coverage_type
eligibility_bucket
enrollment_window_type
window_source_url
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

系统不保存真实 Medicare number、SSN、完整健康诊断、银行卡或未加密完整 PII；测试数据必须使用占位值和 hash。

## 16. ADXKit 对应点和完成形态

ADXKit 类系统里，保险 lead 专题对应以下能力：

| ADXKit 能力 | 保险场景完成形态 | 不交付内容 |
| --- | --- | --- |
| Offer 管理 | subvertical、state、payout、buyer terms、enrollment window、source URL | 未授权保险销售或虚假资质 |
| 落地页采集 | 抽取官方关系、补贴/省钱/批准 claim、表单字段和披露 | cloaking、审核页/用户页不一致 |
| AI 创意生成 | 生成“比较、资格检查、咨询”类低风险素材，并进入 claim review | 保证批准、冒充官方、医疗/年龄焦虑诱导 |
| 投放草稿 | 按 subvertical/state/window 分 campaign/ad group | Cookie 后台自动创建或绕过认证 |
| 换链接 | 只做同主题、同披露、同资格条件、已审核 URL 轮换 | 用换链绕过拒登或跳到未披露 buyer |
| 任务中心 | enrollment window 更新、claim review、buyer feedback 导入、source quarantine | 自动外呼、短信轰炸、刷量或补电话 |
| 来源库 | Google/CMS/Medicare/HealthCare.gov/FTC/NAIC 来源可追踪 | 用二手传闻替代官方规则 |

完成口径：把保险 lead 的行业知识、字段、资格、合规、buyer acceptance、offline value 和系统审计做完整；不做对抗平台、绕过登录、规避检测或制造虚假流量。

## 17. QA 清单

上线前逐项检查：

- `subvertical` 是否明确：ACA、Medicare、Final Expense、Auto、Home 等不能混用。
- 官方关系是否真实：是否误用 Medicare、Marketplace、HealthCare.gov、CMS、carrier 或 government 表达。
- 页面是否有 entity、role、privacy、contact、buyer disclosure 和更新日期。
- enrollment window 是否引用官方 URL，年份是否正确。
- 表单字段是否有 purpose 和 reject reason 映射，是否避免不必要敏感数据。
- Consent 是否包含 contact channel、buyer disclosure、version/hash 和页面证据。
- DNC/opt-out/suppression 是否在 buyer handoff 前检查。
- Buyer terms 是否写明 accepted、qualified、billable、return window、duplicate window、paid definition。
- Creative claim 是否避免 guaranteed approval、guaranteed savings、official relationship、all plans、free benefit 等强承诺。
- Call / pay-per-call 是否保存 buyer disposition，而不是只看 duration。
- Aged lead 是否与 fresh lead 分 conversion action、payout tier 和 attribution。
- Offline value 是否按 accepted、contacted、quoted、application、policy、paid 分层。
- Google Ads primary conversion 是否使用成熟、可收款、低投诉的事件。
- 不使用 Ads Cookie 后台操作、自动登录、cloaking、代理/指纹规避、补点击或封禁规避。

## 18. 信息来源 URL

| 来源 | URL | 用途 |
| --- | --- | --- |
| Google Ads Policy, Health insurance ads | https://support.google.com/adspolicy/answer/15597838 | 支撑健康保险广告认证、地区和产品限制判断 |
| Google Ads Policy, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑健康相关广告、医疗声明和认证边界 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑敏感属性、健康/财务困难和个性化定向边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑官方关系、价格、资格、主体和承诺透明度 |
| Google Ads Policy, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑保险/金融相关条款、费用和资格披露 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Google Ads lead form 的字段、隐私和后续处理边界 |
| Google Ads Help, About call assets | https://support.google.com/google-ads/answer/2453991 | 支撑 call-heavy insurance campaign 的 call asset 和电话信号治理 |
| HealthCare.gov, Dates and deadlines | https://www.healthcare.gov/quick-guide/dates-and-deadlines/ | 支撑 ACA / Marketplace 开放注册日期和页面日期来源 |
| HealthCare.gov, Special Enrollment Period | https://www.healthcare.gov/coverage-outside-open-enrollment/special-enrollment-period/ | 支撑 SEP 条件和 outside open enrollment 页面边界 |
| Medicare.gov, Joining a plan | https://www.medicare.gov/basics/get-started-with-medicare/get-more-coverage/joining-a-plan | 支撑 Medicare 加入/更换计划时间窗口 |
| Medicare.gov, Plan Compare | https://www.medicare.gov/plan-compare/ | 支撑 Medicare 计划比较应优先引用官方工具 |
| CMS, Contract Year 2025 Medicare Advantage and Part D Final Rule | https://www.cms.gov/newsroom/fact-sheets/contract-year-2025-medicare-advantage-and-part-d-final-rule-cms-4205-f | 支撑 Medicare marketing、TPMO、agent/broker 相关治理 |
| CMS Marketplace, Agents and brokers | https://www.cms.gov/marketplace/agents-brokers | 支撑 Marketplace agent/broker 角色和官方资源 |
| CMS Marketplace, Direct Enrollment and Enhanced Direct Enrollment | https://www.cms.gov/marketplace/marketplace-technical-assistance-resources/direct-enrollment-and-enhanced-direct-enrollment | 支撑 Marketplace web-broker / EDE 场景的授权和技术边界 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、lead generation、拒绝联系和披露边界 |
| FCC, TCPA and robocalls information | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑自动拨号、robocall/robotext 和 consent 风险背景 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| NAIC, Producer Licensing | https://content.naic.org/cipr-topics/producer-licensing | 支撑 insurance producer / agent licensing 的角色边界 |
| NAIC, Life Insurance consumer information | https://content.naic.org/consumer/life-insurance.htm | 支撑 life / final expense 用户教育和误导 claim 审核 |
| NIPR, Producer licensing | https://nipr.com/licensing-center | 支撑按州检查 producer licensing 和授权线索 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
