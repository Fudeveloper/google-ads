# 广告创意 Claim 审核与事实核查手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何审核广告标题、描述、关键词角度和 AI 生成素材中的 claim。这里的 claim 指任何会影响用户预期的声明：价格、免费、折扣、保证、排名、官方关系、评价、速度、收益、资格、认证、地区可用性、下一步动作等。

本文不提供规避 Google Ads 审核、自动绕过政策检测、cloaking、虚假承诺、假评价、刷点击或用 Cookie 接管后台的方法。目标是把创意从“能吸引点击”升级为“有页面证据、可解释、可审核、可结算”。

## 1. 为什么 Claim 审核是套利核心

Ads 套利不是单纯买低价点击再卖高价点击。真实利润来自：

```text
正确用户意图
+ 真实广告承诺
+ 可兑现落地页
+ 可结算 Offer
+ 可回收现金流
```

创意 claim 出错会直接污染全链路：

- CTR 变高，但吸引错误用户，RPV/EPC 下降。
- 页面兑现不了承诺，跳出率、投诉、拒登和账号风险上升。
- CPA/CPL 里 lead 质量下降，buyer feedback、reject、scrub、chargeback 增加。
- Smart Bidding 或优化规则学到错误信号，把预算推向低质量流量。
- 审核通过不代表长期安全；结算、投诉、复审、账号健康都可能滞后暴露。

所以 claim 审核不是法务附属流程，而是套利模型的一部分。每条强声明都必须回答：页面哪里证明它，Offer 是否允许它，政策是否限制它，数据是否支持继续放量。

## 2. Claim 生命周期

一个 claim 从产生到投放应经过 7 个节点：

1. 来源：来自 Offer 条款、落地页、广告主资料、用户评价、编辑评测、历史数据或 AI 改写。
2. 分类：价格、保证、排名、官方关系、评价、敏感垂类、CTA、时效等。
3. 证据：页面 snippet、条款、FAQ、资质、评价来源、披露、价格表、实验数据。
4. 风险：misrepresentation、editorial、destination、trademark、personalized ads、FTC endorsement。
5. 改写：把强声明降级为可验证弱表达。
6. 人审：投手或审核人逐条确认。
7. 复盘：把拒登、扣量、低 RPV、投诉、拒付反馈回 claim 库。

ADXKit 类产品常把“AI 生成广告创意”包装成效率功能，但真正难点是 claim governance：不应该让 AI 随机补价格、排名、认证、用户数或官方关系。

## 3. Claim 风险分类

| Claim 类型 | 常见写法 | 主要风险 | 安全表达 |
| --- | --- | --- | --- |
| 保证结果 | guaranteed approval、instant results | 结果无法保证、金融/医疗敏感 | check available options |
| 官方关系 | official、government、certified partner | 冒充官方、商标或资质误导 | guide、comparison、licensed info only if proven |
| 最高级 | best、#1、top rated | 没有排名方法或证据 | compare factors、review options |
| 免费 | free、no cost | 免费范围不清、隐藏费用 | learn what is free and what may cost |
| 折扣/节省 | save 70%、lowest price | 价格过期、无原价依据 | compare pricing signals |
| 评价/评分 | 5-star、trusted by thousands | 假评价、选择性引用、披露不足 | read review signals |
| 稀缺/紧迫 | only 3 left、today only | 虚假稀缺 | check current availability |
| 敏感垂类 | cure、erase debt、win money | 医疗/金融/博彩政策限制 | learn questions to ask |
| CTA/下一步 | download、apply、claim | 页面动作不一致 | describe the real next step |

## 4. Evidence Map

Claim 审核必须维护 evidence map：

| 字段 | 解释 |
| --- | --- |
| claim_text | 广告或页面中的原始声明 |
| asset_type | headline、description、keyword theme、landing H1、CTA |
| claim_type | price、proof、official、guarantee、review、sensitive、editorial |
| source_snippet | 页面或 Offer 资料中的支持片段 |
| source_url | 支撑页面或政策来源 URL |
| proof_strength | strong、medium、weak、missing |
| allowed_rewrite | 可上线弱表达 |
| blocked_reason | 删除原因 |
| reviewer | 人审责任人 |
| reviewed_at | 审核时间 |

强声明不能只因为“页面某处出现了相似词”就放行。比如页面有用户评价，不等于广告可以写 “#1 rated”；页面有“free consultation”，不等于可以写“free service”。

## 5. Google Ads 政策映射

Claim 审核最常用的政策映射：

| 政策主题 | 审核问题 |
| --- | --- |
| Misrepresentation | 是否隐藏主体、资质、商业关系、价格、费用、官方关系或服务结果 |
| Editorial requirements | 是否存在异常大写、标点、符号、错拼、gimmicky wording、display URL 误导 |
| Destination requirements | 广告承诺是否和最终页面一致，页面是否有原创价值和可用导航 |
| Trademarks | 是否在广告文字中不当使用品牌、商标、竞品名或暗示授权 |
| Unacceptable business practices | 是否冒充品牌、组织、公众人物或诱导用户交钱/交信息 |
| Personalized advertising | 是否用健康、金融困境、身份特征等敏感信息定向或写入创意 |
| Financial products and services | 贷款、债务、投资、加密、信用类是否需要披露、认证或地区限制 |
| Healthcare and medicines | 医疗、药品、健康声明是否受认证、地区和结果承诺限制 |

本系统把这些映射落实为风险审计、来源库、创意 claim 审核提示和人审流程。它不会自动提交广告后台，也不会为了通过审核改变用户看到的页面。

## 6. FTC / Review / Testimonial 边界

