# Campaign 命名、Labels、UTM/SubID 与维度治理手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何治理 campaign name、ad group name、label、UTM、ValueTrack、custom parameter、subid、click id、版本号和报表 join key。它解决的不是“名字好不好看”，而是批量投放、换链接、创意测试、收入对账和事故复盘能否落到同一张事实表。

本文只覆盖单团队场景。系统不做多租户，不提供 Ads Cookie 登录、后台接管、自动绕过登录/2FA、安全挑战、补点击、刷展示、模拟自然流量、代理/指纹/Worker 规避关联检测、cloaking、审核页/用户页不一致、封禁规避账号切换等能力。

## 1. 为什么命名和维度治理是套利底座

Ads 套利的核心不是单次投放，而是不断把“买量成本”和“可收款收入”连接起来。只要连接断了，团队就会出现四类典型误判：

- 看 Google Ads campaign ROI，以为某个 campaign 赚钱，但收入实际来自另一个 landing version。
- 看创意 CTR，以为标题好，但 buyer reject 集中在这个 angle。
- 看 GA4 source / medium，以为流量来自 Google Ads，实际 UTM 被跳转覆盖成 referral。
- 看联盟 postback，以为某个 subid 转化高，实际 subid 被多个 campaign 复用。

命名和维度治理的目标是让每个对象都能回答：

```text
谁买来的流量
  -> 哪个 campaign / ad group / keyword / asset / angle
  -> 哪个 landing version / offer / link rule
  -> 哪个 click_id / subid / postback transaction
  -> 哪天、哪个国家、哪个设备、哪个收入状态
  -> 最终是否可收款、是否拒付、是否拒登、是否需要回滚
```

这就是 ADXKit 类工具最常见的“批量投放 + 创意生成 + 换链接 + 报表复盘”底层能力：不是替你点击后台，而是让所有批量对象和结果可命名、可追踪、可还原。

## 2. 核心对象地图

| 对象 | 作用 | 稳定 ID | 可变字段 |
| --- | --- | --- | --- |
| account | 广告账号、付款和访问权限边界 | `ads_customer_id` | account name、status、billing note |
| campaign | 预算、网络、国家、语言、投放目标 | Google Ads `campaign.id` 或内部 draft id | name、budget、bid strategy、status |
| ad group | 意图、关键词主题、资产承载单元 | `ad_group.id` 或内部 group key | name、keywords、default bid |
| keyword / query | 投放设置和真实触发词 | `criterion.id`、query text | match type、negative status |
| creative angle | 用户点击理由 | `angle_key` | lifecycle、risk note |
| asset version | headline、description、image、extension 等具体版本 | `asset_version_id` / hash | text、policy status |
| landing version | 页面版本和证据集合 | `landing_version` / evidence hash | URL、claim/proof、CTA |
| offer | 变现目标和条款边界 | `offer_id` | payout、geo、traffic restrictions |
| link rule | 可审核的换链接计划 | `link_rule_id` / `link_version` | current URL、candidate URL |
| click id | 单次真实点击或访问链路凭证 | `gclid`、`gbraid`、`wbraid`、内部 `click_id` | consent state、session mapping |
| subid | 联盟/买方回传维度槽位 | `subid1..subid5` | 参数映射版本 |
| metric snapshot | 某个日期和维度的事实结果 | `snapshot_id` / payload hash | cost、clicks、revenue、status |

原则：业务对象用稳定 ID，展示名称可以改；报表 join 依赖 ID 和版本，不依赖中文备注或临时名字。

## 3. Campaign 命名规范

推荐结构：

```text
{channel}-{country}-{language}-{vertical}-{offer}-{intent}-{network}-{device}-{yyyymm}-{test}
```

示例：

```text
gads-us-en-cloudbackup-ofr001-compare-search-mobile-202606-t001
gads-ca-en-taxrefund-ofr014-calculator-search-all-202606-t003
gads-us-es-insurance-ofr022-eligibility-search-mobile-202606-t002
```

字段解释：

| 字段 | 示例 | 原理 |
| --- | --- | --- |
| channel | `gads`、`native`、`social` | 买量平台，不和 source/publisher 混用 |
| country | `us`、`ca`、`gb` | 成本、Offer 权限、语言和币种都受国家影响 |
| language | `en`、`es`、`fr-ca` | 同国家多语言需要独立页面和素材证据 |
| vertical | `cloudbackup`、`taxrefund` | 业务垂类，便于风险和素材复用 |
| offer | `ofr001` | 用内部 offer ID，不用广告主昵称 |
| intent | `compare`、`pricing`、`eligibility` | 对应 ad group 和 landing page 的用户意图 |
| network | `search`、`pmax`、`demandgen` | 网络差异会改变流量质量和报表维度 |
| device | `mobile`、`desktop`、`all` | 设备影响 CPC、页面速度、表单质量 |
| yyyymm | `202606` | 便于批次和预算月对齐 |
| test | `t001`、`scale01` | 区分实验或放量批次 |

命名里的每段都必须来自受控枚举，不允许自由发挥。不要使用：

- `test1`、`new`、`final`、`final-final`。
- `过审版`、`备用号`、`安全页`。
- 客户姓名、手机号、邮箱、身份证、病症、收入、信用状态等 PII 或敏感属性。
- 只有投手自己能理解的缩写。

## 4. Ad Group、Asset 和 Landing Version 命名

Campaign name 解决预算和大方向，ad group name 解决意图和关键词主题。

推荐 ad group 结构：

```text
{intent}-{keyword_theme}-{match_policy}-{lpv}-{angle}
```

示例：

```text
compare-cloudbackup-smallbiz-phrase-lpA-ang_compare_cost
pricing-taxrefund-calculator-exact-lpB-ang_cost
eligibility-insurance-quote-phrase-lpC-ang_trust
```

创意和页面版本建议：

| 对象 | 命名 | 示例 |
| --- | --- | --- |
| angle key | `ang_{intent}_{modifier}` | `ang_compare_cost` |
| headline version | `h_{angle}_{role}_v{n}` | `h_compare_cost_problem_v2` |
| description version | `d_{angle}_{role}_v{n}` | `d_trust_disclosure_v1` |
| landing version | `lp{letter_or_number}_{theme}_v{n}` | `lpA_compare_v3` |
| link version | `lnk_{offer}_{route}_v{n}` | `lnk_ofr001_cta_v4` |
| prompt version | `prompt_{task}_v{n}` | `prompt_rsa_brief_v7` |
| experiment id | `exp_{yyyymm}_{seq}` | `exp_202606_014` |

命名要保留语义，但不要把全部信息塞进名字。长字段进入维度字典和 registry，名字只放最关键的拆分维度。

## 5. Labels 使用原则

Google Ads Labels 可以应用到 campaign、ad group、ad、keyword 等对象，用来过滤、报告和组织工作。它们适合做横向分类，但不适合作为唯一事实来源。

推荐标签组：

| 标签组 | 示例 | 用途 |
| --- | --- | --- |
| lifecycle | `draft`、`test`、`scale`、`paused`、`retired` | 当前运营状态 |
| risk | `risk_sensitive_vertical`、`risk_claim_review`、`risk_tracking_change` | 上线前关注点 |
| experiment | `exp_202606_014` | 把实验对象跨层级串起来 |
| owner | `op_alice`、`review_bob` | 单团队内责任人，不是多租户 |
| revenue_state | `estimated_only`、`paid_verified` | 收入口径状态 |
| policy | `policy_watch`、`appeal_pending`、`approved_after_fix` | 审核状态复盘 |
| batch | `batch_20260610_editor_csv` | CSV / Scripts payload 批次 |

Labels 的关键原理：

- Label 是横向标签，不继承所有下级对象。campaign 上打了 label，不代表 ad group、keyword、ad 都自动有同一 label。
- Label 可以被改名、删除或覆盖，所以系统要保存 label snapshot。
- 报表里同一个对象可以有多个 label，按 label 汇总时数字可能不等于总数。
- Label name 适合人看，join 更适合用 label id、resource name 或内部 registry。
- 临时标签必须有过期时间，例如 `review_this_week` 不能永久挂在 campaign 上。

## 6. UTM、ValueTrack、Custom Parameter 与 SubID 映射

追踪参数分四层：

| 层 | 例子 | 谁消费 | 原理 |
| --- | --- | --- | --- |
| UTM | `utm_source`、`utm_medium`、`utm_campaign`、`utm_content`、`utm_term`、`utm_id` | GA4、站内报表 | 用于流量来源和活动维度 |
| ValueTrack | `{campaignid}`、`{adgroupid}`、`{keyword}`、`{matchtype}`、`{creative}`、`{device}`、`{network}` | Google Ads URL 展开、第三方追踪 | 点击时由 Google Ads 替换为触发上下文 |
| Custom parameter | `{_offer}`、`{_lpv}`、`{_angle}`、`{_linkv}` | tracking template / Final URL suffix | 平台对象层级上的业务自定义值 |
| SubID | `subid1..subid5`、`aff_sub`、`click_id` | 联盟网络、买方、postback | 把买量维度传给变现端，用于收入回传 |

推荐映射：

| 内部维度 | URL 参数 | Google Ads/GA4 映射 | 联盟 SubID |
| --- | --- | --- | --- |
| channel | `utm_source=gads` | manual source / source platform | `subid1` |
| campaign | `utm_campaign={campaignid}` 或内部 campaign key | Google Ads campaign ID/name | `subid2` |
| ad group / intent | `utm_content={adgroupid}` + `intent=compare` | Google Ads ad group ID | `subid3` |
| keyword/query | `utm_term={keyword}`、`match={matchtype}` | Manual term / keyword text | `subid4` |
| creative/angle/landing | `creative={creative}`、`angle=...`、`lpv=...` | asset / content 维度 | `subid5` |
| click id | `gclid` + internal `click_id` | auto-tagging/offline conversion | transaction key |

不要把 subid 当成无限维度垃圾桶。一个 subid 槽位只能有一个含义，含义变更必须升级 `parameter_map_version`。

## 7. 参数位置选择

同一个维度可以出现在 campaign name、label、UTM、custom parameter、subid 或数据库字段里，但权威来源不同。

| 维度 | 权威来源 | 可冗余位置 | 原因 |
| --- | --- | --- | --- |
| offer_id | 内部 offers 表 | custom parameter、subid | Offer 是结算和条款对象 |
| campaign_id | Google Ads ID / draft id | campaign name、UTM | 平台 ID 稳定，name 可改 |
| angle_key | Creative Angle Library | `utm_content`、custom parameter | 素材复盘要回写到 angle |
| landing_version | landing registry | URL 参数、custom parameter | 页面变化会影响合规和收入 |
| link_version | link rule registry | custom parameter、audit log | 换链接必须可回滚 |
| source/publisher | traffic source registry | subid、label | Native/渠道场景需要隔离来源 |
| revenue_state | revenue settlement table | label、metrics snapshot | estimated/finalized/paid 不能混 |

原则：URL 上只放复盘需要、非个人、非敏感、可公开暴露也不会伤害用户的数据。PII、lead 信息、cookie、验证码、账号凭据、敏感健康/金融属性不进 URL、不进 subid、不进 prompt。

## 8. 维度字典

维度字典要记录字段名、允许值、来源、更新人和废弃规则。

推荐字段：

| 字段 | 说明 |
| --- | --- |
| `dimension_key` | 机器字段名，例如 `intent` |
| `display_name` | 人类可读名称 |
| `allowed_values` | 枚举或正则 |
| `owner` | 单团队责任人 |
| `source_of_truth` | 表、文件、后台字段或手工 registry |
| `appears_in` | campaign name、label、UTM、subid、CSV、report |
| `pii_allowed` | 默认 false |
| `change_policy` | 修改是否需要审批 |
| `deprecated_at` | 废弃时间 |
| `replacement_key` | 替代字段 |

命名建议：

- 小写。
- 用下划线或短横线，但同一层保持一致。
- 国家用 ISO 风格小写两位，例如 `us`、`ca`。
- 语言用 `en`、`es`、`fr-ca`。
- 日期用 `YYYYMM` 或 `YYYY-MM-DD`，不要混用。
- 金额字段带币种或明确 currency 字段。

## 9. 版本号和 Hash

命名告诉人“这是什么”，版本和 hash 告诉系统“这是不是同一个东西”。

建议记录：

| 字段 | 用途 |
| --- | --- |
| `landing_version` | 页面内容和 CTA 版本 |
| `landing_evidence_hash` | 页面 claim/proof 摘要是否变化 |
| `creative_version` | 素材文本版本 |
| `asset_text_hash` | 防止审核后文本被覆盖 |
| `prompt_template_version` | AI 输出来自哪个模板 |
| `campaign_payload_hash` | CSV / Scripts JSON 是否和审核一致 |
| `link_version` | Final URL、CTA URL、Offer URL 变更版本 |
| `parameter_map_version` | UTM/SubID 字段含义版本 |
| `report_snapshot_hash` | 报表导入文件或 API 查询结果版本 |

事故复盘时，版本字段可以回答：

- 拒登发生时是哪一个 landing evidence？
- 低 paid RPV 是素材改动、页面改动还是 source 改动导致？
- CSV 导出后是否有人在 Editor 里改了字段？
- 换链接是否只换了 URL，还是同时改了承诺和页面？
- 收入导入是否覆盖了上次快照？

## 10. 报表 Join Keys

套利报表至少要能连起四张事实：

```text
Google Ads cost/click
  -> landing/session
  -> offer click/postback
  -> approved/finalized/paid revenue
```

推荐 join keys：

| 链路 | 主 key | 辅助 key | 注意 |
| --- | --- | --- | --- |
| Ads cost -> campaign registry | `customer_id + campaign_id + date` | campaign name snapshot | campaign 改名不应破坏历史 |
| Campaign -> ad group | `campaign_id + ad_group_id` | ad group name snapshot | broad/AI Max 可能带来非预期 query |
| Ad group -> creative | `ad_group_id + asset_id/creative_id` | angle_key、asset hash | RSA 组合需要 asset-level 视角 |
| Click -> landing session | `gclid/gbraid/wbraid` 或 internal `click_id` | timestamp、device、URL params | consent 和 ad blocker 会造成缺口 |
| Landing -> offer click | internal `click_id` | subid map、link_version | CTA 和 link rule 必须版本化 |
| Offer click -> postback | `click_id + transaction_id` | buyer status、payout | transaction 去重，不能制造转化 |
| Postback -> paid revenue | `transaction_id` 或 buyer report id | settlement month、currency | approved 不等于 paid |

当没有 click-level 数据时，退化到 day-level join，但要显式标记精度：

```text
date + channel + country + device + campaign_id + landing_version + offer_id
```

不能把低精度 day-level 推断伪装成 click-level 归因。

## 11. 常见事故

| 事故 | 表现 | 根因 | 修复 |
| --- | --- | --- | --- |
| Campaign 改名后历史报表断裂 | dashboard 出现两个 campaign | 用 name join | 保存 name snapshot，用 ID join |
| 同一 subid 被复用 | 收入归错 campaign | subid 字段无 registry | 建 parameter map 和唯一性检查 |
| UTM 大小写漂移 | GA4 出现 `Google`、`google` 两个 source | 自由输入 | 使用枚举和 URL QA |
| gclid 丢失 | offline conversion 匹配低 | 跳转剥离参数 | 检查 expanded URL、redirect chain、consent |
| Label 被覆盖 | 实验组找不到 | 临时标签无 owner | 保存 label snapshot 和过期规则 |
| link version 不变但 URL 换了 | 无法回滚 | 手动改链接 | link rule 变更必须生成新版本 |
| landing version 复用 | 拒登原因对不上 | 页面覆盖发布 | 页面 evidence hash 入库 |
| estimated revenue 当 paid revenue | 扩量后现金流爆雷 | 收入口径混合 | revenue_state 必须分层 |
| AI Prompt 产物无版本 | 不知道坏素材来源 | prompt 未记录 | prompt input/output hash 入库 |
| broad / AI Max query 无标识 | 搜索自动化流量混入普通关键词 | ValueTrack 不完整 | `{matchtype}`、`{targetid}`、query report 分层 |

## 12. 上线前 QA 清单

每个 campaign draft 导出前检查：

- Campaign name 是否符合受控模板。
- ad group name 是否只表达一个意图。
- Labels 是否包含 lifecycle、risk、experiment/batch。
- Final URL、tracking template、Final URL suffix 是否展开正确。
- UTM 是否完整：至少 `utm_source`、`utm_medium`、`utm_campaign`、`utm_id`。
- ValueTrack 是否包含 campaign/ad group/keyword/match/device/network/creative 所需字段。
- Custom parameters 是否不超过平台限制，是否有 map version。
- subid1..subid5 是否有固定含义。
- URL 不含 PII、敏感属性、Cookie、账号凭据或验证码。
- landing_version、link_version、creative_version、campaign_payload_hash 是否记录。
- CSV / Scripts JSON 是否默认 paused 或 preview。
- 变更是否写入 audit log 和 reviewer。

上线后 24 小时检查：

- Google Ads clicks、landing sessions、offer clicks、postback、revenue 是否分层对上。
- unknown / not set / referral 是否异常。
- `gclid` / `click_id` / subid 保留率是否达标。
- labels 和 campaign registry 是否一致。
- 收入状态是否仍是 estimated，不要提前扩量。
- 拒登、Policy Manager、buyer reject、deduction 是否回写到 angle 和 landing version。

## 13. 系统落地

当前 V1 已有：

| 能力 | 位置 |
| --- | --- |
| Offer、tracking URL、policy note | `/offers` |
| 创意 angle、headlines、descriptions、keywords | Offer 详情页，`creative_sets` |
| Campaign draft、Final URL、CSV / Scripts JSON 导出 | `/campaigns` |
| Campaign 命名、Labels、UTM/SubID 与 join key 评审 | `/taxonomy-governance`，`taxonomy_reviews` |
| 指标导入和 ROI | `/metrics/import`、Dashboard |
| 链接计划和人工换链接 | `/links` |
| 风险审计、来源库、审计日志 | `/risk-audits`、`/sources`、`/logs` |

`/taxonomy-governance` 会把命名维度治理转成导出前 QA 记录，字段包括 offer/campaign 绑定、campaign_name、ad_group_name、labels_text、UTM、ValueTrack template、custom parameter map、SubID map、dimension_dictionary_version、parameter_map_version、landing_version、link_version、creative_version、payload_hash、report_join_gap_count、gclid_preserved、click_id_preserved、lowercase_normalized、url_encoded、no_pii_in_url、no_sensitive_attributes、human_review、Taxonomy Score、risk_level、recommended_action、missing_campaign_tokens、missing_utm_fields、missing_label_groups、valuetrack_fields、blockers、status、notes 和 source_urls。

`/taxonomy-governance/<id>/status` 更新 dictionary_ready、mapping_fix、export_ready、qa_failed、blocked 等内部状态并写入 `/logs`。它只表示命名、追踪和 join key 的内部 QA，不会自动改 Google Ads campaign、URL、label，也不会删除追踪参数或隐藏来源。

后续如果需要拆分更细，可以扩展表：

```sql
CREATE TABLE dimension_dictionary (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  dimension_key VARCHAR(96) NOT NULL UNIQUE,
  display_name VARCHAR(160) NOT NULL,
  allowed_values TEXT,
  source_of_truth VARCHAR(160) NOT NULL,
  appears_in TEXT,
  pii_allowed BOOLEAN NOT NULL DEFAULT FALSE,
  change_policy VARCHAR(64) NOT NULL DEFAULT 'review_required',
  deprecated_at DATETIME NULL,
  replacement_key VARCHAR(96) NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);

CREATE TABLE campaign_name_registry (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  campaign_draft_id BIGINT NULL,
  ads_customer_id VARCHAR(32) NULL,
  ads_campaign_id VARCHAR(32) NULL,
  canonical_name VARCHAR(255) NOT NULL,
  channel VARCHAR(32) NOT NULL,
  country VARCHAR(8) NOT NULL,
  language VARCHAR(16) NOT NULL,
  vertical VARCHAR(96) NOT NULL,
  offer_key VARCHAR(96) NOT NULL,
  intent VARCHAR(96) NOT NULL,
  network VARCHAR(32) NOT NULL,
  device VARCHAR(32) NOT NULL,
  batch_month VARCHAR(6) NOT NULL,
  test_key VARCHAR(64) NOT NULL,
  name_hash VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL
);

CREATE TABLE tracking_parameter_maps (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  map_version VARCHAR(64) NOT NULL,
  channel VARCHAR(32) NOT NULL,
  parameter_name VARCHAR(64) NOT NULL,
  internal_dimension VARCHAR(96) NOT NULL,
  destination_context VARCHAR(64) NOT NULL,
  example_value VARCHAR(255),
  is_pii_allowed BOOLEAN NOT NULL DEFAULT FALSE,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL
);

CREATE TABLE label_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  ads_customer_id VARCHAR(32) NOT NULL,
  object_type VARCHAR(32) NOT NULL,
  object_id VARCHAR(64) NOT NULL,
  label_id VARCHAR(64) NULL,
  label_name VARCHAR(160) NOT NULL,
  label_group VARCHAR(64) NULL,
  captured_at DATETIME NOT NULL,
  source_snapshot_hash VARCHAR(64) NOT NULL
);

CREATE TABLE version_registry (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  object_type VARCHAR(64) NOT NULL,
  object_key VARCHAR(160) NOT NULL,
  version_key VARCHAR(96) NOT NULL,
  content_hash VARCHAR(64) NOT NULL,
  source_url TEXT,
  reviewer VARCHAR(96),
  review_status VARCHAR(32) NOT NULL DEFAULT 'draft',
  created_at DATETIME NOT NULL
);

CREATE TABLE report_join_audits (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  run_key VARCHAR(96) NOT NULL,
  date_start DATE NOT NULL,
  date_end DATE NOT NULL,
  join_level VARCHAR(32) NOT NULL,
  missing_campaign_rows INT NOT NULL DEFAULT 0,
  missing_click_id_rows INT NOT NULL DEFAULT 0,
  missing_subid_rows INT NOT NULL DEFAULT 0,
  unknown_revenue_rows INT NOT NULL DEFAULT 0,
  notes TEXT,
  created_at DATETIME NOT NULL
);
```

这些表服务于命名、映射、版本和 join 审计，不是多租户模型，也不保存登录 Cookie、代理池、浏览器指纹或后台操作凭据。

## 14. ADXKit 对应点和完成形态

ADXKit 类产品通常会把 offer、landing、creative、campaign、link、report、task 放在一个界面里。命名维度治理对应其中的“对象注册和报表统一层”。

| ADXKit 类能力 | 本系统完成形态 |
| --- | --- |
| 批量创建 campaign | 先生成 campaign draft、CSV / Scripts JSON，再人工导入 |
| 创意生成和优化 | angle、asset version、claim review、反馈闭环 |
| 换链接 | link rule、候选 URL、人工轮换、审计日志 |
| 报表聚合 | metrics import、metric dictionary、join key 规则 |
| 多来源追踪 | UTM、ValueTrack、custom parameter、subid map |
| 异常诊断 | click/session/revenue 对账、report join audit |
| 安全自动化 | dry-run、preview、审批、payload hash、Change history |

不完成形态：

- 不用 Ads Cookie 操作后台。
- 不绕过登录、2FA 或安全挑战。
- 不模拟点击、展示、访问、转化或自然流量。
- 不用代理、指纹或 Worker 隐藏关联。
- 不做审核页/用户页不同的 cloaking。
- 不为规避封禁创建、切换或接管账号。

## 15. 最小实施流程

```text
1. 建 offer 和 landing version
2. 建 angle 和 creative version
3. 用命名模板生成 campaign/ad group draft
4. 生成 UTM / ValueTrack / custom parameter / subid map
5. 生成 CSV 或 Scripts JSON preview
6. 人审 name、label、URL、claim、tracking、budget
7. 授权人员导入 Google Ads
8. 导入 Google Ads / GA4 / server / postback / revenue 报表
9. report join audit 找 missing、unknown、duplicate、drift
10. 把结果回写到 angle、landing、link、campaign registry
```

这个流程的重点是“先注册，再投放，再对账，再回写”。不要先在后台手工建一堆 campaign，事后再猜每个名字是什么意思。

## 16. 信息来源 URL

| 来源 | URL | 用法 |
| --- | --- | --- |
| Google Ads Help, About ValueTrack parameters | https://support.google.com/google-ads/answer/2375447 | 解释 ValueTrack 在 final URL、tracking template、custom parameter 中如何被点击上下文替换 |
| Google Ads Help, Set up tracking with ValueTrack parameters | https://support.google.com/google-ads/answer/6305348 | 支撑把设备、位置、关键词、match type 等点击维度带入 URL options |
| Google Ads Help, Create custom parameters for advanced tracking | https://support.google.com/google-ads/answer/6325879 | 支撑 custom parameter 的层级、命名、数量和覆盖规则 |
| Google Ads Help, About ads labels | https://support.google.com/google-ads/answer/2475865 | 支撑 label 可应用到 campaign、ad group、ad、keyword 并用于过滤和报告 |
| Google Ads API, Labels | https://developers.google.com/google-ads/api/docs/reporting/labels | 支撑未来用官方 API 读取 label id、resource name 和 label report，而不是 Cookie 后台抓取 |
| Google Analytics Help, URL builders: Collect campaign data with custom URLs | https://support.google.com/analytics/answer/10917952 | 支撑 UTM 参数、utm_id、utm_content、utm_term 等 campaign URL 规则 |
| Google Analytics Help, Traffic-source dimensions, manual tagging, and auto-tagging | https://support.google.com/analytics/answer/11242870 | 支撑 GA4 manual tagging、auto-tagging 和 traffic-source dimensions 口径 |
| Google Analytics Help, Traffic-source dimensions | https://support.google.com/analytics/answer/15567068 | 支撑 source、medium、campaign 等维度在 GA4 报表中的解释 |
| Google Ads Help, About auto-tagging | https://support.google.com/google-ads/answer/3095550 | 支撑 gclid 等自动标记作为 Google Ads/Analytics 归因和 offline conversion 基础 |
| Google Ads API, Reporting overview | https://developers.google.com/google-ads/api/docs/reporting/overview | 支撑报表同步和字段选择应通过官方 API/GAQL，不应抓 Cookie 后台 |
| Google Ads API, Google Ads Query Language | https://developers.google.com/google-ads/api/docs/query/overview | 支撑报表字段、segment、filter 和查询可复盘 |
| Google Ads API, Field metadata | https://developers.google.com/google-ads/api/fields/latest/overview | 支撑字段兼容性、可选择字段和报表 join 设计 |
| Google Ads API, Upload click conversions | https://developers.google.com/google-ads/api/docs/conversions/upload-clicks | 支撑 click id、conversion time、value、currency 和隐私安全的转化上传口径 |
| Google Ads Policy, Circumventing systems | https://support.google.com/adspolicy/answer/15938075 | 支撑命名、参数、换链接和任务系统不能用于隐藏真实目的地、cloaking、规避政策或多账号规避 |
| Google Ads Policy, Destination requirements | https://support.google.com/adspolicy/answer/6368661 | 支撑 Final URL、目标页可访问性、跳转和广告承诺一致性 |
| Google Ads Policy, Misrepresentation | https://support.google.com/adspolicy/answer/6020955 | 支撑参数和页面版本不能隐藏主体、价格、资格、官方关系或重要限制 |
