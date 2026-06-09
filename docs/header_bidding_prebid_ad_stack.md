# Header Bidding / Prebid.js 与广告栈延迟手册

更新时间：2026-06-08

本文说明 Ads 套利发布商在 AdSense、AdX、Google Ad Manager（GAM）、Open Bidding、Header Bidding、Prebid.js 和第三方 SSP 并存时，如何理解页面端竞价、GAM line item、key-value、price granularity、auction timeout、floor、consent、user ID、ads.txt、sellers.json、schain、延迟和最终收入。目标是帮助团队判断“增加 bidder 是否真的提高 session RPM 和可收款收入”，而不是无节制堆需求源、牺牲页面体验或用不透明供应链抬短期 eCPM。

## 1. 为什么 Header Bidding 影响套利收入

Header Bidding 的核心价值是让多个需求方在广告请求进入 ad server 前先竞争库存。对发布商来说，它可能提高竞价压力和 eCPM；对套利团队来说，它也可能带来页面延迟、fill 波动、报表对账复杂化、隐私合规和供应链解释成本。

套利收入不能只看 bidder 返回的 CPM：

```text
sessions
-> page load
-> Prebid auction
-> bidder responses
-> GAM key-value targeting
-> GAM line item match
-> ad render
-> viewable impression
-> estimated revenue
-> finalized / paid revenue
```

如果 Header Bidding 让页面变慢、CLS 上升、广告更晚渲染或 consent 缺失，短期 eCPM 上升也可能被 session depth、viewability、fill、用户体验和最终扣量抵消。

## 2. 核心链路

典型页面端 Header Bidding 链路：

1. 页面加载广告容器和 GPT / ad server 代码。
2. Prebid.js 读取广告位、尺寸、bidder 参数、timeout、floor、consent 和 user ID 配置。
3. 各 bidder 在 timeout 内返回 bid。
4. Prebid 选择或传递价格桶、bidder、deal、size 等 key-value。
5. GPT / GAM 发起 ad request，并携带这些 targeting keys。
6. GAM 用 line item、creative、priority 和 targeting 决定展示。
7. 页面渲染广告，报表分别在 Prebid、GAM、SSP、AdX 或其他需求源中记录。

关键事实：

- Prebid 不替代 GAM；它通常把页面端竞价结果交给 GAM。
- Bidder 返回高价不等于最终展示或最终可收款。
- GAM line item、priority、creative、price bucket 和 key-value 需要和 Prebid 配置一致。
- timeout 是收入和体验之间的硬权衡。
- 多 SSP 会增加供应链、隐私、恶意广告和对账成本。

## 3. Prebid.js 与 GAM 的协作

Prebid.js 常见落地方式是：页面端运行 auction，设置 GAM targeting，再由 GAM 选择对应 line item。套利团队需要理解三组对象：

| 对象 | 作用 | 风险点 |
| --- | --- | --- |
| Ad unit / ad slot | 页面广告位和尺寸 | 尺寸错配会导致 bid 可用但无法展示 |
| Bidder params | SSP / demand partner 所需参数 | 错误参数导致 no bid、低 fill 或不可结算 |
| GAM key-value | 将 bid 信息传给 ad server | key 不一致会导致 line item 不匹配 |
| Price bucket | 把 CPM 映射到离散价格 | 粒度太粗会低估高价 bid，太细会造成 line item 爆炸 |
| Line item | GAM 中承接价格桶的投放对象 | priority、creative、targeting、currency 要一致 |
| Creative | 用于渲染 winner 的 Prebid creative | creative 设置错误会空白、延迟或报错 |

Header Bidding 的上线事故，很多不是“bidder 不行”，而是 Prebid、GPT 和 GAM 三边配置不同步。

## 4. Price Granularity 和 Line Item

Price granularity 决定 CPM 如何映射成 GAM targeting 的价格桶。示例：

```text
bidder returns $1.37
price granularity maps to hb_pb=1.30 or hb_pb=1.35
GAM matches a line item targeted to hb_pb
```

粒度影响：

| 选择 | 好处 | 风险 |
| --- | --- | --- |
| 粗粒度 | line item 少、易维护 | 高价 bid 被低估，yield 损失 |
| 细粒度 | 更接近真实出价 | GAM line item 数量和管理复杂度上升 |
| 分段粒度 | 高价值区间细、低价值区间粗 | 需要历史报表和国家/广告位分层 |

套利团队不要为了“看起来更高 CPM”盲目增加 line item。真正要看的是：价格桶命中率、winner CPM、render rate、fill、viewability、session RPM 和 finalized revenue。

## 5. Auction Timeout、延迟和页面体验

Timeout 是 Header Bidding 的关键参数。太短会错过可成交 bid；太长会阻塞广告请求和页面渲染。

