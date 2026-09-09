from app.ml.predict_forecaster import FreightForecaster
from app.ml.risk_evaluator import RiskEvaluator
from app.optimization.vessel_solver import VesselOptimizationSolver
from app.optimization.procurement_solver import ProcurementOptimizer

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
        """
        Synthesizes Forecast, Risk, Vessel Optimization, and Procurement into an Actionable Decision.
        """
        # Step 1: Run Freight Forecast
        forecast = self.forecaster.predict_30d_rate(
            current_rate=current_freight_rate,
            bunker_fuel=bunker_fuel_price,
            cargo_demand=cargo_demand_index,
            vessel_avail=vessel_availability_index,
            congestion_days=port_congestion_days
        )

        # Step 2: Run Operational Risk Evaluator
        risk = self.risk_evaluator.evaluate_route_risk(
            port_congestion_days=port_congestion_days,
            weather_risk_index=weather_risk_index,
            vessel_availability_index=vessel_availability_index,
            distance_nautical_miles=route_distance_nm
        )

        # Step 3: Solve Vessel Optimization (MILP)
        charter_plan = self.vessel_solver.solve_vessel_chartering(
            cargo_required_tons=cargo_quantity_tons,
            available_vessels=available_vessels,
            route_distance_nm=route_distance_nm,
            fuel_price_usd_ton=bunker_fuel_price,
            delivery_deadline_days=delivery_deadline_days,
            port_congestion_days=port_congestion_days
        )

        # Step 4: Solve Procurement Optimization
        procurement = self.procurement_optimizer.optimize_procurement(
            cargo_required_tons=cargo_quantity_tons,
            ocean_freight_usd_ton=current_freight_rate
        )

        # Step 5: Synthesize Final Business Recommendation
        predicted_pct_increase = forecast["percentage_change"]
        cost_inr_cr = charter_plan.get("total_cost_inr_cr", 0.0)

        # Business Logic Decision Rules
        if predicted_pct_increase > 3.0 and risk["risk_level"] != "HIGH":
            recommended_action = "CHARTER NOW"
            # Estimated savings compared to waiting for rate increase
            estimated_savings_inr_cr = round(cost_inr_cr * (predicted_pct_increase / 100.0), 2)
            reasoning = (
                f"Freight rates are forecast to increase by {predicted_pct_increase}% over the next 30 days. "
                f"Securing vessel capacity today protects against expected rate spikes and saves an estimated ₹{estimated_savings_inr_cr} Cr."
            )
        elif risk["risk_level"] == "HIGH":
            recommended_action = "REROUTE OR WAIT"
            estimated_savings_inr_cr = 0.50
            reasoning = (
                f"Port congestion ({port_congestion_days} days) presents high demurrage risk (Risk Score: {risk['risk_score']}/100). "
                f"Consider staggering shipment or negotiating flexible laytime terms."
            )
        elif predicted_pct_increase < -3.0:
            recommended_action = "WAIT / SPOT MARKET"
            estimated_savings_inr_cr = round(cost_inr_cr * (abs(predicted_pct_increase) / 100.0), 2)
            reasoning = (
                f"Freight rates are forecast to drop by {abs(predicted_pct_increase)}% over the next 30 days. "
                f"Delaying chartering will likely yield lower spot market rates, saving an estimated ₹{estimated_savings_inr_cr} Cr."
            )
        else:
            recommended_action = "EXECUTE STANDARD CHARTER"
            estimated_savings_inr_cr = 0.80
            reasoning = "Market freight rates remain stable. Proceed with standard fleet schedule."

        return {
            "recommended_action": recommended_action,
            "reasoning": reasoning,
            "financial_summary": {
                "total_estimated_cost_inr_cr": cost_inr_cr,
                "estimated_savings_inr_cr": estimated_savings_inr_cr,
                "current_rate_usd_ton": current_freight_rate,
                "forecast_rate_usd_ton": forecast["predicted_30d_rate_usd"],
                "rate_change_pct": predicted_pct_increase
            },
            "forecast_module": forecast,
            "risk_module": risk,
            "charter_optimization_module": charter_plan,
            "procurement_module": procurement
        }