from sqlalchemy import select

from src.common.repository import BaseRepo
from src.domain.jwt_token.dto.filter import JwtTokenFilterSchema
from src.domain.jwt_token.dto.input import BlacklistTokenCreateSchema
from src.domain.jwt_token.entities import BlacklistToken, OutstandingToken


class BlacklistTokenRepo(
    BaseRepo[BlacklistToken, JwtTokenFilterSchema, BlacklistTokenCreateSchema]
):
    model = BlacklistToken

    async def retrieve(self, params: JwtTokenFilterSchema) -> BlacklistToken:
        query = (
            select(self.model)
            .join(OutstandingToken)
            .where(OutstandingToken.jti == params.jti, OutstandingToken.user_id == params.user_id)
        )
        res = await self.session.execute(query)
        return res.scalars().first()
