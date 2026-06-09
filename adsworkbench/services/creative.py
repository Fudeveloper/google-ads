from __future__ import annotations

from adsworkbench.models import LandingPage, Offer


def generate_creative_sets(offer: Offer, landing: LandingPage | None = None) -> list[dict]:
    context = _context(offer, landing)
    keywords = _keywords(offer, landing)
    return [
        {
            "angle": "Problem Solution",
            "headlines": _headlines(offer, context, "solve"),
            "descriptions": _descriptions(offer, context, "solve"),
            "keywords": keywords[:30],
        },
        {
            "angle": "Comparison",
            "headlines": _headlines(offer, context, "compare"),
            "descriptions": _descriptions(offer, context, "compare"),
            "keywords": keywords[:30],
        },
        {
            "angle": "Guide Checklist",
            "headlines": _headlines(offer, context, "guide"),
            "descriptions": _descriptions(offer, context, "guide"),
            "keywords": keywords[:30],
        },
    ]


def _context(offer: Offer, landing: LandingPage | None) -> str:
    if landing and landing.title:
        summary_hint = ""
        if landing.raw_summary:
            for line in landing.raw_summary.splitlines():
                if line.startswith(("Claim snippets:", "Proof/review snippets:", "CTA texts:")):
                    summary_hint = line.split(":", 1)[1].strip()
                    if summary_hint and summary_hint != "missing":
                        break
        return f"{landing.title} {summary_hint}".strip()
    return f"{offer.name} {offer.vertical}"


def _headlines(offer: Offer, context: str, angle: str) -> list[str]:
    base = offer.name
    vertical = offer.vertical
    country = offer.country
    if angle == "solve":
        drafts = [
            f"{base} Options",
            f"Solve {vertical} Needs",
            f"{vertical} Tools Reviewed",
            f"Find Better {vertical}",
            f"{base} For {country}",
            f"Trusted {vertical} Guide",
            f"Compare Before You Buy",
            f"See Practical Options",
            f"Plan Your Next Step",
            f"Review Costs And Fit",
            f"Simple {vertical} Checklist",
            f"Updated {vertical} Picks",
            f"Make A Smarter Choice",
            f"Check {base} Today",
            f"Explore {context}",
        ]
    elif angle == "compare":
        drafts = [
            f"Compare {base}",
            f"{vertical} Comparison",
            f"Top {vertical} Choices",
            f"Best Fit For {country}",
            f"Pricing And Features",
            f"Side By Side Review",
            f"Compare Plans Fast",
            f"See Pros And Cons",
            f"Before Choosing {base}",
            f"Review {vertical} Brands",
            f"Find The Right Option",
            f"Updated Comparison",
            f"Transparent {vertical} Info",
            f"Shortlist Better Picks",
            f"Compare With Confidence",
        ]
    else:
        drafts = [
            f"{vertical} Buying Guide",
            f"{base} Checklist",
            f"Guide For {country}",
            f"What To Check First",
            f"Avoid Bad Fit Choices",
            f"Questions Before Buying",
            f"Review The Key Factors",
            f"Simple Decision Guide",
            f"Plan With Clear Criteria",
            f"See What Matters",
            f"Updated Guide",
            f"Choose With More Context",
            f"Understand Your Options",
            f"Start With This Checklist",
            f"Make The Choice Easier",
        ]
    return [_clip(item, 30) for item in drafts]


def _descriptions(offer: Offer, context: str, angle: str) -> list[str]:
    vertical = offer.vertical.lower()
    if angle == "solve":
        drafts = [
            f"Review practical {vertical} options before you commit. Clear factors, costs, and next steps.",
            f"Match your needs with relevant {vertical} choices and avoid a poor-fit landing page path.",
            f"Use original comparison content to understand {context} and choose with confidence.",
            f"See features, pricing signals, and decision criteria for real users in {offer.country}.",
        ]
    elif angle == "compare":
        drafts = [
            f"Compare {vertical} options side by side with clear details and transparent navigation.",
            f"Check pricing, benefits, and use cases before selecting a provider or submitting details.",
            f"Find useful context, not a thin bridge page. Review the factors that matter most.",
            f"Use this comparison to shortlist options and keep your next step simple.",
        ]
    else:
        drafts = [
            f"Follow a focused checklist for evaluating {vertical} options without overclaiming results.",
            f"Understand the decision points, risks, and fit before moving to the final offer.",
            f"Review clear guidance and next steps for users looking at {context}.",
            f"Start with a practical guide built around relevance, transparency, and user value.",
        ]
    return [_clip(item, 90) for item in drafts]


def _keywords(offer: Offer, landing: LandingPage | None) -> list[str]:
    bases = [
        offer.name,
        offer.vertical,
        f"{offer.vertical} guide",
        f"{offer.vertical} comparison",
        f"best {offer.vertical}",
        f"{offer.vertical} pricing",
        f"{offer.vertical} reviews",
        f"{offer.vertical} checklist",
        f"{offer.vertical} options",
        f"{offer.vertical} providers",
    ]
    if landing and landing.title:
        bases.append(landing.title)
    modifiers = [
        "for small business",
        "near me",
        "2026",
        "cost",
        "features",
        "alternatives",
        "trusted",
        "secure",
        "quick guide",
        "how to choose",
    ]
    keywords: list[str] = []
    for base in bases:
        clean = " ".join(base.lower().split())
        if clean and clean not in keywords:
            keywords.append(clean)
        for modifier in modifiers:
            keyword = f"{clean} {modifier}".strip()
            if keyword not in keywords:
                keywords.append(keyword)
            if len(keywords) >= 30:
                return keywords
    return keywords


def _clip(value: str, limit: int) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"
