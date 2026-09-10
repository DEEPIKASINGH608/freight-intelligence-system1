from fastapi import APIRouter, HTTPException
from app.optimization.vessel_solver import VesselOptimizationSolver
from app.optimization.procurement_solver import ProcurementOptimizer
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()
vessel_solver = VesselOptimizationSolver()
procurement_optimizer = ProcurementOptimizer()


class VesselOptimizationRequest(BaseModel):
    cargo_required_tons: float = 75000.0
    available_vessels: List[Dict[str, Any]] = []
    route_distance_nm: float = 3850.0
    fuel_price_usd_ton: float = 620.0
    delivery_deadline_days: float = 30.0
    port_congestion_days: float = 2.5


@router.post("/vessels")
def optimize_vessels(payload: VesselOptimizationRequest):
    try:
        return vessel_solver.solve_vessel_chartering(
            cargo_required_tons=payload.cargo_required_tons,
            available_vessels=payload.available_vessels,
            route_distance_nm=payload.route_distance_nm,
            fuel_price_usd_ton=payload.fuel_price_usd_ton,
            delivery_deadline_days=payload.delivery_deadline_days,
            port_congestion_days=payload.port_congestion_days,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))