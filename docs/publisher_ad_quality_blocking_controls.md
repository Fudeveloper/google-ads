# 发布商广告质量、阻止控制与品牌安全手册

更新时间：2026-06-08

本文说明 Ads 套利发布商如何管理广告质量：AdSense blocking controls、Ad review center、general categories、sensitive categories、advertiser URL blocking、Ad Manager protections、竞品广告、低质/误导广告、恶意广告投诉、用户体验和收入权衡。目标是让团队理解“不是所有高 CPM 广告都值得展示”，并建立广告质量审查和阻止策略，而不是靠堆广告、放任低质广告或隐藏广告来源换短期 RPM。

## 1. 为什么广告质量影响套利

发布商套利的收入来自广告展示和点击，但长期收入取决于：

```text
用户信任
-> 页面体验
-> 广告主价值
-> 买方竞价
-> 政策稳定
-> finalized / paid revenue
```

如果页面上出现误导、低俗、仿冒、诈骗、竞品或体验很差的广告，短期可能有 eCPM 或 CTR，但会带来：

- 用户投诉和跳出。
- 品牌或合作方投诉。
- 页面可信度下降。
- 敏感垂类风险。
- 广告服务限制或 Policy Center 问题。
- 低质量需求占用页面库存。
- 发布商团队无法解释收入来源。

广告质量治理不是“把所有广告都拦掉”，而是找到用户体验、政策风险、买方竞争和收入之间的平衡。

## 2. 核心对象

| 对象 | 作用 | 套利团队要理解什么 |
| --- | --- | --- |
| Blocking controls | AdSense 中允许/阻止广告的控制入口 | 控制越多，潜在竞价也可能减少 |
| Ad review center | 查看和处理已经展示或可能展示的单个广告 | 用于发现诈骗、误导、竞品和低质创意 |
| Advertiser URL blocking | 按广告主 URL 阻止广告 | 适合竞品、仿冒、投诉或不适合品牌的广告 |
| General categories | 按一般分类阻止广告 | 范围大，可能明显影响 fill/eCPM |
| Sensitive categories | 按敏感分类阻止广告 | 适合品牌安全和用户体验控制 |
| Ad networks / buyers | 广告需求来源 | 过度阻止会降低竞价密度 |
| GAM protections | Ad Manager 中更细的广告保护和阻止规则 | 需要 ad ops 能力和报表复盘 |
| Bad ad report | 用户或团队报告问题广告 | 需要截图、URL、creative、时间和页面证据 |

## 3. Blocking Controls 的收入权衡

阻止广告会减少可参与竞价的需求，所以不应把 blocking controls 当作“越多越好”的按钮。

常见策略：

| 策略 | 适合场景 | 风险 |
| --- | --- | --- |
| 少量精确阻止 advertiser URL | 明确竞品、诈骗、误导或投诉广告 | 维护成本高 |
| 阻止敏感分类 | 品牌安全、家庭/教育/金融等严格页面 | 可能降低需求密度 |
| 阻止一般分类 | 某些大类明显不适合用户 | 容易误伤收入 |
| 全站统一阻止 | 单站主题非常明确 | 不适合多垂类站点 |
| 按站点阻止 | 多站点、多垂类差异 | 需要站点级策略和复盘 |

操作原则：

1. 先用广告审查和投诉证据定位问题。
2. 优先阻止具体广告主 URL，再考虑 category。
3. 每次阻止前后记录 revenue、coverage、CTR、RPM 和用户投诉。
4. 不因单个低质广告立刻阻止大类。
5. 不为了高 eCPM 放任明显误导或诈骗广告。

## 4. Ad Review Center 工作流

Ad review center 的核心用途是发现并处理具体广告，而不是替代所有广告质量策略。

建议流程：

```text
daily review
-> filter by impressions / sensitive category / advertiser / landing page
-> inspect creative and landing page
-> classify issue
-> block / allow / report / watchlist
-> record evidence
-> review revenue impact
```

分类建议：

| 分类 | 示例 | 动作 |
| --- | --- | --- |
| 竞品广告 | 直接推广同类 Offer 或你的品牌竞争方 | 视业务决定 URL block |
| 仿冒/官方误导 | 伪装政府、银行、医疗、品牌官网 | report + block |
| 低质点击诱导 | “continue”“download”“claim now”误导按钮 | block/report，检查页面广告位 |
| 敏感垂类不匹配 | 成人、博彩、约会、减肥、投资等 | category 或 URL block |
| 恶意或可疑页面 | 跳转、下载、恐吓、钓鱼或欺诈 | report + evidence |
| 品牌不适配 | 与站点调性冲突 | watchlist 或 category rule |

不要只看广告截图。需要打开广告落地页、检查主体、承诺、价格、跳转链和是否与页面用户意图匹配。

## 5. General / Sensitive Categories

General categories 和 sensitive categories 是规模化控制工具。

使用建议：

- 对儿童、教育、金融、医疗、政府服务等页面，先定义不能出现的敏感类别。
- 对新闻、社区、娱乐站点，分类阻止要谨慎，避免过度降低竞价。
- 每次分类阻止后要观察 coverage、RPM、fill、CTR 和用户投诉变化。
- 多站点不要共用同一阻止模板；按站点主题、用户和国家调整。
- 如果某类别只有个别广告低质，优先用 advertiser URL 或 Ad review center。

套利场景特别注意：

- 你的页面如果是贷款信息，不一定要阻止所有金融广告；但要阻止误导、冒充官方、无资质或高风险承诺广告。
- 健康页面要更谨慎处理治疗结果、药品、补充剂和夸张声明。
- 政府服务页面要避免用户误以为广告是官方下一步。

## 6. 竞品广告和品牌安全

竞品广告不是天然违规，但可能影响业务目标：

- 内容站：竞品广告可能仍然产生高收入。
- Affiliate/lead 页面：竞品广告可能抢走用户或造成合作冲突。
- 品牌站：竞品广告可能损害品牌信任。
- 敏感垂类页面：不适合的广告可能引发投诉和合规问题。

决策矩阵：

| 情况 | 建议 |
| --- | --- |
| 竞品广告收入高且不误导用户 | 可保留，继续监控 |
| 竞品广告违反合作条款 | 阻止并保存证据 |
| 竞品广告伪装官方或误导用户 | report + block |
| 竞品广告导致用户投诉 | 阻止，复盘页面广告位置 |
| 竞品广告来自同类敏感垂类 | 检查资质、claim 和 landing page |

不要把竞品阻止当作提高 RPM 的手段。它是品牌安全和合作条款控制。

## 7. 低质广告、诈骗和恶意广告处理

低质广告常见形态：

- 伪装系统提示、下载按钮、继续按钮。
- 假冒政府、银行、知名品牌或官方服务。
- 恐吓式安全提示、病毒提示。
- 夸张收益、减肥、医疗或投资承诺。
- 多次跳转到不透明域名。
- 诱导用户安装软件或提交敏感信息。

处理原则：

1. 截图广告和页面位置。
2. 记录 URL、广告主域名、出现时间、页面 URL、国家、设备。
3. 在 Ad review center 中 block 或 report。
4. 如影响用户投诉，临时降低相关广告位密度。
5. 检查是否来自某个需求源、分类或国家。
6. 将 repeat offender 进入 watchlist。

如果低质广告集中在某类页面、国家或广告位，问题不一定只在广告需求；也可能是页面内容、广告位、流量来源或品牌安全信号吸引了低质需求。

## 8. Ad Manager Protections 和高级场景

GAM / AdX 场景中，广告质量控制会更复杂：

- Buyer / advertiser domain。
- Creative review。
- Ad categories。
- Protections / blocking rules。
- Open auction、deals、direct sold 的边界。
- Ad review center。
- Brand safety 和 competitive exclusions。

原则：

- 直客和程序化需求要分清楚。
- Open auction 的 blocking 不一定影响所有 direct deals。
- Deal / sponsor / direct sold 也需要人工素材审查。
- 恶意广告处理要能追溯到 demand channel、buyer、creative 和页面。
- 不要在没有报表的情况下大范围阻止 buyer 或 category。

