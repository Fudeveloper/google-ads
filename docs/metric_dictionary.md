# Ads 套利指标字典与口径

更新时间：2026-06-08

本文用于统一 Ads 套利团队的指标语言。指标口径不统一，会直接导致误判：有人按 Google Ads clicks 算 CPC，有人按 GA4 sessions 算 RPV，有人按联盟平台 conversions 算 CVR，最后看似都对，实际在比较不同东西。

## 1. 分层口径

Ads 套利至少有 5 层数据：

| 层级 | 典型来源 | 说明 |
| --- | --- | --- |
| 广告曝光层 | Google Ads impressions | 广告被展示，不等于用户访问页面 |
| 付费点击层 | Google Ads clicks / cost | 计费和买量优化的核心口径 |
| 页面访问层 | GA4 sessions / server logs | 用户实际到达页面，受加载、同意、重定向和统计影响 |
| 出站点击层 | offer clicks / affiliate clicks | 用户从落地页进入下游 Offer |
| 收入层 | AdSense / AdX / affiliate postback | 变现金额、转化、扣量、延迟和拒付 |

核心原则：不要跨层混算。

例如：

- CPC 应该用广告花费 / 广告点击。
- Landing arrival rate 应该用页面 sessions / 广告点击。
- Offer CTR 应该用出站点击 / 页面 sessions。
- RPV 可以用收入 / 广告点击，也可以用收入 / 页面 sessions，但必须写清分母。

## 2. 买量指标

| 指标 | 公式 | 用途 | 常见误区 |
| --- | --- | --- | --- |
| Impressions | 平台展示数 | 判断覆盖和 CTR 分母 | 展示不代表页面访问 |
| Clicks | 平台点击数 | CPC、买量样本和成本口径 | 与 GA4 sessions 不一定一致 |
| Cost | 平台花费 | ROI、CPC、预算和止损 | 不同币种和时区要统一 |
| CTR | Clicks / Impressions | 判断广告相关性和吸引力 | 高 CTR 可能只是标题党 |
| CPC | Cost / Clicks | 买量成本 | 不应和 AdSense CPC 混淆 |
| Search term | 用户搜索词 | 找负关键词和新关键词 | 只看高点击不看收入会误扩 |
| Quality proxy | CTR、页面相关性、CPC 变化 | 粗略判断广告与页面匹配 | 不是 Google 官方质量得分 |

判断规则：

- CTR 低、CPC 高：优先检查关键词、素材和页面相关性。
- CTR 高、RPV 低：通常是素材承诺过宽或流量意图不对。
- Clicks 高、sessions 低：检查页面速度、跳转、同意弹窗、统计脚本。

## 3. 页面指标

| 指标 | 公式/来源 | 用途 | 注意 |
| --- | --- | --- | --- |
| Sessions | GA4 session 或服务器 session | 到达页面用户规模 | GA4 session scope 与 user scope 不同 |
| Users | GA4 users | 去重用户规模 | 不适合直接和广告 clicks 对齐 |
| Landing arrival rate | Sessions / Ads Clicks | 判断点击到站损耗 | 受统计阻断和页面加载影响 |
| Page engagement | 停留、滚动、二跳、事件 | 判断内容匹配 | 不应用模拟行为修饰 |
| Outbound clicks | Offer click / CTA click | 判断页面转出能力 | 必须按页面版本和 Offer 记录 |
| Offer CTR | Outbound clicks / Sessions | 页面到 Offer 的点击率 | 过高但低转化可能说明误导 |

GA4 口径要点：

- `First user` 维度回答“用户首次从哪里来”。
- `Session` 维度回答“这次会话从哪里来”。
- `Event` 维度回答“某个事件带了什么 campaign/source 信息”。
- 中途出现新的 campaign/source 参数，不一定会改变当前 session 的归因。

套利日报一般优先用 session-scoped acquisition 口径做页面到达分析，再用 click_id/subid 做收入对账。

## 4. 变现指标

| 指标 | 公式/来源 | 用途 | 注意 |
| --- | --- | --- | --- |
| Revenue | AdSense/AdX/联盟收入 | 收入总额 | 可能有延迟、扣量、拒付 |
| RPM | Revenue / impressions 或 sessions * 1000 | 展示或访问变现强度 | 必须注明分母 |
| RPV | Revenue / paid clicks 或 sessions | 单次访问收入 | 套利最关键指标之一 |
| EPC | Revenue / clicks | 联盟常用每点击收益 | 分母可能是 offer clicks，不一定是 ads clicks |
| CPA payout | 单次合格转化金额 | CPA/CPL 测算 | 要看合格条件和拒付 |
| CVR | Conversions / clicks | 转化效率 | clicks 是广告点击、页面出站点击还是 offer click 必须写清 |
| Deduction rate | 1 - payable / reported | 扣量程度 | 要分平台扣量、无效流量、质量拒付 |

AdSense/AdX 场景要分清：

- Impression RPM：按广告展示算。
- Page RPM / Session RPM：按页面浏览或会话算。
- Ad request RPM：按广告请求算。
- Ad session RPM：按广告会话算。

CPA/CPL 场景要分清：

- Lead 是否通过质量审核。
- 是否有回传延迟。
- 是否按国家、设备、来源扣量。
- 是否按重复线索、无效电话、退款或质量评分拒付。

## 5. 利润指标

