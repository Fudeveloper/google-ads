# 隐私、Consent 与追踪合规手册

更新时间：2026-06-08

本文说明 Ads 套利链路里的隐私、用户同意、Cookie、GA4、Google Ads tags、AdSense / Ad Manager CMP、Consent Mode、Enhanced Conversions、postback 和数据最小化。本文不是法律意见；实际业务需要结合目标国家、用户地区、站点主体、广告产品和法律顾问判断。本文不提供绕过用户同意、隐藏追踪、指纹规避、Cookie 同步滥用或未经授权收集个人数据的方案。

## 1. 为什么 Consent 会影响套利

Ads 套利依赖追踪，但追踪依赖用户同意和平台政策。

```text
用户点击广告
-> 到达页面
-> CMP 展示同意选项
-> Google tag / GA4 / Ads / AdSense 根据 consent 状态工作
-> 指标进入报表
-> 团队计算 RPV、EPC、ROI、扣量和放量决策
```

如果 consent 配置错误，会出现：

- Google Ads 转化变少，智能出价学习失败。
- GA4 session/source/campaign 数据缺失。
- AdSense / GAM 在 EEA、UK、Switzerland 的个性化广告受限。
- `gclid`、UTM、click_id、postback 口径无法对齐。
- 报表显示亏损或异常，团队误判页面、来源或创意。
- 因未按政策取得同意导致账号、发布商或广告服务风险。

## 2. 数据分类

套利团队应把数据分成几类：

| 数据 | 示例 | 用途 | 风险 |
| --- | --- | --- | --- |
| 非个人运营数据 | campaign、ad group、creative、landing_version | 报表和复盘 | 低 |
| 点击标识 | `gclid`、`click_id`、`subid` | 归因和 postback | 中，需要生命周期和最小化 |
| 设备/环境数据 | user agent、IP、设备、地区 | 防错、地理报表、质量分析 | 中，不应做规避或未经说明追踪 |
| Cookie / local storage | GA、Ads、CMP、session cookie | 分析、广告、同意状态 | 高，需要同意和披露 |
| 用户提供数据 | email、phone、name、lead form | Enhanced Conversions、lead 对账 | 高，需合法基础、同意/披露和安全处理 |
| 敏感数据 | 健康、金融、身份、儿童相关 | 特定垂类 | 极高，默认避免用于广告个性化和套利扩量 |

原则：

- 能用 campaign/source/creative 解决的问题，不要收集个人数据。
- `subid` 不放邮箱、电话、姓名、身份证或完整 IP。
- postback 只回传归因所需字段，不回传不必要用户资料。
- 用户提供数据如果用于 enhanced conversions，需要按平台要求和适用法律取得必要同意并做哈希/安全处理。

## 3. Consent Mode 基础

Google Consent Mode 让 Google tags 根据用户同意状态调整行为。常见 consent types：

| Consent type | 含义 | 影响 |
| --- | --- | --- |
| `ad_storage` | 是否允许广告相关存储，例如 cookies | 影响广告点击、转化、remarketing 相关存储 |
| `analytics_storage` | 是否允许分析相关存储 | 影响 GA4 会话、用户和行为分析 |
| `ad_user_data` | 是否同意向 Google 发送广告相关用户数据 | 影响 Enhanced Conversions、tag-based conversion 等测量 |
| `ad_personalization` | 是否同意个性化广告 | 影响 remarketing、audience 和个性化广告 |

基本逻辑：

```text
默认状态先设置
用户做出选择
更新 consent 状态
Google tags 根据状态发送或限制数据
```

关键点：

- Consent 默认值应在 Google tag 之前设置，避免先发后补。
- 用户拒绝时，不能把拒绝当成同意。
- 同意状态要能随用户修改而更新。
- 不同地区可以有不同默认状态，但要有可解释的法律和政策依据。
- Consent Mode 不是“免同意追踪”的通行证；它是让标签按用户选择调整。

## 4. CMP、TCF 和发布商产品

对使用 AdSense、Ad Manager 或 AdMob 的发布商，面向 EEA、UK、Switzerland 用户投放广告时，Google 要求使用经过 Google 认证并集成 IAB TCF 的 CMP。

对套利团队的影响：

- 如果买量进入 EEA/UK/Switzerland，需要确认站点 CMP 和 Google publisher 产品要求匹配。
- 不能只放一个静态 cookie banner，当作已经完成 publisher consent。
- CMP 需要能把用户选择传给广告产品和 Google tags。
- Privacy & messaging 可以用于创建欧洲法规消息、CPRA opt-out 或其他合规消息。
- CMP 变更会影响广告填充、个性化广告、RPM 和 GA4/Ads 数据。

## 5. Google Ads 与 GA4 测量

Google Ads 和 GA4 对 consent 的依赖不同：

| 场景 | 需要注意 |
| --- | --- |
| Google Ads conversion tag | `ad_storage`、`ad_user_data`、`ad_personalization` 会影响广告测量和个性化 |
| GA4 | `analytics_storage` 影响 analytics cookies 和会话行为分析 |
| Enhanced Conversions | 使用用户提供数据时要满足 Google Ads customer data policies 和同意要求 |
| Remarketing / audiences | `ad_personalization` 被拒时不能用于个性化广告 |
| Google Ads 智能出价 | conversion 数据缺失会影响学习和放量判断 |

实操建议：

- 对关键 conversion action 建立 consent 状态报表。
- 单独观察 EEA/UK/Switzerland 与其他地区的数据差异。
- 报表里注明：收入下降是业务下降，还是 consent 后追踪可见度下降。
- 不要为了提高 conversion 数量而强制同意、暗黑模式同意或隐藏拒绝选项。

## 6. UTM、Click ID 与 Postback

