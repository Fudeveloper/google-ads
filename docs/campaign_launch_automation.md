# Google Ads 投放结构与安全自动化手册

更新时间：2026-06-08

本文说明 Ads 套利业务里如何设计 Google Ads 投放结构、预算、出价、关键词、否定词、批量上线和安全自动化流程。本文只覆盖可审计的 Campaign 草稿、Google Ads Editor CSV、Google Ads Scripts/API 方向、人工审核和指标回流；不提供 Ads Cookie 后台接管、绕过登录/2FA、安全挑战、审核系统或封禁规避的方案。

## 1. 投放结构的目标

投放结构不是为了“看起来整齐”，而是为了让每一笔钱都能被解释、暂停和复盘。

健康结构要满足：

- 成本可控：预算在 campaign 或 account budget 层面有上限。
- 意图清晰：ad group 只承载一类关键词或用户意图。
- 页面一致：广告、关键词、Final URL、落地页和 Offer 一致。
- 追踪完整：campaign/ad group/keyword/creative/device/source 能回到收入。
- 风险隔离：高风险垂类、新 Offer、新国家、新页面不和稳定业务混在一起。
- 变更可审计：每次导入、脚本运行、预算调整和 URL 修改都有记录。

## 2. Google Ads 层级

Google Ads 可以按下面层级理解：

```text
Manager account / Ads account
  -> Campaign
      -> Ad group
          -> Keywords / Audiences / Placements
          -> Ads / Assets
      -> Budget / bid strategy / location / language / network
```

在套利场景里，建议：

| 层级 | 放什么 | 不要放什么 |
| --- | --- | --- |
| Account | 付款、权限、转化、基础品牌或业务线 | 不同风险来源混账 |
| Campaign | 国家、语言、网络、预算、目标、主要 Offer | 多个国家/垂类/页面混在一个预算池 |
| Ad group | 单一意图、相近关键词、同一页面主题 | 互相抢量的宽泛关键词 |
| Ad / Asset | 与该意图匹配的 RSA、sitelink、callout | 页面没有证据的承诺 |
| Keyword / Search term | 真实触发意图和清理对象 | 用宽泛词掩盖归因问题 |

## 3. 命名规范

命名要让日报和导出文件不用猜。

```text
{channel}-{country}-{vertical}-{offer}-{intent}-{device}-{date}
```

示例：

```text
gads-us-cloudbackup-offer01-compare-mobile-202606
gads-ca-taxrefund-offer02-calculator-all-202606
```

推荐字段：

| 字段 | 示例 |
| --- | --- |
| channel | `gads_search` |
| country | `us` |
| vertical | `cloudbackup` |
| offer | `offer01` |
| intent | `compare`、`calculator`、`pricing` |
| device | `mobile`、`desktop`、`all` |
| page | `lp-a3` |
| test | `t001` |

不要用“测试1”“新系列”“跑跑看”“过审版”这类无法复盘的名字。

## 4. Campaign 拆分原则

建议单独拆 campaign 的情况：

- 国家不同：CPC、RPM、Offer 允许地区和付款能力不同。
- 语言不同：关键词、文案和页面证据不同。
- 网络不同：Search、Display、Demand Gen、YouTube 的意图和指标完全不同。
- 预算风险不同：冷启动、稳定放量、恢复测试要隔离。
- Offer 或结算方不同：扣量和回款周期不同。
- 页面版本不同且需要独立预算。

不建议过度拆分：

- 每个关键词一个 campaign，导致预算碎片化。
- 只有微小文案差异就拆 campaign，导致学习和管理成本上升。
- 还没跑出样本就按几十个设备/时段/人群拆。

套利冷启动推荐：

```text
1 个国家
1 个语言
1 个网络
1 个 Offer
1-3 个页面版本
3-8 个 ad groups
每个 ad group 1 个主要意图
每个意图 5-20 个关键词或主题
```

## 5. Ad Group 与关键词

Ad group 的核心是“意图一致”：

| 意图 | 示例关键词 | 页面 |
| --- | --- | --- |
| compare | `best cloud backup for small business` | 对比页 |
| pricing | `cloud backup cost calculator` | 计算器页 |
| alternative | `dropbox business alternative` | 替代方案页 |
| how-to | `how to backup office files` | 指南页 |

