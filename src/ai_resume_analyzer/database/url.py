from sqlalchemy.engine import make_url


def get_async_database_url(database_url: str) -> str:
    url = make_url(database_url)

    if url.drivername in {"postgres", "postgresql"}:
        url = url.set(drivername="postgresql+asyncpg")

    if "sslmode" in url.query:
        url = url.difference_update_query(["sslmode"])

    return url.render_as_string(hide_password=False)


def get_asyncpg_connect_args(database_url: str) -> dict[str, object]:
    sslmode = _last_query_value(make_url(database_url).query.get("sslmode"))
    if sslmode is None:
        return {}

    normalized_sslmode = sslmode.lower()
    if normalized_sslmode == "disable":
        return {"ssl": False}
    if normalized_sslmode in {"allow", "prefer", "require", "verify-ca", "verify-full"}:
        return {"ssl": True}

    return {}


def _last_query_value(value: object) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, tuple) and value and isinstance(value[-1], str):
        return value[-1]
    return None
