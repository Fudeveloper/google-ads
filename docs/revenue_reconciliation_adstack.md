# 发布商收入对账、Finalized Revenue 与扣量复盘手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何把买量成本、站内 session、AdSense / AdX / Google Ad Manager 报表、联盟收入、finalized revenue、deduction 和 payment status 对齐。重点是判断“今天看起来赚的钱，最终能不能收回来”。本文只覆盖报表、对账、复盘和预算决策，不提供补展示、刷点击、模拟广告请求、规避无效流量检测或 Cookie 后台接管方法。

## 1. 为什么收入对账是套利生命线

内容套利、搜索套利和混合变现站点的利润不是当天报表里的 `estimated_revenue - cost`，而是：

```text
Paid / finalized revenue
- traffic cost
- deduction
- rejected / scrubbed revenue
- payment delay cost
- content and operation cost
```

很多亏损不是出在 CPC 公式，而是出在口径错配：

- Google Ads 按 click 和 cost 记账，站内按 session 记账，AdSense/GAM 按 ad request、impression、click、estimated revenue 和 finalized revenue 记账。
- 当天 estimated revenue 可能在月初 finalized 时调整。
- 无效流量、广告主付款问题、政策问题、广告服务限制都可能影响最终可收款收入。
- 不按 source、page、device、country 拆收入，就无法知道是哪个流量源造成扣量。

对账能力决定能不能放量。没有经历 finalized revenue 和 payment 的来源，只能小测，不能按表面 ROI 扩量。

## 2. 收入状态模型

建议把所有收入分成以下状态：

| 状态 | 含义 | 是否可用于扩量 |
| --- | --- | --- |
| `reported` | 第三方追踪或页面估算产生的收入 | 只能做方向判断 |
| `estimated` | AdSense/GAM 当月估算收入或联盟 pending payout | 只能按折扣系数使用 |
| `approved` | 联盟或 buyer 已批准但未付款 | 可用于中等置信预算 |
| `finalized` | 发布商平台完成月度结算确认 | 可进入历史模型 |
| `paid` | 已到账 | 可进入现金流模型 |
| `deducted` | 被扣减或追回 | 进入 deduction rate |
| `rejected` | lead/order/conversion 被拒 | 不计收入，必须记录原因 |
| `held` | 付款被 hold 或延迟 | 不可扩量，先处理 hold 原因 |

内部预算不应只看 `revenue` 一个字段，而要知道它处于哪个状态。第一版系统只有聚合 `revenue`，因此建议导入时优先填 approved/finalized/paid revenue；如果导入 estimated revenue，需要在任务、审计或备注里标记状态。

## 3. 对账粒度

最低可用粒度：

```text
day
offer_id / site_id
campaign_draft_id
channel
source / placement / keyword group
country
device
cost
clicks
sessions
ad_requests
ad_impressions
estimated_revenue
finalized_revenue
deduction
paid_revenue
```

第一版系统的 `metrics_daily` 已覆盖 day、offer、campaign、channel、country、device、impressions、clicks、cost、conversions、revenue。它适合做早期 ROI 分析，但月度经营还需要额外对账表或导入文件归档：

- AdSense finalized earnings。
- GAM / AdX historical report。
- AdSense Management API 指标。
- 联盟 approved/rejected/paid report。
- Google Ads cost by campaign/ad group/search term。
- 站内 sessions by source/page/device。

## 4. AdSense 对账

AdSense 侧至少看：

| 指标 | 用途 |
| --- | --- |
| Estimated earnings | 日常趋势，不等于可收款 |
| Finalized earnings | 月度关账依据 |
| Page views / impressions | 判断页面和广告位调用 |
| Clicks / CTR | 异常高可能代表误点或无效流量风险 |
| Page RPM / Impression RPM | 页面、国家、设备和来源的变现能力 |
| Coverage | 请求是否被填充，低覆盖可能是需求、政策或 consent 问题 |
| Active View | 可见率和广告位质量 |
| Deductions | 无效流量、政策或广告主问题造成的收入下调 |

