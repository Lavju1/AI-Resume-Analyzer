from ai_resume_analyzer.database.url import (
    get_async_database_url,
    get_asyncpg_connect_args,
)


def test_postgres_url_is_normalized_for_asyncpg() -> None:
    database_url = (
        "postgres://user:password@ep-test.us-east-1.aws.neon.tech/app"
        "?sslmode=require"
    )

    assert (
        get_async_database_url(database_url)
        == "postgresql+asyncpg://user:password@ep-test.us-east-1.aws.neon.tech/app"
    )


def test_neon_sslmode_is_passed_as_asyncpg_connect_arg() -> None:
    database_url = (
        "postgresql://user:password@ep-test.us-east-1.aws.neon.tech/app"
        "?sslmode=require"
    )

    assert get_asyncpg_connect_args(database_url) == {"ssl": True}
