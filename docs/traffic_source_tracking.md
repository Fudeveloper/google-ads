# 流量源与追踪归因手册

更新时间：2026-06-08

本文解释 Ads 套利中“流量源、追踪、归因、扣量对账”的核心原理和日常流程。它只覆盖真实流量、真实用户行为和可审计归因，不提供补点击、刷展示、模拟自然流量、cloaking、代理/指纹规避或后台 Cookie 操作方案。

## 1. 为什么这是套利核心

Ads 套利的利润不是由单个平均值决定，而是由每个细分流量单元决定：

```text
细分利润 = 细分收入 - 细分买量成本 - 扣量/拒付风险 - 现金流成本 - 人工和工具成本
```

“细分流量单元”至少要能拆到：

- 流量平台：Google Ads、Bing、Native、Social、Direct buy。
- Campaign / Ad group / Keyword / Placement / Creative。
- 国家、语言、设备、浏览器、时段。
- Landing page 版本、Offer、变现方、结算模型。

如果只能看到账户总花费和总收入，就无法判断是哪个关键词、素材、国家、设备或页面版本赚钱。套利团队真正的能力，是把流量拆到可行动的颗粒度，然后持续执行“保留、暂停、降价、换页、换 Offer、扩量”的决策。

## 2. 行业里的流量源分层

| 层级 | 典型来源 | 用户意图 | 常见问题 | 适合动作 |
| --- | --- | --- | --- | --- |
| 高意图搜索 | Google Search、Bing Search | 用户主动搜索问题或产品 | CPC 高、竞争强、政策要求高 | 做长尾词、比较页、计算器、指南页 |
| 半意图推荐 | Native、内容推荐、Discovery | 用户被内容吸引 | 标题党、页面不一致、扣量风险 | 严控素材承诺和页面相关性 |
| 社交流量 | Facebook、TikTok、Reddit 等 | 兴趣/人群驱动 | 转化链路长、归因波动 | 用人群角度和内容页预热 |
| 站点直采 | 媒体包量、Newsletter、合作流量 | 取决于媒体质量 | 来源不透明、便宜流量异常 | 要求样例 URL、报表、灰度测试 |
| 低质/不可控 | 流量交换、激励访问、弹窗垃圾源 | 弱或无真实意图 | 无效流量、扣量、封号 | 拒绝，不进入测试 |

评估流量源不是问“便宜不便宜”，而是问：

1. 来源是否可解释：能否看到投放位置、关键词、页面、媒体清单或 audience 逻辑。
2. 用户是否有真实意图：是否符合广告承诺和落地页内容。
3. 是否可分段：能否带上 campaign、placement、creative、keyword、device、geo 等参数。
4. 是否可停量：发现异常时能否快速暂停某个 source、placement、publisher 或 ad group。
5. 是否可对账：能否把买量点击、站内 session、变现收入、Offer conversion 串起来。

## 3. 流量源尽调清单

购买或放大任何来源前，先问供应方或内部投手：

| 问题 | 合格答案 | 高风险答案 |
| --- | --- | --- |
| 广告会出现在哪里 | 可给样例 URL、placement、关键词或媒体包 | 只说“优质流量”“内部资源”，不给样例 |
| 用户怎么到达页面 | 明确搜索、内容推荐、社交、邮件或直采 | 交换流量、激励访问、自动浏览、弹窗链 |
| 是否允许第三方追踪 | 允许 UTM、ValueTrack、click_id、SubID | 不允许追踪或参数会被剥离 |
| 是否能按来源暂停 | 可按 campaign、publisher、placement、keyword 暂停 | 只能整体买包，无法隔离 |
| 是否有历史质量证据 | 有转化率、跳出率、停留、扣量、退款数据 | 只承诺低价和大流量 |
| 是否匹配 Offer 限制 | 明确允许 search/native/social/brand/no-incent | 不知道或要求隐藏来源 |

拒绝标准：

- 无法说明广告展示位置和流量获取方式。
- 价格明显低于同类来源，却无法解释库存质量。
- 要求隐藏 referrer、去掉追踪参数、替换用户代理或走不可解释跳转链。
- 流量来源包含激励点击、自动访问、流量交换、机器人或“补自然”话术。
- 不能按 source 或 placement 停量，事故时只能整体停。

## 4. 追踪字段命名

建议统一字段：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `traffic_source` | 流量平台或供应商 | `google_ads` |
| `traffic_medium` | 媒介 | `cpc`、`native`、`email` |
| `campaign_id` | 投放活动 ID | `ga-us-tax-202606` |
| `ad_group_id` | 广告组或素材组 | `refund-calc-mobile` |
| `keyword` | 搜索词或关键词 | `{keyword}` |
| `match_type` | 匹配类型 | `{matchtype}` |
| `creative_id` | 素材 ID 或角度 | `proof-v2` |
| `placement` | 展示位置或 publisher | `{placement}` |
| `device` | 设备 | `{device}` |
| `geo` | 国家/地区 | `US` |
| `landing_version` | 落地页版本 | `lp-a3` |
| `offer_id` | Offer 或变现配置 | `cloud-backup-01` |
| `click_id` | 单次点击 ID | `clk_...` |
| `subid1..subid5` | 联盟/追踪平台透传字段 | `campaign/adgroup/creative/source/device` |
| `gclid` | Google Ads 自动标记点击 ID | 自动生成 |

