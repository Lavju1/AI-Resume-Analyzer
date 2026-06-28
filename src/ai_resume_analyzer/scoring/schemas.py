from pydantic import BaseModel, Field


class ATSSectionScores(BaseModel):
    contact: int = Field(ge=0, le=20)
    skills: int = Field(ge=0, le=20)
    education: int = Field(ge=0, le=20)
    experience: int = Field(ge=0, le=20)
    projects: int = Field(ge=0, le=20)


class ATSScore(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    section_scores: ATSSectionScores
    missing_sections: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
