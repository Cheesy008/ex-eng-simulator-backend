from fastapi import HTTPException

from src.data.uow import UnitOfWork
from src.domain.user.dto.filter import UserFilterSchema
from src.domain.user.dto.input import RegisterInSchema, UserCreateInDBSchema
from src.domain.user.entities import User
from src.utils.security import get_password_hash


class Register:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, data: RegisterInSchema) -> User:
        async with self.uow:
            user = await self.uow.user.retrieve(params=UserFilterSchema(username=data.username))
            if user:
                raise HTTPException(status_code=400, detail="This username has already been taken")
            obj = await self.uow.user.create(
                data=UserCreateInDBSchema(
                    username=data.username,
                    hashed_password=get_password_hash(data.password),
                )
            )
            await self.uow.commit()
            await self.uow.refresh(obj)
            return obj
