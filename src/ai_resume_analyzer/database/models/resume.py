from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import BigInteger, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_resume_analyzer.constants.uploads import UPLOAD_STATUS_PENDING
from ai_resume_analyzer.database.models.base import BaseModel

if TYPE_CHECKING:
    from ai_resume_analyzer.database.models.user import User


class Resume(BaseModel):
    __tablename__ = "resumes"

    user_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    original_filename: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )
    stored_filename: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
        unique=True,
    )
    content_type: Mapped[str] = mapped_column(
        String(length=127),
        nullable=False,
    )
    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        String(length=1024),
        nullable=False,
    )
    upload_status: Mapped[str] = mapped_column(
        String(length=50),
        nullable=False,
        default=UPLOAD_STATUS_PENDING,
        server_default=text(f"'{UPLOAD_STATUS_PENDING}'"),
    )

    user: Mapped["User"] = relationship(back_populates="resumes")
