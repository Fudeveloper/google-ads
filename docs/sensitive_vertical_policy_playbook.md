# 敏感垂类政策与 Offer 准入手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何评估金融、信贷、医疗、博彩、住房/就业/信贷、政府服务、技术支持、加密/投资、法律/本地服务等高风险垂类。高 payout 垂类常常伴随认证、地区限制、个性化广告限制、页面披露、资质、广告文案和回款风险。本文只做准入、风控和合规流程，不提供绕过认证、规避审核、伪装主体、虚假资质、cloaking、换号或隐藏真实目的地的方案。

## 1. 准入原则

敏感垂类先问 6 个问题：

1. 这个垂类是否允许投放？
2. 是否需要 Google Ads 认证、许可证、资质或地区限制？
3. Offer/广告主是否具备真实主体和授权？
4. 页面是否能清楚披露价格、限制、风险、数据用途和商业关系？
5. 买量方式是否触碰个性化广告、brand bidding、误导或禁止来源？
6. 即使短期 ROI 为正，扣量、拒付、投诉和账号风险是否可承受？

如果需要“伪装成信息页”“换域名过审”“不写真实主体”“先跑再说”，直接拒绝。

## 2. 垂类风险分层

| 风险层 | 垂类 | 默认动作 |
| --- | --- | --- |
| 极高 | 赌博、处方药、金融投资承诺、债务减免、第三方技术支持、政府文件代办 | 不做，除非已有明确认证、许可、授权和人审 |
| 高 | 保险、贷款、信用卡、医疗服务、法律服务、加密产品、本地维修 | 严格准入，小预算，必须审计 |
| 中 | B2B SaaS、教育、职业培训、本地非敏感服务 | 关注承诺、资质、隐私和 lead 质量 |
| 低 | 普通工具、信息型内容、电商比较 | 常规审计即可 |

高 payout 不是加分项；在敏感垂类里，高 payout 往往代表高监管、高扣量或高投诉风险。

## 3. 金融、信贷和债务

常见 Offer：

- 贷款、信用卡、保险、债务减免、抵押贷款、投资服务、金融规划。
- 加密交易、钱包、投资教育、交易信号。

风险点：

- 金融服务地区监管和认证。
- 高收益、保本、快速批准、无风险等误导承诺。
- 费用、利率、条件、资质和风险披露不足。
- 信贷相关广告触发住房/就业/信贷 personalized advertising 限制。
- Lead 数据敏感，隐私和 consent 要求高。

拒绝标准：

- Offer 不说明许可证、广告主主体或适用地区。
- 页面无法披露费用、风险、资格或数据用途。
- 文案包含 guaranteed approval、instant debt erase、risk-free profit 等承诺。
- 要求隐藏 lead 来源或用非品牌页面伪装官方金融机构。

可测方向：

- 信息型指南、计算器、比较维度。
- 明确“不是财务建议”、说明限制。
- 有真实广告主、许可证、隐私和披露。
- 非 brand bidding，非误导承诺。

## 4. 医疗、健康和药品

常见 Offer：

- 医疗预约、保险、补充剂、诊所、远程医疗、药品、健康设备。

风险点：

- 医疗和药品广告限制。
- 个性化广告里与健康状况相关的 targeting 限制。
- 治愈、保证效果、夸大 before/after。
- 未经批准的药物、补充剂或医疗声明。
- 收集健康数据的隐私风险。

拒绝标准：

- 未经认证却推广处方药或药品销售。
- 页面承诺 cure、guaranteed result、快速治疗。
- 用用户疾病、痛苦或健康状态做个性化定向。
- Lead 表单收集健康信息但无隐私、同意和数据用途说明。

可测方向：

- 高质量信息型内容和问题清单。
- 诊所/服务需有真实资质和联系信息。
- 避免保证疗效，说明适用范围和咨询专业人士。
- 不做敏感健康状态个性化广告。

## 5. 博彩、游戏和抽奖

常见 Offer：

- 在线博彩、体育博彩、赌场、彩票、社交赌场、真钱游戏、抽奖。

风险点：

- 需要国家/地区许可和 Google 认证。
- 年龄限制、地理限制和 responsible gambling 要求。
- 社交赌场也可能受限。
- 变现方和页面如果有 gambling links，非博彩广告也可能被限制。

拒绝标准：

- 无许可证、无认证、无地理限制。
- 用普通游戏页引导到真钱博彩。
- 对未成年人或不可投地区展示。
- 使用 cloaking 或地域分流绕过审核。

可测方向：

- 默认不做。
- 只有明确许可、认证、地区限制、年龄门槛和法律审核后才进入。

## 6. 住房、就业、信贷 Personalized Ads

美国/加拿大住房、就业、信贷类广告有定向限制。

典型范围：

