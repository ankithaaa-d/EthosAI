import os

from dotenv import load_dotenv

# ── Load environment variables ─────────────────────────
load_dotenv()


# ── Model paths ────────────────────────────────────────
PRICE_MODEL_PATH = os.getenv(
    "PRICE_MODEL_PATH"
)

PERMISSION_MODEL_PATH = os.getenv(
    "PERMISSION_MODEL_PATH"
)

SIMILARITY_EMBEDDINGS = os.getenv(
    "SIMILARITY_EMBEDDINGS"
)

SIMILARITY_DATA = os.getenv(
    "SIMILARITY_DATA"
)


# ── General configs ────────────────────────────────────
REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        10
    )
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

ETHOS_API_KEY = os.getenv(
    "ETHOS_API_KEY",
    "ethos_default_dev_key"
)