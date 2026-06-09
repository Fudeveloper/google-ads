# 转化追踪、价值回传与 Attribution 手册

更新时间：2026-06-08

本文解释 Ads 套利中 conversion action、primary / secondary conversions、offline conversions、Enhanced Conversions、click ID、conversion value、attribution window、conversion lag 和 Consent Mode 的关系。目标是让团队把“真实可收回收入”回传给买量和优化系统，而不是让算法优化到 submitted lead、误触点击、pending revenue 或不可收款转化。本文不提供伪造转化、补点击、刷展示、隐藏追踪、绕过用户同意、Cookie 同步滥用或规避平台测量系统的方案。

## 1. 为什么转化追踪决定套利成败

套利业务的优化系统依赖反馈信号：

```text
Paid click -> Landing page -> Event / lead / revenue -> Conversion action -> Bidding / reporting
```

如果反馈信号错了，系统会把预算推向错误流量：

- 把 button click 当成 sale，系统会买更多浅层点击。
- 把 submitted lead 当成 qualified lead，系统会买更多低质量表单。
- 把 reported revenue 当成 paid revenue，系统会忽略扣量和拒付。
- 把所有 Offer 混成一个 conversion action，系统会把不同 payout、延迟和质量混成平均值。
- Consent 或 tag 配置错误，会让 ROI 看起来突然变差或突然变好。

转化追踪不是技术小事，而是套利业务的“反馈神经”。它决定出价系统学什么，团队日报看什么，扩量和止损依据是什么。

## 2. Conversion Action 架构

Google Ads 中，conversion action 是你希望用户完成的有价值动作，例如购买、提交表单、电话、订阅、线下成交或导入的 CRM 状态。多个 conversion actions 可以归到 conversion goal 里，并设置为 primary 或 secondary。

套利团队建议分层：

| 层级 | 示例 | 用途 | 默认 |
| --- | --- | --- | --- |
| Micro event | CTA click、scroll、search action、outbound click | 页面诊断 | Secondary 或内部报表 |
| Submitted lead | 表单提交、电话拨打、chat lead | 冷启动观察 | Secondary，除非质量已验证 |
| Accepted lead | buyer/network 接收 | 初步质量 | 视垂类决定 |
| Qualified lead | buyer 确认可联系且符合资格 | 出价信号 | Primary 候选 |
| Approved / paid conversion | 可计费、已批准或已付款 | 利润优化 | Primary 优先 |
| Refund / reject | 退款、拒付、scrub | 风险反馈 | 不做正向 primary |

原则：

- Primary conversion 应尽量接近可收款价值。
- Secondary conversion 可以用于观察漏斗，但不要让 Smart Bidding 优化到浅层事件。
- 每个 Offer / 垂类 / 国家如果 payout、质量审核和回传延迟差异很大，不应混成一个目标。
- 如果只有 submitted lead 可追踪，出价和预算必须更保守。

## 3. 事件命名和字段规范

建议命名：

```text
lead_submitted_{vertical}_{country}
lead_qualified_{vertical}_{country}
lead_approved_{vertical}_{country}
sale_paid_{vertical}_{country}
adsense_revenue_finalized_{site}_{country}
```

最小字段：

| 字段 | 用途 |
| --- | --- |
| `click_id` / `gclid` / `gbraid` / `wbraid` | 匹配广告点击 |
| `conversion_action` | 区分 submitted、qualified、approved、paid |
| `conversion_time` | 发生时间，注意时区 |
| `conversion_value` | 金额或价值 |
| `currency` | 币种 |
| `transaction_id` | 去重 |
| `status` | pending、approved、rejected、paid |
| `source` / `campaign` / `ad_group` / `keyword` | 内部复盘 |
| `consent_state` | 判断测量可见性和合规边界 |

不要把姓名、邮箱、电话、身份证、完整 IP 或敏感健康/金融信息放进 URL、UTM、subid 或公开日志。

## 4. Click ID 与归因

常见标识：

| 标识 | 说明 | 用途 |
| --- | --- | --- |
| `gclid` | Google click identifier | Google Ads 点击和 offline conversion 匹配 |
| `gbraid` / `wbraid` | 面向部分 iOS / app / web 场景的点击标识 | 通过 API/增强方案处理部分隐私限制场景 |
| `utm_*` | 手动 campaign 维度 | GA4、内部报表、非个人来源分析 |
| `click_id` | 自建随机点击 ID | 联盟 postback 和内部归因 |
| `transaction_id` | 转化唯一 ID | 去重和状态更新 |