- Housing：租房、买房、房贷、房源。
- Employment：招聘、职位、求职。
- Credit：贷款、信用卡、信贷产品。

风险点：

- 某些人口统计、邮编、性别、年龄、婚姻/父母状态等 targeting 受限。
- 页面内容和广告文案可能触发自动分类。
- 使用 audience、remarketing、lookalike 类能力时更敏感。

实践：

- 先确认是否属于 HEC 范围。
- 使用符合政策的地域和定向。
- 避免暗示针对受保护类别。
- 保存分类、申诉和人审记录。

## 7. 政府文件、官方服务和公共服务

常见 Offer：

- 签证、驾照、出生证明、税务、政府补贴、官方表格、预约服务。

风险点：

- 伪装官方。
- 隐藏自己是第三方服务。
- 收费代办但不披露免费官方路径。
- 使用 government、official、gov、state 等让用户误认。

拒绝标准：

- 页面看起来像政府网站但不是。
- 不说明第三方身份、费用和官方替代路径。
- 广告暗示官方批准或政府背书。
- 收集敏感身份信息但无强隐私和安全说明。

可测方向：

- 默认谨慎。
- 必须清楚披露第三方身份、费用、官方渠道和服务内容。

## 8. 第三方技术支持

常见 Offer：

- 电脑维修、软件修复、账户恢复、打印机/路由器/操作系统支持。

风险点：

- 技术支持诈骗历史导致平台限制严格。
- 容易被识别为 third-party consumer technical support。
- 冒充品牌、远程控制、账户恢复、收费修复都很敏感。

拒绝标准：

- 冒充 Apple、Microsoft、Google、HP 等品牌官方支持。
- 用错误弹窗、病毒警告、倒计时诱导联系。
- 要求用户远程控制或付款但主体不清。
- 没有授权却购买品牌/故障词。

可测方向：

- 默认不做第三方 consumer tech support。
- 如为自有产品支持，只能针对自有用户和真实主体。

## 9. 法律和本地服务

常见 Offer：

- 律师咨询、事故赔偿、移民、税务、家政、本地维修。

风险点：

- 地区执业资质。
- Lead 转售和隐私。
- 夸大结果，例如“最高赔偿”“保证胜诉”。
- 本地服务伪装、虚假地址、虚假评论。

准入：

- 有真实执业主体或广告主。
- 服务范围、资质、费用和隐私清楚。
- 表单说明谁会联系用户。
- 不使用保证结果或虚假案例。

## 10. 准入评分

| 维度 | 分值 |
| --- | --- |
| 平台允许性 | 20 |
| 资质/认证/许可证 | 15 |
| 页面披露和主体真实性 | 15 |
| Offer 条款和流量限制清楚 | 15 |
| 隐私和数据合规 | 10 |
| 追踪和拒付可解释 | 10 |
| 创意和关键词低误导 | 10 |
| 现金流和扣量可承受 | 5 |

准入规则：

- 总分 < 75：不测。
- 平台允许性 < 15：不测。
- 资质/认证为 0：敏感垂类不测。
- 任何需要规避审核、隐藏主体或换号的机会：不测。

## 11. 系统落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录垂类、国家、Offer 限制和政策备注 | `/offers` |
| 用 policy_score 和 source_score 影响机会评分 | `/calculators` |
| 创意生成时避免高风险承诺 | Offer 详情页创意生成 |
| 投放前记录风险和来源 URL | `/risk-audits`、`/sources` |
| 导出 Campaign 草稿前人工审核 | `/campaigns` |
| 指标导入后看扣量和拒付 | `/metrics/import`、`/optimization` |
| 账号或广告限制进入申诉 SOP | 账号健康文档 |

系统不做：

- 不绕过认证。
- 不伪装主体或官方身份。
- 不通过 cloaking/换链接过审。
- 不切换账号继续敏感违规 Offer。
- 不生成虚假资质、虚假评论或虚假结果承诺。

## 12. 信息来源 URL

- Google Ads policies, Financial products and services: https://support.google.com/adspolicy/answer/2464998
- Google Ads policies, Healthcare and medicines: https://support.google.com/adspolicy/answer/176031
- Google Ads policies, Gambling and games: https://support.google.com/adspolicy/answer/15132179
- Google Ads policies, Personalized advertising: https://support.google.com/adspolicy/answer/143465
- Google Ads policies, Housing, employment, and credit FAQ: https://support.google.com/adspolicy/answer/9997418
- Google Ads policies, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads policies, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads policies, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads policies, Apply to advertise certain products and services: https://support.google.com/adspolicy/answer/16114090
- Google Ads Blog, Restricting ads in third-party tech support services: https://blog.google/products/ads/restricting-ads-third-party-tech-support-services/
- FTC, The FTC's Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides
