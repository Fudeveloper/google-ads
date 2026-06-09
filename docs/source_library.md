# Ads 套利研究来源库

更新时间：2026-06-09

本文记录本项目用于拆解 ADXKit、Ads 套利流程和高风险能力边界的主要来源。来源分为：

- `primary`：平台官方政策、官方开发文档、标准/技术参考。
- `public_claim`：目标产品公开页面或公开营销文案，只能用于“该产品公开宣称什么”，不能证明其内部实现。
- `industry_reference`：行业术语或研究资料，用于补充概念背景。

## 1. ADXKit 公开产品来源

| 来源 | URL | 用途 |
| --- | --- | --- |
| ADXKit homepage | https://adxkit.com/ | 拆解其公开宣称的一站式 Google Ads 管理、Scripts 同步、补点击、换链接、代理、防关联、AI 创意生成等功能叙事 |

说明：ADXKit 首页属于 `public_claim`，只能作为“公开页面展示了哪些功能和话术”的证据。本项目不会把补点击、流量模拟、规避关联、Cookie 接管、cloaking 或绕封禁功能做成可执行能力。

## 2. 套利业务模式来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑 arbitrage、桥页、网关页、广告网络滥用和低价值目的地风险 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑目的地体验、原创内容、页面可达和广告承诺一致性 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑隐藏真实目的地、向 Google 和用户展示不同内容、多账号规避等红线 |
| AdSense, Online advertising to get new users | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时发布商需要对流量质量负责 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑无效点击、展示和人为抬高收入/成本的风险 |
| AdSense, Metrics glossary | https://support.google.com/adsense/answer/2735899 | 支撑 RPM、CTR、coverage、Active View 等展示广告套利指标 |
| Google Publisher Policies | https://support.google.com/publisherpolicies/answer/10437486 | 支撑发布商库存质量和内容/广告行为边界 |
| IAB UK, Made for Advertising guide | https://www.iabuk.com/news-article/guide-identifying-made-advertising-websites | 支撑 MFA/内容套利高风险库存识别 |
| Jounce Media terminology | https://jouncemedia.com/resources/terminology | 支撑 MFA、arbitrage 等行业术语背景 |

## 3. Google Ads 政策来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 解释规避审核、限制、政策执行、多账号规避和向 Google/用户展示不同内容的风险 |
| Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 解释广告网络滥用、桥页、网关页、arbitrage、cloaking 等风险语境 |
| Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 解释最终 URL、目的地体验、页面可达性和广告承诺一致性要求 |
| Secure your Google Ads account | https://support.google.com/google-ads/answer/2375456 | 支撑 Cookie、账号安全、2-Step Verification、安全挑战、访问审计相关边界 |
| Confirm it is you | https://support.google.com/google-ads/answer/12865189 | 支撑 Google Ads 在敏感或异常场景下要求确认身份的安全挑战逻辑 |
| About access levels in your Google Ads account | https://support.google.com/google-ads/answer/9978556 | 支撑“用权限模型协作，而不是共享登录态或绕过验证” |
| Google Account, Turn on 2-Step Verification | https://support.google.com/accounts/answer/185839 | 支撑第二因素是账号保护机制，不应被自动化或供应商接管 |

## 4. Google 官方自动化来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads API start guide | https://developers.google.com/google-ads/api/docs/start | 官方 API 是长期产品化集成方向 |
| Google Ads API OAuth overview | https://developers.google.com/google-ads/api/docs/oauth/overview | API 调用应通过 OAuth 授权，不需要处理用户登录凭据 |
| Google Ads Scripts start guide | https://developers.google.com/google-ads/scripts/docs/start | Scripts 可作为账号内授权脚本方向，适合有限批量处理和报表 |
| Google Ads Scripts authorization | https://developers.google.com/google-ads/scripts/docs/authorization | Scripts 需要用户授权，适合作为可审计替代方案 |
| Google Ads Scripts, Bulk Upload | https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload | 支撑用 Scripts 创建 bulk upload preview/apply 流程，替代 Cookie 后台批量操作 |
| Google Ads Scripts, Limits | https://developers.google.com/google-ads/scripts/docs/limits | 支撑脚本运行时长、账号范围和配额边界，不适合无限制无人值守 |
| Google Ads Scripts, AdsApp reference | https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp | 支撑 AdsApp 作为授权脚本访问 Google Ads 对象的官方入口 |
| Google Ads Scripts, BulkUpload reference | https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp_bulkupload | 支撑 BulkUpload preview 和 apply 的脚本对象边界 |
| Google Ads Editor Help | https://support.google.com/google-ads/editor | Google Ads Editor 和批量导入导出是人工审核型批量管理方向 |

## 5. Cookie、会话和认证来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| MDN, Using HTTP cookies | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies | Cookie 常用于会话管理，登录 Cookie 是敏感会话凭据 |
| MDN, Set-Cookie header | https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie | `Secure`、`HttpOnly`、`SameSite` 等属性说明 Cookie 安全边界 |
| OWASP Session Management Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | 会话 ID 应被视为敏感凭据，需要生命周期、传输和存储保护 |
| OWASP Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | 支撑认证失败、安全响应、凭据保护和任务升级原则 |
| OWASP Multifactor Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | 支撑 MFA 因子、恢复流程和不可弱化第二因素的治理 |

## 6. 无效流量和发布商质量来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Definition of invalid traffic | https://support.google.com/adsense/answer/16737 | 无效流量包括可能人为抬高广告主成本或发布商收入的点击和展示 |
| AdSense Program policies | https://support.google.com/adsense/answer/48182 | 禁止鼓励点击、自动点击工具、付费点击、自动浏览等行为 |
| Use of online advertising to get new users to the site | https://support.google.com/adsense/answer/1348727 | 购买流量需要对流量质量负责，避免违反无效流量政策 |
| Google Publisher Policies | https://support.google.com/publisherpolicies/answer/10437486 | 支撑内容质量、用户体验和发布商合规边界 |
| How Google prevents invalid traffic | https://support.google.com/adsense/answer/1348752 | Google 使用自动系统和人工审核过滤无效点击、展示和相关活动 |

## 7. 指纹、代理和边缘转发来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| EFF Cover Your Tracks | https://coveryourtracks.eff.org/learn | 浏览器指纹由多个环境信号组合而成，可被用于识别或跟踪 |
| W3C TAG, Unsanctioned Web Tracking | https://www.w3.org/2001/tag/doc/unsanctioned-tracking/ | 指纹和非授权追踪有隐私和治理风险 |
| Cloudflare Workers documentation | https://developers.cloudflare.com/workers/ | Workers 是边缘 serverless 平台，可用于正常 API/任务/缓存，也可能被滥用于隐藏链路 |

## 8. Cloaking 和页面不一致来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Search spam policies | https://developers.google.com/search/docs/essentials/spam-policies | Cloaking 是向用户和搜索引擎展示不同内容以操纵或误导的做法 |
| Google Ads Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | Ads 政策关注向 Google 和用户展示不同内容、隐藏真实目的地、规避审核 |
| Google Ads Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑最终 URL、页面可达性、广告与目的地一致性的审计 |

## 9. 封禁规避和账号治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 多账号滥用、封禁后创建账号继续违规属于规避政策执行 |
| Fix a suspended Google Ads account | https://support.google.com/google-ads/answer/2375414 | 合规路径是理解暂停原因、修复问题、提交申诉 |
| Google Ads account access levels | https://support.google.com/google-ads/answer/9978556 | 正常账号协作应使用访问级别、角色和审计，而不是共享账号或换号 |

## 10. Search Arbitrage、Feed 与 Parking 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google AdSense, Search ads policies | https://support.google.com/adsense/answer/7003954 | 支撑 Search ads 必须基于用户搜索意图、每个用户动作一个广告请求、清楚广告标识和结果页要求 |
| Google AdSense, About Search ads | https://support.google.com/adsense/answer/9000515 | 支撑 AdSense for Search 是在站点搜索结果页用用户查询展示相关广告的产品语境 |
| Google for Developers, Custom Search Ads Web Implementation | https://developers.google.com/custom-search-ads/web/ | 支撑 CSA web implementation 需要 active permission，不能作为任意页面广告组件 |
| Google Ads, Search partners definition | https://support.google.com/google-ads/answer/2616017 | 支撑 Search Partner Network 可包括 Google 搜索合作伙伴和相关搜索库存 |
| Google Ads, Parked domain site | https://support.google.com/google-ads/answer/50002 | 支撑 parked domain 的定义、新旧账号默认 opt out 时间和广告主 opt in/opt out 语境 |
| Google Ads, Exclude specific webpages and videos | https://support.google.com/google-ads/answer/2454012 | 支撑广告主可排除 parked domains、网页、YouTube 内容等展示位置 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑只有广告链接、无独特价值的 parked domain 和低质量目的地风险 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑 arbitrage、bridge/gateway、ad destination low value 和广告网络滥用风险 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑隐藏真实目的地、cloaking、审核页/用户页不一致等风险 |
| AdSense Program policies | https://support.google.com/adsense/answer/48182 | 支撑禁止诱导点击、自动点击、自动浏览、paid-to-click 等无效行为 |
| Google Publisher Policies | https://support.google.com/publisherpolicies/answer/10437486 | 支撑发布商内容、广告体验和流量质量边界 |
| Jounce Media terminology | https://jouncemedia.com/resources/terminology | 支撑行业对 arbitrage、MFA 等术语的背景理解 |

## 11. 流量源、追踪和归因来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About tracking in Google Ads | https://support.google.com/google-ads/answer/6076199 | 支撑 Final URL、tracking template、Final URL suffix、HTTPS 跳转和 Test 验证 |
| Google Ads, About ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 支撑用 `{keyword}`、`{matchtype}`、`{device}` 等参数记录点击上下文 |
| Google Ads, Set up tracking with ValueTrack parameters | https://support.google.com/google-ads/answer/6305348 | 支撑追踪来源、设备、地理位置和广告点击上下文 |
| Google Ads, About auto-tagging | https://support.google.com/google-ads/answer/3095550 | 支撑 Google Ads 与 Analytics 自动标记、`gclid` 和报表归因 |
| GA4, Traffic-source dimensions, manual tagging, and auto-tagging | https://support.google.com/analytics/answer/11242870 | 支撑 UTM、manual tagging、auto-tagging 和 traffic-source 维度 |
| GA4, Campaigns and traffic sources | https://support.google.com/analytics/answer/11242841 | 支撑 source/medium/campaign 的采集、处理和报表逻辑 |
| AdSense, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时需要监控来源、暂停可疑来源并承担流量质量责任 |
| AdSense, Traffic provider checklist | https://support.google.com/adsense/answer/3332805 | 支撑供应商尽调、样例 URL、placement、价格异常和小预算测试 |
| AdSense, Set up a traffic segmentation plan | https://support.google.com/adsense/answer/2583698 | 支撑按来源分段监控、识别异常和预防无效流量 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑联盟/CPA 场景里 click_id、postback、payout 和 conversion 归因原理 |

## 12. Click -> Session -> Revenue 对账来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About tracking in Google Ads | https://support.google.com/google-ads/answer/6076199 | 支撑 Final URL、tracking template、Final URL suffix 和 Test 验证是 click 到站的第一层 QA |
| Google Ads, About ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 支撑用点击上下文参数把 campaign、keyword、device、network 等维度带入对账 |
| Google Ads, About auto-tagging | https://support.google.com/google-ads/answer/3095550 | 支撑 `gclid` 自动标记、Google Ads 与 Analytics 归因和 click ID 保留 |
| Google Ads, About parallel tracking | https://support.google.com/google-ads/answer/7544674 | 支撑 parallel tracking 下 tracking request 和 landing request 可能不再串行 |
| Google Ads, Managing invalid traffic | https://support.google.com/google-ads/answer/11182074 | 支撑 click 异常、invalid clicks 和平台过滤不能用补点击修复 |
| GA4, Traffic-source dimensions, manual tagging, and auto-tagging | https://support.google.com/analytics/answer/11242870 | 支撑 GA4 source/medium/campaign、manual tagging 和 auto-tagging 口径 |
| GA4, Data freshness | https://support.google.com/analytics/answer/11198161 | 支撑日报中标注 GA4 数据刷新延迟，避免当天误判 |
| GA4, Traffic-source dimensions | https://support.google.com/analytics/answer/15567068 | 支撑 session、user、event 等 acquisition 维度口径差异 |
| Google tag, Consent mode overview | https://developers.google.com/tag-platform/security/concepts/consent-mode | 支撑 consent 状态会影响广告和分析存储及测量可见性 |
| Google tag, Set up consent mode on websites | https://developers.google.com/tag-platform/security/guides/consent | 支撑 default consent、update consent 和 tag 执行顺序 |
| Google Ads API, Upload click conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-clicks | 支撑用真实 click ID 上传线下转化，不伪造 conversion |
| Google Ads API, Conversion upload diagnostics | https://developers.google.com/google-ads/api/docs/conversions/upload-summaries | 支撑排查 conversion upload 匹配率、错误和处理状态 |
| AdSense, Metrics glossary | https://support.google.com/adsense/answer/2735899 | 支撑 ad request、impression、CTR、RPM、Active View 和 revenue 口径 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑人为抬高广告主成本或发布商收入的点击/展示属于无效流量 |

## 13. 追踪模板、URL 参数与跳转链 QA 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About tracking in Google Ads | https://support.google.com/google-ads/answer/6076199 | 支撑 Final URL、tracking template、Final URL suffix、URL options 和 Test 验证 |
| Google Ads, About ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 支撑 `{lpurl}`、`{keyword}`、`{matchtype}`、`{device}` 等点击上下文参数 |
| Google Ads, Set up tracking with ValueTrack parameters | https://support.google.com/google-ads/answer/6305348 | 支撑用 ValueTrack 设置追踪模板和最终 URL 参数 |
| Google Ads, About parallel tracking | https://support.google.com/google-ads/answer/7544674 | 支撑 parallel tracking 下用户先到 Final URL、追踪请求后台加载的链路理解 |
| Google Ads, About auto-tagging | https://support.google.com/google-ads/answer/3095550 | 支撑 `gclid` 自动标记和 Google Ads / Analytics 归因 |
| Google Ads, Final URL suffix | https://support.google.com/google-ads/answer/9054021 | 支撑 Final URL suffix 参数追加和 QA |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑最终目的地、URL 一致性、页面可达和透明跳转 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑禁止隐藏真实目的地、审核页/用户页不一致和规避系统 |
| GA4, Traffic-source dimensions, manual tagging, and auto-tagging | https://support.google.com/analytics/answer/11242870 | 支撑 UTM、manual tagging、auto-tagging 与流量来源维度 |
| Google Ads API, Campaign tracking URL template field | https://developers.google.com/google-ads/api/fields/v23/campaign#campaign.tracking_url_template | 支撑未来通过官方 API 读取/管理 tracking template，而不是 Cookie 后台操作 |

## 14. 转化追踪、价值回传与 Attribution 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Different ways to track conversions | https://support.google.com/google-ads/answer/1722054 | 支撑网站、电话、应用、导入等不同转化追踪方式 |
| Google Ads, About conversion measurement | https://support.google.com/google-ads/answer/1722022 | 支撑 conversion action、转化测量和广告效果反馈基础 |
| Google Ads, Primary and secondary conversion actions | https://support.google.com/google-ads/answer/11461796 | 支撑 primary/secondary conversion actions、出价目标和观察口径区分 |
| Google Ads, About enhanced conversions | https://support.google.com/google-ads/answer/9888656 | 支撑 Enhanced Conversions 使用用户提供数据提升测量准确性及其边界 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户提供数据、customer data、consent、披露和数据处理要求 |
| Google Ads API, Manage offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑用 click ID 或增强数据导入线下转化、qualified/paid lead 和后端价值 |
| Google Ads, Offline conversion import discrepancies | https://support.google.com/google-ads/answer/13321563 | 支撑排查 offline conversion import 的错误、未匹配和归因差异 |
| Google Ads, Attribution models | https://support.google.com/google-ads/answer/6259715 | 支撑转化 credit 分配、模型口径和渠道 ROI 差异解释 |
| Google Ads, Data-driven attribution | https://support.google.com/google-ads/answer/6394265 | 支撑数据驱动归因对转化 credit 的分配方式 |
| Google Ads, Conversion windows | https://support.google.com/google-ads/answer/3123169 | 支撑点击后多长时间内计入转化的窗口设置 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑转化延迟、回传延迟和短期 ROI 判断 |
| Google Ads, Conversion tracking status troubleshooting | https://support.google.com/google-ads/troubleshooter/13455130 | 支撑 tag、conversion action、诊断和状态排错 |
| Google tag, Consent mode overview | https://developers.google.com/tag-platform/security/concepts/consent-mode | 支撑 Consent Mode 对广告测量、存储和用户数据信号的影响 |

## 14.3 单位经济模型、Break-even 与安全边际来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Determine a bid strategy based on your goals | https://support.google.com/google-ads/answer/2472725 | 支撑按目标选择出价策略，单位经济要先决定可承受 CPC/CPA/ROAS |
| Google Ads, About Smart Bidding | https://support.google.com/google-ads/answer/7065882 | 支撑自动出价依赖转化和价值信号，不能替代 break-even 模型 |
| Google Ads, Set a target ROAS bid strategy | https://support.google.com/google-ads/answer/6268637 | 支撑 tROAS 与 conversion value 相关，目标应由 net/paid value 倒推 |
| Google Ads, About conversion values | https://support.google.com/google-ads/answer/3419241 | 支撑 conversion value 是价值优化输入，不能用 gross value 误导模型 |
| Google Ads, About conversion measurement | https://support.google.com/google-ads/answer/1722022 | 支撑 conversion measurement 是 ROI、CPA、ROAS 和出价反馈的基础 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 break-even 判断要等待 conversion/revenue lag |
| Google Ads, Budget report | https://support.google.com/google-ads/answer/10702522 | 支撑测试预算、硬止损和预算 pacing 复盘 |
| Google Ads, Performance Planner | https://support.google.com/google-ads/answer/9230124 | 支撑预算和 forecast 只能作为 scenario 输入，不能替代可收款 ROI |
| Google Ads, Measure your results | https://support.google.com/google-ads/answer/6172626 | 支撑 impressions、clicks、cost、conversions 等基础指标口径 |
| Google Ads API, Metrics fields | https://developers.google.com/google-ads/api/fields/v23/metrics | 支撑 future reporting import 的 metrics 字段口径和命名 |
| Google Ads API, Bidding strategy types | https://developers.google.com/google-ads/api/docs/campaigns/bidding/strategy-types | 支撑出价策略类型和目标字段的官方 API 口径 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把 approved/paid value 导回模型，而不是用 submitted lead |
| Google AdSense, Metrics glossary | https://support.google.com/adsense/answer/2735899 | 支撑 RPM、CTR、coverage、Active View 等发布商变现指标 |
| Google AdSense Management API, Metrics and Dimensions | https://developers.google.com/adsense/management/metrics-dimensions | 支撑未来按官方字段导入收入端指标 |
| Google AdSense, Payment timelines | https://support.google.com/adsense/answer/7164703 | 支撑 estimated/finalized/paid revenue 对安全边际和现金流的影响 |
| Google AdSense, Deductions from earnings FAQs | https://support.google.com/adsense/answer/2808531 | 支撑 deduction、invalid traffic 和扣减进入 payable RPV 模型 |

## 14.4 归因、增量性与流量蚕食治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Attribution models | https://support.google.com/google-ads/answer/6259715 | 支撑 attribution model 只是分配 credit，不直接证明增量利润 |
| Google Ads, Data-driven attribution | https://support.google.com/google-ads/answer/6394265 | 支撑 data-driven attribution 是模型输出，仍需 holdout/lift 判断增量 |
| Google Analytics, Get started with attribution | https://support.google.com/analytics/answer/10596866 | 支撑 GA4 attribution reports 和 model scope 与 Google Ads 口径不同 |
| Google Ads, About lift studies | https://support.google.com/google-ads/answer/16104408 | 支撑用 lift studies 衡量广告带来的增量效果 |
| Google Ads, Set up a custom experiment | https://support.google.com/google-ads/answer/6261395 | 支撑用 campaign experiment 做 treatment/control 比较 |
| Google Ads, Monitor your experiments | https://support.google.com/google-ads/answer/6318747 | 支撑实验监控、指标比较和结果判断需要观察窗口 |
| Google Ads API, Experiments | https://developers.google.com/google-ads/api/docs/experiments/experiments | 支撑未来用官方 API 保存 experiment plan 和结果，而不是 Cookie 后台 |
| Google Ads, About Brand Lift | https://support.google.com/google-ads/answer/9049825 | 支撑品牌类 lift 衡量与普通 attributed conversion 不同 |
| Google Ads, Search terms insights | https://support.google.com/google-ads/answer/11386930 | 支撑 PMax / broad 场景下用主题聚合诊断 query 扩展和蚕食 |
| Google Ads, Use broad match with Smart Bidding | https://support.google.com/google-ads/answer/12159290 | 支撑 broad match 扩展需要结合 Smart Bidding、目标和 query 复盘 |
| Google Ads, About Performance Max campaigns | https://support.google.com/google-ads/answer/10724817 | 支撑 PMax 自动跨库存优化，需要检查是否抢品牌、自然或现有需求 |
| Google Ads, Change history | https://support.google.com/google-ads/answer/19888 | 支撑实验期和归因窗口内的预算、URL、goal、strategy 变更复盘 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑增量判断必须等待转化和收入回填 |
| Google Ads, Customer Match policy | https://support.google.com/adspolicy/answer/6299717 | 支撑再营销/Customer Match holdout 和受众使用边界 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑受众和敏感类别广告的增量测试合规边界 |

## 15. 落地页质量、广告密度和 MFA 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑目的地可达、URL 一致、destination experience、原创内容和桥页风险 |
| Google Ads, Destination experience | https://support.google.com/adspolicy/answer/16427615 | 支撑落地页应 functional、useful、easy to navigate，并关联 Better Ads Standards |
| Google Publisher Policies overview | https://support.google.com/publisherpolicies/answer/10400453 | 支撑发布商变现需要遵守 Google Publisher Policies 和 Restrictions |
| AdSense, Ad placement policies | https://support.google.com/adsense/answer/1346295 | 支撑广告不能伪装成内容、不能激励点击、不能改变广告点击结果 |
| AdSense, Best practices for ad placement | https://support.google.com/adsense/answer/1282097 | 支撑内容应易找、广告应可识别、广告数量不能压过内容体验 |
| Coalition for Better Ads, Better Ads Standards | https://www.betterads.org/standards/ | 支撑弹窗、自动播放有声视频、插屏、广告密度、sticky 等低体验广告类型 |
| Coalition for Better Ads, Desktop ad density higher than 50% | https://www.betterads.org/desktop-ad-density-over-50-percent | 支撑桌面主内容广告密度计算方式和 50% 风险阈值 |
| IAB UK, Made for Advertising guide | https://www.iabuk.com/news-article/guide-identifying-made-advertising-websites | 支撑 MFA 的广告密度、内容质量、流量模式和用户旅程特征 |
| Jounce Media terminology | https://jouncemedia.com/resources/terminology | 支撑 MFA 被视为“付费流量 + 过高广告负载”的广告套利库存 |

## 16. 落地页素材抽取、Offer Intelligence 与创意 Brief 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑最终 URL、目的地可达、原创内容、桥页风险和广告承诺一致性 |
| Google Ads, Destination experience | https://support.google.com/adspolicy/answer/16427615 | 支撑落地页要 functional、useful、easy to navigate，不能用低体验页面承接广告 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑创意和页面不得虚假陈述主体、价格、资格、官方关系或服务结果 |
| Google Ads, Text ad requirements | https://support.google.com/adspolicy/answer/6021630 | 支撑文字广告必须满足 Google Ads 标准政策和常见拒登要求 |
| Google Ads, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑广告文字、标点、格式、display URL 和误导性表达检查 |
| Google Search Central, Helpful content | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | 支撑页面内容应以用户为先，有原创价值、可信来源和清楚目的 |
| Google Search Central, Spam policies | https://developers.google.com/search/docs/essentials/spam-policies | 支撑识别 cloaking、薄 affiliate 页面、自动生成低质内容和滥用规模化内容 |
| Google Search Quality Rater Guidelines | https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf | 支撑 E-E-A-T、页面目的、可信度和 YMYL 内容风险判断 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑推荐、评测、用户评价、affiliate 关系和背书披露要求 |
| FTC, Endorsements, influencers, and reviews | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | 支撑评价、达人推荐、商业关系披露和消费者误导风险 |

## 17. 回款、结算和现金流来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About payment settings | https://support.google.com/google-ads/answer/2375432 | 支撑自动付款、手动付款、月结发票和广告费先发生的现金流模型 |
| Google Ads, Create an account budget | https://support.google.com/google-ads/answer/2375395 | 支撑通过 account budgets 控制账号级支出 |
| Google Ads API, Account Budget | https://developers.google.com/google-ads/api/docs/billing/account-budgets | 支撑未来可审计地读取或管理账号预算，不需要 Cookie 操作后台 |
| AdSense, Payment timelines | https://support.google.com/adsense/answer/7164703 | 支撑 estimated earnings、finalized earnings、付款时间和可能 hold/deduct 的周期 |
| AdSense, Payments FAQs | https://support.google.com/adsense/answer/7164701 | 支撑月度付款、付款阈值和到账延迟 |
| AdSense, Payment thresholds | https://support.google.com/adsense/answer/1709871 | 支撑付款阈值、验证阈值、付款方式阈值和取消阈值 |
| AdSense, Deductions from earnings FAQs | https://support.google.com/adsense/answer/2808531 | 支撑 invalid clicks、政策不合规、广告主违约等扣减原因 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑把无效流量扣减纳入现金流安全垫 |

## 17.1 订阅、试用、退款、Chargeback 与 LTV 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Negative Option Rule | https://www.ftc.gov/legal-library/browse/rules/negative-option-rule | 支撑订阅、自动续费和 negative option 场景需要持续关注 FTC 当前规则状态 |
| FTC, Restore Online Shoppers' Confidence Act | https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act | 支撑在线 negative option、同意、披露和取消相关治理背景 |
| FTC, Enforcement Policy Statement Regarding Negative Option Marketing | https://www.ftc.gov/legal-library/browse/federal-register-notices/enforcement-policy-statement-regarding-negative-option-marketing | 支撑试用、自动续费、取消和收费披露风险判断 |
| FTC, .com Disclosures | https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising | 支撑价格、续费、退款、限制和重要条款的清晰披露 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑互联网广告披露、真实性和消费者保护基础 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑隐藏价格、收费、退款、资格或重要限制属于误导风险 |
| Google Ads Policy, Unacceptable business practices | https://support.google.com/adspolicy/answer/15938071 | 支撑严重误导、隐藏身份和诱导用户付款/提交信息的禁投边界 |
| Google Ads Policy, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑广告文本、促销、标点和格式不能误导订阅/试用承诺 |
| Google Ads, About conversion values | https://support.google.com/google-ads/answer/3419241 | 支撑 LTV 和续费价值回传必须使用真实价值口径 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 trial、renewal、refund 和 chargeback 有长延迟窗口 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把真实 renewal、refund-adjusted value 或 paid 状态导回优化系统 |
| Google Ads, Change history | https://support.google.com/google-ads/answer/19888 | 支撑订阅 Offer 的页面、goal、value、budget 变更进入事故复盘 |

