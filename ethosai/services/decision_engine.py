from typing import Dict


# ── Thresholds ──────────────────────────────────────────
LOW_CONFIDENCE_THRESHOLD = 0.60

HIGH_SIMILARITY = "HIGH_SIMILARITY"


# ── Main decision engine ────────────────────────────────
def make_final_decision(
    permission_result: Dict,
    price_result: Dict,
    similarity_result: Dict
) -> Dict:

    permission_label = (
        permission_result.get(
            "label",
            "unknown"
        )
    )

    permission_confidence = (
        permission_result.get(
            "confidence",
            0.0
        )
    )

    price_label = (
        price_result.get(
            "label",
            "unknown"
        )
    )

    price_confidence = (
        price_result.get(
            "confidence",
            0.0
        )
    )

    similarity_status = (
        similarity_result.get(
            "status",
            "LOW_SIMILARITY"
        )
    )

    # ── Low confidence handling ────────────────────────
    if (
        permission_confidence <
        LOW_CONFIDENCE_THRESHOLD
    ):

        return {

            "action": "REVIEW",
            "decision": "review",

            "confidence":
                permission_confidence,
            
            "risk_score": 0.5,

            "reason":
                "Low permission model confidence"
        }

    # ── Hard restriction ───────────────────────────────
    if permission_label == "restricted":

        return {

            "action": "RESTRICT",
            "decision": "restrict",

            "confidence":
                permission_confidence,
            
            "risk_score": 0.95,

            "reason":
                "Permission model marked content as restricted"
        }

    # ── Paid/licensed content ──────────────────────────
    if (
        price_label == "paid" and
        permission_label != "allowed"
    ):

        return {

            "action": "LICENSE",
            "decision": "license",

            "confidence":
                min(
                    permission_confidence,
                    price_confidence
                ),
            
            "risk_score": 0.6,

            "reason":
                "Paid/licensed content detected"
        }

    # ── High similarity reusable content ───────────────
    if (
        similarity_status ==
        HIGH_SIMILARITY and

        permission_label == "allowed"
    ):

        return {

            "action": "CACHE",
            "decision": "cache",

            "confidence":
                permission_confidence,
            
            "risk_score": 0.05,

            "reason":
                "High similarity reusable content"
        }

    # ── Safe content ───────────────────────────────────
    if permission_label in [
        "allowed",
        "conditional"
    ]:
        action = "ALLOW"
        risk_score = 0.1 if permission_label == "allowed" else 0.4
        
        return {
            "action": action,
            "decision": action.lower(),
            "confidence": permission_confidence,
            "risk_score": risk_score,
            "reason": "Content allowed under current policy"
        }

    # ── Fallback ───────────────────────────────────────
    return {
        "action": "REVIEW",
        "decision": "review",
        "confidence": 0.5,
        "risk_score": 0.7,
        "reason": "Unable to determine safe action"
    }