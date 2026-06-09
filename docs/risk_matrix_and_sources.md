# 高风险能力风险矩阵与来源索引

更新时间：2026-06-09

本文把 6 个高风险能力整理成一张可执行风险矩阵，并记录每类能力的主要信息来源 URL。它用于投放前审计、团队培训和复盘。

## 1. 风险矩阵

| 能力 | 业务诉求 | 风险级别 | 主要风险 | 系统控制 |
| --- | --- | --- | --- | --- |
| Ads Cookie 登录和后台操作 | 绕过 API 审批、复用已登录状态、批量操作后台 | 高 | 账号接管、会话泄露、授权不可控、审计缺失 | 禁止存储 Cookie；使用 CSV / Scripts JSON / 官方 API |
| 自动绕过登录、2FA、安全挑战 | 多账号无人值守、减少人工验证 | 高 | 对抗账号安全、未授权访问、责任边界不清 | 人工审核队列、权限管理、授权脚本 |
| 补点击、刷展示、模拟自然流量 | 伪装流量质量、弥补追踪断点、制造互动 | 高 | 无效流量、扣量、账号限制、广告主损失 | 指标导入、异常分析、真实来源隔离 |
| 代理、指纹、Worker 转发规避关联检测 | 多账号隔离、隐藏操作来源、规避关联 | 高 | 规避系统、资产扩大受损、供应商风险 | 账号配置记录、真实业务隔离、审计日志 |
| Cloaking 或审核页/用户页不一致 | 提高审核通过率、隐藏真实 Offer | 高 | 审核规避、拒登、封禁、用户投诉 | 合规链接计划、人工确认、URL 版本记录 |
| 为规避封禁创建或切换账号 | 受限后继续投放、分散高风险 Offer | 高 | 快速关联、资产受损、原问题扩大 | 账号状态备注、复盘、修复证据、申诉流程 |

## 2. 审计字段

每条风险审计记录至少包含：

- Offer 或 Campaign。
- 能力类型。
- 风险级别。
- 发现的问题。
- 处理方案。
- 来源 URL。
- 状态：open、reviewed、mitigated、rejected。

来源 URL 建议同步进入 `/sources` 来源库，补充来源标题、发布方、可信级别和证据摘要。风险审计里的 URL 用于解释单条审计为什么成立；来源库用于长期维护行业知识。`/risk-audits` 支持把记录标记为 open、reviewed、mitigated 或 rejected，状态更新会写入审计日志；状态不等于自动放行，高风险动作仍必须按暂停、修复或拒绝处理。

## 3. 审计判断标准

### 3.1 高风险

满足任一条件就标记为 high：

- 涉及登录态、Cookie、Session Token、浏览器 Profile。
- 涉及绕过 2FA、安全挑战或账号限制。
- 涉及人工或自动制造广告点击、展示、会话。
- 涉及审核页和用户页不一致。
- 涉及封禁后创建或切换账号继续相同业务。

### 3.2 中风险

满足任一条件可标记为 medium：

- URL 轮换原因不清楚。
- 代理、Worker、脚本同步用途不清楚。
- 页面和广告承诺存在轻微不一致。
- 指标出现高 CTR 低 RPV、低停留、无收入消耗。
- 账号配置缺少负责人或同步方式说明。

### 3.3 低风险/信息

满足以下情况可标记为 info：

- 仅做资料学习。
- 仅记录来源。
- 已有明确合规替代方案。
- 已完成复盘并关闭。

## 4. 来源索引

### 4.1 Google Ads 政策

- Advertising network abuse: https://support.google.com/adspolicy/answer/6008942
- Circumventing systems: https://support.google.com/adspolicy/answer/15938075
- Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Secure your Google Ads account: https://support.google.com/google-ads/answer/2375456
- Google Ads account access levels: https://support.google.com/google-ads/answer/9978556
- Fix a suspended Google Ads account: https://support.google.com/google-ads/answer/2375414

### 4.2 Google Ads 官方自动化

- Google Ads API overview: https://developers.google.com/google-ads/api/docs/start
- Google Ads API OAuth overview: https://developers.google.com/google-ads/api/docs/oauth/overview
- Google Ads Scripts start guide: https://developers.google.com/google-ads/scripts/docs/start
- Google Ads Scripts authorization: https://developers.google.com/google-ads/scripts/docs/authorization
- Google Ads Editor Help: https://support.google.com/google-ads/editor

### 4.3 AdSense / Publisher 流量质量

- Definition of invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Program policies: https://support.google.com/adsense/answer/48182
- Use of online advertising to get new users to the site: https://support.google.com/adsense/answer/1348727
- Google Publisher Policies: https://support.google.com/publisherpolicies/answer/10437486
- How Google prevents invalid traffic: https://support.google.com/adsense/answer/1348752

### 4.4 Web 安全和技术背景

- MDN, HTTP cookies: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
- MDN, Set-Cookie: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
- Google Search Central spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Cloudflare Workers documentation: https://developers.cloudflare.com/workers/
- EFF Cover Your Tracks: https://coveryourtracks.eff.org/learn
- W3C TAG, Unsanctioned Web Tracking: https://www.w3.org/2001/tag/doc/unsanctioned-tracking/

### 4.5 产品公开页

- ADXKit homepage: https://adxkit.com/

产品公开页只用于分析其公开宣称的功能和市场定位，不用于证明这些功能的真实内部实现，也不作为合规判断的唯一依据。

## 5. 系统使用方式

进入 `风险审计` 页面：

1. 选择 Offer 或投放草稿。
2. 选择高风险能力类型。
3. 记录发现。
4. 写明处理方案。
5. 粘贴来源 URL。
6. 保存后进入审计日志。
7. 复核后更新状态：open 表示待处理，reviewed 表示已完成事实复核，mitigated 表示已有修复或替代流程，rejected 表示该需求被拒绝。

风险审计不是“放行工具”。如果发现 high 风险，默认动作应是暂停、修复或拒绝，而不是继续自动执行。

进入 `来源库` 页面：

1. 新增来源标题、URL、发布方和可信级别。
2. 绑定到对应高风险能力。
3. 写清该来源支撑的判断。
4. 后续写文档或审计时引用同一 URL。
