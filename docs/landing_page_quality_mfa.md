# 落地页质量、广告密度与 MFA 风险手册

更新时间：2026-06-08

本文解释 Ads 套利里落地页质量、广告密度、桥页、MFA（Made for Advertising）和发布商合规的判断方法。目标不是提高广告堆叠，而是让页面具备独立用户价值、可审核、可长期变现。本文不提供 cloaking、审核页/用户页不一致、诱导点击、广告伪装或无内容页面变现方案。

## 1. 核心原则

一个页面能不能用于长期套利，先看它是否能在不展示广告、不跳转 Offer 的情况下仍然对用户有价值。

合格页面通常有：

- 清晰问题：用户为什么点进来。
- 原创内容：解释、比较、计算、清单、案例、方法或数据整理。
- 透明身份：作者、更新日期、联系方式、隐私政策、广告/联盟披露。
- 可导航：用户能回到首页、分类、相关内容和下一步行动。
- 可审核：Google AdsBot、用户和广告平台看到的是同一类内容和目的地。
- 可测量：页面版本、流量来源、广告位置、CTA 和收入都能对账。

高风险页面通常有：

- 主要内容只是“继续”“查看结果”“下一页”“推荐列表”。
- 广告、弹窗、倒计时、误导按钮或下载按钮压过正文。
- 标题承诺和第一屏内容不一致。
- 内容大量搬运、拼接、模板化，缺少独立观点或工具价值。
- 页面存在多跳中转，最终目的地和广告展示 URL 不一致。

## 2. 页面类型分层

| 页面类型 | 适合套利吗 | 关键要求 |
| --- | --- | --- |
| 对比页 | 适合 | 比较维度真实、优缺点完整、广告/联盟关系披露 |
| 指南页 | 适合 | 解释用户决策过程，有步骤、限制和 FAQ |
| 工具页 | 适合 | 计算器、评分器、清单或模板能独立解决问题 |
| 测评页 | 适合 | 有测试方法、更新日期、适用人群和证据 |
| 本地服务页 | 谨慎 | 联系方式、服务范围、资质和隐私说明要完整 |
| 桥页/网关页 | 高风险 | 只用于把用户送到别处，缺少独立内容 |
| 幻灯片广告页 | 高风险 | 多页点击暴露广告，用户找内容困难 |
| 纯广告聚合页 | 高风险 | 主要目的为展示广告或制造跳转 |

套利团队常见误区是把“能短期出 RPM”的页面当作“能长期稳定”的页面。长期可扩量页面必须同时满足买量平台、发布商政策、用户体验和结算方风控。

## 3. Google Ads 目的地体验

Google Ads 对目的地关注几个点：

- 是否能正常访问：全球常见设备、Google AdsBot 和目标地区用户能访问。
- 是否准确反映目的地：Display URL、Final URL、tracking template 和 expanded URL 指向的内容一致。
- 是否易用安全：没有难以关闭的弹窗、自动下载、误导跳转或滥用体验。
- 是否有原创价值：不是主要为了展示广告，不是复制内容，不是只把用户送去其他网站。

落地页上线前要验证：

```text
Final URL 可访问
移动端可访问
目标国家可访问
HTTP 状态正常
HTTPS 证书正常
无自动下载
无强制弹窗
广告承诺与第一屏一致
追踪模板最终仍到同一内容
```

如果投放系统里用了 tracking template，它必须服务于测量和归因，而不是用于根据 AdsBot、地区、设备、Cookie、IP、登录状态或指纹展示不同页面。

## 4. 广告密度和 Better Ads 标准

广告密度不是“页面上有几个广告位”这么简单，而是广告在主内容区域里占据了多少高度和注意力。

实践中可以用三个阈值做内部红线：

| 场景 | 内部建议 | 高风险信号 |
| --- | --- | --- |
| 移动端主内容广告密度 | 控制在 30% 以下 | 广告占主内容高度过高，用户要频繁越过广告找内容 |
| 桌面端主内容广告密度 | 控制在 50% 以下 | 主内容区域广告高度超过正文体验 |
| Sticky 广告 | 不遮挡内容，不占大面积视口 | 底部/侧边 sticky 过大，移动端遮住 CTA 或正文 |
| 弹窗/插屏 | 避免影响进入内容 | 先弹广告、倒计时、全屏遮挡、自动播放有声视频 |

内部计算方式：

```text
主内容广告密度 = 主内容区内广告高度合计 / 主内容区总高度
```

注意：

- 主内容区不包括页头、页脚、导航和相关文章。
- Sticky 广告只按出现位置计入一次，但仍要看是否遮挡用户任务。
- 视频前贴片如果是页面本身相关视频内容的一部分，和随机展示广告不是同一类体验。
- 不要为了过检测而临时隐藏广告；应从模板层面降低密度和干扰。

## 5. MFA 风险识别

MFA 通常指“为广告而做”的媒体库存。它的核心不是“有广告”，而是“页面主要目标是通过付费流量暴露更多广告，而不是服务用户任务”。

常见特征：

- 付费买量 + 高广告负载。
- 点击诱饵标题，正文价值弱。
- 用户需要不断翻页才能看到很少内容。
- 站点缺乏清晰编辑定位，主题跨度很大。
- 广告密度高、弹窗多、视频广告或 sticky 广告干扰阅读。
- 表面指标好看：viewability、video completion、pageviews 高，但真实购买意图和转化价值弱。
- 流量突然激增，来源解释不清。

