# Gambling、Sweepstakes 与 Sports Betting Lead 治理手册

更新时间：2026-06-09

本文解释 Google Ads CPL / CPA / RevShare / App Install / Registration / First Deposit / First Bet / NGR / Casino / Sports Betting / Social Casino / Sweepstakes / Fantasy Sports / iGaming Affiliate Lead 套利里，Gambling Lead、Sportsbook Lead、Casino Lead、Sweepstakes Casino Lead、Prize Promotion Lead、Fantasy Sports Lead、Lottery Lead、Social Casino Lead 和 iGaming B2B Lead 为什么是高 payout、强地区限制、强年龄限制、强认证和高投诉风险的垂类。它承接 [敏感垂类政策与 Offer 准入手册](sensitive_vertical_policy_playbook.md)、[Crypto、Investment 与 Trading Lead 治理手册](crypto_investment_trading_lead_governance.md)、[广告创意 Claim 审核与事实核查手册](creative_claim_review_fact_checking.md)、[Lead Form 漏斗、资格问题与移动端 UX 治理手册](lead_form_funnel_qualification_ux.md)、[隐私、Consent 与追踪合规手册](privacy_consent_tracking.md)、[受众定向、再营销与 Customer Match 合规手册](audience_remarketing_customer_match_policy.md) 和 [CRM 阶段、Buyer Feedback 与 Offline Conversion Value Mapping 手册](crm_buyer_feedback_offline_conversion_mapping.md)，重点回答：gambling / sweepstakes lead 的 product type、target jurisdiction、Google Ads gambling certification、operator license、age gate、geolocation、self-exclusion、responsible gambling message、bonus terms、sweepstakes official rules、no purchase necessary、fraud red flags、buyer acceptance、deposit / wager / paid value 和广告信号应该如何治理。

本文不是法律意见，也不提供博彩运营、赌博技巧、规避年龄/地域/KYC/self-exclusion、绕 Google Ads gambling certification、伪造 license、诱导未成年人、诱导 problem gambler、伪造 bonus/odds/winnings、cloaking、代理/指纹规避、使用 Ads Cookie 后台操作或封禁规避方案。系统只做行业知识、准入审计、claim 审核、来源 URL、证据字段、buyer terms、reject reason、offline value、风险任务和人工审批。

## 1. 为什么 Gambling Lead 是高 payout 强监管垂类

博彩、sports betting、casino、sweepstakes casino、social casino、lottery、fantasy sports 和 iGaming affiliate 的 payout 可能来自 registration、KYC approved、first deposit、first bet、qualified player、NGR revshare、subscription 或 affiliate commission。表面看单客价值高，但最核心风险是：产品是否允许广告、目标地区是否允许、operator 是否持牌、Google Ads 是否认证、用户是否达到年龄和地区条件、推广是否包含 responsible gambling 保护。

```text
ad intent
  -> operator / affiliate / review landing
  -> product type and jurisdiction check
  -> Google Ads certification / license review
  -> age gate and geo eligibility
  -> registration / account creation
  -> KYC / geolocation / self-exclusion check
  -> first deposit / first bet / qualifying wager
  -> NGR / revshare / CPA approval
  -> chargeback / complaint / clawback
```

常见亏损路径：

- 广告投到未允许地区，或 operator license 与 target geo 不匹配。
- 没有 Google Ads gambling certification，却推广真钱博彩、sports betting、casino、lottery 或 gambling-promoting content。
- “risk-free bet”“free spins”“guaranteed win”“no deposit bonus”没有清楚条件、wagering requirement 或限制。
- Affiliate / review page 隐藏商业关系、排名按佣金排序却不披露。
- Sweepstakes / prize promotion 页面没有 official rules、AMOE、eligibility、odds、start/end date 或 prize details。
- 广告端按 registration 学习，收入端按 first deposit、qualified wager、NGR 或 post-clawback paid 结算。

Gambling lead 的核心是“允许投放 + 持牌/认证 + 年龄/地区/责任博彩 + 真实 paid value”，不是注册越多越好。

## 2. 原理解释：Gambling Lead 是许可、年龄、地区、风险披露和资金行为的交接

