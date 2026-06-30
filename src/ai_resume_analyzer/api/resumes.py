from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, BinaryIO
from uuid import UUID, uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ai_resume_analyzer.ai import AIAnalysisService
from ai_resume_analyzer.auth.dependencies import get_current_user
from ai_resume_analyzer.config import Settings, get_settings
from ai_resume_analyzer.constants.uploads import (
    BYTES_PER_MEGABYTE,
    DEFAULT_ALLOWED_FILE_TYPES,
    UPLOAD_STATUS_STORED,
)
from ai_resume_analyzer.database.models.user import User
from ai_resume_analyzer.database.session import get_db
from ai_resume_analyzer.extractors import ResumeExtractionService
from ai_resume_analyzer.feedback import ResumeFeedbackService
from ai_resume_analyzer.parsers import ResumeParserError, ResumeParserService
from ai_resume_analyzer.repositories.resume_repository import ResumeRepository
from ai_resume_analyzer.schemas.resume import ResumeRead, ResumeUploadResponse
from ai_resume_analyzer.scoring import ResumeScoringService
from ai_resume_analyzer.utils.uploads import (
    FileSizeExceededError,
    UnsupportedFileTypeError,
    UploadValidationError,
    validate_content_type,
    validate_file_size,
    validate_upload_metadata,
)

router = APIRouter(prefix="/resumes", tags=["resumes"])

CONTENT_TYPE_EXTENSIONS = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}
MAX_FILENAME_GENERATION_ATTEMPTS = 10
MAX_ORIGINAL_FILENAME_LENGTH = 255
UPLOAD_CHUNK_SIZE = BYTES_PER_MEGABYTE


@dataclass(frozen=True)
class StoredUpload:
    original_filename: str
    stored_filename: str
    storage_path: Path
    file_size: int
    content_type: str


def get_resume_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ResumeRepository:
    return ResumeRepository(session=session)


def get_resume_parser_service() -> ResumeParserService:
    return ResumeParserService()


def get_resume_extraction_service() -> ResumeExtractionService:
    return ResumeExtractionService()


def get_resume_scoring_service() -> ResumeScoringService:
    return ResumeScoringService()


def get_resume_feedback_service() -> ResumeFeedbackService:
    return ResumeFeedbackService()


def get_ai_analysis_service() -> AIAnalysisService:
    return AIAnalysisService()


def _normalize_original_filename(filename: str | None) -> str:
    normalized_filename = (filename or "upload").strip()
    basename = normalized_filename.replace("\\", "/").rsplit("/", maxsplit=1)[-1]
    if not basename:
        return "upload"
    return basename[:MAX_ORIGINAL_FILENAME_LENGTH]


def _validation_http_exception(exc: UploadValidationError) -> HTTPException:
    if isinstance(exc, FileSizeExceededError):
        return HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(exc),
        )
    if isinstance(exc, UnsupportedFileTypeError):
        return HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        )
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


def _remove_file(path: Path) -> None:
    with suppress(OSError):
        path.unlink(missing_ok=True)


def _not_found_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resume not found",
    )


def _validate_initial_upload_metadata(
    file: UploadFile,
    *,
    content_type: str,
    settings: Settings,
) -> None:
    if file.size is None:
        validate_content_type(
            content_type,
            allowed_file_types=DEFAULT_ALLOWED_FILE_TYPES,
        )
        return

    validate_upload_metadata(
        file_size=file.size,
        content_type=content_type,
        max_size_mb=settings.max_upload_size_mb,
        allowed_file_types=DEFAULT_ALLOWED_FILE_TYPES,
    )


async def _copy_upload_file(
    file: UploadFile,
    destination: BinaryIO,
    *,
    max_size_mb: int,
) -> int:
    file_size = 0
    while chunk := await file.read(UPLOAD_CHUNK_SIZE):
        file_size += len(chunk)
        validate_file_size(file_size, max_size_mb=max_size_mb)
        destination.write(chunk)
    return file_size


