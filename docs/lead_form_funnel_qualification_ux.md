# Lead Form 漏斗、资格问题与移动端 UX 治理手册

更新时间：2026-06-09

本文解释 CPL / CPA / Call Lead / Appointment Lead arbitrage 中，表单漏斗如何影响 submitted lead、buyer acceptance、contact rate、qualified rate、paid rate 和投诉风险。表单不是“字段越少越好”或“字段越多越值钱”，而是在用户意图、资格筛选、隐私披露、移动端体验和 buyer feedback 之间做结构化取舍。

本文不是法律意见，也不提供自动提交表单、伪造 lead、补填用户资料、绕过验证、隐藏 buyer disclosure、规避 DNC/TCPA、cloaking、Cookie 后台接管或封禁后换号的方案。系统落地只做知识、字段设计、form version、QA、审计、来源 URL 和人工审批。

## 1. 为什么表单漏斗决定 CPL 盈亏

CPL 团队常见误判是只看表单提交率：

```text
Landing CVR = Submitted Leads / Clicks
```

但真实利润要看：

```text
Paid Lead Rate =
  Submitted
  -> Validated
  -> Consent valid
  -> Routed / posted
  -> Buyer accepted
  -> Contacted
  -> Qualified
  -> Approved / Paid
```

字段太少可能带来：

- 表单 CVR 高。
- bad geo、wrong service、not qualified、duplicate、low intent 高。
- Buyer accepted rate 和 paid rate 低。
- Google Ads 学到“容易提交但不可收款”的流量。

字段太多可能带来：

- 表单 CVR 低。
- 移动端放弃率高。
- 隐私和安全责任增加。
- 用户觉得被过度索取信息。
- 敏感垂类投诉和删除请求增加。

好表单的目标不是最大化 submitted，而是最大化 `paid revenue per click` 和 `compliant qualified lead rate`。

## 2. 原理解释：摩擦、意图和质量的取舍

表单摩擦有三类：

| 摩擦类型 | 作用 | 风险 |
| --- | --- | --- |
| 必要摩擦 | 过滤不合格用户，例如 state、service type、timeline | 过度会降低 CVR |
| 解释摩擦 | 让用户理解谁联系、为什么联系、会分享给谁 | 位置太晚会引发投诉 |
| 无效摩擦 | 重复字段、过细敏感信息、无用长文本 | 同时降低 CVR 和信任 |

设计原则：

- 用最少字段判断 buyer 是否可能接收。
- 高敏感字段只在必要且披露清楚时收集。
- 先问意图和资格，再问联系方式。
- 联系字段之前让用户知道谁会联系、通过什么渠道联系。
- 表单版本要可追踪，buyer feedback 必须能回到 `form_version_id`。

不要为了提高 CVR：

- 隐藏费用、限制、buyer identity 或数据分享。
- 预勾选 consent。
- 把 disclosure 放到提交后。
- 用“查看结果”伪装 lead submission。
- 把用户输入默认为同意多个 buyer 联系。

## 3. 核心对象地图

| 对象 | 作用 | 套利关注点 |
| --- | --- | --- |
| Form version | 字段、顺序、文案、披露、CTA 的版本 | buyer feedback 必须按版本复盘 |
| Field schema | 字段名、类型、必填、用途 | 防止过度收集和字段漂移 |
| Qualification question | 判断 buyer eligibility | 必须映射到 reject reason |
| Consent block | 联系、分享、渠道、主体同意 | 不能默认勾选或隐藏 |
| Disclosure block | 费用、关系、buyer、隐私、限制 | 必须靠近相关 CTA/claim |
| Error state | 用户输入错误提示 | 不应让用户猜错在哪里 |
| Mobile layout | 移动端输入体验 | 影响 completion 和误填 |
| CTA | 用户提交动作 | 文案必须描述真实下一步 |
| Abandon event | 放弃步骤 | 判断字段摩擦 |
| Buyer feedback | accepted / reject / paid | 回写字段和版本 |

## 4. 单步表单 vs 分步表单

单步表单适合：

- 字段少。
- 用户意图强。
- 资格问题简单。
- 移动端页面需要极短路径。
- B2B newsletter / low-risk inquiry。

分步表单适合：

- 需要 4 个以上字段。
- 资格问题会影响 buyer routing。
- 需要先筛 service type / state / timeline。
- 高 payout、高 reject 垂类。
- 用户需要解释为什么要问这些问题。

分步表单常见结构：

```text
Step 1: service need / vertical intent
Step 2: geo / eligibility
Step 3: timeline / contact preference
Step 4: disclosure + consent + contact fields
Step 5: confirmation / expected next step
```

注意：

- 分步表单不要制造“假进度”，比如 3 步后突然追加 10 个敏感字段。
- 每一步都应能解释为什么问。
- 如果用户不合格，要给安全退出或替代信息，不要诱导乱填。
- 分步结果页不要变成 cloaking 或不一致页面。

## 5. 字段分层和用途说明

字段要按用途分层：

