# Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册

更新时间：2026-06-09

本文解释 CPL / Call Lead / Appointment Lead / Insurance / Finance / Home Services / Education 等 lead arbitrage 场景里，如何治理 consent proof、lead certificate、TrustedForm / Jornaya 类第三方证据、页面版本、同意文本、buyer disclosure、DNC / opt-out、suppression、争议证据包和买方交接。它承接 [Lead Form、电话线索、Call Tracking 与 TCPA 风险手册](lead_form_call_tracking_tcpa_compliance.md)、[Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)、[Lead 验证、Suppression、去重与 PII 治理手册](lead_validation_suppression_pii_governance.md) 和 [Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md)，重点回答：一条 lead 被提交、转售、联系、拒付或投诉时，团队如何证明用户当时看到了什么、同意了什么、同意给谁、允许什么渠道联系、证据由谁保存、保存多久，以及争议时如何取证。

本文不是法律意见，也不提供伪造 consent、伪造 certificate、绕过 TCPA / DNC / TSR、隐藏 buyer、预勾选同意、自动提交表单、补 lead、Cookie 后台操作、cloaking、代理/指纹规避或封禁规避方案。系统只做证据字段、版本、校验、来源 URL、风险评分、争议证据包、人工审批和审计。

## 1. 为什么 Consent Proof 是 CPL 收款资产

很多团队把 consent 当成表单底部一段文字，只有投诉或拒付时才想起来截图。真正的 CPL 业务里，consent proof 是收入资产：

```text
lead submitted
  -> consent and page context captured
  -> validation / suppression / DNC check
  -> buyer disclosure and routing allowed
  -> post / call / CRM handoff
  -> accepted / rejected / paid / returned / complaint
  -> evidence pack if disputed
```

没有 consent proof，会出现：

- Buyer 拒付 `no consent`，团队只能靠聊天记录解释。
- 用户投诉“我没同意这个公司联系我”，无法证明页面披露。
- 同一 lead 被 shared 给多个 buyer，但 consent 文案只写了单一主体。
- 页面改版后，旧 lead 的同意文本和新页面混在一起。
- 第三方 certificate 过期、未 claim、未保存，争议窗口内无法取证。
- DNC / opt-out 已发生，但后续 routing 没有 suppression 证据。
- Google Ads / Analytics / logs 里意外携带 phone、email、name 等 PII。

所以 consent proof 不是“让 lead 更容易卖”的遮羞布，而是让可联系、可分享、可回传、可争议的边界清楚，并尽早停止不可联系或不可出售的 lead。

## 2. 原理解释：证据链证明的是页面上下文

Consent certificate 或 LeadID 类工具通常用于证明 lead 提交当下的上下文，包括页面、表单、同意文本、时间、来源和用户环境。它不等于：

- 不等于法律意见。
- 不等于用户永远同意。
- 不等于 buyer 一定可以电话、短信、邮件或自动化联系。
- 不等于可以转售给任意 buyer。
- 不等于 lead 质量合格、号码真实或会付款。
- 不等于可以忽略 DNC、opt-out、撤回同意、州法、合同或平台政策。

证据链真正回答的问题是：

| 问题 | 需要的证据 |
| --- | --- |
| 用户当时在哪个页面提交 | landing URL、form URL、page version、certificate URL |
| 用户看到了什么同意文本 | consent text、checkbox state、CTA、privacy link、buyer disclosure |
| 同意给谁联系 | named buyer、seller、partner category、buyer list version |
| 允许什么渠道 | phone、SMS、email、manual call、automated technology |
| 什么时候发生 | submit time、certificate capture time、timezone |
| 来源是什么 | campaign、keyword/query、source、subid、creative、landing version |
| 后续是否仍可联系 | opt-out、DNC、suppression、privacy request、lead age |
| 争议时能否复现 | retained certificate、screenshot/hash、audit log、buyer handoff log |

## 3. 核心对象地图

| 对象 | 含义 | 治理作用 |
| --- | --- | --- |
| consent version | 同意文本、复选框、CTA、buyer disclosure 的版本 | 防止页面改版后丢证据 |
| certificate URL / token | TrustedForm / Jornaya 类证据引用 | 支撑第三方取证和争议 |
| page snapshot / hash | 提交页 HTML、截图或内容哈希 | 证明用户当时看到的上下文 |
| buyer disclosure version | 可联系主体、主体类别或 buyer list | 判断 shared / exclusive 边界 |
| consent scope | 渠道、用途、自动化技术、分享范围 | 防止“一次同意无限转售” |
| consent event | 用户提交时的同意事件 | 和 lead、click、form、buyer handoff 关联 |
| suppression event | opt-out、DNC、withdrawal、complaint | 决定是否停止联系或转售 |
| handoff evidence | post event、buyer response、CRM ID | 证明何时交给了谁 |
| dispute evidence pack | 争议证据集合 | 处理 no consent、duplicate、complaint、return |

