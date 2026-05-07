def generate_llm_reasoning(data: dict):

    metadata = data.get("metadata", {})
    value = data.get("value", {})
    cost_risk = data.get("cost_risk", {})
    decision = data.get("decision", {})

    prompt = f"""
You are an AI decision analyst.

Analyze this website evaluation:

Metadata:
Title: {metadata.get("title")}
Description: {metadata.get("description")}
Headings: {metadata.get("headings")}

Value Score: {value.get("value_score")}
Cost Score: {cost_risk.get("cost_score")}
Risk Score: {cost_risk.get("risk_score")}

Current Decision: {decision.get("action")}

Answer:
1. Is the decision correct?
2. Give a short explanation
3. Suggest better decision if needed
"""

    # Placeholder (we will connect Ollama next)
    return {
        "llm_review": "LLM integration pending",
        "confidence": 0.5
    }