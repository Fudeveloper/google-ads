# 买量渠道与流量供应商尽调手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何评估买量渠道和外部流量供应商，包括 Google Search、Search Partners、Display、Demand Gen、Performance Max、Native、Social、Newsletter、Direct buy、流量供应商和代理渠道。目标是用小预算、真实追踪和来源隔离判断流量质量；不是购买不可解释低价流量、模拟自然访问、使用代理/指纹规避、隐藏来源或把低质流量灌进 AdSense/AdX/Offer。

## 1. 先看“来源可解释性”

所有流量先分 4 级：

| 等级 | 描述 | 可测试性 |
| --- | --- | --- |
| A | 平台、campaign、ad group、keyword/placement、creative、device、geo 都可见 | 可测试 |
| B | 平台和 campaign 可见，但 placement/publisher 不完整 | 小预算谨慎测试 |
| C | 只给总点击或总 session，不给来源明细 | 不建议测试 |
| D | 要求隐藏 referrer、去参数、代理转发、模拟自然 | 拒绝 |

套利不是买“便宜点击”，而是买可解释、可停量、可对账的用户意图。来源解释不清，后面所有 RPM、EPC、ROI 都只是表面数。

## 2. 渠道分层

| 渠道 | 用户意图 | 优点 | 常见风险 |
| --- | --- | --- | --- |
| Google Search | 高 | 意图强、搜索词可复盘 | CPC 高、政策严格、交易词竞争强 |
| Search Partners | 中到高，波动大 | 可扩量、部分行业 CPC 低 | 来源透明度低、质量差异大 |
| Display / Demand Gen | 中到低 | 覆盖广、素材驱动 | 误点、低意图、展示质量和页面体验压力 |
| Performance Max | 混合 | 覆盖多库存、自动化强 | 黑盒程度高、套利早期难定位 source |
| Native / Content discovery | 中 | 内容角度容易扩 | 标题党、页面不一致、MFA 风险 |
| Social | 中 | 人群和素材角度丰富 | 转化链路长、归因波动、政策差异 |
| Newsletter / Direct buy | 中到高 | 媒体语境清楚 | 供应商报表、受众真实性和价格风险 |
| 流量供应商/中介 | 不确定 | 便宜、量大 | 无效流量、来源不透明、扣量和账号风险 |

## 3. Google Search

适合：

- 比较型、价格型、替代型、明确任务型关键词。
- CPA/CPL、工具页、比较页、指南页。
- 需要搜索词报告快速学习用户意图的冷启动。

重点看：

```text
Search term
Match type
CPC
Click -> session
CVR / Session RPM
Approved revenue
Policy disapproval
```

测试建议：

- 冷启动用 exact / phrase。
- 每个 ad group 一个意图簇。
- 先关掉不必要的网络扩展，建立 Google Search 本体基线。
- 每天看 search terms，加入否定词。
- 交易词如果 CPC 高于安全 RPV/EPC，不硬冲。

## 4. Search Partners

Search Partners 可能带来额外量，但质量波动较大。它适合在主 Search 基线已经稳定后，作为单独测试项。

测试原则：

- 单独 campaign 或至少单独 network segment 看数据。
- URL 参数中保留 `{network}`、campaign、ad group、keyword、device。
- 不把 Search Partners 的平均数据和 Google Search 混成一个 ROI。
- 一旦 click -> session、conversion、revenue、扣量显著差于 Search，就暂停。

拒绝信号：

- 只在 Search Partners 上花费，Google Search 本体几乎没有量。
- 点击量高但 session 低。
- CTR/CVR 异常高但 approved revenue 差。
- 无法解释下游页面或 publisher 质量。

## 5. Display / Demand Gen

Display 和 Demand Gen 更像“内容/兴趣触达”，不是用户主动搜索。它们适合有强素材、强页面承接和足够预算做素材实验的业务。

适合：

- 垂直内容站。
- 低风险信息型页面。
- 有明确视觉素材和受众假设。
- 再营销或类似人群，但要满足 consent 和个性化广告要求。

风险：

- 用户意图弱，短期点击便宜但转化差。
- 广告靠视觉误导容易带来低质量 session。
- Placement / inventory 质量不均。
- 展示广告流量进入发布商广告页面时，要格外关注无效流量和广告密度。

测试建议：

- 用独立页面版本和 campaign。
- 分设备看 mobile accidental click。
- 不用过高广告密度吸收低意图流量。
- 先看 session 行为，再看 estimated revenue，最后看 finalized revenue。

## 6. Performance Max

Performance Max 覆盖多个 Google Ads inventory，自动化程度高。它适合已有稳定转化和清楚目标的业务，不适合在套利冷启动时当作黑盒找方向。

适合：

- 已有转化数据。
- Offer、页面和 conversion action 稳定。
- 有预算承受探索成本。
- 能接受渠道归因和 inventory 透明度较低。

不适合：

- 新 Offer、新页面、新账号同时测试。
- 还没有 approved revenue 和扣量模型。
- 必须精确知道每个 placement/source 质量的高风险阶段。

套利团队用 PMax 前要先问：

1. conversion 是否代表可收款收入？
2. 是否有扣量和拒付回传？
3. 预算是否能承受探索？
4. 是否能把 PMax 与 Search/Display/Native 的结果分开？

## 7. Native / Content Discovery

