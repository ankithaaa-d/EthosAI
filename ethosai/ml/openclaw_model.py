import logging
import requests

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Ollama config ───────────────────────────────────────
OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

MODEL_NAME = "llama3"


# ── Semantic policy analysis ────────────────────────────
def analyze_policy_semantics(
    policy_text: str
):

    logger.info(
        "Running OpenCLAW semantic analysis"
    )

    if not policy_text or not policy_text.strip():

        return {
            "status": "no_policy_text",
            "analysis": None
        }

    prompt = f"""
You are a legal AI policy analyst.

Analyze the following website policy text
and determine:

1. Whether AI training/scraping is allowed
2. Whether there are licensing restrictions
3. Key legal signals detected
4. Overall risk level (low/medium/high)

Policy text:
{policy_text[:3000]}

Respond with a structured analysis.
"""

    try:

        response = requests.post(

            OLLAMA_URL,

            json={

                "model":
                    MODEL_NAME,

                "prompt":
                    prompt,

                "stream":
                    False
            },

            timeout=30
        )

        result = response.json()

        return {

            "status": "success",

            "analysis":
                result.get(
                    "response",
                    "No analysis generated"
                )
        }

    except Exception as e:

        logger.warning(
            f"OpenCLAW analysis failed: {e}"
        )

        return {

            "status": "error",

            "analysis":
                f"Analysis unavailable: {str(e)}"
        }
