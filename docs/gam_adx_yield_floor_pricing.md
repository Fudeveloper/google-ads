# GAM / AdX Yield、Floor Price 与 Pricing Rules 手册

更新时间：2026-06-08

本文说明 Ads 套利发布商在 Google Ad Manager（GAM）、AdX、Open Bidding、Header Bidding、直客和第三方需求源中，如何理解 yield、floor price、unified pricing rules、line item priority、dynamic allocation、yield group、fill rate、eCPM 和 finalized revenue。目标是帮助团队判断“提高 floor 是否真的提高可收款收入”，而不是用虚假请求、自动刷新、误点、MFA 堆广告或隐藏库存质量来抬短期 RPM。

## 1. 为什么 Yield 决定收入上限

发布商套利收入不是简单的：

```text
sessions * page RPM
```

更真实的链路是：

```text
sessions
-> ad requests
-> eligible demand
-> auction / allocation
-> filled impressions
-> viewable impressions
-> advertiser value
-> estimated revenue
-> finalized / paid revenue
```

Yield 管理要回答：

- 哪些 demand source 有资格竞价？
- 哪些 line item、AdX、Open Bidding、直客或 header bidding 互相竞争？
- 底价是否过滤了低价需求，也是否过滤了本可成交的需求？
- 高 eCPM 是否以低 fill、低 viewability 或高扣量为代价？
- 最终收入是由真实用户价值提升，还是由短期竞价配置波动带来？

套利团队常见误区：

- 只看 eCPM 上升，不看 fill 下降和 session RPM。
- 只看 estimated revenue，不看 finalized revenue 和无效流量扣量。
- floor 一调高就扩量，忽略国家、设备、广告位、页面模板差异。
- 把低填充误诊为“流量不够自然”，而不是 demand、policy、floor 或供应链问题。

## 2. 核心对象

| 对象 | 作用 | 套利团队要理解什么 |
| --- | --- | --- |
| Ad unit | 广告库存单元 | 页面位置、尺寸、设备和模板会影响需求 |
| Line item | GAM 中的投放/需求配置 | priority、goal、rate、targeting 决定竞争资格 |
| AdX / Exchange | 程序化竞价需求 | CPM、floor、买方过滤和供应链质量影响收入 |
| Open Bidding | 第三方 exchange 与 Google demand 竞争 | 增加需求但增加复杂度和对账要求 |
| Header Bidding | 页面端多 SSP 竞价 | 延迟、隐私、供应链和报表复杂度更高 |
| Unified Pricing Rules | 对 Open Auction、First Look、Private Auction 等设置统一价格规则 | floor 影响 eligible demand 和 fill |
| Yield Group | GAM 中组织多个 yield partner 的方式 | 需要按 partner、country、device、ad unit 复盘 |
| Dynamic allocation | GAM 让高价值 demand 与保留库存竞争的机制 | 不同 priority 和 demand channel 的竞争关系 |

## 3. Floor Price 不是越高越好

Floor price 的作用是设定某些库存的最低成交价格。它可以减少低价成交，但也可能降低 fill。

基础公式：

```text
Revenue = filled_impressions * eCPM / 1000
Session RPM = revenue / sessions * 1000
```

如果 floor 从 0.20 调到 0.80：

- eCPM 可能上升。
- filled impressions 可能下降。
- viewability 和 CTR 可能变化。
- 部分国家/设备可能 no fill。
- session RPM 可能上升，也可能下降。

所以 floor 实验必须同时看：

```text
ad_requests
eligible_requests
filled_impressions
fill_rate
eCPM
viewability
ad_CTR
estimated_revenue
finalized_revenue
session_RPM
deduction_rate
```

## 4. Unified Pricing Rules

Unified pricing rules 用于对多种程序化交易设置统一的价格规则。对套利团队来说，它的风险在于范围和粒度：

