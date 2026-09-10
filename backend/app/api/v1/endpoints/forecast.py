from fastapi import APIRouter, HTTPException
from app.ml.predict_forecaster import FreightForecaster
from pydantic import BaseModel

router = APIRouter()
forecaster = FreightForecaster()


class ForecastRequest(BaseModel):
    current_rate: float = 22.50
    bunker_fuel: float = 620.00
    cargo_demand: float = 105.0
    vessel_avail: float = 92.0
    congestion_days: float = 2.5


@router.post("/predict")
def predict_freight_rate(payload: ForecastRequest):
    try:
        result = forecaster.predict_30d_rate(
            current_rate=payload.current_rate,
            bunker_fuel=payload.bunker_fuel,
            cargo_demand=payload.cargo_demand,
            vessel_avail=payload.vessel_avail,
            congestion_days=payload.congestion_days,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))