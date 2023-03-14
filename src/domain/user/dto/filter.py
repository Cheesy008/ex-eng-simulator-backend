from src.common.dto import OrmModel


class UserFilterSchema(OrmModel):
    id: int | None = None
    username: str | None = None
