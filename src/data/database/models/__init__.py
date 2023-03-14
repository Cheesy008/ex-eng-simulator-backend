from sqlalchemy.orm import registry


def start_mappers() -> None:
    from src.data.database.models.user import user_table  # noqa: F401
    from src.data.database.models.outstanding_token import outstanding_token_table  # noqa: F401
    from src.data.database.models.blacklist_token import blacklist_token_table  # noqa: F401


mapper_registry = registry()
