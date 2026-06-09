# 广告位、刷新、可见率与页面体验手册

更新时间：2026-06-08

本文说明 Ads 套利收入端如何做广告位收益优化：广告位数量、位置、可见率、加载策略、广告刷新、Auto ads、手动广告单元、页面体验和扣量复盘。目标是提高真实可收款的 session RPM，而不是通过误点、自动刷新、遮挡内容、补展示或 MFA 堆广告制造短期收入。

## 1. 为什么广告位优化是套利核心

套利利润看起来是买量 CPC 和收入 RPV 的差值，但发布商收入端的 RPV 由广告位和页面体验共同决定：

```text
Paid click
-> Landing session
-> Page view
-> Ad request
-> Filled impression
-> Viewable impression
-> Valid click / advertiser value
-> Estimated revenue
-> Finalized / paid revenue
```

如果只看当日 page RPM，团队很容易误判：

- 加广告位后 estimated revenue 上升，但页面跳出率、广告主价值和 finalized revenue 下降。
- 广告位靠近按钮导致 CTR 升高，但实际是误点和无效流量风险。
- 自动刷新提高 ad requests，却没有真实新增用户注意力。
- Lazy loading 改善加载速度，但广告位太晚加载导致可见展示下降。
- Sticky、插屏、弹窗短期收入高，但页面体验、政策和 Better Ads 风险上升。

所以广告位优化必须同时看收入、可见率、页面体验、用户任务和结算后扣量。

## 2. 指标漏斗

最小日报字段：

```text
day
site
page_template
traffic_source
country
device
sessions
page_views
ad_requests
matched_requests
ad_impressions
viewable_impressions
ad_clicks
estimated_revenue
```

月度复盘字段：

```text
finalized_revenue
deduction
deduction_rate
finalization_ratio
policy_issue
invalid_traffic_note
page_version
ad_layout_version
```

核心指标：

| 指标 | 公式 | 判断 |
| --- | --- | --- |
| Ad request rate | ad_requests / page_views | 广告代码和同意状态是否正常 |
| Fill / coverage | ad_impressions / ad_requests | 需求、政策、地区和广告位是否有问题 |
| Viewability | viewable_impressions / measurable_impressions | 广告是否被真实看到 |
| Ad CTR | ad_clicks / ad_impressions | 过高要查误点和诱导 |
| Ad RPM | revenue / ad_impressions * 1000 | 广告展示价值 |
| Page RPM | revenue / page_views * 1000 | 页面浏览变现 |
| Session RPM | revenue / sessions * 1000 | 套利买量最重要收入口径 |
| Finalization ratio | finalized_revenue / estimated_revenue | 当月收入是否可收款 |

不要只追 ad_requests 或 impressions。套利团队真正要优化的是扣量后、可解释、可持续的 session RPM。

## 3. 广告位设计原则

安全广告位通常有三个特征：用户能自然看到、不会误触、不会压过内容任务。

推荐位置：

- 首段或目录之后的自然段落间。
- 长内容章节之间。
- 文末相关内容或推荐区域。
- 桌面侧栏，但不遮挡正文。
- 移动端非遮挡、可关闭且不贴近导航/CTA 的小型 sticky。

高风险位置：

- 下载、播放、下一步、继续、关闭、表单提交等按钮附近。
- 与内容卡片、搜索结果、导航菜单样式过度相似。
- 首屏内容被广告挤出或遮挡。
- 弹窗、强制插屏、自动展开或用户未请求的新窗口。
- 为制造 pageviews 而分页、翻页或跳转。

广告位评分建议：

| 维度 | 低分信号 | 高分信号 |
| --- | --- | --- |
| 可见率 | 大量广告在用户离开前未进入视口 | 在自然阅读路径中可见 |
| 误点风险 | 靠近交互控件或伪装成内容 | 与按钮、导航和表单有清晰间距 |
| 内容任务 | 广告阻断答案、表单或导航 | 用户能先完成页面主要任务 |
| 收入质量 | CTR 突升、finalized 下调 | RPM 稳定、扣量低 |
| 页面体验 | CLS、插屏、广告密度恶化 | 布局稳定、加载可控 |

## 4. Ad refresh 边界

Ad refresh 指在同一页面会话中重新请求或替换广告。技术上，Google Publisher Tag 支持在控制广告加载时刷新广告 slot；GAM 也要求发布商声明刷新库存。业务上，刷新只有在用户仍有真实注意力、广告位重新可见、需求和政策允许时才有讨论价值。

可接受方向：

- 长阅读页面中，用户停留足够长且广告位仍可见。
- 单页应用或无限滚动中，用户确实进入新内容区域。
- 透明配置刷新类型、最小间隔和触发条件。
- 报表中单独标记 refresh inventory，比较刷新展示的 RPM、viewability、CTR、扣量。

高风险方向：

- 页面刚加载就频繁刷新。
- 用户不可见或离开视口时刷新。
- 为增加请求量而自动刷新广告或页面。
- 刷新导致误点、跳动、CLS 或内容遮挡。
- 不在 GAM 中声明刷新库存，或不区分刷新和普通展示复盘。

内部判断标准：

```text
refresh_allowed =
  user_still_active
  and slot_viewable_or_about_to_be_viewable
  and minimum_interval_met
  and refresh_inventory_declared
  and no_layout_shift
  and no_policy_or_invalid_traffic_issue
```

本项目不实现 ad refresh 代码，只沉淀刷新策略、风险审计和报表口径。

## 5. Viewability 与 Active View

Viewability 不是“广告加载了”，而是广告是否有机会被用户看到。Active View 相关指标能帮助判断广告展示是否可测量、是否可见。

常见问题：

| 现象 | 可能原因 | 动作 |
| --- | --- | --- |
| ad requests 正常，impressions 低 | fill/coverage、政策限制、广告代码或 consent 问题 | 查政策中心、CMP、国家设备 |
| impressions 高，viewability 低 | 广告位过低、加载太晚、页面跳出快 | 调整位置、内容承接和加载 |
| viewability 高，CTR 异常高 | 靠近按钮、误点、广告伪装 | 降低密度、调整间距 |
| RPM 高，finalized 低 | 无效流量、误点、扣量 | 回溯 source、page version、ad layout |
| CLS 上升 | 广告位未预留尺寸或动态插入 | 固定容器尺寸，避免内容跳动 |

套利团队应把 viewability 当作质量诊断，而不是单一 KPI。过低说明广告价值弱，过高且 CTR 异常也可能说明广告位设计有问题。

## 6. Lazy loading 与页面体验

Lazy loading 可以减少初始请求和提升页面加载体验，但广告位不能因为懒加载而造成布局跳动、内容推挤或收入口径混乱。

实践原则：

- 广告容器提前预留宽高，减少 CLS。
- 不为了抢收入阻塞主内容、首屏信息和用户任务。
- 对移动端单独测试，尤其是 sticky、首屏段间广告和表单附近广告。
- 记录页面模板版本和广告位版本，避免不知道哪次改动影响 RPM。
- 使用真实用户数据或实验窗口比较，而不是单日小样本判断。

页面体验不是 SEO 独立问题。对套利团队来说，慢页面、跳动布局和插屏干扰会直接降低 landing arrival、session depth、广告主价值和最终收入。

## 7. Auto ads 与手动广告单元实验

Auto ads 适合快速建立基线，但不能替代人工审计：

- 要检查广告是否遮挡内容、靠近按钮或插入不合适区域。
- 要控制广告负载和格式。
- 要按页面模板、设备、国家和流量来源复盘。

手动广告单元适合做可控实验：

- 每次只调整一个主变量，例如位置、尺寸、数量或模板。
- 建立 `ad_layout_version`，和页面版本、流量来源、收入结算关联。
- 同时看 estimated 和 finalized，不用一天 RPM 决定扩量。

实验矩阵：

| 实验 | 保持不变 | 观察 |
| --- | --- | --- |
| Auto ads vs 手动广告位 | source、页面模板、预算 | session RPM、viewability、CLS、deduction |
| 段间广告位置 | source、广告数量 | viewability、ad CTR、scroll depth |
| sticky 开关 | 页面模板、source | mobile UX、CTR、扣量 |
| lazy loading 参数 | 广告位位置 | LCP、CLS、impressions、viewability |
| refresh 策略 | page version、source | refresh RPM、CTR、finalization ratio |

## 8. 异常复盘

