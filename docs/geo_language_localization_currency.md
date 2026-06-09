# Geo、语言、本地化、时区与币种分层手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何处理国家/地区、语言、设备、时区、币种、本地化页面、地理报表、bad geo、location options、dayparting 和汇率归一。目标是让团队能判断“某个国家或语言是否真的可扩量”，而不是把不同地区、语言、付款能力、政策、payout、时区和页面证据混成一个平均 ROI。

## 1. 为什么 Geo / Language 是套利核心变量

同一个 Offer 在不同国家可能完全不是同一门生意：

- CPC、竞争强度和搜索意图不同。
- payout、approval rate、reject reason 和付款周期不同。
- 页面语言、价格、资格、电话格式、地址、隐私披露不同。
- 监管、认证、敏感垂类限制和广告审核不同。
- AdSense/AdX RPM、fill、扣量和广告主价值不同。
- 时区和币种不同会让日报、ROI、dayparting 和结算错位。

因此，套利测试的最小可解释单元通常是：

```text
offer + country/region + language + device + traffic source + page version + payout currency
```

如果只看 campaign 总 ROI，往往会被高价值国家、小量低质国家或错误语言流量误导。

## 2. 核心对象

| 对象 | 含义 | 套利风险 |
| --- | --- | --- |
| Target location | Google Ads 目标国家、地区、城市、半径或位置组 | 过宽会吸入不允许地区 |
| Location option | presence / interest 相关设置 | “对某地感兴趣”的用户可能不在目标地区 |
| Language targeting | 用户理解的语言信号 | 不是页面翻译工具，不能替代本地化 |
| Device | desktop、mobile、tablet、TV 等 | mobile 误点、速度和 lead quality 差异大 |
| Account timezone | Google Ads 账号日报边界 | dayparting 和日报对账会受影响 |
| Account currency | Google Ads 账单币种 | 设置后难改，ROI 需要换算 |
| Offer payout currency | 联盟或 buyer 结算币种 | 和成本币种不一致会造成利润错算 |
| Localized page | 本地语言、价格、条款、主体和 CTA | 不一致会触发 misrepresentation 或 cloaking 风险 |

## 3. Location Targeting 和 Presence / Interest

Google Ads 地理定位可以按国家、地区、城市、半径或位置组投放。更关键的是 location options：广告可能展示给在目标地点的人，也可能展示给对目标地点表现出兴趣的人，具体取决于设置。

套利团队要明确：

- 如果 Offer 只允许美国用户，通常要优先检查是否只触达目标地实际用户或经常在该地的用户。
- 如果页面是旅游、教育、移民、跨境购物等“对某地感兴趣”合理场景，可以保留更宽设置，但要单独分层看 ROI。
- bad geo 高时，先查 location options、search terms、IP/表单国家、postback reject reason 和页面语言。
- 不能用代理、指纹或 cloaking 假装用户来自某地。

QA 问题：

```text
这个用户为什么会看到该国家的广告？
该用户是否满足 Offer 地区要求？
广告文案和页面是否清楚说明服务地区？
postback / buyer feedback 是否按地区拒付？
```

## 4. Language Targeting 与页面本地化

Language targeting 不是把广告自动翻译成目标语言，也不是保证用户母语一定匹配。它用于触达 Google 判断理解某语言的用户。

本地化要同时处理：

| 层级 | 需要一致 |
| --- | --- |
| Keyword / query | 用户搜索语言和意图 |
| Ad copy | 标题、描述、CTA 和限制 |
| Landing page | 语言、价格、条款、主体、隐私、披露 |
| Form / lead | 电话、邮编、省州、年龄、资格 |
| Offer terms | 允许国家、设备、来源和垂类限制 |
| Support / next step | 用户提交后谁联系、用什么语言、什么时间 |

常见错误：

