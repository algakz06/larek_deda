from fastapi import APIRouter
from app.endpoints.auth import router as auth_router
from app.endpoints.users import router as users_router
from app.endpoints.companies import router as companies_router

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(companies_router)
