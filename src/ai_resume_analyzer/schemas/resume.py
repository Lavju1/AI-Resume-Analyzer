from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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