async def _save_upload_file(
    file: UploadFile,
    *,
    upload_directory: Path,
    content_type: str,
    settings: Settings,
) -> StoredUpload:
    upload_directory.mkdir(parents=True, exist_ok=True)
    original_filename = _normalize_original_filename(file.filename)
    extension = CONTENT_TYPE_EXTENSIONS[content_type]

    for _ in range(MAX_FILENAME_GENERATION_ATTEMPTS):
        stored_filename = f"{uuid4()}{extension}"
        storage_path = upload_directory / stored_filename

        try:
            with storage_path.open("xb") as destination:
                file_size = await _copy_upload_file(
                    file,
                    destination,
                    max_size_mb=settings.max_upload_size_mb,
                )
        except FileExistsError:
            continue
        except UploadValidationError:
            _remove_file(storage_path)
            raise
        except OSError as exc:
            _remove_file(storage_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not save uploaded file",
            ) from exc

        validate_upload_metadata(
            file_size=file_size,
            content_type=content_type,
            max_size_mb=settings.max_upload_size_mb,
            allowed_file_types=DEFAULT_ALLOWED_FILE_TYPES,
        )
        return StoredUpload(
            original_filename=original_filename,
            stored_filename=stored_filename,
            storage_path=storage_path,
            file_size=file_size,
            content_type=content_type,
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Could not allocate a unique upload filename",
    )


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: Annotated[UploadFile, File(...)],
    current_user: Annotated[User, Depends(get_current_user)],
    resume_repository: Annotated[ResumeRepository, Depends(get_resume_repository)],
    resume_parser_service: Annotated[
        ResumeParserService,
        Depends(get_resume_parser_service),
    ],
    resume_extraction_service: Annotated[
        ResumeExtractionService,
        Depends(get_resume_extraction_service),
    ],
    resume_scoring_service: Annotated[
        ResumeScoringService,
        Depends(get_resume_scoring_service),
    ],
    resume_feedback_service: Annotated[
        ResumeFeedbackService,
        Depends(get_resume_feedback_service),
    ],
    ai_analysis_service: Annotated[
        AIAnalysisService,
        Depends(get_ai_analysis_service),
    ],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ResumeUploadResponse:
    content_type = (file.content_type or "").strip().lower()

    try:
        _validate_initial_upload_metadata(
            file,
            content_type=content_type,
            settings=settings,
        )
        stored_upload = await _save_upload_file(
            file,
            upload_directory=Path(settings.upload_directory),
            content_type=content_type,
            settings=settings,
        )
    except UploadValidationError as exc:
        raise _validation_http_exception(exc) from exc

    try:
        parsed_text = await resume_parser_service.parse_resume(
            stored_upload.storage_path
        )
    except ResumeParserError as exc:
        await resume_repository.session.rollback()
        _remove_file(stored_upload.storage_path)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    extracted_data = resume_extraction_service.extract_resume_data(parsed_text)
    ats_score = resume_scoring_service.score_resume(extracted_data)
    feedback = resume_feedback_service.generate_feedback(
        extracted_data=extracted_data,
        ats_score=ats_score,
    )
    ai_analysis = await ai_analysis_service.analyze_resume(
        parsed_text=parsed_text,
        extracted_data=extracted_data,
        ats_score=ats_score,
        feedback=feedback,
    )

    try:
        resume = await resume_repository.create_resume(
            user_id=current_user.id,
            original_filename=stored_upload.original_filename,
            stored_filename=stored_upload.stored_filename,
            content_type=stored_upload.content_type,
            file_size=stored_upload.file_size,
            storage_path=str(stored_upload.storage_path),
            upload_status=UPLOAD_STATUS_STORED,
        )
        await resume_repository.session.commit()
    except SQLAlchemyError as exc:
        await resume_repository.session.rollback()
        _remove_file(stored_upload.storage_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not persist resume metadata",
        ) from exc

    return ResumeUploadResponse(
        resume=ResumeRead.model_validate(resume),
        parsed_text=parsed_text,
        extracted_data=extracted_data,
        ats_score=ats_score,
        feedback=feedback,
        ai_analysis=ai_analysis,
    )


@router.get(
    "",
    response_model=list[ResumeRead],
    status_code=status.HTTP_200_OK,
)
async def list_resumes(
    current_user: Annotated[User, Depends(get_current_user)],
    resume_repository: Annotated[ResumeRepository, Depends(get_resume_repository)],
) -> list[ResumeRead]:
    resumes = await resume_repository.get_all_by_user(current_user.id)
    return [ResumeRead.model_validate(resume) for resume in resumes]


@router.get(
    "/{resume_id}",
    response_model=ResumeRead,
    status_code=status.HTTP_200_OK,
)
async def read_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    resume_repository: Annotated[ResumeRepository, Depends(get_resume_repository)],
) -> ResumeRead:
    resume = await resume_repository.get_by_id_for_user(
        resume_id=resume_id,
        user_id=current_user.id,
    )
    if resume is None:
        raise _not_found_exception()

    return ResumeRead.model_validate(resume)


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resume(
    resume_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    resume_repository: Annotated[ResumeRepository, Depends(get_resume_repository)],
) -> Response:
    resume = await resume_repository.get_by_id_for_user(
        resume_id=resume_id,
        user_id=current_user.id,
    )
    if resume is None:
        raise _not_found_exception()

    storage_path = Path(resume.storage_path)
    try:
        storage_path.unlink()
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete resume file",
        ) from exc

    try:
        await resume_repository.delete(resume)
        await resume_repository.session.commit()
    except SQLAlchemyError as exc:
        await resume_repository.session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete resume metadata",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
