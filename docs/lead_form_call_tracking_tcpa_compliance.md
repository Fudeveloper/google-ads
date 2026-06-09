# Lead Form、电话线索、Call Tracking 与 TCPA 风险手册

更新时间：2026-06-08

本文说明 Ads 套利团队在 CPL、电话线索、本地服务、保险、金融、医疗、法律、教育和高客单价咨询场景里，如何治理 Google Ads Lead Form、网站表单、电话线索、Call Tracking、同意、TCPA、Telemarketing Sales Rule、Do Not Call、录音披露、CRM 交接和 buyer feedback。本文不是法律意见；实际业务必须结合用户所在地、呼叫方所在地、垂类、外呼方式、买方角色和律师意见判断。

本文不提供自动拨号、机器人外呼、短信群发、绕过 consent、伪造 lead、补电话、模拟转化、隐藏呼叫来源、规避 DNC/TCPA 或把用户数据转卖给未披露买方的方案。系统只沉淀知识、字段、审计、QA、对账和合规替代流程。

## 1. 为什么电话和表单 Lead 是套利高风险资产

电话和表单 lead 比普通页面转化更接近真实用户身份。一次 lead 可能包含姓名、电话、邮箱、邮编、地址、收入、健康、债务、保险、信用、住房、就业、教育或法律问题。套利团队如果只看 submitted lead，会把算法训练到“容易提交但不可成交、易投诉、不可合规联系”的人群。

典型链路：

```text
Ad click / call asset click
  -> Google lead form / landing form / tap-to-call
  -> call tracking number / form handler
  -> validation and consent evidence
  -> ping/post or CRM handoff
  -> buyer contact / qualification
  -> accepted / rejected / sold / paid
  -> complaint / DNC / refund feedback
```

风险集中在四个地方：

- 用户是否清楚知道谁会联系自己、因为什么联系、用什么方式联系。
- 收集的字段是否必要、准确、可保护、可删除。
- 电话、短信、自动化拨号、录音是否满足适用法律和平台政策。
- buyer 是否按同样披露、同意和质量规则处理 lead，而不是把投诉反推给流量方。

## 2. 核心对象

| 对象 | 作用 | 套利风险 |
| --- | --- | --- |
| Google Ads Lead Form asset | 直接在广告里收集用户信息 | 表单字段、隐私政策、联盟/聚合转售、敏感垂类限制 |
| Website form | 落地页收集 lead | consent 文案、字段过量、隐藏买方、预勾选 |
| Call asset | 在搜索广告中展示电话入口 | 电话归属、营业时间、接通率、通话质量 |
| Call ad | 历史电话广告格式 | 需迁移到 RSA + call assets，避免格式退役造成断量 |
| Call tracking number | 用动态号码或转接号码归因 | 号码池、录音、来电归因、隐私披露 |
| Consent evidence | 用户同意联系的证据 | checkbox、时间戳、IP/UA、页面版本、买方名单 |
| DNC / opt-out | 用户拒绝被联系 | 未同步会导致投诉、罚款、买方拒付 |
| Buyer / CRM | 接收并处理 lead | 数据转售、未披露主体、状态回传不完整 |
| Postback | 质量、成交和收入回传 | submitted 与 paid revenue 混淆 |

## 3. Google Ads Lead Form 与网站表单

Google Ads lead form assets 的价值是减少落地页摩擦，但它也把隐私、披露和 lead 质量问题前置到广告层。使用前要确认：

- 账号、广告系列、垂类和地区是否符合 Google Ads lead form 的资格与政策。
- 表单里收集的字段是否和服务直接相关。
- 隐私政策 URL 是否可访问，且说明数据用途、接收方、联系方式和用户权利。
- 表单标题、问题、CTA 和后续联系主体是否一致。
- 如果是 affiliate、lead aggregator 或第三方 buyer 场景，是否允许通过该产品收集并转交 lead。
- 敏感垂类是否需要额外资质、免责声明、年龄限制或禁止个性化广告。

网站表单要比 Google 原生表单更细地记录上下文，因为后续 buyer 争议经常需要证明“用户当时看到了什么”。建议保存聚合或审计级证据：

```text
form_version_id
landing_url
privacy_url
terms_url
disclosure_text_hash
consent_text_hash
checkbox_state
buyer_disclosure_version
submitted_at
geo
campaign_id / ad_group_id / creative_id
gclid / wbraid / gbraid / click_id
field_schema
lead_status
```

不要把电话、邮箱、姓名、完整地址、身份证、健康详情或信用详情放进 URL、UTM、subid、日志标题、公开报表或不必要的优化字段。

## 4. 电话线索和 Call Tracking

电话线索不是“call count 越多越好”。套利里要拆成：