MFA 对套利团队的风险：

- 买量端：Google Ads 可能因目的地体验、原创内容不足、桥页或广告网络滥用而拒登或限制。
- 变现端：AdSense/AdX/联盟可能因无效流量、广告密度、低价值内容或诱导点击而扣量。
- 商业端：短期 RPM 可能好看，但用户留存、品牌安全、结算质量和账号寿命都差。

## 6. 内容质量评分

建议 100 分制：

| 维度 | 分值 | 合格标准 |
| --- | --- | --- |
| 意图匹配 | 15 | 广告关键词、标题、第一屏、正文主题一致 |
| 原创价值 | 20 | 有原创解释、比较、数据、工具或方法，不只是聚合 |
| 透明披露 | 10 | 作者、日期、广告/联盟披露、隐私和联系信息 |
| 可导航性 | 10 | 菜单、相关内容、返回路径、CTA 清晰 |
| 技术可达 | 10 | HTTPS、移动端、速度、状态码、目标国家访问正常 |
| 广告体验 | 15 | 广告可识别、不过密、不伪装、不遮挡 |
| 追踪一致 | 10 | Final URL、tracking template、落地页版本一致 |
| 风险证据 | 10 | 有政策检查、来源 URL、上线前审计记录 |

上线建议：

- 80 分以上：可小预算测试。
- 70-79 分：只允许修复后灰度。
- 60-69 分：不建议上线，除非明确修复缺口。
- 60 分以下：拒绝投放或变现。

## 7. 页面上线检查表

上线前逐项确认：

| 检查项 | 通过标准 |
| --- | --- |
| 第一屏 | 用户不用滚动就能确认页面主题和广告承诺一致 |
| 主内容 | 有完整答案、比较、步骤、工具或说明 |
| CTA | 明确但不伪装成系统按钮、下载按钮或广告内容 |
| 广告标签 | 广告可识别，不和菜单、下载、结果按钮混淆 |
| 弹窗 | 不阻断内容，不自动跳转，不诱导点击广告 |
| 移动端 | 字体、按钮、广告、表格和 CTA 不重叠 |
| 速度 | 主要内容可快速加载，广告失败不阻塞正文 |
| 追踪 | UTM/ValueTrack/click_id 不丢失 |
| 目的地 | Final URL、display URL、expanded URL 和页面内容一致 |
| 合规证据 | 保存截图、审计结果、来源 URL 和修改记录 |

## 8. 广告位置实验

广告位置优化应按用户任务来设计，不按“哪里 CTR 最高”来设计。

安全实验：

- 正文首段后一个广告位。
- 章节之间的自然断点。
- 侧栏或文末推荐广告。
- 移动端内容块之间的响应式广告。
- 低干扰 sticky，但必须不遮挡 CTA 和正文。

高风险实验：

- 广告贴着下载、下一步、继续、结果按钮。
- 把广告样式做得像导航、搜索结果或内容卡片。
- 进入页面先弹广告或插屏。
- 为了增加 PV 把短内容拆成多页。
- 用倒计时、误导标签或动态跳转诱导点击。

实验判断不只看 CTR，还要看：

```text
广告收入
页面停留
有效点击率
Offer 转化
扣量比例
退回率
用户是否能完成任务
账号/政策反馈
```

## 9. 复盘模板

```text
页面：
页面版本：
国家/设备：
流量来源：
广告位置版本：
测试周期：

买量点击：
站内 Sessions：
Click -> Session 差异：
页面停留：
广告收入：
Offer 收入：
扣量/拒付：
净 ROI：

质量评分：
广告密度：
政策/目的地问题：
用户体验问题：

结论：
1. 保留 / 降密度 / 重写内容 / 暂停 / 换 Offer
2. 最大收益来源
3. 最大风险来源
4. 下一个页面实验
```

## 10. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录页面 URL、Offer、政策备注 | `/offers` |
| 采集标题、描述、H1/H2、链接数和质量评分 | Offer 详情页的落地页采集 |
| 用质量评分影响机会判断 | `/calculators` 的 content_score、policy_score |
| 记录页面风险和来源 URL | `/risk-audits`、`/sources` |
| 导入页面收入和转化数据 | `/metrics/import` |
| 复盘页面版本和指标 | `/logs`、`/optimization` |

未来可以扩展但仍保持安全边界：

- 页面截图归档。
- 广告密度手工录入和评分。
- 移动端可读性 checklist。
- Final URL / tracking template 一致性检查。
- 不扩展 cloaking、审核页分流、广告伪装或自动点击能力。

## 11. 信息来源 URL

- Google Ads Help, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Help, Destination experience: https://support.google.com/adspolicy/answer/16427615
- Google Publisher Policies, Overview: https://support.google.com/publisherpolicies/answer/10400453
- Google AdSense Help, Ad placement policies: https://support.google.com/adsense/answer/1346295
- Google AdSense Help, Best practices for ad placement: https://support.google.com/adsense/answer/1282097
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Coalition for Better Ads, Better Ads Standards: https://www.betterads.org/standards/
- Coalition for Better Ads, Desktop ad density higher than 50%: https://www.betterads.org/desktop-ad-density-over-50-percent
- IAB UK, A guide to identifying Made for Advertising websites: https://www.iabuk.com/news-article/guide-identifying-made-advertising-websites
- Jounce Media, Terminology: https://jouncemedia.com/resources/terminology