## 18. 发布商收入对账、Finalized Revenue 与扣量复盘来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google AdSense Help, Metrics glossary | https://support.google.com/adsense/answer/2735899 | 支撑 page RPM、impression RPM、coverage、CTR、Active View 等收入端指标口径 |
| Google AdSense Help, Payment timelines | https://support.google.com/adsense/answer/7164703 | 支撑 estimated earnings、finalized earnings、付款时间和 hold/deduct 周期 |
| Google AdSense Help, Payments FAQs | https://support.google.com/adsense/answer/7164701 | 支撑月度付款流程、付款状态、到账和付款问题排查 |
| Google AdSense Help, Payment thresholds | https://support.google.com/adsense/answer/1709871 | 支撑付款阈值、验证阈值和取消阈值对现金流的影响 |
| Google AdSense Help, Deductions from earnings FAQs | https://support.google.com/adsense/answer/2808531 | 支撑无效点击、政策、广告主违约等原因造成的 finalized 下调和扣量 |
| Google AdSense Help, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑把可能人为抬高广告主成本或发布商收入的点击/展示识别为无效流量 |
| Google AdSense Help, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑发布商购买流量时需要监控来源质量并对流量负责 |
| Google AdSense Help, Set up a traffic segmentation plan | https://support.google.com/adsense/answer/2583698 | 支撑按来源分段监控、识别异常和隔离风险来源 |
| Google AdSense Management API, Metrics and Dimensions | https://developers.google.com/adsense/management/metrics-dimensions | 支撑未来收入端指标导入、字段口径和自动化报表扩展 |
| Google Ad Manager API, Reporting | https://developers.google.com/ad-manager/api/reporting | 支撑未来从 GAM 拉取 historical report，而不是 Cookie 后台操作 |
| Google Ad Manager API, ReportService | https://developers.google.com/ad-manager/api/reference/latest/ReportService | 支撑 report job、维度、指标和下载报表的官方 API 方向 |
| Google Publisher Policies, Google Ad Manager Partner Guidelines | https://support.google.com/publisherpolicies/answer/9059370 | 支撑 GAM / AdX 合作伙伴在广告行为、流量质量和政策方面的要求 |
| Google Ad Traffic Quality, How Google prevents invalid traffic | https://www.google.com/ads/adtrafficquality/how-we-prevent-it/ | 支撑 Google 广告流量质量系统对无效流量的检测和预防背景 |

## 19. 创意生成、测试和优化来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads API, Responsive Search Ads | https://developers.google.com/google-ads/api/docs/responsive-search-ads/overview | 支撑 RSA 由多个 headlines/descriptions 自动组合、可 pin、可收集组合表现 |
| Google Ads, About responsive search ads | https://support.google.com/google-ads/answer/7684791 | 支撑 RSA 字段、标题/描述数量、display path 和组合展示逻辑 |
| Google Ads, About Ad strength for responsive search ads | https://support.google.com/google-ads/answer/9921843 | 支撑 Ad Strength 是创意诊断工具，用于提示资产数量、相关性和重复问题 |
| Google Ads, Keyword insertion | https://support.google.com/google-ads/answer/6371157 | 支撑动态关键词插入的相关性收益和语法/政策风险 |
| Google Ads, Text customization in Search campaigns | https://support.google.com/google-ads/answer/11259373 | 支撑自动文本资产/AI Max 需要透明查看、审核和控制 |
| Google Ads, Experiments page | https://support.google.com/google-ads/answer/10682377 | 支撑用 experiments 分流测试 campaign changes 和广告变体 |
| Google Ads Scripts, Campaign Drafts and Experiments | https://developers.google.com/google-ads/scripts/docs/campaigns/drafts-experiments | 支撑用 Scripts 管理草稿和实验的安全自动化方向 |
| Google Ads Policies, Text ad requirements | https://support.google.com/adspolicy/answer/6021630 | 支撑文字广告需要满足标准政策、编辑和常见拒登规则 |
| Google Ads Policies, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑禁止误导声明、虚假身份、隐藏信息和不实承诺 |

## 20. 链接计划和换链接来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目的地可达、Display URL、桥页、原创内容和 URL 一致性检查 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑禁止通过不同页面、隐藏目的地、cloaking 或多账号规避审核和政策执行 |
| Google Ads, About tracking in Google Ads | https://support.google.com/google-ads/answer/6076199 | 支撑 tracking template、Final URL suffix、URL options 和测试流程 |
| Google Ads, ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 支撑用参数记录点击上下文，而不是用追踪链隐藏目的地 |
| Google Ads Editor Help | https://support.google.com/google-ads/editor | 支撑批量链接修改应走可审核导入导出或人工确认路径 |
| Google Ads Scripts start guide | https://developers.google.com/google-ads/scripts/docs/start | 支撑安全自动化用授权脚本，不用 Cookie 后台接管 |
| Google Search spam policies | https://developers.google.com/search/docs/essentials/spam-policies | 支撑 cloaking 是向用户和搜索引擎展示不同内容以操纵或误导的做法 |

## 21. 投放结构和安全自动化来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads API, Campaigns overview | https://developers.google.com/google-ads/api/docs/campaigns/overview | 支撑 campaign、ad group、ad、criterion 等投放结构对象 |
| Google Ads, Create a search campaign | https://support.google.com/google-ads/answer/9510373 | 支撑 Search campaign 创建、关键词、广告和预算基础流程 |
| Google Ads, About negative keywords | https://support.google.com/google-ads/answer/2453972 | 支撑用否定词排除不相关搜索并控制花费 |
| Google Ads, About the search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑用真实查询清理关键词、发现浪费和改善意图匹配 |
| Google Ads, Budgets overview | https://support.google.com/google-ads/answer/10486536 | 支撑平均日预算、预算管理和花费波动理解 |
| Google Ads, About automated bidding | https://support.google.com/google-ads/answer/2979071 | 支撑智能出价需要和真实转化、收入、扣量口径一起判断 |
| Google Ads API, Bidding strategy types | https://developers.google.com/google-ads/api/docs/campaigns/bidding/strategy-types | 支撑 campaign 出价策略类型和 API 方向集成 |
| Google Ads, Optimization score | https://support.google.com/google-ads/answer/9061547 | 支撑 optimization score 是诊断输入，不是套利净利润指标 |
| Google Ads, Types of recommendations | https://support.google.com/google-ads/answer/3416396 | 支撑 recommendations 需要人审，不能盲目自动应用 |
| Google Ads Scripts, Bulk Upload | https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload | 支撑 Scripts 批量上传作为可授权、可审计的自动化路径 |
| Google Ads Scripts, Authorization | https://developers.google.com/google-ads/scripts/docs/authorization | 支撑脚本授权，不处理登录 Cookie 或安全挑战 |

## 22. Google Ads 竞价、Quality Score 和出价来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, How the Google Ads auction works | https://support.google.com/google-ads/answer/6366577 | 支撑 Ad Rank、竞价上下文、质量、出价、资产影响和实际 CPC 的解释 |
| Google Ads, About Quality Score for Search campaigns | https://support.google.com/google-ads/answer/6167118 | 支撑 Quality Score 是诊断指标，包含 expected CTR、ad relevance 和 landing page experience |
| Google Ads, Determine a bid strategy based on your goals | https://support.google.com/google-ads/answer/2472725 | 支撑按目标选择 Manual CPC、Maximize Clicks、Maximize Conversions、Target CPA/ROAS 等策略 |
| Google Ads, About automated bidding | https://support.google.com/google-ads/answer/2979071 | 支撑自动出价和 auction-time bidding 的基本逻辑 |
| Google Ads, About Smart Bidding | https://support.google.com/google-ads/answer/7065882 | 支撑 Smart Bidding 使用转化和转化价值优化，需要高质量转化信号 |
| Google Ads, Google Ads automated bidding | https://support.google.com/google-ads/answer/10964872 | 支撑自动出价可提升效率但需要正确目标和数据输入 |
| Google Ads, About overdelivery and average daily budget | https://support.google.com/google-ads/answer/1704443 | 支撑平均日预算可能 overdelivery，套利团队需要外部硬止损 |
| Google Ads, Optimization score | https://support.google.com/google-ads/answer/9061547 | 支撑 optimization score 是诊断输入，不是套利利润目标 |
| Google Ads, Types of recommendations | https://support.google.com/google-ads/answer/3416396 | 支撑 recommendations 需要人审，不能自动应用高风险变更 |
| Google Ads API, Bidding strategy types | https://developers.google.com/google-ads/api/docs/campaigns/bidding/strategy-types | 支撑 API 层 campaign bid strategy 类型和未来安全集成 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把 approved/qualified/paid 结果作为离线转化回传，避免优化到低质量提交 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑回传延迟会影响 Smart Bidding 和短期 ROI 判断 |

## 22.1 转化信号质量与出价学习治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About Smart Bidding | https://support.google.com/google-ads/answer/7065882 | 支撑 Smart Bidding 围绕转化和转化价值优化，套利团队必须先治理信号质量 |
| Google Ads, Determine a bid strategy based on your goals | https://support.google.com/google-ads/answer/2472725 | 支撑按目标选择 Maximize Conversions、Target CPA、Maximize Conversion Value、Target ROAS 等策略 |
| Google Ads, Primary and secondary conversion actions | https://support.google.com/google-ads/answer/11461796 | 支撑 primary conversion 用于出价目标，secondary 更适合观察和诊断 |
| Google Ads, About conversion goals | https://support.google.com/google-ads/answer/10995103 | 支撑 conversion goal 可能把多个 action 组合，必须防止浅层事件混入出价目标 |
| Google Ads, About conversion measurement | https://support.google.com/google-ads/answer/1722022 | 支撑 conversion measurement 是优化、报告和出价学习的基础输入 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把后端 qualified、approved、paid 状态导入 Google Ads，而不是优化到 submitted lead |
| Google Ads, Offline conversion import discrepancies and errors | https://support.google.com/google-ads/answer/13321563 | 支撑 offline import 要看错误、匹配和处理差异，不把未匹配数据当作真实归因 |
| Google Ads, About enhanced conversions | https://support.google.com/google-ads/answer/9888656 | 支撑 Enhanced Conversions 是真实测量补强，需要同意、政策和数据最小化 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户提供数据、hashed data 和 customer match / enhanced conversions 的合规边界 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑转化延迟会影响近期 CPA/ROAS、学习期和扩量判断 |
| Google Ads, Bid strategy reports | https://support.google.com/google-ads/answer/7074568 | 支撑 bid strategy report 用于观察自动出价状态、学习和限制原因 |
| Google Ads, Evaluate automated bid strategy performance | https://support.google.com/google-ads/answer/10167267 | 支撑评估自动出价时要考虑目标、conversion lag 和足够时间窗口 |
| Google Ads, Use broad match with Smart Bidding | https://support.google.com/google-ads/answer/12159290 | 支撑 broad match 与 Smart Bidding 组合前必须确认目标信号和否定词治理 |
| Google Ads, About Performance Max campaigns | https://support.google.com/google-ads/answer/10724817 | 支撑 PMax 自动化流量依赖目标、素材、资产和转化信号，需要 paid revenue 复盘 |
| Google Ads, Change history | https://support.google.com/google-ads/answer/19888 | 支撑 conversion goal、value、bid strategy 和 budget 变更要进入事故复盘 |
| Google Ads API, Bidding strategy types | https://developers.google.com/google-ads/api/docs/campaigns/bidding/strategy-types | 支撑未来用官方 API 读取或设计 bid strategy 类型，不通过 Cookie 后台操作 |

## 22.1.1 CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把 CRM / buyer 的 qualified、approved、paid 状态以真实点击标识导入 Google Ads |
| Google Ads API, Enhanced conversions for leads | https://developers.google.com/google-ads/api/docs/conversions/enhanced-conversions/leads | 支撑 lead 后续状态匹配可以使用合规哈希用户提供数据，而不是 Cookie 后台或指纹 |
| Google Ads API, Upload conversion adjustments | https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments | 支撑 returned、refund、clawback 或 value 错误后的 conversion adjustment 治理 |
| Google Ads, About conversion measurement | https://support.google.com/google-ads/answer/1722022 | 支撑 conversion action 是广告效果反馈和优化输入 |
| Google Ads, About conversion goals | https://support.google.com/google-ads/answer/10995103 | 支撑多个 conversion actions 进入 goal 后会影响出价目标，需要避免浅层 stage 混入 |
| Google Ads, Set up enhanced conversions for leads | https://support.google.com/google-ads/answer/11021502 | 支撑 enhanced conversions for leads 的产品语境、用户数据和后续离线导入 |
| Google Ads, Offline conversion import discrepancies and errors | https://support.google.com/google-ads/answer/13321563 | 支撑 offline import 的错误、匹配率、未匹配和诊断 QA |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 CRM stage、buyer feedback 和 Ads 报表之间存在延迟窗口 |
| Google Ads, Time lag report | https://support.google.com/google-ads/answer/6239119 | 支撑分析从互动到转化的时间差，避免过早扩停 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑使用用户提供数据、enhanced conversions 和客户数据时的 consent、披露和安全处理要求 |
| Google tag, Consent mode overview | https://developers.google.com/tag-platform/security/concepts/consent-mode | 支撑 consent 状态影响广告测量和用户数据信号 |
| Google Analytics, Data freshness | https://support.google.com/analytics/answer/11198161 | 支撑不同报表有处理延迟，导入和决策应记录数据成熟度 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 lead PII 最小化、保留、删除、访问和供应商管理 |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation、buyer feedback、消费者信息流转和透明度背景 |
| Voluum, Conversion Status | https://doc.voluum.com/article/conversion-status | 支撑 pending、approved、rejected、payout 等 conversion status 与 buyer feedback 对账 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、transaction_id、payout、status 等 postback 参数映射 |

## 22.2 决策窗口、回传延迟与收入延迟治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About data freshness | https://support.google.com/google-ads/answer/2544985 | 支撑不同报表和指标有刷新延迟，不能把当天数字当最终决策依据 |
| Google Ads, Data discrepancies | https://support.google.com/google-ads/answer/7457111 | 支撑 Google Ads、Analytics、第三方和内部报表差异需要分层诊断 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 conversion lag 会影响近期 CPA/ROAS 和扩量窗口 |
| Google Ads, Conversion delay estimates | https://support.google.com/google-ads/answer/14545572 | 支撑用转化延迟估计避免过早判断 campaign 表现 |
| Google Ads, Bid strategy reports | https://support.google.com/google-ads/answer/7074568 | 支撑学习期、限制状态和自动出价表现要结合 lag 观察 |
| Google Ads, Evaluate automated bid strategy performance | https://support.google.com/google-ads/answer/10167267 | 支撑自动出价评估需要足够时间和正确观察窗口 |
| Google Ads, Budget report | https://support.google.com/google-ads/answer/10702522 | 支撑预算变化、花费和 forecast 复盘要结合等待窗口 |
| Google Ads, Change history | https://support.google.com/google-ads/answer/19888 | 支撑预算、出价、URL、goal 等变更进入决策窗口复盘 |
| Google Ads, Monitor experiments | https://support.google.com/google-ads/answer/6318747 | 支撑实验观察期和指标比较需要等待足够数据成熟 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑未来报表导入保存 GAQL、date range、timezone 和快照 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑 offline conversion 导入存在处理和匹配窗口 |
| Google Ads, Offline conversion import discrepancies and errors | https://support.google.com/google-ads/answer/13321563 | 支撑离线导入差异、错误和处理延迟要进入 wait-loss 判断 |
| Google AdSense, Payment timelines | https://support.google.com/adsense/answer/7164703 | 支撑 estimated/finalized/paid 的时间差和现金流窗口 |
| Google AdSense, Deductions from earnings FAQs | https://support.google.com/adsense/answer/2808531 | 支撑 finalized 下调、deduction 和扣量需要进入结算窗口 |
| Google SRE, Managing Incidents | https://sre.google/sre-book/managing-incidents/ | 支撑 stop-loss、containment 和事故分诊流程 |
| Google SRE, Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ | 支撑延迟误判、扩量事故和关账事故复盘 |

## 23. 关键词、搜索意图和选题来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Keyword Planner | https://support.google.com/google-ads/answer/7337243 | 支撑发现新关键词、查看搜索量、预测点击和成本 |
| Google Ads, Keyword matching | https://support.google.com/google-ads/answer/14996023 | 支撑 exact、phrase、broad match 的匹配逻辑和冷启动策略 |
| Google Ads, Negative keywords | https://support.google.com/google-ads/answer/2453972 | 支撑排除不相关搜索、控制花费和避免意图错配 |
| Google Ads, Search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑用真实查询复盘关键词质量和否定词机会 |
| Google Ads, Negative keyword ideas from search terms | https://support.google.com/google-ads/answer/7102466 | 支撑从 search terms 生成否定词 |
| Google Trends, Compare search terms | https://support.google.com/trends/answer/4359550 | 支撑比较搜索兴趣、地区和时间趋势 |
| Google Trends, FAQ about Trends data | https://support.google.com/trends/answer/4365533 | 支撑理解 Trends 数据是归一化兴趣而非绝对搜索量 |
| Google Trends, Related searches | https://support.google.com/trends/answer/4355000 | 支撑发现相关查询和选题方向 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑敏感词和广告承诺的真实性筛查 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑关键词、桥页和低价值目的地风险筛查 |

## 23.0 季节性、事件日历与需求预测来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, Use Keyword Planner | https://support.google.com/google-ads/answer/7337243 | 支撑发现关键词、查看搜索量、竞争和预测输入 |
| Google Ads Help, Get forecasts with Keyword Planner | https://support.google.com/google-ads/answer/3022575 | 支撑按预算、出价、国家和语言估算 clicks、cost 和 forecast |
| Google Trends Help, FAQ about Trends data | https://support.google.com/trends/answer/4365533 | 支撑 Trends 是归一化搜索兴趣，不是绝对搜索量或收入预测 |
| Google Trends Help, Compare Trends search terms | https://support.google.com/trends/answer/4359550 | 支撑比较不同主题、地区和时间窗口的相对兴趣 |
| Google Trends Help, Find related searches | https://support.google.com/trends/answer/4355000 | 支撑寻找相关查询、上升 query 和页面选题线索 |
| Google Ads Help, About the Insights page | https://support.google.com/google-ads/answer/10256472 | 支撑把需求变化、趋势和市场洞察作为诊断输入 |
| Google Ads Help, About demand forecasts on the Insights page | https://support.google.com/google-ads/answer/10787044 | 支撑用 demand forecasts 观察未来需求变化趋势 |
| Google Ads Help, About seasonality adjustments | https://support.google.com/google-ads/answer/10369906 | 支撑 Smart Bidding 短期转化率变化提示的适用边界 |
| Google Ads Help, Budget report | https://support.google.com/google-ads/answer/10702522 | 支撑预算 ramp、每日花费和月度花费限制复盘 |
| Google Ads Help, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑季节高峰后等待 conversion/revenue lag 再判断成败 |
| IRS, Tax Time Guide | https://www.irs.gov/newsroom/tax-time-guide | 支撑税务垂类使用官方税季资料和日期来源 |
| HealthCare.gov, Dates and deadlines | https://www.healthcare.gov/quick-guide/dates-and-deadlines/ | 支撑健康保险开放注册类页面使用官方日期来源 |

## 23.1 Search Terms、否定词与 Query Mining 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑用真实查询、keyword、match type、Search Partners 和表现数据做 query mining |
| Google Ads, Negative keywords | https://support.google.com/google-ads/answer/2453972 | 支撑 negative broad/phrase/exact、account-level negative、negative list 和层级治理 |
| Google Ads, Negative keyword ideas from search terms | https://support.google.com/google-ads/answer/7102466 | 支撑从 search terms report 选择 query 添加到 ad group、campaign 或 negative list |
| Google Ads, Keyword matching options | https://support.google.com/google-ads/answer/7478529 | 支撑 broad、phrase、exact、negative keywords、PMax/Search 优先级和 query 匹配原理 |
| Google Ads, Search terms insights | https://support.google.com/google-ads/answer/11386930 | 支撑 search category、subcategory、PMax/Search/Shopping 聚合查询主题和隐私聚合边界 |
| Google Ads, Search targeting and controls for PMax | https://support.google.com/google-ads/answer/16672776 | 支撑 PMax search themes、negative keywords、brand exclusions 和 Final URL expansion 控制 |
| Google Ads, Broad match | https://support.google.com/google-ads/answer/2407779 | 支撑 broad match 扩展范围、Smart Bidding 依赖和 query drift 风险 |
| Google Ads, Dynamic Search Ads | https://support.google.com/google-ads/answer/2471185 | 支撑 DSA 基于网站内容匹配 query 和自动生成标题的诊断边界 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 query 决策需要等待 conversion/revenue 回填 |
| Google Ads, Change history | https://support.google.com/google-ads/answer/19888 | 支撑否定词、match type、预算、URL、资产批量变更后的复盘 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑未来用官方 API 同步 search terms、segments 和 metrics |
| Google Ads API, Google Ads Query Language | https://developers.google.com/google-ads/api/docs/query/overview | 支撑 GAQL 字段、segment、filter 和查询快照 |
| Google Ads API, SearchTermView | https://developers.google.com/google-ads/api/fields/latest/search_term_view | 支撑未来以 `search_term_view` 保存 query 级报表 |
| Google Ads Policy, Trademarks | https://support.google.com/adspolicy/answer/6118 | 支撑品牌词、竞品词、商标和官方关系风险审计 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑官方身份、价格、资格、结果承诺和重要限制不能误导 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 query、广告承诺和 landing page 目的地一致 |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑不能用动态页面、隐藏目的地、cloaking 或多账号规避来处理 query 风险 |

## 24. 品牌词、商标与竞品投放来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Trademarks | https://support.google.com/adspolicy/answer/6118 | 支撑商标在广告中的使用、商标投诉、reseller/informational site 和关键词区别 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑不得隐藏或歪曲身份、价格、服务、商业关系、官方背书和资质 |
| Google Ads, Unacceptable business practices | https://support.google.com/adspolicy/answer/15938071 | 支撑冒充品牌、组织、公众人物或诱导用户交钱/交信息的严重风险 |
| Google Ads, Counterfeit goods | https://support.google.com/adspolicy/answer/176017 | 支撑仿牌、假货、与商标高度近似商品的禁投边界 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑竞品页、比较页和品牌词落地页需要目的地可用、有价值且与广告一致 |
| Google Ads, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑广告文字、display URL、标点、格式和误导性表达检查 |
| Google Ads, Negative keywords | https://support.google.com/google-ads/answer/2453972 | 支撑把禁止 brand、official、support、login 等词加入否定词清单 |
| Google Ads, Search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑用真实搜索词识别品牌词、竞品词、误触词和拒付风险 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑 affiliate 推荐、评测、排名和商业关系披露 |
| FTC, Disclosures 101 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | 支撑披露应清楚、明显、靠近相关推荐 |
| eCFR, Endorsements and Testimonials | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | 支撑 endorsement/testimonial 广告披露规则文本 |

## 25. 竞品广告、SERP 与 Ads Transparency 情报来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Transparency Center | https://adstransparency.google.com/ | 支撑人工查看公开广告素材、广告主和透明度信息 |
| Google Safety Center, Ads and data | https://safety.google/ads-and-data/ | 支撑广告透明度、广告控制和用户理解广告来源的背景 |
| Google Blog, Ads Transparency Center | https://blog.google/technology/safety-security/ads-transparency-center/ | 支撑 Ads Transparency Center 的公开定位和使用边界 |
| Google Ads Help, Ad Preview and Diagnosis tool | https://support.google.com/google-ads/answer/148778 | 支撑不用真实搜索点击广告，也能预览和诊断广告展示 |
| Google Ads Help, Auction insights | https://support.google.com/google-ads/answer/2579754 | 支撑用 impression share、overlap、top of page 等解释竞争强度 |
| Google Ads Help, Keyword Planner | https://support.google.com/google-ads/answer/7337243 | 支撑把竞品和 SERP 观察转成关键词规模和测试优先级 |
| Google Ads Help, Search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑用真实触发查询识别品牌、竞品、支持/login 和低意图流量 |
| Google Trends Help, FAQ about Trends data | https://support.google.com/trends/answer/4365533 | 支撑 Trends 是归一化兴趣，不是绝对搜索量或收入预测 |
| Google Ads Help, Advertiser verification | https://support.google.com/google-ads/answer/9008739 | 支撑广告主身份、披露和透明度背景 |
| Google Ads Policy, Trademarks | https://support.google.com/adspolicy/answer/6118 | 支撑竞品广告分析不能滑向商标误导或仿冒 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑不得通过竞品素材学习误导性官方关系、价格或资质 claim |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑竞品和自家页面都要满足目的地可用、一致和有价值 |
| FTC, Native Advertising | https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses | 支撑原生广告、商业关系和消费者识别广告性质 |
| FTC, Endorsements and reviews | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | 支撑评价、背书、商业关系和竞品比较页披露 |

## 26. 买量渠道和流量供应商尽调来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| AdSense, Traffic provider checklist | https://support.google.com/adsense/answer/3332805 | 支撑供应商尽调、样例 URL、价格异常、来源透明和测试前问题 |
| AdSense, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时发布商要监控来源并对质量负责 |
| AdSense, Set up a traffic segmentation plan | https://support.google.com/adsense/answer/2583698 | 支撑按 source/channel 分段监控和异常隔离 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑拒绝自动点击、机器人、欺骗软件和人为抬高收入/成本 |
| Google Ad Traffic Quality | https://www.google.com/ads/adtrafficquality/ | 支撑 Google 对广告流量质量、无效流量和生态保护的背景 |
| Google Ad Traffic Quality resources for publishers | https://www.google.com/intl/en/ads/adtrafficquality/publishers/ | 支撑发布商端流量质量管理和无效流量防护 |
| Google Ads, Google Network | https://support.google.com/google-ads/answer/1752334 | 支撑 Search、Display、Search Partners 等网络层级 |
| Google Ads, Display Network | https://support.google.com/google-ads/answer/2404190 | 支撑展示广告网络和低意图流量风险判断 |
| Google Ads, Performance Max | https://support.google.com/google-ads/answer/10724817 | 支撑 PMax 多库存自动化和黑盒测试边界 |
| Google Ads, Demand Gen campaigns | https://support.google.com/google-ads/answer/13695389 | 支撑 Demand Gen 内容/视觉触达特性 |
| Google Ads API, AdNetworkType | https://developers.google.com/google-ads/api/reference/rpc/v20/AdNetworkTypeEnum.AdNetworkType | 支撑按网络类型分析导入指标和自动化报表 |

## 26. Google Ads 流量库存、版位与排除控制来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About content suitability | https://support.google.com/google-ads/answer/12764663 | 支撑通过 content suitability 管理广告展示环境、内容类型和品牌安全 |
| Google Ads, Exclude placements at the account level | https://support.google.com/google-ads/answer/7331110 | 支撑 account-level placement exclusions 覆盖 websites、apps、YouTube videos/channels 等 |
| Google Ads, Exclude specific webpages and videos | https://support.google.com/google-ads/answer/2454012 | 支撑排除网页、YouTube 视频、channels、apps 和 parked domains 等具体位置 |
| Google Ads, Placement exclusion lists | https://support.google.com/google-ads/answer/9162992 | 支撑跨账号复用 placement exclusion lists 的治理思路 |
| Google Ads, Performance Max campaigns | https://support.google.com/google-ads/answer/10724817/about-performance-max-campaigns | 支撑 PMax 跨 Google inventory 自动化投放和适用边界 |
| Google Ads, Search targeting & controls for Performance Max | https://support.google.com/google-ads/answer/16672776 | 支撑 PMax 的 search terms、negative keywords、brand exclusions 和 final URL expansion 控制 |
| Google Ads, PMax channel performance report | https://support.google.com/google-ads/answer/16260130 | 支撑按 Search、YouTube、Discover、Gmail 等 channel 复盘 PMax 表现 |
| Google Ads, Final URL expansion in Performance Max | https://support.google.com/google-ads/answer/14337539 | 支撑 PMax 自动选择同域页面的风险和控制 |
| Google Ads, URL exclusion in Performance Max | https://support.google.com/google-ads/answer/14337773 | 支撑排除不应被 Final URL expansion 使用的页面 |
| Google Ads, Brand exclusions | https://support.google.com/google-ads/answer/14505308 | 支撑 PMax 或 Search campaign 应用 brand exclusions |
| Google Ads, Brand suitability features in Performance Max | https://support.google.com/google-ads/answer/13607727 | 支撑 PMax 中 content suitability、placement exclusions、brand exclusions 等品牌适宜性控制 |
| Google Ads, Asset reporting in Performance Max | https://support.google.com/google-ads/answer/10725056 | 支撑用 asset report 复盘素材表现和误导性高 CTR 风险 |
| Google Ads, Display Network | https://support.google.com/google-ads/answer/2404190 | 支撑 Display inventory、低意图流量和 placement 管理 |
| Google Ads, Demand Gen campaigns | https://support.google.com/google-ads/answer/13695389 | 支撑 Demand Gen 的视觉库存、YouTube/Discover/Gmail 场景和适用边界 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑低价值目的地、arbitrage、桥页和广告网络滥用风险 |

