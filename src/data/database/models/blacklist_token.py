from sqlalchemy import Column, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from src.data.database.models import mapper_registry
from src.domain.jwt_token.entities import BlacklistToken, OutstandingToken

blacklist_token_table = Table(
    "blacklist_tokens",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("outstanding_token_id", Integer, ForeignKey("outstanding_tokens.id")),
)

mapper_registry.map_imperatively(
    BlacklistToken,
    blacklist_token_table,
    properties={
        "outstanding_token": relationship(
            OutstandingToken, back_populates="blacklist_token", uselist=False
        )
    },
)