- 英文广告送到机器翻译页面。
- 页面货币、电话格式、地址和目标国家不一致。
- 广告说“local”但页面主体、服务区域和资格不清楚。
- 同一页面用多个国家混跑，导致 bad geo 和低 approval。
- 把本地化做成审核/用户不一致的地区分流。

正常本地化应保持同主题、同承诺、同业务目的；如果按地区展示完全不同 Offer 或隐藏受限内容，应按 cloaking 风险处理。

## 5. Device 分层

设备不是小维度。移动端和桌面端在套利中经常是两套经济模型：

- 移动端 CPC 可能低，但误点、跳转失败、表单质量和页面速度风险更高。
- 桌面端量可能小，但阅读深度、表单质量或 B2B 意图更强。
- Tablet 和 TV 屏幕在某些 campaign type 中可能带来难解释流量。
- Device bid adjustment 或 -100% 排除在不同 campaign / bidding strategy 下支持边界不同，必须按官方文档和当前 campaign 类型确认。

设备复盘最少看：

```text
cost
clicks
landing_requests
sessions
conversions
approved_revenue
paid_revenue
reject_reason
page_speed
form_completion
```

不要只因为 mobile CTR 高就扩量；要看 mobile 的 paid revenue、bad lead、页面速度和扣量。

## 6. 时区、Dayparting 和回传延迟

时区会影响：

- Google Ads 日报。
- AdSense/GAM 收入日期。
- 联盟 postback 日期。
- GA4 session 日期。
- dayparting 判断。
- 预算 overdelivery 和日报止损。

Google Ads 账号时区和币种属于账号级关键设置。套利团队应在建账号或接管账号时记录：

```text
account_timezone
account_currency
billing_country
reporting_timezone
internal_reporting_timezone
offer_payout_timezone
settlement_timezone
```

Dayparting 不能只看某小时 ROI。需要先确认：

- Google Ads 花费按哪个时区。
- postback / revenue 按哪个时区。
- conversion lag 是否跨日。
- buyer 是否按工作时间审核 lead。
- 目标国家有几个时区。

如果美国全国投放用单一账号时区看小时 ROI，很可能把东西海岸和回传延迟混在一起。

## 7. 币种、汇率和 ROI

套利利润公式必须统一币种：

```text
profit_base_currency =
  revenue_offer_currency * fx_rate
  - cost_account_currency * fx_rate
  - fees
```

常见事故：

- Google Ads 成本是 USD，联盟 payout 是 EUR 或 GBP，但 ROI 直接相除。
- AdSense estimated revenue 和 Google Ads cost 时区不同，跨日错位。
- 账号币种设置错，后续无法轻易更改。
- 多国家 payout 不同，但系统只存一个 payout。
- buyer 用 local currency 扣费或拒付，运营日报没记录汇率时间。

系统中每条导入记录至少应保留 `currency`、`fx_rate_date`、`source_timezone` 和 `normalized_day`。第一版 `metrics_daily` 是简化表，运营上要在 CSV 备注或风险审计里记录币种和汇率来源。

## 8. Geo 扩量流程

不要从一个国家赚钱就直接复制到十个国家。建议流程：

1. 固定一个已验证国家/语言/页面/Offer。
2. 找相邻国家或相同语言市场。
3. 检查 Offer 条款、payout、监管、语言、支付能力和素材可用性。
4. 新建独立 campaign 或至少独立 budget / label。
5. 使用该国家的关键词、页面证据、价格和披露。
6. 小预算测试，按 paid revenue 或 finalized revenue 判断。
7. 只扩通过 bad geo、approval rate、扣量和页面质量检查的国家。

扩国家前要回答：

- 这个国家是否允许投放该 Offer？
- 用户是否能理解页面和下一步动作？
- 页面主体、价格、隐私和披露是否符合当地预期？
- 变现端是否有足够 fill / payout / buyer capacity？
- 失败时能否按国家停量而不影响其他国家？

## 9. Bad Geo 诊断

