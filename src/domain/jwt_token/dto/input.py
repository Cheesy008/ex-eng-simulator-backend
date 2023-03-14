from datetime import datetime

from src.common.dto import BaseInSchema


class OutstandingTokenCreateSchema(BaseInSchema):
    jti: str
    user_id: int
    expires_at: datetime
    token: str


class BlacklistTokenCreateSchema(BaseInSchema):
    outstanding_token_id: int