## 4. TrustedForm / Jornaya 类证据

行业里常见两类第三方证据：

| 类型 | 典型用途 | 关键风险 |
| --- | --- | --- |
| TrustedForm 类 certificate | 捕捉 lead 提交页上下文、claim certificate、保存证据 | 未 claim、过期、证书和 lead 不匹配、页面动态内容未版本化 |
| Jornaya / LeadiD 类 token | 为 lead 事件生成标识，用于 buyer 端验证和 TCPA / consent workflow | token 未随 lead 传递、buyer 不接受、字段与同意范围脱节 |

第三方证据的正确用法：

- 作为 consent evidence 的一部分，而不是全部。
- 和内部 `lead_id`、`form_version`、`consent_version`、`buyer_disclosure_version` 绑定。
- 保存 source URL、claim / retrieve 状态、证据保留期限和访问权限。
- 记录证据提供方、证据时间、页面时间和 lead submit time 的差异。
- 把证据缺失作为 routing block 或 review，而不是事后补证。

错误用法：

- 证书存在就认为可以 shared 给所有 buyer。
- 证书缺失后用截图、手工文本或重新提交来补证。
- 不保存用户看到的 buyer disclosure，只保存一个同意布尔值。
- 不记录 opt-out / DNC，继续使用旧证书联系。
- 把 certificate URL 写入可被公开访问的日志、subid 或广告参数。

## 5. Consent Certificate 生命周期

推荐生命周期：

```text
form render
  -> certificate/token initialized
  -> user sees consent and disclosure
  -> user submits
  -> lead validation
  -> certificate/token persisted
  -> claim/retrieve certificate
  -> buyer eligibility check
  -> post/handoff with allowed evidence fields
  -> monitor rejection/complaint/opt-out
  -> retain, archive, or delete by policy
```

关键状态：

| 状态 | 含义 | 动作 |
| --- | --- | --- |
| missing | 未捕捉或未提交证据 | 不 post，进入 review |
| captured | 已捕捉 token/certificate URL | 继续 validation |
| claimed | 证书已 claim 或可检索 | 可进入 buyer eligibility |
| mismatch | 证书和 lead / page / timestamp 不一致 | block handoff，开事故 |
| expired | 证书过期或超保留窗口 | 不用作争议主证据 |
| revoked / invalid | 提供方或 buyer 判定无效 | 暂停 source / form version |
| suppressed | 用户撤回同意、DNC、opt-out | 停止联系和后续 routing |

## 6. 字段和哈希

不要只保存 `consent=true`。推荐字段：

```text
lead_id
click_id / gclid / source / subid
landing_url
landing_version
form_version
consent_version
consent_text_hash
privacy_policy_url
terms_url
buyer_disclosure_version
buyer_scope
contact_channels_allowed
automated_technology_disclosure
checkbox_state
submit_timestamp
submit_timezone
user_region
certificate_provider
certificate_url_or_token_hash
certificate_status
certificate_claimed_at
page_snapshot_hash
pii_hash_refs
suppression_status
reviewer
decision
```

治理原则：

- 原文 consent text 可版本化保存；证据 URL/token 可以加密或 hash 后保存引用。
- 完整 phone/email/name/address 默认不进 URL、subid、日志、prompt、报表或公开任务。
- 截图、HTML、certificate 的访问要有最小权限和审计日志。
- 删除请求、保留期和争议窗口要按合同、法律、隐私政策和律师意见执行。
- 证据 hash 不能替代原始证据；hash 用于校验未被篡改。

## 7. Buyer 交接和 Ping/Post 边界

Consent proof 必须在 buyer handoff 前完成资格判断：

