# 流量供应商合同、IO、退款与争议治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何管理 traffic vendor、publisher direct buy、newsletter sponsorship、native network、lead buyer、affiliate network 和其他媒体采购合作中的合同、Insertion Order、付款条款、质量条款、退款、credit、makegood、争议和证据包。目标是让“买流量”变成可审计、可停量、可追责、可复盘的商业流程；不是采购不可解释流量、隐藏来源、规避平台检测、补点击、刷展示、模拟自然流量或用供应商口头承诺替代质量证据。

说明：本文是运营和系统设计文档，不构成法律意见。正式合同应由具备资质的法务或律师审核。

## 1. 为什么合同和 IO 是套利风控资产

套利团队经常把精力放在 CPC、CTR、RPM、EPC 和 ROI 上，忽略采购条款。真实风险发生时，能不能追回损失，取决于合同和 IO 是否提前写清：

- 流量来源、publisher、placement、广告位、投放方式。
- 允许和禁止的流量类型。
- 是否允许 UTM、click_id、subid、server log 和第三方追踪。
- 是否能按 source / publisher / placement 停量。
- 无效流量、误点、bot、激励、低质 lead、错 geo、超 cap 的处理方式。
- 报表差异以哪个口径为准，差异超过多少进入争议。
- 退款、credit、makegood、扣款、发票和付款周期如何处理。
- 供应商临时换来源、换 placement、换 creative 或改 tracking 的责任。

没有这些条款，坏来源会从“可争议损失”变成“你自己买错流量”。合同和 IO 的意义不是把供应商管死，而是把风险边界、证据口径和停止条件提前写进合作结构。

## 2. 原理解释：流量合作是三条链路

任何流量采购合作都同时存在三条链路：

```text
traffic flow: 用户从哪里来，为什么点击，落到哪里
money flow: 预算、发票、付款、退款、credit、makegood
evidence flow: 报表、日志、截图、postback、沟通记录、争议证据
```

只签价格，不签证据，等于只管理 money flow；只看供应商点击报表，不看 server log 和 paid revenue，等于只看 traffic flow 的一小段；只在事故后翻聊天记录，等于没有 evidence flow。

一个可扩量的供应商合作，必须满足：

```text
合同定义边界
-> IO 定义本次投放
-> tracking appendix 定义字段
-> reporting appendix 定义口径
-> dispute process 定义争议窗口
-> quality clauses 定义退款和停源条件
```

## 3. 核心对象地图

| 对象 | 解释 | 套利治理作用 |
| --- | --- | --- |
| vendor | 供应商主体、媒体、网络、代理或中介 | 付款、责任和准入主体 |
| publisher | 实际媒体、站点、app、newsletter、channel | 判断流量语境和质量 |
| insertion order / IO | 某次投放的预算、时间、库存、价格和条款 | 采购执行文件 |
| line item | IO 下的国家、placement、format、device、价格和量 | 复盘和争议的最小商务单元 |
| flight | 投放起止日期和节奏 | 判断超投、欠投、暂停和 makegood |
| pricing model | CPM、CPC、CPA、CPL、flat fee、hybrid | 决定风险分配方式 |
| source_id / subid | 追踪维度 | 连接供应商报表、站内日志和收入 |
| tracking appendix | 参数和 postback 字段清单 | 解决报表差异和归因争议 |
| quality clause | 无效流量、禁止来源、停源和退款条款 | 决定坏流量能否追责 |
| discrepancy report | 买方、卖方、第三方和 server log 差异 | 进入争议和调整发票 |
| makegood / credit | 用补投或抵扣修复未达标投放 | 比现金退款更常见 |
| dispute case | 争议工单 | 保存证据、期限、责任和结论 |

## 4. 合作类型和条款重点

| 合作类型 | 常见场景 | 条款重点 | 高风险点 |
| --- | --- | --- | --- |
| Google Ads self-serve | Search、Display、PMax、Demand Gen | 平台政策、账单、无效点击、Change history | 不能把平台无效点击 credit 当成全部质量治理 |
| Native network | 推荐位、内容发现、publisher network | publisher/placement、素材审批、source 明细 | 标题党、低质 placement、MFA |
| Direct publisher buy | 媒体站点、newsletter、赞助位 | placement、受众、样例 URL、发送计划、makegood | 报表夸大、订阅来源不清 |
| Traffic vendor / broker | 流量包、二级媒体、push/pop 等 | 来源透明、禁止流量、停源、退款 | 不透明、bot、激励、代理、不可停量 |
| Affiliate network | CPA/CPL/CPS offer | allowed traffic、cap、postback、scrub、payment term | 事后拒付、条款传递不完整 |
| Lead buyer | 表单或电话 lead | consent、reject reason、exclusive/shared、refund | 投诉、重复 lead、错 geo |