博彩 lead 不是普通 entertainment lead。用户可能存入资金、下注、参与抽奖、接受 bonus 条款，或出现沉迷风险。广告和 landing 的每个表述都需要说明用户看到的是 gambling、social casino、sweepstakes、skill game、fantasy sports、affiliate review、B2B software 还是普通游戏。

| 交接 | 说明 | 失败后果 |
| --- | --- | --- |
| License handoff | operator / affiliate 是否有目标地区许可、认证或授权 | disapproval、regulatory risk |
| Age handoff | 是否只面向 legal gambling age 用户 | minors risk、policy violation |
| Geo handoff | 用户实际位置是否在允许地区 | buyer reject、illegal gambling |
| Responsible gambling handoff | 是否提供 help message、self-exclusion、limits 和风险提示 | harm risk、regulatory issue |
| Bonus handoff | free bet、bonus、odds、wagering requirement 是否清楚 | misrepresentation、complaint |
| Value handoff | registration、KYC、deposit、wager、NGR、paid 是否拆开 | 浅层信号扩量亏损 |

建议测算：

```text
effective_gambling_lead_value =
  headline_payout
  * certification_pass_rate
  * jurisdiction_fit_rate
  * age_gate_pass_rate
  * kyc_geo_pass_rate
  * first_deposit_rate
  * qualifying_wager_rate
  * paid_after_clawback_rate
  - compliance_reserve
  - bonus_abuse_risk
  - chargeback_risk
  - complaint_risk
```

如果 offer 无法提供 license / certification / target geo / age rule / bonus terms / paid definition，默认不进入 paid test。

## 3. Product / Offer Type 地图

| Subvertical | 典型 monetization | 资格字段 | 主要风险 |
| --- | --- | --- | --- |
| Online casino | registration、deposit、NGR | country/state、age、KYC/geo pass | license、casino certification、self-exclusion |
| Sportsbook / sports betting | first deposit、first bet、NGR | state/country、age、sport interest | geo-fencing、bonus terms、odds claim |
| Lottery / raffle / prize promotion | entry、subscription、lead | eligibility、state/country、age | no purchase necessary、official rules、prize scam |
| Sweepstakes casino | registration、coins purchase、redeem | eligibility、state exclusions、age | gambling vs sweepstakes classification |
| Social casino | app install、registration、IAP | age, platform, social casino certification | gambling-like content, minors, misleading redemption |
| Fantasy sports / skill game | signup、deposit、contest entry | state/country、age、sport | legal classification、prize claim |
| Affiliate / review / bonus site | CPA、revshare | geo、operator availability | disclosure、ranking bias、bonus terms |
| iGaming B2B software | B2B demo / lead | operator type、licensed market | indirect gambling promotion, software claim |
| Prediction market | signup、trading volume | jurisdiction、age、product type | gambling vs financial product ambiguity |

## 4. Offer 准入、Google Certification、License 和 Jurisdiction

上线前必须回答：

- 该 product type 是否属于 Google Ads Gambling and games policy 范围？
- 目标国家/州/省是否允许该产品投放？
- 是否需要 Google Ads online gambling、social casino games 或其他 gambling certification？
- Operator / vendor / affiliate 是否持有目标地区 license、authorization 或 contractual approval？
- Landing domain、app ID、operator legal entity、license、advertiser verification、target geo 是否一致？
- 是否有 age limit、geo restriction、KYC/geolocation/self-exclusion rules？
- Affiliate 是否允许该 traffic source、keyword、brand bidding、bonus wording、review/ranking page？

默认拒绝：

- 需要许可但无法提供 license / certification / approval。
- 推广未允许地区、未成年人、self-excluded users 或 vulnerable users。
- 用 sports news、free game、odds calculator、prediction education、social casino 伪装真钱博彩。
- 使用 cloaking、VPN/proxy geo evasion、fake residency、fake KYC 或 age bypass。

## 5. Age Gate、Geolocation、KYC 和 Self-exclusion

博彩 lead 的资格不是表单填完就结束：

