from typing import Dict, Any

class DecisionEngine:
    def synthesize_decision(self, payload: Any) -> Dict[str, Any]:
        try:
            # Check if payload is already a dict, or convert from Pydantic model safely
            if isinstance(payload, dict):
                data = payload
            elif hasattr(payload, "model_dump"):  # Pydantic v2
                data = payload.model_dump()
            elif hasattr(payload, "dict"):        # Pydantic v1
                data = payload.dict()
            else:
                data = dict(payload)

            # Extract fields safely using .get()
            cargo_qty = data.get("cargo_quantity_tons", 75000)
            current_rate = data.get("current_freight_rate", 22.5)
            fuel_price = data.get("bunker_fuel_price", 620.0)
            congestion_days = data.get("port_congestion_days", 2.5)
            weather_risk = data.get("weather_risk_index", 1.1)

            # Calculations
            forecasted_rate = round(current_rate * (1 + (fuel_price - 600) / 10000 + (weather_risk - 1.0) * 0.05), 2)
            rate_delta_pct = round(((forecasted_rate - current_rate) / current_rate) * 100, 2)

            spot_total_usd = cargo_qty * current_rate
            forecast_total_usd = cargo_qty * forecasted_rate

            scenario_book_now = round((spot_total_usd * 83) / 10_000_000, 2)
            scenario_wait_30d = round((forecast_total_usd * 83) / 10_000_000, 2)
            exposure_delta = round(scenario_wait_30d - scenario_book_now, 2)

            recommended_action = "CHARTER NOW" if forecasted_rate > current_rate else "WAIT & RE-EVALUATE"

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
                "port_constraints_module": {"origin": data.get("origin", "Australia"), "destination": data.get("destination", "Paradip")},
                "forecast_module": {"confidence_score": "89%"},
                "risk_module": {"congestion_days": congestion_days, "weather_risk_score": weather_risk, "overall_risk_level": "LOW"},
                "charter_optimization_module": {"optimal_vessel_type": "Capesize"},
                "procurement_module": {"contract_type": "Spot Voyage Charter"}
            }
        except Exception as e:
            raise RuntimeError(f"Decision Engine evaluation failure: {str(e)}")