| 指标 | 公式 | 用途 |
| --- | --- | --- |
| Profit | Revenue - Cost | 绝对利润 |
| ROI | Profit / Cost | 投放效率 |
| ROAS | Revenue / Cost | 收入成本比 |
| Break-even CPC | Revenue / Clicks | 理论盈亏平衡 CPC |
| Safe CPC | RPV * safety_factor | 带风险折扣的最高可买 CPC |
| Payback days | 回款周期 | 现金流压力 |
| Cash buffer | 可支撑测试天数 | 资金安全 |

ROI 与 ROAS 的区别：

- ROI = 0 表示不赚不亏。
- ROAS = 1 表示不赚不亏。
- ROI = 50% 等于 ROAS = 1.5。

团队内部必须统一用哪个指标做扩量判断。套利团队建议以 ROI/Profit 为核心，ROAS 作为辅助。

## 6. 样本和显著性

套利测试经常因为样本太小误判。

经验规则：

- 低 payout / display RPM：需要更多点击和更长时间。
- 高 payout CPA：单次转化波动很大，要看有效线索和拒付。
- 回传延迟长：不能用当天收入直接判断当天花费。
- 国家/设备/关键词差异大：不要把所有流量混成一个平均值。

最小样本建议：

| 场景 | 初始样本 |
| --- | --- |
| Search 高意图 CPA | 100~300 paid clicks |
| Display/Discovery 内容套利 | 500~2000 paid clicks |
| 高 payout 低 CVR | 至少覆盖 3~5 个预期转化 |
| 新页面 RPM 测试 | 至少覆盖多个时段和设备 |

## 7. 回传延迟

收入延迟会让好 Campaign 看起来亏损，也会让坏 Campaign 因延迟收入暂时好看。

记录字段：

- click_time。
- conversion_time。
- postback_time。
- reporting_time。
- payable_time。
- settlement_time。

判断方式：

```text
lag_hours = postback_time - click_time
reporting_lag_days = reporting_time - click_date
payable_lag_days = settlement_time - conversion_date
```

日报里至少要标注：

- 当前收入是否完整。
- 是否有 late conversion。
- 是否按 click date 还是 conversion date 看数据。

Google Ads API metrics 页面也区分部分 by_conversion_date 字段，说明报表口径和日期归属会影响分析。

## 8. 扣量和拒付

扣量不是单一事件，可能来自：

- 无效流量过滤。
- 重复或低质量 lead。
- 国家、设备、来源不符合 Offer 规则。
- 用户退款、取消、欺诈审核。
- 发布商政策或广告主质量审核。
- 统计口径差异。

不要用补点击或模拟自然流量“修扣量”。扣量要通过：

- 来源隔离。
- SubID 追踪。
- 页面承诺修复。
- Offer 规则复核。
- 低质关键词和版位排除。
- 对账证据。

## 9. 常见口径事故

| 事故 | 表现 | 修复 |
| --- | --- | --- |
| CPC 和 AdSense CPC 混用 | 买量成本和发布商点击收益混成一个指标 | 改名为 Ads CPC / Publisher CPC |
| RPV 分母混乱 | 有人按 ads clicks，有人按 sessions | 字段名写成 RPV_ads_click 或 RPV_session |
| GA4 user/session 混用 | 新用户来源和会话来源对不上 | 明确使用 First user 或 Session 维度 |
| click date/conversion date 混用 | 日报和月报收入差异大 | 报表标注日期归属 |
| revenue gross/net 混用 | ROI 虚高 | 分 reported revenue 和 payable revenue |
| 汇率未统一 | 多国家 ROI 不可比 | 固定结算币种和汇率时间 |
| 时区未统一 | 日报边界错位 | 统一平台时区和内部报表时区 |

## 10. 字段命名建议

建议内部字段明确分母：

```text
ads_impressions
ads_clicks
ads_cost
landing_sessions
landing_users
offer_clicks
conversions_reported
conversions_payable
revenue_reported
revenue_payable
rpv_ads_click
rpv_session
epc_offer_click
roi_reported
roi_payable
deduction_rate
postback_lag_hours
```

## 11. 本系统当前口径

`metrics_daily` 目前是 V1 粗口径：

- `impressions`：广告展示。
- `clicks`：广告点击。
- `cost`：广告花费。
- `conversions`：转化数。
- `revenue`：收入。

系统计算：

- CPC = cost / clicks。
- CTR = clicks / impressions。
- CVR = conversions / clicks。
- RPV = revenue / clicks。
- Profit = revenue - cost。
- ROI = profit / cost。

后续如果扩展，应增加：

- sessions。
- offer_clicks。
- revenue_reported / revenue_payable。
- postback_lag。
- source / medium / campaign / content / term。
- landing_page_version。
- currency。

## 12. 信息来源 URL

- Google Ads API metrics fields: https://developers.google.com/google-ads/api/fields/v23/metrics
- GA4 scopes of traffic-source dimensions: https://support.google.com/analytics/answer/11080067
- GA4 traffic-source dimensions, manual tagging, and auto-tagging: https://support.google.com/analytics/answer/11242870
- GA4 campaigns and traffic sources: https://support.google.com/analytics/answer/11242841
- Google AdSense metrics glossary: https://support.google.com/adsense/answer/2735899
- Definition of invalid traffic: https://support.google.com/adsense/answer/16737
- Use of online advertising to get new users to the site: https://support.google.com/adsense/answer/1348727