## 26.1 Source、Publisher、Placement 质量评分与名单治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google AdSense Help, Traffic provider checklist | https://support.google.com/adsense/answer/3332805 | 支撑供应商尽调、来源透明、样例 URL、价格异常和质量报告 |
| Google AdSense Help, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时发布商需要监控每个来源并暂停可疑来源 |
| Google AdSense Help, Set up a traffic segmentation plan | https://support.google.com/adsense/answer/2583698 | 支撑按来源、渠道和广告位置分段监控流量质量 |
| Google AdSense Help, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑无效流量、自动点击、机器人和人为抬高收入的边界 |
| Google Ads Help, Managing invalid traffic | https://support.google.com/google-ads/answer/11182074 | 支撑广告主侧 invalid clicks 和异常来源诊断 |
| Google Ads Help, Use placement exclusion lists | https://support.google.com/google-ads/answer/9162992 | 支撑把坏 publisher、placement、app、channel 进入排除名单 |
| Google Ads Help, About content suitability | https://support.google.com/google-ads/answer/12764663 | 支撑品牌安全、内容适宜性和展示环境控制 |
| Google Ads Help, PMax channel performance report | https://support.google.com/google-ads/answer/16260130 | 支撑 PMax channel 级来源质量复盘 |
| Google Ads Help, Search targeting and brand controls in Performance Max | https://support.google.com/google-ads/answer/16672776 | 支撑 PMax search terms、negative keywords、brand exclusions 和 URL 控制 |
| Google Ads Help, About ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 支撑把 network、campaign、keyword、creative、device 等点击上下文写入追踪 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、payout、transaction_id、status 和 buyer feedback 回传 |
| IAB UK, Made for Advertising website definition | https://www.iabuk.com/jargon-buster/made-advertising-mfa-website | 支撑识别 MFA、低价值 publisher 和页面质量风险 |

## 26.2 流量供应商合同、IO、退款与争议治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| IAB, General Terms and Conditions | https://www.iab.com/guidelines/general-terms-and-conditions/ | 支撑数字广告媒体采购的标准条款、IO、付款、取消和争议治理背景 |
| IAB, IAB unites the industry with new standard terms | https://www.iab.com/blog/iab-unites-the-industry-with-new-standard-terms/ | 支撑行业正在标准化媒体交易条款，降低谈判和执行摩擦 |
| Google AdSense Help, Traffic provider checklist | https://support.google.com/adsense/answer/3332805 | 支撑把来源透明、样例 URL、价格异常和质量报告写进供应商准入 |
| Google AdSense Help, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时需要监控每个来源并暂停可疑来源 |
| Google Ads Help, Managing invalid traffic | https://support.google.com/google-ads/answer/11182074 | 支撑无效点击、invalid click rate、credit 和广告主侧异常诊断 |
| Google Ads Help, About ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 支撑在合同 tracking appendix 中约定可回放的点击上下文字段 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 creative、landing page、tracking URL 和最终页面一致性 |
| FTC, Native Advertising Guide for Businesses | https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses | 支撑 native、advertorial、sponsorship 场景中的广告识别和披露 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑把 click_id、status、payout 和 transaction_id 写入 postback 证据链 |
| Google SRE Book, Managing Incidents | https://sre.google/sre-book/managing-incidents/ | 支撑争议 case 的 owner、状态、恢复和沟通流程 |

## 27. Affiliate Network / Lead Buyer 尽调来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑 affiliate disclosure、推荐、评测和佣金关系披露原则 |
| FTC, Endorsements, Influencers, and Reviews | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | 支撑商业关系披露和消费者误导风险 |
| FTC, Disclosures 101 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | 支撑披露应清楚、明显、靠近相关推荐 |
| eCFR, Endorsements and Testimonials in Advertising | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | 支撑美国 endorsement/testimonial 广告披露规则文本 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑禁止虚假身份、隐藏商业关系、误导价格或服务 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑桥页、网关页、低价值 affiliate 页面和广告网络滥用风险 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 affiliate landing page、Offer URL 和广告承诺一致性 |
| Google Ads, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑金融类 affiliate/lead offer 的认证、限制和敏感垂类风险 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑拒绝伪造 lead、自动点击和人为抬高收入/成本 |
| AdSense, Online advertising to get new users | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时需要对来源质量和无效流量负责 |

## 27.1 Offer Cap、Payout、状态变更与替代 Offer 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| TUNE, Offer Payouts and Caps | https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps | 支撑 affiliate offer 的 payout、conversion cap、budget cap 和 tier 概念 |
| TUNE Dev Hub, OfferConversionCap | https://developers.tune.com/network-models/offerconversioncap/ | 支撑按 offer/affiliate 保存 conversion、payout、revenue cap 的数据模型 |
| Everflow API, Get Offer | https://developers.everflow.io/docs/affiliate/offers/ | 支撑 offer status、daily payout cap、affiliate status 和 offer 字段快照 |
| Everflow Helpdesk, Advertiser Feeds | https://helpdesk.everflow.io/customer/advertiser-feeds | 支撑 advertiser feed 同步 payout、landing page URL、targeting rules 和 caps 可能覆盖本地配置 |
| Voluum, Glossary | https://doc.voluum.com/article/glossary | 支撑 conversion cap、fallback/redirect offer、offer grouping 等追踪概念 |
| Voluum, Tracking Payouts | https://doc.voluum.com/en/tracking_payout.html | 支撑从 affiliate network postback 接收动态 payout |
| Voluum, Conversion Status | https://doc.voluum.com/article/conversion-status | 支撑 conversion status、postback timestamp、payout 等状态对账 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、transaction_id、payout 和 postback 参数设计 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑替代 Offer、payout claim、价格、资格和主体不能误导 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目标页和广告承诺一致，不能切到不相关 Offer |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑不能用动态目的地、cloaking、多账号或隐藏真实目的地规避政策 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑低价值目的地、桥页和流量套利质量风险 |
| FTC, Endorsements, influencers, and reviews | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | 支撑 affiliate 推荐、评价、排名和商业关系披露 |
| FTC, Disclosures 101 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | 支撑 disclosure 应清楚、明显、靠近推荐内容 |

## 28. Lead 质量、Postback 对账与拒付来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation 涉及消费者信息、营销链条、披露和消费者保护问题 |
| FTC, Staff Perspective: Follow the Lead | https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf | 支撑 lead generation 生态、数据流转、透明度和合规风险背景 |
| Google Ads, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Google Ads Lead Form 的资格、隐私政策、收集信息和广告政策要求 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户数据收集、分享、同意、隐私政策和数据处理要求 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 lead 页面主体、价格、服务、商业关系和官方身份不得误导 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑金融、健康、身份等敏感类别在个性化广告中的限制 |
| Google Ads, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑贷款、债务、金融 lead 的认证、披露、地区和禁投项 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑离线转化、lead 后续质量和批准结果回传的安全集成方向 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、transaction_id、payout、status 等 postback 归因和去重概念 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑 affiliate 推荐、评测、商业关系和披露义务 |
| CFPB, Digital comparison-shopping circular | https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/ | 支撑金融产品比较、导流、补偿驱动排序和消费者误导风险 |

## 28.1 Ping/Post、Lead Buyer Routing 与线索市场来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation 生态、消费者信息流转、透明度和消费者保护风险 |
| FTC, Staff Perspective: Follow the Lead | https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf | 支撑 lead marketplace、数据流转、披露和消费者保护背景 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话销售、Do Not Call、seller/telemarketer 责任和记录保存治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 和 suppression 检查需要进入 lead handoff 流程 |
| FTC, .com Disclosures | https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising | 支撑页面和表单披露必须清楚、明显、靠近相关 claim |
| FCC, TCPA one-to-one consent rule court response / deletion order | https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf | 支撑 one-to-one consent 规则状态需要按日期和来源管理 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| eCFR, 16 CFR 310.5 Recordkeeping requirements | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5 | 支撑 consent、交易和电话销售记录保存要求 |
| Google Ads, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Lead Form 资格、隐私政策和广告政策要求 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户数据、披露、同意、分享和隐私政策要求 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑页面主体、价格、服务、商业关系和 buyer handoff 不得误导 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑敏感类别、金融、健康、身份和困境状态不能被不当用于定向 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑用真实 approved/paid buyer feedback 回传，而不是 Cookie 后台操作 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、transaction_id、payout、status 等 postback 归因和去重概念 |
| TUNE, Offer Payouts and Caps | https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps | 支撑 payout、cap、budget、tier 和 offer 经济口径 |
| Everflow API, Get Offer | https://developers.everflow.io/docs/affiliate/offers/ | 支撑 offer、payout、cap、targeting 和 status 字段快照 |
| PingTree, Ping Post | https://docs.pingtree.com/documentation/campaign/distribution/ping-post | 行业参考：支撑 ping/post、lead distribution 和 buyer response 的平台实现概念 |
| ActiveProspect, LeadConduit | https://activeprospect.com/products/leadconduit/ | 行业参考：支撑 lead acquisition、routing、filtering、delivery 和 compliance evidence 的市场工具形态 |

## 28.2 Lead 验证、Suppression、去重与 PII 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑数据最小化、访问控制、保留、删除和个人信息保护基本原则 |
| FTC, Start with Security | https://www.ftc.gov/business-guidance/resources/start-security-guide-business | 支撑按数据生命周期、访问权限和供应商管理治理 lead PII |
| FTC, Data Security | https://www.ftc.gov/business-guidance/privacy-security/data-security | 支撑个人信息安全、数据保留和泄露风险治理 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑 telemarketing、seller、DNC、consent 和记录保存治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和 seller/telemarketer 合规语境 |
| FTC, Q&A for Telemarketers & Sellers About DNC | https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0 | 支撑 entity-specific DNC、opt-out 和电话营销拒绝联系流程 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑商业邮件、退订和 opt-out 请求处理 |
| FTC, Safeguards Rule | https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know | 支撑金融类 customer information 保护、访问控制和供应商监督 |
| NIST, SP 800-122 | https://csrc.nist.gov/pubs/sp/800/122/final | 支撑 PII 识别、最小化、保密性保护和风险分级 |
| NIST, Privacy Framework | https://www.nist.gov/privacy-framework | 支撑隐私风险管理、治理、控制和持续改进框架 |
| California Attorney General, CCPA | https://oag.ca.gov/privacy/ccpa | 支撑加州消费者访问、删除、opt-out 和个人信息权利语境 |
| California Privacy Protection Agency, Data Brokers | https://cppa.ca.gov/data_brokers/ | 支撑数据经纪人、删除请求和数据转售治理语境 |
| CFPB, Regulation V / FCRA | https://www.consumerfinance.gov/rules-policy/regulations/1022/ | 支撑信贷、保险、就业、住房等资格判断场景不能按普通营销 lead 处理 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户数据收集、披露、同意、分享和隐私政策要求 |
| Google Ads, Data collection and use | https://support.google.com/adspolicy/answer/6020956 | 支撑广告页面收集个人信息、披露、用途和安全要求 |
| Google Ads, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Lead Form 的隐私政策、字段收集和广告政策要求 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑敏感类别、身份、健康、金融困境等不能被不当用于定向 |
| Google Analytics, Avoid sending PII | https://support.google.com/analytics/answer/6366371 | 支撑 URL、日志、analytics 字段避免发送 PII |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| eCFR, 16 CFR 310.5 Recordkeeping requirements | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5 | 支撑 consent、交易、电话销售和记录保存要求 |

## 28.3 Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation 涉及消费者信息流转、buyer handoff、透明度和消费者保护风险 |
| FTC, Staff Perspective: Follow the Lead | https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf | 支撑 lead marketplace、数据转售、披露、投诉和监管背景 |
| FTC, .com Disclosures | https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising | 支撑 buyer disclosure、费用/资格限制和 CTA 附近披露 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 lead PII 最小化、访问控制、保留、删除和供应商管理 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话 lead、seller/telemarketer、DNC、consent、记录保存和争议证据 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC、suppression 和停止联系流程需要进入 buyer handoff |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| eCFR, 16 CFR 310.5 Recordkeeping requirements | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5 | 支撑 consent、交易、电话销售和记录保存要求 |
| Google Ads, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Google Ads Lead Form 的隐私政策、字段收集、资格和广告政策要求 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户数据、consent、隐私披露、分享和数据处理要求 |
| Google Ads Policy, Data collection and use | https://support.google.com/adspolicy/answer/6020956 | 支撑广告页面收集个人信息、披露、用途和安全处理要求 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 buyer、价格、资格、官方关系、服务结果和 CTA 不能误导 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把真实 qualified/approved/paid buyer feedback 回传给广告优化，不通过 Cookie 后台操作 |
| Google Ads Help, About enhanced conversions for leads | https://support.google.com/google-ads/answer/11021502 | 支撑 lead 后续状态匹配和回传需要基于用户提供数据、同意和安全处理 |
| TUNE, Offer Payouts and Caps | https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps | 支撑 payout、conversion cap、budget cap 和 offer 经济口径 |
| TUNE Dev Hub, OfferConversionCap | https://developers.tune.com/network-models/offerconversioncap/ | 支撑 offer/affiliate conversion cap、payout/revenue cap 和数据模型 |
| Everflow API, Get Offer | https://developers.everflow.io/docs/affiliate/offers/ | 支撑 offer status、payout、cap、targeting、affiliate status 和字段快照 |
| Voluum, Conversion Status | https://doc.voluum.com/article/conversion-status | 支撑 conversion status、approved/rejected/pending 口径和 postback 状态对账 |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、transaction_id、payout、status 和 postback 参数设计 |

## 29. 实验设计、样本量和优化决策来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Test with confidence with the Experiments page | https://support.google.com/google-ads/answer/7281575 | 支撑 campaign experiment 分流、控制变量和测试变更 |
| Google Ads, Experiments page | https://support.google.com/google-ads/answer/10682377 | 支撑通过 Experiments 页面管理实验、查看结果和应用变更 |
| Google Ads API, Experiments overview | https://developers.google.com/google-ads/api/docs/experiments/overview | 支撑未来用 API 读取或管理 experiments，而不是 Cookie 后台操作 |
| Google Ads API, Create experiments | https://developers.google.com/google-ads/api/docs/experiments/experiments | 支撑实验对象、草稿 campaign 和实验流程 |
| Google Ads Scripts, Campaign Drafts and Experiments | https://developers.google.com/google-ads/scripts/docs/campaigns/drafts-experiments | 支撑通过授权 Scripts 管理草稿和实验 |
| Google Ads, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑转化延迟会影响短期 CPA/ROAS 判断 |
| Google Ads, Conversion delay estimates | https://support.google.com/google-ads/answer/14545572 | 支撑用延迟估计避免过早判断 campaign 表现 |
| Google Ads, Time lag report | https://support.google.com/google-ads/answer/6239119 | 支撑分析客户从点击到转化需要多久 |
| GA4, Data freshness | https://support.google.com/analytics/answer/11198161 | 支撑 GA4 数据处理延迟和日报误差 |
| AdSense, Payment timelines | https://support.google.com/adsense/answer/7164703 | 支撑 estimated/finalized/paid revenue 的时间差 |
| AdSense, Deductions from earnings FAQs | https://support.google.com/adsense/answer/2808531 | 支撑扣量和 finalized revenue 调整对实验结论的影响 |

## 30. 无效流量识别和来源隔离来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑无效点击、无效展示、自动工具和人为抬高收入/成本的定义 |
| AdSense, How Google prevents invalid traffic | https://support.google.com/adsense/answer/1348752 | 支撑 Google 自动系统和人工审核过滤无效点击、展示和相关活动 |
| AdSense, Traffic provider checklist | https://support.google.com/adsense/answer/3332805 | 支撑供应商尽调、来源透明、样例 URL 和价格异常判断 |
| AdSense, Set up a traffic segmentation plan | https://support.google.com/adsense/answer/2583698 | 支撑按流量来源分段监控、识别异常和隔离来源 |
| AdSense, Online advertising to get new users | https://support.google.com/adsense/answer/1348722 | 支撑发布商购买流量时需监控质量并避免无效流量 |
| Google Ads, Managing invalid traffic | https://support.google.com/google-ads/answer/11182074 | 支撑 Google Ads invalid clicks、过滤和广告主侧无效流量管理 |
| Google Ad Traffic Quality, How we prevent it | https://www.google.com/ads/adtrafficquality/how-we-prevent-it/ | 支撑 Google 广告流量质量系统如何预防和检测无效流量 |
| Google Ad Traffic Quality, Publisher resources | https://www.google.com/ads/adtrafficquality/publishers/ | 支撑发布商侧防止无效流量和保护广告库存 |
| Google Ads API, Metrics fields | https://developers.google.com/google-ads/api/fields/v23/metrics | 支撑 invalid clicks、invalid click rate 等指标字段扩展 |
| AdSense, Deductions from earnings FAQs | https://support.google.com/adsense/answer/2808531 | 支撑扣量、收入调整和结算复盘 |

## 31. 内容生产、页面可信度和编辑质量来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Search Central, Helpful content | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | 支撑 people-first content、原创价值、作者/来源/信任和避免搜索引擎优先内容 |
| Google Search Central, SEO Starter Guide | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | 支撑页面标题、结构、内容组织和用户优先的基本页面实践 |
| Google Search Central, Spam policies | https://developers.google.com/search/docs/essentials/spam-policies | 支撑 cloaking、自动生成低质内容、薄 affiliate 页面和滥用规模化内容的风险 |
| Google Search Quality Rater Guidelines | https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf | 支撑 E-E-A-T、页面目的、可信度和 YMYL 判断框架 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑目的地原创内容、页面可达、桥页和广告承诺一致性 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑禁止虚假承诺、隐藏主体、误导价格和商业关系 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑桥页、低价值目的地和套利滥用风险 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑发布商内容、广告行为和用户体验边界 |
| Google Publisher Policies | https://support.google.com/publisherpolicies/answer/10437486 | 支撑发布商库存质量、内容和广告体验 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑 affiliate/推荐/评测页面披露商业关系 |

## 32. 账号健康、政策中心和申诉来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Fix a disapproved ad or appeal a policy decision | https://support.google.com/google-ads/answer/9338593 | 支撑广告拒登修复、申诉入口和 appeal 前先修改广告/资产/目标页 |
| Google Ads, Policy Manager | https://support.google.com/google-ads/answer/9675313 | 支撑集中查看政策问题和申诉状态 |
| Google Ads, Account suspensions overview | https://support.google.com/adspolicy/answer/2375414 | 支撑账号暂停后应修复问题并提交申诉，而不是换账号规避 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑禁止隐藏真实目的地、多账号规避、cloaking 和绕过政策执行 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑主体、价格、服务、资质和商业关系需要真实透明 |
| Google Ads, Advertiser verification | https://support.google.com/adspolicy/answer/9703665 | 支撑广告主身份和业务操作验证 |
| Google Ads, Tasks required for Advertiser verification | https://support.google.com/adspolicy/answer/15577076 | 支撑广告主验证任务、业务操作和资料准备 |
| Google Ads API, Policy support | https://developers.google.com/google-ads/api/support/policy | 支撑通过 API 理解 ad disapprovals 和 account recovery 问题 |
| AdSense, Policy Center statuses | https://support.google.com/adsense/answer/15689616 | 支撑区分 policy issue、regulatory issue、advertiser preference 和 ad serving status |
| AdSense, Fix policy issues that affect ad serving | https://support.google.com/adsense/answer/7003627 | 支撑在 Policy Center 修复问题并 request review |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑发布商基础政策、内容和广告行为边界 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑无效流量、扣量、广告服务限制和来源隔离 |

## 33. 发布商变现栈来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| AdSense, Metrics glossary | https://support.google.com/adsense/answer/2735899 | 支撑 page RPM、impression RPM、Active View、coverage、CTR 等收入端指标 |
| AdSense, Set up ads on your site | https://support.google.com/adsense/answer/7037624 | 支撑 Auto ads、手动广告单元和广告代码设置 |
| AdSense, Ad placement policies | https://support.google.com/adsense/answer/1346295 | 支撑广告不能伪装成内容、不能激励点击、不能改变广告行为 |
| AdSense, Best practices for ad placement | https://support.google.com/adsense/answer/1282097 | 支撑广告位应不压过内容、不误导用户、内容容易找到 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑发布商变现的基础政策边界 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑无效点击、无效展示、自动工具和人为抬高收入的风险 |
| AdSense Management API, Metrics and Dimensions | https://developers.google.com/adsense/management/metrics-dimensions | 支撑未来收入端指标导入和字段口径扩展 |
| Google Ad Manager Partner Guidelines | https://support.google.com/publisherpolicies/answer/9059370 | 支撑 Ad Manager / AdX 合作伙伴政策、广告行为和流量质量要求 |
| Google Ad Manager, Open Bidding | https://admanager.google.com/home/resources/feature-brief-open-bidding/ | 支撑多需求方竞价和 ad stack 复杂化背景 |
| Google Ad Manager, Ad review center | https://admanager.google.com/home/resources/feature-brief-ad-review-center/ | 支撑发布商审查广告质量和需求内容 |

## 34. 程序化供应链透明度来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| IAB Tech Lab, Authorized Digital Sellers ads.txt | https://iabtechlab.com/ads-txt/ | 支撑网站公开授权 seller、DIRECT/RESELLER 和防止未授权库存销售 |
| IAB Tech Lab, sellers.json | https://iabtechlab.com/sellers-json/ | 支撑广告系统公开 seller ID、seller type、name 和 domain |
| IAB Tech Lab, SupplyChain Object | https://iabtechlab.com/supplychainobject/ | 支撑 bid request 中表达供应链节点、complete 和 seller ID |
| IAB Tech Lab, OpenRTB | https://iabtechlab.com/standards/openrtb/ | 支撑程序化交易对象、bid request 和 schain 所在技术语境 |
| Google AdSense, Authorize sellers with ads.txt | https://support.google.com/adsense/answer/7532444 | 支撑 AdSense 发布商通过 ads.txt 授权卖方 |
| Google Ad Manager, Manage ads.txt files | https://support.google.com/admanager/answer/7441288 | 支撑 GAM 场景中管理 ads.txt、授权 seller 和库存可售性 |
| Google Ad Manager, MCM Manage Inventory | https://support.google.com/admanager/answer/11103843 | 支撑 Multiple Customer Management 下 parent/child 和库存管理关系 |
| Google Ad Manager, Multiple Customer Management | https://support.google.com/admanager/answer/11194376 | 支撑 MCM 授权、管理关系和发布商身份解释 |
| Google Ad Manager Partner Guidelines | https://support.google.com/publisherpolicies/answer/9059370 | 支撑 GAM/AdX 伙伴流量质量、广告行为和供应链治理 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑发布商广告行为、内容和流量质量基础政策 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑供应链透明不能替代真实流量质量，异常仍按无效流量复盘 |
| AdSense, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时发布商需要监控来源并承担质量责任 |

## 35. GAM / AdX Yield、Floor Price 与 Pricing Rules 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ad Manager, Unified pricing rules | https://support.google.com/admanager/answer/9298008 | 支撑 floor price、pricing rule 和程序化定价边界 |
| Google Ad Manager, Dynamic allocation | https://support.google.com/admanager/answer/1143651 | 支撑不同 demand、line item 和 AdX/Ad Manager 竞争分配逻辑 |
| Google Ad Manager, Line item types and priorities | https://support.google.com/admanager/answer/177279 | 支撑 sponsorship、standard、price priority、house 等 line item priority |
| Google Ad Manager, Open Bidding | https://support.google.com/admanager/answer/7128453 | 支撑第三方 exchange 与 Google demand 竞争的基本边界 |
| Google Ad Manager, Yield groups | https://support.google.com/admanager/answer/7386124 | 支撑按 yield partner 组织和复盘 demand source |
| Google Ad Manager, Ad Exchange line items | https://support.google.com/admanager/answer/138314 | 支撑 AdX line item 和程序化需求配置 |
| Google Ad Manager, Forecasting | https://support.google.com/admanager/answer/2917835 | 支撑 line item delivery、库存预测和保量冲突诊断 |
| Google Ad Manager, Ad review center | https://admanager.google.com/home/resources/feature-brief-ad-review-center/ | 支撑审查广告质量和需求内容 |
| AdSense, Metrics glossary | https://support.google.com/adsense/answer/2735899 | 支撑 eCPM、RPM、coverage、CTR、Active View 等指标口径 |
| Google Ad Manager Partner Guidelines | https://support.google.com/publisherpolicies/answer/9059370 | 支撑 GAM/AdX partner 合规和流量质量 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑拒绝用刷请求、刷展示、误点或自动化刷新提高 yield |

## 36. Header Bidding / Prebid.js 与广告栈延迟来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Prebid, Prebid.js overview | https://docs.prebid.org/prebid/prebidjs.html | 支撑 Prebid.js 作为页面端 header bidding wrapper 的基础概念 |
| Prebid, Getting started with Prebid.js | https://docs.prebid.org/dev-docs/getting-started.html | 支撑 ad unit、bidder、auction 和 GPT/GAM 协作的基础链路 |
| Prebid, Ad Ops step-by-step | https://docs.prebid.org/adops/step-by-step.html | 支撑 GAM line item、creative、key-value 和 ad ops 配置边界 |
| Prebid, Price granularity | https://docs.prebid.org/adops/price-granularity.html | 支撑 price bucket、line item 数量和 yield 精度权衡 |
| Prebid, Floors module | https://docs.prebid.org/dev-docs/modules/floors.html | 支撑 Prebid floor、bid filtering 和 GAM floor 区分 |
| Prebid, Consent Management TCF module | https://docs.prebid.org/dev-docs/modules/consentManagementTcf.html | 支撑 TCF、CMP、consent 状态和 bidder 参与边界 |
| Prebid, User ID module | https://docs.prebid.org/dev-docs/modules/userId.html | 支撑 User ID、identity、隐私披露和 opt-out 风险判断 |
| Prebid, Supply Chain Object module | https://docs.prebid.org/dev-docs/modules/schain.html | 支撑 Header Bidding 中 schain 传递和供应链解释 |
| Prebid, Troubleshooting guide | https://docs.prebid.org/troubleshooting/troubleshooting-guide.html | 支撑页面端调试、bid response、targeting 和错误排查 |
| Google Publisher Tag, Control ad loading and refresh | https://developers.google.com/publisher-tag/guides/control-ad-loading | 支撑 GPT 广告加载、刷新和页面端广告请求时序 |
| Google Publisher Tag, Ad event listeners sample | https://developers.google.com/publisher-tag/samples/ad-event-listeners | 支撑 slot render、impression viewable 等事件调试 |
| Google Ad Manager, Line item types and priorities | https://support.google.com/admanager/answer/177279 | 支撑 Header Bidding winner 进入 GAM 后的 line item priority 解释 |
| Google Ad Manager, Key-values | https://support.google.com/admanager/answer/177381 | 支撑 hb_pb、hb_bidder、slot 等 key-value targeting QA |
| Google Ad Manager, Google consent management requirements | https://support.google.com/admanager/answer/14139515 | 支撑 GAM / AdX 发布商使用 CMP/TCF 的合规要求 |
| IAB Tech Lab, Authorized Digital Sellers ads.txt | https://iabtechlab.com/ads-txt/ | 支撑 SSP/bidder seller 授权和 DIRECT/RESELLER QA |
| IAB Tech Lab, sellers.json | https://iabtechlab.com/sellers-json/ | 支撑 seller ID、seller type、name 和 domain 解释 |
| IAB Tech Lab, SupplyChain Object | https://iabtechlab.com/supplychainobject/ | 支撑 Header Bidding 和 OpenRTB 链路中的 schain 解释 |