Consent 不等于不能做所有运营归因。可以把字段分层：

| 字段 | 建议 |
| --- | --- |
| `utm_source/medium/campaign/content/term` | 作为非个人 campaign 归因字段保留 |
| `gclid` | 按 Google Ads 和 Consent Mode 要求处理，注意存储和传递 |
| `click_id` | 用随机 ID，生命周期短，不包含个人信息 |
| `subid` | 只放 source/campaign/creative/device/page，不放 PII |
| postback | 只回传交易/事件归因字段和收入，不回传多余个人资料 |

如果用户拒绝相关存储，不要用 fingerprint、ETag、隐藏 local storage、跨域同步或代理链路偷偷恢复用户标识。

## 7. 隐私政策和页面披露

套利站点至少应让用户知道：

- 谁运营站点。
- 使用哪些广告、分析、联盟或第三方服务。
- 是否使用 cookies/local storage。
- 数据用途：广告、分析、归因、站点安全、内容改进。
- 用户如何管理 consent 或 opt out。
- 是否涉及个性化广告。
- 联系方式和政策更新时间。
- 若收集 lead，说明谁接收、用途、保留时间和撤回方式。

隐私政策不是装饰。广告审核、发布商审核、Advertiser Verification、AdSense Policy Center 和用户投诉都可能看这些页面。

## 8. 常见事故

| 事故 | 表现 | 修复 |
| --- | --- | --- |
| Consent 默认太晚 | 页面加载先发广告/分析 tag | 在 Google tag 前设置默认 consent |
| CMP 不传 Google 字段 | GA4/Ads 报 consent 缺失 | 检查 CMP 模板、GTM consent settings |
| 拒绝后仍写 cookie | 合规和信任风险 | 检查所有第三方 tag 和自建脚本 |
| `subid` 放 PII | 联盟、日志、URL 泄露个人数据 | 改成随机 click_id 和非个人维度 |
| Enhanced Conversions 没同意/披露 | 政策和隐私风险 | 重新配置 user-provided data 和 consent |
| EEA 流量无 certified CMP | publisher 广告服务风险 | 使用 Google certified CMP / Privacy & messaging |
| 同意率变化导致 ROI 异常 | 报表收入/转化断崖 | 分地区、分 consent 状态看指标 |
| 供应商脚本私自追踪 | 不明 cookies、页面慢、政策风险 | 审计 tag，移除不可解释供应商 |

## 9. 数据保留和访问控制

建议：

- `click_id` 和 postback 原始日志设置保留周期。
- 不在 URL、日志或 subid 中保存 PII。
- 导出的 CSV、Scripts JSON 和报表不包含敏感个人信息。
- 只有需要的人能访问用户提供数据。
- 对 Enhanced Conversions / lead 数据做哈希、传输加密和最小化。
- 记录谁导入、导出、查看或修改了敏感配置。

## 10. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer 政策和页面隐私备注 | `/offers` |
| 记录追踪字段和来源 URL | `/sources`、`traffic_source_tracking.md` |
| 审计页面隐私、披露和目的地体验 | Offer 详情页、`landing_page_quality_mfa.md` |
| 导入指标时避免个人数据 | `/metrics/import` |
| 记录 Consent/CMP/隐私风险 | `/risk-audits` |
| 用任务中心定期检查页面和脚本 | `/tasks` |
| 通过审计日志保留变更记录 | `/logs` |

当前系统不存储用户个人数据，也不实现 Cookie 登录、后台接管、用户指纹、跨站追踪、隐藏追踪或无同意恢复标识。后续如果扩展 postback 或 enhanced conversions，也应先加数据最小化、字段白名单、保留周期和访问控制。

## 11. 上线检查表

| 检查项 | 通过标准 |
| --- | --- |
| CMP | 目标地区需要 CMP 时已配置并测试 |
| Consent defaults | 默认值在 Google tags 之前设置 |
| Consent update | 用户选择后 consent 状态能更新 |
| GA4 | analytics_storage 与 GA4 tag 行为一致 |
| Google Ads | ad_storage、ad_user_data、ad_personalization 配置清楚 |
| AdSense/GAM | EEA/UK/Switzerland 使用符合要求的 CMP/TCF 路径 |
| Privacy policy | 披露广告、分析、cookies、第三方和联系方式 |
| URL 参数 | 不包含 PII |
| Postback | 只传必要字段 |
| 审计 | 风险记录、来源 URL 和测试结果已保存 |

## 12. 信息来源 URL

- Google for Developers, Consent mode overview: https://developers.google.com/tag-platform/security/concepts/consent-mode
- Google for Developers, Set up consent mode on websites: https://developers.google.com/tag-platform/security/guides/consent
- Google Analytics Help, Consent type: https://support.google.com/analytics/answer/12334711
- Google Analytics Help, Tag Manager consent mode support: https://support.google.com/analytics/answer/10718549
- Google Analytics Help, Consent mode reference: https://support.google.com/analytics/answer/13802165
- Google Ads Help, Obtain required consent signals: https://support.google.com/google-ads/answer/16142449
- Google Ads Help, Customer data policies: https://support.google.com/google-ads/answer/7475709
- Google Ads Help, About enhanced conversions: https://support.google.com/google-ads/answer/9888656
- Google AdSense Help, Comply with the EU user consent policy: https://support.google.com/adsense/answer/7670013
- Google AdSense Help, Google consent management requirements for publishers: https://support.google.com/adsense/answer/13554116
- Google AdSense Help, About Privacy & messaging: https://support.google.com/adsense/answer/10924669
- Google Ad Manager Help, Google consent management requirements: https://support.google.com/admanager/answer/14139515
- Google, Help with the EU user consent policy: https://www.google.com/about/company/user-consent-policy-help/
