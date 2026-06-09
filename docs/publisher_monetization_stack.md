# 发布商变现栈：AdSense / AdX / Google Ad Manager 手册

更新时间：2026-06-08

本文解释 Ads 套利收入端的基础设施：AdSense、AdX、Google Ad Manager（GAM）、Auto ads、手动广告单元、广告请求、展示、点击、Active View、RPM、扣量和广告位策略。目标是帮助团队理解“买来的 session 如何变成可收款收入”，并把广告位优化和发布商合规纳入同一套运营流程。本文不提供诱导点击、广告伪装、自动刷新广告、补展示、刷点击、MFA 堆广告或绕过发布商政策的方案。

## 1. 收入端为什么重要

买量端只回答“流量花了多少钱”，发布商变现端回答“这些访问能否产生可收款收入”。套利模型必须同时看：

```text
Traffic cost
-> Sessions
-> Ad requests
-> Ad impressions
-> Viewable impressions
-> Clicks / conversions
-> Estimated revenue
-> Finalized / paid revenue
-> Deduction / invalid traffic
```

常见误区：

- 只看页面 RPM，不看 click -> session 损耗。
- 只看 estimated earnings，不看 finalized earnings 和扣量。
- 只看广告数量，不看可见率、误点风险和页面体验。
- 把 Auto ads 的短期收入提升误判为长期可扩量。
- 不区分 AdSense、AdX、GAM、联盟和直客的结算口径。

## 2. 产品层级

| 产品/层级 | 作用 | 适合阶段 | 风险 |
| --- | --- | --- | --- |
| AdSense | 入门级发布商变现，自动/手动广告单元 | 小站、内容站、早期测试 | 政策、无效流量、广告服务限制 |
| AdX / Ad Exchange | 更高级的程序化需求，通常通过 GAM 管理 | 有规模、合规和运营能力的发布商 | 买方质量、规则、结算和政策要求更复杂 |
| Google Ad Manager | 广告服务器，管理直接订单、程序化、AdSense/AdX、广告位和报表 | 多需求源、多广告位、直客和程序化混合 | 设置复杂，错误规则会影响收入和合规 |
| Header bidding / Open Bidding | 多需求方竞争库存 | 有 ad ops 能力的站点 | 延迟、复杂度、隐私和需求质量 |
| Direct sold | 直客或赞助 | 垂类强、品牌安全、受众清晰 | 销售周期和履约责任 |

在套利早期，先把 AdSense / 手动广告位 / 指标口径跑清楚，比急着做复杂 ad stack 更重要。

## 3. 核心概念

| 概念 | 含义 | 套利用途 |
| --- | --- | --- |
| Page view | 页面浏览 | 计算 page RPM 和页面承载能力 |
| Session | 用户会话 | 与买量点击对账 |
| Ad request | 页面请求广告 | 判断广告加载和广告位调用 |
| Ad impression | 广告实际展示 | 判断填充和广告位表现 |
| Active View measurable | 可测量可见性的展示 | 判断可见率口径是否足够 |
| Active View viewable | 达到可见标准的展示 | 判断广告位是否有真实可见价值 |
| Ad CTR | 广告点击 / 广告展示 | 过高可能代表误点或诱导点击风险 |
| Ad RPM | 每千次广告展示收入 | 比较广告位价值 |
| Page RPM | 每千次页面浏览收入 | 比较页面变现能力 |
| Session RPM | 每千次 session 收入 | 买量套利最重要收入口径之一 |
| Coverage / Fill | 请求中获得广告的比例 | 判断需求和政策限制 |
| Estimated earnings | 估算收入 | 日常观察，不等于可收款 |
| Finalized earnings | 最终确认收入 | 月度关账和预算安全系数依据 |

关键公式：

```text
Page RPM = Revenue / Page views * 1000
Session RPM = Revenue / Sessions * 1000
Ad RPM = Revenue / Ad impressions * 1000
RPV = Revenue / Sessions
Break-even CPC = RPV * approval_factor * (1 - deduction_rate)
```