- Age gate：广告、landing、registration 和 buyer handoff 都必须只允许 legal age 用户。
- Geolocation：用户 declared location 不等于实际 eligible location；operator 通常需要 geolocation/KYC。
- KYC：identity、address、payment method 等由 licensed operator 或合规 buyer 处理，套利系统不伪造、不补齐、不代操作。
- Self-exclusion：营销名单、retargeting、email、SMS 和 buyer handoff 要尊重 self-exclusion / suppression。
- Responsible gambling：页面和广告要有 required message、help resources、limits、terms 和 risk disclosures。

系统可以记录是否已完成审核、证据来源和人工审批，不能绕过 age/geo/KYC/self-exclusion。

## 6. Google Ads、Gambling and Games、Personalized Ads 边界

治理规则：

- Gambling-related ads 只有在符合政策、允许地区和 Google certification 后才允许。
- Gambling-promoting content、affiliate/review sites、bonus pages、odds pages、social casino app 也可能触发 gambling policy。
- Personalized ads policy 把 gambling / location-based gambling 视为敏感兴趣类别，不能用 advertiser-curated audiences 等敏感定向方式。
- 不用 Customer Match、remarketing、lookalike 或类似方式重新接触 gambling addiction、debt、financial hardship、self-excluded 或 vulnerable 用户。
- Ad copy、keyword、landing、final URL、app store listing、license、responsible gambling message 和 target geo 要一致。

系统只做 policy checklist、source evidence 和 human approval，不做认证绕过或账号规避。

## 7. Sweepstakes、Prize Promotion、Lottery 和 Contest 风险

Sweepstakes / contest / prize promotion 和 gambling 很容易混淆。风险点：

- 是否有 official rules、eligibility、start/end date、prize description、ARV、odds、winner selection、tax responsibility。
- 是否有 no purchase necessary / alternative method of entry，并且入口不是被隐藏或不可用。
- 是否要求用户先付费、付税、付运费、购买产品、转账、gift card 或 crypto 才能领奖。
- 是否冒充政府、FTC、lottery authority、brand 或 celebrity。
- 是否把 sweepstakes casino 的 virtual coin / redeemable prize / purchase mechanism 误导成普通免费游戏。
- 是否使用 influencer / social giveaway，但没有明确 #contest / #sweepstakes 和 material connection disclosure。

如果是 prize promotion lead，而不是 gambling operator lead，系统仍需保存 official rules URL、AMOE review、prize claim proof 和 fraud red flag。

## 8. Bonus、Free Bet、Odds、Winnings 和 Influencer Claim 风险

高风险 claim：

- risk-free、guaranteed win、sure bet、free money、no deposit bonus without conditions。
- “$100 free”但需要 deposit、wagering multiple、minimum odds、state restriction 或 expiration。
- Bonus ranking / best sportsbook / highest payout 没有方法、日期或 affiliate disclosure。
- Influencer / celebrity / athlete endorsement 没有 material connection disclosure。
- Social proof、winnings screenshot、leaderboard、jackpot claim 无法证明或不典型。
- Responsible gambling message 被弱化、隐藏或只放在 footer。

审核规则：

- 每个 bonus claim 必须有 terms URL、effective date、geo、eligibility、wagering requirement、expiration、exclusions。
- Odds / payout / jackpot claim 要有 timestamp 和 source。
- Affiliate ranking 要披露商业关系和排序依据。
- Influencer / review / testimonial 要保存 disclosure proof。

## 9. Lead Delivery：Registration、KYC、Deposit、Wager 和 NGR

常见 payout stage：

| Stage | 说明 | 风险 |
| --- | --- | --- |
| click / app install | 低价值兴趣 | 易被虚量污染 |
| registration | account created | age/geo/KYC 未通过 |
| email/phone verified | contact quality | 仍不是可下注用户 |
| KYC approved | 身份/年龄/地区初步通过 | 仍未入金 |
| first deposit | 资金行为 | chargeback、bonus abuse |
| first wager / qualified bet | 真实投注 | terms / bonus abuse |
| active player / NGR | 收入更接近真实 | 长回传、clawback |
| paid after clawback | 最接近利润 | 回款延迟 |

状态机：

```text
lead_submit
  -> registration
  -> age_gate_pass
  -> geo_pass
  -> kyc_approved
  -> self_exclusion_pass
  -> first_deposit
  -> first_wager
  -> qualified_player
  -> ngr_or_commission
  -> approved_paid_after_clawback
```

