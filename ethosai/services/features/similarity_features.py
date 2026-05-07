from typing import Dict


def build_similarity_features(
    metadata: Dict,
    robots_data: Dict,
    tos_data: Dict
) -> Dict:

    signals = []

    if robots_data.get(
        "robots_allows_ai"
    ) == "no":

        signals.append("robots_blocked")

    combined_text = (
        metadata.get("description", "") +
        " " +
        metadata.get("raw_text", "") +
        " " +
        tos_data.get("tos_text", "")
    )

    lower = combined_text.lower()

    if (
        "paywall" in lower or
        "subscription" in lower
    ):

        signals.append("strong_paywall")

    if (
        "license" in lower or
        "licensed" in lower
    ):

        signals.append("license_required")

    return {

        "url":
            metadata.get("url", ""),

        "text":
            (
                metadata.get("url", "") +
                " " +
                " ".join(signals) +
                " " +
                metadata.get(
                    "description",
                    ""
                )
            )
    }