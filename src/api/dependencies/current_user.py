from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Body
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer

from src.domain.jwt_token.enums import JwtTokenType
from src.domain.jwt_token.use_cases.decode_jwt_token import DecodeJwtToken
from src.domain.user.dto.filter import UserFilterSchema
from src.domain.user.dto.output import UserOutSchema
from src.domain.user.entities import User
from src.domain.user.use_cases.retrieve_user import RetrieveUser
from src.utils.auth import get_token_from_bearer_string

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")

auth_scheme = HTTPBearer()


@inject
async def get_current_user(
    auth_credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    decode_jwt_token: DecodeJwtToken = Depends(Provide["use_cases.decode_jwt_token"]),
    retrieve_user: RetrieveUser = Depends(Provide["use_cases.retrieve_user"]),
) -> User | None:
    token = get_token_from_bearer_string(bearer_string=auth_credentials.credentials)
    decoded_token = await decode_jwt_token(token=token, token_type=JwtTokenType.ACCESS)
    return await retrieve_user(data=UserFilterSchema(id=decoded_token.user_id))


async def get_current_authenticated_user(user: UserOutSchema | None = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user


@inject
async def get_current_user_from_refresh_token(
    refresh_token: str = Body(..., embed=True),
    decode_jwt_token: DecodeJwtToken = Depends(Provide["use_cases.decode_jwt_token"]),
    retrieve_user: RetrieveUser = Depends(Provide["use_cases.retrieve_user"]),
) -> User | None:
    decoded_token = await decode_jwt_token(
        token=refresh_token, token_type=JwtTokenType.REFRESH, add_token_to_blacklist=True
    )
    return await retrieve_user(data=UserFilterSchema(id=decoded_token.user_id))