不能把 registration、install、lead submit 或 bonus claimed 自动当成 paid gambling value。

## 10. Buyer Acceptance、Reject Reason 和 Payment Risk

常见拒绝原因：

| Reject reason | 解释 | 对投放的动作 |
| --- | --- | --- |
| no_certification | 缺 Google / platform certification | 停投 |
| bad_geo | 不在允许地区 | geo 收窄 / 停投 |
| underage | 年龄不符合 | age gate 修复 |
| kyc_failed | 身份或地址不通过 | 不作为 primary |
| self_excluded | self-exclusion / suppression 命中 | 必须排除 |
| no_deposit | 注册但未入金 | 降权 |
| no_qualifying_wager | 未满足投注或 bonus 条件 | 降权 |
| bonus_abuse | 滥用 bonus / 多账户 | source isolation |
| chargeback_refund | 拒付/退款 | source isolation |
| complaint | 用户投诉、误导 bonus 或提款问题 | 事故复盘 |
| illegal_product | 产品不被目标地区允许 | 拒绝 |

Buyer terms 必须写清 CPA / revshare、qualified player definition、clawback window、fraud/bonus abuse、geo restrictions、brand bidding、affiliate disclosure 和 prohibited traffic。

## 11. Consent、Privacy、Payment Data 和 Sensitive Categories

Gambling lead 涉及敏感兴趣、身份、支付和行为数据。治理规则：

- 不收 payment card、bank login、SSN、passport、KYC document、geolocation proof 等高敏材料；由 licensed operator 处理。
- Lead form 只收必要联系方式、geo bucket、age acknowledgement、product interest 和 consent。
- Email/SMS/call follow-up 必须保存 consent、unsubscribe、DNC、self-exclusion/suppression。
- Offline conversion import 不上传 gambling behavior 明细、payment data 或 self-exclusion status。
- Retargeting / Customer Match 要先过 personalized ads 和 sensitive interest 审核。

## 12. Creative / Landing Claim Review

上线前审核表：

| 审核项 | 通过标准 |
| --- | --- |
| Product type | casino、sportsbook、social casino、sweepstakes、fantasy、affiliate 清楚 |
| License / certification | Google certification、operator license、target geo 证据 |
| Age / geo | legal age、state/country restrictions、geolocation 说明 |
| Responsible gambling | required message、helpline、limits/self-exclusion |
| Bonus terms | deposit、wagering requirement、odds、expiry、state restrictions |
| Sweepstakes rules | official rules、AMOE、eligibility、odds、prize |
| Affiliate disclosure | ranking / review / bonus commercial relationship |
| No deceptive claim | no guaranteed win、risk-free、free money without terms |
| Data fields | 不收 payment / KYC / private sensitive docs |
| Offline value | registration、KYC、deposit、wager、paid 拆开 |

## 13. Offline Value Mapping

Gambling lead 的 conversion action 建议：

| Stage | 是否建议 primary | 原因 |
| --- | --- | --- |
| click / page view | no | 只是兴趣 |
| app install | no / secondary | 不代表 eligible player |
| registration | secondary | age/geo/KYC 未完成 |
| email/phone verified | secondary | 基础质量 |
| KYC / geo approved | primary candidate | 接近可服务用户 |
| first deposit | primary candidate | 接近 buyer value |
| first qualifying wager | primary | 更接近可收款 |
| NGR / commission | primary | 接近真实收入 |
| paid after clawback | primary | 最接近利润 |

保守权重：

```text
registration = 0.05
verified_contact = 0.08
kyc_geo_approved = 0.25
first_deposit = 0.55
first_qualifying_wager = 0.75
ngr_or_commission = 0.90
paid_after_clawback = 1.00
```

权重必须按 product type、geo、operator、bonus abuse、chargeback 和 clawback 窗口校准。

## 14. Gambling Lead Quality Score

建议评分：

| 维度 | 权重 | 说明 |
| --- | --- | --- |
| Certification / license fit | 25 | Google certification、operator license、geo |
| Age / geo / KYC controls | 20 | age gate、geo pass、self-exclusion |
| Claim and terms proof | 20 | bonus、odds、sweepstakes rules、affiliate disclosure |
| Responsible gambling | 15 | message、helpline、limits、vulnerable user protection |
| Offline value quality | 10 | deposit、wager、NGR、paid after clawback |
| Source quality | 10 | fraud、bonus abuse、chargeback、complaints |