观察指标：

```text
auction_timeout
bid_response_time
bid_rate
win_rate
render_rate
ad_request_time
ad_render_time
viewability
CLS
LCP
session_depth
session_RPM
```

常见判断：

- 如果 timeout 增加后 eCPM 上升，但 session depth、viewability 或 LCP 变差，可能不是净收益。
- 如果某 bidder 平均响应慢且 win rate 低，应考虑暂停或调低优先级。
- 如果移动端延迟高，应该单独看 mobile page template，而不是全站配置。
- 如果 lazy loading、refresh 和 header bidding 同时调整，实验会难以解释。

Header Bidding 实验必须保留 stack version、timeout、bidder list、price granularity、floor 和页面模板版本。

## 6. Floor、竞价密度和 Fill

Header Bidding 与 floor 的关系很容易误判：

- Bidder 多，不代表有效竞价密度高。
- Floor 高，不代表最终收入高。
- Bid rate 高，不代表 render rate 高。
- Prebid winner 高，不代表 GAM 最终一定展示。

需要同时看：

| 指标 | 解释 |
| --- | --- |
| bid request | bidder 是否收到请求 |
| bid rate | bidder 是否响应 |
| bid CPM | 返回价格 |
| timeout rate | 是否超时 |
| win rate | 是否赢得 Prebid 竞价 |
| render rate | 是否实际渲染 |
| GAM fill | ad server 是否填充 |
| revenue | 估算收入 |
| finalized revenue | 可收款收入 |

Floor 实验应按 ad unit、country、device、bidder 和 page template 分层。不要把 GAM unified pricing rules、Prebid floors、SSP floor 和 deal floor 同时改动；一次只改一个主要变量。

## 7. Consent、User ID 与隐私边界

Header Bidding 往往涉及更多第三方需求方、用户识别、同步和地域规则。对发布商套利来说，隐私不是“法务后置项”，而是直接影响 bid rate、CPM、需求可用性和报表解释。

需要检查：

- CMP 是否按地区触发。
- TCF / consent 字段是否传给相关 bidder。
- Google Ad Manager / AdSense 的 consent 要求是否满足。
- User ID module 的使用是否有合法依据、隐私披露和 opt-out。
- 不用指纹、隐藏存储或未披露 ID sync 绕过 consent。
- EEA、UK、Switzerland、US state privacy 等地区规则是否分层。

如果 consent 配置变化导致收入下降，不能简单归因于 bidder 质量；需要把 consent rate、no-consent traffic、personalized/non-personalized demand 和国家维度一起看。

## 8. ads.txt、sellers.json 与 schain

Header Bidding 会增加供应链节点。每接入一个 SSP 或 reseller，都要确认：

- ads.txt 是否授权该 seller。
- sellers.json 中 seller ID、seller type、name、domain 是否可解释。
- schain 是否表达完整供应链。
- DIRECT / RESELLER 关系是否与合同和实际收款关系一致。
- 是否存在过长链路、未知 reseller、域名套壳或库存不透明。

供应链不透明会影响买方信任、CPM、fill 和扣量。对套利团队来说，接入 bidder 前的最小动作不是“拿到参数就上线”，而是先完成供应链 QA。

## 9. 调试和对账

Header Bidding 对账要把页面端、GAM 和 demand partner 分开：

| 层级 | 要查什么 |
| --- | --- |
| Browser / Prebid | ad unit、bidder、timeout、bid response、targeting、errors |
| GPT / GAM request | slot、size、key-value、line item match、creative render |
| GAM report | impressions、line item revenue、ad unit、country、device |
| SSP report | bid request、bid response、win、gross/net revenue、deduction |
| Site analytics | session、viewability、latency、CLS、LCP、bounce |

常见差异原因：

- Prebid 有 bid，但 GAM key-value 没传入。
- GAM line item 没有对应价格桶。
- Creative 配错导致 winner 无法渲染。
- bidder timeout 或 adapter 报错。
- consent 缺失导致 bidder 不参与。
- ads.txt / schain / seller 配置影响买方过滤。
- SSP gross revenue 和 GAM/net/finalized revenue 口径不同。

对账原则：先证明每一层链路可解释，再谈扩 bidder、调 floor 或改 timeout。

## 10. 常见事故

