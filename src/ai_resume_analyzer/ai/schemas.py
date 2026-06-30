from pydantic import BaseModel


class AIAnalysis(BaseModel):
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