```text
gambling_lead_quality_score =
  certification_license_fit * 0.25
  + age_geo_kyc_controls * 0.20
  + claim_terms_proof * 0.20
  + responsible_gambling * 0.15
  + offline_value_quality * 0.10
  + source_quality * 0.10
```

低于 85 不扩量；低于 75 只允许研究；出现 unlicensed geo、underage risk、self-exclusion breach、fake bonus、VPN/proxy evasion 或 guaranteed win claim 时暂停。

## 15. 系统落地

本系统当前完成的是知识、审核和设计形态：

- `/knowledge/gambling_leads` 展示本手册。
- `/sources` 保存 Google、FTC、NY/NJ regulator、UK Gambling Commission、NCPG、FCC 等来源。
- `/risk-audits` 记录 certification、license、geo、age gate、responsible gambling、bonus terms、sweepstakes rules、affiliate disclosure、KYC/deposit/wager/paid 口径。
- `/offers` 保存垂类、目标 URL、tracking URL、policy notes、creative angles。
- `/calculators` 使用更低 safety factor 和更高 policy score 要求评估是否可测。
- `/metrics/import` 允许导入 KYC approved、deposit、wager、NGR、paid after clawback，不把 registration 默认当收入。

后续如果要实体表，应优先建：

| 表 | 用途 |
| --- | --- |
| `gambling_offer_profiles` | product type、geo、license、certification、paid definition |
| `gambling_license_refs` | operator license、regulator、entity、effective date |
| `gambling_claim_reviews` | bonus、odds、risk-free、free spins、winnings、affiliate disclosure |
| `gambling_responsible_messages` | helpline、self-exclusion、limits、message version |
| `gambling_lead_events` | registration、KYC、geo、deposit、wager、NGR、paid |
| `gambling_reject_reason_maps` | underage、bad geo、self-excluded、bonus abuse、chargeback |
| `gambling_offline_value_maps` | stage、weight、Google Ads conversion mapping |

## 16. ADXKit 对应点和完成形态

| ADXKit 类能力 | Gambling lead 安全完成形态 |
| --- | --- |
| Offer 管理 | 增加 product type、geo、license、Google certification、paid definition |
| 创意生成 | 生成 angle 前先做 bonus/odds/sweepstakes/responsible gambling redline |
| 自动优化 | 基于 KYC/deposit/wager/NGR/paid 和 chargeback/complaint，不基于 registration |
| 自动投放 | 只产出人工审核的结构、CSV、任务，不做 Cookie 后台操作 |
| 换链接 | 只做真实 Final URL 变更 QA，不做 geo cloaking 或 sports news 伪装博彩 |
| 来源库 | 保存 Google/FTC/regulator/NCPG/FCC 等来源和摘要 |
| 风险审计 | 对 certification、license、age/geo、bonus、sweepstakes rules、paid definition 建审计项 |

## 17. QA 清单

- 是否确认 product type：real-money gambling、sports betting、social casino、sweepstakes、fantasy、affiliate 或 B2B？
- 是否确认目标 geo 是否允许，且 operator license 和 Google certification 匹配？
- 是否有 age gate、geo restriction、KYC / self-exclusion / responsible gambling message？
- 是否没有向未成年人、self-excluded users、problem gamblers 或受限制地区定向？
- 是否没有 guaranteed win、risk-free、free money、hidden wagering requirement 或 misleading bonus？
- 是否 sweepstakes 有 official rules、AMOE、eligibility、odds、prize、start/end date？
- 是否 affiliate / review / influencer commercial relationship 清楚披露？
- 是否不收 payment card、bank login、KYC document、SSN 或高敏资料？
- 是否拆开 registration、KYC、deposit、wager、NGR、paid after clawback？
- 是否不使用 Ads Cookie 登录、不绕 2FA、不刷量、不用代理/指纹规避、不做 cloaking、不为规避封禁换号？

## 18. 信息来源 URL

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
