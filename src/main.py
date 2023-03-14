from fastapi import FastAPI

from .api.router import include_routers
from .containers import container


def create_app() -> FastAPI:
    application = FastAPI(debug=container.config.app.debug())
    application.container = container
    application.include_router(include_routers())
    return application


app = create_app()
