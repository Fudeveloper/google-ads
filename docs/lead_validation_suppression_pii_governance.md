# Lead 验证、Suppression、去重与 PII 治理手册

更新时间：2026-06-09

本文解释 CPL / CPA / Lead arbitrage 中的 lead validation、suppression、duplicate detection、DNC / opt-out、PII 最小化、数据保留、删除和 buyer reject 反馈闭环。它承接 [Lead 质量、Postback 对账与拒付管理手册](lead_quality_postback_reconciliation.md)、[Lead Form、电话线索、Call Tracking 与 TCPA 风险手册](lead_form_call_tracking_tcpa_compliance.md) 和 [Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)，重点回答：线索在卖给 buyer 之前，如何判断“可联系、可出售、可回传、可保留、可删除、可解释”。

本文不是法律意见，也不提供伪造 lead、自动提交表单、绕过 buyer 风控、规避 DNC/TCPA、隐藏数据转售、泄露 PII、用补点击修转化、Cookie 后台接管或规避账号关联的方案。系统落地只做验证口径、字段白名单、审计、质量评分、suppression 证据和人工审批。

## 1. 为什么 Lead Validation / Suppression 是套利核心

Lead arbitrage 亏损通常不是发生在点击当下，而是发生在之后：

- 表单提交率高，但电话无效、邮箱无效、地址不在服务区。
- 用户重复提交，或在多个 source / buyer / aggregator 之间重复流转。
- 用户已经 opt out、进入 DNC、撤回同意或投诉。
- 页面收集了不必要敏感信息，导致审核、投诉、泄露和删除请求成本上升。
- Buyer 初始 accepted，但结算时因为 duplicate、invalid contact、bad geo、no consent、low intent 或 prohibited source 拒付。
- Google Ads 把 submitted lead 当作 primary conversion，算法继续买低质流量。

因此，validation 不是“让更多 lead 看起来可卖”，而是把不可卖、不可联系、不可保留、不可回传的数据尽早挡住。一个合格的 lead validation 体系要保护三件事：

```text
Buyer 接收率和 paid revenue
用户同意、退订和隐私权
广告系统的出价学习信号
```

## 2. 原理解释：验证不是造假

验证的正确目标：

- 检查字段格式、必填项、地区、产品资格、source 条款。
- 检查 duplicate、suppression、DNC、opt-out、撤回同意。
- 检查 consent 和 disclosure 是否支持本次 handoff。
- 检查 buyer campaign 是否仍有 cap、营业时间和资格匹配。
- 把 reject reason 反馈给 source、creative、landing、form version 和 buyer routing。

验证的错误用法：

- 自动生成或补填缺失姓名、电话、邮箱、地址。
- 用随机号码、一次性邮箱或伪造身份通过 buyer 校验。
- 对 opt-out / DNC 用户继续换 buyer 转发。
- 隐藏 source、subid、lead age、shared lead 状态。
- 把 rejected lead 继续卖给未披露 buyer。
- 用虚假 conversion 或补点击让广告报表变好看。

行业里真正有价值的 validation，是让差 lead 更早暴露，而不是让差 lead 更晚被拒。

## 3. 数据分类与 PII 最小化

Lead 数据要先分层，才能决定是否收集、如何保存、能否回传。

| 数据层级 | 示例 | 用途 | 治理要求 |
| --- | --- | --- | --- |
| 非个人运营维度 | campaign、keyword、creative、landing、source | 投放复盘 | 可长期保存，避免混入 PII |
| 点击与事件 ID | click_id、gclid、transaction_id、lead_id | 归因、去重、postback | 生命周期、去重、权限控制 |
| 联系字段 | phone、email、name、zip | 联系和 buyer handoff | 最小化、加密、访问控制、删除流程 |
| 资格字段 | service type、state、homeowner、coverage need | buyer 匹配 | 只收业务必要字段 |
| 敏感字段 | 健康、债务、收入、信用、保险、法律问题 | 特定垂类资格 | 默认少收，必须有额外披露和访问限制 |
| 禁止或极高危字段 | SSN、完整银行卡、密码、完整病历 | 通常不应出现在套利 V1 | V1 不收集，不写入日志或 URL |

