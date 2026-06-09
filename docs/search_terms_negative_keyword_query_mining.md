# Search Terms、否定词与 Query Mining 治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何把 Google Ads Search Terms、Search Terms Insights、match type、否定词、query intent、paid revenue 和政策风险连接成一套优化流程。关键词研究解决“投什么”，Search Terms 治理解决“真实买到了什么流量，以及下一步该否定、拆组、加词、改页面、停量还是扩量”。

本文只覆盖真实报表、人工审核、官方导出/API/Scripts 方向和可审计优化建议；不提供模拟搜索、补点击、刷展示、伪造 search term、绕过搜索词隐私限制、Cookie 后台抓取、代理/指纹模拟地区、cloaking 或为规避封禁切换账号。

## 1. 为什么 Search Terms 是 Search 套利的真相层

Search arbitrage 的核心变量不是 campaign name，而是用户真实查询。

```text
keyword / match type
  -> search term / search category
  -> ad promise
  -> landing task
  -> offer click / lead / ad request
  -> approved / finalized / paid revenue
  -> negative / exact / page / creative decision
```

关键词是投手设置的意图假设；search term 是用户真实表达。两者之间的差异决定了套利利润：

- exact/phrase 也可能触发 close variant，导致语义轻微偏移。
- broad、AI Max、PMax search themes、DSA 更容易进入未预期主题。
- Search Partners 的 query 格式和用户意图可能不同。
- 高 CTR query 未必有高 paid revenue，可能只是标题党或低质量意图。
- 某些 query 触发政策风险，例如官方关系、敏感垂类、支持/login、竞品商标。

因此 Search Terms 治理不是简单“加否定词”，而是持续维护搜索意图、页面承诺、收入质量和政策边界。

## 2. 核心对象

| 对象 | 含义 | 套利用法 |
| --- | --- | --- |
| keyword | 广告账号里设置的关键词 | 测试意图假设 |
| match type | broad、phrase、exact | 控制扩展范围和查询质量 |
| search term | 用户实际搜索词 | 判断真实买到的流量 |
| search category | Search Terms Insights 聚合主题 | PMax/broad/隐私聚合场景的意图视图 |
| negative keyword | 排除不想展示的查询 | 控制浪费、政策、低质量 lead |
| negative list | 共享否定词清单 | 账号/业务线级风险控制 |
| query intent | 信息、比较、价格、交易、支持、敏感等 | 决定页面和出价 |
| query decision | add exact、add phrase、negative、split、hold、pause | 把查询转成动作 |
| query evidence | cost、clicks、sessions、revenue、reject、policy issue | 决策证据 |

原则：search term 不只是关键词优化输入，也是创意、落地页、Offer、Link、报表和风险审计的共同证据。

## 3. Search Term vs Keyword

| 维度 | Keyword | Search term |
| --- | --- | --- |
| 来源 | 广告主设置 | 用户实际搜索 |
| 可控性 | 直接添加、暂停、改 match type | 不能直接控制，只能通过关键词、否定词、页面和出价影响 |
| 用途 | 建立投放结构 | 诊断真实意图和流量质量 |
| 风险 | 选词太泛、政策敏感、CPC 高 | 查询漂移、低价值、支持/login、竞品/官方误导 |
| 报表 | keyword report | search terms report / insights |

Google Ads Search Terms Report 说明它展示触发广告的真实搜索及表现，并可用来发现创意、落地页和关键词机会。报告中并非所有 query 都可见，低量查询会因隐私标准被省略或聚合；不要试图通过模拟点击、抓取个人查询或绕过隐私限制补齐不可见 query。

## 4. Match Type 和 Query Drift

匹配类型决定关键词和搜索词之间的距离：

| Match type | Query 范围 | 套利风险 |
| --- | --- | --- |
| Exact | 同义或同意图 | 量小，但可解释性强 |
| Phrase | 包含关键词含义的更具体查询 | 适合冷启动，但仍会扩展到相邻意图 |
| Broad | 相关查询，可结合页面、资产、ad group 其他关键词等信号 | 量大，query drift 和低质量风险高 |

Query drift 常见类型：