广告位实验上线后，出现以下情况应先停实验或降密度：

- ad CTR 突然高于历史基线 2 倍以上。
- estimated revenue 上升但 finalized revenue 明显下调。
- Policy Center 出现广告行为或内容问题。
- 用户投诉广告遮挡、误点、下载按钮混淆。
- 页面 CLS、LCP 或跳出率恶化。
- 某个流量源的 ad CTR、viewability、deduction 同时异常。

复盘顺序：

1. 固定时间区间和时区。
2. 按 source、country、device、page_template、ad_layout_version 分层。
3. 对比实验前后 ad_requests、impressions、viewability、ad CTR、revenue、deduction。
4. 检查页面截图、移动端实际展示、按钮间距和广告标识。
5. 暂停异常 source 或广告位版本。
6. 记录风险审计和来源 URL。

## 9. 系统落地

当前系统支持：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer 和变现模式 | `/offers` |
| 审计页面广告密度和 MFA 风险 | Offer 详情页、`landing_page_quality_mfa.md` |
| 导入 cost/revenue 粗口径 | `/metrics/import` |
| 记录广告位、刷新和误点风险 | `/risk-audits` |
| 沉淀来源 URL | `/sources` |
| 记录广告位实验结论 | `/logs`、运营文档 |

后续可扩展表：

```text
ad_layout_versions
publisher_ad_unit_daily
ad_refresh_tests
page_experience_audits
```

建议字段：

```text
page_template
ad_layout_version
ad_unit
position
device
source
ad_requests
matched_requests
ad_impressions
viewable_impressions
ad_clicks
estimated_revenue
finalized_revenue
cls
lcp
refresh_type
refresh_interval_seconds
```

系统边界：

- 不生成自动刷新广告代码。
- 不制造广告请求、展示或点击。
- 不把广告伪装成内容或按钮。
- 不用 Worker、Bot 分流或 cloaking 改变审核与用户看到的页面。

## 10. QA 清单

上线广告位实验前：

- 广告和内容可清晰区分。
- 广告不贴近下载、播放、继续、表单提交等按钮。
- 移动端没有遮挡主内容或不可关闭 sticky。
- 广告容器预留尺寸，CLS 风险可控。
- 已记录 page_template 和 ad_layout_version。
- 已定义观察窗口、样本量和 stop-loss。
- Ad refresh 如被讨论，必须先确认需求方允许、GAM 声明、触发条件、间隔和报表拆分。
- 不使用补展示、刷点击、自动浏览或诱导点击。

复盘广告位实验时：

- 同时看 estimated 和 finalized revenue。
- 按 source、country、device、page_template 分层。
- 对比 Active View / viewability、ad CTR、session RPM 和 deduction。
- 出现高 CTR 低 finalized 或扣量时先停实验。
- 结论写入来源库、风险审计或运营复盘。

## 11. 信息来源 URL

- Google AdSense Help, Metrics glossary: https://support.google.com/adsense/answer/2735899
- Google AdSense Help, Ad placement policies: https://support.google.com/adsense/answer/1346295
- Google AdSense Help, Best practices for ad placement: https://support.google.com/adsense/answer/1282097
- Google AdSense Help, Set up ads on your site: https://support.google.com/adsense/answer/7037624
- Google AdSense Help, Program policies: https://support.google.com/adsense/answer/48182
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google Ad Manager Help, Declare ad refresh inventory: https://support.google.com/admanager/answer/6286179
- Google Publisher Tag, Control ad loading and refresh: https://developers.google.com/publisher-tag/guides/control-ad-loading
- Google Publisher Tag sample, Lazy loading: https://developers.google.com/publisher-tag/samples/lazy-loading
- Google Publisher Policies Help, Google Ad Manager partner guidelines: https://support.google.com/publisherpolicies/answer/9059370
- Google Search Central, Avoid intrusive interstitials and dialogs: https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials
- web.dev, Cumulative Layout Shift: https://web.dev/articles/cls
- web.dev, Optimize Cumulative Layout Shift: https://web.dev/articles/optimize-cls
- Coalition for Better Ads, Better Ads Standards: https://www.betterads.org/standards/
- Coalition for Better Ads, Desktop ad density higher than 50%: https://www.betterads.org/desktop-ad-density-over-50-percent