常见对账错误：

- 把当日 estimated earnings 当成可收款现金。
- 只看总收入，不按 URL channel、custom channel、country、device 分拆。
- 只看 RPM，不看 CTR 是否异常、page/session 是否异常、来源是否可解释。
- 看到收入下调后继续买同一来源，而没有做 source isolation。

## 5. GAM / AdX 对账

GAM / AdX 会引入更多维度：

| 维度 | 用途 |
| --- | --- |
| Ad unit | 判断哪个广告位赚钱或造成误点 |
| Line item / demand channel | 区分直客、程序化、AdX、Open Bidding |
| Creative / buyer / advertiser | 识别广告质量和需求方问题 |
| Request / matched request / impression | 排查 fill、coverage 和规则配置 |
| Active View measurable / viewable | 判断广告位是否被真实看到 |
| Revenue / eCPM | 比较广告位和需求通道价值 |
| Policy / creative review | 排查恶意广告、违规素材和品牌安全 |

GAM 对账更像 ad ops 工作：line item、price rule、ad unit、blocking、creative review 和 reporting 设置都会影响收入。套利团队不要在还没有稳定来源和页面质量时过早复杂化 ad stack。

## 6. 扣量复盘

扣量复盘必须回答：

```text
哪一天
哪个 source / campaign / page / ad unit
产生了多少 estimated revenue
最终 finalized / paid 多少
扣了多少
扣量原因是什么
是否可以停止或修复
```

扣量率公式：

```text
deduction_rate = deducted_revenue / estimated_revenue
finalization_ratio = finalized_revenue / estimated_revenue
cash_realization_ratio = paid_revenue / estimated_revenue
```

判断建议：

| 结果 | 动作 |
| --- | --- |
| finalization_ratio 稳定高于 0.9 | 可逐步提高该来源安全系数 |
| 0.75 - 0.9 | 小幅扩量，继续观察 |
| 低于 0.75 | 暂停扩量，按 source/page/ad unit 复盘 |
| 连续两期扣量原因不明 | 降低变现方或来源评分 |
| 同一 source 多次扣量 | 停源，保留证据和沟通记录 |

## 7. Click -> Session -> Revenue 对账

对账链路：

```text
Google Ads clicks
-> landing sessions
-> page views
-> ad requests
-> matched requests / ad impressions
-> ad clicks or viewable impressions
-> estimated revenue
-> finalized revenue
-> paid revenue
```

常见断点：

| 断点 | 可能原因 | 处理 |
| --- | --- | --- |
| clicks 高、sessions 低 | 跳转慢、tracking template 错、移动端问题、bot 过滤 | 查 URL、速度、参数和来源 |
| sessions 高、ad requests 低 | 广告代码未加载、CMP 阻断、模板缺广告位 | 查模板、consent、广告代码 |
| ad requests 高、impressions 低 | coverage 低、政策限制、需求不足 | 查 policy center、国家、页面 |
| impressions 高、revenue 低 | 低价值来源、低可见率、低 eCPM | 查 source、ad unit、Active View |
| estimated 高、finalized 低 | 无效流量、误点、来源质量差 | 停源并复盘页面/广告位 |

注意：这些断点不能通过补点击、模拟 session 或刷展示解决，只能通过追踪、页面、来源和广告位治理解决。

## 8. 月度关账

建议每月固定执行：

1. 锁定 Google Ads cost。
2. 锁定站内 session/pageview。
3. 导出 AdSense finalized earnings。
4. 导出 GAM / AdX historical report。
5. 导出联盟 approved/rejected/paid report。
6. 按 source、page、ad unit、country、device 汇总。
7. 计算 finalization_ratio、deduction_rate、cash_realization_ratio。
8. 更新下月 safety_factor、daily budget cap 和 stop-loss。
9. 归档原始 CSV、截图、账单、付款和沟通记录。
10. 把异常来源写入 `/risk-audits`，把来源政策写入 `/sources`。

