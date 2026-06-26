import logging
from typing import Any, cast

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ai_resume_analyzer.utils.context import get_request_id

logger = logging.getLogger(__name__)


def _error_payload(detail: Any) -> dict[str, Any]:
    payload = {"detail": detail}
    request_id = get_request_id()
    if request_id is not None:
        payload["request_id"] = request_id
    return payload


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    http_exc = cast(HTTPException, exc)
    logger.warning(
        "HTTP exception handled",
        extra={"path": request.url.path, "status_code": http_exc.status_code},
    )
    return JSONResponse(
        status_code=http_exc.status_code,
        content=_error_payload(http_exc.detail),
        headers=http_exc.headers,
    )


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    validation_exc = cast(RequestValidationError, exc)
    logger.warning(
        "Request validation failed",
        extra={"path": request.url.path, "errors": validation_exc.errors()},
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_payload(validation_exc.errors()),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled exception",
        extra={"path": request.url.path},
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_payload("Internal server error"),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