## 37. 广告位、刷新、可见率与页面体验来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| AdSense, Metrics glossary | https://support.google.com/adsense/answer/2735899 | 支撑 page RPM、impression RPM、coverage、CTR、Active View 等广告位收入和可见率指标 |
| AdSense, Ad placement policies | https://support.google.com/adsense/answer/1346295 | 支撑广告不能伪装成内容、不能激励点击、不能改变广告行为或误导用户 |
| AdSense, Best practices for ad placement | https://support.google.com/adsense/answer/1282097 | 支撑广告位应清楚可识别、内容容易找到、广告数量不能压过页面任务 |
| AdSense, Set up ads on your site | https://support.google.com/adsense/answer/7037624 | 支撑 Auto ads、手动广告单元和广告代码设置的基础语境 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑发布商不得鼓励点击、自动点击、误导展示和不合规广告行为 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑误点、诱导、自动工具和人为抬高收入/成本的风险复盘 |
| Google Ad Manager, Declare ad refresh inventory | https://support.google.com/admanager/answer/6286179 | 支撑刷新库存需要声明、拆分和按刷新类型复盘 |
| Google Publisher Tag, Control ad loading and refresh | https://developers.google.com/publisher-tag/guides/control-ad-loading | 支撑 GPT 可控制广告加载和刷新，但本系统只沉淀策略和审计，不生成刷新代码 |
| Google Publisher Tag, Lazy loading sample | https://developers.google.com/publisher-tag/samples/lazy-loading | 支撑 lazy loading 广告位需要和可见率、加载性能、布局稳定一起测试 |
| Google Ad Manager Partner Guidelines | https://support.google.com/publisherpolicies/answer/9059370 | 支撑 GAM/AdX 合作伙伴对广告行为、流量质量和合规变现的要求 |
| Google Search Central, Avoid intrusive interstitials and dialogs | https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials | 支撑插屏、遮挡内容和干扰页面任务的体验风险 |
| web.dev, Cumulative Layout Shift | https://web.dev/articles/cls | 支撑广告容器未预留尺寸会造成布局跳动和页面体验问题 |
| web.dev, Optimize Cumulative Layout Shift | https://web.dev/articles/optimize-cls | 支撑广告位优化需要预留尺寸、控制动态插入和减少 CLS |
| Better Ads Standards | https://www.betterads.org/standards/ | 支撑弹窗、插屏、自动播放有声视频、sticky 和广告密度等广告体验标准 |
| Coalition for Better Ads, Desktop ad density higher than 50% | https://www.betterads.org/desktop-ad-density-over-50-percent | 支撑桌面主内容广告密度计算方式和 50% 风险阈值 |

## 38. 隐私、Consent 和追踪合规来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google tag, Consent mode overview | https://developers.google.com/tag-platform/security/concepts/consent-mode | 支撑 Consent Mode、consent types 和 Google tags 根据同意状态调整行为 |
| Google tag, Set up consent mode on websites | https://developers.google.com/tag-platform/security/guides/consent | 支撑网站上设置默认 consent、更新 consent 和标签执行顺序 |
| Google Analytics, Consent type | https://support.google.com/analytics/answer/12334711 | 支撑 `ad_storage`、`analytics_storage`、`ad_user_data`、`ad_personalization` 等字段解释 |
| Google Analytics, Tag Manager consent mode support | https://support.google.com/analytics/answer/10718549 | 支撑 GTM 中 consent settings 和标签依赖配置 |
| Google Analytics, Consent mode reference | https://support.google.com/analytics/answer/13802165 | 支撑 consent mode 参数和参考行为 |
| Google Ads, Obtain required consent signals | https://support.google.com/google-ads/answer/16142449 | 支撑 EEA 等场景广告测量需要传递必要同意信号 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑 Enhanced Conversions 和用户提供数据的政策边界 |
| Google Ads, About enhanced conversions | https://support.google.com/google-ads/answer/9888656 | 支撑 enhanced conversions 的用途、用户提供数据和安全处理 |
| AdSense, EU user consent policy | https://support.google.com/adsense/answer/7670013 | 支撑发布商面向 EEA/UK/Switzerland 用户取得同意 |
| AdSense, Google consent management requirements for publishers | https://support.google.com/adsense/answer/13554116 | 支撑发布商使用 certified CMP 和 TCF 要求 |
| AdSense, Privacy & messaging | https://support.google.com/adsense/answer/10924669 | 支撑 GDPR、CPRA 和其他隐私消息管理 |
| Ad Manager, Google consent management requirements | https://support.google.com/admanager/answer/14139515 | 支撑 GAM / AdX 发布商 consent management 要求 |

## 39. 敏感垂类政策与 Offer 准入来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑金融、贷款、债务、加密、投资和 lead generation 的披露、地区规则、认证和禁投项 |
| Google Ads, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑医疗、药品、远程医疗、健康服务和认证/地区限制判断 |
| Google Ads, Gambling and games | https://support.google.com/adspolicy/answer/15132179 | 支撑博彩、真钱游戏、社交赌场、抽奖和地区/年龄/认证限制 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑敏感兴趣、健康、金融困境、身份特征等个性化广告限制 |
| Google Ads, Housing, employment, and credit FAQ | https://support.google.com/adspolicy/answer/9997418 | 支撑美国/加拿大住房、就业、信贷类广告的定向限制和分类判断 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑敏感垂类中主体、价格、资质、官方身份和商业关系不得误导 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑敏感垂类落地页可达、原创内容、页面承诺和最终 URL 一致性 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑桥页、低价值 affiliate、arbitrage、cloaking 和审核规避风险 |
| Google Ads, Apply to advertise certain products and services | https://support.google.com/adspolicy/answer/16114090 | 支撑受限产品/服务的认证申请、账号资格和准入路径 |
| Google Ads Blog, Restricting third-party tech support ads | https://blog.google/products/ads/restricting-ads-third-party-tech-support-services/ | 支撑第三方 consumer tech support 的严格限制背景 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑 affiliate 推荐、评测、佣金关系和广告披露要求 |

## 39.1 CPL 垂类经济、资格问题与 Buyer Acceptance 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑贷款、债务、抵押、投资和金融 lead 的认证、地区、披露和禁投项 |
| Google Ads, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑医疗、药品、健康服务、远程医疗和认证/地区限制 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑健康、金融困境、身份、住房/就业/信贷等敏感状态不能被不当用于个性化定向 |
| Google Ads, Housing, employment, and credit FAQ | https://support.google.com/adspolicy/answer/9997418 | 支撑美国/加拿大 HEC 类广告的定向限制和分类判断 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑垂类页面不能误导价格、资格、官方关系、结果承诺和商业关系 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing page、final URL、页面可达性、原创内容和广告承诺一致 |
| Google Ads, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Lead Form 的隐私政策、字段收集、资格和广告政策要求 |
| Google Local Services Ads, Platform policies | https://support.google.com/localservices/answer/6224841 | 支撑本地服务 lead 的业务筛查、许可、服务范围和平台政策 |
| Google Local Services Ads, Lead costs and credits | https://support.google.com/localservices/answer/7436333 | 支撑本地服务 lead cost、charged lead、credit/dispute 和 wrong service/area 质量语境 |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation 生态、消费者信息流转和合规风险 |
| FTC, Staff Perspective: Follow the Lead | https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf | 支撑 lead marketplace、透明度、披露和消费者保护问题 |
| FTC, .com Disclosures | https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising | 支撑垂类 landing page 的关键限制、费用、商业关系和 claim 披露 |
| FTC, Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话 lead、seller/telemarketer、DNC、记录和 consent 治理 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑教育、B2B、金融等 email lead 后续联系的 opt-out 和商业邮件边界 |
| CFPB, Digital comparison-shopping circular | https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/ | 支撑金融产品比较、推荐排序、补偿驱动导流和消费者误导风险 |
| CFPB, Regulation V / FCRA | https://www.consumerfinance.gov/rules-policy/regulations/1022/ | 支撑信贷、保险、就业、住房等资格判断不能按普通营销 lead 简化处理 |
| Federal Student Aid, Avoid student loan debt relief scams | https://studentaid.gov/resources/scams | 支撑学生贷款减免、教育债务和冒充官方服务的风险判断 |
| ABA, Model Rule 7.1 | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communications_concerning_a_lawyers_services/ | 支撑法律服务广告不能做 false or misleading communication 的行业规则参考 |

## 39.2 Lead Pricing、Payout Negotiation 与结算安全垫来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation 生态、消费者信息流转、buyer handoff、透明度和投诉风险 |
| FTC, Staff Perspective: Follow the Lead | https://www.ftc.gov/system/files/documents/reports/staff-perspective-follow-lead/leadgenerationworkshop.pdf | 支撑 lead marketplace、数据转售、披露、消费者保护和监管背景 |
| FTC, .com Disclosures | https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising | 支撑价格、资格、限制、商业关系和 CTA 附近披露 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 lead PII 最小化、保留、删除、访问和供应商管理 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话 lead、seller/telemarketer、DNC、consent、记录保存和争议证据 |
| Google Ads, About conversion values | https://support.google.com/google-ads/answer/3419241 | 支撑 conversion value 应反映真实业务价值，不应使用虚高 headline payout |
| Google Ads, Determine a bid strategy based on your goals | https://support.google.com/google-ads/answer/2472725 | 支撑按 Maximize Conversions、Target CPA、Target ROAS 等目标选择出价策略 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把真实 qualified/approved/paid 结果导入 Google Ads，而不是优化到 submitted lead |
| Google Ads Help, About enhanced conversions for leads | https://support.google.com/google-ads/answer/11021502 | 支撑 lead 后续状态匹配需要同意、用户数据政策和安全处理 |
| Google Local Services Ads, Lead costs and credits | https://support.google.com/localservices/answer/7436333 | 支撑 charged lead、wrong service/area、credit 和 lead quality 语境 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑价格、资格、官方关系、服务结果和重要限制不能误导 |
| Google Ads Policy, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑金融 lead 的认证、披露、地区限制和禁投项 |
| Google Ads Policy, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑医疗/预约类 lead 的认证、地区和服务限制 |
| TUNE, Offer Payouts and Caps | https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps | 支撑 affiliate offer payout、cap、budget 和 tier 概念 |
| TUNE Dev Hub, OfferConversionCap | https://developers.tune.com/network-models/offerconversioncap/ | 支撑 offer/affiliate conversion cap、payout/revenue cap 的数据模型 |
| Everflow API, Get Offer | https://developers.everflow.io/docs/affiliate/offers/ | 支撑 offer status、payout、cap、targeting、affiliate status 和字段快照 |
| Voluum, Tracking Payouts | https://doc.voluum.com/en/tracking_payout.html | 支撑从 affiliate postback 接收动态 payout 和按实际 payout 对账 |
| Voluum, Conversion Status | https://doc.voluum.com/article/conversion-status | 支撑 pending、approved、rejected、payout 等 conversion status |
| Voluum, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、transaction_id、payout、status 等 postback 参数设计 |

## 40. 受众、再营销与 Customer Match 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About audience segments | https://support.google.com/google-ads/answer/2497941 | 支撑 affinity、in-market、detailed demographics、custom segments、your data segments 等受众类型 |
| Google Ads, About "Targeting" and "Observation" settings | https://support.google.com/google-ads/answer/7365594 | 支撑 targeting 会限制覆盖，observation 用于观察表现而不收窄流量 |
| Google Ads, Audience manager | https://support.google.com/google-ads/answer/7558048 | 支撑管理数据 segment、组合 segment、Customer Match 和排除名单的基础 |
| Google Ads, About Customer Match | https://support.google.com/google-ads/answer/6379332 | 支撑 Customer Match 是使用客户分享的数据触达或再触达客户 |
| Google Ads, Customer Match policy | https://support.google.com/google-ads/answer/6299717 | 支撑 Customer Match 对数据来源、同意、儿童数据、敏感兴趣和隐私披露的限制 |
| Google Ads, Customer matching process | https://support.google.com/google-ads/answer/7474263 | 支撑 Customer Match 的匹配、哈希和数据处理流程解释 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑 customer data、enhanced conversions、Customer Match 和用户提供数据政策 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑健康、金融困境、身份、关系困境等敏感类别的个性化广告限制 |
| Google Ads, Housing, employment, and credit FAQ | https://support.google.com/adspolicy/answer/9997418 | 支撑美国/加拿大住房、就业、信贷类广告的定向限制 |
| Google Ads, About audience signals for Performance Max campaigns | https://support.google.com/google-ads/answer/14530785 | 支撑 PMax audience signals 是给自动化系统的提示而非硬性定向 |
| Google Ads, About Performance Max campaigns | https://support.google.com/google-ads/answer/10724817 | 支撑 PMax 会跨 Google Ads 库存使用目标和素材自动优化 |
| Google Ads, About optimized targeting | https://support.google.com/google-ads/answer/10537509 | 支撑 optimized targeting 会在手动选择的信号之外寻找更多可能转化用户 |
| Google tag, Consent mode overview | https://developers.google.com/tag-platform/security/concepts/consent-mode | 支撑 consent 状态影响广告存储、用户数据和个性化广告 |

## 41. 预算节奏、扩量与止损来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Budgets overview | https://support.google.com/google-ads/answer/10486536 | 支撑平均日预算、预算管理和投放花费节奏 |
| Google Ads, About overdelivery and average daily budget | https://support.google.com/google-ads/answer/1704443 | 支撑平均日预算可能 overdelivery，需要平台外部硬止损 |
| Google Ads, Budget report | https://support.google.com/google-ads/answer/10702522 | 支撑通过预算报告理解每日花费、月度花费限制和预算变化影响 |
| Google Ads, Create an account budget | https://support.google.com/google-ads/answer/2375395 | 支撑通过 account budget 管理账号级预算约束 |
| Google Ads API, Account Budget | https://developers.google.com/google-ads/api/docs/billing/account-budgets | 支撑未来用官方 API 管理预算，不需要 Cookie 后台操作 |
| Google Ads, About ad scheduling | https://support.google.com/google-ads/answer/6372656 | 支撑 dayparting、按星期和小时控制广告展示 |
| Google Ads, About bid adjustments | https://support.google.com/google-ads/answer/2732132 | 支撑按设备、地点、时段等维度调整出价 |
| Google Ads, About location targeting | https://support.google.com/google-ads/answer/1722043 | 支撑 geo 分层、国家/地区/半径定位和本地预算控制 |
| Google Ads, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑回传延迟会影响短期 ROI 和扩量判断 |
| Google Ads, Time lag report | https://support.google.com/google-ads/answer/6239119 | 支撑分析从点击到转化的时间差，避免过早停量或扩量 |
| Google Ads, Experiments page | https://support.google.com/google-ads/answer/10682377 | 支撑通过实验控制变量测试预算、出价或结构变化 |
| Google Ads, About Performance Planner | https://support.google.com/google-ads/answer/9230124 | 支撑预算预测和计划工具只能作为输入，不能替代可收款 ROI |
| Google Ads, Conversion windows | https://support.google.com/google-ads/answer/3123169 | 支撑转化窗口会影响收入回传和判断周期 |

## 41.1 Portfolio 预算分配、风险集中度与组合治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, Budget report | https://support.google.com/google-ads/answer/10702522 | 支撑理解每日花费、月度花费限制和预算变化对组合节奏的影响 |
| Google Ads Help, About spending limits | https://support.google.com/google-ads/answer/10486637 | 支撑组合层面区分平均日预算、每日花费上限和月度花费上限 |
| Google Ads Help, Create an account budget | https://support.google.com/google-ads/answer/2375395 | 支撑账户预算和发票型客户的 spend cap 治理 |
| Google Ads API, Account budgets | https://developers.google.com/google-ads/api/docs/billing/account-budgets | 支撑未来以官方 API 保存 account budget 证据 |
| Google Ads Help, Performance Planner | https://support.google.com/google-ads/answer/9230124 | 支撑预算预测、不同 spend scenario 和 campaign planning |
| Google Ads Help, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑扩量前等待 conversion lag 和 revenue lag |
| Google Ads Help, Data discrepancies | https://support.google.com/google-ads/answer/7457111 | 支撑组合报表中不同系统数据差异的解释 |
| Google AdSense Help, Payment timelines | https://support.google.com/adsense/answer/7164703 | 支撑 AdSense/发布商收入到账延迟和 cash reserve 规划 |
| Google AdSense Help, Deductions from earnings FAQs | https://support.google.com/adsense/answer/2808531 | 支撑 finalized revenue 下调、deduction 和 paid ratio 风险 |
| Google AdSense Help, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑组合层面对 invalid traffic 和来源集中度设置上限 |

## 42. 广告创意 Claim 审核、事实核查和人审来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑广告创意不得虚假陈述主体、价格、服务、资质、官方关系、商业关系或结果 |
| Google Ads, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑广告文字、标点、大小写、符号、display URL 和 gimmicky wording 审核 |
| Google Ads, Text ad requirements | https://support.google.com/adspolicy/answer/6021630 | 支撑文字广告必须满足 Google Ads 标准政策和常见拒登要求 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑广告承诺和最终页面一致、页面可达、有原创价值且不是桥页 |
| Google Ads, Trademarks | https://support.google.com/adspolicy/answer/6118 | 支撑品牌、商标、竞品词和广告文字中授权关系判断 |
| Google Ads, Unacceptable business practices | https://support.google.com/adspolicy/answer/15938071 | 支撑冒充品牌、组织、公众人物或诱导用户交钱/交信息的严重风险判断 |
| Google Ads, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑健康、金融困境、身份特征等敏感类别在广告定向和表达中的限制 |
| Google Ads, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑金融、贷款、债务、投资等 offer 的披露、认证、地区限制和禁用承诺 |
| Google Ads, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑医疗、药品、健康服务和治疗结果声明的认证和地区限制 |
| Google Ads, About responsive search ads | https://support.google.com/google-ads/answer/7684791 | 支撑 RSA 多 headline/description 组合后仍需要逐条审查 claim |
| Google Ads, Keyword insertion | https://support.google.com/google-ads/answer/6371157 | 支撑动态关键词插入可能带来语法、敏感词、品牌词和不实承诺风险 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑推荐、评测、背书、评价和商业关系披露要求 |
| FTC, Endorsements, influencers, and reviews | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | 支撑评价、达人推荐、商业关系披露和消费者误导风险判断 |

## 43. Google Ads 报表诊断、Search Terms 与 Change History 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About the search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑真实 search term、keyword/match type、否定词和 query intent 复盘 |
| Google Ads, About search terms insights | https://support.google.com/google-ads/answer/11386930 | 支撑聚合查询主题、PMax/broad 扩展和用户意图诊断 |
| Google Ads, Use auction insights to compare performance | https://support.google.com/google-ads/answer/2579754 | 支撑 impression share、overlap、position above、top of page 和 outranking 竞争诊断 |
| Google Ads, About change history | https://support.google.com/google-ads/answer/19888 | 支撑预算、出价、素材、URL、转化和 recommendation 改动复盘 |
| Google Ads, Create custom reports in Report Editor | https://support.google.com/google-ads/answer/7489070 | 支撑保存、下载和分段报表，用于证据归档 |
| Google Ads, Measure your results | https://support.google.com/google-ads/answer/6172626 | 支撑基本效果衡量和报表复盘框架 |
| Google Ads, Evaluate the performance of your landing pages | https://support.google.com/google-ads/answer/7543502 | 支撑 landing page、expanded URL、移动端和页面表现诊断 |
| Google Ads, Campaign level asset reporting for responsive search ads | https://support.google.com/google-ads/answer/9781208 | 支撑 RSA headline/description asset 表现复盘 |
| Google Ads, Find your bid strategy reports | https://support.google.com/google-ads/answer/7074568 | 支撑自动出价学习、状态和组合策略报表定位 |
| Google Ads, Evaluate automated bid strategy performance | https://support.google.com/google-ads/answer/10167267 | 支撑 Smart Bidding 目标、学习、conversion lag 和表现评估 |
| Google Ads, Evaluate Performance Max results | https://support.google.com/google-ads/answer/16279166 | 支撑 PMax 结果、渠道和自动化投放复盘 |
| Google Ads, About the Insights page | https://support.google.com/google-ads/answer/10256472 | 支撑趋势、需求变化和市场洞察作为诊断输入 |

## 44. Geo、语言、本地化、时区与币种分层来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Target ads to geographic locations | https://support.google.com/google-ads/answer/1722043 | 支撑国家、地区、城市、半径和位置组定位 |
| Google Ads, About advanced location options | https://support.google.com/google-ads/answer/1722038 | 支撑 presence、interest 和目标地实际用户/兴趣用户边界 |
| Google Ads, About language targeting | https://support.google.com/google-ads/answer/1722078 | 支撑语言定向不是自动翻译，需与页面本地化一起判断 |
| Google Ads, Measuring geographic performance | https://support.google.com/google-ads/answer/2453994 | 支撑按地理位置查看表现、定位 bad geo 和扩国家机会 |
| Google Ads, About device targeting | https://support.google.com/google-ads/answer/1722028 | 支撑按设备评估展示、点击、转化和页面体验差异 |
| Google Ads, About bid adjustments | https://support.google.com/google-ads/answer/2732132 | 支撑地点、设备、时段等 bid adjustment 与利润分层 |
| Google Ads, Add or remove a bid adjustment | https://support.google.com/google-ads/answer/6262954 | 支撑出价调整的操作边界和不同 campaign 类型限制 |
| Google Ads, About ad scheduling | https://support.google.com/google-ads/answer/6372656 | 支撑 dayparting、星期/小时投放和时区复盘 |
| Google Ads, Language, number format, time zone, and currency settings | https://support.google.com/google-ads/answer/9842104 | 支撑账号语言、数字格式、时区和币种设置的账号级影响 |
| Google Ads, About payment settings | https://support.google.com/google-ads/answer/2375432 | 支撑账单国家、付款方式和账号币种对现金流的影响 |
| Google Ads, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑回传延迟和跨日 ROI 判断 |
| Google Ads, Time lag report | https://support.google.com/google-ads/answer/6239119 | 支撑从点击到转化的时差，避免 dayparting 和日报误判 |

## 45. AdSense 站点审核、Policy Center 与广告投放限制来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| AdSense, Connect your site to AdSense | https://support.google.com/adsense/answer/7584263 | 支撑站点连接方式、代码/ads.txt/meta 和审核前置条件 |
| AdSense, Add a new site to your sites list | https://support.google.com/adsense/answer/12169212 | 支撑添加站点、sites list 和 review 流程 |
| AdSense, Make sure your site's pages are ready for AdSense | https://support.google.com/adsense/answer/7299563 | 支撑站点 ready、内容、导航和可访问性检查 |
| AdSense, Policy Center overview | https://support.google.com/adsense/answer/9485926 | 支撑集中查看影响广告服务的问题和修复状态 |
| AdSense, Policy issues and ad serving statuses | https://support.google.com/adsense/answer/15689616 | 支撑 policy issue、regulatory issue、advertiser preference 和 ad serving status 区分 |
| AdSense, Fix policy issues that affect ad serving | https://support.google.com/adsense/answer/7003627 | 支撑修复问题、request review 和 review status |
| AdSense, Ad serving limits | https://support.google.com/adsense/answer/9437976 | 支撑账号评估、invalid traffic concerns 和广告服务限制响应 |
| AdSense, Limited ad serving vs limited ads | https://support.google.com/adsense/answer/14668281 | 支撑 ad serving limited 与 limited ads 的区别 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑发布商内容、广告行为和流量质量基础政策 |
| Google Publisher Policies | https://support.google.com/adsense/answer/9335564 | 支撑发布商内容和行为政策边界 |
| AdSense, Traffic provider checklist | https://support.google.com/adsense/answer/3332805 | 支撑购买流量供应商尽调和来源责任 |
| AdSense, Set up a traffic segmentation plan | https://support.google.com/adsense/answer/2583698 | 支撑按来源隔离流量和排查无效流量 |
| AdSense, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑发布商对购买流量质量负责 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑无效流量、扣量和广告服务限制风险 |

## 46. 发布商广告质量、阻止控制与品牌安全来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| AdSense, Guide to allow and block ads on your site | https://support.google.com/adsense/answer/180609 | 支撑广告阻止控制、收入权衡和站点级广告质量管理 |
| AdSense, Block sensitive categories | https://support.google.com/adsense/answer/164131 | 支撑敏感分类阻止、品牌安全和用户体验控制 |
| AdSense, Allow and block ads | https://support.google.com/adsense/topic/1727182 | 支撑 blocking controls 入口和可阻止对象范围 |
| AdSense, Ad review center | https://support.google.com/adsense/answer/2469354 | 支撑查看、允许、阻止和报告具体广告 |
| AdSense, Blocking controls by site | https://support.google.com/adsense/answer/12169214 | 支撑按站点管理阻止控制和多站点差异 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑广告行为、无效点击和发布商基础政策 |
| Google Publisher Policies | https://support.google.com/adsense/answer/9335564 | 支撑发布商内容和广告生态政策边界 |
| Google Publisher Restrictions | https://support.google.com/adsense/answer/10437795 | 支撑受限内容可能降低广告需求但不一定违规 |
| AdSense, Policy Center overview | https://support.google.com/adsense/answer/9485926 | 支撑广告质量问题和 Policy Center 关联复盘 |
| AdSense, Invalid traffic | https://support.google.com/adsense/answer/16737 | 支撑误点、诱导点击和无效互动风险 |
| Google Ad Manager, Ad review center | https://admanager.google.com/home/resources/feature-brief-ad-review-center/ | 支撑 GAM 中审查广告创意和需求内容 |
| Google Ad Manager, Brand safety capabilities | https://admanager.google.com/home/capabilities/brand-safety/ | 支撑 GAM 品牌安全、广告质量和阻止能力背景 |

## 47. Performance Max / Demand Gen 自动化流量来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About Performance Max campaigns | https://support.google.com/google-ads/answer/10724817 | 支撑 PMax 会跨 Google inventory 使用目标、素材、页面和转化信号自动优化 |
| Google Ads, Evaluate Performance Max results | https://support.google.com/google-ads/answer/16279166 | 支撑 PMax 结果评估、诊断和自动化流量复盘 |
| Google Ads, Channel performance report for Performance Max | https://support.google.com/google-ads/answer/16260130 | 支撑按 Search、YouTube、Discover、Gmail 等 channel 拆分 PMax 表现 |
| Google Ads, About Performance Max channels | https://support.google.com/google-ads/answer/16683501 | 支撑理解 PMax 各 channel 的库存和报告边界 |
| Google Ads, About Final URL expansion | https://support.google.com/google-ads/answer/16672777 | 支撑 Final URL expansion、URL exclusions、page feed 和 landing page 控制 |
| Google Ads, Search targeting and controls for PMax | https://support.google.com/google-ads/answer/16672776 | 支撑 Search themes、negative keywords、brand exclusions 和 query 控制边界 |
| Google Ads, Search themes with PMax | https://support.google.com/google-ads/answer/14767319 | 支撑 Search themes 是给 PMax 的搜索主题提示，不等同于关键词硬匹配 |
| Google Ads, Set up asset group and assets | https://support.google.com/google-ads/answer/15864535 | 支撑 asset group、素材组合、素材质量和 claim 审核 |
| Google Ads, Audience signals for PMax | https://support.google.com/google-ads/answer/14530785 | 支撑 audience signals 是自动化学习提示，不是硬性定向 |
| Google Ads, About Demand Gen campaigns | https://support.google.com/adwords/answer/6105478 | 支撑 Demand Gen 在视觉/内容消费场景中的触达边界 |
| Google Ads, Demand Gen audiences overview | https://support.google.com/google-ads/answer/15594567 | 支撑 Demand Gen 受众、优化和素材测试复盘 |
| Google Ads, About optimized targeting | https://support.google.com/google-ads/answer/10537509 | 支撑 optimized targeting 会在已选受众外扩展，需用后端收入校验 |

