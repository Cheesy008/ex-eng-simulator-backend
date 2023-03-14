from datetime import datetime, timedelta
from uuid import uuid4

from jose import jwt

from src.data.uow import UnitOfWork
from src.domain.jwt_token.dto.input import OutstandingTokenCreateSchema
from src.domain.jwt_token.dto.output import JwtTokensOutSchema, JwtTokenSchema
from src.domain.jwt_token.enums import JwtTokenType


class CreateJwtTokens:
    def __init__(self, uow: UnitOfWork, config: dict):
        self.uow = uow
        self.config = config

    def _encode_payload(self, token_data: JwtTokenSchema) -> str:
        encoded_jwt = jwt.encode(
            token_data.dict(),
            self.config["secret_key"],
            algorithm=self.config["jwt_algorithm"],
        )
        return encoded_jwt

    async def __call__(self, user_id: int) -> JwtTokensOutSchema:
        jti = uuid4().hex
        access_exp = datetime.utcnow() + timedelta(
            minutes=self.config["access_token_expires_minutes"]
        )
        refresh_exp = datetime.utcnow() + timedelta(
            minutes=self.config["refresh_token_expires_minutes"]
        )

        access_token_payload = JwtTokenSchema(
            user_id=user_id,
            token_type=JwtTokenType.ACCESS,
            exp=access_exp,
            jti=jti,
        )
        refresh_token_payload = JwtTokenSchema(
            user_id=user_id,
            token_type=JwtTokenType.REFRESH,
            exp=refresh_exp,
            jti=jti,
        )

        async with self.uow:
            access_token = await self.uow.outstanding_token.create(
                data=OutstandingTokenCreateSchema(
                    jti=jti,
                    user_id=user_id,
                    expires_at=access_exp,
                    token=self._encode_payload(access_token_payload),
                )
            )
            refresh_token = await self.uow.outstanding_token.create(
                data=OutstandingTokenCreateSchema(
                    jti=jti,
                    user_id=user_id,
                    expires_at=refresh_exp,
                    token=self._encode_payload(refresh_token_payload),
                )
            )
            await self.uow.commit()

        return JwtTokensOutSchema(
            access_token=access_token.token, refresh_token=refresh_token.token
        )
