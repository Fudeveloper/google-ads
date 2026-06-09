from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from adsworkbench.models import LandingPage, Offer


@dataclass
class LandingAuditResult:
    landing_page: LandingPage
    warnings: list[str]


def audit_landing_page(offer: Offer, url: str | None = None) -> LandingAuditResult:
    target_url = url or offer.target_url
    warnings: list[str] = []
    headers = {
        "User-Agent": (
            "AdsWorkbenchAudit/1.0 "
            "(quality audit; contact: local-workbench)"
        )
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=12)
        http_status = response.status_code
        html = response.text
    except requests.RequestException as exc:
        landing = LandingPage(
            offer_id=offer.id,
            url=target_url,
            http_status=None,
            title="",
            description=str(exc),
            raw_summary=f"Fetch failed: {exc}",
            technical_score=0,
            transparency_score=0,
            relevance_score=0,
            quality_score=0,
        )
        return LandingAuditResult(landing_page=landing, warnings=[str(exc)])

    soup = BeautifulSoup(html, "html.parser")
    title = _text_or_empty(soup.title.string if soup.title else "")
    description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        description = _text_or_empty(meta["content"])

    h1 = _first_text(soup, "h1")
    h2_values = [_text_or_empty(tag.get_text(" ", strip=True)) for tag in soup.find_all("h2")[:6]]
    text = _text_or_empty(soup.get_text(" ", strip=True))
    word_count = len(text.split())
    internal_links, external_links = _count_links(target_url, soup)
    evidence = _extract_evidence(soup, text)

    technical_score = 35 if 200 <= http_status < 400 else 5
    if word_count >= 600:
        technical_score += 10
    elif word_count < 150:
        warnings.append("Page has very little readable text.")

    transparency_score = _transparency_score(text)
    relevance_score = _relevance_score(offer, title, description, h1, text)
    quality_score = max(0, min(100, technical_score + transparency_score + relevance_score))

    if transparency_score < 15:
        warnings.append("Transparency signals are weak: check About, Contact, Privacy, Terms.")
    if relevance_score < 18:
        warnings.append("Landing page appears weakly matched to the offer name or vertical.")
    if external_links > internal_links * 3 and external_links > 20:
        warnings.append("External link density is high; check bridge-page risk.")
    if not evidence["cta_texts"]:
        warnings.append("No clear CTA text found; check landing-to-offer path.")
    if evidence["claim_snippets"] and not evidence["proof_snippets"]:
        warnings.append("Claims found but proof/review snippets are weak; fact-check creative copy.")

    landing = LandingPage(
        offer_id=offer.id,
        url=target_url,
        http_status=http_status,
        title=title[:300],
        description=description,
        h1=h1[:300],
        h2=", ".join(h2_values),
        word_count=word_count,
        internal_links=internal_links,
        external_links=external_links,
        technical_score=technical_score,
        transparency_score=transparency_score,
        relevance_score=relevance_score,
        quality_score=quality_score,
        raw_summary=_summary(title, description, h1, word_count, warnings, evidence),
    )
    return LandingAuditResult(landing_page=landing, warnings=warnings)


def _text_or_empty(value: str | None) -> str:
    return " ".join((value or "").split())


def _first_text(soup: BeautifulSoup, selector: str) -> str:
    tag = soup.find(selector)
    return _text_or_empty(tag.get_text(" ", strip=True) if tag else "")


def _count_links(url: str, soup: BeautifulSoup) -> tuple[int, int]:
    parsed = urlparse(url)
    host = parsed.netloc
    internal = 0
    external = 0
    for link in soup.find_all("a"):
        href = link.get("href") or ""
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        parsed_href = urlparse(href)
        if not parsed_href.netloc or parsed_href.netloc == host:
            internal += 1
        else:
            external += 1
    return internal, external


def _extract_evidence(soup: BeautifulSoup, text: str) -> dict[str, list[str] | int]:
    cta_texts = _unique_clipped(
        [
            _text_or_empty(tag.get_text(" ", strip=True) or tag.get("value"))
            for tag in soup.find_all(["a", "button", "input"])
            if _looks_like_cta(_text_or_empty(tag.get_text(" ", strip=True) or tag.get("value")))
        ],
        limit=8,
    )
    sentences = _sentences(text)
    claim_snippets = _unique_clipped(
        [sentence for sentence in sentences if _looks_like_claim(sentence)],
        limit=8,
        clip=180,
    )
    proof_snippets = _unique_clipped(
        [sentence for sentence in sentences if _looks_like_proof(sentence)],
        limit=8,
        clip=180,
    )
    price_snippets = _unique_clipped(
        [sentence for sentence in sentences if _looks_like_price(sentence)],
        limit=6,
        clip=140,
    )
    form_count = len(soup.find_all("form"))
    input_count = len(
        [
            tag
            for tag in soup.find_all(["input", "select", "textarea"])
            if (tag.get("type") or "").lower() not in {"hidden", "submit", "button"}
        ]
    )
    return {
        "cta_texts": cta_texts,
        "claim_snippets": claim_snippets,
        "proof_snippets": proof_snippets,
        "price_snippets": price_snippets,
        "form_count": form_count,
        "input_count": input_count,
    }


def _transparency_score(text: str) -> int:
    lowered = text.lower()
    signals = [
        "privacy",
        "contact",
        "about",
        "terms",
        "editorial",
        "advertising disclosure",
        "隐私",
        "联系",
        "关于",
        "条款",
        "广告披露",
    ]
    hits = sum(1 for signal in signals if signal in lowered)
    return min(30, hits * 8)


def _relevance_score(offer: Offer, *values: str) -> int:
    haystack = " ".join(values).lower()
    tokens = set((offer.name + " " + offer.vertical).lower().replace("-", " ").split())
    tokens = {token for token in tokens if len(token) >= 3}
    if not tokens:
        return 15
    hits = sum(1 for token in tokens if token in haystack)
    return min(30, 10 + hits * 6)


def _sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?。！？])\s+|\s{2,}", text)
    return [_text_or_empty(chunk) for chunk in chunks if 20 <= len(_text_or_empty(chunk)) <= 260]


def _looks_like_cta(value: str) -> bool:
    lowered = value.lower()
    signals = [
        "get started",
        "learn more",
        "compare",
        "check",
        "apply",
        "request",
        "start",
        "continue",
        "quote",
        "download",
        "sign up",
        "submit",
        "查看",
        "比较",
        "申请",
        "开始",
        "获取",
        "提交",
        "下载",
    ]
    return 2 <= len(value) <= 80 and any(signal in lowered for signal in signals)


def _looks_like_claim(sentence: str) -> bool:
    lowered = sentence.lower()
    claim_signals = [
        "best",
        "top",
        "trusted",
        "guarantee",
        "guaranteed",
        "save",
        "free",
        "no obligation",
        "instant",
        "approved",
        "secure",
        "lowest",
        "award",
        "领先",
        "最佳",
        "免费",
        "保证",
        "安全",
        "省",
    ]
    return any(signal in lowered for signal in claim_signals) or bool(re.search(r"\b\d{1,3}%\b", sentence))


def _looks_like_proof(sentence: str) -> bool:
    lowered = sentence.lower()
    proof_signals = [
        "review",
        "reviews",
        "rating",
        "rated",
        "stars",
        "testimonial",
        "customers",
        "users",
        "case study",
        "as seen",
        "verified",
        "editorial",
        "评价",
        "评分",
        "用户",
        "客户",
        "案例",
        "验证",
    ]
    return any(signal in lowered for signal in proof_signals)


def _looks_like_price(sentence: str) -> bool:
    lowered = sentence.lower()
    currency_or_percent = bool(re.search(r"[$€£¥]\s?\d|\b\d+(\.\d+)?\s?(usd|eur|gbp|元|美元|%)\b", lowered))
    pricing_words = any(word in lowered for word in ["price", "pricing", "cost", "fee", "discount", "价格", "费用", "折扣"])
    return currency_or_percent or pricing_words


def _unique_clipped(values: list[str], limit: int, clip: int = 100) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = _text_or_empty(value)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(cleaned[:clip])
        if len(result) >= limit:
            break
    return result


def _summary(
    title: str,
    description: str,
    h1: str,
    word_count: int,
    warnings: list[str],
    evidence: dict[str, list[str] | int],
) -> str:
    parts = [
        f"Title: {title or 'missing'}",
        f"Description: {description or 'missing'}",
        f"H1: {h1 or 'missing'}",
        f"Readable words: {word_count}",
        "CTA texts: " + (" | ".join(evidence["cta_texts"]) if evidence["cta_texts"] else "missing"),
        "Price/value snippets: "
        + (" | ".join(evidence["price_snippets"]) if evidence["price_snippets"] else "missing"),
        "Claim snippets: "
        + (" | ".join(evidence["claim_snippets"]) if evidence["claim_snippets"] else "missing"),
        "Proof/review snippets: "
        + (" | ".join(evidence["proof_snippets"]) if evidence["proof_snippets"] else "missing"),
        f"Forms: {evidence['form_count']} forms / {evidence['input_count']} user inputs",
    ]
    if warnings:
        parts.append("Warnings: " + " | ".join(warnings))
    return "\n".join(parts)