对套利团队来说，GAM 高级阻止控制不是冷启动必需品。先把 AdSense、页面质量、流量来源和基础 Policy Center 稳定，再进入复杂 ad stack。

## 9. 监控指标

广告质量治理要同时看质量和收入：

```text
ad impressions
coverage / fill
eCPM / RPM
CTR
viewability
user complaints
blocked advertiser count
blocked category count
bad ad incidents
policy issues
finalized revenue
deduction rate
```

异常判断：

| 现象 | 可能原因 | 动作 |
| --- | --- | --- |
| 阻止后 RPM 大跌 | 阻止范围过大 | 回滚或改精确 URL block |
| CTR 异常高 | 误导广告或误点位置 | 查 Ad review center 和广告位 |
| 用户投诉广告诈骗 | 低质广告或恶意 landing | block/report，保存证据 |
| 某国家低质广告多 | demand mix 或流量质量差 | 分国家看广告和收入 |
| Policy Center 增加 | 页面内容、广告行为或流量问题 | 先修 policy，再处理 blocking |

## 10. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录广告质量、竞品广告、恶意广告和阻止动作 | `/risk-audits` |
| 保存 AdSense/GAM/Publisher policy 来源 | `/sources` |
| 在页面质量和广告位实验中复盘投诉、CTR 和广告密度 | 相关 Markdown 与 `/metrics/import` |
| 将异常广告作为事故记录 | `/logs`、`/risk-audits` |
| 结合 finalized revenue 判断阻止动作是否影响收入 | `revenue_reconciliation_adstack.md` |

后续可扩展表：

```text
ad_quality_incidents
blocked_advertiser_domains
blocked_ad_categories
ad_review_center_snapshots
publisher_blocking_rule_versions
```

建议字段：

```text
site_domain
page_url
ad_unit
advertiser_domain
creative_summary
category
sensitive_category
incident_type
country
device
first_seen_at
action
blocked_at
reported_at
evidence_url
revenue_impact
review_status
```

系统边界：

- 不点击广告来检查广告或制造证据。
- 不自动模拟用户触发广告。
- 不绕过 AdSense/GAM 后台权限或 Cookie 登录。
- 不用恶意广告投诉作为竞品打击工具。
- 不通过 cloaking 让审核和用户看到不同广告环境。

## 11. QA 清单

- 每个站点有广告质量 owner 和阻止策略。
- Ad review center 定期检查高展示广告、敏感类别和用户投诉广告。
- 阻止 advertiser URL 前保存截图、域名、页面、国家、设备和原因。
- 分类阻止前评估 coverage/RPM 影响。
- 竞品广告按合作条款、用户体验和收入影响判断，不一刀切。
- 恶意广告 report 后记录 review/status，重复出现则进入 watchlist。
- 阻止动作和 Policy Center、ad serving limits、用户投诉一起复盘。
- 不通过点击广告验证 landing page；用审查工具、预览和证据截图。
- 广告质量收益判断以 finalized revenue 和用户体验为准。
- 出现诈骗/仿冒/恶意广告时先保护用户体验，再看短期 RPM。

## 12. 信息来源 URL

- Google AdSense Help, Guide to allow and block ads on your site: https://support.google.com/adsense/answer/180609
- Google AdSense Help, Block sensitive categories: https://support.google.com/adsense/answer/164131
- Google AdSense Help, Allow & block ads: https://support.google.com/adsense/topic/1727182
- Google AdSense Help, Ad review center: https://support.google.com/adsense/answer/2469354
- Google AdSense Help, Blocking controls by site: https://support.google.com/adsense/answer/12169214
- Google AdSense Help, Program policies: https://support.google.com/adsense/answer/48182
- Google Publisher Policies: https://support.google.com/adsense/answer/9335564
- Google Publisher Restrictions: https://support.google.com/adsense/answer/10437795
- Google AdSense Help, Policy Center overview: https://support.google.com/adsense/answer/9485926
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google Ad Manager, Ad review center feature brief: https://admanager.google.com/home/resources/feature-brief-ad-review-center/
- Google Ad Manager, Brand safety capabilities: https://admanager.google.com/home/capabilities/brand-safety/