关键词策略：

- 冷启动优先 phrase/exact 和明确长尾词。
- broad match 要等追踪、否定词、转化和扣量模型稳定后再测试。
- 不要用 brand bidding 触碰 Offer 禁止条款。
- 不要把搜索词和关键词混为一谈：关键词是投放设置，search term 是真实触发查询。

## 6. 搜索词报告与否定词

搜索词报告用于回答：

- 哪些真实查询带来点击和收入？
- 哪些查询只消耗预算？
- 哪些查询显示广告承诺和页面不匹配？
- 哪些查询可能触发政策或低质量 lead？

否定词分层：

| 层级 | 用途 | 示例 |
| --- | --- | --- |
| Account-level negative list | 全账号都不想要 | `free movies`、`jobs`、`torrent` |
| Campaign negative | 某个国家/Offer 不适合 | `government grant` |
| Ad group negative | 防止意图串组 | compare 组否定 `login`、`support` |

日常节奏：

- 冷启动前 3 天每天看 search terms。
- 稳定后每周清理一次。
- 每次清理记录：新增词、层级、原因、影响 campaign。
- 不要把高质量长尾词误杀；先看 session、conversion、revenue 和 Offer 限制。

## 7. 预算和出价

Google Ads 的平均日预算不是严格的每日花费上限。平台可能为了流量波动在某些天花费超过平均日预算，因此套利团队要有外部预算表和硬止损。

预算设计：

```text
测试预算 = 目标点击样本 * 预估 CPC
硬止损 = 测试预算 * 1.2
月度现金预算 = 日预算 * 现金缺口天数 + 应急储备
```

出价策略：

| 阶段 | 可用策略 | 注意 |
| --- | --- | --- |
| 冷启动 | Manual CPC / Maximize Clicks with caps | 先买样本，不追求规模 |
| 有稳定转化 | Maximize Conversions | 需要可靠 conversion 和收入口径 |
| 有批准收入和价值 | Target CPA / Target ROAS | 要把扣量、拒付、现金流纳入目标 |
| 低样本套利 | 谨慎使用智能出价 | 算法优化的 conversion 未必等于可收款收入 |

放量规则：

- 每次预算提升 10%-30%，观察至少 1-3 天或一个回传窗口。
- 不在 estimated revenue 短期上涨时大幅加预算。
- 单一 source、keyword、ad group 未经历结算前不能无限扩。
- 出现扣量、拒付、Policy warning 时停止扩量。

## 8. Google Ads Editor CSV 流程

Editor/CSV 适合批量上线，但要保留人工确认：

1. 系统生成 Campaign 草稿。
2. 导出 Google Ads Editor CSV。
3. 投手在 Editor 里导入并检查字段。
4. 检查 Final URL、budget、bid strategy、keywords、ads、negative keywords。
5. 使用 Editor 的检查/预览能力发现错误。
6. 由授权人员发布到 Google Ads。
7. 回到系统记录导出时间、执行人、版本和结果。

适合 CSV 的操作：

- 批量创建 campaign/ad group/keyword/ad 草稿。
- 批量更新 Final URL 或预算草案。
- 批量添加否定词。
- 批量暂停明显失败的结构，但仍建议人工确认。

不适合直接 CSV 自动发布：

- 高风险 URL 变更。
- 大幅预算提升。
- 敏感垂类文案。
- 未经页面审计的新 Offer。

## 9. Google Ads Scripts / API 安全自动化

安全自动化原则：

- 使用授权用户、OAuth、Scripts 或官方 API，不处理用户密码或登录 Cookie。
- 默认 dry-run，输出计划，不直接执行高风险动作。
- 预算、URL、暂停/启用、关键词扩展都要有审批阈值。
- 每次运行写审计日志：输入、输出、差异、执行人、时间。
- 幂等：同一 payload 重复运行不会重复创建或重复扣动预算。
- 可回滚：保留旧值和变更记录。

本系统的 `/campaigns` 页面把 ADXKit 类“一键提交投放”拆成内部状态机：`draft`、`reviewing`、`approved`、`exported`、`paused`、`rejected`。状态变化写入审计日志，只表示草稿是否进入评审、是否批准导出、是否暂停或拒绝；它不会自动登录 Google Ads，不会自动发布广告，也不会接受 Recommendations 或绕过审核。

