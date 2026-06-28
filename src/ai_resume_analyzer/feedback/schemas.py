from typing import Literal

from pydantic import BaseModel


class FeedbackItem(BaseModel):
    category: str
    severity: Literal["info", "warning", "success"]
    title: str
    message: str


class ResumeFeedback(BaseModel):
    overall_summary: str
    feedback: list[FeedbackItem]
