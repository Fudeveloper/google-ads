# AI Provider、Prompt 模板与创意成本治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何治理 ADXKit 类系统里的 AI 配置、多模型 Provider、Prompt 模板、创意生成成本、输出质量、Claim 边界、人工审核、日志和安全风险。目标不是让 AI “多写几个标题”，而是把 AI 放进 evidence-first 的套利生产线：从 Offer、页面证据、关键词意图、政策限制和历史收入中生成可审核候选，再由人审、Claim 审核和数据复盘决定是否投放。

本文不提供绕过广告审核、生成虚假承诺、伪造评价、冒充官方、隐藏商业关系、自动提交投放、补点击、刷转化、规避账号限制或用 prompt 规避平台政策检测的方案。

## 1. 为什么 AI 配置是套利核心能力

套利团队的创意迭代量很大：同一个 Offer 可能要测国家、语言、设备、query intent、页面版本、claim 角度、广告资产和关键词组合。AI 的价值在于降低候选创意和关键词的生产成本，但风险也很直接：

- AI 容易补不存在的价格、排名、认证、折扣、评价和官方关系。
- 高 CTR 文案可能降低 lead 质量、search feed 质量和 finalized revenue。
- Prompt 如果只要求“提高点击率”，会把系统推向误导性 claim。
- 多模型输出不一致，容易出现不可复现的审核争议。
- 未记录输入、prompt、模型、版本和人工决定时，事故无法复盘。
- 把敏感页面、用户数据或 buyer 信息直接发给模型，会带来隐私和合同风险。

AI 配置在套利业务里的正确角色：

```text
Offer / Landing / Evidence / Policy / Metrics
  -> Prompt template
  -> Model candidates
  -> Claim extraction and risk flags
  -> Human review
  -> Campaign draft
  -> Metrics and rejection feedback
  -> Prompt and angle library update
```

## 2. Provider 抽象和多模型路由

ADXKit 公开页面提到多模型配置和成本控制。系统设计上应把 AI Provider 当成可替换的候选生成器，而不是决定投放的权威。

Provider 配置建议：

| 字段 | 用途 |
| --- | --- |
| provider_name | OpenAI、Gemini、Claude、本地模型或内部服务 |
| model_name | 具体模型和版本 |
| task_type | creative_generation、keyword_expansion、claim_rewrite、translation、summary |
| max_input_tokens | 防止把整站内容塞给模型 |
| max_output_tokens | 控制成本和冗余 |
| temperature_profile | conservative、balanced、exploratory |
| allowed_verticals | 金融、医疗、博彩等敏感垂类可限制模型任务 |
| pii_policy | 是否允许处理用户数据，默认不允许 |
| cost_limit_daily | 日预算上限 |
| review_required | 是否必须人审，默认 true |

多模型路由原则：

- Claim 相关任务使用低温、保守、可复现配置。
- 创意角度探索可以使用更发散配置，但输出不能直接投放。
- 翻译和本地化需要保留原 claim 强度，不得自动放大承诺。
- 敏感垂类优先使用模板和人工改写，不让模型自由发挥。
- Provider 宕机或成本超限时降级为规则模板，而不是跳过审核。

## 3. Prompt 模板结构

Prompt 模板应像投放 brief，而不是一句“帮我写高 CTR 广告”。

推荐结构：

```text
system_boundary:
  You generate draft ad assets only. Do not invent claims.

offer_context:
  name, vertical, country, language, payout_model, restrictions

landing_evidence:
  title, h1, cta, claim snippets, proof snippets, disclosure links

user_intent:
  keyword themes, search terms, audience stage, device

policy_constraints:
  misrepresentation, editorial, sensitive vertical, trademark, privacy

output_contract:
  JSON fields, asset counts, max length, banned phrases, review notes

self_check:
  list every claim and the supporting snippet
```

模板必须明确：

- 只能改写、压缩、组合输入证据。
- 不得新增价格、折扣、排名、认证、用户数、批准率、收益、官方关系或 guarantee。
- 每条 headline / description 都要标注 claim type 和 evidence source。
- 对证据不足的角度输出 `needs_review` 或 `blocked_reason`。
- 输出只是草稿，不自动提交广告后台。

## 4. Evidence-first 输出合同