任务分级：

| 等级 | 示例 | 执行方式 |
| --- | --- | --- |
| 低风险读 | 拉取报表、检查 URL、导出结构 | 可定时 |
| 中风险建议 | 生成否定词建议、预算建议、暂停建议 | 人审后执行 |
| 高风险写 | 修改预算、Final URL、启停 campaign | 双人审核或明确审批 |
| 禁止 | Cookie 后台接管、绕 2FA、审核分流、模拟点击 | 不实现 |

## 10. 优化建议的正确使用

Google Ads 的 optimization score 和 recommendations 是诊断输入，不是套利利润目标。

可以参考：

- 缺少资产。
- 预算受限。
- 关键词或否定词机会。
- 竞价策略配置异常。
- 追踪或转化设置问题。

不能盲目自动应用：

- 增加预算。
- 放宽关键词匹配。
- 自动创建大量资产。
- 改变 bidding strategy。
- 开启自动应用推荐。

套利团队的最终判断应按：

```text
approved_revenue
paid_revenue
deduction_rate
net_roi
cash_buffer_days
policy_status
```

而不是只按 optimization score。

## 11. 上线检查表

| 检查项 | 通过标准 |
| --- | --- |
| Offer | 允许 Google Ads、国家、设备、流量类型 |
| Landing | 页面可达、内容一致、广告密度合格 |
| Tracking | UTM、ValueTrack、click_id、subid 完整 |
| Campaign | 国家、语言、网络、预算、出价策略正确 |
| Ad group | 意图单一，关键词和创意一致 |
| Ads | RSA 文案可被页面证据支撑 |
| Negative | 基础否定词和品牌/禁止词已设置 |
| Budget | 测试预算、硬止损、现金流缓冲记录清楚 |
| Export | CSV / Scripts JSON 已保存版本 |
| Approval | 人工审核记录和风险审计完成 |

## 12. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录账号同步方式和状态 | `/accounts` |
| 生成 Offer 和页面基础信息 | `/offers` |
| 生成创意和关键词候选 | Offer 详情页 |
| 创建 Campaign 草稿 | `/campaigns` |
| 导出 Google Ads Editor CSV | `/campaigns/<id>/export.csv` |
| 导出 Scripts JSON payload | `/campaigns/<id>/export.script.json` |
| 导入指标做优化判断 | `/metrics/import` |
| 生成暂停/优化建议 | `/optimization` |
| 通过任务中心检查导出、URL 和报表 | `/tasks` |
| 记录风险和来源 URL | `/risk-audits`、`/sources` |

CSV / Scripts JSON 导出和任务中心导出检查都会先执行 campaign preflight：草稿必须已批准，Claim 审核不能还有 open、rewrite_required 或 blocked，广告审核案例不能还有 open、appeal_submitted 或 rejected。未通过时系统写入 `export_blocked` 审计日志，不生成可上传 payload。

## 13. 信息来源 URL

- Google Ads API, Campaigns overview: https://developers.google.com/google-ads/api/docs/campaigns/overview
- Google Ads Help, Create a search campaign: https://support.google.com/google-ads/answer/9510373
- Google Ads Help, About negative keywords: https://support.google.com/google-ads/answer/2453972
- Google Ads Help, About the search terms report: https://support.google.com/google-ads/answer/2472708
- Google Ads Help, Get negative keyword ideas using the search terms report: https://support.google.com/google-ads/answer/7102466
- Google Ads Help, Budgets overview: https://support.google.com/google-ads/answer/10486536
- Google Ads Help, About automated bidding: https://support.google.com/google-ads/answer/2979071
- Google Ads API, Bidding strategy types: https://developers.google.com/google-ads/api/docs/campaigns/bidding/strategy-types
- Google Ads Help, Check your optimization score: https://support.google.com/google-ads/answer/9061547
- Google Ads Help, Types of recommendations: https://support.google.com/google-ads/answer/3416396
- Google Ads Scripts, Bulk Upload: https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload
- Google Ads Scripts, Authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- Google Ads Editor: https://ads.google.com/home/tools/ads-editor/