条款越不透明，预算越小、证据要求越高、付款越靠后。不能接受“先跑，月底看情况”的合作方式。

## 5. IO 必备条款

每个 IO 至少应写清：

| 条款 | 必填内容 | 为什么重要 |
| --- | --- | --- |
| contracting party | 法律主体、联系人、付款信息 | 避免多层转包后无人负责 |
| campaign objective | traffic、lead、sale、newsletter click、awareness | 避免供应商用错误优化目标交付 |
| inventory / placement | site、app、newsletter、channel、publisher id、sample URL | 支撑来源透明和后续排除 |
| geography / language | 国家、州、省、语言 | 避免 bad geo 和 buyer reject |
| device / platform | desktop、mobile、tablet、app/web | 识别 mobile 误点和 app 风险 |
| creative / landing | 已批准素材、落地页、offer、tracking URL | 防止供应商私自换素材或目标页 |
| pricing | CPM、CPC、CPA、flat fee、预算上限 | 控制成本和付款口径 |
| flight dates | 开始、结束、暂停、恢复规则 | 判断超投、欠投和 makegood |
| pacing | daily cap、hourly cap、geo cap、source cap | 避免单日爆量和超 cap |
| tracking | UTM、click_id、subid、ValueTrack、postback | 争议和来源评分的基础 |
| reporting | 报表频率、字段、时区、交付方式 | 避免月底才发现问题 |
| quality standard | 禁止 bot、激励、自动浏览、隐藏来源、代理/指纹 | 质量和合规红线 |
| discrepancy threshold | 差异阈值、优先口径、争议窗口 | 决定如何调整发票和 credit |
| refund / credit / makegood | 触发条件、金额、使用期限 | 决定损失如何修复 |
| cancellation | 可取消条件、通知期、未交付预算处理 | 停源时不被锁死 |
| compliance | 平台政策、隐私、广告披露、行业法规 | 减少账号和法律风险 |
| evidence retention | 报表、日志、截图和沟通保存期限 | 争议复盘和审计 |

## 6. Tracking Appendix 和 Reporting Appendix

IO 正文不适合写太多字段细节，应附 tracking appendix：

```text
required_url_params:
  traffic_source
  vendor_id
  publisher_id
  placement_id
  source_id
  subid1..subid5
  campaign_id
  creative_id
  landing_version
  offer_id
  click_id
  device
  geo
  timestamp
```

reporting appendix 至少定义：

```text
date
timezone
vendor_id
publisher_id
placement_id
source_id
subid
campaign
creative
impressions
clicks
cost
invalid_clicks / filtered_clicks
sessions
conversions
approved_revenue
paid_revenue
reject_reason
refund / credit / makegood
```

原则：

- 不允许供应商删除 UTM、click_id、subid 或 referrer 来“提高匹配率”。
- 不允许供应商只给总点击和总成本。
- 不允许供应商拒绝 sample URL、placement 或 publisher 说明。
- 不允许供应商用“我们系统统计为准”覆盖所有 server log、postback 和 paid revenue 证据。

## 7. 质量条款和禁止流量

质量条款要明确禁止：

- bot、爬虫、自动浏览、流量交换、激励点击。
- 补点击、刷展示、模拟自然流量。
- 代理、指纹、VPN、数据中心流量伪装或 Worker 转发隐藏来源。
- 弹窗、强制跳转、误导按钮、广告伪装。
- 未披露的 sub-network 或未批准 publisher。
- 不符合 offer 条款的 brand bidding、adult、incent、push、pop、toolbars。
- 未经批准修改 creative、landing page、tracking URL 或 redirect chain。
- cloaking、审核页/用户页不一致、按 bot/IP/UA 分流页面。

质量条款同时应写清买方权利：

- 发现异常时可立即暂停相关 source / placement / campaign。
- 要求供应商在约定时间内提供明细、样例 URL、来源说明和原始报表。
- 对无效流量、错 geo、未批准来源、超 cap、未授权素材或追踪断裂申请 credit、makegood 或退款。
- 对重复违规供应商进入 blocklist，并拒绝未交付预算继续消耗。