最小化原则：

- 能用 `source_id` 解决的问题，不要存完整用户身份。
- 能用 hash 做 duplicate 检查的问题，不要让明文字段进入 analytics。
- 能在 buyer accepted 后再 post 的字段，不要在 ping 阶段扩散。
- URL、UTM、subid、日志标题、CSV 文件名、报表维度不得包含 phone、email、name、address、SSN、健康或金融详情。
- AI prompt、创意生成、页面摘要和调试日志不得包含真实 lead PII。

## 4. Validation Pipeline

推荐的验证流水线：

```text
Form submit / call event
  -> schema validation
  -> consent and disclosure check
  -> format and normalization
  -> duplicate check
  -> suppression / DNC / opt-out check
  -> geo and offer eligibility
  -> source policy check
  -> buyer campaign and cap check
  -> ping/post routing
  -> buyer response
  -> feedback and paid status
```

每一步都要输出明确状态，而不是一个模糊的 `valid=true`。

| 阶段 | 输出 | 拒绝例子 |
| --- | --- | --- |
| schema | fields_present / missing | 缺 phone 或 service type |
| consent | consent_valid / invalid / unknown | 无 buyer disclosure |
| format | normalized / invalid_format | 电话长度错、邮箱格式错 |
| duplicate | new / duplicate / possible_duplicate | 同 phone hash 在窗口内重复 |
| suppression | allowed / suppressed / dnc / optout | 用户撤回同意 |
| eligibility | eligible / bad_geo / out_of_scope | 州不支持、年龄不符 |
| source policy | allowed / prohibited | Offer 禁止该 source |
| buyer cap | available / cap_reached / stale | buyer 今日 cap 满 |
| routing | posted / no_buyer / hold_for_review | 无合规 buyer |

系统设计上，validation record 应不可覆盖原始事实。后续状态可以追加，但不要把 `rejected_duplicate` 改成 `accepted` 来美化历史。

## 5. Phone / Email / Address / Geo 校验

### Phone

电话校验不是“自动拨打验证”。安全做法包括：

- 格式标准化：国家码、地区码、长度、明显占位号码。
- 重复检查：phone hash、buyer 去重窗口、source 去重窗口。
- 地区匹配：号码地区、用户填写地区、广告 geo、服务区是否冲突。
- 类型风险：固定电话、移动电话、VoIP、不可联系号码要按 buyer 规则处理。
- DNC / suppression：不能因为号码格式有效就忽略 opt-out。

不做：

- 自动外呼、短信轰炸或机器人验证。
- 伪造通话时长。
- 对 opt-out 用户继续测试号码。

### Email

邮箱校验重点：

- 格式、域名、明显一次性域名或占位邮箱。
- hash 去重和 buyer reject 反馈。
- CAN-SPAM / unsubscribe / opt-out 处理。
- 不把邮箱写入 URL、subid、日志或 AI prompt。

邮件可达性不等于营销许可。用户提交邮箱，不自动等于可以无限营销、转售或发送未披露第三方邮件。

### Address / Geo

地址和地区校验重点：

- 国家、州、省、市、邮编与 offer 允许地区一致。
- Google Ads location options、页面语言、电话区号和 buyer 服务区一致。
- 不在不必要场景收完整地址。
- 高敏感垂类避免把详细地址扩散给多 buyer。

Bad geo 通常是投放、页面承诺或 buyer targeting 问题，不是靠改地址字段解决。

## 6. Duplicate、Householding 与跨 Buyer 去重

重复 lead 有几种不同含义：

