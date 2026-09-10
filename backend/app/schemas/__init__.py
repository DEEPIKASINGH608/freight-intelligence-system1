from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DecisionEvaluationRequest(BaseModel):
    origin: str = Field(default="Australia")
    destination: str = Field(default="Paradip")
    cargo_type: str = Field(default="iron_ore")
    cargo_quantity_tons: float = Field(default=75000.0)
    delivery_deadline_days: float = Field(default=30.0)
    current_freight_rate: float = Field(default=22.50)
    bunker_fuel_price: float = Field(default=620.00)
    cargo_demand_index: float = Field(default=105.0)
    vessel_availability_index: float = Field(default=92.0)
    port_congestion_days: float = Field(default=2.5)
    route_distance_nm: float = Field(default=3850.0)
    weather_risk_index: float = Field(default=1.1)
    available_vessels: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class ScenarioAnalysis(BaseModel):
    scenario_book_now_inr_cr: float
    scenario_wait_30d_inr_cr: float
    exposure_delta_inr_cr: float
    basis: str


class DecisionEngineResponse(BaseModel):
    recommended_action: str
    reasoning: str
    scenario_analysis: ScenarioAnalysis
    financial_summary: Dict[str, float]
    port_constraints_module: Dict[str, Any]
    forecast_module: Dict[str, Any]
    risk_module: Dict[str, Any]
    charter_optimization_module: Dict[str, Any]
    procurement_module: Dict[str, Any]


class ForecastRange(BaseModel):
    lower_bound_usd: float
    upper_bound_usd: float
    confidence_level: str = "90%"


class BaselineComparison(BaseModel):
    naive_persistence_mae_usd: float
    model_mae_usd: float


class ForecastResponse(BaseModel):
    current_rate_usd: float
    predicted_30d_rate_usd: float
    rate_change_usd: float
    percentage_change: float
    trend: str
    forecast_range: ForecastRange
    baseline_comparison: BaselineComparison
    recommendation_hint: str
    top_drivers_pct: Dict[str, float]