命名原则：

- 同一个概念只用一个字段名，不要 `campaign`、`camp`、`utm_campaign` 混用。
- 字段值不要写中文、空格和临时备注，方便 CSV、SQL 和报表处理。
- `click_id` 必须是一跳一值，用于转化回传和去重。
- `subid` 不放个人敏感信息，只放 campaign/source/creative 等运营维度。

## 5. Google Ads URL 和 ValueTrack 原理

Google Ads 的追踪可以用三层结构理解：

1. Final URL：用户最终应访问的真实页面。
2. Tracking template：用于把点击先交给追踪系统记录，再把用户带到 Final URL。
3. Final URL suffix / URL parameters：追加到落地页 URL 的追踪参数。

安全原则：

- Final URL 必须是用户真实看到的目的地，广告承诺、页面内容、域名和最终页面要一致。
- Tracking template 只能用于测量和归因，不能用于隐藏真实目的地、审核页/用户页分流或绕过政策。
- 跳转链要可解释、HTTPS、服务端可用，并用 Google Ads 的 Test 功能验证。

Google Ads ValueTrack 会在点击发生时把占位符替换成点击上下文。示例：

```text
Final URL:
https://example.com/tax-refund-calculator

Final URL suffix:
utm_source=google&utm_medium=cpc&utm_campaign=tax_refund_us&utm_content=proof_v2&kw={keyword}&match={matchtype}&device={device}&network={network}
```

如果使用第三方追踪模板，结构应保持透明：

```text
Tracking template:
https://trk.example.com/click?url={lpurl}&src=google&kw={keyword}&match={matchtype}&device={device}&creative={creative}
```

这里的 `trk.example.com` 只记录真实点击和参数，然后把用户带到 `{lpurl}`。它不应该根据审核机器人、IP、Cookie、设备指纹或账号状态给不同页面。

## 6. GA4 UTM、自动标记和口径

GA4 对流量来源的理解有三个层级：

- First user source/medium/campaign：用户首次被获取时的来源。
- Session source/medium/campaign：当前 session 的来源。
- Event 或 conversion attribution：具体事件归因。

常用 UTM：

```text
utm_source=google
utm_medium=cpc
utm_campaign=tax_refund_us
utm_id=ga_tax_us_202606
utm_content=proof_v2
utm_term=refund_calculator
```

实践建议：

- Google Ads 与 GA4 已打通时优先保留自动标记 `gclid`，同时确保最终 URL 不剥离参数。
- 如果手动 UTM 和自动标记并用，要把 `utm_source`、`utm_medium`、`utm_campaign`、`utm_id`、`utm_source_platform` 等关键项补齐，避免报表出现 `(not set)` 或错误归因。
- 站内报表按 session 统计，广告后台按 click 统计，Offer/AdSense 按 conversion 或 revenue 统计，三者天然不会完全一致。
- 对账不要强行让 click = session，而要关注差异率是否稳定、是否集中在某个设备/浏览器/来源。

## 7. Affiliate / S2S Postback 原理

CPA/CPL 套利常见链路：

```text
Ad click
  -> Landing page
  -> Tracker 生成 click_id
  -> Offer URL 携带 subid/click_id
  -> 用户在广告主或联盟页面转化
  -> 联盟通过 S2S postback 回传 click_id、payout、transaction_id
  -> Tracker 把转化归因到原点击
```

核心字段：

| 字段 | 作用 |
| --- | --- |
| `click_id` | 把转化匹配回原点击 |
| `transaction_id` | 去重，防止重复记账 |
| `payout` | 实际收入 |
| `currency` | 币种 |
| `event` | lead、sale、signup、qualified_lead 等 |
| `status` | approved、pending、rejected |
| `subid` | 透传 source/campaign/creative/placement/device |

正确理解：

- Postback 是归因和对账机制，不是制造转化的机制。
- 如果没有原始真实点击 ID，就不能凭空生成转化。
- 如果 Offer 或联盟拒绝说明扣量原因，必须提高安全系数或拒绝放量。
- `transaction_id` 必须去重；重复 postback 不能重复计收入。

## 8. 对账表

每天至少做 4 张表：

| 表 | 来源 | 粒度 | 用途 |
| --- | --- | --- | --- |
| 买量花费 | Google Ads / 其他来源 | campaign/ad group/keyword/device/day | 成本和 CPC |
| 站内行为 | GA4 / server log | session/source/landing/day | 页面质量和参数完整性 |
| 变现收入 | AdSense/AdX/联盟/直客 | offer/source/day 或 channel/day | RPV/EPC/RPM |
| 风险与扣量 | 联盟结算、AdSense 扣减、Policy Center | source/offer/month | 真实可收回收入 |

