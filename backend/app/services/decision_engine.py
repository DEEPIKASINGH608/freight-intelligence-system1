from app.ml.predict_forecaster import FreightForecaster
from app.ml.risk_evaluator import RiskEvaluator
from app.optimization.vessel_solver import VesselOptimizationSolver
from app.optimization.procurement_solver import ProcurementOptimizer
from app.optimization.port_constraints import validate_vessel_port_compatibility


class DecisionEngine:
    def __init__(self):
        self.forecaster = FreightForecaster()
        self.risk_evaluator = RiskEvaluator()
        self.vessel_solver = VesselOptimizationSolver()
        self.procurement_optimizer = ProcurementOptimizer()

    def evaluate_decision(
        self,
        origin: str,
        destination: str,
        cargo_type: str,
        cargo_quantity_tons: float,
        delivery_deadline_days: float,
        available_vessels: list,
        current_freight_rate: float,
        bunker_fuel_price: float,
        cargo_demand_index: float,
        vessel_availability_index: float,
        port_congestion_days: float,
        route_distance_nm: float = 3850.0,
        weather_risk_index: float = 1.1
    ) -> dict:

        # 1. Port Compatibility Filter
        compatible_vessels = []
        port_rejections = []
        for vessel in available_vessels:
            is_compatible, violations = validate_vessel_port_compatibility(
                vessel=vessel, port_name=destination, cargo_type=cargo_type
            )
            if is_compatible:
                compatible_vessels.append(vessel)
            else:
                port_rejections.append({
                    "vessel_name": vessel.get("name", vessel.get("vessel_id", "Unknown")),
                    "violations": violations
                })

        # 2. Run Modules
        forecast = self.forecaster.predict_30d_rate(
            current_rate=current_freight_rate,
            bunker_fuel=bunker_fuel_price,
            cargo_demand=cargo_demand_index,
            vessel_avail=vessel_availability_index,
            congestion_days=port_congestion_days
        )

        risk = self.risk_evaluator.evaluate_route_risk(
            port_congestion_days=port_congestion_days,
            weather_risk_index=weather_risk_index,
            vessel_availability_index=vessel_availability_index,
            distance_nautical_miles=route_distance_nm
        )

        vessels_to_use = compatible_vessels if compatible_vessels else available_vessels
        charter_plan = self.vessel_solver.solve_vessel_chartering(
            cargo_required_tons=cargo_quantity_tons,
            available_vessels=vessels_to_use,
            route_distance_nm=route_distance_nm,
            fuel_price_usd_ton=bunker_fuel_price,
            delivery_deadline_days=delivery_deadline_days,
            port_congestion_days=port_congestion_days
        )

        procurement = self.procurement_optimizer.optimize_procurement(
            cargo_required_tons=cargo_quantity_tons,
            ocean_freight_usd_ton=current_freight_rate
        )

        # 3. Dynamic Scenario Comparison (BOOK NOW vs WAIT)
        predicted_30d_rate = forecast["predicted_30d_rate_usd"]

        # Calculate cost scenarios in INR Cr (Assuming 1 USD = 83 INR for scale)
        usd_to_inr_cr = 83.0 / 10000000.0

        cost_book_now_inr_cr = round(cargo_quantity_tons * current_freight_rate * usd_to_inr_cr, 4)
        cost_wait_30d_inr_cr = round(cargo_quantity_tons * predicted_30d_rate * usd_to_inr_cr, 4)

        # Calculate market exposure delta (No hardcoded 0.50 or 0.80)
        exposure_delta_inr_cr = round(abs(cost_wait_30d_inr_cr - cost_book_now_inr_cr), 4)

        # 4. Action Recommendation Matrix
        predicted_pct_change = forecast["percentage_change"]

        if not compatible_vessels and available_vessels:
            recommended_action = "PORT RESTRICTION"
            reasoning = f"No vessels fit physical draft/LOA limits for port '{destination}'. Alternative chartering required."
        elif predicted_pct_change > 3.0 and risk["risk_level"] != "HIGH":
            recommended_action = "CHARTER NOW"
            reasoning = (
                f"Freight rates projected to rise by {predicted_pct_change}% over 30 days. "
                f"Booking now mitigates potential cost exposure of ₹{exposure_delta_inr_cr} Cr."
            )
        elif risk["risk_level"] == "HIGH":
            recommended_action = "REROUTE OR DELAY"
            reasoning = (
                f"Port congestion ({port_congestion_days} days) presents high demurrage risk. "
                f"Stagger shipment to mitigate operational delays."
            )
        elif predicted_pct_change < -3.0:
            recommended_action = "WAIT / SPOT MARKET"
            reasoning = (
                f"Rates forecast to drop by {abs(predicted_pct_change)}% over 30 days. "
                f"Waiting offers potential cost reduction of ₹{exposure_delta_inr_cr} Cr."
            )
        else:
            recommended_action = "EXECUTE STANDARD CHARTER"
            reasoning = "Market rates remain stable within baseline bounds. Proceed with scheduled allocation."

        return {
            "recommended_action": recommended_action,
            "reasoning": reasoning,
            "scenario_analysis": {
                "scenario_book_now_inr_cr": cost_book_now_inr_cr,
                "scenario_wait_30d_inr_cr": cost_wait_30d_inr_cr,
                "exposure_delta_inr_cr": exposure_delta_inr_cr,
                "basis": "30-Day Market Forecast vs Current Spot Allocation"
            },
            "financial_summary": {
                "total_estimated_cost_inr_cr": charter_plan.get("total_cost_inr_cr", cost_book_now_inr_cr),
                "current_rate_usd_ton": current_freight_rate,
                "forecast_rate_usd_ton": predicted_30d_rate,
                "rate_change_pct": predicted_pct_change
            },
            "port_constraints_module": {
                "destination_port": destination,
                "total_vessels_evaluated": len(available_vessels),
                "compatible_vessels_count": len(compatible_vessels),
                "rejections": port_rejections
            },
            "forecast_module": forecast,
            "risk_module": risk,
            "charter_optimization_module": charter_plan,
            "procurement_module": procurement
        }