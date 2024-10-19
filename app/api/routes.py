from fastapi import APIRouter
from app.api.v1 import users, inputs, indicators, process

router_api = APIRouter()

# Incluye las rutas de users
router_api.include_router(users.router, prefix="/users", tags=["Users"])
router_api.include_router(inputs.router, prefix="/inputs", tags=["Inputs"])
router_api.include_router(indicators.router, prefix="/indicators", tags=["Indicators"])
router_api.include_router(process.router, prefix="/process", tags=["Process"])
