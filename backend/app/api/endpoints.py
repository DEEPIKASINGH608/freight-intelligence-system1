from fastapi import APIRouter, HTTPException, Depends
from app.schemas import DecisionEvaluationRequest, DecisionEngineResponse
from app.services.decision_engine import DecisionEngine
from app.ml.predict_forecaster import FreightForecaster
from app.ml.risk_evaluator import RiskEvaluator

router = APIRouter()

# Instantiate Engines as Singleton Dependencies
decision_engine = DecisionEngine()
forecaster = FreightForecaster()
risk_evaluator = RiskEvaluator()

# Default Fleet Dataset for Optimization fallback
DEFAULT_FLEET = [
    {"id": "V-01", "name": "MV Eastern Glory", "vessel_type": "Capesize", "capacity_dwt": 120000, "daily_charter_rate": 28000, "fuel_consumption_ton_day": 38, "speed_knots": 14.5},
    {"id": "V-02", "name": "MV Pacific Trident", "vessel_type": "Capesize", "capacity_dwt": 100000, "daily_charter_rate": 24000, "fuel_consumption_ton_day": 32, "speed_knots": 14.0},
    {"id": "V-03", "name": "MV Bengal Pioneer", "vessel_type": "Panamax", "capacity_dwt": 75000, "daily_charter_rate": 18500, "fuel_consumption_ton_day": 25, "speed_knots": 13.5},
    {"id": "V-04", "name": "MV Oceanic Sentinel", "vessel_type": "Capesize", "capacity_dwt": 150000, "daily_charter_rate": 34000, "fuel_consumption_ton_day": 42, "speed_knots": 15.0}
]

@router.post("/decision/evaluate", response_model=DecisionEngineResponse, summary="Synthesize Decision Plan")
async def evaluate_decision(payload: DecisionEvaluationRequest):
    """
    Triggers the complete synthesis engine:
    1. 30-Day Freight Rate Machine Learning Forecast
    2. Route Disruption & Demurrage Risk Evaluation
    3. Google OR-Tools MILP Vessel Charter Optimization
    4. Landed Cargo Procurement Optimization
    """
    try:
        vessels = [v.dict() for v in payload.available_vessels] if payload.available_vessels else DEFAULT_FLEET

        result = decision_engine.evaluate_decision(
            origin=payload.origin,
            destination=payload.destination,
            cargo_type=payload.cargo_type,
            cargo_quantity_tons=payload.cargo_quantity_tons,
            delivery_deadline_days=payload.delivery_deadline_days,
            available_vessels=vessels,
            current_freight_rate=payload.current_freight_rate,
            bunker_fuel_price=payload.bunker_fuel_price,
            cargo_demand_index=payload.cargo_demand_index,
            vessel_availability_index=payload.vessel_availability_index,
            port_congestion_days=payload.port_congestion_days,
            route_distance_nm=payload.route_distance_nm,
            weather_risk_index=payload.weather_risk_index
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decision Engine evaluation failure: {str(e)}")

@router.get("/forecast/predict", summary="Standalone ML Freight Rate Forecast")
async def predict_rate(
    current_rate: float = 22.50,
    bunker_fuel: float = 620.0,
    cargo_demand: float = 105.0,
    vessel_avail: float = 92.0,
    congestion_days: float = 2.5
):
    """
    Direct endpoint to query the 30-day Machine Learning rate forecaster.
    """
    try:
        return forecaster.predict_30d_rate(
            current_rate=current_rate,
            bunker_fuel=bunker_fuel,
            cargo_demand=cargo_demand,
            vessel_avail=vessel_avail,
            congestion_days=congestion_days
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk/evaluate", summary="Standalone Operational Risk Evaluation")
async def evaluate_risk(
    congestion_days: float = 2.5,
    weather_risk: float = 1.1,
    vessel_avail: float = 92.0,
    distance_nm: float = 3850.0
):
    """
    Direct endpoint to query the operational delay risk model.
    """
    try:
        return risk_evaluator.evaluate_route_risk(
            port_congestion_days=congestion_days,
            weather_risk_index=weather_risk,
            vessel_availability_index=vessel_avail,
            distance_nautical_miles=distance_nm
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))