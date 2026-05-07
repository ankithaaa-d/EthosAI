from services.robots_parser import parse_robots

from services.tos_fetcher import fetch_tos

from services.metadata_extractor import (
    extract_metadata
)

from services.policy_feature_builder import (
    build_all_features
)

# ── ML inference ────────────────────────────────────────
from ml.permission_inference import (
    predict_permission
)

from ml.price_inference import (
    predict_price_with_confidence
)

from ml.similarity_model import (
    get_best_match
)

# ── Decision engine ─────────────────────────────────────
from services.decision_engine import (
    make_final_decision
)

# ── OpenCLAW semantic reasoning ─────────────────────────
from ml.openclaw_model import (
    analyze_policy_semantics
)

# ── Ollama reasoning layer ──────────────────────────────
from services.reasoning_engine import (
    generate_reasoning
)

# ── Logging ─────────────────────────────────────────────
import logging

logger = logging.getLogger(__name__)


# ── Main orchestration pipeline ─────────────────────────
def analyze_url(url: str):

    logger.info(f"Starting analysis for: {url}")

    try:

        # ====================================================
        # Phase 1 — Data Extraction
        # ====================================================

        logger.info("Running extraction phase")

        robots_data = parse_robots(url)

        tos_data = fetch_tos(url)

        metadata = extract_metadata(url)

        # ====================================================
        # Phase 2 — Feature Engineering
        # ====================================================

        logger.info("Building ML features")

        features = build_all_features(
            metadata,
            robots_data,
            tos_data
        )

        # ====================================================
        # Phase 3 — ML Inference
        # ====================================================

        logger.info("Running ML inference")

        permission_result = predict_permission(
            features["permission_features"]
        )

        price_result = (
            predict_price_with_confidence(
                text=features[
                    "price_features"
                ]["notes"],

                authority_score=features[
                    "price_features"
                ]["authority_score"]
            )
        )

        similarity_result = get_best_match(
            features[
                "similarity_features"
            ]["text"]
        )

        # ====================================================
        # Phase 4 — Decision Engine
        # ====================================================

        logger.info("Running decision engine")

        final_decision = make_final_decision(
            permission_result,
            price_result,
            similarity_result
        )

        # ====================================================
        # Phase 5 — OpenCLAW Semantic Analysis
        # ====================================================

        logger.info("Running semantic policy analysis")

        semantic_analysis = (
            analyze_policy_semantics(

                tos_data.get(
                    "tos_text",
                    ""
                ) +

                " " +

                robots_data.get(
                    "robots_raw",
                    ""
                )
            )
        )

        # ====================================================
        # Phase 6 — Ollama Reasoning Layer
        # ====================================================

        logger.info("Generating explainable reasoning")

        reasoning = generate_reasoning(

            url=url,

            decision=final_decision,

            predictions={

                "permission":
                    permission_result,

                "price":
                    price_result,

                "similarity":
                    similarity_result
            },

            semantic_analysis=
                semantic_analysis
        )

        logger.info("Analysis completed successfully")

        # ====================================================
        # Final Structured Response
        # ====================================================

        return {

            "success": True,

            "url": url,

            "robots":
                robots_data,

            "tos":
                tos_data,

            "metadata":
                metadata,

            "features":
                features,

            "predictions": {

                "permission":
                    permission_result,

                "price":
                    price_result,

                "similarity":
                    similarity_result
            },

            "decision":
                final_decision,

            "semantic_analysis":
                semantic_analysis,

            "reasoning":
                reasoning
        }

    except Exception as e:

        logger.exception(
            "Pipeline execution failed"
        )

        return {

            "success": False,

            "url": url,

            "error": str(e)
        }