## 8. 报表差异和口径

报表差异是常态，不是自动说明一方造假。常见差异来自：

| 差异 | 原因 |
| --- | --- |
| vendor clicks > server landings | 重复点击、无效点击、页面加载失败、跳转慢、预取 |
| server landings > GA4 sessions | consent、采样、脚本加载失败、session 定义不同 |
| clicks 有，conversions 无 | 低意图、页面不匹配、tracking 断裂、回传延迟 |
| conversions 有，approved revenue 低 | buyer reject、duplicate、bad geo、quality hold |
| estimated 好，paid 差 | 扣量、invalid traffic、refund、chargeback |
| invoice cost > approved spend | 超预算、未暂停、未扣除无效量 |

IO 应约定：

- 默认时区。
- 报表更新时间和最终结算窗口。
- 差异阈值，例如 clicks 或 cost 差异超过 10%-15% 进入争议。
- 以哪些数据为准，例如 server landing request、third-party tracker、platform invoice、postback、paid report。
- 无效点击、过滤点击、退款和 credit 如何体现在发票中。

套利团队不要用差异掩盖追踪问题，也不要用追踪问题向供应商无依据扣款。争议必须靠证据包。

## 9. Refund、Credit 和 Makegood

三者区别：

| 机制 | 含义 | 适用场景 | 风险 |
| --- | --- | --- | --- |
| refund | 退回现金 | 明确未交付、违规或无效流量 | 供应商可能拖延 |
| credit | 下次账单抵扣 | 长期合作、差异明确但不退现 | 依赖后续继续采购 |
| makegood | 补投等值库存 | 展示不足、发送失败、排期问题 | 低质补投可能制造新损失 |

触发条件建议：

- 未经批准的 source / publisher / placement。
- 违反禁止流量条款。
- click -> session 明显异常且供应商无法解释。
- 错 geo、错设备、错语言或超 cap。
- 供应商延迟暂停导致超预算。
- newsletter 未按约定发送或发送到错误列表。
- direct buy 未达到约定展示/点击/发送量。
- buyer feedback 证明特定 source 大量 duplicate、incentive、bad geo、complaint。

makegood 不能替代质量修复。低质量来源造成的损失，不应通过同一坏来源补投来解决。

## 10. 争议处理流程

建议流程：

```text
发现异常
-> 暂停相关 source / placement / line item
-> 锁定数据窗口和时区
-> 生成 discrepancy report
-> 收集 evidence pack
-> 向供应商开 dispute case
-> 约定回复截止时间
-> 结论：reject / credit / makegood / refund / blocklist / retest
-> 更新来源评分、合同备注和黑白名单
```

Evidence pack 包含：

- IO、合同、邮件确认、聊天记录和版本。
- campaign、line item、flight、预算和暂停时间。
- vendor report 原始文件和下载时间。
- server log、GA4、tracker、postback、Google Ads、AdSense/GAM/affiliate report。
- source_id、publisher_id、placement_id、subid、device、geo。
- creative、landing page、tracking URL、redirect chain、页面截图。
- buyer feedback、reject reason、invalid traffic、Policy Center、ad serving limit。
- 发票、付款、credit note、makegood 计划。

所有争议必须有 owner、status、金额、证据窗口和结论。不要只在聊天软件里解决。

## 11. 供应商评分和合同状态

供应商不只按 ROI 评分，还要按商务和执行能力评分：

```text
source_transparency       20
tracking_compliance       15
traffic_quality           20
reporting_reliability     15
dispute_responsiveness    10
payment_terms             10
policy_fit                10
```

合同状态建议：

| 状态 | 含义 |
| --- | --- |
| prospect | 未尽调，仅收集资料 |
| preapproved | 条款初步可接受，允许小预算 |
| active_test | 已有 IO，处于小测 |
| active_scale | 有稳定 paid 证据和争议处理记录 |
| watchlist | 报表、质量或响应存在问题 |
| suspended | 暂停采购，等待争议或修复 |
| blocked | 红线或重复事故，不再合作 |
| retired | 合作自然结束 |

任何 blocked 供应商不能通过改名、换销售、换链接继续测试，除非重新尽调并证明实际供给、主体和质量机制已经变化。

## 12. 系统落地

