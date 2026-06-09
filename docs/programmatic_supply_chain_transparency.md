# 程序化供应链透明度：ads.txt / sellers.json / schain 手册

更新时间：2026-06-08

本文说明 Ads 套利发布商在 AdSense、AdX、Google Ad Manager、Open Bidding、Header Bidding 或第三方需求源中，为什么需要理解 ads.txt、app-ads.txt、sellers.json、SupplyChain Object（schain）、MCM、授权卖方、直销/转售和买方过滤。目标是让团队评估“收入是否稳定、买方是否信任、供应链是否透明”，而不是通过伪造 seller、隐藏转售关系、域名套壳或虚假库存提高短期 RPM。

## 1. 为什么供应链透明度影响套利

发布商套利不是只要页面能展示广告就能长期收款。程序化买方会关注：

- 这个 domain/app 是否授权某个 seller 销售库存。
- seller 是 DIRECT 还是 RESELLER。
- 中间经过了哪些 resellers、exchanges、MCM partners 或 ad servers。
- seller identity 是否在 sellers.json 里可查。
- bid request 里的 schain 是否解释清楚供应链节点。
- 页面、流量来源、广告位和 seller 信息是否一致。

如果供应链不透明，可能出现：

- 买方不出价或降低出价。
- fill rate、CPM、coverage 波动。
- 高价值需求源过滤库存。
- 收入端 estimated 看起来有量，但 finalized 或 demand quality 变差。
- 被归类为 MFA、arbitrage、domain spoofing、unauthorized reseller 或低质量库存。

对套利团队来说，供应链透明度是“能否稳定卖库存”的基础设施，不是合规文档装饰。

## 2. 核心对象

| 对象 | 作用 | 套利团队要检查什么 |
| --- | --- | --- |
| ads.txt | 网站声明授权销售自己库存的 seller | domain 根目录可访问、seller ID 正确、DIRECT/RESELLER 清楚 |
| app-ads.txt | App 声明授权 seller | app store 页面是否指向正确开发者网站 |
| sellers.json | 平台声明 seller ID 对应的主体信息 | seller 类型、name、domain、confidential 状态 |
| SupplyChain Object / schain | bid request 中表达交易链路节点 | 节点顺序、seller ID、complete 标记、转售链是否可解释 |
| MCM | GAM 多客户管理关系 | child publisher、parent、授权类型和 ads.txt/schain 是否一致 |
| ads.cert 方向 | cryptographic supply path assurance | 了解概念即可，第一版不落地 |

这些对象共同回答三个问题：

1. 谁有权卖这个库存？
2. 买方看到的 seller 和页面/域名是否一致？
3. 中间链路是否透明、可验证、可复盘？

## 3. ads.txt 原理和 QA

ads.txt 是发布商在网站根目录公开的文本文件，用来声明授权销售该站广告库存的广告系统账号。

常见格式：

```text
google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
exchange.example, 12345, RESELLER, cert-authority-id
```

字段含义：

| 字段 | 含义 |
| --- | --- |
| advertising system domain | 广告系统域名，例如 google.com |
| publisher account ID | seller / publisher account ID |
| relationship | DIRECT 或 RESELLER |
| certification authority ID | 认证机构 ID，若有 |

QA 清单：

- `https://domain.com/ads.txt` 可访问，HTTP 状态正常。
- 生产域名、www/non-www、移动域名和 canonical 域名一致。
- Google publisher ID、AdX/GAM seller ID 和 partner 给出的 ID 一致。
- DIRECT 只用于团队直接控制或直接签约的 seller；转售链用 RESELLER。
- 不保留未知、过期、无法解释的 seller 行。
- 新增需求源前先确认对方要求的 ads.txt 行和业务关系。

风险信号：

- 复制其他站点 ads.txt。
- seller ID 和当前账号不一致。
- 大量无法解释的 RESELLER 行。
- domain 变化后 ads.txt 未更新。
- 通过中转域名或镜像站隐藏真实 publisher。

## 4. sellers.json 原理和 QA

