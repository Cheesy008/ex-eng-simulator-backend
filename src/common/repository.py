from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.entity import Entity

ModelEntity = TypeVar("ModelEntity", bound=Entity)
EntityCovariant = TypeVar("EntityCovariant", bound=Entity, covariant=True)
EntityContravariant = TypeVar("EntityContravariant", bound=Entity, contravariant=True)
FilterSchema = TypeVar("FilterSchema", bound=BaseModel, contravariant=True)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel, contravariant=True)


class BaseRepo(Generic[ModelEntity, FilterSchema, CreateSchema]):
    model: Type[EntityContravariant]

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def retrieve(self, params: FilterSchema) -> ModelEntity:
        filter_params = params.dict(exclude_none=True).items()
        conditions = [getattr(self.model, key) == value for key, value in filter_params]
        query = select(self.model).where(and_(*conditions))
        res = await self.session.execute(query)
        return res.scalars().first()

    async def create(self, data: CreateSchema) -> ModelEntity:
        obj = self.model(**data.dict())
        self.session.add(obj)
        return obj
