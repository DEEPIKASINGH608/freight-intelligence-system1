class RiskEvaluator:
    def __init__(self):
        pass

    def evaluate_route_risk(
        self,
        port_congestion_days: float,
        weather_risk_index: float,
        vessel_availability_index: float,
        distance_nautical_miles: float
    ) -> dict:
        """
        Computes a composite operational delay and route disruption risk score.
        """
        # 1. Congestion Component (0-100)
        congestion_score = min(100.0, (port_congestion_days / 7.0) * 100.0)

        # 2. Weather Component (0-100)
        weather_score = min(100.0, (weather_risk_index / 2.0) * 100.0)

        # 3. Supply Scarcity Component (0-100)
        supply_scarcity_score = max(0.0, min(100.0, (150.0 - vessel_availability_index)))

        # 4. Distance / Transit Complexity Component
        distance_score = min(100.0, (distance_nautical_miles / 10000.0) * 100.0)

        # Weighted Composite Risk Score Formula
        risk_score = round(
            (congestion_score * 0.40) +
            (weather_score * 0.25) +
            (supply_scarcity_score * 0.20) +
            (distance_score * 0.15),
            1
        )

        # Categorize Risk Level
        if risk_score >= 70.0:
            risk_level = "HIGH"
        elif risk_score >= 40.0:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Generate human-readable risk breakdown explanations
        key_drivers = []
        if port_congestion_days >= 3.0:
            key_drivers.append(f"Severe port congestion ({port_congestion_days} days average waiting time).")
        if weather_risk_index > 1.2:
            key_drivers.append("Elevated seasonal weather/monsoon hazards on transit route.")
        if vessel_availability_index < 85.0:
            key_drivers.append("Tight regional vessel supply increasing charter lead time.")
        if not key_drivers:
            key_drivers.append("Normal operational conditions along designated maritime route.")

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "congestion_days": port_congestion_days,
            "key_drivers": key_drivers,
            "sub_scores": {
                "congestion": round(congestion_score, 1),
                "weather": round(weather_score, 1),
                "supply_scarcity": round(supply_scarcity_score, 1),
                "distance_complexity": round(distance_score, 1)
            }
        }