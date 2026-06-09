# 实验设计、样本量与优化决策手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何设计小预算测试、判断样本是否足够、处理转化/收入延迟、避免被早期 ROI 误导，并把停量、扩量、换素材、换页面、换 Offer 等优化动作变成可审计流程。本文不提供通过补点击、刷展示、模拟自然流量、伪造转化或人为制造样本来“跑出显著性”的方法。

## 1. 实验的目标

套利实验不是证明“某个想法一定赚钱”，而是在有限预算内尽快排除坏假设、保留可验证的好假设。

一个好实验要明确：

```text
目标用户意图
流量来源
页面版本
Offer / 变现方式
创意角度
预算和止损
需要观察的收入窗口
放量或停量条件
```

如果没有这些前提，所谓优化就会变成随机调预算、随机换素材、随机换链接。

## 2. 测试假设模板

```text
假设名称：
业务模式：Display / CPA / CPL / Mixed
国家 / 设备：
流量来源：
关键词或受众：
页面版本：
Offer / Ad stack：
创意角度：

假设：
因为 [用户意图]，当用户看到 [广告承诺] 并进入 [页面任务]，
预计会产生 [收入事件]，可承受 CPC 为 [X]。

成功条件：
停止条件：
观察窗口：
需要等待的回传/结算窗口：
```

示例：

```text
US mobile search users looking for cloud backup pricing
-> pricing calculator page
-> cloud backup affiliate lead
成功条件：100 clicks 后 Net EPC >= CPC * 1.3
停止条件：Cost >= 60 USD 且 approved revenue = 0
观察窗口：点击后 72 小时 + 每周 approved lead 复核
```

## 3. 测试单元

测试单元越混乱，结论越没用。建议一个实验只改变一个主变量：

| 主变量 | 固定项 |
| --- | --- |
| 创意角度 | 同一关键词、页面、Offer、预算 |
| 页面版本 | 同一来源、创意、Offer |
| Offer | 同一来源、页面、创意 |
| 关键词簇 | 同一页面、创意角度、Offer |
| 流量来源 | 同一页面、创意、Offer |
| 出价策略 | 同一 campaign/ad group 结构 |

不要同时换页面、换 Offer、换来源、换素材再说“哪个版本赢了”。那只是两个不同业务包，不是实验。

## 4. 样本量和最小预算

套利实验常见样本单位：

| 模式 | 最小观察单位 | 低样本危险 |
| --- | --- | --- |
| Display / AdSense | sessions、page views、ad impressions | 单日 RPM 波动大 |
| CPA / CPL | clicks、qualified conversions、approved revenue | gross conversion 可能被拒付 |
| Search | search terms、clicks、conversion lag | 早期 CPA 被高估 |
| Native / Social | creatives、sessions、scroll、downstream revenue | 点击便宜但意图弱 |

基础预算：

```text
测试预算 = 目标点击样本 * 预估 CPC
硬止损 = 测试预算 * 1.2
最小收入判断 = 目标 clicks 或目标 sessions 达成后再看
```

经验阈值：

- Search 长尾：50-100 clicks 可判断明显坏流量和搜索词偏差。
- CPA/CPL：至少等到第一批 conversion 经过 approval window。
- Display 内容套利：至少跨 2-3 天和多个时段，避免单日 RPM 偏差。
- Native/Social：每个创意角度至少有足够 impressions/clicks 才判断素材。

这些不是统计学保证，而是运营上的最低止损线。真正放量要靠更长窗口和结算后收入。

## 5. 显著性和实际意义

实验判断要区分：

- 统计显著：差异可能不是随机波动。
- 商业显著：差异足够大，能覆盖扣量、现金流和执行成本。
- 风险显著：虽然赚钱，但政策/扣量/账号风险不可接受。

套利团队常犯错：

- 样本很小就因为 ROI 高而放量。
- 只看 CTR 或 CVR，不看 approved revenue。
- 把 estimated revenue 当 paid revenue。
- 忽略 conversion lag，过早暂停好 campaign。
- 忽略扣量，保留坏来源。

内部建议：

```text
只有同时满足商业收益、可解释来源、政策通过、扣量可接受，才算胜出。
```

## 6. 回传延迟和收入延迟

Google Ads conversion lag 会让 CPA 看起来偏高、ROAS 看起来偏低；联盟和 AdSense 也有 pending、finalized、扣量和付款延迟。

决策前要标记：

| 收入口径 | 是否可用于放量 |
| --- | --- |
| estimated same-day revenue | 只能观察趋势 |
| pending conversion revenue | 谨慎，按 approval rate 折扣 |
| approved revenue | 可用于小幅扩量 |
| finalized revenue | 可用于长期模型 |
| paid revenue | 可用于现金流和预算上限 |

实践：

- Search / PMax 要看 conversion lag 报告或历史延迟。
- CPA/CPL 要等 approval window。
- AdSense/AdX 要看 finalized earnings 和 deduction。
- 指标导入时保留 day，不要把收入延迟误认为当天亏损。