原则：

- 点击 ID 是归因证据，不是用户身份画像。
- 跳转链不能剥离 `gclid`、UTM 或内部 `click_id`。
- 同一个转化不能因为多个 postback 重复计收入。
- 没有真实点击 ID 时，不应凭空生成转化回传。
- iOS / consent / browser 限制导致可见度变化时，要在报表中标注，不要用指纹或隐藏存储恢复标识。

## 5. Offline Conversions

Offline conversion import 用于把网站外或延迟发生的结果回传给 Google Ads，例如：

- 线索被 sales 接通。
- 贷款申请通过初审。
- 电话咨询被判定有效。
- 订单线下签约。
- CRM 确认成交或付款。

套利场景的价值：

- 把 submitted lead 和 qualified / paid lead 分开。
- 让 Smart Bidding 看见后端质量。
- 把 reject、scrub、低意图来源从预算里排除。
- 用真实批准收入计算 Target CPA / Target ROAS。

上传原则：

- 使用正确 conversion action 名称。
- 使用点击 ID 或增强转化所需字段匹配。
- conversion time 要接近真实事件时间，时区一致。
- conversion value 要用 approved / paid 口径，而不是虚高 gross 口径。
- 上传后检查 diagnostics、match rate、error 和 processing delay。

## 6. Enhanced Conversions

Enhanced Conversions 使用经过哈希处理的第一方用户提供数据来提升转化测量准确性。它有两类常见场景：

- Enhanced conversions for web：用户在网站上转化，标签发送哈希用户提供数据。
- Enhanced conversions for leads：网站收集 lead，后续离线导入 lead 结果时，用哈希用户数据帮助匹配广告互动。

对套利团队的边界：

- 必须满足 Google Ads customer data policies。
- 页面要有隐私、同意和数据用途披露。
- 只发送必要字段，避免把敏感信息塞进 URL 或日志。
- 对健康、金融、身份等敏感垂类要更谨慎。
- Enhanced Conversions 是补强真实测量，不是绕过 consent 或恢复被拒绝用户标识的工具。

## 7. Conversion Value 设计

Smart Bidding 和 ROI 报表都依赖 value。价值设计要回答：这个事件值多少钱？

| 场景 | 不推荐 value | 推荐 value |
| --- | --- | --- |
| Submitted lead | 固定 payout 全额 | 预估 approval_rate * payout |
| Qualified lead | gross payout | 历史 paid_rate * payout |
| Sale | 订单毛额 | 扣退款、拒付、佣金和税费后的净值 |
| AdSense / AdX | estimated earnings | finalized / paid revenue |
| Search feed | gross revenue | 扣量后 payable revenue |

公式：

```text
expected_value = payout * approval_rate * paid_rate
net_value = revenue_paid - refund - clawback - variable_cost
```

价值设置常见事故：

- 所有 lead 都传同一个 payout，忽略国家、buyer、质量等级。
- 把 gross revenue 用于 tROAS，导致系统高估真实收益。
- 退款或拒付没有负向反馈，系统继续买低质量来源。
- 多个 conversion actions 重复计入同一笔收入。

## 8. Attribution Window 和 Conversion Lag

Attribution window 决定点击或互动后多长时间内发生的转化会被计入。Conversion lag 是点击到转化、转化到回传、回传到报表可见之间的时间差。

套利团队需要记录：

- click_time。
- event_time。
- conversion_time。
- import_time。
- approval_time。
- payable_time。

不要用当天 ROI 判断所有来源：

- 高 payout CPL 可能 7-30 天后才知道质量。
- AdSense/AdX finalized revenue 通常晚于 estimated。
- Offline conversion processing 可能需要时间。
- 数据驱动归因会在多个互动之间分配 credit，日报数字会变化。

日报可看 reported，周报看 approved，月报和扩量看 paid / finalized。

## 9. Attribution Model

Attribution model 解释转化 credit 如何分配给不同广告互动。Google Ads 支持数据驱动归因等模型。对套利团队来说，关键不是争论模型名，而是统一口径：

- 同一实验不要中途切换 attribution model。
- Search、Display、Demand Gen、PMax 混跑时，attribution 会影响渠道 ROI。
- 上游探索型广告可能有 assisted value，但不能替代 payable profit。
- 与 GA4、联盟后台、CRM 的口径差异要在报告中标注。

常见对账事实：

- Google Ads、GA4、联盟后台、CRM 不会天然完全一致。
- Google Ads 按广告互动归因，GA4 有自己的 session/user/event 口径。
- Affiliate postback 按 click_id 或 subid 匹配。
- CRM 按 lead/contact/account 生命周期看。

目标不是让所有数字相等，而是让差异稳定、可解释、可定位。

## 10. 数据 QA 和诊断

上线前检查：

- Conversion action 名称、类别、primary/secondary 设置正确。
- Google tag / GTM / GA4 / Ads link 配置正确。
- Consent defaults 和 updates 在 tag 之前工作。
- Thank-you page、form submit、call、chat、outbound click 不重复触发。
- `gclid`、UTM、click_id 在跳转链里保留。
- transaction_id 去重可用。
- Enhanced Conversions diagnostics 无关键错误。
- Offline conversion upload 有 diagnostics 和错误处理。

每日 QA：

| 异常 | 可能原因 |
| --- | --- |
| Ads clicks 正常，conversions 为 0 | tag 未触发、目标页错、consent 阻断、事件条件错 |
| conversions 暴涨 | 重复触发、浅层事件变 primary、bot/误触 |
| conversion value 暴涨 | 重复 postback、币种错、gross/net 混用 |
| GA4 有转化，Ads 没有 | link/import 设置、attribution、tag、consent、点击 ID 丢失 |
| Offline upload 成功但未归因 | 点击 ID 无效、窗口外、时间错、action name 错、处理延迟 |
| Smart Bidding 学习变差 | primary 目标变更、价值口径变化、样本不足、延迟变长 |

## 11. 系统落地

当前系统支持：

| 业务动作 | 系统位置 |
| --- | --- |
| 导入 cost、clicks、conversions、revenue | `/metrics/import` |
| 记录 Offer payout、限制和政策备注 | `/offers` |
| 保存 UTM、postback、offline conversion、enhanced conversion 来源 | `/sources` |
| 用 ROI、RPV、CVR 生成优化建议 | `/optimization` |
| 记录追踪事故、拒付、Consent 或转化质量风险 | `/risk-audits` |
| 导出投放草稿而不直接修改后台 | `/campaigns` |

后续可扩展但仍安全的能力：

- `conversion_actions`：name、goal、primary/secondary、source、value_mode、owner。
- `conversion_quality_daily`：submitted、qualified、approved、paid、rejected、value。
- `offline_conversion_uploads`：file、rows、matched、errors、imported_at。
- `attribution_reconciliation`：Ads、GA4、CRM、affiliate 差异表。
- 指标导入增加 `revenue_reported`、`revenue_approved`、`revenue_paid`。

不做：

- 不伪造 conversion。
- 不补点击或刷展示来训练 Smart Bidding。
- 不隐藏 tracking 或绕过 consent。
- 不把 PII 放进 URL/subid。
- 不用 Cookie 后台接管 conversion 设置。
- 不自动把浅层事件设为 primary。

## 12. 信息来源 URL

- Google Ads Help, Different ways to track conversions: https://support.google.com/google-ads/answer/1722054
- Google Ads Help, About conversion measurement: https://support.google.com/google-ads/answer/1722022
- Google Ads Help, About primary and secondary conversion actions: https://support.google.com/google-ads/answer/11461796
- Google Ads Help, About enhanced conversions: https://support.google.com/google-ads/answer/9888656
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads API, Manage offline conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-offline
- Google Ads Help, Fix discrepancies and errors in offline conversion imports: https://support.google.com/google-ads/answer/13321563
- Google Ads Help, About attribution models: https://support.google.com/google-ads/answer/6259715
- Google Ads Help, About data-driven attribution: https://support.google.com/google-ads/answer/6394265
- Google Ads Help, About conversion windows: https://support.google.com/google-ads/answer/3123169
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Conversion tracking status troubleshooting: https://support.google.com/google-ads/troubleshooter/13455130
- Google for Developers, Consent mode overview: https://developers.google.com/tag-platform/security/concepts/consent-mode
