from pydantic import BaseModel, Field


class ATSCategoryScore(BaseModel):
    score: int = Field(ge=0)
    max_score: int = Field(gt=0)
    feedback: str


class ATSSectionScores(BaseModel):
    contact_information: ATSCategoryScore
    professional_summary: ATSCategoryScore
    skills: ATSCategoryScore
    education: ATSCategoryScore
    experience: ATSCategoryScore
    projects: ATSCategoryScore
    keywords: ATSCategoryScore
    action_verbs: ATSCategoryScore
    quantified_achievements: ATSCategoryScore
    formatting: ATSCategoryScore


class ATSScore(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    section_scores: ATSSectionScores
    missing_sections: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
