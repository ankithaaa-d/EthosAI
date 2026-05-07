import requests


OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

MODEL_NAME = "llama3"


def generate_reasoning(

    url: str,

    decision: dict,

    predictions: dict,

    semantic_analysis: dict
):

    prompt = f"""

You are an AI policy compliance assistant.

Analyze the following website policy results
and explain the reasoning clearly.

URL:
{url}

Final Decision:
{decision}

ML Predictions:
{predictions}

Semantic Policy Analysis:
{semantic_analysis}

Explain:

1. Why the decision was made
2. What policy signals were detected
3. Whether AI scraping appears allowed
4. Whether licensing/paywalls exist

Keep explanation concise and professional.
"""

    response = requests.post(

        OLLAMA_URL,

        json={

            "model":
                MODEL_NAME,

            "prompt":
                prompt,

            "stream":
                False
        }
    )

    result = response.json()

    return result.get(
        "response",
        "No reasoning generated"
    )