## 4. Auto ads 与手动广告单元

Auto ads：

- 优点：上手快，自动选择位置和格式，适合早期测试。
- 风险：广告位置可能影响用户体验；需要手动排除不适合区域；不能把自动插入当成无需审计。
- 适合：内容结构稳定、页面模板简单、团队缺少 ad ops 能力时。

手动广告单元：

- 优点：位置可控、便于实验、容易做页面版本和广告位级复盘。
- 风险：位置设计不当容易造成误点、广告伪装或广告密度过高。
- 适合：套利团队需要按页面、段落、设备和来源精细评估 RPM 时。

实操建议：

| 阶段 | 建议 |
| --- | --- |
| 冷启动 | Auto ads 或 1-2 个手动广告位，先看基线 RPM 和政策稳定性 |
| 小样本验证 | 增加广告位实验，但保持页面任务可完成 |
| 稳定放量 | 按页面模板、设备和来源建立广告位基准 |
| 异常扣量 | 降低广告密度，暂停异常来源，回到低干扰配置 |

## 5. 广告位策略

安全广告位：

- 正文首段之后。
- 章节之间的自然间隔。
- 侧栏或文末推荐区域。
- 长内容中的段落间广告。
- 不遮挡内容的小尺寸 sticky，且移动端可关闭或不影响任务。

高风险广告位：

- 导航、下载、播放、下一页、继续按钮旁边。
- 与内容卡片样式几乎相同。
- 弹窗、强制插屏、遮挡主内容。
- 自动刷新页面或广告位。
- 用户未请求时自动跳转、打开新窗口或改变广告点击结果。

内部广告位评分：

| 维度 | 低分 | 高分 |
| --- | --- | --- |
| 可见性 | 用户很少看到 | 自然阅读路径中可见 |
| 误点风险 | 靠近按钮/导航/下载 | 与交互控件有距离 |
| 内容干扰 | 打断任务或遮挡正文 | 不影响阅读和 CTA |
| 收入稳定 | 短期高 CTR、长期扣量 | RPM 稳定、扣量低 |
| 合规 | 标签含糊、广告伪装 | 清楚可识别为广告 |

## 6. AdSense / AdX / GAM 指标对账

日报最少拆到：

```text
date
site
page_template
traffic_source
country
device
sessions
page_views
ad_requests
ad_impressions
viewable_impressions
clicks
estimated_revenue
```

月报补充：

```text
finalized_revenue
deduction
deduction_rate
payment_status
invalid_traffic_notes
policy_issues
```

对账问题：

| 现象 | 可能原因 | 动作 |
| --- | --- | --- |
| sessions 正常，ad requests 低 | 广告代码未加载、同意管理、页面模板缺广告位 | 查模板、CMP、广告代码 |
| ad requests 高，impressions 低 | fill/coverage 低、政策限制、需求不足 | 查政策中心、国家/设备/页面 |
| impressions 高，revenue 低 | 低价值来源、低可见率、广告位弱 | 查 source、Active View、页面 |
| CTR 异常高 | 误点、诱导点击、广告伪装 | 立即降密度和改位置 |
| estimated 高，finalized 低 | 扣量、无效流量、结算调整 | 回溯来源和页面版本 |

## 7. 可见率和延迟

Active View / viewability 对收入质量很关键：

- 可见率低：广告虽然加载，但用户没看到，买方价值低。
- 可见率异常高且 CTR 异常高：可能是位置过近、误点或诱导风险。
- 延迟高：广告加载慢会降低 impressions 和收入，也会伤害页面体验。

优化方向：

- 不为了广告加载阻塞主内容。
- 广告位靠近自然阅读路径，但不贴着交互按钮。
- 移动端优先检查首屏、sticky、段间广告和 CTA 关系。
- 不用未经允许的 auto-refresh 提升请求量。
- 保留广告位版本和页面版本，才能知道哪次改动影响 RPM。