| 类型 | 说明 | 处理 |
| --- | --- | --- |
| exact duplicate | 同一 phone/email/hash 在短窗口内重复提交 | 不重复 post，不重复计 revenue |
| source duplicate | 同一 source 反复提交相似 lead | 降低 source score |
| buyer duplicate | buyer 已经接收过该用户 | 记录 buyer reject reason |
| household duplicate | 同地址/家庭多次提交 | 按垂类和 buyer 规则人工判断 |
| cross-network duplicate | 用户在多个 network / aggregator 间流转 | 降低 aged/shared lead 估值 |
| event duplicate | postback 或状态回传重复 | 用 transaction_id 去重 |

去重窗口要按业务定义：

```text
same_phone_24h
same_phone_30d
same_email_30d
same_buyer_campaign_90d
same_transaction_id_forever
```

注意：duplicate 检查应尽量使用 hash、salt 和访问控制。不要为了方便在报表里显示完整 phone/email。

## 7. Suppression、DNC、Opt-out 与撤回同意

Suppression 是“不能继续联系、不能继续出售、不能继续转发”的控制层。常见来源：

- 用户点击 unsubscribe。
- 用户要求不再联系。
- 电话 DNC / entity-specific do-not-call。
- 用户撤回 consent。
- 投诉、chargeback、法律请求。
- Buyer 或 network 要求屏蔽某用户、号码、邮箱或 source。
- 数据保留期到期或删除请求完成。

需要保存的字段：

```text
suppression_id
suppression_type
identifier_hash
scope
source_of_request
received_at
effective_at
expires_at
reason_code
notified_buyers
reviewer
evidence_url
```

关键原则：

- Suppression 必须在 ping/post 之前检查。
- Shared lead 场景要能向已接收 buyer 同步 opt-out / revocation。
- DNC 不是只查一次；外呼前、转发前和批量活动前都要确认适用状态。
- 用户撤回同意后，不要把 lead 换 buyer、换渠道或换话术继续联系。
- Suppression list 本身也是敏感数据，应只保存 hash 或最小必要字段。

## 8. Data Broker、数据转售和用户权利

Lead arbitrage 很容易落入 data broker / lead generator / data sharing 语境。团队要回答：

- 是否向非直接服务提供方出售或分享个人信息。
- 是否允许多个 buyer 联系用户。
- 用户是否知道数据会被分享给哪些类别或具体主体。
- 是否适用 CCPA/CPRA、州隐私法、数据经纪人注册、删除请求、opt-out / limit use 规则。
- 是否涉及金融、保险、就业、住房、信贷等可能触发 FCRA 或其他特殊规则的用途。

运营上，不要把所有 buyer 都写成“合作伙伴”。应至少版本化：

```text
buyer_disclosure_version
buyer_category
buyer_list_url
sale_or_share_flag
opt_out_mechanism
delete_request_status
privacy_policy_version
data_broker_status
```

重要边界：

- 如果 lead 被用于信用、保险、就业、住房或类似资格判断，不能只按普通营销 lead 处理；要做 FCRA/专业法律评估。
- 如果 buyer 会再转售 lead，合同和页面披露必须能解释数据链路。
- 用户删除、访问、纠正、opt-out 请求需要有 ticket、状态和完成证据。

## 9. Retention、Deletion、Disposal 和访问控制

数据保留不是越久越好。套利团队至少要给每类数据定义保留期：

| 数据 | 建议治理 |
| --- | --- |
| campaign/source 聚合指标 | 可长期保留 |
| click_id / transaction_id | 按归因和争议窗口保留 |
| raw lead 明细 | 仅按 buyer、合规和争议需要保留 |
| consent evidence | 按法律/合同/争议窗口保留 |
| suppression hash | 可长期保留以防再次联系，但限制访问 |
| rejected lead 明细 | 短保留，保留原因和聚合统计 |
| call recordings | 单独政策、披露、访问和删除 |

访问控制：

- 投放人员通常不需要看完整 phone/email。
- 创意、AI、报表、关键词优化只看聚合质量信号。
- 只有合规、客服、buyer 对账和受控开发调试可访问必要明细。
- 导出 CSV 要有审批、文件 hash、到期删除和访问日志。

