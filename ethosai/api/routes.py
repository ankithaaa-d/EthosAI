from fastapi import APIRouter, HTTPException, Depends, Security
from pydantic import BaseModel, Field
from typing import Optional

from core.pipeline import analyze_url
from api.auth import get_api_key

router = APIRouter()


class AnalyzeRequest(BaseModel):
    url: str = Field(..., description="The URL of the website to analyze for ethical compliance.")


@router.get("/health")
def health_check():
    """Returns the health status of the EthosAI service."""
    return {"status": "healthy", "service": "EthosAI"}


@router.get("/.well-known/ai-plugin.json", include_in_schema=False)
def get_ai_manifest():
    """Returns the AI manifest for agent auto-discovery."""
    return {
        "schema_version": "v1",
        "name_for_model": "EthosAI",
        "name_for_human": "EthosAI Compliance Tool",
        "description_for_model": "Middleware that evaluates website ethical policies, robots.txt, and terms of service to determine AI compliance and risks.",
        "description_for_human": "Check if a website allows AI scraping and what the ethical implications are.",
        "api": {
            "type": "openapi",
            "url": "/openapi.json"
        },
        "logo_url": "https://ethosai.com/logo.png",
        "contact_email": "support@ethosai.com"
    }


@router.post("/analyze")
def analyze(request: AnalyzeRequest, api_key: str = Depends(get_api_key)):
    """
    Analyzes a website URL to determine compliance with AI policies.
    Returns structured risk assessment, legal signals, and explainable reasoning.
    """
    if not request.url:
        raise HTTPException(
            status_code=400,
            detail="URL is required"
        )

    result = analyze_url(request.url)

    return {
        "success": True,
        "data": result
    }