AI 输出应结构化，方便系统审核和人审。

```json
{
  "angle": "comparison",
  "headlines": [
    {
      "text": "Compare Cloud Backup Options",
      "claim_type": "comparison",
      "evidence_snippet": "Pricing table compares monthly cost and restore limits.",
      "risk": "low"
    }
  ],
  "descriptions": [
    {
      "text": "Review features, pricing, and restore options before choosing.",
      "claim_type": "page_value",
      "evidence_snippet": "A practical comparison of backup tools for small teams.",
      "risk": "low"
    }
  ],
  "blocked_claims": [
    {
      "text": "Guaranteed cheapest backup",
      "reason": "No ranking or guarantee evidence."
    }
  ],
  "review_notes": ["Human review required before export."]
}
```

系统不要只保存最终文案，还要保存：

```text
prompt_template_id
prompt_template_version
provider_name
model_name
input_evidence_hash
output_hash
token_usage
estimated_cost
review_status
reviewer
approved_asset_ids
blocked_reason
```

## 5. Prompt Library 和 Angle Library

套利团队真正可复用的是角度库，而不是随机 prompt。

角度库字段：

| 字段 | 解释 |
| --- | --- |
| angle_name | comparison、guide、eligibility、cost_calculator、local_service |
| intent_stage | awareness、consideration、action |
| allowed_verticals | 可用垂类 |
| banned_verticals | 禁用垂类 |
| proof_required | 价格表、评分、资质、案例、FAQ |
| safe_claim_level | weak、medium、strong |
| historical_rpv | 历史每访客收入 |
| rejection_rate | 拒登/拒付/投诉 |
| recommended_status | use、review、pause |

Prompt Library 要版本化。每次修改模板，记录：

- 修改原因。
- 适用任务。
- 风险变更。
- 回滚版本。
- 测试样本。
- 人审人。

## 6. 成本控制和 ROI 口径

AI 成本不是只看 token 花费。真实成本包括：

- 模型调用成本。
- 落地页抓取和清洗成本。
- 人审时间。
- 拒登返工。
- 低质量文案带来的无效点击、低 RPV、拒付和扣量。
- Prompt 调试和 QA 时间。

建议指标：

| 指标 | 含义 |
| --- | --- |
| cost_per_generated_asset | 模型调用成本 / 生成资产数 |
| cost_per_approved_asset | 总生成成本 / 人审通过资产数 |
| approval_rate | 通过资产 / 生成资产 |
| edit_distance_to_approved | AI 草稿到人审版本的改动幅度 |
| claim_block_rate | 被 claim 审核拦截比例 |
| rejected_ad_rate | 广告平台拒登比例 |
| paid_rpv_by_angle | 角度带来的可收款每访客收入 |
| token_cost_per_paid_revenue | AI 成本 / paid revenue |

一个模型如果便宜但高风险 claim 多、返工多、低质量流量多，综合成本可能更高。扩量依据应是 approved assets 的 paid revenue 表现，而不是生成速度。

## 7. 幻觉、Prompt Injection 和数据安全

AI 创意链路的两类安全问题最常见：

1. 幻觉：模型补出页面没有的事实。
2. Prompt injection：落地页、评价、抓取文本或第三方页面中包含指令，诱导模型忽略规则。

防护原则：

- 抓取内容作为 untrusted input，不让页面文字改写系统指令。
- Prompt 中分隔 evidence、policy 和 task instruction。
- 对输出做 claim 检测、关键词黑名单、敏感垂类规则和长度校验。
- 不把用户 PII、lead 明细、未披露 buyer 数据、账号凭据或 Cookie 发给模型。
- 不让模型直接调用广告后台、链接轮换、预算修改或任务执行。
- 模型输出必须进入人工审核和审计日志。

数据最小化：

```text
允许：页面标题、公开正文片段、CTA、非 PII 的 Offer 条款、聚合指标
限制：buyer 合同全文、内部结算细节、未公开价格、账号 ID
禁止：Ads Cookie、登录态、用户电话/email、lead 明细、付款资料、验证码
```

## 8. 创意、关键词和本地化的不同任务

不同 AI 任务的风险不同。

