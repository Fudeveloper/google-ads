from __future__ import annotations

import re

from adsworkbench.models import CreativeSet, LandingPage


Rule = tuple[str, str, str, str, str]


RULES: list[Rule] = [
    (
        r"\b(guarantee|guaranteed|approved|approval|instant approval)\b",
        "high",
        "Guarantee or approval claim",
        "Keep only if the offer terms and landing page explicitly support the claim.",
        "https://support.google.com/adspolicy/answer/6020955",
    ),
    (
        r"\b(official|government|certified|authorized|licensed)\b",
        "high",
        "Official relationship or qualification claim",
        "Verify authorization, license, or government relationship before export.",
        "https://support.google.com/adspolicy/answer/6020955",
    ),
    (
        r"\b(best|top|#1|number one|lowest|trusted)\b",
        "medium",
        "Ranking, superlative, or trust claim",
        "Needs ranking method, comparison basis, reviews, certification, or other proof.",
        "https://support.google.com/adspolicy/answer/6020955",
    ),
    (
        r"\b(free|no cost|zero cost)\b",
        "medium",
        "Free claim",
        "Check whether the free scope, limits, fees, and eligibility are disclosed.",
        "https://support.google.com/adspolicy/answer/6020955",
    ),
    (
        r"\b(save|discount|deal|off|cheapest)\b|\b\d{1,3}%\b",
        "medium",
        "Savings, discount, or price claim",
        "Needs current price or discount evidence on the landing page.",
        "https://support.google.com/adspolicy/answer/6020955",
    ),
    (
        r"\b(review|reviews|rating|rated|stars|testimonial)\b",
        "medium",
        "Review or testimonial claim",
        "Needs verifiable review source and disclosure for any commercial relationship.",
        "https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides",
    ),
    (
        r"\b(limited time|only \d+|today only|act now|urgent)\b",
        "medium",
        "Scarcity or urgency claim",
        "Use only when the offer has a real, current, and visible limitation.",
        "https://support.google.com/adspolicy/answer/6020955",
    ),
]


def audit_creative_claims(
    creative: CreativeSet, landing_page: LandingPage | None
) -> list[dict[str, str]]:
    evidence = _evidence(landing_page)
    issues: list[dict[str, str]] = []

    if not landing_page or not landing_page.raw_summary:
        issues.append(
            {
                "severity": "medium",
                "asset": "landing",
                "text": "No landing evidence summary",
                "issue": "Missing landing evidence",
                "action": "Crawl the landing page before exporting creative assets.",
                "evidence": "missing",
                "source_url": "https://support.google.com/adspolicy/answer/6368661",
            }
        )

    for asset_type, values in (
        ("headline", creative.headlines or []),
        ("description", creative.descriptions or []),
    ):
        for value in values:
            issues.extend(_check_text(asset_type, str(value), evidence))

    return _dedupe(issues)[:10]


def _check_text(asset_type: str, text: str, evidence: dict[str, str]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    lowered = text.lower()
    for pattern, severity, issue, action, source_url in RULES:
        if not re.search(pattern, lowered):
            continue
        evidence_hint = _supporting_evidence(issue, evidence)
        if evidence_hint:
            action = f"{action} Supporting signal found; still verify manually."
        issues.append(
            {
                "severity": severity,
                "asset": asset_type,
                "text": text,
                "issue": issue,
                "action": action,
                "evidence": evidence_hint or "missing",
                "source_url": source_url,
            }
        )

    if re.search(r"[!！]{2,}", text) or _looks_like_excessive_caps(text):
        issues.append(
            {
                "severity": "low",
                "asset": asset_type,
                "text": text,
                "issue": "Editorial style risk",
                "action": "Check punctuation, capitalization, spacing, repetition, and gimmicky wording.",
                "evidence": "Google Ads editorial requirements",
                "source_url": "https://support.google.com/adspolicy/answer/6021546",
            }
        )
    return issues


def _evidence(landing_page: LandingPage | None) -> dict[str, str]:
    if not landing_page or not landing_page.raw_summary:
        return {}
    result: dict[str, str] = {}
    for line in landing_page.raw_summary.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value and value != "missing":
            result[key.strip().lower()] = value
    return result


def _supporting_evidence(issue: str, evidence: dict[str, str]) -> str:
    if "Free" in issue or "Savings" in issue:
        return evidence.get("price/value snippets", "")
    if "Review" in issue or "Ranking" in issue or "trust" in issue.lower():
        return evidence.get("proof/review snippets", "")
    if "Guarantee" in issue or "Official" in issue:
        return evidence.get("claim snippets", "") or evidence.get("proof/review snippets", "")
    if "Scarcity" in issue:
        return evidence.get("claim snippets", "")
    return ""


def _looks_like_excessive_caps(text: str) -> bool:
    letters = [char for char in text if char.isalpha()]
    if len(letters) < 8:
        return False
    upper = sum(1 for char in letters if char.isupper())
    return upper / len(letters) > 0.65


def _dedupe(issues: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str]] = set()
    result: list[dict[str, str]] = []
    for issue in issues:
        key = (issue["asset"], issue["text"].lower(), issue["issue"])
        if key in seen:
            continue
        seen.add(key)
        result.append(issue)
    return result