sellers.json 是广告系统公开 seller 信息的文件。买方可以用它把 seller ID 对应到实体、域名和 seller 类型。

要检查：

- seller ID 是否存在。
- seller type 是 publisher、intermediary 还是 both。
- name 和 domain 是否和业务主体一致。
- 是否被标记 confidential，以及这是否符合需求源政策。
- 多个账号、MCM 或 reseller 关系是否能解释。

套利场景常见问题：

- 页面 domain 是 A，seller domain 是 B，团队无法解释关系。
- 使用 reseller 账号，但页面宣称 direct publisher。
- MCM partner 提供变现，但 child publisher、seller ID、ads.txt、sellers.json 对不上。
- 为了短期接需求源，堆了多个 seller，却没有合同和权限证据。

## 5. schain / SupplyChain Object

SupplyChain Object 是 OpenRTB 中用于表达 bid request 供应链节点的对象。它让买方知道广告请求从 publisher 到 exchange 经过了哪些 seller、reseller 或 intermediary。

核心概念：

| 字段 | 含义 |
| --- | --- |
| complete | 是否完整表达到最终 seller |
| nodes | 供应链节点列表 |
| asi | advertising system identifier |
| sid | seller ID |
| hp | 是否参与付款流程 |

套利团队不需要手写 schain，但需要理解：

- Header bidding、Open Bidding、AdX reseller、MCM 都可能影响 schain。
- schain 和 ads.txt/sellers.json 不一致时，买方可能过滤或降价。
- 供应链越长，越需要解释每个节点的商业关系和授权。
- 不能通过隐藏中间方、伪造 DIRECT 或伪造 seller ID 来提高买方信任。

## 6. DIRECT、RESELLER、MCM 和套利团队边界

| 场景 | 合理解释 | 高风险解释 |
| --- | --- | --- |
| DIRECT | 团队直接拥有站点和发布商账号 | 账号借用、主体不一致但写 DIRECT |
| RESELLER | 合作伙伴被授权转售库存 | 不知道谁卖库存，只复制要求 |
| MCM | 父级 partner 管理 child publisher 库存 | 用 partner 包装低质站点或隐藏真实主体 |
| 多需求源 | 直客、AdX、Open Bidding、Header bidding 分工清楚 | seller 链路长且无法解释 |
| 新域名 | ads.txt、seller、GAM、隐私和内容一致 | 域名套壳、镜像、审核页/用户页不一致 |

第一原则：供应链身份必须能被合同、账号、域名、页面和报表共同解释。

## 7. 对套利模型的影响

供应链问题会影响收入端多个指标：

| 现象 | 可能供应链原因 |
| --- | --- |
| coverage/fill 低 | ads.txt 缺失、seller 未授权、需求源过滤 |
| CPM 低 | 买方不信任 seller、库存被视为 reseller/long path |
| revenue 波动 | 某需求源过滤、MCM/schain 配置变更 |
| 高价值 demand 缺失 | ads.txt/sellers.json 不完整或站点质量低 |
| finalized revenue 下调 | 无效流量、低质量库存、政策或买方争议 |
| 买方 blocklist | MFA、arbitrage、domain spoofing 或供应链不透明 |

因此，扩量前不能只看短期 RPM。要把 supply path QA 纳入月度关账和来源尽调。

## 8. QA 工作流

上线或接新需求源前：

1. 固定 domain、canonical URL、站点主体、隐私政策和内容类型。
2. 确认 AdSense/GAM/AdX/MCM seller ID。
3. 检查 `ads.txt` 行是否与账号和合作关系一致。
4. 查 sellers.json 中 seller ID、seller type、name、domain。
5. 确认 DIRECT / RESELLER 关系有合同或平台授权证据。
6. 如果使用 Header Bidding / Open Bidding / MCM，确认 schain 可解释。
7. 记录截图、URL、seller ID、检查时间和负责人。

每周：

- 检查 ads.txt 是否被覆盖、缓存或误删。
- 检查新增需求源是否带来无法解释的 seller 行。
- 对比 fill、CPM、viewability、deduction 和 policy issue。

