from __future__ import annotations

from adsworkbench.models import AdReviewCase, CampaignDraft


def campaign_preflight_blockers(campaign: CampaignDraft) -> list[str]:
    blockers: list[str] = []
    if campaign.status not in {"approved", "exported"}:
        blockers.append("投放草稿必须先标记为已批准")

    if campaign.creative:
        blocking_claims = [
            review
            for review in campaign.creative.claim_reviews
            if review.review_status in {"open", "rewrite_required", "blocked"}
        ]
        if blocking_claims:
            labels = ", ".join(
                sorted({f"{review.severity}:{review.issue}" for review in blocking_claims})
            )
            blockers.append(f"创意 Claim 审核仍未放行：{labels}")

    review_cases = AdReviewCase.query.filter_by(campaign_draft_id=campaign.id).all()
    blocking_review_cases = [
        case for case in review_cases if case.status in {"open", "appeal_submitted", "rejected"}
    ]
    if blocking_review_cases:
        labels = ", ".join(
            sorted({f"{case.policy_topic}:{case.status}" for case in blocking_review_cases})
        )
        blockers.append(f"广告审核案例仍未关闭：{labels}")

    return blockers
