from dataclasses import dataclass

from src.common.entity import Entity


@dataclass
class OutstandingToken(Entity):
    user_id: int
    jti: str
    token: str
    expires_at: str


@dataclass
class BlacklistToken(Entity):
    outstanding_token_id: int