## 8. Ad stack 复杂化的边界

引入 GAM、AdX、Open Bidding、第三方需求之前，先确认：

- 站点有稳定合法内容和真实用户。
- 流量来源可解释并能按 source 停量。
- 页面政策和广告位政策稳定。
- 有人能管理 line item、price rule、ad unit、creative review、blocking 和报表。
- 有能力处理隐私、CMP、TCF/Consent、地区监管和广告主品牌安全。

不要为了短期提升 RPM 叠加无法解释的需求源。需求越多，越需要广告质量审查、恶意广告处理、隐私合规和报表对账。

## 9. 发布商风险红线

禁止或高风险：

- 鼓励用户点击广告。
- 把广告伪装成内容、导航、下载、播放或结果按钮。
- 给用户补偿以点击或浏览广告。
- 自动刷新广告或页面来增加请求/展示。
- 在弹窗、软件应用、邮件或无法评估内容里放 AdSense 广告。
- 使用低质量、激励、自动浏览或不可解释流量。
- 为了提高 RPM 做 cloaking、广告密度过高或 MFA 堆页。

发现这些信号时，先停流量和广告位实验，再修复页面和来源，而不是继续扩量。

## 10. 变现实验流程

实验变量：

- Auto ads vs manual ad units。
- 广告位数量。
- 广告位位置。
- 页面模板。
- 设备。
- 国家。
- 流量来源。
- Offer / 直接广告 / 程序化需求组合。

每次只改一个主变量：

```text
页面模板 A + 广告位版本 v1 + source 固定
vs
页面模板 A + 广告位版本 v2 + source 固定
```

观察周期：

- 至少 1-3 天看行为和估算收入。
- 至少一个结算周期看扣量和 finalized revenue。
- 不在未经历扣量前把短期 RPM 作为放量依据。

## 11. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer 和变现模型 | `/offers` |
| 评估 RPM、CPC、CVR 和安全系数 | `/calculators` |
| 审计落地页质量和广告密度风险 | Offer 详情页、`landing_page_quality_mfa.md` |
| 导入 sessions/clicks/revenue 级指标 | `/metrics/import` |
| 分析 ROI 和优化建议 | Dashboard、`/optimization` |
| 记录无效流量、扣量和政策来源 | `/risk-audits`、`/sources` |
| 复盘页面、流量源和收入差异 | `/logs`、运营文档 |

当前系统的 `metrics_daily` 是收入端简化口径。未来可扩展：

- `page_views`
- `ad_requests`
- `ad_impressions`
- `viewable_impressions`
- `estimated_revenue`
- `finalized_revenue`
- `deduction`
- `ad_unit`
- `page_template`

但即使扩展，也只做报表、审计和优化建议，不做补展示、刷点击或广告请求模拟。

## 12. 信息来源 URL

- Google AdSense Help, Metrics glossary: https://support.google.com/adsense/answer/2735899
- Google AdSense Help, Set up ads on your site: https://support.google.com/adsense/answer/7037624
- Google AdSense Help, Ad placement policies: https://support.google.com/adsense/answer/1346295
- Google AdSense Help, Best practices for ad placement: https://support.google.com/adsense/answer/1282097
- Google AdSense Help, AdSense Program policies: https://support.google.com/adsense/answer/48182
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Management API, Metrics and Dimensions: https://developers.google.com/adsense/management/metrics-dimensions
- Google Publisher Policies Help, Google Ad Manager Partner Guidelines: https://support.google.com/publisherpolicies/answer/9059370
- Google Ad Manager, Open Bidding: https://admanager.google.com/home/resources/feature-brief-open-bidding/
- Google Ad Manager, Ad review center: https://admanager.google.com/home/resources/feature-brief-ad-review-center/
- Google Ad Manager, How Authorized Buyers work with Google Ad Manager: https://admanager.google.com/home/resources/how_authorized_buyers_work_with_google/
