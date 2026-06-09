# 链接计划与换链接合规手册

更新时间：2026-06-08

本文解释 Ads 套利中的链接维护、追踪参数更新、Offer URL 替换、落地页版本切换和“换链接”风险。合规换链接的目标是修复不可用页面、更新追踪、替换过期 Offer、做可解释实验；不合规换链接通常会变成 cloaking、隐藏真实目的地、审核页/用户页不一致或规避政策执行。本文不提供 cloaking、Bot 分流、审核绕过、按 IP/指纹/账号状态切换页面或封禁规避方案。

## 1. 链接层级

套利链路里至少有 5 层 URL：

| 层级 | 说明 | 风险 |
| --- | --- | --- |
| Display URL | 广告里展示给用户的域名 | 与最终页面域名不一致会造成误导 |
| Final URL | Google Ads 中的真实落地页 | 页面不可达、内容不一致、桥页会触发目的地问题 |
| Tracking template | 记录点击、参数和归因 | 不能用于隐藏真实目的地或分流审核 |
| Landing page URL | 用户实际看到的页面 | 内容必须兑现广告承诺 |
| Offer / monetization URL | 页面 CTA 或广告链接后的变现目的地 | 不能伪装、误导、强制跳转或隐瞒关系 |
| Postback URL | 联盟/追踪系统转化回传 | 只用于真实归因，不能制造转化 |

“换链接”要先说清楚换的是哪一层。把 Final URL、tracking template、页面 CTA、Offer URL 和 postback URL 混在一起，是很多事故的起点。

## 2. 合理换链接场景

合规且常见的换链接：

- Offer 到期或广告主暂停，需要替换为同类、同承诺、同政策边界的 Offer。
- 原落地页 404、证书失效、移动端不可用，需要切换到修复页。
- 追踪参数模板错误，需要修复 UTM、ValueTrack、click_id 或 subid。
- 页面 A/B 测试，用户和审核方都可访问同类真实内容。
- 目标国家、价格、隐私条款、披露信息更新。
- 广告承诺更新，需要同步 Final URL 和页面内容。
- 变现方要求更换 tracking domain，但最终目的地不变。

高风险或禁止的换链接：

- 审核时给一个页面，审核后给用户另一个页面。
- 对 Google AdsBot、搜索引擎、特定 IP、登录 Cookie、设备指纹展示不同目的地。
- 被拒登或封禁后换域名、换账号继续同一违规内容。
- 把广告承诺指向一个干净页面，再把用户自动转到不相关 Offer。
- 隐藏多跳跳转链、无法解释最终目的地。
- 为规避无效流量、关联检测、政策审核而动态切换。

## 3. 目的地一致性原则

换链接前后都必须满足：

```text
广告文案 -> Display URL -> Final URL -> Landing page -> CTA/Offer
```

这条链路里的承诺、主体、国家、语言、价格、服务、披露和下一步行动要一致。

检查点：

- 广告说“比较云备份方案”，页面就必须是云备份比较或相关工具。
- Display URL 域名和 Final URL 域名不能让用户误认。
- Tracking template 最终展开后仍到同一页面类型。
- CTA 后的 Offer 不应突然变成无关垂类。
- 如果页面里有联盟/广告关系，应明确披露。
- 如果 Offer 不再可用，广告和页面都要同步暂停或重写。

## 4. 链接变更流程

推荐流程：

| 步骤 | 动作 | 输出 |
| --- | --- | --- |
| 1 | 记录变更原因 | offer_expired / tracking_fix / page_test / outage |
| 2 | 确认影响范围 | campaign、ad group、creative、source、country、device |
| 3 | 审核新 URL | 可访问、HTTPS、移动端、政策、内容一致 |
| 4 | 验证追踪参数 | UTM、ValueTrack、click_id、subid、postback |
| 5 | 做风险审计 | 是否涉及 cloaking、目的地不一致、桥页、误导 |
| 6 | 人工批准 | 记录审批人、时间、证据 |
| 7 | 导出或手动更新 | CSV / Scripts JSON / Google Ads Editor |
| 8 | 小流量观察 | 检查 session、收入、拒登、扣量和报错 |
| 9 | 归档历史 | 旧 URL、新 URL、截图、来源 URL、变更结果 |

变更理由必须可审计。不能只写“防封”“过审”“换干净链接”“避关联”。

## 5. 链接测试清单

上线前测试：