| 判断 | 合格条件 | 不合格动作 |
| --- | --- | --- |
| buyer disclosed | buyer 名称、类别或允许范围覆盖本 buyer | 不 post |
| channel allowed | 电话/短信/邮件/自动化技术范围匹配 | 改渠道或停止 |
| certificate valid | provider、token、page、timestamp 可匹配 | review |
| suppression clear | 无 opt-out、DNC、撤回、投诉 | block |
| lead age valid | lead age 在合同和 consent 范围内 | 不做 aged resale |
| vertical allowed | 垂类、地区、敏感属性允许 | 拒绝 handoff |
| data minimized | ping/post 只传必要字段 | 修 schema |

Ping/Post 特别要注意：

- Ping 阶段尽量不发完整 PII，只发 routing 所需最小字段。
- Post 阶段必须绑定 consent version、certificate ref、buyer disclosure 和 suppression check。
- Shared lead 必须比 exclusive lead 更严格，因为用户可能被多方联系。
- Aged lead 必须重新检查 lead age、consent refresh、DNC、opt-out 和 buyer terms。
- Buyer 的 accepted 不等于 paid，也不等于 consent 已充分。

## 8. DNC、Opt-out、撤回同意和投诉

Consent proof 是开始联系的证据，不是继续联系的永久许可证。系统必须把后续事件覆盖到 lead 和 buyer：

| 事件 | 影响 |
| --- | --- |
| DNC match | 不应电话营销联系，进入 suppression |
| opt-out | 停止相应渠道联系 |
| withdrawal of consent | 停止对应范围的 handoff 和联系 |
| privacy deletion request | 按保留/删除流程处理，保留必要审计 |
| complaint | 暂停 source/buyer/form version，生成证据包 |
| buyer reject no consent | 冻结 routing，复查证据链 |

这些事件必须同步给已经接收 lead 的 buyer，至少形成 `suppression_sync_event`。不能把撤回同意后的 lead 换 buyer、换渠道或换话术继续转售。

## 9. 争议证据包

遇到 buyer return、no consent、complaint、TCPA/DNC 风险或扣量时，证据包应包含：

```text
lead_id
buyer_id
handoff_time
buyer_response
invoice / return line
landing_url and page version
form_version
consent_text and hash
buyer disclosure version
privacy policy URL
certificate provider and status
certificate URL/token reference
submit timestamp and timezone
source / campaign / keyword / creative
suppression/DNC/opt-out status at handoff
post payload schema hash
audit log
reviewer decision
```

证据包不能包含不必要完整 PII。需要向 buyer 或律师提供时，应走最小必要、加密传输、访问记录和到期删除。

## 10. Consent Proof Quality Score

建议评分：

```text
consent_proof_quality_score =
  certificate_integrity       20
  consent_text_versioning     15
  buyer_disclosure_fit        15
  channel_scope_fit           10
  suppression_freshness       15
  page_snapshot_integrity     10
  handoff_audit_completeness  10
  retention_policy_fit         5
```

动作：

| Score | 动作 |
| --- | --- |
| 85-100 | 可交接给已披露 buyer |
| 70-84 | 可交接，但需抽样 QA |
| 55-69 | 限量或人工复核 |
| 35-54 | 暂停该 form/source/buyer handoff |
| 0-34 | 停止 routing，开合规事故 |

评分必须用真实投诉、reject、return、DNC/opt-out 和 buyer feedback 校准，不能只看证书捕捉成功率。

## 11. 常见事故和修复

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| buyer reject: no consent | disclosure 不覆盖 buyer，证书缺失或文本错版 | 暂停 buyer handoff，查 consent version |
| certificate mismatch | 页面动态生成、延迟提交、iframe 或脚本问题 | 冻结该 form version，重做 QA |
| complaint 激增 | shared lead 披露不足或联系频率高 | 暂停 source，同步 suppression |
| DNC 命中后仍联系 | suppression sync 失败 | 事故处理和 buyer audit |
| 表单 CVR 高但 paid 低 | 同意/承诺太宽泛，低意图 lead 多 | 调整 qualification 和 CTA |
| 证据包无法生成 | 只存了布尔值，没有版本和 hash | 停止扩量，补数据模型 |
| Google Ads 信号很好但投诉高 | shallow conversion 做 primary | 改 conversion action 和 value mapping |

## 12. 系统落地

当前 V1 可承接：

| 行业动作 | 系统位置 |
| --- | --- |
| 保存 consent / certificate 来源资料 | `/sources` |
| 记录 no consent、complaint、DNC、opt-out 事故 | `/risk-audits` |
| 用 source_score 影响测试预算和止损 | `/calculators` |
| 导入 buyer reject、return、paid 结果 | `/metrics/import` |
| 生成暂停 source、review form、fix disclosure 建议 | `/optimization` |
| 创建 certificate QA、buyer disclosure review 任务 | `/tasks` |