## 48. Search 自动化流量来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About AI Max for Search campaigns | https://support.google.com/google-ads/answer/15910187 | 支撑 AI Max 在 Search campaign 中扩展匹配、资产和 URL 的自动化边界 |
| Google Ads, Set up AI Max in Search campaigns | https://support.google.com/google-ads/answer/15909989 | 支撑 AI Max 设置、控制项和上线前审计 |
| Google Ads, FAQs about AI Max for Search campaigns | https://support.google.com/google-ads/answer/15913066 | 支撑 AI Max 常见问题、报表和控制理解 |
| Google Ads, Final URL expansion in Search campaigns | https://support.google.com/google-ads/answer/16230205 | 支撑 Search campaign 中 Final URL expansion、URL 控制和页面范围风险 |
| Google Ads, Search targeting and controls | https://support.google.com/google-ads/answer/16672776 | 支撑 search terms、negative keywords、brand controls 和 URL 控制 |
| Google Ads, About broad match | https://support.google.com/google-ads/answer/2407779 | 支撑 broad match 会扩大搜索意图覆盖，需要 query 和后端收入复盘 |
| Google Ads, Use broad match with Smart Bidding | https://support.google.com/google-ads/answer/12159290 | 支撑 broad match 与 Smart Bidding 组合时的目标信号风险 |
| Google Ads, About Smart Bidding | https://support.google.com/google-ads/answer/7065882 | 支撑自动出价依赖 conversion / value 质量 |
| Google Ads, About Dynamic Search Ads | https://support.google.com/google-ads/answer/2471185 | 支撑 DSA 基于网站内容匹配 query 和生成标题的边界 |
| Google Ads, Automatically created assets | https://support.google.com/google-ads/answer/11259373 | 支撑自动生成资产需要 claim 审核和人工放行 |
| Google Ads, About the search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑 search term、match type、query intent 和 negative keywords 诊断 |
| Google Ads, About negative keywords | https://support.google.com/google-ads/answer/2453972 | 支撑低质 query、品牌/敏感词和无关流量排除 |
| Google Ads, Landing page performance | https://support.google.com/google-ads/answer/7543502 | 支撑 expanded URL、landing page 和移动端表现诊断 |
| Google Ads, Change history | https://support.google.com/google-ads/answer/19888 | 支撑谁开启 AI Max、broad、DSA、URL expansion 或自动资产的事故复盘 |

## 49. 域名、站点资产与站群治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Search Central, Spam policies | https://developers.google.com/search/docs/essentials/spam-policies | 支撑 expired domain abuse、site reputation abuse、cloaking、scaled content 和低质 affiliate 风险 |
| Google Search Central, Site move with URL changes | https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes | 支撑正常站点迁移、301、监控和迁移计划边界 |
| Google Search Central, Creating helpful content | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | 支撑域名/站点不能只承载低质广告或跳转内容 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、页面可访问、广告承诺一致、桥页/低价值目的地风险 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑 arbitrage、bridge/gateway、低价值目的地和广告网络滥用风险 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑换域名、隐藏目的地、cloaking、多账号或多站点规避政策执行风险 |
| Google Ads, Parked domain site | https://support.google.com/google-ads/answer/50002 | 支撑 parked domain 库存和广告主排除语境 |
| AdSense, Add a new site to your sites list | https://support.google.com/adsense/answer/12169212 | 支撑 AdSense Sites list、添加站点和审核流程 |
| AdSense, Connect your site to AdSense | https://support.google.com/adsense/answer/7584263 | 支撑站点所有权/连接方式和审核前置条件 |
| AdSense, Make sure your site's pages are ready | https://support.google.com/adsense/answer/7299563 | 支撑站点内容、导航、可访问性和 ready 检查 |
| AdSense, Create an ads.txt file | https://support.google.com/adsense/answer/7532444 | 支撑发布商站点授权卖方声明和 ads.txt 治理 |
| AdSense, Program policies | https://support.google.com/adsense/answer/48182 | 支撑发布商广告行为、流量质量和站点合规基础政策 |
| AdSense, If you want to purchase traffic to your site | https://support.google.com/adsense/answer/1348722 | 支撑购买流量时发布商对流量质量负责 |
| Google Publisher Policies | https://support.google.com/publisherpolicies/answer/10437486 | 支撑发布商内容、行为和广告生态边界 |

## 50. 账号、MCC、付款与 Advertiser Verification 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About manager accounts | https://support.google.com/google-ads/answer/6139186 | 支撑 MCC / manager account 是集中管理账号的治理工具，不是账号池 |
| Google Ads, Create a manager account | https://support.google.com/google-ads/answer/7459399 | 支撑 manager account 创建和管理边界 |
| Google Ads, Manager account access levels | https://support.google.com/google-ads/answer/9977851 | 支撑 MCC 中用户访问级别和权限治理 |
| Google Ads, About access levels in your account | https://support.google.com/google-ads/answer/9978556 | 支撑广告账号内 Admin、Standard、Billing、Read only 等权限边界 |
| Google Ads, Manage access to your account | https://support.google.com/google-ads/answer/6372672 | 支撑邀请、移除用户和权限变更审计 |
| Google Ads, About payment settings | https://support.google.com/google-ads/answer/2375432 | 支撑自动付款、手动付款、月结发票和账单国家/币种风险 |
| Google Ads, Payments profile link types | https://support.google.com/google-ads/answer/15758513 | 支撑 payments profile 和 Google Ads 账号之间的付款关系治理 |
| Google Ads, Create an account budget | https://support.google.com/google-ads/answer/2375395 | 支撑 account budget 作为账号级预算控制 |
| Google Ads, Secure your Google Ads account | https://support.google.com/google-ads/answer/2375456 | 支撑不共享登录态、启用安全检查和访问审计 |
| Google Ads, Advertiser verification | https://support.google.com/adspolicy/answer/9703665 | 支撑广告主身份、业务操作和披露验证 |
| Google Ads, Tasks required for Advertiser verification | https://support.google.com/adspolicy/answer/15577076 | 支撑验证任务、资料准备和业务真实性说明 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑多账号滥用、封禁后换号和规避政策执行风险 |

## 51. Native、Advertorial 与 Presell Page 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| FTC, Native Advertising: A Guide for Businesses | https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses | 支撑 native / advertorial 广告性质需要清楚、显著披露 |
| FTC, Enforcement Policy Statement on Deceptively Formatted Advertisements | https://www.ftc.gov/legal-library/browse/commission-policy-statement-enforcement-policy-statement-deceptively-formatted-advertisements | 支撑伪装成新闻、评测或独立内容的广告格式风险 |
| FTC, Disclosures 101 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | 支撑披露应清楚、明显、靠近推荐或 CTA |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑评价、背书、商业关系、佣金和赞助披露 |
| eCFR, Endorsements and Testimonials in Advertising | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 | 支撑 endorsement/testimonial 广告规则文本 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑主体、价格、商业关系、官方关系和结果承诺不得误导 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 presell page 不能是低价值桥页，广告承诺和目的地要一致 |
| Google Ads, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑标题、标点、大小写、gimmicky wording 和素材质量审核 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑 bridge/gateway、低价值 affiliate 和 arbitrage 风险 |
| Google Publisher Policies | https://support.google.com/publisherpolicies/answer/10437486 | 支撑发布商内容、广告体验和流量质量边界 |
| Taboola Advertising Policies | https://www.taboola.com/policies/advertising-policies | 支撑 Native 平台对误导、敏感内容、素材和落地页的要求 |
| Outbrain Advertising Guidelines | https://www.outbrain.com/guidelines/advertising-guidelines/ | 支撑 Native 平台广告格式、误导素材和落地页质量要求 |

## 52. Lead Form、电话线索、Call Tracking 与 TCPA 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Google Ads Lead Form 的资格、隐私政策、收集信息和广告政策要求 |
| Google Ads, Create lead form assets | https://support.google.com/google-ads/answer/9423235 | 支撑 Lead Form 创建、表单字段、问题、隐私 URL 和线索交接 QA |
| Google Ads, About call assets | https://support.google.com/google-ads/answer/2453991 | 支撑 call assets、电话号码、展示和电话入口治理 |
| Google Ads, About call ads | https://support.google.com/google-ads/answer/6341403 | 支撑 call ads 迁移、电话广告格式和电话资产组合治理 |
| Google Ads, About call reporting | https://support.google.com/google-ads/answer/2454052 | 支撑 Google forwarding numbers、通话指标、通话转化和 call duration 阈值 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户提供数据、customer data、consent、隐私披露和数据处理要求 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑把真实、合规、可证明的线下/CRM 状态回传给广告优化 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑 telemarketing、seller、consent、DNC 和记录保存治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和 telemarketer/seller 合规语境 |
| FCC, TCPA one-to-one consent rule deletion order | https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf | 支撑 2025 年 one-to-one consent 规则状态变化需按最新 FCC/eCFR/法律意见更新 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑 TCPA 电话、自动拨号、预录音、短信和 prior express consent 的规则文本 |
| eCFR, 16 CFR 310.5 Recordkeeping requirements | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5 | 支撑 TSR 记录保存、证明链和审计留存要求 |

## 52.0.0 Call Tracking Number Pool、DNI 与电话归因来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About call assets | https://support.google.com/google-ads/answer/2453991 | 支撑 call asset、电话号码、广告内电话入口和主体一致性治理 |
| Google Ads Help, About call reporting | https://support.google.com/google-ads/answer/2454052 | 支撑 Google forwarding numbers、通话指标、来电时间和 call duration |
| Google Ads Help, Phone call conversion tracking | https://support.google.com/google-ads/answer/6100664 | 支撑 call conversion、duration threshold 和 qualified call 口径 |
| Google Ads Help, Measure calls you receive | https://support.google.com/google-ads/answer/6197479 | 支撑网站电话来电、call conversion tracking 和 Google forwarding number 语境 |
| Google Ads Help, About call campaigns | https://support.google.com/google-ads/answer/7159344 | 支撑 call-heavy campaign、电话入口和 RSA/call asset 迁移治理 |
| Google Ads API, CallAsset | https://developers.google.com/google-ads/api/reference/rpc/v21/CallAsset | 支撑 call asset 字段、电话资产和 API 审计方向 |
| Google Ads API, call_view fields | https://developers.google.com/google-ads/api/fields/v18/call_view | 支撑 call detail / call view 报表字段、call start 和 duration 诊断 |
| Google Ads API, Conversion action categories | https://developers.google.com/google-ads/api/docs/conversions/categories | 支撑 phone call、lead、qualified lead 等 conversion category 映射 |
| Google Analytics Help, Avoid sending PII | https://support.google.com/analytics/answer/6366371 | 支撑 caller phone、号码、URL、日志和 analytics 字段的 PII 边界 |
| Google Ads Policy, Data collection and use | https://support.google.com/adspolicy/answer/6020956 | 支撑电话 lead 页面、个人信息收集、披露和安全处理要求 |
| CallRail Help, Dynamic number insertion overview | https://support.callrail.com/hc/en-us/articles/5711814948877-Dynamic-number-insertion-overview | 支撑 DNI、tracking number、swap 和来源归因的行业实现语境 |
| CallRail Help, Visitor tracking basics | https://support.callrail.com/hc/en-us/articles/5712712532109-Visitor-tracking-basics | 支撑 visitor/session 级电话归因和号码分配语境 |
| CallRail Help, Create a website pool | https://support.callrail.com/hc/en-us/articles/5711655270029-Create-a-website-pool | 支撑 website pool、号码池容量和池化配置语境 |
| Twilio, What is Dynamic Number Insertion | https://www.twilio.com/docs/glossary/what-is-dynamic-number-insertion | 支撑 DNI 术语和号码替换原理背景 |
| Twilio, Call Attribution | https://www.twilio.com/docs/glossary/what-is-call-attribution | 支撑 call attribution 术语和归因语境 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、DNC、consent、记录和投诉治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和停止联系流程 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 call log、recording、caller ID 和 PII 最小化治理 |
| NIST SP 800-122 | https://csrc.nist.gov/pubs/sp/800/122/final | 支撑 caller PII、hash、访问控制和保留策略 |

## 52.0.0.1 Pay-per-call、Call Buyer Routing 与 Duration Payout 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About call assets | https://support.google.com/google-ads/answer/2453991 | 支撑 call asset、电话入口和 call-heavy campaign 基础 |
| Google Ads Help, About call reporting | https://support.google.com/google-ads/answer/2454052 | 支撑 Google forwarding numbers、通话指标、call duration 和 call status |
| Google Ads Help, Phone call conversion tracking | https://support.google.com/google-ads/answer/6100664 | 支撑 duration threshold、call conversion 和 qualified call 口径 |
| Google Ads API, call_view fields | https://developers.google.com/google-ads/api/fields/v18/call_view | 支撑 call detail 报表字段、call start、duration、status 和归因对账 |
| Google Ads API, Conversion action categories | https://developers.google.com/google-ads/api/docs/conversions/categories | 支撑 phone call、lead、qualified lead 等 conversion category 映射 |
| Ringba Support, Call Flows with Ringba | https://support.ringba.com/hc/en-us/articles/17989801271703-Call-Flows-with-Ringba | 支撑 call flow、IVR、routing node 和电话路由行业语境 |
| Ringba Support, Campaigns | https://support.ringba.com/hc/en-us/articles/17882602101783-Campaigns-Video | 支撑 pay-per-call campaign、publisher/source 和 buyer routing 语境 |
| Ringba Support, Targets | https://support.ringba.com/hc/en-us/articles/17882949857943-Targets-Video | 支撑 target、buyer endpoint、电话转接和路由目的地语境 |
| Ringba Support, Call Details Report Events Reference | https://support.ringba.com/hc/en-us/articles/33636912201751-Call-Details-Report-Events-Reference | 支撑 call detail event、call lifecycle 和 disposition 对账语境 |
| Retreaver, Pay Per Call Campaign Roadmap | https://retreaver.com/call-tracking/pay-per-call | 支撑 pay-per-call campaign、buyer、publisher 和电话营销基础语境 |
| Retreaver, Introduction | https://learn.retreaver.com/guides/introduction | 支撑 Retreaver 作为 performance marketing call platform 的基本对象 |
| Retreaver, Pay-Per-Call Features | https://learn.retreaver.com/guides/retreaver-pay-per-call-features-to-optimize-your-conversion-performance | 支撑 buyer、routing、number pool、RTB 和 performance optimization 行业语境 |
| Invoca, Call Routing Software | https://www.invoca.com/product/call-routing | 支撑 call routing、routing rules 和 buyer/agent 分配语境 |
| CallRail Help, Dynamic number insertion overview | https://support.callrail.com/hc/en-us/articles/5711814948877-Dynamic-number-insertion-overview | 支撑 DNI、tracking number 和 call source 归因基础 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、DNC、consent、记录保存和投诉治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和停止联系流程 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 call log、caller ID、recording 和 PII 最小化治理 |

## 52.0.1 Lead Consent Proof、TrustedForm / Jornaya 与证据链来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| ActiveProspect, TrustedForm | https://activeprospect.com/products/trustedform/ | 支撑 TrustedForm 类 consent certificate、lead proof 和页面上下文证据 |
| ActiveProspect, Jornaya TCPA Guardian LeadConduit integration | https://activeprospect.com/leadconduit/integrations/jornaya/tcpa_guardian/ | 支撑 Jornaya / TCPA Guardian 类 lead evidence、integration 和 buyer workflow 语境 |
| Verisk, Publisher Guidelines for TCPA Guardian Enhancements | https://marketing.verisk.com/wp-content/uploads/2024/09/Publisher-Guidelines-for-TCPA-Guardian-Enhancements.pdf | 支撑 TCPA Guardian single seller、publisher guideline 和 consent evidence 语境 |
| Verisk, TCPA Guardian Update | https://marketing.verisk.com/wp-content/uploads/2024/12/TCPA-Guardian-Update-New-Single-Seller-and-Select-All-Features.pdf | 支撑 single seller / select all 等 consent workflow 变化需要来源日期管理 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Google Ads Lead Form 的资格、隐私政策和字段收集要求 |
| Google Ads Policy, Data collection and use | https://support.google.com/adspolicy/answer/6020956 | 支撑个人信息收集、披露、用途、隐私和安全处理要求 |
| Google Ads Help, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑 customer data、用户提供数据、consent、隐私披露和分享要求 |
| Google Analytics Help, Avoid sending PII | https://support.google.com/analytics/answer/6366371 | 支撑 URL、日志、analytics、subid 和报表不应携带 PII |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑 telemarketing、seller/telemarketer、DNC、consent、记录和投诉治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和停止联系流程 |
| FTC, Q&A for Telemarketers & Sellers About DNC | https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0 | 支撑 entity-specific DNC、opt-out、suppression 和联系频控 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 lead PII 的最小化、保留、访问控制和安全处理 |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation 信息流转、透明度、披露和消费者投诉背景 |
| FCC, TCPA one-to-one consent rule court response / deletion order | https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf | 支撑 lead generator consent 规则状态要按日期、来源和法律意见管理 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| eCFR, 16 CFR 310.5 Recordkeeping requirements | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5 | 支撑 TSR 记录保存、证明链和审计留存要求 |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑真实、合规、可证明的 CRM / buyer 状态回传，而不是伪造转化 |
| NIST SP 800-122 | https://csrc.nist.gov/pubs/sp/800/122/final | 支撑 PII 识别、最小化、风险分级和访问控制设计 |

## 52.0.2 Lead Freshness、Aged Lead 与 Recontact Window 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Lead Form、隐私政策、字段收集和线索下载语境 |
| Google Ads API, LeadFormAsset | https://developers.google.com/google-ads/api/reference/rpc/v19/LeadFormAsset | 支撑 lead form asset、delivery method 和表单资产字段的官方 API 语境 |
| Google Ads Help, About call reporting | https://support.google.com/google-ads/answer/2454052 | 支撑 call reporting、来电时间、call duration 和 freshness/contact 诊断 |
| Google Ads Help, Phone call conversion tracking | https://support.google.com/google-ads/answer/6100664 | 支撑 phone call conversion、qualified call 和通话转化口径 |
| Google Ads Help, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 lead age 和 paid/qualified feedback 不能只看当天 conversions |
| Google Ads Help, About data freshness | https://support.google.com/google-ads/answer/2544985 | 支撑报表 freshness 和导入判断窗口，不把未成熟数据当最终收入 |
| Google Ads Policy, Data collection and use | https://support.google.com/adspolicy/answer/6020956 | 支撑个人信息收集、披露、用途、隐私和安全处理要求 |
| Google Analytics Help, Avoid sending PII | https://support.google.com/analytics/answer/6366371 | 支撑 URL、subid、日志和 analytics 字段不应携带 PII |
| ActiveProspect, TrustedForm | https://activeprospect.com/products/trustedform/ | 支撑 lead freshness 争议中的 consent certificate 和页面上下文证据 |
| ActiveProspect, Jornaya TCPA Guardian LeadConduit integration | https://activeprospect.com/leadconduit/integrations/jornaya/tcpa_guardian/ | 支撑 Jornaya / TCPA Guardian 类证据和 buyer workflow 语境 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑 recontact、DNC、seller/telemarketer、consent、记录和投诉治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和停止联系流程 |
| FTC, Q&A for Telemarketers & Sellers About DNC | https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0 | 支撑 entity-specific DNC、opt-out、suppression 和联系频控 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑邮件 recontact、退订和商业邮件边界 |
| FCC, TCPA one-to-one consent rule court response / deletion order | https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf | 支撑 lead generator consent 规则状态要按日期和法律意见管理 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| eCFR, 16 CFR 310.5 Recordkeeping requirements | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5 | 支撑 TSR 记录保存、证明链和审计留存要求 |
| NIST SP 800-122 | https://csrc.nist.gov/pubs/sp/800/122/final | 支撑 lead PII、保留、访问控制和风险分级设计 |
| Aged Lead Sales, TCPA compliance for aged leads | https://agedleadsales.com/blog/tcpa-compliance-calling-aged-leads | 仅作为 aged lead 行业语境参考，不作为合规判断依据 |
| InsureLeads, Aged Lead glossary | https://www.getinsureleads.com/glossary/aged-lead | 仅作为 aged lead 术语背景，不作为合规判断依据 |

## 52.1 Speed-to-Lead、联系策略、坐席容量与 SLA 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About call assets | https://support.google.com/google-ads/answer/2453991 | 支撑 call asset、电话入口、call-heavy campaign 和电话资产治理 |
| Google Ads, About call reporting | https://support.google.com/google-ads/answer/2454052 | 支撑 Google forwarding numbers、通话指标、来电时间、call duration 和电话转化诊断 |
| Google Ads, Phone call conversion tracking | https://support.google.com/google-ads/answer/6100664 | 支撑 call conversion、call duration threshold 和电话转化口径 |
| Google Ads, Create call ads | https://support.google.com/google-ads/answer/6341403 | 支撑电话广告格式、迁移和电话入口治理背景 |
| Google Ads, Local Services Ads platform policies | https://support.google.com/localservices/answer/6224841 | 支撑本地服务 lead 的服务范围、平台政策、商家质量和联系边界 |
| Google Ads, Lead costs and credits in Local Services Ads | https://support.google.com/localservices/answer/7436333 | 支撑本地服务 charged lead、credit、wrong service/area 和 lead quality 语境 |
| Google Ads, About ad scheduling | https://support.google.com/google-ads/answer/2404244 | 支撑按营业时间、坐席容量和时区做广告排期 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑电话/表单 lead 数据、同意、披露、分享和隐私要求 |
| FTC, Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话销售、seller/telemarketer、DNC、consent、记录和投诉治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和停止联系流程 |
| FTC, Q&A for Telemarketers & Sellers About DNC | https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0 | 支撑 entity-specific DNC、opt-out、suppression 和联系频控 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑邮件 follow-up、退订和商业邮件边界 |
| FCC, TCPA one-to-one consent rule court response / deletion order | https://docs.fcc.gov/public/attachments/DA-25-621A1.pdf | 支撑 TCPA lead consent 规则状态需要按来源日期管理 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| eCFR, 16 CFR 310.5 Recordkeeping requirements | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.5 | 支撑电话销售、consent、交易和联系记录保存 |

## 52.1.1 Buyer Capacity、Cap Pacing 与 Dayparting 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, Set up an ad schedule | https://support.google.com/google-ads/answer/6372656 | 支撑 ad schedule / dayparting 按星期和小时控制广告展示 |
| Google Ads Help, About ad scheduling | https://support.google.com/google-ads/answer/2404244 | 支撑 call-heavy campaign、营业时间和广告排期语境 |
| Google Ads Help, About overdelivery and average daily budget | https://support.google.com/google-ads/answer/1704443 | 支撑平均日预算可能 overdelivery，需要平台外 hard stop |
| Google Ads Help, Budgets overview | https://support.google.com/google-ads/answer/10486536 | 支撑预算节奏、平均日预算和投放花费管理 |
| Google Ads Help, Budget report | https://support.google.com/google-ads/answer/10702522 | 支撑预算报告、每日/月度花费和 pacing 复盘 |
| Google Ads Help, About bid adjustments | https://support.google.com/google-ads/answer/2732132 | 支撑按设备、地点、时段等维度调节出价 |
| Google Ads Help, About location targeting | https://support.google.com/google-ads/answer/1722043 | 支撑 geo、用户位置和本地 buyer capacity 的匹配 |
| Google Ads Help, About call assets | https://support.google.com/google-ads/answer/2453991 | 支撑电话入口、call asset 和营业时间治理 |
| Google Ads Help, About call reporting | https://support.google.com/google-ads/answer/2454052 | 支撑 call reporting、来电时间、call duration 和 missed call 诊断 |
| Google Ads Help, Phone call conversion tracking | https://support.google.com/google-ads/answer/6100664 | 支撑 call conversion、qualified call 和通话转化口径 |
| Google Ads Help, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 dayparting 不能只看当天 conversions，要考虑 lag |
| Google Ads Help, Time lag report | https://support.google.com/google-ads/answer/6239119 | 支撑从点击到转化的时差，避免时段误判 |
| Google Local Services Ads, Platform policies | https://support.google.com/localservices/answer/6224841 | 支撑本地服务 lead 的服务范围、平台政策和商家质量 |
| Google Local Services Ads, How leads work | https://support.google.com/localservices/answer/7195435 | 支撑 valid lead、charged lead、service area、预算和 lead quality 语境 |
| Google Ads API, Account budgets | https://developers.google.com/google-ads/api/docs/billing/account-budgets | 支撑官方 API account budget 方向，不需要 Cookie 后台操作 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑 telemarketing、seller/telemarketer、DNC、consent、记录和投诉治理 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑 DNC 查询、订阅和停止联系流程 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |

## 52.1.2 Appointment Lead、Booking、Show Rate 与 No-show 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Calendar Help, Create an appointment schedule | https://support.google.com/calendar/answer/10729749 | 支撑 appointment schedule、booking page、availability 和日历预约语境 |
| Google Calendar Help, Learn about appointment schedules | https://support.google.com/calendar/answer/11608416 | 支撑 appointment schedules、可预约时段、预约页和提醒语境 |
| Google Business Profile Help, Set up bookings through a provider | https://support.google.com/business/answer/7475773 | 支撑商家预约 provider、Reserve with Google 和 buyer booking handoff |
| Reserve with Google | https://www.google.com/maps/reserve/ | 支撑用户通过 Google 发现和预约本地服务的公开产品语境 |
| Google Local Services Help | https://support.google.com/localservices/ | 支撑 Local Services lead、service area、预算和本地服务预约语境 |
| Google Local Services Ads, How leads work | https://support.google.com/localservices/answer/7195435 | 支撑 valid lead、charged lead、service area、预算和 lead quality |
| Google Ads Help, Set up an ad schedule | https://support.google.com/google-ads/answer/6372656 | 支撑广告排期要和 buyer hours、calendar capacity 和 slot availability 对齐 |
| Google Ads Help, About call reporting | https://support.google.com/google-ads/answer/2454052 | 支撑 call reporting、来电时间、call duration 和 appointment funnel 诊断 |
| Google Ads Help, Phone call conversion tracking | https://support.google.com/google-ads/answer/6100664 | 支撑 qualified call 和 booked appointment 前置转化口径 |
| Google Ads Help, Conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 booked、showed、paid 有延迟，不能只看当天 conversions |
| Google Ads API, Upload offline conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-offline | 支撑 showed / paid 等真实线下状态回传 |
| Google Ads API, Upload conversion adjustments | https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments | 支撑 no-show、cancel、return 或 value 错误后的调整治理 |
| Google Ads Help, Offline conversion import discrepancies and errors | https://support.google.com/google-ads/answer/13321563 | 支撑 offline import QA、匹配率、错误和诊断 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话确认、提醒、DNC、consent 和记录治理 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑邮件提醒、退订和商业邮件边界 |
| FTC, National Do Not Call Registry | https://telemarketing.donotcall.gov/ | 支撑电话提醒和人工联系前的 DNC 边界 |
| eCFR, 47 CFR 64.1200 Delivery restrictions | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200 | 支撑电话、短信、自动拨号、预录音和同意相关规则文本 |
| Calendly, How to reduce no-shows with email and text reminders | https://calendly.com/blog/guide-calendly-reminders/ | 仅作为 appointment reminder 和 no-show 行业实践参考 |
| Calendly, Reduce no-show rates in sales | https://calendly.com/blog/reduce-no-show-rates-sales | 仅作为 B2B demo no-show 行业语境参考 |
| Square Support, Set up Reserve with Google | https://squareup.com/help/us/en/article/6567-reserve-with-google | 支撑第三方 booking provider 和 Reserve with Google 集成语境 |

