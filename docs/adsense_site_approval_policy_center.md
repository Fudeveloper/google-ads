# AdSense 站点审核、Policy Center 与广告投放限制手册

更新时间：2026-06-08

本文说明 Ads 套利发布商如何理解 AdSense 站点审核、Sites 页面、连接站点、页面准备、Policy Center、ad serving status、ad serving limits、invalid traffic concerns、内容质量、购买流量责任和恢复流程。目标是让团队把“能不能展示广告、能不能稳定收款”当成发布商经营能力，而不是在被限制后通过换域名、换账号、隐藏来源或刷自然流量规避平台判断。

## 1. 为什么站点审核决定收入起点

Google Ads 买量侧可以快速产生点击，但发布商收入侧必须先回答：

```text
这个站点是否被允许展示广告？
页面是否能被审核和爬取？
内容是否有独特价值？
流量是否真实、可解释？
广告代码、ads.txt、隐私和 consent 是否正确？
Policy Center 是否有影响广告服务的问题？
```

如果站点审核没有通过，或者广告服务被限制，后面的 RPM、floor、Header Bidding、广告位实验都没有意义。套利团队常见错误是：把站点审核当作一次性门槛，而不是持续的站点健康管理。

## 2. 核心状态

| 对象 | 作用 | 套利团队要看什么 |
| --- | --- | --- |
| AdSense Sites | 添加、连接和查看站点审核状态 | site 是否 ready，是否需要 review |
| Site review | Google 审核整个站点是否符合政策 | 内容、导航、可访问性、代码、政策 |
| AdSense code / meta / ads.txt | 用于连接或验证站点 | 是否在正确域名、正确位置、可被访问 |
| Policy Center | 查看 policy issue、regulatory issue、advertiser preference 和 ad serving status | 是否影响广告服务或收入 |
| Ad serving limit | 账号或站点广告展示数量被限制 | traffic quality、invalid traffic、账号评估 |
| Publisher policies | 发布商内容、行为、隐私和技术要求 | 站点是否可长期变现 |
| Traffic segmentation | 按来源隔离和解释流量质量 | 限制或扣量时能否定位来源 |

## 3. 站点连接与审核流程

AdSense 新站通常需要先添加站点并连接到 AdSense。连接方式可能包括：

- AdSense code snippet。
- ads.txt code snippet。
- meta tag。

审核会检查整个站点是否符合 AdSense Program policies 和 Google Publisher policies。官方文档也提示：在站点获批前不能展示广告；审核通常需要几天，但有时可能更久。

上线前 QA：

```text
domain
canonical_domain
https_status
homepage_status
robots_status
adsense_code_present
meta_tag_present
ads_txt_present
privacy_policy_url
about_contact_url
content_index_count
regular_visits_page
review_requested_at
review_status
```

常见连接问题：

- AdSense code 缺失、放错域名或没有放在 `<head>`。
- 提交的 URL 和实际站点不一致。
- 站点未发布、被密码保护、无法访问。
- robots.txt 阻止 AdSense crawler。
- 页面几乎没有内容或没有常规访问。
- ads.txt 不在根目录或 publisher ID 错误。

## 4. 站点 Ready 不是只看文章数量

“准备好展示广告”的站点至少要让审核和用户都能理解：

- 这个站点是谁运营。
- 站点提供什么独特内容或工具。
- 用户为什么会访问。
- 页面之间如何导航。
- 隐私、Cookie、广告和联盟关系如何披露。
- 内容和广告是否清楚区分。
- 目标国家用户能否正常访问和理解。

可检查项：

| 维度 | 低风险信号 | 高风险信号 |
| --- | --- | --- |
| 内容价值 | 原创、完整、能解决明确问题 | 复制、拼接、薄页、仅广告或列表 |
| 导航 | 分类、内链、重要页面可达 | 孤岛页、死链、模板页堆叠 |
| 可信度 | About、Contact、Privacy、Disclosure 清楚 | 主体不明、联系方式缺失 |
| 页面体验 | 移动端可用、速度可接受、广告不压内容 | 首屏广告过多、弹窗遮挡、CLS 大 |
| 政策 | 内容垂类、声明、隐私和数据使用可解释 | 敏感垂类无资质、误导、版权或仿冒 |
| 流量 | 来源可解释，可按 source 停量 | 购买低质流量、激励、自动浏览 |

