# Click -> Session -> Revenue 对账 SOP

更新时间：2026-06-08

本文说明 Ads 套利团队如何处理 Google Ads clicks、站内 sessions、server logs、offer clicks、postback、AdSense/GAM revenue 之间的差异。目标是建立可复盘的诊断流程，而不是用补点击、模拟访问、伪造 session、隐藏跳转或重写归因来“修报表”。

## 1. 为什么差异是常态

Ads 套利至少有 6 个不同记账系统：

```text
Google Ads clicks / cost
-> Landing page request
-> GA4 session / event
-> Server log / click_id
-> Offer click / affiliate click
-> Conversion / ad revenue / postback
-> Finalized / paid revenue
```

它们的分母、时间、去重、归因和刷新延迟都不同：

- Google Ads 按广告点击和费用记账。
- GA4 按 session、user、event 和 attribution scope 记账。
- Server log 按 HTTP request 记账。
- Tracker 按 click_id、subid、redirect 和 postback 记账。
- Affiliate / buyer 按 submitted、approved、rejected 或 paid lead 记账。
- AdSense/GAM 按 ad request、impression、click、estimated revenue 和 finalized revenue 记账。

所以 `clicks != sessions != conversions != revenue` 是正常现象。套利团队要判断的是差异率是否稳定、是否集中在某个来源、设备、国家、浏览器、页面版本或时间段。

## 2. 对账漏斗

推荐固定一张漏斗表：

| 层级 | 字段 | 来源 | 关键问题 |
| --- | --- | --- | --- |
| 买量点击 | ads_clicks、cost、gclid/gbraid/wbraid | Google Ads | 点击是否真实、是否被过滤、是否带参数 |
| 到站请求 | landing_requests、status_code、latency | server log / CDN | 用户是否请求到页面 |
| 站内会话 | sessions、engaged_sessions、events | GA4 / analytics | tag、consent、session scope 是否正常 |
| 出站点击 | offer_clicks、cta_clicks、click_id | tracker / landing event | 用户是否进入变现链路 |
| 转化/广告收入 | conversions、ad_revenue、postback | affiliate / AdSense / GAM | 收入是否回传、是否延迟 |
| 结算收入 | finalized_revenue、paid_revenue、deduction | network / buyer / publisher | 是否可收款、扣量原因是什么 |

核心公式：

```text
landing_request_rate = landing_requests / ads_clicks
session_arrival_rate = sessions / ads_clicks
tag_loss_rate = 1 - sessions / landing_requests
offer_ctr = offer_clicks / sessions
conversion_rate = conversions / offer_clicks
rpv_ads_click = revenue / ads_clicks
rpv_session = revenue / sessions
finalization_ratio = finalized_revenue / estimated_revenue
```

每个公式都必须写清分母。不要把 Google Ads clicks、GA4 sessions、AdSense ad clicks、affiliate clicks 混成一个 `clicks`。

## 3. Click -> Landing Request

Google Ads click 到 server request 之间常见损耗：

- tracking template 展开失败。
- `{lpurl}` 或 Final URL suffix 拼接错误。
- HTTP/HTTPS、CDN、WAF、DNS 或证书错误。
- 移动端 deep link、应用跳转或浏览器兼容问题。
- 页面过慢，用户在请求完成前离开。
- parallel tracking 导致 tracking request 和 landing request 不再是串行路径。
- 部分点击被平台视为无效点击或重复点击。

诊断方式：

1. 用 Google Ads URL test 检查 expanded URL。
2. 真实点击或测试点击后查看 landing server log。
3. 确认 `gclid`、UTM、内部 `click_id` 是否到达最终页面。
4. 按 campaign、device、country、browser、hour 分层看 request rate。
5. 发现某设备或某国家断崖，先停该 segment，再修跳转链。

不要把 click -> request 的缺口解释成“需要补 session”。先证明用户是否到达页面。

## 4. Landing Request -> GA4 Session

server request 高于 GA4 sessions 很常见，原因包括：

- GA4 tag 未加载或加载太晚。
- Consent denied 或 CMP 阻断 analytics storage。
- ad blocker、浏览器隐私设置或网络拦截。
- 页面跳转太快，tag 没来得及发送。
- 单页应用路由没有正确发送 page_view。
- GA4 session scope 和内部 request scope 不同。
- 数据刷新延迟导致当日报表不完整。

