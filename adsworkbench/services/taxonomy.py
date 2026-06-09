from __future__ import annotations


REQUIRED_CAMPAIGN_TOKENS = {
    "channel",
    "country",
    "language",
    "vertical",
    "offer",
    "intent",
    "network",
    "device",
    "yyyymm",
    "test",
}

REQUIRED_UTM_FIELDS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_id",
}

REQUIRED_LABEL_GROUPS = {
    "lifecycle",
    "risk",
    "experiment",
    "batch",
}


def calculate_taxonomy_review(
    *,
    campaign_name: str,
    ad_group_name: str,
    labels_text: str,
    utm_source: str,
    utm_medium: str,
    utm_campaign: str,
    utm_id: str,
    utm_content: str,
    utm_term: str,
    valuetrack_template: str,
    custom_parameter_map: str,
    subid_map: str,
    dimension_dictionary_version: str,
    parameter_map_version: str,
    landing_version: str,
    link_version: str,
    creative_version: str,
    payload_hash: str,
    report_join_gap_count: int,
    gclid_preserved: bool,
    click_id_preserved: bool,
    lowercase_normalized: bool,
    url_encoded: bool,
    no_pii_in_url: bool,
    no_sensitive_attributes: bool,
    human_review: bool,
) -> dict[str, object]:
    campaign_tokens = _campaign_tokens(campaign_name)
    missing_campaign_tokens = sorted(REQUIRED_CAMPAIGN_TOKENS - campaign_tokens)
    missing_utm_fields = _missing_utm_fields(
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        utm_id=utm_id,
    )
    label_groups = _label_groups(labels_text)
    missing_label_groups = sorted(REQUIRED_LABEL_GROUPS - label_groups)
    valuetrack_fields = _valuetrack_fields(valuetrack_template)

    blockers = _blockers(
        missing_campaign_tokens=missing_campaign_tokens,
        missing_utm_fields=missing_utm_fields,
        missing_label_groups=missing_label_groups,
        ad_group_name=ad_group_name,
        utm_content=utm_content,
        utm_term=utm_term,
        valuetrack_fields=valuetrack_fields,
        custom_parameter_map=custom_parameter_map,
        subid_map=subid_map,
        dimension_dictionary_version=dimension_dictionary_version,
        parameter_map_version=parameter_map_version,
        landing_version=landing_version,
        link_version=link_version,
        creative_version=creative_version,
        payload_hash=payload_hash,
        report_join_gap_count=report_join_gap_count,
        gclid_preserved=gclid_preserved,
        click_id_preserved=click_id_preserved,
        lowercase_normalized=lowercase_normalized,
        url_encoded=url_encoded,
        no_pii_in_url=no_pii_in_url,
        no_sensitive_attributes=no_sensitive_attributes,
        human_review=human_review,
    )

    score = 0
    score += _token_points(missing_campaign_tokens)
    score += 8 if ad_group_name.strip() else 0
    score += _label_points(missing_label_groups)
    score += _utm_points(missing_utm_fields, utm_content, utm_term)
    score += _valuetrack_points(valuetrack_fields)
    score += 8 if custom_parameter_map.strip() else 0
    score += 8 if subid_map.strip() else 0
    score += 6 if dimension_dictionary_version.strip() else 0
    score += 6 if parameter_map_version.strip() else 0
    score += _version_points(landing_version, link_version, creative_version, payload_hash)
    score += 8 if report_join_gap_count == 0 else max(0, 5 - report_join_gap_count)
    score += 4 if gclid_preserved else 0
    score += 4 if click_id_preserved else 0
    score += 3 if lowercase_normalized else 0
    score += 3 if url_encoded else 0
    score += 5 if no_pii_in_url else 0
    score += 5 if no_sensitive_attributes else 0
    score += 5 if human_review else 0
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(
            score=score,
            blockers=blockers,
            no_pii_in_url=no_pii_in_url,
            no_sensitive_attributes=no_sensitive_attributes,
            report_join_gap_count=report_join_gap_count,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            no_pii_in_url=no_pii_in_url,
            no_sensitive_attributes=no_sensitive_attributes,
            report_join_gap_count=report_join_gap_count,
        ),
        "missing_campaign_tokens": missing_campaign_tokens,
        "missing_utm_fields": missing_utm_fields,
        "missing_label_groups": missing_label_groups,
        "valuetrack_fields": sorted(valuetrack_fields),
        "blockers": blockers,
    }


def _campaign_tokens(campaign_name: str) -> set[str]:
    parts = [part.strip().lower() for part in campaign_name.replace("_", "-").split("-")]
    token_count = len([part for part in parts if part])
    if token_count >= 10:
        return set(REQUIRED_CAMPAIGN_TOKENS)
    token_order = [
        "channel",
        "country",
        "language",
        "vertical",
        "offer",
        "intent",
        "network",
        "device",
        "yyyymm",
        "test",
    ]
    return set(token_order[:token_count])