## 9. 报表字段规范

建议内部统一字段：

| 字段 | 说明 |
| --- | --- |
| `gross_revenue` | 原始估算或追踪收入 |
| `estimated_revenue` | 平台估算收入 |
| `finalized_revenue` | 月度确认收入 |
| `paid_revenue` | 到账收入 |
| `deducted_revenue` | 扣减收入 |
| `deduction_reason` | 扣量原因 |
| `payment_status` | pending、finalized、paid、held |
| `ad_unit` | GAM/AdSense 广告位 |
| `page_template` | 页面模板 |
| `traffic_source` | 买量来源 |
| `source_id` | 内部 source/subid |

第一版系统的 CSV 仍使用 `revenue`，但运营上应明确它是哪种收入。如果不明确，默认按 `estimated` 处理，并使用安全系数折扣。

## 10. 系统落地

当前系统落地方式：

| 行业动作 | 系统位置 |
| --- | --- |
| 导入 cost/clicks/conversions/revenue | `/metrics/import` |
| 用 safety_factor 和 cash_buffer_days 做机会测算 | `/calculators` |
| 记录扣量、hold、无效流量和来源隔离 | `/risk-audits` |
| 记录 AdSense/GAM/政策/指标来源 | `/sources` |
| 用任务中心安排月度关账 | `/tasks` |
| 在运营文档中固定日报、周报、月报口径 | `ads_arbitrage_operations.md` |

后续可扩展：

- `revenue_settlements`：offer、source、month、estimated、finalized、paid、deducted。
- `publisher_metrics_daily`：page_views、ad_requests、ad_impressions、coverage、active_view、ad_unit。
- `reconciliation_runs`：导入文件、关账时间、差异、处理人。
- 导出月度关账 CSV。

这些扩展仍然只做报表和审计，不生成广告请求、点击、展示或规避检测动作。

## 11. QA 清单

| 检查项 | 放行标准 |
| --- | --- |
| 收入口径 | revenue 字段状态明确：estimated、finalized、approved 或 paid |
| 来源拆分 | 能按 source/campaign/page/device/country 定位 |
| 扣量模型 | 有 deduction_rate 和 finalization_ratio |
| 付款周期 | 知道 expected payment date 和 hold 风险 |
| AdSense/GAM 指标 | page RPM、impression RPM、coverage、Active View 可解释 |
| 异常处理 | 高 CTR、低 coverage、finalized 下调有复盘 |
| 月度关账 | 原始报表、账单、截图和来源证据归档 |
| 放量判断 | 不用未结算 estimated revenue 直接扩量 |
| 风险审计 | 异常来源写入 `/risk-audits` |

## 12. 信息来源 URL

- Google AdSense Help, Metrics glossary: https://support.google.com/adsense/answer/2735899
- Google AdSense Help, Payment timelines: https://support.google.com/adsense/answer/7164703
- Google AdSense Help, Payments FAQs: https://support.google.com/adsense/answer/7164701
- Google AdSense Help, Payment thresholds: https://support.google.com/adsense/answer/1709871
- Google AdSense Help, Deductions from earnings FAQs: https://support.google.com/adsense/answer/2808531
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google AdSense Help, Set up a traffic segmentation plan: https://support.google.com/adsense/answer/2583698
- Google AdSense Management API, Metrics and Dimensions: https://developers.google.com/adsense/management/metrics-dimensions
- Google Ad Manager API, Reporting: https://developers.google.com/ad-manager/api/reporting
- Google Ad Manager API, ReportService: https://developers.google.com/ad-manager/api/reference/latest/ReportService
- Google Publisher Policies Help, Google Ad Manager Partner Guidelines: https://support.google.com/publisherpolicies/answer/9059370
- Google Ad Traffic Quality, How Google prevents invalid traffic: https://www.google.com/ads/adtrafficquality/how-we-prevent-it/
