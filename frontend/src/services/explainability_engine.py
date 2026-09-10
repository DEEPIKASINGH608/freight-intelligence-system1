from typing import Dict, Any, List
import numpy as np

try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False


class ForecastExplainabilityEngine:
    def __init__(self, model=None):
        self.model = model
        self.explainer = None
        if HAS_SHAP and model is not None:
            try:
                self.explainer = shap.TreeExplainer(model)
            except Exception:
                self.explainer = None

    def explain_forecast(
        self,
        input_data: Dict[str, float],
        baseline_rate: float,
        forecasted_rate: float
    ) -> Dict[str, Any]:
        """
        Decomposes the difference between current spot rate and 30-day forecasted rate
        into individual feature contributions.
        """
        total_delta_usd = round(forecasted_rate - baseline_rate, 2)
        total_delta_pct = round((total_delta_usd / baseline_rate) * 100, 2)

        # 1. SHAP TreeExplainer Calculation
        if HAS_SHAP and self.explainer is not None:
            feature_vector = np.array([list(input_data.values())])
            shap_values = self.explainer.shap_values(feature_vector)[0]

            contributions = []
            for feat_name, shap_val in zip(input_data.keys(), shap_values):
                pct_impact = round((shap_val / baseline_rate) * 100, 2)
                contributions.append({
                    "feature": feat_name,
                    "usd_impact": round(float(shap_val), 2),
                    "pct_impact": pct_impact,
                    "direction": "INCREASE" if shap_val >= 0 else "DECREASE"
                })
        else:
            # 2. Rule-Based Fallback Decomposition
            fuel_price = input_data.get("bunker_fuel_price", 620.0)
            weather_risk = input_data.get("weather_risk_index", 1.1)
            congestion = input_data.get("port_congestion_days", 2.5)

            fuel_impact = round(baseline_rate * ((fuel_price - 600) / 10000), 2)
            weather_impact = round(baseline_rate * ((weather_risk - 1.0) * 0.05), 2)
            congestion_impact = round(total_delta_usd - (fuel_impact + weather_impact), 2)

            contributions = [
                {
                    "feature": "Port Congestion Days",
                    "usd_impact": congestion_impact,
                    "pct_impact": round((congestion_impact / baseline_rate) * 100, 2),
                    "direction": "INCREASE" if congestion_impact >= 0 else "DECREASE"
                },
                {
                    "feature": "Bunker Fuel Price",
                    "usd_impact": fuel_impact,
                    "pct_impact": round((fuel_impact / baseline_rate) * 100, 2),
                    "direction": "INCREASE" if fuel_impact >= 0 else "DECREASE"
                },
                {
                    "feature": "Weather Risk Index",
                    "usd_impact": weather_impact,
                    "pct_impact": round((weather_impact / baseline_rate) * 100, 2),
                    "direction": "INCREASE" if weather_impact >= 0 else "DECREASE"
                }
            ]

        return {
            "baseline_spot_rate_usd": baseline_rate,
            "forecasted_30d_rate_usd": forecasted_rate,
            "total_change_usd": total_delta_usd,
            "total_change_pct": total_delta_pct,
            "waterfall_breakdown": contributions,
            "explainability_type": "SHAP_TreeExplainer" if (HAS_SHAP and self.explainer) else "Additive_Decomposition"
        }