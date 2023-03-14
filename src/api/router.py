from fastapi import APIRouter

from src.api.endpoints import register_router, auth_router


def include_routers() -> APIRouter:
    main_router = APIRouter()

    main_router.include_router(register_router, prefix="/register", tags=["Registration"])
    main_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

    return main_router