| 类型 | 示例 | 处理 |
| --- | --- | --- |
| support drift | `login`、`customer service`、`cancel subscription` | 加否定词，不做套利页面 |
| free / crack drift | `free download`、`torrent`、`crack` | 账号级或 campaign 级否定 |
| job drift | `jobs`、`salary`、`career` | 否定，除非 Offer 是招聘 |
| official drift | `government login`、`official site` | 审核商标/官方关系，通常否定 |
| brand drift | 竞品或禁止品牌词 | 按 Offer 条款和商标政策处理 |
| low intent drift | `definition`、`examples`、`reddit` | 降预算、改页面或否定 |
| geo drift | 非允许国家/州/城市 | location options 和否定词/页面本地化 |
| sensitive drift | 医疗、金融困境、博彩、药品等敏感 query | 敏感垂类准入和人审 |

宽匹配不是不能用，但必须先有追踪、paid revenue、否定词、预算止损和 search terms 复盘。

## 5. Search Terms Report 工作流

推荐日常流程：

```text
1. 导出 search terms report
2. 合并 Google Ads cost/click/conversion
3. 关联 landing/session、offer click、postback、paid revenue
4. 标注 intent、risk、fit、decision
5. 生成 negative / exact / phrase / split / page brief / hold
6. 人工审核
7. 通过 Editor CSV / Scripts preview / 后台手工执行
8. 记录 Change History 和后续表现
```

基础字段：

| 字段 | 说明 |
| --- | --- |
| date_range | 报表窗口 |
| customer_id / campaign_id / ad_group_id | 平台对象 |
| keyword | 触发关键词 |
| keyword_match_type | 账户里设置的 match type |
| search_term | 用户真实查询 |
| search_term_match_type | 报表里的查询匹配类型 |
| network | Google Search / Search Partners |
| device / geo | 分层诊断 |
| cost / clicks / conversions | 平台指标 |
| sessions / offer_clicks | 内部追踪 |
| approved_revenue / paid_revenue | 可收款证据 |
| reject_reason / deduction_reason | 质量反馈 |
| policy_flags | 商标、官方关系、敏感垂类、误导 |
| decision | negative、promote、split、page、hold、pause |

## 6. Query 决策矩阵

| 查询表现 | 意图匹配 | 收入质量 | 决策 |
| --- | --- | --- | --- |
| 花费高、无 session | 不确定 | 无 | tracking_gap_review，不急着否定 |
| 花费高、session 有、revenue 无 | 低或错配 | 差 | negative 或 pause ad group |
| 点击少但 paid RPV 高 | 高 | 好 | 加 exact/phrase，单独小测 |
| CTR 高、reject 高 | 可能过度承诺 | 差 | 改素材/页面，加入 watchlist |
| conversions 高、paid 低 | 表面好 | 差 | conversion_signal_review，不扩量 |
| query 和页面主题不一致 | 低 | 任意 | negative 或拆新页面 |
| query 暗示官方/品牌/支持 | 高风险 | 任意 | policy review，通常否定 |
| query 是新商业意图 | 高 | 待验证 | page brief + small test |
| query 属于信息型长尾 | 中 | 低或展示广告 | 内容页/SEO/低预算测试 |
| query 是敏感垂类 | 不一定 | 不一定 | 垂类准入、人审、证据增强 |

不要只用 conversion 判断。套利要看 paid/finalized revenue、reject/scrub、deduction、complaint 和政策结果。

## 7. 否定词体系

否定词层级：

| 层级 | 用途 | 示例 |
| --- | --- | --- |
| Account-level negative | 全账号都不想买的 query | `jobs`、`free movie`、`torrent` |
| Shared negative list | 某业务线或垂类共享 | 禁止品牌、官方、支持词 |
| Campaign negative | 某国家、Offer 或页面不适合 | `government login` |
| Ad group negative | 防止意图串组 | comparison 组否定 `login`、pricing 组否定 `free` |
| PMax/Search controls | PMax search targeting controls、brand exclusions、negative keywords | 控制 AI-based 扩展 |

否定词 match type 和正向关键词不同。Google Ads 说明 negative broad、phrase、exact 的行为不同于正向匹配，否定词不会像正向关键词那样匹配 close variants；需要主动考虑同义词、单复数或其他形式，但大小写和拼写错误不需要重复添加。