| 测试项 | 通过标准 |
| --- | --- |
| HTTP 状态 | 200 或合理跳转，不能 404/5xx |
| HTTPS | 证书有效，无混合内容阻塞 |
| 移动端 | 页面可读、按钮可点、广告不遮挡 |
| 目标国家 | 目标地区能访问，非目标地区有清晰说明 |
| Google Ads URL test | Tracking template 能成功展开到 Final URL |
| 参数保留 | UTM、ValueTrack、click_id、subid 不丢 |
| 页面一致 | 审核和普通用户看到同类内容 |
| CTA | CTA 后 Offer 与页面承诺一致 |
| 回传 | postback 能用真实 click_id 匹配转化 |
| 日志 | 变更写入审计记录 |

## 6. 轮换和 A/B 测试

正常 A/B 测试：

- 用户随机或按实验设置看到 A/B 页面。
- A/B 页面都是真实内容，主题和承诺一致。
- 流量分配、页面版本、指标和结论可记录。
- 不按审核方身份、Bot、IP、指纹或 Cookie 切换。
- 实验结束后把失败版本下线或保留证据。

高风险轮换：

- Google AdsBot 看 A，真实用户看 B。
- 新用户看内容页，老用户看高风险 Offer。
- 特定国家/设备/浏览器被送到完全不同垂类。
- 被拒登后只换域名，不修复页面问题。
- 根据账号状态、cookie、代理或 fingerprint 做分流。

关键判断：如果切换逻辑的目的是用户体验、实验或故障恢复，且所有版本都合规可审核，通常可管理；如果切换逻辑的目的是让审核或平台看不到真实用户目的地，就是红线。

## 7. 事故处理

发现链接事故时：

1. 立即暂停受影响 campaign/ad group/link rule。
2. 保存当前广告、Final URL、tracking template、页面截图和服务器日志。
3. 按 source/campaign/device/geo 计算影响范围。
4. 修复 URL 或回滚到最后一个已验证版本。
5. 导入事故期间指标，检查 click -> session、revenue、扣量。
6. 若有政策或无效流量提醒，记录到 `/risk-audits`。
7. 做复盘：原因、影响、修复、预防、是否永久停用供应方或 Offer。

不要在事故中继续“试换链接”碰运气。未验证链接会把小事故变成账号级风险。

## 8. 本系统如何落地

| 行业动作 | 系统位置 |
| --- | --- |
| 记录 Offer 和 tracking URL | `/offers` |
| 记录 Campaign final URL | `/campaigns` |
| 创建合规链接轮换计划 | `/links` |
| 人工执行轮换并写日志 | `/links/<id>/rotate` |
| 记录风险、来源 URL 和修复证据 | `/risk-audits`、`/sources` |
| 通过任务中心安排 URL 定期检查 | `/tasks` |
| 追踪每次变更 | `/logs` |

系统设计选择：

- 默认 `require_manual_review=True`。
- 只把候选 URL 存为计划，不自动接管 Google Ads 后台。
- 链接计划需要先进入 `approved` 状态，才能执行人工轮换；draft、reviewing、paused 和 rejected 状态不能轮换。
- 轮换写入审计日志。
- 不根据 IP、Bot、Cookie、指纹、登录状态做分流。
- 不实现审核页/用户页不一致。

## 9. 链接变更模板

```text
变更名称：
变更日期：
影响范围：
旧 URL：
新 URL：
变更层级：Final URL / Tracking template / Landing CTA / Offer URL / Postback
变更原因：

页面一致性检查：
移动端检查：
追踪参数检查：
Offer 限制检查：
政策来源 URL：
审批人：

上线后 24h 指标：
Click：
Session：
Revenue：
Reject/Deduction：
Policy warning：

结论：
保留 / 回滚 / 继续灰度 / 暂停
```

## 10. 信息来源 URL

- Google Ads Help, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Help, Destination experience: https://support.google.com/adspolicy/answer/16427615
- Google Ads Help, Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Google Ads Help, Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Google Ads Help, About tracking in Google Ads: https://support.google.com/google-ads/answer/6076199
- Google Ads Help, About ValueTrack parameters: https://support.google.com/google-ads/answer/2375447
- Google Ads Help, Set up tracking with ValueTrack parameters: https://support.google.com/google-ads/answer/6305348
- Google Ads Editor Help: https://support.google.com/google-ads/editor
- Google Ads Scripts start guide: https://developers.google.com/google-ads/scripts/docs/start
- Google Search Central, Spam policies: https://developers.google.com/search/docs/essentials/spam-policies
