# 域名、站点资产与站群治理手册

更新时间：2026-06-08

本文说明 Ads 套利团队如何治理域名、站点、子域、落地页版本、过期域名、站点迁移、AdSense / AdX / GAM 发布商站点和 Google Ads Final URL。目标是把“域名资产”当作可审计的业务资产，而不是把换域名、买过期域名、站群、Parking 或站点迁移当作绕审核、绕封禁或隐藏低质流量的工具。

本文不提供批量建站、镜像站、过期域名滥用、站点声誉滥用、cloaking、规避封禁换域名、隐藏最终目的地、伪造 ads.txt 或规避 AdSense / Google Ads 审核的方案。

## 1. 为什么域名和站点资产是套利核心

Ads 套利不是只买流量和算 ROI。域名和站点决定了：

- Google Ads 是否认为目的地可访问、可信、与广告承诺一致。
- AdSense / AdX / GAM 是否能识别发布商、站点和授权卖方关系。
- 用户是否理解页面主体、商业关系、广告和跳转。
- Search / Native / Display / PMax 的落地页质量、内容质量和长期流量质量。
- 账号、域名、付款、内容、流量来源和政策问题是否会互相传染。

同一个 Offer 换到不同域名，短期 CTR、CPC、approval rate、ad serving、RPM、finalized revenue 和扣量都可能变化。套利团队必须把域名看作资产组合，而不是一次性壳。

## 2. 核心对象

| 对象 | 作用 | 套利风险 |
| --- | --- | --- |
| Root domain | 站点主体和品牌承载 | 历史违规、主题跳跃、信任不足 |
| Subdomain | 分主题、分语言或分产品承载 | 被滥用于隔离风险或隐藏真实目的 |
| Landing page URL | Google Ads Final URL / 用户实际访问页面 | 广告承诺、页面内容和最终目的不一致 |
| Tracking domain | 追踪跳转和 click id 承载 | 隐藏目的地、参数丢失、跨域归因问题 |
| Publisher site | AdSense / GAM / AdX 变现站点 | 站点审核、ads.txt、Policy Center、无效流量 |
| Parked domain | 停放域名或 Parking inventory | 用户意图弱、低质量、被广告主排除 |
| Expired domain | 买来的过期域名 | 过期域名滥用、历史主题断裂、垃圾链接 |
| Site portfolio | 多站点资产组合 | 站群、重复内容、政策风险扩散 |

## 3. 域名生命周期与历史风险

域名不是空白容器。一个域名可能带有：

- 旧主题、旧品牌、旧用户预期。
- 搜索索引、反向链接、垃圾链接和历史 spam 信号。
- 过往 AdSense / Google Ads / Search / malware / phishing 风险。
- 旧 ads.txt、seller ID、子域、跳转和缓存页面。
- 商标、品牌混淆或官方关系误解。

上线前应做域名尽调：

1. 主题历史：过去是否与当前 Offer、内容和页面主题一致。
2. 政策历史：是否曾被用于成人、博彩、金融误导、仿冒、下载、诈骗或桥页。
3. 索引历史：是否存在大量无关 URL、日文/博彩/药品 spam、被黑痕迹。
4. 链接历史：是否依赖无关高权重链接来承接新主题。
5. 变现历史：是否有旧 ads.txt、旧 seller ID、旧 GAM / AdSense 关系。
6. 用户预期：访问者是否会误以为仍在访问旧品牌或官方站。

## 4. Expired Domain Abuse / Site Reputation Abuse

Search Central spam policies 明确把 expired domain abuse 作为一种垃圾行为：购买过期域名并重新利用其历史声誉，发布对用户价值很低且与旧站点无关的内容。它的核心不是“买过期域名”本身，而是利用旧信誉承载新低质内容。

套利团队要区分：

| 场景 | 合理解释 | 高风险解释 |
| --- | --- | --- |
| 买旧域名继续经营同主题内容 | 主题延续、用户预期一致、有真实编辑价值 | 只为继承旧权重，换成无关 Offer 页 |
| 收购站点和内容团队 | 内容、作者、披露、用户服务延续 | 只保留域名和链接，替换成广告/跳转页 |
| 合作方在权威站点发布内容 | 编辑责任、披露、质量控制清楚 | 借站点声誉发布低质 affiliate / lead gen 页面 |
| 子目录商业化 | 主站有审核、披露和用户价值 | 站点声誉滥用，主站把子目录出租给第三方 |

