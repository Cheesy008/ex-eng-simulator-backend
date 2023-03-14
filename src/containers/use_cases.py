from dependency_injector import containers, providers

from src.domain.jwt_token.use_cases.create_jwt_tokens import CreateJwtTokens
from src.domain.jwt_token.use_cases.decode_jwt_token import DecodeJwtToken
from src.domain.user.use_cases.authenticate import Authenticate
from src.domain.user.use_cases.register import Register


class UseCases(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    config = providers.Configuration()

    register = providers.Factory(Register, uow=repositories.uow)
    authenticate = providers.Factory(Authenticate, uow=repositories.uow)
    create_jwt_tokens = providers.Factory(CreateJwtTokens, uow=repositories.uow, config=config.app)
    decode_jwt_token = providers.Factory(DecodeJwtToken, uow=repositories.uow, config=config.app)