| 表现 | 可能原因 | 修复方向 |
| --- | --- | --- |
| buyer 拒绝 bad geo | location options 太宽、表单国家不匹配、代理/低质来源 | 收窄 location，修页面国家说明，停异常 source |
| GA4 国家和 Ads 国家不一致 | IP 识别差异、VPN、跨境兴趣、跳转链 | 看趋势和集中度，不按单点修数据 |
| 某国家 clicks 高 sessions 低 | 页面不可达、速度慢、WAF/CDN、语言不匹配 | 做目标国家可达性和 server log 检查 |
| RPM 高但 paid revenue 低 | 无效流量、广告主价值低、扣量 | 等 finalized / paid，不按 estimated 扩量 |
| local 页面拒登 | 主体、价格、资质、地区限制不清楚 | 补披露、资格、服务区域和证据 |

Bad geo 不是用“模拟本地用户”修复的问题。它应该通过 targeting、页面、Offer 条款、来源隔离和对账修复。

## 10. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer 国家、语言、payout 和政策备注 | `/offers` |
| 导入 country/device 维度成本和收入 | `/metrics/import` |
| 按 country/device 生成 ROI 和优化建议 | `/optimization` |
| 记录 bad geo、时区、币种和本地化风险 | `/risk-audits` |
| 沉淀 Google Ads location/language/timezone 来源 | `/sources` |

后续可扩展表：

```text
geo_market_profiles
localized_page_versions
geo_device_metrics_daily
fx_rate_snapshots
timezone_reconciliation_runs
bad_geo_incidents
```

建议字段：

```text
country
region
language
device
account_timezone
source_timezone
normalized_day
account_currency
offer_currency
fx_rate
payout
approved_revenue
paid_revenue
bad_geo_count
reject_reason
localized_page_url
location_option
presence_interest_setting
```

系统边界：

- 不用代理、指纹或 Worker 伪装地区。
- 不按 AdsBot、IP、Cookie、设备或地区做审核页/用户页不一致。
- 不用隐藏本地化页面绕过地区、认证或敏感垂类政策。
- 不伪造国家、设备、币种或 postback 数据。
- 不把 bad geo 用补点击、补访问或模拟本地行为修复。

## 11. QA 清单

- Offer 国家、语言、设备、流量来源和 payout 限制已记录。
- Campaign location targeting 和 advanced location options 已截图或记录。
- 页面语言、价格、电话、地址、隐私、披露和资格与目标国家一致。
- 成本币种、收入币种、汇率日期和账号时区已记录。
- 日报统一 `source_day` 和 `normalized_day`。
- Dayparting 前已考虑目标国家时区和 conversion lag。
- Device 分层同时看 paid revenue、reject reason 和页面速度。
- Bad geo 高时先查 targeting、页面、source 和 buyer feedback。
- 扩相邻国家前先做政策、payout、页面和来源准入。
- 本地化差异不造成审核页/用户页不一致。

## 12. 信息来源 URL

- Google Ads Help, Target ads to geographic locations: https://support.google.com/google-ads/answer/1722043
- Google Ads Help, About advanced location options: https://support.google.com/google-ads/answer/1722038
- Google Ads Help, About language targeting: https://support.google.com/google-ads/answer/1722078
- Google Ads Help, About measuring geographic performance: https://support.google.com/google-ads/answer/2453994
- Google Ads Help, About device targeting: https://support.google.com/google-ads/answer/1722028
- Google Ads Help, About bid adjustments: https://support.google.com/google-ads/answer/2732132
- Google Ads Help, Add or remove a bid adjustment: https://support.google.com/google-ads/answer/6262954
- Google Ads Help, About ad scheduling: https://support.google.com/google-ads/answer/6372656
- Google Ads Help, About your language, number format, time zone, and currency settings: https://support.google.com/google-ads/answer/9842104
- Google Ads Help, About payment settings in Google Ads: https://support.google.com/google-ads/answer/2375432
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, Time lag report: https://support.google.com/google-ads/answer/6239119