系统判断不要只看 domain authority、流量或索引量；要看主题连续性、编辑控制、用户价值和商业披露。

## 5. Parking / Feed / Search Arbitrage 边界

Parking、Search feed 和相关搜索库存不是“域名越多越好”。Google Ads 对 parked domain site 有单独说明，广告主也可以选择排除 parked domain 类型库存。对套利团队而言：

- Parking 流量通常用户意图弱、跳出高、后端收入不稳定。
- 过期域名 typo、品牌混淆或旧导航流量容易触发商标、误导和无效流量问题。
- Search feed / AFS / CSA 必须基于真实用户查询意图，不能预填、诱导、自动搜索或把低质流量灌入搜索广告。
- 如果域名只有广告、搜索框、跳转或 affiliate 链接，容易进入低价值目的地、bridge/gateway 或 MFA 风险。

合格 Parking / Feed 测试至少要记录：

- 用户来源和意图。
- 搜索词或查询动作是否真实。
- 广告标识是否清楚。
- 页面是否有独立价值。
- 收入是否使用 finalized / paid 口径。
- 广告主、发布商和用户是否都能解释这个页面存在的理由。

## 6. 站点组合与资产隔离

多站点管理有正常用途：

- 不同垂类、语言、国家或品牌。
- 不同发布商变现账号或需求源。
- 不同编辑团队和内容主题。
- 不同实验阶段：sandbox、staging、production。

但站点组合不能被用作风险扩散工具：

- 一个站点被拒登后，把同一页面镜像到新域名继续投。
- 一个 AdSense 站点受限后，把流量导到另一个账号或壳站。
- 一个 Offer 被拒付后，换域名、换文案但不修复真实原因。
- 为规避关联，把域名、账号、付款、追踪、Worker、代理和素材拆成多个壳。

治理原则：

1. 每个域名有 owner、用途、垂类、国家、变现方式、tracking domain 和来源说明。
2. 每个域名有 policy notes、ads.txt 状态、站点审核状态和页面质量状态。
3. 高风险域名不能混入主业务 metrics；先独立 source id、预算和审计。
4. 域名迁移、换 Final URL、改 tracking domain 都要写原因、审批、回滚点。
5. 不把“减少关联”作为资产拆分的目标；目标应是业务清晰、责任清晰、用户价值清晰。

## 7. 站点迁移、换域名与封禁规避边界

正常站点迁移：

- 品牌更名、架构调整、HTTPS / www 规范化、国家站点拆分。
- 有完整 301 计划、canonical、sitemap、内部链接、Search Console /日志监控。
- 广告、页面、商家主体、隐私政策、联系信息和用户承诺保持一致。
- Google Ads 和发布商平台中同步更新 Final URL、站点审核和 ads.txt。

高风险换域名：

- 原域名因政策、无效流量、ad serving limit、账号暂停或目的地问题受限后，复制页面到新域继续投。
- 审核前展示正常内容，审核后切换到高风险 Offer 或广告密度页面。
- 用新域名隐藏旧品牌投诉、低质内容、误导承诺或异常流量来源。
- 用子域、Worker、短链或多跳跳转让 Google、用户和发布商看到不同目的地。

判断标准不是“有没有换域名”，而是换域名是否解决了用户价值和政策问题，是否保留了透明证据。

## 8. AdSense / Publisher 站点审核与 ads.txt

发布商变现场景下，域名要同时满足内容、所有权、广告服务和供应链透明度要求：

- AdSense Sites list 中的站点需要添加、连接和审核。
- 站点 ready 需要有足够内容、导航、可访问性和政策合规。
- ads.txt 应声明授权 seller，避免买方无法确认授权关系。
- Policy Center issue、ad serving limit 和 traffic quality 问题要记录 affected URLs、source、修复动作和 review 结果。
- MCM、AdX、GAM、Header Bidding 场景还要记录 seller ID、DIRECT/RESELLER、sellers.json 和 schain。

常见错误：

- 站点还没 ready 就导入付费流量。
- 用新站、镜像站或过期域名绕过旧站 issue。
- ads.txt seller ID、GAM network、MCM parent/child 关系解释不清。
- 把 estimated revenue 当成可扩量收入，不等 finalized revenue 和扣量复盘。

## 9. Google Ads Destination 与 Final URL

Google Ads destination requirements 关注页面是否可访问、是否和广告承诺一致、是否提供足够价值、是否存在桥页/低价值目的地、是否让用户难以返回或理解最终目的。

域名和 Final URL QA：

