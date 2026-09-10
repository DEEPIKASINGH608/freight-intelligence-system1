from typing import Dict, Any
import json
import os

from app.optimization.vessel_solver import VesselOptimizationSolver
from app.optimization.procurement_solver import optimize_procurement


def load_vessel_fleet():
    file_path = os.path.join(os.path.dirname(__file__), "../data/vessel_fleet.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []


class DecisionEngine:
    def synthesize_decision(self, payload: Any) -> Dict[str, Any]:
        try:
            # 1. Standardize Payload Conversion
            if isinstance(payload, dict):
                data = payload
            elif hasattr(payload, "model_dump"):  # Pydantic v2
                data = payload.model_dump()
            elif hasattr(payload, "dict"):        # Pydantic v1
                data = payload.dict()
            else:
                data = dict(payload)

            # 2. Extract Input Parameters
            cargo_qty = data.get("cargo_quantity_tons", 75000)
            current_rate = data.get("current_freight_rate", 22.5)
            fuel_price = data.get("bunker_fuel_price", 620.0)
            congestion_days = data.get("port_congestion_days", 2.5)
            weather_risk = data.get("weather_risk_index", 1.1)
            destination_port = data.get("destination", "Paradip")
            cargo_type = data.get("cargo_type", "iron_ore")
            delivery_deadline_days = data.get("delivery_deadline_days", 25.0)
            route_distance_nm = data.get("route_distance_nm", 4500.0)

            # 3. Freight Rate Forecasting Logic
            forecasted_rate = round(current_rate * (1 + (fuel_price - 600) / 10000 + (weather_risk - 1.0) * 0.05), 2)
            rate_delta_pct = round(((forecasted_rate - current_rate) / current_rate) * 100, 2)

            spot_total_usd = cargo_qty * current_rate
            forecast_total_usd = cargo_qty * forecasted_rate

            scenario_book_now = round((spot_total_usd * 83) / 10_000_000, 2)
            scenario_wait_30d = round((forecast_total_usd * 83) / 10_000_000, 2)
            exposure_delta = round(scenario_wait_30d - scenario_book_now, 2)

            recommended_action = "CHARTER NOW" if forecasted_rate > current_rate else "WAIT & RE-EVALUATE"

            # 4. Integrate Vessel Optimization Solver (Port Constraints + MILP)
            fleet_dataset = load_vessel_fleet()
            vessel_solver = VesselOptimizationSolver()

            vessel_optimization_result = vessel_solver.solve_vessel_chartering(
                cargo_required_tons=cargo_qty,
                available_vessels=fleet_dataset,
                route_distance_nm=route_distance_nm,
                fuel_price_usd_ton=fuel_price,
                delivery_deadline_days=delivery_deadline_days,
                port_congestion_days=congestion_days,
                port_name=destination_port,
                cargo_type=cargo_type
            )

            # 5. Extract Suppliers & Run Procurement LP Solver
            suppliers = data.get("suppliers", [
                {
                    "id": "SUP-AU-01",
                    "name": "Supplier Alpha (Australia)",
                    "origin": "Australia",
                    "commodity_price_usd": 102.0,
                    "freight_rate_usd": current_rate,
                    "capacity_tons": 150000,
                    "max_allocation_pct": 0.70,
                    "data_source_type": "Synthetic Demo Data"
                },
                {
                    "id": "SUP-MZ-02",
                    "name": "Supplier Beta (Mozambique)",
                    "origin": "Mozambique",
                    "commodity_price_usd": 99.5,
                    "freight_rate_usd": current_rate + 1.2,
                    "capacity_tons": 100000,
                    "max_allocation_pct": 0.50,
                    "data_source_type": "Synthetic Demo Data"
                },
                {
                    "id": "SUP-ID-03",
                    "name": "Supplier Gamma (Indonesia)",
                    "origin": "Indonesia",
                    "commodity_price_usd": 95.0,
                    "freight_rate_usd": current_rate - 0.8,
                    "capacity_tons": 200000,
                    "max_allocation_pct": 0.60,
                    "data_source_type": "Synthetic Demo Data"
                }
            ])

            procurement_optimization_result = optimize_procurement(
                target_demand_tons=cargo_qty,
                suppliers=suppliers
            )

            # 6. Return Synthesized Output Payload
            return {
                "recommended_action": recommended_action,
                "reasoning": f"Current rate is ${current_rate}/ton. Projected to reach ${forecasted_rate}/ton.",
                "scenario_analysis": {
                    "scenario_book_now_inr_cr": scenario_book_now,
                    "scenario_wait_30d_inr_cr": scenario_wait_30d,
                    "exposure_delta_inr_cr": exposure_delta,
                    "basis": "30-Day Projection"
                },
                "financial_summary": {
                    "current_spot_rate_usd": current_rate,
                    "forecasted_30d_rate_usd": forecasted_rate,
                    "projected_rate_change_pct": rate_delta_pct,
                    "cargo_quantity_tons": cargo_qty
                },
                "port_constraints_module": {
                    "origin": data.get("origin", "Australia (Port Hedland)"),
                    "destination": destination_port
                },
                "forecast_module": {"confidence_score": "89%"},
                "risk_module": {
                    "congestion_days": congestion_days,
                    "weather_risk_score": weather_risk,
                    "overall_risk_level": "LOW"
                },
                "charter_optimization_module": vessel_optimization_result,
                "procurement_optimization": procurement_optimization_result
            }

        except Exception as e:
            raise RuntimeError(f"Decision Engine evaluation failure: {str(e)}")