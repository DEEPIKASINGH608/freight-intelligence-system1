from fastapi import APIRouter
from app.api.v1.endpoints import (
    forecast,
    risk,
    optimization,
    vessels,
    routes,
    decision,
)

api_router = APIRouter()

api_router.include_router(decision.router, prefix="/decision", tags=["Decision Engine"])
api_router.include_router(forecast.router, prefix="/forecast", tags=["Forecasting"])
api_router.include_router(risk.router, prefix="/risk", tags=["Risk Analysis"])
api_router.include_router(
    optimization.router, prefix="/optimize", tags=["Optimization"]
)
api_router.include_router(vessels.router, prefix="/vessels", tags=["Vessels"])
api_router.include_router(routes.router, prefix="/routes", tags=["Routes"])