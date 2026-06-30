from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    text: str


class JobMatchResult(BaseModel):
    overall_match: float
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
