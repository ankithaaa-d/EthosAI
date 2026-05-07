import logging

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)


# ── Price inference ─────────────────────────────────────
def predict_price_with_confidence(
    text: str,
    authority_score: int = 50
):

    logger.info("Running price inference")

    text_lower = text.lower() if text else ""

    # ── Keyword-based heuristic detection ───────────
    paid_keywords = [
        "paywall",
        "subscription",
        "premium",
        "paid access",
        "enterprise",
        "licensed"
    ]

    free_keywords = [
        "open source",
        "free",
        "public domain",
        "creative commons"
    ]

    paid_score = sum(
        1 for kw in paid_keywords
        if kw in text_lower
    )

    free_score = sum(
        1 for kw in free_keywords
        if kw in text_lower
    )

    # ── Label determination ─────────────────────────
    if paid_score > free_score:

        label = "paid"

        raw_confidence = min(
            0.5 + (paid_score * 0.1),
            0.95
        )

    elif free_score > paid_score:

        label = "free"

        raw_confidence = min(
            0.5 + (free_score * 0.1),
            0.95
        )

    else:

        label = "unknown"
        raw_confidence = 0.5

    # ── Authority adjustment ────────────────────────
    confidence = round(
        raw_confidence *
        (authority_score / 100),
        4
    )

    return {

        "label":
            label,

        "confidence":
            confidence,

        "paid_signals":
            paid_score,

        "free_signals":
            free_score
    }