当前系统已实现 V1 供应商合同/争议工作台。`/vendor-contracts` 会把 vendor、vendor_type、IO、line item、contract status、pricing model、来源明细、tracking appendix、reporting appendix、quality clause、refund / credit / makegood clause、stop control、tracking completeness、report delay、reporting discrepancy、invalid traffic、buyer reject、budget cap、spend、approved / paid revenue、invoice、disputed amount、refund / credit、makegood、dispute response、payment terms、policy issue 和 source URLs 保存到 `vendor_contract_reviews`，并计算 Vendor Contract Score、risk_level、recommended_action、amount_at_risk、paid_roi、approved_roi、invoice_dispute_rate、credit_coverage_rate 和 blockers。

| 行业动作 | 系统位置 |
| --- | --- |
| 做供应商合同、IO 和争议评审 | `/vendor-contracts`，`vendor_contract_reviews` |
| 更新 preapproved / active_test / active_scale / watchlist / dispute_open / suspended / blocked 状态 | `/vendor-contracts/<id>/status`，写入 `/logs` |
| 记录供应商、IO、条款和来源资料 | `/sources` |
| 记录合同风险、争议、退款和停源动作 | `/risk-audits` |
| 用 source_score 参与机会测算 | `/calculators` |
| 导入每日成本、收入和质量结果 | `/metrics/import` |
| 把异常成本、无收入、低 RPV 转成建议 | `/optimization` |
| 创建人工复核任务 | `/tasks` |
| 保存换链接和停源相关审计 | `/logs` |

`vendor_contract_reviews` 的状态只代表内部审批、证据包和争议治理，不会自动采购流量、调用供应商 API、扣款、开 dispute、发送威胁邮件、改广告后台、补点击或安排 makegood 投放。表单文本如果包含 Cookie、cloaking、隐藏来源、未披露子渠道、模拟自然流量、补点击、刷展示、代理/指纹/Worker、防关联、封禁换号等语义，会被拦截并改走风险审计与修复流程。

V1 字段：

```text
vendor_contract_reviews:
  offer_id, campaign_draft_id, name, vendor_name,
  vendor_type, io_number, line_item_ref,
  contract_status, pricing_model, source_detail_level,
  tracking_appendix, reporting_appendix, quality_clause,
  refund_clause, stop_control,
  tracking_completeness_percent, report_delay_days,
  discrepancy_rate_percent, invalid_traffic_rate_percent,
  buyer_reject_rate_percent, budget_cap, spend_to_date,
  approved_revenue, paid_revenue, invoice_amount,
  disputed_amount, refund_credit_amount, makegood_value,
  dispute_response_days, payment_terms_days,
  refund_terms_status, policy_issue_state,
  score, risk_level, recommended_action,
  amount_at_risk, paid_roi, approved_roi,
  invoice_dispute_rate, credit_coverage_rate,
  blockers, status, notes, source_urls
```

V1 评分权重：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| source transparency | 20 | source、publisher、placement、subid 是否透明，能否精确停源 |
| tracking compliance | 15 | tracking appendix 是否存在，URL 参数和 postback 字段是否完整 |
| traffic quality | 20 | invalid traffic、buyer reject、approved / paid ROI 是否支持继续采购 |
| reporting reliability | 15 | reporting appendix、报表延迟和差异率是否可控 |
| dispute responsiveness | 10 | 争议响应速度和 credit / refund / makegood 覆盖率 |
| payment terms | 10 | 付款周期是否允许 revenue validation，refund 条款是否清楚 |
| policy fit | 10 | quality clause 和 policy issue 状态是否支持采购 |

recommended_action 的含义：

| 动作 | 含义 |
| --- | --- |
| allow_scale | 有稳定证据和良好条款，可进入人工扩量审批 |
| approve_small_test | 条款基本可接受，只允许小预算测试 |
| watchlist_hold_scale | 暂停扩量，补齐条款、报表或质量证据 |
| open_dispute | 金额仍有风险，需要开争议并锁定证据窗口 |
| suspend_vendor | 暂停采购，等待修复、credit 或退款 |
| block_vendor | 红线或 active policy issue，不再合作 |
| collect_due_diligence | 资料不足，只能尽调，不能投放 |

后续可把 V1 表拆分为：

```text
traffic_vendor_accounts
media_insertion_orders
media_io_line_items
vendor_tracking_appendices
vendor_report_imports
traffic_dispute_cases
traffic_dispute_evidence
vendor_credit_notes
makegood_plans
vendor_scorecards
contract_versions
```