评价、背书和比较页在套利里很常见，尤其是 affiliate、lead gen 和垂直评测站。审查重点：

- 商业关系、佣金、赞助、赠品、激励需要清楚披露。
- 评价必须真实，不能由 AI 自动伪造。
- 不应选择性引用造成普通消费者会误解的结论。
- 个别结果不能被写成普遍结果。
- 排名页应说明方法、更新时间、覆盖范围和补偿关系。
- 用户评价来源要可追踪，不能把广告主文案包装成独立用户评价。

如果无法证明评价来源和披露，创意应使用 “compare options”、“review factors”、“learn what to check” 等弱表达。

## 7. 敏感垂类 Claim

敏感垂类要比普通 SaaS、工具、消费品更保守：

| 垂类 | 高风险 Claim | 安全方向 |
| --- | --- | --- |
| 金融/贷款/债务 | erase debt、guaranteed loan、no credit check | review eligibility factors、compare debt relief questions |
| 医疗/健康 | cure、treatment guaranteed、lose weight fast | learn treatment questions、compare care options |
| 博彩/游戏/抽奖 | guaranteed win、free money | check eligibility and local rules |
| 住房/就业/信贷 | targeting by sensitive identity or hardship | use broad, policy-safe information content |
| 政府服务 | official application、government refund | government-service guide unless officially authorized |
| 技术支持 | official support、virus removal guaranteed | informational troubleshooting unless approved |

这些垂类的 claim 审核要和 Offer 准入、页面披露、地区限制、账号验证、后续结算一起判断。

## 8. RSA / AI 素材审核

Responsive Search Ads 会组合多个 headlines 和 descriptions，因此不能只看单条文案。需要检查：

- 任何两个 headline 组合后是否产生更强承诺。
- pinned asset 是否必要，是否遮挡披露。
- AI 自动资产是否从页面过期优惠或临时测试文案中提取了不安全 claim。
- keyword insertion 插入后是否变成敏感词、品牌词、官方关系或不实承诺。
- descriptions 是否把弱证据包装成强结果。

AI 生成器应输出候选，不应直接投放。高风险 claim 必须进入人审队列。

## 9. 审核工作流

推荐流程：

1. 采集落地页，抽取 CTA、claim、proof/review、price/value、form signals。
2. 生成创意候选。
3. 对每条 headline/description 做 claim 分类。
4. 匹配 evidence map。
5. 标记 high/medium/low 风险。
6. 删除无证据强声明。
7. 把可保留 claim 改写成页面能证明的表达。
8. 记录来源 URL、reviewer、reviewed_at。
9. 导出 CSV / Scripts JSON 草稿。
10. 指标导入后用 CTR、RPV、CVR、reject、policy warning 复盘 claim 质量。

## 10. 系统落地

当前系统新增：

- `adsworkbench/services/claim_review.py`：只读审查创意标题和描述。
- `creative_claim_reviews` 表：持久化保存 asset、claim issue、severity、action、evidence、source_url 和 review_status。
- Offer 详情页：每个创意组展示 Claim 审核表，并支持 `刷新 Claim 审核`。
- `/claim-reviews/<id>/status`：把审核记录标记为 open、approved、rewrite_required、blocked 或 dismissed，并写入审计日志。
- 审核规则覆盖 guarantee、official、best/top/#1、free、save/discount、review/rating、scarcity、editorial style。
- 审核器读取 `LandingPage.raw_summary` 中的 `Claim snippets:`、`Proof/review snippets:`、`Price/value snippets:` 等 evidence。

当前系统不做：

- 不自动修改 Google Ads 后台。
- 不自动绕过拒登。
- 不生成假评价、假价格、假认证、假官方关系。
- 不为了审核通过显示不同页面。
- 不用补点击或模拟转化证明 claim。

后续可扩展：

- `creative_claim_map`：每条广告资产绑定支持 snippet。
- `blocked_claim_dictionary`：按垂类维护禁用词和降级表达。
- LLM provider 强制输出 source_snippet 和 blocked_claims。

## 11. QA 清单

| 检查项 | 放行标准 |
| --- | --- |
| Claim 来源 | 来自页面、Offer 条款或可信资料 |
| Evidence | 强声明有具体 snippet 或资质证明 |
| 官方关系 | 只有明确授权、认证或官方关系才可写 |
| 免费/折扣 | 范围、条件、地区、时间和费用清楚 |
| 评价/评分 | 来源真实、可验证、有披露 |
| 敏感垂类 | 不保证医疗、金融、博彩、住房就业信贷结果 |
| Editorial | 无异常大写、符号、错拼、误导 display URL |
| 组合效果 | RSA 组合后不产生更强误导承诺 |
| 页面一致 | Final URL 第一屏能兑现广告承诺 |
| 复盘 | 拒登、扣量、拒付和低 RPV 反馈到 claim 审核 |

## 12. 信息来源 URL

- Google Ads, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads, Editorial requirements: https://support.google.com/adspolicy/answer/6021546
- Google Ads, Text ad requirements: https://support.google.com/adspolicy/answer/6021630
- Google Ads, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads, Trademarks: https://support.google.com/adspolicy/answer/6118
- Google Ads, Unacceptable business practices: https://support.google.com/adspolicy/answer/15938071
- Google Ads, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads, Financial products and services: https://support.google.com/adspolicy/answer/2464998
- Google Ads, Healthcare and medicines: https://support.google.com/adspolicy/answer/176031
- Google Ads Help, About responsive search ads: https://support.google.com/google-ads/answer/7684791
- Google Ads Help, Keyword insertion: https://support.google.com/google-ads/answer/6371157
- FTC, Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides
- FTC, Endorsements, influencers, and reviews: https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews
