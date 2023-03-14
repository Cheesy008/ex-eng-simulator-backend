from dataclasses import dataclass

from src.common.entity import Entity


@dataclass
class User(Entity):
    username: str
    hashed_password: str
