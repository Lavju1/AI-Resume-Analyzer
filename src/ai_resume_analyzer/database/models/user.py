from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_resume_analyzer.database.models.base import BaseModel

if TYPE_CHECKING:
    from ai_resume_analyzer.database.models.resume import Resume


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(length=320),
        nullable=False,
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
