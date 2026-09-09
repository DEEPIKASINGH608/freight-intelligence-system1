class ProcurementOptimizer:
    def __init__(self):
        pass

    def optimize_procurement(
        self,
        cargo_required_tons: float,
        ocean_freight_usd_ton: float,
        suppliers: list = None
    ) -> dict:
        """
        Calculates optimal cargo supplier procurement allocation based on total landed cost.
        """
        if not suppliers:
            # Synthetic default regional suppliers
            suppliers = [
                {"name": "Odisha Mining Corp (OMC)", "origin": "Paradip, India", "base_price_usd_ton": 85.0, "purity_pct": 64.0, "available_tons": 150000},
                {"name": "NMDC Limited", "origin": "Vizag, India", "base_price_usd_ton": 88.0, "purity_pct": 65.5, "available_tons": 100000},
                {"name": "Vale Australia", "origin": "Port Hedland, Australia", "base_price_usd_ton": 82.0, "purity_pct": 62.0, "available_tons": 200000}
            ]

        best_supplier = None
        lowest_landed_cost_ton = float("inf")
        procurement_plan = []

        for s in suppliers:
            # Landed cost = Base Commodity Price + Ocean Freight
            landed_cost_ton = s["base_price_usd_ton"] + ocean_freight_usd_ton
            total_procurement_usd = landed_cost_ton * cargo_required_tons

            if landed_cost_ton < lowest_landed_cost_ton:
                lowest_landed_cost_ton = landed_cost_ton
                best_supplier = s

            procurement_plan.append({
                "supplier_name": s["name"],
                "origin": s["origin"],
                "base_price_usd_ton": s["base_price_usd_ton"],
                "ocean_freight_usd_ton": ocean_freight_usd_ton,
                "landed_cost_usd_ton": round(landed_cost_ton, 2),
                "total_cost_inr_cr": round((total_procurement_usd * 83.0) / 10000000.0, 2)
            })

        return {
            "recommended_supplier": best_supplier["name"] if best_supplier else "N/A",
            "recommended_origin": best_supplier["origin"] if best_supplier else "N/A",
            "lowest_landed_cost_usd_ton": round(lowest_landed_cost_ton, 2),
            "total_landed_cost_inr_cr": round(((lowest_landed_cost_ton * cargo_required_tons) * 83.0) / 10000000.0, 2),
            "supplier_options": procurement_plan
        }