- Call asset impressions。
- Call clicks。
- Connected calls。
- Qualified call duration。
- Unique caller。
- Repeat caller。
- Missed call。
- Wrong number。
- Existing customer。
- Sales qualified call。
- Paid / rejected call。

Call tracking 的基本原理是给不同来源、广告系列、关键词、页面或会话分配可归因号码，再把来电、通话时长、录音状态、接通状态和后续 CRM 结果回传。它解决的是“哪一批点击带来可收款电话”，不是用号码池隐藏主体、制造假电话或规避平台审核。

Google Ads call reporting 使用 Google forwarding numbers 等机制报告通话指标和转化。系统复盘时要注意：

- 电话转化阈值应按业务设置，例如 30 秒、60 秒、120 秒，不要把所有短拨号都当有效 lead。
- 营业时间、坐席接通率和 IVR 会影响广告算法学习。
- 号码要和业务主体、地区、页面承诺一致。
- 录音必须有适用地区要求的披露和保存控制。
- 对高投诉来源要按 source、query、geo、device、creative 拆开，而不是用补电话修 ROI。

截至 2026-06-08，Google Ads call ads 需要按官方帮助页和账号内提示迁移到 Responsive Search Ads + call assets 的治理路径。实践上不要把电话业务绑定在单一即将退役的广告格式上；应把电话资产、RSA、call reporting、营业时间、电话号码验证和 call conversion action 放进同一套 QA。

## 5. Consent to Contact、TCPA 和 DNC

美国电话和短信 lead 的关键不是“拿到了号码”，而是“拿到了什么范围、什么主体、什么渠道、什么时间、什么证据的同意”。TCPA、FCC 规则、FTC Telemarketing Sales Rule 和 Do Not Call 规则会共同影响：

- 是否可以给用户打电话。
- 是否可以用自动拨号、预录音、AI/自动语音或短信。
- 是否可以把同意转给一个或多个 buyer。
- 用户撤回同意后多久停止联系。
- DNC 和 entity-specific do-not-call 如何同步。
- 记录需要保留多久、谁负责保留。

运营上需要把 consent 拆成可审计字段：

```text
consent_scope
contact_channel_allowed
seller_name
buyer_name_or_buyer_group
tcpa_language_version
dnc_disclosure_version
consent_source_url
consent_time
consent_event_id
revocation_time
revocation_channel
suppression_list_status
```

重要边界：

- 默认勾选、隐藏同意、模糊“合作伙伴可能联系你”、把一个 consent 当作无限转售，都属于高风险做法。
- 如果用户要求不再联系，应进入 entity-specific DNC / suppression list，并向相关 buyer 同步。
- 外呼、短信、预录音、自动化拨号、AI 语音和人工电话的规则不同，不能混成一个“call allowed”字段。
- FCC 对 lead generator “one-to-one consent”规则曾有变化；2025 年相关 FCC 文件说明该规则受法院裁决影响并被移除。系统文档应记录来源日期，后续按最新 FCC/eCFR/法律意见更新。

## 6. Call Recording 与披露

Call recording 是质检、纠纷和 buyer feedback 的重要证据，但它也是隐私和同意风险点。团队需要先回答：

- 通话双方位于哪些州/国家。
- 是否需要 one-party 或 all-party consent。
- 录音提示在何时播放，是否足够清楚。
- 录音保存多久，谁可访问，是否可删除。
- 录音是否包含敏感健康、金融、法律或身份信息。
- 录音是否会被传给 buyer、外包坐席或 AI 质检服务。

系统第一版不保存录音文件，只记录录音治理状态：

```text
recording_enabled
recording_disclosure_text
recording_disclosure_version
recording_consent_status
recording_retention_days
recording_storage_owner
recording_review_status
```

如果 buyer 要求提供录音抽检，应通过受控链接、最小权限、脱敏和审计日志处理；不要把录音当作普通附件在邮件、表格或聊天工具里流转。

## 7. 表单字段、验证和数据最小化

字段越多，不代表 lead 越值钱。字段过多会增加摩擦、隐私风险、误填率、拒付和投诉。

字段分层：

| 层级 | 示例 | 建议 |
| --- | --- | --- |
| 基础联系 | name、phone、email、zip | 只收必要字段，清楚说明用途 |
| 资格条件 | service type、budget、timeline | 用选择题减少误填 |
| 敏感信息 | debt、income、health、credit、insurance | 需要额外披露和垂类审批 |
| 禁止/高危 | SSN、完整病历、银行卡、密码 | 第一版不收集 |

验证不等于骚扰。可以做格式校验、重复检测、地区匹配、buyer cap 检查和 consent 完整性检查；不要用自动外呼或短信轰炸验证“号码真实”。

## 8. Buyer Handoff、Ping/Post 和 CRM 状态

套利团队常见亏损点是：广告系统看到 submitted lead，买方只支付 qualified / sold lead。要把 handoff 和回传做成闭环。

