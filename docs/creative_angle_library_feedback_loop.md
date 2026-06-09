# Creative Angle Library、素材版本与反馈闭环手册

更新时间：2026-06-09

本文说明 Ads 套利团队如何把广告创意从“一次性 AI 生成”升级为可复用的 Creative Angle Library、素材版本库和反馈闭环。核心目标不是生成更多标题，而是让每个角度、资产、页面、关键词和收入结果可追踪，能把拒登、低 paid RPV、buyer reject、AdSense deduction、投诉和政策事故反馈回下一轮素材生产。

本文不提供虚假评价、伪造背书、夸大 claim、自动绕过审核、Cookie 后台投放、刷点击、刷展示、模拟自然流量或 cloaking 方法。所有自动化只进入草稿、评审、实验、导出和复盘。

## 1. 为什么 Angle Library 是套利复利资产

很多团队把创意看成“标题 + 描述 + 关键词”的输出物。真正能长期跑的套利团队会把创意看成假设资产：

```text
用户意图
  -> angle
  -> headline / description / asset
  -> landing version
  -> keyword / query
  -> source / geo / device
  -> paid revenue / reject / deduction / policy result
  -> angle library update
```

如果没有角度库，团队会反复犯同样的错误：

- 同一个 offer 每周都重新生成相似文案，没有积累。
- 高 CTR 角度持续吸引低质量 lead。
- 某些 claim 反复拒登，但没有回写到 banned pattern。
- 页面更新后，旧素材继续承诺页面已经删除的内容。
- Buyer 已经反馈某类角度质量差，但投放团队还在扩量。
- AI prompt 只学会“更吸引点击”，没有学会“更可收款、更少拒付”。

Angle Library 的作用是把“创意经验”变成结构化数据，而不是留在个人表格和聊天记录里。

## 2. 核心对象

| 对象 | 含义 | 示例字段 |
| --- | --- | --- |
| angle | 创意角度，表达用户为什么点击 | comparison、eligibility、cost、guide、local service、trust |
| asset | 具体广告资产 | headline、description、image、sitelink、callout、business name |
| asset version | 同一资产的版本 | v1、v2、localized、claim downgraded |
| proof snippet | 页面证据 | pricing table、FAQ、disclosure、review source |
| landing version | 页面版本 | lp-a、lp-b、presell-v3 |
| policy status | 审核状态 | approved、limited、disapproved、appeal_pending |
| performance state | 表现状态 | winner、watch、pause、retired、blocked |
| feedback event | 反馈事件 | reject、scrub、deduction、complaint、low RPV、policy issue |
| decision | 复盘结论 | scale、iterate、rewrite、pause、ban pattern |

系统中 `CreativeSet.angle` 只是第一层。真正的角度库应能追踪“这个角度在什么 offer、国家、页面、关键词和收入口径下有效”。

## 3. Angle 分类法

建议 Angle Library 至少有以下分类：

| Angle | 用户心理 | 适合场景 | 风险 |
| --- | --- | --- | --- |
| comparison | 想比较多个方案 | SaaS、保险、本地服务、软件 | 假排名、竞品商标、主观最佳 |
| cost / pricing | 想知道价格 | 订阅、金融、服务 | 虚假折扣、隐藏费用、地区限制 |
| eligibility | 想知道自己是否符合 | 教育、保险、贷款、福利 | 暗示保证批准、敏感属性 |
| guide / checklist | 研究阶段 | 高客单、复杂服务 | 桥页、低价值内容、MFA |
| speed / convenience | 想快速完成 | 本地服务、工具、预约 | 过度承诺处理时间 |
| trust / safety | 担心风险 | 金融、医疗、B2B、备份 | 虚假认证、官方背书 |
| local relevance | 找本地选项 | 家政、法律、维修 | 地区不可用、误导服务范围 |
| problem solution | 明确痛点 | 软件、服务、健康信息 | 保证结果、医疗疗效 |
| offer incentive | 促销或奖励 | 电商、订阅、trial | 折扣无证据、免费误导 |
| editorial review | 看评测/榜单 | Native、advertorial、comparison site | 商业关系不披露、假客观 |

每个 angle 都应有：

- allowed_verticals。
- banned_verticals。
- proof_required。
- banned_claim_patterns。
- recommended_headline_roles。
- CTA style。
- policy watchlist。
- historical result。

## 4. 素材版本规则

每次改素材，都要区分“新资产”和“新版本”。

应该建新版本的场景：

- 同一 angle 的 headline 从强 claim 降级为弱 claim。
- 同一文案做国家/语言本地化。
- 根据拒登原因修改了词汇。
- 根据 buyer feedback 修改了用户承诺。
- 根据 landing page 版本修改了 CTA 或 proof。

应该建新 angle 的场景：

- 用户心理变了，例如从 comparison 改成 eligibility。
- 页面承诺变了，例如从 price table 改成 guide。
- 关键词意图变了，例如从 brand alternative 改成 cost calculator。
- 转化路径变了，例如从 lead form 改成 call。

不要把素材版本覆盖掉。覆盖会让团队无法回答：

- 哪个版本导致拒登？
- 哪个版本带来低质量 lead？
- 哪个版本在某个 GEO 赚钱？
- 哪个版本是在页面改版前生效？
- 哪个版本被人工审核放行？

## 5. 资产表现口径

Google Ads 提供 responsive search ads、asset reporting、ad strength、ad variations、experiments 和 API 报表资源。套利团队使用这些口径时要注意：

| 平台口径 | 能说明 | 不能说明 |
| --- | --- | --- |
| Impressions | 资产获得展示机会 | 用户质量和收入 |
| Clicks / CTR | 吸引点击能力 | 付款收入、扣量、lead 质量 |
| Conversion | 平台内转化 | buyer 是否接受、AdSense 是否 finalized |
| Conversion value | 已配置的价值信号 | 是否等于可收款价值 |
| Asset performance label | 相对资产表现 | 跨 offer/geo 的真实利润 |
| Ad Strength | 资产覆盖和相关性诊断 | 合规、收入、现金流 |
| Experiment result | 指标对照 | 结算后是否仍成立 |

内部必须补充：

- paid_rpv。
- finalized_rpm。
- approved_lead_rate。
- reject_rate。
- deduction_rate。
- policy_issue_rate。
- complaint_rate。
- page_session_rate。
- click_to_session_gap。

## 6. 反馈事件分类

每个反馈事件都要能回写到 angle、asset、landing、keyword 或 source。

| 反馈 | 可能根因 | 回写位置 |
| --- | --- | --- |
| disapproved | claim、目的地、编辑、敏感垂类 | asset version、banned pattern、policy note |
| limited by policy | 垂类或受众限制 | angle allowed geo、vertical gating |
| low paid RPV | 角度吸引低价值用户 | angle status、headline role |
| high reject / scrub | lead 意向差、表单承诺错 | angle、landing CTA、source |
| AdSense deduction | 流量/页面质量问题 | angle、source、ad layout、page |
| complaint | 误导承诺或披露不足 | claim pattern、landing disclosure |
| click/session gap | URL、速度、consent、跳转 | landing version、tracking template |
| high CTR low CVR | 标题过宽或页面不兑现 | asset version、landing brief |
| conversion lag surprise | 扩量太早 | experiment status、budget rule |

反馈事件不是“报表备注”，而是下一次生成和审核的输入。

## 7. Angle 生命周期

建议每个 angle 有生命周期状态：

| 状态 | 含义 | 处理 |
| --- | --- | --- |
| draft | 新角度，未投放 | 只生成候选，先 claim/proof 审核 |
| approved_for_test | 人审通过，可小测 | 限预算、限 geo、限 source |
| testing | 正在测试 | 等待样本、回传、收入回填 |
| winner | 指标和护栏均通过 | 小幅扩量并生成变体 |
| watch | 表现不稳定 | 不扩量，继续观察 |
| paused | 亏损或数据不足 | 停止新建素材 |
| blocked | 政策、拒付、投诉或合同禁止 | 进入 banned pattern |
| retired | 过期或不再适用 | 保留历史，不再生成 |

Angle 进入 `winner` 必须满足：

- paid ROI 或 finalized revenue 通过。
- reject / deduction / complaint 在阈值内。
- 无重复拒登或 policy warning。
- landing version 和 offer 条款仍有效。
- 数据窗口足够，未被 conversion lag 误导。

## 8. Prompt / Angle 回写机制

AI 生成系统要接收负反馈，而不是只接收“赢家样本”。

回写字段：

| 字段 | 用途 |
| --- | --- |
| angle_id | 哪个角度 |
| prompt_template_version | 哪个 prompt 生成 |
| input_evidence_hash | 哪次页面证据 |
| asset_hash | 哪条素材 |
| landing_version | 哪个页面 |
| campaign_ref | 哪个投放结构 |
| policy_result | 审核结果 |
| paid_result | 可收款结果 |
| feedback_type | 拒登、低 RPV、扣量、拒付、投诉 |
| feedback_note | 具体原因 |
| decision | use、rewrite、pause、block |

Prompt 更新规则：

- 如果同类 claim 重复拒登，把短语加入 banned_claim_patterns。
- 如果某 angle 高 CTR 低 paid RPV，把 prompt 从“点击诱因”改成“限定用户意图”。
- 如果 buyer reject 集中在某承诺，把该承诺降级或禁用。
- 如果页面证据发生变化，旧 prompt output 进入 stale。
- 如果某 angle 在一个 GEO 胜出，不自动推广到其他 GEO，先做 localization QA。

## 9. 版本和哈希

为了可复盘，建议每个素材对象保存 hash：

```text
angle_key
asset_text_hash
prompt_input_hash
prompt_output_hash
landing_evidence_hash
campaign_payload_hash
```

hash 的作用：

- 判断导出的 CSV / Scripts payload 是否和审核过的素材一致。
- 判断页面证据是否在投放前后变化。
- 判断事故发生时是否有人改了资产。
- 支持 prompt regression test。
- 支持回滚到已知安全版本。

## 10. 素材实验和组合爆炸

素材库最大的风险是组合太多，看起来都在测试，实际没有结论。

控制原则：

- 一次只让一个主变量变化：angle、headline role、landing version、keyword theme 或 source。
- 每个 offer 只保留少量 active angles。
- 每个 angle 的变体数量要有上限。
- 自动生成的 headline 不能全部进入测试。
- winner 的变体优先围绕证据增强和语义清晰，而不是更刺激。

最小实验单元：

```text
offer_id + country + language + keyword_theme + angle_id + landing_version
```

不要把不同国家、不同页面、不同 source 的结果混成一个 “creative winner”。

## 11. 系统落地

当前 V1 已有：

| 能力 | 位置 |
| --- | --- |
| 保存创意 angle、headlines、descriptions、keywords | `creative_sets` |
| 生成创意候选 | Offer 详情页 |
| Claim 审核 | Offer 详情页 |
| 投放草稿 | `/campaigns` |
| 指标导入和优化建议 | `/metrics/import`、`/optimization` |
| 风险审计和来源库 | `/risk-audits`、`/sources` |

后续可扩展：

```sql
CREATE TABLE creative_angles (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  angle_key VARCHAR(128) NOT NULL,
  angle_name VARCHAR(128) NOT NULL,
  intent_stage VARCHAR(64),
  allowed_verticals JSON,
  banned_verticals JSON,
  proof_required JSON,
  banned_claim_patterns JSON,
  status VARCHAR(32) NOT NULL,
  risk_level VARCHAR(16) NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);

CREATE TABLE creative_asset_versions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  creative_set_id BIGINT,
  angle_id BIGINT,
  asset_type VARCHAR(32) NOT NULL,
  asset_text TEXT NOT NULL,
  asset_text_hash VARCHAR(64) NOT NULL,
  landing_version VARCHAR(128),
  prompt_template_version VARCHAR(128),
  evidence_hash VARCHAR(64),
  review_status VARCHAR(32) NOT NULL,
  policy_status VARCHAR(32),
  performance_state VARCHAR(32),
  created_at DATETIME NOT NULL
);

CREATE TABLE creative_feedback_events (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  asset_version_id BIGINT,
  angle_id BIGINT,
  feedback_type VARCHAR(64) NOT NULL,
  severity VARCHAR(16) NOT NULL,
  source_type VARCHAR(64),
  source_ref VARCHAR(255),
  metric_snapshot_json JSON,
  feedback_note TEXT,
  decision VARCHAR(32) NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE TABLE angle_performance_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  angle_id BIGINT NOT NULL,
  offer_id BIGINT,
  country VARCHAR(32),
  language VARCHAR(32),
  keyword_theme VARCHAR(255),
  landing_version VARCHAR(128),
  impressions INT,
  clicks INT,
  cost DECIMAL(12,2),
  paid_revenue DECIMAL(12,2),
  paid_rpv DECIMAL(12,4),
  reject_rate DECIMAL(8,4),
  deduction_rate DECIMAL(8,4),
  policy_issue_rate DECIMAL(8,4),
  captured_at DATETIME NOT NULL
);
```