## 52.2 Lead Form 漏斗、资格问题与移动端 UX 来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Google Ads Lead Form 的资格、隐私政策、字段收集和广告政策要求 |
| Google Ads, Create lead form assets | https://support.google.com/google-ads/answer/9423235 | 支撑 Lead Form 创建、问题、字段、隐私 URL 和线索交接 QA |
| Google Ads Policy, Data collection and use | https://support.google.com/adspolicy/answer/6020956 | 支撑表单收集个人信息、披露、用途和安全处理要求 |
| Google Ads, Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户数据、consent、隐私披露、分享和数据处理要求 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 CTA、资格、价格、官方关系和服务结果不能误导 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing page、form、final URL 和广告承诺一致 |
| FTC, .com Disclosures | https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising | 支撑披露清楚、明显、靠近相关 claim 或 CTA |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑表单 PII 最小化、访问控制、保留和删除 |
| FTC, Follow the Lead workshop | https://www.ftc.gov/news-events/events/2015/10/follow-lead-ftc-workshop-lead-generation | 支撑 lead generation 中消费者信息流转、透明度和披露风险 |
| Google Analytics, Avoid sending PII | https://support.google.com/analytics/answer/6366371 | 支撑表单、URL、analytics 字段和日志不发送 PII |
| web.dev, Learn Forms | https://web.dev/learn/forms | 支撑表单结构、label、输入和用户体验基础 |
| web.dev, Autofill | https://web.dev/learn/forms/autofill | 支撑 mobile/autofill 和减少误填的实践 |
| web.dev, Validation | https://web.dev/learn/forms/validation | 支撑表单验证、错误提示和输入反馈 |
| MDN, autocomplete | https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete | 支撑 autocomplete attribute 和表单输入语义 |
| W3C WAI, Forms Tutorial | https://www.w3.org/WAI/tutorials/forms/ | 支撑可访问表单、label、说明和错误提示 |
| WCAG 2.2, Labels or Instructions | https://www.w3.org/TR/WCAG22/#labels-or-instructions | 支撑输入字段 label/instructions 可访问性要求 |

## 53. RSOC / N2S、Search Feed Partner 与相关搜索来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google AdSense, Related search for content pages | https://support.google.com/adsense/answer/10233819 | 支撑 RSOC/Related Search 的产品语境、二屏 search ads 变现、文本内容和权限要求 |
| Google AdSense, AFS Product-Integrated Feature policies | https://support.google.com/adsense/answer/14638581 | 支撑 PIF、Related Search、partner-provided terms、广告请求和诱导点击边界 |
| Google AdSense, AdSense for Search policies | https://support.google.com/adsense/answer/1354757 | 支撑搜索结果页、代码修改、广告数量和用户搜索行为边界 |
| Google AdSense, Search ads policies | https://support.google.com/adsense/answer/7003954 | 支撑 search ads 必须基于用户动作、清楚标识广告、避免激励搜索或广告点击 |
| Google Custom Search Ads implementation guide | https://developers.google.com/custom-search-ads/s/docs/implementation-guide | 支撑 RAC/referrerAdCreative、content page、related search unit 和参数实现语境 |
| Google AdSense, Search ads parameter descriptions | https://support.google.com/adsense/answer/9055049 | 支撑 pageOptions、adblock、referrerAdCreative、terms 和 ad unit 参数语义 |
| Google AdSense, Restricted Access Features | https://support.google.com/adsense/answer/16262554 | 支撑 RAF/strike、访问权限受限功能和 policy violation 后果 |
| Google AdSense, Policy violations in scope for RAFs | https://support.google.com/adsense/answer/16269587 | 支撑哪些政策问题会影响 Related Search / RAF 权限 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑 bridge/gateway、arbitrage、低价值目的地和广告网络滥用风险 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑内容页、搜索结果页和广告承诺一致、可访问、非低价值目的地 |
| Jounce Media terminology | https://jouncemedia.com/resources/terminology | 支撑 MFA、arbitrage 等行业术语背景 |
| Coinis RSOC glossary | https://coinis.com/glossary/rsoc-related-search-on-content | 仅作为行业术语背景，不作为合规判断依据 |

## 54. AI Provider、Prompt 模板与创意成本治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Automatically created assets | https://support.google.com/google-ads/answer/11259373 | 支撑自动生成资产仍需进入 Claim 审核和人工放行 |
| Google Ads, Text customization | https://support.google.com/google-ads/answer/6072565 | 支撑动态文案、参数化文案和模板化创意的边界 |
| Google Ads, Responsive search ads | https://support.google.com/google-ads/answer/7684791 | 支撑 RSA 资产组合、headline/description 候选和测试语境 |
| Google Ads, Ad Strength | https://support.google.com/google-ads/answer/9921843 | 支撑 Ad Strength 只是诊断工具，不等于合规或可收款 |
| Google Ads, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 AI 输出不得新增主体、价格、资质、官方关系或结果承诺 |
| Google Ads, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑 AI 输出需要标点、大小写、样式、重复和文案质量检查 |
| Google Ads API, Automatically created assets | https://developers.google.com/google-ads/api/docs/assets/automatically-created-assets | 支撑自动资产的 API 语境和后续审计方向 |
| NIST, AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | 支撑 AI 风险、治理、测量和管理框架 |
| NIST, AI RMF Generative AI Profile | https://www.nist.gov/itl/ai-risk-management-framework/generative-ai-profile | 支撑生成式 AI 幻觉、内容风险和治理控制 |
| OWASP, Top 10 for LLM Applications | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | 支撑 prompt injection、数据泄漏、输出处理和 LLM 应用安全 |
| Google, Generative AI Prohibited Use Policy | https://policies.google.com/terms/generative-ai/use-policy | 支撑生成式 AI 使用边界、滥用和有害内容限制 |

## 55. Google Ads Editor CSV 与 Bulk Upload 批量变更来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Editor Help | https://support.google.com/google-ads/editor | 支撑 Editor 是官方离线编辑和批量管理工具 |
| Google Ads Editor, Prepare a CSV file | https://support.google.com/google-ads/editor/answer/56368 | 支撑 CSV 字段合同、离线准备和导入前结构化检查 |
| Google Ads Editor, Check changes before posting | https://support.google.com/google-ads/editor/answer/56370 | 支撑发布前检查变更、发现错误和人工确认 |
| Google Ads Editor, Review recent account changes | https://support.google.com/google-ads/editor/answer/30582 | 支撑拉取外部变更、避免 stale payload 覆盖后台手工变更 |
| Google Ads Editor, Share proposed changes | https://support.google.com/google-ads/editor/answer/38664 | 支撑把批量变更作为可审阅包交给他人确认，而不是无人发布 |
| Google Ads Editor, Post changes | https://support.google.com/google-ads/editor/answer/30583 | 支撑授权用户在 Editor 中发布，而不是工作台自动点击后台 |
| Google Ads Help, Bulk uploads | https://support.google.com/google-ads/answer/10702433 | 支撑 Google Ads 后台 bulk upload 的 preview/apply 和批量结果治理 |
| Google Ads Help, Change history | https://support.google.com/google-ads/answer/19888 | 支撑批量变更发布后用 Change history 做外部审计 |
| Google Ads Scripts, Bulk upload | https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload | 支撑 Scripts bulk upload preview/apply 作为可授权、可审计替代 |
| Google Ads Scripts, Preview mode | https://developers.google.com/google-ads/scripts/docs/preview | 支撑默认 preview，不自动 apply 高风险变更 |
| Google Ads API, Partial failures | https://developers.google.com/google-ads/api/docs/best-practices/partial-failures | 支撑批量变更必须保存行级错误和部分失败 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑 CSV / bulk upload 不能用于绕审核、cloaking 或规避政策执行 |
| Google Ads, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、页面可达、广告承诺一致性和目的地质量检查 |

## 56. Google Ads Scripts 数据同步、快照与一致性来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Scripts, Reports | https://developers.google.com/google-ads/scripts/docs/concepts/reports | 支撑用 `AdsApp.report()` / `AdsApp.search()` 读取 GAQL 报表并保存 query、date range 和拉取时间 |
| Google Ads Scripts, Manager account scripts | https://developers.google.com/google-ads/scripts/docs/concepts/manager-scripts | 支撑 MCC 下选择 client accounts 和并行处理多个账号，但不能作为账号池或规避封禁工具 |
| Google Ads Scripts, External data integration | https://developers.google.com/google-ads/scripts/docs/integrations/external-data | 支撑 Sheets、Drive、JDBC、URL Fetch 等外部数据集成边界 |
| Google Ads Scripts, Limits | https://developers.google.com/google-ads/scripts/docs/limits | 支撑同步频率、运行时长、账号范围和配额治理 |
| Google Ads Scripts, Execution logs | https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs | 支撑同步任务保留运行日志、warning 和 error |
| Google Ads Scripts, Preview mode | https://developers.google.com/google-ads/scripts/docs/preview | 支撑写入前先 preview，不把同步器做成无人审批写入器 |
| Google Ads Scripts, Mutate | https://developers.google.com/google-ads/scripts/docs/concepts/mutate | 支撑结构化写入必须和预览、审批、回滚、日志一起治理 |
| Google Ads Scripts, Bulk upload | https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload | 支撑 CSV / bulk upload preview 与 apply 的分离 |
| Google Ads Scripts, Link Checker solution | https://developers.google.com/google-ads/scripts/docs/solutions/link-checker | 支撑 URL 检查类同步任务应是 QA 和提醒，不是 cloaking 或分流 |
| Google Ads, About data freshness | https://support.google.com/google-ads/answer/2544985 | 支撑 Google Ads 报表有数据处理延迟，15 分钟同步不等于最终真相 |
| Google Ads, Data discrepancies | https://support.google.com/google-ads/answer/7457111 | 支撑 Google Ads、Analytics、server log 和第三方报表差异需要解释和对账 |
| Google Ads, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑近期 CPA/ROAS 会受 conversion lag 影响，扩量前要等待窗口稳定 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑未来 API 报表同步应保留 GAQL 查询、customer id 和快照 |
| Google Ads API, Google Ads Query Language | https://developers.google.com/google-ads/api/docs/query/overview | 支撑字段选择、分段和过滤决定同步口径 |
| Google Ads API, Change event | https://developers.google.com/google-ads/api/docs/change-event | 支撑用 ChangeEvent 对齐外部变更和内部 payload 版本 |
| Google Ads API, API limits and quotas | https://developers.google.com/google-ads/api/docs/best-practices/quotas | 支撑同步和重试必须遵守官方配额边界 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑同步系统不能用于隐藏真实目的地、cloaking、多账号规避或绕过政策执行 |

## 57. 任务编排、安全审批、执行日志与事故复盘来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads, Using scripts to make automated changes | https://support.google.com/google-ads/answer/188712 | 支撑 Scripts 可用于自动化变更，但需要在官方授权和脚本语境内运行 |
| Google Ads Scripts, Authorization | https://developers.google.com/google-ads/scripts/docs/authorization | 支撑 Scripts 需要授权用户授权，不是 Cookie 后台接管 |
| Google Ads Scripts, Limits | https://developers.google.com/google-ads/scripts/docs/limits | 支撑任务编排必须考虑脚本运行时长、账号范围和配额边界 |
| Google Ads Scripts, Bulk upload | https://developers.google.com/google-ads/scripts/docs/concepts/bulk-upload | 支撑 bulk upload preview/apply 流程和人工放行闸门 |
| Google Ads Scripts, Execution logs | https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs | 支撑任务运行后保留脚本日志、错误和执行证据 |
| Google Ads Scripts, Preview mode | https://developers.google.com/google-ads/scripts/docs/preview | 支撑先 preview 再 apply 的安全执行等级 |
| Google Ads, Change history | https://support.google.com/google-ads/answer/19888 | 支撑广告后台变更追踪和事故复盘证据链 |
| Google Ads API, Change event | https://developers.google.com/google-ads/api/docs/change-event | 支撑通过官方 API 读取变更事件用于外部审计 |
| Google Ads API, Mutating overview | https://developers.google.com/google-ads/api/docs/mutating/overview | 支撑未来 API 写入也要用 validate/dry run、错误处理和审计 |
| Google Ads API, Partial failures | https://developers.google.com/google-ads/api/docs/best-practices/partial-failures | 支撑批量变更不能把局部失败隐藏成整体成功 |
| Google Ads API, Quotas | https://developers.google.com/google-ads/api/docs/best-practices/quotas | 支撑调度和重试必须遵守官方 API 配额和速率边界 |
| Google Ads, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑任务系统不能用于 cloaking、多账号规避或绕过政策执行 |
| Google Ads, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑套利、桥页、低价值目的地和广告网络滥用风险 |
| Google SRE, Postmortem culture | https://sre.google/sre-book/postmortem-culture/ | 支撑无责复盘、时间线、根因和预防项 |
| Google SRE, Managing incidents | https://sre.google/sre-book/managing-incidents/ | 支撑 freeze、triage、contain、reconcile 的事故响应流程 |

## 58. Google Ads 广告审核、拒登、Policy Manager 与申诉证据包来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About the ad review process | https://support.google.com/google-ads/answer/1722120 | 支撑新建或修改广告/素材后进入审核，审核广告内容、关键词、目标页、图片、视频和其他资产 |
| Google Ads Help, Fix a disapproved ad or appeal a policy decision | https://support.google.com/google-ads/answer/9338593 | 支撑拒登后先定位政策问题、修复广告/资产/目的地，再提交 appeal 或重新审核 |
| Google Ads Help, Submit a campaign for policy review | https://support.google.com/google-ads/answer/9456683 | 支撑 campaign 级政策 review 的提交和等待口径 |
| Google Ads Help, About Policy Manager | https://support.google.com/google-ads/answer/9675313 | 支撑集中查看 policy issue、申诉状态和处理结果 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目标页可达性、跳转链和广告承诺一致性检查 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑主体、价格、资质、官方关系、结果承诺和重要限制不得误导 |
| Google Ads Policy, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑标点、大小写、重复、语法、格式和文本质量检查 |
| Google Ads Policy, Text ad requirements | https://support.google.com/adspolicy/answer/6021630 | 支撑文字广告资产、标题、描述和 display URL 的标准政策边界 |
| Google Ads Policy, Trademarks | https://support.google.com/adspolicy/answer/6118 | 支撑品牌词、商标、官方关系和竞品投放风险判断 |
| Google Ads Policy, Unacceptable business practices | https://support.google.com/adspolicy/answer/15938071 | 支撑严重误导、隐藏身份、诱导提交信息和欺骗性业务模式识别 |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑不把换域名、换账号、cloaking、动态目的地或多账号操作作为拒登修复 |
| Google Ads API, Policy support | https://developers.google.com/google-ads/api/support/policy | 支撑未来用官方 API 读取政策摘要和政策主题，而不是 Cookie 后台抓取 |
| Google Ads API, PolicyTopicEntry | https://developers.google.com/google-ads/api/reference/rpc/latest/PolicyTopicEntry | 支撑把 policy topic 结构化保存到 ad_review_cases 和 policy_decision_snapshots |
| Google Ads API, PolicySummary | https://developers.google.com/google-ads/api/reference/rpc/latest/PolicySummary | 支撑保存审核状态、审批状态和政策审查摘要 |

## 59. Google Ads Recommendations、Experiments 与 Auto-apply 优化治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About recommendations | https://support.google.com/google-ads/answer/3448398 | 支撑 Recommendations 是平台生成的优化建议，不能直接等同于套利 paid revenue |
| Google Ads Help, Check your optimization score | https://support.google.com/google-ads/answer/9061547 | 支撑 Optimization Score 是设置优化估算，不是利润分数 |
| Google Ads Help, Types of recommendations | https://support.google.com/google-ads/answer/3416396 | 支撑按 Repairs、Bidding/Budget、Keywords、Ads/Assets、Measurement 等类别做风险分级 |
| Google Ads Help, Apply or dismiss recommendations | https://support.google.com/google-ads/answer/10169817 | 支撑建议需要 apply、dismiss、review，而不是默认执行 |
| Google Ads Help, About applying recommendations automatically | https://support.google.com/google-ads/answer/10279006 | 支撑 Auto-apply 会定期自动应用选择类型的建议，套利 V1 默认关闭 |
| Google Ads Help, Manage auto-apply recommendations | https://support.google.com/google-ads/answer/10276359 | 支撑 Auto-apply queue、history 和设置巡检 |
| Google Ads Help, Change history | https://support.google.com/google-ads/answer/19888 | 支撑把 recommendation、auto-apply、Scripts、Editor 和人工变更纳入复盘 |
| Google Ads Help, Set up a custom experiment | https://support.google.com/google-ads/answer/6261395 | 支撑实验流量拆分、基线对照和单一假设验证 |
| Google Ads Help, Monitor experiments | https://support.google.com/google-ads/answer/6318747 | 支撑实验期间监控、比较和决策流程 |
| Google Ads Help, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑等待 conversion lag 和收入回填后再接受扩量建议 |
| Google Ads API, Optimization score and recommendations | https://developers.google.com/google-ads/api/docs/recommendations | 支撑未来通过官方 API 只读同步 recommendation，而不是 Cookie 后台抓取 |
| Google Ads API, Take actions on recommendations | https://developers.google.com/google-ads/api/docs/recommendations/action | 支撑 apply/dismiss 等写入动作必须审批和记录 |
| Google Ads API, Experiments overview | https://developers.google.com/google-ads/api/docs/experiments/overview | 支撑未来把 experiment plan、split 和 result 结构化保存 |
| Google Ads API, Change event | https://developers.google.com/google-ads/api/docs/change-event | 支撑把建议执行结果、外部变更和事故复盘对齐 |

## 60. Creative Angle Library、素材版本与反馈闭环来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About responsive search ads | https://support.google.com/google-ads/answer/7684791 | 支撑 RSA 多标题/描述资产组合和素材多样性治理 |
| Google Ads Help, About Ad Strength | https://support.google.com/google-ads/answer/9921843 | 支撑 Ad Strength 只是诊断，不等于利润、合规或可收款收入 |
| Google Ads Help, View asset reporting for responsive search ads | https://support.google.com/google-ads/answer/9781208 | 支撑 asset-level 表现反馈和素材版本复盘 |
| Google Ads Help, Set up ad variations | https://support.google.com/google-ads/answer/7438541 | 支撑对文案、URL 和资产改动做实验化比较 |
| Google Ads Help, About automatically created assets | https://support.google.com/google-ads/answer/11259373 | 支撑自动资产必须进入 claim/proof 审核和版本记录 |
| Google Ads Help, Monitor experiments | https://support.google.com/google-ads/answer/6318747 | 支撑素材实验要保留基线、指标和决策结果 |
| Google Ads Help, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑创意 winner 判断必须等待回传和收入延迟 |
| Google Ads Help, Change history | https://support.google.com/google-ads/answer/19888 | 支撑素材、资产和页面变更进入事故复盘 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑把误导 claim、官方关系、价格和结果承诺写入 banned patterns |
| Google Ads Policy, Editorial requirements | https://support.google.com/adspolicy/answer/6021546 | 支撑素材版本需要记录标点、大小写、重复和编辑质量修复 |
| Google Ads API, Responsive Search Ads | https://developers.google.com/google-ads/api/docs/responsive-search-ads/overview | 支撑未来按 RSA 资产和组合保存素材版本 |
| Google Ads API, Ad group ad asset view | https://developers.google.com/google-ads/api/fields/latest/ad_group_ad_asset_view | 支撑未来以官方 API 读取广告组资产表现，而不是 Cookie 后台抓取 |
| Google Ads API, Asset group asset | https://developers.google.com/google-ads/api/fields/latest/asset_group_asset | 支撑 PMax / asset group 场景的资产表现和状态复盘 |
| FTC, Endorsements, influencers, and reviews | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | 支撑评价、背书、商业关系披露和创意 claim 边界 |

## 61. Campaign 命名、Labels、UTM/SubID 与维度治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 支撑用 ValueTrack 把 campaign、ad group、keyword、match type、device、network、creative 等点击上下文带入 URL |
| Google Ads Help, Set up tracking with ValueTrack parameters | https://support.google.com/google-ads/answer/6305348 | 支撑 tracking template、Final URL suffix 和 URL options 的字段设计与上线 QA |
| Google Ads Help, Create custom parameters for advanced tracking | https://support.google.com/google-ads/answer/6325879 | 支撑 `{_offer}`、`{_lpv}`、`{_angle}`、`{_linkv}` 等 custom parameter 的层级和覆盖规则 |
| Google Ads Help, About ads labels | https://support.google.com/google-ads/answer/2475865 | 支撑 Labels 用于组织 campaign、ad group、ad、keyword，并说明 label 适合做横向分类而非唯一事实来源 |
| Google Ads API, Labels | https://developers.google.com/google-ads/api/docs/reporting/labels | 支撑未来以官方 API 读取 label id、resource name 和 label report，而不是 Cookie 后台抓取 |
| Google Analytics Help, URL builders: Collect campaign data with custom URLs | https://support.google.com/analytics/answer/10917952 | 支撑 UTM source、medium、campaign、term、content、id 等 URL 命名和手动标记 |
| Google Analytics Help, Traffic-source dimensions, manual tagging, and auto-tagging | https://support.google.com/analytics/answer/11242870 | 支撑 GA4 manual tagging、auto-tagging 和 traffic-source dimensions 的报表口径 |
| Google Analytics Help, Traffic-source dimensions | https://support.google.com/analytics/answer/15567068 | 支撑 source、medium、campaign、manual term、manual content 等维度解释 |
| Google Ads Help, About auto-tagging | https://support.google.com/google-ads/answer/3095550 | 支撑 `gclid` 等自动标记用于 Ads/Analytics 归因和 offline conversion 匹配 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑未来报表同步保留 customer id、date range、query、segments 和快照证据 |
| Google Ads API, Google Ads Query Language | https://developers.google.com/google-ads/api/docs/query/overview | 支撑用 GAQL 字段、segment、filter 做可复盘报表，不依赖后台 Cookie 镜像 |
| Google Ads API, Field metadata | https://developers.google.com/google-ads/api/fields/latest/overview | 支撑字段兼容性、可选择字段、segments 和 metrics 的 join 设计 |
| Google Ads API, Upload click conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-clicks | 支撑 click id、conversion time、value、currency 和 transaction 去重口径 |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑命名、参数、换链接和任务系统不能用于隐藏真实目的地、cloaking、规避政策或多账号规避 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目标页可访问性、跳转和广告承诺一致性 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑页面版本、参数和创意不能隐藏主体、价格、资格、官方关系或重要限制 |

## 62. 异常监控、告警、止损队列与事故分诊来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Help, About spending limits | https://support.google.com/google-ads/answer/10486637 | 支撑 average daily budget、daily/monthly spending limit、served cost 和 billed cost 的预算告警 |
| Google Ads Help, Set up automated rules | https://support.google.com/google-ads/answer/2472779 | 支撑自动规则有条件、频率和执行边界，V1 应先做建议和审批 |
| Google Ads Help, Common ways to use automated rules | https://support.google.com/google-ads/answer/2497710 | 支撑按预算、成本、状态和时间做规则化运营，但要保留人工闸门 |
| Google Ads Help, Data discrepancies | https://support.google.com/google-ads/answer/7457111 | 支撑 Google Ads、GA4、第三方和内部报表差异需要分层诊断 |
| Google Ads Help, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑近期 CPA、ROAS、RPV 和 ROI 告警必须考虑 conversion delay |
| Google Ads Help, Invalid clicks | https://support.google.com/google-ads/answer/42995 | 支撑异常点击和无效流量分诊，不用补点击或模拟访问修报表 |
| Google Ads Help, About explanations | https://support.google.com/google-ads/answer/9000655 | 支撑大幅波动可结合 explanations 看 budget、bidding、conversion delay、asset、eligibility 和 Change history |
| Google Ads Help, Change history | https://support.google.com/google-ads/answer/19888 | 支撑异常前后按时间线查预算、关键词、URL、素材和操作人 |
| Google Ads API, Change event | https://developers.google.com/google-ads/api/docs/change-event | 支撑未来以官方 API 读取变更事件用于事故证据 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑报表同步、快照、维度分段和 alert rule 输入 |
| Google Ads Scripts, Limits | https://developers.google.com/google-ads/scripts/docs/limits | 支撑任务执行和重试必须遵守 Scripts 配额、运行时间和账号限制 |
| Google Ads Scripts, Execution logs | https://developers.google.com/google-ads/scripts/docs/troubleshooting/execution-logs | 支撑任务失败要保存脚本日志和错误证据 |
| Google Analytics Help, Analytics Insights | https://support.google.com/analytics/answer/9443595 | 支撑 automated/custom insights、email alerts 和异常检测思路 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 URL、landing、可访问性、crawlability 和 destination mismatch 告警 |
| PageSpeed Insights API | https://developers.google.com/speed/docs/insights/v5/get-started | 支撑未来页面速度和体验监控 |
| Google SRE Book, Monitoring Distributed Systems | https://sre.google/sre-book/monitoring-distributed-systems/ | 支撑低噪声、高行动性的监控和四个黄金信号 |
| Google SRE Workbook, Alerting on SLOs | https://sre.google/workbook/alerting-on-slos/ | 支撑告警窗口、错误预算和可行动告警设计 |
| Google SRE Book, Managing Incidents | https://sre.google/sre-book/managing-incidents/ | 支撑事故分诊、协作、恢复和状态管理 |
| Google SRE Book, Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ | 支撑无责复盘、根因分析和预防项 |

## 63. Insurance、Medicare / ACA 与 Final Expense Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Health insurance ads | https://support.google.com/adspolicy/answer/15597838 | 支撑健康保险广告认证、地区和产品限制判断 |
| Google Ads Policy, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑健康相关广告、医疗声明和认证边界 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑敏感属性、健康/财务困难和个性化定向边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑官方关系、价格、资格、主体和承诺透明度 |
| Google Ads Policy, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑保险/金融相关条款、费用和资格披露 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 Google Ads lead form 的字段、隐私和后续处理边界 |
| Google Ads Help, About call assets | https://support.google.com/google-ads/answer/2453991 | 支撑 call-heavy insurance campaign 的 call asset 和电话信号治理 |
| HealthCare.gov, Dates and deadlines | https://www.healthcare.gov/quick-guide/dates-and-deadlines/ | 支撑 ACA / Marketplace 开放注册日期和页面日期来源 |
| HealthCare.gov, Special Enrollment Period | https://www.healthcare.gov/coverage-outside-open-enrollment/special-enrollment-period/ | 支撑 SEP 条件和 outside open enrollment 页面边界 |
| Medicare.gov, Joining a plan | https://www.medicare.gov/basics/get-started-with-medicare/get-more-coverage/joining-a-plan | 支撑 Medicare 加入/更换计划时间窗口 |
| Medicare.gov, Plan Compare | https://www.medicare.gov/plan-compare/ | 支撑 Medicare 计划比较应优先引用官方工具 |
| CMS, Contract Year 2025 Medicare Advantage and Part D Final Rule | https://www.cms.gov/newsroom/fact-sheets/contract-year-2025-medicare-advantage-and-part-d-final-rule-cms-4205-f | 支撑 Medicare marketing、TPMO、agent/broker 相关治理 |
| CMS Marketplace, Agents and brokers | https://www.cms.gov/marketplace/agents-brokers | 支撑 Marketplace agent/broker 角色和官方资源 |
| CMS Marketplace, Direct Enrollment and Enhanced Direct Enrollment | https://www.cms.gov/marketplace/marketplace-technical-assistance-resources/direct-enrollment-and-enhanced-direct-enrollment | 支撑 Marketplace web-broker / EDE 场景的授权和技术边界 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、lead generation、拒绝联系和披露边界 |
| FCC, TCPA and robocalls information | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑自动拨号、robocall/robotext 和 consent 风险背景 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| NAIC, Producer Licensing | https://content.naic.org/cipr-topics/producer-licensing | 支撑 insurance producer / agent licensing 的角色边界 |
| NAIC, Life Insurance consumer information | https://content.naic.org/consumer/life-insurance.htm | 支撑 life / final expense 用户教育和误导 claim 审核 |
| NIPR, Producer licensing | https://nipr.com/licensing-center | 支撑按州检查 producer licensing 和授权线索 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |

## 64. Loan、Mortgage、Credit 与 Debt Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑贷款、债务、信用、金融服务广告的披露、地区规则、认证和禁投项 |
| Google Ads Policy, Housing, employment, and credit FAQ | https://support.google.com/adspolicy/answer/9997418 | 支撑美国/加拿大住房、就业、信贷广告定向限制 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑财务困难、债务、信用状态等敏感个性化定向边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑费用、资格、主体、政府关系和结果承诺透明度 |
| Google Ads Policy, Unacceptable business practices | https://support.google.com/adspolicy/answer/6020954 | 支撑欺骗性金融服务、虚假资质和不可信业务模式审查 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| CFPB, Digital comparison-shopping circular | https://www.consumerfinance.gov/compliance/circulars/consumer-financial-protection-circular-2024-01-preferential-treatment-and-steering-practices-by-digital-intermediaries-for-consumer-financial-products-or-services/ | 支撑金融产品比较、推荐排序、补偿驱动导流和消费者误导风险 |
| CFPB, Regulation V / Fair Credit Reporting Act | https://www.consumerfinance.gov/rules-policy/regulations/1022/ | 支撑 consumer report、信贷/保险/就业/住房资格判断边界 |
| CFPB, Regulation B / Equal Credit Opportunity Act | https://www.consumerfinance.gov/rules-policy/regulations/1002/ | 支撑信贷资格、歧视风险和 adverse action 相关边界 |
| CFPB, Regulation Z / Truth in Lending Act | https://www.consumerfinance.gov/rules-policy/regulations/1026/ | 支撑 APR、rate、payment、term 等信贷广告披露 |
| CFPB, Mortgage resources | https://www.consumerfinance.gov/consumer-tools/mortgages/ | 支撑 mortgage / refinance 用户教育和页面 claim 审核 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、debt relief、DNC、advance fee 和记录治理 |
| FTC, Credit Repair: How to Help Yourself | https://consumer.ftc.gov/articles/credit-repair-how-help-yourself | 支撑 credit repair claim、用户权利和保证修复风险 |
| FTC, Mortgage and foreclosure rescue scams | https://consumer.ftc.gov/articles/mortgage-and-foreclosure-rescue-scams | 支撑 mortgage relief、foreclosure rescue 和政府/收费误导风险 |
| Federal Student Aid, Avoid student loan debt relief scams | https://studentaid.gov/resources/scams | 支撑 student loan relief、官方项目和收费代办风险 |
| NMLS Consumer Access | https://www.nmlsconsumeraccess.org/ | 支撑 mortgage loan originator、lender、broker license 查询 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上金融广告披露、真实陈述和 claim proof |

## 65. Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| ABA Model Rule 7.1, Communications Concerning a Lawyer's Services | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communications_concerning_a_lawyers_services/ | 支撑法律服务广告不能 false or misleading |
| ABA Model Rule 7.2, Communications Concerning a Lawyer's Services: Specific Rules | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_2_communications_concerning_a_lawyers_services_specific_rules/ | 支撑律师广告、lead generator、推荐和联系方式披露边界 |
| ABA Model Rule 7.3, Solicitation of Clients | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_3_solicitation_of_clients/ | 支撑 solicitation、实时联系和压力式获取客户风险 |
| ABA Model Rule 1.18, Duties to Prospective Client | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_18_duties_to_prospective_client/ | 支撑 prospective client 信息和初次咨询资料处理 |
| ABA Model Rule 1.6, Confidentiality of Information | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_6_confidentiality_of_information/ | 支撑敏感案件信息、录音和访问控制边界 |
| ABA Model Rule 5.4, Professional Independence of a Lawyer | https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_5_4_professional_independence_of_a_lawyer/ | 支撑非律师、fee sharing、referral 和 lead generator 边界 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑法律问题、身份、健康、财务困境等敏感状态的个性化广告边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑官方关系、费用、资格、结果和主体透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Policy, Unacceptable business practices | https://support.google.com/adspolicy/answer/6020954 | 支撑欺骗性法律服务、虚假资质和不可信业务模式审查 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Local Services Ads, How leads work | https://support.google.com/localservices/answer/7195435 | 支撑 LSA lead、charged lead、valid lead 和服务地区语境 |
| Google Local Services Ads, Google Screened | https://support.google.com/localservices/answer/9376651 | 支撑法律/专业服务筛查、license、reviews 和 Google Screened 语境 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、DNC、拒绝联系和记录治理 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | 支撑 testimonials、reviews、past results 和 material connection 披露 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
| FTC, Enforcement Policy Statement on Deceptively Formatted Advertisements | https://www.ftc.gov/legal-library/browse/commission-policy-statement-enforcement-policy-statement-deceptively-formatted-advertisements | 支撑 advertorial、伪装新闻/评测/公益法律信息的格式风险 |
| Legal Services Corporation, Find Legal Aid | https://www.lsc.gov/about-lsc/what-legal-aid/get-legal-help | 支撑不要冒充 legal aid、官方公益法律服务或政府援助 |

## 66. Home Services、Solar 与 Local Services Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Local Services Ads, How leads work | https://support.google.com/localservices/answer/7195435 | 支撑 valid lead、charged lead、lead type、budget、credits 和 LSA lead 口径 |
| Google Local Services Ads, Understand the screening and verification process | https://support.google.com/localservices/answer/6226575 | 支撑 background、business registration、insurance、license、review requirements 和持续复审 |
| Google Local Services Ads, How providers qualify | https://support.google.com/localservices/answer/6230381 | 支撑 Local Services provider screening、license、insurance 和 verification 语境 |
| Google Local Services Ads, Business screening and verification requirements | https://support.google.com/localservices/answer/12174778 | 支撑美国本地服务商 background、license、insurance 和 category-specific requirements |
| Google Ads Policy, Local Services platform policies | https://support.google.com/adspolicy/answer/6245891 | 支撑 service provider、agency、lead generation、aggregator 的 Local Services 平台政策 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑价格、服务范围、资质、badge、官方关系和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Business Profile, Guidelines for representing your business | https://support.google.com/business/answer/3038177 | 支撑真实业务名称、地址、service area 和本地业务资料一致性 |
| FTC, How To Avoid a Home Improvement Scam | https://consumer.ftc.gov/articles/how-avoid-home-improvement-scam | 支撑 contractor、合同、付款、pressure tactic 和 home improvement scam claim 审核 |
| FTC, Solar Power for Your Home | https://consumer.ftc.gov/articles/solar-power-your-home | 支撑 solar savings、lease/PPA、tax credit、PACE financing、roof/utility 条件和 installer 评估 |
| DOE, Homeowner's Guide to Going Solar | https://www.energy.gov/eere/solar/homeowners-guide-going-solar | 支撑 solar consumer education、financing、scam awareness 和官方资源 |
| FTC, HomeAdvisor lead marketing order | https://www.ftc.gov/node/80302 | 支撑 home improvement lead seller 不能误导服务商关于 lead quality、source 和 billing |
| FTC, Advertising FAQ's: A Guide for Small Business | https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business | 支撑 truth-in-advertising、material claim 和 substantiation |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | 支撑 reviews、testimonials、ratings 和 material connection 披露 |
| FTC, Complying with the Telemarketing Sales Rule | https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule | 支撑电话营销、DNC、拒绝联系和记录治理 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
| FTC, Consumer Reviews and Testimonials Final Rule | https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers | 支撑虚假评价、购买评价和 review claim 风险 |

## 67. Education、Career Training 与 Student Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑学校主体、accreditation、费用、资助、就业结果和重要限制透明度 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑敏感身份、未成年人、财务困难、宗教/身份相关教育等个性化广告边界 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Ads Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户提供数据、enhanced conversions、consent 和安全处理 |
| FTC, Guides for Private Vocational and Distance Education Schools | https://www.ftc.gov/legal-library/browse/rules/private-vocational-distance-education-schools | 支撑 vocational / distance education 的 accreditation、就业前景、入学资格和 deceptive sales claim |
| eCFR, 16 CFR Part 254 Guides for Private Vocational and Distance Education Schools | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-254 | 支撑现行 vocational school guides 条文引用 |
| FTC, Choosing a Vocational School or Certificate Program | https://consumer.ftc.gov/articles/choosing-vocational-school-or-certificate-program | 支撑 job placement、accreditation、licensing、cost、financial aid 和职业培训用户教育 |
| FTC, Choosing a College: Questions To Ask | https://consumer.ftc.gov/choosing-college-questions-ask | 支撑 college selection、accreditation、cost、graduation 和 job outcome 问题 |
| FTC, College Degree Scams | https://consumer.ftc.gov/articles/college-degree-scams | 支撑虚假 degree、假 accreditation 和 diploma mill 风险 |
| U.S. Department of Education, College Accreditation | https://www.ed.gov/laws-and-policy/higher-education-laws-and-policy/college-accreditation | 支撑 accreditation 来源和认可框架 |
| U.S. Department of Education, Find a College or Educational Program | https://www.ed.gov/higher-education/find-college-or-educational-program | 支撑 College Scorecard、College Navigator 和 program comparison 官方入口 |
| U.S. Department of Education, College Affordability and Transparency | https://www.ed.gov/higher-education/paying-college/college-affordability-and-transparency | 支撑 cost、debt、graduation rate、College Scorecard 和 College Navigator |
| College Navigator, NCES | https://nces.ed.gov/collegenavigator/ | 支撑 program、tuition、aid、admissions、accreditation、graduation rate 查询 |
| College Scorecard | https://collegescorecard.ed.gov/ | 支撑 cost、fields of study、graduation、debt、earnings 和 school comparison |
| Federal Student Aid, Avoid student loan debt relief scams | https://studentaid.gov/resources/scams | 支撑 student loan relief、政府冒充和收费代办风险 |
| Federal Student Aid, Preparing for College | https://studentaid.gov/resources/prepare-for-college | 支撑 college planning、financial aid 和官方学生资源 |
| FTC, How Student Loans Work and How To Avoid Scams | https://consumer.ftc.gov/articles/how-student-loans-work-how-avoid-scams | 支撑 student loan、financial aid 和教育债务 claim 风险 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑教育 lead 后续 email 联系、unsubscribe 和商业邮件边界 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |

## 68. Healthcare、Medical Appointment 与 Clinic Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑医疗、药品、认证、地区和禁止内容边界 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑健康状态、敏感兴趣和个性化广告限制 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑资质、费用、可约时间、保险网络和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Ads Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑用户提供数据、enhanced conversions、consent 和安全处理 |
| HHS OCR, HIPAA Privacy Rule | https://www.hhs.gov/hipaa/for-professionals/privacy/index.html | 支撑 PHI、covered entity、privacy safeguards 和医疗数据治理语境 |
| HHS OCR, Marketing under the HIPAA Privacy Rule | https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/marketing/index.html | 支撑医疗营销通信、授权和例外判断 |
| HHS OCR, Use of Online Tracking Technologies | https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html | 支撑医疗页面 pixel、analytics、tracking tech 和 PHI 泄露风险 |
| FTC, Health Products Compliance Guidance | https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance | 支撑健康产品和疗效 claim 的 substantiation |
| FTC, Health Breach Notification Rule | https://www.ftc.gov/legal-library/browse/rules/health-breach-notification-rule | 支撑 health app、健康数据泄露通知和非 HIPAA 健康数据风险 |
| FDA, Prescription Drug Advertising | https://www.fda.gov/drugs/information-consumers-and-patients-drugs/prescription-drug-advertising | 支撑处方药广告、benefit/risk 和 FDA 语境 |
| FDA, Overview of Device Regulation | https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/overview-device-regulation | 支撑医疗器械、device category 和 FDA regulatory context |
| CMS, Medical Bill Rights | https://www.cms.gov/medical-bill-rights | 支撑 No Surprises Act、医疗账单权利和费用透明语境 |
| CMS, Good Faith Estimate | https://www.cms.gov/medical-bill-rights/help/guides/good-faith-estimate | 支撑 uninsured/self-pay good faith estimate 和费用 claim |
| SAMHSA, Confidentiality Regulations FAQs | https://www.samhsa.gov/about-us/who-we-are/laws-regulations/confidentiality-regulations-faqs | 支撑 substance use disorder records 和 Part 2 高敏语境 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑医疗 lead 后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | 支撑 testimonials、reviews、before/after 和 material connection 披露 |

## 69. B2B SaaS、Professional Services 与 Demo Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑主体、价格、功能、官方关系、trial 和重要限制透明度 |
| Google Ads Policy, Trademarks | https://support.google.com/adspolicy/answer/6118 | 支撑竞品词、商标、ad text、reseller / informational site 边界 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Policy, Unwanted software | https://support.google.com/adspolicy/answer/15938073 | 支撑软件下载、插件、安装器、权限和透明度边界 |
| Google Ads Policy, Malicious software | https://support.google.com/adspolicy/answer/15939580 | 支撑恶意软件、compromised site 和下载页风险 |
| Google Software Principles | https://www.google.com/about/software-principles.html | 支撑软件透明、安装、广告标识、隐私政策和卸载原则 |
| Google Unwanted Software Policy | https://www.google.com/about/unwanted-software-policy.html | 支撑软件权限、个人数据传输、广告注入和官方关系表述 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和 webhook 边界 |
| Google Ads Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑 Customer Match、用户提供数据、披露和 consent |
| Google Ads, About enhanced conversions for leads | https://support.google.com/google-ads/answer/15713840 | 支撑 hashed first-party lead data 与 offline conversion attribution |
| Google Ads, Set up offline conversion imports using GCLID | https://support.google.com/google-ads/answer/7012522 | 支撑 GCLID、CRM 回传和 offline conversion import |
| FTC, Advertising and Marketing on the Internet | https://www.ftc.gov/business-guidance/resources/advertising-marketing-internet-rules-road | 支撑线上广告披露、真实陈述和 claim proof |
| FTC, Dot Com Disclosures | https://www.ftc.gov/system/files/documents/plain-language/bus41-dot-com-disclosures-information-about-online-advertising.pdf | 支撑数字广告披露清晰和显著性 |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑 testimonials、reviews、material connection 和 customer quote |
| FTC, Consumer Reviews and Testimonials Rule Q&A | https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers | 支撑 fake review、testimonial、review suppression 风险 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑 B2B lead 后续 email 联系、unsubscribe 和商业邮件边界 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 B2B 联系人数据最小化、保留、安全和删除 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| National Do Not Call Registry | https://www.donotcall.gov/ | 支撑 DNC / suppression 治理 |
| NIST Privacy Framework | https://www.nist.gov/privacy-framework | 支撑 B2B 数据处理、隐私风险和企业治理框架 |
| HubSpot, Marketing Qualified Lead | https://blog.hubspot.com/marketing/definition-marketing-qualified-lead-mql-under-100-sr | 支撑 MQL/SQL 和营销到销售交接概念 |
| Salesforce, Sales Qualified Lead | https://www.salesforce.com/blog/sales/sales-qualified-lead/ | 支撑 SQL、BANT、销售资格确认和 follow-up 语境 |

## 70. Crypto、Investment 与 Trading Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Cryptocurrencies and related products | https://support.google.com/adspolicy/answer/14009787 | 支撑 crypto exchange、wallet、coin trust、NFT、certification 和禁止/受限范围 |
| Google Ads Policy, Financial products and services | https://support.google.com/adspolicy/answer/2464998 | 支撑金融产品、费用、主体、地区、披露和金融服务政策 |
| Google Ads Policy, Complex speculative financial products | https://support.google.com/adspolicy/answer/15188218 | 支撑 CFD、forex、spread betting、rolling spot forex 等复杂投机产品边界 |
| Google Ads Policy, Apply to advertise restricted financial products | https://support.google.com/adspolicy/answer/7645254 | 支撑 restricted financial products certification 和地区/产品限制 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑主体、资质、费用、风险、官方关系和重要限制透明度 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑财务困难、脆弱状态和个性化广告限制 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| SEC, Crypto Assets and Emerging Technology | https://www.sec.gov/securities-topics/crypto-assets | 支撑 SEC crypto assets 教育、监管和 investor protection 语境 |
| SEC, Crypto Assets and the Federal Securities Laws | https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/crypto-assets-federal-securities-laws | 支撑 crypto assets 与 federal securities laws 关系 |
| Investor.gov, Exercise Caution with Crypto Asset Securities | https://www.investor.gov/index.php/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-alerts/crypto-asset-securities | 支撑 crypto asset securities、注册缺失和 fraud 风险 |
| Investor.gov, Red Flags of Investment Fraud Checklist | https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud/red-flags-investment-fraud-checklist | 支撑投资诈骗 red flag |
| Investor.gov, What You Can Do to Avoid Investment Fraud | https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud/what-you-can-do-avoid-investment-fraud | 支撑背景核验、注册检查和欺诈识别 |
| SEC IAPD | https://adviserinfo.sec.gov/firm/index.html | 支撑 investment adviser public disclosure 和注册查询 |
| FINRA, Crypto Assets Risks | https://www.finra.org/investors/investing/investment-products/crypto-assets/risks | 支撑 crypto asset 风险、unregistered entities 和 investor protection |
| FINRA BrokerCheck | https://brokercheck.finra.org/ | 支撑 broker / firm 背景和注册查询 |
| CFTC, Digital Asset Frauds | https://www.cftc.gov/LearnAndProtect/digitalassetfrauds | 支撑 digital asset fraud、虚假平台和监管投诉语境 |
| CFTC, Beware Virtual Currency Pump-and-Dump Schemes | https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/beware_virtual_currency_pump_dump.html | 支撑 pump-and-dump、社群喊单和操纵风险 |
| CFTC, Watch Out for Fraudulent Digital Asset and Crypto Trading Websites | https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/watch_out_for_digital_fraud.html | 支撑 fake trading platform 和 withdrawal scam 风险 |
| FTC, Investment Scams | https://consumer.ftc.gov/articles/investment-scams | 支撑 pressure tactic、guarantee、注册查询和消费者风险 |
| FinCEN, MSB Registration | https://www.fincen.gov/supporting-documentation-definitions | 支撑 MSB registration 语境和 registration 不等于投资合法性 |
| NMLS Consumer Access | https://www.nmlsconsumeraccess.org/ | 支撑 money transmitter / financial services state licensing 查询 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑金融 lead 后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |

## 71. Employment、Recruiting 与 Staffing Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑 employment opportunity / hiring 相关个性化广告和 HEC targeting 限制 |
| Google Ads Policy, Housing, employment, and credit FAQ | https://support.google.com/adspolicy/answer/9997418 | 支撑美国/加拿大 employment ads scope、policy acceptance 和 appeal 语境 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑职位真实性、主体、费用、薪资、远程和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Ads Policy, Lead form requirements | https://support.google.com/adspolicy/answer/9472930 | 支撑 lead form 内容限制、字段和敏感垂类边界 |
| Google Ads Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑 Customer Match、用户提供数据、披露和 consent |
| FTC, Job Scams | https://consumer.ftc.gov/articles/job-scams | 支撑 job scam、placement firm fee、government/postal job scam 和求职安全 |
| FTC, Job and Money-Making Scams | https://consumer.ftc.gov/features/job-and-money-making-scams | 支撑 job scam、work-from-home、money-making scheme 风险 |
| FTC, Business Opportunity Rule | https://www.ftc.gov/legal-library/browse/rules/business-opportunity-rule | 支撑 business opportunity、work-at-home disclosure 和 earnings claim 语境 |
| FTC, Selling a Work-at-Home or Other Business Opportunity | https://www.ftc.gov/business-guidance/resources/selling-work-home-or-other-business-opportunity-revised-rule-may-apply-you-1 | 支撑 work-at-home / bizopp disclosure、language 和 earnings claim |
| FTC, Taking the Ploy out of Employment Scams | https://www.ftc.gov/business-guidance/blog/2023/01/taking-ploy-out-employment-scams | 支撑 fake check、job opportunity scam 和 business guidance |
| EEOC, Prohibited Employment Policies/Practices | https://www.eeoc.gov/prohibited-employment-policiespractices | 支撑 job ad、recruitment、application、protected-class discrimination 边界 |
| EEOC, Recruiting, Hiring, or Promoting Employees | https://www.eeoc.gov/employers/small-business/3-im-recruiting-hiring-or-promoting-employees | 支撑招聘、筛选、测试、背景调查和小企业 hiring guidance |
| EEOC, Background Checks | https://www.eeoc.gov/background-checks | 支撑 background check 和 equal employment opportunity 边界 |
| FTC, Background Checks: What Employers Need to Know | https://www.ftc.gov/business-guidance/resources/background-checks-what-employers-need-know | 支撑 employment background reports、written permission、FCRA 和 adverse action |
| DOL, Misclassification of Employees as Independent Contractors | https://www.dol.gov/agencies/whd/flsa/misclassification | 支撑 employee vs independent contractor 和 FLSA misclassification 风险 |
| IRS, Independent Contractor or Employee | https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-self-employed-or-employee | 支撑 worker classification、behavioral/financial/control 判断 |
| CareerOneStop, Job Search | https://www.careeronestop.org/JobSearch/job-search.aspx | 支撑 DOL-sponsored job search 资源和可信求职来源 |
| CareerOneStop, 3 Tips to Avoid Job Scams | https://blog.careeronestop.org/3-tips-to-avoid-job-scams/ | 支撑求职骗局、预付费和非法活动警示 |
| USA.gov, How to Find a Job | https://www.usa.gov/job-help | 支撑政府 job search、CareerOneStop 和 official resource |
| USAJOBS | https://www.usajobs.gov/ | 支撑 federal government job official source |
| USPS Inspection Service, Government Employment Scams | https://www.uspis.gov/news/scam-article/usps-government-employment-scams | 支撑 postal/government job impersonation 和收费骗局 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑求职后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |

## 72. Gambling、Sweepstakes 与 Sports Betting Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Gambling and games | https://support.google.com/adspolicy/answer/6018017 | 支撑 gambling-related content、online gambling、social casino、certification 和 country restrictions |
| Google Ads Policy, Gambling and games policy overview | https://support.google.com/adspolicy/answer/6008942 | 支撑 responsible gambling advertising、local laws 和 certification 语境 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑 gambling / location-based gambling sensitive interest targeting 限制 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 bonus、odds、fees、operator identity、terms 和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| FTC, Fake Prize, Sweepstakes, and Lottery Scams | https://consumer.ftc.gov/articles/fake-prize-sweepstakes-and-lottery-scams | 支撑 prize / sweepstakes scam、预付费领奖和个人信息风险 |
| FTC, "You've Won" Scams | https://consumer.ftc.gov/features/pass-it-on/youve-won-scams | 支撑 prize scam、gift card、wire、crypto payment red flags |
| FTC, Endorsement Guides | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides | 支撑 influencer、contest/sweepstakes hashtag、material connection 披露 |
| FTC, Consumer Reviews and Testimonials Rule Q&A | https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers | 支撑 fake review、testimonial、review suppression 风险 |
| New York State Gaming Commission, Advertising Restrictions | https://gaming.ny.gov/advertising-restrictions | 支撑 sports wagering advertising、responsible gambling message 和 licensee responsibility |
| New York State Gaming Commission, Sports Wagering | https://gaming.ny.gov/sports-wagering | 支撑 NY sports wagering、operator context 和 responsible gambling reporting |
| New York State Gaming Commission, Avoid the Risky Bets of Unlawful Online Gambling | https://gaming.ny.gov/avoid-risky-bets-unlawful-online-gambling | 支撑 lawful operator、responsible gaming resources 和 unlawful online gambling risk |
| New Jersey Division of Gaming Enforcement, Sports Wagering | https://www.njoag.gov/about/divisions-and-offices/division-of-gaming-enforcement-home/sports-wagering/ | 支撑 NJ sports wagering law、rules、responsible gaming 和 regulator context |
| New Jersey DGE, Advertising Standards Best Practices | https://www.nj.gov/oag/ge/docs/BestPractices/AdvertisingBestPractices.pdf | 支撑 advertising standards、responsible gaming 和 prohibited / risky marketing practices |
| New Jersey DGE, Self Exclusion | https://www.njportal.com/dge/selfexclusion | 支撑 voluntary self-exclusion 和 suppression 语境 |
| UK Gambling Commission, Gambling marketing and advertising | https://www.gamblingcommission.gov.uk/about-us/guide/page/gambling-marketing-and-advertising | 支撑 gambling marketing、ASA/CAP 和 social responsibility 语境 |
| UK Gambling Commission, Advertising and marketing rules and regulations | https://www.gamblingcommission.gov.uk/licensees-and-businesses/guide/advertising-marketing-rules-and-regulations | 支撑 licensee advertising duties 和 socially responsible marketing |
| UK Gambling Commission, Remote gambling technical standards advertising | https://www.gamblingcommission.gov.uk/manual/remote-gambling-and-software-technical-standards/part-29-advertising | 支撑 rules、game descriptions、likelihood of winning 和 remote gambling ads |
| National Council on Problem Gambling | https://www.ncpgambling.org/ncpg/ | 支撑 problem gambling resources、helpline 和 responsible gambling 语境 |
| Washington WAC 230-06-068 Advertising | https://app.leg.wa.gov/WAC/default.aspx?cite=230-06-068 | 支撑 responsible gambling message 和 direct advertising unsubscribe 规则示例 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑 gambling lead 后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |
| FTC, Protecting Personal Information | https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business | 支撑 gambling lead 个人数据最小化、保留、安全和删除 |

## 73. Addiction Treatment、Rehab 与 Behavioral Health Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Healthcare and medicines | https://support.google.com/adspolicy/answer/176031 | 支撑 addiction services certification、healthcare policy 和 restricted medical content 边界 |
| Google Ads Policy, Personalized advertising | https://support.google.com/adspolicy/answer/143465 | 支撑 addiction、health、sensitive interest 和 remarketing / audience 边界 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 facility identity、insurance、official relationship、availability 和重要限制透明度 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| LegitScript, Addiction Treatment Certification Process | https://www.legitscript.com/certification/addiction-treatment-certification/addiction-treatment-certification-process/ | 支撑 addiction treatment advertising certification、provider/referral scope 和 platform trust |
| LegitScript, Addiction Treatment Certification FAQ | https://www.legitscript.com/service/certification/addiction-treatment/addiction-treatment-certification-faq/ | 支撑哪些服务/lead generator/referral agency 可能进入 certification 范围 |
| SAMHSA, Find Substance Use Disorder Treatment | https://www.samhsa.gov/substance-use/treatment/find-treatment/ | 支撑 official treatment locator、treatment options 和 public resource |
| FindTreatment.gov | https://findtreatment.gov/locator | 支撑 treatment facility lookup 和 official SAMHSA locator |
| SAMHSA, Find Help | https://www.samhsa.gov/find-help | 支撑 National Helpline、crisis / treatment support 和官方资源 |
| SAMHSA, Opioid Treatment Program Directory | https://www.samhsa.gov/find-help/locators/opioid-treatment-program-directory | 支撑 OTP certification / directory 和 provider verification |
| SAMHSA, Become an Opioid Treatment Program | https://www.samhsa.gov/substance-use/treatment/opioid-treatment-program/become-otp | 支撑 OTP certification、42 CFR Part 8 和 accreditation 语境 |
| HHS, Understanding Confidentiality of SUD Patient Records / Part 2 | https://www.hhs.gov/hipaa/for-professionals/special-topics/hipaa-part-2/index.html | 支撑 42 CFR Part 2、SUD patient record confidentiality 和 complaint path |
| HHS, Fact Sheet 42 CFR Part 2 Final Rule | https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html | 支撑 2024 Part 2 final rule 和 HIPAA alignment |
| HHS OCR, HIPAA Privacy Rule Marketing | https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/marketing/index.html | 支撑 PHI marketing、authorization 和 treatment communication boundary |
| HHS OCR, Use of Online Tracking Technologies | https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html | 支撑医疗页面 pixel、analytics、tracking tech 和 PHI 泄露风险 |
| HHS / FTC, Collecting, Using, or Sharing Consumer Health Information? | https://www.hhs.gov/hipaa/for-professionals/special-topics/hipaa-ftc-act/index.html | 支撑 HIPAA / FTC Act、health data claims 和 deceptive authorization 风险 |
| CDC, Treatment of Opioid Use Disorder | https://www.cdc.gov/overdose-prevention/treatment/opioid-use-disorder.html | 支撑 OUD evidence-based treatment、MOUD 和 treatment referral 语境 |
| CDC, Opioid Use Disorder: Treating | https://www.cdc.gov/overdose-prevention/hcp/clinical-care/opioid-use-disorder-treating.html | 支撑 clinician treatment、arrange care 和 evidence-based OUD care |
| SAMHSA, ASAM National Practice Guideline for OUD | https://www.samhsa.gov/resource/ebp/asam-national-practice-guideline-treatment-opioid-use-disorder | 支撑 OUD guideline 和 evidence-based practice 语境 |
| California DHCS, Licensing and Certification Division | https://www.dhcs.ca.gov/providers-partners/licensing-and-certification-division/ | 支撑 state provider licensing / certification 语境 |
| Florida Statutes 817.505, Patient brokering prohibited | https://www.flsenate.gov/Laws/Statutes/2024/0817.505 | 支撑 patient brokering、kickback 和 referral payment 风险 |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |

## 74. Government Services、Immigration 与 Public Benefits Lead 治理来源

| 来源 | URL | 支撑判断 |
| --- | --- | --- |
| Google Ads Policy, Government documents and services | https://support.google.com/adspolicy/answer/13156083 | 支撑 government documents/services scope、authorized provider、certification 和 Not a government website disclosure |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑 official relationship、government entity、pricing、business identity 和 misleading claim |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 landing、Final URL、跳转和用户体验一致性 |
| Google Ads Help, About lead form assets | https://support.google.com/google-ads/answer/9423234 | 支撑 lead form、隐私政策、字段和后续处理边界 |
| Google Ads Customer data policies | https://support.google.com/google-ads/answer/7475709 | 支撑 Customer Match、用户提供数据、披露和 consent |
| FTC, How To Avoid Imposter Scams | https://consumer.ftc.gov/imposters | 支撑 government imposter、agency-like communication 和 report path |
| FTC, How To Avoid Immigration Scams and Get Real Help | https://consumer.ftc.gov/articles/how-avoid-immigration-scams-and-get-real-help | 支撑 notario scam、official forms、real immigration help 和 payment red flags |
| FTC, Scams Against Immigrants | https://consumer.ftc.gov/features/scams-against-immigrants | 支撑 immigrant-targeted scams、multilingual education 和 reporting |
| USCIS, Avoid Scams | https://www.uscis.gov/scams-fraud-and-misconduct/avoid-scams | 支撑 immigration scam、official USCIS source 和 anti-fraud guidance |
| USCIS, Find Legal Services | https://www.uscis.gov/scams-fraud-and-misconduct/avoid-scams/find-legal-services | 支撑 attorney、DOJ accredited representative 和 authorized help |
| DOJ EOIR, Can Someone Represent You Before EOIR? | https://www.justice.gov/eoir/can-someone-represent-you-eoir | 支撑 immigration representation、attorney 和 accredited representative |
| DOJ EOIR, Recognition and Accreditation Program FAQ | https://www.justice.gov/eoir/recognition-and-accreditation-program-frequently-asked-questions | 支撑 recognized organization / accredited representative 规则 |
| USA.gov | https://www.usa.gov/ | 支撑 official guide to government information and services |
| USA.gov, Scams and fraud | https://www.usa.gov/scams-and-fraud | 支撑 scam reporting、government agency routing 和 consumer guidance |
| USA.gov, Avoid "free money" from the government scams | https://www.usa.gov/no-free-money | 支撑 free government money scam、benefit finder 和 grants.gov official path |
| Benefits.gov | https://www.benefits.gov/ | 支撑 official benefits eligibility finder and government benefit resources |
| IRS, Tax scams | https://www.irs.gov/scams | 支撑 IRS impersonation、tax scam、refund scam 和 official IRS resources |
| IRS, If you were scammed | https://www.irs.gov/help/tax-scams/if-you-were-scammed | 支撑 tax scam victim steps and reporting |
| SSA, Social Security-related scams | https://www.ssa.gov/scam/ | 支撑 SSA impersonation and official reporting |
| Travel.State.gov, Passport Fees | https://travel.state.gov/content/travel/en/passports/how-apply/fees.html | 支撑 official passport fees and service fee comparison |
| USA.gov, Replace vital documents | https://www.usa.gov/replace-vital-documents | 支撑 vital records official paths and agency routing |
| Grants.gov, Grant fraud | https://www.grants.gov/learn-grants/grant-fraud.html | 支撑 grant scam / fraud and official grant resources |
| FTC, CAN-SPAM Act compliance guide | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 支撑后续 email 联系、unsubscribe 和商业邮件边界 |
| FCC, Telemarketing and robocalls | https://www.fcc.gov/general/telemarketing-and-robocalls | 支撑电话和短信联系、robocall/robotext consent 风险 |

## 75. 本系统如何使用来源

来源进入系统有三种方式：

1. Markdown 文档：每个高风险专题末尾保留来源 URL。
2. `/sources` 页面：记录主题、能力、标题、URL、发布方、证据摘要、可信级别和复核状态。
3. `/risk-audits` 页面：每条上线前审计记录可绑定来源 URL，用于说明为什么放行、暂停、修复或拒绝。

验收标准：

- 每个高风险能力至少有 2 个来源 URL。
- 关键判断优先引用 Google 官方政策、Google 官方开发文档、MDN/OWASP/W3C 等基础资料。
- 产品公开页面只用于拆解功能宣称，不作为合规判断的唯一依据。
- `/sources` 里的 candidate、accepted、needs_update、archived 只表示来源复核状态；accepted 可以作为文档引用证据，但不自动放行任何广告后台动作。
- 对任何高风险能力，只沉淀原理、风险、识别思路和合规替代，不沉淀可执行规避步骤。

相关运营知识见 [Ads 套利业务模式拆解手册](ads_arbitrage_business_models.md)、[Ads 套利运营手册](ads_arbitrage_operations.md)、[Search Arbitrage、Feed 与 Parking 模式手册](search_arbitrage_feed_parking.md)、[RSOC / N2S、Search Feed Partner 与相关搜索套利治理手册](rsoc_n2s_search_feed_partner_governance.md)、[关键词、搜索意图与选题研究手册](keyword_intent_research.md)、[Search Terms、否定词与 Query Mining 治理手册](search_terms_negative_keyword_query_mining.md)、[品牌词、商标与竞品投放合规手册](brand_bidding_trademark_competitor_policy.md)、[买量渠道与流量供应商尽调手册](traffic_channel_vendor_due_diligence.md)、[Google Ads 流量库存、版位与排除控制手册](traffic_inventory_controls.md)、[Source、Publisher、Placement 质量评分与名单治理手册](source_publisher_placement_quality_governance.md)、[受众定向、再营销与 Customer Match 合规手册](audience_remarketing_customer_match_policy.md)、[Affiliate Network / Lead Buyer 尽调与条款手册](affiliate_network_due_diligence.md)、[Lead 质量、Postback 对账与拒付管理手册](lead_quality_postback_reconciliation.md)、[Lead Form、电话线索、Call Tracking 与 TCPA 风险手册](lead_form_call_tracking_tcpa_compliance.md)、[Ping/Post、Lead Buyer Routing 与线索市场治理手册](ping_post_lead_marketplace_buyer_routing.md)、[Lead 验证、Suppression、去重与 PII 治理手册](lead_validation_suppression_pii_governance.md)、[实验设计、样本量与优化决策手册](experiment_design_optimization.md)、[无效流量识别、异常监控与来源隔离 SOP](invalid_traffic_detection_sop.md)、[异常监控、告警、止损队列与事故分诊手册](anomaly_monitoring_alerting_stoploss_incident_triage.md)、[内容生产、页面可信度与编辑质量手册](content_production_editorial_quality.md)、[敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)、[流量源与追踪归因手册](traffic_source_tracking.md)、[Native、Advertorial 与 Presell Page 套利手册](native_advertorial_presell_compliance.md)、[Click -> Session -> Revenue 对账 SOP](click_session_revenue_reconciliation.md)、[Campaign 命名、Labels、UTM/SubID 与维度治理手册](campaign_taxonomy_naming_label_dimension_governance.md)、[转化追踪、价值回传与 Attribution 手册](conversion_tracking_value_feedback.md)、[落地页质量、广告密度与 MFA 风险手册](landing_page_quality_mfa.md)、[域名、站点资产与站群治理手册](domain_site_asset_governance.md)、[落地页素材抽取、Offer Intelligence 与创意 Brief 手册](landing_offer_intelligence_creative_brief.md)、[回款、结算与现金流风险手册](cashflow_settlement_risk.md)、[发布商收入对账、Finalized Revenue 与扣量复盘手册](revenue_reconciliation_adstack.md)、[广告创意生成、测试与优化手册](creative_testing_optimization.md)、[广告创意 Claim 审核与事实核查手册](creative_claim_review_fact_checking.md)、[AI Provider、Prompt 模板与创意成本治理手册](ai_provider_prompt_cost_governance.md)、[链接计划与换链接合规手册](link_rotation_compliance.md)、[Google Ads 投放结构与安全自动化手册](campaign_launch_automation.md)、[任务编排、安全审批、执行日志与事故复盘手册](task_orchestration_approval_audit_runbook.md)、[Google Ads 竞价、Quality Score 与套利出价手册](google_ads_auction_bidding_quality_score.md)、[Google Ads 报表诊断、Search Terms 与 Change History 手册](google_ads_reporting_diagnostics.md)、[Search 自动化流量：AI Max、Broad Match 与 DSA 套利风险手册](search_automation_ai_max_broad_match.md)、[Performance Max / Demand Gen 自动化流量与套利风险手册](performance_max_demand_gen_automation.md)、[Geo、语言、本地化、时区与币种分层手册](geo_language_localization_currency.md)、[预算节奏、扩量与止损手册](budget_pacing_scaling_stoploss.md)、[账号、MCC、付款与 Advertiser Verification 治理手册](account_mcc_billing_verification_governance.md)、[账号健康、政策中心与申诉 SOP](policy_account_health_sop.md)、[AdSense 站点审核、Policy Center 与广告投放限制手册](adsense_site_approval_policy_center.md)、[发布商变现栈：AdSense / AdX / Google Ad Manager 手册](publisher_monetization_stack.md)、[发布商广告质量、阻止控制与品牌安全手册](publisher_ad_quality_blocking_controls.md)、[程序化供应链透明度：ads.txt / sellers.json / schain 手册](programmatic_supply_chain_transparency.md)、[GAM / AdX Yield、Floor Price 与 Pricing Rules 手册](gam_adx_yield_floor_pricing.md)、[Header Bidding / Prebid.js 与广告栈延迟手册](header_bidding_prebid_ad_stack.md)、[广告位、刷新、可见率与页面体验手册](ad_placement_refresh_viewability.md) 和 [隐私、Consent 与追踪合规手册](privacy_consent_tracking.md)，其中把来源用于模式判断、search feed/parking 评估、RSOC、N2S、Related Search、PIF、RAC、Feed partner、query intent、关键词意图、search terms、negative keywords、query mining、品牌词/商标审计、渠道尽调、Source Quality Score、allowlist/watchlist/quarantine/blocklist、停源恢复、Native、Advertorial、Presell Page、source quality、publisher quality、placement quality、buyer feedback、disclosure、FTC native advertising、库存/版位控制、AI Max、Broad Match、Dynamic Search Ads、automatically created assets、Search automation controls、AI Provider、Prompt 模板、prompt injection、LLM 成本、人工审核、Performance Max、Demand Gen、Final URL expansion、Search themes、Audience signals、Brand exclusions、Channel performance、placement report、PMax 排除、受众/再营销/Customer Match 审计、联盟条款、lead 质量、postback 对账、拒付管理、Lead Form、电话线索、Call Tracking、TCPA、DNC、录音披露、buyer handoff、Ping/Post、buyer routing、exclusive/shared/aged lead、cap snapshot、no buyer、lead validation、suppression、duplicate、PII 最小化、retention/deletion、实验决策、无效流量隔离、异常监控、告警分级、止损队列、事故分诊、内容质量、敏感垂类准入、真实追踪、click/session/revenue 对账、命名维度、Labels、UTM、ValueTrack、custom parameter、subid、报表 join key、转化追踪、价值回传、页面质量、域名资产、过期域名、site reputation abuse、site migration、Final URL change、账号/MCC、payments profile、account budget、Advertiser Verification、访问权限、代理关系、素材证据抽取、claim/proof 创意核查、强声明事实核查、finalized revenue 对账、扣量复盘、task orchestration、approval、execution log、idempotency、retry、Change history、Scripts log、incident response、postmortem、search terms、Auction Insights、Change history、Report Editor、landing page report、asset report、bid strategy report、Geo、language、localization、location options、bad geo、timezone、currency、fx rate、site review、Policy Center、ad serving limits、traffic segmentation、blocking controls、Ad review center、sensitive categories、advertiser URL block、brand safety、ads.txt、sellers.json、schain、授权卖方、floor price、pricing rules、Open Bidding、Header Bidding、Prebid.js、bidder、auction timeout、price granularity、广告栈延迟、fill/eCPM、广告位、Ad refresh、viewability、CLS、预算节奏、dayparting、geo/device 分层、对账、止损、回款、创意人审、链接变更、投放结构、竞价出价、申诉证据、广告位变现、Consent 和事故复盘。

CPL 垂类经济专题另见 [CPL 垂类经济、资格问题与 Buyer Acceptance 手册](cpl_vertical_economics_qualification_playbook.md)，用于解释 insurance、loan/debt、legal、home services、education、healthcare、B2B lead 的 qualification fields、buyer acceptance、reject reason、feedback lag、Vertical Fit Score 和垂类测试模板。

Lead Pricing 专题另见 [Lead Pricing、Payout Negotiation 与结算安全垫治理手册](lead_pricing_payout_negotiation_governance.md)，用于解释 raw CPL、qualified CPL、pay-per-call、appointment、CPA、revshare、effective payout、scrub buffer、floor、tier、cap、rate card 和谈价证据。

Speed-to-Lead 专题另见 [Speed-to-Lead、联系策略、坐席容量与 SLA 治理手册](speed_to_lead_contact_sla_governance.md)，用于解释 first attempt SLA、contact cadence、call disposition、call center capacity、DNC/opt-out sync、call reporting、qualified call 和 Contact Quality Score。

Buyer Capacity 专题另见 [Buyer Capacity、Cap Pacing 与 Dayparting 治理手册](buyer_capacity_cap_pacing_dayparting_governance.md)，用于解释 buyer capacity、cap snapshot、cap reset、operating hours、holiday calendar、ad schedule、overdelivery、no buyer、fallback、timezone 和 Capacity Quality Score。

Appointment Lead 专题另见 [Appointment Lead、Booking、Show Rate 与 No-show 治理手册](appointment_lead_booking_show_rate_governance.md)，用于解释 submitted、booked、confirmed、showed、completed、paid、calendar capacity、reminder、show rate、cancel/no-show、offline conversion value 和 Booking Quality Score。

Lead Form 漏斗专题另见 [Lead Form 漏斗、资格问题与移动端 UX 治理手册](lead_form_funnel_qualification_ux.md)，用于解释 form version、字段用途、分步表单、qualification questions、disclosure/consent/CTA、mobile UX、abandon/error、buyer feedback 和 Form Funnel Quality Score。

Lead Consent Proof 专题另见 [Lead Consent Proof、TrustedForm / Jornaya 与证据链治理手册](lead_consent_proof_certificate_evidence_governance.md)，用于解释 consent proof、TrustedForm、Jornaya、certificate、LeadID、page snapshot、buyer disclosure、suppression、handoff evidence 和 dispute evidence pack。

Call Tracking 专题另见 [Call Tracking Number Pool、DNI 与电话归因治理手册](call_tracking_dni_number_pool_attribution_governance.md)，用于解释 Google forwarding number、third-party DNI、number pool、call log join key、IVR/转接链、recording/PII、call conversion mapping 和 Call Attribution Quality Score。

Pay-per-call 专题另见 [Pay-per-call、Call Buyer Routing 与 Duration Payout 治理手册](pay_per_call_buyer_routing_duration_payout_governance.md)，用于解释 call buyer、target、routing plan、IVR、buyer cap/hours、duplicate caller、qualified duration、duration payout、buyer disposition 和 Call Buyer Quality Score。

Lead Freshness 专题另见 [Lead Freshness、Aged Lead 与 Recontact Window 治理手册](lead_freshness_aged_recontact_governance.md)，用于解释 lead freshness、lead age bucket、fresh/same-day/aged/recycled lead、recontact window、consent refresh、suppression、payout tier、aged revenue attribution 和 Freshness Quality Score。

Insurance Lead 专题另见 [Insurance、Medicare / ACA 与 Final Expense Lead 治理手册](insurance_medicare_aca_final_expense_lead_governance.md)，用于解释 insurance lead、Medicare lead、ACA / Marketplace lead、final expense lead、qualification fields、licensed agent/broker、enrollment window、buyer acceptance、reject reason、consent proof、Google Ads health insurance policy、CMS/Marketplace/Medicare marketing、offline value mapping 和 Insurance Lead Quality Score。

Loan / Debt Lead 专题另见 [Loan、Mortgage、Credit 与 Debt Lead 治理手册](loan_mortgage_credit_debt_lead_governance.md)，用于解释 personal loan、mortgage/refinance、HELOC、credit card、debt relief、credit repair、student loan relief、qualification fields、financial disclosure、licensed lender/broker/lead generator、CFPB comparison-shopping、FCRA/ECOA/TILA、Google Ads HEC / Personalized Ads、buyer acceptance、reject reason、offline value mapping 和 Financial Lead Quality Score。

Legal Lead 专题另见 [Legal Case Intake、Mass Tort 与 Personal Injury Lead 治理手册](legal_case_intake_mass_tort_lead_governance.md)，用于解释 legal lead、personal injury、mass tort、case intake、practice area、jurisdiction、incident date、representation status、attorney/law firm/intake center/lead generator 边界、lawyer advertising、solicitation、confidentiality、retainer signed、case accepted、offline value mapping 和 Legal Lead Quality Score。

Home Services / Solar Lead 专题另见 [Home Services、Solar 与 Local Services Lead 治理手册](home_services_solar_local_services_lead_governance.md)，用于解释 home services lead、solar lead、local services lead、service area、contractor license/insurance、dispatch capacity、emergency lead、Google Local Services Ads、charged lead、credit/dispute、job booked、showed/dispatch、quoted、sold/completed、solar savings claim 和 Home Services Lead Quality Score。

Education Lead 专题另见 [Education、Career Training 与 Student Lead 治理手册](education_career_training_student_lead_governance.md)，用于解释 education lead、career training lead、student inquiry、program interest、school type、state authorization、accreditation、licensure、transferability、job placement、salary claim、financial aid、student loan、admissions eligibility、buyer acceptance、enrollment funnel、offline value mapping 和 Education Lead Quality Score。

Healthcare Lead 专题另见 [Healthcare、Medical Appointment 与 Clinic Lead 治理手册](healthcare_medical_appointment_lead_governance.md)，用于解释 healthcare lead、medical appointment、dental、vision、mental health、urgent care、specialist、telehealth、clinic lead、PHI、HIPAA/tracking、health claim、provider eligibility、insurance/payment fit、appointment showed/treated/paid 和 Healthcare Lead Quality Score。

B2B SaaS Lead 专题另见 [B2B SaaS、Professional Services 与 Demo Lead 治理手册](b2b_saas_professional_services_lead_governance.md)，用于解释 B2B SaaS lead、professional services lead、demo request、trial、webinar、ICP、firmographic qualification、role/persona、buyer committee、MQL/SAL/SQL/opportunity/won、PQL、competitor query、software policy、customer logo/review/security claim 和 B2B Lead Quality Score。

Crypto / Investment Lead 专题另见 [Crypto、Investment 与 Trading Lead 治理手册](crypto_investment_trading_lead_governance.md)，用于解释 crypto lead、investment lead、trading lead、Google crypto / financial / complex speculative product policy、certification、license/registration、jurisdiction、risk disclosure、fraud red flags、KYC、funded account、first trade、paid value 和 Crypto / Investment Lead Quality Score。

Employment Lead 专题另见 [Employment、Recruiting 与 Staffing Lead 治理手册](employment_recruiting_staffing_lead_governance.md)，用于解释 employment lead、job applicant lead、staffing lead、real job order、employer authorization、ghost job、HEC / employment targeting、job scam、work-from-home、business opportunity、EEOC recruiting、pay/remote claim、resume privacy、background check、interview/hire/start/paid 和 Employment Lead Quality Score。

Gambling Lead 专题另见 [Gambling、Sweepstakes 与 Sports Betting Lead 治理手册](gambling_sweepstakes_sports_betting_lead_governance.md)，用于解释 gambling lead、sportsbook、casino、sweepstakes casino、social casino、fantasy sports、Google gambling certification、license/jurisdiction、age gate、geolocation、self-exclusion、responsible gambling、bonus terms、sweepstakes rules、KYC/deposit/wager/NGR/paid 和 Gambling Lead Quality Score。

Addiction Treatment Lead 专题另见 [Addiction Treatment、Rehab 与 Behavioral Health Lead 治理手册](addiction_treatment_rehab_behavioral_health_lead_governance.md)，用于解释 addiction treatment lead、drug rehab lead、detox、residential、IOP/PHP、OTP、MAT/MOUD、LegitScript / Google certification、provider/referral role、crisis handling、Part 2 / HIPAA tracking、patient brokering、admissions call、clinical assessment、insurance verification、admitted/started/paid 和 Addiction Lead Quality Score。

Government Services Lead 专题另见 [Government Services、Immigration 与 Public Benefits Lead 治理手册](government_services_immigration_public_benefits_lead_governance.md)，用于解释 government services lead、immigration、passport、visa、DMV、vital records、Social Security、tax / IRS help、public benefits、government grants、official relationship、Google government documents and services policy、certification、notario scam、authorized representative、official fee、identity data、application filed、issued document、paid after refund window 和 Government Services Lead Quality Score。

Google Ads Scripts 同步专题另见 [Google Ads Scripts 数据同步、快照与一致性手册](google_ads_scripts_data_sync_consistency.md)，用于解释 15 分钟同步、报表快照、窗口重拉、冲突治理、数据新鲜度和 ChangeEvent 证据链。

Google Ads Editor / Bulk Upload 专题另见 [Google Ads Editor CSV 与 Bulk Upload 批量变更治理手册](google_ads_editor_csv_bulk_upload_governance.md)，用于解释离线批量变更、CSV 字段合同、发布前检查、行级错误、Change history 和回滚治理。

Google Ads 广告审核专题另见 [Google Ads 广告审核、拒登、Policy Manager 与申诉证据包手册](google_ads_ad_review_disapproval_appeal_playbook.md)，用于解释广告级审核、policy topic、拒登修复、申诉证据包和复盘治理。

单位经济专题另见 [单位经济模型、Break-even 与安全边际手册](unit_economics_margin_safety.md)，用于解释 RPV/EPC、break-even CPC、safe CPC、safety margin、safety factor、sensitivity analysis、test budget、hard stop 和出价策略映射。

Google Ads Recommendations / Experiments 专题另见 [Google Ads Recommendations、Experiments 与 Auto-apply 优化治理手册](google_ads_recommendations_experiments_auto_apply_governance.md)，用于解释 optimization score、recommendations、auto-apply、实验设计、Change History 和套利优化建议评审。

Creative Angle Library 专题另见 [Creative Angle Library、素材版本与反馈闭环手册](creative_angle_library_feedback_loop.md)，用于解释 angle、素材版本、asset report、paid revenue、拒登、扣量、buyer feedback 和 prompt 回写闭环。

竞品广告情报专题另见 [竞品广告、SERP 与 Ads Transparency 情报手册](competitor_ad_intelligence_serp_transparency.md)，用于解释 Ads Transparency Center、Ad Preview、Auction Insights、SERP 采样、竞品素材拆解和合规边界。

Campaign 命名维度治理专题另见 [Campaign 命名、Labels、UTM/SubID 与维度治理手册](campaign_taxonomy_naming_label_dimension_governance.md)，用于解释 campaign/ad group 命名、Labels、UTM、ValueTrack、custom parameter、subid、version hash 和 report join key。

归因增量专题另见 [归因、增量性与流量蚕食治理手册](attribution_incrementality_cannibalization.md)，用于解释 attribution credit、incrementality、cannibalization、holdout、lift、iROAS、brand/organic/remarketing/PMax 蚕食和增量实验。

转化信号质量专题另见 [转化信号质量与出价学习治理手册](conversion_signal_quality_bidding_learning_governance.md)，用于解释 Signal Quality Score、primary/secondary、value feedback、offline conversion、Enhanced Conversions、Smart Bidding learning、bid strategy report、自动出价准入和信号事故响应。

CRM 阶段映射专题另见 [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md)，用于解释 CRM stage、buyer status、conversion action mapping、value mode、transaction_id、conversion adjustment、import batch QA、diagnostics 和 lag profile。

决策窗口专题另见 [决策窗口、回传延迟与收入延迟治理手册](decision_window_revenue_lag_governance.md)，用于解释 data freshness、conversion lag、revenue lag、cohort maturity、Decision Window Score、stop-loss、wait-loss、budget ramp 和 settlement close。

Seasonality 专题另见 [季节性、事件日历与需求预测手册](seasonality_event_demand_forecasting.md)，用于解释 event calendar、Google Trends、Keyword Planner、Insights、demand forecast、readiness gate、budget ramp、seasonality adjustment 和 post-peak exit。

Portfolio 专题另见 [Portfolio 预算分配、风险集中度与组合治理手册](portfolio_budget_allocation_risk_concentration.md)，用于解释 Core、Scale、Test、Explore、Quarantine、concentration exposure、correlation exposure、revenue status mix 和 allocation score。

异常监控专题另见 [异常监控、告警、止损队列与事故分诊手册](anomaly_monitoring_alerting_stoploss_incident_triage.md)，用于解释 alert rule、severity、stop-loss queue、evidence pack、incident triage、Change History、conversion lag 和 postmortem。

Search Terms 专题另见 [Search Terms、否定词与 Query Mining 治理手册](search_terms_negative_keyword_query_mining.md)，用于解释 search terms report、search terms insights、negative keywords、query drift、query promotion、query sculpting 和 paid revenue 决策。

Offer Cap / Payout 专题另见 [Offer Cap、Payout、状态变更与替代 Offer 治理手册](offer_cap_payout_status_governance.md)，用于解释 cap pacing、payout version、offer status、buyer capacity、replacement offer、paid revenue 和预算联动。

订阅 LTV 专题另见 [订阅、试用、退款、Chargeback 与 LTV 治理手册](subscription_refund_ltv_chargeback_governance.md)，用于解释 trial、subscription、renewal、refund、chargeback、clawback、negative option、cancellation disclosure、cohort LTV 和 net value feedback。

Source Quality 专题另见 [Source、Publisher、Placement 质量评分与名单治理手册](source_publisher_placement_quality_governance.md)，用于解释 source、publisher、placement、subid、buyer feedback、Source Quality Score、allowlist、watchlist、quarantine、blocklist、停源恢复和排除清单治理。

Vendor Contract 专题另见 [流量供应商合同、IO、退款与争议治理手册](traffic_vendor_contract_io_dispute_governance.md)，用于解释 traffic vendor、publisher direct buy、IO、tracking appendix、reporting appendix、discrepancy、refund、credit、makegood 和 dispute evidence。

Lead Buyer 合同专题另见 [Lead Buyer 合同、IO、Accepted / Qualified / Paid 口径治理手册](lead_buyer_contract_io_paid_definition_governance.md)，用于解释 accepted、qualified、billable、approved、paid、return window、scrub、buyer postback、invoice、payment 和 dispute evidence。
