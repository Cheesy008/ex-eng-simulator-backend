from pydantic import Field

from src.common.dto import BaseInSchema


class AuthInSchema(BaseInSchema):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class RegisterInSchema(BaseInSchema):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    password_repeat: str = Field(..., description="Repeated password")


class UserCreateInDBSchema(BaseInSchema):
    username: str
    hashed_password: str
