from fastapi import APIRouter
from app.api.v1 import users

router_api = APIRouter()

# Incluye las rutas de users
router_api.include_router(users.router, prefix="/users", tags=["Users"])
