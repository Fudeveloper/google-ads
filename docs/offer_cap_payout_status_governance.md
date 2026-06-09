# Offer Cap、Payout、状态变更与替代 Offer 治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何管理 Offer cap、payout、approval window、paused/expired status、buyer capacity、replacement offer 和投放止损联动。它解决的是变现端运行风险：不是“有没有一个高 payout Offer”，而是“当前这个 Offer 今天还能不能接量、超 cap 是否付款、payout 是否变了、状态是否暂停、替代 Offer 是否同主题且已审核”。

本文只覆盖真实条款、报表、邮件/后台证据、人工审核、链接计划和安全导出；不提供联盟后台 Cookie 登录、隐藏来源、自动伪造 lead/conversion、Cookie stuffing、cloaking、审核页/用户页不一致、超 cap 后继续灌量、封禁后切换账号或为规避扣量动态换 Offer 的方案。

## 1. 为什么 Cap 和 Payout 是套利风险核心

套利团队常用公式：

```text
expected EPC = CVR * payout
profit per click = expected EPC - CPC
```

但运行中真实公式更接近：

```text
net EPC =
  CVR
  * effective_payout
  * approval_rate
  * paid_rate
  * cap_fill_factor
  * (1 - deduction_rate)

net profit = net EPC - CPC - tracking_cost - cashflow_cost
```

其中任何一个因子变化，原本赚钱的 campaign 都会变成亏损：

- daily cap 满了，超出转化不付或转到低价 buyer。
- payout 从 42 降到 28，但 Google Ads 预算还按旧 payout 跑。
- Offer paused/expired，tracking URL 仍可访问但不计费。
- buyer 周末不接量，周末转化 pending 后被拒。
- cap 是按 source/affiliate/geo/device 拆的，平均日报看不出来。
- replacement offer 是不同主体、不同国家或不同承诺，直接换会触发 misrepresentation 和 destination mismatch。
- network 月末统一 scrub，没有 reason code，历史 ROI 被重写。

Cap / payout / status 治理的目标，是让投放预算跟变现端真实接收能力同步。

## 2. 核心对象

| 对象 | 含义 | 关键字段 |
| --- | --- | --- |
| offer | 可推广的变现对象 | offer_id、vertical、geo、traffic_allowed、status |
| payout version | payout 金额和模型的版本 | model、value、currency、effective_from、evidence |
| cap | 可接受的转化、revenue、click 或 payout 上限 | type、period、scope、limit、used、remaining |
| approval window | pending 到 approved/rejected 的审核周期 | hours/days、cutoff、timezone |
| buyer capacity | buyer 当前接量能力 | daily lead target、quality cap、paused reason |
| offer status | active、paused、expired、private、pending approval | status、reason、changed_at |
| replacement offer | cap 满或暂停时的替代方案 | offer_id、fit score、approval status、risk |
| link version | 真实 URL / tracking URL 的版本 | old_url、new_url、reviewer、rollback |
| settlement state | pending、approved、rejected、paid、clawback | amount、reason、invoice |

关键原则：payout、cap 和 status 都必须版本化。只记录“当前 payout”会让历史 ROI 失真。

## 3. Offer 生命周期

建议生命周期：

| 状态 | 含义 | 可做动作 |
| --- | --- | --- |
| researching | 正在评估 | 收集条款和来源，不投放 |
| pending_approval | 等待 network/advertiser 审核页面或素材 | 不导出投放 |
| approved_for_test | 允许小测 | 限预算、限 source、限 cap |
| active | 可正常接量 | 按 cap 和质量放量 |
| near_cap | 接近 cap | 降预算、暂停扩量、准备替代 |
| capped | cap 已满 | 停量或切到已审核替代 Offer |
| paused_by_network | network/advertiser 暂停 | 立即停量，保全证据 |
| expired | Offer 过期 | 停投，替代需重新审核 |
| quality_hold | 质量或拒付问题 | 暂停来源，等反馈 |
| retired | 不再推广 | 保留历史和结算 |

不要把 `paused_by_network` 当作“换个链接继续跑”。paused 说明变现端不接量或不允许当前流量，继续买量只会制造亏损、拒付和政策风险。

## 4. Cap 类型

Cap 不一定只有 daily conversion cap。常见类型：

| Cap 类型 | 说明 | 风险 |
| --- | --- | --- |
| daily conversion cap | 每天可计费转化数 | 超出不付或转 pending 后拒 |
| monthly conversion cap | 月度转化上限 | 月末突然无量可接 |
| revenue cap | 可计费金额上限 | 高 payout Offer 更容易触顶 |
| payout cap | affiliate 可获得 payout 上限 | 继续跑会降价或不付 |
| source cap | 某 source / affiliate / publisher 上限 | 平均 cap 未满但某来源已满 |
| geo cap | 国家/州/城市上限 | bad geo 和 cap 混在一起 |
| device cap | mobile/desktop 不同容量 | 移动端可能更快触顶 |
| quality cap | buyer 质量评分触发的软上限 | 转化仍有，但后续 scrub |
| click cap | click 或 lead submission 上限 | 点击继续买但转化不计费 |
| schedule cap | 工作日/周末/时段接量 | 周末或夜间 lead 质量差 |

系统要记录 cap 的 scope：

```text
offer_id + period + cap_type + geo + source + device + buyer + timezone
```

如果只看全局 daily cap，会漏掉 source cap、buyer cap 和 quality cap。

## 5. Cap Pacing 计算

每天至少计算：

```text
cap_used = approved_or_accepted_conversions
cap_remaining = cap_limit - cap_used
cap_usage_rate = cap_used / cap_limit
projected_end_of_day = current_used / elapsed_day_ratio
safe_spend_remaining = cap_remaining * net_epc_estimate / safety_factor
```

触发建议：

| 条件 | 建议 |
| --- | --- |
| cap_usage_rate >= 70% | watch，禁止扩量 |
| cap_usage_rate >= 85% | near_cap，降预算或限 source |
| projected_end_of_day >= cap_limit | 暂停扩量，准备替代 |
| cap_remaining <= expected next batch conversions | 停止新批量导出 |
| quality cap warning | 暂停低质量 source，等 buyer feedback |
| cap 未更新超过 24h | 降低安全系数，不放量 |

Cap pacing 必须考虑时区。Google Ads 账号时区、affiliate network 时区、buyer cutoff 和本地国家时区可能不同。

## 6. Payout 版本和 Effective Payout

Payout 不只是一个数字。

| 模型 | 说明 | 风险 |
| --- | --- | --- |
| fixed CPA/CPL | 每个 approved conversion 固定金额 | 容易忽略 approval rate |
| tiered payout | 根据量级或质量阶梯变化 | 小样本高价，放量降价 |
| geo payout | 国家/州不同价 | bad geo 会稀释 EPC |
| device/source payout | 来源或设备不同价 | 平均 payout 误导预算 |
| revshare | 按后续收入分成 | 回款周期和退款风险高 |
| hybrid | base + revenue share | 对账复杂 |
| dynamic payout | postback 返回实际 payout | 必须保存每笔 payout |

Effective payout：

```text
effective_payout =
  weighted_average(approved_payout_by_geo_source_device)
  * approval_rate
  * paid_rate
  * (1 - clawback_rate)
```

系统不能只用 offer card 上的 headline payout 做 ROI。每次 payout 变更要记录：

- old payout / new payout。
- effective_from。
- source evidence：后台截图、API snapshot、邮件确认、IO/terms。
- 是否影响历史 pending conversions。
- 是否需要调预算、出价、停止扩量或重算 opportunity assessment。

## 7. 状态变更触发器

以下事件必须进入告警或任务队列：

| 事件 | 处理 |
| --- | --- |
| Offer status 从 active 变 paused | 立即停量，冻结新导出 |
| Offer expired date 临近 | 提前准备替代或退役 |
| payout 降低 | 重算 break-even CPC 和 stop-loss |
| payout 提高 | 不立即扩量，先确认 cap 和结算条款 |
| cap 降低 | 降预算，更新 pacing |
| cap 已满 | 停量或切已审核替代 Offer |
| allowed traffic 变更 | 风险审计，暂停冲突来源 |
| brand bidding 规则变更 | 更新否定词和 campaign 规则 |
| rejection reason 激增 | quality_hold，暂停相关 source |
| payment hold | 降安全系数，停止扩量 |

状态变更不能只靠聊天消息。至少要保存 evidence URL、截图路径或邮件摘要。

## 8. 替代 Offer 和 Fallback 规则

替代 Offer 不是 cloaking，也不是审核绕过。它必须满足：

- 同垂类、同用户意图、同国家/语言。
- 页面承诺仍然真实。
- traffic type 和 source 被允许。
- payout、cap、approval window 可解释。
- landing page 已审核。
- tracking、subid、postback 和 disclosure 更新。
- 不冒充原 Offer、品牌、官方或服务主体。
- 用户看到的页面和广告承诺一致。

替代 Offer 决策：

| 场景 | 可否替代 | 条件 |
| --- | --- | --- |
| primary cap 满 | 可以 | replacement 已预审，同主题同承诺 |
| primary paused by network | 谨慎 | 先确认不是政策/质量问题导致 |
| payout 降低 | 可以重测 | 重算 break-even，低预算验证 |
| buyer quality hold | 不应直接替代 | 先查来源和页面质量 |
| policy issue | 不应替代绕过 | 修广告/页面/Offer 条款 |
| account suspension | 不可替代规避 | 走账号健康和申诉 SOP |

禁止：

- 根据 AdsBot、IP、User-Agent、Cookie、地理位置动态切不同 Offer。
- 审核看到 A，真实用户看到 B。
- 超 cap 后把用户偷偷转到无披露、不同主题或未审核 Offer。
- 为了避免拒付把 source/subid 改名。

## 9. Cap 和预算联动

Google Ads 预算不能独立于 cap。

预算建议：

```text
max_daily_media_cost =
  min(
    cash_budget,
    cap_remaining * expected_effective_payout * safety_factor,
    source_quality_limit,
    policy_risk_limit
  )
```

投放动作：

| Cap 状态 | 投放动作 |
| --- | --- |
| cap < 50% used | 正常小测或稳定投放 |
| 50%-70% used | 不新增大批量 campaign |
| 70%-85% used | 禁止扩量，只优化质量 |
| 85%-100% projected | 降预算或暂停低质量 source |
| cap reached | 停量或人工切换已审核替代 |
| cap unknown | 按高风险处理，降低预算 |

不要把 Google Ads average daily budget 当作硬 cap。套利系统需要外部 cap/payout/paid revenue 预算闸门。

## 10. 对账和结算窗口

Cap 和 payout 决策必须等结算状态回填：

| 状态 | 用途 |
| --- | --- |
| pending | 只作早期信号，不扩量 |
| accepted | buyer 初步接收，但仍可能拒付 |
| approved | 可计费基础 |
| paid | 现金确认 |
| rejected | 质量或条款问题 |
| clawback | 历史收入被追回 |

月度复盘：

- payout version 是否变更。
- cap 是否触顶或被临时下调。
- approval_rate、paid_rate、deduction_rate。
- 超 cap 转化是否被拒。
- 哪些 source 在 cap 满前消耗最多。
- 是否存在未解释 scrub。
- replacement offer 是否真实提高 paid revenue。

## 11. 系统落地

当前系统已实现 Offer Cap / Payout 治理 V1：

| 能力 | 位置 |
| --- | --- |
| Offer payout、country、status、policy notes | `/offers` |
| 测算 payout、CVR、CPC 和安全系数 | `/calculators` |
| 生成 campaign draft 和 tracking URL | `/campaigns` |
| 指标导入和优化建议 | `/metrics/import`、`/optimization` |
| 记录 cap、payout、status、buyer capacity 和替代 Offer 评审 | `/offer-cap-payout` |
| 链接计划和人工轮换 | `/links` |
| 风险审计和来源证据 | `/risk-audits`、`/sources` |

V1 表：

```text
offer_cap_reviews
```

核心字段：

```text
offer_cap_reviews:
  offer_id, replacement_offer_id, campaign_draft_id, name,
  offer_status, cap_type, cap_period, cap_limit, cap_used,
  expected_next_conversions, current_payout, new_payout,
  approval_rate_percent, paid_rate_percent, deduction_rate_percent,
  days_since_cap_update, buyer_capacity_status,
  replacement_status, replacement_fit_score, same_intent_review,
  source_quality, policy_risk, score, risk_level,
  recommended_action, cap_usage_percent, cap_remaining,
  effective_payout, safe_daily_media_cost, blockers,
  status, notes, source_urls
```

状态流：

```text
open -> reviewed
open -> waiting_cap_update
open -> reduce_budget
open -> pause_traffic
open -> manual_replacement_ready
open -> closed
```

`/offer-cap-payout/<id>/status` 只更新内部处理状态并写入 `audit_logs`。它不会自动登录 affiliate network、Google Ads 或发布商后台，不会改 budget、tracking URL、Final URL、link rule，也不会把用户切到未审核或不同承诺的 Offer。

后续可拆分表：

```sql
CREATE TABLE offer_status_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  offer_id BIGINT NOT NULL,
  status VARCHAR(64) NOT NULL,
  reason_code VARCHAR(96) NULL,
  effective_at DATETIME NOT NULL,
  source_evidence_url TEXT,
  captured_by VARCHAR(96) NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE TABLE offer_payout_versions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  offer_id BIGINT NOT NULL,
  payout_model VARCHAR(64) NOT NULL,
  payout_value DECIMAL(12,4) NOT NULL,
  currency VARCHAR(8) NOT NULL,
  scope_json JSON NOT NULL,
  effective_from DATETIME NOT NULL,
  effective_to DATETIME NULL,
  evidence_url TEXT,
  created_at DATETIME NOT NULL
);

CREATE TABLE offer_cap_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  offer_id BIGINT NOT NULL,
  cap_type VARCHAR(64) NOT NULL,
  cap_period VARCHAR(32) NOT NULL,
  scope_json JSON NOT NULL,
  cap_limit DECIMAL(12,4) NOT NULL,
  cap_used DECIMAL(12,4) NOT NULL DEFAULT 0,
  cap_remaining DECIMAL(12,4) NOT NULL DEFAULT 0,
  timezone VARCHAR(64) NOT NULL,
  captured_at DATETIME NOT NULL,
  evidence_url TEXT
);

CREATE TABLE offer_replacement_plans (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  primary_offer_id BIGINT NOT NULL,
  replacement_offer_id BIGINT NOT NULL,
  trigger_reason VARCHAR(96) NOT NULL,
  fit_score INT NOT NULL,
  approval_status VARCHAR(32) NOT NULL DEFAULT 'draft',
  reviewer VARCHAR(96),
  risk_notes TEXT,
  rollback_plan TEXT,
  created_at DATETIME NOT NULL
);

CREATE TABLE cap_pacing_alerts (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  offer_id BIGINT NOT NULL,
  cap_snapshot_id BIGINT NOT NULL,
  severity VARCHAR(16) NOT NULL,
  alert_type VARCHAR(64) NOT NULL,
  message TEXT NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'open',
  created_at DATETIME NOT NULL
);
```

这些表只保存状态、cap、payout、证据和人工决策，不执行 Cookie 后台登录，不自动切换未审核 Offer，不隐藏真实目的地。

## 12. ADXKit 对应点和完成形态

| ADXKit 类能力 | 行业需求 | 本系统完成形态 |
| --- | --- | --- |
| Offer 管理 | 管理 payout、状态、URL 和备注 | `/offers` + 本手册 |
| Cap / Payout 门禁 | 判断 cap usage、effective payout、safe media cost 和阻塞项 | `/offer-cap-payout` 保存评分、建议动作、来源 URL 和状态流 |
| 换链接 | cap 满或 URL 故障时切换 | `/links` 人审、link version、审计日志 |
| 优化建议 | cap/payout/status 触发停量或降预算 | `/optimization` 和 `/offer-cap-payout` |
| 数据同步 | 获取 cap、payout、approved/paid 状态 | 未来官方/API/CSV 快照，不抓 Cookie |
| 任务追踪 | 跟踪 cap 检查、替代审核、回滚 | `/tasks`、`/logs` |

完成标准：

- Offer payout、cap、status 都可追溯到来源。
- 每次 payout/status/cap 变更有版本。
- `/offer-cap-payout` 能保存 cap pacing、effective payout、safe_daily_media_cost、recommended_action 和 blockers。
- replacement offer 已审核且同主题。
- 投放预算和 cap/payout 联动。
- 不把替代 Offer 用作 cloaking 或规避拒付。

## 13. QA 清单

上线前：

- payout model、value、currency 是否确认。
- cap type、period、scope、timezone 是否确认。
- approval window 和 rejection reason 是否确认。
- allowed/prohibited traffic 是否确认。
- brand bidding、competitor bidding、native/social/email 是否确认。
- landing/creative 是否需要 advertiser pre-approval。
- replacement offer 是否同主题、同 geo、同 disclosure。
- tracking/postback 是否能传 click_id、subid、payout、status、transaction_id。

每日：

- cap_used、cap_remaining、projected_end_of_day。
- Offer status 是否变 paused/expired/private。
- payout 是否变化。
- buyer quality warning 是否出现。
- accepted/approved/paid 是否低于预期。
- payment hold 或 unexplained scrub 是否出现。
- Google Ads 预算是否超过 cap 可承受金额。

事故复盘：

- 异常开始前后是否有 payout/cap/status 变更。
- 是否超 cap 继续买量。
- replacement offer 是否导致用户承诺不一致。
- 是否有 source 触发 quality cap。
- 是否有扣量无 reason code。
- 是否需要下调 safety factor 或拒绝该 network。

## 14. 信息来源 URL

| 来源 | URL | 用法 |
| --- | --- | --- |
| TUNE, Offer Payouts and Caps | https://support.tune.com/hc/en-us/sections/1500000824241-Offer-Payouts-and-Caps | 支撑 affiliate offer 的 payout、conversion cap、budget cap 和 tiers 概念 |
| TUNE Dev Hub, OfferConversionCap | https://developers.tune.com/network-models/offerconversioncap/ | 支撑按 offer/affiliate 保存 conversion、payout、revenue cap 的数据模型 |
| Everflow API, Get Offer | https://developers.everflow.io/docs/affiliate/offers/ | 支撑 offer status、daily payout cap、affiliate status 等字段快照 |
| Everflow Helpdesk, Advertiser Feeds | https://helpdesk.everflow.io/customer/advertiser-feeds | 支撑 advertiser feed 同步 payout、landing page URL、targeting rules 和 caps 可能覆盖本地配置 |
| Voluum Documentation, Glossary | https://doc.voluum.com/article/glossary | 支撑 conversion cap、fallback/redirect offer、offer grouping 等追踪概念 |
| Voluum Documentation, Tracking Payouts | https://doc.voluum.com/en/tracking_payout.html | 支撑从 affiliate network postback 接收动态 payout |
| Voluum Documentation, Conversion Status | https://doc.voluum.com/article/conversion-status | 支撑 conversion status、postback timestamp、payout 等状态对账 |
| Voluum Documentation, Parameters in Postback URLs | https://doc.voluum.com/article/parameters-in-postback-urls | 支撑 click_id、transaction_id、payout 和 postback 参数设计 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑替代 Offer、payout claim、价格/资格/主体不能误导 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目标页和广告承诺一致，不能切到不相关 Offer |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑不能用动态目的地、cloaking、多账号或隐藏真实目的地规避政策 |
| Google Ads Policy, Advertising network abuse | https://support.google.com/adspolicy/answer/6008942 | 支撑低价值目的地、桥页和流量套利质量风险 |
| FTC, Endorsements, influencers, and reviews | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | 支撑 affiliate 推荐、评价、排名和商业关系披露 |
| FTC, Disclosures 101 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | 支撑 disclosure 应清楚、明显、靠近推荐内容 |
