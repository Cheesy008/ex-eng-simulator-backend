from sqlalchemy import Column, Integer, String, Table

from src.data.database.models import mapper_registry
from src.domain.user.entities import User

user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String(), nullable=False, unique=True),
    Column("hashed_password", String(), nullable=False),
)

mapper_registry.map_imperatively(User, user_table)
