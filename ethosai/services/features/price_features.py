from typing import Dict


def detect_paywall(text: str) -> str:

    text = text.lower()

    keywords = [
        "paywall",
        "subscription",
        "premium",
        "paid access"
    ]

    for word in keywords:
        if word in text:
            return "yes"

    return "no"


def detect_license_requirement(text: str) -> str:

    text = text.lower()

    keywords = [
        "licensed",
        "license required",
        "enterprise"
    ]

    for word in keywords:
        if word in text:
            return "yes"

    return "no"


def build_price_features(
    metadata: Dict,
    robots_data: Dict,
    tos_data: Dict
) -> Dict:

    tos_text = tos_data.get("tos_text", "")

    combined_text = (
        metadata.get("description", "") +
        " " +
        metadata.get("raw_text", "") +
        " " +
        tos_text
    )

    return {

        "domain":
            metadata.get("domain", ""),

        "content_type":
            metadata.get("description", ""),

        "has_paywall":
            detect_paywall(combined_text),

        "requires_license":
            detect_license_requirement(
                combined_text
            ),

        "notes":
            combined_text[:3000],

        "authority_score":
            60
    }