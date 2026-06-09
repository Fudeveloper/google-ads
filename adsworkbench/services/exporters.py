from __future__ import annotations

import csv
import json
from io import StringIO

from adsworkbench.models import CampaignDraft


def campaign_to_google_ads_editor_csv(campaign: CampaignDraft) -> str:
    creative = campaign.creative
    headlines = (creative.headlines if creative else []) or []
    descriptions = (creative.descriptions if creative else []) or []
    keywords = (creative.keywords if creative else []) or ["broad match keyword"]

    buffer = StringIO()
    fieldnames = [
        "Campaign",
        "Ad group",
        "Keyword",
        "Match type",
        "Final URL",
        "Daily budget",
        "Bid strategy",
    ]
    fieldnames += [f"Headline {idx}" for idx in range(1, 16)]
    fieldnames += [f"Description {idx}" for idx in range(1, 5)]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for keyword in keywords:
        row = {
            "Campaign": campaign.name,
            "Ad group": campaign.offer.vertical,
            "Keyword": keyword,
            "Match type": "Phrase",
            "Final URL": campaign.final_url,
            "Daily budget": f"{campaign.budget_float:.2f}",
            "Bid strategy": campaign.bid_strategy,
        }
        for idx in range(1, 16):
            row[f"Headline {idx}"] = headlines[idx - 1] if idx <= len(headlines) else ""
        for idx in range(1, 5):
            row[f"Description {idx}"] = (
                descriptions[idx - 1] if idx <= len(descriptions) else ""
            )
        writer.writerow(row)
    return buffer.getvalue()


def campaign_to_scripts_payload(campaign: CampaignDraft) -> str:
    creative = campaign.creative
    payload = {
        "mode": "manual_review_required",
        "campaign": {
            "name": campaign.name,
            "channel": campaign.channel,
            "daily_budget": campaign.budget_float,
            "bid_strategy": campaign.bid_strategy,
            "final_url": campaign.final_url,
            "status": campaign.status,
        },
        "offer": {
            "id": campaign.offer.id,
            "name": campaign.offer.name,
            "vertical": campaign.offer.vertical,
            "country": campaign.offer.country,
            "language": campaign.offer.language,
        },
        "creative": {
            "angle": creative.angle if creative else None,
            "headlines": (creative.headlines if creative else []) or [],
            "descriptions": (creative.descriptions if creative else []) or [],
            "keywords": (creative.keywords if creative else []) or [],
        },
        "safety": {
            "no_cookie_automation": True,
            "requires_human_approval": True,
            "notes": "Use this payload from a reviewed Google Ads Script or manual workflow.",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