不要把“多发几篇 AI 文章”当作站点准备。站点审核更像“发布商可信度、内容价值、技术可访问性和广告生态风险”的综合判断。

## 5. Policy Center 状态

Policy Center 用来集中查看可能影响收入的问题。需要区分：

| 类型 | 含义 | 处理 |
| --- | --- | --- |
| Policy issue | 政策问题，可能导致页面/站点广告服务受限或停用 | 修复后 request review |
| Regulatory issue | 监管要求或地区规则，可能影响需求 | 按地区、CMP、隐私和内容要求修复 |
| Advertiser preference | 广告主偏好导致需求减少 | 评估是否调整内容或接受低需求 |
| Disabled ad serving | 广告服务被停用 | 先修复，不扩量 |
| Restricted demand | 需求受限 | 看内容、监管、品牌安全和广告主偏好 |
| Limited ad serving | 广告展示数量受限 | 查 traffic quality、invalid traffic 和账号评估 |

排序优先级：

1. Disabled ad serving。
2. Account-level or site-level limits。
3. 大量 affected ad requests。
4. 新增问题或重复问题。
5. 高价值页面/国家/来源对应问题。

## 6. Ad Serving Limits

Ad serving limits 可能来自账号正在被评估，也可能来自 invalid traffic concerns。官方文档说明：限制期间账号通常仍可访问，系统会继续评估和更新限制；时间可能少于 30 天，也可能更久。

套利团队不要做：

- 补自然流量。
- 刷展示或点击。
- 用代理/指纹模拟真实用户。
- 快速换域名或换账号。
- 继续扩大未知来源。

正确动作：

1. 暂停最近新增或不可解释来源。
2. 降低广告密度，移除高误点广告位。
3. 按 source、campaign、country、device、page template 查看 CTR、viewability、session depth、ad requests、revenue。
4. 检查是否有自动刷新、激励、低质量 placement、社群灌流或异常 referrer。
5. 记录 Policy Center 状态和时间线。
6. 等待系统评估，同时继续建设内容和真实受众。

如果问题来自 invalid traffic，恢复不是“让数据看起来更自然”，而是停止异常来源、修复页面和广告位、证明流量可解释。

## 7. 购买流量责任

AdSense 允许发布商通过线上广告获取用户，但发布商要对买来的流量质量负责。对套利团队来说，这意味着：

- 每个 source 必须可解释。
- 能按 campaign / subid / placement 停量。
- 不能使用 paid-to-click、paid-to-surf、autosurf、click exchange、激励访问或自动浏览。
- 流量供应商必须提供来源、结算方式、停源机制和质量证据。
- 高 CTR、低停留、低 viewability、低 finalized revenue 的来源要先隔离。

购买流量不是问题，无法解释、无法隔离、无法证明用户意图的流量才是问题。

## 8. 恢复和 Review 流程

当站点审核失败或 Policy Center 出现问题：

```text
freeze changes
-> capture issue details
-> classify issue
-> fix page / source / ad layout / consent / ads.txt
-> collect before-after evidence
-> request review where available
-> monitor status and revenue
-> update SOP
```

证据包：

```text
site
issue_type
ad_serving_status
affected_urls
affected_ad_requests
date_reported
source_segments
page_screenshots_before
page_screenshots_after
traffic_changes
ad_layout_changes
policy_source_urls
review_requested_at
review_result
```

如果 review rejected，不要立即重复提交。先对照 issue details、页面内容、广告位、流量来源和隐私/CMP 再修一次。

## 9. 常见事故