建议否定词记录字段：

| 字段 | 说明 |
| --- | --- |
| negative_text | 否定词文本 |
| negative_match_type | broad / phrase / exact |
| level | account / list / campaign / ad_group |
| reason_code | low_intent / support / brand / policy / no_revenue / bad_geo |
| source_search_term | 触发来源 |
| evidence_window | 报表日期 |
| cost_saved_estimate | 预估节省 |
| risk_of_overblocking | 误杀风险 |
| reviewer | 审核人 |
| applied_batch | CSV / Scripts / manual batch |
| rollback_note | 回滚条件 |

## 8. 否定词常见误区

| 误区 | 后果 | 正确做法 |
| --- | --- | --- |
| 看到无转化就立刻否定 | 回传延迟导致误杀 | 先看 conversion lag、session、paid window |
| 只加 exact negative | 同类 query 继续烧钱 | 按语义决定 phrase/broad/list |
| account 级否定太激进 | 误杀其他 Offer | 先 campaign/ad group，稳定后上升层级 |
| 删除 conflicting negative | 打开低质 query | 逐条看 search terms 和 paid revenue |
| 把品牌词一律当机会 | 商标/Offer 条款风险 | 先看品牌政策和合同限制 |
| 只看 CTR | 标题党和误点扩量 | 看 RPV、reject、deduction、complaint |
| 用补点击验证 query | 产生无效流量 | 用真实小预算和报表验证 |
| 用代理模拟地区查词 | 关联/规避风险 | 用官方 Ad Preview、报表和合法市场研究 |

## 9. Query Promotion：把好查询变成关键词

不是所有赚钱 query 都要直接扩量。推荐流程：

```text
search term positive signal
-> check paid revenue and policy
-> add exact or phrase candidate
-> create small test ad group
-> align ad promise and landing page
-> monitor query drift and revenue quality
```

Promotion 条件：

- paid RPV 或 approved lead quality 过线。
- query intent 清晰，非偶然。
- 页面能真实满足 query。
- 广告文案有对应 evidence。
- 不违反 Offer 条款、商标、敏感垂类或官方关系政策。
- 有足够样本，或样本虽小但商业意图很强，需要小预算再验。

Promotion 后要避免重复竞争：

- 不要同一个 query 同时在多个 ad group 互相抢量。
- 加 exact/phrase 后观察原 broad/phrase ad group 是否继续买同类 query。
- 必要时用 ad group 级 negative 做 query sculpting。
- 保留 Change History 和批次。

## 10. Query Sculpting 和拆组

Query sculpting 的目标不是“操控系统”，而是让不同意图进入对应页面和素材。

可拆组的信号：

- 一个 ad group 同时买到 compare、pricing、support、how-to 等不同意图。
- 某类 query paid revenue 好，但被 campaign 平均值掩盖。
- 某类 query policy risk 高，需要独立人审和页面证据。
- 设备/geo/语言差异导致同一 query 表现不同。
- broad / AI Max 带来一组可解释的新意图，需要单独页面。

拆组后：

- 新 ad group 只保留一个主要意图。
- 配套 landing version、angle、headline role 和否定词。
- 预算小测，不直接继承原 campaign 扩量预算。
- 结果回写到 Creative Angle Library 和维度字典。

## 11. Search Terms Insights 与隐私聚合

Search Terms Insights 会把搜索词按类别和子类别聚合，包含 Search、Search Partners、Google Maps 等范围的聚合表现。它适合：

- 在 search terms report 不完整时理解主题。
- 诊断 PMax、broad、AI-powered Search 的流量扩展。
- 找出新的页面主题和创意 angle。
- 发现某类 search category 消耗高但 paid revenue 差。

限制：

- category 不是完整 query。
- 低量或不可识别 query 会被合并为 other/uncategorized。
- 不能把聚合类别还原成个人搜索或敏感画像。
- 对套利决策仍要结合 paid revenue、landing version、source 和 policy evidence。

## 12. PMax、AI Max、Broad 和 DSA 场景

自动化流量让 query 解释更重要：

| 场景 | 关键风险 | 必查 |
| --- | --- | --- |
| Broad match | 扩到相关但低价值 query | search terms、match type、negative list |
| AI Max | 资产和查询由 AI 扩展 | search terms、asset claim、paid revenue |
| PMax | 多渠道、多页面、多 search theme | search terms insights、channel、asset group、Final URL expansion |
| DSA | 网站内容触发查询和标题 | page feed、URL exclusions、search terms |

这类场景的安全原则：

- 不在追踪和收入回传不稳定时开启。
- 不只看 Google Ads conversions，要看 paid/finalized revenue。
- 不接受自动建议删除否定词，除非逐条复核。
- 不用 Final URL expansion 把用户带到不适合广告承诺的页面。
- 不把 query 不可见当成补点击或模拟搜索的理由。

## 13. 政策和品牌边界

Search terms 里出现以下内容要进入风险审计：

- 官方、政府、登录、支持、客服、取消、退款。
- 竞品商标、品牌名、近似拼写。
- 医疗治疗、金融困境、贷款保证、博彩、成人、药品、技术支持。
- “scam、complaint、lawsuit”等负面或投诉意图。
- “free、crack、torrent、coupon hack”等低质量或违规意图。
- 暗示用户已经和某主体有关系的 query。

处理原则：

- Offer 条款禁止的 brand bidding，直接加入否定词或禁止列表。
- 页面没有资质、价格、身份或限制说明，不承接高风险 query。
- query 暗示官方关系时，广告和页面必须避免冒充。
- 敏感垂类先做准入和政策审计，再决定是否小测。

## 14. 系统落地

当前系统已实现 V1 Query Mining 工作台。`/query-mining` 会把真实 search term / Search Terms Insights category、keyword、match type、network、device、geo、landing version、source file hash、clicks、sessions、conversions、cost、approved / paid revenue、buyer reject、intent fit、policy risk、revenue status、data status、conversion lag、brand / official risk、support / login intent 和 source URLs 保存到 `query_mining_reviews`，并计算 Query Mining Score、risk_level、recommended_action、negative_match_type、negative_level、click_session_rate、CPC、approved_rpv、paid_rpv、approved_roi、paid_roi 和 blockers。

| 能力 | 位置 |
| --- | --- |
| 做 Search Terms / Query Mining 评审 | `/query-mining`，`query_mining_reviews` |
| 更新 negative_proposed / promotion_proposed / page_brief / risk_review / applied 状态 | `/query-mining/<id>/status`，写入 `/logs` |
| 关键词候选生成 | Offer 详情页的创意生成 |
| Campaign / Ad Group / Keyword 草稿 | `/campaigns` |
| Google Ads Editor CSV 导出 | `/campaigns/<id>/export.csv` |
| 指标导入和优化建议 | `/metrics/import`、`/optimization` |
| 报表诊断和来源知识 | `google_ads_reporting_diagnostics.md`、`/sources` |
| 风险审计 | `/risk-audits` |

`query_mining_reviews` 的状态只代表内部审批和批量变更准备，不会自动登录 Google Ads 后台，不会自动新增/删除否定词或关键词，不会点击广告，不会模拟搜索，不会绕过 search terms 隐私聚合，也不会用代理/指纹模拟地区。表单文本如果包含模拟搜索、伪造 search term、补点击、刷展示、Cookie 抓后台、代理/指纹、cloaking、换号等语义，会被拦截并改走风险审计与修复流程。

V1 字段：

```text
query_mining_reviews:
  offer_id, campaign_draft_id, name, date_window,
  ads_customer_id, campaign_ref, ad_group_ref,
  keyword_text, keyword_match_type, search_term,
  search_term_match_type, query_intent, network,
  device, country, landing_version, source_file_hash,
  clicks, sessions, conversions, cost,
  approved_revenue, paid_revenue,
  buyer_reject_rate_percent, intent_fit_score,
  policy_risk, revenue_status, data_status,
  conversion_lag_days, brand_or_official, support_or_login,
  score, risk_level, recommended_action,
  negative_match_type, negative_level,
  click_session_rate, cpc, approved_rpv, paid_rpv,
  approved_roi, paid_roi, blockers, status, notes, source_urls
```

V1 评分权重：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| query intent / fit | 25 | 查询意图和页面/Offer/素材是否匹配 |
| revenue quality | 25 | approved / paid revenue、ROI、buyer reject 是否支持动作 |
| cost control | 15 | 成本和样本是否足够，成熟花费无收入是否应否定 |
| policy safety | 20 | 品牌、官方、支持、敏感、误导等政策风险 |
| data maturity | 10 | 是否已过 conversion lag 和 revenue 回填窗口 |
| actionability | 5 | match type、network 和后续动作是否可控 |

recommended_action 的含义：

| 动作 | 含义 |
| --- | --- |
| promote_exact_test | 高意图、有 approved / paid 证据，可人工加 exact 小测 |
| promote_phrase_test | 意图较好但证据略弱，可人工加 phrase 小测 |
| add_negative_phrase | 低意图、支持/login/free/job 或成熟亏损 query，建议加否定词 |
| policy_review_negative | 品牌、官方、敏感或高政策风险 query，先进风险复核，通常否定 |
| create_page_brief | 有新商业意图但当前页面不够匹配，生成页面/素材 brief |
| tracking_gap_review | 点击有样本但 session 缺失，先排查追踪，不急着否定 |
| watch_wait_for_revenue | 数据新鲜或只到 reported，等待 approved / paid 回填 |
| split_or_pause_ad_group | 语义漂移或低质来源，拆组或暂停 ad group 待审核 |
| scale_exact_cautiously | exact query 已有 paid evidence，只允许小幅人工扩量 |

后续可把 V1 表拆分为导入快照、决策表和否定词 registry：

```sql
CREATE TABLE search_term_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  ads_customer_id VARCHAR(32) NOT NULL,
  campaign_id VARCHAR(64) NOT NULL,
  ad_group_id VARCHAR(64) NULL,
  keyword_text VARCHAR(255) NULL,
  keyword_match_type VARCHAR(32) NULL,
  search_term VARCHAR(500) NOT NULL,
  search_term_match_type VARCHAR(64) NULL,
  date_start DATE NOT NULL,
  date_end DATE NOT NULL,
  device VARCHAR(32) NULL,
  network VARCHAR(64) NULL,
  cost DECIMAL(12,4) NOT NULL DEFAULT 0,
  clicks INT NOT NULL DEFAULT 0,
  conversions INT NOT NULL DEFAULT 0,
  approved_revenue DECIMAL(12,4) NOT NULL DEFAULT 0,
  paid_revenue DECIMAL(12,4) NOT NULL DEFAULT 0,
  source_file_hash VARCHAR(64) NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE TABLE query_mining_decisions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  search_term_snapshot_id BIGINT NOT NULL,
  intent_type VARCHAR(64) NOT NULL,
  decision VARCHAR(64) NOT NULL,
  reason_code VARCHAR(96) NOT NULL,
  risk_level VARCHAR(16) NOT NULL,
  evidence_summary TEXT NOT NULL,
  reviewer VARCHAR(96) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'open',
  batch_key VARCHAR(96) NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);

CREATE TABLE negative_keyword_registry (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  negative_text VARCHAR(255) NOT NULL,
  negative_match_type VARCHAR(32) NOT NULL,
  level VARCHAR(32) NOT NULL,
  target_ref VARCHAR(128) NULL,
  reason_code VARCHAR(96) NOT NULL,
  source_search_term VARCHAR(500) NULL,
  evidence_window VARCHAR(64) NULL,
  reviewer VARCHAR(96) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'proposed',
  applied_batch VARCHAR(96) NULL,
  rollback_condition TEXT,
  created_at DATETIME NOT NULL
);
```

这些表只做报表导入、决策、审计、批量导出和复盘，不自动登录后台、不抓 Cookie、不绕过 Search Terms 隐私限制、不生成点击或搜索。

## 15. ADXKit 对应点和完成形态

| ADXKit 类能力 | 行业需求 | 本系统完成形态 |
| --- | --- | --- |
| 关键词管理 | 批量创建和优化关键词 | `/campaigns` 草稿、CSV 导出 |
| 优化建议 | 找亏损 query 和扩量 query | `/optimization` + `/query-mining` |
| 数据同步 | 定期拉 search terms 和收入 | V1 用 `/query-mining` 保存人工导出/官方同步证据，后续拆 `search_term_snapshots` |
| 批量否定词 | 降低浪费和政策风险 | `/query-mining` 生成 negative_match_type / negative_level，人审后 CSV/Scripts preview |
| AI 创意/页面 | 根据 query 改 angle 和 landing | Creative Angle Library 和页面 brief |
| 风险控制 | brand、官方、敏感 query | `/risk-audits` 和来源库 |