| 粒度 | 常见用途 | 风险 |
| --- | --- | --- |
| network-wide | 全站最低保护 | 一次改动影响所有国家、设备、广告位 |
| ad unit | 按广告位设底价 | 需要广告位级报表和样本 |
| country / geo | 高低价值地区分开 | 时区、流量质量、扣量要分开看 |
| device | mobile/desktop 差异 | 移动端误点和页面体验风险不同 |
| inventory size | 尺寸维度 | 尺寸变化可能影响 fill 和 viewability |
| demand channel | 区分 auction / deal | 可能影响直客、PMP、Open Auction 关系 |

操作原则：

1. 不在全站一刀切调 floor。
2. 每次只改一个主要变量。
3. 先小流量、短窗口测试，再等结算周期复盘。
4. 不把高 eCPM 当作唯一成功指标。
5. 记录规则版本、变更人、原因和回滚点。

## 5. Dynamic Allocation 和 Line Item Priority

GAM 中不同 demand source 并不是简单“谁出价高谁赢”。Line item priority、目标、频次、库存可用性、直接订单和程序化竞价都会影响分配。

套利团队要关心：

- 直客或 sponsorship 是否被程序化需求挤压。
- House / fallback 是否掩盖了 no fill 问题。
- price priority、network、bulk、sponsorship 等 line item 是否目标和优先级合理。
- AdX/Open Bidding 是否有机会和保留库存竞争。
- 规则改动后是否影响了关键广告位或高价值国家。

常见事故：

| 现象 | 可能原因 |
| --- | --- |
| fill 突降 | floor 太高、targeting 过窄、policy 限制、需求源失效 |
| eCPM 升高 revenue 下降 | 高底价过滤了大量可成交展示 |
| 直客 delivery 不足 | 程序化或其他 line item 竞争/优先级设置错误 |
| 程序化收入波动 | buyer filtering、supply chain、floor、viewability 或来源变化 |
| fallback 占比升高 | 需求不足或规则阻塞高价值 demand |

## 6. Open Bidding / Header Bidding 边界

增加需求源可能提高竞争，但也增加：

- 延迟。
- 隐私和 consent 要求。
- ads.txt / sellers.json / schain 复杂度。
- 买方质量和恶意广告审查。
- 报表对账成本。
- 扣量和争议来源。

接入前应确认：

- 页面和流量来源稳定。
- 已有 ad unit / country / device 级基线。
- 有能力按 partner 复盘 bid request、fill、eCPM、revenue、deduction。
- 供应链透明度已检查。
- 遇到恶意广告或低质量需求有 block / review 流程。

不要在套利冷启动阶段叠加多个 demand partner。先证明真实用户、页面质量和基础收入口径稳定。

## 7. Yield 实验设计

一次 yield 实验的变量应明确：

```text
site/domain
page_template
ad_unit
country
device
demand_channel
pricing_rule_version
floor_price
start_time
end_time
rollback_rule
```

观察指标：

| 指标 | 为什么看 |
| --- | --- |
| ad_requests | 流量和广告调用是否稳定 |
| matched_requests / fill | floor 和需求源是否过滤过多 |
| impressions | 实际可卖展示 |
| viewability | 买方价值和广告位质量 |
| eCPM | 单展示价值 |
| revenue | 总收入 |
| session RPM | 套利买量真正关心的收入分母 |
| deduction / finalization ratio | 是否可收款 |
| latency / CLS | yield 改动是否伤页面体验 |

最小判断：

- 不用少量单日样本判断。
- 国家、设备、广告位必须分层。
- 至少等一个收入结算或扣量窗口复盘高风险来源。
- 如果 revenue 增长来自高 CTR、低 finalized 或异常 source，应先风险审计。

## 8. Floor 调整决策树

```text
eCPM 低
-> fill 是否高？
   -> 是：可小幅测试 floor，上限按 ad unit/country/device 分层
   -> 否：先查 demand、policy、ads.txt/schain、consent、viewability

eCPM 高但 revenue 低
-> fill 是否下降？
   -> 是：floor 过高或需求不足，降回上一版本
   -> 否：查流量量级、viewability、session depth

estimated 高但 finalized 低
-> 查 invalid traffic、误点、source、ad layout、buyer disputes
-> 不扩量，不继续抬 floor
```