| 事故 | 表现 | 修复方向 |
| --- | --- | --- |
| 审核长期 pending | 代码未被检测、站点没流量、爬虫无法访问 | 检查 code/meta/ads.txt、robots、公开访问 |
| Site not ready | 内容薄、导航弱、主体不明、页面未完成 | 补原创内容、信任页、导航和页面体验 |
| Low value / thin content | 页面无独特价值、复制或模板化 | 增加真实分析、工具说明、作者/来源、内部链接 |
| Policy issue | 某页面广告服务停用 | 修具体 URL 后 request review |
| Regulatory issue | 特定地区需求减少 | CMP、隐私、内容分类和地区规则 |
| Ad serving limited | 展示明显下降 | 停异常来源，降低误点，等待评估 |
| Restricted demand | Fill/RPM 下降 | 检查内容、品牌安全、广告主偏好 |
| 审核通过后马上扣量 | 买量质量差或广告位误点 | 降广告密度、隔离来源、复盘 CTR/IVT |

## 10. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录站点审核、Policy Center、ad serving limit 风险 | `/risk-audits` |
| 导入 source/country/device 级指标 | `/metrics/import` |
| 沉淀 AdSense、Publisher policies 和 invalid traffic 来源 | `/sources` |
| 将页面质量和广告密度问题纳入 Offer 详情页审计 | Offer 详情页 |
| 在无效流量 SOP 中隔离异常来源 | `invalid_traffic_detection_sop.md` |

后续可扩展表：

```text
publisher_site_reviews
adsense_policy_center_issues
ad_serving_limit_events
publisher_site_readiness_checks
policy_review_requests
```

建议字段：

```text
site_domain
review_status
connection_method
adsense_code_status
ads_txt_status
crawler_access_status
policy_issue_type
ad_serving_status
affected_urls
affected_ad_requests
traffic_source
root_cause
fix_summary
review_requested_at
review_result
evidence_urls
```

系统边界：

- 不批量创建站点或账号规避审核。
- 不用镜像站、换域名或 cloaking 绕过站点审核。
- 不生成刷流量、补点击、补展示或“自然流量”任务。
- 不删除证据来掩盖 Policy Center 问题。
- 不用 Cookie 后台操作读取或处理 AdSense。

## 11. QA 清单

- 站点可公开访问，HTTPS 正常，robots 不阻止审核所需 crawler。
- AdSense code、meta 或 ads.txt verification 方法清楚且只用于真实站点。
- 页面有原创内容、清晰导航、About/Contact/Privacy/Disclosure。
- 广告不压过内容，不伪装成导航/下载/播放/下一步。
- 买量来源可按 source/campaign/subid 停量。
- Policy Center 每日检查，按 ad serving impact 排序。
- 出现 ad serving limit 时先停异常来源和高风险广告位。
- Review 只在修复后提交，证据包包含前后截图和来源 URL。
- 站点审核失败不通过换域名、换账号或审核页/用户页差异化处理。
- 恢复后至少等扣量和 finalized revenue 复盘再扩量。

## 12. 信息来源 URL

- Google AdSense Help, Connect your site to AdSense: https://support.google.com/adsense/answer/7584263
- Google AdSense Help, Add a new site to your AdSense sites list: https://support.google.com/adsense/answer/12169212
- Google AdSense Help, Make sure your site's pages are ready for AdSense: https://support.google.com/adsense/answer/7299563
- Google AdSense Help, Overview of the Policy center: https://support.google.com/adsense/answer/9485926
- Google AdSense Help, Policy issues, regulatory issues, advertiser preferences, and ad serving statuses: https://support.google.com/adsense/answer/15689616
- Google AdSense Help, Fix policy issues that affect ad serving: https://support.google.com/adsense/answer/7003627
- Google AdSense Help, Ad serving limits: https://support.google.com/adsense/answer/9437976
- Google AdSense Help, Limited ad serving vs. limited ads: https://support.google.com/adsense/answer/14668281
- Google AdSense Help, Program policies: https://support.google.com/adsense/answer/48182
- Google Publisher Policies: https://support.google.com/adsense/answer/9335564
- Google AdSense Help, Traffic provider checklist: https://support.google.com/adsense/answer/3332805
- Google AdSense Help, Set up a traffic segmentation plan: https://support.google.com/adsense/answer/2583698
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
