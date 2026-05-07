import os
import logging
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Config ──────────────────────────────────────────────
REQUEST_TIMEOUT = int(os.getenv("METADATA_TIMEOUT", 10))

USER_AGENT = os.getenv(
    "METADATA_USER_AGENT",
    "EthosAI-Bot"
)

MAX_RAW_TEXT = int(
    os.getenv("MAX_RAW_TEXT_LENGTH", 5000)
)


# ── Extract clean text ──────────────────────────────────
def extract_clean_text(soup: BeautifulSoup) -> str:

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    text = " ".join(text.split())

    return text[:MAX_RAW_TEXT]


# ── Main extractor ──────────────────────────────────────
def extract_metadata(url: str) -> Dict:

    try:

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": USER_AGENT
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else ""
        )

        description = ""

        meta_desc = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_desc:
            description = meta_desc.get("content", "").strip()

        headings = [
            h.get_text(strip=True)
            for h in soup.find_all(["h1", "h2"])
        ]

        raw_text = extract_clean_text(soup)

        domain = urlparse(url).netloc

        return {
            "success": True,
            "url": url,
            "domain": domain,
            "title": title,
            "description": description,
            "headings": headings,
            "raw_text": raw_text
        }

    except requests.RequestException as e:

        logger.error(f"Metadata extraction failed: {url} | {e}")

        return {
            "success": False,
            "url": url,
            "domain": "",
            "title": "",
            "description": "",
            "headings": [],
            "raw_text": ""
        }