from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_resume_analyzer import __version__
from ai_resume_analyzer.api.auth import router as auth_router
from ai_resume_analyzer.config import Settings, get_settings
from ai_resume_analyzer.constants.http import HEALTH_PATH, HEALTH_STATUS_OK
from ai_resume_analyzer.core.logging import configure_logging
from ai_resume_analyzer.exceptions.handlers import register_exception_handlers
from ai_resume_analyzer.middleware.request_id import RequestIDMiddleware


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)

    app = FastAPI(
        title=resolved_settings.app_name,
        version=__version__,
        debug=resolved_settings.debug,
    )
    app.state.settings = resolved_settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_allow_origins,
        allow_credentials=resolved_settings.cors_allow_credentials,
        allow_methods=resolved_settings.cors_allow_methods,
        allow_headers=resolved_settings.cors_allow_headers,
    )
    app.add_middleware(
        RequestIDMiddleware,
        header_name=resolved_settings.request_id_header,
    )

    register_exception_handlers(app)
    app.include_router(auth_router)

    @app.get(HEALTH_PATH, tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": HEALTH_STATUS_OK}

    return app


app = create_app()