## 7. 实验分流

可选方式：

| 方式 | 适合 | 注意 |
| --- | --- | --- |
| Google Ads Experiments | 测试 bidding、campaign structure、asset changes | 不要在实验中途频繁改 base campaign |
| Campaign 拆分 | 测试国家、来源、页面、Offer | 预算和流量可能不均衡 |
| Ad group 拆分 | 测试意图簇或关键词 | 需要防止词互抢 |
| URL 参数 / landing_version | 测试页面版本 | 不可做审核页/用户页不一致 |
| 手工灰度 | 高风险变更、链接和预算 | 必须保留审批和日志 |

本系统当前采用 campaign draft + CSV/Scripts JSON + 指标导入 + 优化建议的安全流程。它不直接在 Google Ads 后台创建实验，也不自动执行高风险变更。

## 8. 优化动作分级

| 等级 | 动作 | 是否可自动 |
| --- | --- | --- |
| L1 读和建议 | 生成报表、标记亏损、建议否定词 | 可自动生成 |
| L2 低风险草稿 | 生成创意变体、CSV 草稿、Scripts JSON | 可自动生成，需人审 |
| L3 中风险变更 | 降预算、暂停关键词、替换素材 | 需人工确认 |
| L4 高风险变更 | 大幅加预算、换 Final URL、启停 campaign | 需双人审核或审批 |
| 禁止 | 补点击、刷展示、模拟转化、cloaking | 不实现 |

优化不是“系统替人点按钮”，而是把决策证据整理出来，让人更快做对。

## 9. 停量、保留、扩量规则

停量：

- Cost >= 硬止损且没有可解释收入。
- click -> session 异常低。
- conversion 高但 rejected 高。
- 出现 policy、invalid traffic、ad serving limit。
- 来源或供应商拒绝提供明细。

保留观察：

- ROI 接近盈亏平衡，但样本不足。
- conversion lag 明显，尚未过窗口。
- Search terms 质量好但页面转化弱。
- RPM 有波动但 finalized 还没出来。

小幅扩量：

- Net ROI 为正。
- approved/finalized revenue 支撑。
- 扣量可接受。
- 来源可解释，能按 source/campaign 停。
- 每日预算提升 10%-30%，观察新窗口。

拒绝放量：

- 只靠 gross conversion 赚钱。
- 只靠 estimated revenue 赚钱。
- 需要隐藏来源或规避审核。
- 页面/创意/Offer 承诺不一致。

## 10. 复盘口径

每个实验结束必须保存：

```text
实验假设：
测试单元：
预算和止损：
实际花费：
点击 / sessions：
转化 / approved / rejected：
estimated / finalized / paid revenue：
扣量原因：
政策或账号状态：
结论：
下一步：
```

复盘不要只写“亏了”或“赚了”。要回答：

- 哪个变量贡献最大？
- 是流量问题、页面问题、Offer 问题，还是追踪问题？
- 下次该保留什么、删除什么、再测什么？
- 这次经验是否能复用到其他国家/设备/Offer？

## 11. 系统落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer、页面和限制 | `/offers` |
| 估算 CPC、CVR、RPM、测试预算和硬止损 | `/calculators` |
| 创建 campaign 草稿和导出版本 | `/campaigns` |
| 导入实验结果 | `/metrics/import` |
| 生成优化建议 | `/optimization` |
| 记录风险、来源和政策证据 | `/risk-audits`、`/sources` |
| 安排日报、周报、URL 检查和结算复盘 | `/tasks` |
| 留存导出、轮换和运行日志 | `/logs` |

未来可扩展：

- Experiment 表：记录 hypothesis、variant、budget、window、status。
- Cohort 收入导入：按 click_date 和 revenue_date 分离。
- Approval/rejection 字段：支持 CPA/CPL 净收入分析。
- 但仍不做模拟样本、刷指标或自动高风险变更。

## 12. 信息来源 URL

- Google Ads Help, Test with confidence with the Experiments page: https://support.google.com/google-ads/answer/7281575
- Google Ads Help, About the Experiments page: https://support.google.com/google-ads/answer/10682377
- Google Ads API, Experiments overview: https://developers.google.com/google-ads/api/docs/experiments/overview
- Google Ads API, Create experiments: https://developers.google.com/google-ads/api/docs/experiments/experiments
- Google Ads Scripts, Campaign Drafts and Experiments: https://developers.google.com/google-ads/scripts/docs/campaigns/drafts-experiments
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, About conversion delay estimates: https://support.google.com/google-ads/answer/14545572
- Google Ads Help, Find out how long it takes for your customers to convert: https://support.google.com/google-ads/answer/6239119
- Google Analytics Help, GA4 data freshness: https://support.google.com/analytics/answer/11198161
- Google AdSense Help, Payment timelines: https://support.google.com/adsense/answer/7164703
- Google AdSense Help, Deductions from earnings FAQs: https://support.google.com/adsense/answer/2808531
