import os
import logging
import requests

from bs4 import BeautifulSoup
from typing import Dict, Optional

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Config ──────────────────────────────────────────────
COMMON_TOS_PATHS = [
    "/terms",
    "/tos",
    "/terms-of-service",
    "/terms-and-conditions",
    "/privacy",
    "/legal",
    "/wiki/Wikipedia:Terms_of_Use"
]

REQUEST_TIMEOUT = int(os.getenv("TOS_TIMEOUT", 10))

USER_AGENT = os.getenv(
    "TOS_USER_AGENT",
    "EthosAI-Bot"
)

MAX_TEXT_LENGTH = int(
    os.getenv("MAX_TOS_TEXT_LENGTH", 5000)
)


# ── Clean HTML ──────────────────────────────────────────
def extract_clean_text(html: str) -> str:

    soup = BeautifulSoup(html, "html.parser")

    # remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # normalize whitespace
    text = " ".join(text.split())

    return text[:MAX_TEXT_LENGTH]


# ── Fetch single page ───────────────────────────────────
def fetch_page(url: str) -> Optional[str]:

    try:

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": USER_AGENT
            }
        )

        if response.status_code == 200:
            return response.text

        logger.warning(
            f"Failed ToS fetch: {url} "
            f"(status={response.status_code})"
        )

        return None

    except requests.RequestException as e:

        logger.error(f"ToS request failed: {url} | {e}")

        return None


# ── Main fetcher ────────────────────────────────────────
def fetch_tos(base_url: str) -> Dict:

    base_url = base_url.rstrip("/")

    for path in COMMON_TOS_PATHS:

        full_url = f"{base_url}{path}"

        logger.info(f"Trying ToS URL: {full_url}")

        html = fetch_page(full_url)

        if html:

            clean_text = extract_clean_text(html)

            # basic validation
            if len(clean_text) > 200:

                return {
                    "success": True,
                    "tos_found": True,
                    "tos_url": full_url,
                    "tos_text": clean_text
                }

    return {
        "success": False,
        "tos_found": False,
        "tos_url": None,
        "tos_text": ""
    }