建议后续表：

```text
lead_consent_versions
lead_consent_events
lead_certificate_refs
lead_page_snapshots
buyer_disclosure_versions
lead_suppression_sync_events
lead_consent_dispute_cases
consent_proof_quality_daily
```

核心字段：

```text
lead_certificate_refs:
  lead_id, provider, certificate_ref_hash, certificate_status,
  captured_at, claimed_at, expires_at, source_url,
  form_version, consent_version, reviewer

lead_consent_events:
  lead_id, form_version, consent_version, consent_text_hash,
  buyer_disclosure_version, contact_channels_allowed,
  submit_timestamp, submit_timezone, page_snapshot_hash,
  suppression_status_at_submit, decision
```

系统不抓取或伪造第三方 certificate，不自动绕过 consent，不自动外呼，不自动 post 给未披露 buyer，不把真实 PII 写入 URL/subid/log/prompt。

## 13. ADXKit 对应点和完成形态

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| 表单/落地页采集 | 记录页面版本、consent text、privacy URL、buyer disclosure |
| 自动优化 | 根据 no consent、complaint、reject、certificate mismatch 生成降速建议 |
| 自动投放 | 只输出待审广告和表单 QA，不用 Cookie 后台发布 |
| 换链接 / routing | 只在 consent scope、buyer disclosure、cap 和 suppression 允许时建议 |
| ROI 看板 | 同时看 submitted、accepted、paid、returned、complaint、no consent |
| 任务中心 | certificate QA、DNC sync、buyer disclosure review、evidence pack |

完成标准：

- 能解释 consent proof、certificate、LeadID、page snapshot 和 buyer disclosure 的差异。
- 能说明证据链证明什么、不证明什么。
- 能把 consent scope、contact channel、buyer scope、suppression 和 handoff 绑定。
- 能生成 no consent / complaint / DNC / return 争议证据包。
- 明确不交付伪造 consent、补 lead、自动外呼、Cookie 后台操作、cloaking 或规避检测。

## 14. QA 清单

上线表单或 buyer handoff 前检查：

- 是否有 form version、landing version 和 consent version。
- 同意文本是否清楚说明联系主体、渠道、用途和自动化技术。
- Buyer disclosure 是否覆盖实际 routing buyer。
- Privacy policy、terms 和 disclosure 链接是否可访问并版本化。
- Certificate/token 是否捕捉、保存、claim 或可检索。
- Certificate 是否和 lead_id、page、timestamp、form version 匹配。
- 是否只保存必要字段，PII 是否没有进入 URL、subid、日志、prompt。
- Post 前是否检查 DNC、opt-out、suppression 和撤回同意。
- Shared / aged lead 是否有额外 consent、lead age 和 buyer terms 检查。
- Buyer reject 和 complaint 是否能回写到 form/source/angle。
- Evidence pack 是否能在争议窗口内生成。
- 是否没有预勾选同意、隐藏披露、伪造证据或绕过 TCPA/DNC/TSR。

## 15. 信息来源 URL

- ActiveProspect, TrustedForm: https://activeprospect.com/products/trustedform/
- ActiveProspect, Jornaya TCPA Guardian LeadConduit integration: https://activeprospect.com/leadconduit/integrations/jornaya/tcpa_guardian/
- Verisk, Publisher Guidelines for TCPA Guardian Enhancements: https://marketing.verisk.com/wp-content/uploads/2024/09/Publisher-Guidelines-for-TCPA-Guardian-Enhancements.pdf
- Verisk, TCPA Guardian Update: https://marketing.verisk.com/wp-content/uploads/2024/12/TCPA-Guardian-Update-New-Single-Seller-and-Select-All-Features.pdf
- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Policy, Data collection and use: https://support.google.com/adspolicy/answer/6020956
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Analytics Help, Best practices to avoid sending PII: https://support.google.com/analytics/answer/6366371
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- FTC, Q&A for Telemarketers & Sellers About DNC: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- FTC, Protecting Personal Information: A Guide for Business: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- FTC, Follow the Lead workshop: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- FCC, TCPA one-to-one consent rule court response / deletion order: https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- eCFR, 16 CFR 310.5 Recordkeeping requirements: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- NIST SP 800-122, Guide to Protecting the Confidentiality of PII: https://csrc.nist.gov/pubs/sp/800/122/final