删除/处置：

- 删除请求要覆盖 active lead、CRM、buyer handoff、导出文件和备份策略。
- 删除完成后保留最小证明记录，例如 request_id、hash、completed_at、scope。
- 不要把 suppressed 用户重新导入广告受众、再营销或 Customer Match。

## 10. Lead Validation Score

建议把 validation 做成解释性评分，而不是黑箱。

```text
Lead Validation Score =
  0.20 * consent_integrity
  + 0.15 * contact_format_quality
  + 0.15 * duplicate_safety
  + 0.15 * suppression_clearance
  + 0.10 * geo_offer_fit
  + 0.10 * source_policy_fit
  + 0.10 * buyer_feedback_quality
  + 0.05 * pii_minimization
```

评分解释：

| 维度 | 看什么 |
| --- | --- |
| consent_integrity | 同意范围、渠道、buyer disclosure、时间和页面版本 |
| contact_format_quality | 电话、邮箱、地址、地区是否基本可用 |
| duplicate_safety | 是否重复、是否在 buyer 窗口内 |
| suppression_clearance | DNC、opt-out、revocation、complaint 是否清除 |
| geo_offer_fit | 地区和 offer 条款是否匹配 |
| source_policy_fit | source、creative、landing 是否符合 buyer/network 条款 |
| buyer_feedback_quality | accepted、qualified、paid、complaint 历史 |
| pii_minimization | 是否只收集和传递必要字段 |

动作阈值：

| 分数 | 动作 |
| --- | --- |
| 85-100 | 可进入正常 routing，但仍等 buyer paid feedback |
| 70-84 | 可小规模测试，观察 reject reason |
| 50-69 | hold for review 或只发给低风险 buyer |
| < 50 | 不 post，进入 source/form 修复 |

## 11. Buyer Reject Reason 到修复动作

| Reject reason | 不要做 | 应该做 |
| --- | --- | --- |
| duplicate | 换 buyer 继续卖 | 查重复窗口、source、form retry、buyer history |
| invalid phone | 补号码或自动外呼 | 修表单、格式校验、source quality |
| invalid email | 自动生成邮箱 | 修输入提示、拦截明显占位邮箱 |
| bad geo | 改用户地址 | 修广告 geo、页面国家、offer eligibility |
| no consent | 换话术或隐藏披露 | 暂停 handoff，重审 consent 文案 |
| dnc / opt-out | 换号码/渠道联系 | suppression 生效并通知 buyer |
| prohibited source | 隐藏 subid/source | 停 source，修合同和投放设置 |
| low intent | 夸大承诺刺激提交 | 修 keyword、creative、页面筛选问题 |
| complaint | 继续放量 | 停 source，做 consent/buyer 行为审计 |

拒绝原因要进入 `/risk-audits` 或 future `lead_validation_events`，并反向影响预算、source score、creative brief 和 buyer routing。

## 12. Google Ads 与出价信号边界

Validation 直接影响 Google Ads 自动出价：

- submitted lead 可以作为浅层 observation，但不应默认 primary。
- `validated` 也只是中间状态，不等于 buyer accepted。
- `accepted` 仍可能被 scrub，不等于 paid。
- 最适合训练出价的是 qualified、approved、sold、paid 或带 value 的 buyer feedback。
- suppression / DNC / duplicate / invalid lead 不应回传为正向 conversion。
- no buyer、cap reached 和 rejected lead 要单独记状态，避免污染 Smart Bidding。

如果把低质量 submitted lead 回传为高价值 conversion，系统会学习“买更多容易提交、不可收款、易投诉的点击”。这比没有自动化更危险。

## 13. 系统落地

当前 V1 可用：

| 需求 | 当前位置 |
| --- | --- |
| Offer、buyer 条款和限制备注 | `/offers` |
| Lead 质量、Ping/Post、电话 Lead 知识 | `/knowledge/lead_quality`、`/knowledge/ping_post_leads`、`/knowledge/lead_call_tracking` |
| 成本、收入、approved/paid 口径导入 | `/metrics/import` |
| duplicate、bad geo、invalid phone、no consent 事件记录 | `/risk-audits` |
| Google/FTC/FCC/NIST/CPPA 来源沉淀 | `/sources` |

