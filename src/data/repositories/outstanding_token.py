from src.common.repository import BaseRepo
from src.domain.jwt_token.dto.filter import JwtTokenFilterSchema
from src.domain.jwt_token.dto.input import OutstandingTokenCreateSchema
from src.domain.jwt_token.entities import OutstandingToken


class OutstandingTokenRepo(
    BaseRepo[OutstandingToken, JwtTokenFilterSchema, OutstandingTokenCreateSchema]
):
    model = OutstandingToken