不完成形态：

- 不模拟用户搜索来制造 search terms。
- 不点击广告验证关键词。
- 不绕过 Google 对低量 query 的隐私聚合。
- 不用代理/指纹模拟地区。
- 不用 Cookie 后台抓报表。
- 不自动删除否定词或打开高风险流量。
- `/query-mining` 能保存评审、计算 blockers、更新状态并写入 `/logs`。

## 16. QA 清单

每次 search terms 复盘：

- 报表日期、账号、时区和 campaign 范围是否明确。
- 是否有 keyword、match type、search term、device、network。
- 是否关联 landing/session、offer click、approved/paid revenue。
- 是否考虑 conversion lag 和收入回填。
- 是否区分 Google Search 和 Search Partners。
- 是否标注支持/login、free、job、brand、official、sensitive query。
- 否定词 match type 是否合适。
- account/campaign/ad group 层级是否不会误杀其他 Offer。
- 新增 exact/phrase 是否有页面和素材证据。
- 删除或放宽否定词是否经过 paid revenue 和政策复核。
- 批量动作是否有 batch_key、reviewer、Change History 证据。

## 17. 信息来源 URL

| 来源 | URL | 用法 |
| --- | --- | --- |
| Google Ads Help, About the search terms report | https://support.google.com/google-ads/answer/2472708 | 支撑 search term 与 keyword 区分、真实查询表现、match type、Search Partners 和管理关键词 |
| Google Ads Help, About negative keywords | https://support.google.com/google-ads/answer/2453972 | 支撑否定词用途、account-level negative、negative match type 行为和层级设计 |
| Google Ads Help, Get negative keyword ideas using the search terms report | https://support.google.com/google-ads/answer/7102466 | 支撑从 search terms report 选择 query 添加为 ad group、campaign 或 negative list |
| Google Ads Help, About keyword matching options | https://support.google.com/google-ads/answer/7478529 | 支撑 broad、phrase、exact、negative keywords、PMax/Search 优先级和 query 匹配原理 |
| Google Ads Help, About search terms insights | https://support.google.com/google-ads/answer/11386930 | 支撑 search categories、subcategories、PMax/Search/Shopping 适用和隐私聚合 |
| Google Ads Help, Search targeting & controls for Performance Max | https://support.google.com/google-ads/answer/16672776 | 支撑 PMax search themes、negative keywords、brand exclusions 和 Final URL expansion 控制 |
| Google Ads Help, About broad match | https://support.google.com/google-ads/answer/2407779 | 支撑 broad match 扩展范围、Smart Bidding 依赖和 query drift 风险 |
| Google Ads Help, About Dynamic Search Ads | https://support.google.com/google-ads/answer/2471185 | 支撑 DSA 基于站点内容匹配 query 和自动生成标题的诊断边界 |
| Google Ads Help, About conversion lag reporting | https://support.google.com/google-ads/answer/9347141 | 支撑 query 决策要等待 conversion/revenue 回填 |
| Google Ads Help, Change history | https://support.google.com/google-ads/answer/19888 | 支撑否定词、match type、预算、URL、资产批量变更后的复盘 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑未来用官方 API 同步 search terms、segments 和 metrics |
| Google Ads API, Google Ads Query Language | https://developers.google.com/google-ads/api/docs/query/overview | 支撑 GAQL 字段、segment、filter 和查询快照 |
| Google Ads API, SearchTermView field reference | https://developers.google.com/google-ads/api/fields/latest/search_term_view | 支撑未来以 `search_term_view` 保存 query 级报表 |
| Google Ads Policy, Trademarks | https://support.google.com/adspolicy/answer/6118 | 支撑品牌词、竞品词、商标和官方关系风险审计 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑官方身份、价格、资格、结果承诺和重要限制不能误导 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 query、广告承诺和 landing page 目的地一致 |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑不能用动态页面、隐藏目的地、cloaking 或多账号规避来处理 query 风险 |
