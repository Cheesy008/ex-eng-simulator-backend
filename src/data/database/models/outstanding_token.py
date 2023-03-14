from sqlalchemy import Column, Integer, Table, String, DateTime
from sqlalchemy.orm import relationship

from src.data.database.models import mapper_registry
from src.domain.jwt_token.entities import OutstandingToken, BlacklistToken

outstanding_token_table = Table(
    "outstanding_tokens",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, nullable=False),
    Column("jti", String, index=True, nullable=False),
    Column("token", String, nullable=False),
    Column("expires_at", DateTime(timezone=True)),
)

mapper_registry.map_imperatively(
    OutstandingToken,
    outstanding_token_table,
    properties={
        "blacklist_token": relationship(BlacklistToken, back_populates="outstanding_token")
    },
)