Native 常用于内容套利和联盟预热页，但也是 MFA 和误导标题高发渠道。

适合：

- 信息型、故事型、指南型页面。
- 有真实内容和后续 CTA。
- 可按 publisher/placement/source id 停量。

高风险：

- 标题承诺与页面不一致。
- 页面主要为了翻页和广告曝光。
- publisher 质量不透明。
- 低价大流量但无 source 明细。

测试时必须要求：

- source/publisher/placement 维度。
- click_id 或 subid。
- 退款/扣量原因。
- 小预算白名单或黑名单机制。

## 8. Social

Social 流量由素材、人群和内容语境驱动。它更适合垂直内容站、工具页、教育型 funnel，而不是直接把低意图用户送去高广告密度页面。

重点看：

- 素材角度是否误导。
- 用户进入页面后的停留和 scroll。
- 转化是否由真实意图驱动。
- 归因窗口和 postback 是否一致。
- 是否触发平台自己的广告政策。

社交流量进入 AdSense/AdX 页面时，要特别关注：

- click -> session 差异。
- ad CTR 是否异常。
- 页面广告密度。
- 来源突然放量后的 finalized revenue 和扣量。

## 9. Newsletter / Direct Buy

Newsletter、媒体直采、社区赞助可以是高质量来源，但需要供应商尽调。

供应商必须提供：

- 媒体名称和样例 URL。
- 历史发送频率、订阅来源、打开率、点击率。
- 受众国家、语言、行业。
- 是否有 bot/click filtering。
- 是否允许 UTM、click_id、subid。
- 是否能按 placement/source 停量或退款。

小测：

- 单独 landing page 或至少单独 source id。
- 限制首单预算。
- 看 clicks、sessions、time on page、conversion、revenue。
- 不用供应商自己的点击报表代替站内数据。

## 10. 流量供应商尽调表

| 问题 | 合格回答 | 拒绝信号 |
| --- | --- | --- |
| 流量从哪里来 | 可列平台、媒体、placement、投放方式 | “内部渠道”“保量流量”但不给明细 |
| 用户为什么点击 | 广告语、页面、媒体语境清楚 | 激励、自动浏览、弹窗、误导 |
| 是否允许追踪 | 允许 UTM、click_id、subid | 不允许参数或要求隐藏来源 |
| 是否能停量 | 能按 source/publisher/campaign 停 | 只能整体买包 |
| 是否有质量报告 | 提供历史转化、扣量、退款数据 | 只有低价和大流量承诺 |
| 是否合规 | 不涉及 bot、代理、指纹、激励 | “模拟自然”“补真实用户行为” |

供应商评分：

```text
source_transparency 25
tracking_support 20
traffic_intent 20
historical_quality 15
stop_loss_control 10
policy_fit 10
```

低于 75 不进入测试；任一红线为 0 则直接拒绝。

## 11. 小预算测试流程

```text
供应商/渠道尽调
-> 建独立 source_id
-> 单独 campaign / landing / link rule
-> 设置预算和硬止损
-> 导入每日指标
-> 看 click -> session -> revenue -> approved/finalized
-> 决定保留、暂停、降级或放量
```

硬止损：

- `clicks >= 样本阈值` 且 `sessions/clicks` 异常低。
- `cost >= 测试预算` 且 `revenue = 0`。
- source 有 invalid traffic、policy、deduction 提醒。
- 供应商拒绝提供 source 明细。
- 页面指标显示误点或低意图。

## 12. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录渠道、Offer、URL 和政策限制 | `/offers` |
| 用 source_score 参与机会评分 | `/calculators` |
| 用 Campaign 草稿隔离渠道测试 | `/campaigns` |
| 用 UTM/click_id/subid 设计追踪 | 流量追踪手册、Campaign final URL |
| 导入每日成本和收入 | `/metrics/import` |
| 根据 ROI 和异常生成优化建议 | `/optimization` |
| 记录供应商尽调、来源 URL 和风险 | `/sources`、`/risk-audits` |
| 用任务中心安排日报、URL 检查和导出检查 | `/tasks` |

系统不做：

- 不采购或转售不可解释流量。
- 不模拟自然流量。
- 不隐藏 referrer 或剥离追踪参数。
- 不用代理、指纹、Worker 转发规避检测。
- 不把供应商 API 做成自动灌流量能力。

## 13. 信息来源 URL

- Google AdSense Help, Traffic provider checklist: https://support.google.com/adsense/answer/3332805
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google AdSense Help, Set up a traffic segmentation plan: https://support.google.com/adsense/answer/2583698
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google Ad Traffic Quality: https://www.google.com/ads/adtrafficquality/
- Google Ad Traffic Quality resources for publishers: https://www.google.com/intl/en/ads/adtrafficquality/publishers/
- Google Ads Help, Google Network: https://support.google.com/google-ads/answer/1752334
- Google Ads Help, About Display ads and the Google Display Network: https://support.google.com/google-ads/answer/2404190
- Google Ads Help, About Performance Max campaigns: https://support.google.com/google-ads/answer/10724817
- Google Ads Help, Create a Demand Gen campaign: https://support.google.com/google-ads/answer/13695389
- Google Ads API, AdNetworkType: https://developers.google.com/google-ads/api/reference/rpc/v20/AdNetworkTypeEnum.AdNetworkType