每月：

- 清理过期 seller。
- 对照 finalized revenue 和 buyer feedback 复盘供应链质量。
- 更新 source library 和风险审计。

## 9. 常见事故

| 事故 | 表现 | 修复 |
| --- | --- | --- |
| ads.txt 缺少 Google seller ID | coverage 或 demand 下降 | 添加正确 ID，等待缓存刷新 |
| DIRECT 写错成 RESELLER 或相反 | 买方信任和报表解释混乱 | 按真实合同关系更正 |
| seller ID 复制错误 | 无授权 seller，需求源过滤 | 与平台后台 ID 对齐 |
| MCM child publisher 信息不清 | seller/schain 解释不清 | 确认 parent-child 授权和 ads.txt 要求 |
| 域名迁移未更新 ads.txt | 新站收入低或 no fill | 同步 canonical domain 和 ads.txt |
| 大量未知 reseller | 买方认为 supply path 低质量 | 清理并保留合同证据 |

## 10. 系统落地

当前系统可落地：

| 行业动作 | 系统位置 |
| --- | --- |
| 记录站点、Offer、变现模型和政策备注 | `/offers` |
| 记录供应链风险和处理方案 | `/risk-audits` |
| 沉淀 IAB、Google、AdSense/GAM 来源 | `/sources` |
| 在月度收入对账中解释 fill、CPM、扣量和 finalized revenue | `revenue_reconciliation_adstack.md` |
| 记录事故和修复 | `/logs` |

后续可扩展表：

```text
publisher_sites
ads_txt_snapshots
sellers_json_checks
supply_chain_checks
demand_partner_accounts
```

建议字段：

```text
domain
canonical_domain
seller_system_domain
seller_id
relationship_type
certification_authority_id
seller_type
seller_name
seller_domain
schain_complete
last_checked_at
status
evidence_url
```

系统边界：

- 不伪造 seller ID。
- 不生成虚假 ads.txt/sellers.json/schain。
- 不隐藏真实 publisher、reseller、MCM 或需求源关系。
- 不用域名套壳、cloaking 或镜像站绕过买方过滤。

## 11. QA 清单

- ads.txt 可访问，内容和当前账号一致。
- DIRECT/RESELLER 关系和合同、账号、MCM 授权一致。
- sellers.json 中 seller ID 可查，seller type 可解释。
- schain 节点能解释供应链和付款路径。
- 新增需求源前有来源 URL、授权证据和负责人。
- 过期 seller 已清理。
- fill/CPM/revenue/deduction 异常时检查供应链变更。
- 风险审计中出现“借账号”“套 seller”“隐藏 reseller”“复制 ads.txt”等语义时默认 high。

## 12. 信息来源 URL

- IAB Tech Lab, Authorized Digital Sellers ads.txt: https://iabtechlab.com/ads-txt/
- IAB Tech Lab, sellers.json: https://iabtechlab.com/sellers-json/
- IAB Tech Lab, SupplyChain Object: https://iabtechlab.com/supplychainobject/
- IAB Tech Lab, OpenRTB: https://iabtechlab.com/standards/openrtb/
- Google AdSense Help, Authorize sellers with ads.txt: https://support.google.com/adsense/answer/7532444
- Google Ad Manager Help, Manage ads.txt files: https://support.google.com/admanager/answer/7441288
- Google Ad Manager Help, MCM Manage Inventory: https://support.google.com/admanager/answer/11103843
- Google Ad Manager Help, Multiple Customer Management: https://support.google.com/admanager/answer/11194376
- Google Publisher Policies Help, Google Ad Manager partner guidelines: https://support.google.com/publisherpolicies/answer/9059370
- Google AdSense Help, Program policies: https://support.google.com/adsense/answer/48182
- Google AdSense Help, Invalid traffic: https://support.google.com/adsense/answer/16737
- Google AdSense Help, If you want to purchase traffic to your site: https://support.google.com/adsense/answer/1348722
