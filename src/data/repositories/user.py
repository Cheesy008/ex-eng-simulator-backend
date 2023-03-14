from src.common.repository import BaseRepo
from src.domain.user.dto.filter import UserFilterSchema
from src.domain.user.dto.input import UserCreateInDBSchema
from src.domain.user.entities import User


class UserRepo(BaseRepo[User, UserFilterSchema, UserCreateInDBSchema]):
    model = User