推荐状态机：

```text
submitted
  -> consent_validated
  -> posted_to_buyer
  -> accepted
  -> contacted
  -> qualified
  -> sold / approved / paid
  -> rejected / duplicate / invalid_phone / bad_geo / no_consent / complaint
```

buyer handoff 要记录：

- buyer 或 buyer group。
- post 时间和响应。
- buyer lead ID。
- accepted / rejected 原因。
- payout / adjusted payout。
- complaint 或 DNC 事件。
- buyer 对 contact attempt 的规则。
- 用户是否知道该 buyer 会联系。

Google Ads offline conversions 或 enhanced conversions 只能用于真实、合规、可证明的转化反馈；不能用来补 submitted lead、伪造成交或绕过用户同意。

## 9. 质量、拒付和投诉诊断

电话/表单 lead 诊断不能只看 CPL。

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| submitted 高，accepted 低 | 字段缺失、重复、bad geo、buyer cap | 查表单 schema、地区、buyer 响应 |
| accepted 高，paid 低 | 低意图、电话不接、夸张 claim | 查 query、creative、页面承诺 |
| call clicks 高，connected 低 | 营业时间、号码错误、坐席不足 | 查 call reporting、号码、排期 |
| call duration 短 | 误点、错误服务、价格不匹配 | 查广告文案、CTA、query |
| complaint / DNC 高 | consent 不清、buyer 未披露、外呼频繁 | 暂停来源，审 consent 和 buyer |
| TCPA 风险上升 | 自动化拨号/短信、同意范围不足 | 法务审查，停自动联系 |

高风险来源应进入 `/risk-audits`，并按 source、campaign、keyword、creative、landing version、buyer 拆分。不要通过增加拨打次数、伪造通话时长或隐藏 buyer 名称来“修复”报表。

## 10. 系统落地

当前 V1 可用模块：

| 需求 | 当前页面 / 文档 |
| --- | --- |
| 记录 Offer 是否允许 CPL、电话、lead form、buyer 转售 | `/offers` 和 [Affiliate 尽调手册](affiliate_network_due_diligence.md) |
| 审核表单字段、隐私、披露和页面承诺 | `/offers/<id>/crawl`、Claim 审核、[隐私手册](privacy_consent_tracking.md) |
| 导入 cost、conversion、paid revenue | `/metrics/import` |
| 记录 duplicate、invalid phone、bad geo、no consent、complaint | `/risk-audits` |
| 保存 Google/FTC/FCC/eCFR 来源 | `/sources` |
| 生成优化建议 | `/optimization` |

后续可扩展表：

```text
lead_form_versions
lead_consent_events
lead_call_events
call_tracking_numbers
lead_buyer_handoffs
lead_status_history
lead_suppression_events
lead_compliance_audits
call_recording_reviews
```

这些表只用于证据、质量、对账和合规治理。第一版不保存完整 PII，不保存通话录音，不做自动外呼、短信群发、Cookie 登录、后台接管或规避审核。

## 11. QA 清单

- Offer 条款是否允许 Google Lead Form、网站表单、电话线索和第三方 buyer。
- 页面是否清楚说明谁会联系用户、为什么联系、用什么渠道联系。
- 隐私政策、terms、consent 文案和 buyer disclosure 是否可访问、可版本化。
- 表单字段是否最小化，是否避免收集无必要敏感信息。
- consent 是否不是默认勾选，且可按渠道、主体、时间证明。
- DNC、撤回同意和 suppression list 是否能同步给 buyer。
- Call tracking 号码是否和业务主体、地区、页面承诺一致。
- Call reporting、call duration threshold、营业时间和 missed call 是否进入报表。
- Call recording 是否有披露、访问控制、保留周期和删除机制。
- buyer feedback 是否能回传到 campaign、source、creative、landing version。
- Google Ads primary conversion 是否使用 approved/qualified/paid 口径，而不是 submitted lead。
- 投诉、invalid phone、bad geo、no consent 是否能触发暂停和审计。

## 12. 信息来源 URL

- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Help, Create lead form assets: https://support.google.com/google-ads/answer/9423235
- Google Ads Help, About call assets: https://support.google.com/google-ads/answer/2453991
- Google Ads Help, About call ads: https://support.google.com/google-ads/answer/6341403
- Google Ads Help, About call reporting: https://support.google.com/google-ads/answer/2454052
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Policy, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads API, Upload offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads API, Upload click conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-clicks
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, Q&A for Telemarketers & Sellers About DNC Provisions in TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- FTC, National Do Not Call Registry: https://telemarketing.donotcall.gov/
- FCC, TCPA one-to-one consent rule court response / deletion order: https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf
- eCFR, 47 CFR 64.1200 Delivery restrictions: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- eCFR, 16 CFR 310.5 Recordkeeping requirements: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5
