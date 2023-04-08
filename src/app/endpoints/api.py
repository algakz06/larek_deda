from fastapi import APIRouter
from app.endpoints.auth import router as authrouter
from app.endpoints.users import router as usersrouter

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

router.include_router(authrouter)
router.include_router(usersrouter)