| 任务 | 可自动化程度 | 主要风险 |
| --- | --- | --- |
| 关键词主题扩展 | 中 | 扩到敏感、品牌、低意图或不允许词 |
| Headline / Description 草稿 | 中 | 强 claim、误导承诺、编辑政策 |
| Claim 降级改写 | 高 | 需要证据映射，不能改变真实含义 |
| 翻译 / 本地化 | 中 | 夸大承诺、本地法律/价格错误 |
| 竞品差异总结 | 低到中 | 商标、事实错误、冒充官方 |
| 用户评价摘要 | 低 | 评价造假、选择性引用、披露不足 |
| 敏感垂类文案 | 低 | 金融、医疗、住房就业信贷、博彩政策 |

关键词生成要进入否定词、品牌词、敏感词和 Offer 条款检查。翻译任务要保留限制条件，例如 “may”、 “compare”、 “learn” 不能被翻成确定性承诺。

## 9. 人审和发布闸门

AI 输出的上线条件：

1. 落地页 evidence 完整。
2. Claim 审核通过或已降级。
3. 敏感垂类政策检查通过。
4. Offer 条款允许该角度和流量来源。
5. CTA 和下一步动作一致。
6. 长度、标点、大小写、重复和 editorial 检查通过。
7. 审核人记录明确。
8. 只导出到 CSV / Scripts payload / Campaign draft，不自动提交后台。

发布闸门要把拒登、低 paid RPV、投诉、buyer reject、AdSense deduction 等反馈写回 angle 和 prompt 版本。不要让“生成通过”变成“持续可投”的默认状态。

## 10. 系统落地

当前 V1 已有：

| 需求 | 当前页面 / 文档 |
| --- | --- |
| 从 Offer 和页面摘要生成创意候选 | `/offers/<id>/creatives/generate` |
| 页面证据抽取 | `/offers/<id>/crawl` |
| Claim 风险提示 | Offer 详情页 Claim 审核 |
| 投放草稿 | `/campaigns` |
| 人工审核和导出 | CSV / Scripts payload |
| 来源和审计 | `/sources`、`/risk-audits`、`/logs` |

后续可扩展表：

```text
ai_providers
ai_model_profiles
prompt_templates
prompt_runs
ai_output_assets
creative_angle_library
claim_evidence_maps
ai_cost_daily
ai_review_decisions
prompt_regression_tests
```

这些表只用于候选生成、成本分析、审计、人审和回滚。不保存 Cookie、登录态、用户 PII、验证码或广告后台执行权限。

## 11. QA 清单

- Prompt 是否明确禁止新增页面没有的 claim。
- 输出是否结构化保存 evidence_snippet、risk、blocked_reason。
- Provider、model、prompt version、token usage、cost 是否可追溯。
- 是否对落地页文本做 prompt injection 防护。
- 是否禁止把用户 PII、Cookie、账号凭据发给模型。
- 敏感垂类是否默认强制人审。
- 翻译是否保留原 claim 强度和限制条件。
- 创意是否通过 misrepresentation、editorial、trademark、personalized ads 检查。
- 生成资产是否只进入草稿/导出，不自动提交广告后台。
- 拒登、扣量、低 RPV、投诉是否能反馈到 prompt 和 angle 库。
- 成本报表是否按 approved asset 和 paid revenue 看，而不是只看 token 单价。

## 12. 信息来源 URL

- Google Ads Help, About automatically created assets: https://support.google.com/google-ads/answer/11259373
- Google Ads Help, About text customization: https://support.google.com/google-ads/answer/6072565
- Google Ads Help, About responsive search ads: https://support.google.com/google-ads/answer/7684791
- Google Ads Help, About Ad Strength: https://support.google.com/google-ads/answer/9921843
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Editorial requirements: https://support.google.com/adspolicy/answer/6021546
- Google Ads Policy, Trademarks: https://support.google.com/adspolicy/answer/6118
- Google Ads Policy, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads API, Automatically created assets: https://developers.google.com/google-ads/api/docs/assets/automatically-created-assets
- NIST, AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST, AI RMF Generative AI Profile: https://www.nist.gov/itl/ai-risk-management-framework/generative-ai-profile
- OWASP, Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Google, Generative AI Prohibited Use Policy: https://policies.google.com/terms/generative-ai/use-policy