诊断方式：

| 检查 | 通过标准 |
| --- | --- |
| Tag 初始化 | 页面首屏和路由变化都触发必要事件 |
| Consent | 默认值、更新顺序和地区规则清楚 |
| Data freshness | 日报标注 GA4 数据是否完整 |
| Server log | 作为 landing request 的独立真相层 |
| 分层 | device/browser/source/country 是否集中掉数 |

GA4 sessions 是分析口径，不是唯一真相。套利团队至少要保留 server log 或 CDN log 的 landing request 口径，用来判断是页面没到、tag 没发，还是报表未刷新。

## 5. Session -> Offer Click / Ad Request

用户到站后，收入链路可能分成两类：

CPA/CPL：

```text
session -> CTA click -> offer click -> lead/sale -> postback -> approved/paid
```

Publisher/AdSense/GAM：

```text
session -> page_view -> ad_request -> ad_impression -> ad_click/ad_revenue -> finalized revenue
```

常见断点：

- 页面承诺与广告不一致，用户跳出。
- CTA 不清楚、按钮不可见或移动端折叠。
- offer URL 没带 click_id/subid。
- 广告代码受 consent、广告拦截、模板错误影响。
- 页面模板没有广告位或广告位加载太晚。
- AdSense/GAM coverage 低或政策限制导致 no fill。

诊断重点：

- CPA/CPL 看 `offer_clicks / sessions` 和 `approved revenue / offer_clicks`。
- Publisher 看 `ad_requests / sessions`、`coverage`、`viewability`、`ad CTR`、`finalized revenue / sessions`。
- 不要用模拟访问补 CTA 或广告请求；应修页面、参数、广告位和来源质量。

## 6. Conversion / Revenue Delay

收入延迟会让当天 ROI 失真：

- GA4 数据有刷新延迟。
- Google Ads conversion 可能按 click date 或 conversion date 查看。
- Offline conversion 上传有处理和匹配延迟。
- Affiliate postback 可能先 pending，后 approved/rejected。
- AdSense/GAM estimated revenue 月初才 finalized，并可能扣量。

日报必须标注：

```text
cost_date
click_date
session_date
conversion_date
postback_date
reporting_date
finalized_month
revenue_status
```

扩量前至少回答：

- 当前收入是 estimated、approved、finalized 还是 paid？
- 回传窗口是否完整？
- 是否存在 late conversions？
- 是否按点击日期、转化日期还是付款日期看 ROI？
- 扣量或拒付是否已经暴露？

## 7. 异常诊断矩阵

| 表现 | 可能原因 | 处理 |
| --- | --- | --- |
| Ads clicks 高，server requests 低 | URL 展开错误、跳转慢、移动端失败、无效点击过滤 | 查 expanded URL、server log、设备国家 |
| Server requests 正常，GA4 sessions 低 | tag/CMP/ad blocker/data freshness | 查 tag、consent、browser、GA4 freshness |
| Sessions 正常，offer clicks 低 | 页面不匹配、CTA 弱、移动端体验差 | 修页面和 CTA，不补点击 |
| Offer clicks 正常，postback 少 | click_id 丢失、buyer 延迟、去重或拒付 | 查 subid、transaction_id、buyer feedback |
| Sessions 正常，ad requests 低 | 广告代码、CMP、模板缺广告位 | 查 ad code、consent、page template |
| Ad requests 高，revenue 低 | low fill、低价值来源、低 viewability | 查 coverage、Active View、source |
| Estimated 高，finalized 低 | invalid traffic、误点、扣量、政策 | 停异常 source 和页面版本 |
| 某来源差异突然变大 | 供应商质量变化、bot、placement 变化 | 隔离 source/placement，进入风险审计 |

## 8. 数据修复原则

可以做：

- 补导入漏掉的 CSV 报表。
- 修正时区、币种、日期归属。
- 去重 transaction_id。
- 恢复丢失但有证据的 click_id 映射。
- 标记 estimated、approved、finalized、paid 状态。
- 把异常来源隔离，不参与扩量判断。

不可以做：

- 补点击、刷展示、模拟自然 session。
- 伪造 GA4 event 或 postback。
- 用指纹、隐藏存储或无 consent 方式恢复用户身份。
- 根据 AdsBot、IP、设备、Cookie 展示不同页面。
- 为了让报表好看而改写原始日志。

