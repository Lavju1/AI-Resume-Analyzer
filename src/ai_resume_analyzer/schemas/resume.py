from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ai_resume_analyzer.ai.schemas import AIAnalysis
from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.feedback.schemas import ResumeFeedback
from ai_resume_analyzer.scoring.schemas import ATSScore


class ResumeCreate(BaseModel):
    original_filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(min_length=1, max_length=127)
    file_size: int = Field(ge=0)


class ResumeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    original_filename: str
    content_type: str
    file_size: int
    upload_status: str
    created_at: datetime
    updated_at: datetime


class ResumeUploadResponse(BaseModel):
    resume: ResumeRead
    parsed_text: str
    extracted_data: ResumeData
    ats_score: ATSScore
    feedback: ResumeFeedback
    ai_analysis: AIAnalysis


class ResumeJobMatchRequest(BaseModel):
    resume_id: UUID
    job_description_text: str = Field(min_length=1)


class ResumeJobMatchResponse(BaseModel):
    overall_match: float
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    ai_analysis: AIAnalysis
