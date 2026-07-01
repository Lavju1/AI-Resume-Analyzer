import pytest
from pydantic import ValidationError

from ai_resume_analyzer.config import Settings


def test_production_requires_non_default_jwt_secret() -> None:
    with pytest.raises(ValidationError, match="JWT_SECRET_KEY"):
        Settings(
            app_env="production",
            debug=False,
            gemini_api_key="test-gemini-key",
            jwt_secret_key="change-me-in-production",
        )


def test_production_accepts_required_secret_configuration() -> None:
    settings = Settings(
        app_env="production",
        debug=False,
        gemini_api_key="test-gemini-key",
        jwt_secret_key="production-secret",
    )

    assert settings.app_env == "production"
