from fastapi import HTTPException
from jose import jwt
from pydantic import ValidationError

from src.data.uow import UnitOfWork
from src.domain.jwt_token.dto.filter import JwtTokenFilterSchema
from src.domain.jwt_token.dto.input import OutstandingTokenCreateSchema, BlacklistTokenCreateSchema
from src.domain.jwt_token.dto.output import JwtTokenSchema
from src.domain.jwt_token.enums import JwtTokenType


class DecodeJwtToken:
    def __init__(self, uow: UnitOfWork, config: dict):
        self.uow = uow
        self.config = config

    async def _add_token_to_blacklist(self, decoded_data: JwtTokenSchema, token: str):
        async with self.uow:
            outstanding_token = await self.uow.outstanding_token.retrieve(
                JwtTokenFilterSchema(jti=decoded_data.jti, user_id=decoded_data.user_id)
            )
            if not outstanding_token:
                outstanding_token = await self.uow.outstanding_token.create(
                    OutstandingTokenCreateSchema(
                        jti=decoded_data.jti,
                        user_id=decoded_data.user_id,
                        expires_at=decoded_data.exp,
                        token=token,
                    )
                )
                await self.uow.commit()
                await self.uow.refresh(outstanding_token)

            await self.uow.blacklist_token.create(
                BlacklistTokenCreateSchema(outstanding_token_id=outstanding_token.id)
            )
            await self.uow.commit()

    async def __call__(
        self, token: str, token_type: JwtTokenType, add_token_to_blacklist: bool = False
    ) -> JwtTokenSchema:
        try:
            payload = jwt.decode(
                token, self.config["secret_key"], algorithms=[self.config["jwt_algorithm"]]
            )
            decoded_token = JwtTokenSchema(**payload)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=403,
                detail="Could not validate credentials",
            )

        async with self.uow:
            blacklist_token = await self.uow.blacklist_token.retrieve(
                JwtTokenFilterSchema(jti=decoded_token.jti, user_id=decoded_token.user_id)
            )
            if blacklist_token:
                raise HTTPException(status_code=403, detail="Token in blacklist")

            if decoded_token.token_type != token_type:
                raise HTTPException(
                    status_code=403,
                    detail="Token has incorrect type",
                )

            if add_token_to_blacklist:
                await self._add_token_to_blacklist(decoded_token, token)

        return decoded_token