核心字段示例：

```text
media_insertion_orders:
  vendor_id, io_number, status, start_date, end_date,
  budget_cap, pricing_model, cancellation_terms,
  quality_terms, discrepancy_threshold, payment_terms,
  contract_file_ref, approved_by

traffic_dispute_cases:
  vendor_id, io_id, line_item_id, source_id, placement_id,
  amount_at_risk, issue_type, evidence_window,
  status, requested_resolution, final_resolution,
  source_urls, opened_at, closed_at
```

系统只做资料、评分、争议、证据和建议，不自动采购流量，不调用供应商 API 灌量，不通过 Cookie 后台改广告，不生成补点击或伪装流量。

## 13. ADXKit 对应点和完成形态

ADXKit 类工具常把“买量、看 ROI、换链接、自动优化”做成一体化体验。合同和争议治理对应的是它背后的运营底座：

| ADXKit 类能力 | 安全完成形态 |
| --- | --- |
| traffic vendor 管理 | `/vendor-contracts` 保存供应商状态、来源透明度、合同和质量证据 |
| 自动优化来源 | 生成暂停、争议和名单建议，不自动购买或伪装流量 |
| ROI 看板 | 同时看 invoice cost、approved/paid revenue、refund、credit 和 amount_at_risk |
| 换链接 | 只允许合同和 offer 条款允许的已审核替代链接 |
| 任务自动化 | 生成报表检查、争议证据包和人工审批任务 |
| source blocklist | 基于 IO、报表和 buyer feedback 建立名单 |

完成标准：

- 能解释合同、IO、tracking appendix、reporting appendix 和 dispute case 的关系。
- 能列出禁止流量、质量条款、报表差异、退款、credit 和 makegood 的处理逻辑。
- 能把供应商合作状态接到 source quality、risk audits、optimization 和 cashflow。
- `/vendor-contracts` 能保存评审、计算 blockers、更新状态并写入 `/logs`。
- 明确不实现采购不可解释流量、补点击、模拟自然、代理/指纹/Worker 转发、cloaking 或封禁规避。

## 14. QA 清单

签 IO 或首投前检查：

- 合同主体、付款主体和实际供给主体是否一致。
- 是否有 publisher、placement、sample URL 或 source 明细。
- 是否明确禁止 bot、激励、自动浏览、代理/指纹、隐藏来源、cloaking 和未披露 sub-network。
- 是否允许 UTM、click_id、subid、postback、server log 和第三方追踪。
- 是否能按 source / publisher / placement / subid 停量。
- 是否写清 flight、budget cap、daily cap、geo/device cap 和暂停规则。
- 是否写清 discrepancy threshold、时区、最终结算窗口和优先口径。
- 是否写清 refund、credit、makegood 的触发条件和期限。
- 是否有 creative、landing page、tracking URL 的审批和变更控制。
- 是否约定 vendor report 字段、频率和原始文件保存。
- 是否能把 buyer feedback、reject reason、deduction、invalid traffic 反馈到 source。
- 是否为争议保存 evidence pack 和 owner。

## 15. 信息来源 URL

- IAB, General Terms and Conditions: https://www.iab.com/guidelines/general-terms-and-conditions/
- IAB, IAB unites the industry with new standard terms: https://www.iab.com/blog/iab-unites-the-industry-with-new-standard-terms/
- Google AdSense Help, Traffic provider checklist: https://support.google.com/adsense/answer/3332805
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
- Google AdSense Help, Set up a traffic segmentation plan: https://support.google.com/adsense/answer/2583698
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google Ads Help, Managing invalid traffic: https://support.google.com/google-ads/answer/11182074
- Google Ads Help, About ValueTrack parameters: https://support.google.com/google-ads/answer/2375447
- Google Ads Help, About content suitability: https://support.google.com/google-ads/answer/12764663
- Google Ads Policy, Destination requirements: https://support.google.com/adspolicy/answer/6368661
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- FTC, Native Advertising Guide for Businesses: https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses
- FTC, Endorsements, influencers, and reviews: https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews
- Voluum, Parameters in Postback URLs: https://doc.voluum.com/article/parameters-in-postback-urls
- Google SRE Book, Managing Incidents: https://sre.google/sre-book/managing-incidents/
- Google SRE Book, Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
