from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import Response

from src.api.dependencies.current_user import auth_scheme, get_current_user_from_refresh_token
from src.domain.jwt_token.dto.output import JwtTokensOutSchema
from src.domain.jwt_token.enums import JwtTokenType
from src.domain.jwt_token.use_cases.create_jwt_tokens import CreateJwtTokens
from src.domain.jwt_token.use_cases.decode_jwt_token import DecodeJwtToken
from src.domain.user.dto.input import AuthInSchema
from src.domain.user.entities import User
from src.domain.user.use_cases.authenticate import Authenticate
from src.utils.auth import get_token_from_bearer_string

router = APIRouter()


@router.post("/access-token", status_code=200, response_model=JwtTokensOutSchema)
@inject
async def access_token_route(
    data: AuthInSchema,
    authenticate: Authenticate = Depends(Provide["use_cases.authenticate"]),
    create_jwt_tokens: CreateJwtTokens = Depends(Provide["use_cases.create_jwt_tokens"]),
):
    user = await authenticate(data)
    return await create_jwt_tokens(user_id=user.id)


@router.post("/refresh-token", status_code=200, response_model=JwtTokensOutSchema)
@inject
async def access_token_route(
    user: User = Depends(get_current_user_from_refresh_token),
    create_jwt_tokens: CreateJwtTokens = Depends(Provide["use_cases.create_jwt_tokens"]),
):
    return await create_jwt_tokens(user_id=user.id)


@router.post("/revoke-token", status_code=204)
@inject
async def revoke_token_route(
    auth_credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    decode_jwt_token: DecodeJwtToken = Depends(Provide["use_cases.decode_jwt_token"]),
):
    token = get_token_from_bearer_string(bearer_string=auth_credentials.credentials)
    await decode_jwt_token(token=token, token_type=JwtTokenType.ACCESS, add_token_to_blacklist=True)
    return Response(status_code=204)