后续可扩展表：

```text
lead_validation_rules
lead_validation_events
lead_identifier_hashes
lead_duplicate_checks
lead_suppression_records
lead_privacy_requests
lead_retention_policies
lead_data_access_logs
lead_export_reviews
lead_validation_score_daily
buyer_reject_reason_maps
```

这些表只保存规则、hash、状态、证据、评分和聚合质量，不默认保存完整 PII。需要保存 PII 时必须有字段白名单、加密、访问控制、保留期、删除流程和审计日志。

## 14. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本项目完成形态 |
| --- | --- |
| Lead 数据处理 | 做 validation/suppression/PII 字段设计，不保存不必要明文 |
| 自动投放优化 | 用 approved/paid 和 reject reason 影响预算建议 |
| 换链接或 fallback | 只在 consent/source/offer 允许时做合规 fallback |
| Buyer routing | 先检查 suppression、duplicate、cap 和 buyer disclosure |
| 数据同步 | 只导入真实 buyer feedback、rejection report 和 privacy request 状态 |
| 高风险操作 | 不伪造 lead、不绕过 DNC/TCPA、不隐藏 source、不做 Cookie 后台 |

这块能力的核心不是“让 lead 更容易卖出”，而是让不可卖的 lead 尽早停止，让可卖的 lead 有证据、有范围、有状态、有回款口径。

## 15. QA 清单

- 表单字段是否只收业务必要信息。
- URL、subid、日志、CSV 文件名、AI prompt 是否不含 PII。
- consent 是否记录页面版本、文案 hash、渠道、buyer disclosure 和时间。
- phone/email/address 是否有格式与地区校验。
- duplicate 是否按 phone/email/transaction/buyer window 去重。
- suppression、DNC、opt-out、revocation 是否在 ping/post 前检查。
- shared lead 是否能向已接收 buyer 同步 opt-out。
- raw lead 明细是否有保留期、删除流程和访问日志。
- buyer reject reason 是否能回到 source、creative、landing、form version。
- Google Ads primary conversion 是否避免使用 submitted / invalid / duplicate / suppressed lead。
- 高风险垂类是否做 FCRA、GLBA、HIPAA、州隐私法或律师评估。
- 是否禁止自动生成/补填用户资料、伪造 lead、绕过 buyer 风控和 Cookie 后台操作。

## 16. 信息来源 URL

- FTC, Protecting Personal Information: A Guide for Business: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- FTC, Start with Security: A Guide for Business: https://www.ftc.gov/business-guidance/resources/start-security-guide-business
- FTC, Data Security: https://www.ftc.gov/business-guidance/privacy-security/data-security
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- FTC, Q&A for Telemarketers & Sellers About DNC Provisions in TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- FTC, CAN-SPAM Act: A Compliance Guide for Business: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FTC, Safeguards Rule: What Your Business Needs to Know: https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know
- NIST, SP 800-122 Guide to Protecting the Confidentiality of Personally Identifiable Information: https://csrc.nist.gov/pubs/sp/800/122/final
- NIST, Privacy Framework: https://www.nist.gov/privacy-framework
- California Attorney General, California Consumer Privacy Act: https://oag.ca.gov/privacy/ccpa
- California Privacy Protection Agency, Data Brokers: https://cppa.ca.gov/data_brokers/
- CFPB, Regulation V / Fair Credit Reporting Act: https://www.consumerfinance.gov/rules-policy/regulations/1022/
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Policies, Data collection and use: https://support.google.com/adspolicy/answer/6020956
- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Policies, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Analytics Help, Best practices to avoid sending Personally Identifiable Information: https://support.google.com/analytics/answer/6366371
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- eCFR, 16 CFR 310.5 Recordkeeping requirements: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5