| 事故 | 表现 | 修复方向 |
| --- | --- | --- |
| line item 价格桶缺失 | Prebid 有 bid，GAM 无法命中 | 补齐价格桶、key-value 和 creative |
| bidder 响应慢 | 页面广告晚出、viewability 下降 | 调 timeout、暂停慢 bidder、分设备测试 |
| consent 未传 | EEA 流量 bid rate 断崖 | 检查 CMP、TCF、bidder consent 配置 |
| ads.txt 缺 seller | 某 SSP fill 低或买方过滤 | 补授权、核对 seller ID 和 DIRECT/RESELLER |
| price granularity 太粗 | 高价 bid 被低价桶承接 | 按高价值区间细化粒度 |
| bidder 太多 | 延迟上升、收益不升 | 按净增量和 render rate 淘汰 |
| 报表口径混用 | Prebid winner revenue 和 GAM final 不一致 | 建立 gross/net/finalized 字段 |
| 多变量同时改 | 无法判断收益变化原因 | stack version、单变量实验、回滚点 |

## 11. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Header Bidding 风险、供应链和 consent 审计 | `/risk-audits` |
| 沉淀 Prebid、GAM、IAB 和 Google 来源 | `/sources` |
| 在发布商收入对账中记录 gross/net/finalized 差异 | `revenue_reconciliation_adstack.md` |
| 在广告位实验中记录 viewability、CLS、LCP 和 session RPM | `ad_placement_refresh_viewability.md` |
| 在 GAM Yield 手册中衔接 floor、line item 和 demand partner | `gam_adx_yield_floor_pricing.md` |

后续可扩展表：

```text
header_bidding_stack_versions
header_bidding_bidder_daily
header_bidding_auction_daily
header_bidding_debug_events
```

建议字段：

```text
day
domain
page_template
ad_unit
country
device
stack_version
prebid_version
bidder
timeout_ms
price_granularity
floor_rule
bid_requests
bid_responses
timeout_count
wins
renders
gam_impressions
gross_revenue
net_revenue
finalized_revenue
viewability
cls
lcp_ms
consent_state
ads_txt_status
schain_status
```

系统边界：

- 不生成站点端 Prebid 生产代码。
- 不自动接入 bidder 或写入 GAM。
- 不绕过 consent、TCF、ads.txt、sellers.json 或 schain。
- 不制造 ad requests、impressions、clicks 或 refresh。
- 不用指纹、隐藏 ID 或未披露 sync 恢复用户标识。

## 12. QA 清单

- 每次 Header Bidding 配置有 stack version、变更原因、负责人和回滚点。
- bidder 接入前完成 ads.txt、sellers.json、schain、合同和收款关系 QA。
- GAM key-value、line item、creative、price bucket 与 Prebid 配置一致。
- timeout 按设备、页面模板和 bidder 响应时间测试。
- 同时看 bid rate、win rate、render rate、fill、viewability、session RPM 和 finalized revenue。
- consent / TCF / CMP 状态按地区验证。
- User ID、identity、sync 行为有隐私披露和 opt-out 路径。
- 任何收益增长都要看页面速度、CLS、LCP、用户行为和扣量。
- 多 bidder 接入必须证明净增量，而不是只看毛收入或单 bidder CPM。
- 风险审计中出现“隐藏 seller”“绕 consent”“强制 ID sync”“无限 bidder 堆叠”“自动刷新抬 RPM”等语义时默认 high。

## 13. 信息来源 URL

- Prebid, Prebid.js overview: https://docs.prebid.org/prebid/prebidjs.html
- Prebid, Getting started with Prebid.js: https://docs.prebid.org/dev-docs/getting-started.html
- Prebid, Ad Ops step-by-step: https://docs.prebid.org/adops/step-by-step.html
- Prebid, Price granularity: https://docs.prebid.org/adops/price-granularity.html
- Prebid, Floors module: https://docs.prebid.org/dev-docs/modules/floors.html
- Prebid, Consent Management TCF module: https://docs.prebid.org/dev-docs/modules/consentManagementTcf.html
- Prebid, User ID module: https://docs.prebid.org/dev-docs/modules/userId.html
- Prebid, Supply Chain Object module: https://docs.prebid.org/dev-docs/modules/schain.html
- Prebid, Troubleshooting guide: https://docs.prebid.org/troubleshooting/troubleshooting-guide.html
- Google Publisher Tag, Control ad loading and refresh: https://developers.google.com/publisher-tag/guides/control-ad-loading
- Google Publisher Tag, Ad event listeners sample: https://developers.google.com/publisher-tag/samples/ad-event-listeners
- Google Ad Manager Help, Line item types and priorities: https://support.google.com/admanager/answer/177279
- Google Ad Manager Help, Key-values: https://support.google.com/admanager/answer/177381
- Google Ad Manager Help, Google consent management requirements: https://support.google.com/admanager/answer/14139515
- IAB Tech Lab, Authorized Digital Sellers ads.txt: https://iabtechlab.com/ads-txt/
- IAB Tech Lab, sellers.json: https://iabtechlab.com/sellers-json/
- IAB Tech Lab, SupplyChain Object: https://iabtechlab.com/supplychainobject/