V1 边界：

- 可以保存 angle 和反馈字段。
- 可以输出素材库 QA、人工审核和复盘报告。
- 不把 AI 输出自动提交广告后台。
- 不用自动生成假评价、假价格、假认证。
- 不通过补点击或模拟访问“验证”素材。
- 不用 cloaking 或动态页面让不同对象看到不同承诺。

## 12. QA 清单

| 检查项 | 放行标准 |
| --- | --- |
| angle 定义 | 有用户意图、适用垂类、禁止垂类 |
| proof required | 强 claim 有页面证据 |
| asset version | 改文案不覆盖旧版本 |
| policy status | 拒登、受限、申诉结果可回写 |
| paid revenue | 不只看 CTR 和 conversion |
| feedback event | reject、deduction、complaint 能落到 angle/asset/source |
| stale check | 页面或 offer 变化后旧素材进入复核 |
| experiment scope | 国家、语言、keyword theme、landing version 不混算 |
| prompt update | 负反馈能进入 banned patterns 或 prompt regression |
| export integrity | 导出 payload 与审核素材 hash 一致 |

## 13. ADXKit 对应点和完成形态

| ADXKit 类能力 | 本系统完成形态 |
| --- | --- |
| AI 生成创意 | 生成候选，并要求 angle/proof/review |
| 自动优化 | 把指标、拒登、扣量、buyer feedback 回写到 angle library |
| 批量投放 | 只导出已审核素材版本，不自动提交后台 |
| 数据同步 | 未来可读 asset performance、experiments、change history |
| 换链接 | landing version 变化会触发素材 stale check |
| 任务追踪 | feedback event 和 prompt/asset 版本进入事故复盘 |

## 14. 信息来源 URL

- Google Ads Help, About responsive search ads: https://support.google.com/google-ads/answer/7684791
- Google Ads Help, About Ad Strength: https://support.google.com/google-ads/answer/9921843
- Google Ads Help, View asset reporting for responsive search ads: https://support.google.com/google-ads/answer/9781208
- Google Ads Help, Set up ad variations: https://support.google.com/google-ads/answer/7438541
- Google Ads Help, About automatically created assets: https://support.google.com/google-ads/answer/11259373
- Google Ads Help, About the Experiments page: https://support.google.com/google-ads/answer/10682377
- Google Ads Help, Monitor experiments: https://support.google.com/google-ads/answer/6318747
- Google Ads Help, About conversion lag reporting: https://support.google.com/google-ads/answer/9347141
- Google Ads Help, About data freshness: https://support.google.com/google-ads/answer/2544985
- Google Ads Help, Change history: https://support.google.com/google-ads/answer/19888
- Google Ads Policy, Misrepresentation: https://support.google.com/adspolicy/answer/6020955
- Google Ads Policy, Editorial requirements: https://support.google.com/adspolicy/answer/6021546
- Google Ads API, Responsive Search Ads: https://developers.google.com/google-ads/api/docs/responsive-search-ads/overview
- Google Ads API, Ad group ad asset view: https://developers.google.com/google-ads/api/fields/latest/ad_group_ad_asset_view
- Google Ads API, Asset group asset: https://developers.google.com/google-ads/api/fields/latest/asset_group_asset
- Google Ads API, Experiments overview: https://developers.google.com/google-ads/api/docs/experiments/overview
- FTC, Endorsements, influencers, and reviews: https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews

