import os
import logging
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from config import (
    SIMILARITY_EMBEDDINGS,
    SIMILARITY_DATA
)

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Config ──────────────────────────────────────────────
EMBED_PATH = SIMILARITY_EMBEDDINGS
DATA_PATH = SIMILARITY_DATA

HIGH_SIMILARITY_THRESHOLD = 0.72
MEDIUM_SIMILARITY_THRESHOLD = 0.60

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# ── Lazy-loaded resources ───────────────────────────────
_model = None
_embeddings = None
_df = None
_initialized = False


def _load_resources():

    global _model, _embeddings, _df, _initialized

    if _initialized:
        return

    if not EMBED_PATH or not os.path.exists(
        EMBED_PATH
    ):

        raise FileNotFoundError(
            f"Similarity embeddings not found: "
            f"{EMBED_PATH}"
        )

    if not DATA_PATH or not os.path.exists(
        DATA_PATH
    ):

        raise FileNotFoundError(
            f"Similarity dataset not found: "
            f"{DATA_PATH}"
        )

    # ── Load embedding model ────────────────────────
    logger.info(
        "Loading similarity embedding model..."
    )

    _model = SentenceTransformer(MODEL_NAME)

    # ── Load embeddings/data ────────────────────────
    logger.info(
        "Loading similarity embeddings..."
    )

    _embeddings = np.load(EMBED_PATH)

    logger.info(
        "Loading processed similarity dataset..."
    )

    _df = pd.read_csv(DATA_PATH)

    # ── Validation ──────────────────────────────────
    required_columns = [
        "url",
        "text"
    ]

    for col in required_columns:

        if col not in _df.columns:

            raise ValueError(
                f"Missing required column: {col}"
            )

    logger.info(
        f"Loaded {len(_df)} similarity records"
    )

    _initialized = True



# ── Similarity search ───────────────────────────────────
def find_similar(
    query: str,
    top_k: int = 5
):

    _load_resources()

    if not query or not query.strip():

        raise ValueError(
            "Query cannot be empty"
        )

    query = query.lower().strip()

    # Encode query
    query_embedding = _model.encode(
        [query],
        convert_to_numpy=True
    )

    # Compute similarity
    scores = cosine_similarity(
        query_embedding,
        _embeddings
    )[0]

    # Top matches
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for idx in top_indices:

        row = _df.iloc[idx]

        results.append({

            "url":
                row["url"],

            "text":
                row["text"][:200],

            "score":
                round(float(scores[idx]), 4)
        })

    return results


# ── Main inference API ──────────────────────────────────
def get_best_match(
    query: str
):

    results = find_similar(
        query=query,
        top_k=1
    )

    if not results:

        return {

            "status":
                "LOW_SIMILARITY",

            "match":
                None
        }

    best = results[0]

    score = best["score"]

    # ── High similarity ────────────────────────────────
    if score >= HIGH_SIMILARITY_THRESHOLD:

        return {

            "status":
                "HIGH_SIMILARITY",

            "match":
                best
        }

    # ── Medium similarity ──────────────────────────────
    if score >= MEDIUM_SIMILARITY_THRESHOLD:

        return {

            "status":
                "MEDIUM_SIMILARITY",

            "match":
                best
        }

    # ── Low similarity ─────────────────────────────────
    return {

        "status":
            "LOW_SIMILARITY",

        "match":
            None
    }


# ── Optional local testing ──────────────────────────────
if __name__ == "__main__":

    test_query = (
        "subscription-based "
        "news website with paywall"
    )

    result = get_best_match(
        test_query
    )

    print("\nSimilarity Result:\n")

    print(result)