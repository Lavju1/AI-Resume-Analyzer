from collections.abc import Iterable

from ai_resume_analyzer.config import get_settings
from ai_resume_analyzer.constants.uploads import BYTES_PER_MEGABYTE


class UploadValidationError(ValueError):
    """Raised when upload metadata fails validation."""


class FileSizeExceededError(UploadValidationError):
    """Raised when an uploaded file is larger than the configured limit."""


class UnsupportedFileTypeError(UploadValidationError):
    """Raised when an uploaded file has an unsupported content type."""


def max_upload_size_bytes(max_size_mb: int | None = None) -> int:
    resolved_max_size_mb = (
        get_settings().max_upload_size_mb if max_size_mb is None else max_size_mb
    )
    return resolved_max_size_mb * BYTES_PER_MEGABYTE


def validate_file_size(file_size: int, *, max_size_mb: int | None = None) -> None:
    if file_size < 0:
        msg = "File size must not be negative"
        raise UploadValidationError(msg)

    max_size_bytes = max_upload_size_bytes(max_size_mb)
    if file_size > max_size_bytes:
        msg = f"File size exceeds maximum allowed size of {max_size_bytes} bytes"
        raise FileSizeExceededError(msg)


def validate_content_type(
    content_type: str,
    *,
    allowed_file_types: Iterable[str] | None = None,
) -> None:
    normalized_content_type = content_type.strip().lower()
    if not normalized_content_type:
        msg = "Content type must not be empty"
        raise UnsupportedFileTypeError(msg)

    configured_file_types = (
        get_settings().allowed_file_types
        if allowed_file_types is None
        else allowed_file_types
    )
    normalized_file_types = {
        allowed_content_type.strip().lower()
        for allowed_content_type in configured_file_types
    }
    if normalized_content_type not in normalized_file_types:
        msg = f"Unsupported file content type: {content_type}"
        raise UnsupportedFileTypeError(msg)


def validate_upload_metadata(
    *,
    file_size: int,
    content_type: str,
    max_size_mb: int | None = None,
    allowed_file_types: Iterable[str] | None = None,
) -> None:
    validate_file_size(file_size, max_size_mb=max_size_mb)
    validate_content_type(content_type, allowed_file_types=allowed_file_types)