## 9. 常见事故

| 事故 | 表现 | 修复 |
| --- | --- | --- |
| 全站 floor 过高 | coverage 下降、no fill 上升 | 回滚，按国家/广告位分层测试 |
| 低价值国家套用高价值 floor | 某些 geo revenue 消失 | geo 分组规则 |
| Header bidding latency 上升 | landing/session 体验下降、广告展示变少 | 减少 partner、优化 timeout |
| Open Bidding partner 低质 | eCPM 低、恶意广告或扣量 | block / review / 暂停 partner |
| 直客 delivery 受影响 | guaranteed campaign 不达标 | 检查 priority、forecast、competition |
| floor 实验没有版本 | 无法判断哪次改动影响 revenue | 建立 pricing_rule_version 和审计日志 |

## 10. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录收入模型和 Offer | `/offers` |
| 导入 cost/revenue 粗口径 | `/metrics/import` |
| 记录 yield、floor、Open Bidding、规则变更风险 | `/risk-audits` |
| 沉淀 Google Ad Manager 和 IAB 来源 | `/sources` |
| 在收入对账中复盘 fill、eCPM、deduction | `revenue_reconciliation_adstack.md` |

后续可扩展表：

```text
gam_pricing_rule_versions
ad_unit_yield_daily
demand_partner_yield_daily
yield_experiments
line_item_delivery_snapshots
```

建议字段：

```text
day
domain
ad_unit
country
device
demand_channel
pricing_rule_version
floor_price
ad_requests
matched_requests
impressions
viewable_impressions
ecpm
estimated_revenue
finalized_revenue
deduction_rate
latency_ms
experiment_status
```

系统边界：

- 不制造 ad requests、impressions 或 clicks。
- 不通过自动刷新、误点、MFA 堆广告提高 yield。
- 不伪造 auction、bid、seller 或 demand source。
- 不绕过买方过滤、供应链透明或发布商政策。

## 11. QA 清单

- pricing rule 有版本、原因、负责人和回滚点。
- floor 按 ad unit / country / device 分层测试。
- 同时看 fill、eCPM、revenue、session RPM 和 finalized revenue。
- Open Bidding / Header Bidding partner 有 ads.txt、sellers.json、schain 和隐私检查。
- 直客、sponsorship、guaranteed line item 不被误伤。
- 异常高 eCPM 或 CTR 要查误点、无效流量和来源质量。
- 收入增长必须经过扣量窗口验证。
- 风险审计中出现“刷请求”“自动刷新抬 RPM”“伪造竞价”“隐藏需求源”等语义时默认 high。

## 12. 信息来源 URL

- Google Ad Manager Help, Unified pricing rules: https://support.google.com/admanager/answer/9298008
- Google Ad Manager Help, Pricing rules: https://support.google.com/admanager/answer/9298008
- Google Ad Manager Help, Dynamic allocation: https://support.google.com/admanager/answer/1143651
- Google Ad Manager Help, Line item types and priorities: https://support.google.com/admanager/answer/177279
- Google Ad Manager Help, Open Bidding: https://support.google.com/admanager/answer/7128453
- Google Ad Manager Help, Yield groups: https://support.google.com/admanager/answer/7386124
- Google Ad Manager Help, Ad Exchange line items: https://support.google.com/admanager/answer/138314
- Google Ad Manager Help, Forecasting: https://support.google.com/admanager/answer/2917835
- Google Ad Manager Help, Ad review center: https://admanager.google.com/home/resources/feature-brief-ad-review-center/
- Google AdSense Help, Metrics glossary: https://support.google.com/adsense/answer/2735899
- Google Publisher Policies Help, Google Ad Manager partner guidelines: https://support.google.com/publisherpolicies/answer/9059370
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