关键差异：

```text
Click -> Session 差异率 = 1 - sessions / ad_clicks
Revenue lag = 回传收入日期 - 点击日期
Deduction rate = rejected_or_deducted_revenue / gross_revenue
Net ROI = (approved_revenue - cost) / cost
```

异常判断：

- Click 很高但 Session 很低：参数丢失、页面慢、跳转错误、机器人点击、移动端失败。
- Session 高但 Revenue 为 0：Offer 不匹配、页面 CTA 弱、追踪断、变现方延迟。
- Revenue 初期好、结算大扣量：来源质量不稳定或 Offer 风控滞后。
- 某来源 CTR/CVR 异常高：先查是否激励、自动点击、素材误导、页面不一致。

## 9. 流量测试节奏

### 9.1 最小测试

建议一个测试单元只改一个主变量：

```text
国家 + 设备 + 流量源 + 页面版本 + Offer + 素材角度
```

预算：

- 搜索高意图：至少覆盖 50-100 次点击，看搜索词和页面行为。
- Native/Social：至少覆盖 3-5 个素材角度，每个角度保留足够展示和点击。
- CPA/CPL：至少跑过 1 个回传延迟窗口，不用第一天收入判断全部结果。

### 9.2 放量条件

满足这些条件再扩量：

- 参数完整率稳定，来源、campaign、creative、device 都能回溯。
- Click -> Session 差异率稳定，没有某一来源突然断崖。
- 至少一个结算周期内扣量可接受，拒付原因可解释。
- 页面没有政策警告，广告承诺和页面内容一致。
- 扩量后仍可按 campaign/placement/keyword/source 迅速停量。

### 9.3 停量条件

立刻暂停或隔离：

- 无法解释的点击、展示、session 激增。
- 单一来源带来高点击、低停留、零收入。
- 流量供应方不提供 placement/source 明细。
- Offer 风控反馈某 source 或 subid 质量异常。
- 广告平台、AdSense、联盟或直客出现政策/无效流量警告。

## 10. 常见追踪事故

| 事故 | 表现 | 修复 |
| --- | --- | --- |
| UTM 只填一半 | GA4 出现 `(not set)` 或来源错乱 | 统一 URL 模板，缺字段不得上线 |
| `gclid` 被跳转剥离 | Google Ads 与 GA4 对不上 | 检查重定向、HTTPS、最终 URL 参数保留 |
| Tracking template 没带 `{lpurl}` | 点击无法到达页面 | 用 Test 功能验证落地页 URL |
| click_id 未传给 Offer | 有点击无转化归因 | Offer URL 必须携带联盟要求的参数 |
| postback 重复入账 | 收入虚高，月末被扣 | 用 `transaction_id` 去重 |
| 时区不一致 | 日报成本和收入错位 | 统一报表时区，单独记录收入回传日期 |
| 设备/国家字段缺失 | 无法判断放量方向 | URL 参数和导入 CSV 都要保留维度 |
| 素材承诺与页面不一致 | 转化短期高、长期扣量和封禁风险高 | 重新审计素材与落地页一致性 |

## 11. 本系统如何落地

当前系统以“记录、导入、导出、审计”为主：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer、tracking URL、政策限制 | `/offers` |
| 做 RPV/EPC/CPC 安全测算 | `/calculators` |
| 生成可人工审核的 Campaign 草稿 | `/campaigns` |
| 导出 Google Ads Editor CSV | `/campaigns/<id>/export.csv` |
| 导出 Google Ads Scripts JSON 草稿 | `/campaigns/<id>/export.script.json` |
| 导入每日成本、点击、转化、收入 | `/metrics/import` |
| 根据指标生成停量/优化建议 | `/optimization` |
| 记录高风险来源和政策证据 | `/risk-audits`、`/sources` |
| 管理合规链接轮换计划 | `/links` |

本系统不做：

- 不接管 Google Ads Cookie 或后台 UI。
- 不绕过登录、2FA、安全挑战。
- 不模拟点击、展示、session 或转化。
- 不隐藏真实目的地，不做审核页/用户页分流。
- 不用代理、指纹、Worker 转发规避关联检测。

## 12. 信息来源 URL

- Google Ads Help, About tracking in Google Ads: https://support.google.com/google-ads/answer/6076199
- Google Ads Help, About ValueTrack parameters: https://support.google.com/google-ads/answer/2375447
- Google Ads Help, Set up tracking with ValueTrack parameters: https://support.google.com/google-ads/answer/6305348
- Google Ads Help, About auto-tagging: https://support.google.com/google-ads/answer/3095550
- Google Analytics Help, Traffic-source dimensions, manual tagging, and auto-tagging: https://support.google.com/analytics/answer/11242870
- Google Analytics Help, Campaigns and traffic sources: https://support.google.com/analytics/answer/11242841
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google AdSense Help, Traffic provider checklist: https://support.google.com/adsense/answer/3332805
- Google AdSense Help, Set up a traffic segmentation plan: https://support.google.com/adsense/answer/2583698
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Voluum Documentation, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