原则：数据修复必须保留原始记录、修复原因、操作人、时间和证据来源。

## 9. 对账工作流

每日：

1. 导入 Google Ads cost/clicks。
2. 导入或汇总 server landing requests。
3. 导入 GA4 sessions/events。
4. 导入 affiliate / AdSense / GAM estimated revenue。
5. 输出 click -> request -> session -> revenue 漏斗。
6. 标记异常 segment，不直接扩量。

每周：

1. 按 source、campaign、device、country、landing_version 聚合。
2. 查 click/session 差异、offer CTR、ad request rate、RPV。
3. 对高成本低收入 segment 执行 pause / isolate。
4. 对追踪事故补 QA 记录和风险审计。

每月：

1. 替换或补充 finalized / paid revenue。
2. 计算 finalization ratio 和 deduction rate。
3. 回溯扣量来源、页面版本和广告位版本。
4. 更新安全系数、预算上限和来源白名单。

## 10. 系统落地

当前系统已支持：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer、target URL、tracking URL | `/offers` |
| 导出 Google Ads 草稿 | `/campaigns` |
| 导入 clicks/cost/conversions/revenue | `/metrics/import` |
| 生成 ROI/RPV/CPC 和异常建议 | `/optimization` |
| 记录追踪、无效流量和扣量风险 | `/risk-audits` |
| 记录来源 URL | `/sources` |
| 安排链接和指标复核任务 | `/tasks` |

后续安全扩展：

```text
landing_request_daily
click_session_reconciliation_runs
postback_events
revenue_status_daily
source_quality_segments
```

建议字段：

```text
day
source
campaign
ad_group
keyword
device
country
ads_clicks
landing_requests
ga4_sessions
offer_clicks
ad_requests
conversions
estimated_revenue
approved_revenue
finalized_revenue
paid_revenue
click_session_gap_reason
revenue_status
```

系统边界：

- 不产生点击、展示、session、conversion 或 postback。
- 不用模拟流量修复对账差异。
- 不隐藏追踪链路或最终目的地。
- 不绕过 consent、浏览器隐私或平台测量规则。

## 11. QA 清单

上线前：

- Google Ads auto-tagging 状态明确。
- Final URL、tracking template、Final URL suffix 测试通过。
- `gclid` / `gbraid` / `wbraid` / UTM / internal click_id 不被重定向剥离。
- Consent 默认值和更新顺序清楚。
- Server log 能看到 landing request 和关键参数。
- Offer URL 带 click_id/subid，postback 能去重。
- AdSense/GAM 页面模板和广告代码能按 source/page/device 复盘。

上线后：

- 24 小时内看 click -> request -> session 差异。
- 发现差异集中在某 segment，先暂停或降预算。
- 日报标注数据刷新状态和收入状态。
- 周报按 source/campaign/device/country/page version 分层。
- 月报用 finalized / paid revenue 复盘扩量决策。

## 12. 信息来源 URL

- Google Ads Help, About tracking in Google Ads: https://support.google.com/google-ads/answer/6076199
- Google Ads Help, About ValueTrack parameters: https://support.google.com/google-ads/answer/2375447
- Google Ads Help, About auto-tagging: https://support.google.com/google-ads/answer/3095550
- Google Ads Help, About parallel tracking: https://support.google.com/google-ads/answer/7544674
- Google Ads Help, Managing invalid traffic: https://support.google.com/google-ads/answer/11182074
- Google Analytics Help, Traffic-source dimensions, manual tagging, and auto-tagging: https://support.google.com/analytics/answer/11242870
- Google Analytics Help, Data freshness: https://support.google.com/analytics/answer/11198161
- Google Analytics Help, Traffic-source dimensions: https://support.google.com/analytics/answer/15567068
- Google tag, Consent mode overview: https://developers.google.com/tag-platform/security/concepts/consent-mode
- Google tag, Set up consent mode on websites: https://developers.google.com/tag-platform/security/guides/consent
- Google Ads API, Upload click conversions: https://developers.google.com/google-ads/api/docs/conversions/upload-clicks
- Google Ads API, Conversion upload diagnostics: https://developers.google.com/google-ads/api/docs/conversions/upload-summaries
- Google AdSense Help, Metrics glossary: https://support.google.com/adsense/answer/2735899
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
