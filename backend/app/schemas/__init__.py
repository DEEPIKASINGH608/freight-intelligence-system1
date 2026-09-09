from typing import List, Optional, Dict
from pydantic import BaseModel, Field

# --- VESSEL SCHEMAS ---
class VesselInput(BaseModel):
    id: str = Field(..., example="VESSEL-001")
    name: str = Field(..., example="MV Eastern Glory")
    vessel_type: str = Field(default="Capesize", example="Capesize")
    capacity_dwt: float = Field(..., gt=0, example=120000.0)
    daily_charter_rate: float = Field(..., gt=0, example=25000.0)
    fuel_consumption_ton_day: float = Field(..., gt=0, example=35.0)
    speed_knots: float = Field(default=14.0, gt=0, example=14.0)

# --- DECISION EVALUATION REQUEST SCHEMA ---
class DecisionEvaluationRequest(BaseModel):
    origin: str = Field(default="Paradip, India", example="Paradip, India")
    destination: str = Field(default="Qingdao, China", example="Qingdao, China")
    cargo_type: str = Field(default="Iron Ore", example="Iron Ore")
    cargo_quantity_tons: float = Field(default=150000.0, gt=0, example=150000.0)
    delivery_deadline_days: float = Field(default=30.0, gt=0, example=30.0)

    # Market Parameters
    current_freight_rate: float = Field(default=22.50, gt=0, example=22.50)
    bunker_fuel_price: float = Field(default=620.00, gt=0, example=620.00)
    cargo_demand_index: float = Field(default=105.0, gt=0, example=105.0)
    vessel_availability_index: float = Field(default=92.0, gt=0, example=92.0)
    port_congestion_days: float = Field(default=2.5, ge=0, example=2.5)
    route_distance_nm: float = Field(default=3850.0, gt=0, example=3850.0)
    weather_risk_index: float = Field(default=1.1, ge=0, example=1.1)

    # Available Fleet for MILP Optimization
    available_vessels: Optional[List[VesselInput]] = Field(default=None)

# --- INDIVIDUAL ENGINE RESPONSE SCHEMAS ---
class ForecastResponse(BaseModel):
    current_rate_usd: float
    predicted_30d_rate_usd: float
    rate_change_usd: float
    percentage_change: float
    trend: str
    confidence_score: float
    recommendation_hint: str
    top_drivers_pct: Dict[str, float]

class RiskResponse(BaseModel):
    risk_score: float
    risk_level: str
    congestion_days: float
    key_drivers: List[str]
    sub_scores: Dict[str, float]

# --- UNIFIED DECISION ENGINE RESPONSE SCHEMA ---
class DecisionEngineResponse(BaseModel):
    recommended_action: str
    reasoning: str
    financial_summary: Dict[str, float]
    forecast_module: Dict
    risk_module: Dict
    charter_optimization_module: Dict
    procurement_module: Dict