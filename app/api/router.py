from fastapi import APIRouter

from app.api.endpoints import user_router, tron_router


main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(tron_router)
