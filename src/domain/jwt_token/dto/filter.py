from src.common.dto import OrmModel


class JwtTokenFilterSchema(OrmModel):
    jti: str
    user_id: int
