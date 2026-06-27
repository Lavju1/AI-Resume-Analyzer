BYTES_PER_MEGABYTE = 1024 * 1024

DEFAULT_UPLOAD_DIRECTORY = "uploads/resumes"
DEFAULT_MAX_UPLOAD_SIZE_MB = 10
DEFAULT_ALLOWED_FILE_TYPES = (
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)

UPLOAD_STATUS_PENDING = "pending"
UPLOAD_STATUS_STORED = "stored"
UPLOAD_STATUS_FAILED = "failed"
UPLOAD_STATUSES = frozenset(
    {
        UPLOAD_STATUS_PENDING,
        UPLOAD_STATUS_STORED,
        UPLOAD_STATUS_FAILED,
    }
)
