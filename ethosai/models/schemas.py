from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    url: str
    robots: dict | None
    tos: dict | None
    metadata: dict | None
    decision: dict | None