| 检查项 | 通过标准 | 风险信号 |
| --- | --- | --- |
| Final URL | 用户最终到达的真实页面 | 短链、多跳隐藏真实目的 |
| Display URL | 与实际域名和主体一致 | 暗示官方、品牌或不真实关系 |
| 页面主题 | 与关键词、广告、Offer 一致 | 关键词一套，页面另一套 |
| 可访问性 | Googlebot、用户、移动端都能访问 | 地区、设备、Bot 看到不同页面 |
| 页面价值 | 有独立内容、披露、导航和主体信息 | 只有广告、搜索框、跳转或薄内容 |
| 追踪域 | 参数透明、可测试、可回滚 | 参数丢失、跨域归因混乱 |

任何 Final URL、tracking template、root domain 或 offer domain 变更，都应进入风险审计和链接计划。

## 10. 域名尽调清单

上线前收集：

- 域名、子域、站点用途、owner、业务线。
- 当前垂类、历史垂类、是否收购或过期域名。
- Google Ads Final URL、Display URL、tracking template、Final URL suffix。
- AdSense / GAM / AdX site status、ads.txt、seller ID。
- 是否有 Policy Center issue、ad serving limit、账号拒登或暂停历史。
- 内容质量：原创性、导航、about/contact/privacy、作者/更新、商业披露。
- 页面质量：移动端、速度、表单、广告密度、CLS、可访问性。
- 流量来源：Google Search、Search Partners、Display、Native、Direct buy、PMax。
- 收入状态：estimated、finalized、paid、deduction、refund、chargeback。
- 风险结论：approved、test_only、needs_fix、blocked。

## 11. 系统落地

当前 V1 用已有模块落地：

| 需求 | 当前页面 / 文档 |
| --- | --- |
| 记录域名用途、垂类、目标 URL、追踪 URL | `/offers` |
| 采集和审计落地页 | `/offers/<id>/crawl` |
| 记录换域名、换 URL、换 tracking domain | `/links` 和 [链接计划与换链接合规手册](link_rotation_compliance.md) |
| 记录 AdSense site review / Policy Center | [AdSense 站点审核手册](adsense_site_approval_policy_center.md) 和 `/risk-audits` |
| 记录 ads.txt / sellers.json / schain | [程序化供应链透明度手册](programmatic_supply_chain_transparency.md) 和 `/sources` |
| 记录高风险换域名、cloaking 或规避封禁 | `/risk-audits` |
| 保存来源 URL | `/sources` |

后续可新增表：

```text
domain_assets
domain_history_checks
site_migration_plans
publisher_site_assets
ads_txt_asset_checks
final_url_change_reviews
domain_risk_audits
```

这些表只用于资产管理、证据留存、迁移计划和风险审计，不用于批量建站、镜像站、cloaking、规避封禁或隐藏最终目的地。

## 12. QA 清单

- 域名用途、owner、垂类、国家和变现方式清楚。
- 域名历史主题和当前主题不冲突。
- 不是为了继承过期域名声誉发布无关低质内容。
- 没有把权威站子目录出租给无审核第三方低质 affiliate 内容。
- Final URL、Display URL、tracking domain 和 offer domain 可解释。
- 用户、Google Ads 审核、Googlebot、移动端看到的业务目的一致。
- AdSense / GAM / AdX 站点审核、ads.txt、seller ID 和 Policy Center 状态记录齐全。
- 换域名不是为了绕过拒登、封禁、ad serving limit、Policy Center 或无效流量问题。
- 站点组合按真实业务拆分，不按规避关联拆分。
- 收入使用 finalized / paid 口径做扩量决策。

## 13. 信息来源 URL

- Google Search Central, Spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Google Search Central, Site move with URL changes: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Google Search Central, Creating helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Ads Help, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Help, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads Help, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads Help, Parked domain site: https://support.google.com/google-ads/answer/50002
- Google AdSense Help, Add a new site to your sites list: https://support.google.com/adsense/answer/12169212
- Google AdSense Help, Connect your site to AdSense: https://support.google.com/adsense/answer/7584263
- Google AdSense Help, Make sure your site's pages are ready for AdSense: https://support.google.com/adsense/answer/7299563
- Google AdSense Help, Create an ads.txt file: https://support.google.com/adsense/answer/7532444
- Google AdSense Help, Program policies: https://support.google.com/adsense/answer/48182
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google Publisher Policies: https://support.google.com/publisherpolicies/answer/10437486
