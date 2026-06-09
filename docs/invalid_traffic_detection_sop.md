# 无效流量识别、异常监控与来源隔离 SOP

更新时间：2026-06-08

本文说明 Ads 套利团队如何识别无效流量、异常点击、异常展示、误点、低质量来源、扣量和 ad serving limit 风险，并建立来源隔离、证据保存和复盘流程。本文不提供补点击、刷展示、模拟自然流量、代理/指纹伪装、自动浏览、流量清洗伪装或绕过平台检测的方法。

## 1. 定义和边界

无效流量不是单一现象，而是一组“不能代表真实用户意图”的点击、展示、访问或互动：

- 自动工具、机器人、脚本、爬虫。
- 人为或软件制造的重复点击、展示、访问。
- 激励点击、付费点击、流量交换。
- 误导性按钮、广告伪装、误点。
- 来源不可解释的突增流量。
- 低质量供应商把非真实用户行为卖给发布商或广告主。

本系统的边界：

- 做检测、记录、隔离、停量和复盘。
- 不生成访问、点击、展示或转化。
- 不用代理、指纹、Worker 转发掩盖异常来源。
- 不把异常流量“洗成自然流量”。

## 2. 无效流量的两面

Ads 套利同时站在广告主和发布商两侧：

| 视角 | 风险 | 结果 |
| --- | --- | --- |
| 买量端 | Google Ads 里买到低质量或无效点击 | 花费浪费、Invalid clicks、ROI 失真 |
| 发布商端 | AdSense/AdX/GAM 收到无效广告请求/点击/展示 | 收入扣减、ad serving limited、账号风险 |
| Affiliate 端 | Lead 或 conversion 低质、重复、伪造 | scrub、reject、hold、封 Offer |
| 用户体验 | 广告伪装、误点、跳转异常 | 投诉、政策问题、长期变现下降 |

所以检测不能只看一个平台。要串：

```text
ad clicks -> sessions -> page behavior -> ad requests/impressions/clicks
-> conversions -> approved/finalized revenue -> deductions
```

## 3. 核心监控指标

| 指标 | 异常表现 | 可能原因 |
| --- | --- | --- |
| Click -> Session rate | 突然下降 | 无效点击、页面慢、跳转错误、参数丢失 |
| Sessions -> Page views | 异常低或异常高 | 秒退、自动翻页、页面循环 |
| Time on page | 大量极低 | 低意图或机器人 |
| Ad CTR | 远高于历史 | 误点、诱导点击、广告伪装、异常来源 |
| Ad requests/session | 突然升高 | 广告位重复请求、自动刷新、异常页面 |
| Revenue/session | 突然升高 | 短期异常、可能后续扣量 |
| Estimated -> finalized delta | 下调变大 | 无效流量扣减、质量问题 |
| Approved rate | 下降 | Lead 质量差、Offer 限制不匹配 |
| Invalid click rate | 上升 | Google Ads 过滤到无效点击 |
| Source concentration | 单一来源突然放大 | 供应商异常或投放失控 |

## 4. 异常信号分级

| 等级 | 信号 | 动作 |
| --- | --- | --- |
| P0 | AdSense disabled、Google Ads 账号暂停、重大扣量 | 全面暂停相关来源，启动事故复盘 |
| P1 | ad serving limited、source 扣量突增、Google Ads invalid traffic credit 明显 | 暂停 source/campaign，保留证据 |
| P2 | click/session 断崖、ad CTR 异常、single source 激增 | 降预算或隔离，观察 24-72h |
| P3 | 小幅波动、报表延迟、单日 RPM 异常 | 标记观察，不直接放量 |

不要把 P3 当灾难，也不要把 P1 当正常波动。

## 5. 来源隔离

每个新来源都要独立识别：

```text
source_id
platform
campaign_id
ad_group_id
creative_id
placement / publisher
device
country
landing_version
offer_id
```

隔离原则：

- 新供应商单独 source id。
- 新渠道单独 campaign 或至少单独 URL 参数。
- 新页面版本单独 landing_version。
- 高风险来源不和稳定来源混入同一个报表口径。
- 不能按 source 停量的来源，不进入放量。

如果无法定位异常来源，只能整体停量，这说明追踪设计本身失败。

## 6. 检测流程

每日流程：

1. 拉取买量 clicks/cost。
2. 拉取站内 sessions/page views/time on page。
3. 拉取发布商 estimated revenue/ad metrics。
4. 拉取 affiliate pending/approved/rejected。
5. 按 source/campaign/device/country 对账。
6. 标记异常来源。
7. 写入风险审计和任务。