def _missing_utm_fields(
    *,
    utm_source: str,
    utm_medium: str,
    utm_campaign: str,
    utm_id: str,
) -> list[str]:
    values = {
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
        "utm_id": utm_id,
    }
    return sorted(key for key, value in values.items() if not value.strip())


def _label_groups(labels_text: str) -> set[str]:
    text = labels_text.lower()
    groups: set[str] = set()
    for group in REQUIRED_LABEL_GROUPS:
        if group in text:
            groups.add(group)
    return groups


def _valuetrack_fields(valuetrack_template: str) -> set[str]:
    fields: set[str] = set()
    for field in [
        "campaignid",
        "adgroupid",
        "keyword",
        "matchtype",
        "creative",
        "device",
        "network",
        "targetid",
    ]:
        if "{" + field + "}" in valuetrack_template.lower():
            fields.add(field)
    return fields


def _token_points(missing_campaign_tokens: list[str]) -> int:
    return max(0, 12 - len(missing_campaign_tokens) * 2)


def _label_points(missing_label_groups: list[str]) -> int:
    return max(0, 10 - len(missing_label_groups) * 2)


def _utm_points(missing_utm_fields: list[str], utm_content: str, utm_term: str) -> int:
    score = max(0, 12 - len(missing_utm_fields) * 3)
    if utm_content.strip():
        score += 2
    if utm_term.strip():
        score += 2
    return min(score, 16)


def _valuetrack_points(valuetrack_fields: set[str]) -> int:
    required = {"campaignid", "adgroupid", "keyword", "matchtype", "device", "network"}
    missing = required - valuetrack_fields
    return max(0, 12 - len(missing) * 2)


def _version_points(
    landing_version: str,
    link_version: str,
    creative_version: str,
    payload_hash: str,
) -> int:
    values = [landing_version, link_version, creative_version, payload_hash]
    return sum(3 for value in values if value.strip())


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    no_pii_in_url: bool,
    no_sensitive_attributes: bool,
    report_join_gap_count: int,
) -> str:
    if not no_pii_in_url or not no_sensitive_attributes or report_join_gap_count > 0:
        return "high"
    if score >= 80 and not blockers:
        return "low"
    if score >= 60:
        return "medium"
    return "high"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    no_pii_in_url: bool,
    no_sensitive_attributes: bool,
    report_join_gap_count: int,
) -> str:
    if not no_pii_in_url or not no_sensitive_attributes:
        return "remove_sensitive_url_data"
    if report_join_gap_count > 0:
        return "fix_report_join_gaps"
    if blockers:
        return "fix_taxonomy_mapping"
    if score >= 80:
        return "approve_export"
    if score >= 60:
        return "dictionary_review"
    return "hold_for_mapping"


def _blockers(
    *,
    missing_campaign_tokens: list[str],
    missing_utm_fields: list[str],
    missing_label_groups: list[str],
    ad_group_name: str,
    utm_content: str,
    utm_term: str,
    valuetrack_fields: set[str],
    custom_parameter_map: str,
    subid_map: str,
    dimension_dictionary_version: str,
    parameter_map_version: str,
    landing_version: str,
    link_version: str,
    creative_version: str,
    payload_hash: str,
    report_join_gap_count: int,
    gclid_preserved: bool,
    click_id_preserved: bool,
    lowercase_normalized: bool,
    url_encoded: bool,
    no_pii_in_url: bool,
    no_sensitive_attributes: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if missing_campaign_tokens:
        blockers.append("campaign name is missing required tokens")
    if not ad_group_name.strip():
        blockers.append("ad group name is missing")
    if missing_label_groups:
        blockers.append("label groups are incomplete")
    if missing_utm_fields:
        blockers.append("required UTM fields are missing")
    if not utm_content.strip() or not utm_term.strip():
        blockers.append("utm_content or utm_term is missing")
    required_vt = {"campaignid", "adgroupid", "keyword", "matchtype", "device", "network"}
    if required_vt - valuetrack_fields:
        blockers.append("ValueTrack template is missing core click context")
    if not custom_parameter_map.strip():
        blockers.append("custom parameter map is missing")
    if not subid_map.strip():
        blockers.append("SubID map is missing")
    if not dimension_dictionary_version.strip():
        blockers.append("dimension dictionary version is missing")
    if not parameter_map_version.strip():
        blockers.append("parameter map version is missing")
    if not landing_version.strip() or not link_version.strip() or not creative_version.strip():
        blockers.append("landing, link, or creative version is missing")
    if not payload_hash.strip():
        blockers.append("campaign payload hash is missing")
    if report_join_gap_count > 0:
        blockers.append("report join audit has missing rows")
    if not gclid_preserved:
        blockers.append("gclid or auto-tagging join key is not preserved")
    if not click_id_preserved:
        blockers.append("internal click_id is not preserved")
    if not lowercase_normalized:
        blockers.append("taxonomy values are not lowercase-normalized")
    if not url_encoded:
        blockers.append("URL parameters are not encoding-safe")
    if not no_pii_in_url:
        blockers.append("URL or SubID contains PII-like data")
    if not no_sensitive_attributes:
        blockers.append("URL or taxonomy contains sensitive attributes")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