| 层级 | 示例 | 建议 |
| --- | --- | --- |
| Intent | service type、product interest、case type | 通常先问 |
| Geo | state、zip、city | 只问服务区所需精度 |
| Eligibility | homeowner、debt range、coverage type、program interest | 必须映射 buyer 规则 |
| Timeline | immediate、this week、30 days | 用于优先级和 SLA |
| Contact | phone、email、preferred time | 在 disclosure 后收 |
| Consent | channel、seller/buyer scope、terms | 单独记录版本 |
| Sensitive | income、health、credit、legal details | 默认少收，使用区间 |
| Prohibited / avoid | SSN、full medical record、bank card、password | V1 不收集 |

每个字段都要能回答：

```text
field_name:
purpose:
required_by:
reject_reason_prevented:
pii_level:
retention:
buyer_visible:
used_in_ads_feedback:
```

如果一个字段不能减少 reject、改善 routing、满足 consent 或完成服务，就不要收。

## 6. 资格问题设计

资格问题要和 buyer reject reason 一一对应。

| Reject reason | 对应问题 | 注意 |
| --- | --- | --- |
| bad geo | state / zip / service area | 不要收完整地址除非必要 |
| wrong service | service type / case type | 选项要覆盖 buyer 分类 |
| not homeowner | homeowner / property role | 不要暗示只有某类人可获更好待遇 |
| low debt amount | debt amount range | 用区间，避免精确敏感数据 |
| wrong insurance status | current coverage / plan type | 避免承诺省钱或批准 |
| already represented | legal representation status | 法律垂类常用 |
| low intent | timeline / project stage | 不用虚假 urgency |
| invalid contact | phone/email format | 不等于自动外呼验证 |

常见错误：

- 用开放文本收集敏感叙述，后续无法结构化复盘。
- 把 buyer 的内部术语直接给用户看，导致误选。
- 为所有垂类共用一套资格问题。
- 表单改版后没有保留版本，导致 reject rate 无法解释。

## 7. 披露、Consent 和 CTA 位置

披露要靠近相关动作，而不是藏在页脚。

关键位置：

- 首屏：说明页面身份和服务类型。
- 表单开始前：说明收集信息的用途。
- 联系字段前：说明谁可能联系、什么渠道、何时联系。
- 提交按钮附近：说明点击按钮意味着什么。
- 提交后：确认下一步和 opt-out / contact preference。

CTA 文案要描述真实动作：

| 高风险 CTA | 更安全表达 |
| --- | --- |
| See if you qualify instantly | Request eligibility information |
| Claim your guaranteed savings | Compare available options |
| Get approved now | Request a quote / consultation |
| View my results | Submit request and get contacted |
| Continue | Continue to contact details |

Consent 设计原则：

- 不默认勾选。
- 不把多个渠道混成一个总同意。
- shared lead 要说明 buyer 或 buyer group。
- opt-out、privacy policy、terms 要可访问。
- 表单提交记录要保存 consent text hash 和 version。

## 8. 移动端 UX 和可访问性

移动端通常是 CPL 主要流量来源。表单要针对移动端：

- 使用合适 input type，例如 `tel`、`email`、`numeric`。
- label 始终可见，不只依赖 placeholder。
- 错误提示要指出字段和修复方式。
- 按钮足够大，和广告、导航、sticky 元素保持距离。
- 表单字段不要被广告或弹窗遮挡。
- 使用 autocomplete，但不要预填敏感或不适用字段。
- 每一步只问少量问题，避免小屏长表单。
- 提交后明确下一步，不让用户重复提交。

可访问性不是装饰。标签、说明、错误、焦点状态和键盘操作会影响真实用户完成率，也影响质量。

## 9. Form Versioning 和实验设计

每次改表单都要生成版本：

```text
form_version_id
landing_version_id
field_schema_hash
field_order
required_fields
disclosure_version
consent_version
cta_version
mobile_layout_version
effective_from
reviewer
```

实验不应只看 submitted CVR：

| 指标 | 说明 |
| --- | --- |
| step completion rate | 哪一步掉人 |
| field error rate | 哪个字段误填 |
| submitted rate | 表单提交 |
| validation pass rate | 基础验证通过 |
| accepted rate | buyer 接收 |
| contact rate | 接通 |
| qualified rate | 合格 |
| paid rate | 可收款 |
| complaint / opt-out rate | 合规风险 |

如果新表单 CVR 提升 30%，但 accepted rate 下降 50%，它不是优化。

## 10. Abandon、Error 和 Low Intent 诊断

常见问题：

| 现象 | 可能原因 | 第一动作 |
| --- | --- | --- |
| Step 1 掉人高 | 广告承诺和页面不一致 | 查 query、headline、first screen |
| Geo 字段错误多 | 格式不清、服务区不匹配 | 改为 state/zip 选择或提示 |
| Phone error 高 | 输入类型或格式提示差 | 使用 tel input 和本地化提示 |
| Contact step 掉人高 | 披露不足或信任低 | 加强主体、隐私、buyer 说明 |
| Submitted 高 accepted 低 | 资格问题不足 | 增加必要筛选 |
| Accepted 高 paid 低 | 意图弱或联系慢 | 查 timeline、speed-to-lead |
| Complaint 高 | CTA/披露误导、shared lead 过度联系 | 暂停 source/form，审 consent |

诊断要按 `source + campaign + query + creative + landing_version + form_version + buyer` 拆。

## 11. 表单质量评分

建议评分：

```text
Form Funnel Quality Score =
  0.20 * qualification_fit
  + 0.15 * consent_disclosure_clarity
  + 0.15 * mobile_completion_health
  + 0.15 * buyer_acceptance_rate
  + 0.10 * paid_rate
  + 0.10 * error_rate_control
  + 0.10 * pii_minimization
  + 0.05 * accessibility_safety
```

动作阈值：

| 分数 | 动作 |
| --- | --- |
| 85-100 | 可小步放量 |
| 70-84 | 维持测试，修字段或披露 |
| 50-69 | 降预算，只做修复实验 |
| < 50 | 暂停该 form version |

## 12. Google Ads 与转化信号边界

表单转化要分层：

- `form_start`：只能做诊断。
- `step_complete`：只能做漏斗分析。
- `submitted_lead`：浅层 conversion，不适合默认 primary。
- `validated_lead`：仍需 buyer acceptance。
- `accepted_lead`：可作为中间信号。
- `qualified_lead / booked / approved / paid`：更适合自动出价。

不要把低质量表单提交直接回传为高价值 conversion。表单越容易，越需要 buyer feedback 校准。

## 13. 系统落地

当前 V1 可用：

| 需求 | 当前位置 |
| --- | --- |
| 抽取表单数量、CTA、privacy/contact/about 信号 | `/offers/<id>/crawl` |
| 记录 Offer 垂类、限制和政策备注 | `/offers` |
| 导入 cost、conversion、paid revenue | `/metrics/import` |
| 记录 bad geo、invalid phone、no consent、complaint | `/risk-audits` |
| 查看 Lead、Ping/Post、验证和 SLA 手册 | `/knowledge/...` |

后续可扩展表：

```text
lead_form_versions
lead_form_fields
lead_form_step_events
lead_form_error_events
lead_form_abandon_events
lead_form_consent_blocks
lead_form_disclosure_versions
lead_form_quality_scores
form_buyer_feedback_daily
```

这些表用于字段版本、步骤、错误、放弃、consent/disclosure 和 buyer feedback。第一版不保存完整 PII，不做自动提交、表单轰炸、伪造 lead 或绕过验证。

## 14. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本项目完成形态 |
| --- | --- |
| 落地页/表单采集 | 抽取 form signals、CTA、privacy、disclosure 和字段数量 |
| 创意优化 | 用 low intent、field error、reject reason 回写 brief |
| 自动投放优化 | 只按 accepted/qualified/paid 与 Form Funnel Quality Score 生成建议 |
| 换链接 | 表单版本变更必须留痕，不做审核页/用户页不一致 |
| 数据同步 | 导入 buyer feedback 和 form version performance |
| 高风险表单操作 | 不自动提交、不补字段、不伪造 lead、不隐藏 disclosure |

## 15. QA 清单

- 每个字段是否有明确 purpose 和 reject reason 映射。
- 是否避免收集 SSN、银行卡、完整病历、密码等高危字段。
- 联系字段前是否有 buyer disclosure 和数据用途说明。
- Consent 是否不默认勾选，且按渠道/主体拆分。
- CTA 是否准确描述下一步。
- 移动端 label、input type、错误提示、按钮间距是否可用。
- 表单是否不被广告、弹窗、sticky 元素遮挡。
- form version、disclosure version、consent version 是否留痕。
- 是否按 form_version 复盘 accepted、qualified、paid、complaint。
- submitted lead 是否没有被默认设为 primary conversion。
- 是否禁止自动提交、伪造 lead、隐藏 buyer 或绕过验证。

## 16. 信息来源 URL

- Google Ads Help, About lead form assets: https://support.google.com/google-ads/answer/9423234
- Google Ads Help, Create lead form assets: https://support.google.com/google-ads/answer/9423235
- Google Ads Policy, Data collection and use: https://support.google.com/adspolicy/answer/6020956
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- FTC, .com Disclosures: How to Make Effective Disclosures in Digital Advertising: https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising
- FTC, Protecting Personal Information: A Guide for Business: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- FTC, Follow the Lead: An FTC Workshop on Lead Generation: https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation
- Google Analytics Help, Best practices to avoid sending PII: https://support.google.com/analytics/answer/6366371
- web.dev, Learn Forms: https://web.dev/learn/forms
- web.dev, Autofill: https://web.dev/learn/forms/autofill
- web.dev, Validation: https://web.dev/learn/forms/validation
- MDN, HTML attribute autocomplete: https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
- W3C WAI, Forms Tutorial: https://www.w3.org/WAI/tutorials/forms/
- W3C WCAG 2.2, Labels or Instructions: https://www.w3.org/TR/WCAG22/#labels-or-instructions
