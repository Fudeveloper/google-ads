/**
 * Google Ads Scripts payload preview template.
 *
 * Paste the JSON exported from /campaigns/<id>/export.script.json into
 * PAYLOAD_JSON, run in Google Ads Scripts, review logs and bulk upload preview,
 * then apply only after human approval.
 *
 * This template does not use browser cookies, login sessions, proxies,
 * cloaking, click simulation, or security-challenge bypasses.
 */

var PREVIEW_ONLY = true;
var ALLOW_APPLY = false;

var PAYLOAD_JSON = String.raw`
{
  "mode": "manual_review_required",
  "campaign": {
    "name": "example-campaign",
    "channel": "Google Search",
    "daily_budget": 30,
    "bid_strategy": "Maximize Clicks",
    "final_url": "https://example.com",
    "status": "draft"
  },
  "offer": {
    "id": 1,
    "name": "Example Offer",
    "vertical": "example",
    "country": "US",
    "language": "en"
  },
  "creative": {
    "angle": "example",
    "headlines": ["Example headline 1", "Example headline 2", "Example headline 3"],
    "descriptions": ["Example description 1", "Example description 2"],
    "keywords": ["example keyword"]
  },
  "safety": {
    "no_cookie_automation": true,
    "requires_human_approval": true
  }
}
`;

function main() {
  var payload = parsePayload_(PAYLOAD_JSON);
  validatePayload_(payload);

  var rows = buildCampaignRows_(payload);
  Logger.log("Payload validated. no_cookie_automation=true, human approval required.");
  Logger.log("Rows prepared for preview: " + rows.length);
  rows.forEach(function(row, index) {
    Logger.log("Row " + (index + 1) + ": " + JSON.stringify(row));
  });

  previewBulkUpload_(rows);

  if (!PREVIEW_ONLY && ALLOW_APPLY) {
    throw new Error(
      "Apply mode is intentionally disabled in this template. Review the preview, " +
      "record approval, then adapt this script under your own Google Ads governance."
    );
  }
}

function parsePayload_(jsonText) {
  try {
    return JSON.parse(jsonText);
  } catch (error) {
    throw new Error("Invalid JSON payload: " + error.message);
  }
}

function validatePayload_(payload) {
  if (!payload || payload.mode !== "manual_review_required") {
    throw new Error("Payload mode must be manual_review_required.");
  }
  if (!payload.safety || payload.safety.no_cookie_automation !== true) {
    throw new Error("Payload must include safety.no_cookie_automation=true.");
  }
  if (payload.safety.requires_human_approval !== true) {
    throw new Error("Payload must include safety.requires_human_approval=true.");
  }
  if (!payload.campaign || !payload.campaign.name) {
    throw new Error("Payload must include campaign.name.");
  }
  if (!isHttpsUrl_(payload.campaign.final_url)) {
    throw new Error("Final URL must be HTTPS.");
  }
  var budget = Number(payload.campaign.daily_budget);
  if (!isFinite(budget) || budget <= 0) {
    throw new Error("Daily budget must be positive.");
  }
  if (budget > 500) {
    throw new Error("Daily budget exceeds template guardrail. Review budget pacing first.");
  }
  var creative = payload.creative || {};
  if (!creative.headlines || creative.headlines.length < 3) {
    throw new Error("At least 3 headlines are required for preview.");
  }
  if (!creative.descriptions || creative.descriptions.length < 2) {
    throw new Error("At least 2 descriptions are required for preview.");
  }
  if (!creative.keywords || creative.keywords.length === 0) {
    throw new Error("At least 1 keyword is required for preview.");
  }
}

function buildCampaignRows_(payload) {
  var campaign = payload.campaign;
  var offer = payload.offer || {};
  var creative = payload.creative || {};
  var adGroupName = normalizeName_(offer.vertical || offer.name || "ad-group");
  return creative.keywords.map(function(keyword) {
    return {
      "Campaign": campaign.name,
      "Ad group": adGroupName,
      "Keyword": keyword,
      "Match type": "Phrase",
      "Final URL": campaign.final_url,
      "Daily budget": Number(campaign.daily_budget).toFixed(2),
      "Bid strategy": campaign.bid_strategy || "Maximize Clicks",
      "Status": "Paused",
      "Headlines": creative.headlines.slice(0, 15).join(" | "),
      "Descriptions": creative.descriptions.slice(0, 4).join(" | ")
    };
  });
}

function previewBulkUpload_(rows) {
  var columns = [
    "Campaign",
    "Ad group",
    "Keyword",
    "Match type",
    "Final URL",
    "Daily budget",
    "Bid strategy",
    "Status",
    "Headlines",
    "Descriptions"
  ];
  Logger.log("Preparing bulk upload preview. Check column names against Google Ads bulk upload docs before apply.");
  var upload = AdsApp.bulkUploads().newCsvUpload(columns);
  rows.forEach(function(row) {
    upload.append(row);
  });
  upload.forCampaignManagement();
  upload.preview();
  Logger.log("Bulk upload preview created. Review it in Google Ads before any manual apply.");
}

function isHttpsUrl_(url) {
  return typeof url === "string" && /^https:\/\/[^ ]+$/i.test(url);
}

function normalizeName_(value) {
  return String(value || "ad-group")
    .toLowerCase()
    .replace(/[^a-z0-9-_]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "ad-group";
}