每周流程：

- 复盘 invalid click rate、扣量、rejected leads。
- 检查供应商和 source 的排名。
- 更新黑名单和观察名单。
- 复查广告位、页面和 CTA 是否有误点风险。
- 对低质量来源降低测试预算或永久拒绝。

月度流程：

- 用 finalized/paid revenue 重算 ROI。
- 统计 deduction rate。
- 更新来源评分、Offer 评分和安全系数。
- 复盘账号健康和 Policy Center。

## 7. 异常来源处理

处理步骤：

```text
发现异常
-> 暂停或降预算
-> 保存指标和页面证据
-> 按 source/campaign/device/landing 分段
-> 联系供应商或平台支持
-> 等待 finalized/approved 结果
-> 更新来源评分
-> 决定恢复、降级或永久拒绝
```

证据包：

- 日期和时区。
- campaign、source、placement、device、country。
- click、session、ad request、impression、CTR、revenue。
- 页面截图和广告位截图。
- tracking URL 和参数。
- 供应商报表。
- 平台通知、Policy Center、invalid traffic credit 或扣量截图。

## 8. 供应商黑名单条件

直接拒绝或永久停用：

- 不提供 source/publisher/placement 明细。
- 要求隐藏 referrer、去掉 UTM、去掉 click_id。
- 提供“模拟自然”“真实用户行为补量”“防扣量”话术。
- CTR/CVR 短期极高，approved/finalized 收入极差。
- 多次出现 invalid traffic 或扣量，不解释原因。
- 要求使用代理、指纹、Worker 转发或 cloaking。
- 变更来源不通知。

## 9. Google Ads invalid clicks

Google Ads 会识别并过滤无效点击，并提供 invalid clicks / invalid click rate 等指标或账单 credit。但团队不能只依赖平台过滤：

- 平台过滤有延迟。
- 不同报表口径可能不同。
- 用户到站后行为仍需要自己分析。
- 被过滤的点击不一定出现在 GA4 session 中。

实践：

- 在 Google Ads 报表中加入 invalid clicks / invalid click rate。
- 按 campaign、network、device、location、hour 分段观察。
- 高异常来源不要只等 credit，先降预算或暂停。
- 避免用短期点击激增判断“机会来了”。

## 10. AdSense / AdX invalid traffic

发布商端核心原则：

- 发布商对广告流量质量负责。
- 不能点击自己的广告。
- 不能鼓励、诱导或奖励用户点击广告。
- 不能用自动工具增加展示或点击。
- 不能把广告放在导致误点的位置。

响应：

- 出现 ad serving limited 或 invalid traffic 提醒时，先停异常来源。
- 降低广告密度和误点风险。
- 检查 traffic provider 和 source segmentation。
- 保存修复证据。
- 不通过“补自然流量”稀释异常。

## 11. 系统落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录来源和供应商证据 | `/sources` |
| 记录异常、扣量、停量和修复 | `/risk-audits` |
| 导入每日 cost/click/revenue/conversion | `/metrics/import` |
| 生成亏损和低收入优化建议 | `/optimization` |
| 创建 URL 检查、报表检查、导出检查任务 | `/tasks` |
| 通过审计日志追踪停量和链接变更 | `/logs` |
| 用来源评分参与机会评估 | `/calculators` 的 source_score |

未来可扩展：

- `source_id` 字段。
- `invalid_clicks`、`invalid_click_rate`。
- `ad_requests`、`ad_impressions`、`ad_ctr`。
- `estimated_revenue`、`finalized_revenue`、`deduction`。
- `approved_revenue`、`rejected_revenue`、`rejection_reason`。

但这些扩展仍只用于检测和复盘，不用于生成或伪装流量。

## 12. 信息来源 URL

- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Help, How Google prevents invalid traffic: https://support.google.com/adsense/answer/1348752
- Google AdSense Help, Traffic provider checklist: https://support.google.com/adsense/answer/3332805
- Google AdSense Help, Set up a traffic segmentation plan: https://support.google.com/adsense/answer/2583698
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google Ads Help, Managing invalid traffic: https://support.google.com/google-ads/answer/11182074
- Google Ad Traffic Quality, How we prevent it: https://www.google.com/ads/adtrafficquality/how-we-prevent-it/
- Google Ad Traffic Quality, Resources for publishers: https://www.google.com/ads/adtrafficquality/publishers/
- Google Ads API, metrics fields: https://developers.google.com/google-ads/api/fields/v23/metrics
- Google AdSense Help, Deductions from earnings FAQs: https://support.google.com/adsense/answer/2808531
