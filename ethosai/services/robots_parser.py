import os
import logging
import requests

from urllib.parse import urlparse
from typing import Dict, Optional

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Configurable AI agents ──────────────────────────────
DEFAULT_AI_AGENTS = [
    "GPTBot",
    "ClaudeBot",
    "anthropic-ai"
]

AI_AGENTS = os.getenv(
    "AI_AGENTS",
    ",".join(DEFAULT_AI_AGENTS)
).split(",")

# ── Config ──────────────────────────────────────────────
REQUEST_TIMEOUT = int(os.getenv("ROBOTS_TIMEOUT", 10))

USER_AGENT = os.getenv(
    "ROBOTS_USER_AGENT",
    "EthosAI-Bot"
)


# ── Build robots.txt URL ────────────────────────────────
def build_robots_url(url: str) -> str:

    parsed = urlparse(url)

    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


# ── Fetch robots.txt ────────────────────────────────────
def fetch_robots_txt(robots_url: str) -> Optional[str]:

    try:

        response = requests.get(
            robots_url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": USER_AGENT
            }
        )

        if response.status_code == 200:
            return response.text

        logger.warning(
            f"robots.txt unavailable: {robots_url} "
            f"(status={response.status_code})"
        )

        return None

    except requests.RequestException as e:

        logger.error(
            f"Failed to fetch robots.txt from {robots_url}: {e}"
        )

        return None


# ── Detect AI permissions ───────────────────────────────
def detect_ai_permission(robots_text: str) -> str:

    if not robots_text:
        return "unknown"

    robots_lower = robots_text.lower()

    # Look for AI-specific restrictions
    for bot in AI_AGENTS:

        bot_lower = bot.lower()

        if bot_lower in robots_lower:

            # simple deny detection
            if "disallow: /" in robots_lower:
                return "no"

            return "partial"

    return "yes"


# ── Main parser ─────────────────────────────────────────
def parse_robots(url: str) -> Dict:

    robots_url = build_robots_url(url)

    logger.info(f"Parsing robots.txt: {robots_url}")

    robots_text = fetch_robots_txt(robots_url)

    if robots_text:

        permission = detect_ai_permission(robots_text)

        return {
            "success": True,
            "has_robots_txt": "yes",
            "robots_allows_ai": permission,
            "robots_raw": robots_text,
            "robots_url": robots_url
        }

    return {
        "success": False,
        "has_robots_txt": "unknown",
        "robots_allows_ai": "unknown",
        "robots_raw": "",
        "robots_url": robots_url
    }