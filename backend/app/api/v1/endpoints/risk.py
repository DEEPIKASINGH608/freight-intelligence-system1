from fastapi import APIRouter, HTTPException
from app.ml.risk_evaluator import RiskEvaluator
from pydantic import BaseModel

router = APIRouter()
risk_evaluator = RiskEvaluator()


class RiskRequest(BaseModel):
    port_congestion_days: float = 2.5
    weather_risk_index: float = 1.1
    vessel_availability_index: float = 92.0
    distance_nautical_miles: float = 3850.0


@router.post("/evaluate")
def evaluate_risk(payload: RiskRequest):
    try:
        return risk_evaluator.evaluate_route_risk(
            port_congestion_days=payload.port_congestion_days,
            weather_risk_index=payload.weather_risk_index,
            vessel_availability_index=payload.vessel_availability_index,
            distance_nautical_miles=payload.distance_nautical_miles,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))